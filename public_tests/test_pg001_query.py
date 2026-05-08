"""PG-001 query API public tests.

Exercises the documented Python API and the CLI examples from the spec's
§"Query API Surface". Tests assume the published atlas exists; if not,
they skip with a reason (PG-001 may not have run on this branch).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
ATLAS_PATH = REPO_ROOT / "reports" / "project_genealogy" / "atlas_latest.json"


def _require_atlas() -> Path:
    if not ATLAS_PATH.is_file():
        pytest.skip(f"atlas_latest.json absent at {ATLAS_PATH}")
    return ATLAS_PATH


def test_query_index_loads() -> None:
    _require_atlas()
    from project_genealogy.query import GenealogyIndex
    idx = GenealogyIndex.load(ATLAS_PATH)
    assert idx.atlas["schema"] == "ProjectGenealogyAtlas.v1"


def test_query_files_filter_returns_required_columns() -> None:
    _require_atlas()
    from project_genealogy.query import GenealogyIndex
    idx = GenealogyIndex.load(ATLAS_PATH)
    rows = idx.files(artifact_family="doctrine")
    assert isinstance(rows, list)
    for r in rows:
        assert "path" in r and "dossier_path" in r and "dossier_hash" in r


def test_query_files_path_glob() -> None:
    _require_atlas()
    from project_genealogy.query import GenealogyIndex
    idx = GenealogyIndex.load(ATLAS_PATH)
    rows = idx.files(path_glob="docs/*.md")
    for r in rows:
        assert r["path"].startswith("docs/")
        assert r["path"].endswith(".md")


def test_query_orphans_kinds_distinct() -> None:
    _require_atlas()
    from project_genealogy.query import GenealogyIndex
    idx = GenealogyIndex.load(ATLAS_PATH)
    no_birth = idx.orphans(kind="no_birth_predicate")
    no_runtime = idx.orphans(kind="no_runtime_refs")
    no_parent = idx.orphans(kind="no_parent")
    assert isinstance(no_birth, list)
    assert isinstance(no_runtime, list)
    assert isinstance(no_parent, list)


def test_query_findings_reproducer_filter() -> None:
    _require_atlas()
    from project_genealogy.query import GenealogyIndex
    idx = GenealogyIndex.load(ATLAS_PATH)
    rows = idx.findings(reproducible=True)
    for r in rows:
        assert r["reproducer"].get("command")


def test_query_doctrine_collisions_returns_canonical_shape() -> None:
    _require_atlas()
    from project_genealogy.query import GenealogyIndex
    idx = GenealogyIndex.load(ATLAS_PATH)
    rows = idx.doctrine_collisions()
    for r in rows:
        assert r["edge_type"] in {"contradicts_doctrine_peer", "implements_same_doctrine"}
        assert "path" in r and "dossier_path" in r and "dossier_hash" in r


def test_query_depth_outliers_shape() -> None:
    _require_atlas()
    from project_genealogy.query import GenealogyIndex
    idx = GenealogyIndex.load(ATLAS_PATH)
    rows = idx.depth_outliers(axis="predicate_atom_coverage", bottom_n=5)
    assert len(rows) <= 5
    for r in rows:
        assert "axis" in r and "value" in r


def test_cli_files_runs_against_atlas() -> None:
    _require_atlas()
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "project_genealogy.query",
            "--atlas",
            str(ATLAS_PATH),
            "files",
            "--artifact-family",
            "doctrine",
        ],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
    rows = json.loads(proc.stdout)
    assert isinstance(rows, list)


def test_cli_orphans_runs() -> None:
    _require_atlas()
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "project_genealogy.query",
            "--atlas",
            str(ATLAS_PATH),
            "orphans",
            "--kind",
            "no_birth_predicate",
        ],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
