"""World Observatory — proposal §7.2.

World inventory grid + density status + falsifier links. Surfaces the
canonical 13 worlds (W1–W13) plus the Campaign 016 additions
W-1 (atomic/molecular) and W0 (math primitives) for a current 15-world
inventory.

Worlds are surfaced from the campaign reports and factory store. The
densification status comes from Campaign 016 intake_dock_state when
present.
"""

from __future__ import annotations

from typing import Any

from control_room.adapters import (
    parse_campaign_reports,
    parse_factory_store,
    parse_methods_falsifiers,
)
from control_room.components import (
    metric_card,
    panel,
    render_empty_state,
    render_html,
    room_emblem,
    status_pill,
    world_card,
)


ROOM_ID = "world_observatory"
ROOM_NAME = "World Observatory"
ROOM_ICON = "🌍"
ROOM_TAGLINE = "Visualize the simulation worlds — sparse to claim-ready."
ROOM_PHASE = "Phase 1"


# Canonical world inventory (proposal §1.2 + Campaign 016 additions).
# Each entry: (world_id, display_name, world_family, density_default).
WORLD_INVENTORY = [
    ("W-1", "Atomic / Molecular Primitives", "atomic_molecular", "claim_ready_densified"),
    ("W0",  "Math Primitives",                "math_primitives",   "claim_ready_densified"),
    ("W1",  "Chemistry / RAFs",               "crn",               "trace_valid"),
    ("W2",  "Protocell",                      "protocell",         "trace_valid"),
    ("W3",  "Reaction-Diffusion Field",       "field",             "trace_valid"),
    ("W4",  "Morphogenesis (GRN)",            "morphogenesis",     "trace_valid"),
    ("W5",  "Digital (Avida-class)",          "digital",           "trace_valid"),
    ("W6",  "Ecosystem",                      "ecosystem",         "trace_valid"),
    ("W7",  "Swarm",                          "swarm",             "exploratory_densified"),
    ("W8",  "Cognitive",                      "cognitive",         "trace_valid"),
    ("W9",  "Origins Chemistry",              "origins_chemistry", "trace_valid"),
    ("W10", "Hypergraph Reactions",           "hypergraph_reactions", "trace_valid"),
    ("W11", "Quasispecies",                   "quasispecies",      "trace_valid"),
    ("W12", "Symbiogenesis",                  "symbiogenesis",     "trace_valid"),
    ("W13", "Multi-scale Composition",        "multiscale",        "falsifier_active"),
]


