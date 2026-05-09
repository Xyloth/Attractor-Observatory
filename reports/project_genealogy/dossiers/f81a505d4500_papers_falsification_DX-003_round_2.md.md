# Dossier: `papers/falsification/DX-003/round_2.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/f81a505d4500_papers_falsification_DX-003_round_2.md.json`
- JSON content_hash: `sha256:911c3b46644e930f6b37a27b9d581be4e8c1152338c5d4abf12a1ef6ea9af8cb`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `paper`
- Generated status: `source`
- Lines: 106 / Bytes: 6933

## Birth
- Status: `recovered`
- First-seen commit: `844cabcdf62eab71eec5a894c36b18b11204c102`
- First-seen date: `2026-05-08T17:55:16-04:00`
- Spawn ticket: `DX-003`
- Cohort: `DX-003`

### Birth predicate atoms
- **paper_artifact_in_falsifier_or_prereg** — Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.
- **header_declared_intent** — ﻿# DX-003 Round 2 - Project Genealogy Self-Map Collision
round_id: DX-003-R2
attack_angle: I attacked PG-001 as a self-map of the project rather than as another report. The core question was whether the genealogy atlas and coherence report are actually bound to consolidated main and whether they audit the surfaces introduced by PG-001/CB-020/CB-021, or whether the self-map excludes the newest terr

## Current
- Status: `recovered`
- Observed doctrines: `D17, D17.5, D29, D30, D31, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D17.5', 'D29', 'D30', 'D31', 'D9'], 'verified': ['D17', 'D17.5', 'D29', 'D30', 'D31', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 1
- Letter-vs-spirit surfaces: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/falsification/DX-003/round_2.md-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 43: print(len([p for p in missing if not p.startswith('papers/falsification/DX-003/')]))
- **PG-papers/falsification/DX-003/round_2.md-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 44: print('\n'.join([p for p in missing if not p.startswith('papers/falsification/DX-003/')][:25]))

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.