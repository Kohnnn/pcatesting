"""
Property-based tests for data pipeline components.

**Feature: sentimentalpha-vietnam**
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from hypothesis import given, strategies as st, assume, settings
import pandas as pd
import numpy as np
from data_transformer import DataTransformer


class TestDataPipelineProperties:
    """Property-based tests for data pipeline."""
    
    @settings(max_examples=100)
    @given(
        n_tickers=st.integers(min_value=1, max_value=20),
        n_dates=st.integers(min_value=1, max_value=50),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_wide_to_long_round_trip(self, n_tickers, n_dates, seed):
        """
        **Feature: sentimentalpha-vietnam, Property 1: Wide-to-Long Transformation Round Trip**
        **Validates: Requirements 1.3**
        
        For any valid wide-format DataFrame with N tickers and M dates,
        melting to long format and pivoting back should produce an equivalent DataFrame.
        """
        np.random.seed(seed)
        
        # Generate random dates
        start_date = pd.Timestamp('2020-01-01')
        dates = pd.date_range(start=start_date, periods=n_dates, freq='D')
        
        # Generate random ticker names
        tickers = [f"TICK{i:03d}" for i in range(n_tickers)]
        
        # Generate random price data (positive values)
        data = np.random.uniform(1000, 50000, size=(n_dates, n_tickers))
        
        # Create wide-format DataFrame
        wide_df = pd.DataFrame(data, columns=tickers)
        wide_df.insert(0, 'Date', dates)
        
        # Transform to long format
        transformer = DataTransformer()
        long_df = transformer.melt_wide_to_long(wide_df, 'value')
        
        # Pivot back to wide format
        pivoted = long_df.pivot(index='date', columns='ticker', values='value')
        pivoted = pivoted.reset_index()
        pivoted.columns.name = None
        
        # Sort columns for comparison
        original_cols = sorted([col for col in wide_df.columns if col != 'Date'])
        pivoted_cols = sorted([col for col in pivoted.columns if col != 'date'])
        
        # Check that we have the same tickers
        assert original_cols == pivoted_cols, "Ticker columns don't match after round trip"
        
        # Check that we have the same number of dates
        assert len(wide_df) == len(pivoted), "Number of dates doesn't match after round trip"
        
        # Check values are approximately equal (accounting for floating point)
        for ticker in tickers:
            original_values = wide_df[ticker].values
            pivoted_values = pivoted[ticker].values
            
            # Use numpy's allclose for floating point comparison
            assert np.allclose(original_values, pivoted_values, rtol=1e-9, atol=1e-9), \
                f"Values for {ticker} don't match after round trip"
    
    @settings(max_examples=100)
    @given(
        rating=st.sampled_from([
            'buy', 'strong buy', 'outperform',
            'accumulate', 'overweight',
            'hold', 'market perform', 'neutral',
            'reduce', 'underweight',
            'sell', 'strong sell', 'underperform',
            # Test case variations
            'BUY', 'Buy', 'SELL', 'Sell', 'HOLD', 'Hold',
            '  buy  ', '  sell  ', '  hold  '  # with whitespace
        ])
    )
    def test_rating_standardization_range(self, rating):
        """
        **Feature: sentimentalpha-vietnam, Property 2: Rating Standardization Range**
        **Validates: Requirements 1.5**
        
        For any valid recommendation rating string (buy, sell, hold, outperform, 
        underperform, etc.), the standardized numeric rating should be in the range [1, 5].
        """
        transformer = DataTransformer()
        
        # Standardize the rating
        numeric_rating = transformer.standardize_rating(rating)
        
        # Check that rating is in valid range
        assert 1 <= numeric_rating <= 5, \
            f"Rating '{rating}' standardized to {numeric_rating}, which is outside [1, 5]"
        
        # Check that rating is an integer
        assert isinstance(numeric_rating, int), \
            f"Rating '{rating}' standardized to {numeric_rating}, which is not an integer"
    
    @settings(max_examples=100, deadline=None)
    @given(
        n_existing=st.integers(min_value=5, max_value=30),
        n_new=st.integers(min_value=1, max_value=20),
        n_tickers=st.integers(min_value=1, max_value=5),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_incremental_update_correctness(self, n_existing, n_new, n_tickers, seed):
        """
        **Feature: sentimentalpha-vietnam, Property 3: Incremental Update Correctness**
        **Validates: Requirements 1.10**
        
        For any database with existing data up to date D, running incremental update 
        with new data should only insert records with dates > D.
        """
        import tempfile
        import os
        from database import DatabaseManager
        
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
            tickers = [f"TICK{i:03d}" for i in range(n_tickers)]
            
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
                    # On Windows, sometimes the file is still locked
                    pass
    
    @settings(max_examples=100, deadline=None)
    @given(
        n_rows=st.integers(min_value=10, max_value=100),
        n_tickers=st.integers(min_value=1, max_value=10),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_data_persistence_round_trip(self, n_rows, n_tickers, seed):
        """
        **Feature: sentimentalpha-vietnam, Property 4: Data Persistence Round Trip**
        **Validates: Requirements 1.9**
        
        For any DataFrame saved to SQLite/Parquet, reading it back should produce 
        an equivalent DataFrame (within floating-point tolerance).
        """
        import tempfile
        import os
        from database import DatabaseManager
        from sqlalchemy import select
        from database import MarketData
        
        np.random.seed(seed)
        
        # Generate test data
        start_date = pd.Timestamp('2024-01-01')
        dates = pd.date_range(start=start_date, periods=n_rows, freq='D')
        tickers = [f"TICK{i:03d}" for i in range(n_tickers)]
        
        data = []
        for date in dates:
            for ticker in tickers:
                data.append({
                    'date': date,
                    'ticker': ticker,
                    'close_price': np.random.uniform(1000, 50000),
                    'buy_volume': int(np.random.uniform(1000, 100000)),
                    'sell_volume': int(np.random.uniform(1000, 100000)),
                    'total_volume': int(np.random.uniform(2000, 200000)),
                    'shares_outstanding': int(np.random.uniform(1000000, 10000000))
                })
        
        original_df = pd.DataFrame(data)
        
        # Test SQLite round trip
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            db = DatabaseManager(db_path)
            db.create_tables()
            
            # Write to database
            db.upsert_market_data(original_df)
            
            # Read back from database
            session = db.Session()
            try:
                query = select(MarketData)
                results = session.execute(query).scalars().all()
                
                read_data = []
                for row in results:
                    read_data.append({
                        'date': pd.Timestamp(row.date),
                        'ticker': row.ticker,
                        'close_price': row.close_price,
                        'buy_volume': row.buy_volume,
                        'sell_volume': row.sell_volume,
                        'total_volume': row.total_volume,
                        'shares_outstanding': row.shares_outstanding
                    })
                
                read_df = pd.DataFrame(read_data)
                read_df = read_df.sort_values(['date', 'ticker']).reset_index(drop=True)
                original_sorted = original_df.sort_values(['date', 'ticker']).reset_index(drop=True)
                
                # Check that we have the same number of rows
                assert len(read_df) == len(original_sorted), \
                    f"SQLite round trip: Expected {len(original_sorted)} rows, got {len(read_df)}"
                
                # Check that tickers match
                assert list(read_df['ticker']) == list(original_sorted['ticker']), \
                    "SQLite round trip: Tickers don't match"
                
                # Check that dates match
                assert list(read_df['date']) == list(original_sorted['date']), \
                    "SQLite round trip: Dates don't match"
                
                # Check numeric values (with floating point tolerance)
                for col in ['close_price', 'buy_volume', 'sell_volume', 'total_volume', 'shares_outstanding']:
                    assert np.allclose(read_df[col], original_sorted[col], rtol=1e-9, atol=1e-9), \
                        f"SQLite round trip: {col} values don't match"
                
            finally:
                session.close()
                db.engine.dispose()
        
        finally:
            if os.path.exists(db_path):
                try:
                    os.unlink(db_path)
                except PermissionError:
                    pass
        
        # Test Parquet round trip
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp:
            parquet_path = tmp.name
        
        try:
            # Write to Parquet
            original_df.to_parquet(parquet_path, index=False)
            
            # Read back from Parquet
            read_df = pd.read_parquet(parquet_path)
            read_df = read_df.sort_values(['date', 'ticker']).reset_index(drop=True)
            original_sorted = original_df.sort_values(['date', 'ticker']).reset_index(drop=True)
            
            # Check that we have the same number of rows
            assert len(read_df) == len(original_sorted), \
                f"Parquet round trip: Expected {len(original_sorted)} rows, got {len(read_df)}"
            
            # Check that tickers match
            assert list(read_df['ticker']) == list(original_sorted['ticker']), \
                "Parquet round trip: Tickers don't match"
            
            # Check numeric values (with floating point tolerance)
            for col in ['close_price', 'buy_volume', 'sell_volume', 'total_volume', 'shares_outstanding']:
                assert np.allclose(read_df[col], original_sorted[col], rtol=1e-9, atol=1e-9), \
                    f"Parquet round trip: {col} values don't match"
        
        finally:
            if os.path.exists(parquet_path):
                try:
                    os.unlink(parquet_path)
                except PermissionError:
                    pass
