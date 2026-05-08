# Dossier: `docs/doctrine_d23.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/38ecc97bbf96_docs_doctrine_d23.md.json`
- JSON content_hash: `sha256:25b4d9c38ffb2d698c3c32d09eeef287c90f9d2ebc4c6f54394f5f5506f06cf5`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `doctrine`
- Generated status: `source`
- Lines: 34 / Bytes: 1417

## Birth
- Status: `recovered`
- First-seen commit: `ff7a2adff3a2bcf5dbddec8e613b3a17dc69edfd`
- First-seen date: `2026-05-06T14:39:23-04:00`
- Spawn ticket: `TASK-033`
- Cohort: `TASK-033`

### Birth predicate atoms
- **binding_rule_named** — Document declares a binding doctrine rule with a numbered ID and ratification.
- **header_declared_intent** — # Doctrine D23 - Dereferenceable Evidence or Explicit Private Boundary
Mode: foundational
Signed-by: Codex 1.5x (TASK-033, ratifying TASK-032 candidate)
D23 - Every artifact path used as evidence resolves in the shipped surface or
carries an explicit machine-readable private/unshipped marker at point of use.
## Failure mode caught
DX-001 found public reports whose evidence paths pointed into gitig

## Current
- Status: `recovered`
- Observed doctrines: `D23`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D23'], 'verified': ['D23'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
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
- **PG-docs/doctrine_d23.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.