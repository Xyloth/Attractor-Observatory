#!/usr/bin/env bash
# ============================================================================
# CB-013 T1 — setup_worktree.sh
#
# POSIX equivalent of setup_worktree.bat. Copies private (git-ignored)
# modules from the main checkout into a newly-created git worktree so
# the daemon and the Control Room can import them.
#
# Usage from a fresh worktree:
#   scripts/setup_worktree.sh
#   scripts/setup_worktree.sh /path/to/main      (override main)
#
# Default source: ``C:/Attractor Observatory`` assuming the canonical
# DX-worktree layout. POSIX users override via the explicit path arg.
# ============================================================================

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
worktree_root="$(cd "${script_dir}/.." && pwd)"

if [ "$#" -ge 1 ]; then
    main_repo="$1"
else
    candidate="C:/Attractor Observatory"
    if [ -d "${candidate}/formalism" ]; then
        main_repo="${candidate}"
    else
        echo "[setup_worktree] ERROR: cannot auto-locate main checkout." >&2
        echo "                 Pass it explicitly: scripts/setup_worktree.sh <path-to-main>" >&2
        exit 2
    fi
fi

if [ ! -d "${main_repo}/formalism" ]; then
    echo "[setup_worktree] ERROR: ${main_repo}/formalism not found." >&2
    echo "                 Source path is not a valid Attractor Observatory checkout." >&2
    exit 2
fi

echo "[setup_worktree] worktree: ${worktree_root}"
echo "[setup_worktree] main:     ${main_repo}"

# Modules to copy. Listed in .gitignore so each worktree has its own.
# Append new gitignored modules the daemon imports here AND audit
# factory_lowlevel/*.py for the import line (see SETUP_WORKTREE.md).
modules=(formalism worlds trace)

for d in "${modules[@]}"; do
    src="${main_repo}/${d}"
    dst="${worktree_root}/${d}"
    if [ ! -d "${src}" ]; then
        echo "[setup_worktree] WARNING: ${src} not found; skipping"
        continue
    fi
    if [ -d "${dst}" ]; then
        echo "[setup_worktree] ${d} already present — skipping"
        continue
    fi
    echo "[setup_worktree] copying ${d} ..."
    cp -r "${src}" "${dst}"
done

echo "[setup_worktree] done. Verify with: python -c \"import formalism, worlds, trace; print('ok')\""
