@echo off
setlocal
chcp 65001 >nul
title COLREGS-3D - MO PHONG BUONG LAI HANG HAI
cls

cd /d "%~dp0"
set "HTML_FILE=%~dp0simulator.html"

echo ======================================================================
echo    KHOI CHAY PHAN MEM MO PHONG BUONG LAI COLREGS-3D
echo ======================================================================
echo.
echo Dang mo mo phong tren man hinh...
echo.

set "BROWSER_EXE="
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" set "BROWSER_EXE=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not defined BROWSER_EXE if exist "C:\Program Files\Microsoft\Edge\Application\msedge.exe" set "BROWSER_EXE=C:\Program Files\Microsoft\Edge\Application\msedge.exe"
if not defined BROWSER_EXE if exist "%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe" set "BROWSER_EXE=%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"
if not defined BROWSER_EXE if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set "BROWSER_EXE=C:\Program Files\Google\Chrome\Application\chrome.exe"
if not defined BROWSER_EXE if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" set "BROWSER_EXE=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

if defined BROWSER_EXE goto OPEN_APP_MODE
goto OPEN_DEFAULT

:OPEN_APP_MODE
echo Dang mo cua so ung dung: "%BROWSER_EXE%"
start "" "%BROWSER_EXE%" --app="file:///%HTML_FILE:\=/%" --allow-file-access-from-files --window-size=1520,940 --start-maximized
goto FINISH

:OPEN_DEFAULT
echo Dang mo qua trinh duyet mac dinh cua he thong...
start "" "%HTML_FILE%"

:FINISH
echo.
echo ======================================================================
echo [THANH CONG] Da khoi chay mo phong COLREGS-3D!
echo ======================================================================
echo.
timeout /t 3 >nul
