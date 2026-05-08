"""Drift detection — atom diff between birth and current predicates.

Drift statuses (per spec):

* none
* positive_deepening
* neutral_refactor
* review_required
* bad_drift
* honest_decline
"""

from __future__ import annotations

from typing import Any


def _atom_ids(atoms: list[dict[str, Any]]) -> set[str]:
    return {a.get("atom_id") for a in atoms if a.get("atom_id")}


def assess_drift(
    birth: dict[str, Any],
    current: dict[str, Any],
    threshold_policy: dict[str, Any],
    artifact_family: str = "",
) -> dict[str, Any]:
    """Return the drift_assessment block."""
    if birth.get("status") != "recovered" or current.get("status") != "recovered":
        return {
            "status": "honest_decline",
            "missing_birth_atoms": [],
            "changed_atoms": [],
            "new_atoms": [],
            "doctrine_boundary_crossings": [],
            "letter_vs_spirit_flags": [],
            "negative_space_flags": [],
            "reproducer_refs": [],
            "decline_reason": (
                birth.get("decline_reason")
                or current.get("decline_reason")
                or "predicate_not_recoverable"
            ),
        }

    birth_atoms = birth.get("birth_predicate", {}).get("atoms", [])
    current_atoms = current.get("current_predicate", {}).get("atoms", [])
    birth_ids = _atom_ids(birth_atoms)
    current_ids = _atom_ids(current_atoms)

    # Atom-level matching: a birth atom counts as served if the current
    # predicate carries an atom whose source_ref.kind matches one of the
    # birth atom's `acceptance_evidence_expected[*].kind`. Atom IDs differ
    # between birth seeds (family-specific intent) and current extraction
    # (mechanical surface kinds), so kind-matching is the canonical
    # comparison; pure ID-set diff would over-flag drift.
    current_kinds = {
        (a.get("source_ref") or {}).get("kind", "")
        for a in current_atoms
    }
    current_kinds.discard("")

    missing: list[str] = []
    for atom in birth_atoms:
        atom_id = atom.get("atom_id", "")
        if not atom_id:
            continue
        expected = atom.get("acceptance_evidence_expected", [])
        if expected:
            kinds = {ev.get("kind", "") for ev in expected}
            kinds.discard("")
            served = bool(kinds & current_kinds) or atom_id in current_ids
        else:
            # No specific selector — served if any current atom exists.
            served = bool(current_atoms) or atom_id in current_ids
        if not served:
            missing.append(atom_id)

    # New: current atom IDs not present at birth.
    new = sorted(current_ids - birth_ids)
    missing = sorted(missing)

    # Letter-vs-spirit flags (one per surface).
    cp = current.get("current_predicate", {})
    surfaces = cp.get("letter_vs_spirit_surfaces", [])
    lvs_flags = [
        {
            "kind": "letter_coupled_surface",
            "line": surf.get("line"),
            "snippet": surf.get("snippet"),
            "pattern": surf.get("pattern"),
            "reproducer": {
                "kind": "grep",
                "command": f'rg "{surf.get("pattern", "")}" -n',
                "expected_result": "matches at line(s) listed",
                "last_run_status": "not_run",
            },
        }
        for surf in surfaces
    ]

    # Doctrine boundary crossings: required doctrines from birth not in current.
    expected_d = set(birth.get("birth_predicate", {}).get("expected_doctrine_bindings", []))
    observed_d = set(cp.get("observed_doctrine_bindings", []))
    missing_doctrines = sorted(expected_d - observed_d)
    boundary_crossings = [
        {
            "doctrine_id": d,
            "kind": "missing_required_doctrine_binding",
            "evidence_ref": {
                "ref_id": f"doctrine::{d}::missing",
                "kind": "grep",
                "locator": f"absent doctrine binding {d}",
                "content_hash": "",
                "evidence_private": False,
                "note": "expected at birth, absent in current observation",
            },
        }
        for d in missing_doctrines
    ]

    negative_space_flags: list[dict[str, Any]] = []
    if missing:
        negative_space_flags.append({
            "kind": "missing_birth_atoms",
            "atom_ids": list(missing),
            "note": "atoms promised at birth absent from current predicate",
        })

    drift_thresh = threshold_policy.get("drift", {})
    bad_count = drift_thresh.get("missing_birth_atom_count_for_bad", 2)
    review_count = drift_thresh.get("missing_birth_atom_count_for_review", 1)
    boundary_for_bad = drift_thresh.get("doctrine_boundary_crossing_for_bad", 2)
    drift_critical_families = set(
        drift_thresh.get("drift_critical_families", [])
    )

    # Doctrine boundary crossings only drive bad_drift / review_required
    # for families where doctrine binding is load-bearing. For other
    # families (memory logs, atlas pages, telemetry records), boundary
    # crossings are recorded as drift evidence but downgraded to info
    # findings rather than bad_drift drivers.
    boundary_drives_status = artifact_family in drift_critical_families
    boundary_count = len(boundary_crossings) if boundary_drives_status else 0

    # Letter-vs-spirit surfaces are recorded as flags in the dossier
    # regardless of drift status. They drive review_required only when
    # multiple surfaces are present in a critical-family file (single
    # try/except or one regex gate is normal defensive code, not drift).
    lvs_drives_status = (
        artifact_family in drift_critical_families
        and len(lvs_flags) >= 3
    )

    if not missing and not new and not lvs_flags and not boundary_crossings:
        status = "none"
    elif boundary_count >= boundary_for_bad and missing:
        status = "bad_drift"
    elif len(missing) >= bad_count:
        status = "bad_drift"
    elif len(missing) >= review_count or lvs_drives_status or boundary_count:
        status = "review_required"
    elif new and not missing:
        status = "positive_deepening"
    else:
        status = "neutral_refactor"

    reproducer_refs = []
    if missing or boundary_crossings:
        reproducer_refs.append({
            "ref_id": "drift::atom_diff",
            "kind": "json_query",
            "locator": "$.drift_assessment.missing_birth_atoms",
            "content_hash": "",
            "evidence_private": False,
            "note": "atom diff stored in this dossier",
        })

    return {
        "status": status,
        "missing_birth_atoms": list(missing),
        "changed_atoms": [],
        "new_atoms": list(new),
        "doctrine_boundary_crossings": boundary_crossings,
        "letter_vs_spirit_flags": lvs_flags,
        "negative_space_flags": negative_space_flags,
        "reproducer_refs": reproducer_refs,
    }