def render() -> None:
    import streamlit as st

    render_html(room_emblem(ROOM_NAME, ROOM_TAGLINE, ROOM_ID))

    factory = parse_factory_store()
    campaigns = parse_campaign_reports()
    falsifiers = parse_methods_falsifiers()

    # Density classes from Campaign 016 intake_dock_state (when present)
    density_overrides: dict[str, str] = {}
    if factory["status"] == "ok":
        intake = factory["data"].get("intake_dock_state") or {}
        intake_data = intake.get("data") or {}
        if isinstance(intake_data, dict):
            density_overrides = intake_data.get("density_classes") or {}

    # Falsifier links per world
    falsifier_world_hits: dict[str, list[str]] = {}
    if falsifiers["status"] == "ok":
        for d in falsifiers["data"]["falsifier_docs"]:
            name = d["name"].lower()
            for wid in ("w1","w2","w3","w4","w5","w6","w7","w8","w9","w10","w11","w12","w13"):
                if wid in name:
                    falsifier_world_hits.setdefault(wid.upper(), []).append(d["name"])

    # ------------------------------------------------------------------
    # DRILLDOWN MODE — when a world is selected, the drilldown TAKES
    # OVER the screen ("brings it to the forefront in its own screen"
    # per PI request). We render the back button + drilldown only,
    # skipping the inventory grid + heatmap until the user clicks back.
    # This is the canonical Streamlit pattern for "tab switch" without
    # losing state (vs. a panel-below pattern, which dumps content far
    # below the click point and looks like the click did nothing).
    # ------------------------------------------------------------------
    selected = st.session_state.get("world_obs_selected")
    if selected:
        family_sel, wid_sel, name_sel = selected
        # Sticky back button at the top of the drilldown view.
        back_col, _ = st.columns([1, 5])
        with back_col:
            if st.button("← Back to all worlds", key="world_obs_back", use_container_width=True):
                st.session_state.pop("world_obs_selected", None)
                st.rerun()
        try:
            from control_room.rooms._world_drilldown import render_world_drilldown
            render_world_drilldown(family_sel, wid_sel, name_sel)
        except Exception as e:  # surface any render error visibly
            st.error(f"Drilldown render error: {type(e).__name__}: {e}")
            import traceback
            st.code(traceback.format_exc())
        return  # ← critical: skip the inventory grid render below

    # ------------------------------------------------------------------
    # INVENTORY MODE (default) — metric cards + 15-world grid + heatmap
    # ------------------------------------------------------------------
    # Top metrics — display labels are humanized; underlying density-class
    # enum names are surfaced via the metric_card subtext where useful.
    cols = st.columns(4)
    with cols[0]:
        render_html(metric_card("Worlds total", str(len(WORLD_INVENTORY)), "active", "W-1, W0, W1 through W13"))
    with cols[1]:
        claim_ready = sum(
            1 for wid, _, family, d in WORLD_INVENTORY
            if d == "claim_ready_densified" or family in density_overrides
        )
        render_html(metric_card("Densification sufficient", str(claim_ready), "verified", "promoted via D21 audit"))
    with cols[2]:
        falsified = sum(1 for _, _, _, d in WORLD_INVENTORY if d == "falsifier_active")
        render_html(metric_card("Falsified", str(falsified), "failed", "downgraded under D17"))
    with cols[3]:
        falsifier_count = sum(len(v) for v in falsifier_world_hits.values())
        render_html(metric_card("Falsifier records", str(falsifier_count), "warning" if falsifier_count else "verified", "published papers"))

    # World inventory grid (3 columns of cards). Each card has an "Open"
    # button that brings that world into the drilldown view (replaces
    # this grid with a per-world detail screen).
    st.markdown('<span class="cap">world inventory · 15 worlds · click open to drill down</span>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (wid, display_name, family, default_density) in enumerate(WORLD_INVENTORY):
        density = density_overrides.get(family, default_density)
        falsifier_links = falsifier_world_hits.get(wid, [])
        family_human = _humanize_world_family(family)
        density_human = _humanize_density(density)
        meta_lines: list[dict[str, str]] = [
            {
                "display": f"Family: {family_human}",
                "tooltip": f"world_family: {family}",
            },
            {
                "display": f"Density: {density_human}",
                "tooltip": f"density: {density}",
            },
        ]
        if falsifier_links:
            meta_lines.append({
                "display": f"Falsifier docs: {len(falsifier_links)}",
                "tooltip": "papers/falsifiers/ entries naming this world",
            })
        with cols[i % 3]:
            render_html(world_card(
                name=f"{wid} · {display_name}",
                world_family=family,
                status="verified" if density == "claim_ready_densified" else
                       "warning" if density == "exploratory_densified" else
                       "failed" if density == "falsifier_active" else
                       "active",
                meta_lines=meta_lines,
            ))
            # Click-to-open button. Streamlit doesn't have native
            # click-on-card, so a slim button beneath each card is the
            # canonical pattern.
            if st.button(f"Open {wid}", key=f"world_obs_open_{wid}", use_container_width=True):
                st.session_state["world_obs_selected"] = (family, wid, display_name)
                st.rerun()

    # World heatmap (proposal §9.4) — bar chart of density-class per world
    st.markdown('<span class="cap">world heatmap · density × motif richness</span>', unsafe_allow_html=True)
    _world_heatmap(WORLD_INVENTORY, density_overrides, falsifier_world_hits)


# Humanizers for the world-card surface — keep the raw variable name on
# hover via the chrome.world_card meta_lines tooltip path.

_FAMILY_HUMAN = {
    "atomic_molecular": "Atomic / molecular",
    "math_primitives":  "Math primitives",
    "crn":              "Chemistry (CRN)",
    "protocell":        "Protocell",
    "field":            "Reaction-diffusion field",
    "morphogenesis":    "Morphogenesis (GRN)",
    "digital":          "Digital (Avida-class)",
    "ecosystem":        "Ecosystem",
    "swarm":            "Swarm",
    "cognitive":        "Cognitive",
    "origins_chemistry": "Origins chemistry",
    "hypergraph_reactions": "Hypergraph reactions",
    "quasispecies":     "Quasispecies",
    "symbiogenesis":    "Symbiogenesis",
    "multiscale":       "Multi-scale",
}

_DENSITY_HUMAN = {
    "claim_ready_densified":   "Sufficient",
    "densification_validated": "Sufficient (audited)",
    "exploratory_densified":   "Exploratory",
    "trace_valid":             "Trace verified",
    "skeleton":                "Skeleton",
    "falsifier_active":        "Falsified",
}


def _humanize_world_family(family: str) -> str:
    """Return a display-friendly version of the canonical world_family
    identifier. Hover tooltip on the world card carries the raw value
    so the variable name is still discoverable."""
    return _FAMILY_HUMAN.get(family, family.replace("_", " ").title())


def _humanize_density(density: str) -> str:
    """Display name for the density class. Hover tooltip surfaces the
    raw enum value (e.g., ``claim_ready_densified``)."""
    return _DENSITY_HUMAN.get(density, density.replace("_", " ").title())


def _world_heatmap(
    inventory: list[tuple[str, str, str, str]],
    density_overrides: dict[str, str],
    falsifier_hits: dict[str, list[str]],
) -> None:
    import streamlit as st
    import plotly.graph_objects as go

    density_score_map = {
        "claim_ready_densified": 4,
        "densification_validated": 4,
        "exploratory_densified": 3,
        "trace_valid": 2,
        "skeleton": 1,
        "falsifier_active": 0,
    }
    density_color_map = {
        "claim_ready_densified": "#3ddc84",
        "densification_validated": "#3ddc84",
        "exploratory_densified": "#f5a623",
        "trace_valid": "#22d3ee",
        "skeleton": "#5b6478",
        "falsifier_active": "#ff5468",
    }
    xs = []
    densities = []
    colors = []
    falsifiers = []
    hover = []
    for wid, display_name, family, default_density in inventory:
        density = density_overrides.get(family, default_density)
        score = density_score_map.get(density, 2)
        color = density_color_map.get(density, "#5b6478")
        n_fals = len(falsifier_hits.get(wid, []))
        xs.append(wid)
        densities.append(score)
        colors.append(color)
        falsifiers.append(n_fals)
        hover.append(f"{wid} · {display_name}<br>family: {family}<br>density: {density}<br>falsifiers: {n_fals}")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=xs, y=densities,
        marker=dict(color=colors, line=dict(color="#283042", width=1)),
        hovertext=hover, hoverinfo="text",
        name="density score",
    ))
    fig.update_layout(
        height=240,
        margin=dict(l=20, r=20, t=10, b=40),
        plot_bgcolor="#121826",
        paper_bgcolor="#0a0e16",
        font=dict(family="JetBrains Mono, monospace", size=11, color="#9aa0ac"),
        xaxis=dict(gridcolor="#283042", title="", tickangle=0),
        yaxis=dict(
            gridcolor="#283042",
            title="Density score",
            tickmode="array",
            tickvals=[0, 1, 2, 3, 4],
            ticktext=["Falsified", "Skeleton", "Trace verified", "Exploratory", "Sufficient"],
            range=[-0.5, 4.5],
        ),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
