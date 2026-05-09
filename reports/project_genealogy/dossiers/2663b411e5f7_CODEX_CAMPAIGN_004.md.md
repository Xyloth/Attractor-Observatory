# Dossier: `CODEX_CAMPAIGN_004.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/2663b411e5f7_CODEX_CAMPAIGN_004.md.json`
- JSON content_hash: `sha256:b5ed8d2a0bc9654bea00d26ac9d8f3a41fc3d78b80510e6a1e8918d200413063`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 110 / Bytes: 4422

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.
- **header_declared_intent** — # CODEX Campaign 004: Discovery, Calibration, and Negative-Space Engine
## Doctrine
This campaign treats v1.2 as the floor. It does not end at a coherent
narrative. It ends when every gate below is evaluated with generated artifacts
and either green or escalated as a named blocker.
No partial/foundation-slice exit is available for TASK-011.
## Scientific Questions
1. Can the named but incomplete K

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': [], 'verified': [], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-CODEX_CAMPAIGN_004.md-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 14
- **PG-CODEX_CAMPAIGN_004.md-class-1** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 102

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.