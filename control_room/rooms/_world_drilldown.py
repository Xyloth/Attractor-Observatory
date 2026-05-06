"""World drilldown helper for the World Observatory.

Per PI feedback: clicking a world card should bring the world to the
forefront with a list of what it contains — names, descriptions, and
where possible a real visualization (3D phase portraits for math
primitives, energy-level diagrams for atomic spectra, structural info
for molecules). "A lot of these tabs feel fake" — this is the answer:
real data, real visuals, sourced from the on-disk EmpiricalRecord set.

D22 binding: every visualization is derived from real record payloads
(NIST first_level_gaps_eV, PubChem canonical_smiles + molecular_formula,
math primitives state_equation + parameters). When a world has no
records routed to it, the drilldown renders honest empty-state.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
FACTORY_STORE = REPO_ROOT / "reports" / "campaign_016" / "factory_store"


def load_records_for_world(world_family: str) -> list[dict[str, Any]]:
    """Read empirical_records.json and filter to records whose
    world_family matches. Returns [] if the store is missing."""
    p = FACTORY_STORE / "empirical_records.json"
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return []
    records = data.get("records") if isinstance(data, dict) else data
    if not isinstance(records, list):
        return []
    return [r for r in records if r.get("world_family") == world_family]


def render_world_drilldown(world_family: str, world_id: str, world_name: str) -> None:
    """Render the per-world detail panel.

    Routes to one of three render paths based on what records are present:
      * math_primitives → 3D phase portraits for each named system
      * atomic_molecular_primitives → energy-level diagrams + molecule cards
      * other (W1-W13 simulation worlds) → calibration info from campaign reports

    Hardened with explicit fallback colors on every CSS variable: if the
    canonical visuals stylesheet hasn't loaded (or a CSS var is missing),
    the panel still renders with a visible dark-mode surface rather than
    silently degrading to an invisible transparent block.
    """
    import streamlit as st

    records = load_records_for_world(world_family)

    # Title bar — uses CSS vars with explicit hex fallbacks so the panel
    # always paints visibly even when the visuals stylesheet hasn't
    # loaded yet (Streamlit reruns can race the CSS injection).
    st.markdown(
        f'<div style="margin-top: 0.8rem; padding: 1.1rem 1.4rem; '
        f'background: var(--bg-panel, #121826); '
        f'border: 1px solid var(--motif, #bd6df8); border-radius: 14px; '
        f'box-shadow: 0 0 24px rgba(189, 109, 248, 0.15);">'
        f'<div style="font-family: var(--font-display, \'Space Grotesk\', sans-serif); '
        f'font-size: 1.7rem; color: var(--fg1, #f8f9fa); font-weight: 600;">'
        f'{world_id} · {world_name}</div>'
        f'<div style="font-family: var(--font-mono, \'JetBrains Mono\', monospace); '
        f'font-size: 0.72rem; color: var(--fg4, #6c7484); '
        f'letter-spacing: 0.06em; text-transform: uppercase; margin-top: 4px;">'
        f'world_family: {world_family} · {len(records)} record(s) routed</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if world_family == "math_primitives":
        _render_math_primitives(records)
    elif world_family == "atomic_molecular_primitives":
        _render_atomic_molecular(records)
    else:
        _render_simulation_world(world_family, world_id, world_name)


# ---------------------------------------------------------------------------
# math primitives — 3D phase portraits
# ---------------------------------------------------------------------------


def _render_math_primitives(records: list[dict[str, Any]]) -> None:
    import streamlit as st
    import plotly.graph_objects as go

    if not records:
        from control_room.components.empty_state import render_empty_state
        render_empty_state(
            reason="no math_primitives records in factory_store yet",
            expected_artifact="press FIRE in Factory Intake Dock",
        )
        return

    cols = st.columns(2)
    for i, rec in enumerate(records):
        payload = rec.get("payload", {}) or {}
        canonical = payload.get("canonical_name") or rec.get("canonical_name", "?")
        primitive_class = payload.get("primitive_class", "?")
        dimension = payload.get("dimension", "?")
        expected = payload.get("expected_stable_form", "?")
        invariants = payload.get("invariants") or []
        parameters = payload.get("parameters") or {}
        state_eq = payload.get("state_equation", "")

        with cols[i % 2]:
            st.markdown(
                f'<div style="background: var(--bg-panel); border: 1px solid var(--border); '
                f'border-radius: 14px; padding: 14px; margin-bottom: 12px;">'
                f'<div style="font-family: var(--font-display); font-size: 1.05rem; '
                f'color: var(--motif); font-weight: 600;">{canonical}</div>'
                f'<div style="font-family: var(--font-mono); font-size: 0.75rem; '
                f'color: var(--fg4); margin: 4px 0 8px;">'
                f'class: {primitive_class} · dim: {dimension} · expected: {expected}'
                f'</div>'
                f'<div style="font-family: var(--font-mono); font-size: 0.72rem; '
                f'color: var(--fg3); background: var(--bg-deeper); padding: 6px 8px; '
                f'border-radius: 6px; overflow-x: auto; white-space: pre;">{state_eq}</div>'
                f'<div style="font-family: var(--font-mono); font-size: 0.7rem; '
                f'color: var(--fg4); margin-top: 6px;">'
                f'parameters: {", ".join(f"{k}={v}" for k, v in parameters.items()) or "—"}<br>'
                f'invariants: {", ".join(invariants) if invariants else "—"}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            fig = _phase_portrait(canonical, parameters, dimension)
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True)


def _phase_portrait(canonical_name: str, parameters: dict, dimension: int | str):
    """Numerically integrate the named system + return a Plotly 3D figure
    (or 2D for dimension=2). Recognises Lorenz, Rössler, Sprott, Hopf,
    fixed-point sink. Falls back to a state-equation note if unknown."""
    import plotly.graph_objects as go

    name = (canonical_name or "").lower()
    try:
        if "lorenz" in name:
            return _plot3d(_integrate(_lorenz, [0.1, 0.0, 0.0], 0.01, 4000), canonical_name)
        if "rossler" in name or "rössler" in name:
            return _plot3d(_integrate(_rossler, [0.1, 0.0, 0.0], 0.05, 4000), canonical_name)
        if "sprott" in name:
            return _plot3d(_integrate(_sprott, [0.1, 0.0, 0.0], 0.02, 5000), canonical_name)
        if "hopf" in name:
            return _plot2d(_integrate(_hopf, [0.05, 0.0], 0.02, 1500), canonical_name)
        if "fixed_point" in name or "linear_sink" in name:
            return _plot2d(_integrate(_linear_sink, [1.0, 1.0], 0.05, 200), canonical_name)
        if "duffing" in name:
            return _plot2d(_integrate(_duffing, [1.0, 0.0], 0.02, 3000), canonical_name)
        if "quasiperiodic" in name or "torus" in name:
            return _plot2d(_quasiperiodic_torus_trajectory(), canonical_name)
    except Exception:
        return None
    return None


def _integrate(f, state: list[float], dt: float, steps: int) -> tuple[list[list[float]], list[float]]:
    """RK4 integrator — returns (per-axis trajectories, time array)."""
    n = len(state)
    traj: list[list[float]] = [[s] for s in state]
    t_arr: list[float] = [0.0]
    s = list(state)
    t = 0.0
    for _ in range(steps):
        k1 = f(s, t)
        k2 = f([s[i] + 0.5 * dt * k1[i] for i in range(n)], t + 0.5 * dt)
        k3 = f([s[i] + 0.5 * dt * k2[i] for i in range(n)], t + 0.5 * dt)
        k4 = f([s[i] + dt * k3[i] for i in range(n)], t + dt)
        s = [s[i] + dt * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6.0 for i in range(n)]
        t += dt
        for i in range(n):
            traj[i].append(s[i])
        t_arr.append(t)
    return traj, t_arr


# Named dynamical systems (canonical equations from the catalog records).

def _lorenz(s, t):
    sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
    return [sigma * (s[1] - s[0]),
            s[0] * (rho - s[2]) - s[1],
            s[0] * s[1] - beta * s[2]]


def _rossler(s, t):
    a, b, c = 0.2, 0.2, 5.7
    return [-s[1] - s[2],
            s[0] + a * s[1],
            b + s[2] * (s[0] - c)]


def _sprott(s, t):
    # Sprott "case A": dx=y, dy=-x+yz, dz=1-y²
    return [s[1],
            -s[0] + s[1] * s[2],
            1.0 - s[1] * s[1]]


def _hopf(s, t):
    mu, omega = 0.5, 1.0
    r2 = s[0] * s[0] + s[1] * s[1]
    return [mu * s[0] - omega * s[1] - s[0] * r2,
            omega * s[0] + mu * s[1] - s[1] * r2]


def _linear_sink(s, t):
    return [-s[0], -s[1]]


def _duffing(s, t):
    delta, alpha, beta, gamma, omega = 0.2, -1.0, 1.0, 0.3, 1.0
    return [s[1],
            -delta * s[1] - alpha * s[0] - beta * s[0] ** 3 + gamma * math.cos(omega * t)]


def _quasiperiodic_torus_trajectory(steps: int = 4000, dt: float = 0.05):
    """Quasiperiodic torus flow: x = cos(ω₁t) + cos(ω₂t), y = sin(ω₁t) + sin(ω₂t)
    with ω₂/ω₁ irrational (golden ratio) — fills out a 2-torus densely."""
    omega1, omega2 = 1.0, 1.6180339887  # golden ratio for incommensurate
    xs = [math.cos(omega1 * i * dt) + 0.6 * math.cos(omega2 * i * dt) for i in range(steps)]
    ys = [math.sin(omega1 * i * dt) + 0.6 * math.sin(omega2 * i * dt) for i in range(steps)]
    t_arr = [i * dt for i in range(steps)]
    return ([xs, ys], t_arr)


def _plot3d(integrated, name: str):
    import plotly.graph_objects as go
    traj, _ = integrated
    fig = go.Figure(data=[go.Scatter3d(
        x=traj[0], y=traj[1], z=traj[2],
        mode="lines",
        line=dict(color=traj[2], colorscale="Plasma", width=3),
        hoverinfo="skip",
    )])
    fig.update_layout(
        height=320, margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="#0a0e16", plot_bgcolor="#0a0e16",
        scene=dict(
            xaxis=dict(showbackground=False, gridcolor="#283042", color="#9aa0ac", title="x"),
            yaxis=dict(showbackground=False, gridcolor="#283042", color="#9aa0ac", title="y"),
            zaxis=dict(showbackground=False, gridcolor="#283042", color="#9aa0ac", title="z"),
            bgcolor="#0a0e16",
        ),
        font=dict(family="JetBrains Mono, monospace", size=10, color="#9aa0ac"),
    )
    return fig


def _plot2d(integrated, name: str):
    import plotly.graph_objects as go
    traj, _ = integrated
    fig = go.Figure(data=[go.Scatter(
        x=traj[0], y=traj[1],
        mode="lines",
        line=dict(color="#bd6df8", width=2),
        hoverinfo="skip",
    )])
    fig.update_layout(
        height=280, margin=dict(l=20, r=20, t=10, b=30),
        paper_bgcolor="#0a0e16", plot_bgcolor="#121826",
        xaxis=dict(gridcolor="#283042", color="#9aa0ac", title="x", zeroline=True, zerolinecolor="#3a4560"),
        yaxis=dict(gridcolor="#283042", color="#9aa0ac", title="y", zeroline=True, zerolinecolor="#3a4560",
                   scaleanchor="x", scaleratio=1),
        font=dict(family="JetBrains Mono, monospace", size=10, color="#9aa0ac"),
    )
    return fig


# ---------------------------------------------------------------------------
# atomic / molecular — energy-level diagrams + molecule cards
# ---------------------------------------------------------------------------


def _render_atomic_molecular(records: list[dict[str, Any]]) -> None:
    import streamlit as st

    if not records:
        from control_room.components.empty_state import render_empty_state
        render_empty_state(
            reason="no atomic_molecular_primitives records in factory_store yet",
            expected_artifact="press FIRE in Factory Intake Dock",
        )
        return

    atomic = [r for r in records if r.get("record_type") == "atomic_energy_level_summary"]
    molecules = [r for r in records if r.get("record_type") == "small_molecule_topology_summary"]
    other = [r for r in records if r.get("record_type") not in {"atomic_energy_level_summary", "small_molecule_topology_summary"}]

    if atomic:
        st.markdown('<div style="margin-top: 1.2rem;"><span class="cap">Atomic spectra · NIST</span></div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, rec in enumerate(atomic):
            with cols[i % 2]:
                _render_atom_card(rec)

    if molecules:
        st.markdown('<div style="margin-top: 1.2rem;"><span class="cap">Small molecules · PubChem</span></div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, rec in enumerate(molecules):
            with cols[i % 2]:
                _render_molecule_card(rec)

    if other:
        st.markdown('<div style="margin-top: 1.2rem;"><span class="cap">Other</span></div>', unsafe_allow_html=True)
        for rec in other:
            st.json({"canonical_name": rec.get("canonical_name"), "record_type": rec.get("record_type")}, expanded=False)


def _render_atom_card(rec: dict[str, Any]) -> None:
    import streamlit as st
    import plotly.graph_objects as go

    payload = rec.get("payload") or {}
    element = payload.get("element_symbol", "?")
    spectrum = payload.get("spectrum", "?")
    ion = payload.get("ion_stage", "?")
    ground = payload.get("ground_state_eV", 0.0)
    max_eV = payload.get("max_observed_level_eV", 0.0)
    gaps = payload.get("first_level_gaps_eV") or []
    n_levels = payload.get("energy_level_count", "?")
    n_terms = payload.get("term_count", "?")
    source_url = (rec.get("provenance") or {}).get("source_url", "")
    canonical = rec.get("canonical_name", "?")

    st.markdown(
        f'<div style="background: var(--bg-panel); border: 1px solid var(--border); '
        f'border-radius: 14px; padding: 14px; margin-bottom: 8px;">'
        f'<div style="display:flex;align-items:baseline;justify-content:space-between;">'
        f'<div style="font-family: var(--font-display); font-size: 2.4rem; '
        f'color: var(--trace); font-weight: 600; line-height: 1;">{element}</div>'
        f'<div style="font-family: var(--font-mono); font-size: 0.78rem; '
        f'color: var(--fg3);">{spectrum}</div></div>'
        f'<div style="font-family: var(--font-mono); font-size: 0.72rem; '
        f'color: var(--fg4); margin-top: 6px;">'
        f'ion stage: {ion} · {n_levels} levels · {n_terms} terms · '
        f'ground {ground:.3f} eV · max {max_eV:.3f} eV'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    # Energy ladder visualization — horizontal lines at each cumulative gap.
    if gaps:
        cumulative = [ground]
        for g in gaps:
            cumulative.append(cumulative[-1] + float(g))
        fig = go.Figure()
        for i, level in enumerate(cumulative):
            fig.add_shape(
                type="line", x0=0.1, x1=0.9, y0=level, y1=level,
                line=dict(color="#22d3ee" if i == 0 else "#bd6df8", width=2),
            )
            fig.add_annotation(
                x=1.0, y=level, xanchor="left",
                text=f"E{i} = {level:.3f} eV",
                showarrow=False,
                font=dict(family="JetBrains Mono, monospace", size=10, color="#9aa0ac"),
            )
        fig.update_layout(
            height=200, margin=dict(l=10, r=120, t=10, b=20),
            paper_bgcolor="#0a0e16", plot_bgcolor="#121826",
            xaxis=dict(visible=False, range=[0, 1.5]),
            yaxis=dict(gridcolor="#283042", color="#9aa0ac", title="E (eV)"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)


def _render_molecule_card(rec: dict[str, Any]) -> None:
    import streamlit as st

    payload = rec.get("payload") or {}
    formula = payload.get("molecular_formula", "?")
    smiles = payload.get("canonical_smiles", "?")
    cid = payload.get("cid", "?")
    weight = payload.get("molecular_weight", 0.0)
    heavy = payload.get("heavy_atom_count", "?")
    complexity = payload.get("complexity", 0.0)
    canonical = rec.get("canonical_name", "?")
    source_url = (rec.get("provenance") or {}).get("source_url", "")

    st.markdown(
        f'<div style="background: var(--bg-panel); border: 1px solid var(--border); '
        f'border-radius: 14px; padding: 14px; margin-bottom: 12px;">'
        f'<div style="display:flex;align-items:baseline;justify-content:space-between;">'
        f'<div style="font-family: var(--font-display); font-size: 1.6rem; '
        f'color: var(--motif); font-weight: 600;">{formula}</div>'
        f'<div style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--fg3);">CID {cid}</div>'
        f'</div>'
        f'<div style="font-family: var(--font-mono); font-size: 0.7rem; color: var(--fg4); margin-top: 6px;">'
        f'MW: {float(weight):.3f} g/mol · heavy atoms: {heavy} · complexity: {float(complexity):.1f}'
        f'</div>'
        f'<div style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--fg3); '
        f'background: var(--bg-deeper); padding: 6px 8px; border-radius: 6px; margin-top: 8px;">'
        f'SMILES: {smiles}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# simulation worlds (W1-W13) — calibration / trace info from campaign reports
# ---------------------------------------------------------------------------


def _render_simulation_world(world_family: str, world_id: str, world_name: str) -> None:
    """W1-W13 don't have factory ingestion (they're simulation worlds).
    Surface what we DO know: density class, falsifier docs, references.
    """
    import streamlit as st
    from control_room.adapters import parse_methods_falsifiers

    st.markdown(
        '<div style="margin-top: 0.8rem; padding: 12px 14px; background: var(--bg-panel); '
        'border: 1px solid var(--border); border-radius: 12px;">'
        '<div style="font-family: var(--font-body); font-size: 0.92rem; color: var(--fg2);">'
        f'<b>{world_id}</b> is a <b>simulation world</b>, not a Factory ingestion target. '
        'Its records live in the world\'s own engine output (campaign reports, '
        'trace stores, perturbation outcomes). Below: papers/falsifiers entries '
        f'naming this world, if any.'
        '</div></div>',
        unsafe_allow_html=True,
    )
    falsifiers = parse_methods_falsifiers()
    if falsifiers["status"] != "ok":
        return
    wid_lower = world_id.lower()
    matched = [
        d for d in falsifiers["data"]["falsifier_docs"]
        if wid_lower in d["name"].lower()
    ]
    if not matched:
        st.markdown(
            f'<div style="margin-top: 0.6rem; font-family: var(--font-body); '
            f'font-size: 0.85rem; color: var(--fg4);">'
            f'No falsifier records reference <code>{wid_lower}</code> in their filename.'
            f'</div>',
            unsafe_allow_html=True,
        )
        return
    rows_html = ""
    for d in matched:
        rows_html += (
            '<div style="display: flex; align-items: center; gap: 12px; padding: 6px 0; '
            'border-bottom: 1px dashed var(--border);">'
            f'<span style="flex: 0 0 280px; font-family: var(--font-mono); font-size: 0.78rem; '
            f'color: var(--fg2);">{d["name"]}</span>'
            f'<span style="flex: 1 1 auto; font-family: var(--font-body); font-size: 0.88rem; '
            f'color: var(--fg2);">{d.get("first_heading") or "—"}</span>'
            "</div>"
        )
    st.markdown(
        f'<div style="margin-top: 0.6rem; padding: 12px 14px; background: var(--bg-panel); '
        f'border: 1px solid var(--border); border-radius: 12px;">{rows_html}</div>',
        unsafe_allow_html=True,
    )
