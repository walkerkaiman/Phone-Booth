@echo off
setlocal enabledelayedexpansion

rem Example script to fetch model assets required by backend/frontend (placeholder).
rem Edit to add real download URLs and target directories.

set MODELS_DIR=%MODELS_DIR%
if "%MODELS_DIR%"=="" set MODELS_DIR=%cd%\models
if not exist "%MODELS_DIR%" mkdir "%MODELS_DIR%"

echo Models directory: "%MODELS_DIR%"
echo Populate this script with powershell/curl commands to download GGUF and TTS models.

rem Example (commented):
rem powershell -Command "Invoke-WebRequest -Uri https://example.com/llama3.1-8b.Q4_K_M.gguf -OutFile `"%MODELS_DIR%\llama3.1-8b.Q4_K_M.gguf`""

exit /b 0


