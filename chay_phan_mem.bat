@echo off
setlocal
chcp 65001 >nul
title COLREGS-3D - MO PHONG BUONG LAI HANG HAI
cls

cd /d "%~dp0"

echo ======================================================================
echo    DANG KHOI CHAY PHAN MEM COLREGS-3D (CUA SO DESKTOP DOC LAP)
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

echo Moi truong: %PY%
echo Dang mo cua so mo phong buong lai 3D...
echo.

set "PYTHONIOENCODING=utf-8"
"%PY%" run_app.py

if %errorlevel% neq 0 goto ERROR_RUN
goto FINISH

:NO_PYTHON
echo ======================================================================
echo [CANH BAO] Khong tim thay Python tren may tinh!
echo Dang mo truc tiep mo phong bang trinh duyet...
echo ======================================================================
start "" "%~dp0simulator.html"
goto FINISH

:ERROR_RUN
echo.
echo ======================================================================
echo [THONG BAO] Dang mo giao dien truc tiep bang trinh duyet...
echo ======================================================================
start "" "%~dp0simulator.html"

:FINISH
echo.
echo Nhap phim bat ky de thoat...
pause >nul
