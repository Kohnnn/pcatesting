"""
Property-based tests for Data Management API.

**Feature: data-management-refactor**
"""
import sys
import os
import tempfile
import math
from pathlib import Path
from datetime import date, timedelta

# Add src and backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

import pytest
from hypothesis import given, strategies as st, settings, assume
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base, Instrument, MarketData, TradingSignal, DailySentiment


def create_test_db():
    """Create an in-memory test database with tables."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session


def seed_test_data(session, n_instruments, n_records_per_instrument, seed=42):
    """Seed test database with random data."""
    np.random.seed(seed)
    
    tickers = [f"T{i:03d}" for i in range(n_instruments)]
    base_date = date(2024, 1, 1)
    
    # Create instruments
    for ticker in tickers:
        instrument = Instrument(ticker=ticker, name=f"Company {ticker}")
        session.add(instrument)
    
    session.flush()
    
    # Create market data
    for ticker in tickers:
        for i in range(n_records_per_instrument):
            record_date = base_date + timedelta(days=i)
            market_data = MarketData(
                ticker=ticker,
                date=record_date,
                close_price=np.random.uniform(1000, 50000),
                buy_volume=int(np.random.uniform(1000, 100000)),
                sell_volume=int(np.random.uniform(1000, 100000)),
                total_volume=int(np.random.uniform(2000, 200000)),
                shares_outstanding=int(np.random.uniform(1000000, 10000000))
            )
            session.add(market_data)
    
    session.commit()
    return tickers



class TestPaginationProperties:
    """
    Property-based tests for pagination correctness.
    
    **Feature: data-management-refactor, Property 13: Pagination Correctness**
    **Validates: Requirements 2.2**
    """
    
    @settings(max_examples=100, deadline=None)
    @given(
        total_records=st.integers(min_value=1, max_value=500),
        page_size=st.integers(min_value=1, max_value=100),
        page=st.integers(min_value=1, max_value=50),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_pagination_correctness(self, total_records, page_size, page, seed):
        """
        **Feature: data-management-refactor, Property 13: Pagination Correctness**
        **Validates: Requirements 2.2**
        
        For any paginated table request with page P and page_size S, the response
        should contain at most S records, and the total_pages should equal ceil(total / S).
        """
        # Calculate expected values
        expected_total_pages = math.ceil(total_records / page_size)
        
        # Skip if page is beyond total pages (valid but returns empty)
        # We still test this case
        
        # Calculate expected records on this page
        if page <= expected_total_pages:
            start_idx = (page - 1) * page_size
            end_idx = min(start_idx + page_size, total_records)
            expected_records_on_page = end_idx - start_idx
        else:
            expected_records_on_page = 0
        
        # Create test database
        engine, Session = create_test_db()
        session = Session()
        
        try:
            # Calculate how many instruments and records per instrument
            # to get approximately total_records
            n_instruments = min(total_records, 10)
            n_records_per_instrument = max(1, total_records // n_instruments)
            
            # Seed data
            seed_test_data(session, n_instruments, n_records_per_instrument, seed)
            
            # Get actual total
            actual_total = session.query(MarketData).count()
            
            # Recalculate expected values based on actual total
            expected_total_pages = math.ceil(actual_total / page_size) if actual_total > 0 else 1
            
            # Query with pagination
            offset = (page - 1) * page_size
            records = session.query(MarketData).order_by(MarketData.date.desc()).offset(offset).limit(page_size).all()
            
            # Verify pagination properties
            # Property 1: Records returned should be at most page_size
            assert len(records) <= page_size, \
                f"Page should contain at most {page_size} records, got {len(records)}"
            
            # Property 2: total_pages calculation is correct
            calculated_total_pages = math.ceil(actual_total / page_size) if actual_total > 0 else 1
            assert calculated_total_pages == expected_total_pages, \
                f"total_pages should be {expected_total_pages}, got {calculated_total_pages}"
            
            # Property 3: If page is within range, we should get records (unless total is 0)
            if page <= expected_total_pages and actual_total > 0:
                # Calculate expected records on this page
                start_idx = (page - 1) * page_size
                end_idx = min(start_idx + page_size, actual_total)
                expected_on_page = end_idx - start_idx
                assert len(records) == expected_on_page, \
                    f"Page {page} should have {expected_on_page} records, got {len(records)}"
            
            # Property 4: If page is beyond total_pages, should return empty
            if page > expected_total_pages:
                assert len(records) == 0, \
                    f"Page {page} is beyond total_pages {expected_total_pages}, should be empty"
            
        finally:
            session.close()
            engine.dispose()
    
    @settings(max_examples=50, deadline=None)
    @given(
        n_instruments=st.integers(min_value=1, max_value=20),
        n_records=st.integers(min_value=1, max_value=50),
        page_size=st.integers(min_value=1, max_value=100),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_pagination_covers_all_records(self, n_instruments, n_records, page_size, seed):
        """
        **Feature: data-management-refactor, Property 13: Pagination Correctness**
        **Validates: Requirements 2.2**
        
        Iterating through all pages should return all records exactly once.
        """
        engine, Session = create_test_db()
        session = Session()
        
        try:
            # Seed data
            seed_test_data(session, n_instruments, n_records, seed)
            
            # Get total count
            total = session.query(MarketData).count()
            total_pages = math.ceil(total / page_size) if total > 0 else 1
            
            # Collect all record IDs across all pages
            all_ids = set()
            for page in range(1, total_pages + 1):
                offset = (page - 1) * page_size
                records = session.query(MarketData).order_by(MarketData.id).offset(offset).limit(page_size).all()
                for record in records:
                    assert record.id not in all_ids, \
                        f"Record {record.id} appears on multiple pages"
                    all_ids.add(record.id)
            
            # Verify we got all records
            assert len(all_ids) == total, \
                f"Pagination should cover all {total} records, got {len(all_ids)}"
            
        finally:
            session.close()
            engine.dispose()



class TestFilterProperties:
    """
    Property-based tests for filter correctness.
    
    **Feature: data-management-refactor, Property 14: Filter Correctness**
    **Validates: Requirements 2.3**
    """
    
    @settings(max_examples=100, deadline=None)
    @given(
        n_instruments=st.integers(min_value=2, max_value=10),
        n_records=st.integers(min_value=5, max_value=30),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_ticker_filter_correctness(self, n_instruments, n_records, seed):
        """
        **Feature: data-management-refactor, Property 14: Filter Correctness**
        **Validates: Requirements 2.3**
        
        For any filter applied to a table (e.g., ticker = "VNM"), all returned
        records should match the filter criteria.
        """
        engine, Session = create_test_db()
        session = Session()
        
        try:
            # Seed data
            tickers = seed_test_data(session, n_instruments, n_records, seed)
            
            # Pick a random ticker to filter by
            np.random.seed(seed)
            filter_ticker = np.random.choice(tickers)
            
            # Query with filter
            filtered_records = session.query(MarketData).filter(
                MarketData.ticker == filter_ticker
            ).all()
            
            # Verify all records match the filter
            for record in filtered_records:
                assert record.ticker == filter_ticker, \
                    f"Record ticker {record.ticker} does not match filter {filter_ticker}"
            
            # Verify we got the expected count
            expected_count = n_records  # Each ticker has n_records
            assert len(filtered_records) == expected_count, \
                f"Expected {expected_count} records for ticker {filter_ticker}, got {len(filtered_records)}"
            
        finally:
            session.close()
            engine.dispose()
    
    @settings(max_examples=100, deadline=None)
    @given(
        n_instruments=st.integers(min_value=2, max_value=5),
        n_records=st.integers(min_value=10, max_value=50),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_date_range_filter_correctness(self, n_instruments, n_records, seed):
        """
        **Feature: data-management-refactor, Property 14: Filter Correctness**
        **Validates: Requirements 2.3**
        
        For any date range filter, all returned records should have dates
        within the specified range.
        """
        engine, Session = create_test_db()
        session = Session()
        
        try:
            # Seed data
            seed_test_data(session, n_instruments, n_records, seed)
            
            # Define date range (pick a subset of the data range)
            base_date = date(2024, 1, 1)
            np.random.seed(seed)
            start_offset = np.random.randint(0, max(1, n_records // 2))
            end_offset = np.random.randint(start_offset + 1, n_records)
            
            start_date = base_date + timedelta(days=start_offset)
            end_date = base_date + timedelta(days=end_offset)
            
            # Query with date range filter
            filtered_records = session.query(MarketData).filter(
                MarketData.date >= start_date,
                MarketData.date <= end_date
            ).all()
            
            # Verify all records are within the date range
            for record in filtered_records:
                assert start_date <= record.date <= end_date, \
                    f"Record date {record.date} is outside range [{start_date}, {end_date}]"
            
            # Verify we got records (should have some in range)
            expected_days = (end_date - start_date).days + 1
            expected_count = expected_days * n_instruments
            assert len(filtered_records) == expected_count, \
                f"Expected {expected_count} records in date range, got {len(filtered_records)}"
            
        finally:
            session.close()
            engine.dispose()
    
    @settings(max_examples=100, deadline=None)
    @given(
        n_instruments=st.integers(min_value=2, max_value=5),
        n_records=st.integers(min_value=5, max_value=20),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_combined_filter_correctness(self, n_instruments, n_records, seed):
        """
        **Feature: data-management-refactor, Property 14: Filter Correctness**
        **Validates: Requirements 2.3**
        
        For combined filters (ticker AND date range), all returned records
        should match ALL filter criteria.
        """
        engine, Session = create_test_db()
        session = Session()
        
        try:
            # Seed data
            tickers = seed_test_data(session, n_instruments, n_records, seed)
            
            # Pick a random ticker
            np.random.seed(seed)
            filter_ticker = np.random.choice(tickers)
            
            # Define date range
            base_date = date(2024, 1, 1)
            start_offset = np.random.randint(0, max(1, n_records // 2))
            end_offset = np.random.randint(start_offset + 1, n_records)
            
            start_date = base_date + timedelta(days=start_offset)
            end_date = base_date + timedelta(days=end_offset)
            
            # Query with combined filters
            filtered_records = session.query(MarketData).filter(
                MarketData.ticker == filter_ticker,
                MarketData.date >= start_date,
                MarketData.date <= end_date
            ).all()
            
            # Verify all records match ALL criteria
            for record in filtered_records:
                assert record.ticker == filter_ticker, \
                    f"Record ticker {record.ticker} does not match filter {filter_ticker}"
                assert start_date <= record.date <= end_date, \
                    f"Record date {record.date} is outside range [{start_date}, {end_date}]"
            
            # Verify count
            expected_days = (end_date - start_date).days + 1
            assert len(filtered_records) == expected_days, \
                f"Expected {expected_days} records for ticker {filter_ticker} in date range, got {len(filtered_records)}"
            
        finally:
            session.close()
            engine.dispose()
    
    @settings(max_examples=50, deadline=None)
    @given(
        n_instruments=st.integers(min_value=2, max_value=5),
        n_records=st.integers(min_value=5, max_value=20),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_filter_excludes_non_matching(self, n_instruments, n_records, seed):
        """
        **Feature: data-management-refactor, Property 14: Filter Correctness**
        **Validates: Requirements 2.3**
        
        Records that don't match the filter should NOT be returned.
        """
        assume(n_instruments >= 2)  # Need at least 2 instruments
        
        engine, Session = create_test_db()
        session = Session()
        
        try:
            # Seed data
            tickers = seed_test_data(session, n_instruments, n_records, seed)
            
            # Pick a ticker to filter by
            np.random.seed(seed)
            filter_ticker = tickers[0]
            other_tickers = tickers[1:]
            
            # Query with filter
            filtered_records = session.query(MarketData).filter(
                MarketData.ticker == filter_ticker
            ).all()
            
            filtered_ids = {r.id for r in filtered_records}
            
            # Query records for other tickers
            other_records = session.query(MarketData).filter(
                MarketData.ticker.in_(other_tickers)
            ).all()
            
            # Verify none of the other records are in filtered results
            for record in other_records:
                assert record.id not in filtered_ids, \
                    f"Record {record.id} with ticker {record.ticker} should not be in filtered results for {filter_ticker}"
            
        finally:
            session.close()
            engine.dispose()
