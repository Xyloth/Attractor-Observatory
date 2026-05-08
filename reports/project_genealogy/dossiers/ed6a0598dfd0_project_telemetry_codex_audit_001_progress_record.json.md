# Dossier: `project_telemetry/codex_audit_001_progress_record.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/ed6a0598dfd0_project_telemetry_codex_audit_001_progress_record.json.json`
- JSON content_hash: `sha256:d11ffcb15630c5a88888f4f5d32de9a53c24d431720e9c0d94d4127dfeaaa858`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `telemetry`
- Generated status: `source`
- Lines: 39 / Bytes: 3414

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
"actual_files": 6,
"actual_minutes": null,
"actual_tests": 0,
"calibration_method": "Reference class: bounded code-review/audit task, not a build campaign. Closest prior shapes are design/audit slices in the 15-35 minute range, plus TASK-024 verification work where the relevant harness and reports are already in place. Estimate formula: 10 min required reading + 15

## Current
- Status: `recovered`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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