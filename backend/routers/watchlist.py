"""
Watchlist router for portfolio watchlist endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import Watchlist, Instrument, TradingSignal
from backend.schemas import (
    WatchlistCreate,
    WatchlistResponse,
    WatchlistWithSignal
)

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.get("", response_model=List[WatchlistWithSignal])
def get_watchlist(db: Session = Depends(get_db)) -> List[dict]:
    """
    Get all watchlist entries with their latest signals.
    
    Args:
        db: Database session
        
    Returns:
        List of watchlist entries with latest signal information
    """
    watchlist_items = db.query(Watchlist).order_by(Watchlist.added_at.desc()).all()
    
    result = []
    for item in watchlist_items:
        # Get latest signal for this ticker
        latest_signal = (
            db.query(TradingSignal)
            .filter(TradingSignal.ticker == item.ticker)
            .order_by(TradingSignal.date.desc())
            .first()
        )
        
        result.append({
            'id': item.id,
            'ticker': item.ticker,
            'added_at': item.added_at,
            'latest_signal': latest_signal
        })
    
    return result


@router.post("", response_model=WatchlistResponse, status_code=status.HTTP_201_CREATED)
def add_to_watchlist(
    watchlist_item: WatchlistCreate,
    db: Session = Depends(get_db)
) -> Watchlist:
    """
    Add a ticker to the watchlist.
    
    Args:
        watchlist_item: Watchlist entry to create
        db: Database session
        
    Returns:
        Created watchlist entry
        
    Raises:
        HTTPException: 404 if ticker not found
        HTTPException: 409 if ticker already in watchlist
    """
    # Check if instrument exists
    instrument = db.query(Instrument).filter(
        Instrument.ticker == watchlist_item.ticker.upper()
    ).first()
    
    if not instrument:
        raise HTTPException(
            status_code=404,
            detail=f"Ticker {watchlist_item.ticker} not found"
        )
    
    # Check if already in watchlist
    existing = db.query(Watchlist).filter(
        Watchlist.ticker == watchlist_item.ticker.upper()
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Ticker {watchlist_item.ticker} already in watchlist"
        )
    
    # Create new watchlist entry
    new_item = Watchlist(ticker=watchlist_item.ticker.upper())
    db.add(new_item)
    
    try:
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add to watchlist: {str(e)}"
        )


@router.delete("/{watchlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_watchlist(
    watchlist_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Remove a ticker from the watchlist.
    
    Args:
        watchlist_id: ID of watchlist entry to delete
        db: Database session
        
    Raises:
        HTTPException: 404 if watchlist entry not found
    """
    watchlist_item = db.query(Watchlist).filter(Watchlist.id == watchlist_id).first()
    
    if not watchlist_item:
        raise HTTPException(
            status_code=404,
            detail=f"Watchlist entry {watchlist_id} not found"
        )
    
    try:
        db.delete(watchlist_item)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to remove from watchlist: {str(e)}"
        )
