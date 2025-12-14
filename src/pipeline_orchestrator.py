"""
Pipeline Orchestrator for SentimentAlpha Vietnam Data Pipeline.

Orchestrates the complete ETL process including:
- File change detection
- Schema validation
- Data loading and transformation
- Incremental database updates
- Pipeline execution reporting
"""
import json
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Any

import pandas as pd
from sqlalchemy.sql import func

from src.database import (
    DatabaseManager, PipelineRun, MarketData, VNIndex, 
    RiskFreeRate, AnalystRecommendation, Instrument
)
from src.file_detector import FileChangeDetector
from src.schema_validator import SchemaValidator, ValidationResult
from src.data_loader import DataLoader
from src.data_transformer import DataTransformer
from src.data_validator import DataValidator
from src.resource_monitor import ResourceMonitor, force_garbage_collection


@dataclass
class ProcessingResult:
    """Result of processing a single file or file group."""
    file_type: str
    files_processed: List[str]
    records_inserted: int
    records_updated: int
    errors: List[str]
    warnings: List[str]
    
    @property
    def is_success(self) -> bool:
        """Check if processing was successful (no errors)."""
        return len(self.errors) == 0


@dataclass
class PipelineReport:
    """Summary report of pipeline execution."""
    run_id: int
    started_at: datetime
    completed_at: Optional[datetime]
    status: str  # 'running', 'success', 'partial', 'failed'
    files_processed: int
    records_inserted: int
    records_updated: int
    errors_count: int
    error_details: List[str]
    processing_results: List[ProcessingResult] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            'run_id': self.run_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'status': self.status,
            'files_processed': self.files_processed,
            'records_inserted': self.records_inserted,
            'records_updated': self.records_updated,
            'errors_count': self.errors_count,
            'error_details': self.error_details,
        }


