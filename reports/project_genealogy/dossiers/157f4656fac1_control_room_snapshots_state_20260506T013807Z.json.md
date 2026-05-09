# Dossier: `control_room/snapshots/state_20260506T013807Z.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/157f4656fac1_control_room_snapshots_state_20260506T013807Z.json.json`
- JSON content_hash: `sha256:a8066db35d4dcc38b8cd0b65ef3e43f4eda0196b0a00bcc77a8d151a2f68c1df`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `generated`
- Lines: 447 / Bytes: 12948

## Birth
- Status: `honest_decline`
- First-seen commit: ``
- First-seen date: ``
- Spawn ticket: ``
- Cohort: ``
- Decline reason: `private_history_unavailable`

### Birth predicate atoms

## Current
- Status: `recovered`
- Observed doctrines: `D13, D14, D17, D18, D19, D20, D21, D22, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 0, 'covered_atoms': 0, 'missing_atoms': [], 'value': None}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D13', 'D14', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D7'], 'verified': ['D13', 'D14', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 1, 'dereferenceable_evidence_refs': 1, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `honest_decline`

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

## Declines
- birth: `private_history_unavailable`
- drift: `private_history_unavailable`

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.