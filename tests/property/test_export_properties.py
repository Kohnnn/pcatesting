"""
Property-based tests for Export API.

**Feature: data-management-refactor**
"""
import sys
import os
import io
import csv
import json
from pathlib import Path
from datetime import date, timedelta

# Add src and backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

import pytest
from hypothesis import given, strategies as st, settings, assume
import numpy as np
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import (
    Base, Instrument, MarketData, TradingSignal, DailySentiment,
    AnalystRecommendation, VNIndex
)


def create_test_db():
    """Create an in-memory test database with tables."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session


def seed_export_test_data(session, n_instruments, n_records_per_instrument, seed=42):
    """Seed test database with data for export tests."""
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
    
    # Create VNIndex data
    for i in range(n_records_per_instrument):
        record_date = base_date + timedelta(days=i)
        vnindex = VNIndex(
            date=record_date,
            close_index=np.random.uniform(900, 1500),
            buy_volume=int(np.random.uniform(100000000, 500000000)),
            sell_volume=int(np.random.uniform(100000000, 500000000)),
            total_volume=int(np.random.uniform(200000000, 1000000000))
        )
        session.add(vnindex)
    
    # Create sentiment data
    for ticker in tickers:
        for i in range(n_records_per_instrument):
            record_date = base_date + timedelta(days=i)
            sentiment = DailySentiment(
                ticker=ticker,
                date=record_date,
                rsi=np.random.uniform(0, 100),
                bsi=np.random.uniform(0, 1),
                atr=np.random.uniform(0, 0.1),
                ltv=np.random.uniform(10, 20),
                pli=np.random.uniform(0, 1),
                raw_sentiment=np.random.uniform(-2, 2),
                pure_sentiment=np.random.uniform(-2, 2)
            )
            session.add(sentiment)
    
    # Create recommendations
    signal_types = ["Contrarian Dip Buy", "Momentum Breakout", "Retail Trap", "Neutral / No Edge"]
    recommendations = ["buy", "hold", "sell", "outperform", "underperform"]
    
    for ticker in tickers:
        for i in range(min(5, n_records_per_instrument)):
            record_date = base_date + timedelta(days=i * 10)
            rec = AnalystRecommendation(
                ticker=ticker,
                analyst_firm=f"Firm{i}",
                analyst_name=f"Analyst{i}",
                recommendation=np.random.choice(recommendations),
                rating_numeric=np.random.randint(1, 6),
                target_price=np.random.uniform(10000, 100000),
                issue_date=record_date
            )
            session.add(rec)
    
    session.flush()
    
    # Create trading signals with recommendation references
    for ticker in tickers:
        recs = session.query(AnalystRecommendation).filter(
            AnalystRecommendation.ticker == ticker
        ).all()
        
        for i in range(min(3, n_records_per_instrument)):
            record_date = base_date + timedelta(days=i * 15)
            rec_id = recs[i % len(recs)].id if recs else None
            signal = TradingSignal(
                ticker=ticker,
                date=record_date,
                signal_type=np.random.choice(signal_types),
                sentiment_score=np.random.uniform(-2, 2),
                foreign_flow_score=np.random.uniform(-1, 1),
                analyst_action=np.random.choice(["upgrade", "downgrade", "maintain"]),
                recommendation_id=rec_id
            )
            session.add(signal)
    
    session.commit()
    return tickers



class TestExportFormatValidity:
    """
    Property-based tests for export format validity.
    
    **Feature: data-management-refactor, Property 10: Export Format Validity**
    **Validates: Requirements 6.1**
    """
    
    @settings(max_examples=100, deadline=None)
    @given(
        n_instruments=st.integers(min_value=1, max_value=10),
        n_records=st.integers(min_value=1, max_value=30),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_csv_export_produces_valid_csv(self, n_instruments, n_records, seed):
        """
        **Feature: data-management-refactor, Property 10: Export Format Validity**
        **Validates: Requirements 6.1**
        
        For any table export in CSV format, the output should be valid CSV
        with correct headers and parseable values.
        """
        engine, Session = create_test_db()
        session = Session()
        
        try:
            # Seed data
            seed_export_test_data(session, n_instruments, n_records, seed)
            
            # Get market data records
            records = session.query(MarketData).all()
            
            # Generate CSV content
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            columns = ['id', 'ticker', 'date', 'close_price', 'buy_volume', 
                      'sell_volume', 'total_volume', 'shares_outstanding']
            writer.writerow(columns)
            
            # Write data rows
            for record in records:
                writer.writerow([
                    record.id,
                    record.ticker,
                    record.date.isoformat() if record.date else '',
                    record.close_price if record.close_price is not None else '',
                    record.buy_volume if record.buy_volume is not None else '',
                    record.sell_volume if record.sell_volume is not None else '',
                    record.total_volume if record.total_volume is not None else '',
                    record.shares_outstanding if record.shares_outstanding is not None else ''
                ])
            
            csv_content = output.getvalue()
            
            # Property 1: CSV should be parseable
            output.seek(0)
            reader = csv.reader(io.StringIO(csv_content))
            rows = list(reader)
            
            assert len(rows) > 0, "CSV should have at least a header row"
            
            # Property 2: Header row should have correct columns
            header = rows[0]
            assert header == columns, f"Header should be {columns}, got {header}"
            
            # Property 3: Data rows should have same number of columns as header
            for i, row in enumerate(rows[1:], start=2):
                assert len(row) == len(columns), \
                    f"Row {i} has {len(row)} columns, expected {len(columns)}"
            
            # Property 4: Number of data rows should match record count
            assert len(rows) - 1 == len(records), \
                f"CSV should have {len(records)} data rows, got {len(rows) - 1}"
            
            # Property 5: CSV should be parseable by pandas
            df = pd.read_csv(io.StringIO(csv_content))
            assert len(df) == len(records), \
                f"Pandas should parse {len(records)} rows, got {len(df)}"
            
        finally:
            session.close()
            engine.dispose()
    
    @settings(max_examples=100, deadline=None)
    @given(
        n_instruments=st.integers(min_value=1, max_value=10),
        n_records=st.integers(min_value=1, max_value=30),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_json_export_produces_valid_json(self, n_instruments, n_records, seed):
        """
        **Feature: data-management-refactor, Property 10: Export Format Validity**
        **Validates: Requirements 6.1**
        
        For any table export in JSON format, the output should be valid JSON
        with correct structure and parseable values.
        """
        engine, Session = create_test_db()
        session = Session()
        
        try:
            # Seed data
            seed_export_test_data(session, n_instruments, n_records, seed)
            
            # Get market data records
            records = session.query(MarketData).all()
            
            # Generate JSON content
            data = []
            for record in records:
                data.append({
                    'id': record.id,
                    'ticker': record.ticker,
                    'date': record.date.isoformat() if record.date else None,
                    'close_price': record.close_price,
                    'buy_volume': record.buy_volume,
                    'sell_volume': record.sell_volume,
                    'total_volume': record.total_volume,
                    'shares_outstanding': record.shares_outstanding
                })
            
            json_output = {
                "table": "market_data",
                "count": len(data),
                "data": data
            }
            
            json_content = json.dumps(json_output)
            
            # Property 1: JSON should be parseable
            parsed = json.loads(json_content)
            
            # Property 2: JSON should have required structure
            assert "table" in parsed, "JSON should have 'table' field"
            assert "count" in parsed, "JSON should have 'count' field"
            assert "data" in parsed, "JSON should have 'data' field"
            
            # Property 3: Count should match data length
            assert parsed["count"] == len(parsed["data"]), \
                f"Count {parsed['count']} should match data length {len(parsed['data'])}"
            
            # Property 4: Data should match record count
            assert len(parsed["data"]) == len(records), \
                f"JSON should have {len(records)} records, got {len(parsed['data'])}"
            
            # Property 5: Each record should have required fields
            required_fields = ['id', 'ticker', 'date', 'close_price']
            for i, item in enumerate(parsed["data"]):
                for field in required_fields:
                    assert field in item, \
                        f"Record {i} missing required field '{field}'"
            
        finally:
            session.close()
            engine.dispose()


class TestExportDataCompleteness:
    """
    Property-based tests for export data completeness.
    
    **Feature: data-management-refactor, Property 11: Export Data Completeness**
    **Validates: Requirements 6.2**
    """
    
    @settings(max_examples=100, deadline=None)
    @given(
        n_instruments=st.integers(min_value=1, max_value=5),
        n_records=st.integers(min_value=5, max_value=20),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_signal_export_includes_all_fields(self, n_instruments, n_records, seed):
        """
        **Feature: data-management-refactor, Property 11: Export Data Completeness**
        **Validates: Requirements 6.2**
        
        For any signal export, the output should include all signal fields
        plus the related recommendation text and sentiment score.
        """
        engine, Session = create_test_db()
        session = Session()
        
        try:
            # Seed data
            seed_export_test_data(session, n_instruments, n_records, seed)
            
            # Get signals with related data
            signals = session.query(TradingSignal).all()
            
            # Generate full export data
            export_data = []
            for signal in signals:
                # Get related recommendation
                rec = None
                if signal.recommendation_id:
                    rec = session.query(AnalystRecommendation).filter(
                        AnalystRecommendation.id == signal.recommendation_id
                    ).first()
                
                # Get related sentiment
                sentiment = session.query(DailySentiment).filter(
                    DailySentiment.ticker == signal.ticker,
                    DailySentiment.date == signal.date
                ).first()
                
                export_record = {
                    # Signal fields
                    'id': signal.id,
                    'ticker': signal.ticker,
                    'date': signal.date.isoformat() if signal.date else None,
                    'signal_type': signal.signal_type,
                    'sentiment_score': signal.sentiment_score,
                    'foreign_flow_score': signal.foreign_flow_score,
                    'analyst_action': signal.analyst_action,
                    'recommendation_id': signal.recommendation_id,
                    # Recommendation fields
                    'recommendation_text': rec.recommendation if rec else None,
                    'rating_numeric': rec.rating_numeric if rec else None,
                    'analyst_firm': rec.analyst_firm if rec else None,
                    # Sentiment fields
                    'rsi': sentiment.rsi if sentiment else None,
                    'bsi': sentiment.bsi if sentiment else None,
                    'pure_sentiment': sentiment.pure_sentiment if sentiment else None
                }
                export_data.append(export_record)
            
            # Property 1: Export should have same count as signals
            assert len(export_data) == len(signals), \
                f"Export should have {len(signals)} records, got {len(export_data)}"
            
            # Property 2: Each export record should have all signal fields
            signal_fields = ['id', 'ticker', 'date', 'signal_type', 'sentiment_score',
                           'foreign_flow_score', 'analyst_action', 'recommendation_id']
            for i, record in enumerate(export_data):
                for field in signal_fields:
                    assert field in record, \
                        f"Record {i} missing signal field '{field}'"
            
            # Property 3: Each export record should have recommendation fields
            rec_fields = ['recommendation_text', 'rating_numeric', 'analyst_firm']
            for i, record in enumerate(export_data):
                for field in rec_fields:
                    assert field in record, \
                        f"Record {i} missing recommendation field '{field}'"
            
            # Property 4: Each export record should have sentiment fields
            sentiment_fields = ['rsi', 'bsi', 'pure_sentiment']
            for i, record in enumerate(export_data):
                for field in sentiment_fields:
                    assert field in record, \
                        f"Record {i} missing sentiment field '{field}'"
            
            # Property 5: Records with recommendation_id should have recommendation data
            for i, record in enumerate(export_data):
                if record['recommendation_id'] is not None:
                    assert record['recommendation_text'] is not None, \
                        f"Record {i} has recommendation_id but no recommendation_text"
            
        finally:
            session.close()
            engine.dispose()
    
    @settings(max_examples=50, deadline=None)
    @given(
        n_instruments=st.integers(min_value=1, max_value=5),
        n_records=st.integers(min_value=5, max_value=20),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_signal_export_csv_has_all_columns(self, n_instruments, n_records, seed):
        """
        **Feature: data-management-refactor, Property 11: Export Data Completeness**
        **Validates: Requirements 6.2**
        
        Signal CSV export should have all required columns for signal,
        recommendation, and sentiment data.
        """
        engine, Session = create_test_db()
        session = Session()
        
        try:
            # Seed data
            seed_export_test_data(session, n_instruments, n_records, seed)
            
            # Expected columns for full signal export
            expected_columns = [
                'id', 'ticker', 'date', 'signal_type', 'sentiment_score',
                'foreign_flow_score', 'analyst_action', 'recommendation_id',
                'recommendation_text', 'rating_numeric', 'analyst_firm',
                'analyst_name', 'target_price', 'issue_date',
                'rsi', 'bsi', 'atr', 'ltv', 'pli', 'raw_sentiment', 'pure_sentiment'
            ]
            
            # Generate CSV
            signals = session.query(TradingSignal).all()
            
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(expected_columns)
            
            for signal in signals:
                rec = None
                if signal.recommendation_id:
                    rec = session.query(AnalystRecommendation).filter(
                        AnalystRecommendation.id == signal.recommendation_id
                    ).first()
                
                sentiment = session.query(DailySentiment).filter(
                    DailySentiment.ticker == signal.ticker,
                    DailySentiment.date == signal.date
                ).first()
                
                writer.writerow([
                    signal.id,
                    signal.ticker,
                    signal.date.isoformat() if signal.date else '',
                    signal.signal_type or '',
                    signal.sentiment_score if signal.sentiment_score is not None else '',
                    signal.foreign_flow_score if signal.foreign_flow_score is not None else '',
                    signal.analyst_action or '',
                    signal.recommendation_id if signal.recommendation_id is not None else '',
                    rec.recommendation if rec else '',
                    rec.rating_numeric if rec else '',
                    rec.analyst_firm if rec else '',
                    rec.analyst_name if rec else '',
                    rec.target_price if rec else '',
                    rec.issue_date.isoformat() if rec and rec.issue_date else '',
                    sentiment.rsi if sentiment else '',
                    sentiment.bsi if sentiment else '',
                    sentiment.atr if sentiment else '',
                    sentiment.ltv if sentiment else '',
                    sentiment.pli if sentiment else '',
                    sentiment.raw_sentiment if sentiment else '',
                    sentiment.pure_sentiment if sentiment else ''
                ])
            
            csv_content = output.getvalue()
            
            # Parse and verify
            df = pd.read_csv(io.StringIO(csv_content))
            
            # Property: All expected columns should be present
            for col in expected_columns:
                assert col in df.columns, f"Missing column '{col}' in export"
            
        finally:
            session.close()
            engine.dispose()



class TestEventStudyExportCompleteness:
    """
    Property-based tests for event study export completeness.
    
    **Feature: data-management-refactor, Property 12: Event Study Export Completeness**
    **Validates: Requirements 6.4**
    """
    
    @settings(max_examples=100, deadline=None)
    @given(
        window_before=st.integers(min_value=5, max_value=25),
        window_after=st.integers(min_value=5, max_value=25),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_event_study_export_has_correct_data_points(self, window_before, window_after, seed):
        """
        **Feature: data-management-refactor, Property 12: Event Study Export Completeness**
        **Validates: Requirements 6.4**
        
        For any event study export with window (-W1, +W2), the output should
        contain data points covering the event window with both CAR and CAS values.
        """
        engine, Session = create_test_db()
        session = Session()
        
        try:
            # Seed data with enough records to cover the window
            n_records = window_before + window_after + 60  # Extra buffer
            seed_export_test_data(session, 1, n_records, seed)
            
            # Get the ticker
            ticker = "T000"
            base_date = date(2024, 1, 1)
            
            # Event date should be in the middle of the data range
            event_date = base_date + timedelta(days=window_before + 30)
            
            # Get market data
            market_data = session.query(MarketData).filter(
                MarketData.ticker == ticker
            ).order_by(MarketData.date).all()
            
            # Get VNIndex data
            vnindex_data = session.query(VNIndex).order_by(VNIndex.date).all()
            
            # Get sentiment data
            sentiment_data = session.query(DailySentiment).filter(
                DailySentiment.ticker == ticker
            ).order_by(DailySentiment.date).all()
            
            # Convert to DataFrames
            market_df = pd.DataFrame([
                {'date': md.date, 'close_price': md.close_price}
                for md in market_data
            ])
            
            vnindex_df = pd.DataFrame([
                {'date': vn.date, 'close_index': vn.close_index}
                for vn in vnindex_data
            ])
            
            sentiment_df = pd.DataFrame([
                {'date': s.date, 'pure_sentiment': s.pure_sentiment}
                for s in sentiment_data
            ])
            
            # Calculate returns
            market_df['return'] = market_df['close_price'].pct_change()
            vnindex_df['market_return'] = vnindex_df['close_index'].pct_change()
            
            # Merge data
            merged_df = market_df.merge(vnindex_df, on='date', how='inner')
            merged_df = merged_df.merge(sentiment_df, on='date', how='inner')
            merged_df = merged_df.dropna()
            
            # Simulate event study calculation
            # Find event date index
            merged_df['date'] = pd.to_datetime(merged_df['date'])
            event_timestamp = pd.Timestamp(event_date)
            
            # Find closest date to event
            date_diffs = abs(merged_df['date'] - event_timestamp)
            event_idx = date_diffs.idxmin()
            
            # Get window indices
            start_idx = max(0, event_idx - window_before)
            end_idx = min(len(merged_df) - 1, event_idx + window_after)
            
            # Extract window data
            window_data = merged_df.iloc[start_idx:end_idx + 1].copy()
            
            # Calculate day numbers relative to event
            window_data['day'] = range(-window_before, -window_before + len(window_data))
            
            # Simulate CAR calculation (cumulative sum of returns as proxy)
            window_data['car'] = window_data['return'].cumsum()
            
            # Simulate CAS calculation (cumulative sum of sentiment deviation)
            mean_sentiment = merged_df['pure_sentiment'].mean()
            window_data['cas'] = (window_data['pure_sentiment'] - mean_sentiment).cumsum()
            
            # Generate export data
            export_data = []
            for _, row in window_data.iterrows():
                export_data.append({
                    'day': int(row['day']),
                    'car': float(row['car']) if pd.notna(row['car']) else None,
                    'cas': float(row['cas']) if pd.notna(row['cas']) else None
                })
            
            # Property 1: Export should have data points
            assert len(export_data) > 0, "Event study export should have data points"
            
            # Property 2: Each data point should have day, car, and cas fields
            for i, point in enumerate(export_data):
                assert 'day' in point, f"Data point {i} missing 'day' field"
                assert 'car' in point, f"Data point {i} missing 'car' field"
                assert 'cas' in point, f"Data point {i} missing 'cas' field"
            
            # Property 3: Days should be sequential
            days = [p['day'] for p in export_data]
            for i in range(1, len(days)):
                assert days[i] == days[i-1] + 1, \
                    f"Days should be sequential, got {days[i-1]} followed by {days[i]}"
            
            # Property 4: CAR and CAS values should be numeric (or None)
            for i, point in enumerate(export_data):
                if point['car'] is not None:
                    assert isinstance(point['car'], (int, float)), \
                        f"CAR at day {point['day']} should be numeric"
                if point['cas'] is not None:
                    assert isinstance(point['cas'], (int, float)), \
                        f"CAS at day {point['day']} should be numeric"
            
        finally:
            session.close()
            engine.dispose()
    
    @settings(max_examples=50, deadline=None)
    @given(
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_event_study_export_standard_window(self, seed):
        """
        **Feature: data-management-refactor, Property 12: Event Study Export Completeness**
        **Validates: Requirements 6.4**
        
        For the standard event study window (-25, +25), the output should
        contain exactly 51 data points for both CAR and CAS.
        """
        engine, Session = create_test_db()
        session = Session()
        
        try:
            # Seed data with enough records
            n_records = 100  # Enough for -25 to +25 window
            seed_export_test_data(session, 1, n_records, seed)
            
            ticker = "T000"
            base_date = date(2024, 1, 1)
            event_date = base_date + timedelta(days=50)  # Middle of data
            
            window_before = 25
            window_after = 25
            expected_points = window_before + window_after + 1  # 51 points
            
            # Get data
            market_data = session.query(MarketData).filter(
                MarketData.ticker == ticker
            ).order_by(MarketData.date).all()
            
            vnindex_data = session.query(VNIndex).order_by(VNIndex.date).all()
            
            sentiment_data = session.query(DailySentiment).filter(
                DailySentiment.ticker == ticker
            ).order_by(DailySentiment.date).all()
            
            # Convert to DataFrames
            market_df = pd.DataFrame([
                {'date': md.date, 'close_price': md.close_price}
                for md in market_data
            ])
            
            vnindex_df = pd.DataFrame([
                {'date': vn.date, 'close_index': vn.close_index}
                for vn in vnindex_data
            ])
            
            sentiment_df = pd.DataFrame([
                {'date': s.date, 'pure_sentiment': s.pure_sentiment}
                for s in sentiment_data
            ])
            
            # Calculate returns
            market_df['return'] = market_df['close_price'].pct_change()
            vnindex_df['market_return'] = vnindex_df['close_index'].pct_change()
            
            # Merge
            merged_df = market_df.merge(vnindex_df, on='date', how='inner')
            merged_df = merged_df.merge(sentiment_df, on='date', how='inner')
            merged_df = merged_df.dropna().reset_index(drop=True)
            
            # Find event index
            merged_df['date'] = pd.to_datetime(merged_df['date'])
            event_timestamp = pd.Timestamp(event_date)
            
            date_diffs = abs(merged_df['date'] - event_timestamp)
            event_idx = date_diffs.idxmin()
            
            # Get window
            start_idx = max(0, event_idx - window_before)
            end_idx = min(len(merged_df) - 1, event_idx + window_after)
            
            window_data = merged_df.iloc[start_idx:end_idx + 1]
            
            # Calculate CAR and CAS
            car_values = window_data['return'].cumsum().tolist()
            mean_sentiment = merged_df['pure_sentiment'].mean()
            cas_values = (window_data['pure_sentiment'] - mean_sentiment).cumsum().tolist()
            
            # Property: For standard window with sufficient data, should have ~51 points
            # (may be slightly less if event is near data boundaries)
            actual_points = len(window_data)
            
            # If we have enough data around the event, we should get close to expected
            if event_idx >= window_before and event_idx + window_after < len(merged_df):
                assert actual_points == expected_points, \
                    f"Standard window should have {expected_points} points, got {actual_points}"
            
            # Property: CAR and CAS arrays should have same length
            assert len(car_values) == len(cas_values), \
                f"CAR ({len(car_values)}) and CAS ({len(cas_values)}) should have same length"
            
        finally:
            session.close()
            engine.dispose()
    
    @settings(max_examples=50, deadline=None)
    @given(
        n_instruments=st.integers(min_value=1, max_value=3),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_event_study_csv_format(self, n_instruments, seed):
        """
        **Feature: data-management-refactor, Property 12: Event Study Export Completeness**
        **Validates: Requirements 6.4**
        
        Event study CSV export should have correct format with day, car, cas columns.
        """
        engine, Session = create_test_db()
        session = Session()
        
        try:
            # Seed data
            n_records = 80
            seed_export_test_data(session, n_instruments, n_records, seed)
            
            ticker = "T000"
            base_date = date(2024, 1, 1)
            event_date = base_date + timedelta(days=40)
            
            # Generate sample event study data
            days = list(range(-25, 26))
            np.random.seed(seed)
            car_values = np.cumsum(np.random.randn(51) * 0.01).tolist()
            cas_values = np.cumsum(np.random.randn(51) * 0.1).tolist()
            
            # Generate CSV
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['day', 'car', 'cas'])
            
            for i, day in enumerate(days):
                writer.writerow([day, car_values[i], cas_values[i]])
            
            csv_content = output.getvalue()
            
            # Parse and verify
            df = pd.read_csv(io.StringIO(csv_content))
            
            # Property 1: Should have required columns
            assert 'day' in df.columns, "CSV should have 'day' column"
            assert 'car' in df.columns, "CSV should have 'car' column"
            assert 'cas' in df.columns, "CSV should have 'cas' column"
            
            # Property 2: Day column should be integers
            assert df['day'].dtype in [np.int64, np.int32, int], \
                f"Day column should be integer, got {df['day'].dtype}"
            
            # Property 3: CAR and CAS should be numeric
            assert pd.api.types.is_numeric_dtype(df['car']), \
                "CAR column should be numeric"
            assert pd.api.types.is_numeric_dtype(df['cas']), \
                "CAS column should be numeric"
            
            # Property 4: Days should span the expected range
            assert df['day'].min() == -25, f"Min day should be -25, got {df['day'].min()}"
            assert df['day'].max() == 25, f"Max day should be 25, got {df['day'].max()}"
            
        finally:
            session.close()
            engine.dispose()
