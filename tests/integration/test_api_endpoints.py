"""
Integration tests for FastAPI endpoints.
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os
import tempfile
from datetime import date, datetime

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from backend.main import app
from backend.database import SessionLocal, engine
from backend.models import (
    Base, Instrument, TradingSignal, DailySentiment,
    MarketData, VNIndex, Settings, Watchlist
)


@pytest.fixture(scope="function")
def test_client():
    """Create a test client with a fresh database."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create test client
    client = TestClient(app)
    
    yield client
    
    # Clean up
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a database session for test data setup."""
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def sample_data(db_session):
    """Create sample data for testing."""
    # Create instruments
    instruments = [
        Instrument(ticker="AAA", name="Test Company A"),
        Instrument(ticker="BBB", name="Test Company B"),
        Instrument(ticker="CCC", name="Test Company C")
    ]
    for inst in instruments:
        db_session.add(inst)
    
    # Create trading signals
    signals = [
        TradingSignal(
            ticker="AAA",
            date=date(2024, 1, 15),
            signal_type="Contrarian Dip Buy",
            sentiment_score=1.5,
            foreign_flow_score=0.8,
            analyst_action="Downgrade"
        ),
        TradingSignal(
            ticker="BBB",
            date=date(2024, 1, 16),
            signal_type="Momentum Breakout",
            sentiment_score=0.9,
            foreign_flow_score=0.6,
            analyst_action="Upgrade"
        )
    ]
    for signal in signals:
        db_session.add(signal)
    
    # Create sentiment data
    sentiment_data = [
        DailySentiment(
            ticker="AAA",
            date=date(2024, 1, 15),
            rsi=45.5,
            bsi=0.6,
            atr=2.3,
            ltv=15.2,
            pli=0.7,
            raw_sentiment=0.5,
            pure_sentiment=1.2
        )
    ]
    for sent in sentiment_data:
        db_session.add(sent)
    
    # Create market data
    market_data = [
        MarketData(
            ticker="AAA",
            date=date(2024, 1, 15),
            close_price=100.0,
            buy_volume=1000000,
            sell_volume=800000,
            total_volume=1800000,
            shares_outstanding=10000000
        )
    ]
    for md in market_data:
        db_session.add(md)
    
    # Create VNIndex data
    vnindex_data = [
        VNIndex(
            date=date(2024, 1, 15),
            close_index=1200.5,
            buy_volume=5000000,
            sell_volume=4500000,
            total_volume=9500000
        )
    ]
    for vn in vnindex_data:
        db_session.add(vn)
    
    db_session.commit()
    
    return {
        'instruments': instruments,
        'signals': signals,
        'sentiment': sentiment_data,
        'market_data': market_data,
        'vnindex': vnindex_data
    }


class TestSignalsEndpoints:
    """Test signals router endpoints."""
    
    def test_get_signals_returns_list(self, test_client, sample_data):
        """GET /signals should return a list of signals."""
        response = test_client.get("/signals")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_signals_pagination(self, test_client, sample_data):
        """GET /signals should support pagination."""
        response = test_client.get("/signals?limit=1&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 1
    
    def test_get_signals_by_ticker(self, test_client, sample_data):
        """GET /signals/{ticker} should return signals for specific ticker."""
        response = test_client.get("/signals/AAA")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert data[0]['ticker'] == "AAA"
    
    def test_get_signals_ticker_not_found(self, test_client, sample_data):
        """GET /signals/{ticker} should return 404 for non-existent ticker."""
        response = test_client.get("/signals/NONEXISTENT")
        assert response.status_code == 404


class TestSentimentEndpoints:
    """Test sentiment router endpoints."""
    
    def test_get_sentiment_history(self, test_client, sample_data):
        """GET /sentiment/{ticker} should return sentiment history."""
        response = test_client.get("/sentiment/AAA")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Check structure
        assert 'rsi' in data[0]
        assert 'bsi' in data[0]
        assert 'pure_sentiment' in data[0]
    
    def test_get_sentiment_ticker_not_found(self, test_client, sample_data):
        """GET /sentiment/{ticker} should return 404 for non-existent ticker."""
        response = test_client.get("/sentiment/NONEXISTENT")
        assert response.status_code == 404


class TestSettingsEndpoints:
    """Test settings router endpoints."""
    
    def test_get_settings_returns_defaults(self, test_client):
        """GET /settings should return default settings."""
        response = test_client.get("/settings")
        assert response.status_code == 200
        data = response.json()
        assert 'sentiment_min' in data
        assert 'rsi_max' in data
        assert 'rsi_min' in data
        assert 'bsi_min' in data
        assert 'bsi_max' in data
    
    def test_post_settings_updates_values(self, test_client):
        """POST /settings should update settings."""
        new_settings = {
            'sentiment_min': 1.5,
            'rsi_max': 75.0,
            'rsi_min': 25.0,
            'bsi_min': 0.4,
            'bsi_max': 0.9
        }
        response = test_client.post("/settings", json=new_settings)
        assert response.status_code == 200
        data = response.json()
        assert data['sentiment_min'] == 1.5
        assert data['rsi_max'] == 75.0


class TestWatchlistEndpoints:
    """Test watchlist router endpoints."""
    
    def test_get_watchlist_empty(self, test_client, sample_data):
        """GET /watchlist should return empty list initially."""
        response = test_client.get("/watchlist")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_post_watchlist_adds_ticker(self, test_client, sample_data):
        """POST /watchlist should add ticker to watchlist."""
        response = test_client.post("/watchlist", json={"ticker": "AAA"})
        assert response.status_code == 201
        data = response.json()
        assert data['ticker'] == "AAA"
    
    def test_post_watchlist_duplicate_returns_409(self, test_client, sample_data):
        """POST /watchlist should return 409 for duplicate ticker."""
        # Add first time
        test_client.post("/watchlist", json={"ticker": "AAA"})
        # Try to add again
        response = test_client.post("/watchlist", json={"ticker": "AAA"})
        assert response.status_code == 409
    
    def test_delete_watchlist_removes_ticker(self, test_client, sample_data):
        """DELETE /watchlist/{id} should remove ticker from watchlist."""
        # Add ticker
        add_response = test_client.post("/watchlist", json={"ticker": "AAA"})
        watchlist_id = add_response.json()['id']
        
        # Delete ticker
        delete_response = test_client.delete(f"/watchlist/{watchlist_id}")
        assert delete_response.status_code == 204


class TestExportEndpoints:
    """Test export router endpoints."""
    
    def test_export_daily_signals_csv(self, test_client, sample_data):
        """GET /export/daily_signals.csv should return CSV file."""
        response = test_client.get("/export/daily_signals.csv")
        assert response.status_code == 200
        assert response.headers['content-type'] == 'text/csv; charset=utf-8'
        assert 'Content-Disposition' in response.headers
        # Check CSV content
        content = response.text
        assert 'ticker' in content
        assert 'signal_type' in content


class TestHealthEndpoints:
    """Test health and root endpoints."""
    
    def test_root_endpoint(self, test_client):
        """GET / should return API information."""
        response = test_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert 'message' in data
        assert 'version' in data
    
    def test_health_check(self, test_client):
        """GET /health should return healthy status."""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
