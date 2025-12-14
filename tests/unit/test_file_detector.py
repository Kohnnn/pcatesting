"""
Unit tests for FileChangeDetector.

Tests detection of new files, modified files, and unchanged files.
Requirements: 1.1
"""
import os
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.file_detector import FileChangeDetector
from src.database import DatabaseManager, PipelineRun


class TestFileChangeDetector:
    """Unit tests for FileChangeDetector class."""
    
    @pytest.fixture
    def temp_data_dir(self):
        """Create a temporary directory with test CSV files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create some test CSV files
            for name in ['close1.csv', 'buy1.csv', 'sell1.csv', 'vnindex.csv', 'rec.csv', 'rfr.csv']:
                filepath = Path(tmpdir) / name
                filepath.write_text(f"test,data\n1,2\n")
            yield tmpdir
    
    @pytest.fixture
    def mock_db_manager(self):
        """Create a mock DatabaseManager."""
        mock = MagicMock()
        mock_session = MagicMock()
        mock.Session.return_value = mock_session
        return mock
    
    def test_get_all_csv_files(self, temp_data_dir):
        """Test that all CSV files are detected."""
        detector = FileChangeDetector(data_dir=temp_data_dir)
        files = detector.get_all_csv_files()
        
        assert len(files) == 6
        filenames = [f.name for f in files]
        assert 'close1.csv' in filenames
        assert 'vnindex.csv' in filenames
        assert 'rec.csv' in filenames

    def test_get_all_csv_files_empty_dir(self):
        """Test with empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            detector = FileChangeDetector(data_dir=tmpdir)
            files = detector.get_all_csv_files()
            assert len(files) == 0
    
    def test_get_all_csv_files_nonexistent_dir(self):
        """Test with non-existent directory."""
        detector = FileChangeDetector(data_dir="/nonexistent/path")
        files = detector.get_all_csv_files()
        assert len(files) == 0
    
    def test_detect_modified_files_no_previous_run(self, temp_data_dir, mock_db_manager):
        """Test that all files are returned when no previous run exists."""
        # Mock no previous runs
        mock_session = mock_db_manager.Session.return_value
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.first.return_value = None
        
        detector = FileChangeDetector(data_dir=temp_data_dir, db_manager=mock_db_manager)
        modified = detector.detect_modified_files()
        
        # All files should be returned when no previous run
        assert len(modified) == 6
    
    def test_detect_modified_files_with_timestamp(self, temp_data_dir):
        """Test detection of files modified after a given timestamp."""
        detector = FileChangeDetector(data_dir=temp_data_dir)
        
        # Use a timestamp in the past - all files should be newer
        past_time = datetime.now() - timedelta(hours=1)
        modified = detector.detect_modified_files(since=past_time)
        assert len(modified) == 6
        
        # Use a timestamp in the future - no files should be newer
        future_time = datetime.now() + timedelta(hours=1)
        modified = detector.detect_modified_files(since=future_time)
        assert len(modified) == 0
    
    def test_detect_modified_files_partial(self, temp_data_dir):
        """Test detection when only some files are modified."""
        detector = FileChangeDetector(data_dir=temp_data_dir)
        
        # Get current time
        check_time = datetime.now()
        
        # Wait a moment and modify one file
        time.sleep(0.1)
        modified_file = Path(temp_data_dir) / 'close1.csv'
        modified_file.write_text("updated,data\n3,4\n")
        
        # Only the modified file should be detected
        modified = detector.detect_modified_files(since=check_time)
        assert len(modified) == 1
        assert modified[0].name == 'close1.csv'
    
    def test_get_file_metadata(self, temp_data_dir):
        """Test file metadata retrieval."""
        detector = FileChangeDetector(data_dir=temp_data_dir)
        filepath = Path(temp_data_dir) / 'close1.csv'
        
        metadata = detector.get_file_metadata(filepath)
        
        assert 'path' in metadata
        assert 'size' in metadata
        assert 'mtime' in metadata
        assert 'checksum' in metadata
        assert metadata['size'] > 0
        assert isinstance(metadata['mtime'], datetime)
        assert len(metadata['checksum']) == 32  # MD5 hex digest length
    
    def test_get_file_metadata_nonexistent(self, temp_data_dir):
        """Test metadata retrieval for non-existent file."""
        detector = FileChangeDetector(data_dir=temp_data_dir)
        filepath = Path(temp_data_dir) / 'nonexistent.csv'
        
        with pytest.raises(FileNotFoundError):
            detector.get_file_metadata(filepath)
    
    def test_categorize_files(self, temp_data_dir):
        """Test file categorization by type."""
        detector = FileChangeDetector(data_dir=temp_data_dir)
        categorized = detector.categorize_files()
        
        assert 'market_data' in categorized
        assert 'vnindex' in categorized
        assert 'recommendations' in categorized
        assert 'risk_free_rate' in categorized
        
        # Check market data files
        market_data_names = [f.name for f in categorized['market_data']]
        assert 'close1.csv' in market_data_names
        assert 'buy1.csv' in market_data_names
        assert 'sell1.csv' in market_data_names
        
        # Check other categories
        assert len(categorized['vnindex']) == 1
        assert categorized['vnindex'][0].name == 'vnindex.csv'
        
        assert len(categorized['recommendations']) == 1
        assert categorized['recommendations'][0].name == 'rec.csv'
        
        assert len(categorized['risk_free_rate']) == 1
        assert categorized['risk_free_rate'][0].name == 'rfr.csv'
    
    def test_categorize_files_with_unknown(self, temp_data_dir):
        """Test categorization with unknown file types."""
        # Add an unknown file
        unknown_file = Path(temp_data_dir) / 'unknown.csv'
        unknown_file.write_text("test,data\n")
        
        detector = FileChangeDetector(data_dir=temp_data_dir)
        categorized = detector.categorize_files()
        
        assert len(categorized['unknown']) == 1
        assert categorized['unknown'][0].name == 'unknown.csv'
    
    def test_has_new_files_true(self, temp_data_dir, mock_db_manager):
        """Test has_new_files returns True when files exist and no previous run."""
        mock_session = mock_db_manager.Session.return_value
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.first.return_value = None
        
        detector = FileChangeDetector(data_dir=temp_data_dir, db_manager=mock_db_manager)
        assert detector.has_new_files() is True
    
    def test_checksum_consistency(self, temp_data_dir):
        """Test that checksum is consistent for same file content."""
        detector = FileChangeDetector(data_dir=temp_data_dir)
        filepath = Path(temp_data_dir) / 'close1.csv'
        
        checksum1 = detector._calculate_checksum(filepath)
        checksum2 = detector._calculate_checksum(filepath)
        
        assert checksum1 == checksum2
    
    def test_checksum_changes_with_content(self, temp_data_dir):
        """Test that checksum changes when file content changes."""
        detector = FileChangeDetector(data_dir=temp_data_dir)
        filepath = Path(temp_data_dir) / 'close1.csv'
        
        checksum1 = detector._calculate_checksum(filepath)
        
        # Modify file content
        filepath.write_text("different,content\n5,6\n")
        
        checksum2 = detector._calculate_checksum(filepath)
        
        assert checksum1 != checksum2
