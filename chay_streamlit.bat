@echo off
setlocal
chcp 65001 >nul
title COLREGS-3D - MAY CHU STREAMLIT (MOBILE VA PC)
cls

cd /d "%~dp0"

echo ======================================================================
echo    KHOI CHAY MO PHONG COLREGS-3D QUA STREAMLIT
echo    (Cho phep ket noi tu ca May tinh va Dien thoai qua WiFi)
echo ======================================================================
echo.

set "PY="
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PY if exist "C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe" set "PY=C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe"
if not defined PY if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
if not defined PY if exist "C:\Users\ASUS\AppData\Local\Programs\Python\Python310\python.exe" set "PY=C:\Users\ASUS\AppData\Local\Programs\Python\Python310\python.exe"

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
echo Dang khoi chay Streamlit server...
echo Sau khi server chay, hay xem dong "Network URL" de mo tren dien thoai!
echo.

"%PY%" -m streamlit run app.py
if %errorlevel% neq 0 goto ERROR_RUN
goto FINISH

:NO_PYTHON
echo [LOI] Khong tim thay Python!
start "" "%~dp0simulator.html"
goto FINISH

:ERROR_RUN
echo.
echo Khong khoi chay duoc Streamlit qua lenh truc tiep.
echo Dang mo tep simulator.html bang trinh duyet...
start "" "%~dp0simulator.html"

:FINISH
echo.
echo Nhan phim bat ky de thoat...
pause >nul
