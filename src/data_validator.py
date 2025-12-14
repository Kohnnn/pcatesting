"""
Data Validator for SentimentAlpha Vietnam Data Pipeline.

Validates data values for market data, recommendations, and other data types.
Ensures data quality by checking prices, volumes, dates, and detecting anomalies.
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

import pandas as pd


@dataclass
class AnomalyRecord:
    """Represents a detected data anomaly."""
    record_index: int
    record_type: str  # 'market_data' or 'recommendation'
    missing_fields: List[str]
    record_data: Dict[str, Any]
    
    def __str__(self) -> str:
        return f"Anomaly at index {self.record_index}: missing {self.missing_fields}"


@dataclass
class ValidationSummary:
    """Summary of validation results for a dataset."""
    total_records: int
    valid_records: int
    invalid_records: int
    anomalies: List[AnomalyRecord] = field(default_factory=list)
    price_errors: List[str] = field(default_factory=list)
    volume_errors: List[str] = field(default_factory=list)
    date_errors: List[str] = field(default_factory=list)
    
    @property
    def is_valid(self) -> bool:
        """Check if all records are valid."""
        return self.invalid_records == 0
    
    @property
    def error_count(self) -> int:
        """Total number of errors."""
        return len(self.price_errors) + len(self.volume_errors) + len(self.date_errors)


class DataValidator:
    """Validates data values for the SentimentAlpha pipeline."""
    
    # Date range for valid recommendations (2014-2024)
    MIN_DATE = date(2014, 1, 1)
    MAX_DATE = date(2024, 12, 31)
    
    # Critical fields that must be present
    MARKET_DATA_CRITICAL_FIELDS = ['ticker', 'date', 'close_price']
    RECOMMENDATION_CRITICAL_FIELDS = ['ticker', 'recommendation', 'issue_date']
    
    def validate_price(self, price: Any) -> bool:
        """
        Validate that a price is a positive number.
        
        Args:
            price: The price value to validate
            
        Returns:
            True if price is a positive number, False otherwise
        """
        if price is None or pd.isna(price):
            return False
        
        try:
            price_float = float(price)
            # Check for positive, finite number (reject NaN and infinity)
            import math
            if math.isnan(price_float) or math.isinf(price_float):
                return False
            return price_float > 0
        except (ValueError, TypeError):
            return False
    
    def validate_volume(self, volume: Any) -> bool:
        """
        Validate that a volume is a non-negative integer.
        
        Args:
            volume: The volume value to validate
            
        Returns:
            True if volume is a non-negative integer, False otherwise
        """
        if volume is None or pd.isna(volume):
            return False
        
        try:
            # Convert to float first to handle string inputs
            volume_float = float(volume)
            # Check if it's non-negative and effectively an integer
            return volume_float >= 0 and volume_float == int(volume_float)
        except (ValueError, TypeError):
            return False
    
    def validate_date_range(self, date_value: Any) -> bool:
        """
        Validate that a date is within the expected range (2014-2024).
        
        Args:
            date_value: The date value to validate (date, datetime, or string)
            
        Returns:
            True if date is within range, False otherwise
        """
        if date_value is None or pd.isna(date_value):
            return False
        
        try:
            # Convert to date object
            if isinstance(date_value, datetime):
                check_date = date_value.date()
            elif isinstance(date_value, date):
                check_date = date_value
            elif isinstance(date_value, str):
                # Try common date formats
                for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y', '%m/%d/%Y']:
                    try:
                        check_date = datetime.strptime(date_value, fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    return False
            elif isinstance(date_value, pd.Timestamp):
                check_date = date_value.date()
            else:
                return False
            
            return self.MIN_DATE <= check_date <= self.MAX_DATE
        except (ValueError, TypeError, AttributeError):
            return False

    def detect_anomalies(
        self,
        records: Union[pd.DataFrame, List[Dict]],
        record_type: str = 'market_data'
    ) -> List[AnomalyRecord]:
        """
        Detect records with missing critical fields.
        
        For market_data: ticker, date, close_price are critical
        For recommendation: ticker, recommendation, issue_date are critical
        
        Args:
            records: DataFrame or list of dictionaries containing records
            record_type: Type of records ('market_data' or 'recommendation')
            
        Returns:
            List of AnomalyRecord objects for records with missing critical fields
        """
        anomalies = []
        
        # Determine critical fields based on record type
        if record_type == 'market_data':
            critical_fields = self.MARKET_DATA_CRITICAL_FIELDS
        elif record_type == 'recommendation':
            critical_fields = self.RECOMMENDATION_CRITICAL_FIELDS
        else:
            raise ValueError(f"Unknown record type: {record_type}")
        
        # Convert DataFrame to list of dicts if needed
        if isinstance(records, pd.DataFrame):
            records_list = records.to_dict('records')
            # Normalize column names to lowercase
            records_list = [
                {k.lower(): v for k, v in record.items()}
                for record in records_list
            ]
        else:
            records_list = [
                {k.lower(): v for k, v in record.items()}
                for record in records
            ]
        
        for idx, record in enumerate(records_list):
            missing_fields = []
            
            for field in critical_fields:
                field_lower = field.lower()
                value = record.get(field_lower)
                
                # Check if field is missing or null
                if value is None or pd.isna(value):
                    missing_fields.append(field)
                elif isinstance(value, str) and value.strip() == '':
                    missing_fields.append(field)
            
            if missing_fields:
                anomalies.append(AnomalyRecord(
                    record_index=idx,
                    record_type=record_type,
                    missing_fields=missing_fields,
                    record_data=record
                ))
        
        return anomalies
    
    def validate_market_data(self, df: pd.DataFrame) -> ValidationSummary:
        """
        Validate a DataFrame of market data.
        
        Checks:
        - Close prices are positive
        - Volumes are non-negative integers
        - Critical fields are present
        
        Args:
            df: DataFrame with market data
            
        Returns:
            ValidationSummary with validation results
        """
        total_records = len(df)
        price_errors = []
        volume_errors = []
        invalid_count = 0
        
        # Normalize column names
        df_normalized = df.copy()
        df_normalized.columns = [col.lower() for col in df_normalized.columns]
        
        # Validate prices
        if 'close_price' in df_normalized.columns:
            for idx, price in enumerate(df_normalized['close_price']):
                if not pd.isna(price) and not self.validate_price(price):
                    price_errors.append(f"Row {idx}: Invalid price {price}")
                    invalid_count += 1
        
        # Validate volumes
        volume_cols = ['buy_volume', 'sell_volume', 'total_volume']
        for vol_col in volume_cols:
            if vol_col in df_normalized.columns:
                for idx, volume in enumerate(df_normalized[vol_col]):
                    if not pd.isna(volume) and not self.validate_volume(volume):
                        volume_errors.append(f"Row {idx}: Invalid {vol_col} {volume}")
                        invalid_count += 1
        
        # Detect anomalies
        anomalies = self.detect_anomalies(df_normalized, 'market_data')
        invalid_count += len(anomalies)
        
        return ValidationSummary(
            total_records=total_records,
            valid_records=total_records - invalid_count,
            invalid_records=invalid_count,
            anomalies=anomalies,
            price_errors=price_errors,
            volume_errors=volume_errors,
            date_errors=[]
        )
    
    def validate_recommendations(self, df: pd.DataFrame) -> ValidationSummary:
        """
        Validate a DataFrame of recommendation data.
        
        Checks:
        - Issue dates are within expected range (2014-2024)
        - Critical fields are present
        
        Args:
            df: DataFrame with recommendation data
            
        Returns:
            ValidationSummary with validation results
        """
        total_records = len(df)
        date_errors = []
        invalid_count = 0
        
        # Normalize column names
        df_normalized = df.copy()
        df_normalized.columns = [col.lower() for col in df_normalized.columns]
        
        # Validate dates
        if 'issue_date' in df_normalized.columns:
            for idx, date_val in enumerate(df_normalized['issue_date']):
                if not pd.isna(date_val) and not self.validate_date_range(date_val):
                    date_errors.append(f"Row {idx}: Date {date_val} outside range 2014-2024")
                    invalid_count += 1
        
        # Detect anomalies
        anomalies = self.detect_anomalies(df_normalized, 'recommendation')
        invalid_count += len(anomalies)
        
        return ValidationSummary(
            total_records=total_records,
            valid_records=total_records - invalid_count,
            invalid_records=invalid_count,
            anomalies=anomalies,
            price_errors=[],
            volume_errors=[],
            date_errors=date_errors
        )
