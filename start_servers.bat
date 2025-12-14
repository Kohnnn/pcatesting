@echo off
echo Starting SentimentAlpha Vietnam servers...

echo.
echo Starting Backend Server (Port 8000)...
start "SentimentAlpha Backend" cmd /k "title SentimentAlpha Backend && python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server (Port 3000)...
start "SentimentAlpha Frontend" cmd /k "title SentimentAlpha Frontend && cd frontend && npm run dev"

echo.
echo ✓ Servers started successfully!
echo.
echo   Dashboard:  http://localhost:3000
echo   API:        http://localhost:8000
echo   API Docs:   http://localhost:8000/docs
echo.
echo Press any key to exit (servers will keep running)
pause >nul