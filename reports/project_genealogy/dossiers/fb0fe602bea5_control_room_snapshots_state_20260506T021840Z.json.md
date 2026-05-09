# Dossier: `control_room/snapshots/state_20260506T021840Z.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/fb0fe602bea5_control_room_snapshots_state_20260506T021840Z.json.json`
- JSON content_hash: `sha256:be83ad5459c8ae735dc21276d6c8f779a1692599f3349318552b37124d3a7a33`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `generated`
- Lines: 562 / Bytes: 16497

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
- Observed doctrines: `D10, D11, D12, D13, D14, D15, D16, D17, D17.5, D18, D19, D20, D21, D22, D23, D24, D25, D7, D8, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 0, 'covered_atoms': 0, 'missing_atoms': [], 'value': None}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D7', 'D8', 'D9'], 'verified': ['D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D7', 'D8', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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