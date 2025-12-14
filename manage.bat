@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: SentimentAlpha Vietnam - Unified Management Script
:: All-in-one batch file for development, testing, and deployment
:: ============================================================================

title SentimentAlpha Vietnam

set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

set "BACKEND_PORT=8000"
set "FRONTEND_PORT=3000"
set "LOG_DIR=logs"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

:menu
cls
echo %BLUE%============================================================================%RESET%
echo %BLUE%                    SentimentAlpha Vietnam Manager                         %RESET%
echo %BLUE%============================================================================%RESET%
echo.
echo   %GREEN%[1]%RESET% Quick Start (Start Both Servers)
echo   %GREEN%[2]%RESET% Full Setup (Install Dependencies + Initialize DB)
echo   %GREEN%[3]%RESET% Backend Only
echo   %GREEN%[4]%RESET% Frontend Only
echo   %GREEN%[5]%RESET% Database Operations
echo   %GREEN%[6]%RESET% Update Data (Incremental)
echo   %GREEN%[7]%RESET% Run Tests
echo   %GREEN%[8]%RESET% Verify Installation
echo   %GREEN%[9]%RESET% Clean Build Artifacts
echo   %GREEN%[0]%RESET% Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto quick_start
if "%choice%"=="2" goto full_setup
if "%choice%"=="3" goto backend_only
if "%choice%"=="4" goto frontend_only
if "%choice%"=="5" goto db_menu
if "%choice%"=="6" goto update_data
if "%choice%"=="7" goto test_menu
if "%choice%"=="8" goto verify
if "%choice%"=="9" goto clean
if "%choice%"=="0" goto end
goto menu

:: ============================================================================
:: Quick Start
:: ============================================================================
:quick_start
cls
echo %BLUE%Starting SentimentAlpha Vietnam...%RESET%
echo.
echo %YELLOW%Starting Backend (Port %BACKEND_PORT%)...%RESET%
start "SentimentAlpha Backend" cmd /k "title SentimentAlpha Backend && python -m uvicorn backend.main:app --host 0.0.0.0 --port %BACKEND_PORT% --reload"
timeout /t 3 /nobreak >nul

echo %YELLOW%Starting Frontend (Port %FRONTEND_PORT%)...%RESET%
start "SentimentAlpha Frontend" cmd /k "title SentimentAlpha Frontend && cd frontend && npm run dev"

echo.
echo %GREEN%✓ Servers started successfully!%RESET%
echo.
echo   Dashboard:  %BLUE%http://localhost:%FRONTEND_PORT%%RESET%
echo   API:        %BLUE%http://localhost:%BACKEND_PORT%%RESET%
echo   API Docs:   %BLUE%http://localhost:%BACKEND_PORT%/docs%RESET%
echo.
pause
goto menu

:: ============================================================================
:: Full Setup
:: ============================================================================
:full_setup
cls
echo %BLUE%Full Setup%RESET%
echo.

echo %YELLOW%[1/4] Checking Python...%RESET%
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%ERROR: Python not found. Install Python 3.8+%RESET%
    pause
    goto menu
)
echo       %GREEN%✓ Python found%RESET%

echo %YELLOW%[2/4] Installing Python dependencies...%RESET%
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo %RED%ERROR: Failed to install Python dependencies%RESET%
    pause
    goto menu
)
echo       %GREEN%✓ Python dependencies installed%RESET%

echo %YELLOW%[3/4] Checking Node.js...%RESET%
node --version >nul 2>&1
if errorlevel 1 (
    echo %RED%ERROR: Node.js not found. Install Node.js 16+%RESET%
    pause
    goto menu
)
echo       %GREEN%✓ Node.js found%RESET%

echo %YELLOW%[4/4] Installing frontend dependencies...%RESET%
cd frontend
call npm install --silent
cd ..
echo       %GREEN%✓ Frontend dependencies installed%RESET%

echo.
echo %GREEN%✓ Setup completed!%RESET%
echo.
set /p init_db="Initialize database with seed data? (y/n): "
if /i "%init_db%"=="y" goto seed_db
pause
goto menu

:: ============================================================================
:: Backend Only
:: ============================================================================
:backend_only
cls
echo %BLUE%Starting Backend Server...%RESET%
python -m uvicorn backend.main:app --host 0.0.0.0 --port %BACKEND_PORT% --reload
goto menu

:: ============================================================================
:: Frontend Only
:: ============================================================================
:frontend_only
cls
echo %BLUE%Starting Frontend Server...%RESET%
cd frontend
call npm run dev
cd ..
goto menu

:: ============================================================================
:: Database Menu
:: ============================================================================
:db_menu
cls
echo %BLUE%Database Operations%RESET%
echo.
echo   %GREEN%[1]%RESET% Initialize/Seed Database
echo   %GREEN%[2]%RESET% Backup Database
echo   %GREEN%[3]%RESET% Reset Database
echo   %GREEN%[4]%RESET% View Database Stats
echo   %GREEN%[0]%RESET% Back
echo.
set /p db_choice="Select option: "

if "%db_choice%"=="1" goto seed_db
if "%db_choice%"=="2" goto backup_db
if "%db_choice%"=="3" goto reset_db
if "%db_choice%"=="4" goto db_stats
if "%db_choice%"=="0" goto menu
goto db_menu

:seed_db
cls
echo %YELLOW%Initializing database...%RESET%
python seed_data.py
if errorlevel 1 (
    echo %RED%ERROR: Database seeding failed%RESET%
) else (
    echo %GREEN%✓ Database initialized!%RESET%
)
pause
goto db_menu

