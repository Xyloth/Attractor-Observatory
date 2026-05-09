import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _registry() -> dict:
    return json.loads(_read("docs/mistake_catalog_registry.json"))


def test_mistake_catalog_registry_is_canonical_and_ratified():
    registry = _registry()
    classes = registry["classes"]
    by_id = {entry["id"]: entry for entry in classes}

    assert registry["schema"] == "MistakeCatalogRegistry.v1"
    assert len(classes) == 13
    assert set(by_id) == {f"Class {i}" for i in range(1, 14)}
    assert all(entry["status"] == "ratified" for entry in classes)
    assert by_id["Class 12"]["title"] == "Decorative Completeness"
    assert by_id["Class 13"]["title"] == "Predicate-detector surface coupling"


def test_narrative_surfaces_agree_with_registry():
    registry = _registry()
    classes = registry["classes"]
    claude = _read("CLAUDE_BUILDER_INITIATION.md")
    readme = _read("README.md")
    d22 = _read("docs/doctrine_d22.md")

    for entry in classes:
        assert f"### {entry['id']}" in claude
        assert entry["title"].split(" / ")[0] in claude

    assert "thirteen ratified classes" in readme
    assert "docs/mistake_catalog_registry.json" in readme
    assert "Class 12 - Decorative Completeness (ratified)" in d22
    assert "Class 12 candidate" not in d22


def test_control_room_reads_mistake_catalog_registry():
    ai_ops = _read("control_room/rooms/ai_operations_tower.py")
    doctrine_console = _read("control_room/rooms/doctrine_console.py")
    snapshot = _read("control_room/snapshot.py")

    for source in (ai_ops, doctrine_console, snapshot):
        assert "parse_mistake_catalog" in source
        assert "MISTAKE_CATALOG" not in source

    assert "D7-D31" in ai_ops
    assert "D7-D31" in doctrine_console
