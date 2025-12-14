"""
Data Management router for browsing and managing database contents.
Implements Requirements 2.1, 2.2, 2.3, 2.4, 2.5
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, inspect, desc, asc
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel
import math

from backend.database import get_db
from backend.models import (
    Instrument, MarketData, VNIndex, RiskFreeRate,
    AnalystRecommendation, DailySentiment, TradingSignal
)

# Import DataQualityMetric from src.database
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.database import DataQualityMetric

router = APIRouter(prefix="/data-management", tags=["data-management"])


# Pydantic schemas for data management
class ColumnInfo(BaseModel):
    """Schema for column information."""
    name: str
    display_name: str
    data_type: str
    sortable: bool
    filterable: bool


class TableInfo(BaseModel):
    """Schema for table information."""
    name: str
    display_name: str
    record_count: int
    last_updated: Optional[datetime] = None
    columns: List[ColumnInfo]


class PaginatedResponse(BaseModel):
    """Schema for paginated responses."""
    data: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int
    total_pages: int


class InstrumentDetail(BaseModel):
    """Schema for instrument detail view."""
    ticker: str
    name: Optional[str] = None
    market_data_count: int
    recommendations_count: int
    signals_count: int
    latest_price: Optional[float] = None
    latest_sentiment: Optional[Dict[str, Any]] = None
    recent_signals: List[Dict[str, Any]]


class DataQualityMetricResponse(BaseModel):
    """Schema for data quality metrics."""
    table_name: str
    display_name: str
    total_records: int
    completeness_pct: float
    anomaly_count: int
    last_updated: Optional[datetime] = None


# Table metadata configuration
TABLE_CONFIG = {
    "instruments": {
        "display_name": "Instruments",
        "model": Instrument,
        "columns": [
            {"name": "ticker", "display_name": "Ticker", "data_type": "string", "sortable": True, "filterable": True},
            {"name": "name", "display_name": "Name", "data_type": "string", "sortable": True, "filterable": True},
            {"name": "created_at", "display_name": "Created At", "data_type": "datetime", "sortable": True, "filterable": False},
        ]
    },
    "market_data": {
        "display_name": "Market Data",
        "model": MarketData,
        "columns": [
            {"name": "id", "display_name": "ID", "data_type": "integer", "sortable": True, "filterable": False},
            {"name": "ticker", "display_name": "Ticker", "data_type": "string", "sortable": True, "filterable": True},
            {"name": "date", "display_name": "Date", "data_type": "date", "sortable": True, "filterable": True},
            {"name": "close_price", "display_name": "Close Price", "data_type": "float", "sortable": True, "filterable": False},
            {"name": "buy_volume", "display_name": "Buy Volume", "data_type": "integer", "sortable": True, "filterable": False},
            {"name": "sell_volume", "display_name": "Sell Volume", "data_type": "integer", "sortable": True, "filterable": False},
            {"name": "total_volume", "display_name": "Total Volume", "data_type": "integer", "sortable": True, "filterable": False},
            {"name": "shares_outstanding", "display_name": "Shares Outstanding", "data_type": "integer", "sortable": True, "filterable": False},
        ]
    },
    "analyst_recommendations": {
        "display_name": "Recommendations",
        "model": AnalystRecommendation,
        "columns": [
            {"name": "id", "display_name": "ID", "data_type": "integer", "sortable": True, "filterable": False},
            {"name": "ticker", "display_name": "Ticker", "data_type": "string", "sortable": True, "filterable": True},
            {"name": "analyst_firm", "display_name": "Analyst Firm", "data_type": "string", "sortable": True, "filterable": True},
            {"name": "analyst_name", "display_name": "Analyst Name", "data_type": "string", "sortable": True, "filterable": True},
            {"name": "recommendation", "display_name": "Recommendation", "data_type": "string", "sortable": True, "filterable": True},
            {"name": "rating_numeric", "display_name": "Rating (1-5)", "data_type": "integer", "sortable": True, "filterable": True},
            {"name": "target_price", "display_name": "Target Price", "data_type": "float", "sortable": True, "filterable": False},
            {"name": "issue_date", "display_name": "Issue Date", "data_type": "date", "sortable": True, "filterable": True},
        ]
    },
    "daily_sentiment": {
        "display_name": "Sentiment",
        "model": DailySentiment,
        "columns": [
            {"name": "id", "display_name": "ID", "data_type": "integer", "sortable": True, "filterable": False},
            {"name": "ticker", "display_name": "Ticker", "data_type": "string", "sortable": True, "filterable": True},
            {"name": "date", "display_name": "Date", "data_type": "date", "sortable": True, "filterable": True},
            {"name": "rsi", "display_name": "RSI", "data_type": "float", "sortable": True, "filterable": False},
            {"name": "bsi", "display_name": "BSI", "data_type": "float", "sortable": True, "filterable": False},
            {"name": "atr", "display_name": "ATR", "data_type": "float", "sortable": True, "filterable": False},
            {"name": "ltv", "display_name": "LTV", "data_type": "float", "sortable": True, "filterable": False},
            {"name": "pli", "display_name": "PLI", "data_type": "float", "sortable": True, "filterable": False},
            {"name": "raw_sentiment", "display_name": "Raw Sentiment", "data_type": "float", "sortable": True, "filterable": False},
            {"name": "pure_sentiment", "display_name": "Pure Sentiment", "data_type": "float", "sortable": True, "filterable": False},
        ]
    },
    "trading_signals": {
        "display_name": "Signals",
        "model": TradingSignal,
        "columns": [
            {"name": "id", "display_name": "ID", "data_type": "integer", "sortable": True, "filterable": False},
            {"name": "ticker", "display_name": "Ticker", "data_type": "string", "sortable": True, "filterable": True},
            {"name": "date", "display_name": "Date", "data_type": "date", "sortable": True, "filterable": True},
            {"name": "signal_type", "display_name": "Signal Type", "data_type": "string", "sortable": True, "filterable": True},
            {"name": "sentiment_score", "display_name": "Sentiment Score", "data_type": "float", "sortable": True, "filterable": False},
            {"name": "foreign_flow_score", "display_name": "Foreign Flow Score", "data_type": "float", "sortable": True, "filterable": False},
            {"name": "analyst_action", "display_name": "Analyst Action", "data_type": "string", "sortable": True, "filterable": True},
        ]
    },
    "vnindex": {
        "display_name": "VNIndex",
        "model": VNIndex,
        "columns": [
            {"name": "date", "display_name": "Date", "data_type": "date", "sortable": True, "filterable": True},
            {"name": "close_index", "display_name": "Close Index", "data_type": "float", "sortable": True, "filterable": False},
            {"name": "buy_volume", "display_name": "Buy Volume", "data_type": "integer", "sortable": True, "filterable": False},
            {"name": "sell_volume", "display_name": "Sell Volume", "data_type": "integer", "sortable": True, "filterable": False},
            {"name": "total_volume", "display_name": "Total Volume", "data_type": "integer", "sortable": True, "filterable": False},
        ]
    },
    "risk_free_rate": {
        "display_name": "Risk-Free Rate",
        "model": RiskFreeRate,
        "columns": [
            {"name": "date", "display_name": "Date", "data_type": "date", "sortable": True, "filterable": True},
            {"name": "rate", "display_name": "Rate (%)", "data_type": "float", "sortable": True, "filterable": False},
        ]
    },
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


@router.get("/tables", response_model=List[TableInfo])
def list_tables(db: Session = Depends(get_db)) -> List[TableInfo]:
    """
    List all data tables with record counts.
    
    Implements Requirement 2.1: Display a tabbed interface for each data table.
    
    Returns:
        List of table information including name, display name, record count, and columns.
    """
    tables = []
    
    for table_name, config in TABLE_CONFIG.items():
        model = config["model"]
        
        # Get record count
        record_count = db.query(func.count()).select_from(model).scalar() or 0
        
        # Build column info
        columns = [ColumnInfo(**col) for col in config["columns"]]
        
        tables.append(TableInfo(
            name=table_name,
            display_name=config["display_name"],
            record_count=record_count,
            last_updated=None,  # Could be enhanced to track last update time
            columns=columns
        ))
    
    return tables


@router.get("/tables/{table_name}", response_model=PaginatedResponse)
def get_table_data(
    table_name: str,
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=50, ge=1, le=100, description="Records per page"),
    sort_by: Optional[str] = Query(default=None, description="Column to sort by"),
    sort_order: str = Query(default="desc", regex="^(asc|desc)$", description="Sort order"),
    ticker: Optional[str] = Query(default=None, description="Filter by ticker"),
    start_date: Optional[date] = Query(default=None, description="Filter from date"),
    end_date: Optional[date] = Query(default=None, description="Filter to date"),
    signal_type: Optional[str] = Query(default=None, description="Filter by signal type"),
    recommendation: Optional[str] = Query(default=None, description="Filter by recommendation"),
    db: Session = Depends(get_db)
) -> PaginatedResponse:
    """
    Get paginated, sortable, filterable table data.
    
    Implements Requirements 2.2, 2.3:
    - 2.2: Display records in a paginated, sortable table
    - 2.3: Provide search and filter capabilities
    
    Args:
        table_name: Name of the table to query
        page: Page number (1-indexed)
        page_size: Number of records per page
        sort_by: Column name to sort by
        sort_order: Sort direction ('asc' or 'desc')
        ticker: Filter by ticker symbol
        start_date: Filter records from this date
        end_date: Filter records up to this date
        signal_type: Filter by signal type (for trading_signals table)
        recommendation: Filter by recommendation text (for analyst_recommendations table)
        
    Returns:
        Paginated response with data, total count, and pagination metadata.
        
    Raises:
        HTTPException: 404 if table not found, 422 if invalid parameters
    """
    if table_name not in TABLE_CONFIG:
        raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
    
    config = TABLE_CONFIG[table_name]
    model = config["model"]
    
    # Build base query
    query = db.query(model)
    
    # Apply filters based on table type
    if ticker:
        ticker_upper = ticker.upper()
        if hasattr(model, 'ticker'):
            query = query.filter(model.ticker == ticker_upper)
    
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
    
    if signal_type and hasattr(model, 'signal_type'):
        query = query.filter(model.signal_type == signal_type)
    
    if recommendation and hasattr(model, 'recommendation'):
        query = query.filter(model.recommendation.ilike(f"%{recommendation}%"))
    
    # Apply sorting BEFORE counting for better performance
    if sort_by:
        # Validate sort column exists
        valid_columns = [col["name"] for col in config["columns"] if col["sortable"]]
        if sort_by not in valid_columns:
            raise HTTPException(
                status_code=422, 
                detail=f"Invalid sort column '{sort_by}'. Valid columns: {valid_columns}"
            )
        
        sort_column = getattr(model, sort_by)
        if sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
    else:
        # Default sorting
        if hasattr(model, 'date'):
            query = query.order_by(desc(model.date))
        elif hasattr(model, 'issue_date'):
            query = query.order_by(desc(model.issue_date))
        elif hasattr(model, 'id'):
            query = query.order_by(desc(model.id))
    
    # Get total count - use func.count() for better performance
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    offset = (page - 1) * page_size
    
    # Limit maximum page size to prevent memory issues
    if page_size > 100:
        page_size = 100
    
    # Apply pagination with LIMIT to prevent loading entire table
    records = query.offset(offset).limit(page_size).all()
    
    # Convert to dictionaries - process in batches to avoid memory spike
    data = []
    for record in records:
        data.append(model_to_dict(record))
    
    # Clear records from memory
    records = None
    
    return PaginatedResponse(
        data=data,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )



@router.get("/instruments/{ticker}", response_model=InstrumentDetail)
def get_instrument_detail(
    ticker: str,
    db: Session = Depends(get_db)
) -> InstrumentDetail:
    """
    Get instrument detail view with related market data, recommendations, and signals.
    
    Implements Requirements 2.4, 2.5:
    - 2.4: Display a detail view with related market data, recommendations, and signals
    - 2.5: Display both the original rating text and the standardized numeric rating
    
    Args:
        ticker: Ticker symbol
        
    Returns:
        Instrument detail with counts and recent data.
        
    Raises:
        HTTPException: 404 if ticker not found
    """
    ticker_upper = ticker.upper()
    
    # Get instrument
    instrument = db.query(Instrument).filter(Instrument.ticker == ticker_upper).first()
    if not instrument:
        raise HTTPException(status_code=404, detail=f"Ticker '{ticker}' not found")
    
    # Get counts
    market_data_count = db.query(func.count()).select_from(MarketData).filter(
        MarketData.ticker == ticker_upper
    ).scalar() or 0
    
    recommendations_count = db.query(func.count()).select_from(AnalystRecommendation).filter(
        AnalystRecommendation.ticker == ticker_upper
    ).scalar() or 0
    
    signals_count = db.query(func.count()).select_from(TradingSignal).filter(
        TradingSignal.ticker == ticker_upper
    ).scalar() or 0
    
    # Get latest price
    latest_market_data = db.query(MarketData).filter(
        MarketData.ticker == ticker_upper
    ).order_by(desc(MarketData.date)).first()
    
    latest_price = latest_market_data.close_price if latest_market_data else None
    
    # Get latest sentiment
    latest_sentiment_record = db.query(DailySentiment).filter(
        DailySentiment.ticker == ticker_upper
    ).order_by(desc(DailySentiment.date)).first()
    
    latest_sentiment = model_to_dict(latest_sentiment_record) if latest_sentiment_record else None
    
    # Get recent signals (last 10)
    recent_signals_records = db.query(TradingSignal).filter(
        TradingSignal.ticker == ticker_upper
    ).order_by(desc(TradingSignal.date)).limit(10).all()
    
    recent_signals = [model_to_dict(s) for s in recent_signals_records]
    
    return InstrumentDetail(
        ticker=instrument.ticker,
        name=instrument.name,
        market_data_count=market_data_count,
        recommendations_count=recommendations_count,
        signals_count=signals_count,
        latest_price=latest_price,
        latest_sentiment=latest_sentiment,
        recent_signals=recent_signals
    )


@router.get("/quality", response_model=List[DataQualityMetricResponse])
def get_data_quality(db: Session = Depends(get_db)) -> List[DataQualityMetricResponse]:
    """
    Get data quality metrics for all tables.
    
    Implements Requirement 7.6: Show a data quality dashboard with completeness metrics per table.
    
    Returns:
        List of data quality metrics for each table.
    """
    quality_metrics = []
    
    # Define tables to check quality for
    tables_to_check = [
        ("instruments", "Instruments", Instrument, ["ticker"]),
        ("market_data", "Market Data", MarketData, ["ticker", "date", "close_price"]),
        ("analyst_recommendations", "Recommendations", AnalystRecommendation, ["ticker", "recommendation", "issue_date"]),
        ("daily_sentiment", "Sentiment", DailySentiment, ["ticker", "date"]),
        ("trading_signals", "Signals", TradingSignal, ["ticker", "date", "signal_type"]),
        ("vnindex", "VNIndex", VNIndex, ["date", "close_index"]),
        ("risk_free_rate", "Risk-Free Rate", RiskFreeRate, ["date", "rate"]),
    ]
    
    for table_name, display_name, model, critical_fields in tables_to_check:
        # Get total records
        total_records = db.query(func.count()).select_from(model).scalar() or 0
        
        if total_records == 0:
            quality_metrics.append(DataQualityMetricResponse(
                table_name=table_name,
                display_name=display_name,
                total_records=0,
                completeness_pct=100.0,
                anomaly_count=0,
                last_updated=None
            ))
            continue
        
        # Count records with null critical fields (anomalies)
        anomaly_count = 0
        for field_name in critical_fields:
            if hasattr(model, field_name):
                field = getattr(model, field_name)
                null_count = db.query(func.count()).select_from(model).filter(
                    field.is_(None)
                ).scalar() or 0
                anomaly_count += null_count
        
        # Calculate completeness percentage
        # Total possible values = total_records * number of critical fields
        total_possible = total_records * len(critical_fields)
        completeness_pct = ((total_possible - anomaly_count) / total_possible * 100) if total_possible > 0 else 100.0
        
        # Get last updated from stored metrics if available
        stored_metric = db.query(DataQualityMetric).filter(
            DataQualityMetric.table_name == table_name
        ).order_by(desc(DataQualityMetric.updated_at)).first()
        
        last_updated = stored_metric.updated_at if stored_metric else None
        
        quality_metrics.append(DataQualityMetricResponse(
            table_name=table_name,
            display_name=display_name,
            total_records=total_records,
            completeness_pct=round(completeness_pct, 2),
            anomaly_count=anomaly_count,
            last_updated=last_updated
        ))
    
    return quality_metrics
