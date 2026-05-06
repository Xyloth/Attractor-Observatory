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

    # CB-009 T1 — Atlas Periodic Table view (motif × world matrix).
    # The pre-existing motif × lens heatmap below stays as the formalism
    # diagnostic; the periodic table is a substrate-coverage view.
    st.markdown('<span class="cap">atlas periodic table · motif × world detection state</span>', unsafe_allow_html=True)
    _render_periodic_table()

    # Motif × world matrix (proposal §9.5 motif embedding) — formal
    # lens × motif coverage retained as a separate diagnostic surface.
    st.markdown('<span class="cap">motif × lens coverage (formal)</span>', unsafe_allow_html=True)
    if campaigns["status"] != "ok":
        render_empty_state(
            reason="campaign reports unavailable; cannot derive motif × lens coverage",
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


# ---------------------------------------------------------------------------
# CB-009 T1 — Atlas Periodic Table (motif × world detection-state matrix)
# ---------------------------------------------------------------------------

# Reuse the canonical 15-world inventory from the World Observatory so the
# Atlas matrix and the World room agree on row order, world ids, and
# display names. Tuple shape: (world_id, display_name, world_family).
_WORLD_AXIS = [
    ("W-1", "Atomic / Molecular", "atomic_molecular"),
    ("W0",  "Math primitives",    "math_primitives"),
    ("W1",  "Chemistry / RAFs",   "crn"),
    ("W2",  "Protocell",          "protocell"),
    ("W3",  "Reaction-diffusion", "field"),
    ("W4",  "Morphogenesis",      "morphogenesis"),
    ("W5",  "Digital",            "digital"),
    ("W6",  "Ecosystem",          "ecosystem"),
    ("W7",  "Swarm",              "swarm"),
    ("W8",  "Cognitive",          "cognitive"),
    ("W9",  "Origins chemistry",  "origins_chemistry"),
    ("W10", "Hypergraph",         "hypergraph_reactions"),
    ("W11", "Quasispecies",       "quasispecies"),
    ("W12", "Symbiogenesis",      "symbiogenesis"),
    ("W13", "Multi-scale",        "multiscale"),
]


# Conservative campaign → worlds mapping derived from filename evidence
# in reports/campaign_*/. Only entries we can verify from artifact names
# (e.g., bfg_w8_w11_w12.json explicitly names W8/W11/W12). Where a
# campaign's world coverage is unknown, the cell stays empty (D22).
_CAMPAIGN_WORLD_MAP: dict[str, list[str]] = {
    # phase1 / cross-substrate baseline — known from BUILD_LOG
    "002": ["W1", "W3", "W7", "W12"],
    # KF detector + floor calibration touched W1 RAF, W2 protocell, W11
    "009": ["W1", "W2", "W11"],
    # bfg_w8_w11_w12 explicit; coverage_matrix.json + cross_substrate
    "010": ["W8", "W11", "W12"],
    # Atlas seed campaign + ITIS extraction — biological (W6 ecosystem)
    "013": ["W6"],
}


def _load_atlas_entries() -> list[dict[str, Any]]:
    """Read every ``atlas/entries/atlas.<motif>.001.json`` file. Returns
    a list of dicts. Empty if the directory is missing — caller renders
    an honest absence (D22)."""
    entries_dir = Path("atlas/entries")
    if not entries_dir.exists():
        return []
    out: list[dict[str, Any]] = []
    for p in sorted(entries_dir.glob("atlas.*.json")):
        try:
            out.append(json.loads(p.read_text(encoding="utf-8-sig")))
        except (OSError, json.JSONDecodeError):
            continue
    return out


def _classify_motif_world_cell(
    motif_entry: dict[str, Any],
    world_id: str,
) -> dict[str, Any]:
    """Decide the (color, count, total, status, hover_text) tuple for a
    single (motif, world) cell. Color semantics per CB-009 brief:
      gray   = no detection / not evaluated
      amber  = weak / declined
      green  = fired
      red    = falsified
      purple = formal-deficit candidate
    The "fire count" is the number of campaigns we can verifiably attest
    touched this (motif, world) pair; the "trace count" is the number of
    campaigns the motif was attested in overall (provenance.campaigns).
    Honest absences fall through to the gray "no data" branch."""
    motif_id = motif_entry.get("motif_id", "")
    campaigns = (motif_entry.get("provenance") or {}).get("campaigns") or []
    verdict = (motif_entry.get("provenance") or {}).get("replication_verdict", "")
    formal_gap_score = float(motif_entry.get("formal_gap_score") or 0.0)
    mode_tag = motif_entry.get("mode_tag", "exploratory")

    # Count this motif's campaigns that touched this world per the
    # conservative campaign→worlds mapping.
    fire_campaigns = [
        c for c in campaigns
        if world_id in _CAMPAIGN_WORLD_MAP.get(c, [])
    ]
    fire_count = len(fire_campaigns)
    total = len(campaigns)

    if "floor_connectivity" in motif_id and fire_count > 0:
        # The floor-connectivity motif is the canonical formal-deficit
        # candidate (Campaign 013 verdict). Color it purple when seen.
        color = "#bd6df8"
        status = "formal_deficit_candidate"
    elif verdict == "falsified":
        color = "#ff5468"
        status = "falsified"
    elif fire_count == 0:
        color = "#283042"  # COLOR_BORDER — visible-but-empty, D22 honest absence
        status = "no_detection"
    elif mode_tag == "candidate" or formal_gap_score > 0.5:
        color = "#f5a623"  # COLOR_WARNING — weak / declined
        status = "weak"
    else:
        color = "#3ddc84"  # COLOR_VERIFIED — fired
        status = "fired"

    if fire_count == 0:
        hover_text = (
            f"motif_id: {motif_id}<br>world: {world_id}<br>"
            f"no detection on this world (D22 honest absence)<br>"
            f"motif appears in campaigns: {', '.join(campaigns) or '—'}<br>"
            f"campaign→world mapping unknown for this pair"
        )
    else:
        hover_text = (
            f"motif_id: {motif_id}<br>world: {world_id}<br>"
            f"status: {status}<br>"
            f"fire campaigns: {', '.join(fire_campaigns)}<br>"
            f"all motif campaigns: {', '.join(campaigns)}<br>"
            f"replication: {verdict or 'unknown'}"
        )

    return {
        "color": color,
        "count": fire_count,
        "total": total,
        "status": status,
        "hover": hover_text,
        "fire_campaigns": fire_campaigns,
    }


def _render_periodic_table() -> None:
    """Render the motif × world periodic-table matrix.

    Layout:
      * Y axis: 6 motifs (registry order)
      * X axis: 15 worlds (W-1, W0, W1..W13)
      * Cell: count "<fire>/<total>" + color
      * Per-row tally column on the right
      * Per-column tally row at the bottom
      * Click a world column header to drill into that world's atlas
        evidence panel below the table.
    """
    import streamlit as st

    entries = _load_atlas_entries()
    if not entries:
        from control_room.components import render_empty_state
        render_empty_state(
            reason="atlas/entries/ is empty or unreadable",
            expected_artifact="atlas/entries/atlas.<motif>.001.json files",
        )
        return

    # Build header row (worlds) + body rows (motifs)
    headers = "".join(
        f'<th style="background:var(--bg-panel,#121826);color:var(--fg3,#9aa0ac);'
        f'font-family:var(--font-mono,monospace);font-size:0.72rem;padding:6px 4px;'
        f'border:1px solid var(--border,#283042);text-align:center;writing-mode:horizontal-tb;'
        f'letter-spacing:0.04em;" title="{display_name}">{wid}</th>'
        for wid, display_name, _family in _WORLD_AXIS
    )
    header_row = (
        '<tr>'
        '<th style="background:var(--bg-panel,#121826);color:var(--fg3,#9aa0ac);'
        'font-family:var(--font-mono,monospace);font-size:0.72rem;padding:6px 8px;'
        'border:1px solid var(--border,#283042);text-align:left;letter-spacing:0.04em;">motif</th>'
        f'{headers}'
        '<th style="background:var(--bg-panel,#121826);color:var(--fg3,#9aa0ac);'
        'font-family:var(--font-mono,monospace);font-size:0.72rem;padding:6px 8px;'
        'border:1px solid var(--border,#283042);text-align:center;letter-spacing:0.04em;">Σ row</th>'
        '</tr>'
    )

    body_rows: list[str] = []
    col_tallies = {wid: 0 for wid, _, _ in _WORLD_AXIS}
    row_tallies: list[int] = []

    for entry in entries:
        motif_id = entry.get("motif_id", "?")
        short = motif_id.split(".")[1] if "." in motif_id else motif_id
        cells: list[str] = []
        row_total = 0
        for wid, _, _ in _WORLD_AXIS:
            info = _classify_motif_world_cell(entry, wid)
            count = info["count"]
            total = info["total"]
            color = info["color"]
            content = (
                f'{count}/{total}' if count > 0
                else '<span style="opacity:0.4;">—</span>'
            )
            text_color = "#0a0e16" if info["status"] in ("fired", "formal_deficit_candidate") else "#e3e6ec"
            cells.append(
                f'<td style="background:{color};color:{text_color};'
                f'font-family:var(--font-mono,monospace);font-size:0.72rem;'
                f'padding:8px 4px;border:1px solid var(--border,#283042);'
                f'text-align:center;cursor:help;" title="{info["hover"].replace(chr(60)+"br"+chr(62), chr(10))}">'
                f'{content}</td>'
            )
            col_tallies[wid] += count
            row_total += count
        row_tallies.append(row_total)
        body_rows.append(
            '<tr>'
            f'<td style="background:var(--bg-panel,#121826);color:var(--fg2,#e3e6ec);'
            f'font-family:var(--font-display,sans-serif);font-size:0.85rem;padding:6px 8px;'
            f'border:1px solid var(--border,#283042);text-align:left;font-weight:500;">{short}</td>'
            + "".join(cells)
            + f'<td style="background:var(--bg-panel,#121826);color:var(--fg1,#f8f9fa);'
            f'font-family:var(--font-mono,monospace);font-size:0.78rem;padding:6px 8px;'
            f'border:1px solid var(--border,#283042);text-align:center;font-weight:600;">{row_total}</td>'
            '</tr>'
        )

    tally_cells = "".join(
        f'<td style="background:var(--bg-panel,#121826);color:var(--fg1,#f8f9fa);'
        f'font-family:var(--font-mono,monospace);font-size:0.78rem;padding:6px 4px;'
        f'border:1px solid var(--border,#283042);text-align:center;font-weight:600;">{col_tallies[wid]}</td>'
        for wid, _, _ in _WORLD_AXIS
    )
    grand_total = sum(row_tallies)
    tally_row = (
        '<tr>'
        '<td style="background:var(--bg-panel,#121826);color:var(--fg3,#9aa0ac);'
        'font-family:var(--font-mono,monospace);font-size:0.72rem;padding:6px 8px;'
        'border:1px solid var(--border,#283042);text-align:left;font-weight:500;">Σ col</td>'
        f'{tally_cells}'
        f'<td style="background:var(--motif,#bd6df8);color:#0a0e16;'
        f'font-family:var(--font-mono,monospace);font-size:0.85rem;padding:6px 8px;'
        f'border:1px solid var(--border,#283042);text-align:center;font-weight:700;">{grand_total}</td>'
        '</tr>'
    )

    table = (
        '<table style="border-collapse:collapse;width:100%;margin-bottom:12px;">'
        f'<thead>{header_row}</thead>'
        f'<tbody>{"".join(body_rows)}{tally_row}</tbody>'
        '</table>'
    )
    render_html(table)

    # Legend
    legend = (
        '<div style="display:flex;gap:14px;flex-wrap:wrap;align-items:center;'
        'font-family:var(--font-mono,monospace);font-size:0.72rem;color:var(--fg3,#9aa0ac);'
        'margin-top:6px;margin-bottom:14px;">'
        '<span><span style="display:inline-block;width:14px;height:14px;background:#283042;'
        'border:1px solid #283042;vertical-align:middle;margin-right:4px;"></span>no detection</span>'
        '<span><span style="display:inline-block;width:14px;height:14px;background:#f5a623;'
        'vertical-align:middle;margin-right:4px;"></span>weak / declined</span>'
        '<span><span style="display:inline-block;width:14px;height:14px;background:#3ddc84;'
        'vertical-align:middle;margin-right:4px;"></span>fired</span>'
        '<span><span style="display:inline-block;width:14px;height:14px;background:#ff5468;'
        'vertical-align:middle;margin-right:4px;"></span>falsified</span>'
        '<span><span style="display:inline-block;width:14px;height:14px;background:#bd6df8;'
        'vertical-align:middle;margin-right:4px;"></span>formal-deficit candidate</span>'
        '</div>'
    )
    render_html(legend)

    # Drilldown: pick a (motif, world) pair to see the campaign reports that produced it.
    import streamlit as st
    drill_cols = st.columns([2, 2, 6])
    with drill_cols[0]:
        motif_choice = st.selectbox(
            "drill motif",
            options=[e.get("motif_id", "?") for e in entries],
            key="atlas_pt_drill_motif",
        )
    with drill_cols[1]:
        world_choice = st.selectbox(
            "drill world",
            options=[wid for wid, _, _ in _WORLD_AXIS],
            key="atlas_pt_drill_world",
        )
    if motif_choice and world_choice:
        entry = next((e for e in entries if e.get("motif_id") == motif_choice), None)
        if entry:
            info = _classify_motif_world_cell(entry, world_choice)
            fire_campaigns = info["fire_campaigns"]
            campaign_links = "".join(
                f'<li style="margin:4px 0;"><a href="?room=campaign_command" '
                f'style="color:var(--trace,#22d3ee);text-decoration:none;font-family:var(--font-mono,monospace);">'
                f'reports/campaign_{c}/full_report.json</a> '
                f'<span style="color:var(--fg4,#6c7484);font-family:var(--font-mono,monospace);font-size:0.7rem;">'
                f'(per Campaign {c})</span></li>'
                for c in fire_campaigns
            ) or '<li style="color:var(--fg4,#6c7484);font-family:var(--font-body,sans-serif);">no campaign reports cite this motif on this world (D22 honest absence)</li>'
            render_html(
                f'<div style="background:var(--bg-panel,#121826);border:1px solid var(--border,#283042);'
                f'border-radius:14px;padding:14px;margin-top:8px;">'
                f'<div style="font-family:var(--font-display,sans-serif);font-size:1.05rem;color:var(--fg1,#f8f9fa);'
                f'font-weight:600;">{motif_choice} × {world_choice}</div>'
                f'<div style="font-family:var(--font-mono,monospace);font-size:0.72rem;color:var(--fg4,#6c7484);'
                f'margin:4px 0 8px;">status: {info["status"]} · fired in {info["count"]}/{info["total"]} campaigns</div>'
                f'<ul style="margin:6px 0 0 16px;padding:0;">{campaign_links}</ul>'
                f'</div>'
            )


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
