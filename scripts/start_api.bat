@echo off
SETLOCAL

:: Change to the parent directory containing this script
cd /d "%~dp0"\..

IF "%1"=="" (
    SET PORT=8000
) ELSE (
    SET PORT=%1
)

echo Activating virtual environment...
call .venv\scripts\activate.bat

if errorlevel 1 (
    echo Failed to activate virtual environment.
    echo Please run scripts\initial_setup.bat first.
    pause
    exit /b 1
)

echo Starting Agent C API on port %PORT% ...
python -m uvicorn agent_c_api.main:app --host 0.0.0.0 --port %PORT% --log-level info --ssl-keyfile agent_c_config/certs/dev_key.pem --ssl-certfile agent_c_config/certs/dev_cert.pem
pause