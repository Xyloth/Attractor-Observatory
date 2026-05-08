"""Per-file dossier builder.

Pulls together birth + current + depth + drift + probe into a single
``ProjectGenealogyDossier.v1`` payload, plus the Markdown rendering.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from project_genealogy import DOSSIER_SCHEMA, DOSSIER_DIR
from project_genealogy.birth import reconstruct_birth
from project_genealogy.current import extract_current
from project_genealogy.depth import compute_depth
from project_genealogy.drift import assess_drift
from project_genealogy.graph import StructuralGraph
from project_genealogy.hashing import write_with_hash, content_hash, hash_file
from project_genealogy.probe import run_probe


def safe_path(rel_path: str) -> str:
    """Convert a tracked path to a safe dossier filename component.

    Windows filesystems are case-insensitive, so two distinct repo paths
    that differ only by case (e.g. ``Control_Room_README.md`` and
    ``control_room/README.md`` after path-separator collapse) would
    otherwise overwrite each other on disk. The 12-hex prefix derives
    from a SHA-256 of the case-preserving relative path and disambiguates
    such collisions while keeping the human-readable suffix intact.
    """
    import hashlib
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", rel_path).strip("_")
    digest = hashlib.sha256(rel_path.encode("utf-8")).hexdigest()[:12]
    return f"{digest}_{cleaned}"


def build_findings(
    rel_path: str,
    artifact_family: str,
    drift: dict[str, Any],
    current: dict[str, Any],
    threshold_policy: dict[str, Any],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    cp = current.get("current_predicate", {})

    # Letter-vs-spirit findings (one per surface, mistake_class Class13/Class7).
    for i, surf in enumerate(cp.get("letter_vs_spirit_surfaces", [])):
        findings.append({
            "finding_id": f"PG-{rel_path}-lvs-{i}",
            "severity": "info",
            "status": "hypothesis",
            "claim": (
                f"Detected letter-coupled fix surface at line {surf.get('line')}: "
                f"{surf.get('snippet', '')[:120]}"
            ),
            "mistake_classes": ["Class7", "Class13"],
            "doctrine_refs": ["D26", "D27"],
            "evidence_refs": [
                {
                    "ref_id": f"finding::{rel_path}::lvs::{i}",
                    "kind": "grep",
                    "locator": f"{rel_path}#L{surf.get('line')}",
                    "content_hash": "",
                    "evidence_private": False,
                    "note": "letter-coupled surface detected mechanically",
                }
            ],
            "reproducer": {
                "kind": "grep",
                "command": f'rg -n -F {repr(surf.get("snippet", "")[:60])} -- {rel_path}',
                "expected_result": "non-zero match at the cited line",
                "last_run_status": "not_run",
            },
            "recommendation": (
                "Determine whether the surface gates a class of failure or "
                "only a literal symptom; if literal, add a class-level guard "
                "or downgrade to honest_decline."
            ),
        })

    # Class pattern matches (engineered passing, decorative completeness, etc.)
    for i, m in enumerate(cp.get("class_pattern_matches", [])):
        findings.append({
            "finding_id": f"PG-{rel_path}-class-{i}",
            "severity": "low",
            "status": "hypothesis",
            "claim": (
                f"Detected pattern matching {m['class_id']} ({m['note']}) at line {m.get('line')}"
            ),
            "mistake_classes": [m["class_id"]],
            "doctrine_refs": [],
            "evidence_refs": [
                {
                    "ref_id": f"finding::{rel_path}::cls::{i}",
                    "kind": "grep",
                    "locator": f"{rel_path}#L{m.get('line')}",
                    "content_hash": "",
                    "evidence_private": False,
                    "note": m["note"],
                }
            ],
            "reproducer": {
                "kind": "grep",
                "command": f'rg -n -F {repr(m.get("snippet", "")[:60])} -- {rel_path}',
                "expected_result": "match at the cited line",
                "last_run_status": "not_run",
            },
            "recommendation": (
                "Cross-reference with the originating campaign brief; if the "
                "pattern is intentional and source-bound, document; if not, "
                "open a follow-up ticket."
            ),
        })

    # Bad/review drift findings.
    if drift.get("status") == "bad_drift":
        findings.append({
            "finding_id": f"PG-{rel_path}-drift-bad",
            "severity": "high",
            "status": "confirmed",
            "claim": (
                "Bad drift: birth predicate atoms missing from current "
                f"predicate ({len(drift.get('missing_birth_atoms', []))} missing) or "
                "doctrine boundary crossings detected."
            ),
            "mistake_classes": ["Class5"],
            "doctrine_refs": drift.get("doctrine_boundary_crossings", []) and [
                c.get("doctrine_id", "")
                for c in drift["doctrine_boundary_crossings"]
            ] or [],
            "evidence_refs": drift.get("reproducer_refs", []),
            "reproducer": {
                "kind": "json_query",
                "command": (
                    f"python -c \"import json,sys; d=json.load(open('{DOSSIER_DIR}/{safe_path(rel_path)}.json')); "
                    "print(d['drift_assessment'])\""
                ),
                "expected_result": "drift_assessment payload with bad_drift status",
                "last_run_status": "pass",
            },
            "recommendation": (
                "Trace the missing atoms to the originating campaign and "
                "either add executable evidence for them or downgrade to "
                "honest_decline with reason."
            ),
        })
    elif drift.get("status") == "review_required":
        findings.append({
            "finding_id": f"PG-{rel_path}-drift-review",
            "severity": "medium",
            "status": "hypothesis",
            "claim": (
                "Drift requires review: missing or new atoms or letter-vs-spirit "
                "surfaces present without yet crossing a doctrine boundary."
            ),
            "mistake_classes": ["Class5"],
            "doctrine_refs": [],
            "evidence_refs": drift.get("reproducer_refs", []),
            "reproducer": {
                "kind": "json_query",
                "command": (
                    f"python -c \"import json,sys; d=json.load(open('{DOSSIER_DIR}/{safe_path(rel_path)}.json')); "
                    "print(d['drift_assessment'])\""
                ),
                "expected_result": "drift_assessment payload with review_required status",
                "last_run_status": "pass",
            },
            "recommendation": "Cross-audit with campaign driver and add explicit acceptance evidence.",
        })

    return findings


def build_dossier(
    repo_root: Path,
    rel_path: str,
    artifact_family: str,
    manifest: dict[str, Any],
    graph: StructuralGraph,
    birth_record: dict[str, Any] | None = None,
    current_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble the full dossier payload."""
    abs_path = repo_root / rel_path
    line_count = 0
    byte_count = 0
    if abs_path.is_file():
        try:
            text = abs_path.read_text(encoding="utf-8", errors="replace")
            line_count = text.count("\n") + (0 if text.endswith("\n") else 1)
            byte_count = len(text.encode("utf-8"))
        except OSError:
            pass

    if birth_record is None:
        birth_record = reconstruct_birth(repo_root, rel_path, artifact_family)
    if current_record is None:
        current_record = extract_current(repo_root, rel_path, artifact_family)

    incoming = graph.parents(rel_path) if rel_path in graph.nodes else []
    outgoing = graph.children(rel_path) if rel_path in graph.nodes else []

    threshold_policy = manifest.get("threshold_policy", {})
    expected_d = birth_record.get("birth_predicate", {}).get("expected_doctrine_bindings", [])
    declared = current_record.get("current_predicate", {}).get("observed_doctrine_bindings", [])
    depth = compute_depth(
        rel_path,
        artifact_family,
        birth_record,
        current_record,
        incoming,
        outgoing,
        expected_d,
        declared,
    )
    drift = assess_drift(
        birth_record,
        current_record,
        threshold_policy,
        artifact_family=artifact_family,
    )
    liveness = run_probe(rel_path, artifact_family, threshold_policy, incoming)
    findings = build_findings(rel_path, artifact_family, drift, current_record, threshold_policy)

    declines: list[dict[str, Any]] = []
    if birth_record.get("status") == "honest_decline":
        declines.append({
            "kind": "birth",
            "reason": birth_record.get("decline_reason", "birth_predicate_not_recoverable"),
            "evidence_ref": {
                "ref_id": f"decline::{rel_path}::birth",
                "kind": "git_query",
                "locator": f"git log --diff-filter=A --follow -- {rel_path}",
                "content_hash": "",
                "evidence_private": False,
                "note": "first-add commit not resolvable",
            },
        })
    if current_record.get("status") == "honest_decline":
        declines.append({
            "kind": "current",
            "reason": current_record.get("decline_reason", "current_predicate_not_recoverable"),
            "evidence_ref": {
                "ref_id": f"decline::{rel_path}::current",
                "kind": "file_span",
                "locator": rel_path,
                "content_hash": "",
                "evidence_private": False,
                "note": "current contents not readable",
            },
        })
    if drift.get("status") == "honest_decline":
        declines.append({
            "kind": "drift",
            "reason": drift.get("decline_reason", "no_mechanical_reproducer"),
            "evidence_ref": {
                "ref_id": f"decline::{rel_path}::drift",
                "kind": "json_query",
                "locator": f"{DOSSIER_DIR}/{safe_path(rel_path)}.json#drift_assessment",
                "content_hash": "",
                "evidence_private": False,
                "note": "drift cannot be assessed without recoverable predicates",
            },
        })

    cohort_id = birth_record.get("birth_cohort_id", "")
    cohort = graph.cohorts.get(cohort_id, {
        "cohort_id": cohort_id,
        "spawn_ticket": birth_record.get("spawn_ticket", ""),
        "members": [rel_path],
    })

    is_python = rel_path.endswith(".py")
    language = "python" if is_python else (
        "markdown" if rel_path.endswith(".md") else (
            "json" if rel_path.endswith(".json") or rel_path.endswith(".jsonld") else (
                "shell" if rel_path.endswith(".sh") else (
                    "batch" if rel_path.endswith(".bat") else "text"
                )
            )
        )
    )
    generated_status = "report" if rel_path.startswith("reports/") else (
        "generated" if "generated" in rel_path or "snapshot" in rel_path else "source"
    )

    payload: dict[str, Any] = {
        "schema": DOSSIER_SCHEMA,
        "file": {
            "path": rel_path,
            "path_hash": hash_file(repo_root / rel_path) if (repo_root / rel_path).is_file() else "",
            "tracked": True,
            "language": language,
            "artifact_family": artifact_family,
            "line_count": line_count,
            "byte_count": byte_count,
            "generated_status": generated_status,
            "private_boundary": {
                "evidence_private": False,
                "reason": "",
            },
        },
        "run_binding": {
            "input_manifest_hash": manifest.get("content_hash", ""),
            "branch": manifest.get("run_binding", {}).get("branch", ""),
            "head_commit": manifest.get("run_binding", {}).get("head_commit", ""),
            "workspace_dirty": manifest.get("run_binding", {}).get("workspace_dirty", False),
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "generation_command": "python -m project_genealogy run-pass2",
            "pg_version": "PG-001",
        },
        "birth": birth_record,
        "current": current_record,
        "genealogy": {
            "parents": [
                {
                    "edge_id": e["edge_id"],
                    "edge_type": e["edge_type"],
                    "source": e["source"],
                    "evidence_refs": e.get("evidence_refs", []),
                }
                for e in incoming
            ],
            "children": [
                {
                    "edge_id": e["edge_id"],
                    "edge_type": e["edge_type"],
                    "target": e["target"],
                    "evidence_refs": e.get("evidence_refs", []),
                }
                for e in outgoing
            ],
            "siblings": [
                m for m in cohort.get("members", []) if m != rel_path
            ][:50],
            "cohort": cohort,
            "edges": incoming + outgoing,
        },
        "depth": depth,
        "drift_assessment": drift,
        "liveness": liveness,
        "consistency": {
            "cohort_findings": [],
            "cross_doctrine_collisions": [],
            "sibling_divergence": [],
        },
        "findings": findings,
        "declines": declines,
    }
    return payload


