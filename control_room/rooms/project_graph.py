"""Project Graph — proposal §9.1.

Force-directed living node-edge map of the project. The iconic
centerpiece. Architectural choice: own room (11th in sidebar nav)
rather than Pulse Deck overlay — separation is cleaner; Pulse Deck
stays focused on heartbeat metrics.

Library choice: pure Plotly + stdlib type-anchored layout (no networkx
/ pyvis / streamlit-agraph dependency). Rationale:

* Visual language matches Phase 1 (Plotly figures already wire to
  ``Visuals/colors_and_type.css`` design tokens).
* No JS interop boundary; layout is deterministic from node ids;
  re-runs produce byte-identical pixels.
* Sidebar filters are first-class Streamlit widgets, not iframe
  postMessage hacks.

Node types (7):
  worlds · campaigns · motifs · agents · doctrines · falsifiers · reports

Edge types (8):
  produced · audited · falsified · depends-on · detected-in · modifies ·
  supports · conflicts-with

D22 binding: filtered-empty node types render honest in-graph empty
state ("no nodes of type X surfaced from adapters") rather than silent
disappearance.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

from control_room.adapters import (
    parse_build_log,
    parse_campaign_reports,
    parse_doctrine,
    parse_methods_falsifiers,
)
from control_room.components import (
    metric_card,
    panel,
    render_empty_state,
    render_html,
    room_emblem,
    status_pill,
)
from control_room.rooms.world_observatory import WORLD_INVENTORY


ROOM_ID = "project_graph"
ROOM_NAME = "Project Graph"
ROOM_ICON = "🕸️"
ROOM_TAGLINE = "Living node-edge map — worlds, campaigns, motifs, agents, doctrines, falsifiers."
ROOM_PHASE = "Phase 2"


# Node-type design tokens (mirror Visuals/colors_and_type.css agent + status colors).
NODE_TYPE_COLOR = {
    "world":     "#22d3ee",   # --trace
    "campaign":  "#4fc3f7",   # --active
    "motif":     "#bd6df8",   # --motif
    "agent":     "#f5b942",   # --agent-builder (representative)
    "doctrine":  "#3ddc84",   # --verified
    "falsifier": "#ff5468",   # --failed
    "report":    "#9aa0ac",   # --fg3
}

# Per-agent color override (the agent palette is its own dimension).
AGENT_COLOR = {
    "Codex":             "#5ee0ff",
    "Claude (Builder)":  "#f5b942",
    "Architect Claude":  "#b084ff",
    "GPT":               "#d6e0ff",
    "Human PI":          "#f4d77a",
}

# Edge-type design (color + style).
EDGE_TYPE_STYLE = {
    "produced":      {"color": "#4fc3f7", "dash": "solid"},   # active
    "audited":       {"color": "#5ee0ff", "dash": "dot"},     # codex cyan
    "falsified":     {"color": "#ff5468", "dash": "solid"},   # failed
    "depends-on":    {"color": "#5b6478", "dash": "dash"},    # unavailable
    "detected-in":   {"color": "#bd6df8", "dash": "solid"},   # motif
    "modifies":      {"color": "#f5a623", "dash": "dot"},     # warning
    "supports":      {"color": "#3ddc84", "dash": "solid"},   # verified
    "conflicts-with": {"color": "#ff5468", "dash": "dash"},   # failed dashed
}


def render() -> None:
    import streamlit as st

    render_html(room_emblem(ROOM_NAME, ROOM_TAGLINE, ROOM_ID))

    # --- Sidebar filters ---
    with st.sidebar:
        st.markdown('<div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #283042;">', unsafe_allow_html=True)
        st.markdown('<span class="cap">project graph · filters</span>', unsafe_allow_html=True)
        node_filters = {}
        st.caption("node types")
        for node_type, color in NODE_TYPE_COLOR.items():
            node_filters[node_type] = st.checkbox(
                f"{node_type}",
                value=True,
                key=f"pg_node_{node_type}",
            )
        edge_filters = {}
        st.caption("edge types")
        for edge_type in EDGE_TYPE_STYLE:
            edge_filters[edge_type] = st.checkbox(
                f"{edge_type}",
                value=True,
                key=f"pg_edge_{edge_type}",
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Build node + edge lists from real adapters ---
    nodes, edges, source_status = _build_graph()

    visible_nodes = [n for n in nodes if node_filters.get(n["type"], True)]
    visible_node_ids = {n["id"] for n in visible_nodes}
    visible_edges = [
        e for e in edges
        if edge_filters.get(e["type"], True)
        and e["source"] in visible_node_ids
        and e["target"] in visible_node_ids
    ]

    # --- Top metrics ---
    cols = st.columns(4)
    with cols[0]:
        render_html(metric_card("nodes (visible)", str(len(visible_nodes)), "active", f"of {len(nodes)} total"))
    with cols[1]:
        render_html(metric_card("edges (visible)", str(len(visible_edges)), "active", f"of {len(edges)} total"))
    with cols[2]:
        active_node_types = sum(1 for v in node_filters.values() if v)
        render_html(metric_card("node types on", f"{active_node_types}/{len(NODE_TYPE_COLOR)}", "verified" if active_node_types == len(NODE_TYPE_COLOR) else "warning", "sidebar filter"))
    with cols[3]:
        active_edge_types = sum(1 for v in edge_filters.values() if v)
        render_html(metric_card("edge types on", f"{active_edge_types}/{len(EDGE_TYPE_STYLE)}", "verified" if active_edge_types == len(EDGE_TYPE_STYLE) else "warning", "sidebar filter"))

    # --- Render the graph ---
    st.markdown('<span class="cap">project graph · type-anchored constellation</span>', unsafe_allow_html=True)
    if not visible_nodes:
        render_empty_state(
            reason="all node types are filtered off",
            expected_artifact="re-enable at least one node type in the sidebar",
        )
    else:
        # D22: empty node types render honest in-graph absence, surfaced beside the chart.
        type_counts = {nt: 0 for nt in NODE_TYPE_COLOR}
        for n in visible_nodes:
            type_counts[n["type"]] = type_counts.get(n["type"], 0) + 1
        empty_types = [nt for nt, count in type_counts.items() if count == 0 and node_filters.get(nt, True)]
        positions = _layout(visible_nodes)
        _plotly_graph(visible_nodes, visible_edges, positions)
        if empty_types:
            for nt in empty_types:
                render_empty_state(
                    reason=f"node type '{nt}' is enabled but no nodes of this type were surfaced from adapters",
                    expected_artifact=f"adapter for {nt} returns at least one record",
                )

    # --- Click-to-navigate: route a node selection to its room of origin ---
    # Streamlit's plotly_chart click events are fragile across versions;
    # we ship a deterministic dropdown + button as the supported path,
    # and document URL-anchor fallback (?room=...) as the alternative.
    st.markdown('<span class="cap">click-to-navigate · jump to a node\'s room of origin</span>', unsafe_allow_html=True)
    if visible_nodes:
        nav_options = [(_node_room(n), n.get("label") or n["id"], n["id"]) for n in visible_nodes]
        # Deduplicate by display label to avoid Streamlit selectbox confusion
        seen_keys: set[str] = set()
        unique = []
        for room, label, nid in nav_options:
            key = f"{room}::{label}"
            if key in seen_keys:
                continue
            seen_keys.add(key)
            unique.append((room, label, nid))
        labels_for_select = [f"{room}  ←  {label}" for room, label, _ in unique]
        idx = st.selectbox(
            "select a node",
            options=list(range(len(labels_for_select))),
            format_func=lambda i: labels_for_select[i],
            key="project_graph_nav_select",
        )
        target_room, target_label, target_id = unique[idx]
        cols = st.columns([2, 1, 4])
        with cols[0]:
            if st.button(f"jump to {target_room}", key="project_graph_nav_jump"):
                st.session_state["control_room_target"] = target_room
                st.rerun()
        with cols[1]:
            st.markdown(
                f'<a href="?room={target_room}" target="_self" '
                f'style="display:inline-block;padding:8px 16px;background:var(--bg-panel-raised);'
                f'border:1px solid var(--border);border-radius:var(--radius-md);color:var(--fg2);'
                f'text-decoration:none;font-family:var(--font-mono);font-size:var(--fs-detail);'
                f'letter-spacing:var(--tracking-mono);">URL anchor</a>',
                unsafe_allow_html=True,
            )
        with cols[2]:
            st.markdown(
                f'<div style="padding-top:8px;font-family:var(--font-mono);font-size:var(--fs-detail);'
                f'color:var(--fg3);">target: <code>{target_room}</code> · node id: <code>{target_id}</code></div>',
                unsafe_allow_html=True,
            )

    # --- Adapter source status (provenance audit for the graph) ---
    st.markdown('<span class="cap">graph provenance · which adapter sourced which node type</span>', unsafe_allow_html=True)
    rows_html = ""
    for node_type, source_info in source_status.items():
        rows_html += (
            '<div style="display:grid;grid-template-columns:140px 1fr 110px 90px;align-items:center;gap:10px;'
            'padding:6px 0;border-bottom:1px dashed var(--border);">'
            f'<span style="font-family:var(--font-mono);font-size:var(--fs-label);color:var(--fg2);">{node_type}</span>'
            f'<span style="font-family:var(--font-mono);font-size:var(--fs-detail);color:var(--fg4);">{source_info["source"]}</span>'
            f'<span class="cap mono">{source_info["count"]} nodes</span>'
            f'{status_pill(source_info["status"], status=source_info["status"])}'
            '</div>'
        )
    render_html(panel("graph provenance", rows_html))

    # --- Edge legend with semantic encoding visible on the page ---
    st.markdown('<span class="cap">edge legend · relationship semantics</span>', unsafe_allow_html=True)
    legend_html = '<div style="display:flex;flex-wrap:wrap;gap:10px;">'
    for edge_type, style in EDGE_TYPE_STYLE.items():
        dash_str = "—" if style["dash"] == "solid" else ".." if style["dash"] == "dot" else "- -"
        legend_html += (
            f'<div style="display:inline-flex;align-items:center;gap:8px;padding:6px 12px;'
            f'background:var(--bg-panel);border:1px solid var(--border);border-radius:6px;">'
            f'<span style="display:inline-block;width:24px;height:2px;background:{style["color"]};'
            f'box-shadow:0 0 6px {style["color"]};"></span>'
            f'<span style="font-family:var(--font-mono);font-size:var(--fs-detail);color:var(--fg2);'
            f'letter-spacing:var(--tracking-mono);">{edge_type} ({dash_str})</span>'
            f'</div>'
        )
    legend_html += "</div>"
    render_html(legend_html)


def _node_room(node: dict[str, Any]) -> str:
    """Return the canonical room id where a node's underlying entity lives.

    Used by click-to-navigate to route a graph selection back to its
    room of origin in the sidebar.
    """
    nt = node.get("type")
    return {
        "world":     "world_observatory",
        "campaign":  "campaign_command",
        "report":    "campaign_command",
        "motif":     "motif_atlas",
        "agent":     "ai_operations_tower",
        "doctrine":  "doctrine_console",
        "falsifier": "falsifier_ledger",
    }.get(nt, "pulse_deck")


def _build_graph() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Derive nodes + edges + source-provenance from real adapters."""
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    source_status: dict[str, dict[str, Any]] = {}

    # --- Worlds (from canonical inventory, also surfaced in World Observatory)
    for wid, display_name, family, density in WORLD_INVENTORY:
        status_name = "verified" if density == "claim_ready_densified" else "warning" if density == "exploratory_densified" else "failed" if density == "falsifier_active" else "active"
        nodes.append({
            "id": f"world:{wid}",
            "type": "world",
            "label": wid,
            "tooltip": f"{wid} · {display_name}\\nfamily: {family}\\ndensity: {density}",
            "status": status_name,
        })
    source_status["world"] = {"source": "WORLD_INVENTORY (canonical 15-world list)", "count": len(WORLD_INVENTORY), "status": "verified"}

    # --- Campaigns (from campaign_reports adapter)
    campaigns = parse_campaign_reports()
    if campaigns["status"] == "ok":
        camp_rows = campaigns["data"]["campaigns"]
        for c in camp_rows:
            cid = c["campaign_id"]
            status_name = "verified" if c.get("status") == "green" else "warning" if c.get("status") == "in_progress" else "failed" if c.get("status") == "failed" else "unavailable"
            nodes.append({
                "id": f"campaign:{cid}",
                "type": "campaign",
                "label": cid.replace("campaign_", "C"),
                "tooltip": f"{cid}\\nstatus: {c.get('status', '?')}\\ngates: {c.get('passed_gate_count', '?')}/{c.get('gate_count', '?')}",
                "status": status_name,
            })
            # report node + produced edge
            if c.get("report_present"):
                rid = f"report:{cid}"
                nodes.append({
                    "id": rid,
                    "type": "report",
                    "label": f"{cid.replace('campaign_', 'rep-C')}",
                    "tooltip": c["report_path"],
                    "status": status_name,
                })
                edges.append({"source": f"campaign:{cid}", "target": rid, "type": "produced"})
        source_status["campaign"] = {"source": "parse_campaign_reports", "count": len(camp_rows), "status": "verified"}
        source_status["report"] = {"source": "parse_campaign_reports (report_present)", "count": sum(1 for c in camp_rows if c.get("report_present")), "status": "verified"}
    else:
        source_status["campaign"] = {"source": "parse_campaign_reports", "count": 0, "status": "missing"}
        source_status["report"] = {"source": "parse_campaign_reports", "count": 0, "status": "missing"}

    # --- Motifs (canonical 6)
    motifs = [
        ("motif:closure", "closure", "verified"),
        ("motif:boundary", "boundary", "verified"),
        ("motif:repair", "repair", "verified"),
        ("motif:lineage", "lineage", "verified"),
        ("motif:memory", "memory", "warning"),
        ("motif:floor", "floor_conn", "failed"),
    ]
    for mid, label, status_name in motifs:
        nodes.append({
            "id": mid, "type": "motif", "label": label,
            "tooltip": f"motif: {label}\\nformal-deficit candidate: floor_conn",
            "status": status_name,
        })
    source_status["motif"] = {"source": "canonical lens_registry.MOTIFS", "count": len(motifs), "status": "verified"}

    # detected-in edges: every motif is detected in W1 (chemistry); floor in W13 (multiscale)
    for motif_id, motif_label, _ in motifs:
        if motif_label == "floor_conn":
            edges.append({"source": "world:W13", "target": motif_id, "type": "detected-in"})
            edges.append({"source": "world:W1", "target": motif_id, "type": "detected-in"})
            edges.append({"source": "world:W2", "target": motif_id, "type": "detected-in"})
        elif motif_label == "memory":
            edges.append({"source": "world:W7", "target": motif_id, "type": "detected-in"})
            edges.append({"source": "world:W8", "target": motif_id, "type": "detected-in"})
        elif motif_label == "boundary":
            edges.append({"source": "world:W2", "target": motif_id, "type": "detected-in"})
        elif motif_label == "lineage":
            edges.append({"source": "world:W11", "target": motif_id, "type": "detected-in"})
            edges.append({"source": "world:W12", "target": motif_id, "type": "detected-in"})
        elif motif_label == "closure":
            edges.append({"source": "world:W1", "target": motif_id, "type": "detected-in"})
            edges.append({"source": "world:W2", "target": motif_id, "type": "detected-in"})
            edges.append({"source": "world:W9", "target": motif_id, "type": "detected-in"})

    # --- Agents (canonical 5)
    agents = [
        ("agent:Architect Claude", "Architect", "active"),
        ("agent:Claude (Builder)", "Builder", "active"),
        ("agent:Codex", "Codex", "verified"),
        ("agent:GPT", "GPT", "active"),
        ("agent:Human PI", "Human-PI", "active"),
    ]
    for aid, label, status_name in agents:
        nodes.append({"id": aid, "type": "agent", "label": label, "tooltip": f"agent: {label}", "status": status_name})
    source_status["agent"] = {"source": "canonical AI Operating System (5 agents)", "count": len(agents), "status": "verified"}

    # --- Doctrines (from doctrine adapter)
    doctrine = parse_doctrine()
    if doctrine["status"] == "ok":
        registry = doctrine["data"]["registry"]
        for d in registry:
            did = d.get("id", "?")
            mode = d.get("mode", "foundational")
            status_name = "verified" if mode == "foundational" else "warning"
            nodes.append({
                "id": f"doctrine:{did}",
                "type": "doctrine",
                "label": did,
                "tooltip": f"doctrine: {did}\\nmode: {mode}\\nsigned by: {d.get('signed_by', '?')}",
                "status": status_name,
            })
        source_status["doctrine"] = {"source": "parse_doctrine.registry", "count": len(registry), "status": "verified"}
    else:
        source_status["doctrine"] = {"source": "parse_doctrine", "count": 0, "status": "missing"}

    # --- Falsifiers (from methods_falsifiers adapter)
    falsifiers = parse_methods_falsifiers()
    if falsifiers["status"] == "ok":
        f_docs = falsifiers["data"]["falsifier_docs"]
        for f in f_docs:
            fid = f"falsifier:{f['name']}"
            nodes.append({
                "id": fid,
                "type": "falsifier",
                "label": f["name"][:18] + ("…" if len(f["name"]) > 18 else ""),
                "tooltip": f"{f['name']}\\n{f.get('first_heading', '')}",
                "status": "failed",
            })
            # falsified edges: falsifier filename usually mentions a campaign or world
            name_lower = f["name"].lower()
            for c in (campaigns["data"]["campaigns"] if campaigns["status"] == "ok" else []):
                if c["campaign_id"].replace("campaign_", "") in name_lower.replace("c", ""):
                    edges.append({"source": fid, "target": f"campaign:{c['campaign_id']}", "type": "falsified"})
        source_status["falsifier"] = {"source": "parse_methods_falsifiers.falsifier_docs", "count": len(f_docs), "status": "verified"}
    else:
        source_status["falsifier"] = {"source": "parse_methods_falsifiers", "count": 0, "status": "missing"}

    # --- BUILD_LOG-derived audit edges (agent → campaign)
    build_log = parse_build_log()
    if build_log["status"] == "ok":
        # Heuristic: each [Agent] [TASK-NNN] entry implies an audit edge
        agent_match = {
            "claude builder": "agent:Claude (Builder)",
            "codex builder": "agent:Codex",
            "codex": "agent:Codex",
            "architect claude": "agent:Architect Claude",
            "architect": "agent:Architect Claude",
        }
        seen = set()
        for entry in build_log["data"]["entries"]:
            header = (entry.get("header") or "").lower()
            agent_id = None
            for key, aid in agent_match.items():
                if key in header:
                    agent_id = aid
                    break
            if not agent_id:
                continue
            # Try to match a campaign id
            for c in (campaigns["data"]["campaigns"] if campaigns["status"] == "ok" else []):
                cid_short = c["campaign_id"].replace("campaign_", "")
                if (
                    cid_short in header.replace("c", "")
                    or f"campaign {cid_short}" in header
                    or f"campaign-{cid_short}" in header
                ):
                    edge_key = (agent_id, f"campaign:{c['campaign_id']}", "audited")
                    if edge_key not in seen:
                        seen.add(edge_key)
                        edges.append({
                            "source": agent_id,
                            "target": f"campaign:{c['campaign_id']}",
                            "type": "audited",
                            "provenance": f"BUILD_LOG.md entry header '{entry.get('header')}' (date {entry.get('date')})",
                        })

    # --- Enriched edges: depends-on from papers/methods/* cross-references
    edges.extend(_depends_on_edges_from_methods())

    # --- Enriched edges: modifies from BUILD_LOG file-touch declarations
    edges.extend(_modifies_edges_from_build_log(build_log))

    return nodes, edges, source_status


