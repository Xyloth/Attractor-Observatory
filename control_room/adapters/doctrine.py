"""Parse the doctrine registry, the consolidated ``DOCTRINE.md`` index,
and the per-rule ``doctrine_d*.md`` files into a structured payload."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


_DOCTRINE_HEADING_RE = re.compile(r"^##\s+(D\d+(?:\.\d+)?(?:[-–]\D\d+(?:\.\d+)?)?)(?:\s+Candidate)?\s*[—–-]\s*(.+?)\s*$")


def parse_doctrine(
    registry_path: str | Path = "docs/doctrine_registry.json",
    consolidated_path: str | Path = "docs/DOCTRINE.md",
    docs_dir: str | Path = "docs",
) -> dict[str, Any]:
    """Parse doctrine registry + consolidated index + per-rule docs."""
    rp = Path(registry_path)
    cp = Path(consolidated_path)
    dd = Path(docs_dir)
    if not rp.exists():
        return {
            "status": "missing",
            "data": None,
            "rationale": f"doctrine registry not found at {rp.as_posix()}",
        }
    try:
        registry = json.loads(rp.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "status": "malformed",
            "data": None,
            "rationale": f"Could not parse {rp.as_posix()}: {exc!r}",
        }
    consolidated_entries: list[dict[str, str]] = []
    if cp.exists():
        try:
            text = cp.read_text(encoding="utf-8")
            for line in text.splitlines():
                m = _DOCTRINE_HEADING_RE.match(line)
                if m:
                    consolidated_entries.append({
                        "id": m.group(1).strip(),
                        "heading": m.group(2).strip(),
                    })
        except (OSError, UnicodeDecodeError):
            consolidated_entries = []
    per_rule_files: list[dict[str, Any]] = []
    if dd.exists() and dd.is_dir():
        for child in sorted(dd.glob("doctrine_d*.md")):
            try:
                first_line = child.read_text(encoding="utf-8").splitlines()[:1]
                first = first_line[0] if first_line else ""
            except (OSError, UnicodeDecodeError):
                first = ""
            per_rule_files.append({
                "path": child.relative_to(dd.parent).as_posix() if dd.parent != Path(".") else child.as_posix(),
                "first_heading": first.lstrip("# ").strip(),
            })
    return {
        "status": "ok",
        "data": {
            "registry_path": rp.as_posix(),
            "registry_entry_count": len(registry.get("doctrines", [])),
            "registry": registry.get("doctrines", []),
            "consolidated_index_path": cp.as_posix() if cp.exists() else None,
            "consolidated_entry_count": len(consolidated_entries),
            "consolidated_entries": consolidated_entries,
            "per_rule_files": per_rule_files,
        },
        "rationale": (
            f"parsed {len(registry.get('doctrines', []))} registry rows; "
            f"{len(consolidated_entries)} consolidated headings; "
            f"{len(per_rule_files)} per-rule files"
        ),
    }


def parse_mistake_catalog(
    registry_path: str | Path = "docs/mistake_catalog_registry.json",
) -> dict[str, Any]:
    """Parse the canonical mistake-catalog registry.

    DX-003 found that README, Control Room, and initiation surfaces drifted
    because each carried its own frozen class list. This adapter is the single
    public reader for the canonical registry.
    """

    rp = Path(registry_path)
    if not rp.exists():
        return {
            "status": "missing",
            "data": None,
            "rationale": f"mistake catalog registry not found at {rp.as_posix()}",
        }
    try:
        registry = json.loads(rp.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "status": "malformed",
            "data": None,
            "rationale": f"Could not parse {rp.as_posix()}: {exc!r}",
        }
    classes = registry.get("classes", [])
    ratified = [c for c in classes if c.get("status") == "ratified"]
    candidates = [c for c in classes if c.get("status") == "candidate"]
    skipped = [c for c in classes if c.get("status") == "skipped"]
    return {
        "status": "ok",
        "data": {
            "registry_path": rp.as_posix(),
            "schema": registry.get("schema"),
            "class_count": len(classes),
            "ratified_count": len(ratified),
            "candidate_count": len(candidates),
            "skipped_count": len(skipped),
            "classes": classes,
        },
        "rationale": (
            f"parsed {len(classes)} mistake classes; "
            f"{len(ratified)} ratified; {len(candidates)} candidates; "
            f"{len(skipped)} skipped"
        ),
    }
