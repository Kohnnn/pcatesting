"""
Property-based tests for schema validation.

**Feature: data-management-refactor**
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from hypothesis import given, strategies as st, settings, assume
import tempfile
import os
import csv

from schema_validator import SchemaValidator, ValidationResult


class TestSchemaValidationProperties:
    """Property-based tests for schema validation completeness."""
    
    @settings(max_examples=100, deadline=None)
    @given(
        filename=st.sampled_from([
            'close1.csv', 'close2.csv', 'buy1.csv', 'sell3.csv', 'tra5.csv', 'sha9.csv',
            'vnindex.csv', 'rec.csv', 'rfr.csv',
            'unknown.csv', 'random.csv', 'data.csv'
        ])
    )
    def test_schema_type_inference_completeness(self, filename):
        """
        **Feature: data-management-refactor, Property 5: Schema Validation Completeness**
        **Validates: Requirements 1.2, 1.3**
        
        For any filename, the schema validator should either correctly infer
        a known schema type or return None for unknown files.
        """
        validator = SchemaValidator()
        filepath = Path(filename)
        
        schema_type = validator.infer_schema_type(filepath)
        
        # Known patterns should be recognized
        if filename.startswith(('close', 'buy', 'sell', 'tra', 'sha')) and filename[:-4][-1].isdigit():
            assert schema_type == 'market_data', f"Expected 'market_data' for {filename}"
        elif filename == 'vnindex.csv':
            assert schema_type == 'vnindex', f"Expected 'vnindex' for {filename}"
        elif filename == 'rec.csv':
            assert schema_type == 'recommendations', f"Expected 'recommendations' for {filename}"
        elif filename == 'rfr.csv':
            assert schema_type == 'risk_free_rate', f"Expected 'risk_free_rate' for {filename}"
        else:
            # Unknown files should return None
            assert schema_type is None, f"Expected None for unknown file {filename}, got {schema_type}"

    @settings(max_examples=100, deadline=None)
    @given(
        has_no_col=st.booleans(),
        has_date_col=st.booleans(),
        num_ticker_cols=st.integers(min_value=0, max_value=10),
        num_data_rows=st.integers(min_value=0, max_value=5)
    )
    def test_market_data_validation_completeness(
        self, has_no_col, has_date_col, num_ticker_cols, num_data_rows
    ):
        """
        **Feature: data-management-refactor, Property 5: Schema Validation Completeness**
        **Validates: Requirements 1.2, 1.3**
        
        For any CSV file, the schema validator should either accept it as valid
        (matching expected structure) or reject it with specific error messages,
        never silently accepting malformed data.
        """
        validator = SchemaValidator()
        
        # Create a temporary CSV file with controlled structure
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, newline=''
        ) as tmp:
            writer = csv.writer(tmp)
            
            # Write 8 header rows (market_data format expects skiprows=8)
            # Rows 0-7 are metadata, row 8 is the actual column header
            for i in range(8):
                writer.writerow([''] * 5)
            
            # Write column header row (this is row 8, which becomes the header after skiprows=8)
            headers = []
            if has_no_col:
                headers.append('No')
            if has_date_col:
                headers.append('Date')
            
            # Add ticker columns (3-letter uppercase)
            tickers = [f"T{chr(65+i)}{chr(65+i)}" for i in range(num_ticker_cols)]
            headers.extend(tickers)
            
            if not headers:
                headers = ['Empty']
            
            writer.writerow(headers)
            
            # Write data rows
            for row_num in range(num_data_rows):
                row = []
                if has_no_col:
                    row.append(str(row_num + 1))
                if has_date_col:
                    row.append('2024-01-01 00:00:00')
                row.extend(['100.0'] * num_ticker_cols)
                if not row:
                    row = ['']
                writer.writerow(row)
            
            tmp_path = tmp.name
        
        try:
            result = validator.validate_file(Path(tmp_path), 'market_data')
            
            # Result should always be a ValidationResult
            assert isinstance(result, ValidationResult)
            assert result.schema_type == 'market_data'
            
            # If missing required columns, should have errors
            if not has_no_col:
                assert not result.is_valid, "Should be invalid without 'No' column"
                assert any('No' in err for err in result.errors), \
                    "Should have error about missing 'No' column"
            
            if not has_date_col:
                assert not result.is_valid, "Should be invalid without 'Date' column"
                assert any('Date' in err for err in result.errors), \
                    "Should have error about missing 'Date' column"
            
            # If has required columns, should be valid (or have only warnings)
            if has_no_col and has_date_col:
                # Should be valid or have only warnings, not errors about required columns
                required_col_errors = [
                    e for e in result.errors 
                    if 'Missing required column' in e
                ]
                assert len(required_col_errors) == 0, \
                    f"Should not have required column errors when columns present: {required_col_errors}"
        
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    @settings(max_examples=100, deadline=None)
    @given(
        has_ticker=st.booleans(),
        has_recommendation=st.booleans(),
        has_issue_date=st.booleans(),
        num_data_rows=st.integers(min_value=0, max_value=5)
    )
    def test_recommendations_validation_completeness(
        self, has_ticker, has_recommendation, has_issue_date, num_data_rows
    ):
        """
        **Feature: data-management-refactor, Property 5: Schema Validation Completeness**
        **Validates: Requirements 1.2, 1.3**
        
        For any recommendations CSV file, the schema validator should either 
        accept it as valid or reject it with specific error messages about 
        missing required columns.
        """
        validator = SchemaValidator()
        
        # Create a temporary CSV file with controlled structure
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, newline=''
        ) as tmp:
            writer = csv.writer(tmp)
            
            # Write 2 header rows (recommendations format expects skiprows=2)
            # Rows 0-1 are metadata, row 2 is the actual column header
            writer.writerow([''] * 5)
            writer.writerow([''] * 5)
            
            # Write column header row (this is row 2, which becomes the header after skiprows=2)
            headers = []
            if has_ticker:
                headers.append('Ticker')
            if has_recommendation:
                headers.append('Recommendation')
            if has_issue_date:
                headers.append('Issue date')
            
            # Add some optional columns
            headers.extend(['Comp name', 'Analyst'])
            
            writer.writerow(headers)
            
            # Write data rows
            for row_num in range(num_data_rows):
                row = []
                if has_ticker:
                    row.append('AAA')
                if has_recommendation:
                    row.append('buy')
                if has_issue_date:
                    row.append('2024-01-01 00:00:00')
                row.extend(['Test Firm', 'Test Analyst'])
                writer.writerow(row)
            
            tmp_path = tmp.name
        
        try:
            result = validator.validate_file(Path(tmp_path), 'recommendations')
            
            # Result should always be a ValidationResult
            assert isinstance(result, ValidationResult)
            assert result.schema_type == 'recommendations'
            
            # Check for specific error messages about missing columns
            if not has_ticker:
                assert not result.is_valid, "Should be invalid without 'Ticker' column"
                assert any('Ticker' in err for err in result.errors), \
                    "Should have error about missing 'Ticker' column"
            
            if not has_recommendation:
                assert not result.is_valid, "Should be invalid without 'Recommendation' column"
                assert any('Recommendation' in err for err in result.errors), \
                    "Should have error about missing 'Recommendation' column"
            
            if not has_issue_date:
                assert not result.is_valid, "Should be invalid without 'Issue date' column"
                assert any('Issue date' in err for err in result.errors), \
                    "Should have error about missing 'Issue date' column"
            
            # If all required columns present, should be valid
            if has_ticker and has_recommendation and has_issue_date:
                required_col_errors = [
                    e for e in result.errors 
                    if 'Missing required column' in e
                ]
                assert len(required_col_errors) == 0, \
                    f"Should not have required column errors: {required_col_errors}"
        
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    @settings(max_examples=50, deadline=None)
    @given(
        date_format=st.sampled_from([
            '2024-01-15 00:00:00',  # Valid format
            '2024-01-15',           # Alternative valid format
            'invalid-date',         # Invalid format
            '15/01/2024',           # Different format
            '',                     # Empty
        ])
    )
    def test_date_format_validation(self, date_format):
        """
        **Feature: data-management-refactor, Property 5: Schema Validation Completeness**
        **Validates: Requirements 1.2, 1.3**
        
        For any date format in CSV files, the validator should either accept
        valid formats or report specific errors/warnings for invalid formats.
        """
        validator = SchemaValidator()
        
        # Create a temporary CSV file with the date format
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, newline=''
        ) as tmp:
            writer = csv.writer(tmp)
            
            # Write 8 header rows (market_data format expects skiprows=8)
            for i in range(8):
                writer.writerow([''] * 3)
            
            # Write column headers (this is row 8, which becomes the header after skiprows=8)
            writer.writerow(['No', 'Date', 'AAA'])
            
            # Write data row with the test date
            writer.writerow(['1', date_format, '100.0'])
            
            tmp_path = tmp.name
        
        try:
            result = validator.validate_file(Path(tmp_path), 'market_data')
            
            # Result should always be a ValidationResult
            assert isinstance(result, ValidationResult)
            
            # Valid date formats should not produce date-related errors
            if date_format in ['2024-01-15 00:00:00', '2024-01-15']:
                date_errors = [e for e in result.errors if 'date' in e.lower()]
                # May have warnings but not errors for valid dates
                assert len(date_errors) == 0, \
                    f"Valid date format should not produce errors: {date_errors}"
            
            # Invalid date formats should produce errors or warnings
            if date_format == 'invalid-date':
                has_date_issue = (
                    any('date' in e.lower() for e in result.errors) or
                    any('date' in w.lower() for w in result.warnings)
                )
                assert has_date_issue, \
                    "Invalid date format should produce error or warning"
        
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_nonexistent_file_validation(self):
        """
        **Feature: data-management-refactor, Property 5: Schema Validation Completeness**
        **Validates: Requirements 1.2, 1.3**
        
        For any nonexistent file, the validator should return an invalid result
        with a specific error message.
        """
        validator = SchemaValidator()
        
        result = validator.validate_file(Path('/nonexistent/path/file.csv'), 'market_data')
        
        assert isinstance(result, ValidationResult)
        assert not result.is_valid
        assert any('not found' in err.lower() or 'File not found' in err for err in result.errors)
    
    def test_unknown_schema_type_validation(self):
        """
        **Feature: data-management-refactor, Property 5: Schema Validation Completeness**
        **Validates: Requirements 1.2, 1.3**
        
        For any unknown schema type, the validator should return an invalid result
        with a specific error message.
        """
        validator = SchemaValidator()
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, newline=''
        ) as tmp:
            tmp.write('col1,col2\n1,2\n')
            tmp_path = tmp.name
        
        try:
            result = validator.validate_file(Path(tmp_path), 'unknown_type')
            
            assert isinstance(result, ValidationResult)
            assert not result.is_valid
            assert any('unknown' in err.lower() for err in result.errors)
        
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
