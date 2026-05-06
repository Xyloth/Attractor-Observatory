"""Parse git metadata: current branch, last commit, recent commits.

The adapter shells out to ``git`` via ``subprocess``. If git is not
available or the repo is not a git checkout, it degrades to
``status: missing`` rather than raising.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any


def parse_git_metadata(repo_dir: str | Path = ".") -> dict[str, Any]:
    """Return the active branch, last commit, and recent log."""
    rd = Path(repo_dir)
    if not (rd / ".git").exists() and not _is_worktree(rd):
        return {
            "status": "missing",
            "data": None,
            "rationale": f"{rd.as_posix()} does not look like a git checkout",
        }
    if shutil.which("git") is None:
        return {
            "status": "missing",
            "data": None,
            "rationale": "git executable not on PATH",
        }
    branch = _git(rd, ["rev-parse", "--abbrev-ref", "HEAD"]) or "(detached)"
    last_commit_full = _git(rd, ["log", "-1", "--pretty=format:%H%n%h%n%an%n%ae%n%ai%n%s"])
    if last_commit_full is None:
        return {
            "status": "malformed",
            "data": None,
            "rationale": f"git log -1 failed in {rd.as_posix()}",
        }
    parts = last_commit_full.split("\n", 5)
    commit = {
        "hash": parts[0] if len(parts) > 0 else "",
        "short": parts[1] if len(parts) > 1 else "",
        "author_name": parts[2] if len(parts) > 2 else "",
        "author_email": parts[3] if len(parts) > 3 else "",
        "iso_date": parts[4] if len(parts) > 4 else "",
        "subject": parts[5] if len(parts) > 5 else "",
    }
    recent_log = _git(rd, ["log", "-10", "--pretty=format:%h\t%ai\t%an\t%s"]) or ""
    recent: list[dict[str, str]] = []
    for line in recent_log.splitlines():
        cells = line.split("\t", 3)
        if len(cells) == 4:
            recent.append({
                "short": cells[0],
                "iso_date": cells[1],
                "author_name": cells[2],
                "subject": cells[3],
            })
    return {
        "status": "ok",
        "data": {
            "repo_dir": rd.as_posix(),
            "branch": branch,
            "last_commit": commit,
            "recent_commits": recent,
            "recent_commit_count": len(recent),
        },
        "rationale": (
            f"branch={branch}, last_commit={commit['short']}, "
            f"recent_log_count={len(recent)}"
        ),
    }


def _is_worktree(rd: Path) -> bool:
    """Worktrees have a `.git` *file* (pointer), not a directory."""
    git_path = rd / ".git"
    return git_path.is_file()


def _git(repo: Path, args: list[str]) -> str | None:
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=str(repo),
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.rstrip("\n")
