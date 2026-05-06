@echo off
REM Attractor Observatory - Control Room Launcher (CB-007 hardened)
REM Double-click to start the Control Room as a native desktop window.
REM
REM Optional flags:
REM   /quiet     - run without console window via pythonw (silent mode)
REM   /no-window - skip native window; start Streamlit only (browser path)
REM   /port=N    - use port N instead of the default 8765
REM   /port-kill - opt in to killing a process that already holds the port

cd /d "%~dp0"
set PYTHONPATH=%~dp0;%PYTHONPATH%

REM Parse the optional /quiet flag — runs via pythonw (no console window)
set "INVOCATION=python"
if /I "%1"=="/quiet" (
    set "INVOCATION=pythonw"
    shift
)

if /I "%INVOCATION%"=="pythonw" goto :quiet_path

echo.
echo ===========================================
echo  Attractor Observatory Control Room
echo ===========================================
echo.
echo Starting native window. Close the window to exit.
echo.

%INVOCATION% -m control_room.launcher %*

REM If the launcher exits non-zero, surface the error so the user can read it.
if errorlevel 1 (
    echo.
    echo Launcher exited with an error. Press any key to close.
    pause >nul
)
goto :eof

:quiet_path
REM Silent mode: no console output. Suppress any error popup; user must check
REM Task Manager / browser if it doesn't appear.
start "" %INVOCATION% -m control_room.launcher %*
goto :eof
