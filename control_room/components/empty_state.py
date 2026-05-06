"""Empty-state component — the single source of truth for "no data" rendering.

D22 binding: every Control Room room that would otherwise show absent,
malformed, or exploratory data MUST route through this component. There
is no other pathway. The visual language declares the absence rather
than papering over it (Class 12 — Decorative Completeness — is on watch).

Two render paths:

* ``render_empty_state(reason, expected_artifact)`` — Streamlit-bound,
  used by rooms inside ``app.py``.
* ``render_empty_state_html(reason, expected_artifact)`` — pure-string
  variant, used by tests and any non-Streamlit consumer (e.g., screenshot
  rigs, README embeds).

Both paths emit the same HTML structure and carry the
``EMPTY_STATE_HTML_MARKER`` so the read-only / no-mock-data tests can
assert that any "no data" surface in the rendered app went through
this component.
"""

from __future__ import annotations

from typing import Optional

from control_room.design_tokens import (
    COLOR_TEXT_MUTED,
    COLOR_TEXT_SECONDARY,
    COLOR_UNAVAILABLE,
)


# Tests assert this marker appears in any rendered no-data surface.
EMPTY_STATE_HTML_MARKER: str = "data-control-room-empty-state"


def render_empty_state_html(
    reason: str,
    expected_artifact: Optional[str] = None,
    label: str = "no data",
) -> str:
    """Return HTML markup for an honest empty state.

    The structure carries the ``EMPTY_STATE_HTML_MARKER`` attribute so
    automated checks can verify the empty-state pathway is being used.
    Rooms calling this helper from inside Streamlit pass the result to
    ``st.markdown(html, unsafe_allow_html=True)`` (or use
    ``render_empty_state`` instead, which does that for them).
    """
    expected = ""
    if expected_artifact:
        expected = (
            f'<div class="control-room-empty-expected">'
            f"expected artifact: <code>{_escape(expected_artifact)}</code>"
            f"</div>"
        )
    return (
        f'<div class="control-room-empty" {EMPTY_STATE_HTML_MARKER}="true">'
        f'<div class="control-room-empty-label">{_escape(label)}</div>'
        f'<div class="control-room-empty-reason">{_escape(reason)}</div>'
        f"{expected}"
        f"</div>"
    )


def render_empty_state(
    reason: str,
    expected_artifact: Optional[str] = None,
    label: str = "no data",
) -> None:
    """Streamlit-bound empty-state render.

    Imports streamlit lazily so non-Streamlit consumers (tests, parsers)
    can import this module without a streamlit dependency.
    """
    import streamlit as st  # local import: keep adapter tests stdlib-only

    st.markdown(
        render_empty_state_html(
            reason=reason,
            expected_artifact=expected_artifact,
            label=label,
        ),
        unsafe_allow_html=True,
    )


def _escape(value: str) -> str:
    """Minimal HTML escape — control-room consumes its own markup, so we
    avoid a heavy dependency for what is a small set of inputs."""
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )
