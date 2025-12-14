"""
AlphaGenerator class for generating trading signals based on sentiment and analyst actions.
"""
import pandas as pd
import numpy as np
from typing import Optional


class AlphaGenerator:
    """Generates trading signals based on sentiment and analyst actions."""
    
    def classify_signal(
        self,
        action: str,
        pure_sentiment: Optional[float],
        nfb: Optional[float],
        rsi: Optional[float],
        bsi: Optional[float],
        sentiment_slope: Optional[float]
    ) -> str:
        """
        Classify signal type based on conditions.
        
        Signal Classification Rules:
        1. Contrarian Dip Buy: downgrade AND pure_sentiment > 1.0 AND nfb > 0
        2. Momentum Breakout: upgrade AND sentiment_slope > 0 AND rsi < 70
        3. Retail Trap: downgrade AND bsi > 0 AND nfb < 0
        4. Neutral / No Edge: all other conditions
        
        Args:
            action: Analyst action ('upgrade' or 'downgrade')
            pure_sentiment: Pure sentiment score
            nfb: Net foreign buy (positive = foreign buying, negative = foreign selling)
            rsi: Relative Strength Index (0-100)
            bsi: Buy-Sell Imbalance (0-1)
            sentiment_slope: Slope of sentiment trend (positive = rising, negative = falling)
            
        Returns:
            Signal type: 'Contrarian Dip Buy', 'Momentum Breakout', 'Retail Trap', or 'Neutral / No Edge'
        """
        # Normalize action to lowercase for comparison
        action_lower = action.lower() if action else ''
        
        # Check for Contrarian Dip Buy
        # Condition: downgrade AND pure_sentiment > 1.0 AND nfb > 0
        if 'downgrade' in action_lower or 'down' in action_lower:
            if pure_sentiment is not None and pure_sentiment > 1.0:
                if nfb is not None and nfb > 0:
                    return 'Contrarian Dip Buy'
        
        # Check for Momentum Breakout
        # Condition: upgrade AND sentiment_slope > 0 AND rsi < 70
        if 'upgrade' in action_lower or 'up' in action_lower:
            if sentiment_slope is not None and sentiment_slope > 0:
                if rsi is not None and rsi < 70:
                    return 'Momentum Breakout'
        
        # Check for Retail Trap
        # Condition: downgrade AND bsi > 0 AND nfb < 0
        if 'downgrade' in action_lower or 'down' in action_lower:
            if bsi is not None and bsi > 0:
                if nfb is not None and nfb < 0:
                    return 'Retail Trap'
        
        # Default to Neutral / No Edge
        return 'Neutral / No Edge'
    
    def generate_signals(
        self,
        recommendations: pd.DataFrame,
        sentiment: pd.DataFrame,
        market_data: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Generate signals for all recommendation events.
        
        This method processes analyst recommendations and combines them with
        sentiment data to generate trading signals.
        
        Args:
            recommendations: DataFrame with columns:
                - ticker: Stock ticker
                - issue_date: Date of recommendation
                - rating_numeric: Numeric rating (1-5)
                - recommendation: Original recommendation text
                - (optional) id: Recommendation ID
            sentiment: DataFrame with columns:
                - ticker: Stock ticker
                - date: Date
                - pure_sentiment: Pure sentiment score
                - rsi: RSI value
                - bsi: BSI value
            market_data: Optional DataFrame with columns:
                - ticker: Stock ticker
                - date: Date
                - buy_volume: Buy volume
                - sell_volume: Sell volume
                
        Returns:
            DataFrame with columns:
                - ticker: Stock ticker
                - date: Signal date (recommendation issue date)
                - signal_type: Type of signal
                - sentiment_score: Pure sentiment at signal date
                - foreign_flow_score: Net foreign buy score
                - analyst_action: Upgrade/downgrade/initiation
                - recommendation_id: ID of the recommendation (if provided)
        """
        signals = []
        
        # Sort recommendations by ticker and date
        recs = recommendations.sort_values(['ticker', 'issue_date']).reset_index(drop=True)
        
        for idx, rec in recs.iterrows():
            ticker = rec['ticker']
            issue_date = rec['issue_date']
            rating = rec['rating_numeric']
            
            # Determine analyst action by comparing to previous rating
            prev_recs = recs[
                (recs['ticker'] == ticker) & 
                (recs['issue_date'] < issue_date)
            ]
            
            if len(prev_recs) > 0:
                prev_rating = prev_recs.iloc[-1]['rating_numeric']
                if rating > prev_rating:
                    action = 'upgrade'
                elif rating < prev_rating:
                    action = 'downgrade'
                else:
                    action = 'reiteration'
            else:
                action = 'initiation'
            
            # Get sentiment data for this ticker at this date
            sentiment_row = sentiment[
                (sentiment['ticker'] == ticker) & 
                (sentiment['date'] == issue_date)
            ]
            
            if len(sentiment_row) == 0:
                # No sentiment data available, use None values
                pure_sentiment = None
                rsi_val = None
                bsi_val = None
            else:
                sentiment_row = sentiment_row.iloc[0]
                pure_sentiment = sentiment_row.get('pure_sentiment')
                rsi_val = sentiment_row.get('rsi')
                bsi_val = sentiment_row.get('bsi')
            
            # Calculate sentiment slope (trend over last 5 days)
            sentiment_history = sentiment[
                (sentiment['ticker'] == ticker) & 
                (sentiment['date'] <= issue_date)
            ].sort_values('date').tail(5)
            
            if len(sentiment_history) >= 2:
                # Simple linear slope calculation
                sentiment_values = sentiment_history['pure_sentiment'].dropna()
                if len(sentiment_values) >= 2:
                    x = np.arange(len(sentiment_values))
                    y = sentiment_values.values
                    # Calculate slope using least squares
                    slope = np.polyfit(x, y, 1)[0]
                    sentiment_slope = slope
                else:
                    sentiment_slope = None
            else:
                sentiment_slope = None
            
            # Calculate net foreign buy (NFB)
            # NFB is calculated from market data if available
            if market_data is not None:
                market_row = market_data[
                    (market_data['ticker'] == ticker) & 
                    (market_data['date'] == issue_date)
                ]
                
                if len(market_row) > 0:
                    market_row = market_row.iloc[0]
                    buy_vol = market_row.get('buy_volume', 0)
                    sell_vol = market_row.get('sell_volume', 0)
                    
                    # NFB = buy_volume - sell_volume
                    # Normalize by total volume to get a score
                    total_vol = buy_vol + sell_vol
                    if total_vol > 0:
                        nfb = (buy_vol - sell_vol) / total_vol
                    else:
                        nfb = 0
                else:
                    nfb = None
            else:
                # If no market data, try to infer from BSI
                # BSI = buy / (buy + sell), so NFB ≈ 2*BSI - 1
                if bsi_val is not None:
                    nfb = 2 * bsi_val - 1
                else:
                    nfb = None
            
            # Classify the signal
            signal_type = self.classify_signal(
                action=action,
                pure_sentiment=pure_sentiment,
                nfb=nfb,
                rsi=rsi_val,
                bsi=bsi_val,
                sentiment_slope=sentiment_slope
            )
            
            # Create signal record
            signal = {
                'ticker': ticker,
                'date': issue_date,
                'signal_type': signal_type,
                'sentiment_score': pure_sentiment,
                'foreign_flow_score': nfb,
                'analyst_action': action,
            }
            
            # Add recommendation_id if available
            if 'id' in rec:
                signal['recommendation_id'] = rec['id']
            
            signals.append(signal)
        
        # Convert to DataFrame
        signals_df = pd.DataFrame(signals)
        
        return signals_df
