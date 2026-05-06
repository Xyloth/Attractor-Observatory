"""Parse ``atlas/negative_space/*.md`` entries.

The negative-space registry catalogs honest absences — things the project
expected to find but didn't, calibration gaps, falsified directions.
Like the methods/falsifiers adapter, this returns a flat index suitable
for the Falsifier Ledger and Negative-Space rooms.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def parse_negative_space(
    negative_space_dir: str | Path = "atlas/negative_space",
) -> dict[str, Any]:
    """Index the negative-space markdown registry."""
    nd = Path(negative_space_dir)
    if not nd.exists():
        return {
            "status": "missing",
            "data": None,
            "rationale": f"negative_space dir not found at {nd.as_posix()}",
        }
    if not nd.is_dir():
        return {
            "status": "malformed",
            "data": None,
            "rationale": f"{nd.as_posix()} is not a directory",
        }
    entries: list[dict[str, Any]] = []
    for path in sorted(nd.glob("*.md")):
        try:
            head = ""
            with path.open("r", encoding="utf-8") as fh:
                for line in fh:
                    if line.lstrip().startswith("#"):
                        head = line.lstrip("#").strip()
                        break
                    if line.strip():
                        head = line.strip()
                        break
            stat = path.stat()
        except (OSError, UnicodeDecodeError):
            head = ""
            stat = None
        entries.append({
            "path": path.as_posix(),
            "name": path.name,
            "first_heading": head,
            "mtime": stat.st_mtime if stat else None,
            "size_bytes": stat.st_size if stat else None,
        })
    return {
        "status": "ok",
        "data": {
            "negative_space_dir": nd.as_posix(),
            "entry_count": len(entries),
            "entries": entries,
        },
        "rationale": f"indexed {len(entries)} negative-space entries from {nd.as_posix()}",
    }