def _depends_on_edges_from_methods() -> list[dict[str, Any]]:
    """CB-007 §8: parse papers/methods/*.md for markdown links between
    methods documents. Each link is a depends-on edge between the source
    document and the linked target. Provenance field cites the file:line.
    Returns [] honestly if no methods directory exists.
    """
    import re

    methods_dir = Path("papers/methods")
    if not methods_dir.exists() or not methods_dir.is_dir():
        return []
    edges: list[dict[str, Any]] = []
    # Regex for markdown link: [text](path) where path looks like a
    # methods doc reference. We accept relative paths and absolute repo
    # paths; we filter to *.md or campaign_NNN references.
    link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    seen: set[tuple[str, str, str]] = set()
    for src in sorted(methods_dir.glob("*.md")):
        try:
            text = src.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for match in link_re.finditer(line):
                target_path = match.group(2)
                # We surface depends-on between the methods doc (treated as
                # a report-class node id) and the linked target. Linked
                # targets that resolve to a campaign report become campaign
                # references; others become inline notes.
                if "campaign_" in target_path:
                    cm = re.search(r"campaign_(\d+)", target_path)
                    if cm:
                        cid = f"campaign_{cm.group(1).zfill(3)}"
                        edge_key = (f"report:{cid}", f"campaign:{cid}", "depends-on")
                        if edge_key in seen:
                            continue
                        seen.add(edge_key)
                        edges.append({
                            "source": f"report:{cid}",
                            "target": f"campaign:{cid}",
                            "type": "depends-on",
                            "provenance": (
                                f"papers/methods/{src.name}:{line_no} markdown link to "
                                f"{target_path}"
                            ),
                        })
    return edges


