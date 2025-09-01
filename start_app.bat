@echo off
echo AI Collection Agent - Port Management Tool
echo =========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if app.py exists
if not exist "app.py" (
    echo Error: app.py not found in current directory
    pause
    exit /b 1
)

echo.
echo Available options:
echo 1. Start with automatic port detection (recommended)
echo 2. Start on specific port
echo 3. Find available ports
echo 4. Kill process on port 7861
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Starting with automatic port detection...
    python start_app.py
) else if "%choice%"=="2" (
    set /p port="Enter port number: "
    echo Starting on port %port%...
    set GRADIO_SERVER_PORT=%port%
    python app.py
) else if "%choice%"=="3" (
    echo Finding available ports...
    python start_app.py --find-port
    pause
) else if "%choice%"=="4" (
    echo Killing process on port 7861...
    python start_app.py --force
    pause
) else if "%choice%"=="5" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice. Please try again.
    pause
    goto :eof
)

pause


