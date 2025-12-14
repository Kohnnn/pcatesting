@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: SentimentAlpha Vietnam - Development Script
:: Comprehensive batch file for development, testing, and deployment
:: ============================================================================

title SentimentAlpha Vietnam - Development Environment

:: Colors for output (Windows 10+)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

:: Configuration
set "BACKEND_PORT=8000"
set "FRONTEND_PORT=3000"
set "LOG_DIR=logs"
set "LOG_FILE=%LOG_DIR%\dev_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%.log"

:: Create logs directory
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

:: Main menu
:menu
cls
echo %BLUE%============================================================================%RESET%
echo %BLUE%           SentimentAlpha Vietnam - Development Environment                %RESET%
echo %BLUE%============================================================================%RESET%
echo.
echo   %GREEN%[1]%RESET% Full Setup (Install all dependencies + Initialize DB)
echo   %GREEN%[2]%RESET% Start Development Servers (Frontend + Backend)
echo   %GREEN%[3]%RESET% Backend Only
echo   %GREEN%[4]%RESET% Frontend Only
echo   %GREEN%[5]%RESET% Database Operations
echo   %GREEN%[6]%RESET% Run Tests
echo   %GREEN%[7]%RESET% Update Data (Incremental)
echo   %GREEN%[8]%RESET% Debug Mode (Verbose Logging)
echo   %GREEN%[9]%RESET% Clean Build Artifacts
echo   %GREEN%[0]%RESET% Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto full_setup
if "%choice%"=="2" goto start_dev
if "%choice%"=="3" goto backend_only
if "%choice%"=="4" goto frontend_only
if "%choice%"=="5" goto db_menu
if "%choice%"=="6" goto test_menu
if "%choice%"=="7" goto update_data
if "%choice%"=="8" goto debug_mode
if "%choice%"=="9" goto clean
if "%choice%"=="0" goto end
goto menu

:: ============================================================================
:: Full Setup
:: ============================================================================
:full_setup
cls
echo %BLUE%============================================================================%RESET%
echo %BLUE%                         Full Setup                                        %RESET%
echo %BLUE%============================================================================%RESET%
echo.
call :log "Starting full setup..."

echo %YELLOW%[1/4] Checking Python installation...%RESET%
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%ERROR: Python not found. Please install Python 3.8+%RESET%
    call :log "ERROR: Python not found"
    pause
    goto menu
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo       Python %PYTHON_VERSION% found
call :log "Python %PYTHON_VERSION% found"

echo %YELLOW%[2/4] Installing Python dependencies...%RESET%
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo %RED%ERROR: Failed to install Python dependencies%RESET%
    call :log "ERROR: pip install failed"
    pause
    goto menu
)
echo       %GREEN%Python dependencies installed successfully%RESET%
call :log "Python dependencies installed"

echo %YELLOW%[3/4] Checking Node.js installation...%RESET%
node --version >nul 2>&1
if errorlevel 1 (
    echo %RED%ERROR: Node.js not found. Please install Node.js 16+%RESET%
    call :log "ERROR: Node.js not found"
    pause
    goto menu
)
for /f "tokens=1" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
echo       Node.js %NODE_VERSION% found
call :log "Node.js %NODE_VERSION% found"

echo %YELLOW%[4/4] Installing frontend dependencies...%RESET%
cd frontend
call npm install --silent
if errorlevel 1 (
    echo %RED%ERROR: Failed to install frontend dependencies%RESET%
    call :log "ERROR: npm install failed"
    cd ..
    pause
    goto menu
)
cd ..
echo       %GREEN%Frontend dependencies installed successfully%RESET%
call :log "Frontend dependencies installed"

echo.
echo %GREEN%============================================================================%RESET%
echo %GREEN%                    Setup completed successfully!                          %RESET%
echo %GREEN%============================================================================%RESET%
call :log "Full setup completed successfully"
echo.
set /p init_db="Initialize database with seed data? (y/n): "
if /i "%init_db%"=="y" goto seed_db
pause
goto menu

:: ============================================================================
:: Start Development Servers
:: ============================================================================
:start_dev
cls
echo %BLUE%============================================================================%RESET%
echo %BLUE%                Starting Development Servers                               %RESET%
echo %BLUE%============================================================================%RESET%
echo.
call :log "Starting development servers..."

echo %YELLOW%Starting Backend (Port %BACKEND_PORT%)...%RESET%
start "SentimentAlpha Backend" cmd /k "title SentimentAlpha Backend && python -m uvicorn backend.main:app --host 0.0.0.0 --port %BACKEND_PORT% --reload"
call :log "Backend server started on port %BACKEND_PORT%"

