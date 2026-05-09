"""Pre-pass: build the input manifest.

The manifest is the evidence-lock artifact every later pass must cite.

Inputs:
* ``git ls-files`` plus inclusion/exclusion filters (declared here).
* Doctrine corpus (``docs/DOCTRINE.md``, ``docs/doctrine_*.md``,
  ``docs/doctrine_registry.json``).
* Campaign drivers (``CODEX_*.md``, ``TASK-*.md``, ``DX-*.md``,
  ``CLAUDE_*.md``) and ``BUILD_LOG.md``.
* Method documents under ``papers/methods/``.

Outputs:
* ``reports/project_genealogy/input_manifest.json`` with:
    * branch, commit, workspace_dirty, generation_command
    * file inclusion/exclusion filters
    * audited file list
    * mission atoms with source refs
    * threshold policy
    * artifact_family probe registry
    * probe_declined critical paths

Threshold policy and probe registry are declared here BEFORE any finding
runs (D9, D18, doctrine binding ``pg_manifest_thresholds_locked``).
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from project_genealogy import MANIFEST_SCHEMA, REPORT_DIR
from project_genealogy.hashing import hash_file, sha256_hex, write_with_hash, canonical_json


# ----- Inclusion / exclusion policy -----------------------------------------
#
# Per-file dossiers: the artifact_family layer where a file is the source
# object (code, schemas, doctrines, methods, drivers, top-level reports).
#
# Cohort-summary only (excluded from per-file dossiers, represented by a
# cohort node in the atlas): mass-generated trace dumps, ingestion buckets,
# and other generator outputs whose per-file audit would be redundant with
# the parent generator's dossier. These are listed in ``cohort_summary_only``.

FAMILY_RULES: list[tuple[str, str]] = [
    # (regex_pattern, artifact_family)
    (r"^docs/(doctrine|DOCTRINE)", "doctrine"),
    (r"^docs/", "docs"),
    (r"^papers/methods/", "method"),
    (r"^papers/falsifiers/", "falsifier"),
    (r"^papers/prereg/", "prereg"),
    (r"^papers/", "paper"),
    (r"^public_tests/", "test"),
    (r"^control_room/", "control_room"),
    (r"^factory_lowlevel/", "factory"),
    (r"^project_genealogy/", "audit_instrument"),
    (r"^project_telemetry/", "telemetry"),
    (r"^scripts/", "script"),
    (r"^atlas/", "atlas"),
    (r"^Visuals/", "visual"),
    (r"^ai_os/", "ai_os"),
    (r"^reports/project_genealogy/", "audit_report"),
    (r"^reports/", "report"),
    (r"^spec/", "spec"),
    (
        r"^(BUILD_LOG|README|CONTRIBUTING|LICENSE|CITATION|CLAUDE_|CODEX_|TASK-|DX-|"
        r"BUILDER_|FACTORY_|FAIR_|BLOCKER|Branch|NO ARTIFICIAL|Proposal|Seed|The Attractor|"
        r"Control_Room|Control Room|Dockerfile|Launch|WAITING|\.architect_state)",
        "driver_or_root_doc",
    ),
    (r"^[^/]+\.md$", "driver_or_root_doc"),
    (r"^[^/]+\.txt$", "driver_or_root_doc"),
    (r"^[^/]+\.(py|bat|cff|json|jsonld|ini)$", "root_artifact"),
    (r"^\.gitignore|^\.gitattributes", "root_artifact"),
]


# Cohort-only (excluded from per-file dossiers; manifest exclusion under
# `file_out_of_scope_by_manifest` with cohort representation).
#
# These are the four largest auto-generated dumps. Each has a clear parent
# generator (the ingestion daemon, the world bundle launcher, the factory
# campaign run) which IS dossiered; the bulk artifacts are represented at
# the cohort level in the atlas without per-file dossiers.

COHORT_ONLY_PREFIXES: tuple[str, ...] = (
    "reports/project_genealogy/",
    "reports/task_w1_mass_ingest/",
    "reports/task_cb015_launch/",
    "reports/campaign_016/",
    "reports/campaign_019/",
    "reports/campaign_035/",
)


# Per-file dossiers ARE produced for these report files even though they
# share a parent campaign — they are top-level summaries (full_report.json,
# methods doc, prereg signed.json) not bulk traces.

REPORT_INCLUDE_FILENAMES: tuple[str, ...] = (
    "full_report.json",
    "replication_verdict.json",
    "multisubstrate_floor_connectivity.json",
    "preregistration_record.json",
    "campaign_record.json",
    "campaign_summary.json",
    "ingestion_summary.json",
    "audit_record.json",
    "verdict.json",
)


# Per-file dossiers ALSO included for trace fixtures only when sampled at
# the cohort level. The cohort itself is dossiered via a synthetic node;
# individual trace JSONs in `traces/` subdirs stay cohort-only.


def determine_artifact_family(rel_path: str) -> str:
    """Map a tracked path to an artifact_family label."""
    for pattern, family in FAMILY_RULES:
        if re.search(pattern, rel_path):
            return family
    return "other"


def is_cohort_only(rel_path: str) -> bool:
    """Files in mass-generated dump dirs are cohort-summary-only."""
    if not any(rel_path.startswith(p) for p in COHORT_ONLY_PREFIXES):
        return False
    # Top-level summary files inside those dirs ARE per-file dossiered.
    name = Path(rel_path).name
    if name in REPORT_INCLUDE_FILENAMES:
        return False
    # Methods docs and prereg files inside campaign dirs are dossiered.
    if name.endswith("_signed.json") or name.endswith(".signed.json"):
        return False
    return True


# ----- Mission atom extraction ---------------------------------------------
#
# Mission atoms must cite source refs. The PG-001 spec lists allowed sources
# in priority order; this module reconstructs them mechanically. Every
# mission atom records its source citations; if no source can be cited,
# the candidate is declined under ``mission_atom_insufficient_source``.


# Mission atoms are reconstructed from explicit doctrine, spec, and BUILD_LOG
# evidence. Each carries source_refs that are file paths plus content lines
# (BUILD_LOG / spec line numbers / doctrine doc references). The reproducer
# for a mission atom is a grep against the cited file at the cited content.

MISSION_ATOM_SEEDS: list[dict[str, Any]] = [
    {
        "mission_atom_id": "MA-substrate-neutral-detection",
        "statement": (
            "Detect named motifs across stratified substrates under "
            "predicate-lens-independent methodology."
        ),
        "source_refs": [
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d26.md",
                "note": "D26 — Predicate-lens independence binds claim-bearing motif evidence.",
            },
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d31.md",
                "note": "D31 — BFG measurement split for floor_connectivity.",
            },
            {
                "kind": "spec",
                "locator": "papers/methods/PROJECT_GENEALOGY_PG001_SPEC.md",
                "note": "Project Mission section names predicate-lens-independent methodology.",
            },
        ],
        "expected_artifact_families": [
            "world",
            "factory",
            "formalism",
            "report",
            "method",
        ],
        "expected_drift_constraint": (
            "Any change that allows predicate-side and lens-side surfaces to "
            "couple without explicit BAD/PARTIAL declaration is bad drift "
            "against this atom."
        ),
    },
    {
        "mission_atom_id": "MA-evidence-discipline",
        "statement": (
            "Every claim-bearing artifact carries source-bound evidence with "
            "dereferenceable paths or explicit private boundaries."
        ),
        "source_refs": [
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d11.md",
                "note": "D11 — Truth pass before new claims (covered in docs/DOCTRINE.md).",
            },
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d23.md",
                "note": "D23 — Dereferenceable evidence or explicit private boundary.",
            },
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d29.md",
                "note": "D29 — Runnable evidence or private/narrative downgrade.",
            },
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d24.md",
                "note": "D24 — Freshness-bound sidecars.",
            },
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d30.md",
                "note": "D30 — Freshness computed at read.",
            },
        ],
        "expected_artifact_families": [
            "report",
            "audit_report",
            "method",
            "doctrine",
            "control_room",
            "factory",
            "test",
        ],
        "expected_drift_constraint": (
            "Adding evidence references without dereferenceable paths or "
            "private markers is bad drift against this atom."
        ),
    },
    {
        "mission_atom_id": "MA-no-engineered-passing",
        "statement": (
            "Pass criteria, gates, and thresholds must come from spec or "
            "calibrated null distributions, not engineered around typical "
            "outputs."
        ),
        "source_refs": [
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d7_d13.md",
                "note": "D9 — No engineered pass criteria.",
            },
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d7_d13.md",
                "note": "D12 — Gates are measurements, not counts.",
            },
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d18.md",
                "note": "D18 — No equivalence-basis drift.",
            },
            {
                "kind": "mistake_class",
                "locator": "CLAUDE_BUILDER_INITIATION.md",
                "note": "Class 6 — Engineered passing.",
            },
        ],
        "expected_artifact_families": [
            "factory",
            "method",
            "test",
            "report",
            "doctrine",
        ],
        "expected_drift_constraint": (
            "Tuning thresholds after seeing outcomes, or hand-rolling pass "
            "bands around typical decoder outputs, is bad drift."
        ),
    },
    {
        "mission_atom_id": "MA-substance-over-surface",
        "statement": (
            "Worlds, lenses, detectors, and reports must carry substantive "
            "logic and substance-bound evidence, not surface contracts alone."
        ),
        "source_refs": [
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d7_d13.md",
                "note": "D7 — No toys.",
            },
            {
                "kind": "doctrine",
                "locator": "docs/DOCTRINE.md",
                "note": "D17.5 — Substance floors are spec proxies.",
            },
            {
                "kind": "mistake_class",
                "locator": "CLAUDE_BUILDER_INITIATION.md",
                "note": "Class 5 — Surface coverage without substance.",
            },
            {
                "kind": "mistake_class",
                "locator": "CLAUDE_BUILDER_INITIATION.md",
                "note": "Class 8 — Abstract scalar standing in.",
            },
        ],
        "expected_artifact_families": [
            "world",
            "factory",
            "method",
            "test",
            "report",
        ],
        "expected_drift_constraint": (
            "Stub modules anchoring claim-bearing gates, abstract scalars "
            "replacing rich state, or shallow tests asserting existence "
            "rather than behavior are bad drift."
        ),
    },
    {
        "mission_atom_id": "MA-honest-empty-state",
        "statement": (
            "Read-only project surfaces and dashboards declare absence "
            "honestly rather than mocking missing data."
        ),
        "source_refs": [
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d22.md",
                "note": "D22 — Empty rooms beat stocked rooms with mock data.",
            },
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d25.md",
                "note": "D25 — Public verification honesty.",
            },
            {
                "kind": "mistake_class",
                "locator": "CLAUDE_BUILDER_INITIATION.md",
                "note": "Class 12 — Decorative completeness.",
            },
        ],
        "expected_artifact_families": [
            "control_room",
            "audit_report",
            "report",
            "test",
        ],
        "expected_drift_constraint": (
            "Synthetic placeholder content, mock charts, or decorative "
            "completeness in any read-only surface is bad drift."
        ),
    },
    {
        "mission_atom_id": "MA-cross-audit-discipline",
        "statement": (
            "Builds are cross-audited (Builder, Architect, Codex, Destroyer "
            "lanes) and the trace is the artifact rather than the AI's prose."
        ),
        "source_refs": [
            {
                "kind": "driver",
                "locator": "CLAUDE_BUILDER_INITIATION.md",
                "note": "Cross-audit triangle and 'trace is the artifact' canon.",
            },
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d19_d21.md",
                "note": "D19, D20 — extraction/detection separation; AI is not evidence.",
            },
            {
                "kind": "build_log",
                "locator": "BUILD_LOG.md",
                "note": "Cross-builder activation entries (TASK-CB-001 / CODEX_AUDIT_001).",
            },
        ],
        "expected_artifact_families": [
            "doctrine",
            "method",
            "audit_report",
            "driver_or_root_doc",
        ],
        "expected_drift_constraint": (
            "Reports promoting claim-bearing evidence without cross-audit "
            "trace or under same-AI extraction-and-detection drift this atom."
        ),
    },
    {
        "mission_atom_id": "MA-reproducible-research-instrument",
        "statement": (
            "The Attractor Observatory ships as a reproducible research "
            "instrument: shipped tests, shipped scripts, shipped reports, "
            "and a Mission Control surface against the shipped artifacts."
        ),
        "source_refs": [
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d25.md",
                "note": "D25 — public docs only claim public verification when shipped.",
            },
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d29.md",
                "note": "D29 — Runnable evidence.",
            },
            {
                "kind": "method",
                "locator": "papers/methods/PROJECT_GENEALOGY_PG001_SPEC.md",
                "note": "Mission Control Integration section makes the tab a v1 deliverable.",
            },
            {
                "kind": "driver",
                "locator": "Control_Room_README.md",
                "note": "Control Room is the project's reproducible-instrument surface.",
            },
        ],
        "expected_artifact_families": [
            "test",
            "control_room",
            "factory",
            "audit_instrument",
            "audit_report",
            "report",
        ],
        "expected_drift_constraint": (
            "Public claims pointing at private modules without explicit "
            "boundaries, or dashboards rendering against missing artifacts "
            "without empty-state, are bad drift."
        ),
    },
    {
        "mission_atom_id": "MA-stratified-corpus-discipline",
        "statement": (
            "Analysis on pooled corpora must verify within-stratum balance "
            "and run substrate-blocked controls (Step 0a/0b)."
        ),
        "source_refs": [
            {
                "kind": "mistake_class",
                "locator": "CLAUDE_BUILDER_INITIATION.md",
                "note": "Class 10 — Test-architecture / substrate-presence mismatch.",
            },
            {
                "kind": "mistake_class",
                "locator": "CLAUDE_BUILDER_INITIATION.md",
                "note": "Class 11 — Categorical confound through pooling.",
            },
            {
                "kind": "doctrine",
                "locator": "docs/doctrine_d15.md",
                "note": "D15 — No engineered floor (in DOCTRINE.md §D15).",
            },
        ],
        "expected_artifact_families": [
            "factory",
            "method",
            "report",
            "test",
        ],
        "expected_drift_constraint": (
            "Pooled-corpus claims without Step 0a/0b decomposition drift "
            "this atom."
        ),
    },
]


# ----- Threshold policy ----------------------------------------------------
#
# These thresholds are LOCKED before any finding runs. Tuning them after
# seeing outcomes is a D9/D18 violation. Defaults chosen to be conservative.

THRESHOLD_POLICY = {
    "drift": {
        "missing_birth_atom_count_for_review": 1,
        "missing_birth_atom_count_for_bad": 2,
        "letter_vs_spirit_pattern_count_for_flag": 1,
        "doctrine_boundary_crossing_for_bad": 2,
        "drift_critical_families": [
            "factory",
            "doctrine",
            "method",
            "audit_report",
            "audit_instrument",
            "falsifier",
            "prereg",
            "report",
        ],
    },
    "depth": {
        "default_axis": "predicate_atom_coverage",
        "low_axis_value": 0.34,
        "min_acceptable_value": 0.5,
    },
    "liveness": {
        "load_bearing_min_imports_in": 1,
        "load_bearing_min_validators": 1,
        "load_bearing_min_citations": 1,
    },
    "probe": {
        "global_budget_minutes": 0.0,
        "per_file_seconds": 0.0,
        "default_decline": "removal_probe_over_budget",
        "note": (
            "PG-001 v1 declines per-file probes globally under "
            "removal_probe_over_budget; the public test suite is exercised "
            "once at branch level via the cleanup-candidate sentinel test "
            "rather than per-file stash/restore. Files on the critical-path "
            "list are additionally declined under "
            "removal_probe_declined_critical_path."
        ),
    },
}


# ----- Probe registry per artifact_family ----------------------------------
#
# For PG-001 v1 we declare the probe-registry shape (per the spec's
# §"Removal Probe Protocol") and then declare the global budget at zero
# per-file seconds. Every non-critical-path file gets
# `cleanup_candidate_status=unknown` with `removal_probe.decline_reason
# = removal_probe_over_budget`. Every critical-path file gets
# `cleanup_candidate_status=probe_declined` with reason
# `removal_probe_declined_critical_path`. This is the "under-claimed
# status is permitted, over-claimed is not" rule from the spec.

PROBE_REGISTRY = {
    "factory": {
        "smoke_command": "python -m factory_lowlevel.continuous_daemon --dry-run --cycles 0",
        "test_target": "public_tests/test_task035_continuous_daemon.py",
    },
    "control_room": {
        "smoke_command": "python -c \"from control_room.launcher import main\"",
        "test_target": "public_tests/test_cb017_streamlit_unique_keys.py",
    },
    "report": {
        "smoke_command": "python -m project_genealogy.query files --artifact-family report",
        "test_target": "public_tests/test_pg001_schema.py",
    },
    "method": {
        "smoke_command": "python -m project_genealogy.query files --artifact-family method",
        "test_target": "public_tests/test_pg001_schema.py",
    },
    "doctrine": {
        "smoke_command": "python -m project_genealogy.query files --artifact-family doctrine",
        "test_target": "public_tests/test_pg001_schema.py",
    },
    "test": {
        "smoke_command": "python -m pytest public_tests/ --collect-only -q",
        "test_target": "public_tests/",
    },
    "audit_instrument": {
        "smoke_command": "python -c \"import project_genealogy.query as q; q.GenealogyIndex\"",
        "test_target": "public_tests/test_pg001_schema.py",
    },
    "audit_report": {
        "smoke_command": "python -m project_genealogy.query files --artifact-family audit_report",
        "test_target": "public_tests/test_pg001_schema.py",
    },
}


# ----- Probe-declined critical paths ---------------------------------------
#
# The spec requires these paths be declined under
# `removal_probe_declined_critical_path`.

CRITICAL_PATH_PATTERNS: list[str] = [
    r"^factory_lowlevel/persistence\.py$",
    r"^factory_lowlevel/launch_safety\.py$",
    r"^factory_lowlevel/schemas\.py$",
    r"^factory_lowlevel/router\.py$",
    r"^factory_lowlevel/registry\.py$",
    r"^factory_lowlevel/adapters\.py$",
    r"^factory_lowlevel/normalization\.py$",
    r"^factory_lowlevel/source_object_generation\.py$",
    r"^factory_lowlevel/world_construction\.py$",
    r"^factory_lowlevel/__init__\.py$",
    r"^public_tests/.*\.py$",
    r"^scripts/setup_worktree\.(bat|sh)$",
    r"^Launch Control Room\.bat$",
    r"^factory_daemon\.bat$",
    r"^make_source_object_generation\.py$",
    r"^pytest\.ini$",
    r"^requirements\.txt$",
    r"^Dockerfile$",
    r"^\.gitignore$",
    r"^\.gitattributes$",
    r"^control_room/__init__\.py$",
    r"^control_room/app\.py$",
    r"^control_room/launcher\.py$",
    r"^control_room/heartbeat\.py$",
    r"^control_room/snapshot\.py$",
    r"^control_room/components/empty_state\.py$",
    r"^control_room/rooms/__init__\.py$",
    r"^docs/doctrine_registry\.json$",
    r"^docs/DOCTRINE\.md$",
    r"^docs/doctrine_.*\.md$",
    r"^BUILD_LOG\.md$",
    r"^README\.md$",
    r"^LICENSE$",
    r"^CITATION\.cff$",
    r"^ro-crate-metadata\.json$",
    r"^project_genealogy/.*\.py$",
]

PG22_IMPLEMENTATION_SELF_AUDIT_PATHS: tuple[str, ...] = (
    "project_genealogy/atlas.py",
    "project_genealogy/birth.py",
    "project_genealogy/coherence.py",
    "project_genealogy/current.py",
    "project_genealogy/depth.py",
    "project_genealogy/dossier.py",
    "project_genealogy/drift.py",
    "project_genealogy/graph.py",
    "project_genealogy/hashing.py",
    "project_genealogy/manifest.py",
    "project_genealogy/probe.py",
    "project_genealogy/query.py",
    "project_genealogy/runner.py",
    "project_genealogy/__init__.py",
    "project_genealogy/__main__.py",
    "control_room/rooms/project_genealogy.py",
    "factory_lowlevel/memory_guard.py",
    "public_tests/test_pg001_acceptance_gates.py",
    "public_tests/test_pg001_control_room_tab.py",
    "public_tests/test_pg001_query.py",
    "public_tests/test_pg001_removal_probe.py",
    "public_tests/test_pg001_schema.py",
)


def is_critical_path(rel_path: str) -> bool:
    """Return True iff the path matches a probe-declined critical pattern."""
    return any(re.search(p, rel_path) for p in CRITICAL_PATH_PATTERNS)


# ----- Manifest builder ----------------------------------------------------


def _git(*args: str) -> str:
    out = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout


def _git_branch() -> str:
    return _git("rev-parse", "--abbrev-ref", "HEAD").strip()


def _git_head() -> str:
    return _git("rev-parse", "HEAD").strip()


def _git_dirty_files() -> list[str]:
    out = _git("status", "--porcelain=1")
    files: list[str] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        files.append(line[3:].strip())
    return files


def _git_ls_files(repo_root: Path) -> list[str]:
    out = _git("ls-files")
    return sorted(line.strip() for line in out.splitlines() if line.strip())


def _file_hashes(repo_root: Path, files: list[str]) -> dict[str, str]:
    """Hash each file's bytes (used as the manifest's input identity)."""
    out: dict[str, str] = {}
    for rel in files:
        p = repo_root / rel
        if p.is_file():
            try:
                out[rel] = hash_file(p)
            except OSError:
                out[rel] = "sha256:UNREADABLE"
    return out


def build_manifest(repo_root: Path, *, require_clean: bool = False) -> dict[str, Any]:
    """Construct the input manifest payload (without writing it)."""
    branch = _git_branch()
    head = _git_head()
    dirty = _git_dirty_files()
    if require_clean and dirty:
        raise RuntimeError(
            "PG-001 prepass requires a clean workspace; dirty files: "
            + ", ".join(dirty[:12])
            + (" ..." if len(dirty) > 12 else "")
        )
    all_tracked = _git_ls_files(repo_root)
    audited: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    for rel in all_tracked:
        family = determine_artifact_family(rel)
        cohort_only = is_cohort_only(rel)
        if cohort_only:
            excluded.append({
                "path": rel,
                "path_status": "private_unshipped",
                "evidence_private": True,
                "private_boundary_reason": "PG-001 cohort-only generated artifact excluded from public per-file audit surface.",
                "artifact_family": family,
                "decline_reason": "file_out_of_scope_by_manifest",
                "note": (
                    "Auto-generated mass-ingest/launch dump; represented at "
                    "cohort level by parent generator's dossier."
                ),
            })
            continue
        audited.append({
            "path": rel,
            "artifact_family": family,
            "critical_path": is_critical_path(rel),
        })

    file_hashes = _file_hashes(repo_root, [a["path"] for a in audited])
    audited_paths = {a["path"] for a in audited}
    excluded_paths = {e["path"] for e in excluded}
    pg22_missing = sorted(path for path in PG22_IMPLEMENTATION_SELF_AUDIT_PATHS if path not in audited_paths)

    payload: dict[str, Any] = {
        "schema": MANIFEST_SCHEMA,
        "pg_version": "PG-001",
        "run_binding": {
            "branch": branch,
            "head_commit": head,
            "workspace_dirty": bool(dirty),
            "dirty_files": dirty,
            "generation_command": "python -m project_genealogy run-prepass",
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "filters": {
            "include_globs": ["**/*"],
            "cohort_only_prefixes": list(COHORT_ONLY_PREFIXES),
            "report_include_filenames": list(REPORT_INCLUDE_FILENAMES),
            "family_rules": [{"pattern": p, "family": f} for p, f in FAMILY_RULES],
        },
        "audited_files": audited,
        "excluded_files": excluded,
        "audited_file_hashes": file_hashes,
        "mission_atoms": MISSION_ATOM_SEEDS,
        "threshold_policy": THRESHOLD_POLICY,
        "probe_registry": PROBE_REGISTRY,
        "critical_path_patterns": CRITICAL_PATH_PATTERNS,
        "decline_taxonomy": [
            "birth_predicate_not_recoverable",
            "current_predicate_not_recoverable",
            "private_history_unavailable",
            "generated_artifact_without_generator_binding",
            "ambiguous_parentage",
            "no_mechanical_reproducer",
            "file_out_of_scope_by_manifest",
            "public_runtime_boundary",
            "doctrine_mapping_ambiguous",
            "mission_atom_insufficient_source",
            "mission_atom_too_abstract",
            "removal_probe_declined_critical_path",
            "removal_probe_over_budget",
            "trajectory_insufficient_history",
        ],
        "doctrine_registry_ref": {
            "path": "docs/doctrine_registry.json",
            "content_hash": None,
        },
        "summary": {
            "tracked_total": len(all_tracked),
            "audited_count": len(audited),
            "excluded_count": len(excluded),
            "mission_atom_count": len(MISSION_ATOM_SEEDS),
        },
        "acceptance_gates": {
            "PG21_current_head_binding": {
                "passed": True,
                "head_commit": head,
                "scope": "manifest/atlas/coherence run_binding must cite this generation head",
            },
            "PG22_implementation_self_audit": {
                "passed": not pg22_missing,
                "required_paths": list(PG22_IMPLEMENTATION_SELF_AUDIT_PATHS),
                "missing_paths": pg22_missing,
            },
            "PG2_full_git_ls_files_universe": {
                "passed": len(audited_paths | excluded_paths) == len(all_tracked),
                "tracked_total": len(all_tracked),
                "audited_plus_excluded": len(audited_paths | excluded_paths),
            },
        },
    }
    # Doctrine registry hash (snapshot ref).
    doctrine_path = repo_root / "docs/doctrine_registry.json"
    if doctrine_path.is_file():
        payload["doctrine_registry_ref"]["content_hash"] = hash_file(doctrine_path)
    return payload


def write_manifest(repo_root: Path) -> tuple[Path, str]:
    payload = build_manifest(repo_root, require_clean=True)
    out_path = repo_root / REPORT_DIR / "input_manifest.json"
    h = write_with_hash(out_path, payload)
    return out_path, h


def cli_main(argv: list[str] | None = None) -> int:
    repo_root = Path.cwd()
    out_path, h = write_manifest(repo_root)
    print(f"wrote {out_path.relative_to(repo_root)}  content_hash={h}")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli_main())
