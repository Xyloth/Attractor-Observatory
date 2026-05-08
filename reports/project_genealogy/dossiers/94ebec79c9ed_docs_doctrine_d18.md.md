# Dossier: `docs/doctrine_d18.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/94ebec79c9ed_docs_doctrine_d18.md.json`
- JSON content_hash: `sha256:d720d610627621dfc511289df7992ba594b0c2b718934fb5d9474e557ec111d0`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `doctrine`
- Generated status: `source`
- Lines: 18 / Bytes: 765

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **binding_rule_named** — Document declares a binding doctrine rule with a numbered ID and ratification.
- **header_declared_intent** — # Doctrine D18: No Equivalence-Basis Drift
Mode: foundational
Signed-by: Codex Builder
Source: TASK-020 / Campaign 009
The invariant basis, substrate-erasure projection family, distance-metric family,
perturbation magnitude policy, and abstention rules used by a floor detector
must be content-hash-locked in a pre-registration record before any detection
run is scheduled against any non-calibration

## Current
- Status: `recovered`
- Observed doctrines: `D18`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D18'], 'verified': ['D18'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['docs/doctrine_registry.json'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-docs/doctrine_d18.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.