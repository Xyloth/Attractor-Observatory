"""Design tokens for the Observatory Control Room.

Centralizes the visual language declared in ``Control Room v0.txt`` §14
(Visual design system) and §6 (Visual identity). No room may inline a
hex code, font weight, or animation duration; everything routes through
constants here.

Color semantics, motion semantics, typography hierarchy, and density
guidance follow proposal §14. Dark-mode default per proposal §6.
"""

from __future__ import annotations

from typing import Final


# ----------------------------------------------------------------------
# Color semantics (proposal §14.1)
# ----------------------------------------------------------------------
# Each color is a *semantic role*, not a decorative choice. Rooms and
# components consume the role names; the hex values are tuned for
# dark-mode legibility and contrast against COLOR_BG_DEEP.

COLOR_BG_DEEP: Final[str] = "#0a0e16"          # background, observatory deep
COLOR_BG_PANEL: Final[str] = "#121826"         # panel surface
COLOR_BG_PANEL_RAISED: Final[str] = "#1a2032"  # raised card surface
COLOR_BORDER: Final[str] = "#283042"           # subtle panel border

COLOR_VERIFIED: Final[str] = "#3ddc84"         # green — verified / pass / healthy
COLOR_WARNING: Final[str] = "#f5a623"          # amber — needs review
COLOR_FAILED: Final[str] = "#ff5468"           # red — failed / falsifier / high risk
COLOR_ACTIVE: Final[str] = "#4fc3f7"           # blue — active / in progress
COLOR_MOTIF: Final[str] = "#bd6df8"            # purple — motif / formalism
COLOR_TRACE: Final[str] = "#22d3ee"            # cyan — trace / world activity
COLOR_UNAVAILABLE: Final[str] = "#5b6478"      # gray — unavailable / unknown
COLOR_CLAIM_BEARING: Final[str] = "#f8f9fa"    # white — claim-bearing / high-confidence text
COLOR_TEXT_PRIMARY: Final[str] = "#e3e6ec"     # primary copy
COLOR_TEXT_SECONDARY: Final[str] = "#9aa0ac"   # secondary copy
COLOR_TEXT_MUTED: Final[str] = "#6c7484"       # muted / metadata


# Status to color mapping (canonical)
STATUS_COLORS: Final[dict[str, str]] = {
    "ok": COLOR_VERIFIED,
    "verified": COLOR_VERIFIED,
    "pass": COLOR_VERIFIED,
    "healthy": COLOR_VERIFIED,
    "claim_bearing": COLOR_CLAIM_BEARING,
    "warning": COLOR_WARNING,
    "needs_review": COLOR_WARNING,
    "exploratory": COLOR_WARNING,
    "failed": COLOR_FAILED,
    "fail": COLOR_FAILED,
    "falsifier": COLOR_FAILED,
    "high_risk": COLOR_FAILED,
    "active": COLOR_ACTIVE,
    "in_progress": COLOR_ACTIVE,
    "motif": COLOR_MOTIF,
    "formalism": COLOR_MOTIF,
    "trace": COLOR_TRACE,
    "world_activity": COLOR_TRACE,
    "unavailable": COLOR_UNAVAILABLE,
    "unknown": COLOR_UNAVAILABLE,
    "missing": COLOR_UNAVAILABLE,
    "malformed": COLOR_UNAVAILABLE,
}


# ----------------------------------------------------------------------
# Motion semantics (proposal §14.2)
# ----------------------------------------------------------------------
# Animation durations in milliseconds. Motion encodes meaning:
#   pulse ........ active process
#   slow_glow .... live monitored item
#   flash ........ recent event (< 5 minutes)
#   fade ......... historical artifact
#   orbit/flow ... dependency or trace relation
#   jitter ....... uncertainty (used sparingly)

MOTION_PULSE_MS: Final[int] = 1800
MOTION_SLOW_GLOW_MS: Final[int] = 4200
MOTION_FLASH_MS: Final[int] = 600
MOTION_FADE_MS: Final[int] = 800
MOTION_ORBIT_MS: Final[int] = 8000
MOTION_JITTER_MS: Final[int] = 300

# Motion is OFF by default in print/screenshot/test contexts.
MOTION_ENABLED_DEFAULT: Final[bool] = True


# ----------------------------------------------------------------------
# Typography hierarchy (proposal §14.3)
# ----------------------------------------------------------------------
# Font sizes are CSS-compatible strings; weights follow CSS conventions.
# Hierarchy is explicit rather than relative so screenshots remain
# legible at multiple zoom levels.

FONT_FAMILY_DISPLAY: Final[str] = (
    "'Space Grotesk', 'Inter', 'system-ui', sans-serif"
)
FONT_FAMILY_BODY: Final[str] = (
    "'Inter', 'system-ui', -apple-system, BlinkMacSystemFont, sans-serif"
)
FONT_FAMILY_MONO: Final[str] = (
    "'JetBrains Mono', 'IBM Plex Mono', ui-monospace, 'Cascadia Code', monospace"
)

