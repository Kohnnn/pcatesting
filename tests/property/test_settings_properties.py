"""
Property-based tests for settings operations.

**Feature: sentimentalpha-vietnam, Property 15: Settings Round Trip**
**Validates: Requirements 8.2, 8.3**
"""
from hypothesis import given, strategies as st, settings
from hypothesis import assume
import pytest
import sys
import os
import json
import tempfile

# Add src and backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.database import DatabaseManager, Settings as SettingsModel
from sqlalchemy.orm import Session


class TestSettingsProperties:
    """Property-based tests for settings round trip."""
    
    @given(
        sentiment_min=st.floats(min_value=0.0, max_value=5.0, allow_nan=False, allow_infinity=False),
        rsi_max=st.floats(min_value=50.0, max_value=100.0, allow_nan=False, allow_infinity=False),
        rsi_min=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False),
        bsi_min=st.floats(min_value=0.0, max_value=0.5, allow_nan=False, allow_infinity=False),
        bsi_max=st.floats(min_value=0.5, max_value=1.0, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100, deadline=None)
    def test_settings_round_trip(
        self,
        sentiment_min,
        rsi_max,
        rsi_min,
        bsi_min,
        bsi_max
    ):
        """
        **Feature: sentimentalpha-vietnam, Property 15: Settings Round Trip**
        **Validates: Requirements 8.2, 8.3**
        
        For any valid settings object saved to the database,
        retrieving it should return an equivalent object.
        """
        # Create temporary database for this test
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        db_manager = DatabaseManager(db_path)
        db_manager.create_tables()
        session = db_manager.Session()
        
        try:
            # Create settings dictionary
            settings_dict = {
                'sentiment_min': sentiment_min,
                'rsi_max': rsi_max,
                'rsi_min': rsi_min,
                'bsi_min': bsi_min,
                'bsi_max': bsi_max
            }
            
            # Save settings to database
            for key, value in settings_dict.items():
                existing = session.query(SettingsModel).filter(SettingsModel.key == key).first()
                
                if existing:
                    existing.value = json.dumps(value)
                else:
                    new_setting = SettingsModel(
                        key=key,
                        value=json.dumps(value),
                        category='signal_thresholds'
                    )
                    session.add(new_setting)
            
            session.commit()
            
            # Retrieve settings from database
            retrieved_dict = {}
            for key in settings_dict.keys():
                setting = session.query(SettingsModel).filter(SettingsModel.key == key).first()
                assert setting is not None, f"Setting {key} not found in database"
                retrieved_dict[key] = json.loads(setting.value)
            
            # Verify round trip - values should be equal within floating point tolerance
            for key in settings_dict.keys():
                original = settings_dict[key]
                retrieved = retrieved_dict[key]
                
                # Check equality with tolerance for floating point
                assert abs(original - retrieved) < 1e-9, \
                    f"Round trip failed for {key}: {original} != {retrieved}"
        
        finally:
            session.close()
            # Close all connections
            db_manager.engine.dispose()
            # Clean up temporary database
            try:
                if os.path.exists(db_path):
                    os.unlink(db_path)
            except PermissionError:
                # On Windows, file might still be locked
                pass
    
    @given(
        key=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'), whitelist_characters='_')),
        value=st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100, deadline=None)
    def test_arbitrary_setting_round_trip(self, key, value):
        """
        For any arbitrary key-value pair, saving and retrieving should preserve the value.
        """
        # Create temporary database for this test
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        db_manager = DatabaseManager(db_path)
        db_manager.create_tables()
        session = db_manager.Session()
        
        try:
            # Save setting
            new_setting = SettingsModel(
                key=key,
                value=json.dumps(value),
                category='test'
            )
            session.add(new_setting)
            session.commit()
            
            # Retrieve setting
            retrieved = session.query(SettingsModel).filter(SettingsModel.key == key).first()
            assert retrieved is not None, f"Setting {key} not found"
            
            retrieved_value = json.loads(retrieved.value)
            
            # Verify equality
            assert abs(value - retrieved_value) < 1e-9, \
                f"Round trip failed: {value} != {retrieved_value}"
        
        finally:
            session.close()
            # Close all connections
            db_manager.engine.dispose()
            # Clean up temporary database
            try:
                if os.path.exists(db_path):
                    os.unlink(db_path)
            except PermissionError:
                # On Windows, file might still be locked
                pass
    
    @given(
        value=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100, deadline=None)
    def test_setting_update_preserves_value(self, value):
        """
        For any setting, updating it multiple times should preserve the latest value.
        """
        # Create temporary database for this test
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        db_manager = DatabaseManager(db_path)
        db_manager.create_tables()
        session = db_manager.Session()
        key = 'test_update_key'
        
        try:
            # Create initial setting
            setting = SettingsModel(
                key=key,
                value=json.dumps(0.0),
                category='test'
            )
            session.add(setting)
            session.commit()
            
            # Update setting
            existing = session.query(SettingsModel).filter(SettingsModel.key == key).first()
            existing.value = json.dumps(value)
            session.commit()
            
            # Retrieve and verify
            retrieved = session.query(SettingsModel).filter(SettingsModel.key == key).first()
            retrieved_value = json.loads(retrieved.value)
            
            assert abs(value - retrieved_value) < 1e-9, \
                f"Update failed: {value} != {retrieved_value}"
        
        finally:
            session.close()
            # Close all connections
            db_manager.engine.dispose()
            # Clean up temporary database
            try:
                if os.path.exists(db_path):
                    os.unlink(db_path)
            except PermissionError:
                # On Windows, file might still be locked
                pass
