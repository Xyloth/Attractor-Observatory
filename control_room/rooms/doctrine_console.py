"""Doctrine and Integrity Console — proposal §7.8.

Track the project's rules, doctrines, and guardrails. Wires doctrine
adapter (registry + DOCTRINE.md + per-rule files) and surfaces the
Class 1-12 mistake catalog watch list. Includes the Campaign 016
detector decline finding (96/96 declined at low-level primitives) as
a load-bearing signal per Campaign 016's interpretation note.
"""

from __future__ import annotations

from control_room.adapters import parse_doctrine, parse_factory_store
from control_room.components import (
    doctrine_tablet,
    metric_card,
    panel,
    render_empty_state,
    render_html,
    room_emblem,
    status_pill,
)


ROOM_ID = "doctrine_console"
ROOM_NAME = "Doctrine & Integrity Console"
ROOM_ICON = "📜"
ROOM_TAGLINE = "Rules, lints, audits — the discipline made visible."
ROOM_PHASE = "Phase 1"


# Frozen as of CB-005 (matches AI Operations Tower).
MISTAKE_CATALOG = [
    ("1", "Static-input contamination", "ratified", "Architect caught Campaign 002"),
    ("2", "Direction inversion", "ratified", "Architect caught TASK-008"),
    ("3", "Soft enforcement / strict display", "ratified", "Codex caught BLOCKER-SH3"),
    ("4", "Scenario-internal hardcoding", "ratified", "Architect caught TASK-016 → D14"),
    ("5", "Surface-coverage-without-substance", "ratified", "Architect caught Campaign 006 → D7"),
    ("6", "Engineered passing", "ratified", "Architect caught Campaign 010 → D9"),
    ("7", "Surface-labels-as-primitives", "ratified", "Architect caught TASK-022 → D10/D19"),
    ("8", "Abstract-scalar-standing-in", "ratified", "Codex caught W13 multiscale via BFG"),
    ("9", "Spec-detail mismatch", "ratified", "Codex caught Campaign 011 driver"),
    ("10", "Test-architecture / substrate-presence mismatch", "ratified after CB-001", "Claude Builder caught self"),
    ("11", "Categorical confound through pooling", "ratified after CODEX_AUDIT_002", "Codex caught Claude Builder"),
    ("12", "Decorative completeness", "candidate (D22 binding)", "Architect ratified D22 in CB-004"),
]


