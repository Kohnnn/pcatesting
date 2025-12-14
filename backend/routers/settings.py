"""
Settings router for system settings endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from typing import Dict, Any

from backend.database import get_db
from backend.models import Settings
from backend.schemas import (
    SettingsResponse,
    SignalThresholdsRequest,
    SignalThresholdsResponse
)

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=SignalThresholdsResponse)
def get_settings(db: Session = Depends(get_db)) -> SignalThresholdsResponse:
    """
    Get current system settings (signal thresholds).
    
    Args:
        db: Database session
        
    Returns:
        Current signal threshold settings
    """
    # Default values
    defaults = {
        'sentiment_min': 1.0,
        'rsi_max': 70.0,
        'rsi_min': 30.0,
        'bsi_min': 0.5,
        'bsi_max': 0.8
    }
    
    # Try to load from database
    settings_dict = {}
    for key in defaults.keys():
        setting = db.query(Settings).filter(Settings.key == key).first()
        if setting:
            try:
                settings_dict[key] = json.loads(setting.value)
            except (json.JSONDecodeError, ValueError):
                # If value is not JSON, try to parse as float
                try:
                    settings_dict[key] = float(setting.value)
                except ValueError:
                    settings_dict[key] = defaults[key]
        else:
            settings_dict[key] = defaults[key]
    
    return SignalThresholdsResponse(**settings_dict)


@router.post("", response_model=SignalThresholdsResponse)
def update_settings(
    settings: SignalThresholdsRequest,
    db: Session = Depends(get_db)
) -> SignalThresholdsResponse:
    """
    Update system settings (signal thresholds).
    
    Args:
        settings: New signal threshold values
        db: Database session
        
    Returns:
        Updated signal threshold settings
    """
    settings_dict = settings.model_dump()
    
    # Update each setting in the database
    for key, value in settings_dict.items():
        existing = db.query(Settings).filter(Settings.key == key).first()
        
        if existing:
            # Update existing setting
            existing.value = json.dumps(value)
        else:
            # Create new setting
            new_setting = Settings(
                key=key,
                value=json.dumps(value),
                category='signal_thresholds'
            )
            db.add(new_setting)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update settings: {str(e)}"
        )
    
    return SignalThresholdsResponse(**settings_dict)


@router.get("/all", response_model=Dict[str, Any])
def get_all_settings(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get all settings from the database.
    
    Args:
        db: Database session
        
    Returns:
        Dictionary of all settings
    """
    all_settings = db.query(Settings).all()
    
    result = {}
    for setting in all_settings:
        try:
            result[setting.key] = json.loads(setting.value)
        except (json.JSONDecodeError, ValueError):
            result[setting.key] = setting.value
    
    return result
