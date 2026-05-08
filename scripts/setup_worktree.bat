@echo off
REM ===========================================================================
REM CB-013 T1 — setup_worktree.bat
REM
REM Copies private (git-ignored) modules from the main checkout into a
REM newly-created git worktree so the daemon and the Control Room
REM can import them. The .gitignore implementation-module list keeps
REM these directories private to each working copy; fresh worktrees
REM miss them and FIRE crashes with ModuleNotFoundError.
REM
REM Usage from a fresh worktree:
REM   scripts\setup_worktree.bat
REM   scripts\setup_worktree.bat C:\Attractor Observatory      (override main)
REM
REM Default source: the parent of the worktree's parent dir,
REM resolved to "C:\Attractor Observatory" assuming the canonical
REM layout under "C:\Attractor Observatory DX Worktrees\<name>\".
REM ===========================================================================

setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "WORKTREE_ROOT=%SCRIPT_DIR%.."
pushd "%WORKTREE_ROOT%" >nul
set "WORKTREE_ROOT=%CD%"
popd >nul

if "%~1"=="" (
    REM Auto-detect main: walk up until we find a directory with formalism/.
    set "CANDIDATE=C:\Attractor Observatory"
    if not exist "!CANDIDATE!\formalism" (
        echo [setup_worktree] ERROR: cannot auto-locate main checkout.
        echo                  Pass it explicitly: scripts\setup_worktree.bat ^<path-to-main^>
        exit /b 2
    )
    set "MAIN_REPO=!CANDIDATE!"
) else (
    set "MAIN_REPO=%~1"
)

if not exist "%MAIN_REPO%\formalism" (
    echo [setup_worktree] ERROR: %MAIN_REPO%\formalism not found.
    echo                  Source path is not a valid Attractor Observatory checkout.
    exit /b 2
)

echo [setup_worktree] worktree: %WORKTREE_ROOT%
echo [setup_worktree] main:     %MAIN_REPO%

REM Modules to copy. These are listed in .gitignore so each worktree
REM has its own copy. Adding a new gitignored module the daemon
REM imports? Append it here AND audit factory_lowlevel/*.py for the
REM import line (see SETUP_WORKTREE.md).
for %%D in (worlds motifs validation nulls core trace formalism biology search ops experiments evidence tests) do (
    if exist "%MAIN_REPO%\%%D" (
        if exist "%WORKTREE_ROOT%\%%D" (
            echo [setup_worktree] %%D already present — skipping
        ) else (
            echo [setup_worktree] copying %%D ...
            xcopy /E /I /Y /Q "%MAIN_REPO%\%%D" "%WORKTREE_ROOT%\%%D" >nul
            if errorlevel 1 (
                echo [setup_worktree] ERROR: copy of %%D failed
                exit /b 3
            )
        )
    ) else (
        echo [setup_worktree] WARNING: %MAIN_REPO%\%%D not found; skipping
    )
)

echo [setup_worktree] done. Verify with: python -c "import formalism, worlds, trace; print('ok')"
exit /b 0
