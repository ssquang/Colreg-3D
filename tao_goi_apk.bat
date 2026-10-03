@echo off
setlocal
chcp 65001 >nul
title COLREGS-3D - DONG GOI BO CAI APK CHO ANDROID
cls

cd /d "%~dp0"

echo ======================================================================
echo       COLREGS-3D - TAO ICON VA GOI DONG GOI APK CHO ANDROID
echo ======================================================================
echo.

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

echo [1/2] Dang tao bo icon va goi ung dung...
set "PYTHONIOENCODING=utf-8"
set "PYTHONUNBUFFERED=1"
if defined PY "%PY%" -u "%~dp0tao_icon_va_goi_apk.py"

if not exist "%~dp0COLREGS_3D_Mobile_Package.zip" goto COMPRESS_PS
goto CHECK_RESULT

:COMPRESS_PS
echo [Thong bao] Dang nen tep bang PowerShell Windows...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path '%~dp0simulator.html', '%~dp0manifest.json', '%~dp0sw.js', '%~dp0js', '%~dp0icons' -DestinationPath '%~dp0COLREGS_3D_Mobile_Package.zip' -Force"

:CHECK_RESULT
echo.
if not exist "%~dp0COLREGS_3D_Mobile_Package.zip" goto FAILED

echo ======================================================================
echo  [THANH CONG] DA TAO XONG GOI DONG GOI APK CHO DIEN THOAI!
echo ======================================================================
echo.
echo  Tep da duoc tao tai:
echo  COLREGS_3D_Mobile_Package.zip
echo.
echo ----------------------------------------------------------------------
echo  HUONG DAN 3 BUOC DE LAY FILE .APK CAI VAO DIEN THOAI:
echo ----------------------------------------------------------------------
echo  1. Mo trinh duyet web va truy cap: https://www.webintoapp.com
echo  2. Chon muc "HTML / All Files" (Website to App).
echo     Bam [Upload] va chon tep "COLREGS_3D_Mobile_Package.zip".
echo     Dat ten App: COLREGS 3D
echo  3. Bam nut [MAKE APP] (Tao ung dung).
echo     Sau 30 giay, bam [Download APK] hoac dung dien thoai quet ma QR
echo     de tai file APK truc tiep ve may Android va cai dat!
echo ======================================================================
goto FINISH

:FAILED
echo ======================================================================
echo  [LOI] Chua the tao tep nen tu dong.
echo ======================================================================

:FINISH
echo.
echo Nhan phim bat ky de dong cua so nay...
pause >nul
