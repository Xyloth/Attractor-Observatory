# Dossier: `control_room/rooms/_placeholder.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/db511372baac_control_room_rooms__placeholder.py.json`
- JSON content_hash: `sha256:7c636d64e6ac15bc9b00a903bb7884ca4c678cca5b9202ae7fec7f2a44b9054a`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 66 / Bytes: 2078

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — Shared placeholder render helper — D22 binding.

Phase 0 rooms render via this helper exclusively. The helper writes the
room title bar (so layouts are consistent across rooms) and then routes
to ``render_empty_state`` for the body. This is the SOLE no-data
pathway permitted by D22.

Phase 1+ will modify each room module individually to consume its
adapter(s) and render real content; until then, t

## Current
- Status: `recovered`
- Public symbols: `render_placeholder_room`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/rooms/_placeholder.py-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 1
- **PG-control_room/rooms/_placeholder.py-class-1** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 9
- **PG-control_room/rooms/_placeholder.py-class-2** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 27
- **PG-control_room/rooms/_placeholder.py-class-3** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 36
- **PG-control_room/rooms/_placeholder.py-class-4** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 62

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.