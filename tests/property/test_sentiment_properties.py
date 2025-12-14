"""
Property-based tests for sentiment engine components.

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
from sentiment_engine import SentimentEngine


class TestSentimentProperties:
    """Property-based tests for sentiment calculations."""
    
    @settings(max_examples=100)
    @given(
        n_days=st.integers(min_value=20, max_value=100),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_rsi_range_invariant(self, n_days, seed):
        """
        **Feature: sentimentalpha-vietnam, Property 5: RSI Range Invariant**
        **Validates: Requirements 2.1**
        
        For any valid price series with at least 14 data points, 
        the calculated RSI should be in the range [0, 100].
        """
        np.random.seed(seed)
        
        # Generate random price series (positive values)
        # Use random walk to create realistic price movements
        initial_price = np.random.uniform(1000, 50000)
        returns = np.random.normal(0, 0.02, n_days)  # 2% daily volatility
        prices = initial_price * np.exp(np.cumsum(returns))
        
        price_series = pd.Series(prices)
        
        # Calculate RSI
        engine = SentimentEngine()
        rsi = engine.calculate_rsi(price_series)
        
        # Drop NaN values (first few values will be NaN due to lookback period)
        valid_rsi = rsi.dropna()
        
        # Check that all valid RSI values are in [0, 100]
        assert len(valid_rsi) > 0, "RSI should produce at least some valid values"
        assert all(0 <= r <= 100 for r in valid_rsi), \
            f"RSI values outside [0, 100] range: min={valid_rsi.min()}, max={valid_rsi.max()}"
    
    @settings(max_examples=100)
    @given(
        n_days=st.integers(min_value=10, max_value=100),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_bsi_range_invariant(self, n_days, seed):
        """
        **Feature: sentimentalpha-vietnam, Property 6: BSI Range Invariant**
        **Validates: Requirements 2.2**
        
        For any non-negative buy_volume and sell_volume where at least one is positive,
        BSI should be in the range [0, 1].
        """
        np.random.seed(seed)
        
        # Generate random buy and sell volumes
        buy_volumes = np.random.uniform(0, 1000000, n_days)
        sell_volumes = np.random.uniform(0, 1000000, n_days)
        
        # Ensure at least some non-zero volumes
        # (hypothesis will generate some cases with zeros naturally)
        buy_series = pd.Series(buy_volumes)
        sell_series = pd.Series(sell_volumes)
        
        # Calculate BSI
        engine = SentimentEngine()
        bsi = engine.calculate_bsi(buy_series, sell_series)
        
        # Check that all BSI values are in [0, 1]
        assert all(0 <= b <= 1 for b in bsi), \
            f"BSI values outside [0, 1] range: min={bsi.min()}, max={bsi.max()}"
        
        # Check that BSI handles zero volumes correctly
        # When both are zero, should return 0.5 (neutral)
        zero_mask = (buy_series == 0) & (sell_series == 0)
        if zero_mask.any():
            assert all(bsi[zero_mask] == 0.5), \
                "BSI should return 0.5 when both buy and sell volumes are 0"
    
    @settings(max_examples=100)
    @given(
        n_days=st.integers(min_value=20, max_value=100),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_atr_non_negativity(self, n_days, seed):
        """
        **Feature: sentimentalpha-vietnam, Property 7: ATR Non-Negativity**
        **Validates: Requirements 2.3**
        
        For any valid OHLC price data, ATR should always be non-negative.
        """
        np.random.seed(seed)
        
        # Generate realistic OHLC data
        # Start with close prices
        initial_price = np.random.uniform(1000, 50000)
        returns = np.random.normal(0, 0.02, n_days)
        close_prices = initial_price * np.exp(np.cumsum(returns))
        
        # Generate high and low based on close
        # High is close + some positive amount
        # Low is close - some positive amount
        high_offset = np.random.uniform(0, 0.05, n_days) * close_prices
        low_offset = np.random.uniform(0, 0.05, n_days) * close_prices
        
        high_prices = close_prices + high_offset
        low_prices = close_prices - low_offset
        
        # Ensure high >= low (should be guaranteed by construction, but double-check)
        high_prices = np.maximum(high_prices, low_prices)
        
        high_series = pd.Series(high_prices)
        low_series = pd.Series(low_prices)
        close_series = pd.Series(close_prices)
        
        # Calculate ATR
        engine = SentimentEngine()
        atr = engine.calculate_atr(high_series, low_series, close_series)
        
        # Drop NaN values
        valid_atr = atr.dropna()
        
        # Check that all ATR values are non-negative
        assert len(valid_atr) > 0, "ATR should produce at least some valid values"
        assert all(a >= 0 for a in valid_atr), \
            f"ATR values should be non-negative: min={valid_atr.min()}"
    
    @settings(max_examples=100)
    @given(
        n_days=st.integers(min_value=20, max_value=100),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_pli_range_invariant(self, n_days, seed):
        """
        **Feature: sentimentalpha-vietnam, Property 8: PLI Range Invariant**
        **Validates: Requirements 2.5**
        
        For any price series with at least 14 data points, 
        PLI should be in the range [0, 1].
        """
        np.random.seed(seed)
        
        # Generate random price series
        initial_price = np.random.uniform(1000, 50000)
        returns = np.random.normal(0, 0.02, n_days)
        prices = initial_price * np.exp(np.cumsum(returns))
        
        price_series = pd.Series(prices)
        
        # Calculate PLI
        engine = SentimentEngine()
        pli = engine.calculate_pli(price_series)
        
        # Drop NaN values
        valid_pli = pli.dropna()
        
        # Check that all PLI values are in [0, 1]
        assert len(valid_pli) > 0, "PLI should produce at least some valid values"
        assert all(0 <= p <= 1 for p in valid_pli), \
            f"PLI values outside [0, 1] range: min={valid_pli.min()}, max={valid_pli.max()}"
    
    @settings(max_examples=100)
    @given(
        n_rows=st.integers(min_value=20, max_value=100),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_pca_output_length_preservation(self, n_rows, seed):
        """
        **Feature: sentimentalpha-vietnam, Property 9: PCA Output Length Preservation**
        **Validates: Requirements 2.6**
        
        For any input DataFrame with N rows, PCA sentiment index output 
        should also have N rows.
        """
        np.random.seed(seed)
        
        # Generate random sentiment proxy data
        # Create realistic proxy values in their expected ranges
        rsi = np.random.uniform(0, 100, n_rows)
        bsi = np.random.uniform(0, 1, n_rows)
        atr = np.random.uniform(0, 1000, n_rows)
        ltv = np.random.uniform(0, 20, n_rows)  # log of volume
        pli = np.random.uniform(0, 1, n_rows)
        
        # Create DataFrame
        proxies = pd.DataFrame({
            'rsi': rsi,
            'bsi': bsi,
            'atr': atr,
            'ltv': ltv,
            'pli': pli
        })
        
        # Apply PCA
        engine = SentimentEngine()
        sentiment_index = engine.construct_sentiment_index(proxies)
        
        # Check that output has same length as input
        assert len(sentiment_index) == len(proxies), \
            f"PCA output length {len(sentiment_index)} doesn't match input length {len(proxies)}"
        
        # Check that output is a Series
        assert isinstance(sentiment_index, pd.Series), \
            "PCA output should be a pandas Series"
        
        # Check that we have some valid (non-NaN) values
        valid_count = sentiment_index.notna().sum()
        assert valid_count > 0, "PCA should produce at least some valid values"
    
    @settings(max_examples=100)
    @given(
        n_days=st.integers(min_value=30, max_value=100),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_pure_sentiment_orthogonality(self, n_days, seed):
        """
        **Feature: sentimentalpha-vietnam, Property 10: Pure Sentiment Orthogonality**
        **Validates: Requirements 2.7**
        
        For any purified sentiment series, the correlation with market returns 
        should be approximately zero (within statistical tolerance).
        """
        np.random.seed(seed)
        
        # Generate random market returns
        market_returns = np.random.normal(0, 0.02, n_days)
        
        # Generate raw sentiment that is correlated with market returns
        # raw_sentiment = beta * market_returns + noise
        beta = np.random.uniform(-2, 2)
        noise = np.random.normal(0, 1, n_days)
        raw_sentiment = beta * market_returns + noise
        
        market_series = pd.Series(market_returns)
        sentiment_series = pd.Series(raw_sentiment)
        
        # Purify sentiment
        engine = SentimentEngine()
        pure_sentiment = engine.purify_sentiment(sentiment_series, market_series)
        
        # Drop NaN values
        combined = pd.DataFrame({
            'pure_sentiment': pure_sentiment,
            'market_returns': market_series
        }).dropna()
        
        # Check that we have enough data
        assert len(combined) >= 10, "Should have at least 10 valid data points"
        
        # Calculate correlation between pure sentiment and market returns
        correlation = combined['pure_sentiment'].corr(combined['market_returns'])
        
        # The correlation should be very close to zero
        # We use a tolerance based on statistical significance
        # For a sample size of 30+, correlation < 0.3 is generally considered weak
        # For residuals from regression, we expect even closer to zero
        tolerance = 0.15  # Allow small correlation due to numerical precision
        
        assert abs(correlation) < tolerance, \
            f"Pure sentiment correlation with market returns is {correlation:.4f}, " \
            f"which exceeds tolerance of {tolerance}. " \
            f"Pure sentiment should be orthogonal to market returns."
