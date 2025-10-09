@echo off
SETLOCAL

:: Change to the parent directory containing this script
cd /d "%~dp0"\..
call docker_support\windows.env.bat
docker build -t ghcr.io/centricconsulting/agentc-api:latest -f api.Dockerfile .