# Dossier: `project_telemetry/task_024_progress_record.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/e09180baeb5b_project_telemetry_task_024_progress_record.json.json`
- JSON content_hash: `sha256:c494e33a8123015a97d4d541bb041856b26ba01f5340587781a2ce9c4d4480c9`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `telemetry`
- Generated status: `source`
- Lines: 79 / Bytes: 4053

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **telemetry_record_appended** — File appends a telemetry record under a stable schema.
- **header_declared_intent** — {
"acceptance_outcome": "pass",
"actual_files": 34,
"actual_minutes": null,
"actual_tests": 265,
"complexity_score": 8,
"estimated_files": 40,
"estimated_minutes": 70,
"estimated_tests": 260,
"estimation_delta": null,
"execution_context": {
"speed_mode": "regular",
"advertised_speedup": 1.0,
"quality_gate_policy": "unchanged",
"note": "PI supplied TASK-023 actual at 25m54s and regular speed remain

## Current
- Status: `recovered`
- Observed doctrines: `D14, D17.5, D18, D19, D20, D21`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17.5', 'D18', 'D19', 'D20', 'D21'], 'verified': ['D14', 'D17.5', 'D18', 'D19', 'D20', 'D21'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

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