"""Pulse Deck — proposal §7.1.

Live heartbeat. First screen on app open. Wires git_metadata,
builder_telemetry, build_log, campaign_reports, pytest_cache,
methods_falsifiers adapters into the hierarchy:

  First glance — branch / latest commit / latest tests / current builder
                 task + needs-attention lane.
  Second glance — campaign gate grid + recent BUILD_LOG events +
                  calibration trajectory + recent falsifiers.

D22 binding: every adapter's non-ok status routes to the empty-state
component; no plausible-defaults pathway. Every panel that has no real
data shows honest absence labelled with the artifact that would
populate it.
"""

from __future__ import annotations

from typing import Any

from control_room.adapters import (
    parse_build_log,
    parse_builder_telemetry,
    parse_campaign_reports,
    parse_git_metadata,
    parse_methods_falsifiers,
    parse_pytest_cache,
)
from control_room.components import (
    agent_chip,
    event_row,
    gate_grid,
    metric_card,
    needs_attention,
    panel,
    render_empty_state,
    render_html,
    room_emblem,
    status_pill,
)
from control_room.snapshot import build_snapshot, diff_snapshots, load_prior


ROOM_ID = "pulse_deck"
ROOM_NAME = "Pulse Deck"
ROOM_ICON = "📡"
ROOM_TAGLINE = "Live heartbeat — what is happening right now?"
ROOM_PHASE = "Phase 1"


