"""Reusable Control Room UI components.

D22 binding: ``empty_state.render_empty_state`` is the SOLE pathway by
which any room is permitted to render "no data". Rooms must not invent
their own placeholder, mock, or fallback rendering.
"""

from __future__ import annotations

from control_room.components.empty_state import (
    EMPTY_STATE_HTML_MARKER,
    render_empty_state,
    render_empty_state_html,
)
from control_room.components.chrome import (
    STATUS_TO_PILL_CLASS,
    WORLD_ICON_FILE,
    agent_chip,
    doctrine_tablet,
    event_row,
    gate_grid,
    metric_card,
    needs_attention,
    panel,
    pill_class,
    render_html,
    room_emblem,
    status_pill,
    world_card,
    world_icon_svg,
)

__all__ = [
    "EMPTY_STATE_HTML_MARKER",
    "render_empty_state",
    "render_empty_state_html",
    "STATUS_TO_PILL_CLASS",
    "WORLD_ICON_FILE",
    "agent_chip",
    "doctrine_tablet",
    "event_row",
    "gate_grid",
    "metric_card",
    "needs_attention",
    "panel",
    "pill_class",
    "render_html",
    "room_emblem",
    "status_pill",
    "world_card",
    "world_icon_svg",
]
