@echo off
setlocal
chcp 65001 >nul
title COLREGS-3D - MAY CHU MOBILE VA PC
cls

cd /d "%~dp0"

echo ======================================================================
echo    KHOI CHAY MAY CHU CHO DIEN THOAI VA MAY TINH (COLREGS-3D)
echo ======================================================================
echo.

set "PY="
if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if not defined PY if exist "C:\Users\ASUS\AppData\Local\Programs\Python\Python310\python.exe" set "PY=C:\Users\ASUS\AppData\Local\Programs\Python\Python310\python.exe"
if not defined PY if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PY if exist "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe" set "PY=C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe"
if not defined PY if exist "%ProgramFiles%\Python310\python.exe" set "PY=%ProgramFiles%\Python310\python.exe"
if not defined PY if exist "%ProgramFiles%\Python311\python.exe" set "PY=%ProgramFiles%\Python311\python.exe"
if not defined PY if exist "%ProgramFiles%\Python312\python.exe" set "PY=%ProgramFiles%\Python312\python.exe"

if not defined PY (
    where py >nul 2>nul
    if %errorlevel% equ 0 set "PY=py"
)

if not defined PY (
    where python >nul 2>nul
    if %errorlevel% equ 0 set "PY=python"
)

if not defined PY goto NO_PYTHON

echo [1/2] Moi truong Python: %PY%
echo [2/2] Dang khoi dong may chu ket noi WiFi...
echo.

set "PYTHONIOENCODING=utf-8"
set "PYTHONUNBUFFERED=1"
"%PY%" -u "%~dp0server_mobile.py"
goto FINISH

:NO_PYTHON
echo ======================================================================
echo [CANH BAO] Khong tim thay Python tren may tinh!
echo Dang mo truc tiep mo phong bang trinh duyet...
echo ======================================================================
start "" "%~dp0simulator.html"

:FINISH
echo.
echo ======================================================================
echo Cua so may chu da dung. Nhan phim bat ky de thoat...
echo ======================================================================
pause >nul
