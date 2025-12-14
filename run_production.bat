@echo off
echo ========================================
echo SentimentAlpha Vietnam - Production Launcher
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if database exists
if not exist sentimentalpha.db (
    echo.
    echo Database not found. Initializing database...
    echo This may take a few minutes...
    echo.
    python seed_data.py
    if errorlevel 1 (
        echo ERROR: Database initialization failed
        pause
        exit /b 1
    )
    echo.
    echo Database initialized successfully!
    echo.
) else (
    echo.
    echo Database found. Running incremental data pipeline...
    echo.
    python update_data.py
    if errorlevel 1 (
        echo WARNING: Data pipeline completed with errors
        echo Check the output above for details
        echo.
    ) else (
        echo.
        echo Data pipeline completed successfully!
        echo.
    )
)

echo Starting Backend Server...
echo Backend will be available at: http://localhost:8000
echo.

REM Start backend in a new window
start "SentimentAlpha Backend" cmd /k "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
echo Frontend will be available at: http://localhost:3000
echo.

REM Start frontend in a new window
start "SentimentAlpha Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo Data Management: http://localhost:3000/data-management
echo ========================================
echo.
echo Press any key to exit this launcher window.
echo (The servers will continue running in their own windows)
pause >nul
