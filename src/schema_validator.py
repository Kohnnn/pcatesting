"""
Schema Validator for SentimentAlpha Vietnam Data Pipeline.

Validates CSV file structure against expected schemas for market data,
VNIndex, recommendations, and risk-free rate files.
"""
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd


@dataclass
class ValidationResult:
    """Result of schema validation."""
    is_valid: bool
    file_path: str
    schema_type: str
    errors: List[str]
    warnings: List[str]
    
    @property
    def error_message(self) -> str:
        """Get combined error message."""
        return "; ".join(self.errors) if self.errors else ""


class SchemaValidator:
    """Validates CSV file structure against expected schema."""
    
    # Expected schemas for different file types
    # Note: header_rows is the number of rows to skip before the actual column header row
    EXPECTED_SCHEMAS = {
        'market_data': {
            'header_rows': 8,  # Skip 8 rows (0-7), row 8 has "No,Date,..."
            'required_columns': ['No', 'Date'],
            'date_format': '%Y-%m-%d %H:%M:%S',
            'data_title_row': 5,  # Row containing "DE - Trading Data - Company" (1-indexed)
            'data_title_pattern': r'DE\s*-\s*Trading\s*Data\s*-\s*Company',
            'ticker_row': 8,  # Row containing ticker symbols (1-indexed)
        },
        'vnindex': {
            'header_rows': 7,  # Skip 7 rows, row 7 has "No,Index/Sector,..."
            'required_columns': ['No', 'Index/Sector', 'Level', 'Date'],
            'date_format': '%Y-%m-%d %H:%M:%S',
            'data_title_row': 5,
            'data_title_pattern': r'DE\s*-\s*TradingData\s*-\s*Index\s*&\s*Sector',
        },
        'recommendations': {
            'header_rows': 2,  # Skip 2 rows, row 2 has "Ticker,Comp name,..."
            'required_columns': ['Ticker', 'Recommendation', 'Issue date'],
            'date_format': '%Y-%m-%d %H:%M:%S',
            'optional_columns': ['Comp name', 'Analyst', 'Target price', 'Date collected'],
        },
        'risk_free_rate': {
            'header_rows': 7,  # Skip 7 rows, row 7 has "STT,Kỳ,..."
            'required_columns': ['STT', 'Kỳ', 'Ngày'],
            'date_format': '%Y-%m-%d %H:%M:%S',
            'data_title_row': 5,
            'data_title_pattern': r'DE\s*-\s*Dữ\s*liệu\s*vĩ\s*mô',
        }
    }
    
    # Filename patterns for schema type inference
    FILE_PATTERNS = {
        'market_data': [
            r'^close\d+\.csv$',
            r'^buy\d+\.csv$',
            r'^sell\d+\.csv$',
            r'^tra\d+\.csv$',
            r'^sha\d+\.csv$',
        ],
        'vnindex': [r'^vnindex\.csv$'],
        'recommendations': [r'^rec\.csv$'],
        'risk_free_rate': [r'^rfr\.csv$'],
    }

    def infer_schema_type(self, filepath: Path) -> Optional[str]:
        """
        Infer schema type from filename pattern.
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            Schema type string ('market_data', 'vnindex', 'recommendations', 
            'risk_free_rate') or None if not recognized
        """
        filename = filepath.name.lower()
        
        for schema_type, patterns in self.FILE_PATTERNS.items():
            for pattern in patterns:
                if re.match(pattern, filename):
                    return schema_type
        
        return None
    
    def validate_file(self, filepath: Path, schema_type: Optional[str] = None) -> ValidationResult:
        """
        Validate file against expected schema.
        
        Args:
            filepath: Path to the CSV file
            schema_type: Schema type to validate against. If None, inferred from filename.
            
        Returns:
            ValidationResult with validation status and any errors
        """
        filepath = Path(filepath)
        errors: List[str] = []
        warnings: List[str] = []
        
        # Infer schema type if not provided
        if schema_type is None:
            schema_type = self.infer_schema_type(filepath)
        
        if schema_type is None:
            return ValidationResult(
                is_valid=False,
                file_path=str(filepath),
                schema_type='unknown',
                errors=[f"Cannot infer schema type from filename: {filepath.name}"],
                warnings=[]
            )
        
        # Check file exists
        if not filepath.exists():
            return ValidationResult(
                is_valid=False,
                file_path=str(filepath),
                schema_type=schema_type,
                errors=[f"File not found: {filepath}"],
                warnings=[]
            )
        
        schema = self.EXPECTED_SCHEMAS.get(schema_type)
        if schema is None:
            return ValidationResult(
                is_valid=False,
                file_path=str(filepath),
                schema_type=schema_type,
                errors=[f"Unknown schema type: {schema_type}"],
                warnings=[]
            )
        
        # Validate structure
        structure_errors, structure_warnings = self._validate_structure(filepath, schema, schema_type)
        errors.extend(structure_errors)
        warnings.extend(structure_warnings)
        
        # Validate columns
        column_errors, column_warnings = self._validate_columns(filepath, schema, schema_type)
        errors.extend(column_errors)
        warnings.extend(column_warnings)
        
        # Validate date format (sample check)
        date_errors, date_warnings = self._validate_date_format(filepath, schema, schema_type)
        errors.extend(date_errors)
        warnings.extend(date_warnings)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            file_path=str(filepath),
            schema_type=schema_type,
            errors=errors,
            warnings=warnings
        )

    def _validate_structure(
        self, filepath: Path, schema: Dict, schema_type: str
    ) -> Tuple[List[str], List[str]]:
        """Validate file structure (header rows, data title)."""
        errors: List[str] = []
        warnings: List[str] = []
        
        try:
            # Read raw file to check structure
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = [f.readline() for _ in range(10)]
            
            # Check data title if applicable
            if 'data_title_pattern' in schema and 'data_title_row' in schema:
                title_row_idx = schema['data_title_row'] - 1  # Convert to 0-indexed
                if title_row_idx < len(lines):
                    title_line = lines[title_row_idx]
                    pattern = schema['data_title_pattern']
                    if not re.search(pattern, title_line, re.IGNORECASE):
                        warnings.append(
                            f"Data title row {schema['data_title_row']} does not match "
                            f"expected pattern for {schema_type}"
                        )
        except Exception as e:
            errors.append(f"Error reading file structure: {str(e)}")
        
        return errors, warnings
    
    def _validate_columns(
        self, filepath: Path, schema: Dict, schema_type: str
    ) -> Tuple[List[str], List[str]]:
        """Validate required columns exist."""
        errors: List[str] = []
        warnings: List[str] = []
        
        try:
            header_rows = schema.get('header_rows', 0)
            
            # Read just the header to check columns
            df = pd.read_csv(filepath, skiprows=header_rows, nrows=0)
            columns = [str(col).strip() for col in df.columns]
            
            # For market_data, columns are ticker symbols after No and Date
            if schema_type == 'market_data':
                # Check for No and Date columns
                has_no = any('No' in col or col == 'No' for col in columns)
                has_date = any('Date' in col for col in columns)
                
                if not has_no:
                    errors.append("Missing required column: 'No'")
                if not has_date:
                    errors.append("Missing required column: 'Date'")
                    
                # Check that there are ticker columns (3-letter uppercase)
                ticker_cols = [c for c in columns if re.match(r'^[A-Z]{3}$', c)]
                if len(ticker_cols) == 0:
                    warnings.append("No ticker columns found (expected 3-letter uppercase symbols)")
            else:
                # Standard column check for other types
                required_columns = schema.get('required_columns', [])
                for req_col in required_columns:
                    # Flexible matching - check if column name contains required text
                    found = any(req_col in col for col in columns)
                    if not found:
                        errors.append(f"Missing required column: '{req_col}'")
                
        except Exception as e:
            errors.append(f"Error reading columns: {str(e)}")
        
        return errors, warnings
    
    def _validate_date_format(
        self, filepath: Path, schema: Dict, schema_type: str
    ) -> Tuple[List[str], List[str]]:
        """Validate date format in data rows."""
        errors: List[str] = []
        warnings: List[str] = []
        
        try:
            header_rows = schema.get('header_rows', 0)
            date_format = schema.get('date_format', '%Y-%m-%d %H:%M:%S')
            
            # Read a few data rows to check date format
            df = pd.read_csv(filepath, skiprows=header_rows, nrows=5)
            
            # Find date column
            date_col = None
            for col in df.columns:
                col_lower = str(col).lower()
                if 'date' in col_lower or col_lower == 'ngày' or col_lower == 'kỳ':
                    date_col = col
                    break
            
            if date_col is None:
                # Date column not found, but this might be caught by column validation
                return errors, warnings
            
            # Check date format on sample rows
            for idx, value in enumerate(df[date_col].dropna().head(3)):
                try:
                    if pd.isna(value):
                        continue
                    # Try parsing with expected format
                    datetime.strptime(str(value), date_format)
                except ValueError:
                    # Try alternative formats
                    parsed = False
                    for alt_format in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
                        try:
                            datetime.strptime(str(value), alt_format)
                            parsed = True
                            warnings.append(
                                f"Date format differs from expected. Found: {value}, "
                                f"expected format: {date_format}"
                            )
                            break
                        except ValueError:
                            continue
                    
                    if not parsed:
                        errors.append(
                            f"Invalid date format in row {idx + 1}: '{value}'. "
                            f"Expected format: {date_format}"
                        )
                    break  # Only report first date format issue
                    
        except Exception as e:
            warnings.append(f"Could not validate date format: {str(e)}")
        
        return errors, warnings

    def validate_all_files(self, data_dir: str = "xlsx") -> Dict[str, List[ValidationResult]]:
        """
        Validate all CSV files in a directory.
        
        Args:
            data_dir: Directory containing CSV files
            
        Returns:
            Dictionary mapping schema type to list of validation results
        """
        data_path = Path(data_dir)
        results: Dict[str, List[ValidationResult]] = {
            'market_data': [],
            'vnindex': [],
            'recommendations': [],
            'risk_free_rate': [],
            'unknown': []
        }
        
        if not data_path.exists():
            return results
        
        for filepath in sorted(data_path.glob("*.csv")):
            schema_type = self.infer_schema_type(filepath)
            result = self.validate_file(filepath, schema_type)
            
            category = schema_type if schema_type else 'unknown'
            results[category].append(result)
        
        return results
    
    def get_valid_files(self, data_dir: str = "xlsx") -> Dict[str, List[Path]]:
        """
        Get all valid files grouped by schema type.
        
        Args:
            data_dir: Directory containing CSV files
            
        Returns:
            Dictionary mapping schema type to list of valid file paths
        """
        all_results = self.validate_all_files(data_dir)
        valid_files: Dict[str, List[Path]] = {}
        
        for schema_type, results in all_results.items():
            valid_files[schema_type] = [
                Path(r.file_path) for r in results if r.is_valid
            ]
        
        return valid_files
    
    def get_schema_info(self, schema_type: str) -> Optional[Dict]:
        """
        Get schema information for a given type.
        
        Args:
            schema_type: Type of schema to retrieve
            
        Returns:
            Schema dictionary or None if not found
        """
        return self.EXPECTED_SCHEMAS.get(schema_type)
