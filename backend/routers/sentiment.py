"""
Sentiment router for sentiment history endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from backend.database import get_db
from backend.models import DailySentiment, Instrument
from backend.schemas import DailySentimentResponse

router = APIRouter(prefix="/sentiment", tags=["sentiment"])


@router.get("/{ticker}", response_model=List[DailySentimentResponse])
def get_sentiment_history(
    ticker: str,
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
) -> List[DailySentiment]:
    """
    Get sentiment history for a specific ticker.
    
    Args:
        ticker: Ticker symbol
        start_date: Filter sentiment from this date onwards
        end_date: Filter sentiment up to this date
        limit: Maximum number of results to return (1-500)
        offset: Number of results to skip
        db: Database session
        
    Returns:
        List of daily sentiment records including all proxy values
        
    Raises:
        HTTPException: 404 if ticker not found
    """
    # Check if instrument exists
    instrument = db.query(Instrument).filter(Instrument.ticker == ticker.upper()).first()
    if not instrument:
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found")
    
    # Build query
    query = db.query(DailySentiment).filter(DailySentiment.ticker == ticker.upper())
    
    # Apply date filters
    if start_date:
        query = query.filter(DailySentiment.date >= start_date)
    
    if end_date:
        query = query.filter(DailySentiment.date <= end_date)
    
    # Order by date ascending (chronological order for charts)
    query = query.order_by(DailySentiment.date.asc())
    
    # Apply pagination
    sentiment_data = query.offset(offset).limit(limit).all()
    
    if not sentiment_data:
        raise HTTPException(
            status_code=404, 
            detail=f"No sentiment data found for ticker {ticker}"
        )
    
    return sentiment_data