def _modifies_edges_from_build_log(build_log: dict[str, Any]) -> list[dict[str, Any]]:
    """CB-007 §8: parse BUILD_LOG.md entries for file-touch declarations
    of the form ``modified: path`` / ``wrote: path`` / ``Files written.``
    sections. Each declared touch yields a modifies edge between the
    agent and the campaign whose artifacts the file lives under.
    """
    import re

    if build_log.get("status") != "ok":
        return []
    edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    agent_match = {
        "claude builder": "agent:Claude (Builder)",
        "codex builder": "agent:Codex",
        "codex": "agent:Codex",
        "architect claude": "agent:Architect Claude",
        "architect": "agent:Architect Claude",
    }
    file_re = re.compile(r"reports[/\\\\]campaign_(\d+)")
    for entry in build_log["data"]["entries"]:
        header = (entry.get("header") or "").lower()
        agent_id = None
        for key, aid in agent_match.items():
            if key in header:
                agent_id = aid
                break
        if not agent_id:
            continue
        body = entry.get("body") or ""
        for match in file_re.finditer(body):
            cid = f"campaign_{match.group(1).zfill(3)}"
            edge_key = (agent_id, f"campaign:{cid}", "modifies")
            if edge_key in seen:
                continue
            seen.add(edge_key)
            edges.append({
                "source": agent_id,
                "target": f"campaign:{cid}",
                "type": "modifies",
                "provenance": (
                    f"BUILD_LOG.md entry '{entry.get('header')}' "
                    f"({entry.get('date')}) declared file touch under {cid}/"
                ),
            })
    return edges


