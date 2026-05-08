"""Control Room rooms — sidebar navigation surfaces (proposal §7).

Phase 0 ships 10 placeholder rooms. Each room module exports:

* ``ROOM_ID``   — short slug, used as anchor and dict key
* ``ROOM_NAME`` — human-readable nav label
* ``ROOM_ICON`` — single-glyph emoji used in the sidebar
* ``ROOM_TAGLINE`` — one-line subtitle shown at the top of the room
* ``ROOM_PHASE`` — the Phase that ships the real content
* ``render()``  — Streamlit-bound entry point. Phase 0 rooms call
  ``components.empty_state.render_empty_state`` exclusively. Phase 1+
  may consume adapters and render real visualizations, but ``render()``
  must still route any non-``ok`` adapter status through the
  empty-state component (D22 binding).
"""

from __future__ import annotations

from control_room.rooms import (
    ai_operations_tower,
    basin_floor_lab,
    campaign_command,
    doctrine_console,
    factory_intake_dock,
    falsifier_ledger,
    motif_atlas,
    portfolio_demo,
    project_genealogy,
    project_graph,
    pulse_deck,
    world_observatory,
)


ROOMS = (
    pulse_deck,
    world_observatory,
    campaign_command,
    ai_operations_tower,
    motif_atlas,
    basin_floor_lab,
    falsifier_ledger,
    doctrine_console,
    factory_intake_dock,
    project_graph,    # 11th room — Phase 2 (Project Graph)
    project_genealogy, # 12th room — PG-001 (Project Genealogy)
    portfolio_demo,
)


def room_registry() -> list[dict[str, str]]:
    """Return the room nav metadata, in sidebar order."""
    return [
        {
            "id": room.ROOM_ID,
            "name": room.ROOM_NAME,
            "icon": room.ROOM_ICON,
            "tagline": room.ROOM_TAGLINE,
            "phase": room.ROOM_PHASE,
            "module": room.__name__,
        }
        for room in ROOMS
    ]


def render_room(room_id: str) -> None:
    """Look up a room by id and call its ``render()``."""
    for room in ROOMS:
        if room.ROOM_ID == room_id:
            room.render()
            return
    raise KeyError(f"unknown room: {room_id}")


__all__ = [
    "ROOMS",
    "room_registry",
    "render_room",
]
