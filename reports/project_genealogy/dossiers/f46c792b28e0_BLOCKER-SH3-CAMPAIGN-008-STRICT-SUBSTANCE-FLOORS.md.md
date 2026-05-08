# Dossier: `BLOCKER-SH3-CAMPAIGN-008-STRICT-SUBSTANCE-FLOORS.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/f46c792b28e0_BLOCKER-SH3-CAMPAIGN-008-STRICT-SUBSTANCE-FLOORS.md.json`
- JSON content_hash: `sha256:6983ff0b6e6759a2c2ec49d509427850770bee5d347f21bc2da6e0653178c872`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 85 / Bytes: 3662

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.
- **header_declared_intent** — # BLOCKER-SH3: Campaign 008 Strict Substance Floors
Status: closed
Campaign: Campaign 008
Blocking gates: SH3, W6R, W7R, W8R, W9R, W10R, W11R, W12R, W13R
Resolution: D17.5 substance audits plus W8/W11/W12/W13 deepening
## Summary
Campaign 008 behavior gates, causal controls, invariants, D14 lint, K3-K10 calibration, CLI generation, and full regression are green. I am not claiming Campaign 008 comp

## Current
- Status: `recovered`
- Observed doctrines: `D14, D17.5`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17.5'], 'verified': ['D14', 'D17.5'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-BLOCKER-SH3-CAMPAIGN-008-STRICT-SUBSTANCE-FLOORS.md-class-0** (low, hypothesis): Detected pattern matching Class3 (soft enforcement comments) at line 12

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.