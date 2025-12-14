"""
Integration tests for PipelineOrchestrator.

Tests complete pipeline execution with real CSV files.
**Feature: data-management-refactor**
"""
import pytest
import sys
import os
import tempfile
import shutil
from pathlib import Path
from datetime import date, datetime

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from src.database import DatabaseManager, PipelineRun, MarketData, AnalystRecommendation
from src.pipeline_orchestrator import PipelineOrchestrator, ProcessingResult, PipelineReport
from src.file_detector import FileChangeDetector
from src.schema_validator import SchemaValidator


class TestPipelineIntegration:
    """Integration tests for PipelineOrchestrator with real CSV files."""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        db = DatabaseManager(db_path)
        db.create_tables()
        
        yield db, db_path
        
        # Cleanup
        db.engine.dispose()
        if os.path.exists(db_path):
            try:
                os.unlink(db_path)
            except PermissionError:
                pass
    
    @pytest.fixture
    def xlsx_dir(self):
        """Get the xlsx directory path."""
        xlsx_path = Path(__file__).parent.parent.parent / "xlsx"
        if not xlsx_path.exists():
            pytest.skip("xlsx directory not found")
        return str(xlsx_path)
    
    def test_full_pipeline_execution(self, temp_db, xlsx_dir):
        """
        Test complete pipeline execution with real CSV files.
        
        _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8_
        """
        db, db_path = temp_db
        
        # Create orchestrator
        orchestrator = PipelineOrchestrator(db_manager=db, data_dir=xlsx_dir)
        
        # Run pipeline
        report = orchestrator.run_pipeline(force_full=True)
        
        # Verify pipeline completed
        assert report.status in ['success', 'partial'], \
            f"Pipeline failed with status: {report.status}, errors: {report.error_details}"
        
        # Verify files were processed
        assert report.files_processed > 0, "No files were processed"
        
        # Verify records were inserted
        assert report.records_inserted > 0, "No records were inserted"
        
        # Verify pipeline run was recorded (Property 4: Pipeline Audit Trail)
        session = db.Session()
        try:
            pipeline_run = session.query(PipelineRun).filter_by(id=report.run_id).first()
            assert pipeline_run is not None, "Pipeline run not recorded in database"
            assert pipeline_run.status == report.status
            assert pipeline_run.files_processed == report.files_processed
            assert pipeline_run.records_inserted == report.records_inserted
        finally:
            session.close()
    
    def test_pipeline_creates_audit_trail(self, temp_db, xlsx_dir):
        """
        Test that pipeline creates proper audit trail.
        
        **Property 4: Pipeline Audit Trail**
        **Validates: Requirements 1.8**
        """
        db, db_path = temp_db
        
        orchestrator = PipelineOrchestrator(db_manager=db, data_dir=xlsx_dir)
        
        # Run pipeline
        report = orchestrator.run_pipeline(force_full=True)
        
        # Verify audit trail
        session = db.Session()
        try:
            pipeline_run = session.query(PipelineRun).filter_by(id=report.run_id).first()
            
            assert pipeline_run is not None, "Pipeline run not recorded"
            assert pipeline_run.started_at is not None, "started_at not recorded"
            assert pipeline_run.completed_at is not None, "completed_at not recorded"
            assert pipeline_run.status in ['running', 'success', 'partial', 'failed']
            assert pipeline_run.files_processed >= 0
            assert pipeline_run.records_inserted >= 0
            assert pipeline_run.errors_count >= 0
        finally:
            session.close()
    
    def test_incremental_update(self, temp_db, xlsx_dir):
        """
        Test that second pipeline run performs incremental update.
        
        **Property 3: Incremental Update Correctness**
        **Validates: Requirements 1.6**
        """
        db, db_path = temp_db
        
        orchestrator = PipelineOrchestrator(db_manager=db, data_dir=xlsx_dir)
        
        # First run - full load
        report1 = orchestrator.run_pipeline(force_full=True)
        
        # Get record count after first run
        session = db.Session()
        try:
            count_after_first = session.query(MarketData).count()
        finally:
            session.close()
        
        # Second run - should be incremental (no new files modified)
        report2 = orchestrator.run_pipeline(force_full=False)
        
        # Get record count after second run
        session = db.Session()
        try:
            count_after_second = session.query(MarketData).count()
        finally:
            session.close()
        
        # Record count should be the same (no new data)
        assert count_after_second == count_after_first, \
            "Incremental update should not insert duplicate records"
    
    def test_pipeline_history(self, temp_db, xlsx_dir):
        """
        Test pipeline history retrieval.
        
        _Requirements: 2.8_
        """
        db, db_path = temp_db
        
        orchestrator = PipelineOrchestrator(db_manager=db, data_dir=xlsx_dir)
        
        # Run pipeline twice
        orchestrator.run_pipeline(force_full=True)
        orchestrator.run_pipeline(force_full=False)
        
        # Get history
        history = orchestrator.get_pipeline_history(limit=10)
        
        assert len(history) >= 2, "Should have at least 2 pipeline runs in history"
        
        # Verify history structure
        for run in history:
            assert 'id' in run
            assert 'started_at' in run
            assert 'status' in run
            assert 'files_processed' in run
    
    def test_pipeline_status(self, temp_db, xlsx_dir):
        """
        Test pipeline status retrieval.
        
        _Requirements: 2.7_
        """
        db, db_path = temp_db
        
        orchestrator = PipelineOrchestrator(db_manager=db, data_dir=xlsx_dir)
        
        # Run pipeline
        report = orchestrator.run_pipeline(force_full=True)
        
        # Get status
        status = orchestrator.get_pipeline_status(report.run_id)
        
        assert status is not None, "Pipeline status should be retrievable"
        assert status['id'] == report.run_id
        assert status['status'] == report.status
        assert status['files_processed'] == report.files_processed