timeout /t 3 /nobreak >nul

echo %YELLOW%Starting Frontend (Port %FRONTEND_PORT%)...%RESET%
start "SentimentAlpha Frontend" cmd /k "title SentimentAlpha Frontend && cd frontend && npm run dev"
call :log "Frontend server started on port %FRONTEND_PORT%"

echo.
echo %GREEN%============================================================================%RESET%
echo %GREEN%                    Servers Started Successfully!                          %RESET%
echo %GREEN%============================================================================%RESET%
echo.
echo   Dashboard:  %BLUE%http://localhost:%FRONTEND_PORT%%RESET%
echo   API:        %BLUE%http://localhost:%BACKEND_PORT%%RESET%
echo   API Docs:   %BLUE%http://localhost:%BACKEND_PORT%/docs%RESET%
echo.
echo   Press any key to return to menu (servers will keep running)
pause >nul
goto menu

:: ============================================================================
:: Backend Only
:: ============================================================================
:backend_only
cls
echo %BLUE%Starting Backend Server...%RESET%
call :log "Starting backend only..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port %BACKEND_PORT% --reload
goto menu

:: ============================================================================
:: Frontend Only
:: ============================================================================
:frontend_only
cls
echo %BLUE%Starting Frontend Server...%RESET%
call :log "Starting frontend only..."
cd frontend
call npm run dev
cd ..
goto menu

:: ============================================================================
:: Database Menu
:: ============================================================================
:db_menu
cls
echo %BLUE%============================================================================%RESET%
echo %BLUE%                      Database Operations                                   %RESET%
echo %BLUE%============================================================================%RESET%
echo.
echo   %GREEN%[1]%RESET% Initialize/Seed Database
echo   %GREEN%[2]%RESET% Backup Database
echo   %GREEN%[3]%RESET% Restore Database
echo   %GREEN%[4]%RESET% Reset Database (Delete and Recreate)
echo   %GREEN%[5]%RESET% View Database Stats
echo   %GREEN%[0]%RESET% Back to Main Menu
echo.
set /p db_choice="Select option: "

if "%db_choice%"=="1" goto seed_db
if "%db_choice%"=="2" goto backup_db
if "%db_choice%"=="3" goto restore_db
if "%db_choice%"=="4" goto reset_db
if "%db_choice%"=="5" goto db_stats
if "%db_choice%"=="0" goto menu
goto db_menu

:seed_db
cls
echo %YELLOW%Initializing database with seed data...%RESET%
call :log "Seeding database..."
python seed_data.py
if errorlevel 1 (
    echo %RED%ERROR: Database seeding failed%RESET%
    call :log "ERROR: Database seeding failed"
) else (
    echo %GREEN%Database initialized successfully!%RESET%
    call :log "Database seeded successfully"
)
pause
goto db_menu

:backup_db
cls
set "BACKUP_FILE=backups\sentimentalpha_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db"
if not exist "backups" mkdir "backups"
echo %YELLOW%Creating backup: %BACKUP_FILE%%RESET%
copy sentimentalpha.db "%BACKUP_FILE%" >nul
if errorlevel 1 (
    echo %RED%ERROR: Backup failed%RESET%
    call :log "ERROR: Database backup failed"
) else (
    echo %GREEN%Backup created successfully!%RESET%
    call :log "Database backed up to %BACKUP_FILE%"
)
pause
goto db_menu

:restore_db
cls
echo %YELLOW%Available backups:%RESET%
dir /b backups\*.db 2>nul
if errorlevel 1 (
    echo %RED%No backups found%RESET%
    pause
    goto db_menu
)
echo.
set /p restore_file="Enter backup filename (or 0 to cancel): "
if "%restore_file%"=="0" goto db_menu
if exist "backups\%restore_file%" (
    copy "backups\%restore_file%" sentimentalpha.db >nul
    echo %GREEN%Database restored from %restore_file%%RESET%
    call :log "Database restored from %restore_file%"
) else (
    echo %RED%Backup file not found%RESET%
)
pause
goto db_menu

