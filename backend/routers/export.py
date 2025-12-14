"""
Export router for data export endpoints.
Implements Requirements 6.1, 6.2, 6.3, 6.4
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import inspect, desc
from typing import Optional, Dict, Any, List
from datetime import date, datetime, timedelta
import io
import csv
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from backend.database import get_db
from backend.models import (
    TradingSignal, Instrument, MarketData, VNIndex, RiskFreeRate,
    AnalystRecommendation, DailySentiment
)
from src.event_study_analyzer import EventStudyAnalyzer
import pandas as pd

router = APIRouter(prefix="/export", tags=["export"])

# Table model mapping
TABLE_MODELS = {
    "instruments": Instrument,
    "market_data": MarketData,
    "vnindex": VNIndex,
    "risk_free_rate": RiskFreeRate,
    "analyst_recommendations": AnalystRecommendation,
    "daily_sentiment": DailySentiment,
    "trading_signals": TradingSignal,
}


def model_to_dict(obj) -> Dict[str, Any]:
    """Convert SQLAlchemy model instance to dictionary."""
    result = {}
    for column in inspect(obj.__class__).columns:
        value = getattr(obj, column.name)
        # Convert date/datetime to ISO format string
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        result[column.name] = value
    return result


def get_column_names(model) -> List[str]:
    """Get column names from SQLAlchemy model."""
    return [column.name for column in inspect(model).columns]


def records_to_csv(records: List[Any], columns: List[str]) -> str:
    """Convert list of records to CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(columns)
    
    # Write data rows
    for record in records:
        row = []
        for col in columns:
            value = getattr(record, col, None)
            if isinstance(value, (date, datetime)):
                value = value.isoformat()
            elif value is None:
                value = ''
            row.append(value)
        writer.writerow(row)
    
    output.seek(0)
    return output.getvalue()


@router.get("/daily_signals.csv")
def export_daily_signals(
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    signal_type: Optional[str] = Query(default=None),
    db: Session = Depends(get_db)
) -> StreamingResponse:
    """
    Export trading signals as CSV file (legacy endpoint).
    
    Args:
        start_date: Filter signals from this date onwards
        end_date: Filter signals up to this date
        signal_type: Filter by signal type
        db: Database session
        
    Returns:
        CSV file as streaming response
    """
    # Build query
    query = db.query(TradingSignal)
    
    # Apply filters
    if start_date:
        query = query.filter(TradingSignal.date >= start_date)
    
    if end_date:
        query = query.filter(TradingSignal.date <= end_date)
    
    if signal_type:
        query = query.filter(TradingSignal.signal_type == signal_type)
    
    # Order by date descending
    query = query.order_by(TradingSignal.date.desc())
    
    # Get all signals
    signals = query.all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'id',
        'ticker',
        'date',
        'signal_type',
        'sentiment_score',
        'foreign_flow_score',
        'analyst_action',
        'recommendation_id'
    ])
    
    # Write data rows
    for signal in signals:
        writer.writerow([
            signal.id,
            signal.ticker,
            signal.date.isoformat() if signal.date else '',
            signal.signal_type,
            signal.sentiment_score if signal.sentiment_score is not None else '',
            signal.foreign_flow_score if signal.foreign_flow_score is not None else '',
            signal.analyst_action if signal.analyst_action else '',
            signal.recommendation_id if signal.recommendation_id is not None else ''
        ])
    
    # Prepare response
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=daily_signals.csv"
        }
    )


