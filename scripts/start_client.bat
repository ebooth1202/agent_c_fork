@echo off
SETLOCAL

cd /d "%~dp0"\..\src\realtime_client
pnpm dev
