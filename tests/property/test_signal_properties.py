"""
Property-based tests for signal generation components.

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
from alpha_generator import AlphaGenerator


class TestSignalProperties:
    """Property-based tests for signal generation."""
    
    @settings(max_examples=100)
    @given(
        action=st.sampled_from(['upgrade', 'downgrade', 'initiation', 'reiteration']),
        pure_sentiment=st.one_of(st.none(), st.floats(min_value=-5, max_value=5)),
        nfb=st.one_of(st.none(), st.floats(min_value=-1, max_value=1)),
        rsi=st.one_of(st.none(), st.floats(min_value=0, max_value=100)),
        bsi=st.one_of(st.none(), st.floats(min_value=0, max_value=1)),
        sentiment_slope=st.one_of(st.none(), st.floats(min_value=-2, max_value=2))
    )
    def test_signal_classification_completeness(
        self, action, pure_sentiment, nfb, rsi, bsi, sentiment_slope
    ):
        """
        **Feature: sentimentalpha-vietnam, Property 11: Signal Classification Completeness**
        **Validates: Requirements 3.1, 3.2, 3.3, 3.4**
        
        For any combination of analyst action and market conditions, 
        exactly one signal type should be assigned (no signal should be unclassified).
        """
        generator = AlphaGenerator()
        
        # Classify the signal
        signal_type = generator.classify_signal(
            action=action,
            pure_sentiment=pure_sentiment,
            nfb=nfb,
            rsi=rsi,
            bsi=bsi,
            sentiment_slope=sentiment_slope
        )
        
        # Check that a signal type was assigned
        assert signal_type is not None, "Signal type should not be None"
        assert isinstance(signal_type, str), "Signal type should be a string"
        assert len(signal_type) > 0, "Signal type should not be empty"
        
        # Check that signal type is one of the valid types
        valid_types = [
            'Contrarian Dip Buy',
            'Momentum Breakout',
            'Retail Trap',
            'Neutral / No Edge'
        ]
        assert signal_type in valid_types, \
            f"Signal type '{signal_type}' is not a valid signal type. " \
            f"Valid types: {valid_types}"
    
    @settings(max_examples=100)
    @given(
        n_signals=st.integers(min_value=1, max_value=20),
        seed=st.integers(min_value=0, max_value=10000)
    )
    def test_signal_required_fields(self, n_signals, seed):
        """
        **Feature: sentimentalpha-vietnam, Property 12: Signal Required Fields**
        **Validates: Requirements 3.5**
        
        For any generated signal, the fields ticker, date, and signal_type 
        should be non-null.
        """
        np.random.seed(seed)
        
        # Generate random recommendations
        tickers = [f'TICK{i}' for i in range(n_signals)]
        dates = pd.date_range('2023-01-01', periods=n_signals, freq='D')
        ratings = np.random.randint(1, 6, n_signals)
        
        recommendations = pd.DataFrame({
            'ticker': tickers,
            'issue_date': dates,
            'rating_numeric': ratings,
            'recommendation': ['buy'] * n_signals,
            'id': range(n_signals)
        })
        
        # Generate random sentiment data
        sentiment_dates = pd.date_range('2022-12-01', periods=n_signals + 30, freq='D')
        sentiment_data = []
        
        for ticker in tickers:
            for date in sentiment_dates:
                sentiment_data.append({
                    'ticker': ticker,
                    'date': date,
                    'pure_sentiment': np.random.uniform(-2, 2),
                    'rsi': np.random.uniform(0, 100),
                    'bsi': np.random.uniform(0, 1)
                })
        
        sentiment = pd.DataFrame(sentiment_data)
        
        # Generate signals
        generator = AlphaGenerator()
        signals = generator.generate_signals(recommendations, sentiment)
        
        # Check that signals were generated
        assert len(signals) > 0, "Should generate at least one signal"
        
        # Check required fields for each signal
        for idx, signal in signals.iterrows():
            # Check ticker is not null
            assert signal['ticker'] is not None, \
                f"Signal {idx}: ticker should not be None"
            assert pd.notna(signal['ticker']), \
                f"Signal {idx}: ticker should not be NaN"
            assert len(str(signal['ticker'])) > 0, \
                f"Signal {idx}: ticker should not be empty"
            
            # Check date is not null
            assert signal['date'] is not None, \
                f"Signal {idx}: date should not be None"
            assert pd.notna(signal['date']), \
                f"Signal {idx}: date should not be NaN"
            
            # Check signal_type is not null
            assert signal['signal_type'] is not None, \
                f"Signal {idx}: signal_type should not be None"
            assert pd.notna(signal['signal_type']), \
                f"Signal {idx}: signal_type should not be NaN"
            assert len(str(signal['signal_type'])) > 0, \
                f"Signal {idx}: signal_type should not be empty"
            
            # Verify signal_type is valid
            valid_types = [
                'Contrarian Dip Buy',
                'Momentum Breakout',
                'Retail Trap',
                'Neutral / No Edge'
            ]
            assert signal['signal_type'] in valid_types, \
                f"Signal {idx}: signal_type '{signal['signal_type']}' is not valid"
