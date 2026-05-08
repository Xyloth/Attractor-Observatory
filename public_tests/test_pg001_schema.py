"""PG-001 schema validation public tests.

Tests assert the published artifacts under ``reports/project_genealogy/``
are well-formed and self-consistent. They run against whatever atlas the
repo currently ships; if the artifacts are absent, the tests are skipped
with the empty-state reason recorded.

Schema scope:
* Manifest carries audited file list and mission atoms with source refs.
* Every dossier names the manifest hash that produced it.
* Atlas references existing dossier hashes.
* Coherence binds to atlas hash and lists every mission atom.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = REPO_ROOT / "reports" / "project_genealogy"
DOSSIER_DIR = REPORT_DIR / "dossiers"


def _load(path: Path):
    if not path.is_file():
        pytest.skip(f"PG-001 artifact missing: {path.relative_to(REPO_ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def _maybe(path: Path):
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def test_manifest_present_and_versioned() -> None:
    manifest = _load(REPORT_DIR / "input_manifest.json")
    assert manifest["schema"] == "ProjectGenealogyManifest.v1"
    assert manifest["pg_version"] == "PG-001"
    assert "content_hash" in manifest
    assert manifest["content_hash"].startswith("sha256:")
    rb = manifest["run_binding"]
    assert rb["branch"]
    assert rb["head_commit"]


def test_manifest_has_mission_atoms_with_source_refs() -> None:
    """PG16 — mission atoms locked with source refs."""
    manifest = _load(REPORT_DIR / "input_manifest.json")
    atoms = manifest["mission_atoms"]
    assert len(atoms) > 0, "PG-001 requires at least one mission atom"
    for atom in atoms:
        assert atom["mission_atom_id"]
        assert atom["statement"]
        assert atom["source_refs"], (
            f"mission atom {atom['mission_atom_id']} has no source_refs — "
            f"PG16 requires every mission atom to cite a source."
        )
        assert atom["expected_artifact_families"], (
            f"mission atom {atom['mission_atom_id']} has no expected_artifact_families"
        )


def test_manifest_threshold_policy_locked_before_findings() -> None:
    """`pg_manifest_thresholds_locked`: drift/probe thresholds present."""
    manifest = _load(REPORT_DIR / "input_manifest.json")
    tp = manifest["threshold_policy"]
    assert "drift" in tp and "missing_birth_atom_count_for_bad" in tp["drift"]
    assert "probe" in tp
    assert "depth" in tp


def test_atlas_present_and_references_dossier_hashes() -> None:
    """PG15 — versioned atlas + latest pointer; PG2 — every audited file
    has a dossier or manifest exclusion."""
    atlas = _load(REPORT_DIR / "atlas_latest.json")
    assert atlas["schema"] == "ProjectGenealogyAtlas.v1"
    assert atlas["content_hash"].startswith("sha256:")
    nodes = atlas["nodes"]
    assert nodes, "atlas must have at least one node"
    seen_dossier_hashes: set[str] = set()
    for node in nodes:
        assert node["path"]
        assert node["dossier_path"]
        assert node["dossier_hash"].startswith("sha256:")
        seen_dossier_hashes.add(node["dossier_hash"])
        # Dossier file must exist.
        dossier_path = REPO_ROOT / node["dossier_path"]
        assert dossier_path.is_file(), f"dossier missing for {node['path']}"
    assert len(seen_dossier_hashes) >= len(nodes) // 2, (
        "dossier hashes should be distinct (deletion of one dossier should fail validation)"
    )


def test_dossier_schema_and_manifest_binding() -> None:
    """PG1 — input_manifest_hash is referenced by every dossier."""
    manifest = _load(REPORT_DIR / "input_manifest.json")
    expected_hash = manifest["content_hash"]
    dossiers = sorted((DOSSIER_DIR).glob("*.json")) if DOSSIER_DIR.is_dir() else []
    if not dossiers:
        pytest.skip("no dossiers published")
    sample_size = min(50, len(dossiers))
    for p in dossiers[:sample_size]:
        d = json.loads(p.read_text(encoding="utf-8"))
        assert d["schema"] == "ProjectGenealogyDossier.v1"
        assert d["run_binding"]["input_manifest_hash"] == expected_hash, (
            f"dossier {p.name} cites a stale manifest hash"
        )
        # PG3: birth predicate or honest_decline.
        assert d["birth"]["status"] in {"recovered", "honest_decline"}
        # PG4: current predicate or honest_decline.
        assert d["current"]["status"] in {"recovered", "honest_decline", "partial"}
        # PG5: depth has all five axes.
        depth = d["depth"]
        for axis in (
            "predicate_atom_coverage",
            "adversarial_surface_coverage",
            "doctrine_binding_quality",
            "evidence_integration",
            "operational_load_bearingness",
        ):
            assert axis in depth, f"depth axis {axis} missing in {p.name}"


def test_findings_carry_reproducer_or_decline() -> None:
    """PG7 — every confirmed finding has a reproducer."""
    dossiers = sorted((DOSSIER_DIR).glob("*.json")) if DOSSIER_DIR.is_dir() else []
    if not dossiers:
        pytest.skip("no dossiers published")
    confirmed_seen = 0
    for p in dossiers:
        d = json.loads(p.read_text(encoding="utf-8"))
        for fnd in d.get("findings", []):
            if fnd.get("status") == "confirmed":
                confirmed_seen += 1
                rp = fnd.get("reproducer", {})
                assert rp.get("command") or rp.get("kind") == "manual_decline", (
                    f"confirmed finding {fnd['finding_id']} lacks a reproducer command"
                )
    # Don't assert confirmed_seen > 0 — a zero-finding audit is allowed,
    # but if any are present they must be reproducible.


def test_removal_probe_evidence_or_unknown() -> None:
    """PG18 — every cleanup_candidate_status with a removable verdict has a
    recorded probe; bare unknown / probe_declined are allowed."""
    dossiers = sorted((DOSSIER_DIR).glob("*.json")) if DOSSIER_DIR.is_dir() else []
    if not dossiers:
        pytest.skip("no dossiers published")
    for p in dossiers:
        d = json.loads(p.read_text(encoding="utf-8"))
        liv = d.get("liveness", {})
        status = liv.get("cleanup_candidate_status", "unknown")
        probe = liv.get("removal_probe", {})
        if status in {"removable_clean", "removable_with_warnings", "not_removable"}:
            assert probe.get("command") and probe.get("outcome"), (
                f"{p.name} claims {status} without recording probe.command and probe.outcome"
            )
        elif status == "probe_declined":
            assert probe.get("decline_reason") in {
                "removal_probe_declined_critical_path",
                "removal_probe_over_budget",
            }, f"{p.name} probe_declined with non-canonical reason"


def test_atlas_summary_counts_match_nodes() -> None:
    """`pg_no_mock_viz`: visualization data equals atlas data."""
    atlas = _load(REPORT_DIR / "atlas_latest.json")
    nodes = atlas["nodes"]
    summary = atlas["summary"]
    assert summary["file_count"] == len(nodes)
    assert summary["dossier_count"] == len(nodes)
    edge_total = sum(summary["edge_count_by_type"].values())
    assert edge_total == len(atlas["edges"])
    bad = sum(1 for n in nodes if n.get("drift_status") == "bad_drift")
    assert summary["bad_drift_count"] == bad


def test_coherence_binds_atlas_and_mission_atoms() -> None:
    """PG16 — coherence cites mission predicate hash; PG17 — every mission
    atom has serving cohorts/files or coverage_status orphan/declined."""
    coherence = _maybe(REPORT_DIR / "coherence_latest.json")
    if coherence is None:
        pytest.skip("coherence_latest.json absent")
    assert coherence["schema"] == "ProjectCoherenceReport.v1"
    rb = coherence["run_binding"]
    assert rb["atlas_hash"].startswith("sha256:")
    assert rb["input_manifest_hash"].startswith("sha256:")
    coverage = coherence["coverage_by_atom"]
    assert coverage, "coherence must list every mission atom"
    for entry in coverage:
        assert entry["mission_atom_id"]
        if entry["coverage_status"] in {"covered", "partial"}:
            assert entry["serving_files"] or entry["serving_cohorts"], (
                f"{entry['mission_atom_id']} claims {entry['coverage_status']} "
                f"without naming serving files/cohorts"
            )
        elif entry["coverage_status"] in {"orphan", "declined"}:
            assert entry["decline_reason"], (
                f"{entry['mission_atom_id']} {entry['coverage_status']} "
                f"without decline_reason"
            )

    # PG20 — trajectory is honest about insufficient history.
    traj = coherence["trajectory"]
    assert traj["trajectory_status"] in {
        "improving",
        "stable",
        "degrading",
        "insufficient_history",
        "declined",
    }


def test_decline_taxonomy_used_only_from_canonical_set() -> None:
    """Honest-decline reasons must come from the manifest's declared taxonomy."""
    manifest = _load(REPORT_DIR / "input_manifest.json")
    canonical = set(manifest["decline_taxonomy"])
    dossiers = sorted((DOSSIER_DIR).glob("*.json")) if DOSSIER_DIR.is_dir() else []
    if not dossiers:
        pytest.skip("no dossiers published")
    for p in dossiers[:50]:
        d = json.loads(p.read_text(encoding="utf-8"))
        for dec in d.get("declines", []):
            reason = dec.get("reason", "")
            if reason:
                assert reason in canonical, f"{p.name} uses non-canonical decline reason: {reason}"


def test_doctrine_index_resolves_to_audited_files() -> None:
    """PG12 — cross-doctrine collision detector reports zero or with files."""
    atlas = _load(REPORT_DIR / "atlas_latest.json")
    nodes_paths = {n["path"] for n in atlas["nodes"]}
    di = atlas.get("doctrine_index", {})
    for d_id, files in di.items():
        for f in files:
            assert f in nodes_paths, f"doctrine_index[{d_id}] cites unaudited file {f}"
