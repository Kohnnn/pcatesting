"""
Event study router for CAR/CAS analysis endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from backend.database import get_db
from backend.models import Instrument, MarketData, DailySentiment, VNIndex
from backend.schemas import EventStudyResponse
from src.event_study_analyzer import EventStudyAnalyzer

router = APIRouter(prefix="/event-study", tags=["event-study"])


@router.get("/{ticker}/{event_date}", response_model=EventStudyResponse)
def get_event_study(
    ticker: str,
    event_date: date,
    window_before: int = 25,
    window_after: int = 25,
    db: Session = Depends(get_db)
) -> EventStudyResponse:
    """
    Get CAR and CAS event study data for a specific ticker and event date.
    
    Args:
        ticker: Ticker symbol
        event_date: Event date (analyst recommendation date)
        window_before: Number of days before event (default: 25)
        window_after: Number of days after event (default: 25)
        db: Database session
        
    Returns:
        Event study data with days, CAR, and CAS arrays
        
    Raises:
        HTTPException: 404 if ticker not found or insufficient data
    """
    # Check if instrument exists
    instrument = db.query(Instrument).filter(Instrument.ticker == ticker.upper()).first()
    if not instrument:
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found")
    
    # Calculate date range for event window
    start_date = event_date - timedelta(days=window_before + 30)  # Extra buffer for estimation
    end_date = event_date + timedelta(days=window_after + 10)
    
    # Get market data for the ticker
    market_data = (
        db.query(MarketData)
        .filter(
            MarketData.ticker == ticker.upper(),
            MarketData.date >= start_date,
            MarketData.date <= end_date
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
            VNIndex.date >= start_date,
            VNIndex.date <= end_date
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
            DailySentiment.ticker == ticker.upper(),
            DailySentiment.date >= start_date,
            DailySentiment.date <= end_date
        )
        .order_by(DailySentiment.date.asc())
        .all()
    )
    
    if not sentiment_data:
        raise HTTPException(
            status_code=404,
            detail=f"No sentiment data found for {ticker} around {event_date}"
        )
    
    # Convert to dictionaries for easier processing
    import pandas as pd
    
    market_df = pd.DataFrame([
        {
            'date': md.date,
            'close_price': md.close_price
        }
        for md in market_data
    ])
    
    vnindex_df = pd.DataFrame([
        {
            'date': vn.date,
            'close_index': vn.close_index
        }
        for vn in vnindex_data
    ])
    
    sentiment_df = pd.DataFrame([
        {
            'date': s.date,
            'pure_sentiment': s.pure_sentiment
        }
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
        
        # Prepare response
        if car_df.empty or cas_df.empty:
            raise HTTPException(
                status_code=404,
                detail="Insufficient data to calculate event study metrics"
            )
        
        # Merge CAR and CAS on day
        result_df = car_df.merge(cas_df, left_index=True, right_index=True, how='inner')
        
        return EventStudyResponse(
            days=result_df.index.tolist(),
            car=result_df['car'].tolist(),
            cas=result_df['cas'].tolist()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating event study: {str(e)}"
        )
