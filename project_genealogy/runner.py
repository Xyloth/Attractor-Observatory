"""End-to-end runner for PG-001 passes.

Public entry points (called by ``project_genealogy.__main__``):

* ``run_prepass`` — write input_manifest.json
* ``run_pass1`` — build structural graph (in-memory; consumed by Pass 2/3)
* ``run_pass2`` — produce per-file dossiers
* ``run_pass3`` — assemble atlas + ``atlas_latest.json``
* ``run_pass4`` — produce coherence report + ``coherence_latest.json``
* ``run_all`` — run all five in sequence

The runner is the single mechanical pipeline that drives the audit; each
pass writes its own checkpoint files. Pass 2 is parallelism-safe; here it
runs sequentially because per-file work is fast (~few ms) and the git log
cache benefits from sequential locality on Windows.
"""

from __future__ import annotations

import json
import sys
import time
import traceback
from collections import defaultdict
from pathlib import Path
from typing import Any

from project_genealogy import REPORT_DIR, DOSSIER_DIR
from project_genealogy.atlas import build_atlas, write_atlas
from project_genealogy.birth import reconstruct_birth
from project_genealogy.coherence import build_coherence, write_coherence
from project_genealogy.current import extract_current
from project_genealogy.dossier import build_dossier, write_dossier, safe_path
from project_genealogy.graph import build_structural_graph
from project_genealogy.hashing import canonical_json, sha256_hex, write_with_hash
from project_genealogy.manifest import build_manifest


def _now_msg(prefix: str, msg: str) -> None:
    print(f"[{prefix}] {msg}", flush=True)


def run_prepass(repo_root: Path) -> dict[str, Any]:
    _now_msg("prepass", "building input manifest …")
    payload = build_manifest(repo_root)
    out_path = repo_root / REPORT_DIR / "input_manifest.json"
    h = write_with_hash(out_path, payload)
    payload = json.loads(out_path.read_text(encoding="utf-8"))
    _now_msg(
        "prepass",
        f"manifest hash={h}  audited={payload['summary']['audited_count']}  "
        f"excluded={payload['summary']['excluded_count']}  "
        f"missions={payload['summary']['mission_atom_count']}",
    )
    return payload


