@echo off
setlocal
cd /d "%~dp0"

set "VENV_PATH=%~dp0venv"

if not exist "%VENV_PATH%" (
    echo ⚠️ Virtual environment not found. Running setup first...
    call setup.bat
)

:MENU
echo.
echo ========================================
echo       MediMind AI Launcher
echo ========================================
echo.
echo Choose which backend to run:
echo [1] Flask (Port 5000)
echo [2] FastAPI (Port 8000)
echo [3] Exit
echo.

set /p choice="Enter your choice (1, 2, or 3): "

:: Remove any potential quotes or spaces
set choice=%choice:"=%
set choice=%choice: =%

if "%choice%"=="1" goto RUN_FLASK
if "%choice%"=="2" goto RUN_FASTAPI
if "%choice%"=="3" exit /b

echo ❌ Invalid choice. Please try again.
goto MENU

:RUN_FLASK
echo.
echo 🚀 Starting MediMind AI (Flask Backend)...
if exist "app\app.py" (
    "%VENV_PATH%\Scripts\python.exe" app\app.py
) else (
    echo ❌ ERROR: app\app.py not found!
    echo Current location: %CD%
)
goto END

:RUN_FASTAPI
echo.
echo 🚀 Starting MediMind AI (FastAPI Backend)...
if exist "app\main.py" (
    "%VENV_PATH%\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
) else (
    echo ❌ ERROR: app\main.py not found!
    echo Current location: %CD%
)
goto END

:END
echo.
echo 👋 Press any key to close launcher...
pause >nul
exit /b
