@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    if not exist ".venv\Scripts\python.exe" py -3 -m venv .venv
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo Python 3 is required. Install Python 3.10 or newer, then run this file again.
        echo During setup, select the option to add Python to PATH.
        pause
        exit /b 1
    )
    if not exist ".venv\Scripts\python.exe" python -m venv .venv
)

if errorlevel 1 (
    echo Could not create the local Python environment.
    pause
    exit /b 1
)

call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 goto :failed
python -m pip install -r requirements.txt
if errorlevel 1 goto :failed
python -m streamlit run app.py
if errorlevel 1 goto :failed
exit /b 0

:failed
echo.
echo BuildPilot could not start. Check the message above and your internet connection.
pause
exit /b 1
