@echo off
setlocal
cd /d "%~dp0"
"%~dp0runtime\python.exe" -I -B "%~dp0launcher.py" %*
if errorlevel 1 pause