def render() -> None:
    import streamlit as st

    render_html(room_emblem(ROOM_NAME, ROOM_TAGLINE, ROOM_ID))

    git = parse_git_metadata(".")
    telemetry = parse_builder_telemetry()
    build_log = parse_build_log()
    campaigns = parse_campaign_reports()
    pytest_cache = parse_pytest_cache()
    falsifiers = parse_methods_falsifiers()

    # ------- FIRST GLANCE -------
    # Branch / commit / tests / current task as 4 mini cards.
    cols = st.columns(4)
    with cols[0]:
        if git["status"] == "ok":
            d = git["data"]
            commit = d["last_commit"]
            render_html(metric_card(
                label="active branch",
                value=d["branch"],
                status="active",
                subtext=f'{commit.get("short", "")} · {commit.get("subject", "")[:40]}',
            ))
        else:
            render_empty_state(reason=git["rationale"], expected_artifact="git repository .git/")
    with cols[1]:
        if git["status"] == "ok":
            commit = git["data"]["last_commit"]
            render_html(metric_card(
                label="latest commit",
                value=commit.get("short", "—"),
                status="verified",
                subtext=f'{commit.get("author_name", "")} · {commit.get("iso_date", "")[:10]}',
            ))
        else:
            render_empty_state(reason="git unavailable", expected_artifact=".git/")
    with cols[2]:
        if pytest_cache["status"] == "ok":
            d = pytest_cache["data"]
            failed = d["last_failed_count"]
            total = d.get("nodeid_count")
            value = f'{(total or "?")}n / {failed}f' if total is not None else f'{failed}f'
            render_html(metric_card(
                label="pytest cache",
                value=value,
                status="verified" if failed == 0 else "failed",
                subtext=f'last_failed: {failed}',
            ))
        else:
            render_empty_state(reason=pytest_cache["rationale"], expected_artifact=".pytest_cache/v/cache/")
    with cols[3]:
        if telemetry["status"] == "ok":
            d = telemetry["data"]
            most_recent_id = None
            for r in reversed(d["records"]):
                if r.get("model_name", "").startswith("Claude (Builder)"):
                    most_recent_id = r.get("task_id")
                    break
            most_recent_id = most_recent_id or "—"
            cb_summary = d["by_model"].get("Claude (Builder)", {})
            delta_mean = cb_summary.get("delta_mean")
            delta_text = f'mean delta: {delta_mean:.3f}' if delta_mean is not None else "no delta yet"
            render_html(metric_card(
                label="builder task",
                value=most_recent_id,
                status="active",
                subtext=delta_text,
            ))
        else:
            render_empty_state(reason=telemetry["rationale"], expected_artifact="project_telemetry/ai_builder_tasks.jsonl")

    # Needs attention lane — derived from pytest + falsifiers
    alerts: list[dict[str, str]] = []
    failed_count = 0
    warn_count = 0
    if pytest_cache["status"] == "ok":
        failed = pytest_cache["data"]["last_failed_count"]
        # CB-011 fix #2: stale_cache flag — never display the failed
        # count as live state if the cache mtime is older than the
        # adapter's threshold. D17 binding (stale → flagged, not faked).
        stale = pytest_cache["data"].get("stale_cache", False)
        age = pytest_cache["data"].get("lastfailed_age_seconds")
        if failed and failed > 0:
            if stale:
                # Still surface, but as a warn (not an active "tests
                # are failing right now") alert. Age makes it concrete.
                age_str = (
                    f"~{int(age/3600)}h ago" if age and age >= 3600
                    else f"~{int(age/60)}m ago" if age else "stale"
                )
                warn_count += 1
                alerts.append({
                    "text": f"{failed} pytest tests failed (STALE cache, last touched {age_str})",
                    "when": "stale",
                })
            else:
                failed_count += failed
                alerts.append({
                    "text": f"{failed} pytest tests failed last run",
                    "when": "last test run",
                })
    if campaigns["status"] == "ok":
        not_green = [c for c in campaigns["data"]["campaigns"] if c.get("status") not in (None, "green")]
        for c in not_green[:2]:
            warn_count += 1
            alerts.append({"text": f"{c['campaign_id']} status={c['status']}", "when": ""})
    render_html(needs_attention(alerts=alerts, failed_count=failed_count, warn_count=warn_count))

    # ------- SECOND GLANCE -------
    left, right = st.columns([7, 5])

    # Gate grid
    with left:
        st.markdown('<span class="cap">campaigns × gates</span>', unsafe_allow_html=True)
        if campaigns["status"] == "ok" and campaigns["data"]["campaigns"]:
            render_html(panel("gate status", gate_grid(campaigns["data"]["campaigns"])))
        else:
            render_empty_state(reason=campaigns["rationale"], expected_artifact="reports/campaign_*/full_report.json")

    # Recent events from BUILD_LOG
    with right:
        st.markdown('<span class="cap">delta — what changed</span>', unsafe_allow_html=True)
        if build_log["status"] == "ok" and build_log["data"]["entries"]:
            entries = build_log["data"]["entries"][-8:][::-1]
            rows_html = ""
            for entry in entries:
                date = entry.get("date") or "—"
                header = entry.get("header") or ""
                kind = entry.get("kind") or "other"
                status_for_kind = {
                    "work": "active",
                    "audit": "warning",
                    "talk": "trace",
                    "architect": "motif",
                }.get(kind, "active")
                rows_html += event_row(when=date, text=header[:96], status=status_for_kind)
            render_html(panel("recent BUILD_LOG entries", rows_html))
        else:
            render_empty_state(reason=build_log["rationale"], expected_artifact="BUILD_LOG.md")

    # Calibration trajectory — full width below
    st.markdown('<span class="cap">calibration · estimate vs actual</span>', unsafe_allow_html=True)
    if telemetry["status"] == "ok":
        records = telemetry["data"]["records"]
        with_actuals = [
            r for r in records
            if isinstance(r.get("estimated_minutes"), (int, float))
            and isinstance(r.get("actual_minutes"), (int, float))
        ]
        if not with_actuals:
            render_empty_state(
                reason="no telemetry records have actual_minutes filled yet",
                expected_artifact="project_telemetry/ai_builder_tasks.jsonl with actual_minutes set on prior tasks",
            )
        else:
            _calibration_chart(with_actuals)
    else:
        render_empty_state(reason=telemetry["rationale"], expected_artifact="project_telemetry/ai_builder_tasks.jsonl")

    # What-changed-since-last-session panel.
    # CB-011 fix #1: previously this rendered the raw snapshot diff,
    # which dumped BUILD_LOG preamble text when the parser returned
    # status=malformed. Now we render the LATEST BUILD_LOG work
    # entries as titled event cards (date · header · first line of
    # body) PLUS the structural snapshot diff alongside. This is what
    # James asked for: "TASK-MOTIF-IMPL completed 17:30 EST",
    # "TASK-W-1-MASS-INGEST: 1,375 records".
    st.markdown('<span class="cap">what changed since last session</span>', unsafe_allow_html=True)
    if build_log["status"] != "ok":
        render_empty_state(
            reason=build_log["rationale"],
            expected_artifact="BUILD_LOG.md (UTF-8 readable)",
        )
    else:
        recent_entries = build_log["data"]["entries"][-8:][::-1]
        cards_html = ""
        for entry in recent_entries:
            date = entry.get("date") or "—"
            header = entry.get("header") or "(untitled)"
            body = (entry.get("body") or "").strip()
            # First non-empty line of body, truncated.
            first_line = next(
                (ln.strip() for ln in body.splitlines() if ln.strip()),
                "",
            )[:140]
            kind = entry.get("kind") or "other"
            kind_color = {
                "work":      "#4fc3f7",  # active
                "audit":     "#f5a623",  # warning
                "talk":      "#22d3ee",  # trace
                "architect": "#bd6df8",  # motif
            }.get(kind, "#9aa0ac")
            first_line_html = (
                '<div style="font-family:var(--font-mono);font-size:var(--fs-detail);'
                f'color:var(--fg4);margin-top:2px;">{first_line}</div>'
                if first_line else ""
            )
            cards_html += (
                f'<div style="display:grid;grid-template-columns:90px 1fr 60px;gap:10px;'
                f'padding:8px 0;border-bottom:1px dashed var(--border);align-items:start;">'
                f'<span style="font-family:var(--font-mono);font-size:var(--fs-detail);'
                f'color:var(--fg4);">{date}</span>'
                f'<div>'
                f'<div style="font-family:var(--font-display);font-size:var(--fs-body);'
                f'color:var(--fg2);font-weight:500;">{header[:90]}</div>'
                f'{first_line_html}'
                f'</div>'
                f'<span class="cap" style="color:{kind_color};text-align:right;">{kind}</span>'
                f'</div>'
            )
        render_html(panel(
            f"latest {len(recent_entries)} BUILD_LOG entries · click into Doctrine Console for full audit trail",
            cards_html,
        ))

        # Then surface the structural snapshot diff alongside for non-
        # BUILD_LOG changes (campaign status flips, falsifier counts,
        # registry growth). Renders cleanly when prior snapshot exists.
        prior_snap = load_prior()
        current_snap = build_snapshot()
        diff = diff_snapshots(prior_snap, current_snap)
        if diff["status"] == "first_launch":
            pass  # silent — the build_log cards above carry the load
        elif diff["delta_count"] == 0:
            render_html(panel(
                "structural deltas · steady state",
                '<div style="font-family: var(--font-body); font-size: var(--fs-detail); color: var(--fg4);">'
                f'No campaign / falsifier / doctrine changes between '
                f'{diff["prior_generated_at"][:19]} and {diff["current_generated_at"][:19]}.'
                '</div>',
            ))
        else:
            delta_rows_html = ""
            for d in diff["deltas"][:10]:
                kind = d.get("kind", "?")
                # CB-011 hardening: only render deltas with KNOWN kinds;
                # unknown kinds render as a typed pill rather than the
                # f'{kind}: {d}' raw-dict dump that produced the
                # docstring-leak bug.
                description = _describe_delta(d)
                if description.startswith(f'{kind}: ') and kind != "?":
                    description = f'unknown delta kind={kind} (suppressed raw payload)'
                delta_rows_html += event_row(
                    when="delta",
                    text=description,
                    status="active" if "added" in kind or "new" in kind
                          else "warning" if "changed" in kind
                          else "trace",
                )
            render_html(panel(
                f"structural deltas · {diff['delta_count']} since prior snapshot",
                delta_rows_html,
            ))

    # Recent falsifiers
    st.markdown('<span class="cap">recent falsifiers</span>', unsafe_allow_html=True)
    if falsifiers["status"] == "ok" and falsifiers["data"]["falsifier_doc_count"] > 0:
        f_docs = falsifiers["data"]["falsifier_docs"]
        rows_html = ""
        for d in f_docs[-6:][::-1]:
            rows_html += event_row(when="—", text=d.get("first_heading") or d["name"], status="failed")
        render_html(panel(f'{len(f_docs)} falsifier records', rows_html))
    else:
        render_empty_state(
            reason="no falsifier records present" if falsifiers["status"] == "ok" else falsifiers["rationale"],
            expected_artifact="papers/falsifiers/*.md",
        )


