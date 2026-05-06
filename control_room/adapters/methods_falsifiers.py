"""Parse ``papers/methods/*.md`` and ``papers/falsifiers/*.md`` index entries.

We do not parse the markdown body in detail — that's reserved for the
Phase 1 methods/falsifier rooms. The adapter returns a flat index of
present documents with their first heading and modification mtime so
the Pulse Deck and Falsifier Ledger rooms can render counts and
activity without re-walking the filesystem.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def parse_methods_falsifiers(
    methods_dir: str | Path = "papers/methods",
    falsifiers_dir: str | Path = "papers/falsifiers",
) -> dict[str, Any]:
    """Index methods + falsifier markdown documents."""
    md = Path(methods_dir)
    fd = Path(falsifiers_dir)
    methods_present = md.exists() and md.is_dir()
    falsifiers_present = fd.exists() and fd.is_dir()
    if not methods_present and not falsifiers_present:
        return {
            "status": "missing",
            "data": None,
            "rationale": (
                f"neither methods dir ({md.as_posix()}) nor falsifiers dir "
                f"({fd.as_posix()}) is present"
            ),
        }
    methods = _index(md) if methods_present else []
    falsifiers = _index(fd) if falsifiers_present else []
    return {
        "status": "ok",
        "data": {
            "methods_dir": md.as_posix(),
            "methods_dir_present": methods_present,
            "method_doc_count": len(methods),
            "method_docs": methods,
            "falsifiers_dir": fd.as_posix(),
            "falsifiers_dir_present": falsifiers_present,
            "falsifier_doc_count": len(falsifiers),
            "falsifier_docs": falsifiers,
        },
        "rationale": (
            f"indexed {len(methods)} methods, {len(falsifiers)} falsifiers"
            + ("" if methods_present else " (methods dir absent)")
            + ("" if falsifiers_present else " (falsifiers dir absent)")
        ),
    }


def _index(directory: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.md")):
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
            mtime = path.stat().st_mtime
            size = path.stat().st_size
        except (OSError, UnicodeDecodeError):
            head = ""
            mtime = None
            size = None
        rows.append({
            "path": path.as_posix(),
            "name": path.name,
            "first_heading": head,
            "mtime": mtime,
            "size_bytes": size,
        })
    return rows
