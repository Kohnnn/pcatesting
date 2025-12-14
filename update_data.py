"""
Incremental data update script for SentimentAlpha Vietnam.

Uses the new PipelineOrchestrator for automated data pipeline execution.
Supports command-line options for force-full updates.
"""
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from database import DatabaseManager
from pipeline_orchestrator import PipelineOrchestrator

# Import logging configuration
sys.path.insert(0, str(Path(__file__).parent))
from logging_config import setup_logging, cleanup_old_logs


def main():
    """Main incremental update function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Update SentimentAlpha Vietnam data incrementally"
    )
    parser.add_argument(
        "--force-full",
        action="store_true",
        help="Force full update of all data (ignore last run timestamp)"
    )
    parser.add_argument(
        "--data-dir",
        default="xlsx",
        help="Directory containing CSV data files (default: xlsx)"
    )
    parser.add_argument(
        "--db-path",
        default="sentimentalpha.db",
        help="Path to SQLite database (default: sentimentalpha.db)"
    )
    
    args = parser.parse_args()
    
    # Setup logging with rotation
    setup_logging(log_dir="logs", log_level=20)  # INFO level
    
    # Cleanup old logs (keep last 30 days)
    cleanup_old_logs(log_dir="logs", days_to_keep=30)
    
    print("=" * 60)
    print("SentimentAlpha Vietnam - Data Pipeline")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'FULL UPDATE' if args.force_full else 'INCREMENTAL UPDATE'}")
    print(f"Data directory: {args.data_dir}")
    print(f"Database: {args.db_path}")
    print("=" * 60)
    print()
    
    db_manager = None
    orchestrator = None
    
    try:
        # Initialize database manager and pipeline orchestrator
        db_manager = DatabaseManager(args.db_path)
        orchestrator = PipelineOrchestrator(
            db_manager=db_manager,
            data_dir=args.data_dir
        )
        
        # Run the pipeline
        print("Starting data pipeline...")
        print()
        report = orchestrator.run_pipeline(force_full=args.force_full)
        
        # Display results
        print()
        print("=" * 60)
        print("Pipeline Execution Summary")
        print("=" * 60)
        print(f"Status: {report.status.upper()}")
        print(f"Files processed: {report.files_processed}")
        print(f"Records inserted: {report.records_inserted}")
        print(f"Records updated: {report.records_updated}")
        print(f"Errors: {report.errors_count}")
        
        if report.errors_count > 0 and report.error_details:
            print()
            print("Error Details:")
            for error in report.error_details[:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(report.error_details) > 10:
                print(f"  ... and {len(report.error_details) - 10} more errors")
        
        print()
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Exit with appropriate code
        exit_code = 0
        if report.status == 'success':
            exit_code = 0
        elif report.status == 'partial':
            print("\nWarning: Pipeline completed with some errors")
            exit_code = 1
        else:
            print("\nError: Pipeline failed")
            exit_code = 2
        
        return exit_code
            
    except Exception as e:
        print()
        print("=" * 60)
        print("FATAL ERROR")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        print()
        print(f"Failed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        return 3
    
    finally:
        # Cleanup resources
        if orchestrator is not None:
            orchestrator.cleanup()
        if db_manager is not None:
            db_manager.dispose()


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
