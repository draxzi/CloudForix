@echo off
:: Cloud Forix — Launcher
:: Uses the full Python 3.12 installation to avoid Windows Store python.exe stub.

set PYTHON_EXE=C:\Users\student\AppData\Local\Programs\Python\Python312\python.exe

echo.
echo  ====================================
echo    CLOUD FORIX — Launch Options
echo  ====================================
echo   1. GUI Mode (Tkinter)
echo   2. CLI Mode (Terminal pipeline)
echo   3. Exit
echo  ====================================
echo.
set /p CHOICE="  Select [1/2/3]: "

if "%CHOICE%"=="1" goto GUI
if "%CHOICE%"=="2" goto CLI
if "%CHOICE%"=="3" goto END

:GUI
echo.
echo [*] Launching Cloud Forix GUI...
echo [*] Python: %PYTHON_EXE%
"%PYTHON_EXE%" gui.py
goto END

:CLI
echo.
echo [*] Starting Cloud Forix CLI pipeline...
echo [*] Python: %PYTHON_EXE%
"%PYTHON_EXE%" main.py
goto END

:END
