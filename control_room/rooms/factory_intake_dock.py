"""Factory Intake Dock - real monitor state when Campaign 016 has run.

D22 still applies: if no monitor state exists, the room renders an honest empty
state rather than stocked mock data.
"""

from __future__ import annotations

import json
from pathlib import Path

from control_room.rooms._placeholder import render_placeholder_room

ROOM_ID = "factory_intake_dock"
ROOM_NAME = "Factory Intake Dock"
ROOM_ICON = ">>"
ROOM_TAGLINE = "Autonomous Factory monitor - source-bound, zero-AI routine ingest."
ROOM_PHASE = "Phase 2"
STATE_PATH = Path("reports/campaign_016/factory_intake_dock_state.json")


def render() -> None:
    if not STATE_PATH.exists():
        render_placeholder_room(
            room_name=ROOM_NAME,
            room_icon=ROOM_ICON,
            tagline="Empty by design - no Campaign 016 Factory state has been generated yet.",
            phase=ROOM_PHASE,
            planned_artifacts=[
                "low-level source cache counts",
                "EmpiricalRecord counts",
                "NormalizedReference counts",
                "EvidenceGraph edge counts",
                "audit queue",
                "detector coverage summary",
            ],
            expected_phase_ticket="Run `python make_campaign_016.py` to populate the dock with real monitor state.",
        )
        return

    import streamlit as st  # local import keeps non-UI tests stdlib-only

    state = json.loads(STATE_PATH.read_text(encoding="utf-8-sig"))
    st.markdown(f"# {ROOM_ICON} {ROOM_NAME}")
    st.caption(ROOM_TAGLINE)
    st.json(
        {
            "status": state.get("status"),
            "updated_at": state.get("updated_at"),
            "routine_ingest_ai_runtime_required": state.get("routine_ingest_ai_runtime_required"),
            "claim_bearing_promotions": state.get("claim_bearing_promotions"),
            "density_classes": state.get("density_classes"),
            "store_counts": state.get("store_counts"),
            "audit_queue_count": state.get("audit_queue_count"),
            "detector_summary": state.get("detector_summary"),
        },
        expanded=False,
    )
