# Dossier: `papers/falsification/DX-003/index.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/73188e58f1b8_papers_falsification_DX-003_index.md.json`
- JSON content_hash: `sha256:af905d7e08c7acb99e95048895cfb1d4558af46fa57b2de766052b2c93e6d0b8`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `paper`
- Generated status: `source`
- Lines: 97 / Bytes: 7071

## Birth
- Status: `recovered`
- First-seen commit: `8dc3566743af47675abe34a8a4b5b6d653f306fd`
- First-seen date: `2026-05-08T18:26:47-04:00`
- Spawn ticket: `DX-003`
- Cohort: `DX-003`

### Birth predicate atoms
- **paper_artifact_in_falsifier_or_prereg** — Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.
- **header_declared_intent** — ﻿# DX-003 Branch Falsification Bath Index
T_start_UTC: 2026-05-08T21:40:48.9304878Z
T_start_EST: 2026-05-08 17:40:48
T_end_UTC: 2026-05-08T22:26:03.6708377Z
T_end_EST: 2026-05-08 18:26:03
total_elapsed: 00:45:14.7403499
branch: falsification/dx-003-20260508T214003Z-4147aad
main_head_at_start: 4147aad
private_surface_verified: yes, 13/13 directories present after scripts/setup_worktree.bat
## Roll-

## Current
- Status: `recovered`
- Observed doctrines: `D26, D29, D31, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D26', 'D29', 'D31', 'D7'], 'verified': ['D26', 'D29', 'D31', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.