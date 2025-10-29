@echo off
SETLOCAL

pnpm --dir "%~dp0\..\src\typescript_client_sdk" dev