@router.get("/{table_name}.csv")
def export_table_csv(
    table_name: str,
    ticker: Optional[str] = Query(default=None, description="Filter by ticker"),
    start_date: Optional[date] = Query(default=None, description="Filter from date"),
    end_date: Optional[date] = Query(default=None, description="Filter to date"),
    db: Session = Depends(get_db)
) -> StreamingResponse:
    """
    Export table data as CSV file.
    
    Implements Requirement 6.1: Support CSV format for all data tables.
    
    Args:
        table_name: Name of the table to export
        ticker: Optional ticker filter
        start_date: Optional start date filter
        end_date: Optional end date filter
        db: Database session
        
    Returns:
        CSV file as streaming response
        
    Raises:
        HTTPException: 404 if table not found
    """
    if table_name not in TABLE_MODELS:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
    model = TABLE_MODELS[table_name]
    query = db.query(model)
    
    # Apply filters
    if ticker and hasattr(model, 'ticker'):
        query = query.filter(model.ticker == ticker.upper())
    
    if start_date:
        if hasattr(model, 'date'):
            query = query.filter(model.date >= start_date)
        elif hasattr(model, 'issue_date'):
            query = query.filter(model.issue_date >= start_date)
    
    if end_date:
        if hasattr(model, 'date'):
            query = query.filter(model.date <= end_date)
        elif hasattr(model, 'issue_date'):
            query = query.filter(model.issue_date <= end_date)
    
    # Order by date if available
    if hasattr(model, 'date'):
        query = query.order_by(desc(model.date))
    elif hasattr(model, 'issue_date'):
        query = query.order_by(desc(model.issue_date))
    
    records = query.all()
    columns = get_column_names(model)
    csv_content = records_to_csv(records, columns)
    
    return StreamingResponse(
        iter([csv_content]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={table_name}.csv"
        }
    )


@router.get("/{table_name}.json")
def export_table_json(
    table_name: str,
    ticker: Optional[str] = Query(default=None, description="Filter by ticker"),
    start_date: Optional[date] = Query(default=None, description="Filter from date"),
    end_date: Optional[date] = Query(default=None, description="Filter to date"),
    db: Session = Depends(get_db)
) -> JSONResponse:
    """
    Export table data as JSON file.
    
    Implements Requirement 6.1: Support JSON format for all data tables.
    
    Args:
        table_name: Name of the table to export
        ticker: Optional ticker filter
        start_date: Optional start date filter
        end_date: Optional end date filter
        db: Database session
        
    Returns:
        JSON response with table data
        
    Raises:
        HTTPException: 404 if table not found
    """
    if table_name not in TABLE_MODELS:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
    model = TABLE_MODELS[table_name]
    query = db.query(model)
    
    # Apply filters
    if ticker and hasattr(model, 'ticker'):
        query = query.filter(model.ticker == ticker.upper())
    
    if start_date:
        if hasattr(model, 'date'):
            query = query.filter(model.date >= start_date)
        elif hasattr(model, 'issue_date'):
            query = query.filter(model.issue_date >= start_date)
    
    if end_date:
        if hasattr(model, 'date'):
            query = query.filter(model.date <= end_date)
        elif hasattr(model, 'issue_date'):
            query = query.filter(model.issue_date <= end_date)
    
    # Order by date if available
    if hasattr(model, 'date'):
        query = query.order_by(desc(model.date))
    elif hasattr(model, 'issue_date'):
        query = query.order_by(desc(model.issue_date))
    
    records = query.all()
    data = [model_to_dict(record) for record in records]
    
    return JSONResponse(
        content={"table": table_name, "count": len(data), "data": data},
        headers={
            "Content-Disposition": f"attachment; filename={table_name}.json"
        }
    )



