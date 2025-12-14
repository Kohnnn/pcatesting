"""
SentimentEngine class for calculating sentiment proxies and constructing sentiment index.
"""
import pandas as pd
import numpy as np
from typing import Optional
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


class SentimentEngine:
    """Calculates sentiment proxies and constructs sentiment index."""
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index.
        
        RSI measures the speed and magnitude of price changes.
        Formula: RSI = 100 - (100 / (1 + RS))
        where RS = Average Gain / Average Loss over the period
        
        Args:
            prices: Series of closing prices
            period: Lookback period (default 14 days)
            
        Returns:
            Series of RSI values (0-100 range)
        """
        # Calculate price changes
        delta = prices.diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0.0)
        losses = -delta.where(delta < 0, 0.0)
        
        # Calculate average gains and losses using exponential moving average
        avg_gains = gains.ewm(span=period, adjust=False, min_periods=period).mean()
        avg_losses = losses.ewm(span=period, adjust=False, min_periods=period).mean()
        
        # Calculate RS (Relative Strength)
        rs = avg_gains / avg_losses
        
        # Calculate RSI
        rsi = 100 - (100 / (1 + rs))
        
        # Handle edge cases where avg_losses is 0
        rsi = rsi.fillna(100)  # If no losses, RSI = 100
        
        return rsi
    
    def calculate_bsi(self, buy_vol: pd.Series, sell_vol: pd.Series) -> pd.Series:
        """
        Calculate Buy-Sell Imbalance.
        
        BSI measures buying pressure as a ratio of buy volume to total volume.
        Formula: BSI = buy_volume / (buy_volume + sell_volume)
        
        Args:
            buy_vol: Series of buy volumes
            sell_vol: Series of sell volumes
            
        Returns:
            Series of BSI values (0-1 range)
        """
        total_vol = buy_vol + sell_vol
        
        # Calculate BSI
        bsi = buy_vol / total_vol
        
        # Handle edge cases where total volume is 0
        # Return 0.5 (neutral) when both buy and sell are 0
        bsi = bsi.fillna(0.5)
        
        return bsi
    
    def calculate_atr(
        self, 
        high: pd.Series, 
        low: pd.Series, 
        close: pd.Series, 
        period: int = 14
    ) -> pd.Series:
        """
        Calculate Average True Range.
        
        ATR measures market volatility by calculating the average of true ranges.
        True Range = max(high - low, abs(high - prev_close), abs(low - prev_close))
        
        Args:
            high: Series of high prices
            low: Series of low prices
            close: Series of closing prices
            period: Lookback period (default 14 days)
            
        Returns:
            Series of ATR values (always non-negative)
        """
        # Calculate previous close
        prev_close = close.shift(1)
        
        # Calculate true range components
        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()
        
        # True range is the maximum of the three
        true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Calculate ATR using exponential moving average
        atr = true_range.ewm(span=period, adjust=False, min_periods=period).mean()
        
        return atr
    
    def calculate_ltv(self, volume: pd.Series) -> pd.Series:
        """
        Calculate Log Trading Volume.
        
        LTV normalizes trading volume using natural logarithm to reduce
        the impact of extreme values.
        
        Args:
            volume: Series of trading volumes
            
        Returns:
            Series of log-transformed volumes
        """
        # Add small constant to avoid log(0)
        # Use log1p which computes log(1 + x) for numerical stability
        ltv = np.log1p(volume)
        
        return ltv
    
    def calculate_pli(self, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Psychological Line Index.
        
        PLI measures the proportion of recent trading days with price increases.
        Formula: PLI = (number of up days in period) / period
        
        Args:
            close: Series of closing prices
            period: Lookback period (default 14 days)
            
        Returns:
            Series of PLI values (0-1 range)
        """
        # Calculate price changes
        price_change = close.diff()
        
        # Create binary indicator: 1 for up days, 0 for down days
        up_days = (price_change > 0).astype(int)
        
        # Calculate rolling sum of up days
        up_count = up_days.rolling(window=period, min_periods=period).sum()
        
        # Calculate PLI as proportion
        pli = up_count / period
        
        return pli
    
    def construct_sentiment_index(self, proxies: pd.DataFrame) -> pd.Series:
        """
        Apply PCA to extract first principal component as raw sentiment.
        
        This method takes multiple sentiment proxies (RSI, BSI, ATR, LTV, PLI)
        and reduces them to a single sentiment index using Principal Component Analysis.
        
        Args:
            proxies: DataFrame with sentiment proxy columns (rsi, bsi, atr, ltv, pli)
                     Each row represents a time period (e.g., daily data)
                     
        Returns:
            Series of raw sentiment index values (first principal component)
        """
        # Drop rows with any NaN values
        clean_proxies = proxies.dropna()
        
        if len(clean_proxies) == 0:
            # If no valid data, return empty series
            return pd.Series(dtype=float)
        
        # Standardize the features (mean=0, std=1)
        # This is important for PCA to give equal weight to all proxies
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(clean_proxies)
        
        # Apply PCA and extract first principal component
        pca = PCA(n_components=1)
        first_pc = pca.fit_transform(scaled_data)
        
        # Convert to Series with original index
        sentiment_index = pd.Series(
            first_pc.flatten(),
            index=clean_proxies.index,
            name='raw_sentiment'
        )
        
        # Reindex to match original proxies DataFrame (will have NaN for dropped rows)
        sentiment_index = sentiment_index.reindex(proxies.index)
        
        return sentiment_index
    
    def purify_sentiment(
        self, 
        raw_sentiment: pd.Series, 
        market_returns: pd.Series
    ) -> pd.Series:
        """
        Purify sentiment by regressing against market returns.
        
        This method removes the market-related component from sentiment,
        isolating firm-specific sentiment. The residuals from the regression
        represent "pure sentiment" that is orthogonal to market movements.
        
        Args:
            raw_sentiment: Series of raw sentiment index values
            market_returns: Series of market excess returns (e.g., VNIndex returns)
                           Must have same index as raw_sentiment
                           
        Returns:
            Series of pure sentiment values (residuals from regression)
        """
        # Align the two series and drop NaN values
        combined = pd.DataFrame({
            'sentiment': raw_sentiment,
            'market_returns': market_returns
        }).dropna()
        
        if len(combined) < 2:
            # Not enough data for regression, return empty series
            return pd.Series(dtype=float, index=raw_sentiment.index)
        
        # Perform linear regression: sentiment = alpha + beta * market_returns + residual
        # We use numpy's polyfit for simple linear regression
        X = combined['market_returns'].values
        y = combined['sentiment'].values
        
        # Fit linear model: y = beta * X + alpha
        coefficients = np.polyfit(X, y, deg=1)
        beta = coefficients[0]
        alpha = coefficients[1]
        
        # Calculate predicted sentiment
        predicted = alpha + beta * X
        
        # Calculate residuals (pure sentiment)
        residuals = y - predicted
        
        # Create Series with residuals
        pure_sentiment = pd.Series(
            residuals,
            index=combined.index,
            name='pure_sentiment'
        )
        
        # Reindex to match original raw_sentiment (will have NaN for dropped rows)
        pure_sentiment = pure_sentiment.reindex(raw_sentiment.index)
        
        return pure_sentiment
