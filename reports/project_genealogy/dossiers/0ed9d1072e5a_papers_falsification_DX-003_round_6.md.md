# Dossier: `papers/falsification/DX-003/round_6.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/0ed9d1072e5a_papers_falsification_DX-003_round_6.md.json`
- JSON content_hash: `sha256:b55d1d2d3a81c37f880fd4be3a0546ebf02b17615cf9cd46e7b198eb9ea54545`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `paper`
- Generated status: `source`
- Lines: 112 / Bytes: 7184

## Birth
- Status: `recovered`
- First-seen commit: `1a6d92a153cad0458e97738cdae31e23566f6fc2`
- First-seen date: `2026-05-08T18:14:42-04:00`
- Spawn ticket: `DX-003`
- Cohort: `DX-003`

### Birth predicate atoms
- **paper_artifact_in_falsifier_or_prereg** — Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.
- **header_declared_intent** — ﻿# DX-003 Round 6 - External Identifier Reality Collision
round_id: 6
attack_angle: I treated the project's external citations as reality anchors rather than internal tokens. This round asked whether MotifContract.v2's `empirically_positive_worlds` citations resolve against live external registries, whether the resolved titles support the world/motif labels they are used for, and whether campaign

## Current
- Status: `recovered`
- Observed doctrines: `D17, D23, D26, D29`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D23', 'D26', 'D29'], 'verified': ['D17', 'D23', 'D26', 'D29'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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