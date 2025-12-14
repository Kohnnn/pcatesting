"""
Resource diagnostic script for identifying memory leaks and disk issues.
"""
import sys
import psutil
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from resource_monitor import ResourceMonitor, force_garbage_collection
from database import DatabaseManager


def diagnose_system_resources():
    """Diagnose system-level resource usage."""
    print("=" * 60)
    print("System Resource Diagnosis")
    print("=" * 60)
    print()
    
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    print(f"CPU Usage: {cpu_percent}% ({cpu_count} cores)")
    
    # Memory
    memory = psutil.virtual_memory()
    print(f"Memory Total: {memory.total / 1024 / 1024 / 1024:.2f} GB")
    print(f"Memory Available: {memory.available / 1024 / 1024 / 1024:.2f} GB")
    print(f"Memory Used: {memory.used / 1024 / 1024 / 1024:.2f} GB ({memory.percent}%)")
    
    # Disk
    disk = psutil.disk_usage('.')
    print(f"Disk Total: {disk.total / 1024 / 1024 / 1024:.2f} GB")
    print(f"Disk Free: {disk.free / 1024 / 1024 / 1024:.2f} GB ({100 - disk.percent:.1f}%)")
    print(f"Disk Used: {disk.used / 1024 / 1024 / 1024:.2f} GB ({disk.percent}%)")
    
    print()


def diagnose_database():
    """Diagnose database-related issues."""
    print("=" * 60)
    print("Database Diagnosis")
    print("=" * 60)
    print()
    
    db_path = Path("sentimentalpha.db")
    if db_path.exists():
        db_size = db_path.stat().st_size / 1024 / 1024
        print(f"Database file: {db_path}")
        print(f"Database size: {db_size:.2f} MB")
        
        # Check for WAL files (Write-Ahead Logging)
        wal_path = Path("sentimentalpha.db-wal")
        if wal_path.exists():
            wal_size = wal_path.stat().st_size / 1024 / 1024
            print(f"WAL file size: {wal_size:.2f} MB")
            if wal_size > 100:
                print("  WARNING: Large WAL file detected - may indicate checkpoint issues")
        
        # Check for SHM files (Shared Memory)
        shm_path = Path("sentimentalpha.db-shm")
        if shm_path.exists():
            shm_size = shm_path.stat().st_size / 1024 / 1024
            print(f"SHM file size: {shm_size:.2f} MB")
        
        # Test database connection
        try:
            db_manager = DatabaseManager()
            session = db_manager.Session()
            
            # Count records in key tables
            from database import MarketData, AnalystRecommendation, PipelineRun
            
            market_count = session.query(MarketData).count()
            rec_count = session.query(AnalystRecommendation).count()
            pipeline_count = session.query(PipelineRun).count()
            
            print(f"Market data records: {market_count:,}")
            print(f"Recommendation records: {rec_count:,}")
            print(f"Pipeline runs: {pipeline_count}")
            
            # Check for stuck pipeline runs
            stuck_runs = session.query(PipelineRun).filter(
                PipelineRun.status == 'running'
            ).count()
            if stuck_runs > 0:
                print(f"  WARNING: {stuck_runs} pipeline runs stuck in 'running' state")
            
            session.close()
            db_manager.dispose()
            
        except Exception as e:
            print(f"  ERROR: Failed to connect to database: {e}")
    else:
        print("Database file not found")
    
    print()


def diagnose_log_files():
    """Diagnose log file disk usage."""
    print("=" * 60)
    print("Log Files Diagnosis")
    print("=" * 60)
    print()
    
    log_dir = Path("logs")
    if log_dir.exists():
        total_size = 0
        file_count = 0
        large_files = []
        
        for log_file in log_dir.glob("*.log*"):
            size = log_file.stat().st_size / 1024 / 1024
            total_size += size
            file_count += 1
            
            if size > 10:  # Files larger than 10 MB
                large_files.append((log_file.name, size))
        
        print(f"Log directory: {log_dir}")
        print(f"Total log files: {file_count}")
        print(f"Total log size: {total_size:.2f} MB")
        
        if large_files:
            print("\nLarge log files (>10 MB):")
            for filename, size in sorted(large_files, key=lambda x: x[1], reverse=True):
                print(f"  {filename}: {size:.2f} MB")
        
        if total_size > 100:
            print("  WARNING: Log files consuming significant disk space")
            print("  Consider running log cleanup or reducing log retention")
    else:
        print("Log directory not found")
    
    print()


