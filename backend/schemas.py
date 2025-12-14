"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List


# Trading Signal Schemas
class TradingSignalBase(BaseModel):
    """Base schema for trading signals."""
    ticker: str
    date: date
    signal_type: str
    sentiment_score: Optional[float] = None
    foreign_flow_score: Optional[float] = None
    analyst_action: Optional[str] = None


class TradingSignalCreate(TradingSignalBase):
    """Schema for creating trading signals."""
    recommendation_id: Optional[int] = None


class TradingSignalResponse(TradingSignalBase):
    """Schema for trading signal responses."""
    id: int
    recommendation_id: Optional[int] = None
    
    class Config:
        from_attributes = True


# Sentiment Schemas
class DailySentimentBase(BaseModel):
    """Base schema for daily sentiment."""
    ticker: str
    date: date
    rsi: Optional[float] = None
    bsi: Optional[float] = None
    atr: Optional[float] = None
    ltv: Optional[float] = None
    pli: Optional[float] = None
    raw_sentiment: Optional[float] = None
    pure_sentiment: Optional[float] = None


class DailySentimentResponse(DailySentimentBase):
    """Schema for daily sentiment responses."""
    id: int
    
    class Config:
        from_attributes = True


# Event Study Schemas
class EventStudyResponse(BaseModel):
    """Schema for event study responses."""
    days: List[int]
    car: List[float]
    cas: List[float]


# Settings Schemas
class SettingsBase(BaseModel):
    """Base schema for settings."""
    key: str
    value: str
    category: Optional[str] = None


class SettingsCreate(SettingsBase):
    """Schema for creating settings."""
    pass


class SettingsUpdate(BaseModel):
    """Schema for updating settings."""
    value: str


class SettingsResponse(SettingsBase):
    """Schema for settings responses."""
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SignalThresholdsRequest(BaseModel):
    """Schema for signal thresholds settings."""
    sentiment_min: float = Field(default=1.0)
    rsi_max: float = Field(default=70.0)
    rsi_min: float = Field(default=30.0)
    bsi_min: float = Field(default=0.5)
    bsi_max: float = Field(default=0.8)


class SignalThresholdsResponse(BaseModel):
    """Schema for signal thresholds response."""
    sentiment_min: float
    rsi_max: float
    rsi_min: float
    bsi_min: float
    bsi_max: float


# Watchlist Schemas
class WatchlistBase(BaseModel):
    """Base schema for watchlist."""
    ticker: str


class WatchlistCreate(WatchlistBase):
    """Schema for creating watchlist entries."""
    pass


class WatchlistResponse(WatchlistBase):
    """Schema for watchlist responses."""
    id: int
    added_at: datetime
    
    class Config:
        from_attributes = True


class WatchlistWithSignal(WatchlistResponse):
    """Schema for watchlist with latest signal."""
    latest_signal: Optional[TradingSignalResponse] = None


# Instrument Schemas
class InstrumentResponse(BaseModel):
    """Schema for instrument responses."""
    ticker: str
    name: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Analyst Recommendation Schemas
class AnalystRecommendationResponse(BaseModel):
    """Schema for analyst recommendation responses."""
    id: int
    ticker: str
    analyst_firm: Optional[str] = None
    analyst_name: Optional[str] = None
    recommendation: Optional[str] = None
    rating_numeric: Optional[int] = None
    target_price: Optional[float] = None
    issue_date: date
    
    class Config:
        from_attributes = True


# Pagination
class PaginationParams(BaseModel):
    """Schema for pagination parameters."""
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