class TestFileDetectorIntegration:
    """Integration tests for FileChangeDetector."""
    
    @pytest.fixture
    def xlsx_dir(self):
        """Get the xlsx directory path."""
        xlsx_path = Path(__file__).parent.parent.parent / "xlsx"
        if not xlsx_path.exists():
            pytest.skip("xlsx directory not found")
        return str(xlsx_path)
    
    def test_detect_all_csv_files(self, xlsx_dir):
        """Test that all CSV files are detected."""
        detector = FileChangeDetector(xlsx_dir)
        
        files = detector.get_all_csv_files()
        
        assert len(files) > 0, "Should detect CSV files in xlsx directory"
        
        # Verify all are CSV files
        for f in files:
            assert f.suffix.lower() == '.csv', f"Non-CSV file detected: {f}"
    
    def test_categorize_files(self, xlsx_dir):
        """Test file categorization by type."""
        detector = FileChangeDetector(xlsx_dir)
        
        categorized = detector.categorize_files()
        
        # Should have market data files
        assert len(categorized.get('market_data', [])) > 0, \
            "Should detect market data files"
        
        # Should have recommendations file
        assert len(categorized.get('recommendations', [])) > 0, \
            "Should detect recommendations file"


class TestSchemaValidatorIntegration:
    """Integration tests for SchemaValidator."""
    
    @pytest.fixture
    def xlsx_dir(self):
        """Get the xlsx directory path."""
        xlsx_path = Path(__file__).parent.parent.parent / "xlsx"
        if not xlsx_path.exists():
            pytest.skip("xlsx directory not found")
        return str(xlsx_path)
    
    def test_validate_market_data_files(self, xlsx_dir):
        """Test validation of market data files."""
        validator = SchemaValidator()
        xlsx_path = Path(xlsx_dir)
        
        # Find a close file
        close_files = list(xlsx_path.glob("close*.csv"))
        if not close_files:
            pytest.skip("No close files found")
        
        result = validator.validate_file(close_files[0], 'market_data')
        
        # Should be valid or have only warnings
        assert result.is_valid or len(result.warnings) > 0, \
            f"Market data file validation failed: {result.errors}"
    
    def test_validate_recommendations_file(self, xlsx_dir):
        """Test validation of recommendations file."""
        validator = SchemaValidator()
        xlsx_path = Path(xlsx_dir)
        
        rec_file = xlsx_path / "rec.csv"
        if not rec_file.exists():
            pytest.skip("rec.csv not found")
        
        result = validator.validate_file(rec_file, 'recommendations')
        
        # Should be valid or have only warnings
        assert result.is_valid or len(result.warnings) > 0, \
            f"Recommendations file validation failed: {result.errors}"
    
    def test_infer_schema_type(self, xlsx_dir):
        """Test schema type inference from filename."""
        validator = SchemaValidator()
        xlsx_path = Path(xlsx_dir)
        
        # Test market data files
        for prefix in ['close', 'buy', 'sell', 'tra', 'sha']:
            files = list(xlsx_path.glob(f"{prefix}*.csv"))
            if files:
                schema_type = validator.infer_schema_type(files[0])
                assert schema_type == 'market_data', \
                    f"Expected 'market_data' for {files[0].name}, got {schema_type}"
        
        # Test recommendations
        rec_file = xlsx_path / "rec.csv"
        if rec_file.exists():
            schema_type = validator.infer_schema_type(rec_file)
            assert schema_type == 'recommendations', \
                f"Expected 'recommendations' for rec.csv, got {schema_type}"


