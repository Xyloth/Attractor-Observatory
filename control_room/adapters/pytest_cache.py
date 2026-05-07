"""Parse the pytest cache directory if present.

The pytest cache (``.pytest_cache/``) carries lastfailed, nodeids, and
v/cache/ metadata. We extract the lastfailed list and a count of
known nodeids; this is enough for the Pulse Deck to surface "tests
that failed last run." Absent cache → ``status: missing``.

CB-011 fix #2 — Stale cache detection.
James reported the dashboard saying "4 pytest failed last run" while
those failures were days old. The cache file's mtime now drives a
``stale_cache`` flag that consumers (Pulse Deck Needs Attention lane)
use to flag the count as STALE rather than displaying it as live
state. D17 binding: stale data flagged as stale, never silently
treated as live.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


# Cache stale after this many seconds. 6 hours is the default; a fresh
# pre-commit run will refresh, but a cache untouched for half a day
# probably reflects yesterday's failures, not today's state.
DEFAULT_STALE_THRESHOLD_SECONDS = 6 * 3600


def parse_pytest_cache(
    cache_dir: str | Path = ".pytest_cache",
    *,
    stale_threshold_seconds: int = DEFAULT_STALE_THRESHOLD_SECONDS,
) -> dict[str, Any]:
    """Return a structured snapshot of the pytest cache.

    Adds two CB-011 fields to ``data``:
      * ``lastfailed_age_seconds`` — seconds since the lastfailed file's
        mtime. ``None`` when the file is missing.
      * ``stale_cache`` — True iff the lastfailed file is older than
        ``stale_threshold_seconds``. Consumers MUST flag the count as
        STALE rather than displaying it as live state (D17).
    """
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
    lastfailed_age: float | None = None
    stale_cache = False
    if lastfailed_path.exists():
        try:
            payload = json.loads(lastfailed_path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                last_failed = payload
                last_failed_count = sum(1 for v in payload.values() if v)
        except (OSError, json.JSONDecodeError):
            last_failed = {}
            last_failed_count = -1
        try:
            lastfailed_age = time.time() - lastfailed_path.stat().st_mtime
            stale_cache = lastfailed_age > stale_threshold_seconds
        except OSError:
            lastfailed_age = None
            stale_cache = False
    nodeid_count: int | None = None
    coverage_status = "nodeids_missing"
    if nodeids_path.exists():
        try:
            payload = json.loads(nodeids_path.read_text(encoding="utf-8"))
            if isinstance(payload, list):
                nodeid_count = len(payload)
                coverage_status = "zero_coverage" if nodeid_count == 0 else "has_nodeids"
        except (OSError, json.JSONDecodeError):
            nodeid_count = None
            coverage_status = "malformed_nodeids"
    return {
        "status": "ok",
        "data": {
            "cache_dir": cd.as_posix(),
            "lastfailed_path": lastfailed_path.as_posix(),
            "lastfailed_present": lastfailed_path.exists(),
            "lastfailed_age_seconds": (
                round(lastfailed_age, 1) if lastfailed_age is not None else None
            ),
            "stale_cache": stale_cache,
            "stale_threshold_seconds": stale_threshold_seconds,
            "last_failed_count": last_failed_count,
            "last_failed": last_failed,
            "nodeid_path": nodeids_path.as_posix(),
            "nodeid_count": nodeid_count,
            "coverage_status": coverage_status,
        },
        "rationale": (
            f"pytest cache present at {cd.as_posix()}; "
            f"last_failed_count={last_failed_count}, "
            f"nodeid_count={nodeid_count}"
            + (f"; STALE (age {int(lastfailed_age)}s > {stale_threshold_seconds}s)"
               if stale_cache else "")
        ),
    }
