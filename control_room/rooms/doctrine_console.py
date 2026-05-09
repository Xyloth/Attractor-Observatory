"""Doctrine and Integrity Console.

Tracks the project's doctrine registry, consolidated doctrine index, and
canonical mistake-catalog registry. DX-003 made the mistake catalog registry
the single source of truth for Class 1-13 status.
"""

from __future__ import annotations

from control_room.adapters import parse_doctrine, parse_factory_store, parse_mistake_catalog
from control_room.components import (
    doctrine_tablet,
    metric_card,
    panel,
    render_empty_state,
    render_html,
    room_emblem,
)


ROOM_ID = "doctrine_console"
ROOM_NAME = "Doctrine & Integrity Console"
ROOM_ICON = "DOC"
ROOM_TAGLINE = "Rules, lints, audits - the discipline made visible."
ROOM_PHASE = "Phase 1"


def render() -> None:
    import streamlit as st

    render_html(room_emblem(ROOM_NAME, ROOM_TAGLINE, ROOM_ID))

    doctrine = parse_doctrine()
    factory = parse_factory_store()
    mistakes = parse_mistake_catalog()

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
        if mistakes["status"] == "ok":
            md = mistakes["data"]
            render_html(metric_card(
                "mistake catalog",
                str(md["class_count"]),
                "verified",
                f"{md['ratified_count']} ratified - registry-bound",
            ))
        else:
            render_html(metric_card("mistake catalog", "0", "unavailable", mistakes["rationale"]))

    st.markdown('<span class="cap">doctrine registry - D7-D31</span>', unsafe_allow_html=True)
    if doctrine["status"] != "ok":
        render_empty_state(reason=doctrine["rationale"], expected_artifact="docs/doctrine_registry.json")
    else:
        items_html = ""
        for entry in doctrine["data"]["registry"]:
            items_html += doctrine_tablet(
                doctrine_id=entry.get("id", "?"),
                title=entry.get("path", "-").replace("docs\\\\", "").replace("\\\\", "/"),
                status=entry.get("mode", "foundational"),
                signed_by=entry.get("signed_by", ""),
            )
        render_html(panel(f"{n_registry} registry entries", items_html))

    if doctrine["status"] == "ok" and doctrine["data"].get("consolidated_entries"):
        st.markdown('<span class="cap">consolidated index - DOCTRINE.md</span>', unsafe_allow_html=True)
        items_html = ""
        for entry in doctrine["data"]["consolidated_entries"]:
            items_html += doctrine_tablet(
                doctrine_id=entry["id"],
                title=entry["heading"],
                status="foundational",
                signed_by="DOCTRINE.md index",
            )
        render_html(panel(f"{n_consolidated} headings (consolidated)", items_html))

    st.markdown('<span class="cap">mistake catalog - registry-bound classes</span>', unsafe_allow_html=True)
    if mistakes["status"] != "ok":
        render_empty_state(reason=mistakes["rationale"], expected_artifact="docs/mistake_catalog_registry.json")
    else:
        rows_html = ""
        for entry in mistakes["data"]["classes"]:
            status = entry.get("status", "unknown")
            accent = "var(--warning)" if status == "candidate" else "var(--verified)"
            rows_html += (
                '<div style="display:grid;grid-template-columns:80px 1fr 150px 260px;align-items:center;gap:10px;'
                'padding:8px 0;border-bottom:1px dashed var(--border);">'
                f'<span style="font-family:var(--font-mono);font-size:1rem;color:{accent};font-weight:600;">{entry.get("id", "?")}</span>'
                f'<span style="font-family:var(--font-body);color:var(--fg1);">{entry.get("title", "-")}</span>'
                f'<span class="cap" style="color:var(--fg4);">{status}</span>'
                f'<span class="cap" style="color:var(--fg4);">{entry.get("ratification_source", "-")}</span>'
                '</div>'
            )
        render_html(panel(
            f"{mistakes['data']['class_count']} classes from docs/mistake_catalog_registry.json",
            rows_html,
        ))

    st.markdown('<span class="cap">campaign 016 detector decline - honest signal</span>', unsafe_allow_html=True)
    if factory["status"] == "ok":
        intake = factory["data"].get("intake_dock_state") or {}
        intake_data = intake.get("data") or {}
        ds = intake_data.get("detector_summary") if isinstance(intake_data, dict) else {}
        if ds:
            declined = ds.get("declined_count", 0)
            evals = ds.get("evaluation_count", 0)
            interpretation = ds.get("interpretation", "-")
            body_html = (
                '<div style="display:grid;grid-template-columns:120px 1fr;gap:14px;align-items:center;">'
                f'<div style="font-family:var(--font-mono);font-size:2.4rem;color:var(--warning);font-weight:600;">'
                f'{declined}/{evals}</div>'
                f'<div style="font-family:var(--font-body);font-size:var(--fs-body);color:var(--fg2);">'
                f'<b>Detector decline rate at low-level primitives.</b><br>{interpretation}</div>'
                '</div>'
                '<div style="margin-top:12px;padding:10px;background:var(--warning-soft);border-left:2px solid var(--warning);'
                'border-radius:6px;font-family:var(--font-mono);font-size:var(--fs-detail);color:var(--fg2);">'
                "D17 binding: floor falsifiers are publishable. The 96/96 decline is rendered as load-bearing "
                "signal per Campaign 016 interpretation note - not a failure to suppress."
                '</div>'
            )
            render_html(panel("low-level detector coverage - honest signal", body_html))
        else:
            render_empty_state(
                reason="Campaign 016 intake_dock_state has no detector_summary",
                expected_artifact="reports/campaign_016/factory_intake_dock_state.json with detector_summary",
            )
    else:
        render_empty_state(reason=factory["rationale"], expected_artifact="reports/campaign_016/factory_store/")
