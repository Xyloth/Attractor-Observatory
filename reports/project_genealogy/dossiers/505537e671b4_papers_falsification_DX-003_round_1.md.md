# Dossier: `papers/falsification/DX-003/round_1.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/505537e671b4_papers_falsification_DX-003_round_1.md.json`
- JSON content_hash: `sha256:ad8d39f8426b98cc3707d3367714b6b77a8ccf07df8442efc9ae0bacae158513`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `paper`
- Generated status: `source`
- Lines: 111 / Bytes: 7484

## Birth
- Status: `recovered`
- First-seen commit: `42118fd96d37ba847675096ee38ca5aa768b06ac`
- First-seen date: `2026-05-08T17:48:00-04:00`
- Spawn ticket: `DX-003`
- Cohort: `DX-003`

### Birth predicate atoms
- **paper_artifact_in_falsifier_or_prereg** — Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.
- **header_declared_intent** — ﻿# DX-003 Round 1 - Executable Substrate and Worktree Reality
round_id: DX-003-R1
attack_angle: I attacked the consolidated instrument as an executable object rather than as a narrative repository: fresh branch from main, private setup script, all declared private directories, default test command, explicit public/private test commands, and targeted smoke tests for MotifContract and Control Room.

## Current
- Status: `recovered`
- Observed doctrines: `D17, D21, D22, D29, D30, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D21', 'D22', 'D29', 'D30', 'D9'], 'verified': ['D17', 'D21', 'D22', 'D29', 'D30', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

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