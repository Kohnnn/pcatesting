@echo off
echo ============================================================
echo Installing UI Dependencies for SentimentAlpha Vietnam
echo ============================================================
echo.

cd frontend

echo Installing @heroicons/react for theme toggle icons...
call npm install @heroicons/react@^2.1.1

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Run: npm run dev
echo   2. Visit: http://localhost:3000/
echo   3. Test dark mode toggle in sidebar
echo.

cd ..
