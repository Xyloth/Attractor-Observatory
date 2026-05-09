# Dossier: `papers/prereg/bfg_v0.signed.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/6056334b3c18_papers_prereg_bfg_v0.signed.json.json`
- JSON content_hash: `sha256:959a04e0fee48bd7f433e0d61aa7d460ddc1c11857a02eeaa13b8aabba3dd3c8`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `prereg`
- Generated status: `source`
- Lines: 215 / Bytes: 7226

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **prereg_locks_instruments** — Prereg artifact locks basis/lens instruments with a content_hash.
- **header_declared_intent** — {
"campaign_id": "campaign-009",
"equivalence_basis": {
"abstention_rules": {
"abstain_on_basis_hash_mismatch": true,
"abstain_on_missing_prereg_hash": true,
"min_event_diversity_for_positive": 2,
"min_invariant_strength": 0.5,
"min_trace_states": 2
},
"distance_metric_family": {
"cognitive": "task-blind representation/state vector + event-surface distance",
"crn": "catalytic dependency graph edit

## Current
- Status: `recovered`
- Observed doctrines: `D23, D29`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D23', 'D29'], 'verified': ['D23', 'D29'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md', 'CODEX_TASK_020_DRIVE.md', 'reports/campaign_009/bfg_preregistration_gate.json', 'reports/campaign_009/cli_full_report.json', 'reports/campaign_009/full_report.json', 'reports/campaign_009/provenance_graph.json', 'reports/campaign_009/regression_verification.json', 'reports/task_cb022_evidence_discipline/path_reference_markers.json'], 'weighted_value': 12.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/prereg/bfg_v0.signed.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.