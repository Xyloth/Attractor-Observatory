"""Parse the pytest cache directory if present.

The pytest cache (``.pytest_cache/``) carries lastfailed, nodeids, and
v/cache/ metadata. We extract the lastfailed list and a count of
known nodeids; this is enough for the Pulse Deck to surface "tests
that failed last run." Absent cache → ``status: missing``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def parse_pytest_cache(
    cache_dir: str | Path = ".pytest_cache",
) -> dict[str, Any]:
    """Return a structured snapshot of the pytest cache."""
    cd = Path(cache_dir)
    if not cd.exists():
        return {
            "status": "missing",
            "data": None,
            "rationale": f"pytest cache not found at {cd.as_posix()}",
        }
    if not cd.is_dir():
        return {
            "status": "malformed",
            "data": None,
            "rationale": f"{cd.as_posix()} is not a directory",
        }
    lastfailed_path = cd / "v" / "cache" / "lastfailed"
    nodeids_path = cd / "v" / "cache" / "nodeids"
    last_failed: dict[str, bool] = {}
    last_failed_count = 0
    if lastfailed_path.exists():
        try:
            payload = json.loads(lastfailed_path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                last_failed = payload
                last_failed_count = sum(1 for v in payload.values() if v)
        except (OSError, json.JSONDecodeError):
            last_failed = {}
            last_failed_count = -1
    nodeid_count: int | None = None
    if nodeids_path.exists():
        try:
            payload = json.loads(nodeids_path.read_text(encoding="utf-8"))
            if isinstance(payload, list):
                nodeid_count = len(payload)
        except (OSError, json.JSONDecodeError):
            nodeid_count = None
    return {
        "status": "ok",
        "data": {
            "cache_dir": cd.as_posix(),
            "lastfailed_path": lastfailed_path.as_posix(),
            "lastfailed_present": lastfailed_path.exists(),
            "last_failed_count": last_failed_count,
            "last_failed": last_failed,
            "nodeid_path": nodeids_path.as_posix(),
            "nodeid_count": nodeid_count,
        },
        "rationale": (
            f"pytest cache present at {cd.as_posix()}; "
            f"last_failed_count={last_failed_count}, "
            f"nodeid_count={nodeid_count}"
        ),
    }
