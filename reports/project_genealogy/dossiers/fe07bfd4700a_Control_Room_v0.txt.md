# Dossier: `Control Room v0.txt`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/fe07bfd4700a_Control_Room_v0.txt.json`
- JSON content_hash: `sha256:f2a5b1e6fa736cbbea6e92d06216d3afeabcbd54325b85451a4c177e087b908e`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 1215 / Bytes: 28784

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.

## Current
- Status: `recovered`
- Observed doctrines: `D18, D19`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D18', 'D19'], 'verified': ['D18', 'D19'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-Control Room v0.txt-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 795
- **PG-Control Room v0.txt-class-1** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 1195

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.