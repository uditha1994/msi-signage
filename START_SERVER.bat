@echo off
title MSI Digital Signage
color 0A
chcp 65001 >nul 2>&1

echo.
echo  ================================================
echo    MSI Campus Digital Signage System
echo  ================================================
echo.

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo  [ERROR] Python not installed!
    echo  Download from: https://python.org
    echo  Check "Add Python to PATH" when installing.
    pause & exit /b 1
)

echo  [..] Installing packages...
pip install flask flask-cors werkzeug --quiet --disable-pip-version-check
echo  [OK] Ready.
echo.

:: Allow through Windows Firewall (so Smart TV can access)
echo  [..] Allowing port 5000 through Windows Firewall...
netsh advfirewall firewall delete rule name="MSI Signage Port 5000" >nul 2>&1
netsh advfirewall firewall add rule name="MSI Signage Port 5000" dir=in action=allow protocol=TCP localport=5000 >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo  [OK] Firewall rule added - network devices can now connect.
) ELSE (
    echo  [WARN] Could not add firewall rule - run as Administrator if TV cannot connect.
)
echo.

:: Open admin in browser
timeout /t 2 /nobreak >nul
start http://localhost:5000

:: Start server
python server.py

pause
