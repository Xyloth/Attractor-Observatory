"""Factory Intake Dock monitor state for Control Room Room 9."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .persistence import write_json
from .schemas import sha256, utc_now


def build_monitor_state(
    *,
    store_snapshot: dict[str, Any],
    densification_reports: list[dict[str, Any]],
    detector_coverage: dict[str, Any],
    source_registry: dict[str, Any],
    audit_queue_count: int,
    out_path: str | Path = "reports/campaign_016/factory_intake_dock_state.json",
) -> dict[str, Any]:
    state = {
        "schema": "FactoryIntakeDockState.v1",
        "room_id": "factory_intake_dock",
        "updated_at": utc_now(),
        "status": "active",
        "routine_ingest_ai_runtime_required": False,
        "mode_tag": "exploratory",
        "claim_bearing_promotions": 0,
        "density_classes": {
            report["world_family"]: report["density_class"] for report in densification_reports
        },
        "store_counts": store_snapshot["counts"],
        "source_count": source_registry["validation"]["source_count"],
        "audit_queue_count": audit_queue_count,
        "detector_summary": detector_coverage["summary"],
        "empty_state_honesty": {
            "applies": False,
            "message": "Campaign 016 has ingested low-level source records; counts above are measured from persistence.",
        },
    }
    state["content_hash"] = sha256({key: value for key, value in state.items() if key != "content_hash"})
    return write_json(out_path, state)
