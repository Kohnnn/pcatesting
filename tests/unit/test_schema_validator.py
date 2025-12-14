"""
Unit tests for SchemaValidator.

Tests that valid files pass validation and invalid files fail with specific errors.
**Validates: Requirements 1.2, 1.3**
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
import tempfile
import os
import csv

from schema_validator import SchemaValidator, ValidationResult


class TestSchemaValidatorInference:
    """Tests for schema type inference from filenames."""
    
    def test_infer_market_data_close(self):
        """Close files should be inferred as market_data."""
        validator = SchemaValidator()
        for i in range(1, 10):
            result = validator.infer_schema_type(Path(f"close{i}.csv"))
            assert result == 'market_data', f"close{i}.csv should be market_data"
    
    def test_infer_market_data_buy(self):
        """Buy files should be inferred as market_data."""
        validator = SchemaValidator()
        for i in range(1, 10):
            result = validator.infer_schema_type(Path(f"buy{i}.csv"))
            assert result == 'market_data', f"buy{i}.csv should be market_data"
    
    def test_infer_market_data_sell(self):
        """Sell files should be inferred as market_data."""
        validator = SchemaValidator()
        for i in range(1, 10):
            result = validator.infer_schema_type(Path(f"sell{i}.csv"))
            assert result == 'market_data', f"sell{i}.csv should be market_data"
    
    def test_infer_vnindex(self):
        """vnindex.csv should be inferred as vnindex."""
        validator = SchemaValidator()
        result = validator.infer_schema_type(Path("vnindex.csv"))
        assert result == 'vnindex'
    
    def test_infer_recommendations(self):
        """rec.csv should be inferred as recommendations."""
        validator = SchemaValidator()
        result = validator.infer_schema_type(Path("rec.csv"))
        assert result == 'recommendations'
    
    def test_infer_risk_free_rate(self):
        """rfr.csv should be inferred as risk_free_rate."""
        validator = SchemaValidator()
        result = validator.infer_schema_type(Path("rfr.csv"))
        assert result == 'risk_free_rate'
    
    def test_infer_unknown(self):
        """Unknown files should return None."""
        validator = SchemaValidator()
        assert validator.infer_schema_type(Path("unknown.csv")) is None
        assert validator.infer_schema_type(Path("data.csv")) is None
        assert validator.infer_schema_type(Path("random_file.csv")) is None


class TestSchemaValidatorValidFiles:
    """Tests that valid files pass validation."""
    
    def test_valid_market_data_file(self):
        """Valid market data CSV should pass validation."""
        validator = SchemaValidator()
        # Test with actual file from xlsx directory
        result = validator.validate_file(Path("xlsx/close1.csv"), "market_data")
        assert result.is_valid, f"close1.csv should be valid: {result.errors}"
        assert result.schema_type == 'market_data'
    
    def test_valid_vnindex_file(self):
        """Valid vnindex CSV should pass validation."""
        validator = SchemaValidator()
        result = validator.validate_file(Path("xlsx/vnindex.csv"), "vnindex")
        assert result.is_valid, f"vnindex.csv should be valid: {result.errors}"
        assert result.schema_type == 'vnindex'
    
    def test_valid_recommendations_file(self):
        """Valid recommendations CSV should pass validation."""
        validator = SchemaValidator()
        result = validator.validate_file(Path("xlsx/rec.csv"), "recommendations")
        assert result.is_valid, f"rec.csv should be valid: {result.errors}"
        assert result.schema_type == 'recommendations'
    
    def test_valid_risk_free_rate_file(self):
        """Valid risk-free rate CSV should pass validation."""
        validator = SchemaValidator()
        result = validator.validate_file(Path("xlsx/rfr.csv"), "risk_free_rate")
        assert result.is_valid, f"rfr.csv should be valid: {result.errors}"
        assert result.schema_type == 'risk_free_rate'


class TestSchemaValidatorInvalidFiles:
    """Tests that invalid files fail with specific errors."""
    
    def test_missing_no_column(self):
        """Market data without 'No' column should fail."""
        validator = SchemaValidator()
        
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, newline=''
        ) as tmp:
            writer = csv.writer(tmp)
            # Write 8 header rows (market_data expects skiprows=8)
            for _ in range(8):
                writer.writerow([''] * 3)
            # Write header without 'No' column
            writer.writerow(['Date', 'AAA', 'BBB'])
            writer.writerow(['2024-01-01 00:00:00', '100', '200'])
            tmp_path = tmp.name
        
        try:
            result = validator.validate_file(Path(tmp_path), 'market_data')
            assert not result.is_valid
            assert any('No' in err for err in result.errors), \
                f"Should have error about missing 'No' column: {result.errors}"
        finally:
            os.unlink(tmp_path)
    
    def test_missing_date_column(self):
        """Market data without 'Date' column should fail."""
        validator = SchemaValidator()
        
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, newline=''
        ) as tmp:
            writer = csv.writer(tmp)
            # Write 8 header rows (market_data expects skiprows=8)
            for _ in range(8):
                writer.writerow([''] * 3)
            # Write header without 'Date' column
            writer.writerow(['No', 'AAA', 'BBB'])
            writer.writerow(['1', '100', '200'])
            tmp_path = tmp.name
        
        try:
            result = validator.validate_file(Path(tmp_path), 'market_data')
            assert not result.is_valid
            assert any('Date' in err for err in result.errors), \
                f"Should have error about missing 'Date' column: {result.errors}"
        finally:
            os.unlink(tmp_path)
    
    def test_missing_ticker_column_recommendations(self):
        """Recommendations without 'Ticker' column should fail."""
        validator = SchemaValidator()
        
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, newline=''
        ) as tmp:
            writer = csv.writer(tmp)
            # Write 2 header rows
            for _ in range(2):
                writer.writerow([''] * 3)
            # Write header without 'Ticker' column
            writer.writerow(['Recommendation', 'Issue date', 'Analyst'])
            writer.writerow(['buy', '2024-01-01 00:00:00', 'Test'])
            tmp_path = tmp.name
        
        try:
            result = validator.validate_file(Path(tmp_path), 'recommendations')
            assert not result.is_valid
            assert any('Ticker' in err for err in result.errors), \
                f"Should have error about missing 'Ticker' column: {result.errors}"
        finally:
            os.unlink(tmp_path)
    
    def test_nonexistent_file(self):
        """Nonexistent file should fail with file not found error."""
        validator = SchemaValidator()
        result = validator.validate_file(Path("/nonexistent/file.csv"), 'market_data')
        assert not result.is_valid
        assert any('not found' in err.lower() for err in result.errors)
    
    def test_unknown_schema_type(self):
        """Unknown schema type should fail with specific error."""
        validator = SchemaValidator()
        
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, newline=''
        ) as tmp:
            tmp.write('col1,col2\n1,2\n')
            tmp_path = tmp.name
        
        try:
            result = validator.validate_file(Path(tmp_path), 'invalid_type')
            assert not result.is_valid
            assert any('unknown' in err.lower() for err in result.errors)
        finally:
            os.unlink(tmp_path)


class TestSchemaValidatorHelpers:
    """Tests for helper methods."""
    
    def test_get_schema_info(self):
        """get_schema_info should return schema for known types."""
        validator = SchemaValidator()
        
        schema = validator.get_schema_info('market_data')
        assert schema is not None
        assert 'header_rows' in schema
        assert 'required_columns' in schema
        
        schema = validator.get_schema_info('unknown_type')
        assert schema is None
    
    def test_validation_result_error_message(self):
        """ValidationResult.error_message should combine errors."""
        result = ValidationResult(
            is_valid=False,
            file_path='test.csv',
            schema_type='market_data',
            errors=['Error 1', 'Error 2'],
            warnings=[]
        )
        assert 'Error 1' in result.error_message
        assert 'Error 2' in result.error_message
        
        # Empty errors should return empty string
        result_valid = ValidationResult(
            is_valid=True,
            file_path='test.csv',
            schema_type='market_data',
            errors=[],
            warnings=[]
        )
        assert result_valid.error_message == ""
