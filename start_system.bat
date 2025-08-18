@echo off
REM Phone Booth System - Master Startup Script
REM ===========================================
REM Starts backend, waits for it to be ready, then launches frontend

echo.
echo ========================================
echo   Phone Booth System - Starting...
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
cd /d "%~dp0"

echo Step 1: Starting Backend Server...
echo.

REM Start backend in a new window
start "Phone Booth Backend" cmd /c "backend\run_backend.bat"

echo Backend starting in new window...
echo Waiting for backend to be ready...

REM Wait for backend to be accessible
:wait_loop
timeout /t 2 /nobreak >nul
python -c "import httpx; response = httpx.get('http://localhost:8080/v1/healthz', timeout=5); print('Backend is ready!' if response.status_code == 200 else 'Still waiting...')" 2>nul
if errorlevel 1 (
    echo Still waiting for backend...
    goto wait_loop
)

echo.
echo Backend is ready! Starting Frontend...
echo.

REM Start frontend (which will also launch web UI)
start "Phone Booth Frontend" cmd /c "frontend\run_frontend.bat"

echo.
echo ========================================
echo   System Started Successfully!
echo ========================================
echo.
echo Backend: http://localhost:8080
echo Web UI:  http://localhost:5000
echo.
echo Both applications are running in separate windows.
echo Close those windows to stop the system.
echo.
pause
