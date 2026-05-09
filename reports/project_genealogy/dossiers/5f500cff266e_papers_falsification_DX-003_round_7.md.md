# Dossier: `papers/falsification/DX-003/round_7.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/5f500cff266e_papers_falsification_DX-003_round_7.md.json`
- JSON content_hash: `sha256:83ef15cc49bf58055847df39a62aeda75085267588b29c0c937de2e37bef4b02`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `paper`
- Generated status: `source`
- Lines: 120 / Bytes: 6721

## Birth
- Status: `recovered`
- First-seen commit: `a434ca4f20e84c1af1a60954ab5d4ace4a5772d3`
- First-seen date: `2026-05-08T18:19:27-04:00`
- Spawn ticket: `DX-003`
- Cohort: `DX-003`

### Birth predicate atoms
- **paper_artifact_in_falsifier_or_prereg** — Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.
- **header_declared_intent** — ﻿# DX-003 Round 7 - Identity And Telemetry Accounting Collision
round_id: 7
attack_angle: I attacked the project's self-accounting layer: the Estimation Loop ledger, README claims about builder identities and task counts, the public telemetry contract test, BUILD_LOG mention coverage, and the Control Room AI Operations Tower. The question was whether the project can honestly answer who did what an

## Current
- Status: `recovered`
- Observed doctrines: `D17, D25, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D25', 'D9'], 'verified': ['D17', 'D25', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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