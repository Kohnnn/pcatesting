"""
Production Health Check Script
Comprehensive system health monitoring for production readiness
"""
import sys
import os
import psutil
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


class HealthCheck:
    """Production health check system."""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.passed = []
        
    def add_issue(self, severity: str, category: str, message: str):
        """Add an issue to the report."""
        self.issues.append({
            'severity': severity,
            'category': category,
            'message': message,
            'timestamp': datetime.now()
        })
    
    def add_warning(self, category: str, message: str):
        """Add a warning to the report."""
        self.warnings.append({
            'category': category,
            'message': message,
            'timestamp': datetime.now()
        })
    
    def add_passed(self, category: str, message: str):
        """Add a passed check to the report."""
        self.passed.append({
            'category': category,
            'message': message
        })
    
    def check_disk_space(self) -> bool:
        """Check disk space availability."""
        disk = psutil.disk_usage('.')
        percent_used = disk.percent
        free_gb = disk.free / (1024 ** 3)
        
        if percent_used > 90:
            self.add_issue('CRITICAL', 'Disk Space', 
                          f'Disk usage at {percent_used:.1f}% (only {free_gb:.2f} GB free)')
            return False
        elif percent_used > 80:
            self.add_warning('Disk Space', 
                           f'Disk usage at {percent_used:.1f}% (warning threshold)')
            return True
        else:
            self.add_passed('Disk Space', 
                          f'Disk usage at {percent_used:.1f}% ({free_gb:.2f} GB free)')
            return True
    
    def check_memory(self) -> bool:
        """Check memory usage."""
        memory = psutil.virtual_memory()
        percent_used = memory.percent
        
        if percent_used > 90:
            self.add_issue('CRITICAL', 'Memory', 
                          f'Memory usage at {percent_used:.1f}%')
            return False
        elif percent_used > 80:
            self.add_warning('Memory', 
                           f'Memory usage at {percent_used:.1f}%')
            return True
        else:
            self.add_passed('Memory', 
                          f'Memory usage at {percent_used:.1f}%')
            return True
    
    def check_database(self) -> bool:
        """Check database health."""
        db_path = Path('sentimentalpha.db')
        
        if not db_path.exists():
            self.add_issue('CRITICAL', 'Database', 'Database file not found')
            return False
        
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Check integrity
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            if result[0] != 'ok':
                self.add_issue('CRITICAL', 'Database', 
                              f'Integrity check failed: {result[0]}')
                return False
            
            # Check for stuck pipeline runs
            cursor.execute("""
                SELECT COUNT(*) FROM pipeline_runs 
                WHERE status='running'
            """)
            stuck_count = cursor.fetchone()[0]
            
            if stuck_count > 0:
                self.add_issue('HIGH', 'Database', 
                              f'{stuck_count} pipeline runs stuck in running state')
                return False
            
            # Check data freshness
            cursor.execute("""
                SELECT MAX(date) FROM market_data
            """)
            latest_date = cursor.fetchone()[0]
            
            if latest_date:
                latest = datetime.strptime(latest_date, '%Y-%m-%d')
                days_old = (datetime.now() - latest).days
                
                if days_old > 7:
                    self.add_warning('Database', 
                                   f'Market data is {days_old} days old')
                else:
                    self.add_passed('Database', 
                                  f'Market data is up to date ({days_old} days old)')
            
            # Check database size
            db_size_mb = db_path.stat().st_size / (1024 ** 2)
            if db_size_mb > 1000:
                self.add_warning('Database', 
                               f'Database size is {db_size_mb:.2f} MB')
            else:
                self.add_passed('Database', 
                              f'Database size is {db_size_mb:.2f} MB')
            
            conn.close()
            self.add_passed('Database', 'Integrity check passed')
            return True
            
        except Exception as e:
            self.add_issue('CRITICAL', 'Database', 
                          f'Database check failed: {str(e)}')
            return False
    
    def check_log_files(self) -> bool:
        """Check log file status."""
        log_dir = Path('logs')
        
        if not log_dir.exists():
            self.add_warning('Logging', 'Log directory not found')
            return True
        
        total_size = 0
        file_count = 0
        
        for log_file in log_dir.glob('*.log*'):
            size = log_file.stat().st_size
            total_size += size
            file_count += 1
        
        total_size_mb = total_size / (1024 ** 2)
        
        if total_size_mb > 500:
            self.add_warning('Logging', 
                           f'Log files consuming {total_size_mb:.2f} MB')
        else:
            self.add_passed('Logging', 
                          f'Log files: {file_count} files, {total_size_mb:.2f} MB')
        
        return True
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed."""
        required = [
            'fastapi',
            'uvicorn',
            'sqlalchemy',
            'pandas',
            'psutil',
        ]
        
        missing = []
        for package in required:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            self.add_issue('HIGH', 'Dependencies', 
                          f'Missing packages: {", ".join(missing)}')
            return False
        else:
            self.add_passed('Dependencies', 'All required packages installed')
            return True
    
    def check_configuration(self) -> bool:
        """Check configuration files."""
        issues_found = False
        
        # Check .env file
        if not Path('.env').exists():
            self.add_warning('Configuration', '.env file not found')
        else:
            self.add_passed('Configuration', '.env file exists')
        
        # Check frontend config
        if not Path('frontend/package.json').exists():
            self.add_issue('HIGH', 'Configuration', 
                          'Frontend package.json not found')
            issues_found = True
        else:
            self.add_passed('Configuration', 'Frontend configured')
        
        # Check backend config
        if not Path('backend/main.py').exists():
            self.add_issue('CRITICAL', 'Configuration', 
                          'Backend main.py not found')
            issues_found = True
        else:
            self.add_passed('Configuration', 'Backend configured')
        
        return not issues_found
    
    def check_security(self) -> bool:
        """Check security configuration."""
        issues_found = False
        
        # Check for authentication
        try:
            with open('backend/main.py', 'r') as f:
                content = f.read()
                if 'auth' not in content.lower() and 'jwt' not in content.lower():
                    self.add_issue('CRITICAL', 'Security', 
                                  'No authentication system detected')
                    issues_found = True
        except:
            pass
        
        # Check for rate limiting
        try:
            with open('backend/main.py', 'r') as f:
                content = f.read()
                if 'limiter' not in content.lower():
                    self.add_issue('HIGH', 'Security', 
                                  'No rate limiting detected')
                    issues_found = True
        except:
            pass
        
        # Check for HTTPS configuration
        try:
            with open('backend/main.py', 'r') as f:
                content = f.read()
                if 'ssl' not in content.lower() and 'https' not in content.lower():
                    self.add_warning('Security', 
                                   'No HTTPS configuration detected')
        except:
            pass
        
        return not issues_found
    
    def run_all_checks(self) -> Dict:
        """Run all health checks."""
        print("Running production health checks...")
        print()
        
        checks = [
            ('Disk Space', self.check_disk_space),
            ('Memory', self.check_memory),
            ('Database', self.check_database),
            ('Log Files', self.check_log_files),
            ('Dependencies', self.check_dependencies),
            ('Configuration', self.check_configuration),
            ('Security', self.check_security),
        ]
        
        results = {}
        for name, check_func in checks:
            print(f"Checking {name}...", end=' ')
            try:
                result = check_func()
                results[name] = result
                print("✓" if result else "✗")
            except Exception as e:
                print(f"ERROR: {str(e)}")
                results[name] = False
                self.add_issue('CRITICAL', name, f'Check failed: {str(e)}')
        
        return results
    
    def generate_report(self) -> str:
        """Generate health check report."""
        report = []
        report.append("=" * 60)
        report.append("PRODUCTION HEALTH CHECK REPORT")
        report.append("=" * 60)
        report.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        critical_count = len([i for i in self.issues if i['severity'] == 'CRITICAL'])
        high_count = len([i for i in self.issues if i['severity'] == 'HIGH'])
        warning_count = len(self.warnings)
        passed_count = len(self.passed)
        
        report.append("SUMMARY")
        report.append("-" * 60)
        report.append(f"✓ Passed: {passed_count}")
        report.append(f"⚠ Warnings: {warning_count}")
        report.append(f"🔴 High Priority Issues: {high_count}")
        report.append(f"🔴 Critical Issues: {critical_count}")
        report.append("")
        
        # Overall status
        if critical_count > 0:
            report.append("STATUS: 🔴 NOT READY FOR PRODUCTION")
        elif high_count > 0:
            report.append("STATUS: ⚠️ NEEDS ATTENTION")
        elif warning_count > 0:
            report.append("STATUS: ⚠️ READY WITH WARNINGS")
        else:
            report.append("STATUS: ✅ PRODUCTION READY")
        report.append("")
        
        # Critical issues
        if critical_count > 0:
            report.append("CRITICAL ISSUES (MUST FIX)")
            report.append("-" * 60)
            for issue in [i for i in self.issues if i['severity'] == 'CRITICAL']:
                report.append(f"🔴 [{issue['category']}] {issue['message']}")
            report.append("")
        
        # High priority issues
        if high_count > 0:
            report.append("HIGH PRIORITY ISSUES")
            report.append("-" * 60)
            for issue in [i for i in self.issues if i['severity'] == 'HIGH']:
                report.append(f"🟠 [{issue['category']}] {issue['message']}")
            report.append("")
        
        # Warnings
        if warning_count > 0:
            report.append("WARNINGS")
            report.append("-" * 60)
            for warning in self.warnings:
                report.append(f"⚠️  [{warning['category']}] {warning['message']}")
            report.append("")
        
        # Passed checks
        if passed_count > 0:
            report.append("PASSED CHECKS")
            report.append("-" * 60)
            for passed in self.passed:
                report.append(f"✓ [{passed['category']}] {passed['message']}")
            report.append("")
        
        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 60)
        if critical_count > 0:
            report.append("1. Address all critical issues immediately")
            report.append("2. Do not deploy to production until resolved")
            report.append("3. Run health check again after fixes")
        elif high_count > 0:
            report.append("1. Address high priority issues before production")
            report.append("2. Set up monitoring for warnings")
            report.append("3. Plan maintenance window for fixes")
        elif warning_count > 0:
            report.append("1. Monitor warnings closely")
            report.append("2. Plan to address warnings in next sprint")
            report.append("3. Set up automated health checks")
        else:
            report.append("1. Set up continuous monitoring")
            report.append("2. Schedule regular health checks")
            report.append("3. Maintain documentation")
        report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    """Run health check and generate report."""
    health_check = HealthCheck()
    
    # Run all checks
    results = health_check.run_all_checks()
    
    print()
    
    # Generate and print report
    report = health_check.generate_report()
    print(report)
    
    # Save report to file
    report_file = f"health_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved to: {report_file}")
    
    # Exit with appropriate code
    critical_count = len([i for i in health_check.issues if i['severity'] == 'CRITICAL'])
    if critical_count > 0:
        sys.exit(2)  # Critical issues
    elif len(health_check.issues) > 0:
        sys.exit(1)  # High priority issues
    else:
        sys.exit(0)  # All good


if __name__ == "__main__":
    main()
