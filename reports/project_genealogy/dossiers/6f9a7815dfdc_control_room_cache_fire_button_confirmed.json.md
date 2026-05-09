# Dossier: `control_room/cache/fire_button_confirmed.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/6f9a7815dfdc_control_room_cache_fire_button_confirmed.json.json`
- JSON content_hash: `sha256:5af6b4bc2e4dabb74c0005feecdb5301f93eb0e7ba967d02c6e77df1122f370b`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 40 / Bytes: 2255

## Birth
- Status: `recovered`
- First-seen commit: `eba9d36d2bd24e11b9fcf23fc9e58e74b8cad85e`
- First-seen date: `2026-05-07T07:46:38-04:00`
- Spawn ticket: `CB-011`
- Cohort: `CB-011`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — {
"schema": "FireButtonConfirmation.v1",
"task_id": "TASK-CB-011",
"confirmed_working_at": "2026-05-06T23:46:00Z",
"confirmed_by": "Claude (Builder) self-test",
"test_args": {
"allow_network": false,
"target_worlds": ["atomic_molecular_primitives"],
"source_ids": ["source.nist.asd.energy_levels"],
"rationale": "minimum cycle: NIST atomic spectra, offline (bundled seed), single world"
},
"results":

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 1, 'missing_atoms': ['control_room_surface_renders'], 'value': 0.5}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D22', 'D24', 'D30'], 'verified': [], 'claimed_only': ['D22', 'D24', 'D30'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Missing birth atoms: `control_room_surface_renders`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/cache/fire_button_confirmed.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.