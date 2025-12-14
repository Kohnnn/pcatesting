"""
File Change Detector for SentimentAlpha Vietnam Data Pipeline.

Detects new or modified CSV files since the last pipeline run.
"""
import hashlib
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.database import DatabaseManager, PipelineRun


class FileChangeDetector:
    """Detects new or modified CSV files since last pipeline run."""
    
    # Expected file patterns in the data directory
    FILE_PATTERNS = {
        'market_data': ['close', 'buy', 'sell', 'tra', 'sha'],
        'vnindex': ['vnindex'],
        'recommendations': ['rec'],
        'risk_free_rate': ['rfr']
    }
    
    def __init__(self, data_dir: Optional[str] = None, db_manager: Optional[DatabaseManager] = None):
        """
        Initialize FileChangeDetector.
        
        Args:
            data_dir: Directory containing CSV files (defaults to DATA_SOURCE_DIR env var or 'xlsx')
            db_manager: DatabaseManager instance for querying pipeline_runs
        """
        import os
        if data_dir is None:
            data_dir = os.getenv("DATA_SOURCE_DIR", "xlsx")
        self.data_dir = Path(data_dir)
        self.db_manager = db_manager or DatabaseManager()
    
    def get_last_run_timestamp(self) -> Optional[datetime]:
        """
        Get timestamp of last successful pipeline run from database.
        
        Returns:
            Datetime of last successful run, or None if no runs exist
        """
        session = self.db_manager.Session()
        try:
            last_run = session.query(PipelineRun).filter(
                PipelineRun.status.in_(['success', 'partial'])
            ).order_by(desc(PipelineRun.completed_at)).first()
            
            if last_run and last_run.completed_at:
                return last_run.completed_at
            return None
        finally:
            session.close()

    def detect_modified_files(self, since: Optional[datetime] = None) -> List[Path]:
        """
        Return list of files modified since the given timestamp.
        
        If no timestamp is provided, uses the last successful pipeline run timestamp.
        If no previous run exists, returns all CSV files.
        
        Args:
            since: Optional datetime to compare against. If None, uses last run timestamp.
            
        Returns:
            List of Path objects for modified files
        """
        if since is None:
            since = self.get_last_run_timestamp()
        
        modified_files = []
        
        if not self.data_dir.exists():
            return modified_files
        
        for filepath in self.data_dir.glob("*.csv"):
            if since is None:
                # No previous run, include all files
                modified_files.append(filepath)
            else:
                # Check if file was modified after the last run
                mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                if mtime > since:
                    modified_files.append(filepath)
        
        return sorted(modified_files)
    
    def get_file_metadata(self, filepath: Path) -> Dict:
        """
        Return file metadata including size, modification time, and checksum.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Dictionary with keys: size, mtime, checksum
        """
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        stat = filepath.stat()
        
        return {
            'path': str(filepath),
            'size': stat.st_size,
            'mtime': datetime.fromtimestamp(stat.st_mtime),
            'checksum': self._calculate_checksum(filepath)
        }
    
    def _calculate_checksum(self, filepath: Path, chunk_size: int = 8192) -> str:
        """
        Calculate MD5 checksum of a file.
        
        Args:
            filepath: Path to the file
            chunk_size: Size of chunks to read
            
        Returns:
            MD5 hex digest string
        """
        md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5.update(chunk)
        return md5.hexdigest()
    
    def get_all_csv_files(self) -> List[Path]:
        """
        Get all CSV files in the data directory.
        
        Returns:
            List of Path objects for all CSV files
        """
        if not self.data_dir.exists():
            return []
        return sorted(self.data_dir.glob("*.csv"))
    
    def categorize_files(self, files: Optional[List[Path]] = None) -> Dict[str, List[Path]]:
        """
        Categorize files by their type based on filename patterns.
        
        Args:
            files: List of files to categorize. If None, uses all CSV files.
            
        Returns:
            Dictionary mapping category to list of files
        """
        if files is None:
            files = self.get_all_csv_files()
        
        categorized = {
            'market_data': [],
            'vnindex': [],
            'recommendations': [],
            'risk_free_rate': [],
            'unknown': []
        }
        
        for filepath in files:
            filename = filepath.stem.lower()
            categorized_flag = False
            
            # Check market data patterns (close1-9, buy1-9, etc.)
            for pattern in self.FILE_PATTERNS['market_data']:
                if filename.startswith(pattern) and filename[len(pattern):].isdigit():
                    categorized['market_data'].append(filepath)
                    categorized_flag = True
                    break
            
            if categorized_flag:
                continue
            
            # Check other patterns
            if filename == 'vnindex':
                categorized['vnindex'].append(filepath)
            elif filename == 'rec':
                categorized['recommendations'].append(filepath)
            elif filename == 'rfr':
                categorized['risk_free_rate'].append(filepath)
            else:
                categorized['unknown'].append(filepath)
        
        return categorized
    
    def has_new_files(self) -> bool:
        """
        Check if there are any new or modified files since last run.
        
        Returns:
            True if there are modified files, False otherwise
        """
        return len(self.detect_modified_files()) > 0
