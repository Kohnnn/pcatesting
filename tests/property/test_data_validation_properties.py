"""
Property-based tests for data validation.

**Feature: data-management-refactor**
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from hypothesis import given, strategies as st, settings, assume
import pandas as pd
from datetime import date, datetime

from data_validator import DataValidator, AnomalyRecord, ValidationSummary


class TestPricePositivityProperty:
    """
    **Feature: data-management-refactor, Property 6: Price Positivity**
    **Validates: Requirements 7.1**
    
    For any close price value imported into the database, 
    the value should be a positive number (> 0).
    """
    
    @settings(max_examples=100, deadline=None)
    @given(price=st.floats(min_value=0.01, max_value=1e9))
    def test_valid_prices_accepted(self, price):
        """Valid positive prices should be accepted."""
        validator = DataValidator()
        assert validator.validate_price(price) is True
    
    @settings(max_examples=100, deadline=None)
    @given(price=st.floats(max_value=0, allow_nan=False, allow_infinity=False))
    def test_non_positive_prices_rejected(self, price):
        """Non-positive prices (zero or negative) should be rejected."""
        validator = DataValidator()
        assert validator.validate_price(price) is False
    
    @settings(max_examples=50, deadline=None)
    @given(price=st.one_of(
        st.none(),
        st.text(min_size=1, max_size=10).filter(lambda x: not _is_numeric_string(x)),
    ))
    def test_invalid_price_types_rejected(self, price):
        """Invalid price types (None, non-numeric strings) should be rejected."""
        validator = DataValidator()
        assert validator.validate_price(price) is False
    
    @settings(max_examples=50, deadline=None)
    @given(price=st.sampled_from([float('nan'), float('inf'), float('-inf')]))
    def test_nan_and_infinity_rejected(self, price):
        """NaN and infinity values should be rejected."""
        validator = DataValidator()
        assert validator.validate_price(price) is False


class TestVolumeNonNegativityProperty:
    """
    **Feature: data-management-refactor, Property 7: Volume Non-Negativity**
    **Validates: Requirements 7.2**
    
    For any volume value (buy_volume, sell_volume, total_volume) imported 
    into the database, the value should be a non-negative integer (>= 0).
    """
    
    @settings(max_examples=100, deadline=None)
    @given(volume=st.integers(min_value=0, max_value=10**12))
    def test_valid_volumes_accepted(self, volume):
        """Non-negative integer volumes should be accepted."""
        validator = DataValidator()
        assert validator.validate_volume(volume) is True
    
    @settings(max_examples=100, deadline=None)
    @given(volume=st.integers(max_value=-1))
    def test_negative_volumes_rejected(self, volume):
        """Negative volumes should be rejected."""
        validator = DataValidator()
        assert validator.validate_volume(volume) is False
    
    @settings(max_examples=50, deadline=None)
    @given(volume=st.floats(min_value=0.01, max_value=1000).filter(
        lambda x: x != int(x)  # Non-integer floats
    ))
    def test_non_integer_volumes_rejected(self, volume):
        """Non-integer volumes should be rejected."""
        validator = DataValidator()
        assert validator.validate_volume(volume) is False
    
    @settings(max_examples=50, deadline=None)
    @given(volume=st.one_of(
        st.none(),
        st.text(min_size=1, max_size=10).filter(lambda x: not _is_numeric_string(x)),
    ))
    def test_invalid_volume_types_rejected(self, volume):
        """Invalid volume types (None, non-numeric strings) should be rejected."""
        validator = DataValidator()
        assert validator.validate_volume(volume) is False


def _is_numeric_string(s: str) -> bool:
    """Check if a string can be parsed as a number."""
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


class TestDateRangeValidityProperty:
    """
    **Feature: data-management-refactor, Property 8: Date Range Validity**
    **Validates: Requirements 7.3**
    
    For any recommendation issue date imported into the database, 
    the date should be within the expected range (2014-01-01 to 2024-12-31).
    """
    
    @settings(max_examples=100, deadline=None)
    @given(
        year=st.integers(min_value=2014, max_value=2024),
        month=st.integers(min_value=1, max_value=12),
        day=st.integers(min_value=1, max_value=28)  # Use 28 to avoid month-end issues
    )
    def test_valid_dates_accepted(self, year, month, day):
        """Dates within 2014-2024 range should be accepted."""
        validator = DataValidator()
        test_date = date(year, month, day)
        assert validator.validate_date_range(test_date) is True
    
    @settings(max_examples=100, deadline=None)
    @given(
        year=st.integers(min_value=2014, max_value=2024),
        month=st.integers(min_value=1, max_value=12),
        day=st.integers(min_value=1, max_value=28)
    )
    def test_valid_datetime_accepted(self, year, month, day):
        """Datetime objects within 2014-2024 range should be accepted."""
        validator = DataValidator()
        test_datetime = datetime(year, month, day, 12, 0, 0)
        assert validator.validate_date_range(test_datetime) is True
    
    @settings(max_examples=100, deadline=None)
    @given(
        year=st.integers(min_value=2014, max_value=2024),
        month=st.integers(min_value=1, max_value=12),
        day=st.integers(min_value=1, max_value=28)
    )
    def test_valid_date_strings_accepted(self, year, month, day):
        """Date strings within 2014-2024 range should be accepted."""
        validator = DataValidator()
        date_str = f"{year}-{month:02d}-{day:02d}"
        assert validator.validate_date_range(date_str) is True
    
    @settings(max_examples=50, deadline=None)
    @given(year=st.integers(min_value=1900, max_value=2013))
    def test_dates_before_2014_rejected(self, year):
        """Dates before 2014 should be rejected."""
        validator = DataValidator()
        test_date = date(year, 6, 15)
        assert validator.validate_date_range(test_date) is False
    
    @settings(max_examples=50, deadline=None)
    @given(year=st.integers(min_value=2025, max_value=2100))
    def test_dates_after_2024_rejected(self, year):
        """Dates after 2024 should be rejected."""
        validator = DataValidator()
        test_date = date(year, 6, 15)
        assert validator.validate_date_range(test_date) is False
    
    @settings(max_examples=50, deadline=None)
    @given(date_val=st.one_of(
        st.none(),
        st.text(min_size=1, max_size=20).filter(
            lambda x: not any(c.isdigit() for c in x)  # No digits = invalid date
        ),
    ))
    def test_invalid_date_types_rejected(self, date_val):
        """Invalid date types (None, non-date strings) should be rejected."""
        validator = DataValidator()
        assert validator.validate_date_range(date_val) is False


class TestAnomalyDetectionCompletenessProperty:
    """
    **Feature: data-management-refactor, Property 9: Anomaly Detection Completeness**
    **Validates: Requirements 7.5**
    
    For any record with missing critical fields (ticker, date, close_price for 
    market data; ticker, recommendation, issue_date for recommendations), 
    the pipeline should flag it as an anomaly.
    """
    
    @settings(max_examples=100, deadline=None)
    @given(
        has_ticker=st.booleans(),
        has_date=st.booleans(),
        has_close_price=st.booleans()
    )
    def test_market_data_anomaly_detection(self, has_ticker, has_date, has_close_price):
        """
        Market data records missing critical fields should be flagged as anomalies.
        Critical fields: ticker, date, close_price
        """
        validator = DataValidator()
        
        # Build record with optional fields
        record = {}
        if has_ticker:
            record['ticker'] = 'AAA'
        if has_date:
            record['date'] = '2024-01-15'
        if has_close_price:
            record['close_price'] = 100.0
        
        # Add some non-critical fields
        record['buy_volume'] = 1000
        record['sell_volume'] = 500
        
        anomalies = validator.detect_anomalies([record], 'market_data')
        
        # Should have anomaly if any critical field is missing
        should_have_anomaly = not (has_ticker and has_date and has_close_price)
        
        if should_have_anomaly:
            assert len(anomalies) == 1, f"Expected 1 anomaly, got {len(anomalies)}"
            anomaly = anomalies[0]
            
            # Check that missing fields are correctly identified
            if not has_ticker:
                assert 'ticker' in anomaly.missing_fields
            if not has_date:
                assert 'date' in anomaly.missing_fields
            if not has_close_price:
                assert 'close_price' in anomaly.missing_fields
        else:
            assert len(anomalies) == 0, f"Expected no anomalies, got {len(anomalies)}"
    
    @settings(max_examples=100, deadline=None)
    @given(
        has_ticker=st.booleans(),
        has_recommendation=st.booleans(),
        has_issue_date=st.booleans()
    )
    def test_recommendation_anomaly_detection(self, has_ticker, has_recommendation, has_issue_date):
        """
        Recommendation records missing critical fields should be flagged as anomalies.
        Critical fields: ticker, recommendation, issue_date
        """
        validator = DataValidator()
        
        # Build record with optional fields
        record = {}
        if has_ticker:
            record['ticker'] = 'AAA'
        if has_recommendation:
            record['recommendation'] = 'buy'
        if has_issue_date:
            record['issue_date'] = '2024-01-15'
        
        # Add some non-critical fields
        record['analyst'] = 'Test Analyst'
        record['target_price'] = 150.0
        
        anomalies = validator.detect_anomalies([record], 'recommendation')
        
        # Should have anomaly if any critical field is missing
        should_have_anomaly = not (has_ticker and has_recommendation and has_issue_date)
        
        if should_have_anomaly:
            assert len(anomalies) == 1, f"Expected 1 anomaly, got {len(anomalies)}"
            anomaly = anomalies[0]
            
            # Check that missing fields are correctly identified
            if not has_ticker:
                assert 'ticker' in anomaly.missing_fields
            if not has_recommendation:
                assert 'recommendation' in anomaly.missing_fields
            if not has_issue_date:
                assert 'issue_date' in anomaly.missing_fields
        else:
            assert len(anomalies) == 0, f"Expected no anomalies, got {len(anomalies)}"
    
    @settings(max_examples=50, deadline=None)
    @given(
        num_valid=st.integers(min_value=0, max_value=10),
        num_invalid=st.integers(min_value=0, max_value=10)
    )
    def test_anomaly_count_accuracy(self, num_valid, num_invalid):
        """
        The number of detected anomalies should match the number of records
        with missing critical fields.
        """
        validator = DataValidator()
        
        records = []
        
        # Add valid records (all critical fields present)
        for i in range(num_valid):
            records.append({
                'ticker': f'T{i:02d}',
                'date': '2024-01-15',
                'close_price': 100.0 + i
            })
        
        # Add invalid records (missing at least one critical field)
        for i in range(num_invalid):
            records.append({
                'ticker': f'X{i:02d}',
                # Missing date and close_price
                'buy_volume': 1000
            })
        
        anomalies = validator.detect_anomalies(records, 'market_data')
        
        assert len(anomalies) == num_invalid, \
            f"Expected {num_invalid} anomalies, got {len(anomalies)}"
    
    @settings(max_examples=50, deadline=None)
    @given(
        ticker=st.one_of(st.none(), st.just(''), st.just('   ')),
        date_val=st.one_of(st.none(), st.just(''), st.just('   ')),
        price=st.one_of(st.none(), st.just(''), st.just('   '))
    )
    def test_empty_and_whitespace_treated_as_missing(self, ticker, date_val, price):
        """
        Empty strings and whitespace-only values should be treated as missing.
        """
        validator = DataValidator()
        
        record = {
            'ticker': ticker,
            'date': date_val,
            'close_price': price
        }
        
        anomalies = validator.detect_anomalies([record], 'market_data')
        
        # All fields are effectively missing, so should have anomaly
        assert len(anomalies) == 1
        
        # All critical fields should be in missing_fields
        assert 'ticker' in anomalies[0].missing_fields
        assert 'date' in anomalies[0].missing_fields
        assert 'close_price' in anomalies[0].missing_fields
    
    @settings(max_examples=50, deadline=None)
    @given(
        num_records=st.integers(min_value=1, max_value=20),
        missing_field_indices=st.lists(
            st.integers(min_value=0, max_value=19),
            min_size=0,
            max_size=10,
            unique=True
        )
    )
    def test_dataframe_anomaly_detection(self, num_records, missing_field_indices):
        """
        Anomaly detection should work correctly with DataFrame input.
        """
        assume(all(i < num_records for i in missing_field_indices))
        
        validator = DataValidator()
        
        # Create DataFrame
        data = {
            'ticker': [f'T{i:02d}' for i in range(num_records)],
            'date': ['2024-01-15'] * num_records,
            'close_price': [100.0 + i for i in range(num_records)]
        }
        df = pd.DataFrame(data)
        
        # Set some values to None to create anomalies
        for idx in missing_field_indices:
            if idx < num_records:
                df.loc[idx, 'close_price'] = None
        
        anomalies = validator.detect_anomalies(df, 'market_data')
        
        expected_anomalies = len([i for i in missing_field_indices if i < num_records])
        assert len(anomalies) == expected_anomalies, \
            f"Expected {expected_anomalies} anomalies, got {len(anomalies)}"
