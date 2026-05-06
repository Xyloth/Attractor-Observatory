"""Streamlit entry for the Observatory Control Room.

Run::

    streamlit run control_room/app.py

The app shell is dark-mode by default per proposal §6, applies the
design tokens from ``control_room.design_tokens``, and renders sidebar
navigation across all 11 rooms (proposal §7 + Project Graph). Phase 0
shipped the foundation; Phase 1+2 wired real rooms; Phase 3 (CB-007)
ships polish, click-to-navigate, snapshot endpoint, and Portfolio Mode.

Each render writes a snapshot to ``control_room/snapshots/`` for AI
consumption; this is a sidecar-writable path per the read-only
enforcement test's whitelist.

URL-anchor routing: ``?room=<room_id>`` selects a room from a query
parameter (used by Project Graph click-to-navigate fallback). When
session state is set first (clicked node), it wins.
"""

from __future__ import annotations

import os
import subprocess
from typing import Any

import streamlit as st

from control_room.design_tokens import (
    COLOR_TEXT_MUTED,
    COLOR_TEXT_SECONDARY,
    FONT_FAMILY_DISPLAY,
    FONT_FAMILY_MONO,
    FONT_SIZE_DETAIL,
    FONT_SIZE_HEADING_3,
    FONT_SIZE_LABEL,
    PAGE_ICON,
    PAGE_LAYOUT,
    PAGE_SUBTITLE,
    PAGE_TITLE,
    streamlit_theme_css,
)
from control_room.heartbeat import render_sidebar_panel as render_heartbeat_panel
from control_room.rooms import render_room, room_registry
from control_room.snapshot import write_snapshot


def _git_branch() -> str:
    """Best-effort git branch read for the sidebar header.

    Falls back to a static label if git isn't on PATH.
    """
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=2, check=False,
        )
        if out.returncode == 0:
            return out.stdout.strip() or "(detached)"
    except (OSError, subprocess.SubprocessError):
        pass
    return "feature/control-room-v0"


def _phase_label() -> str:
    """Phase label shown in the sidebar header. Reflects current state
    (Campaign 015 closed at CB-007). Not git-derived; the ``__phase__``
    constant in ``control_room/__init__.py`` could carry this, but a
    simple label here suffices for the sidebar chrome."""
    return "campaign 015 — production"


def _resolve_room_from_query_or_state(rooms: list[dict[str, Any]]) -> int | None:
    """Return the index of a room selected via session_state or
    ``?room=<id>`` query param. Returns None if no override.

    Click-to-navigate from Project Graph sets ``st.session_state["control_room_target"]``
    before rerun; URL anchor is the fallback path.
    """
    target = st.session_state.get("control_room_target")
    if target:
        for i, r in enumerate(rooms):
            if r["id"] == target:
                # Consume the target so subsequent reruns honor sidebar choice.
                st.session_state.pop("control_room_target", None)
                return i
    # Fallback: read query param.
    try:
        params = st.query_params
        room_q = params.get("room")
    except Exception:
        room_q = None
    if room_q:
        for i, r in enumerate(rooms):
            if r["id"] == room_q:
                return i
    return None


