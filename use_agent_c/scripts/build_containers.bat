@echo off
SETLOCAL

:: Change to the directory containing this script
cd /d "%~dp0"
cd ..\..
docker build -t agentc-api:latest -f api.Dockerfile .
docker build -t agentc-client:latest -f client.Dockerfile src\realtime_client

cd /d "%~dp0"