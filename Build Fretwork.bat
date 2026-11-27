@echo off
title Building Fretwork
cd /d "%~dp0"

set PY=
where py >nul 2>nul && set PY=py
if not defined PY where python >nul 2>nul && set PY=python
if not defined PY (
  echo Python is not installed.
  echo Install it from https://www.python.org/downloads/ ^(tick "Add python.exe to PATH"^), then run this again.
  pause
  exit /b 1
)

echo Installing the parts Fretwork needs...
%PY% -m pip install --upgrade pywebview pyinstaller || goto fail

echo Building Fretwork.exe...
%PY% -m PyInstaller --noconfirm --onefile --windowed --name Fretwork --add-data "fretwork.html;." fretwork_app.py || goto fail

copy /y "dist\Fretwork.exe" "Fretwork.exe" >nul
rmdir /s /q build >nul 2>nul
rmdir /s /q dist >nul 2>nul
del /q Fretwork.spec >nul 2>nul

echo.
echo Done. Fretwork.exe is in this folder. Double-click it to start,
echo or right-click it and choose "Pin to Start" / "Pin to taskbar".
pause
exit /b 0

:fail
echo.
echo Something went wrong. Copy the messages above and send them to Claude.
pause
exit /b 1