def _describe_delta(d: dict[str, Any]) -> str:
    kind = d.get("kind", "?")
    if kind == "campaign_added":
        return f'campaign added: {d.get("id")} (status {d.get("status")})'
    if kind == "campaign_status_changed":
        return f'{d.get("id")}: {d.get("from")} → {d.get("to")}'
    if kind == "pytest_failed_count_changed":
        return f'pytest last_failed: {d.get("from")} → {d.get("to")}'
    if kind == "falsifier_count_changed":
        return f'falsifier count: {d.get("from")} → {d.get("to")}'
    if kind == "doctrine_registry_count_changed":
        return f'doctrine registry: {d.get("from")} → {d.get("to")}'
    if kind == "build_log_entry_new":
        return f'BUILD_LOG ({d.get("date")}): {(d.get("header") or "")[:80]}'
    if kind == "claude_builder_latest_delta_changed":
        from_v = d.get("from")
        to_v = d.get("to")
        try:
            return f'Claude (Builder) latest Δ: {float(from_v):.3f} → {float(to_v):.3f}' if from_v is not None and to_v is not None else f'latest delta changed'
        except (TypeError, ValueError):
            return f'latest delta changed'
    return f'{kind}: {d}'


def _calibration_chart(with_actuals: list[dict[str, Any]]) -> None:
    import streamlit as st
    import plotly.graph_objects as go

    by_model: dict[str, list[dict[str, Any]]] = {}
    for r in with_actuals:
        by_model.setdefault(r.get("model_name", "unknown"), []).append(r)

    fig = go.Figure()
    color_for = {
        "Claude (Builder)": "#f5b942",  # agent-builder
        "Codex": "#5ee0ff",             # agent-codex
        "Architect Claude": "#b084ff",  # agent-architect
    }
    for model, rows in by_model.items():
        rows = sorted(rows, key=lambda r: r.get("task_id", ""))
        labels = [r.get("task_id", "?") for r in rows]
        ests = [float(r["estimated_minutes"]) for r in rows]
        acts = [float(r["actual_minutes"]) for r in rows]
        color = color_for.get(model, "#9aa0ac")
        fig.add_trace(go.Scatter(
            x=labels, y=ests, mode="lines+markers",
            name=f"{model} estimated",
            line=dict(color=color, width=1, dash="dash"),
            marker=dict(symbol="circle-open", size=8),
            opacity=0.6,
        ))
        fig.add_trace(go.Scatter(
            x=labels, y=acts, mode="lines+markers",
            name=f"{model} actual",
            line=dict(color=color, width=2.5),
            marker=dict(size=10),
        ))
    # Polish iteration: switch to log y so small actuals (12-25 min) stay
    # visible alongside the huge legacy estimates (some Codex tasks
    # estimated 1000+ min). Linear scale flattened the actuals into a
    # single low line that was unreadable.
    fig.update_layout(
        height=340,
        margin=dict(l=20, r=20, t=10, b=40),
        plot_bgcolor="#121826",
        paper_bgcolor="#0a0e16",
        font=dict(family="JetBrains Mono, monospace", size=11, color="#9aa0ac"),
        xaxis=dict(gridcolor="#283042", title="task", tickangle=-45),
        yaxis=dict(
            gridcolor="#283042",
            title="minutes (log scale)",
            type="log",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)
