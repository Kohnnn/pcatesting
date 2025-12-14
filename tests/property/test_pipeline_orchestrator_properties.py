"""
Property-based tests for PipelineOrchestrator.

**Feature: data-management-refactor**
"""
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from hypothesis import given, strategies as st, settings, assume
import pandas as pd
import numpy as np

from database import DatabaseManager, MarketData, PipelineRun
from pipeline_orchestrator import PipelineOrchestrator, ProcessingResult, PipelineReport


class TestPipelineOrchestratorProperties:
    """Property-based tests for PipelineOrchestrator."""
    
    @settings(max_examples=100, deadline=None)
    @given(
        n_existing=st.integers(min_value=5, max_value=20),
        n_new=st.integers(min_value=1, max_value=10),
        n_tickers=st.integers(min_value=1, max_value=3),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_incremental_update_correctness(self, n_existing, n_new, n_tickers, seed):
        """
        **Feature: data-management-refactor, Property 3: Incremental Update Correctness**
        **Validates: Requirements 1.6**
        
        For any database with existing data up to date D, running the pipeline
        with new data should only insert records with dates > D, and existing
        records should remain unchanged.
        """
        np.random.seed(seed)
        
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            db = DatabaseManager(db_path)
            db.create_tables()
            
            # Generate existing data
            start_date = pd.Timestamp('2024-01-01')
            existing_dates = pd.date_range(start=start_date, periods=n_existing, freq='D')
            tickers = [f"T{i:02d}" for i in range(n_tickers)]
            
            existing_data = []
            for date in existing_dates:
                for ticker in tickers:
                    existing_data.append({
                        'date': date,
                        'ticker': ticker,
                        'close_price': np.random.uniform(1000, 50000),
                        'buy_volume': int(np.random.uniform(1000, 100000)),
                        'sell_volume': int(np.random.uniform(1000, 100000)),
                        'total_volume': int(np.random.uniform(2000, 200000)),
                        'shares_outstanding': int(np.random.uniform(1000000, 10000000))
                    })
            
            existing_df = pd.DataFrame(existing_data)
            
            # Insert existing data
            count1 = db.upsert_market_data(existing_df)
            assert count1 == len(existing_data), "Initial insert should insert all records"
            
            # Store original values for comparison
            session = db.Session()
            original_records = {}
            try:
                for record in session.query(MarketData).all():
                    key = (record.ticker, record.date)
                    original_records[key] = {
                        'close_price': record.close_price,
                        'buy_volume': record.buy_volume,
                        'sell_volume': record.sell_volume,
                        'total_volume': record.total_volume,
                        'shares_outstanding': record.shares_outstanding
                    }
            finally:
                session.close()
            
            # Get latest date
            latest_date = db.get_latest_date('market_data')
            assert latest_date == existing_dates[-1].date(), "Latest date should match last inserted date"
            
            # Generate new data (dates after latest_date)
            new_start_date = existing_dates[-1] + pd.Timedelta(days=1)
            new_dates = pd.date_range(start=new_start_date, periods=n_new, freq='D')
            
            new_data = []
            for date in new_dates:
                for ticker in tickers:
                    new_data.append({
                        'date': date,
                        'ticker': ticker,
                        'close_price': np.random.uniform(1000, 50000),
                        'buy_volume': int(np.random.uniform(1000, 100000)),
                        'sell_volume': int(np.random.uniform(1000, 100000)),
                        'total_volume': int(np.random.uniform(2000, 200000)),
                        'shares_outstanding': int(np.random.uniform(1000000, 10000000))
                    })
            
            new_df = pd.DataFrame(new_data)
            
            # Insert new data (incremental update)
            count2 = db.upsert_market_data(new_df)
            
            # Check that only new records were inserted
            assert count2 == len(new_data), \
                f"Incremental update should insert {len(new_data)} new records, but inserted {count2}"
            
            # Verify existing records are unchanged
            session = db.Session()
            try:
                for record in session.query(MarketData).all():
                    key = (record.ticker, record.date)
                    if key in original_records:
                        orig = original_records[key]
                        assert np.isclose(record.close_price, orig['close_price'], rtol=1e-9), \
                            f"Existing record {key} close_price was modified"
                        assert record.buy_volume == orig['buy_volume'], \
                            f"Existing record {key} buy_volume was modified"
                        assert record.sell_volume == orig['sell_volume'], \
                            f"Existing record {key} sell_volume was modified"
            finally:
                session.close()
            
            # Verify latest date is updated
            latest_date_after = db.get_latest_date('market_data')
            assert latest_date_after == new_dates[-1].date(), \
                "Latest date should be updated to the last new date"
            
            # Try inserting existing data again (should not insert new records)
            count3 = db.upsert_market_data(existing_df)
            assert count3 == 0, "Re-inserting existing data should not create new records"
            
        finally:
            # Close database connections
            db.engine.dispose()
            
            # Clean up temporary database
            if os.path.exists(db_path):
                try:
                    os.unlink(db_path)
                except PermissionError:
                    pass
