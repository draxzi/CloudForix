@echo off
:: Cloud Forix — Pipeline Launcher
:: Uses the full Python installation (Python 3.12) that has all dependencies.
:: This avoids the Windows Store python.exe stub which has no packages.

set PYTHON_EXE=C:\Users\student\AppData\Local\Programs\Python\Python312\python.exe

echo [*] Python executable: %PYTHON_EXE%
"%PYTHON_EXE%" --version
echo [*] Starting Cloud Forix pipeline...
"%PYTHON_EXE%" main.py
