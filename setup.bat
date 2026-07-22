@echo off
REM LiveMagic Pro Setup Script for Windows

echo ============================================
echo LiveMagic Pro - Setup Script
echo ============================================
echo.

REM Check Python version
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo XX Python not found!
    echo Install from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo OK Found Python %PYTHON_VERSION%
echo.

REM Install dependencies
echo [2/4] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo XX Failed to install dependencies
    pause
    exit /b 1
)
echo OK Dependencies installed
echo.

REM Check FFmpeg
echo [3/4] Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ^^ FFmpeg not found
    echo The app will auto-download FFmpeg on first run
) else (
    echo OK FFmpeg found
)
echo.

REM Create directories
echo [4/4] Creating directories...
if not exist "logs" mkdir logs
if not exist ".cache" mkdir .cache
echo OK Directories created
echo.

echo ============================================
echo OK Setup Complete!
echo ============================================
echo.
echo To start streaming:
echo   python live_streamer_enhanced.py
echo.
pause