@router.get("/signals/full.csv")
def export_signals_full(
    start_date: Optional[date] = Query(default=None, description="Filter from date"),
    end_date: Optional[date] = Query(default=None, description="Filter to date"),
    ticker: Optional[str] = Query(default=None, description="Filter by ticker"),
    signal_type: Optional[str] = Query(default=None, description="Filter by signal type"),
    db: Session = Depends(get_db)
) -> StreamingResponse:
    """
    Export signals with related recommendation and sentiment data.
    
    Implements Requirement 6.2: Export signals with all signal fields plus 
    related recommendation and sentiment data.
    
    Args:
        start_date: Optional start date filter
        end_date: Optional end date filter
        ticker: Optional ticker filter
        signal_type: Optional signal type filter
        db: Database session
        
    Returns:
        CSV file with full signal data including related recommendation and sentiment
    """
    # Build query with joins
    query = db.query(TradingSignal)
    
    # Apply filters
    if ticker:
        query = query.filter(TradingSignal.ticker == ticker.upper())
    
    if start_date:
        query = query.filter(TradingSignal.date >= start_date)
    
    if end_date:
        query = query.filter(TradingSignal.date <= end_date)
    
    if signal_type:
        query = query.filter(TradingSignal.signal_type == signal_type)
    
    # Order by date descending
    query = query.order_by(desc(TradingSignal.date))
    
    signals = query.all()
    
    # Create CSV with full data
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header with all fields
    writer.writerow([
        'id',
        'ticker',
        'date',
        'signal_type',
        'sentiment_score',
        'foreign_flow_score',
        'analyst_action',
        'recommendation_id',
        # Related recommendation fields
        'recommendation_text',
        'rating_numeric',
        'analyst_firm',
        'analyst_name',
        'target_price',
        'issue_date',
        # Related sentiment fields
        'rsi',
        'bsi',
        'atr',
        'ltv',
        'pli',
        'raw_sentiment',
        'pure_sentiment'
    ])
    
    # Write data rows with related data
    for signal in signals:
        # Get related recommendation
        rec = None
        if signal.recommendation_id:
            rec = db.query(AnalystRecommendation).filter(
                AnalystRecommendation.id == signal.recommendation_id
            ).first()
        
        # Get related sentiment for the same ticker and date
        sentiment = db.query(DailySentiment).filter(
            DailySentiment.ticker == signal.ticker,
            DailySentiment.date == signal.date
        ).first()
        
        writer.writerow([
            signal.id,
            signal.ticker,
            signal.date.isoformat() if signal.date else '',
            signal.signal_type or '',
            signal.sentiment_score if signal.sentiment_score is not None else '',
            signal.foreign_flow_score if signal.foreign_flow_score is not None else '',
            signal.analyst_action or '',
            signal.recommendation_id if signal.recommendation_id is not None else '',
            # Recommendation fields
            rec.recommendation if rec else '',
            rec.rating_numeric if rec else '',
            rec.analyst_firm if rec else '',
            rec.analyst_name if rec else '',
            rec.target_price if rec else '',
            rec.issue_date.isoformat() if rec and rec.issue_date else '',
            # Sentiment fields
            sentiment.rsi if sentiment else '',
            sentiment.bsi if sentiment else '',
            sentiment.atr if sentiment else '',
            sentiment.ltv if sentiment else '',
            sentiment.pli if sentiment else '',
            sentiment.raw_sentiment if sentiment else '',
            sentiment.pure_sentiment if sentiment else ''
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=signals_full.csv"
        }
    )


