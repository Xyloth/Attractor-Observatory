"""Render structured Campaign 006 Atlas pages."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _write_page(path: Path, title: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", "", "Generated from structured Campaign 006 inputs.", ""]
    for row in rows:
        status = row.get("claim_status", row.get("status", "candidate"))
        mode = row.get("mode_tag", row.get("mode", "exploratory"))
        lines.append(f"- `{row.get('id', row.get('candidate_id', row.get('entry_id', row.get('world_id', 'artifact'))))}` mode={mode} status={status}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": str(path), "row_count": len(rows), "title": title}


def render_campaign006_atlas(reports: dict[str, Any], out_dir: str | Path = "atlas/status_viewer/generated/campaign_006") -> dict[str, Any]:
    root = Path(out_dir)
    pages = {}
    candidates = reports["candidate_audit"]["audits"]
    negative = reports["negative_space"]["entries"]
    beta_worlds = reports["beta_worlds"]["rows"]
    health_components = [
        {"id": name, "mode_tag": "foundational", "claim_status": "candidate", **row}
        for name, row in reports["health"]["components"].items()
    ]
    transfer_rows = reports["transfer"]["matrix"][:24]
    pages["candidates"] = _write_page(root / "candidates.md", "Campaign 006 Candidates", candidates)
    pages["negative_space"] = _write_page(root / "negative_space.md", "Campaign 006 Negative Space", negative)
    pages["worlds"] = _write_page(root / "worlds.md", "Campaign 006 Beta Worlds", beta_worlds)
    pages["health"] = _write_page(root / "health.md", "Campaign 006 Instrument Health", health_components)
    pages["transfer"] = _write_page(root / "transfer.md", "Campaign 006 Transfer Matrix", transfer_rows)

    queries = {
        "candidates_by_status": {},
        "open_negative_space_entries": [row["entry_id"] for row in negative if row["status"] == "open"],
        "evidence_by_world_family": {},
        "failed_perturbation_regimes": [row["id"] for row in reports["perturbation"]["failure_artifacts"][:12]],
        "blocked_from_claim_use": [row["candidate_id"] for row in candidates if row["promotion_status"] != "audited_candidate"],
        "external_review_packet": "reports/campaign_006/external_review_packet.json",
    }
    for candidate in candidates:
        queries["candidates_by_status"].setdefault(candidate["promotion_status"], []).append(candidate["candidate_id"])
    for row in beta_worlds:
        queries["evidence_by_world_family"].setdefault(row["world_family"], []).append(row["trace_id"])
    (root / "queries.json").write_text(json.dumps(queries, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    index = {"pages": pages, "queries": queries, "page_count": len(pages), "mode_tag_visible": True, "claim_status_visible": True}
    (root / "index.json").write_text(json.dumps(index, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return index
