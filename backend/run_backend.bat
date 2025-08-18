@echo off
setlocal enabledelayedexpansion

rem Character Booth Backend - Main Entry Point
rem Developer helper to start the backend server on Windows.
rem Requires dependencies from backend\requirements.txt installed in the active venv.

echo Character Booth Backend - Starting...
echo.

rem Check if we're in a virtual environment
python -c "import sys; exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" 2>nul
if %ERRORLEVEL% neq 0 (
    echo WARNING: Virtual environment not detected.
    echo Please activate your virtual environment first:
    echo   .venv\Scripts\Activate.ps1
    echo.
)

rem Change to project root directory (parent of backend/)
cd /d "%~dp0.."

rem Set up environment
set APP_IMPORT=backend.app.main:create_app
set HOST=0.0.0.0
set PORT=8080

echo Starting server on %HOST%:%PORT%...
echo.
echo Network Access:
echo   - Local: http://localhost:%PORT%
echo   - Network: http://[YOUR_IP]:%PORT%
echo   - Update config/frontend.json with your backend IP
echo.
echo Press Ctrl+C to stop the server.
echo.

rem Start the server
python -m uvicorn %APP_IMPORT% --host %HOST% --port %PORT%
set EXITCODE=%ERRORLEVEL%

if %EXITCODE% neq 0 (
    echo.
    echo Server exited with error code %EXITCODE%
    echo Check that:
    echo   1. Virtual environment is activated
    echo   2. Dependencies are installed: pip install -r backend\requirements.txt
    echo   3. No other service is using port %PORT%
)

exit /b %EXITCODE%