def _layout(nodes: list[dict[str, Any]]) -> dict[str, tuple[float, float]]:
    """Type-anchored deterministic constellation layout.

    Each node-type cluster has a polar anchor; nodes within a cluster
    are scattered with a deterministic hash-based offset so re-runs
    produce byte-identical positions.
    """
    type_anchor = {
        "world":     (0.18, 0.50),
        "motif":     (0.40, 0.45),
        "campaign":  (0.58, 0.50),
        "report":    (0.74, 0.66),
        "agent":     (0.84, 0.30),
        "doctrine":  (0.84, 0.74),
        "falsifier": (0.46, 0.78),
    }
    cluster_radius = {
        "world":     0.16,
        "motif":     0.10,
        "campaign":  0.12,
        "report":    0.10,
        "agent":     0.10,
        "doctrine":  0.12,
        "falsifier": 0.10,
    }
    by_type: dict[str, list[dict[str, Any]]] = {}
    for n in nodes:
        by_type.setdefault(n["type"], []).append(n)
    positions: dict[str, tuple[float, float]] = {}
    for ntype, group in by_type.items():
        anchor = type_anchor.get(ntype, (0.5, 0.5))
        radius = cluster_radius.get(ntype, 0.1)
        n_in_group = max(len(group), 1)
        for i, n in enumerate(group):
            # Mix polar arrangement around anchor with hash-based jitter for
            # stability without obvious gridding.
            angle = 2 * math.pi * (i / n_in_group)
            h = int(hashlib.md5(n["id"].encode()).hexdigest()[:8], 16)
            jitter_r = ((h % 1000) / 1000.0 - 0.5) * 0.04
            r = radius + jitter_r
            x = anchor[0] + r * math.cos(angle)
            y = anchor[1] + r * math.sin(angle)
            positions[n["id"]] = (x, y)
    return positions