def render() -> None:
    import streamlit as st

    render_html(room_emblem(ROOM_NAME, ROOM_TAGLINE, ROOM_ID))

    doctrine = parse_doctrine()
    factory = parse_factory_store()

    cols = st.columns(4)
    if doctrine["status"] == "ok":
        n_registry = doctrine["data"]["registry_entry_count"]
        n_consolidated = doctrine["data"]["consolidated_entry_count"]
        n_per_rule = len(doctrine["data"]["per_rule_files"])
    else:
        n_registry = n_consolidated = n_per_rule = 0
    with cols[0]:
        render_html(metric_card("registry rows", str(n_registry), "verified" if n_registry else "unavailable", "docs/doctrine_registry.json"))
    with cols[1]:
        render_html(metric_card("consolidated headings", str(n_consolidated), "verified" if n_consolidated else "unavailable", "docs/DOCTRINE.md"))
    with cols[2]:
        render_html(metric_card("per-rule files", str(n_per_rule), "verified" if n_per_rule else "unavailable", "docs/doctrine_d*.md"))
    with cols[3]:
        render_html(metric_card("mistake catalog", "12", "warning", "Class 1-11 ratified · Class 12 candidate"))

    # Doctrine registry cards
    st.markdown('<span class="cap">doctrine registry · D7 — D22</span>', unsafe_allow_html=True)
    if doctrine["status"] != "ok":
        render_empty_state(reason=doctrine["rationale"], expected_artifact="docs/doctrine_registry.json")
    else:
        items_html = ""
        for entry in doctrine["data"]["registry"]:
            items_html += doctrine_tablet(
                doctrine_id=entry.get("id", "?"),
                title=entry.get("path", "—").replace("docs\\\\", "").replace("\\\\", "/"),
                status=entry.get("mode", "foundational"),
                signed_by=entry.get("signed_by", ""),
            )
        render_html(panel(f"{n_registry} registry entries", items_html))

    # Consolidated headings (DOCTRINE.md)
    if doctrine["status"] == "ok" and doctrine["data"].get("consolidated_entries"):
        st.markdown('<span class="cap">consolidated index · DOCTRINE.md</span>', unsafe_allow_html=True)
        items_html = ""
        for entry in doctrine["data"]["consolidated_entries"]:
            items_html += doctrine_tablet(
                doctrine_id=entry["id"],
                title=entry["heading"],
                status="foundational",
                signed_by="DOCTRINE.md index",
            )
        render_html(panel(f"{n_consolidated} headings (consolidated)", items_html))

    # Mistake catalog
    st.markdown('<span class="cap">mistake catalog · class 1 — 12</span>', unsafe_allow_html=True)
    rows_html = ""
    for cls_id, name, status, origin in MISTAKE_CATALOG:
        accent = "var(--warning)" if "candidate" in status else "var(--verified)"
        rows_html += (
            '<div style="display:grid;grid-template-columns:60px 1fr 220px 220px;align-items:center;gap:10px;'
            f'padding:8px 0;border-bottom:1px dashed var(--border);">'
            f'<span style="font-family:var(--font-mono);font-size:1rem;color:{accent};font-weight:600;">{cls_id}</span>'
            f'<span style="font-family:var(--font-body);color:var(--fg1);">{name}</span>'
            f'<span class="cap" style="color:var(--fg4);">{status}</span>'
            f'<span class="cap" style="color:var(--fg4);">{origin}</span>'
            '</div>'
        )
    render_html(panel("classes 1-12 (Class 12 on watch per D22)", rows_html))

    # Campaign 016 detector decline as load-bearing signal
    st.markdown('<span class="cap">campaign 016 detector decline · honest signal</span>', unsafe_allow_html=True)
    if factory["status"] == "ok":
        intake = factory["data"].get("intake_dock_state") or {}
        intake_data = intake.get("data") or {}
        ds = intake_data.get("detector_summary") if isinstance(intake_data, dict) else {}
        if ds:
            declined = ds.get("declined_count", 0)
            evals = ds.get("evaluation_count", 0)
            interpretation = ds.get("interpretation", "—")
            body_html = (
                '<div style="display:grid;grid-template-columns:120px 1fr;gap:14px;align-items:center;">'
                f'<div style="font-family:var(--font-mono);font-size:2.4rem;color:var(--warning);font-weight:600;">'
                f'{declined}/{evals}</div>'
                f'<div style="font-family:var(--font-body);font-size:var(--fs-body);color:var(--fg2);">'
                f'<b>Detector decline rate at low-level primitives.</b><br>'
                f'{interpretation}</div>'
                '</div>'
                '<div style="margin-top:12px;padding:10px;background:var(--warning-soft);border-left:2px solid var(--warning);'
                'border-radius:6px;font-family:var(--font-mono);font-size:var(--fs-detail);color:var(--fg2);">'
                "D17 binding: floor falsifiers are publishable. The 96/96 decline is rendered as load-bearing "
                "signal per Campaign 016 interpretation note — not a failure to suppress."
                '</div>'
            )
            render_html(panel("low-level detector coverage · honest signal", body_html))
        else:
            render_empty_state(
                reason="Campaign 016 intake_dock_state has no detector_summary",
                expected_artifact="reports/campaign_016/factory_intake_dock_state.json with detector_summary",
            )
    else:
        render_empty_state(reason=factory["rationale"], expected_artifact="reports/campaign_016/factory_store/")
