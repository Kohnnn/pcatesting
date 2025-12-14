@echo off
echo ========================================
echo SentimentAlpha Vietnam - Data Update
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Running incremental data update...
echo.

python update_data.py

echo.
echo ========================================
echo Update process complete
echo ========================================
echo.
pause
