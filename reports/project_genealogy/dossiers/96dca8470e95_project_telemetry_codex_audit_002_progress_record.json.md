# Dossier: `project_telemetry/codex_audit_002_progress_record.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/96dca8470e95_project_telemetry_codex_audit_002_progress_record.json.json`
- JSON content_hash: `sha256:eaa977b5881ed9490fdac59055326bc9c0c189f6f046c343119707a6a525a4fb`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `telemetry`
- Generated status: `source`
- Lines: 42 / Bytes: 3329

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **telemetry_record_appended** — File appends a telemetry record under a stable schema.
- **header_declared_intent** — {
"task_id": "CODEX_AUDIT_002",
"task_class": "audit",
"model_name": "Codex",
"model_version": "gpt-5",
"scope_score": 5,
"complexity_score": 6,
"estimated_minutes": 55,
"estimated_files": 3,
"estimated_tests": 0,
"actual_minutes": null,
"actual_files": 6,
"actual_tests": 0,
"acceptance_outcome": "partial_signoff_with_blocker",
"calibration_method": "Reference class: CODEX_AUDIT_001 took a bounded

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