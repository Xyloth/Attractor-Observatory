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
# CB-007 polish iteration: bumped radius from 0.5rem (~8px) to ~14px so
# panels read more like a polished native macOS surface than a flat
# admin dashboard. Also widens the radius hierarchy in the inline shell
# CSS below.
DENSITY_BORDER_RADIUS_REM: Final[float] = 0.85


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
    /* Hide Streamlit's white header / Deploy bar / hamburger / footer.
     * The Deploy button is a hosted-Streamlit affordance that doesn't
     * apply to a sidecar dashboard, and its white background was the
     * white strip at the top of the screen the user pointed out. */
    [data-testid="stHeader"] {{ display: none !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    [data-testid="stDeployButton"] {{ display: none !important; }}
    [data-testid="stStatusWidget"] {{ display: none !important; }}
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    [data-testid="stDecoration"] {{ display: none !important; }}
    /* Pull the main block to the top now that the header is gone. */
    .stApp > div:first-child {{ padding-top: 0 !important; }}
    [data-testid="stAppViewBlockContainer"] {{
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1480px;
    }}
    [data-testid="stSidebar"] {{
        background: var(--bg-deeper, #060912);
        border-right: 1px solid var(--border, {COLOR_BORDER});
    }}
    /* HEADER NUKE — multiple selectors because Streamlit changes testids
     * across versions. The white bar + Deploy button live in any of these. */
    header,
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stToolbarActions"],
    [data-testid="stDeployButton"],
    [data-testid="stStatusWidget"],
    [data-testid="stMainMenu"],
    [data-testid="stActionButton"],
    [data-testid="stAppDeployButton"],
    .stDeployButton,
    .stAppDeployButton,
    div[class*="DeployButton"],
    div[class*="deployButton"],
    button[kind="header"],
    button[kind="headerNoPadding"] {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
        opacity: 0 !important;
        position: absolute !important;
        left: -9999px !important;
    }}
    .stApp > header {{ display: none !important; }}
    /* In case the header isn't testid'd at all, target the topmost fixed
     * white bar that holds the Deploy button — it lives outside the
     * sidebar and the main block container. */
    body > div:first-child > div:first-child > div:first-child > [data-testid="stHeader"],
    body > div[data-testid="stApp"] > div:first-of-type {{
        display: none !important;
    }}

    /* Sidebar radio: NUKE every native circle/marker/svg/input. The
     * label text becomes the click target; active state is shown via
     * background + glow + left-border accent + brighter color. No dot. */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] {{
        gap: 4px;
    }}
    /* The label is the entire row; we want it to fill the sidebar width. */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label,
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label[data-baseweb="radio"] {{
        color: var(--fg3, {COLOR_TEXT_SECONDARY}) !important;
        font-family: var(--font-display, {FONT_FAMILY_DISPLAY}) !important;
        font-size: 1.18rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.01em !important;
        padding: 10px 14px !important;
        border-radius: 12px !important;
        border-left: 2px solid transparent !important;
        background: transparent !important;
        transition: color 200ms ease, background 200ms ease, border-color 200ms ease, text-shadow 250ms ease, transform 150ms ease;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
    }}
    /* Brute-force hide every native marker variant Streamlit emits.
     * The "white circle that turns red on click" is BaseWeb's radio
     * marker, which can render as: an <input>, an <svg>, a styled
     * <div data-baseweb="radio-marker">, OR just the first child div
     * of the label. Hit ALL of them. */
    [data-testid="stSidebar"] [data-testid="stRadio"] input,
    [data-testid="stSidebar"] [data-testid="stRadio"] svg,
    [data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio-marker"],
    [data-testid="stSidebar"] [data-testid="stRadio"] [class*="StyledRadioMark"],
    [data-testid="stSidebar"] [data-testid="stRadio"] [class*="radio-mark"],
    [data-testid="stSidebar"] [data-testid="stRadio"] [class*="RadioMarker"],
    [data-testid="stSidebar"] [data-testid="stRadio"] label::before {{
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
        position: absolute !important;
        left: -9999px !important;
    }}
    /* Aggressive: collapse every NON-LAST div inside the radio label.
     * BaseWeb renders [marker_container, text_container] as siblings;
     * the marker is always first, the text is always last. This kills
     * the marker even when the inner CSS classes change between
     * Streamlit versions. */
    [data-testid="stSidebar"] [data-testid="stRadio"] label > div:not(:last-child),
    [data-testid="stSidebar"] [data-testid="stRadio"] label > span:not(:last-child) {{
        display: none !important;
        max-width: 0 !important;
        max-height: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    /* Hover */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:hover {{
        color: var(--fg1, {COLOR_CLAIM_BEARING}) !important;
        background: rgba(79, 195, 247, 0.06) !important;
        transform: translateX(2px);
    }}
    /* Active row: blue glow + accent border running down the line.
     * Targets multiple shapes since Streamlit versions vary in DOM. */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked),
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"],
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label[aria-checked="true"] {{
        color: #4fc3f7 !important;
        border-left-color: #4fc3f7 !important;
        background: rgba(79, 195, 247, 0.10) !important;
        text-shadow: 0 0 22px rgba(79, 195, 247, 0.55);
        font-weight: 600 !important;
    }}
    [data-testid="stSidebar"] .stMarkdown {{
        color: var(--fg2, {COLOR_TEXT_PRIMARY});
    }}
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
        border-radius: 14px;
        padding: var(--space-5, 20px);
        margin-bottom: var(--space-4, 16px);
    }}
    /* Polish iteration: macOS-flavored radius bump. The base Visuals/
     * stylesheet declares --radius-lg: 12px; we override here for the
     * Streamlit shell so cards and panels read as more polished surfaces. */
    .panel, .empty-state, .quarantine, .world-card,
    .control-room-empty, [data-testid="stMetric"] {{
        border-radius: 14px !important;
    }}
    .panel.raised {{ border-radius: 14px !important; }}
    /* Plotly chart container — soften the corners */
    .stPlotlyChart, [data-testid="stPlotlyChart"] {{
        border-radius: 14px;
        overflow: hidden;
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
