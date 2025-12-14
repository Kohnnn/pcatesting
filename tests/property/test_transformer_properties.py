"""
Property-based tests for DataTransformer.

**Feature: data-management-refactor**

Tests the correctness properties defined in the design document:
- Property 1: Wide-to-Long Transformation Preserves Data
- Property 2: Rating Standardization Range
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from hypothesis import given, strategies as st, assume, settings
import pandas as pd
import numpy as np
from data_transformer import DataTransformer, TransformationResult


class TestWideToLongTransformationProperty:
    """
    **Feature: data-management-refactor, Property 1: Wide-to-Long Transformation Preserves Data**
    **Validates: Requirements 1.4**
    
    For any valid wide-format DataFrame with N tickers and M dates,
    transforming to long format should produce exactly N × M rows with no data loss.
    """
    
    @settings(max_examples=100)
    @given(
        n_tickers=st.integers(min_value=1, max_value=50),
        n_dates=st.integers(min_value=1, max_value=100),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_wide_to_long_row_count_preservation(self, n_tickers, n_dates, seed):
        """
        **Feature: data-management-refactor, Property 1: Wide-to-Long Transformation Preserves Data**
        **Validates: Requirements 1.4**
        
        The transformation should produce exactly N × M rows where N is the number
        of tickers and M is the number of dates.
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
        
        # Property: Row count should be exactly N × M
        expected_rows = n_tickers * n_dates
        actual_rows = len(long_df)
        
        assert actual_rows == expected_rows, \
            f"Expected {expected_rows} rows (N={n_tickers} × M={n_dates}), got {actual_rows}"
    
    @settings(max_examples=100)
    @given(
        n_tickers=st.integers(min_value=1, max_value=20),
        n_dates=st.integers(min_value=1, max_value=50),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_wide_to_long_data_preservation(self, n_tickers, n_dates, seed):
        """
        **Feature: data-management-refactor, Property 1: Wide-to-Long Transformation Preserves Data**
        **Validates: Requirements 1.4**
        
        All original values should be present in the transformed DataFrame.
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
        
        # Property: All original values should be present
        # Check each ticker's values
        for ticker in tickers:
            original_values = set(wide_df[ticker].values)
            long_ticker_values = set(long_df[long_df['ticker'] == ticker]['value'].values)
            
            assert original_values == long_ticker_values, \
                f"Values for ticker {ticker} don't match after transformation"
    
    @settings(max_examples=100)
    @given(
        n_tickers=st.integers(min_value=1, max_value=20),
        n_dates=st.integers(min_value=1, max_value=50),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_wide_to_long_ticker_preservation(self, n_tickers, n_dates, seed):
        """
        **Feature: data-management-refactor, Property 1: Wide-to-Long Transformation Preserves Data**
        **Validates: Requirements 1.4**
        
        All original tickers should be present in the transformed DataFrame.
        """
        np.random.seed(seed)
        
        # Generate random dates
        start_date = pd.Timestamp('2020-01-01')
        dates = pd.date_range(start=start_date, periods=n_dates, freq='D')
        
        # Generate random ticker names
        tickers = [f"TICK{i:03d}" for i in range(n_tickers)]
        
        # Generate random price data
        data = np.random.uniform(1000, 50000, size=(n_dates, n_tickers))
        
        # Create wide-format DataFrame
        wide_df = pd.DataFrame(data, columns=tickers)
        wide_df.insert(0, 'Date', dates)
        
        # Transform to long format
        transformer = DataTransformer()
        long_df = transformer.melt_wide_to_long(wide_df, 'value')
        
        # Property: All original tickers should be present
        original_tickers = set(tickers)
        transformed_tickers = set(long_df['ticker'].unique())
        
        assert original_tickers == transformed_tickers, \
            f"Tickers don't match: original={original_tickers}, transformed={transformed_tickers}"
    
    @settings(max_examples=100)
    @given(
        n_tickers=st.integers(min_value=1, max_value=20),
        n_dates=st.integers(min_value=1, max_value=50),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_wide_to_long_date_preservation(self, n_tickers, n_dates, seed):
        """
        **Feature: data-management-refactor, Property 1: Wide-to-Long Transformation Preserves Data**
        **Validates: Requirements 1.4**
        
        All original dates should be present in the transformed DataFrame.
        """
        np.random.seed(seed)
        
        # Generate random dates
        start_date = pd.Timestamp('2020-01-01')
        dates = pd.date_range(start=start_date, periods=n_dates, freq='D')
        
        # Generate random ticker names
        tickers = [f"TICK{i:03d}" for i in range(n_tickers)]
        
        # Generate random price data
        data = np.random.uniform(1000, 50000, size=(n_dates, n_tickers))
        
        # Create wide-format DataFrame
        wide_df = pd.DataFrame(data, columns=tickers)
        wide_df.insert(0, 'Date', dates)
        
        # Transform to long format
        transformer = DataTransformer()
        long_df = transformer.melt_wide_to_long(wide_df, 'value')
        
        # Property: All original dates should be present
        original_dates = set(dates)
        transformed_dates = set(long_df['date'].unique())
        
        assert original_dates == transformed_dates, \
            f"Dates don't match: expected {len(original_dates)} dates, got {len(transformed_dates)}"


class TestRatingStandardizationProperty:
    """
    **Feature: data-management-refactor, Property 2: Rating Standardization Range**
    **Validates: Requirements 1.5**
    
    For any valid recommendation rating string (buy, sell, hold, outperform, 
    underperform, accumulate, reduce, neutral, market perform, strong buy, 
    strong sell), the standardized numeric rating should be in the range [1, 5].
    """
    
    # All valid rating strings from the thesis Table 2
    VALID_RATINGS = [
        # Grade 5 = Buy
        'buy', 'strong buy', 'add', 'accumulate',
        # Grade 4 = Overweight
        'outperform', 'overweight', 'overwt/in-line',
        # Grade 3 = Hold
        'hold', 'market perform', 'neutral',
        # Grade 2 = Underweight
        'underperform', 'underweight',
        # Grade 1 = Sell
        'reduce', 'sell', 'strong sell',
    ]
    
    # Expected mappings for verification
    EXPECTED_MAPPINGS = {
        'buy': 5, 'strong buy': 5, 'add': 5, 'accumulate': 5,
        'outperform': 4, 'overweight': 4, 'overwt/in-line': 4,
        'hold': 3, 'market perform': 3, 'neutral': 3,
        'underperform': 2, 'underweight': 2,
        'reduce': 1, 'sell': 1, 'strong sell': 1,
    }
    
    @settings(max_examples=100)
    @given(rating=st.sampled_from(VALID_RATINGS))
    def test_rating_standardization_in_range(self, rating):
        """
        **Feature: data-management-refactor, Property 2: Rating Standardization Range**
        **Validates: Requirements 1.5**
        
        All valid ratings should produce a numeric value in [1, 5].
        """
        transformer = DataTransformer()
        
        # Standardize the rating
        numeric_rating = transformer.standardize_rating(rating)
        
        # Property: Rating should be in valid range [1, 5]
        assert numeric_rating is not None, f"Rating '{rating}' returned None"
        assert 1 <= numeric_rating <= 5, \
            f"Rating '{rating}' standardized to {numeric_rating}, which is outside [1, 5]"
    
    @settings(max_examples=100)
    @given(rating=st.sampled_from(VALID_RATINGS))
    def test_rating_standardization_is_integer(self, rating):
        """
        **Feature: data-management-refactor, Property 2: Rating Standardization Range**
        **Validates: Requirements 1.5**
        
        All standardized ratings should be integers.
        """
        transformer = DataTransformer()
        
        # Standardize the rating
        numeric_rating = transformer.standardize_rating(rating)
        
        # Property: Rating should be an integer
        assert numeric_rating is not None, f"Rating '{rating}' returned None"
        assert isinstance(numeric_rating, int), \
            f"Rating '{rating}' standardized to {numeric_rating}, which is not an integer"
    
    @settings(max_examples=100)
    @given(rating=st.sampled_from(VALID_RATINGS))
    def test_rating_standardization_correct_mapping(self, rating):
        """
        **Feature: data-management-refactor, Property 2: Rating Standardization Range**
        **Validates: Requirements 1.5**
        
        Each rating should map to its expected numeric value per thesis Table 2.
        """
        transformer = DataTransformer()
        
        # Standardize the rating
        numeric_rating = transformer.standardize_rating(rating)
        
        # Property: Rating should match expected mapping
        expected = self.EXPECTED_MAPPINGS[rating]
        assert numeric_rating == expected, \
            f"Rating '{rating}' standardized to {numeric_rating}, expected {expected}"
    
    @settings(max_examples=100)
    @given(
        rating=st.sampled_from(VALID_RATINGS),
        case_variation=st.sampled_from(['lower', 'upper', 'title', 'mixed'])
    )
    def test_rating_standardization_case_insensitive(self, rating, case_variation):
        """
        **Feature: data-management-refactor, Property 2: Rating Standardization Range**
        **Validates: Requirements 1.5**
        
        Rating standardization should be case-insensitive.
        """
        transformer = DataTransformer()
        
        # Apply case variation
        if case_variation == 'lower':
            test_rating = rating.lower()
        elif case_variation == 'upper':
            test_rating = rating.upper()
        elif case_variation == 'title':
            test_rating = rating.title()
        else:  # mixed
            test_rating = ''.join(
                c.upper() if i % 2 == 0 else c.lower() 
                for i, c in enumerate(rating)
            )
        
        # Standardize the rating
        numeric_rating = transformer.standardize_rating(test_rating)
        
        # Property: Should produce same result regardless of case
        expected = self.EXPECTED_MAPPINGS[rating]
        assert numeric_rating == expected, \
            f"Rating '{test_rating}' (from '{rating}') standardized to {numeric_rating}, expected {expected}"
    
    @settings(max_examples=100)
    @given(
        rating=st.sampled_from(VALID_RATINGS),
        whitespace=st.sampled_from(['', ' ', '  ', '\t', ' \t '])
    )
    def test_rating_standardization_whitespace_tolerant(self, rating, whitespace):
        """
        **Feature: data-management-refactor, Property 2: Rating Standardization Range**
        **Validates: Requirements 1.5**
        
        Rating standardization should handle leading/trailing whitespace.
        """
        transformer = DataTransformer()
        
        # Add whitespace
        test_rating = whitespace + rating + whitespace
        
        # Standardize the rating
        numeric_rating = transformer.standardize_rating(test_rating)
        
        # Property: Should produce same result regardless of whitespace
        expected = self.EXPECTED_MAPPINGS[rating]
        assert numeric_rating == expected, \
            f"Rating '{test_rating}' standardized to {numeric_rating}, expected {expected}"
    
    @settings(max_examples=100)
    @given(
        ratings=st.lists(
            st.sampled_from(VALID_RATINGS),
            min_size=1,
            max_size=50
        )
    )
    def test_batch_rating_standardization(self, ratings):
        """
        **Feature: data-management-refactor, Property 2: Rating Standardization Range**
        **Validates: Requirements 1.5**
        
        Batch rating standardization should produce valid results for all records.
        """
        transformer = DataTransformer()
        
        # Create DataFrame with ratings
        df = pd.DataFrame({
            'ticker': [f'TICK{i:03d}' for i in range(len(ratings))],
            'recommendation': ratings,
            'issue_date': pd.date_range('2024-01-01', periods=len(ratings))
        })
        
        # Standardize batch
        result = transformer.standardize_ratings_batch(df, 'recommendation')
        
        # Property: All ratings should be valid
        assert result.is_valid, f"Batch standardization had {result.invalid_records} invalid records"
        assert result.total_records == len(ratings)
        assert result.valid_records == len(ratings)
        
        # Property: All numeric ratings should be in [1, 5]
        for idx, row in result.data.iterrows():
            numeric = row['rating_numeric']
            assert numeric is not None, f"Row {idx} has None rating"
            assert 1 <= numeric <= 5, f"Row {idx} has rating {numeric} outside [1, 5]"
