# Dossier: `project_telemetry/task_018_progress_record.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/eeb55e5ed7da_project_telemetry_task_018_progress_record.json.json`
- JSON content_hash: `sha256:b1b582ddd60f9548f9178b2b3ed0a0fddc8db26dc07d43516608b50feaf13939`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `telemetry`
- Generated status: `source`
- Lines: 61 / Bytes: 3640

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
"actual_files": 19,
"actual_minutes": 84.03333333333333,
"actual_tests": 205,
"complexity_score": 10,
"estimated_files": 90,
"estimated_minutes": 90,
"estimated_tests": 250,
"estimation_delta": 0.9337037037037037,
"expansions_planned": [
"Implement CODEX_CAMPAIGN_008.md as the next foundation-first campaign.",
"Treat W6-W13 production substrate reconstruction an

## Current
- Status: `recovered`
- Observed doctrines: `D14, D17`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17'], 'verified': ['D14', 'D17'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-project_telemetry/task_018_progress_record.json-class-0** (low, hypothesis): Detected pattern matching Class3 (soft enforcement comments) at line 22
- **PG-project_telemetry/task_018_progress_record.json-class-1** (low, hypothesis): Detected pattern matching Class3 (soft enforcement comments) at line 31

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.