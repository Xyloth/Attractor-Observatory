"""Agent heartbeat ledger.

Lightweight presence tracking for AI agents working in the repo. Each
agent (Architect Claude, Codex, Claude Builder, Codex 1.5x, Destroyer
Claude — slot reserved, see below) flips a bit on entry and on exit:

* On entry, the agent calls ``mark_entered(agent_id, task_id)``.
* On exit, the agent calls ``mark_exited(agent_id)``.

The Control Room reads ``read_heartbeat()`` on each render and the
sidebar shows which agents are currently active (with a slow pulse
animation). When an agent forgets to mark exit (crash, compaction),
``stale_threshold_seconds`` reclassifies them as ``stale`` rather than
``active`` so the panel doesn't lie about presence.

The ledger lives at ``control_room/cache/agent_heartbeat.json``. That
path is on the read-only-enforcement whitelist; this is the canonical
sidecar-writable location.

DESIGN NOTE — "Destroyer" (placeholder): the user has reserved a fifth
agent role labelled "Destroyer Claude" but has not yet described its
job. The slot is included in CANONICAL_AGENTS with a "role pending"
description so the Control Room renders the absence honestly per D22
rather than fabricating a role description.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HEARTBEAT_PATH = Path(__file__).resolve().parent / "cache" / "agent_heartbeat.json"
HEARTBEAT_SCHEMA = "AgentHeartbeat.v1"
DEFAULT_STALE_THRESHOLD_SECONDS = 600  # 10 minutes — agent presumed gone


# Canonical agent roster. Every Control Room render shows ALL of these
# in the sidebar panel; status flips by ledger contents. Slot reserved
# for "Destroyer" per the user's CB-007 polish note ("you don't know
# anything about him yet"); the role description is intentionally
# blank so the panel renders honest absence per D22.
CANONICAL_AGENTS = [
    {"id": "architect_claude", "label": "Architect", "role": "design + meta-audit", "color_token": "agent-architect"},
    {"id": "claude_builder",   "label": "Builder",   "role": "analytical + UI",     "color_token": "agent-builder"},
    {"id": "codex",            "label": "Codex",     "role": "implementation + audit", "color_token": "agent-codex"},
    {"id": "codex_1_5x",       "label": "Codex 1.5x","role": "Factory hardening (TASK-027 lane)", "color_token": "agent-codex"},
    {"id": "destroyer_claude", "label": "Destroyer", "role": "(role pending — user will brief separately)", "color_token": "agent-architect"},
    {"id": "human_pi",         "label": "Human PI",  "role": "arbitration + actuals", "color_token": "agent-human"},
]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load() -> dict[str, Any]:
    if not HEARTBEAT_PATH.exists():
        return {"schema": HEARTBEAT_SCHEMA, "agents": {}}
    try:
        payload = json.loads(HEARTBEAT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"schema": HEARTBEAT_SCHEMA, "agents": {}}
    if not isinstance(payload, dict) or "agents" not in payload:
        return {"schema": HEARTBEAT_SCHEMA, "agents": {}}
    return payload


def _save(payload: dict[str, Any]) -> None:
    HEARTBEAT_PATH.parent.mkdir(parents=True, exist_ok=True)
    HEARTBEAT_PATH.write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def mark_entered(agent_id: str, task_id: str | None = None) -> None:
    """Agent calls this on entry to the repo. Idempotent — re-entries
    refresh the timestamp."""
    payload = _load()
    payload["schema"] = HEARTBEAT_SCHEMA
    now = _now_iso()
    rec = payload["agents"].get(agent_id, {})
    rec.update({
        "agent_id": agent_id,
        "active": True,
        "entered_at": rec.get("entered_at") if rec.get("active") else now,
        "last_seen_at": now,
        "task_id": task_id or rec.get("task_id"),
    })
    payload["agents"][agent_id] = rec
    _save(payload)


def mark_seen(agent_id: str, task_id: str | None = None) -> None:
    """Heartbeat tick — refresh ``last_seen_at`` without changing entered_at."""
    payload = _load()
    payload["schema"] = HEARTBEAT_SCHEMA
    rec = payload["agents"].get(agent_id) or {"agent_id": agent_id, "entered_at": _now_iso()}
    rec.update({
        "active": True,
        "last_seen_at": _now_iso(),
    })
    if task_id:
        rec["task_id"] = task_id
    payload["agents"][agent_id] = rec
    _save(payload)


def mark_exited(agent_id: str) -> None:
    """Agent calls this on exit. Sets active=False but preserves the
    timestamps so the panel can show recent-departure history."""
    payload = _load()
    payload["schema"] = HEARTBEAT_SCHEMA
    rec = payload["agents"].get(agent_id) or {"agent_id": agent_id}
    rec["active"] = False
    rec["exited_at"] = _now_iso()
    payload["agents"][agent_id] = rec
    _save(payload)


def read_heartbeat(stale_threshold_seconds: int = DEFAULT_STALE_THRESHOLD_SECONDS) -> dict[str, Any]:
    """Read the ledger and return a normalized payload for the panel.

    Each agent in CANONICAL_AGENTS is present in the result; agents
    not in the ledger are reported as ``status: quiet``. Agents whose
    last_seen is older than the stale threshold are reclassified as
    ``status: stale`` (active flag was probably never reset).
    """
    payload = _load()
    now = datetime.now(timezone.utc)
    rows = []
    for canonical in CANONICAL_AGENTS:
        rec = payload["agents"].get(canonical["id"], {})
        active = bool(rec.get("active"))
        last_seen_iso = rec.get("last_seen_at")
        seconds_since = None
        status = "quiet"
        if last_seen_iso:
            try:
                last_seen = datetime.fromisoformat(last_seen_iso)
                if last_seen.tzinfo is None:
                    last_seen = last_seen.replace(tzinfo=timezone.utc)
                seconds_since = (now - last_seen).total_seconds()
            except ValueError:
                pass
        if active and seconds_since is not None and seconds_since <= stale_threshold_seconds:
            status = "active"
        elif active and seconds_since is not None and seconds_since > stale_threshold_seconds:
            status = "stale"
        elif rec.get("exited_at"):
            status = "departed"
        elif last_seen_iso and not active:
            status = "departed"
        rows.append({
            **canonical,
            "status": status,
            "last_seen_at": last_seen_iso,
            "entered_at": rec.get("entered_at"),
            "exited_at": rec.get("exited_at"),
            "task_id": rec.get("task_id"),
            "seconds_since_seen": seconds_since,
        })
    return {
        "schema": HEARTBEAT_SCHEMA,
        "stale_threshold_seconds": stale_threshold_seconds,
        "ledger_path": HEARTBEAT_PATH.as_posix(),
        "ledger_present": HEARTBEAT_PATH.exists(),
        "agents": rows,
    }


def render_sidebar_panel() -> None:
    """Render the heartbeat panel in the Streamlit sidebar.

    Shows every canonical agent with a status dot. Active agents pulse
    via the design-system ``--motion-pulse`` keyframes (slow blink).
    Click on a stale agent surfaces a tooltip noting the agent forgot
    to mark exit.
    """
    import streamlit as st

    state = read_heartbeat()
    color_map = {
        "active":   ("var(--verified)", "agent active in repo"),
        "stale":    ("var(--warning)", "agent did not mark exit; presumed crashed/compacted"),
        "departed": ("var(--unavailable)", "agent left cleanly"),
        "quiet":    ("var(--fg5)",       "agent has not entered yet"),
    }
    rows_html = ""
    for agent in state["agents"]:
        color, tooltip_base = color_map.get(agent["status"], color_map["quiet"])
        active_anim = "animation: pulse-soft var(--motion-pulse) ease-in-out infinite;" if agent["status"] == "active" else ""
        token_var = f"var(--{agent['color_token']})"
        last_seen = agent.get("last_seen_at") or "never"
        task_id = agent.get("task_id") or "—"
        tooltip = f"{tooltip_base} · last seen: {last_seen} · task: {task_id}"
        rows_html += (
            f'<div title="{tooltip}" style="display:flex;align-items:center;gap:8px;'
            f'padding:5px 8px;border-radius:8px;margin-bottom:2px;'
            f'border-left:2px solid {token_var};background:rgba(255,255,255,0.015);">'
            f'<span style="width:8px;height:8px;border-radius:50%;background:{color};'
            f'box-shadow:0 0 8px {color};{active_anim}"></span>'
            f'<span style="flex:1;font-family:var(--font-mono);font-size:0.78rem;'
            f'color:var(--fg2);letter-spacing:0.04em;">{agent["label"]}</span>'
            f'<span style="font-family:var(--font-mono);font-size:0.7rem;color:var(--fg4);'
            f'text-transform:uppercase;letter-spacing:0.06em;">{agent["status"]}</span>'
            "</div>"
        )
    st.markdown(
        '<div style="margin-top:1rem;padding-top:0.8rem;border-top:1px solid #283042;">'
        '<div style="font-family:var(--font-mono);font-size:0.7rem;color:var(--fg4);'
        'text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">agents · live</div>'
        + rows_html
        + ('<div style="font-family:var(--font-mono);font-size:0.65rem;color:var(--fg5);'
           'margin-top:6px;">'
           f'ledger: <code>{HEARTBEAT_PATH.name}</code>'
           '</div>')
        + '</div>',
        unsafe_allow_html=True,
    )
