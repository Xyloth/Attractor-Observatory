"""Shared placeholder render helper — D22 binding.

Phase 0 rooms render via this helper exclusively. The helper writes the
room title bar (so layouts are consistent across rooms) and then routes
to ``render_empty_state`` for the body. This is the SOLE no-data
pathway permitted by D22.

Phase 1+ will modify each room module individually to consume its
adapter(s) and render real content; until then, the placeholder is the
honest answer.
"""

from __future__ import annotations

from typing import Iterable, Optional

from control_room.components.empty_state import render_empty_state
from control_room.design_tokens import (
    COLOR_TEXT_SECONDARY,
    FONT_FAMILY_DISPLAY,
    FONT_SIZE_HEADING_1,
    FONT_SIZE_HEADING_2,
    FONT_WEIGHT_DISPLAY,
)


def render_placeholder_room(
    *,
    room_name: str,
    room_icon: str,
    tagline: str,
    phase: str,
    planned_artifacts: Iterable[str],
    expected_phase_ticket: Optional[str] = None,
) -> None:
    """Render a Phase-0 placeholder room.

    Title bar + tagline + empty-state body.
    """
    import streamlit as st  # local import: keep adapter tests stdlib-only

    st.markdown(
        f"""
        <div style="margin-bottom: 1.4rem;">
          <div style="
            font-family: {FONT_FAMILY_DISPLAY};
            font-size: {FONT_SIZE_HEADING_1};
            font-weight: {FONT_WEIGHT_DISPLAY};
            letter-spacing: 0.01em;
          ">{room_icon}&nbsp;&nbsp;{room_name}</div>
          <div style="
            color: {COLOR_TEXT_SECONDARY};
            font-size: {FONT_SIZE_HEADING_2};
            margin-top: 0.2rem;
          ">{tagline}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    artifacts_summary = "; ".join(planned_artifacts) if planned_artifacts else "—"
    reason = (
        f"{room_name} is a Phase 0 placeholder. {phase} will populate this "
        f"room with: {artifacts_summary}."
    )
    expected = expected_phase_ticket or f"{phase} ticket (Architect to assign)"
    render_empty_state(reason=reason, expected_artifact=expected)