@router.get("/event-study/{ticker}/{event_date}")
def export_event_study(
    ticker: str,
    event_date: date,
    format: str = Query(default="csv", regex="^(csv|json)$", description="Export format"),
    window_before: int = Query(default=25, ge=1, le=50, description="Days before event"),
    window_after: int = Query(default=25, ge=1, le=50, description="Days after event"),
    db: Session = Depends(get_db)
):
    """
    Export full CAR/CAS time series for event study.
    
    Implements Requirement 6.4: Export the full CAR and CAS time series 
    for the event window.
    
    Args:
        ticker: Ticker symbol
        event_date: Event date (analyst recommendation date)
        format: Export format ('csv' or 'json')
        window_before: Number of days before event (default: 25)
        window_after: Number of days after event (default: 25)
        db: Database session
        
    Returns:
        CSV or JSON file with CAR and CAS time series
        
    Raises:
        HTTPException: 404 if ticker not found or insufficient data
    """
    ticker_upper = ticker.upper()
    
    # Check if instrument exists
    instrument = db.query(Instrument).filter(Instrument.ticker == ticker_upper).first()
    if not instrument:
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found")
    
    # Calculate date range for event window
    start_date_range = event_date - timedelta(days=window_before + 30)
    end_date_range = event_date + timedelta(days=window_after + 10)
    
    # Get market data for the ticker
    market_data = (
        db.query(MarketData)
        .filter(
            MarketData.ticker == ticker_upper,
            MarketData.date >= start_date_range,
            MarketData.date <= end_date_range
        )
        .order_by(MarketData.date.asc())
        .all()
    )
    
    if not market_data:
        raise HTTPException(
            status_code=404,
            detail=f"No market data found for {ticker} around {event_date}"
        )
    
    # Get VNIndex data for market returns
    vnindex_data = (
        db.query(VNIndex)
        .filter(
            VNIndex.date >= start_date_range,
            VNIndex.date <= end_date_range
        )
        .order_by(VNIndex.date.asc())
        .all()
    )
    
    if not vnindex_data:
        raise HTTPException(
            status_code=404,
            detail="No VNIndex data found for the specified period"
        )
    
    # Get sentiment data
    sentiment_data = (
        db.query(DailySentiment)
        .filter(
            DailySentiment.ticker == ticker_upper,
            DailySentiment.date >= start_date_range,
            DailySentiment.date <= end_date_range
        )
        .order_by(DailySentiment.date.asc())
        .all()
    )
    
    if not sentiment_data:
        raise HTTPException(
            status_code=404,
            detail=f"No sentiment data found for {ticker} around {event_date}"
        )
    
    # Convert to DataFrames
    market_df = pd.DataFrame([
        {'date': md.date, 'close_price': md.close_price}
        for md in market_data
    ])
    
    vnindex_df = pd.DataFrame([
        {'date': vn.date, 'close_index': vn.close_index}
        for vn in vnindex_data
    ])
    
    sentiment_df = pd.DataFrame([
        {'date': s.date, 'pure_sentiment': s.pure_sentiment}
        for s in sentiment_data
    ])
    
    # Calculate returns
    market_df['return'] = market_df['close_price'].pct_change()
    vnindex_df['market_return'] = vnindex_df['close_index'].pct_change()
    
    # Merge data
    merged_df = market_df.merge(vnindex_df, on='date', how='inner')
    merged_df = merged_df.merge(sentiment_df, on='date', how='inner')
    
    # Use EventStudyAnalyzer
    analyzer = EventStudyAnalyzer()
    
    try:
        # Calculate abnormal returns
        abnormal_returns = analyzer.calculate_abnormal_returns(
            merged_df.set_index('date')['return'],
            merged_df.set_index('date')['market_return']
        )
        
        # Calculate CAR
        car_df = analyzer.calculate_car(
            abnormal_returns,
            event_date,
            window=(-window_before, window_after)
        )
        
        # Calculate CAS
        cas_df = analyzer.calculate_cas(
            merged_df.set_index('date')['pure_sentiment'],
            event_date,
            window=(-window_before, window_after)
        )
        
        if car_df.empty or cas_df.empty:
            raise HTTPException(
                status_code=404,
                detail="Insufficient data to calculate event study metrics"
            )
        
        # Merge CAR and CAS
        # Both DataFrames have 'day' column, merge on that
        result_df = car_df.merge(cas_df, on='day', how='outer').sort_values('day')
        
        if format == "json":
            data = {
                "ticker": ticker_upper,
                "event_date": event_date.isoformat(),
                "window": {"before": window_before, "after": window_after},
                "data_points": len(result_df),
                "data": [
                    {
                        "day": int(row['day']),
                        "car": float(row['car']) if pd.notna(row.get('car')) else None,
                        "cas": float(row['cas']) if pd.notna(row.get('cas')) else None
                    }
                    for _, row in result_df.iterrows()
                ]
            }
            return JSONResponse(
                content=data,
                headers={
                    "Content-Disposition": f"attachment; filename=event_study_{ticker_upper}_{event_date}.json"
                }
            )
        else:
            # CSV format
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow(['day', 'car', 'cas'])
            
            # Write data rows
            for _, row in result_df.iterrows():
                writer.writerow([
                    int(row['day']),
                    row['car'] if pd.notna(row.get('car')) else '',
                    row['cas'] if pd.notna(row.get('cas')) else ''
                ])
            
            output.seek(0)
            
            return StreamingResponse(
                iter([output.getvalue()]),
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename=event_study_{ticker_upper}_{event_date}.csv"
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating event study: {str(e)}"
        )


