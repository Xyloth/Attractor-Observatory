"""Atlas builder — Pass 3.

Aggregates all per-file dossiers into a single ``ProjectGenealogyAtlas.v1``
payload. The atlas is the only artifact the visualization and Mission
Control tab consume; the spec requires the atlas be reconstructable from
dossier JSON alone.
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from project_genealogy import ATLAS_SCHEMA, REPORT_DIR, DOSSIER_DIR
from project_genealogy.graph import StructuralGraph
from project_genealogy.hashing import (
    canonical_json,
    content_hash,
    hash_file,
    sha256_hex,
    write_with_hash,
)


def _node_from_dossier(payload: dict[str, Any], dossier_path: str, dossier_hash: str) -> dict[str, Any]:
    f = payload["file"]
    b = payload["birth"]
    d = payload["drift_assessment"]
    depth = payload["depth"]
    liv = payload["liveness"]
    return {
        "node_id": f["path"],
        "path": f["path"],
        "artifact_family": f["artifact_family"],
        "birth_time": b.get("first_seen_date", ""),
        "spawn_ticket": b.get("spawn_ticket", ""),
        "dossier_path": dossier_path,
        "dossier_hash": dossier_hash,
        "depth": depth,
        "drift_status": d.get("status", "honest_decline"),
        "load_bearingness": depth.get("operational_load_bearingness", {}).get("weighted_value", 0.0),
        "doctrine_refs": payload["current"].get("current_predicate", {}).get("observed_doctrine_bindings", []),
        "mistake_classes": sorted({
            cls
            for fnd in payload.get("findings", [])
            for cls in fnd.get("mistake_classes", [])
        }),
        "cleanup_candidate": liv.get("cleanup_candidate_status") in (
            "removable_clean", "removable_with_warnings"
        ),
        "honest_decline": (
            b.get("status") == "honest_decline"
            or payload["current"].get("status") == "honest_decline"
        ),
        "cleanup_candidate_status": liv.get("cleanup_candidate_status", "unknown"),
    }


def build_atlas(
    repo_root: Path,
    manifest: dict[str, Any],
    graph: StructuralGraph,
    dossier_index: dict[str, tuple[Path, str]],
) -> dict[str, Any]:
    """Assemble atlas payload.

    ``dossier_index`` maps rel_path -> (json_path, content_hash).
    """
    nodes: list[dict[str, Any]] = []
    decline_count = 0
    confirmed_finding_count = 0
    bad_drift_count = 0
    cleanup_status_counts: dict[str, int] = defaultdict(int)
    drift_status_counts: dict[str, int] = defaultdict(int)
    edge_count_by_type: dict[str, int] = defaultdict(int)
    depth_axis_distributions: dict[str, dict[str, int]] = {
        "predicate_atom_coverage": {"low": 0, "medium": 0, "high": 0, "null": 0},
        "adversarial_surface_coverage": {"low": 0, "medium": 0, "high": 0, "null": 0},
    }
    doctrine_index: dict[str, list[str]] = defaultdict(list)
    ticket_index: dict[str, list[str]] = defaultdict(list)
    mistake_class_index: dict[str, list[str]] = defaultdict(list)
    liveness_index: dict[str, list[str]] = defaultdict(list)

    for rel, (json_path, h) in dossier_index.items():
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        rel_dossier_path = str(json_path.relative_to(repo_root)).replace("\\", "/")
        node = _node_from_dossier(payload, rel_dossier_path, h)
        nodes.append(node)
        # Tally summaries.
        drift_status_counts[node["drift_status"]] += 1
        if node["drift_status"] == "bad_drift":
            bad_drift_count += 1
        cleanup_status_counts[node["cleanup_candidate_status"]] += 1
        liveness_index[node["cleanup_candidate_status"]].append(rel)
        for d in node["doctrine_refs"]:
            doctrine_index[d].append(rel)
        if node["spawn_ticket"]:
            ticket_index[node["spawn_ticket"]].append(rel)
        for cls in node["mistake_classes"]:
            mistake_class_index[cls].append(rel)
        for fnd in payload.get("findings", []):
            if fnd.get("status") == "confirmed":
                confirmed_finding_count += 1
        decline_count += len(payload.get("declines", []))

        for axis_name in ("predicate_atom_coverage", "adversarial_surface_coverage"):
            v = node["depth"].get(axis_name, {}).get("value")
            if v is None:
                depth_axis_distributions[axis_name]["null"] += 1
            elif v < 0.34:
                depth_axis_distributions[axis_name]["low"] += 1
            elif v < 0.67:
                depth_axis_distributions[axis_name]["medium"] += 1
            else:
                depth_axis_distributions[axis_name]["high"] += 1

    for e in graph.edges:
        edge_count_by_type[e["edge_type"]] += 1

    cohorts = list(graph.cohorts.values())

    payload = {
        "schema": ATLAS_SCHEMA,
        "run_binding": {
            "input_manifest_hash": manifest.get("content_hash", ""),
            "branch": manifest.get("run_binding", {}).get("branch", ""),
            "head_commit": manifest.get("run_binding", {}).get("head_commit", ""),
            "workspace_dirty": manifest.get("run_binding", {}).get("workspace_dirty", False),
            "generation_command": "python -m project_genealogy run-pass3",
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "freshness_status": "computed_at_read",
        },
        "summary": {
            "file_count": len(nodes),
            "dossier_count": len(dossier_index),
            "decline_count": decline_count,
            "confirmed_finding_count": confirmed_finding_count,
            "finding_partition": {
                "dossier_confirmed_finding_count": confirmed_finding_count,
                "coherence_mission_finding_count": None,
                "scope_note": "Atlas confirmed_finding_count counts per-file dossier findings; coherence findings are mission-coverage findings.",
            },
            "bad_drift_count": bad_drift_count,
            "cleanup_candidate_count_by_status": dict(cleanup_status_counts),
            "cohort_count": len(cohorts),
            "edge_count_by_type": dict(edge_count_by_type),
            "depth_axis_distributions": depth_axis_distributions,
            "drift_status_counts": dict(drift_status_counts),
            "mission_atom_count": len(manifest.get("mission_atoms", [])),
            "mission_coverage_status_counts": {},
            "cohort_alignment_status_counts": {},
            "coherence_report_path": "",
            "coherence_report_hash": "",
        },
        "nodes": nodes,
        "edges": list(graph.edges),
        "cohorts": cohorts,
        "doctrine_index": dict(doctrine_index),
        "ticket_index": dict(ticket_index),
        "mistake_class_index": dict(mistake_class_index),
        "liveness_index": dict(liveness_index),
        "query_materializations": {},
        "acceptance_gates": {
            "PG21_current_head_binding": {
                "passed": payload["run_binding"]["head_commit"] == manifest.get("run_binding", {}).get("head_commit", ""),
                "head_commit": payload["run_binding"]["head_commit"],
                "input_manifest_hash": manifest.get("content_hash", ""),
            },
            "PG22_implementation_self_audit": manifest.get("acceptance_gates", {}).get("PG22_implementation_self_audit", {}),
        },
        "declines": [
            {
                "kind": "manifest_excluded",
                "path": e["path"],
                "path_status": e.get("path_status", "private_unshipped"),
                "evidence_private": e.get("evidence_private", True),
                "private_boundary_reason": e.get(
                    "private_boundary_reason",
                    "PG-001 manifest-excluded artifact is not presented as dereferenceable public evidence.",
                ),
                "reason": e["decline_reason"],
                "note": e.get("note", ""),
            }
            for e in manifest.get("excluded_files", [])
        ],
    }
    return payload


def write_atlas(
    repo_root: Path,
    payload: dict[str, Any],
) -> tuple[Path, Path, str]:
    """Write versioned atlas JSON plus update atlas_latest.json pointer."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    versioned = repo_root / REPORT_DIR / f"atlas_{ts}.json"
    pointer = repo_root / REPORT_DIR / "atlas_latest.json"
    h = write_with_hash(versioned, payload)
    # Pointer carries the same content (a copy under a stable name).
    pointer_payload = {**payload, "_pointer_to": versioned.name, "_atlas_version": ts}
    pointer_payload.pop("content_hash", None)
    write_with_hash(pointer, pointer_payload)
    return versioned, pointer, h
