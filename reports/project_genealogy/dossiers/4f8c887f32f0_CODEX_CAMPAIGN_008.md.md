# Dossier: `CODEX_CAMPAIGN_008.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/4f8c887f32f0_CODEX_CAMPAIGN_008.md.json`
- JSON content_hash: `sha256:8df0cac5d53016d8b7a47ad8e0b9f1c0e90a819025ffc7e5556d70b2f1d8bb74`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 402 / Bytes: 19398

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.
- **header_declared_intent** — # CODEX CAMPAIGN 008: Load-Bearing Substrate Completion
Status: ready for Builder implementation
Spec base: Attractor Observatory v1.2
Depends on: Campaign 007 Truth Pass, W3R-W5R, HE1-HE9, D14
Primary task class: integration
Recommended first implementation estimate: 75-120 minutes for the first large vertical; continue until gates are green or blockers are written
## 1. Why This Campaign Is Next

## Current
- Status: `recovered`
- Observed doctrines: `D14, D15, D16, D17, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D15', 'D16', 'D17', 'D7'], 'verified': ['D14', 'D15', 'D16', 'D17', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-CODEX_CAMPAIGN_008.md-class-0** (low, hypothesis): Detected pattern matching Class4 (scenario-internal benchmark branching) at line 377

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.