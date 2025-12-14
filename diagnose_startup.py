"""
Diagnostic script to identify startup and memory issues.
"""
import sys
import os
import sqlite3
from pathlib import Path

def check_python_version():
    """Check Python version."""
    print("=" * 60)
    print("Python Version Check")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    if sys.version_info < (3, 8):
        print("❌ ERROR: Python 3.8+ required")
        return False
    print("✓ Python version OK")
    return True

def check_dependencies():
    """Check if required Python packages are installed."""
    print("\n" + "=" * 60)
    print("Python Dependencies Check")
    print("=" * 60)
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pandas',
        'numpy',
        'sklearn',
        'scipy',
        'psutil'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} - NOT FOUND")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✓ All dependencies installed")
    return True

def check_database():
    """Check database file and size."""
    print("\n" + "=" * 60)
    print("Database Check")
    print("=" * 60)
    
    db_path = Path("sentimentalpha.db")
    
    if not db_path.exists():
        print("❌ Database file not found: sentimentalpha.db")
        print("Run: python seed_data.py")
        return False
    
    # Check size
    size_mb = db_path.stat().st_size / 1024 / 1024
    print(f"✓ Database found: {size_mb:.2f} MB")
    
    if size_mb > 1000:
        print(f"⚠️  WARNING: Large database ({size_mb:.2f} MB) may cause memory issues")
    
    # Check tables
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\nTables found: {len(tables)}")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"  - {table[0]}: {count:,} rows")
        
        conn.close()
        print("\n✓ Database structure OK")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_disk_space():
    """Check available disk space."""
    print("\n" + "=" * 60)
    print("Disk Space Check")
    print("=" * 60)
    
    try:
        import psutil
        disk = psutil.disk_usage('.')
        
        free_gb = disk.free / 1024 / 1024 / 1024
        total_gb = disk.total / 1024 / 1024 / 1024
        percent = disk.percent
        
        print(f"Total: {total_gb:.2f} GB")
        print(f"Used: {percent:.1f}%")
        print(f"Free: {free_gb:.2f} GB")
        
        if free_gb < 1.0:
            print(f"❌ ERROR: Low disk space ({free_gb:.2f} GB free)")
            print("   Need at least 1 GB free for safe operation")
            return False
        elif free_gb < 5.0:
            print(f"⚠️  WARNING: Low disk space ({free_gb:.2f} GB free)")
        
        print("✓ Disk space OK")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not check disk space: {e}")
        return True

def check_memory():
    """Check available memory."""
    print("\n" + "=" * 60)
    print("Memory Check")
    print("=" * 60)
    
    try:
        import psutil
        mem = psutil.virtual_memory()
        
        total_gb = mem.total / 1024 / 1024 / 1024
        available_gb = mem.available / 1024 / 1024 / 1024
        percent = mem.percent
        
        print(f"Total: {total_gb:.2f} GB")
        print(f"Used: {percent:.1f}%")
        print(f"Available: {available_gb:.2f} GB")
        
        if available_gb < 0.5:
            print(f"❌ ERROR: Low memory ({available_gb:.2f} GB available)")
            return False
        elif available_gb < 2.0:
            print(f"⚠️  WARNING: Low memory ({available_gb:.2f} GB available)")
        
        print("✓ Memory OK")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not check memory: {e}")
        return True

def check_data_directory():
    """Check data directory structure."""
    print("\n" + "=" * 60)
    print("Data Directory Check")
    print("=" * 60)
    
    data_dir = Path("xlsx")
    
    if not data_dir.exists():
        print("❌ Data directory not found: xlsx/")
        return False
    
    csv_files = list(data_dir.glob("*.csv"))
    print(f"✓ Data directory found: {len(csv_files)} CSV files")
    
    # Check for required files
    required_patterns = ['close', 'buy', 'sell', 'tra', 'sha', 'rec', 'vnindex', 'rfr']
    found_patterns = set()
    
    for csv_file in csv_files:
        name = csv_file.stem.lower()
        for pattern in required_patterns:
            if pattern in name:
                found_patterns.add(pattern)
    
    missing = set(required_patterns) - found_patterns
    if missing:
        print(f"⚠️  WARNING: Missing data files: {', '.join(missing)}")
    else:
        print("✓ All required data files present")
    
    return True

def check_frontend():
    """Check frontend setup."""
    print("\n" + "=" * 60)
    print("Frontend Check")
    print("=" * 60)
    
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ package.json not found")
        return False
    
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("❌ node_modules not found")
        print("Run: cd frontend && npm install")
        return False
    
    print("✓ Frontend structure OK")
    return True

def check_backend_imports():
    """Check if backend can be imported."""
    print("\n" + "=" * 60)
    print("Backend Import Check")
    print("=" * 60)
    
    try:
        import backend.main
        print("✓ Backend imports successfully")
        return True
    except Exception as e:
        print(f"❌ Backend import error: {e}")
        return False

def main():
    """Run all diagnostic checks."""
    print("\n" + "=" * 60)
    print("SentimentAlpha Vietnam - Startup Diagnostics")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Database", check_database),
        ("Disk Space", check_disk_space),
        ("Memory", check_memory),
        ("Data Directory", check_data_directory),
        ("Frontend", check_frontend),
        ("Backend Imports", check_backend_imports),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ {name} check failed with error: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ All checks passed! You can start the application.")
        print("\nTo start:")
        print("  Option 1: Run dev.bat and select option [2]")
        print("  Option 2: Run run_production.bat")
    else:
        print("\n❌ Some checks failed. Please fix the issues above before starting.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
