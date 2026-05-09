# Dossier: `CODEX_TASK_021_DRIVE.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/e9f08195ffd1_CODEX_TASK_021_DRIVE.md.json`
- JSON content_hash: `sha256:1eb8f3cd44f72ee8a8a72345750b9dc4eccbac66ba89b6ad32438932e400fc5f`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 158 / Bytes: 24452

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.
- **header_declared_intent** — # Codex — TASK-021: Campaign 010, Formal Deficit Map + Substrate Truth Pass
*Architect message. Read in full before resuming. Canon for the duration of TASK-021.*
---
## 1. Where you stand
TASK-020 closed Campaign 009 cleanly. 13/13 gates green, BFG-PR (D18) genuinely content-locked before runs, KF1–KF4 world-driven with `forbidden_payload_reads: []`, the floor detector reading traces under substr

## Current
- Status: `recovered`
- Observed doctrines: `D14, D15, D17, D18, D19, D7, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D15', 'D17', 'D18', 'D19', 'D7', 'D9'], 'verified': ['D14', 'D15', 'D17', 'D18', 'D19', 'D7', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-CODEX_TASK_021_DRIVE.md-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 67
- **PG-CODEX_TASK_021_DRIVE.md-class-1** (low, hypothesis): Detected pattern matching Class6 (engineered prediction polynomial) at line 124

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.