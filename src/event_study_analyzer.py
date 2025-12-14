"""
EventStudyAnalyzer class for performing event study analysis.
"""
import pandas as pd
import numpy as np
from typing import Tuple, Optional
from scipy import stats


class EventStudyAnalyzer:
    """Performs event study analysis for CAR and CAS."""
    
    def calculate_abnormal_returns(
        self,
        returns: pd.Series,
        market_returns: pd.Series
    ) -> pd.Series:
        """
        Calculate abnormal returns using market model.
        
        The market model estimates expected returns based on market movements:
        Expected Return = alpha + beta * Market Return
        Abnormal Return = Actual Return - Expected Return
        
        Args:
            returns: Series of actual stock returns
            market_returns: Series of market returns (e.g., VNIndex returns)
                           Must have same index as returns
                           
        Returns:
            Series of abnormal returns
        """
        # Align the two series and drop NaN values
        combined = pd.DataFrame({
            'returns': returns,
            'market_returns': market_returns
        }).dropna()
        
        if len(combined) < 2:
            # Not enough data for regression, return empty series
            return pd.Series(dtype=float, index=returns.index)
        
        # Perform linear regression: returns = alpha + beta * market_returns + residual
        X = combined['market_returns'].values
        y = combined['returns'].values
        
        # Fit linear model: y = beta * X + alpha
        coefficients = np.polyfit(X, y, deg=1)
        beta = coefficients[0]
        alpha = coefficients[1]
        
        # Calculate expected returns
        expected_returns = alpha + beta * X
        
        # Calculate abnormal returns (residuals)
        abnormal_returns = y - expected_returns
        
        # Create Series with abnormal returns
        abnormal_returns_series = pd.Series(
            abnormal_returns,
            index=combined.index,
            name='abnormal_returns'
        )
        
        # Reindex to match original returns (will have NaN for dropped rows)
        abnormal_returns_series = abnormal_returns_series.reindex(returns.index)
        
        return abnormal_returns_series
    
    def calculate_car(
        self,
        abnormal_returns: pd.Series,
        event_date: pd.Timestamp,
        window: Tuple[int, int] = (-25, 25)
    ) -> pd.DataFrame:
        """
        Calculate Cumulative Abnormal Returns over event window.
        
        CAR is the sum of abnormal returns from the start of the event window
        to each day in the window. This measures the cumulative price reaction
        to an event (e.g., analyst recommendation).
        
        Args:
            abnormal_returns: Series of abnormal returns with date index
            event_date: Date of the event (day 0)
            window: Tuple of (start_day, end_day) relative to event_date
                   Default is (-25, 25) for 25 days before and after
                   
        Returns:
            DataFrame with columns:
                - day: Days relative to event (e.g., -25 to 25)
                - car: Cumulative abnormal return at each day
        """
        # Ensure abnormal_returns has a datetime index
        if not isinstance(abnormal_returns.index, pd.DatetimeIndex):
            abnormal_returns.index = pd.to_datetime(abnormal_returns.index)
        
        # Ensure event_date is a Timestamp
        if not isinstance(event_date, pd.Timestamp):
            event_date = pd.Timestamp(event_date)
        
        # Sort by date
        abnormal_returns = abnormal_returns.sort_index()
        
        # Get all dates in the series
        all_dates = abnormal_returns.index
        
        # Find the event date or the closest date after it
        event_idx = all_dates.searchsorted(event_date)
        
        if event_idx >= len(all_dates):
            # Event date is after all data
            return pd.DataFrame(columns=['day', 'car'])
        
        # Get the actual event date from the data
        actual_event_date = all_dates[event_idx]
        
        # Calculate the window dates
        start_day, end_day = window
        
        # Get indices for the window
        start_idx = max(0, event_idx + start_day)
        end_idx = min(len(all_dates) - 1, event_idx + end_day)
        
        # Extract abnormal returns in the window
        window_returns = abnormal_returns.iloc[start_idx:end_idx + 1]
        
        # Calculate cumulative sum
        car_values = window_returns.cumsum()
        
        # Calculate day numbers relative to event
        window_dates = window_returns.index
        day_numbers = [(date - actual_event_date).days for date in window_dates]
        
        # Create result DataFrame
        result = pd.DataFrame({
            'day': day_numbers,
            'car': car_values.values
        })
        
        return result
    
    def calculate_cas(
        self,
        sentiment: pd.Series,
        event_date: pd.Timestamp,
        window: Tuple[int, int] = (-25, 25)
    ) -> pd.DataFrame:
        """
        Calculate Cumulative Abnormal Sentiment over event window.
        
        CAS is similar to CAR but for sentiment instead of returns.
        It measures the cumulative sentiment reaction to an event.
        
        For sentiment, "abnormal" means deviation from the mean sentiment.
        
        Args:
            sentiment: Series of sentiment values with date index
            event_date: Date of the event (day 0)
            window: Tuple of (start_day, end_day) relative to event_date
                   Default is (-25, 25) for 25 days before and after
                   
        Returns:
            DataFrame with columns:
                - day: Days relative to event (e.g., -25 to 25)
                - cas: Cumulative abnormal sentiment at each day
        """
        # Ensure sentiment has a datetime index
        if not isinstance(sentiment.index, pd.DatetimeIndex):
            sentiment.index = pd.to_datetime(sentiment.index)
        
        # Ensure event_date is a Timestamp
        if not isinstance(event_date, pd.Timestamp):
            event_date = pd.Timestamp(event_date)
        
        # Sort by date
        sentiment = sentiment.sort_index()
        
        # Calculate abnormal sentiment (deviation from mean)
        mean_sentiment = sentiment.mean()
        abnormal_sentiment = sentiment - mean_sentiment
        
        # Get all dates in the series
        all_dates = sentiment.index
        
        # Find the event date or the closest date after it
        event_idx = all_dates.searchsorted(event_date)
        
        if event_idx >= len(all_dates):
            # Event date is after all data
            return pd.DataFrame(columns=['day', 'cas'])
        
        # Get the actual event date from the data
        actual_event_date = all_dates[event_idx]
        
        # Calculate the window dates
        start_day, end_day = window
        
        # Get indices for the window
        start_idx = max(0, event_idx + start_day)
        end_idx = min(len(all_dates) - 1, event_idx + end_day)
        
        # Extract abnormal sentiment in the window
        window_sentiment = abnormal_sentiment.iloc[start_idx:end_idx + 1]
        
        # Calculate cumulative sum
        cas_values = window_sentiment.cumsum()
        
        # Calculate day numbers relative to event
        window_dates = window_sentiment.index
        day_numbers = [(date - actual_event_date).days for date in window_dates]
        
        # Create result DataFrame
        result = pd.DataFrame({
            'day': day_numbers,
            'cas': cas_values.values
        })
        
        return result
    
    def perform_t_test(self, values: pd.Series) -> Tuple[float, float]:
        """
        Perform t-test and return t-statistic and p-value.
        
        This tests whether the mean of the values is significantly different
        from zero (one-sample t-test).
        
        Args:
            values: Series of values to test (e.g., CAR or CAS values)
            
        Returns:
            Tuple of (t_statistic, p_value)
        """
        # Drop NaN values
        clean_values = values.dropna()
        
        if len(clean_values) < 2:
            # Not enough data for t-test
            return (np.nan, np.nan)
        
        # Perform one-sample t-test against mean of 0
        t_statistic, p_value = stats.ttest_1samp(clean_values, 0)
        
        return (t_statistic, p_value)