:reset_db
cls
echo %RED%WARNING: This will delete all data!%RESET%
set /p confirm="Are you sure? Type 'yes' to confirm: "
if /i "%confirm%"=="yes" (
    del sentimentalpha.db 2>nul
    echo %YELLOW%Database deleted. Re-seeding...%RESET%
    call :log "Database reset initiated"
    python seed_data.py
    echo %GREEN%Database reset complete!%RESET%
    call :log "Database reset completed"
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
:: Test Menu
:: ============================================================================
:test_menu
cls
echo %BLUE%============================================================================%RESET%
echo %BLUE%                         Test Suite                                        %RESET%
echo %BLUE%============================================================================%RESET%
echo.
echo   %GREEN%[1]%RESET% Run All Tests
echo   %GREEN%[2]%RESET% Run Unit Tests
echo   %GREEN%[3]%RESET% Run Integration Tests
echo   %GREEN%[4]%RESET% Run Property-Based Tests
echo   %GREEN%[5]%RESET% Run Tests with Coverage
echo   %GREEN%[6]%RESET% Run Frontend Lint
echo   %GREEN%[0]%RESET% Back to Main Menu
echo.
set /p test_choice="Select option: "

if "%test_choice%"=="1" goto test_all
if "%test_choice%"=="2" goto test_unit
if "%test_choice%"=="3" goto test_integration
if "%test_choice%"=="4" goto test_property
if "%test_choice%"=="5" goto test_coverage
if "%test_choice%"=="6" goto test_lint
if "%test_choice%"=="0" goto menu
goto test_menu

:test_all
cls
echo %YELLOW%Running all tests...%RESET%
call :log "Running all tests..."
pytest tests/ -v
call :log "All tests completed"
pause
goto test_menu

:test_unit
cls
echo %YELLOW%Running unit tests...%RESET%
pytest tests/unit/ -v
pause
goto test_menu

:test_integration
cls
echo %YELLOW%Running integration tests...%RESET%
pytest tests/integration/ -v
pause
goto test_menu

:test_property
cls
echo %YELLOW%Running property-based tests...%RESET%
pytest tests/property/ -v
pause
goto test_menu

:test_coverage
cls
echo %YELLOW%Running tests with coverage...%RESET%
pytest tests/ -v --cov=src --cov=backend --cov-report=html
echo %GREEN%Coverage report generated in htmlcov/%RESET%
pause
goto test_menu

:test_lint
cls
echo %YELLOW%Running frontend lint...%RESET%
cd frontend
call npm run lint
cd ..
pause
goto test_menu

:: ============================================================================
:: Update Data
:: ============================================================================
:update_data
cls
echo %BLUE%============================================================================%RESET%
echo %BLUE%                    Incremental Data Update                                %RESET%
echo %BLUE%============================================================================%RESET%
echo.
call :log "Starting incremental data update..."
python update_data.py
if errorlevel 1 (
    echo %RED%ERROR: Data update failed%RESET%
    call :log "ERROR: Data update failed"
) else (
    echo %GREEN%Data updated successfully!%RESET%
    call :log "Data update completed"
)
pause
goto menu

:: ============================================================================
:: Debug Mode
:: ============================================================================
:debug_mode
cls
echo %BLUE%============================================================================%RESET%
echo %BLUE%                    Debug Mode (Verbose Logging)                           %RESET%
echo %BLUE%============================================================================%RESET%
echo.
call :log "Starting debug mode..."

echo %YELLOW%Starting Backend with DEBUG logging...%RESET%
set LOG_LEVEL=DEBUG
start "SentimentAlpha Backend (DEBUG)" cmd /k "title SentimentAlpha Backend (DEBUG) && set LOG_LEVEL=DEBUG && python -m uvicorn backend.main:app --host 0.0.0.0 --port %BACKEND_PORT% --reload --log-level debug"

timeout /t 3 /nobreak >nul

echo %YELLOW%Starting Frontend with verbose output...%RESET%
start "SentimentAlpha Frontend (DEBUG)" cmd /k "title SentimentAlpha Frontend (DEBUG) && cd frontend && set DEBUG=* && npm run dev"

echo.
echo %GREEN%Debug servers started with verbose logging%RESET%
echo Check the terminal windows for detailed output
echo.
pause
goto menu

:: ============================================================================
:: Clean Build Artifacts
:: ============================================================================
:clean
cls
echo %BLUE%============================================================================%RESET%
echo %BLUE%                    Cleaning Build Artifacts                               %RESET%
echo %BLUE%============================================================================%RESET%
echo.
call :log "Cleaning build artifacts..."

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
echo %GREEN%Cleanup complete!%RESET%
call :log "Cleanup completed"
pause
goto menu

:: ============================================================================
:: Logging Function
:: ============================================================================
:log
echo [%date% %time%] %~1 >> "%LOG_FILE%"
goto :eof

:: ============================================================================
:: End
:: ============================================================================
:end
echo.
echo %GREEN%Goodbye!%RESET%
call :log "Development script ended"
endlocal
exit /b 0