FONT_SIZE_STATUS_NUMBER: Final[str] = "2.6rem"
FONT_SIZE_HEADING_1: Final[str] = "2.0rem"
FONT_SIZE_HEADING_2: Final[str] = "1.4rem"
FONT_SIZE_HEADING_3: Final[str] = "1.1rem"
FONT_SIZE_BODY: Final[str] = "0.95rem"
FONT_SIZE_LABEL: Final[str] = "0.85rem"
FONT_SIZE_DETAIL: Final[str] = "0.78rem"

FONT_WEIGHT_DISPLAY: Final[int] = 600
FONT_WEIGHT_HEADING: Final[int] = 600
FONT_WEIGHT_BODY: Final[int] = 400
FONT_WEIGHT_LABEL: Final[int] = 500
FONT_WEIGHT_MONO: Final[int] = 500


# ----------------------------------------------------------------------
# Density / layout
# ----------------------------------------------------------------------
# The proposal calls for "dense, but layered." First glance simple, click
# drill-down detailed.

DENSITY_PANEL_PADDING_REM: Final[float] = 1.2
DENSITY_CARD_GAP_REM: Final[float] = 0.6
DENSITY_SECTION_GAP_REM: Final[float] = 1.6
DENSITY_BORDER_RADIUS_REM: Final[float] = 0.5


# ----------------------------------------------------------------------
# Streamlit page config defaults
# ----------------------------------------------------------------------

PAGE_TITLE: Final[str] = "Attractor Observatory Control Room"
PAGE_SUBTITLE: Final[str] = (
    "Live command interface for worlds, campaigns, motifs, falsifiers, "
    "and AI research operations."
)
PAGE_ICON: Final[str] = "📡"
PAGE_LAYOUT: Final[str] = "wide"


def status_color(status: str, fallback: str = COLOR_UNAVAILABLE) -> str:
    """Look up a hex color for a status name, with fallback for unknowns."""
    return STATUS_COLORS.get(status.lower(), fallback)


