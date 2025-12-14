"""
Logging configuration with rotation to prevent disk overflow.
"""
import logging
import logging.handlers
import os
from pathlib import Path


def setup_logging(
    log_dir: str = "logs",
    log_level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5
) -> None:
    """
    Configure logging with rotation to prevent disk overflow.
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level (default: INFO)
        max_bytes: Maximum size of each log file before rotation (default: 10MB)
        backup_count: Number of backup files to keep (default: 5)
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler for immediate feedback
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Rotating file handler for application logs
    app_log_file = log_path / "sentimentalpha.log"
    file_handler = logging.handlers.RotatingFileHandler(
        app_log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Separate rotating handler for pipeline logs
    pipeline_log_file = log_path / "pipeline.log"
    pipeline_handler = logging.handlers.RotatingFileHandler(
        pipeline_log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    pipeline_handler.setLevel(log_level)
    pipeline_handler.setFormatter(file_formatter)
    
    # Add pipeline handler to pipeline-related loggers
    pipeline_logger = logging.getLogger('src.pipeline_orchestrator')
    pipeline_logger.addHandler(pipeline_handler)
    
    data_logger = logging.getLogger('src.data_consolidator')
    data_logger.addHandler(pipeline_handler)
    
    # Separate rotating handler for error logs
    error_log_file = log_path / "errors.log"
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    root_logger.addHandler(error_handler)
    
    logging.info(f"Logging configured: {log_dir}")
    logging.info(f"Max log file size: {max_bytes / 1024 / 1024:.1f} MB")
    logging.info(f"Backup files: {backup_count}")


def cleanup_old_logs(log_dir: str = "logs", days_to_keep: int = 30) -> None:
    """
    Clean up log files older than specified days.
    
    Args:
        log_dir: Directory containing log files
        days_to_keep: Number of days to keep logs (default: 30)
    """
    import time
    from datetime import datetime, timedelta
    
    log_path = Path(log_dir)
    if not log_path.exists():
        return
    
    cutoff_time = time.time() - (days_to_keep * 86400)
    deleted_count = 0
    
    for log_file in log_path.glob("*.log*"):
        if log_file.stat().st_mtime < cutoff_time:
            try:
                log_file.unlink()
                deleted_count += 1
                logging.info(f"Deleted old log file: {log_file}")
            except Exception as e:
                logging.error(f"Failed to delete {log_file}: {e}")
    
    if deleted_count > 0:
        logging.info(f"Cleaned up {deleted_count} old log files")


def get_log_disk_usage(log_dir: str = "logs") -> dict:
    """
    Get disk usage statistics for log directory.
    
    Args:
        log_dir: Directory containing log files
        
    Returns:
        Dictionary with disk usage statistics
    """
    log_path = Path(log_dir)
    if not log_path.exists():
        return {"total_size_mb": 0, "file_count": 0}
    
    total_size = 0
    file_count = 0
    
    for log_file in log_path.glob("*.log*"):
        total_size += log_file.stat().st_size
        file_count += 1
    
    return {
        "total_size_mb": total_size / 1024 / 1024,
        "file_count": file_count,
        "directory": str(log_path.absolute())
    }


if __name__ == "__main__":
    # Test logging configuration
    setup_logging()
    
    # Test log messages
    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    
    # Show disk usage
    usage = get_log_disk_usage()
    print(f"\nLog disk usage: {usage}")
