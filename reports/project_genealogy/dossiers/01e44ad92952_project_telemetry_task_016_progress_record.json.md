# Dossier: `project_telemetry/task_016_progress_record.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/01e44ad92952_project_telemetry_task_016_progress_record.json.json`
- JSON content_hash: `sha256:33a8c154936bccd9b28534825c23c9cc23a803c842b7437c26de8aad43a3b3eb`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `telemetry`
- Generated status: `source`
- Lines: 71 / Bytes: 3747

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **telemetry_record_appended** — File appends a telemetry record under a stable schema.
- **header_declared_intent** — {
"acceptance_outcome": "deferred",
"actual_files": 31,
"actual_minutes": 48.583333333333336,
"actual_tests": 184,
"complexity_score": 10,
"estimated_files": 120,
"estimated_minutes": 180,
"estimated_tests": 120,
"estimation_delta": 0.26990740740740743,
"expansions_planned": [
"Continue Campaign 007 under D7-D13: no toys, no number-generator corpora, no hardcoded science, and gates as measurements

## Current
- Status: `recovered`
- Observed doctrines: `D11, D13, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D13', 'D7'], 'verified': ['D11', 'D13', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.