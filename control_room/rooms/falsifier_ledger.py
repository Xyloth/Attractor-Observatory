"""Falsifier and Negative-Space Ledger — proposal §7.7.

Make failure visible and valuable. Wires methods_falsifiers (falsifier
doc index) and negative_space (atlas/negative_space index) adapters.

Per proposal §7.7: this room is culturally important. The project
should look proud of honest failures. D17 (floor falsifiers are
publishable) binds.
"""

from __future__ import annotations

from control_room.adapters import parse_methods_falsifiers, parse_negative_space
from control_room.components import (
    metric_card,
    panel,
    render_empty_state,
    render_html,
    room_emblem,
    status_pill,
)


ROOM_ID = "falsifier_ledger"
ROOM_NAME = "Falsifier & Negative-Space Ledger"
ROOM_ICON = "🛑"
ROOM_TAGLINE = "Honest failures, downgraded claims, structural absences."
ROOM_PHASE = "Phase 1"


def render() -> None:
    import streamlit as st

    render_html(room_emblem(ROOM_NAME, ROOM_TAGLINE, ROOM_ID))

    falsifiers = parse_methods_falsifiers()
    negative_space = parse_negative_space()

    # Top metrics
    cols = st.columns(3)
    n_falsifiers = falsifiers["data"]["falsifier_doc_count"] if falsifiers["status"] == "ok" else 0
    n_methods = falsifiers["data"]["method_doc_count"] if falsifiers["status"] == "ok" else 0
    n_negative = negative_space["data"]["entry_count"] if negative_space["status"] == "ok" else 0
    with cols[0]:
        render_html(metric_card(
            "falsifier records",
            str(n_falsifiers),
            "failed" if n_falsifiers > 0 else "verified",
            "papers/falsifiers/",
        ))
    with cols[1]:
        render_html(metric_card(
            "methods documents",
            str(n_methods),
            "active" if n_methods > 0 else "unavailable",
            "papers/methods/",
        ))
    with cols[2]:
        render_html(metric_card(
            "negative-space entries",
            str(n_negative),
            "warning" if n_negative > 0 else "verified",
            "atlas/negative_space/",
        ))

    # Falsifier timeline
    st.markdown('<span class="cap">falsifier timeline · papers/falsifiers/</span>', unsafe_allow_html=True)
    if falsifiers["status"] != "ok":
        render_empty_state(reason=falsifiers["rationale"], expected_artifact="papers/falsifiers/*.md")
    elif n_falsifiers == 0:
        render_empty_state(
            reason="no falsifier records present (papers/falsifiers/ is empty)",
            expected_artifact="papers/falsifiers/*.md per D17",
        )
    else:
        rows_html = ""
        for d in falsifiers["data"]["falsifier_docs"]:
            heading = d.get("first_heading") or d["name"]
            rows_html += (
                '<div style="display:grid;grid-template-columns:300px 1fr 110px;align-items:center;gap:10px;'
                'padding:8px 0;border-bottom:1px dashed var(--border);">'
                f'<span style="font-family:var(--font-mono);font-size:var(--fs-label);color:var(--fg2);">{d["name"]}</span>'
                f'<span style="font-family:var(--font-body);font-size:var(--fs-body);color:var(--fg2);">{heading}</span>'
                f'{status_pill("published", status="failed")}'
                "</div>"
            )
        render_html(panel(f"{n_falsifiers} falsifier records · this failed honestly", rows_html))

    # Negative-space registry
    st.markdown('<span class="cap">negative-space registry · atlas/negative_space/</span>', unsafe_allow_html=True)
    if negative_space["status"] != "ok":
        render_empty_state(reason=negative_space["rationale"], expected_artifact="atlas/negative_space/*.md")
    elif n_negative == 0:
        render_empty_state(
            reason="no negative-space entries present",
            expected_artifact="atlas/negative_space/*.md (honest absences catalog)",
        )
    else:
        rows_html = ""
        for d in negative_space["data"]["entries"]:
            heading = d.get("first_heading") or d["name"]
            rows_html += (
                '<div style="display:grid;grid-template-columns:280px 1fr 110px;align-items:center;gap:10px;'
                'padding:8px 0;border-bottom:1px dashed var(--border);">'
                f'<span style="font-family:var(--font-mono);font-size:var(--fs-label);color:var(--fg2);">{d["name"]}</span>'
                f'<span style="font-family:var(--font-body);font-size:var(--fs-body);color:var(--fg2);">{heading}</span>'
                f'{status_pill("absence", status="warning")}'
                "</div>"
            )
        render_html(panel(f"{n_negative} negative-space entries", rows_html))

    # Methods documents (the audit + truth-pass + substance-audit pile)
    st.markdown('<span class="cap">methods documents · papers/methods/</span>', unsafe_allow_html=True)
    if falsifiers["status"] != "ok":
        render_empty_state(reason=falsifiers["rationale"], expected_artifact="papers/methods/*.md")
    elif n_methods == 0:
        render_empty_state(
            reason="no methods documents present",
            expected_artifact="papers/methods/*.md (Truth Pass, Substance Audits, methods docs)",
        )
    else:
        rows_html = ""
        for d in falsifiers["data"]["method_docs"]:
            heading = d.get("first_heading") or d["name"]
            kind = "truth-pass" if "truth" in d["name"].lower() else (
                "substance-audit" if "substance" in d["name"].lower() else "methods"
            )
            rows_html += (
                '<div style="display:grid;grid-template-columns:340px 1fr 130px;align-items:center;gap:10px;'
                'padding:6px 0;border-bottom:1px dashed var(--border);">'
                f'<span style="font-family:var(--font-mono);font-size:var(--fs-label);color:var(--fg2);">{d["name"]}</span>'
                f'<span style="font-family:var(--font-body);font-size:var(--fs-body);color:var(--fg2);">{heading[:80]}</span>'
                f'{status_pill(kind, status="active")}'
                "</div>"
            )
        render_html(panel(f"{n_methods} methods records", rows_html))
