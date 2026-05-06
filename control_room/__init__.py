"""Observatory Control Room — sidecar visualization layer.

Read-heavy, branch-isolated, non-claim-bearing. The Control Room MAY
visualize almost everything; it MUST mutate almost nothing. The only
writable path is ``control_room/cache/``; this is enforced mechanically
by the read-only test (see ``tests/test_control_room_readonly.py``).

Phase 0 (TASK-CB-004) ships:

* Streamlit + Plotly app shell with sidebar navigation across all 10 rooms.
* Design tokens centralized in ``design_tokens.py``.
* Empty-state component as the single source of truth for "no data"
  rendering (D22 binding).
* Adapter layer for project artifacts (BUILD_LOG, builder telemetry,
  doctrine, campaign reports, methods/falsifiers, negative-space, git,
  pytest).
* Read-only enforcement test (mechanism, not policy).

Phases 1-4 fill the rooms with real visualizations; this module's
contract is that any new room MUST consume an adapter and MUST route
non-``ok`` adapter status through ``components.empty_state.render_empty_state``.
"""

from __future__ import annotations

__version__ = "0.1.0"
__phase__ = "phase_0_foundation"
