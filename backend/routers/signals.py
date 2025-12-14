"""
Signals router for trading signals endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from backend.database import get_db
from backend.models import TradingSignal, Instrument
from backend.schemas import TradingSignalResponse

router = APIRouter(prefix="/signals", tags=["signals"])


@router.get("", response_model=List[TradingSignalResponse])
def get_signals(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    ticker: Optional[str] = Query(default=None),
    signal_type: Optional[str] = Query(default=None),
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    db: Session = Depends(get_db)
) -> List[TradingSignal]:
    """
    Get list of trading signals with pagination and filtering.
    
    Args:
        limit: Maximum number of results to return (1-100)
        offset: Number of results to skip
        ticker: Filter by ticker symbol
        signal_type: Filter by signal type
        start_date: Filter signals from this date onwards
        end_date: Filter signals up to this date
        db: Database session
        
    Returns:
        List of trading signals
    """
    query = db.query(TradingSignal)
    
    # Apply filters
    if ticker:
        query = query.filter(TradingSignal.ticker == ticker.upper())
    
    if signal_type:
        query = query.filter(TradingSignal.signal_type == signal_type)
    
    if start_date:
        query = query.filter(TradingSignal.date >= start_date)
    
    if end_date:
        query = query.filter(TradingSignal.date <= end_date)
    
    # Order by date descending (most recent first)
    query = query.order_by(TradingSignal.date.desc())
    
    # Apply pagination
    signals = query.offset(offset).limit(limit).all()
    
    return signals


@router.get("/{ticker}", response_model=List[TradingSignalResponse])
def get_signals_by_ticker(
    ticker: str,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
) -> List[TradingSignal]:
    """
    Get detailed signal information for a specific ticker.
    
    Args:
        ticker: Ticker symbol
        limit: Maximum number of results to return
        offset: Number of results to skip
        db: Database session
        
    Returns:
        List of trading signals for the ticker
        
    Raises:
        HTTPException: 404 if ticker not found
    """
    # Check if instrument exists
    instrument = db.query(Instrument).filter(Instrument.ticker == ticker.upper()).first()
    if not instrument:
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found")
    
    # Get signals for this ticker
    signals = (
        db.query(TradingSignal)
        .filter(TradingSignal.ticker == ticker.upper())
        .order_by(TradingSignal.date.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    
    return signals
