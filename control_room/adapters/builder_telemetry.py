"""Parse ``project_telemetry/ai_builder_tasks.jsonl`` (Estimation Loop ledger).

Each line is one task record per the schema in
``CLAUDE_BUILDER_INITIATION.md`` (and Codex's parallel records). Some
records carry ``actual_minutes`` and ``estimation_delta``; some don't.
The adapter does not fill in missing fields — it returns whatever is
on disk.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def parse_builder_telemetry(
    path: str | Path = "project_telemetry/ai_builder_tasks.jsonl",
) -> dict[str, Any]:
    """Parse the AI builder tasks ledger into a structured payload."""
    p = Path(path)
    if not p.exists():
        return {
            "status": "missing",
            "data": None,
            "rationale": f"builder telemetry ledger not found at {p.as_posix()}",
        }
    try:
        raw = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return {
            "status": "malformed",
            "data": None,
            "rationale": f"Could not read {p.as_posix()}: {exc!r}",
        }
    records: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for line_no, line in enumerate(raw.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            record = json.loads(stripped)
        except json.JSONDecodeError as exc:
            skipped.append({"line_no": line_no, "error": str(exc)})
            continue
        if isinstance(record, dict):
            records.append(record)
    by_model = _group_by_model(records)
    if skipped and not records:
        return {
            "status": "malformed",
            "data": {"skipped": skipped},
            "rationale": (
                f"every JSONL record in {p.as_posix()} failed to parse "
                f"({len(skipped)} skipped)"
            ),
        }
    return {
        "status": "ok",
        "data": {
            "path": p.as_posix(),
            "record_count": len(records),
            "records": records,
            "skipped_lines": skipped,
            "by_model": by_model,
        },
        "rationale": (
            f"parsed {len(records)} records from {p.as_posix()}"
            + (f" ({len(skipped)} malformed lines skipped)" if skipped else "")
        ),
    }


def _group_by_model(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for r in records:
        model = str(r.get("model_name") or "unknown")
        grouped.setdefault(model, []).append(r)
    summary: dict[str, dict[str, Any]] = {}
    for model, model_records in grouped.items():
        deltas = [
            r.get("estimation_delta")
            for r in model_records
            if isinstance(r.get("estimation_delta"), (int, float))
        ]
        actuals = [
            r.get("actual_minutes")
            for r in model_records
            if isinstance(r.get("actual_minutes"), (int, float))
        ]
        summary[model] = {
            "task_count": len(model_records),
            "actual_minutes_count": len(actuals),
            "delta_count": len(deltas),
            "delta_mean": (sum(deltas) / len(deltas)) if deltas else None,
            "delta_min": min(deltas) if deltas else None,
            "delta_max": max(deltas) if deltas else None,
            "most_recent_task_id": model_records[-1].get("task_id"),
        }
    return summary
