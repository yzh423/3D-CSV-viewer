@echo off
setlocal
cd /d "%~dp0\..\.."
set "VENV_PY=.venv\Scripts\python.exe"

if not exist "%VENV_PY%" (
  echo [3D CSV Viewer] Creating isolated Python environment...
  python -m venv .venv
  if errorlevel 1 goto :error
)

"%VENV_PY%" -c "import PySide6, matplotlib, numpy" >nul 2>&1
if errorlevel 1 (
  echo [3D CSV Viewer] Installing required packages. This only happens on first launch...
  "%VENV_PY%" -m pip install -r requirements.txt
  if errorlevel 1 goto :error
)

"%VENV_PY%" scripts\episode_3d_desktop.py %*
if errorlevel 1 goto :error
exit /b 0

:error
echo.
echo [3D CSV Viewer] Startup failed. Check the message above.
pause
exit /b 1
