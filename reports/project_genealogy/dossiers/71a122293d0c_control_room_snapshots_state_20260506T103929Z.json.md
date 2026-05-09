# Dossier: `control_room/snapshots/state_20260506T103929Z.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/71a122293d0c_control_room_snapshots_state_20260506T103929Z.json.json`
- JSON content_hash: `sha256:ffbb7a41acccaa2b4e2c676304eb981a6d1c57e4b0f78a3bde4c0c61c630d30a`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `generated`
- Lines: 504 / Bytes: 278883

## Birth
- Status: `recovered`
- First-seen commit: `ff7a2adff3a2bcf5dbddec8e613b3a17dc69edfd`
- First-seen date: `2026-05-06T14:39:23-04:00`
- Spawn ticket: `TASK-033`
- Cohort: `TASK-033`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — {
"calibration_trajectory": {
"by_model": {
"Claude (Builder)": {
"latest_delta": 0.26954545454545453,
"max_delta": 0.5555555555555556,
"mean_delta": 0.2304038961038961,
"min_delta": 0.09066666666666667,
"task_count": 8
},
"Codex": {
"latest_delta": 0.10814285714285715,
"max_delta": 0.9710261538461539,
"mean_delta": 0.29600608276154416,
"min_delta": 0.018591269841269843,
"task_count": 25
},
"Codex

## Current
- Status: `recovered`
- Observed doctrines: `D10, D11, D12, D13, D14, D15, D16, D17, D17.5, D18, D19, D20, D21, D22, D23, D24, D25, D7, D8, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D7', 'D8', 'D9'], 'verified': ['D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D7', 'D8', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-control_room/snapshots/state_20260506T103929Z.json-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 463
- **PG-control_room/snapshots/state_20260506T103929Z.json-class-1** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 500

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.