class TestPipelineAPIEndpoints:
    """
    Integration tests for Pipeline API endpoints.
    
    Tests pipeline trigger, status check, and history retrieval.
    _Requirements: 2.6, 2.7, 2.8_
    """
    
    @pytest.fixture
    def test_client(self):
        """Create a test client with a fresh database."""
        from fastapi.testclient import TestClient
        from backend.main import app
        from backend.database import engine
        from src.database import Base
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Create test client
        client = TestClient(app)
        
        yield client
        
        # Clean up - drop all tables
        Base.metadata.drop_all(bind=engine)
    
    @pytest.fixture
    def db_session(self):
        """Create a database session for test data setup."""
        from backend.database import SessionLocal
        session = SessionLocal()
        yield session
        session.close()
    
    @pytest.fixture
    def sample_pipeline_runs(self, db_session):
        """Create sample pipeline run data for testing."""
        import json
        
        # Create some pipeline run records
        runs = [
            PipelineRun(
                started_at=datetime(2024, 1, 15, 10, 0, 0),
                completed_at=datetime(2024, 1, 15, 10, 5, 0),
                status='success',
                files_processed=10,
                records_inserted=1000,
                records_updated=50,
                errors_count=0,
                error_details=json.dumps([])
            ),
            PipelineRun(
                started_at=datetime(2024, 1, 14, 10, 0, 0),
                completed_at=datetime(2024, 1, 14, 10, 3, 0),
                status='partial',
                files_processed=8,
                records_inserted=800,
                records_updated=20,
                errors_count=2,
                error_details=json.dumps(["Error 1", "Error 2"])
            ),
            PipelineRun(
                started_at=datetime(2024, 1, 13, 10, 0, 0),
                completed_at=datetime(2024, 1, 13, 10, 1, 0),
                status='failed',
                files_processed=0,
                records_inserted=0,
                records_updated=0,
                errors_count=1,
                error_details=json.dumps(["Critical error"])
            )
        ]
        
        for run in runs:
            db_session.add(run)
        db_session.commit()
        
        # Refresh to get IDs
        for run in runs:
            db_session.refresh(run)
        
        return runs
    
    def test_get_pipeline_history_returns_list(self, test_client, sample_pipeline_runs):
        """
        GET /pipeline/history should return a list of pipeline runs.
        
        _Requirements: 2.8_
        """
        response = test_client.get("/pipeline/history")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3  # We created 3 sample runs
    
    def test_get_pipeline_history_ordered_by_date(self, test_client, sample_pipeline_runs):
        """
        GET /pipeline/history should return runs ordered by start time (most recent first).
        
        _Requirements: 2.8_
        """
        response = test_client.get("/pipeline/history")
        assert response.status_code == 200
        data = response.json()
        
        # Verify ordering (most recent first)
        if len(data) >= 2:
            for i in range(len(data) - 1):
                assert data[i]['started_at'] >= data[i + 1]['started_at'], \
                    "Pipeline runs should be ordered by start time (descending)"
    
    def test_get_pipeline_history_with_limit(self, test_client, sample_pipeline_runs):
        """
        GET /pipeline/history should respect limit parameter.
        
        _Requirements: 2.8_
        """
        response = test_client.get("/pipeline/history?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2
    
    def test_get_pipeline_status_returns_run_details(self, test_client, sample_pipeline_runs):
        """
        GET /pipeline/status/{run_id} should return run details.
        
        _Requirements: 2.7_
        """
        run_id = sample_pipeline_runs[0].id
        response = test_client.get(f"/pipeline/status/{run_id}")
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert data['id'] == run_id
        assert data['status'] == 'success'
        assert data['files_processed'] == 10
        assert data['records_inserted'] == 1000
        assert data['records_updated'] == 50
        assert data['errors_count'] == 0
    
    def test_get_pipeline_status_not_found(self, test_client, sample_pipeline_runs):
        """
        GET /pipeline/status/{run_id} should return 404 for non-existent run.
        
        _Requirements: 2.7_
        """
        response = test_client.get("/pipeline/status/99999")
        assert response.status_code == 404
    
    def test_get_pipeline_status_with_errors(self, test_client, sample_pipeline_runs):
        """
        GET /pipeline/status/{run_id} should include error details.
        
        _Requirements: 2.7_
        """
        # Get the partial run with errors
        run_id = sample_pipeline_runs[1].id
        response = test_client.get(f"/pipeline/status/{run_id}")
        assert response.status_code == 200
        data = response.json()
        
        assert data['status'] == 'partial'
        assert data['errors_count'] == 2
        assert data['error_details'] is not None
        assert len(data['error_details']) == 2
    
    def test_get_latest_pipeline_run(self, test_client, sample_pipeline_runs):
        """
        GET /pipeline/latest should return the most recent pipeline run.
        """
        response = test_client.get("/pipeline/latest")
        assert response.status_code == 200
        data = response.json()
        
        # Should be the most recent run (2024-01-15)
        assert data is not None
        assert data['status'] == 'success'
    
    def test_get_latest_pipeline_run_empty(self, test_client):
        """
        GET /pipeline/latest should return null when no runs exist.
        """
        response = test_client.get("/pipeline/latest")
        assert response.status_code == 200
        # Response should be null/None when no runs exist
        data = response.json()
        assert data is None
    
    def test_pipeline_history_structure(self, test_client, sample_pipeline_runs):
        """
        GET /pipeline/history should return properly structured data.
        
        _Requirements: 2.8_
        """
        response = test_client.get("/pipeline/history")
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure of each run
        for run in data:
            assert 'id' in run
            assert 'started_at' in run
            assert 'completed_at' in run
            assert 'status' in run
            assert 'files_processed' in run
            assert 'records_inserted' in run
            assert 'records_updated' in run
            assert 'errors_count' in run
            assert 'error_details' in run
    
    def test_post_pipeline_run_triggers_execution(self, test_client):
        """
        POST /pipeline/run should trigger pipeline execution.
        
        _Requirements: 2.6_
        """
        response = test_client.post("/pipeline/run")
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert 'id' in data
        assert 'status' in data
        assert 'message' in data
        assert data['status'] == 'running'
        assert data['message'] == 'Pipeline execution started'
    
    def test_post_pipeline_run_with_force_full(self, test_client):
        """
        POST /pipeline/run should accept force_full parameter.
        
        _Requirements: 2.6_
        """
        response = test_client.post("/pipeline/run", json={"force_full": True})
        assert response.status_code == 200
        data = response.json()
        
        assert 'id' in data
        assert data['status'] == 'running'
    
    def test_post_pipeline_run_prevents_concurrent_execution(self, test_client, sample_pipeline_runs):
        """
        POST /pipeline/run should return 409 if pipeline is already running.
        
        _Requirements: 2.6_
        """
        # Create a running pipeline
        import json
        running_run = PipelineRun(
            started_at=datetime.now(),
            status='running',
            files_processed=0,
            records_inserted=0,
            records_updated=0,
            errors_count=0,
            error_details=json.dumps([])
        )
        
        from backend.database import SessionLocal
        session = SessionLocal()
        session.add(running_run)
        session.commit()
        session.close()
        
        # Try to start another pipeline
        response = test_client.post("/pipeline/run")
        assert response.status_code == 409
        assert 'already running' in response.json()['detail'].lower()
    
    def test_post_pipeline_run_creates_database_record(self, test_client, db_session):
        """
        POST /pipeline/run should create a pipeline run record in the database.
        
        _Requirements: 2.6, 1.8_
        """
        # Trigger pipeline
        response = test_client.post("/pipeline/run")
        assert response.status_code == 200
        run_id = response.json()['id']
        
        # Verify database record was created
        pipeline_run = db_session.query(PipelineRun).filter_by(id=run_id).first()
        assert pipeline_run is not None
        assert pipeline_run.status == 'running'
        assert pipeline_run.started_at is not None
    
    def test_pipeline_trigger_and_status_check_workflow(self, test_client):
        """
        Test complete workflow: trigger pipeline and check status.
        
        _Requirements: 2.6, 2.7_
        """
        # Step 1: Trigger pipeline
        trigger_response = test_client.post("/pipeline/run")
        assert trigger_response.status_code == 200
        run_id = trigger_response.json()['id']
        
        # Step 2: Check status
        status_response = test_client.get(f"/pipeline/status/{run_id}")
        assert status_response.status_code == 200
        status_data = status_response.json()
        
        # Verify status data
        assert status_data['id'] == run_id
        assert status_data['status'] in ['running', 'success', 'partial', 'failed']
        assert 'files_processed' in status_data
        assert 'records_inserted' in status_data
    
    def test_pipeline_trigger_and_history_workflow(self, test_client):
        """
        Test complete workflow: trigger pipeline and check history.
        
        _Requirements: 2.6, 2.8_
        """
        # Step 1: Trigger pipeline
        trigger_response = test_client.post("/pipeline/run")
        assert trigger_response.status_code == 200
        run_id = trigger_response.json()['id']
        
        # Step 2: Check history
        history_response = test_client.get("/pipeline/history")
        assert history_response.status_code == 200
        history_data = history_response.json()
        
        # Verify the triggered run appears in history
        run_ids = [run['id'] for run in history_data]
        assert run_id in run_ids
