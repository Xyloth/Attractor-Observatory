# Dossier: `control_room/rooms/README.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/867fa276d4fe_control_room_rooms_README.md.json`
- JSON content_hash: `sha256:c4905cba5f5ad213588247f700ee46bbfd057af45edd8a1bdfe69960c4822ff5`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 189 / Bytes: 8166

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — # Control Room — Room Reference
Quick per-room reference for AI agents reading the codebase. Each room
follows the same shape: imports adapter(s), routes non-`ok` status
through `render_empty_state`, renders real-data panels via the chrome
helpers in `control_room.components`.
D22 binds every room: **the empty-state component is the SOLE no-data
render path**. No fallbacks, no plausible defaults,

## Current
- Status: `recovered`
- Observed doctrines: `D17, D22, D23, D25, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D22', 'D23', 'D25', 'D7'], 'verified': ['D17', 'D22', 'D23', 'D25', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md', 'Control_Room_README.md', 'README.md', 'reports/task_032_dx001_disposition.json'], 'weighted_value': 6.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.