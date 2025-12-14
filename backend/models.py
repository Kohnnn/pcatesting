"""
SQLAlchemy ORM models for FastAPI backend.
Re-exports models from src.database for use in FastAPI.
"""
import sys
import os

# Add src to path to import models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import (
    Base,
    Instrument,
    MarketData,
    VNIndex,
    RiskFreeRate,
    AnalystRecommendation,
    DailySentiment,
    TradingSignal,
    Settings,
    Watchlist
)

__all__ = [
    'Base',
    'Instrument',
    'MarketData',
    'VNIndex',
    'RiskFreeRate',
    'AnalystRecommendation',
    'DailySentiment',
    'TradingSignal',
    'Settings',
    'Watchlist'
]
