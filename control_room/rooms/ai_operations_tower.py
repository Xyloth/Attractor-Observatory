"""AI Operations Tower — proposal §7.4.

Multi-agent build organization view + Paper A's calibration empirics
visual layer. Wires builder_telemetry + build_log + doctrine adapters.
The calibration trajectory plots all builder + Codex + (eventually
Architect) records over time so the AI-orchestration research is
visible in one place.

Paper A claim surfaced here: calibration_delta convergence is the
empirical signal that the Estimation Loop discipline works. Render
honestly — including the over-estimation regime where delta is far
from 1.0.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from control_room.adapters import (
    parse_build_log,
    parse_builder_telemetry,
    parse_doctrine,
    parse_mistake_catalog,
)
from control_room.components import (
    agent_chip,
    doctrine_tablet,
    event_row,
    metric_card,
    panel,
    render_empty_state,
    render_html,
    room_emblem,
    status_pill,
)


ROOM_ID = "ai_operations_tower"
ROOM_NAME = "AI Operations Tower"
ROOM_ICON = "🛰️"
ROOM_TAGLINE = "Claude Architect / Codex Builder / Claude Builder — sidecar telemetry."
ROOM_PHASE = "Phase 1"


def render() -> None:
    import streamlit as st

    render_html(room_emblem(ROOM_NAME, ROOM_TAGLINE, ROOM_ID))

    telemetry = parse_builder_telemetry()
    build_log = parse_build_log()
    doctrine = parse_doctrine()
    mistakes = parse_mistake_catalog()

    # Agent cards row
    cols = st.columns(3)
    by_model = telemetry["data"]["by_model"] if telemetry["status"] == "ok" else {}
    for col, (label, agent_key) in zip(
        cols,
        [("Claude Builder", "Claude (Builder)"), ("Codex", "Codex"), ("Architect Claude", "Architect Claude")],
    ):
        with col:
            summary = by_model.get(agent_key, {})
            task_count = summary.get("task_count", 0)
            delta_mean = summary.get("delta_mean")
            delta_text = (
                f"mean delta {delta_mean:.3f}"
                if isinstance(delta_mean, (int, float))
                else "no delta yet"
            )
            most_recent = summary.get("most_recent_task_id") or "—"
            render_html(
                metric_card(
                    label=f"{label.lower()} · agent",
                    value=most_recent,
                    status="active" if task_count > 0 else "unavailable",
                    subtext=f"{task_count} tasks · {delta_text}",
                )
            )

    # Calibration trajectory — the load-bearing AI-research artifact.
    st.markdown('<span class="cap">paper a · estimate vs actual · all records</span>', unsafe_allow_html=True)
    if telemetry["status"] != "ok":
        render_empty_state(
            reason=telemetry["rationale"],
            expected_artifact="project_telemetry/ai_builder_tasks.jsonl",
        )
    else:
        records = telemetry["data"]["records"]
        with_actuals = [
            r for r in records
            if isinstance(r.get("estimated_minutes"), (int, float))
            and isinstance(r.get("actual_minutes"), (int, float))
        ]
        if not with_actuals:
            render_empty_state(
                reason="no telemetry records carry actual_minutes yet",
                expected_artifact="actuals must be filled by PI on session close",
            )
        else:
            _delta_chart(with_actuals)
            _delta_summary_strip(with_actuals)

    # Mistake catalog
    st.markdown('<span class="cap">mistake catalog - registry-bound classes</span>', unsafe_allow_html=True)
    if mistakes["status"] != "ok":
        render_empty_state(reason=mistakes["rationale"], expected_artifact="docs/mistake_catalog_registry.json")
    else:
        rows_html = ""
        for entry in mistakes["data"]["classes"]:
            status = entry.get("status", "unknown")
            is_candidate = status == "candidate"
            accent = "var(--warning)" if is_candidate else "var(--verified)"
            rows_html += (
                f'<div style="display:grid;grid-template-columns:80px 1fr 160px;align-items:center;'
                f'gap:10px;padding:6px 0;border-bottom:1px dashed var(--border);">'
                f'<span style="font-family:var(--font-mono);font-size:1rem;color:{accent};font-weight:600;">{entry.get("id", "?")}</span>'
                f'<span style="font-family:var(--font-body);color:var(--fg2);">{entry.get("title", "-")}</span>'
                f'<span class="cap" style="color:var(--fg4);">{status}</span>'
                f'</div>'
            )
        render_html(panel("mistake catalog (registry-bound class 1-13)", rows_html))

    # Defect catches via BUILD_LOG audit entries
    st.markdown('<span class="cap">recent audit catches</span>', unsafe_allow_html=True)
    if build_log["status"] == "ok":
        audits = [e for e in build_log["data"]["entries"] if e.get("kind") in ("audit", "architect", "talk")]
        if audits:
            rows_html = ""
            for a in audits[-8:][::-1]:
                rows_html += event_row(
                    when=a.get("date") or "—",
                    text=(a.get("header") or "")[:90],
                    status="warning" if "audit" in (a.get("header") or "").lower() else "trace",
                )
            render_html(panel("audit + meta-audit + cross-builder talk", rows_html))
        else:
            render_empty_state(
                reason="no audit entries in BUILD_LOG yet",
                expected_artifact="BUILD_LOG.md ### [...] audit entries",
            )
    else:
        render_empty_state(reason=build_log["rationale"], expected_artifact="BUILD_LOG.md")

    # Doctrine arc
    st.markdown('<span class="cap">doctrine arc - D7-D31</span>', unsafe_allow_html=True)
    if doctrine["status"] == "ok":
        items_html = ""
        for entry in doctrine["data"]["registry"]:
            items_html += doctrine_tablet(
                doctrine_id=entry.get("id", "?"),
                title=entry.get("path", "—"),
                status=entry.get("mode", "foundational"),
                signed_by=entry.get("signed_by", ""),
            )
        # Also surface consolidated headings from DOCTRINE.md when registry is sparse
        for entry in doctrine["data"].get("consolidated_entries", []):
            items_html += doctrine_tablet(
                doctrine_id=entry["id"],
                title=entry["heading"],
                status="foundational",
                signed_by="DOCTRINE.md index",
            )
        render_html(panel("doctrine registry + consolidated index", items_html))
    else:
        render_empty_state(reason=doctrine["rationale"], expected_artifact="docs/doctrine_registry.json")


def _delta_chart(records: list[dict[str, Any]]) -> None:
    import streamlit as st
    import plotly.graph_objects as go
    import math

    color_for = {
        "Claude (Builder)": "#f5b942",
        "Codex": "#5ee0ff",
        "Architect Claude": "#b084ff",
    }
    by_model: dict[str, list[dict[str, Any]]] = {}
    for r in records:
        by_model.setdefault(r.get("model_name", "unknown"), []).append(r)

    fig = go.Figure()
    for model, rows in by_model.items():
        rows = sorted(rows, key=lambda r: r.get("task_id", ""))
        labels = [r.get("task_id", "?") for r in rows]
        deltas = []
        for r in rows:
            est = float(r["estimated_minutes"])
            act = float(r["actual_minutes"])
            if est <= 0 or act <= 0:
                deltas.append(None)
            else:
                deltas.append(act / est)  # codified convention: actual / estimated
        color = color_for.get(model, "#9aa0ac")
        fig.add_trace(go.Scatter(
            x=labels, y=deltas, mode="lines+markers",
            name=model,
            line=dict(color=color, width=2.5),
            marker=dict(size=10),
        ))
    # 1.0 reference line
    fig.add_hline(y=1.0, line_dash="dash", line_color="#3ddc84", opacity=0.7,
                  annotation_text="perfect (1.0)", annotation_font_color="#3ddc84")
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=10, b=40),
        plot_bgcolor="#121826",
        paper_bgcolor="#0a0e16",
        font=dict(family="JetBrains Mono, monospace", size=11, color="#9aa0ac"),
        xaxis=dict(gridcolor="#283042", title="task", tickangle=-45),
        yaxis=dict(gridcolor="#283042", title="delta = actual / estimated", type="log"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)


def _delta_summary_strip(records: list[dict[str, Any]]) -> None:
    import streamlit as st

    by_model: dict[str, list[float]] = {}
    for r in records:
        est = float(r.get("estimated_minutes", 0) or 0)
        act = float(r.get("actual_minutes", 0) or 0)
        if est > 0 and act > 0:
            by_model.setdefault(r.get("model_name", "unknown"), []).append(act / est)
    cols = st.columns(max(len(by_model), 1))
    for col, (model, deltas) in zip(cols, by_model.items()):
        if not deltas:
            continue
        mean = sum(deltas) / len(deltas)
        last = deltas[-1]
        # Convergence status: closer to 1.0 = better
        is_converged = abs(mean - 1.0) <= 0.5
        with col:
            render_html(metric_card(
                label=f"{model} · n={len(deltas)}",
                value=f"mean Δ {mean:.3f}",
                status="verified" if is_converged else "warning",
                subtext=f"latest {last:.3f}",
            ))
