# Dossier: `papers/falsification/DX-003/round_9_reproducers/doctrine_catalog_drift_probe.txt`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/86de444dbe81_papers_falsification_DX-003_round_9_reproducers_doctrine_catalog_drift_probe.txt.json`
- JSON content_hash: `sha256:3589bc523fe0f927f9b89fe0065e11e2e6cda97992a68cf25cdbff83f3bf8de2`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `paper`
- Generated status: `source`
- Lines: 17 / Bytes: 1141

## Birth
- Status: `recovered`
- First-seen commit: `51403025f988031d7e5ddf07ce115bb9a6ebfc05`
- First-seen date: `2026-05-08T18:23:53-04:00`
- Spawn ticket: `DX-003`
- Cohort: `DX-003`

### Birth predicate atoms
- **paper_artifact_in_falsifier_or_prereg** — Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.

## Current
- Status: `recovered`
- Observed doctrines: `D22, D24, D25, D26, D27, D28, D29, D30, D31, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D22', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D7'], 'verified': ['D22', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.