def render_markdown(payload: dict[str, Any], json_path_rel: str) -> str:
    """Render a Markdown view of the dossier — JSON is authoritative.

    Per spec: deleting the Markdown must not remove machine-readable claims;
    deleting the JSON must invalidate the Markdown rendering.
    """
    f = payload["file"]
    b = payload["birth"]
    c = payload["current"]
    d = payload["drift_assessment"]
    depth = payload["depth"]
    liv = payload["liveness"]
    findings = payload.get("findings", [])

    lines: list[str] = []
    lines.append(f"# Dossier: `{f['path']}`")
    lines.append("")
    lines.append("> JSON is authoritative. This file is a rendering of the JSON dossier.")
    lines.append("")
    lines.append(f"- JSON: `{json_path_rel}`")
    lines.append(f"- JSON content_hash: `{payload.get('content_hash', '<computed at write>')}`")
    lines.append(f"- Schema: `{payload['schema']}`")
    lines.append(f"- Artifact family: `{f['artifact_family']}`")
    lines.append(f"- Generated status: `{f['generated_status']}`")
    lines.append(f"- Lines: {f['line_count']} / Bytes: {f['byte_count']}")
    lines.append("")
    lines.append("## Birth")
    lines.append(f"- Status: `{b.get('status', '')}`")
    lines.append(f"- First-seen commit: `{b.get('first_seen_commit', '')}`")
    lines.append(f"- First-seen date: `{b.get('first_seen_date', '')}`")
    lines.append(f"- Spawn ticket: `{b.get('spawn_ticket', '')}`")
    lines.append(f"- Cohort: `{b.get('birth_cohort_id', '')}`")
    if b.get("decline_reason"):
        lines.append(f"- Decline reason: `{b['decline_reason']}`")
    lines.append("")
    lines.append("### Birth predicate atoms")
    for atom in b.get("birth_predicate", {}).get("atoms", []):
        lines.append(f"- **{atom.get('atom_id', '')}** — {atom.get('statement', '')}")
    lines.append("")
    lines.append("## Current")
    lines.append(f"- Status: `{c.get('status', '')}`")
    cp = c.get("current_predicate", {})
    if cp.get("public_symbols"):
        lines.append(f"- Public symbols: `{', '.join(cp['public_symbols'][:10])}`")
    if cp.get("observed_doctrine_bindings"):
        lines.append(f"- Observed doctrines: `{', '.join(cp['observed_doctrine_bindings'])}`")
    lines.append("")
    lines.append("## DepthVector.v1")
    for axis in (
        "predicate_atom_coverage",
        "adversarial_surface_coverage",
        "doctrine_binding_quality",
        "evidence_integration",
        "operational_load_bearingness",
    ):
        lines.append(f"- **{axis}**: `{depth.get(axis, {})}`")
    lines.append("")
    lines.append("## Drift")
    lines.append(f"- Status: `{d.get('status', '')}`")
    if d.get("missing_birth_atoms"):
        lines.append(f"- Missing birth atoms: `{', '.join(d['missing_birth_atoms'])}`")
    if d.get("doctrine_boundary_crossings"):
        lines.append(f"- Doctrine boundary crossings: {len(d['doctrine_boundary_crossings'])}")
    if d.get("letter_vs_spirit_flags"):
        lines.append(f"- Letter-vs-spirit surfaces: {len(d['letter_vs_spirit_flags'])}")
    lines.append("")
    lines.append("## Liveness")
    lines.append(f"- Cleanup candidate status: `{liv.get('cleanup_candidate_status', '')}`")
    lines.append(f"- Cleanup reason: {liv.get('cleanup_reason', '')}")
    lines.append(f"- Probe outcome: `{liv.get('removal_probe', {}).get('outcome', '')}`")
    lines.append(f"- Probe decline reason: `{liv.get('removal_probe', {}).get('decline_reason', '')}`")
    lines.append("")
    lines.append("## Findings")
    if not findings:
        lines.append("_No findings detected mechanically._")
    for fnd in findings:
        lines.append(
            f"- **{fnd['finding_id']}** "
            f"({fnd['severity']}, {fnd['status']}): {fnd['claim']}"
        )
    lines.append("")
    declines = payload.get("declines", [])
    if declines:
        lines.append("## Declines")
        for dec in declines:
            lines.append(f"- {dec['kind']}: `{dec['reason']}`")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.")
    return "\n".join(lines)


def write_dossier(
    repo_root: Path,
    payload: dict[str, Any],
) -> tuple[Path, Path, str]:
    """Write JSON + Markdown dossier; return (json_path, md_path, hash)."""
    rel = payload["file"]["path"]
    name = safe_path(rel)
    json_path = repo_root / DOSSIER_DIR / (name + ".json")
    md_path = repo_root / DOSSIER_DIR / (name + ".md")
    h = write_with_hash(json_path, payload)
    md = render_markdown({**payload, "content_hash": h}, str(json_path.relative_to(repo_root)).replace("\\", "/"))
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(md, encoding="utf-8")
    return json_path, md_path, h
