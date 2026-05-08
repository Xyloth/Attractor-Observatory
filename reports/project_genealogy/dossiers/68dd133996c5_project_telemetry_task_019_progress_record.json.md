# Dossier: `project_telemetry/task_019_progress_record.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/68dd133996c5_project_telemetry_task_019_progress_record.json.json`
- JSON content_hash: `sha256:230c6cd8fe61b4bab2f6a619915f0040123d8f7ac404bda8e9f5435148398b64`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `telemetry`
- Generated status: `source`
- Lines: 59 / Bytes: 2768

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **telemetry_record_appended** — File appends a telemetry record under a stable schema.
- **header_declared_intent** — {
"acceptance_outcome": "pass",
"actual_files": 24,
"actual_minutes": 53.96666666666667,
"actual_tests": 208,
"complexity_score": 10,
"estimated_files": 30,
"estimated_minutes": 60,
"estimated_tests": 210,
"estimation_delta": 0.8994444444444445,
"expansions_planned": [
"Close Campaign 008 honestly by deepening W8/W11/W12/W13 against v1.0 section 3 and using D17.5 audits where line floors diverge f

## Current
- Status: `recovered`
- Observed doctrines: `D17.5, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D17.5', 'D7'], 'verified': ['D17.5', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
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