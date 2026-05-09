# Dossier: `papers/methods/MOTIF_CONTRACTS_v1_DRAFT.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/48307b7f168f_papers_methods_MOTIF_CONTRACTS_v1_DRAFT.md.json`
- JSON content_hash: `sha256:b7bccc08de7f4b1d1d7a946c7f40c1d5bfa34ed8d511ac4f61795afbd7866b1f`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 1047 / Bytes: 54257

## Birth
- Status: `recovered`
- First-seen commit: `b8473aa3ed840989f6dce967fc460df34c7eed60`
- First-seen date: `2026-05-06T19:23:03-04:00`
- Spawn ticket: `TASK-MOTIF-IMPL`
- Cohort: `TASK-MOTIF-IMPL`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — ﻿# Motif Contracts v1 Draft
Status: Codex 1.5x coauthor draft, pending PI + Architect consensus.
Mode: contract authoring only. No implementation in this task.
Origin: C020 methodology leak, where labels and lens features both depended on
`formalism.lens_registry._label_feature_for_motif`.
## Blind Spots Architect Missed
> **DX-002 public runtime boundary:** References to `formalism/*`, `trace/*`,

## Current
- Status: `recovered`
- Observed doctrines: `D26, D29`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D26', 'D29'], 'verified': ['D26', 'D29'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md', 'papers/methods/MOTIF_CONTRACT_SCHEMA_DRAFT.md'], 'weighted_value': 3.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/methods/MOTIF_CONTRACTS_v1_DRAFT.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.