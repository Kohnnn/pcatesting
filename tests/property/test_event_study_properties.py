"""
Property-based tests for event study analysis components.

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
from event_study_analyzer import EventStudyAnalyzer


class TestEventStudyProperties:
    """Property-based tests for event study analysis."""
    
    @settings(max_examples=100)
    @given(
        n_days=st.integers(min_value=60, max_value=150),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_car_cumulative_sum(self, n_days, seed):
        """
        **Feature: sentimentalpha-vietnam, Property 13: CAR Cumulative Sum**
        **Validates: Requirements 4.2**
        
        For any event window, CAR at day T should equal the sum of abnormal returns
        from the start of the window to day T.
        """
        np.random.seed(seed)
        
        # Generate random abnormal returns
        abnormal_returns = np.random.normal(0, 0.02, n_days)
        
        # Create date index
        start_date = pd.Timestamp('2020-01-01')
        dates = pd.date_range(start=start_date, periods=n_days, freq='D')
        
        # Create Series
        ar_series = pd.Series(abnormal_returns, index=dates)
        
        # Set event date (ensure it's within bounds and has enough data on both sides)
        # We need at least 25 days before and after for the full window
        # For n_days=60, we can use indices 30 to 29 (not valid), so we need to ensure n_days > 60
        max_offset = min(n_days - 30, n_days - 1)
        if max_offset <= 30:
            # Not enough data, use middle
            event_day_offset = n_days // 2
        else:
            event_day_offset = np.random.randint(30, max_offset)
        event_date = dates[event_day_offset]
        
        # Calculate CAR
        analyzer = EventStudyAnalyzer()
        car_df = analyzer.calculate_car(ar_series, event_date, window=(-25, 25))
        
        # Skip if no data returned (edge case)
        assume(len(car_df) > 0)
        
        # For each day in the CAR result, verify it equals the cumulative sum
        # Get the abnormal returns in the event window
        event_idx = dates.get_loc(event_date)
        start_idx = max(0, event_idx - 25)
        end_idx = min(len(dates) - 1, event_idx + 25)
        
        window_returns = ar_series.iloc[start_idx:end_idx + 1]
        
        # Calculate expected cumulative sum
        expected_car = window_returns.cumsum()
        
        # Compare with actual CAR values
        # Note: We need to match by position since day numbers might not align perfectly
        # due to missing dates or edge effects
        actual_car = car_df['car'].values
        
        # The length should match
        assert len(actual_car) == len(expected_car), \
            f"CAR length {len(actual_car)} doesn't match expected {len(expected_car)}"
        
        # Each CAR value should equal the cumulative sum up to that point
        for i in range(len(actual_car)):
            expected_value = expected_car.iloc[i]
            actual_value = actual_car[i]
            
            # Allow small numerical tolerance
            assert abs(actual_value - expected_value) < 1e-10, \
                f"CAR at position {i} is {actual_value}, expected {expected_value}"
    
    @settings(max_examples=100)
    @given(
        n_days=st.integers(min_value=60, max_value=150),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_event_window_length(self, n_days, seed):
        """
        **Feature: sentimentalpha-vietnam, Property 14: Event Window Length**
        **Validates: Requirements 4.5**
        
        For any event study with window (-25, +25), the output should contain
        exactly 51 data points (assuming sufficient data exists).
        """
        np.random.seed(seed)
        
        # Generate random abnormal returns
        abnormal_returns = np.random.normal(0, 0.02, n_days)
        
        # Create date index
        start_date = pd.Timestamp('2020-01-01')
        dates = pd.date_range(start=start_date, periods=n_days, freq='D')
        
        # Create Series
        ar_series = pd.Series(abnormal_returns, index=dates)
        
        # Set event date (ensure we have enough data on both sides)
        # We need at least 25 days before and after for the full window
        max_offset = min(n_days - 30, n_days - 1)
        if max_offset <= 30:
            # Not enough data, use middle
            event_day_offset = n_days // 2
        else:
            event_day_offset = np.random.randint(30, max_offset)
        event_date = dates[event_day_offset]
        
        # Calculate CAR with window (-25, 25)
        analyzer = EventStudyAnalyzer()
        car_df = analyzer.calculate_car(ar_series, event_date, window=(-25, 25))
        
        # Check the length
        # The window (-25, 25) should give us 51 days: -25, -24, ..., 0, ..., 24, 25
        # However, if we're near the edges of the data, we might get fewer
        
        # Calculate expected length based on available data
        event_idx = dates.get_loc(event_date)
        start_idx = max(0, event_idx - 25)
        end_idx = min(len(dates) - 1, event_idx + 25)
        expected_length = end_idx - start_idx + 1
        
        actual_length = len(car_df)
        
        assert actual_length == expected_length, \
            f"Event window length is {actual_length}, expected {expected_length}"
        
        # If we have full data (not near edges), should be exactly 51
        if event_idx >= 25 and event_idx + 25 < len(dates):
            assert actual_length == 51, \
                f"With full data, event window should have 51 points, got {actual_length}"
        
        # Test the same for CAS
        sentiment = np.random.normal(0, 1, n_days)
        sentiment_series = pd.Series(sentiment, index=dates)
        
        cas_df = analyzer.calculate_cas(sentiment_series, event_date, window=(-25, 25))
        
        assert len(cas_df) == expected_length, \
            f"CAS window length is {len(cas_df)}, expected {expected_length}"
        
        if event_idx >= 25 and event_idx + 25 < len(dates):
            assert len(cas_df) == 51, \
                f"With full data, CAS window should have 51 points, got {len(cas_df)}"
