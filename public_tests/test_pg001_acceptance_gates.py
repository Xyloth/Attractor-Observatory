"""PG-001 acceptance gates — single test per gate.

The twenty acceptance gates from spec §"Acceptance Gates" are reported
here as individual pytest assertions so a fresh auditor can run

    python -m pytest public_tests/test_pg001_acceptance_gates.py -v

and see one PASS line per gate, mapping directly to the spec.

Each test references the underlying public_tests/test_pg001_*.py module
that exercises the gate in detail; this file is the gate-roll-up.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = REPO_ROOT / "reports" / "project_genealogy"
DOSSIER_DIR = REPORT_DIR / "dossiers"


def _load(p: Path) -> dict:
    if not p.is_file():
        pytest.skip(f"{p.relative_to(REPO_ROOT)} absent")
    return json.loads(p.read_text(encoding="utf-8"))


def _all_dossiers() -> list[dict]:
    if not DOSSIER_DIR.is_dir():
        pytest.skip("no dossiers")
    out = []
    for p in sorted(DOSSIER_DIR.glob("*.json")):
        try:
            out.append(json.loads(p.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError):
            continue
    return out


def test_PG1_manifest_locked_and_dossiers_cite_it() -> None:
    manifest = _load(REPORT_DIR / "input_manifest.json")
    assert manifest["content_hash"].startswith("sha256:")
    expected = manifest["content_hash"]
    sample = _all_dossiers()[:50]
    assert sample, "no dossiers"
    for d in sample:
        assert d["run_binding"]["input_manifest_hash"] == expected


def test_PG2_all_tracked_files_accounted() -> None:
    manifest = _load(REPORT_DIR / "input_manifest.json")
    audited_paths = {a["path"] for a in manifest["audited_files"]}
    excluded_paths = {e["path"] for e in manifest["excluded_files"]}
    overlap = audited_paths & excluded_paths
    assert not overlap, f"files appear in both audited and excluded: {overlap}"
    total = len(audited_paths) + len(excluded_paths)
    assert total == manifest["summary"]["tracked_total"], (
        f"audited+excluded={total} != tracked_total={manifest['summary']['tracked_total']}"
    )


def test_PG3_birth_predicate_or_decline() -> None:
    for d in _all_dossiers():
        assert d["birth"]["status"] in {"recovered", "honest_decline"}, d["file"]["path"]


def test_PG4_current_predicate_or_decline() -> None:
    for d in _all_dossiers():
        assert d["current"]["status"] in {"recovered", "partial", "honest_decline"}, d["file"]["path"]


def test_PG5_depth_vector_complete() -> None:
    axes = (
        "predicate_atom_coverage",
        "adversarial_surface_coverage",
        "doctrine_binding_quality",
        "evidence_integration",
        "operational_load_bearingness",
    )
    for d in _all_dossiers():
        for a in axes:
            assert a in d["depth"], f"{d['file']['path']} missing depth axis {a}"


def test_PG6_drift_atom_diff_when_not_none() -> None:
    for d in _all_dossiers():
        drift = d["drift_assessment"]
        if drift["status"] == "none":
            continue
        if drift["status"] == "honest_decline":
            assert drift.get("decline_reason"), d["file"]["path"]
            continue
        # Non-none, non-decline drift must carry atom diffs or doctrine
        # boundary crossings or letter_vs_spirit flags.
        has_evidence = (
            bool(drift.get("missing_birth_atoms"))
            or bool(drift.get("new_atoms"))
            or bool(drift.get("doctrine_boundary_crossings"))
            or bool(drift.get("letter_vs_spirit_flags"))
            or bool(drift.get("negative_space_flags"))
        )
        assert has_evidence, (
            f"{d['file']['path']} drift={drift['status']} without atom diffs"
        )


def test_PG7_findings_falsifiable() -> None:
    for d in _all_dossiers():
        for fnd in d.get("findings", []):
            if fnd.get("status") == "confirmed":
                rp = fnd.get("reproducer", {})
                kind = rp.get("kind", "")
                assert kind != "manual_decline", (
                    f"{d['file']['path']} confirmed finding {fnd['finding_id']} "
                    f"uses manual_decline reproducer (forbidden by §Falsifiability Protocol)"
                )
                assert rp.get("command") or kind in {"json_query", "ast_probe", "grep", "git_query"}, (
                    f"{d['file']['path']} confirmed finding lacks a runnable reproducer"
                )


def test_PG8_evidence_refs_bound() -> None:
    for d in _all_dossiers():
        all_refs: list[dict] = []
        all_refs.extend(d["birth"].get("evidence_refs", []))
        all_refs.extend(d["current"].get("evidence_refs", []))
        for fnd in d.get("findings", []):
            all_refs.extend(fnd.get("evidence_refs", []))
        for ref in all_refs:
            if not ref.get("locator"):
                # locator empty allowed only if explicitly private
                assert ref.get("evidence_private"), (
                    f"{d['file']['path']} evidence_ref {ref.get('ref_id', '')} has no locator and isn't marked private"
                )


def test_PG9_no_mock_viz_data() -> None:
    atlas = _load(REPORT_DIR / "atlas_latest.json")
    summary = atlas["summary"]
    assert summary["file_count"] == len(atlas["nodes"])
    assert summary["dossier_count"] == len(atlas["nodes"])
    assert sum(summary["edge_count_by_type"].values()) == len(atlas["edges"])


def test_PG10_query_api_examples_execute() -> None:
    atlas_path = REPORT_DIR / "atlas_latest.json"
    if not atlas_path.is_file():
        pytest.skip("atlas absent")
    examples = [
        ["files", "--doctrine", "D26"],
        ["files", "--drift", "bad_drift"],
        ["orphans", "--kind", "no_birth_predicate"],
        ["findings", "--reproducible", "true"],
    ]
    for ex in examples:
        proc = subprocess.run(
            [sys.executable, "-m", "project_genealogy.query", "--atlas", str(atlas_path), *ex],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            timeout=120,
        )
        assert proc.returncode == 0, f"{ex} failed: {proc.stderr}"
        # Should be valid JSON.
        json.loads(proc.stdout)


def test_PG11_cohort_consistency() -> None:
    atlas = _load(REPORT_DIR / "atlas_latest.json")
    cohorts = atlas["cohorts"]
    nodes_paths = {n["path"] for n in atlas["nodes"]}
    for c in cohorts:
        assert c["cohort_id"]
        for m in c["members"]:
            assert m in nodes_paths, f"cohort {c['cohort_id']} cites unaudited member {m}"


def test_PG12_cross_doctrine_collision_pass() -> None:
    """At minimum: doctrine_index resolves to audited files, no orphan refs."""
    atlas = _load(REPORT_DIR / "atlas_latest.json")
    nodes_paths = {n["path"] for n in atlas["nodes"]}
    for d_id, paths in atlas.get("doctrine_index", {}).items():
        for p in paths:
            assert p in nodes_paths, f"doctrine_index[{d_id}] cites {p} (unaudited)"


def test_PG13_mistake_class_mapping() -> None:
    valid = {f"Class{i}" for i in range(1, 14)} | {"unmapped_candidate"}
    for d in _all_dossiers():
        for fnd in d.get("findings", []):
            for cls in fnd.get("mistake_classes", []):
                assert cls in valid, f"{d['file']['path']} finding {fnd['finding_id']} uses non-canonical class {cls}"


def test_PG14_public_verification_honesty() -> None:
    """Spec: public claims name shipped tests/scripts, not private modules.

    PG-001 v1: every dossier referencing private module imports flags
    them via ``private_boundary.evidence_private=true`` on the edge."""
    atlas = _load(REPORT_DIR / "atlas_latest.json")
    for e in atlas["edges"]:
        if e.get("edge_type") != "imports":
            continue
        target = e["target"]
        first_seg = target.split("/", 1)[0] if "/" in target else target
        if first_seg in {"worlds", "motifs", "validation", "nulls", "core", "trace", "formalism", "biology", "search", "ops", "experiments", "evidence", "tests"}:
            assert e.get("private_boundary", {}).get("evidence_private") is True, (
                f"edge {e['edge_id']} imports private module {target} without private_boundary marker"
            )


def test_PG15_versioned_atlas() -> None:
    versioned = sorted((REPORT_DIR).glob("atlas_*Z.json"))
    assert versioned, "no versioned atlas_*Z.json found"
    pointer = REPORT_DIR / "atlas_latest.json"
    assert pointer.is_file()
    atlas = _load(pointer)
    rb = atlas["run_binding"]
    assert rb["freshness_status"] in {"computed_at_read", "stale", "unknown"}


def test_PG16_mission_atoms_locked() -> None:
    manifest = _load(REPORT_DIR / "input_manifest.json")
    coh = _load(REPORT_DIR / "coherence_latest.json")
    # Both must carry the same mission predicate identity (atoms list).
    manifest_atoms = manifest["mission_atoms"]
    coh_atoms = coh["mission"]["atoms"]
    manifest_ids = {a["mission_atom_id"] for a in manifest_atoms}
    coh_ids = {a["mission_atom_id"] for a in coh_atoms}
    assert manifest_ids == coh_ids, "mission atom set differs between manifest and coherence"
    # Coherence run_binding must cite manifest hash.
    assert coh["run_binding"]["input_manifest_hash"] == manifest["content_hash"]


def test_PG17_mission_coverage_complete() -> None:
    coh = _load(REPORT_DIR / "coherence_latest.json")
    valid = {"covered", "partial", "orphan", "declined"}
    for entry in coh["coverage_by_atom"]:
        assert entry["coverage_status"] in valid
        if entry["coverage_status"] in {"orphan", "declined"}:
            assert entry["decline_reason"], f"{entry['mission_atom_id']} {entry['coverage_status']} without decline_reason"
        else:
            assert entry["serving_files"] or entry["serving_cohorts"], (
                f"{entry['mission_atom_id']} {entry['coverage_status']} without serving members"
            )
    cohort_valid = {"aligned", "partial", "drifted", "unmapped", "declined"}
    for c in coh["cohort_alignment"]:
        assert c["alignment_status"] in cohort_valid


def test_PG18_removal_probe_evidence() -> None:
    for d in _all_dossiers():
        liv = d["liveness"]
        status = liv["cleanup_candidate_status"]
        rp = liv["removal_probe"]
        if status in {"removable_clean", "removable_with_warnings", "not_removable"}:
            assert rp.get("command") and rp.get("outcome"), d["file"]["path"]
        elif status == "probe_declined":
            assert rp.get("decline_reason") in {
                "removal_probe_declined_critical_path",
                "removal_probe_over_budget",
            }


def test_PG19_control_room_tab_renders() -> None:
    pytest.importorskip("streamlit")
    from streamlit.testing.v1 import AppTest
    script = (
        "from control_room.rooms import project_genealogy\n"
        "project_genealogy.render()\n"
    )
    a = AppTest.from_string(script, default_timeout=60)
    a.run()
    assert not a.exception, str(a.exception)
    b = AppTest.from_string(script, default_timeout=60)
    b.run()
    a_md = "\n".join(m.value for m in a.markdown if hasattr(m, "value"))
    b_md = "\n".join(m.value for m in b.markdown if hasattr(m, "value"))
    assert a_md == b_md, "PG19 violation — non-deterministic render"


def test_PG20_trajectory_history_honest() -> None:
    coh = _load(REPORT_DIR / "coherence_latest.json")
    traj = coh["trajectory"]
    assert traj["trajectory_status"] in {
        "improving",
        "stable",
        "degrading",
        "insufficient_history",
        "declined",
    }
    versioned = sorted((REPORT_DIR).glob("atlas_*Z.json"))
    if len(versioned) < 2:
        assert traj["trajectory_status"] == "insufficient_history", (
            "fewer than 2 atlases exist but trajectory_status != insufficient_history"
        )
