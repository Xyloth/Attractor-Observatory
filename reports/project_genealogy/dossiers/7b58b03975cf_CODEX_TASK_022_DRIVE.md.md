# Dossier: `CODEX_TASK_022_DRIVE.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/7b58b03975cf_CODEX_TASK_022_DRIVE.md.json`
- JSON content_hash: `sha256:b6bbfe04e22ee8dd331a736db09044327b3cc9fe1ab69b9f3a25c3ac80d54dcd`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 247 / Bytes: 30239

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.
- **header_declared_intent** — # Codex — TASK-022: Campaign 011, Build the Factory
*Architect message. Read in full before resuming. Canon for the duration of TASK-022.*
---
## 1. Where you stand
TASK-021 closed Campaign 010 cleanly. 24/24 gates green, the lens registry expanded from 3 to 8, the Formal Deficit Map landed with one honest candidate (`motif.floor_connectivity.draft`, formal_gap 0.308, attractor_strength 0.9, best_

## Current
- Status: `recovered`
- Observed doctrines: `D14, D17.5, D18, D19, D20, D21, D7, D8, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D7', 'D8', 'D9'], 'verified': ['D14', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D7', 'D8', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.