def _gather_birth_current(
    repo_root: Path,
    audited_files: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    births: dict[str, dict[str, Any]] = {}
    currents: dict[str, dict[str, Any]] = {}
    n = len(audited_files)
    t0 = time.time()
    for i, entry in enumerate(audited_files):
        rel = entry["path"]
        family = entry["artifact_family"]
        try:
            births[rel] = reconstruct_birth(repo_root, rel, family)
        except Exception as e:  # noqa: BLE001
            births[rel] = {
                "status": "honest_decline",
                "decline_reason": "no_mechanical_reproducer",
                "first_seen_commit": "",
                "first_seen_date": "",
                "spawn_ticket": "",
                "birth_cohort_id": "",
                "parent_refs": [],
                "evidence_refs": [],
                "birth_predicate": {
                    "predicate_id": f"birth::{rel}",
                    "atoms": [],
                    "acceptance_criteria": [],
                    "forbidden_patterns": [],
                    "expected_doctrine_bindings": [],
                    "content_hash": "",
                },
            }
        try:
            currents[rel] = extract_current(repo_root, rel, family)
        except Exception:  # noqa: BLE001
            currents[rel] = {
                "status": "honest_decline",
                "decline_reason": "current_predicate_not_recoverable",
                "evidence_refs": [],
                "current_predicate": {
                    "predicate_id": f"current::{rel}",
                    "atoms": [],
                    "public_symbols": [],
                    "commands": [],
                    "generated_artifacts": [],
                    "observed_doctrine_bindings": [],
                    "content_hash": "",
                },
            }
        if (i + 1) % 50 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / max(elapsed, 1e-3)
            _now_msg(
                "pass1+2",
                f"birth/current {i + 1}/{n} ({rate:.1f}/s, {elapsed:.1f}s)",
            )
    _now_msg(
        "pass1+2",
        f"birth/current done in {time.time() - t0:.1f}s for {n} files",
    )
    return births, currents


def run_pass1(
    repo_root: Path,
    manifest: dict[str, Any],
    births: dict[str, dict[str, Any]] | None = None,
    currents: dict[str, dict[str, Any]] | None = None,
):
    _now_msg("pass1", "building structural graph …")
    audited = manifest["audited_files"]
    if births is None or currents is None:
        births, currents = _gather_birth_current(repo_root, audited)
    g = build_structural_graph(repo_root, audited, births, currents)
    _now_msg(
        "pass1",
        f"nodes={len(g.nodes)} edges={len(g.edges)} cohorts={len(g.cohorts)}",
    )
    return g, births, currents


def run_pass2(
    repo_root: Path,
    manifest: dict[str, Any],
    graph,
    births: dict[str, dict[str, Any]],
    currents: dict[str, dict[str, Any]],
) -> dict[str, tuple[Path, str]]:
    _now_msg("pass2", "writing per-file dossiers …")
    dossier_root = repo_root / DOSSIER_DIR
    if dossier_root.is_dir():
        for old_path in dossier_root.glob("*"):
            if old_path.suffix in {".json", ".md"}:
                old_path.unlink()
    n = len(manifest["audited_files"])
    out: dict[str, tuple[Path, str]] = {}
    t0 = time.time()
    for i, entry in enumerate(manifest["audited_files"]):
        rel = entry["path"]
        family = entry["artifact_family"]
        payload = build_dossier(
            repo_root,
            rel,
            family,
            manifest,
            graph,
            births.get(rel),
            currents.get(rel),
        )
        json_path, _md, h = write_dossier(repo_root, payload)
        out[rel] = (json_path, h)
        if (i + 1) % 50 == 0:
            _now_msg("pass2", f"dossiers {i + 1}/{n} ({(i + 1) / max(time.time() - t0, 1e-3):.1f}/s)")
    _now_msg("pass2", f"wrote {len(out)} dossiers in {time.time() - t0:.1f}s")
    return out


def run_pass3(
    repo_root: Path,
    manifest: dict[str, Any],
    graph,
    dossier_index: dict[str, tuple[Path, str]],
) -> dict[str, Any]:
    _now_msg("pass3", "assembling atlas …")
    atlas = build_atlas(repo_root, manifest, graph, dossier_index)
    versioned, pointer, h = write_atlas(repo_root, atlas)
    atlas["content_hash"] = h
    _now_msg("pass3", f"atlas={versioned.name} hash={h}")
    return atlas


def run_pass4(
    repo_root: Path,
    manifest: dict[str, Any],
    atlas: dict[str, Any],
) -> dict[str, Any]:
    _now_msg("pass4", "building coherence report …")
    coh = build_coherence(repo_root, manifest, atlas)
    versioned, pointer, h = write_coherence(repo_root, coh)
    coh["content_hash"] = h
    # Update atlas summary with coherence binding (re-write atlas_latest in place).
    atlas["summary"]["coherence_report_path"] = str(versioned.relative_to(repo_root)).replace("\\", "/")
    atlas["summary"]["coherence_report_hash"] = h
    atlas["summary"]["mission_atom_count"] = coh["summary"]["mission_atom_count"]
    atlas["summary"]["mission_coverage_status_counts"] = coh["summary"]["mission_coverage_status_counts"]
    atlas["summary"]["cohort_alignment_status_counts"] = coh["summary"]["cohort_alignment_status_counts"]
    atlas["summary"].setdefault("finding_partition", {})["coherence_mission_finding_count"] = len(coh.get("findings", []))
    # Re-write atlas_latest with coherence binding.
    pointer = repo_root / REPORT_DIR / "atlas_latest.json"
    atlas_payload = {**atlas}
    atlas_payload.pop("content_hash", None)
    write_with_hash(pointer, atlas_payload)
    _now_msg("pass4", f"coherence={versioned.name} hash={h}")
    return coh


def run_all(repo_root: Path) -> dict[str, Any]:
    manifest = run_prepass(repo_root)
    graph, births, currents = run_pass1(repo_root, manifest)
    dossier_index = run_pass2(repo_root, manifest, graph, births, currents)
    atlas = run_pass3(repo_root, manifest, graph, dossier_index)
    coh = run_pass4(repo_root, manifest, atlas)
    return {
        "manifest_hash": manifest.get("content_hash", ""),
        "atlas_hash": atlas.get("content_hash", ""),
        "coherence_hash": coh.get("content_hash", ""),
        "audited_count": manifest["summary"]["audited_count"],
        "excluded_count": manifest["summary"]["excluded_count"],
        "dossier_count": len(dossier_index),
        "edge_count": len(graph.edges),
        "cohort_count": len(graph.cohorts),
        "mission_atom_count": coh["summary"]["mission_atom_count"],
    }
