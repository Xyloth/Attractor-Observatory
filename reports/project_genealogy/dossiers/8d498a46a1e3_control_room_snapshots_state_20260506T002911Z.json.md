# Dossier: `control_room/snapshots/state_20260506T002911Z.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/8d498a46a1e3_control_room_snapshots_state_20260506T002911Z.json.json`
- JSON content_hash: `sha256:2155b457eb16ead9ebc9a9250aeb483f9ad5281d22f4799446a85e85faea2693`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `generated`
- Lines: 417 / Bytes: 12237

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — {
"calibration_trajectory": {
"by_model": {
"Claude (Builder)": {
"latest_delta": 0.20973333333333333,
"max_delta": 0.5555555555555556,
"mean_delta": 0.2248122448979592,
"min_delta": 0.09066666666666667,
"task_count": 7
},
"Codex": {
"latest_delta": 0.7030957142857144,
"max_delta": 0.9337037037037037,
"mean_delta": 0.28895242453297376,
"min_delta": 0.018591269841269843,
"task_count": 21
},
"unknow

## Current
- Status: `recovered`
- Observed doctrines: `D13, D14, D17, D18, D19, D20, D21, D22, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 1, 'missing_atoms': ['control_room_surface_renders'], 'value': 0.5}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D13', 'D14', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D7'], 'verified': ['D13', 'D14', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Missing birth atoms: `control_room_surface_renders`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/snapshots/state_20260506T002911Z.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.