# Dossier: `control_room/rooms/pulse_deck.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/7978229337d8_control_room_rooms_pulse_deck.py.json`
- JSON content_hash: `sha256:2c1b7dcbaeaf6989abaaf0f265f0e9edea91f21c61c5efe1140d7e169ddf2bc9`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 398 / Bytes: 17264

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.

## Current
- Status: `recovered`
- Public symbols: `render`
- Observed doctrines: `D17, D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 342}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': 1.0}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D22'], 'verified': ['D17', 'D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 1, 'imports_out': 16, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 10.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2
- Letter-vs-spirit surfaces: 9

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/rooms/pulse_deck.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 109: if r.get("model_name", "").startswith("Claude (Builder)"):
- **PG-control_room/rooms/pulse_deck.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 325: if kind == "campaign_added":
- **PG-control_room/rooms/pulse_deck.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 327: if kind == "campaign_status_changed":
- **PG-control_room/rooms/pulse_deck.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 329: if kind == "pytest_failed_count_changed":
- **PG-control_room/rooms/pulse_deck.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 331: if kind == "falsifier_count_changed":
- **PG-control_room/rooms/pulse_deck.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 333: if kind == "doctrine_registry_count_changed":
- **PG-control_room/rooms/pulse_deck.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 335: if kind == "build_log_entry_new":
- **PG-control_room/rooms/pulse_deck.py-lvs-7** (info, hypothesis): Detected letter-coupled fix surface at line 337: if kind == "claude_builder_latest_delta_changed":
- **PG-control_room/rooms/pulse_deck.py-lvs-8** (info, hypothesis): Detected letter-coupled fix surface at line 342: except (TypeError, ValueError):

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.