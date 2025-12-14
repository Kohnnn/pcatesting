@echo off
echo Testing Application Startup
echo ============================
echo.

echo [1/5] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found
    exit /b 1
)
echo OK
echo.

echo [2/5] Checking Node.js...
node --version
if errorlevel 1 (
    echo ERROR: Node.js not found
    exit /b 1
)
echo OK
echo.

echo [3/5] Checking Backend Dependencies...
python -c "import fastapi, uvicorn, sqlalchemy, pandas" 2>nul
if errorlevel 1 (
    echo ERROR: Backend dependencies missing
    echo Run: pip install -r requirements.txt
    exit /b 1
)
echo OK
echo.

echo [4/5] Checking Frontend Dependencies...
if not exist "frontend\node_modules" (
    echo ERROR: Frontend dependencies missing
    echo Run: cd frontend && npm install
    exit /b 1
)
echo OK
echo.

echo [5/5] Checking Database...
if not exist "sentimentalpha.db" (
    echo WARNING: Database not found
    echo Run: python seed_data.py
) else (
    echo OK
)
echo.

echo ============================
echo All checks passed!
echo.
echo To start the application:
echo   1. Backend: python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
echo   2. Frontend: cd frontend && npm run dev
echo.
echo Or use: run_production.bat
echo ============================
pause
