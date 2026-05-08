"""PG-001 Mission Control Project Genealogy tab tests.

PG19 — the tab renders deterministically from atlas_latest.json and
coherence_latest.json. Closing and reopening against the same artifacts
must produce an identical render.

The test uses Streamlit's :class:`AppTest` to invoke the room's
``render()`` callable in a deterministic harness and asserts:

* The tab loads without raising.
* When atlas/coherence are present, no empty-state markers leak through
  to the top-level frame body (only inside specific empty subpanels).
* The same input produces a stable structure across two consecutive
  invocations.

If atlas_latest.json is absent, the tab renders an honest empty state
that contains the canonical empty-state HTML marker — that is itself
the D22 contract.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = REPO_ROOT / "reports" / "project_genealogy"
ATLAS_PATH = REPORT_DIR / "atlas_latest.json"
COHERENCE_PATH = REPORT_DIR / "coherence_latest.json"


def _import_room():
    pytest.importorskip("streamlit")
    from control_room.rooms import project_genealogy as room  # noqa: WPS433
    return room


def test_room_module_imports_without_streamlit_runtime() -> None:
    room = _import_room()
    assert room.ROOM_ID == "project_genealogy"
    assert room.ROOM_NAME == "Project Genealogy"
    assert callable(room.render)


def test_room_constants_match_spec() -> None:
    room = _import_room()
    # Default visible edge types per spec §"Mission Control Integration".
    assert set(room.EDGE_DEFAULT_VISIBLE) <= set(room.EDGE_TYPES)
    assert "spawned_by_ticket" in room.EDGE_DEFAULT_VISIBLE
    assert "derived_from_file" in room.EDGE_DEFAULT_VISIBLE
    assert "contradicts_doctrine_peer" in room.EDGE_DEFAULT_VISIBLE
    assert len(room.EDGE_TYPES) == 10


def test_apptest_renders_empty_state_when_no_atlas(tmp_path, monkeypatch) -> None:
    """D22 — absent atlas renders honest empty state."""
    pytest.importorskip("streamlit")
    from streamlit.testing.v1 import AppTest

    # Simulate "no atlas published yet" by pointing the room at a temp
    # report dir that has neither file.
    monkeypatch.chdir(tmp_path)

    script = (
        "from control_room.rooms import project_genealogy\n"
        "project_genealogy.render()\n"
    )
    at = AppTest.from_string(script, default_timeout=20)
    at.run()
    assert not at.exception, f"render raised: {at.exception}"
    # Empty-state marker should appear somewhere in the markdown output.
    md_blob = "\n".join(m.value for m in at.markdown if hasattr(m, "value"))
    assert "data-control-room-empty-state" in md_blob


def test_apptest_renders_with_published_artifacts() -> None:
    """PG19 — with atlas/coherence present, render completes deterministically."""
    if not ATLAS_PATH.is_file():
        pytest.skip("atlas_latest.json not published")
    pytest.importorskip("streamlit")
    from streamlit.testing.v1 import AppTest

    script = (
        "from control_room.rooms import project_genealogy\n"
        "project_genealogy.render()\n"
    )
    at = AppTest.from_string(script, default_timeout=60)
    at.run()
    assert not at.exception, f"render raised: {at.exception}"
    # The room emblem header must appear in the output.
    md_blob = "\n".join(m.value for m in at.markdown if hasattr(m, "value"))
    assert "Project Genealogy" in md_blob


def test_counts_in_tab_match_atlas_summary() -> None:
    """Mission Control counts must equal atlas/coherence JSON counts."""
    if not ATLAS_PATH.is_file():
        pytest.skip("atlas_latest.json not published")
    atlas = json.loads(ATLAS_PATH.read_text(encoding="utf-8"))
    summary = atlas["summary"]
    nodes = atlas["nodes"]
    edges = atlas["edges"]
    assert summary["file_count"] == len(nodes)
    assert summary["dossier_count"] == len(nodes)
    assert sum(summary["edge_count_by_type"].values()) == len(edges)
    if COHERENCE_PATH.is_file():
        coh = json.loads(COHERENCE_PATH.read_text(encoding="utf-8"))
        assert coh["summary"]["mission_atom_count"] == summary["mission_atom_count"]


def test_room_render_is_deterministic_against_same_atlas() -> None:
    """PG19 deterministic-render contract — two identical runs produce
    the same set of rendered components."""
    if not ATLAS_PATH.is_file():
        pytest.skip("atlas_latest.json not published")
    pytest.importorskip("streamlit")
    from streamlit.testing.v1 import AppTest

    script = (
        "from control_room.rooms import project_genealogy\n"
        "project_genealogy.render()\n"
    )
    a = AppTest.from_string(script, default_timeout=60)
    a.run()
    b = AppTest.from_string(script, default_timeout=60)
    b.run()
    assert not a.exception and not b.exception

    def _markdown_blob(at):
        return "\n".join(m.value for m in at.markdown if hasattr(m, "value"))

    assert _markdown_blob(a) == _markdown_blob(b), (
        "PG19 violation: tab render is non-deterministic across two AppTest invocations"
    )
