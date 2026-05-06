"""Parse ``reports/campaign_*/`` JSON outputs gracefully across schema variation.

Each campaign directory may carry many files; we focus on
``full_report.json`` (canonical per the project's reproducibility scripts)
and degrade gracefully if it is missing for any campaign. The adapter
does not assume schema fields beyond ``status``, ``gates``, ``gate_count``,
``passed_gate_count`` — anything else is passed through verbatim.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def parse_campaign_reports(reports_dir: str | Path = "reports") -> dict[str, Any]:
    """Walk ``reports/campaign_*/full_report.json`` files and summarize each."""
    rd = Path(reports_dir)
    if not rd.exists():
        return {
            "status": "missing",
            "data": None,
            "rationale": f"reports directory not found at {rd.as_posix()}",
        }
    if not rd.is_dir():
        return {
            "status": "malformed",
            "data": None,
            "rationale": f"{rd.as_posix()} is not a directory",
        }
    campaigns: list[dict[str, Any]] = []
    for campaign_dir in sorted(rd.glob("campaign_*")):
        if not campaign_dir.is_dir():
            continue
        full_report = campaign_dir / "full_report.json"
        record: dict[str, Any] = {
            "campaign_id": campaign_dir.name,
            "report_path": full_report.as_posix(),
            "report_present": full_report.exists(),
            "status": None,
            "gate_count": None,
            "passed_gate_count": None,
            "schema": None,
            "artifacts": None,
        }
        if full_report.exists():
            try:
                payload = json.loads(full_report.read_text(encoding="utf-8"))
                record["status"] = payload.get("status")
                record["gate_count"] = payload.get("gate_count")
                record["passed_gate_count"] = payload.get("passed_gate_count")
                record["schema"] = payload.get("schema")
                record["artifacts"] = payload.get("artifacts")
                record["raw_top_level_keys"] = sorted(payload.keys()) if isinstance(payload, dict) else []
            except json.JSONDecodeError as exc:
                record["status"] = "malformed_json"
                record["error"] = repr(exc)
        campaigns.append(record)
    if not campaigns:
        return {
            "status": "missing",
            "data": None,
            "rationale": f"no campaign_* subdirectories found under {rd.as_posix()}",
        }
    green = [c for c in campaigns if c.get("status") == "green"]
    return {
        "status": "ok",
        "data": {
            "reports_dir": rd.as_posix(),
            "campaign_count": len(campaigns),
            "green_count": len(green),
            "campaigns": campaigns,
        },
        "rationale": (
            f"surveyed {len(campaigns)} campaign directories; "
            f"{len(green)} green; "
            f"{sum(1 for c in campaigns if not c['report_present'])} missing full_report.json"
        ),
    }
