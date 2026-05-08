"""Project Genealogy — Mission Control room (PG-001 v1).

The room renders the published ``ProjectGenealogyAtlas.v1`` and
``ProjectCoherenceReport.v1`` artifacts from
``reports/project_genealogy/`` per the spec's
§"Mission Control Integration". It does not run the audit; reruns are
CLI-only in v1 (``python -m project_genealogy run-all``).

D22 binding: when atlas or coherence artifacts are missing, the room
renders an honest empty state via ``render_empty_state``.

Determinism contract: closing and reopening the room against the same
``atlas_latest.json`` and ``coherence_latest.json`` produces an identical
render — Plotly traces are seeded from the JSON in deterministic order;
no shuffling, no random color assignment, no live data fetches.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from control_room.components import (
    metric_card,
    panel,
    render_empty_state,
    render_html,
    room_emblem,
    status_pill,
)
from control_room.components.empty_state import EMPTY_STATE_HTML_MARKER


ROOM_ID = "project_genealogy"
ROOM_NAME = "Project Genealogy"
ROOM_ICON = "🌳"
ROOM_TAGLINE = "Source-bound, doctrine-aware genealogy of every audited file."
ROOM_PHASE = "PG-001"


REPORT_DIR = "reports/project_genealogy"


# Color tokens (mirror Visuals/colors_and_type.css; tokens consumed via
# string for Plotly compatibility — Streamlit's design tokens are CSS).
ARTIFACT_FAMILY_COLOR = {
    "doctrine": "#3ddc84",
    "method": "#bd6df8",
    "factory": "#f5b942",
    "control_room": "#22d3ee",
    "report": "#9aa0ac",
    "audit_report": "#5ee0ff",
    "audit_instrument": "#b084ff",
    "test": "#3ddc84",
    "atlas": "#4fc3f7",
    "telemetry": "#f5d77a",
    "script": "#5b6478",
    "spec": "#bd6df8",
    "visual": "#fff",
    "ai_os": "#9aa0ac",
    "driver_or_root_doc": "#d6e0ff",
    "root_artifact": "#5b6478",
    "docs": "#3ddc84",
    "paper": "#bd6df8",
    "falsifier": "#ff5468",
    "prereg": "#bd6df8",
    "other": "#5b6478",
}

DRIFT_STATUS_COLOR = {
    "none": "#3ddc84",
    "positive_deepening": "#5ee0ff",
    "neutral_refactor": "#9aa0ac",
    "review_required": "#f5b942",
    "bad_drift": "#ff5468",
    "honest_decline": "#5b6478",
}

EDGE_TYPES = (
    "spawned_by_ticket",
    "derived_from_file",
    "generated_by",
    "imports",
    "executes",
    "validates",
    "cites",
    "shares_birth_cohort",
    "implements_same_doctrine",
    "contradicts_doctrine_peer",
)

EDGE_DEFAULT_VISIBLE = (
    "derived_from_file",
    "spawned_by_ticket",
    "contradicts_doctrine_peer",
)


def _atlas_path() -> Path:
    return Path(REPORT_DIR) / "atlas_latest.json"


def _coherence_path() -> Path:
    return Path(REPORT_DIR) / "coherence_latest.json"


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _versioned_atlases() -> list[Path]:
    p = Path(REPORT_DIR)
    if not p.is_dir():
        return []
    return sorted(p.glob("atlas_*Z.json"))


def _node_axes(nodes: list[dict[str, Any]], depth_axis: str) -> tuple[list[float], list[str], list[float]]:
    """Return X (birth time ordinal), Y (artifact_family ordinal), Z (depth axis value)."""
    # X: rank order by birth_time (string-sorted)
    sorted_by_time = sorted(
        enumerate(nodes),
        key=lambda iv: (iv[1].get("birth_time") or "", iv[1].get("path", "")),
    )
    x_rank: dict[int, int] = {}
    for rank, (i, _) in enumerate(sorted_by_time):
        x_rank[i] = rank
    xs = [x_rank[i] for i in range(len(nodes))]

    # Y: artifact_family slot
    families = sorted({n["artifact_family"] for n in nodes})
    family_slot = {f: i for i, f in enumerate(families)}
    ys = [n["artifact_family"] for n in nodes]
    y_slot = [family_slot[f] for f in ys]

    # Z: depth axis value (defaults to predicate_atom_coverage)
    zs: list[float] = []
    for n in nodes:
        v = n.get("depth", {}).get(depth_axis, {}).get("value")
        if v is None:
            v = 0.0
        zs.append(float(v))
    return xs, [str(f) for f in ys], zs


def _hover_text(node: dict[str, Any]) -> str:
    depth = node.get("depth", {})
    pa = depth.get("predicate_atom_coverage", {}).get("value")
    av = depth.get("adversarial_surface_coverage", {}).get("value")
    di = depth.get("doctrine_binding_quality", {}).get("verified", [])
    return (
        f"<b>{node['path']}</b><br>"
        f"family: {node['artifact_family']}<br>"
        f"spawn: {node.get('spawn_ticket') or '—'}<br>"
        f"drift: {node.get('drift_status', '')}<br>"
        f"PA-cov: {pa}<br>"
        f"adv-cov: {av}<br>"
        f"verified doctrines: {', '.join(di) or '—'}<br>"
        f"dossier_hash: {node.get('dossier_hash', '')[:14]}…"
    )


def _build_3d_figure(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    visible_edge_types: set[str],
    visible_families: set[str],
    depth_axis: str,
):
    import plotly.graph_objects as go

    visible_nodes = [n for n in nodes if n["artifact_family"] in visible_families]
    if not visible_nodes:
        return None

    xs, ys, zs = _node_axes(visible_nodes, depth_axis)
    family_to_idx: dict[str, list[int]] = defaultdict(list)
    for i, n in enumerate(visible_nodes):
        family_to_idx[n["artifact_family"]].append(i)

    # node_id -> (x, y, z) lookup for edge endpoint coords.
    node_coords: dict[str, tuple[float, float, float]] = {}
    family_slot = sorted({n["artifact_family"] for n in visible_nodes})
    family_slot_idx = {f: i for i, f in enumerate(family_slot)}
    for i, n in enumerate(visible_nodes):
        node_coords[n["path"]] = (xs[i], family_slot_idx[n["artifact_family"]], zs[i])

    fig = go.Figure()

    # One Scatter3d trace per (family, honest_decline) tuple — deterministic
    # order. The honest-decline split is a separate trace because Plotly
    # scatter3d's `marker.line.width` is per-trace, not per-point, so
    # honest-decline nodes get their own outlined trace.
    for family in sorted(family_to_idx.keys()):
        for honest_decline_flag in (False, True):
            idxs = [
                i for i in family_to_idx[family]
                if bool(visible_nodes[i].get("honest_decline")) == honest_decline_flag
            ]
            if not idxs:
                continue
            trace_name = f"{family} (honest_decline)" if honest_decline_flag else family
            fig.add_trace(go.Scatter3d(
                x=[xs[i] for i in idxs],
                y=[family_slot_idx[family]] * len(idxs),
                z=[zs[i] for i in idxs],
                mode="markers",
                name=trace_name,
                marker=dict(
                    size=[
                        4 + min(20, float(visible_nodes[i].get("load_bearingness", 0))) ** 0.5
                        for i in idxs
                    ],
                    color=[
                        DRIFT_STATUS_COLOR.get(visible_nodes[i].get("drift_status", "honest_decline"), "#5b6478")
                        for i in idxs
                    ],
                    line=dict(
                        width=2 if honest_decline_flag else 0,
                        color="#fff",
                    ),
                ),
                hovertext=[_hover_text(visible_nodes[i]) for i in idxs],
                hoverinfo="text",
                customdata=[visible_nodes[i]["path"] for i in idxs],
            ))

    # Edges as Plotly 3D line traces, one per visible edge type.
    visible_paths = {n["path"] for n in visible_nodes}
    for et in sorted(visible_edge_types):
        ex: list[float | None] = []
        ey: list[float | None] = []
        ez: list[float | None] = []
        for e in edges:
            if e.get("edge_type") != et:
                continue
            s = e.get("source")
            t = e.get("target")
            if s not in node_coords or t not in node_coords:
                # Edge crosses out of the visible projection; skip.
                continue
            x1, y1, z1 = node_coords[s]
            x2, y2, z2 = node_coords[t]
            ex.extend([x1, x2, None])
            ey.extend([y1, y2, None])
            ez.extend([z1, z2, None])
        if not ex:
            continue
        fig.add_trace(go.Scatter3d(
            x=ex, y=ey, z=ez,
            mode="lines",
            name=et,
            line=dict(width=1, color="#5b6478"),
            opacity=0.4,
            hoverinfo="skip",
        ))

    # Layout — deterministic ranges keyed off visible data.
    family_ticks = list(range(len(family_slot)))
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="birth time ordinal", showbackground=False),
            yaxis=dict(
                title="artifact family",
                tickmode="array",
                tickvals=family_ticks,
                ticktext=family_slot,
                showbackground=False,
            ),
            zaxis=dict(title=depth_axis, range=[0, 1], showbackground=False),
            aspectmode="cube",
        ),
        showlegend=True,
        margin=dict(l=0, r=0, b=0, t=10),
        paper_bgcolor="#0f1116",
        plot_bgcolor="#0f1116",
        font=dict(color="#d6e0ff"),
        height=520,
    )
    return fig


def _filter_nodes(nodes: list[dict[str, Any]], filters: dict[str, Any]) -> list[dict[str, Any]]:
    out = list(nodes)
    if filters.get("doctrine"):
        d = filters["doctrine"]
        out = [n for n in out if d in n.get("doctrine_refs", [])]
    if filters.get("drift_status") and filters["drift_status"] != "(any)":
        out = [n for n in out if n.get("drift_status") == filters["drift_status"]]
    if filters.get("mistake_class") and filters["mistake_class"] != "(any)":
        out = [n for n in out if filters["mistake_class"] in n.get("mistake_classes", [])]
    if filters.get("cohort") and filters["cohort"] != "(any)":
        out = [n for n in out if n.get("spawn_ticket") == filters["cohort"]]
    if filters.get("cleanup_status") and filters["cleanup_status"] != "(any)":
        out = [n for n in out if n.get("cleanup_candidate_status") == filters["cleanup_status"]]
    if filters.get("honest_decline_only"):
        out = [n for n in out if n.get("honest_decline")]
    return out


def render() -> None:
    import streamlit as st

    render_html(room_emblem(ROOM_NAME, ROOM_TAGLINE, ROOM_ID))

    atlas = _load_json(_atlas_path())
    coherence = _load_json(_coherence_path())

    if atlas is None and coherence is None:
        render_empty_state(
            reason=(
                "No PG-001 artifacts published. Generate them with "
                "`python -m project_genealogy run-all` from the repo root."
            ),
            expected_artifact="reports/project_genealogy/atlas_latest.json",
        )
        return

    if atlas is None:
        render_empty_state(
            reason="atlas_latest.json missing or unreadable.",
            expected_artifact="reports/project_genealogy/atlas_latest.json",
        )
        return

    summary = atlas.get("summary", {})

    # Top-row metrics.
    cols = st.columns(5)
    with cols[0]:
        render_html(metric_card(
            label="audited files",
            value=str(summary.get("file_count", 0)),
            subtext=f"{len(atlas.get('cohorts', []))} cohorts",
            status="active",
        ))
    with cols[1]:
        render_html(metric_card(
            label="bad drift",
            value=str(summary.get("bad_drift_count", 0)),
            subtext=f"{summary.get('confirmed_finding_count', 0)} confirmed findings",
            status="failed" if summary.get("bad_drift_count", 0) > 0 else "verified",
        ))
    with cols[2]:
        render_html(metric_card(
            label="declines",
            value=str(summary.get("decline_count", 0)),
            subtext="honest-decline taxonomy",
            status="trace",
        ))
    with cols[3]:
        coverage = summary.get("mission_coverage_status_counts", {})
        ms_total = summary.get("mission_atom_count", 0)
        ms_covered = coverage.get("covered", 0)
        render_html(metric_card(
            label="mission atoms",
            value=f"{ms_covered}/{ms_total} covered",
            subtext=f"orphan: {coverage.get('orphan', 0)}, partial: {coverage.get('partial', 0)}",
            status="verified" if ms_total and ms_covered == ms_total else "active",
        ))
    with cols[4]:
        cleanup = summary.get("cleanup_candidate_count_by_status", {})
        render_html(metric_card(
            label="cleanup candidates",
            value=str(cleanup.get("removable_clean", 0) + cleanup.get("removable_with_warnings", 0)),
            subtext=f"unknown: {cleanup.get('unknown', 0)}, declined: {cleanup.get('probe_declined', 0)}",
            status="active",
        ))

    # Counts mismatch banner (D22-style honest degraded-state banner).
    nodes = atlas.get("nodes", [])
    edges = atlas.get("edges", [])
    actual_node_count = len(nodes)
    actual_edge_count = sum(len(v) for v in [edges]) if edges else len(edges)
    if actual_node_count != summary.get("file_count", 0):
        render_html(panel(
            title="degraded state — node count mismatch",
            content=(
                f"summary.file_count={summary.get('file_count')} but "
                f"len(nodes)={actual_node_count}. The tab does not silently "
                f"reconcile — investigate atlas integrity before trusting "
                f"per-panel counts."
            ),
            status="failed",
        ))
        return

    # ------- Sidebar filters -------
    with st.sidebar:
        st.markdown("---")
        st.markdown("**Project Genealogy filters**")
        doctrines = sorted({d for n in nodes for d in n.get("doctrine_refs", [])})
        chosen_d = st.selectbox("doctrine", ["(any)"] + doctrines, key="pg_doctrine")
        drift_options = ["(any)"] + sorted({n.get("drift_status", "") for n in nodes if n.get("drift_status")})
        chosen_drift = st.selectbox("drift_status", drift_options, key="pg_drift")
        mistakes = sorted({m for n in nodes for m in n.get("mistake_classes", [])})
        chosen_m = st.selectbox("mistake_class", ["(any)"] + mistakes, key="pg_mistake")
        cohorts_list = sorted({n.get("spawn_ticket") for n in nodes if n.get("spawn_ticket")})
        chosen_c = st.selectbox("cohort (spawn_ticket)", ["(any)"] + cohorts_list, key="pg_cohort")
        cleanup_opts = ["(any)"] + sorted({n.get("cleanup_candidate_status", "unknown") for n in nodes})
        chosen_cleanup = st.selectbox("cleanup_status", cleanup_opts, key="pg_cleanup")
        honest_only = st.checkbox("honest decline only", value=False, key="pg_honest")

        st.markdown("**Edge types**")
        edge_filters: dict[str, bool] = {}
        for et in EDGE_TYPES:
            edge_filters[et] = st.checkbox(
                et,
                value=(et in EDGE_DEFAULT_VISIBLE),
                key=f"pg_edge_{et}",
            )

        st.markdown("**Depth axis**")
        depth_axis = st.selectbox(
            "depth axis",
            [
                "predicate_atom_coverage",
                "adversarial_surface_coverage",
            ],
            key="pg_depth_axis",
        )

        st.markdown("**Atlas time slider**")
        versioned = _versioned_atlases()
        if len(versioned) >= 2:
            options = [v.name for v in versioned]
            chosen_atlas = st.select_slider(
                "atlas snapshot",
                options=options,
                value=options[-1],
                key="pg_atlas_slider",
            )
        else:
            st.caption("single snapshot — slider disabled.")

    filters = {
        "doctrine": chosen_d if chosen_d != "(any)" else None,
        "drift_status": chosen_drift,
        "mistake_class": chosen_m,
        "cohort": chosen_c,
        "cleanup_status": chosen_cleanup,
        "honest_decline_only": honest_only,
    }
    visible_nodes = _filter_nodes(nodes, filters)

    visible_edge_types = {et for et, v in edge_filters.items() if v}
    visible_families = sorted({n["artifact_family"] for n in visible_nodes})

    # ------- 3D figure -------
    st.subheader("Atlas — typed multigraph")
    if visible_nodes:
        fig = _build_3d_figure(
            visible_nodes,
            edges,
            visible_edge_types,
            set(visible_families),
            depth_axis,
        )
        if fig is not None:
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displaylogo": False},
                key="pg_atlas_3d",
            )
        else:
            render_empty_state(
                reason="No nodes matched the active filters.",
                expected_artifact="reports/project_genealogy/atlas_latest.json",
            )
    else:
        render_empty_state(
            reason="No nodes matched the active filters.",
            expected_artifact="reports/project_genealogy/atlas_latest.json",
        )

    # ------- Mission Coherence panel -------
    st.subheader("Mission Coherence")
    if coherence is None:
        render_empty_state(
            reason="coherence_latest.json missing — Pass 4 has not run.",
            expected_artifact="reports/project_genealogy/coherence_latest.json",
        )
    else:
        coverage_by_atom = coherence.get("coverage_by_atom", [])
        cohort_alignment = coherence.get("cohort_alignment", [])
        # Counts must match atlas summary (D22 banner if not).
        coh_counts = coherence.get("summary", {}).get("mission_coverage_status_counts", {})
        atlas_coh_counts = summary.get("mission_coverage_status_counts", {})
        if coh_counts != atlas_coh_counts:
            render_html(panel(
                title="degraded state — mission coverage count mismatch",
                content=(
                    f"atlas.summary={atlas_coh_counts}, coherence.summary={coh_counts}. "
                    f"Tab does not reconcile silently."
                ),
                status="failed",
            ))
        for entry in coverage_by_atom:
            badge_status = {
                "covered": "verified",
                "partial": "active",
                "orphan": "failed",
                "declined": "trace",
            }.get(entry.get("coverage_status", ""), "trace")
            st.markdown(
                f"- **{entry['mission_atom_id']}** "
                f"`{entry.get('coverage_status', '')}`: {entry.get('statement', '')}"
            )
        # Cohort alignment heatmap (textual; visual heatmap is post-PG-001).
        align_status_counts = coherence.get("summary", {}).get("cohort_alignment_status_counts", {})
        st.caption(f"cohort alignment: {dict(align_status_counts)}")
        traj = coherence.get("trajectory", {})
        st.caption(f"trajectory: {traj.get('trajectory_status', 'insufficient_history')}")

    # ------- Removable Files panel -------
    st.subheader("Removable Files (candidates)")
    cleanup_counts = summary.get("cleanup_candidate_count_by_status", {})
    if not cleanup_counts:
        render_empty_state(
            reason="No cleanup-candidate data; run-all has not produced liveness.",
            expected_artifact="reports/project_genealogy/atlas_latest.json#liveness_index",
        )
    else:
        cs_cols = st.columns(len(cleanup_counts))
        for i, (status, count) in enumerate(sorted(cleanup_counts.items())):
            with cs_cols[i]:
                render_html(metric_card(
                    label=status,
                    value=str(count),
                    subtext="probe outcome",
                    status="trace",
                ))
        st.caption(
            "Removable Files panel surfaces probe-outcome distribution. "
            "PG-001 v1 budgets per-file probes at zero seconds; status "
            "defaults to `unknown` rather than over-claim."
        )

    # ------- Findings table -------
    st.subheader("Findings")
    findings_list: list[dict[str, Any]] = []
    for n in visible_nodes[:200]:
        try:
            d = json.loads(Path(n["dossier_path"]).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for fnd in d.get("findings", [])[:5]:
            findings_list.append({
                "path": n["path"],
                "finding_id": fnd.get("finding_id", ""),
                "severity": fnd.get("severity", ""),
                "status": fnd.get("status", ""),
                "claim": fnd.get("claim", "")[:160],
                "mistake_classes": ", ".join(fnd.get("mistake_classes", [])),
                "reproducible": bool(fnd.get("reproducer", {}).get("command")),
            })
    if findings_list:
        st.dataframe(findings_list, use_container_width=True, height=400)
    else:
        render_empty_state(
            reason="No findings emitted by the active filter set.",
            expected_artifact="reports/project_genealogy/atlas_latest.json#mistake_class_index",
        )

    # ------- Run binding footer -------
    rb = atlas.get("run_binding", {})
    st.caption(
        f"atlas hash: `{atlas.get('content_hash', '')[:24]}…`  "
        f"| manifest: `{rb.get('input_manifest_hash', '')[:24]}…`  "
        f"| branch: `{rb.get('branch', '')}`  "
        f"| HEAD: `{(rb.get('head_commit') or '')[:8]}`  "
        f"| generated_at: `{rb.get('generated_at', '')}`"
    )
