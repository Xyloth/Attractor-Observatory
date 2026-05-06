"""Basin-Floor Geometry Lab — proposal §7.6.

Surfaces the basin-floor candidate (`motif.floor_connectivity.draft`)
trail through Campaigns 010 (deficit map), 013 (replication), CB-001
through CB-003 (multisubstrate + adversarial + substrate-blocked
controls), and Campaign 010 deficit map history.

Per §7.6 of the proposal: the room MUST NOT fake mathematical precision.
If basin diagrams aren't measurable from on-disk artifacts, render
honest absence rather than synthesize plausible chart shapes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from control_room.adapters import parse_campaign_reports, parse_methods_falsifiers
from control_room.components import (
    metric_card,
    panel,
    render_empty_state,
    render_html,
    room_emblem,
    status_pill,
)


ROOM_ID = "basin_floor_lab"
ROOM_NAME = "Basin-Floor Geometry Lab"
ROOM_ICON = "🪐"
ROOM_TAGLINE = "Floors, perturbation outcomes, and substrate-blind signatures."
ROOM_PHASE = "Phase 1"


def render() -> None:
    import streamlit as st

    render_html(room_emblem(ROOM_NAME, ROOM_TAGLINE, ROOM_ID))

    deficit = _load_json("reports/campaign_010/formal_deficit_map.json")
    replication = _load_json("reports/campaign_013/replication_verdict.json")
    multisubstrate_v2 = _load_json("reports/campaign_013/multisubstrate_floor_connectivity_v2.json")
    adversarial = _load_json("reports/campaign_013/methodology_adversarial_control.json")
    substrate_blocked = _load_json("reports/campaign_013/substrate_blocked_control.json")

    # Top metrics
    cols = st.columns(4)
    with cols[0]:
        if replication:
            fg = replication.get("formal_gap", {}).get("formal_gap")
            value = f"{fg:.4f}" if fg is not None else "—"
            render_html(metric_card("formal_gap (C013)", value, "motif", "floor_connectivity"))
        else:
            render_empty_state(reason="C013 replication verdict missing", expected_artifact="reports/campaign_013/replication_verdict.json")
    with cols[1]:
        if replication:
            p = replication.get("n7", {}).get("empirical_p")
            value = f"{p:.4f}" if p is not None else "—"
            render_html(metric_card("N7 empirical p", value, "verified" if p and p < 0.05 else "warning", "N=1000 lens permutation"))
        else:
            render_html(metric_card("N7 empirical p", "—", "unavailable", "no replication record"))
    with cols[2]:
        if adversarial:
            verdict = adversarial.get("interpretation", {}).get("verdict", "?")
            render_html(metric_card(
                "adversarial control",
                verdict,
                "verified" if verdict == "methodology_sound" else "warning",
                "TASK-CB-003 MV4-MV5",
            ))
        else:
            render_empty_state(reason="adversarial control not run", expected_artifact="reports/campaign_013/methodology_adversarial_control.json")
    with cols[3]:
        if substrate_blocked:
            verdict = substrate_blocked.get("interpretation", {}).get("verdict", "?")
            ok = verdict in ("signal_survives_shuffle",)
            render_html(metric_card(
                "substrate-blocked",
                verdict,
                "verified" if ok else "warning",
                "TASK-CB-003 MV7-MV8",
            ))
        else:
            render_empty_state(reason="substrate-blocked control not run", expected_artifact="reports/campaign_013/substrate_blocked_control.json")

    # Replication trail
    st.markdown('<span class="cap">replication trail · floor_connectivity candidate</span>', unsafe_allow_html=True)
    if deficit and deficit.get("candidates"):
        history = []
        for cand in deficit["candidates"]:
            if cand.get("motif_id") == "motif.floor_connectivity.draft":
                history = cand.get("replication_history", [])
                break
        if history:
            rows_html = ""
            for h in history:
                cid = h.get("campaign_id", "?")
                verdict = h.get("verdict", h.get("adversarial_verdict") or h.get("substrate_blocked_verdict") or "?")
                fg = h.get("formal_gap")
                p = h.get("empirical_p")
                meta = []
                if fg is not None:
                    meta.append(f"gap={fg:.4f}" if isinstance(fg, (int, float)) else f"gap={fg}")
                if p is not None:
                    meta.append(f"p={p:.4f}" if isinstance(p, (int, float)) else f"p={p}")
                meta_str = " · ".join(meta) if meta else ""
                rows_html += (
                    '<div style="display:grid;grid-template-columns:160px 1fr 220px;align-items:center;'
                    'gap:10px;padding:6px 0;border-bottom:1px dashed var(--border);">'
                    f'<span style="font-family:var(--font-mono);font-size:var(--fs-label);color:var(--fg2);">{cid}</span>'
                    f'<span style="font-family:var(--font-mono);font-size:var(--fs-detail);color:var(--fg3);">{meta_str}</span>'
                    f'{status_pill(str(verdict), status="verified" if verdict in ("replicated", "methodology_sound") else "warning")}'
                    "</div>"
                )
            render_html(panel(f"{len(history)} replication / control entries", rows_html))
        else:
            render_empty_state(reason="formal_deficit_map has no replication_history for floor", expected_artifact="reports/campaign_010/formal_deficit_map.json with floor candidate replication_history")
    else:
        render_empty_state(reason="formal_deficit_map missing or empty", expected_artifact="reports/campaign_010/formal_deficit_map.json")

    # Multisubstrate v2 results (CB-002)
    st.markdown('<span class="cap">multisubstrate v2 · per-substrate scientific verdicts</span>', unsafe_allow_html=True)
    if multisubstrate_v2:
        substrate_results = multisubstrate_v2.get("substrate_results", {})
        rows_html = ""
        for name, payload in sorted(substrate_results.items()):
            sv = payload.get("scientific_verdict", "?")
            tv = payload.get("threshold_verdict", {}).get("verdict", "?")
            s0 = payload.get("step_0", {}).get("step_0_status", "?")
            rows_html += (
                '<div style="display:grid;grid-template-columns:140px 1fr 1fr 1fr;align-items:center;'
                'gap:10px;padding:6px 0;border-bottom:1px dashed var(--border);">'
                f'<span style="font-family:var(--font-mono);font-size:var(--fs-label);color:var(--fg2);">{name}</span>'
                f'<span class="cap mono" style="color:var(--fg4);">step0: {s0}</span>'
                f'<span class="cap mono" style="color:var(--fg4);">threshold: {tv}</span>'
                f'{status_pill(sv, status="warning" if "not_evaluable" in sv else "verified")}'
                "</div>"
            )
        render_html(panel(f"{len(substrate_results)} substrates evaluated", rows_html))
    else:
        render_empty_state(reason="multisubstrate v2 record missing", expected_artifact="reports/campaign_013/multisubstrate_floor_connectivity_v2.json")

    # Falsifier-active worlds
    st.markdown('<span class="cap">falsifier records · this room\'s scientific watch list</span>', unsafe_allow_html=True)
    falsifiers = parse_methods_falsifiers()
    if falsifiers["status"] == "ok" and falsifiers["data"]["falsifier_doc_count"] > 0:
        rows_html = ""
        for d in falsifiers["data"]["falsifier_docs"]:
            rows_html += (
                '<div style="display:flex;align-items:center;gap:10px;padding:5px 0;'
                'border-bottom:1px dashed var(--border);">'
                f'<span style="font-family:var(--font-mono);font-size:var(--fs-detail);color:var(--fg3);width:200px;">{d["name"]}</span>'
                f'<span style="font-family:var(--font-body);font-size:var(--fs-body);color:var(--fg2);flex:1;">{d.get("first_heading") or "—"}</span>'
                f'{status_pill("falsifier", status="failed")}'
                "</div>"
            )
        render_html(panel(f"{falsifiers['data']['falsifier_doc_count']} falsifier records", rows_html))
    else:
        render_empty_state(
            reason="no falsifier records found" if falsifiers["status"] == "ok" else falsifiers["rationale"],
            expected_artifact="papers/falsifiers/*.md",
        )

    # Honest absence note for the basin-surface visualization (proposal §9.6)
    st.markdown('<span class="cap">basin surface visualization (proposal §9.6)</span>', unsafe_allow_html=True)
    render_empty_state(
        reason=(
            "Basin surface 3D visualization is intentionally not rendered in Phase 1: "
            "the underlying perturbation outcome distributions live in reports/campaign_009/ "
            "and reports/campaign_013/ but a faithful 3D surface requires the lens-projected "
            "trace coordinates, not a stylized synthesis. Per proposal §7.6 closing line "
            "('this room should not fake mathematical precision') and D22, this surface stays "
            "empty until the projection coordinates are exposed by Campaign 017+ work."
        ),
        expected_artifact="basin-projection coordinates from a future campaign (not yet shipped)",
    )


def _load_json(path: str) -> dict[str, Any] | None:
    p = Path(path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None
