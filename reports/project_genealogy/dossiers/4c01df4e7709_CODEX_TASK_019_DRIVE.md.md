# Dossier: `CODEX_TASK_019_DRIVE.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/4c01df4e7709_CODEX_TASK_019_DRIVE.md.json`
- JSON content_hash: `sha256:32dc738f4bc575521155c8b608eaaa986aa32245b8caf35c3740dcab6ebdcae4`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 218 / Bytes: 21374

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.
- **header_declared_intent** — # Codex — TASK-019: Close Campaign 008 + Queue Campaign 009
*Architect message. Read in full before resuming. Canon for the duration of TASK-019.*
---
## 1. Where you stand
Two campaigns since the last audit: TASK-017 (41m45s) excised the W3/W4/W5 hardcodes; TASK-018 (1h24m2s) shipped Campaign 008 substantive-thin worlds W6–W13 plus trace-backed K3–K10 calibration plus an honest BLOCKER-SH3 refusi

## Current
- Status: `recovered`
- Observed doctrines: `D14, D17, D17.5, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17', 'D17.5', 'D7'], 'verified': ['D14', 'D17', 'D17.5', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-CODEX_TASK_019_DRIVE.md-class-0** (low, hypothesis): Detected pattern matching Class3 (soft enforcement comments) at line 9
- **PG-CODEX_TASK_019_DRIVE.md-class-1** (low, hypothesis): Detected pattern matching Class4 (scenario-internal benchmark branching) at line 15
- **PG-CODEX_TASK_019_DRIVE.md-class-2** (low, hypothesis): Detected pattern matching Class3 (soft enforcement comments) at line 27
- **PG-CODEX_TASK_019_DRIVE.md-class-3** (low, hypothesis): Detected pattern matching Class3 (soft enforcement comments) at line 159

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.