@echo off
setlocal enabledelayedexpansion

rem Character Booth Frontend - Main Entry Point
rem Developer helper to run the frontend booth loop on Windows.
rem Requires dependencies from frontend\requirements.txt installed in the active venv.

echo Character Booth Frontend - Starting...
echo.

rem Check if we're in a virtual environment
python -c "import sys; exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" 2>nul
if %ERRORLEVEL% neq 0 (
    echo WARNING: Virtual environment not detected.
    echo Please activate your virtual environment first:
    echo   .venv\Scripts\Activate.ps1
    echo.
)

rem Change to project root directory (parent of frontend/)
cd /d "%~dp0.."

echo Starting booth application...
echo Press Ctrl+C to stop the application.
echo.

rem Start the frontend application
python -m frontend.booth.main
set EXITCODE=%ERRORLEVEL%

if %EXITCODE% neq 0 (
    echo.
    echo Application exited with error code %EXITCODE%
    echo Check that:
    echo   1. Virtual environment is activated
    echo   2. Dependencies are installed: pip install -r frontend\requirements.txt
    echo   3. Backend server is running (if needed)
)

exit /b %EXITCODE%


