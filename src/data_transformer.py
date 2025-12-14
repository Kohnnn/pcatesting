"""
DataTransformer class for transforming and normalizing data.

Provides functionality for:
- Wide-to-long format transformation
- Rating standardization (1-5 scale)
- Market data merging
- Validation integration with error collection
"""
import pandas as pd
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any


@dataclass
class TransformationError:
    """Represents an error encountered during transformation."""
    row_index: int
    column: str
    value: Any
    error_type: str
    message: str
    
    def __str__(self) -> str:
        return f"Row {self.row_index}, Column '{self.column}': {self.message}"


@dataclass
class TransformationResult:
    """Result of a transformation operation with validation."""
    data: pd.DataFrame
    total_records: int
    valid_records: int
    invalid_records: int
    errors: List[TransformationError] = field(default_factory=list)
    
    @property
    def is_valid(self) -> bool:
        """Check if all records are valid."""
        return self.invalid_records == 0
    
    @property
    def success_rate(self) -> float:
        """Calculate the percentage of valid records."""
        if self.total_records == 0:
            return 100.0
        return (self.valid_records / self.total_records) * 100


class DataTransformer:
    """
    Transforms wide-format data to normalized long-format.
    
    Includes validation integration for data quality checks during transformation.
    """
    
    # Rating standardization mapping (per thesis Table 2)
    RATING_MAP = {
        # 5 = Buy: buy, strong buy, add, accumulate
        'buy': 5,
        'strong buy': 5,
        'add': 5,
        'accumulate': 5,
        
        # 4 = Overweight: outperform, overweight, overwt/in-line
        'outperform': 4,
        'overweight': 4,
        'overwt/in-line': 4,
        
        # 3 = Hold: hold, market perform, neutral
        'hold': 3,
        'market perform': 3,
        'neutral': 3,
        
        # 2 = Underweight: underperform, underweight
        'underperform': 2,
        'underweight': 2,
        
        # 1 = Sell: reduce, sell, strong sell
        'reduce': 1,
        'sell': 1,
        'strong sell': 1,
    }
    
    def __init__(self, validator: Optional[Any] = None):
        """
        Initialize DataTransformer with optional validator.
        
        Args:
            validator: Optional DataValidator instance for validation during transformation
        """
        self._validator = validator
        self._errors: List[TransformationError] = []
    
    @property
    def errors(self) -> List[TransformationError]:
        """Get collected errors from last transformation."""
        return self._errors.copy()
    
    def clear_errors(self) -> None:
        """Clear collected errors."""
        self._errors = []
    
    def _add_error(
        self,
        row_index: int,
        column: str,
        value: Any,
        error_type: str,
        message: str
    ) -> None:
        """Add an error to the collection."""
        self._errors.append(TransformationError(
            row_index=row_index,
            column=column,
            value=value,
            error_type=error_type,
            message=message
        ))
    
    def melt_wide_to_long(
        self,
        df: pd.DataFrame,
        value_name: str,
        validate: bool = False
    ) -> pd.DataFrame:
        """
        Convert wide format (tickers as columns) to long format.
        
        Property 1: Wide-to-Long Transformation Preserves Data
        For any valid wide-format DataFrame with N tickers and M dates,
        transforming to long format should produce exactly N × M rows with no data loss.
        
        Args:
            df: Wide-format DataFrame with Date column and ticker columns
            value_name: Name for the value column in long format
            validate: If True, validate values during transformation
            
        Returns:
            Long-format DataFrame with columns: date, ticker, value
        """
        # Identify the date column (case-insensitive)
        date_col = None
        for col in df.columns:
            if col.lower() == 'date':
                date_col = col
                break
        
        if date_col is None:
            raise ValueError("DataFrame must have a 'Date' column")
        
        # Get all columns except Date
        ticker_cols = [col for col in df.columns if col != date_col]
        
        # Calculate expected row count for validation
        n_dates = len(df)
        n_tickers = len(ticker_cols)
        expected_rows = n_dates * n_tickers
        
        # Melt the DataFrame
        long_df = df.melt(
            id_vars=[date_col],
            value_vars=ticker_cols,
            var_name='ticker',
            value_name=value_name
        )
        
        # Rename Date column to lowercase
        long_df = long_df.rename(columns={date_col: 'date'})
        
        # Validate row count preservation
        actual_rows = len(long_df)
        if actual_rows != expected_rows:
            self._add_error(
                row_index=-1,
                column='transformation',
                value=f"expected={expected_rows}, actual={actual_rows}",
                error_type='row_count_mismatch',
                message=f"Wide-to-long transformation produced {actual_rows} rows, expected {expected_rows}"
            )
        
        # Validate values if requested and validator is available
        if validate and self._validator is not None:
            self._validate_transformed_values(long_df, value_name)
        
        # Sort by date and ticker
        long_df = long_df.sort_values(['date', 'ticker']).reset_index(drop=True)
        
        return long_df
    
    def _validate_transformed_values(
        self,
        df: pd.DataFrame,
        value_name: str
    ) -> None:
        """
        Validate values in transformed DataFrame.
        
        Args:
            df: Long-format DataFrame to validate
            value_name: Name of the value column
        """
        if self._validator is None:
            return
        
        # Determine validation type based on value_name
        is_price = value_name in ['close_price', 'price', 'value']
        is_volume = value_name in ['buy_volume', 'sell_volume', 'total_volume', 'volume']
        
        for idx, row in df.iterrows():
            value = row[value_name]
            
            # Skip null values (they may be valid missing data)
            if pd.isna(value):
                continue
            
            if is_price:
                if not self._validator.validate_price(value):
                    self._add_error(
                        row_index=idx,
                        column=value_name,
                        value=value,
                        error_type='invalid_price',
                        message=f"Invalid price value: {value} (must be positive)"
                    )
            elif is_volume:
                if not self._validator.validate_volume(value):
                    self._add_error(
                        row_index=idx,
                        column=value_name,
                        value=value,
                        error_type='invalid_volume',
                        message=f"Invalid volume value: {value} (must be non-negative integer)"
                    )
    
    def standardize_rating(self, rating: str, row_index: int = -1) -> Optional[int]:
        """
        Map recommendation text to 1-5 numeric scale.
        
        Property 2: Rating Standardization Range
        For any valid recommendation rating string, the standardized numeric 
        rating should be in the range [1, 5].
        
        Scale (per thesis Table 2):
        - 5 = Buy: buy, strong buy, add, accumulate
        - 4 = Overweight: outperform, overweight, overwt/in-line
        - 3 = Hold: hold, market perform, neutral
        - 2 = Underweight: underperform, underweight
        - 1 = Sell: reduce, sell, strong sell
        
        Args:
            rating: Recommendation text (case-insensitive)
            row_index: Optional row index for error tracking
            
        Returns:
            Numeric rating from 1-5, or None if rating is invalid
        """
        if pd.isna(rating):
            self._add_error(
                row_index=row_index,
                column='rating',
                value=rating,
                error_type='null_rating',
                message="Rating cannot be null"
            )
            return None
        
        # Convert to lowercase and strip whitespace
        rating_clean = str(rating).lower().strip()
        
        # Look up in mapping
        if rating_clean in self.RATING_MAP:
            return self.RATING_MAP[rating_clean]
        else:
            self._add_error(
                row_index=row_index,
                column='rating',
                value=rating,
                error_type='unknown_rating',
                message=f"Unknown rating: '{rating}'"
            )
            return None
    
    def standardize_ratings_batch(
        self,
        df: pd.DataFrame,
        rating_column: str = 'recommendation'
    ) -> TransformationResult:
        """
        Standardize ratings for an entire DataFrame.
        
        Args:
            df: DataFrame containing recommendation data
            rating_column: Name of the column containing rating text
            
        Returns:
            TransformationResult with standardized ratings and error collection
        """
        self.clear_errors()
        
        result_df = df.copy()
        valid_count = 0
        invalid_count = 0
        
        # Normalize column names
        col_map = {col: col.lower() for col in result_df.columns}
        result_df = result_df.rename(columns=col_map)
        rating_col_lower = rating_column.lower()
        
        if rating_col_lower not in result_df.columns:
            raise ValueError(f"Column '{rating_column}' not found in DataFrame")
        
        # Add rating_numeric column
        rating_numeric = []
        
        for idx, row in result_df.iterrows():
            rating = row[rating_col_lower]
            numeric = self.standardize_rating(rating, row_index=idx)
            rating_numeric.append(numeric)
            
            if numeric is not None:
                valid_count += 1
            else:
                invalid_count += 1
        
        result_df['rating_numeric'] = rating_numeric
        
        return TransformationResult(
            data=result_df,
            total_records=len(df),
            valid_records=valid_count,
            invalid_records=invalid_count,
            errors=self.errors
        )
    
    def merge_market_data(
        self,
        close_df: pd.DataFrame,
        buy_df: pd.DataFrame,
        sell_df: pd.DataFrame,
        tra_df: pd.DataFrame,
        sha_df: pd.DataFrame,
        validate: bool = False
    ) -> TransformationResult:
        """
        Combine all market data into single DataFrame with validation.
        
        Args:
            close_df: Close prices (wide format)
            buy_df: Buy volumes (wide format)
            sell_df: Sell volumes (wide format)
            tra_df: Total trading volumes (wide format)
            sha_df: Shares outstanding (wide format)
            validate: If True, validate values during transformation
            
        Returns:
            TransformationResult with merged data and validation errors
        """
        self.clear_errors()
        
        # Convert each to long format with validation
        close_long = self.melt_wide_to_long(close_df, 'close_price', validate=validate)
        buy_long = self.melt_wide_to_long(buy_df, 'buy_volume', validate=validate)
        sell_long = self.melt_wide_to_long(sell_df, 'sell_volume', validate=validate)
        tra_long = self.melt_wide_to_long(tra_df, 'total_volume', validate=validate)
        sha_long = self.melt_wide_to_long(sha_df, 'shares_outstanding', validate=validate)
        
        # Merge all dataframes on date and ticker
        merged = close_long.copy()
        
        # Merge buy volume
        merged = merged.merge(
            buy_long[['date', 'ticker', 'buy_volume']],
            on=['date', 'ticker'],
            how='left'
        )
        
        # Merge sell volume
        merged = merged.merge(
            sell_long[['date', 'ticker', 'sell_volume']],
            on=['date', 'ticker'],
            how='left'
        )
        
        # Merge total volume
        merged = merged.merge(
            tra_long[['date', 'ticker', 'total_volume']],
            on=['date', 'ticker'],
            how='left'
        )
        
        # Merge shares outstanding
        merged = merged.merge(
            sha_long[['date', 'ticker', 'shares_outstanding']],
            on=['date', 'ticker'],
            how='left'
        )
        
        # Count valid/invalid records
        total_records = len(merged)
        invalid_records = len(self._errors)
        valid_records = total_records - invalid_records
        
        return TransformationResult(
            data=merged,
            total_records=total_records,
            valid_records=valid_records,
            invalid_records=invalid_records,
            errors=self.errors
        )
    
    def transform_with_validation(
        self,
        df: pd.DataFrame,
        value_name: str
    ) -> TransformationResult:
        """
        Transform wide-format data to long-format with full validation.
        
        This is a convenience method that combines transformation and validation.
        
        Args:
            df: Wide-format DataFrame with Date column and ticker columns
            value_name: Name for the value column in long format
            
        Returns:
            TransformationResult with transformed data and validation errors
        """
        self.clear_errors()
        
        # Transform with validation enabled
        long_df = self.melt_wide_to_long(df, value_name, validate=True)
        
        # Count valid/invalid records
        total_records = len(long_df)
        invalid_records = len(self._errors)
        valid_records = total_records - invalid_records
        
        return TransformationResult(
            data=long_df,
            total_records=total_records,
            valid_records=valid_records,
            invalid_records=invalid_records,
            errors=self.errors
        )
