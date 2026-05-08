# Dossier: `WAITING_TO_BE_PUBLISHED.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/2705399b44de_WAITING_TO_BE_PUBLISHED.md.json`
- JSON content_hash: `sha256:0a987bc727bf16f3764f5eb5abd351d2ff0a5152b362131e0978ec83fb6456f1`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 121 / Bytes: 9702

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.
- **header_declared_intent** — # Waiting to be Published
*Living log of the project's potential publishable artifacts. Each entry tracks what's there now, what tier it's at, and what's needed to move it up. Updated as campaigns close and as scope narrows toward write-up.*
*Last update: 2026-05-05 (after TASK-CB-003 close).*
---
## Tier definitions
- **Preprint ready** — could go up to arXiv / Zenodo / bioRxiv this week. No furt

## Current
- Status: `recovered`
- Observed doctrines: `D21, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D21', 'D7'], 'verified': ['D21', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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