def main() -> None:
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=PAGE_LAYOUT,
        initial_sidebar_state="expanded",
    )
    st.markdown(streamlit_theme_css(), unsafe_allow_html=True)

    rooms = room_registry()
    room_labels = [f"{r['icon']}  {r['name']}" for r in rooms]
    label_to_id = {label: r["id"] for label, r in zip(room_labels, rooms)}

    branch = _git_branch()
    phase = _phase_label()

    initial_index = _resolve_room_from_query_or_state(rooms) or 0

    with st.sidebar:
        st.markdown(
            f"""
            <div style="
                font-family: {FONT_FAMILY_DISPLAY};
                font-size: {FONT_SIZE_HEADING_3};
                font-weight: 600;
                margin-bottom: 0.2rem;
            ">{PAGE_TITLE}</div>
            <div style="
                font-family: {FONT_FAMILY_MONO};
                font-size: {FONT_SIZE_DETAIL};
                color: {COLOR_TEXT_MUTED};
                letter-spacing: 0.06em;
                text-transform: uppercase;
                margin-bottom: 1.2rem;
            ">{phase} · {branch}</div>
            """,
            unsafe_allow_html=True,
        )
        choice = st.radio(
            "rooms",
            options=room_labels,
            index=initial_index,
            label_visibility="collapsed",
            key="control_room_radio",
        )
        # Refresh control + auto-refresh selector. The refresh button
        # invalidates Streamlit caches and reruns; auto-refresh wires the
        # native st.autorefresh helper at user-chosen intervals so the
        # dashboard updates live as agents touch the heartbeat ledger.
        st.markdown(
            '<div style="margin-top:1rem;padding-top:0.8rem;border-top:1px solid #283042;">'
            '<div style="font-family:var(--font-mono);font-size:0.7rem;color:var(--fg4);'
            'text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">refresh</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        refresh_cols = st.columns([1, 1])
        with refresh_cols[0]:
            if st.button("↻ refresh", key="control_room_refresh_button", use_container_width=True):
                st.rerun()
        with refresh_cols[1]:
            interval_label = st.selectbox(
                "live every",
                options=["off", "5s", "15s", "1m", "5m"],
                index=2,
                key="control_room_refresh_interval",
                label_visibility="collapsed",
            )
        interval_seconds = {"off": 0, "5s": 5, "15s": 15, "1m": 60, "5m": 300}.get(interval_label, 0)
        if interval_seconds > 0:
            try:
                # Streamlit ≥ 1.30 ships st.fragment / st.autorefresh; older
                # versions fall back gracefully to manual refresh only.
                if hasattr(st, "autorefresh"):
                    st.autorefresh(interval=interval_seconds * 1000, key="control_room_autorefresh")
            except Exception:
                pass

        # Heartbeat panel — shows which AI agents are currently active.
        # Every agent in the canonical roster appears with a status dot
        # (active pulses; stale = forgot to mark exit; departed; quiet).
        render_heartbeat_panel()

        st.markdown(
            f"""
            <div style="
                margin-top: 1.4rem;
                padding-top: 1rem;
                border-top: 1px solid #283042;
                font-size: {FONT_SIZE_LABEL};
                color: {COLOR_TEXT_SECONDARY};
            ">
            <strong>read-only sidecar.</strong><br/>
            D22 binding: empty rooms over mock data.<br/>
            <span style="color: {COLOR_TEXT_MUTED}; font-size: {FONT_SIZE_DETAIL};">
              writes restricted to <code>cache/</code>, <code>snapshots/</code>, <code>portfolio/</code>
            </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    selected_id = label_to_id[choice]
    render_room(selected_id)

    # Snapshot endpoint — write a structured digest after each render so
    # fresh AI agents (post-compaction Architect Claude, fresh Codex 1.5x,
    # etc.) can read state via a single file. Failures here must not
    # break the dashboard render; we swallow with a sidebar-foot note.
    try:
        snapshot_path = write_snapshot()
        # Render a discreet footer pointing to the snapshot, so consumers
        # know where to look without scanning the source.
        with st.sidebar:
            relative = snapshot_path.name
            st.markdown(
                f"""
                <div style="
                    margin-top: 1rem;
                    font-family: {FONT_FAMILY_MONO};
                    font-size: {FONT_SIZE_DETAIL};
                    color: {COLOR_TEXT_MUTED};
                    letter-spacing: 0.04em;
                ">snapshot · {relative}</div>
                """,
                unsafe_allow_html=True,
            )
    except Exception as exc:  # noqa: BLE001 -- snapshot must not break render
        with st.sidebar:
            st.markdown(
                f'<div style="color: var(--warning); font-family: var(--font-mono); '
                f'font-size: var(--fs-detail);">snapshot write failed: {type(exc).__name__}</div>',
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
