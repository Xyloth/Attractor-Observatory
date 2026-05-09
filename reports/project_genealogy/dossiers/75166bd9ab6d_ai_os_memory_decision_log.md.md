# Dossier: `ai_os/memory/decision_log.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/75166bd9ab6d_ai_os_memory_decision_log.md.json`
- JSON content_hash: `sha256:7bba86eb7abfcac66a5ffd54ca0c98eaef33f96543940be2609cf0e9fccee301`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `ai_os`
- Generated status: `source`
- Lines: 87 / Bytes: 9721

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **ai_os_state_recorded** — ai_os/ artifact records cross-builder state, decision logs, or memory in a machine-readable form.
- **header_declared_intent** — # Decision Log
Research Memory Ledger index of decisions that affect project direction,
contracts, claims, or operating doctrine.
## Entry Schema
```text
date:
author_or_model:
spec_version:
decision:
why_it_matters:
status:
evidence:
counterargument:
next_action:
linked_artifacts:
```
## Entries
date: 2026-05-02
author_or_model: Codex Builder
spec_version: v1.2 + D17.5
decision: Campaign 009 shou

## Current
- Status: `recovered`
- Observed doctrines: `D15, D17.5, D18, D19, D21, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D15', 'D17.5', 'D18', 'D19', 'D21', 'D7'], 'verified': ['D15', 'D17.5', 'D18', 'D19', 'D21', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
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