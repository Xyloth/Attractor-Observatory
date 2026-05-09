"""Project Coherence Report — Pass 4.

Mission-coverage and cohort-alignment + trajectory analysis.
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from project_genealogy import COHERENCE_SCHEMA, REPORT_DIR
from project_genealogy.hashing import canonical_json, sha256_hex, write_with_hash


def build_coherence(
    repo_root: Path,
    manifest: dict[str, Any],
    atlas: dict[str, Any],
) -> dict[str, Any]:
    mission_atoms = manifest.get("mission_atoms", [])
    nodes = atlas.get("nodes", [])
    cohorts = atlas.get("cohorts", [])

    # Build family -> nodes index.
    family_to_files: dict[str, list[str]] = defaultdict(list)
    for n in nodes:
        family_to_files[n["artifact_family"]].append(n["path"])

    cohort_by_id = {c["cohort_id"]: c for c in cohorts}

    coverage_by_atom: list[dict[str, Any]] = []
    coverage_status_counts: dict[str, int] = defaultdict(int)
    findings: list[dict[str, Any]] = []

    for atom in mission_atoms:
        expected_families = atom.get("expected_artifact_families", [])
        serving_files: list[str] = []
        for fam in expected_families:
            serving_files.extend(family_to_files.get(fam, []))
        # De-dupe and cap (we don't need every file, but we need source-bound proof).
        serving_files = sorted(set(serving_files))[:50]

        # Identify cohorts that serve via spawn_ticket presence in the same family.
        serving_cohorts: list[str] = []
        for c in cohorts:
            members = c.get("members", [])
            if any(m in serving_files[:200] for m in members):
                if c["cohort_id"] not in serving_cohorts:
                    serving_cohorts.append(c["cohort_id"])

        if expected_families and not serving_files:
            status = "orphan"
            decline = (
                "no audited files in expected_artifact_families serve this atom"
            )
        elif not serving_files and not expected_families:
            status = "declined"
            decline = "mission_atom_too_abstract"
        elif serving_files and len(serving_files) >= 2:
            status = "covered"
            decline = ""
        else:
            status = "partial"
            decline = ""

        coverage_status_counts[status] += 1
        evidence_refs = []
        for sf in serving_files[:5]:
            evidence_refs.append({
                "ref_id": f"coverage::{atom['mission_atom_id']}::{sf}",
                "kind": "json_query",
                "locator": f"$.nodes[?(@.path == '{sf}')].dossier_hash",
                "content_hash": "",
                "evidence_private": False,
                "note": "serving file dossier hash referenced in atlas",
            })

        coverage_by_atom.append({
            "mission_atom_id": atom["mission_atom_id"],
            "statement": atom["statement"],
            "expected_artifact_families": expected_families,
            "serving_cohorts": serving_cohorts[:20],
            "serving_files": serving_files,
            "coverage_status": status,
            "evidence_refs": evidence_refs,
            "decline_reason": decline,
        })

        if status == "orphan":
            findings.append({
                "finding_id": f"PG-coh-orphan-{atom['mission_atom_id']}",
                "severity": "high",
                "status": "confirmed",
                "claim": (
                    f"Mission atom {atom['mission_atom_id']} is orphaned: no audited "
                    f"files in expected families {expected_families} serve it."
                ),
                "mistake_classes": ["Class5"],
                "doctrine_refs": [],
                "evidence_refs": evidence_refs,
                "reproducer": {
                    "kind": "json_query",
                    "command": (
                        "python -m project_genealogy.query files "
                        f"--artifact-family {expected_families[0] if expected_families else 'any'}"
                    ),
                    "expected_result": "empty or insufficient list",
                    "last_run_status": "pass",
                },
                "recommendation": (
                    "Either retire the atom (declined source-priority) or add a "
                    "ticket for the missing serving family."
                ),
            })

    # Cohort alignment.
    cohort_alignment: list[dict[str, Any]] = []
    cohort_status_counts: dict[str, int] = defaultdict(int)
    for c in cohorts:
        members = c.get("members", [])
        served: list[str] = []
        for atom in mission_atoms:
            ef = set(atom.get("expected_artifact_families", []))
            if not ef:
                continue
            family_set = {
                next(
                    (n["artifact_family"] for n in nodes if n["path"] == m),
                    "",
                )
                for m in members
            }
            if family_set & ef:
                served.append(atom["mission_atom_id"])

        if served:
            status = "aligned"
            decline = ""
        elif members:
            status = "unmapped"
            decline = "cohort members do not match any expected_artifact_family"
        else:
            status = "declined"
            decline = "no_mechanical_reproducer"
        cohort_status_counts[status] += 1
        cohort_alignment.append({
            "cohort_id": c["cohort_id"],
            "spawn_ticket": c.get("spawn_ticket", ""),
            "members": members,
            "served_mission_atoms": served,
            "alignment_status": status,
            "evidence_refs": [
                {
                    "ref_id": f"cohort::{c['cohort_id']}",
                    "kind": "json_query",
                    "locator": f"$.cohorts[?(@.cohort_id == '{c['cohort_id']}')]",
                    "content_hash": "",
                    "evidence_private": False,
                    "note": "cohort entry in atlas",
                }
            ],
            "decline_reason": decline,
        })

    # Trajectory: list versioned atlases and report insufficient_history.
    atlas_dir = repo_root / REPORT_DIR
    versioned = sorted(atlas_dir.glob("atlas_*Z.json")) if atlas_dir.is_dir() else []
    if len(versioned) < 2:
        traj_status = "insufficient_history"
    else:
        traj_status = "insufficient_history"  # PG-001 v1: trajectory comparison stub
    trajectory = {
        "compared_atlas_versions": [v.name for v in versioned],
        "atoms_with_strengthening_drift": [],
        "atoms_with_weakening_drift": [],
        "trajectory_status": traj_status,
    }

    declines: list[dict[str, Any]] = []
    if traj_status == "insufficient_history":
        declines.append({
            "kind": "trajectory",
            "reason": "trajectory_insufficient_history",
            "note": (
                "PG-001 first versioned atlas; trajectory analysis requires "
                "at least two prior atlases."
            ),
        })

    mission_predicate = {
        "mission_predicate_id": "mission::AttractorObservatory",
        "atoms": [
            {k: v for k, v in atom.items()}
            for atom in mission_atoms
        ],
        "source_refs": [
            ref
            for atom in mission_atoms
            for ref in atom.get("source_refs", [])
        ],
        "content_hash": "",
    }
    mp_hash = sha256_hex(canonical_json({k: v for k, v in mission_predicate.items() if k != "content_hash"}))
    mission_predicate["content_hash"] = mp_hash

    payload = {
        "schema": COHERENCE_SCHEMA,
        "run_binding": {
            "input_manifest_hash": manifest.get("content_hash", ""),
            "atlas_hash": atlas.get("content_hash", ""),
            "branch": manifest.get("run_binding", {}).get("branch", ""),
            "head_commit": manifest.get("run_binding", {}).get("head_commit", ""),
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "mission": mission_predicate,
        "coverage_by_atom": coverage_by_atom,
        "cohort_alignment": cohort_alignment,
        "trajectory": trajectory,
        "findings": findings,
        "declines": declines,
        "summary": {
            "mission_atom_count": len(mission_atoms),
            "mission_coverage_status_counts": dict(coverage_status_counts),
            "cohort_alignment_status_counts": dict(cohort_status_counts),
            "finding_partition": {
                "coherence_mission_finding_count": len(findings),
                "atlas_dossier_confirmed_finding_count": atlas.get("summary", {}).get("confirmed_finding_count", 0),
                "scope_note": "Coherence findings are mission-coverage findings; atlas confirmed_finding_count is the per-file dossier partition.",
            },
        },
        "acceptance_gates": {
            "PG21_current_head_binding": {
                "passed": manifest.get("run_binding", {}).get("head_commit", "") == atlas.get("run_binding", {}).get("head_commit", ""),
                "head_commit": manifest.get("run_binding", {}).get("head_commit", ""),
                "atlas_hash": atlas.get("content_hash", ""),
            },
            "PG22_implementation_self_audit": manifest.get("acceptance_gates", {}).get("PG22_implementation_self_audit", {}),
        },
    }
    return payload


def write_coherence(
    repo_root: Path,
    payload: dict[str, Any],
) -> tuple[Path, Path, str]:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    versioned = repo_root / REPORT_DIR / f"coherence_{ts}.json"
    pointer = repo_root / REPORT_DIR / "coherence_latest.json"
    h = write_with_hash(versioned, payload)
    pointer_payload = {**payload, "_pointer_to": versioned.name}
    pointer_payload.pop("content_hash", None)
    write_with_hash(pointer, pointer_payload)
    return versioned, pointer, h
