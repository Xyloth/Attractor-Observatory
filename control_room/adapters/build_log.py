"""Parse ``BUILD_LOG.md`` into structured entries.

BUILD_LOG.md uses two entry types per the file's own preamble:
work entries (``[timestamp] [builder] [task_id] [pillar/sub-task]``)
and talk entries (``[timestamp] [from] -> [to]``). The convention is
informal; we extract date sections and `### [...]` headers, leaving
prose intact.

Status values: ``ok`` (file present and parsed), ``missing`` (file
not found), ``malformed`` (file present but unreadable).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


_DATE_HEADER_RE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$")
_ENTRY_HEADER_RE = re.compile(r"^###\s+(.+?)\s*$")


def parse_build_log(path: str | Path = "BUILD_LOG.md") -> dict[str, Any]:
    """Parse the project's BUILD_LOG.md into a structured payload."""
    p = Path(path)
    if not p.exists():
        return {
            "status": "missing",
            "data": None,
            "rationale": f"BUILD_LOG.md not found at {p.as_posix()}",
        }
    try:
        text = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return {
            "status": "malformed",
            "data": None,
            "rationale": f"Could not read {p.as_posix()}: {exc!r}",
        }
    sections: list[dict[str, Any]] = []
    current_date: str | None = None
    current_entry: dict[str, Any] | None = None
    body_lines: list[str] = []
    for raw in text.splitlines():
        date_match = _DATE_HEADER_RE.match(raw)
        if date_match:
            if current_entry is not None:
                current_entry["body"] = "\n".join(body_lines).strip()
                sections.append(current_entry)
                current_entry = None
                body_lines = []
            current_date = date_match.group(1)
            continue
        entry_match = _ENTRY_HEADER_RE.match(raw)
        if entry_match:
            if current_entry is not None:
                current_entry["body"] = "\n".join(body_lines).strip()
                sections.append(current_entry)
                body_lines = []
            current_entry = {
                "date": current_date,
                "header": entry_match.group(1).strip(),
                "kind": _classify_entry(entry_match.group(1)),
                "body": "",
            }
            continue
        if current_entry is not None:
            body_lines.append(raw)
    if current_entry is not None:
        current_entry["body"] = "\n".join(body_lines).strip()
        sections.append(current_entry)
    return {
        "status": "ok",
        "data": {
            "path": p.as_posix(),
            "entry_count": len(sections),
            "entries": sections,
            "most_recent": sections[-1] if sections else None,
        },
        "rationale": f"parsed {len(sections)} entries from {p.as_posix()}",
    }


def _classify_entry(header: str) -> str:
    lowered = header.lower()
    if "talk" in lowered:
        return "talk"
    if "work" in lowered or "start" in lowered or "complete" in lowered:
        return "work"
    if "audit" in lowered:
        return "audit"
    if "meta-audit" in lowered or "cross-builder" in lowered:
        return "architect"
    return "other"
