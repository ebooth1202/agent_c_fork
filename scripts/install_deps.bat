@echo off
SETLOCAL

:: Store the starting directory
pushd %CD%
CALL .venv\scripts\activate

:: Install the Python backend requirements
echo Installing Python backend dependencies...
python -m pip install --upgrade pip

cd src

echo Installing agent_c_core...
pip install -e agent_c_core

if errorlevel 1 (
    echo Failed to install agent_c_core.
    popd
    exit /b 1
)

echo Installing agent_c_tools (includes playwright)...
pip install -e agent_c_tools

if errorlevel 1 (
    echo Failed to install agent_c_tools.
    popd
    exit /b 1
)

echo Installing agent_c_api...
pip install -e agent_c_api[dev]

if errorlevel 1 (
    echo Failed to install agent_c_api.
    popd
    exit /b 1
)

echo Installing Playwright browsers...
playwright install

if errorlevel 1 (
    echo Failed to install Playwright browsers.
    popd
    exit /b 1
)

echo Installing ace_proto...
pip install -e ace_proto

if errorlevel 1 (
    echo Failed to install ace_proto.
    popd
    exit /b 1
)

echo Rebuilding TypeScript Client SDK...
cd typescript_client_sdk
call scripts\rebuild.bat

if errorlevel 1 (
    echo Failed to rebuild TypeScript Client SDK.
    popd
    exit /b 1
)

:: Return to the original directory
popd

echo All dependencies installed successfully.
ENDLOCAL