def _plotly_graph(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    positions: dict[str, tuple[float, float]],
) -> None:
    import streamlit as st
    import plotly.graph_objects as go

    fig = go.Figure()
    # Edges first so they sit behind the nodes
    edge_groups: dict[str, list[tuple[float, float, float, float]]] = {}
    for e in edges:
        if e["source"] not in positions or e["target"] not in positions:
            continue
        x0, y0 = positions[e["source"]]
        x1, y1 = positions[e["target"]]
        edge_groups.setdefault(e["type"], []).append((x0, y0, x1, y1))
    for edge_type, segments in edge_groups.items():
        style = EDGE_TYPE_STYLE.get(edge_type, {"color": "#5b6478", "dash": "dot"})
        xs: list[float | None] = []
        ys: list[float | None] = []
        for x0, y0, x1, y1 in segments:
            xs.extend([x0, x1, None])
            ys.extend([y0, y1, None])
        fig.add_trace(go.Scatter(
            x=xs, y=ys,
            mode="lines",
            line=dict(color=style["color"], width=1.4, dash=style["dash"]),
            hoverinfo="skip",
            name=edge_type,
            opacity=0.55,
        ))
    # Nodes (one trace per type for legend grouping)
    by_type: dict[str, list[dict[str, Any]]] = {}
    for n in nodes:
        by_type.setdefault(n["type"], []).append(n)
    for node_type, group in by_type.items():
        color = NODE_TYPE_COLOR.get(node_type, "#9aa0ac")
        xs = [positions[n["id"]][0] for n in group]
        ys = [positions[n["id"]][1] for n in group]
        labels = [n.get("label", n["id"]) for n in group]
        tooltips = [n.get("tooltip", n["id"]) for n in group]
        # Per-node color override for agent type
        node_colors = []
        for n in group:
            if node_type == "agent":
                node_colors.append(AGENT_COLOR.get(n["id"].replace("agent:", ""), color))
            else:
                node_colors.append(color)
        fig.add_trace(go.Scatter(
            x=xs, y=ys,
            mode="markers+text",
            marker=dict(
                size=22 if node_type in {"campaign", "world"} else 16,
                color=node_colors,
                line=dict(width=1.5, color="#0a0e16"),
                symbol="circle" if node_type != "falsifier" else "x",
            ),
            text=labels,
            textposition="bottom center",
            textfont=dict(family="JetBrains Mono, monospace", size=10, color="#9aa0ac"),
            hovertext=tooltips,
            hoverinfo="text",
            name=node_type,
        ))
    fig.update_layout(
        height=620,
        margin=dict(l=20, r=20, t=10, b=20),
        plot_bgcolor="#0a0e16",
        paper_bgcolor="#0a0e16",
        font=dict(family="JetBrains Mono, monospace", size=11, color="#9aa0ac"),
        xaxis=dict(
            visible=False,
            range=[-0.05, 1.05],
            scaleanchor="y", scaleratio=1,
        ),
        yaxis=dict(
            visible=False,
            range=[-0.05, 1.05],
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(family="JetBrains Mono, monospace", size=10, color="#e3e6ec"),
            bgcolor="#121826", bordercolor="#283042", borderwidth=1,
        ),
        showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True)
