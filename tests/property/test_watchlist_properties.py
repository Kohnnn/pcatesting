"""
Property-based tests for watchlist operations.

**Feature: sentimentalpha-vietnam, Property 16: Watchlist Add-Contains**
**Validates: Requirements 9.2, 9.3**
"""
from hypothesis import given, strategies as st, settings
import pytest
import sys
import os
import tempfile

# Add src and backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.database import DatabaseManager, Watchlist as WatchlistModel, Instrument


class TestWatchlistProperties:
    """Property-based tests for watchlist operations."""
    
    @given(
        ticker=st.text(
            min_size=1,
            max_size=10,
            alphabet=st.characters(whitelist_categories=('Lu',), min_codepoint=65, max_codepoint=90)
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_watchlist_add_contains(self, ticker):
        """
        **Feature: sentimentalpha-vietnam, Property 16: Watchlist Add-Contains**
        **Validates: Requirements 9.2, 9.3**
        
        For any ticker added to the watchlist,
        querying the watchlist should include that ticker.
        """
        # Create temporary database for this test
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        db_manager = DatabaseManager(db_path)
        db_manager.create_tables()
        session = db_manager.Session()
        
        try:
            # First, create the instrument
            instrument = Instrument(ticker=ticker, name=f"Test Company {ticker}")
            session.add(instrument)
            session.commit()
            
            # Add ticker to watchlist
            watchlist_item = WatchlistModel(ticker=ticker)
            session.add(watchlist_item)
            session.commit()
            
            # Query watchlist
            watchlist_entries = session.query(WatchlistModel).all()
            watchlist_tickers = [entry.ticker for entry in watchlist_entries]
            
            # Verify ticker is in watchlist
            assert ticker in watchlist_tickers, \
                f"Ticker {ticker} not found in watchlist after adding"
        
        finally:
            session.close()
            # Close all connections
            db_manager.engine.dispose()
            # Clean up temporary database
            try:
                if os.path.exists(db_path):
                    os.unlink(db_path)
            except PermissionError:
                # On Windows, file might still be locked
                pass
    
    @given(
        tickers=st.lists(
            st.text(
                min_size=1,
                max_size=10,
                alphabet=st.characters(whitelist_categories=('Lu',), min_codepoint=65, max_codepoint=90)
            ),
            min_size=1,
            max_size=10,
            unique=True
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_watchlist_multiple_add_all_present(self, tickers):
        """
        For any list of tickers added to the watchlist,
        all tickers should be present when querying the watchlist.
        """
        # Create temporary database for this test
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        db_manager = DatabaseManager(db_path)
        db_manager.create_tables()
        session = db_manager.Session()
        
        try:
            # Create instruments and add to watchlist
            for ticker in tickers:
                # Create instrument
                instrument = Instrument(ticker=ticker, name=f"Test Company {ticker}")
                session.add(instrument)
                
                # Add to watchlist
                watchlist_item = WatchlistModel(ticker=ticker)
                session.add(watchlist_item)
            
            session.commit()
            
            # Query watchlist
            watchlist_entries = session.query(WatchlistModel).all()
            watchlist_tickers = set(entry.ticker for entry in watchlist_entries)
            
            # Verify all tickers are in watchlist
            for ticker in tickers:
                assert ticker in watchlist_tickers, \
                    f"Ticker {ticker} not found in watchlist after adding"
            
            # Verify count matches
            assert len(watchlist_tickers) == len(tickers), \
                f"Watchlist count mismatch: expected {len(tickers)}, got {len(watchlist_tickers)}"
        
        finally:
            session.close()
            # Close all connections
            db_manager.engine.dispose()
            # Clean up temporary database
            try:
                if os.path.exists(db_path):
                    os.unlink(db_path)
            except PermissionError:
                # On Windows, file might still be locked
                pass
    
    @given(
        ticker=st.text(
            min_size=1,
            max_size=10,
            alphabet=st.characters(whitelist_categories=('Lu',), min_codepoint=65, max_codepoint=90)
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_watchlist_add_remove_not_present(self, ticker):
        """
        For any ticker added then removed from the watchlist,
        the ticker should not be present when querying the watchlist.
        """
        # Create temporary database for this test
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        db_manager = DatabaseManager(db_path)
        db_manager.create_tables()
        session = db_manager.Session()
        
        try:
            # Create instrument
            instrument = Instrument(ticker=ticker, name=f"Test Company {ticker}")
            session.add(instrument)
            session.commit()
            
            # Add to watchlist
            watchlist_item = WatchlistModel(ticker=ticker)
            session.add(watchlist_item)
            session.commit()
            
            # Verify it's there
            entry = session.query(WatchlistModel).filter(WatchlistModel.ticker == ticker).first()
            assert entry is not None, f"Ticker {ticker} not found after adding"
            
            # Remove from watchlist
            session.delete(entry)
            session.commit()
            
            # Query watchlist
            watchlist_entries = session.query(WatchlistModel).all()
            watchlist_tickers = [entry.ticker for entry in watchlist_entries]
            
            # Verify ticker is not in watchlist
            assert ticker not in watchlist_tickers, \
                f"Ticker {ticker} still in watchlist after removal"
        
        finally:
            session.close()
            # Close all connections
            db_manager.engine.dispose()
            # Clean up temporary database
            try:
                if os.path.exists(db_path):
                    os.unlink(db_path)
            except PermissionError:
                # On Windows, file might still be locked
                pass
