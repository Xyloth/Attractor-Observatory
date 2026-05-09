# Dossier: `docs/screenshots/02-world-observatory.png`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/7e035bded111_docs_screenshots_02-world-observatory.png.json`
- JSON content_hash: `sha256:5bd51ebd8ea2f4faee5d6f0aaf2689e0a2ef8d7c74831a75f6c65394691d9ac9`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `docs`
- Generated status: `source`
- Lines: 3434 / Bytes: 1006940

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **doc_serves_handbook** — Doc serves the project handbook (doctrine support, methodology, audit notes).

## Current
- Status: `recovered`
- Observed doctrines: `D0, D1, D13, D2, D3, D4, D46, D5, D51, D6, D7, D9, D۳`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D0', 'D1', 'D13', 'D2', 'D3', 'D4', 'D46', 'D5', 'D51', 'D6', 'D7', 'D9', 'D۳'], 'verified': ['D0', 'D1', 'D13', 'D2', 'D3', 'D4', 'D46', 'D5', 'D51', 'D6', 'D7', 'D9', 'D۳'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['Control_Room_README.md', 'README.md', 'reports/task_032_dx001_disposition.json'], 'weighted_value': 4.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.