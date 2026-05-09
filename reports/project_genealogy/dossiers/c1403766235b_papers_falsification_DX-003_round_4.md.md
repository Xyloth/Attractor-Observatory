# Dossier: `papers/falsification/DX-003/round_4.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/c1403766235b_papers_falsification_DX-003_round_4.md.json`
- JSON content_hash: `sha256:170106c7501dfa18aaa3f21a27ba6ec6c068a7529ce83210463fe87c44c9a6b2`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `paper`
- Generated status: `source`
- Lines: 87 / Bytes: 4984

## Birth
- Status: `recovered`
- First-seen commit: `9240e0e2b5cb9eb9f7827edc57a7ffd2a95986c8`
- First-seen date: `2026-05-08T18:04:47-04:00`
- Spawn ticket: `DX-003`
- Cohort: `DX-003`

### Birth predicate atoms
- **paper_artifact_in_falsifier_or_prereg** — Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.
- **header_declared_intent** — ﻿# DX-003 Round 4 - Evidence Dereferenceability and Private-Boundary Marking
round_id: DX-003-R4
attack_angle: I attacked evidence as dereferenceable substrate. Instead of asking whether reports parse or tests pass, I scanned structured artifacts for path-bearing fields and checked whether the referenced files actually exist from the consolidated branch state, distinguishing private-marked absence

## Current
- Status: `recovered`
- Observed doctrines: `D11, D17, D29, D30, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D17', 'D29', 'D30', 'D9'], 'verified': ['D11', 'D17', 'D29', 'D30', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
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