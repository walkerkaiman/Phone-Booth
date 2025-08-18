@echo off
REM Phone Booth Web UI Startup Script
REM ===================================

echo.
echo ========================================
echo   Phone Booth Web UI - Starting...
echo ========================================
echo.

REM Check if we're in a virtual environment
if not defined VIRTUAL_ENV (
    echo WARNING: Virtual environment not detected!
    echo Please activate your virtual environment first:
    echo   .venv\Scripts\activate
    echo.
    pause
    exit /b 1
)

REM Change to project root directory
cd /d "%~dp0..\.."

REM Check if backend is running
echo Checking backend connectivity...
python -c "import httpx; response = httpx.get('http://localhost:8080/v1/healthz', timeout=5); print('Backend is running' if response.status_code == 200 else 'Backend not responding')" 2>nul
if errorlevel 1 (
    echo WARNING: Backend not accessible at http://localhost:8080
    echo Please start the backend first:
    echo   backend\run_backend.bat
    echo.
    pause
    exit /b 1
)

REM Install web UI dependencies if needed
echo Installing web UI dependencies...
pip install -r frontend/web_ui/requirements.txt

REM Start the web UI
echo.
echo Starting Phone Booth Web UI...
echo.
echo Access the interface at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server.
echo.

python frontend/web_ui/app.py

pause
