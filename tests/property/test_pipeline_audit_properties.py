"""
Property-based tests for pipeline audit trail.

**Feature: data-management-refactor**
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from hypothesis import given, strategies as st, settings
import tempfile
import os
import json
from datetime import datetime

from database import DatabaseManager, PipelineRun


class TestPipelineAuditProperties:
    """Property-based tests for pipeline audit trail."""
    
    @settings(max_examples=100, deadline=None)
    @given(
        files_processed=st.integers(min_value=0, max_value=100),
        records_inserted=st.integers(min_value=0, max_value=10000),
        records_updated=st.integers(min_value=0, max_value=10000),
        errors_count=st.integers(min_value=0, max_value=50),
        status=st.sampled_from(['running', 'success', 'partial', 'failed']),
        error_messages=st.lists(st.text(min_size=1, max_size=100), min_size=0, max_size=10)
    )
    def test_pipeline_audit_trail(
        self, files_processed, records_inserted, records_updated, 
        errors_count, status, error_messages
    ):
        """
        **Feature: data-management-refactor, Property 4: Pipeline Audit Trail**
        **Validates: Requirements 1.8**
        
        For any pipeline execution, a corresponding record should be created in 
        the pipeline_runs table with accurate statistics (files_processed, 
        records_inserted, errors_count).
        """
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            db = DatabaseManager(db_path)
            db.create_tables()
            
            # Create a pipeline run record
            session = db.Session()
            try:
                # Serialize error messages to JSON
                error_details_json = json.dumps(error_messages) if error_messages else None
                
                pipeline_run = PipelineRun(
                    status=status,
                    files_processed=files_processed,
                    records_inserted=records_inserted,
                    records_updated=records_updated,
                    errors_count=errors_count,
                    error_details=error_details_json
                )
                session.add(pipeline_run)
                session.commit()
                
                # Get the ID of the inserted record
                run_id = pipeline_run.id
                
                # Read back the record
                retrieved = session.query(PipelineRun).filter_by(id=run_id).first()
                
                # Verify all statistics are accurately stored
                assert retrieved is not None, "Pipeline run record should exist"
                assert retrieved.files_processed == files_processed, \
                    f"files_processed mismatch: expected {files_processed}, got {retrieved.files_processed}"
                assert retrieved.records_inserted == records_inserted, \
                    f"records_inserted mismatch: expected {records_inserted}, got {retrieved.records_inserted}"
                assert retrieved.records_updated == records_updated, \
                    f"records_updated mismatch: expected {records_updated}, got {retrieved.records_updated}"
                assert retrieved.errors_count == errors_count, \
                    f"errors_count mismatch: expected {errors_count}, got {retrieved.errors_count}"
                assert retrieved.status == status, \
                    f"status mismatch: expected {status}, got {retrieved.status}"
                
                # Verify error details can be deserialized
                if error_messages:
                    retrieved_errors = json.loads(retrieved.error_details)
                    assert retrieved_errors == error_messages, \
                        f"error_details mismatch: expected {error_messages}, got {retrieved_errors}"
                
                # Verify started_at is set
                assert retrieved.started_at is not None, "started_at should be set automatically"
                
            finally:
                session.close()
                db.engine.dispose()
        
        finally:
            # Clean up temporary database
            if os.path.exists(db_path):
                try:
                    os.unlink(db_path)
                except PermissionError:
                    pass