@router.get("/daily-report")
def generate_daily_report(
    report_date: Optional[date] = Query(default=None, description="Report date (defaults to today)"),
    db: Session = Depends(get_db)
) -> JSONResponse:
    """
    Generate daily summary report.
    
    Implements Requirement 6.3: Generate a summary of new signals, 
    top movers, and sentiment changes.
    
    Args:
        report_date: Date for the report (defaults to today)
        db: Database session
        
    Returns:
        JSON response with daily report data
    """
    if report_date is None:
        report_date = date.today()
    
    # Get new signals for the date
    new_signals = db.query(TradingSignal).filter(
        TradingSignal.date == report_date
    ).order_by(desc(TradingSignal.sentiment_score)).all()
    
    # Get top movers (stocks with highest absolute sentiment change)
    # Compare sentiment from report_date vs previous day
    previous_date = report_date - timedelta(days=1)
    
    # Get sentiment for report date
    current_sentiment = db.query(DailySentiment).filter(
        DailySentiment.date == report_date
    ).all()
    
    # Get sentiment for previous date
    previous_sentiment = db.query(DailySentiment).filter(
        DailySentiment.date == previous_date
    ).all()
    
    # Calculate sentiment changes
    prev_sentiment_map = {s.ticker: s.pure_sentiment for s in previous_sentiment}
    
    sentiment_changes = []
    for curr in current_sentiment:
        prev_value = prev_sentiment_map.get(curr.ticker)
        if prev_value is not None and curr.pure_sentiment is not None:
            change = curr.pure_sentiment - prev_value
            sentiment_changes.append({
                "ticker": curr.ticker,
                "previous_sentiment": prev_value,
                "current_sentiment": curr.pure_sentiment,
                "change": change,
                "change_pct": (change / abs(prev_value) * 100) if prev_value != 0 else 0
            })
    
    # Sort by absolute change
    sentiment_changes.sort(key=lambda x: abs(x["change"]), reverse=True)
    top_movers = sentiment_changes[:10]  # Top 10 movers
    
    # Get market data for top movers to include price info
    top_movers_with_price = []
    for mover in top_movers:
        market_data = db.query(MarketData).filter(
            MarketData.ticker == mover["ticker"],
            MarketData.date == report_date
        ).first()
        
        mover_data = {
            **mover,
            "close_price": market_data.close_price if market_data else None,
            "total_volume": market_data.total_volume if market_data else None
        }
        top_movers_with_price.append(mover_data)
    
    # Build report
    report = {
        "report_date": report_date.isoformat(),
        "new_signals_count": len(new_signals),
        "new_signals": [
            {
                "id": s.id,
                "ticker": s.ticker,
                "signal_type": s.signal_type,
                "sentiment_score": s.sentiment_score,
                "foreign_flow_score": s.foreign_flow_score,
                "analyst_action": s.analyst_action
            }
            for s in new_signals
        ],
        "top_movers": top_movers_with_price,
        "sentiment_changes_count": len(sentiment_changes),
        "sentiment_changes": sentiment_changes[:20]  # Top 20 changes
    }
    
    return JSONResponse(content=report)
