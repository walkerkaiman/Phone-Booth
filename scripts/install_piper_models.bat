@echo off
REM Install Piper TTS Models
REM ========================

echo 🎤 Piper TTS Model Installer
echo =============================
echo.

REM Check if virtual environment is active
if not defined VIRTUAL_ENV (
    echo WARNING: Virtual environment not detected!
    echo Please activate your virtual environment first:
    echo   .venv\Scripts\Activate.ps1
    echo.
    pause
    exit /b 1
)

REM Change to project root
cd /d "%~dp0.."

echo Installing Piper TTS models...
echo.

REM Run the installer script
python scripts\install_piper_models.py

echo.
echo Installation complete!
echo.
echo To use the new models:
echo 1. Restart the web UI
echo 2. Test with different personalities
echo.
pause
