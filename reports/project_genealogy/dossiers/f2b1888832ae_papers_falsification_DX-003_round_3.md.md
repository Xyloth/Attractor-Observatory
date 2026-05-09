# Dossier: `papers/falsification/DX-003/round_3.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/f2b1888832ae_papers_falsification_DX-003_round_3.md.json`
- JSON content_hash: `sha256:b781028e703ef19fe5d0f57a373f3af56d5e2c88baed25e9ac01a23f06f2d42e`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `paper`
- Generated status: `source`
- Lines: 94 / Bytes: 7025

## Birth
- Status: `recovered`
- First-seen commit: `2eb181f5b951c4a84b344468c7a366371058cb46`
- First-seen date: `2026-05-08T17:59:37-04:00`
- Spawn ticket: `DX-003`
- Cohort: `DX-003`

### Birth predicate atoms
- **paper_artifact_in_falsifier_or_prereg** — Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.
- **header_declared_intent** — ﻿# DX-003 Round 3 - Doctrine/Contract Violator Construction
round_id: DX-003-R3
attack_angle: I attacked D26/D27/D31 as operational tests, not as doctrine prose. The goal was to construct concrete violators that keep the current gates green: source-object aliases that evade exact matching, metadata-based predicates outside the four adversarial transforms, numeric value channels that survive key re

## Current
- Status: `recovered`
- Observed doctrines: `D11, D14, D17, D17.5, D26, D27, D31, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D14', 'D17', 'D17.5', 'D26', 'D27', 'D31', 'D9'], 'verified': ['D11', 'D14', 'D17', 'D17.5', 'D26', 'D27', 'D31', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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