class PipelineOrchestrator:
    """
    Orchestrates the complete data pipeline execution.
    
    Coordinates file detection, validation, transformation, and loading
    to perform incremental database updates from CSV files.
    """
    
    def __init__(
        self,
        db_manager: Optional[DatabaseManager] = None,
        data_dir: Optional[str] = None
    ):
        """
        Initialize PipelineOrchestrator.
        
        Args:
            db_manager: DatabaseManager instance for database operations
            data_dir: Directory containing CSV files (defaults to DATA_SOURCE_DIR env var or 'xlsx')
        """
        import os
        if data_dir is None:
            data_dir = os.getenv("DATA_SOURCE_DIR", "xlsx")
        
        self.db = db_manager or DatabaseManager()
        self._owns_db = db_manager is None  # Track if we created the db_manager
        self.data_dir = data_dir
        self.detector = FileChangeDetector(data_dir, self.db)
        self.validator = SchemaValidator()
        self.loader = DataLoader(data_dir)
        self.transformer = DataTransformer()
        self.data_validator = DataValidator()
        self.monitor = ResourceMonitor(log_interval=5)
        
        # Ensure tables exist
        self.db.create_tables()
    
    def cleanup(self) -> None:
        """
        Clean up resources. Call this when done with the orchestrator.
        """
        if self._owns_db and hasattr(self, 'db'):
            self.db.dispose()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures cleanup."""
        self.cleanup()
        return False
    
    def run_pipeline(self, force_full: bool = False) -> PipelineReport:
        """
        Execute the complete pipeline.
        
        Property 3: Incremental Update Correctness
        For any database with existing data up to date D, running the pipeline
        with new data should only insert records with dates > D, and existing
        records should remain unchanged.
        
        Args:
            force_full: If True, process all files regardless of modification time
            
        Returns:
            PipelineReport with execution summary
        """
        # Start resource monitoring
        self.monitor.start_monitoring()
        self.monitor.log_resource_usage("Pipeline start", force=True)
        
        # Check resource limits before starting
        limits = self.monitor.check_resource_limits(max_memory_percent=85.0, min_disk_free_gb=1.0)
        if not limits["memory_ok"] or not limits["disk_ok"]:
            raise RuntimeError(
                f"Insufficient resources to run pipeline. "
                f"Memory: {limits['memory_percent']:.1f}%, "
                f"Disk free: {limits['disk_free_gb']:.2f} GB"
            )
        
        # Create pipeline run record
        session = self.db.Session()
        pipeline_run = PipelineRun(
            started_at=datetime.now(),
            status='running',
            files_processed=0,
            records_inserted=0,
            records_updated=0,
            errors_count=0
        )
        session.add(pipeline_run)
        session.commit()
        run_id = pipeline_run.id
        session.close()
        
        # Initialize report
        report = PipelineReport(
            run_id=run_id,
            started_at=pipeline_run.started_at,
            completed_at=None,
            status='running',
            files_processed=0,
            records_inserted=0,
            records_updated=0,
            errors_count=0,
            error_details=[]
        )
        
        try:
            # Detect files to process
            self.monitor.log_resource_usage("File detection")
            if force_full:
                files = self.detector.get_all_csv_files()
            else:
                files = self.detector.detect_modified_files()
            
            if not files:
                report.status = 'success'
                report.completed_at = datetime.now()
                self._update_pipeline_run(run_id, report)
                self.monitor.log_resource_usage("Pipeline complete (no files)", force=True)
                self.monitor.get_summary()
                return report
            
            # Categorize files
            categorized = self.detector.categorize_files(files)
            
            # Process market data files
            if categorized.get('market_data'):
                self.monitor.log_resource_usage("Before market data processing", force=True)
                result = self.process_market_data(categorized['market_data'])
                report.processing_results.append(result)
                report.files_processed += len(result.files_processed)
                report.records_inserted += result.records_inserted
                report.records_updated += result.records_updated
                report.error_details.extend(result.errors)
                # Force garbage collection after large operation
                force_garbage_collection()
                self.monitor.log_resource_usage("After market data processing", force=True)
            
            # Process VNIndex
            if categorized.get('vnindex'):
                self.monitor.log_resource_usage("VNIndex processing")
                result = self.process_vnindex(categorized['vnindex'])
                report.processing_results.append(result)
                report.files_processed += len(result.files_processed)
                report.records_inserted += result.records_inserted
                report.records_updated += result.records_updated
                report.error_details.extend(result.errors)
            
            # Process recommendations
            if categorized.get('recommendations'):
                self.monitor.log_resource_usage("Recommendations processing")
                result = self.process_recommendations(categorized['recommendations'])
                report.processing_results.append(result)
                report.files_processed += len(result.files_processed)
                report.records_inserted += result.records_inserted
                report.records_updated += result.records_updated
                report.error_details.extend(result.errors)
            
            # Process risk-free rate
            if categorized.get('risk_free_rate'):
                self.monitor.log_resource_usage("Risk-free rate processing")
                result = self.process_risk_free_rate(categorized['risk_free_rate'])
                report.processing_results.append(result)
                report.files_processed += len(result.files_processed)
                report.records_inserted += result.records_inserted
                report.records_updated += result.records_updated
                report.error_details.extend(result.errors)
            
            # Determine final status
            report.errors_count = len(report.error_details)
            if report.errors_count == 0:
                report.status = 'success'
            elif report.records_inserted > 0 or report.records_updated > 0:
                report.status = 'partial'
            else:
                report.status = 'failed'
            
            report.completed_at = datetime.now()
            
        except Exception as e:
            report.status = 'failed'
            report.error_details.append(f"Pipeline error: {str(e)}")
            report.errors_count = len(report.error_details)
            report.completed_at = datetime.now()
        
        # Update pipeline run record
        self._update_pipeline_run(run_id, report)
        
        # Force garbage collection to release DataFrame memory
        force_garbage_collection()
        
        # Log final resource usage and summary
        self.monitor.log_resource_usage("Pipeline complete", force=True)
        self.monitor.get_summary()
        
        return report
    
    def _update_pipeline_run(self, run_id: int, report: PipelineReport) -> None:
        """Update pipeline run record with final results."""
        session = self.db.Session()
        try:
            pipeline_run = session.query(PipelineRun).filter_by(id=run_id).first()
            if pipeline_run:
                pipeline_run.completed_at = report.completed_at
                pipeline_run.status = report.status
                pipeline_run.files_processed = report.files_processed
                pipeline_run.records_inserted = report.records_inserted
                pipeline_run.records_updated = report.records_updated
                pipeline_run.errors_count = report.errors_count
                # Truncate error details to prevent database bloat (max 100 errors)
                truncated_errors = report.error_details[:100]
                if len(report.error_details) > 100:
                    truncated_errors.append(f"... and {len(report.error_details) - 100} more errors (truncated)")
                pipeline_run.error_details = json.dumps(truncated_errors)
                session.commit()
        finally:
            session.close()

    
    def process_market_data(self, files: List[Path]) -> ProcessingResult:
        """
        Process market data files (close, buy, sell, tra, sha).
        
        Merges fragmented files, transforms to long format, and loads to database.
        
        Args:
            files: List of market data file paths
            
        Returns:
            ProcessingResult with processing summary
        """
        errors = []
        warnings = []
        records_inserted = 0
        records_updated = 0
        processed_files = []
        
        # Validate files first
        valid_files = []
        for filepath in files:
            result = self.validator.validate_file(filepath, 'market_data')
            if result.is_valid:
                valid_files.append(filepath)
                processed_files.append(str(filepath))
            else:
                errors.extend(result.errors)
                warnings.extend(result.warnings)
        
        if not valid_files:
            return ProcessingResult(
                file_type='market_data',
                files_processed=processed_files,
                records_inserted=0,
                records_updated=0,
                errors=errors,
                warnings=warnings
            )
        
        try:
            # Group files by prefix (close, buy, sell, tra, sha)
            file_groups = self._group_market_files(valid_files)
            
            # Load and merge each type
            dfs = {}
            for prefix in ['close', 'buy', 'sell', 'tra', 'sha']:
                if prefix in file_groups:
                    try:
                        merged_df = self.loader.merge_fragmented_files(prefix)
                        dfs[prefix] = merged_df
                    except Exception as e:
                        errors.append(f"Error loading {prefix} files: {str(e)}")
            
            # Need at least close prices to proceed
            if 'close' not in dfs:
                errors.append("No close price data available")
                return ProcessingResult(
                    file_type='market_data',
                    files_processed=processed_files,
                    records_inserted=0,
                    records_updated=0,
                    errors=errors,
                    warnings=warnings
                )
            
            # Transform and merge market data
            result = self.transformer.merge_market_data(
                close_df=dfs.get('close', pd.DataFrame()),
                buy_df=dfs.get('buy', pd.DataFrame()),
                sell_df=dfs.get('sell', pd.DataFrame()),
                tra_df=dfs.get('tra', pd.DataFrame()),
                sha_df=dfs.get('sha', pd.DataFrame()),
                validate=True
            )
            
            # Add transformation errors
            for err in result.errors:
                errors.append(str(err))
            
            if result.data.empty:
                return ProcessingResult(
                    file_type='market_data',
                    files_processed=processed_files,
                    records_inserted=0,
                    records_updated=0,
                    errors=errors,
                    warnings=warnings
                )
            
            # Get latest date for incremental update
            latest_date = self.db.get_latest_date('market_data')
            
            # Filter to only new records
            if latest_date:
                new_data = result.data[result.data['date'] > pd.Timestamp(latest_date)]
            else:
                new_data = result.data
            
            # Validate data before insertion
            validation_result = self.data_validator.validate_market_data(new_data)
            for anomaly in validation_result.anomalies:
                warnings.append(str(anomaly))
            
            # Insert to database
            if not new_data.empty:
                records_inserted = self.db.upsert_market_data(new_data)
            
        except Exception as e:
            errors.append(f"Market data processing error: {str(e)}")
        
        return ProcessingResult(
            file_type='market_data',
            files_processed=processed_files,
            records_inserted=records_inserted,
            records_updated=records_updated,
            errors=errors,
            warnings=warnings
        )
    
    def _group_market_files(self, files: List[Path]) -> Dict[str, List[Path]]:
        """Group market data files by prefix."""
        groups = {}
        for filepath in files:
            filename = filepath.stem.lower()
            for prefix in ['close', 'buy', 'sell', 'tra', 'sha']:
                if filename.startswith(prefix):
                    if prefix not in groups:
                        groups[prefix] = []
                    groups[prefix].append(filepath)
                    break
        return groups
    
    def process_vnindex(self, files: List[Path]) -> ProcessingResult:
        """
        Process VNIndex benchmark data.
        
        Args:
            files: List of VNIndex file paths (typically just one)
            
        Returns:
            ProcessingResult with processing summary
        """
        errors = []
        warnings = []
        records_inserted = 0
        processed_files = []
        
        for filepath in files:
            # Validate file
            result = self.validator.validate_file(filepath, 'vnindex')
            if not result.is_valid:
                errors.extend(result.errors)
                continue
            
            processed_files.append(str(filepath))
            
            try:
                # Load VNIndex data
                df = self.loader.load_vnindex()
                
                # Get latest date for incremental update
                latest_date = self.db.get_latest_date('vnindex')
                
                # Filter to only new records
                if latest_date:
                    df = df[df['Date'] > pd.Timestamp(latest_date)]
                
                if df.empty:
                    continue
                
                # Insert to database
                session = self.db.Session()
                try:
                    for _, row in df.iterrows():
                        vnindex = VNIndex(
                            date=row['Date'].date() if hasattr(row['Date'], 'date') else row['Date'],
                            close_index=row.get('close_index'),
                            buy_volume=row.get('buy_volume'),
                            sell_volume=row.get('sell_volume'),
                            total_volume=row.get('total_volume')
                        )
                        session.merge(vnindex)
                        records_inserted += 1
                    session.commit()
                finally:
                    session.close()
                    
            except Exception as e:
                errors.append(f"VNIndex processing error: {str(e)}")
        
        return ProcessingResult(
            file_type='vnindex',
            files_processed=processed_files,
            records_inserted=records_inserted,
            records_updated=0,
            errors=errors,
            warnings=warnings
        )

    
    def process_recommendations(self, files: List[Path]) -> ProcessingResult:
        """
        Process recommendations file with rating standardization.
        
        Args:
            files: List of recommendation file paths (typically just rec.csv)
            
        Returns:
            ProcessingResult with processing summary
        """
        errors = []
        warnings = []
        records_inserted = 0
        processed_files = []
        
        for filepath in files:
            # Validate file
            result = self.validator.validate_file(filepath, 'recommendations')
            if not result.is_valid:
                errors.extend(result.errors)
                continue
            
            processed_files.append(str(filepath))
            
            try:
                # Load recommendations
                df = self.loader.load_recommendations()
                
                # Validate dates
                validation_result = self.data_validator.validate_recommendations(df)
                for err in validation_result.date_errors:
                    warnings.append(err)
                for anomaly in validation_result.anomalies:
                    warnings.append(str(anomaly))
                
                # Standardize ratings
                transform_result = self.transformer.standardize_ratings_batch(
                    df, rating_column='Recommendation'
                )
                
                # Add transformation errors as warnings
                for err in transform_result.errors:
                    warnings.append(str(err))
                
                df_with_ratings = transform_result.data
                
                # Rename columns back to expected format for database
                df_with_ratings = df_with_ratings.rename(columns={
                    'ticker': 'Ticker',
                    'comp name': 'Comp name',
                    'analyst': 'Analyst',
                    'recommendation': 'Recommendation',
                    'target price': 'Target price',
                    'issue date': 'Issue date'
                })
                
                # Get latest date for incremental update
                latest_date = self.db.get_latest_date('analyst_recommendations')
                
                # Filter to only new records
                if latest_date and 'Issue date' in df_with_ratings.columns:
                    df_with_ratings = df_with_ratings[
                        df_with_ratings['Issue date'] > pd.Timestamp(latest_date)
                    ]
                
                if df_with_ratings.empty:
                    continue
                
                # Insert to database
                records_inserted += self.db.upsert_recommendations(df_with_ratings)
                
            except Exception as e:
                errors.append(f"Recommendations processing error: {str(e)}")
        
        return ProcessingResult(
            file_type='recommendations',
            files_processed=processed_files,
            records_inserted=records_inserted,
            records_updated=0,
            errors=errors,
            warnings=warnings
        )
    
    def process_risk_free_rate(self, files: List[Path]) -> ProcessingResult:
        """
        Process risk-free rate data.
        
        Args:
            files: List of risk-free rate file paths (typically just rfr.csv)
            
        Returns:
            ProcessingResult with processing summary
        """
        errors = []
        warnings = []
        records_inserted = 0
        processed_files = []
        
        for filepath in files:
            # Validate file
            result = self.validator.validate_file(filepath, 'risk_free_rate')
            if not result.is_valid:
                errors.extend(result.errors)
                continue
            
            processed_files.append(str(filepath))
            
            try:
                # Load risk-free rate data
                df = self.loader.load_risk_free_rate()
                
                # Get latest date for incremental update
                latest_date = self.db.get_latest_date('risk_free_rate')
                
                # Filter to only new records
                if latest_date:
                    df = df[df['Date'] > pd.Timestamp(latest_date)]
                
                if df.empty:
                    continue
                
                # Insert to database
                session = self.db.Session()
                try:
                    for _, row in df.iterrows():
                        rfr = RiskFreeRate(
                            date=row['Date'].date() if hasattr(row['Date'], 'date') else row['Date'],
                            rate=row.get('rate')
                        )
                        session.merge(rfr)
                        records_inserted += 1
                    session.commit()
                finally:
                    session.close()
                    
            except Exception as e:
                errors.append(f"Risk-free rate processing error: {str(e)}")
        
        return ProcessingResult(
            file_type='risk_free_rate',
            files_processed=processed_files,
            records_inserted=records_inserted,
            records_updated=0,
            errors=errors,
            warnings=warnings
        )
    
    def generate_report(self, results: List[ProcessingResult]) -> PipelineReport:
        """
        Generate summary report from processing results.
        
        Args:
            results: List of ProcessingResult objects
            
        Returns:
            PipelineReport with aggregated statistics
        """
        total_files = 0
        total_inserted = 0
        total_updated = 0
        all_errors = []
        
        for result in results:
            total_files += len(result.files_processed)
            total_inserted += result.records_inserted
            total_updated += result.records_updated
            all_errors.extend(result.errors)
        
        # Determine status
        if len(all_errors) == 0:
            status = 'success'
        elif total_inserted > 0 or total_updated > 0:
            status = 'partial'
        else:
            status = 'failed'
        
        return PipelineReport(
            run_id=0,  # Will be set by caller
            started_at=datetime.now(),
            completed_at=datetime.now(),
            status=status,
            files_processed=total_files,
            records_inserted=total_inserted,
            records_updated=total_updated,
            errors_count=len(all_errors),
            error_details=all_errors,
            processing_results=results
        )
    
    def get_pipeline_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get history of pipeline runs.
        
        Args:
            limit: Maximum number of runs to return
            
        Returns:
            List of pipeline run dictionaries
        """
        session = self.db.Session()
        try:
            runs = session.query(PipelineRun).order_by(
                PipelineRun.started_at.desc()
            ).limit(limit).all()
            
            return [
                {
                    'id': run.id,
                    'started_at': run.started_at.isoformat() if run.started_at else None,
                    'completed_at': run.completed_at.isoformat() if run.completed_at else None,
                    'status': run.status,
                    'files_processed': run.files_processed,
                    'records_inserted': run.records_inserted,
                    'records_updated': run.records_updated,
                    'errors_count': run.errors_count,
                    'error_details': json.loads(run.error_details) if run.error_details else []
                }
                for run in runs
            ]
        finally:
            session.close()
    
    def get_pipeline_status(self, run_id: int) -> Optional[Dict[str, Any]]:
        """
        Get status of a specific pipeline run.
        
        Args:
            run_id: ID of the pipeline run
            
        Returns:
            Pipeline run dictionary or None if not found
        """
        session = self.db.Session()
        try:
            run = session.query(PipelineRun).filter_by(id=run_id).first()
            if not run:
                return None
            
            return {
                'id': run.id,
                'started_at': run.started_at.isoformat() if run.started_at else None,
                'completed_at': run.completed_at.isoformat() if run.completed_at else None,
                'status': run.status,
                'files_processed': run.files_processed,
                'records_inserted': run.records_inserted,
                'records_updated': run.records_updated,
                'errors_count': run.errors_count,
                'error_details': json.loads(run.error_details) if run.error_details else []
            }
        finally:
            session.close()
