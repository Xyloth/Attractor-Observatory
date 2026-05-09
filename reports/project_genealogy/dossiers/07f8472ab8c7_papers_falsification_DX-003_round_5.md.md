# Dossier: `papers/falsification/DX-003/round_5.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/07f8472ab8c7_papers_falsification_DX-003_round_5.md.json`
- JSON content_hash: `sha256:afbb4b47bd44b433f298beb9f3d7c3e6b73f4a09548643d096123d7776fd2e99`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `paper`
- Generated status: `source`
- Lines: 79 / Bytes: 5398

## Birth
- Status: `recovered`
- First-seen commit: `3bdd384806bce9a56cbc9fbfb513bd2ab1b07f12`
- First-seen date: `2026-05-08T18:08:20-04:00`
- Spawn ticket: `DX-003`
- Cohort: `DX-003`

### Birth predicate atoms
- **paper_artifact_in_falsifier_or_prereg** — Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.
- **header_declared_intent** — ﻿# DX-003 Round 5 - Control Room and Snapshot Truthfulness
round_id: DX-003-R5
attack_angle: I attacked the dashboard as a truth surface. The question was not whether Streamlit renders, but whether Control Room and Mission Control surfaces tell a fresh AI/human the same truth as the underlying repository state, especially for stale sidecars and PG-001's currentness.
elapsed_at_round_start: 00:22:3

## Current
- Status: `recovered`
- Observed doctrines: `D17, D22, D24, D29, D30, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D22', 'D24', 'D29', 'D30', 'D9'], 'verified': ['D17', 'D22', 'D24', 'D29', 'D30', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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