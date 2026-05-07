@echo off
REM ===========================================================================
REM factory_daemon.bat — Windows entry point for the continuous Factory daemon.
REM
REM CB-013 T1: fail-fast check for required runtime modules.
REM Without formalism/, worlds/, or trace/ on disk, the daemon's import
REM chain crashes with ModuleNotFoundError. Surface that BEFORE starting
REM the daemon process so the operator knows to run setup_worktree.bat.
REM ===========================================================================

setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%"
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

REM Required runtime modules (gitignored — copied per worktree).
set "MISSING="
for %%D in (formalism worlds trace) do (
    if not exist "%REPO_ROOT%\%%D\__init__.py" (
        if not exist "%REPO_ROOT%\%%D" (
            set "MISSING=!MISSING! %%D"
        ) else (
            REM dir exists but no __init__.py — possibly partial copy
            set "MISSING=!MISSING! %%D[partial]"
        )
    )
)

if not "%MISSING%"=="" (
    echo.
    echo [factory_daemon] ERROR: required runtime modules missing: !MISSING!
    echo.
    echo                  These modules are gitignored. Run setup before launching:
    echo.
    echo                    scripts\setup_worktree.bat
    echo.
    echo                  Or copy from the main checkout manually:
    echo                    xcopy /E /I "C:\Attractor Observatory\formalism" formalism
    echo                    xcopy /E /I "C:\Attractor Observatory\worlds" worlds
    echo                    xcopy /E /I "C:\Attractor Observatory\trace" trace
    echo.
    echo                  See scripts\SETUP_WORKTREE.md for full instructions.
    echo.
    exit /b 4
)

python -m factory_lowlevel.continuous_daemon %*
