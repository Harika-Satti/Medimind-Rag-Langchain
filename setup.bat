@echo off
setlocal

:: Change to the directory where the script is located
cd /d "%~dp0"

echo 🛠️ Setting up MediMind Environment...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.10+ and try again.
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo 🏗️ Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ ERROR: Failed to create virtual environment.
        pause
        exit /b %errorlevel%
    )
)

echo 📦 Installing/Updating dependencies...
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ ERROR: Failed to install requirements. Please check your internet connection.
    pause
    exit /b %errorlevel%
)

echo.
echo -----------------------------------
echo ✅ Setup complete! You can now run MediMind using run.bat.
echo -----------------------------------
pause
