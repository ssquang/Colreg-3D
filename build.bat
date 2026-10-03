@echo off
setlocal
chcp 65001 >nul
title COLREGS-3D - DONG GOI PHAN MEM EXE
cls

cd /d "%~dp0"

set "PY="
if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if not defined PY if exist "C:\Users\ASUS\AppData\Local\Programs\Python\Python310\python.exe" set "PY=C:\Users\ASUS\AppData\Local\Programs\Python\Python310\python.exe"
if not defined PY if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PY if exist "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe" set "PY=C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe"

if not defined PY (
    where py >nul 2>nul
    if %errorlevel% equ 0 set "PY=py"
)

if not defined PY (
    where python >nul 2>nul
    if %errorlevel% equ 0 set "PY=python"
)

if not defined PY goto NO_PYTHON

echo ======================================================================
echo    HE THONG DONG GOI PHAN MEM COLREGS-3D THANH FILE .EXE DOC LAP
echo ======================================================================
echo Su dung: %PY%
echo.
echo Dang tien hanh dong goi... Qua trinh nay se mat khoang 30 - 60 giay.
echo Vui long khong dong cua so nay cho toi khi hoan tat.
echo.

set "PYTHONIOENCODING=utf-8"
"%PY%" build_exe.py
goto FINISH

:NO_PYTHON
echo ======================================================================
echo [LOI] Khong tim thay Python tren may tinh!
echo ======================================================================

:FINISH
echo.
echo ======================================================================
pause
