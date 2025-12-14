"""
Resource monitoring utilities for tracking memory and disk usage.
"""
import psutil
import logging
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class ResourceMonitor:
    """Monitor system resources during pipeline execution."""
    
    def __init__(self, log_interval: int = 10):
        """
        Initialize ResourceMonitor.
        
        Args:
            log_interval: Log resource usage every N operations (default: 10)
        """
        self.process = psutil.Process()
        self.log_interval = log_interval
        self.operation_count = 0
        self.baseline_memory = None
        self.peak_memory = 0
        self.start_time = None
    
    def start_monitoring(self) -> None:
        """Start monitoring session."""
        self.baseline_memory = self.get_memory_usage()
        self.peak_memory = self.baseline_memory
        self.start_time = datetime.now()
        self.operation_count = 0
        logger.info(f"Resource monitoring started - Baseline memory: {self.baseline_memory:.2f} MB")
    
    def get_memory_usage(self) -> float:
        """
        Get current memory usage in MB.
        
        Returns:
            Memory usage in megabytes
        """
        mem_info = self.process.memory_info()
        return mem_info.rss / 1024 / 1024
    
    def get_memory_percent(self) -> float:
        """
        Get memory usage as percentage of total system memory.
        
        Returns:
            Memory usage percentage
        """
        return self.process.memory_percent()
    
    def get_open_files_count(self) -> int:
        """
        Get count of open file descriptors.
        
        Returns:
            Number of open files
        """
        try:
            return len(self.process.open_files())
        except (psutil.AccessDenied, AttributeError):
            return 0
    
    def get_connections_count(self) -> int:
        """
        Get count of open network connections.
        
        Returns:
            Number of open connections
        """
        try:
            return len(self.process.connections())
        except (psutil.AccessDenied, AttributeError):
            return 0
    
    def get_disk_usage(self, path: str = ".") -> Dict[str, float]:
        """
        Get disk usage statistics.
        
        Args:
            path: Path to check disk usage (default: current directory)
            
        Returns:
            Dictionary with disk usage statistics
        """
        disk = psutil.disk_usage(path)
        return {
            "total_gb": disk.total / 1024 / 1024 / 1024,
            "used_gb": disk.used / 1024 / 1024 / 1024,
            "free_gb": disk.free / 1024 / 1024 / 1024,
            "percent": disk.percent
        }
    
    def get_database_size(self, db_path: str = "sentimentalpha.db") -> float:
        """
        Get database file size in MB.
        
        Args:
            db_path: Path to database file
            
        Returns:
            Database size in megabytes
        """
        try:
            db_file = Path(db_path)
            if db_file.exists():
                return db_file.stat().st_size / 1024 / 1024
        except Exception as e:
            logger.error(f"Failed to get database size: {e}")
        return 0.0
    
    def log_resource_usage(self, stage: str, force: bool = False) -> Dict[str, any]:
        """
        Log current resource usage.
        
        Args:
            stage: Description of current stage
            force: Force logging regardless of interval
            
        Returns:
            Dictionary with resource statistics
        """
        self.operation_count += 1
        
        # Only log at intervals unless forced
        if not force and self.operation_count % self.log_interval != 0:
            return {}
        
        current_memory = self.get_memory_usage()
        memory_percent = self.get_memory_percent()
        open_files = self.get_open_files_count()
        connections = self.get_connections_count()
        
        # Track peak memory
        if current_memory > self.peak_memory:
            self.peak_memory = current_memory
        
        # Calculate memory delta from baseline
        memory_delta = current_memory - self.baseline_memory if self.baseline_memory else 0
        
        stats = {
            "stage": stage,
            "memory_mb": current_memory,
            "memory_percent": memory_percent,
            "memory_delta_mb": memory_delta,
            "peak_memory_mb": self.peak_memory,
            "open_files": open_files,
            "connections": connections,
            "operation_count": self.operation_count
        }
        
        logger.info(
            f"[{stage}] Memory: {current_memory:.2f} MB ({memory_percent:.1f}%), "
            f"Delta: {memory_delta:+.2f} MB, Peak: {self.peak_memory:.2f} MB, "
            f"Files: {open_files}, Connections: {connections}"
        )
        
        # Warn if memory usage is high
        if memory_percent > 80:
            logger.warning(f"High memory usage detected: {memory_percent:.1f}%")
        
        # Warn if too many files are open
        if open_files > 100:
            logger.warning(f"High number of open files: {open_files}")
        
        return stats
    
    def get_summary(self) -> Dict[str, any]:
        """
        Get monitoring session summary.
        
        Returns:
            Dictionary with summary statistics
        """
        if self.start_time is None:
            return {}
        
        duration = (datetime.now() - self.start_time).total_seconds()
        current_memory = self.get_memory_usage()
        memory_delta = current_memory - self.baseline_memory if self.baseline_memory else 0
        
        disk_usage = self.get_disk_usage()
        db_size = self.get_database_size()
        
        summary = {
            "duration_seconds": duration,
            "baseline_memory_mb": self.baseline_memory,
            "final_memory_mb": current_memory,
            "peak_memory_mb": self.peak_memory,
            "memory_delta_mb": memory_delta,
            "operations_count": self.operation_count,
            "disk_usage_percent": disk_usage["percent"],
            "disk_free_gb": disk_usage["free_gb"],
            "database_size_mb": db_size
        }
        
        logger.info("=" * 60)
        logger.info("Resource Monitoring Summary")
        logger.info("=" * 60)
        logger.info(f"Duration: {duration:.1f} seconds")
        logger.info(f"Baseline memory: {self.baseline_memory:.2f} MB")
        logger.info(f"Final memory: {current_memory:.2f} MB")
        logger.info(f"Peak memory: {self.peak_memory:.2f} MB")
        logger.info(f"Memory delta: {memory_delta:+.2f} MB")
        logger.info(f"Operations: {self.operation_count}")
        logger.info(f"Disk usage: {disk_usage['percent']:.1f}% ({disk_usage['free_gb']:.2f} GB free)")
        logger.info(f"Database size: {db_size:.2f} MB")
        logger.info("=" * 60)
        
        return summary
    
    def check_resource_limits(
        self,
        max_memory_percent: float = 85.0,
        min_disk_free_gb: float = 1.0
    ) -> Dict[str, bool]:
        """
        Check if resource usage is within acceptable limits.
        
        Args:
            max_memory_percent: Maximum allowed memory usage percentage
            min_disk_free_gb: Minimum required free disk space in GB
            
        Returns:
            Dictionary with limit check results
        """
        memory_percent = self.get_memory_percent()
        disk_usage = self.get_disk_usage()
        
        checks = {
            "memory_ok": memory_percent < max_memory_percent,
            "disk_ok": disk_usage["free_gb"] > min_disk_free_gb,
            "memory_percent": memory_percent,
            "disk_free_gb": disk_usage["free_gb"]
        }
        
        if not checks["memory_ok"]:
            logger.error(
                f"Memory limit exceeded: {memory_percent:.1f}% > {max_memory_percent}%"
            )
        
        if not checks["disk_ok"]:
            logger.error(
                f"Disk space low: {disk_usage['free_gb']:.2f} GB < {min_disk_free_gb} GB"
            )
        
        return checks


def force_garbage_collection() -> Dict[str, int]:
    """
    Force garbage collection and return statistics.
    
    Returns:
        Dictionary with garbage collection statistics
    """
    import gc
    
    # Get counts before collection
    before = sum(gc.get_count())
    
    # Force collection of all generations
    collected = gc.collect()
    
    # Get counts after collection
    after = sum(gc.get_count())
    
    stats = {
        "objects_before": before,
        "objects_after": after,
        "objects_collected": collected
    }
    
    logger.debug(f"Garbage collection: {collected} objects collected")
    
    return stats


if __name__ == "__main__":
    # Test resource monitoring
    import time
    
    logging.basicConfig(level=logging.INFO)
    
    monitor = ResourceMonitor(log_interval=1)
    monitor.start_monitoring()
    
    # Simulate some operations
    for i in range(5):
        # Allocate some memory
        data = [0] * 1000000
        monitor.log_resource_usage(f"Operation {i+1}")
        time.sleep(0.5)
        del data
    
    # Force garbage collection
    force_garbage_collection()
    
    # Get summary
    summary = monitor.get_summary()
    
    # Check limits
    limits = monitor.check_resource_limits()
    print(f"\nResource limits OK: {all(limits.values())}")
