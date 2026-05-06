"""Motif Atlas — proposal §7.5.

Motifs as living objects. Wires factory_store (Campaign 016 normalized
references give ProcessRole / InteractionChannel / StateSpaceEffect /
OverlapField counts), campaign_reports (motif IDs surface from the
deficit map and replication verdicts).

Motif registry is canonical: 6 motifs from the v0.13 ontology.
Coverage data folds in Campaign 010 / 013 results.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from control_room.adapters import parse_campaign_reports, parse_factory_store
from control_room.components import (
    metric_card,
    panel,
    render_empty_state,
    render_html,
    room_emblem,
    status_pill,
)


ROOM_ID = "motif_atlas"
ROOM_NAME = "Motif Atlas"
ROOM_ICON = "🧬"
ROOM_TAGLINE = "Motifs as living objects — worlds, process roles, channels."
ROOM_PHASE = "Phase 1"


# Canonical motif registry (formalism/lens_registry.MOTIFS).
MOTIFS = [
    ("motif.autocatalytic_closure.draft",     "Autocatalytic closure",        "exploratory"),
    ("motif.self_maintained_boundary.draft",  "Self-maintained boundary",     "exploratory"),
    ("motif.repair.draft",                    "Repair",                       "exploratory"),
    ("motif.replication_lineage.draft",       "Replication lineage",          "exploratory"),
    ("motif.externalized_memory.draft",       "Externalized memory",          "exploratory"),
    ("motif.floor_connectivity.draft",        "Floor connectivity (deficit)", "candidate"),
]


def render() -> None:
    import streamlit as st

    render_html(room_emblem(ROOM_NAME, ROOM_TAGLINE, ROOM_ID))

    factory = parse_factory_store()
    campaigns = parse_campaign_reports()

    # Top metrics from Campaign 016 ontology counts.
    cols = st.columns(4)
    counts = _ontology_counts(factory)
    with cols[0]:
        render_html(metric_card("motifs registered", str(len(MOTIFS)), "motif", "v0.13 ontology"))
    with cols[1]:
        render_html(metric_card(
            "process roles",
            str(counts.get("process_role", "—")),
            "active" if counts.get("process_role") else "unavailable",
            "from normalized_refs",
        ))
    with cols[2]:
        render_html(metric_card(
            "interaction channels",
            str(counts.get("interaction_channel", "—")),
            "active" if counts.get("interaction_channel") else "unavailable",
            "from normalized_refs",
        ))
    with cols[3]:
        render_html(metric_card(
            "overlap fields",
            str(counts.get("overlap_field", "—")),
            "active" if counts.get("overlap_field") else "unavailable",
            "from normalized_refs",
        ))

    # Motif cards
    st.markdown('<span class="cap">motif registry · 6 entries</span>', unsafe_allow_html=True)
    cols = st.columns(2)
    floor_gap = _read_floor_gap()
    for i, (motif_id, label, status) in enumerate(MOTIFS):
        is_floor = "floor_connectivity" in motif_id
        body_html = (
            f'<div class="cap" style="margin-bottom:6px;">{motif_id}</div>'
            f'<div style="font-family:var(--font-display);font-size:var(--fs-h3);color:var(--fg1);'
            f'margin-bottom:8px;">{label}</div>'
            f'<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">'
            f'{status_pill(status, status=status)}'
            f'</div>'
        )
        if is_floor and floor_gap is not None:
            body_html += (
                f'<div style="margin-top:10px;padding:8px;background:var(--motif-soft);'
                f'border-left:2px solid var(--motif);border-radius:6px;'
                f'font-family:var(--font-mono);font-size:var(--fs-detail);color:var(--fg2);">'
                f'Campaign 013 replication: formal_gap = {floor_gap["formal_gap"]:.4f}, '
                f'p = {floor_gap["empirical_p"]:.4f}, verdict = <b>{floor_gap["verdict"]}</b>'
                f'</div>'
            )
        with cols[i % 2]:
            render_html(panel(motif_id.split(".")[1], body_html))

    # Motif × world matrix (proposal §9.5 motif embedding)
    st.markdown('<span class="cap">motif × world coverage matrix</span>', unsafe_allow_html=True)
    if campaigns["status"] != "ok":
        render_empty_state(
            reason="campaign reports unavailable; cannot derive motif × world coverage",
            expected_artifact="reports/campaign_010/coverage_matrix.json",
        )
    else:
        coverage_path = Path("reports/campaign_010/coverage_matrix.json")
        if not coverage_path.exists():
            render_empty_state(
                reason=f"{coverage_path.as_posix()} not present",
                expected_artifact="Campaign 010 coverage_matrix.json",
            )
        else:
            try:
                cov = json.loads(coverage_path.read_text(encoding="utf-8-sig"))
                _coverage_heatmap(cov)
            except (OSError, json.JSONDecodeError) as exc:
                render_empty_state(
                    reason=f"could not parse {coverage_path}: {exc}",
                    expected_artifact="reports/campaign_010/coverage_matrix.json (valid JSON)",
                )


def _ontology_counts(factory: dict[str, Any]) -> dict[str, int]:
    if factory["status"] != "ok":
        return {}
    payload = factory["data"]["store_payloads"]
    normalized = payload.get("normalized", {})
    if not normalized.get("present"):
        return {}
    data = normalized.get("data") or {}
    records = data.get("records") if isinstance(data, dict) else None
    if not isinstance(records, list):
        return {}
    counts: dict[str, int] = {}
    for r in records:
        if not isinstance(r, dict):
            continue
        for kind in ("process_role", "interaction_channel", "state_space_effect", "overlap_field"):
            value = r.get(kind) or r.get(f"{kind}_id") or r.get(f"{kind}s")
            if value:
                counts[kind] = counts.get(kind, 0) + 1
    return counts


def _read_floor_gap() -> dict[str, Any] | None:
    p = Path("reports/campaign_013/replication_verdict.json")
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None
    fg = data.get("formal_gap") or {}
    n7 = data.get("n7") or {}
    verdict = data.get("verdict") or {}
    return {
        "formal_gap": float(fg.get("formal_gap", 0.0)),
        "empirical_p": float(n7.get("empirical_p", 1.0)),
        "verdict": verdict.get("verdict", "?"),
    }


def _coverage_heatmap(cov: dict[str, Any]) -> None:
    import streamlit as st
    import plotly.graph_objects as go

    rows = cov.get("rows", [])
    if not rows:
        from control_room.components import render_empty_state
        render_empty_state(
            reason="coverage matrix has no rows",
            expected_artifact="non-empty coverage_matrix.json",
        )
        return
    motif_ids = sorted({r["motif_id"] for r in rows})
    lens_ids = sorted({r["lens_id"] for r in rows})
    z = [[None] * len(motif_ids) for _ in lens_ids]
    for r in rows:
        i = lens_ids.index(r["lens_id"])
        j = motif_ids.index(r["motif_id"])
        z[i][j] = r.get("coverage_score", 0.0)
    motif_short = [m.split(".")[1] for m in motif_ids]
    fig = go.Figure(data=go.Heatmap(
        z=z, x=motif_short, y=lens_ids,
        colorscale=[[0, "#1a2032"], [0.4, "#283042"], [0.7, "#bd6df8"], [1.0, "#3ddc84"]],
        zmin=0, zmax=1,
        colorbar=dict(title="coverage", tickfont=dict(color="#9aa0ac")),
        hovertemplate="lens=%{y}<br>motif=%{x}<br>coverage=%{z:.3f}<extra></extra>",
    ))
    fig.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=10, b=40),
        plot_bgcolor="#121826",
        paper_bgcolor="#0a0e16",
        font=dict(family="JetBrains Mono, monospace", size=11, color="#9aa0ac"),
        xaxis=dict(title="motif", tickangle=-30),
        yaxis=dict(title="lens"),
    )
    st.plotly_chart(fig, use_container_width=True)
