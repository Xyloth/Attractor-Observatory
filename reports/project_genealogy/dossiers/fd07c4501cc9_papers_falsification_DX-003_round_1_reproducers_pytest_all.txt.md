# Dossier: `papers/falsification/DX-003/round_1_reproducers/pytest_all.txt`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/fd07c4501cc9_papers_falsification_DX-003_round_1_reproducers_pytest_all.txt.json`
- JSON content_hash: `sha256:fee70bbe5fdf9014bde42097e207bdb81eb8c4a33abba4d475557cd2da64131c`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `paper`
- Generated status: `source`
- Lines: 87 / Bytes: 5744

## Birth
- Status: `recovered`
- First-seen commit: `42118fd96d37ba847675096ee38ca5aa768b06ac`
- First-seen date: `2026-05-08T17:48:00-04:00`
- Spawn ticket: `DX-003`
- Cohort: `DX-003`

### Birth predicate atoms
- **paper_artifact_in_falsifier_or_prereg** — Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D18'], 'verified': [], 'claimed_only': ['D17', 'D18'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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