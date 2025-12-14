@echo off
echo ========================================
echo Environment Variable Check
echo ========================================
echo.
echo Checking frontend/.env.local:
type frontend\.env.local
echo.
echo ========================================
echo Checking frontend/.env.production:
type frontend\.env.production
echo.
echo ========================================
echo.
echo The .env.local file takes precedence!
echo Make sure it points to: https://backendforpca.share.zrok.io
echo.
pause
