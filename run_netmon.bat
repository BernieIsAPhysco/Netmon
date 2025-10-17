@echo off
title NetMon - Network Monitor
echo.
echo ==============================
echo    Launching NetMon Tool
echo ==============================
echo.

REM Activate virtualenv if you have one (optional)
REM call venv\Scripts\activate

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python not found. Please install Python 3.9+ and try again.
    pause
    exit /b
)

REM Install dependencies if missing
echo Installing required packages...
python -m pip install -r requirements.txt >nul 2>&1

REM Run the app
echo Starting NetMon...
echo (Press Ctrl+C to stop)
echo.
python main.py

echo.
echo ==============================
echo NetMon stopped.
pause
