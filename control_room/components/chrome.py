"""Reusable visual chrome for Control Room rooms.

These helpers translate the JSX patterns under
``Visuals/ui_kits/control_room/`` into Streamlit-compatible
HTML/markdown. Every helper consumes the canonical design tokens from
``control_room.design_tokens`` (which inlines
``Visuals/colors_and_type.css`` at app startup) so component output
matches the canonical visual language declared in proposal §6 + §14.

The helpers are pure HTML-string generators where possible; rooms call
them and pass the result to ``st.markdown(html, unsafe_allow_html=True)``.
This keeps the components testable without a Streamlit runtime and
makes the JSX → Streamlit translation one-to-one.

D22 binding: nothing in this module produces "fake" or "placeholder"
content. Every helper takes the data it needs as arguments; rooms are
responsible for routing absent data through ``render_empty_state``.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any, Iterable, Optional


# Canonical SVG asset paths — the static/ runtime tree.
_STATIC_ROOT = Path(__file__).resolve().parents[1] / "static"
_ROOM_ICON_DIR = _STATIC_ROOT / "room-icons"
_WORLD_ICON_DIR = _STATIC_ROOT / "world-icons"
_LOGO_DIR = _STATIC_ROOT / "logo"


# Status taxonomy (mirrors Visuals/colors_and_type.css `.pill.<status>`).
STATUS_TO_PILL_CLASS = {
    "ok": "verified",
    "verified": "verified",
    "pass": "verified",
    "healthy": "verified",
    "passed": "verified",
    "green": "verified",
    "active": "active",
    "in_progress": "active",
    "warning": "warning",
    "exploratory": "warning",
    "candidate": "warning",
    "needs_review": "warning",
    "amber": "warning",
    "yellow": "warning",
    "failed": "failed",
    "fail": "failed",
    "falsifier": "failed",
    "falsified": "failed",
    "high_risk": "failed",
    "red": "failed",
    "motif": "motif",
    "formalism": "motif",
    "trace": "trace",
    "world_activity": "trace",
    "missing": "unavailable",
    "malformed": "unavailable",
    "unavailable": "unavailable",
    "unknown": "unavailable",
    "skipped": "unavailable",
    "no_data": "unavailable",
}


def pill_class(status: str) -> str:
    """Map a status label to one of the 7 canonical pill class names."""
    return STATUS_TO_PILL_CLASS.get(str(status).lower(), "unavailable")


def status_pill(label: str, status: str = "active") -> str:
    """Return inline HTML for a status pill matching the .pill class."""
    klass = pill_class(status)
    return f'<span class="pill {klass}">{escape(str(label))}</span>'


def _read_svg(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def room_emblem(name: str, tagline: str, room_id: str) -> str:
    """Render the room title bar with the SVG glyph from
    ``static/room-icons/<room_id>.svg``."""
    glyph_path = _room_icon_path_for(room_id)
    glyph_svg = _read_svg(glyph_path)
    if not glyph_svg:
        glyph_svg = '<div class="emblem-glyph"></div>'
    return (
        f'<div class="room-emblem">'
        f'<div class="emblem-glyph">{glyph_svg}</div>'
        f'<div>'
        f'<div class="emblem-text-name">{escape(name)}</div>'
        f'<div class="emblem-text-tagline">{escape(tagline)}</div>'
        f'</div>'
        f'</div>'
    )


def _room_icon_path_for(room_id: str) -> Path:
    canonical = {
        "pulse_deck": "pulse-deck.svg",
        "world_observatory": "world-observatory.svg",
        "campaign_command": "campaign-command.svg",
        "ai_operations_tower": "ai-ops-tower.svg",
        "motif_atlas": "motif-atlas.svg",
        "basin_floor_lab": "basin-floor-lab.svg",
        "falsifier_ledger": "falsifier-ledger.svg",
        "doctrine_console": "doctrine-console.svg",
        "factory_intake_dock": "factory-intake.svg",
        "portfolio_demo": "portfolio-demo.svg",
    }
    return _ROOM_ICON_DIR / canonical.get(room_id, "")


WORLD_ICON_FILE = {
    "chemistry": "w1-chemistry.svg",
    "crn": "w1-chemistry.svg",
    "protocell": "w2-protocell.svg",
    "field": "w3-field.svg",
    "morphogenesis": "w4-morphogenesis.svg",
    "digital": "w5-digital.svg",
    "ecosystem": "w6-ecosystem.svg",
    "swarm": "w7-swarm.svg",
    "cognitive": "w8-cognitive.svg",
    "origins_chemistry": "w9-origins.svg",
    "hypergraph_reactions": "w10-hypergraph.svg",
    "quasispecies": "w11-quasispecies.svg",
    "symbiogenesis": "w12-symbiogenesis.svg",
    "multiscale": "w13-multiscale.svg",
    # CB-007: W0 / W-1 icons. Codex 1.5x is producing these in parallel
    # under TASK-027. We accept any of several plausible filenames so the
    # icon resolves the moment Codex's deliverables land.
    "math_primitives": "w0-math-primitives.svg",
    "atomic_molecular": "w-minus1-atomic-molecular.svg",
}

# CB-007: alternate filenames the icon resolver will try if the canonical
# name above is missing. Lets us accept either of Codex's naming choices.
WORLD_ICON_ALTERNATES: dict[str, list[str]] = {
    "math_primitives": [
        "w0-math.svg", "w0-primitives.svg", "w-zero-math.svg",
    ],
    "atomic_molecular": [
        "w-1-atomic.svg", "w-1-molecular.svg",
        "w-minus-1-atomic-molecular.svg", "wm1-atomic.svg",
    ],
}


def world_icon_svg(world_family: str) -> str:
    """Look up the SVG for a world family.

    Tries the canonical filename first, then any alternates declared in
    ``WORLD_ICON_ALTERNATES``. Returns an empty string if no icon
    resolves — callers (e.g. ``world_card``) render an honest gray
    placeholder block. CB-007: this lets the W0 / W-1 icons "just work"
    the moment Codex 1.5x's parallel deliverables land in the static dir.
    """
    family_lower = world_family.lower()
    fname = WORLD_ICON_FILE.get(family_lower)
    candidates = []
    if fname:
        candidates.append(fname)
    candidates.extend(WORLD_ICON_ALTERNATES.get(family_lower, []))
    for candidate in candidates:
        path = _WORLD_ICON_DIR / candidate
        if path.exists():
            return _read_svg(path)
    return ""


def world_card(name: str, world_family: str, status: str, meta_lines: list[str] | list[dict[str, str]]) -> str:
    """Render a world card matching Visuals/preview/world-card.html shape.

    ``meta_lines`` accepts either:
      * list of plain strings — rendered as-is;
      * list of ``{"display": str, "tooltip": str}`` dicts — rendered with
        a ``title`` attribute so hover surfaces the underlying variable
        name (e.g., ``Family: math primitives`` displayed, with hover
        ``world_family: math_primitives``). This is the path used by the
        World Observatory after the CB-007 polish pass that asked for
        humanized labels with the raw variable available on hover.
    """
    glyph = world_icon_svg(world_family) or '<div style="width:40px;height:40px;background:var(--unavailable-soft);border-radius:8px;"></div>'
    pill_html = status_pill(status, status=status)
    meta_pieces: list[str] = []
    for m in meta_lines:
        if isinstance(m, dict):
            display = escape(str(m.get("display", "")))
            tooltip = escape(str(m.get("tooltip", "")))
            meta_pieces.append(
                f'<span title="{tooltip}" '
                f'style="border-bottom:1px dotted var(--fg5);cursor:help;">{display}</span>'
            )
        else:
            meta_pieces.append(escape(str(m)))
    meta_html = "<br>".join(meta_pieces)
    return (
        f'<div class="world-card">'
        f'<div class="world-glyph">{glyph}</div>'
        f'<div style="flex:1;">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;">'
        f'<span class="world-name">{escape(name)}</span>'
        f'{pill_html}'
        f'</div>'
        f'<div class="world-meta">{meta_html}</div>'
        f'</div>'
        f'</div>'
    )


def panel(title: str, body_html: str, raised: bool = False) -> str:
    """Generic .panel wrapper from Visuals/colors_and_type.css."""
    klass = "panel raised" if raised else "panel"
    return (
        f'<div class="{klass}" style="margin-bottom: 16px;">'
        f'<div style="font-family:var(--font-display);font-size:var(--fs-h3);color:var(--fg2);'
        f'font-weight:var(--fw-heading);margin-bottom:10px;">{escape(title)}</div>'
        f'{body_html}'
        f'</div>'
    )


def metric_card(label: str, value: str, status: str = "active", subtext: str = "") -> str:
    """Render a single metric card (eyebrow + value + meta + status)."""
    return (
        f'<div style="background:var(--bg-panel);border:1px solid var(--border);'
        f'border-radius:var(--radius-md);padding:12px;display:flex;flex-direction:column;gap:6px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<span class="cap">{escape(label)}</span>'
        f'{status_pill(status, status=status)}'
        f'</div>'
        f'<div style="font-family:var(--font-mono);font-size:1.1rem;color:var(--fg1);'
        f'font-weight:500;letter-spacing:0.04em;overflow:hidden;text-overflow:ellipsis;'
        f'white-space:nowrap;">{escape(str(value))}</div>'
        f'<div style="font-family:var(--font-mono);font-size:var(--fs-detail);color:var(--fg3);">'
        f'{escape(subtext)}</div>'
        f'</div>'
    )


def needs_attention(alerts: list[dict[str, str]], failed_count: int = 0, warn_count: int = 0) -> str:
    """Render the Pulse Deck "all clear" / "needs attention" lane."""
    all_clear = not alerts and failed_count == 0 and warn_count == 0
    color = "var(--verified)" if all_clear else "var(--failed)"
    label = "all clear" if all_clear else "needs attention"
    summary = f"{failed_count} failed · {warn_count} warning"
    if all_clear:
        body = (
            '<span style="font-family:var(--font-body);font-size:0.92rem;color:var(--fg3);">'
            "no falsifier or warning events surfaced from the most recent BUILD_LOG / pytest cache. "
            "background watchers green.</span>"
        )
    else:
        rows = []
        for a in alerts[:3]:
            rows.append(
                '<div style="display:flex;align-items:center;gap:6px;">'
                f'<span style="width:6px;height:6px;border-radius:50%;background:{color};box-shadow:0 0 6px {color};"></span>'
                f'<span style="color:var(--fg1);font-family:var(--font-body);font-size:0.92rem;">{escape(a.get("text", ""))}</span>'
                f'<span style="color:var(--fg4);font-family:var(--font-mono);font-size:var(--fs-detail);">{escape(a.get("when", ""))}</span>'
                "</div>"
            )
        body = "".join(rows)
    return (
        '<div style="'
        f"background:{'var(--bg-panel)' if all_clear else 'linear-gradient(90deg, rgba(255,84,104,0.06), rgba(245,166,35,0.04) 60%, transparent)'};"
        f"border:1px solid {color};"
        f"border-left:3px solid {color};"
        "border-radius:var(--radius-md);padding:10px 14px;display:flex;align-items:center;gap:14px;min-height:52px;margin-bottom:16px;\">"
        f'<span style="font-family:var(--font-mono);font-size:var(--fs-detail);letter-spacing:var(--tracking-cap);'
        f'text-transform:uppercase;color:{color};flex-shrink:0;font-weight:500;">{label}</span>'
        f'<span style="font-family:var(--font-mono);font-size:var(--fs-detail);color:var(--fg3);'
        f'border-left:1px solid var(--border-strong);padding-left:12px;">{summary}</span>'
        f'<div style="display:flex;gap:14px;flex:1;flex-wrap:wrap;overflow:hidden;">{body}</div>'
        "</div>"
    )


def agent_chip(agent: str, label: Optional[str] = None) -> str:
    """Render an agent identity chip matching Visuals/AgentIdentity.jsx."""
    agent_to_color = {
        "builder": "var(--agent-builder)",
        "claude_builder": "var(--agent-builder)",
        "claude (builder)": "var(--agent-builder)",
        "codex": "var(--agent-codex)",
        "architect": "var(--agent-architect)",
        "claude_architect": "var(--agent-architect)",
        "gpt": "var(--agent-gpt)",
        "human": "var(--agent-human)",
        "human_pi": "var(--agent-human)",
    }
    color = agent_to_color.get(agent.lower(), "var(--unavailable)")
    text = label or agent
    return (
        f'<span style="display:inline-flex;align-items:center;gap:6px;'
        f'background:rgba(0,0,0,0);border:1px solid {color};color:{color};'
        f'padding:2px 8px;border-radius:var(--radius-pill);'
        f'font-family:var(--font-mono);font-size:var(--fs-detail);'
        f'letter-spacing:var(--tracking-cap);text-transform:uppercase;">'
        f'<span style="width:6px;height:6px;background:{color};border-radius:50%;box-shadow:0 0 6px {color};"></span>'
        f'{escape(text)}</span>'
    )


def gate_grid(campaigns: Iterable[dict[str, Any]]) -> str:
    """Render the campaign × gate grid (Visuals/GateGrid.jsx pattern).

    Each campaign row shows: id, status pill, gate counts. The grid is
    visual rather than tabular so the at-a-glance pattern of greens vs
    yellows is preserved.
    """
    rows: list[str] = []
    for c in campaigns:
        cid = c.get("campaign_id", "?")
        status = (c.get("status") or "unknown")
        gate_count = c.get("gate_count")
        passed = c.get("passed_gate_count")
        if gate_count and passed is not None and gate_count > 0:
            ratio = passed / gate_count
        else:
            ratio = None
        if ratio is None:
            bar = '<div style="height:6px;background:var(--unavailable-soft);border-radius:3px;flex:1;"></div>'
            stats = '<span class="cap">no full report</span>'
        else:
            bar = (
                f'<div style="height:6px;background:var(--unavailable-soft);border-radius:3px;flex:1;overflow:hidden;">'
                f'<div style="height:100%;width:{int(ratio*100)}%;'
                f'background:{"var(--verified)" if status == "green" else "var(--warning)" if status in ("in_progress", "yellow") else "var(--failed)" if status in ("failed", "red") else "var(--unavailable)"};"></div>'
                f'</div>'
            )
            stats = f'<span class="cap mono">{passed}/{gate_count}</span>'
        rows.append(
            '<div style="display:grid;grid-template-columns:140px 1fr 110px 80px;align-items:center;'
            'gap:10px;padding:6px 0;border-bottom:1px solid var(--border);">'
            f'<span style="font-family:var(--font-mono);font-size:var(--fs-label);color:var(--fg2);">{escape(cid)}</span>'
            f'{bar}'
            f'{stats}'
            f'{status_pill(status, status=status)}'
            "</div>"
        )
    return '<div style="display:flex;flex-direction:column;gap:0;">' + "".join(rows) + "</div>"


def event_row(when: str, text: str, status: str = "active") -> str:
    color_map = {
        "verified": "var(--verified)",
        "active": "var(--trace)",
        "warning": "var(--warning)",
        "failed": "var(--failed)",
    }
    color = color_map.get(pill_class(status), "var(--active)")
    return (
        '<div style="display:flex;align-items:center;gap:10px;padding:5px 0;'
        'border-bottom:1px dashed var(--border);">'
        f'<span style="font-family:var(--font-mono);font-size:var(--fs-detail);color:var(--fg3);width:80px;flex-shrink:0;">{escape(when)}</span>'
        f'<span style="width:6px;height:6px;border-radius:50%;background:{color};box-shadow:0 0 6px {color};flex-shrink:0;"></span>'
        f'<span style="font-family:var(--font-body);font-size:var(--fs-body);color:var(--fg2);flex:1;">{escape(text)}</span>'
        '</div>'
    )


def doctrine_tablet(doctrine_id: str, title: str, status: str, signed_by: str = "") -> str:
    """Render a doctrine card matching Visuals/DoctrineTablet.jsx."""
    color_map = {
        "foundational": "var(--verified)",
        "binding": "var(--verified)",
        "candidate": "var(--warning)",
        "proposal": "var(--warning)",
    }
    accent = color_map.get(status.lower(), "var(--motif)")
    return (
        f'<div style="background:var(--bg-panel);border:1px solid var(--border);'
        f'border-left:3px solid {accent};border-radius:var(--radius-md);'
        f'padding:12px 14px;margin-bottom:8px;display:flex;align-items:flex-start;gap:12px;">'
        f'<div style="font-family:var(--font-mono);font-size:1.0rem;font-weight:600;color:{accent};'
        f'min-width:48px;letter-spacing:var(--tracking-mono);">{escape(doctrine_id)}</div>'
        f'<div style="flex:1;">'
        f'<div style="font-family:var(--font-display);font-size:var(--fs-h3);color:var(--fg1);">{escape(title)}</div>'
        f'<div style="font-family:var(--font-mono);font-size:var(--fs-detail);color:var(--fg4);margin-top:4px;">'
        f'{("signed by " + escape(signed_by)) if signed_by else ""}</div>'
        '</div></div>'
    )


def render_html(html: str) -> None:
    """Streamlit render with unsafe HTML enabled. Lazy import keeps
    the module testable outside Streamlit."""
    import streamlit as st
    st.markdown(html, unsafe_allow_html=True)
