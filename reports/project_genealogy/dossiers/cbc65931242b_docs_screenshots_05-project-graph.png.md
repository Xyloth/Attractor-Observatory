# Dossier: `docs/screenshots/05-project-graph.png`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/cbc65931242b_docs_screenshots_05-project-graph.png.json`
- JSON content_hash: `sha256:f928c4733dfbed2bf381e74c50952ba9d3d05eb0805c33d5a3fd9195f26915d2`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `docs`
- Generated status: `source`
- Lines: 2742 / Bytes: 882873

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
- Observed doctrines: `D2, D3, D4, D6, D7, D8, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D2', 'D3', 'D4', 'D6', 'D7', 'D8', 'D9'], 'verified': ['D2', 'D3', 'D4', 'D6', 'D7', 'D8', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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