"""Campaign Command — proposal §7.3.

Campaign timeline + gate grid + audit summaries. Wires
campaign_reports + build_log adapters. Covers Campaigns 002–016
(everything that exists on disk; gracefully handles missing campaigns).
"""

from __future__ import annotations

from typing import Any

from control_room.adapters import parse_build_log, parse_campaign_reports
from control_room.components import (
    event_row,
    gate_grid,
    metric_card,
    panel,
    render_empty_state,
    render_html,
    room_emblem,
    status_pill,
)


ROOM_ID = "campaign_command"
ROOM_NAME = "Campaign Command"
ROOM_ICON = "🎯"
ROOM_TAGLINE = "Track campaigns, tasks, tests, and audits across the project."
ROOM_PHASE = "Phase 1"


def render() -> None:
    import streamlit as st

    render_html(room_emblem(ROOM_NAME, ROOM_TAGLINE, ROOM_ID))

    campaigns = parse_campaign_reports()
    build_log = parse_build_log()

    if campaigns["status"] != "ok":
        render_empty_state(
            reason=campaigns["rationale"],
            expected_artifact="reports/campaign_*/full_report.json",
        )
        return

    rows = campaigns["data"]["campaigns"]
    green = sum(1 for c in rows if c.get("status") == "green")
    in_progress = sum(1 for c in rows if c.get("status") in ("in_progress", "yellow"))
    failed = sum(1 for c in rows if c.get("status") == "failed")
    no_report = sum(1 for c in rows if not c.get("report_present"))

    cols = st.columns(4)
    with cols[0]:
        render_html(metric_card("campaigns total", str(len(rows)), "active", f"002–016 surveyed"))
    with cols[1]:
        render_html(metric_card("green", str(green), "verified", f"{green}/{len(rows)}"))
    with cols[2]:
        render_html(metric_card("in progress", str(in_progress), "warning", f"non-green campaigns"))
    with cols[3]:
        render_html(metric_card(
            "no report",
            str(no_report),
            "unavailable" if no_report > 0 else "verified",
            "campaigns without full_report.json",
        ))

    # Campaign Timeline (proposal §9.2)
    st.markdown('<span class="cap">campaign timeline · 002 — 016</span>', unsafe_allow_html=True)
    _campaign_timeline(rows)

    # Gate grid
    st.markdown('<span class="cap">gate status · campaigns × gates</span>', unsafe_allow_html=True)
    render_html(panel("gate grid", gate_grid(rows)))

    # Per-campaign drilldown table
    st.markdown('<span class="cap">per-campaign detail</span>', unsafe_allow_html=True)
    rows_html = ""
    for c in rows:
        passed = c.get("passed_gate_count")
        total = c.get("gate_count")
        gate_text = f"{passed}/{total}" if (total is not None and passed is not None) else "—"
        artifacts = c.get("artifacts") or {}
        n_artifacts = len(artifacts) if isinstance(artifacts, dict) else 0
        rows_html += (
            '<div style="display:grid;grid-template-columns:140px 1fr 110px 90px 110px;align-items:center;gap:10px;'
            'padding:8px 0;border-bottom:1px dashed var(--border);">'
            f'<span style="font-family:var(--font-mono);font-size:0.95rem;color:var(--fg2);">{c["campaign_id"]}</span>'
            f'<span style="font-family:var(--font-mono);font-size:var(--fs-detail);color:var(--fg4);">{c.get("schema") or ""}</span>'
            f'<span class="cap mono">{gate_text}</span>'
            f'<span class="cap mono">{n_artifacts} artifacts</span>'
            f'{status_pill(str(c.get("status") or "unknown"), status=str(c.get("status") or "unknown"))}'
            "</div>"
        )
    render_html(panel("campaign detail table", rows_html))

    # Recent BUILD_LOG audits per campaign
    st.markdown('<span class="cap">audit + meta-audit log (BUILD_LOG)</span>', unsafe_allow_html=True)
    if build_log["status"] == "ok":
        audits = [
            e for e in build_log["data"]["entries"]
            if any(token in (e.get("header") or "").lower() for token in ("audit", "meta-audit", "campaign"))
        ]
        if audits:
            rows_html = ""
            for a in audits[-10:][::-1]:
                rows_html += event_row(
                    when=a.get("date") or "—",
                    text=(a.get("header") or "")[:96],
                    status="warning" if "audit" in (a.get("header") or "").lower() else "active",
                )
            render_html(panel(f"{len(audits)} audit-related entries", rows_html))
        else:
            render_empty_state(
                reason="no audit-related entries surfaced from BUILD_LOG",
                expected_artifact="BUILD_LOG.md ### [...] audit lines",
            )
    else:
        render_empty_state(reason=build_log["rationale"], expected_artifact="BUILD_LOG.md")


def _campaign_timeline(rows: list[dict[str, Any]]) -> None:
    import streamlit as st
    import plotly.graph_objects as go

    # X = campaign index; Y = passed_gate_count (0 if missing). Markers
    # colored by status. The timeline is intentionally minimalist —
    # the gate grid carries the per-gate detail.
    xs = [r["campaign_id"] for r in rows]
    ys = []
    colors = []
    hover = []
    color_map = {
        "green": "#3ddc84",
        "in_progress": "#f5a623",
        "failed": "#ff5468",
    }
    for r in rows:
        passed = r.get("passed_gate_count") or 0
        total = r.get("gate_count") or 0
        ys.append(passed)
        colors.append(color_map.get(r.get("status"), "#5b6478"))
        hover.append(f"{r['campaign_id']}<br>{passed}/{total} passed<br>status: {r.get('status') or '?'}")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=xs, y=ys,
        marker=dict(color=colors, line=dict(color="#283042", width=1)),
        hovertext=hover, hoverinfo="text",
    ))
    fig.update_layout(
        height=240,
        margin=dict(l=20, r=20, t=10, b=40),
        plot_bgcolor="#121826",
        paper_bgcolor="#0a0e16",
        font=dict(family="JetBrains Mono, monospace", size=11, color="#9aa0ac"),
        xaxis=dict(gridcolor="#283042", title="", tickangle=-45),
        yaxis=dict(gridcolor="#283042", title="passed gates"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