def diagnose_data_files():
    """Diagnose data file disk usage."""
    print("=" * 60)
    print("Data Files Diagnosis")
    print("=" * 60)
    print()
    
    data_dir = Path("xlsx")
    if data_dir.exists():
        total_size = 0
        file_count = 0
        
        for csv_file in data_dir.glob("*.csv"):
            size = csv_file.stat().st_size / 1024 / 1024
            total_size += size
            file_count += 1
        
        print(f"Data directory: {data_dir}")
        print(f"Total CSV files: {file_count}")
        print(f"Total data size: {total_size:.2f} MB")
    else:
        print("Data directory not found")
    
    print()


def diagnose_process_resources():
    """Diagnose current process resource usage."""
    print("=" * 60)
    print("Current Process Diagnosis")
    print("=" * 60)
    print()
    
    process = psutil.Process()
    
    # Memory
    mem_info = process.memory_info()
    print(f"Process memory (RSS): {mem_info.rss / 1024 / 1024:.2f} MB")
    print(f"Process memory (VMS): {mem_info.vms / 1024 / 1024:.2f} MB")
    print(f"Process memory %: {process.memory_percent():.2f}%")
    
    # Open files
    try:
        open_files = process.open_files()
        print(f"Open files: {len(open_files)}")
        if len(open_files) > 50:
            print("  WARNING: High number of open files")
            print("  Top 10 open files:")
            for f in open_files[:10]:
                print(f"    {f.path}")
    except (psutil.AccessDenied, AttributeError):
        print("Open files: Unable to access (permission denied)")
    
    # Connections
    try:
        connections = process.connections()
        print(f"Open connections: {len(connections)}")
        if len(connections) > 10:
            print("  WARNING: High number of open connections")
    except (psutil.AccessDenied, AttributeError):
        print("Open connections: Unable to access (permission denied)")
    
    # Threads
    num_threads = process.num_threads()
    print(f"Threads: {num_threads}")
    
    print()


def check_resource_limits():
    """Check if resources are within acceptable limits."""
    print("=" * 60)
    print("Resource Limit Checks")
    print("=" * 60)
    print()
    
    issues = []
    
    # Memory check
    memory = psutil.virtual_memory()
    if memory.percent > 85:
        issues.append(f"High memory usage: {memory.percent}%")
    
    # Disk check
    disk = psutil.disk_usage('.')
    if disk.percent > 90:
        issues.append(f"Low disk space: {100 - disk.percent:.1f}% free")
    elif disk.free < 1024 * 1024 * 1024:  # Less than 1 GB
        issues.append(f"Low disk space: {disk.free / 1024 / 1024 / 1024:.2f} GB free")
    
    # Database size check
    db_path = Path("sentimentalpha.db")
    if db_path.exists():
        db_size = db_path.stat().st_size / 1024 / 1024
        if db_size > 1000:  # Larger than 1 GB
            issues.append(f"Large database: {db_size:.2f} MB")
    
    # Log size check
    log_dir = Path("logs")
    if log_dir.exists():
        total_log_size = sum(f.stat().st_size for f in log_dir.glob("*.log*"))
        total_log_size_mb = total_log_size / 1024 / 1024
        if total_log_size_mb > 100:
            issues.append(f"Large log files: {total_log_size_mb:.2f} MB")
    
    if issues:
        print("ISSUES DETECTED:")
        for issue in issues:
            print(f"  ⚠ {issue}")
    else:
        print("✓ All resource checks passed")
    
    print()
    
    return len(issues) == 0


def main():
    """Run all diagnostic checks."""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "SentimentAlpha Resource Diagnostics" + " " * 13 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all diagnostics
    diagnose_system_resources()
    diagnose_database()
    diagnose_log_files()
    diagnose_data_files()
    diagnose_process_resources()
    
    # Check limits
    all_ok = check_resource_limits()
    
    # Recommendations
    print("=" * 60)
    print("Recommendations")
    print("=" * 60)
    print()
    
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('.')
    
    if memory.percent > 80:
        print("• Consider closing other applications to free memory")
        print("• Run garbage collection: python -c 'import gc; gc.collect()'")
    
    if disk.percent > 85:
        print("• Clean up old log files: python logging_config.py")
        print("• Archive or delete old data files")
        print("• Consider database vacuum: sqlite3 sentimentalpha.db 'VACUUM;'")
    
    db_path = Path("sentimentalpha.db")
    if db_path.exists():
        db_size = db_path.stat().st_size / 1024 / 1024
        if db_size > 500:
            print("• Consider archiving old data from database")
            print("• Run VACUUM to reclaim space: sqlite3 sentimentalpha.db 'VACUUM;'")
    
    if not all_ok:
        print("\n⚠ Action required to prevent resource issues")
        return 1
    else:
        print("✓ System resources are healthy")
        return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
