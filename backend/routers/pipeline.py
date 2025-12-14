"""
Pipeline router for triggering and monitoring data pipeline execution.
Implements Requirements 2.6, 2.7, 2.8
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
import json

from backend.database import get_db

# Import PipelineRun model and PipelineOrchestrator
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.database import PipelineRun, DatabaseManager
from src.pipeline_orchestrator import PipelineOrchestrator

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


# Pydantic schemas for pipeline API
class PipelineRunResponse(BaseModel):
    """Schema for pipeline run response."""
    id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str
    files_processed: int
    records_inserted: int
    records_updated: int
    errors_count: int
    error_details: Optional[List[str]] = None

    class Config:
        from_attributes = True


class PipelineTriggerRequest(BaseModel):
    """Schema for pipeline trigger request."""
    force_full: bool = False


class PipelineTriggerResponse(BaseModel):
    """Schema for pipeline trigger response."""
    id: int
    status: str
    message: str


# Global variable to track if pipeline is running
_pipeline_running = False


def _run_pipeline_task(force_full: bool = False):
    """
    Background task to run the pipeline.
    
    Args:
        force_full: If True, process all files regardless of modification time
    """
    global _pipeline_running
    db_manager = None
    try:
        # Use context manager to ensure proper cleanup
        db_manager = DatabaseManager()
        orchestrator = PipelineOrchestrator(db_manager=db_manager, data_dir="xlsx")
        orchestrator.run_pipeline(force_full=force_full)
    finally:
        _pipeline_running = False
        # Explicitly dispose of database connections to prevent leaks
        if db_manager is not None:
            db_manager.dispose()
        # Force garbage collection to release memory
        import gc
        gc.collect()


@router.post("/run", response_model=PipelineTriggerResponse)
async def run_pipeline(
    background_tasks: BackgroundTasks,
    request: PipelineTriggerRequest = PipelineTriggerRequest(),
    db: Session = Depends(get_db)
) -> PipelineTriggerResponse:
    """
    Trigger pipeline execution.
    
    Implements Requirement 2.6: When the user clicks "Run Pipeline", 
    the UI SHALL trigger the data pipeline and display progress status.
    
    Args:
        background_tasks: FastAPI background tasks
        request: Pipeline trigger request with optional force_full flag
        db: Database session
        
    Returns:
        Pipeline trigger response with run ID and status.
        
    Raises:
        HTTPException: 409 if pipeline is already running
    """
    global _pipeline_running
    
    # Check if pipeline is already running
    if _pipeline_running:
        raise HTTPException(
            status_code=409,
            detail="Pipeline is already running"
        )
    
    # Also check database for running pipelines
    running_pipeline = db.query(PipelineRun).filter(
        PipelineRun.status == 'running'
    ).first()
    
    if running_pipeline:
        raise HTTPException(
            status_code=409,
            detail="Pipeline is already running"
        )
    
    # Create initial pipeline run record
    pipeline_run = PipelineRun(
        started_at=datetime.now(),
        status='running',
        files_processed=0,
        records_inserted=0,
        records_updated=0,
        errors_count=0
    )
    db.add(pipeline_run)
    db.commit()
    db.refresh(pipeline_run)
    
    run_id = pipeline_run.id
    
    # Mark pipeline as running
    _pipeline_running = True
    
    # Start pipeline in background
    background_tasks.add_task(_run_pipeline_task, request.force_full)
    
    return PipelineTriggerResponse(
        id=run_id,
        status='running',
        message='Pipeline execution started'
    )


@router.get("/status/{run_id}", response_model=PipelineRunResponse)
def get_pipeline_status(
    run_id: int,
    db: Session = Depends(get_db)
) -> PipelineRunResponse:
    """
    Get status of a specific pipeline run.
    
    Implements Requirement 2.7: When pipeline execution completes, 
    the UI SHALL display the summary report with success/error counts.
    
    Args:
        run_id: ID of the pipeline run
        db: Database session
        
    Returns:
        Pipeline run status and statistics.
        
    Raises:
        HTTPException: 404 if run not found
    """
    pipeline_run = db.query(PipelineRun).filter(PipelineRun.id == run_id).first()
    
    if not pipeline_run:
        raise HTTPException(
            status_code=404,
            detail=f"Pipeline run {run_id} not found"
        )
    
    # Parse error_details from JSON
    error_details = None
    if pipeline_run.error_details:
        try:
            error_details = json.loads(pipeline_run.error_details)
        except json.JSONDecodeError:
            error_details = [pipeline_run.error_details]
    
    return PipelineRunResponse(
        id=pipeline_run.id,
        started_at=pipeline_run.started_at,
        completed_at=pipeline_run.completed_at,
        status=pipeline_run.status,
        files_processed=pipeline_run.files_processed or 0,
        records_inserted=pipeline_run.records_inserted or 0,
        records_updated=pipeline_run.records_updated or 0,
        errors_count=pipeline_run.errors_count or 0,
        error_details=error_details
    )


@router.get("/history", response_model=List[PipelineRunResponse])
def get_pipeline_history(
    limit: int = 20,
    db: Session = Depends(get_db)
) -> List[PipelineRunResponse]:
    """
    Get history of pipeline runs.
    
    Implements Requirement 2.8: When viewing pipeline history, 
    the UI SHALL display a list of past pipeline runs with timestamps and statistics.
    
    Args:
        limit: Maximum number of runs to return (default: 20)
        db: Database session
        
    Returns:
        List of pipeline runs ordered by start time (most recent first).
    """
    pipeline_runs = db.query(PipelineRun).order_by(
        desc(PipelineRun.started_at)
    ).limit(limit).all()
    
    results = []
    for run in pipeline_runs:
        # Parse error_details from JSON
        error_details = None
        if run.error_details:
            try:
                error_details = json.loads(run.error_details)
            except json.JSONDecodeError:
                error_details = [run.error_details]
        
        results.append(PipelineRunResponse(
            id=run.id,
            started_at=run.started_at,
            completed_at=run.completed_at,
            status=run.status,
            files_processed=run.files_processed or 0,
            records_inserted=run.records_inserted or 0,
            records_updated=run.records_updated or 0,
            errors_count=run.errors_count or 0,
            error_details=error_details
        ))
    
    return results


@router.get("/latest", response_model=Optional[PipelineRunResponse])
def get_latest_pipeline_run(
    db: Session = Depends(get_db)
) -> Optional[PipelineRunResponse]:
    """
    Get the most recent pipeline run.
    
    Args:
        db: Database session
        
    Returns:
        Most recent pipeline run or None if no runs exist.
    """
    pipeline_run = db.query(PipelineRun).order_by(
        desc(PipelineRun.started_at)
    ).first()
    
    if not pipeline_run:
        return None
    
    # Parse error_details from JSON
    error_details = None
    if pipeline_run.error_details:
        try:
            error_details = json.loads(pipeline_run.error_details)
        except json.JSONDecodeError:
            error_details = [pipeline_run.error_details]
    
    return PipelineRunResponse(
        id=pipeline_run.id,
        started_at=pipeline_run.started_at,
        completed_at=pipeline_run.completed_at,
        status=pipeline_run.status,
        files_processed=pipeline_run.files_processed or 0,
        records_inserted=pipeline_run.records_inserted or 0,
        records_updated=pipeline_run.records_updated or 0,
        errors_count=pipeline_run.errors_count or 0,
        error_details=error_details
    )
