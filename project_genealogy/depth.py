"""DepthVector.v1 — five-axis depth measurement.

Per spec §"DepthVector.v1": five mechanical axes, never compressed into a
single scalar at storage time. UIs may pick a single axis to display.

* predicate_atom_coverage
* adversarial_surface_coverage
* doctrine_binding_quality
* evidence_integration
* operational_load_bearingness
"""

from __future__ import annotations

from typing import Any


def _safe_div(num: float, den: float) -> float | None:
    if den <= 0:
        return None
    return float(num) / float(den)


def compute_depth(
    rel_path: str,
    artifact_family: str,
    birth: dict[str, Any],
    current: dict[str, Any],
    incoming_edges: list[dict[str, Any]],
    outgoing_edges: list[dict[str, Any]],
    expected_doctrine_bindings: list[str],
    declared_at_birth: list[str],
) -> dict[str, Any]:
    """Compute the five-axis depth vector."""
    birth_atoms = birth.get("birth_predicate", {}).get("atoms", [])
    current_atoms = current.get("current_predicate", {}).get("atoms", [])

    # Axis 1: predicate_atom_coverage
    claimable = len(birth_atoms)
    covered = 0
    missing: list[str] = []
    if claimable > 0:
        # An atom is "covered" if any current atom statement contains a
        # related keyword (very weak link; PG-001 v1 keeps coverage
        # mechanical: every birth atom whose acceptance_evidence_expected
        # selector matches *something* in current atoms counts).
        current_kinds = {
            (a.get("source_ref", {}) or {}).get("kind", "")
            for a in current_atoms
        }
        current_kinds.discard("")
        for atom in birth_atoms:
            evidence_expected = atom.get("acceptance_evidence_expected", [])
            if not evidence_expected:
                # No specific selector demanded; presence of public surface
                # or content in current counts as coverage.
                if current_atoms:
                    covered += 1
                else:
                    missing.append(atom.get("atom_id", ""))
                continue
            matched = False
            for ev in evidence_expected:
                kind = ev.get("kind", "")
                if kind in current_kinds:
                    matched = True
                    break
            if matched:
                covered += 1
            else:
                missing.append(atom.get("atom_id", ""))
    cov_value = _safe_div(covered, claimable) if claimable else None

    # Axis 2: adversarial_surface_coverage
    # PG-001 v1 records the surfaces detected (letter_vs_spirit_surfaces,
    # class_pattern_matches) but treats coverage of *bad cases* as a list
    # of patterns observed vs a per-family expected count.
    cp = current.get("current_predicate", {})
    letter_surfaces = cp.get("letter_vs_spirit_surfaces", [])
    class_matches = cp.get("class_pattern_matches", [])
    required_bad_cases: list[dict[str, Any]] = []
    if artifact_family in {"factory", "control_room", "report"}:
        # These families are expected to surface error/edge handling.
        required_bad_cases = [
            {"id": "error_branch", "kind": "letter_pattern"},
            {"id": "decline_branch", "kind": "letter_pattern"},
        ]
    covered_bad = []
    for surf in letter_surfaces:
        if surf.get("pattern", "").startswith("except"):
            covered_bad.append({"id": "error_branch", "line": surf.get("line")})
    if any(s.get("snippet", "").startswith("if") for s in letter_surfaces):
        covered_bad.append({"id": "decline_branch", "line": None})
    missing_bad = []
    for r in required_bad_cases:
        if not any(c.get("id") == r["id"] for c in covered_bad):
            missing_bad.append(r)
    if required_bad_cases:
        adv_value = _safe_div(len(covered_bad), len(required_bad_cases))
    else:
        adv_value = None

    # Axis 3: doctrine_binding_quality (classified, not counted)
    observed = set(cp.get("observed_doctrine_bindings", []))
    expected = set(declared_at_birth or expected_doctrine_bindings or [])
    verified = sorted(observed & expected)
    claimed_only = sorted(expected - observed)
    missing_d = sorted([])  # would be filled if we resolved to actual binding sites
    contradicted: list[str] = []
    not_applicable = sorted(observed - expected)

    # Axis 4: evidence_integration
    e_refs = (birth.get("evidence_refs", []) or []) + (current.get("evidence_refs", []) or [])
    source_bound = sum(1 for e in e_refs if (e.get("kind") in {"commit", "ticket", "test", "report", "command", "ast_probe", "grep", "json_query", "schema", "file_span", "build_log", "git_query"}))
    deref = sum(1 for e in e_refs if not e.get("evidence_private"))
    private = sum(1 for e in e_refs if e.get("evidence_private"))
    unresolved = sum(1 for e in e_refs if not e.get("locator"))
    audit_route = "present" if rel_path.startswith(("reports/project_genealogy/", "project_genealogy/")) else (
        "present" if artifact_family in {"audit_report", "audit_instrument", "doctrine", "method"} else "absent"
    )

    # Axis 5: operational_load_bearingness
    imports_in = sum(1 for e in incoming_edges if e.get("edge_type") == "imports")
    imports_out = sum(1 for e in outgoing_edges if e.get("edge_type") == "imports")
    validators = sum(1 for e in incoming_edges if e.get("edge_type") == "validates")
    citations = sum(1 for e in incoming_edges if e.get("edge_type") == "cites")
    weight = (
        2.0 * imports_in
        + 0.5 * imports_out
        + 3.0 * validators
        + 1.5 * citations
    )

    return {
        "predicate_atom_coverage": {
            "claimable_atoms": claimable,
            "covered_atoms": covered,
            "missing_atoms": missing,
            "value": cov_value,
        },
        "adversarial_surface_coverage": {
            "required_bad_cases": required_bad_cases,
            "covered_bad_cases": covered_bad,
            "missing_bad_cases": missing_bad,
            "value": adv_value,
        },
        "doctrine_binding_quality": {
            "required": sorted(expected),
            "verified": verified,
            "claimed_only": claimed_only,
            "missing": missing_d,
            "contradicted": contradicted,
            "not_applicable": not_applicable,
        },
        "evidence_integration": {
            "source_bound_claims": source_bound,
            "dereferenceable_evidence_refs": deref,
            "private_evidence_refs": private,
            "unresolved_evidence_refs": unresolved,
            "audit_queue_or_falsifier_route": audit_route,
        },
        "operational_load_bearingness": {
            "imports_in": imports_in,
            "imports_out": imports_out,
            "generates_artifacts": [],
            "validated_by": [
                e["source"]
                for e in incoming_edges
                if e.get("edge_type") == "validates"
            ],
            "cited_by_reports": [
                e["source"]
                for e in incoming_edges
                if e.get("edge_type") == "cites"
            ],
            "weighted_value": round(weight, 4),
        },
    }
