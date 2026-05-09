# Dossier: `CODEX_TASK_009_DRIVE.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/5503c65bed17_CODEX_TASK_009_DRIVE.md.json`
- JSON content_hash: `sha256:2e165c54c37e59f550f1c199e910b983725d81bc76d24dfa71f298802fbd88de`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 393 / Bytes: 29545

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.
- **header_declared_intent** — # Codex — TASK-009: Drive Campaign 002 from G3 through G20
*Architect message. Read in full before resuming. Canon for the duration of TASK-009.*
---
## 1. Where you stand
TASK-008 actuals are now in the ledger: 13m45s wall-clock, estimation_delta 0.0229, gates evaluated 5/20.
The work you did in those 13 minutes was real, and it is worth saying so before the rest of this message lands:
- `worlds/

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': [], 'verified': [], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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