def streamlit_theme_css() -> str:
    """Return inline CSS that applies the design tokens to the
    Streamlit shell. Used once at app entry.

    Inlines the full canonical design system from
    ``Visuals/colors_and_type.css`` (the source of truth for the
    Attractor Observatory visual identity, declared in v1.2 §6 + §14)
    plus a Streamlit-specific shell layer that overrides Streamlit's
    default theming with the dark observatory base.

    The Visuals/ stylesheet is loaded at runtime via Path read; if it
    cannot be read (deployment context lacks Visuals/), the function
    falls back to the Python-token-derived shell CSS so the app still
    renders coherently.
    """
    visuals_css = _load_visuals_css()
    shell_css = f"""
    /* ============================================================
     * Streamlit shell overrides — wires the design tokens above
     * onto Streamlit's default surfaces.
     * ============================================================ */
    .stApp {{
        background: var(--bg-deep, {COLOR_BG_DEEP});
        color: var(--fg2, {COLOR_TEXT_PRIMARY});
        font-family: var(--font-body, {FONT_FAMILY_BODY});
    }}
    [data-testid="stSidebar"] {{
        background: var(--bg-deeper, #060912);
        border-right: 1px solid var(--border, {COLOR_BORDER});
    }}
    [data-testid="stSidebar"] .stRadio label {{
        color: var(--fg2, {COLOR_TEXT_PRIMARY}) !important;
        font-family: var(--font-body, {FONT_FAMILY_BODY}) !important;
        font-size: var(--fs-body, {FONT_SIZE_BODY}) !important;
    }}
    [data-testid="stSidebar"] .stMarkdown {{
        color: var(--fg2, {COLOR_TEXT_PRIMARY});
    }}
    /* Hide Streamlit chrome that visually intrudes on the cockpit feel. */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    [data-testid="stDecoration"] {{ visibility: hidden; }}
    /* Card / panel surfaces declared by the canonical stylesheet are
     * already styled. The shell layer below adds Streamlit-specific
     * fallback styles for components Streamlit renders by default. */
    .control-room-headline {{
        font-family: var(--font-display, {FONT_FAMILY_DISPLAY});
        font-size: var(--fs-h1, {FONT_SIZE_HEADING_1});
        font-weight: var(--fw-display, {FONT_WEIGHT_DISPLAY});
        color: var(--fg1, {COLOR_CLAIM_BEARING});
        letter-spacing: var(--tracking-tight, 0.02em);
    }}
    .control-room-subtitle {{
        font-family: var(--font-body, {FONT_FAMILY_BODY});
        font-size: var(--fs-h3, {FONT_SIZE_HEADING_3});
        color: var(--fg3, {COLOR_TEXT_SECONDARY});
        margin-bottom: 1.4rem;
    }}
    .control-room-panel {{
        background: var(--bg-panel, {COLOR_BG_PANEL});
        border: 1px solid var(--border, {COLOR_BORDER});
        border-radius: var(--radius-lg, 12px);
        padding: var(--space-5, 20px);
        margin-bottom: var(--space-4, 16px);
    }}
    /* Empty-state block (D22 binding). Mirrors the Visuals/ canonical
     * .empty-state class with control_room/-specific selectors so the
     * existing render_empty_state_html() output remains compatible. */
    .control-room-empty {{
        background: var(--bg-panel, {COLOR_BG_PANEL});
        border: 1px dashed var(--border-dashed, #4a5266);
        border-radius: var(--radius-lg, 12px);
        padding: var(--space-6, 24px) var(--space-5, 20px);
        font-family: var(--font-mono, {FONT_FAMILY_MONO});
        color: var(--fg3, {COLOR_TEXT_SECONDARY});
    }}
    .control-room-empty-label {{
        color: var(--unavailable, {COLOR_UNAVAILABLE});
        font-weight: var(--fw-label, {FONT_WEIGHT_LABEL});
        text-transform: uppercase;
        letter-spacing: var(--tracking-cap, 0.08em);
        font-size: var(--fs-detail, {FONT_SIZE_DETAIL});
        margin-bottom: 0.5rem;
    }}
    .control-room-empty-reason {{
        color: var(--fg2, {COLOR_TEXT_PRIMARY});
        font-size: var(--fs-body, {FONT_SIZE_BODY});
        font-family: var(--font-body, {FONT_FAMILY_BODY});
        margin-bottom: 0.5rem;
    }}
    .control-room-empty-expected {{
        color: var(--fg4, {COLOR_TEXT_MUTED});
        font-size: var(--fs-label, {FONT_SIZE_LABEL});
    }}
    /* Metric / status pills mirror Visuals/ .pill semantics */
    .control-room-status-pill {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0.2rem 0.7rem;
        border-radius: var(--radius-pill, 999px);
        font-size: var(--fs-detail, {FONT_SIZE_DETAIL});
        font-weight: var(--fw-label, {FONT_WEIGHT_LABEL});
        font-family: var(--font-mono, {FONT_FAMILY_MONO});
        letter-spacing: var(--tracking-cap, 0.08em);
        text-transform: uppercase;
    }}
    /* World card and room emblem chrome */
    .room-emblem {{
        display: flex;
        align-items: center;
        gap: var(--space-3, 12px);
        margin-bottom: var(--space-4, 16px);
    }}
    .room-emblem .emblem-glyph {{
        width: 48px; height: 48px;
        flex-shrink: 0;
        opacity: 0.92;
    }}
    .room-emblem .emblem-text-name {{
        font-family: var(--font-display, {FONT_FAMILY_DISPLAY});
        font-size: var(--fs-h1, {FONT_SIZE_HEADING_1});
        font-weight: var(--fw-display, {FONT_WEIGHT_DISPLAY});
        color: var(--fg1, {COLOR_CLAIM_BEARING});
        letter-spacing: var(--tracking-tight, -0.01em);
    }}
    .room-emblem .emblem-text-tagline {{
        font-family: var(--font-body, {FONT_FAMILY_BODY});
        font-size: var(--fs-h3, {FONT_SIZE_HEADING_3});
        color: var(--fg3, {COLOR_TEXT_SECONDARY});
        margin-top: 2px;
    }}
    .world-card {{
        background: var(--bg-panel, {COLOR_BG_PANEL});
        border: 1px solid var(--border, {COLOR_BORDER});
        border-radius: var(--radius-md, 8px);
        padding: var(--space-3, 12px);
        margin-bottom: var(--space-2, 8px);
        display: flex;
        align-items: flex-start;
        gap: var(--space-3, 12px);
    }}
    .world-card .world-glyph {{ width: 40px; height: 40px; flex-shrink: 0; opacity: 0.85; }}
    .world-card .world-name {{
        font-family: var(--font-display, {FONT_FAMILY_DISPLAY});
        font-size: var(--fs-h3, {FONT_SIZE_HEADING_3});
        font-weight: var(--fw-heading, {FONT_WEIGHT_HEADING});
        color: var(--fg1, {COLOR_CLAIM_BEARING});
    }}
    .world-card .world-meta {{
        font-family: var(--font-mono, {FONT_FAMILY_MONO});
        font-size: var(--fs-detail, {FONT_SIZE_DETAIL});
        color: var(--fg4, {COLOR_TEXT_MUTED});
        margin-top: 2px;
    }}
    """
    return f"<style>\n{visuals_css}\n{shell_css}\n</style>"


def _load_visuals_css() -> str:
    """Read ``Visuals/colors_and_type.css`` if available; return empty
    string otherwise so the shell CSS still produces a coherent result.

    This is a READ; it does not violate D22 read-only enforcement (the
    test scanner only flags writes). The Visuals/ directory is the
    design source-of-truth and stays unchanged.
    """
    from pathlib import Path
    candidates = [
        Path("Visuals/colors_and_type.css"),
        Path(__file__).resolve().parents[1] / "Visuals" / "colors_and_type.css",
    ]
    for candidate in candidates:
        if candidate.exists():
            try:
                return candidate.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
    return ""
