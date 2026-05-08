# Dossier: `ai_os/memory/model_calibration_report.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/efd8ce195042_ai_os_memory_model_calibration_report.md.json`
- JSON content_hash: `sha256:99590f91506810307297957c06f76ba118be36ef45d3fddd86068d630d4dd39f`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `ai_os`
- Generated status: `source`
- Lines: 115 / Bytes: 5897

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **ai_os_state_recorded** — ai_os/ artifact records cross-builder state, decision logs, or memory in a machine-readable form.
- **header_declared_intent** — # Model Calibration Report
Running summary of Estimation Calibration Loop outcomes.
## Entry Schema
```text
date:
author_or_model:
spec_version:
model_name:
task_class:
record_window:
median_estimation_delta:
median_scope_delta:
calibration_status:
why_it_matters:
counterargument:
next_action:
linked_artifacts:
```
## Entries
### 2026-05-01 - TASK-001..TASK-003 Baseline
```text
date: 2026-05-01
au

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11'], 'verified': [], 'claimed_only': ['D11'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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