@echo off
:: This version runs with admin rights for firewall config
net session >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Requesting Administrator access...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
call "%~dp0START_SERVER.bat"