:backup_db
cls
set "BACKUP_FILE=backups\sentimentalpha_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db"
if not exist "backups" mkdir "backups"
echo %YELLOW%Creating backup...%RESET%
copy sentimentalpha.db "%BACKUP_FILE%" >nul
if errorlevel 1 (
    echo %RED%ERROR: Backup failed%RESET%
) else (
    echo %GREEN%✓ Backup created: %BACKUP_FILE%%RESET%
)
pause
goto db_menu

:reset_db
cls
echo %RED%WARNING: This will delete all data!%RESET%
set /p confirm="Type 'yes' to confirm: "
if /i "%confirm%"=="yes" (
    del sentimentalpha.db 2>nul
    echo %YELLOW%Re-seeding database...%RESET%
    python seed_data.py
    echo %GREEN%✓ Database reset complete!%RESET%
)
pause
goto db_menu

:db_stats
cls
echo %BLUE%Database Statistics%RESET%
echo.
python -c "import sqlite3; conn = sqlite3.connect('sentimentalpha.db'); cursor = conn.cursor(); cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table'\"); tables = cursor.fetchall(); print('Tables:', len(tables)); [print(f'  - {t[0]}: {cursor.execute(f\"SELECT COUNT(*) FROM {t[0]}\").fetchone()[0]} rows') for t in tables]; conn.close()"
echo.
pause
goto db_menu

:: ============================================================================
:: Update Data
:: ============================================================================
:update_data
cls
echo %BLUE%Incremental Data Update%RESET%
echo.
python update_data.py
if errorlevel 1 (
    echo %RED%ERROR: Data update failed%RESET%
) else (
    echo %GREEN%✓ Data updated!%RESET%
)
pause
goto menu

:: ============================================================================
:: Test Menu
:: ============================================================================
:test_menu
cls
echo %BLUE%Test Suite%RESET%
echo.
echo   %GREEN%[1]%RESET% Run All Tests
echo   %GREEN%[2]%RESET% Run Unit Tests
echo   %GREEN%[3]%RESET% Run Integration Tests
echo   %GREEN%[4]%RESET% Run Property Tests
echo   %GREEN%[5]%RESET% Run with Coverage
echo   %GREEN%[6]%RESET% Frontend Lint
echo   %GREEN%[0]%RESET% Back
echo.
set /p test_choice="Select option: "

if "%test_choice%"=="1" (pytest tests/ -v & pause & goto test_menu)
if "%test_choice%"=="2" (pytest tests/unit/ -v & pause & goto test_menu)
if "%test_choice%"=="3" (pytest tests/integration/ -v & pause & goto test_menu)
if "%test_choice%"=="4" (pytest tests/property/ -v & pause & goto test_menu)
if "%test_choice%"=="5" (pytest tests/ -v --cov=src --cov=backend --cov-report=html & echo Coverage: htmlcov/index.html & pause & goto test_menu)
if "%test_choice%"=="6" (cd frontend & call npm run lint & cd .. & pause & goto test_menu)
if "%test_choice%"=="0" goto menu
goto test_menu

:: ============================================================================
:: Verify Installation
:: ============================================================================
:verify
cls
echo %BLUE%Verifying Installation%RESET%
echo.

set "pass=0"
set "fail=0"

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (echo   %RED%✗ Python not found%RESET% & set /a fail+=1) else (echo   %GREEN%✓ Python found%RESET% & set /a pass+=1)

echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (echo   %RED%✗ Node.js not found%RESET% & set /a fail+=1) else (echo   %GREEN%✓ Node.js found%RESET% & set /a pass+=1)

echo Checking backend files...
if exist "backend\main.py" (echo   %GREEN%✓ Backend files found%RESET% & set /a pass+=1) else (echo   %RED%✗ Backend files missing%RESET% & set /a fail+=1)

echo Checking frontend files...
if exist "frontend\package.json" (echo   %GREEN%✓ Frontend files found%RESET% & set /a pass+=1) else (echo   %RED%✗ Frontend files missing%RESET% & set /a fail+=1)

echo Checking database...
if exist "sentimentalpha.db" (echo   %GREEN%✓ Database found%RESET% & set /a pass+=1) else (echo   %YELLOW%! Database not found (run option 5-1 to initialize)%RESET%)

echo Checking frontend dependencies...
if exist "frontend\node_modules" (echo   %GREEN%✓ Node modules installed%RESET% & set /a pass+=1) else (echo   %YELLOW%! Node modules not installed (run option 2)%RESET%)

echo.
echo %BLUE%Results: %GREEN%!pass! passed%RESET% %RED%!fail! failed%RESET%
echo.
if !fail! equ 0 (
    echo %GREEN%✓ Ready to start! Use option 1 to launch.%RESET%
) else (
    echo %RED%✗ Please fix errors above before starting.%RESET%
)
echo.
pause
goto menu

:: ============================================================================
:: Clean
:: ============================================================================
:clean
cls
echo %BLUE%Cleaning Build Artifacts%RESET%
echo.
echo %YELLOW%Cleaning Python cache...%RESET%
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul

echo %YELLOW%Cleaning frontend build...%RESET%
if exist "frontend\.next" rd /s /q "frontend\.next"
if exist "frontend\node_modules\.cache" rd /s /q "frontend\node_modules\.cache"

echo %YELLOW%Cleaning logs...%RESET%
if exist "%LOG_DIR%" del /q "%LOG_DIR%\*.log" 2>nul

echo.
echo %GREEN%✓ Cleanup complete!%RESET%
pause
goto menu

:: ============================================================================
:: End
:: ============================================================================
:end
echo.
echo %GREEN%Goodbye!%RESET%
endlocal
exit /b 0
