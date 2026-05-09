# Dossier: `control_room/rooms/basin_floor_lab.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/5d763d96f23a_control_room_rooms_basin_floor_lab.py.json`
- JSON content_hash: `sha256:4c7f69ce3d042c9083bfd7cf387b886188a5828fe8ab6c9a16e4138f7fbbe6b9`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 188 / Bytes: 9570

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — Basin-Floor Geometry Lab — proposal §7.6.

Surfaces the basin-floor candidate (`motif.floor_connectivity.draft`)
trail through Campaigns 010 (deficit map), 013 (replication), CB-001
through CB-003 (multisubstrate + adversarial + substrate-blocked
controls), and Campaign 010 deficit map history.

Per §7.6 of the proposal: the room MUST NOT fake mathematical precision.
If basin diagrams aren't measu

## Current
- Status: `recovered`
- Public symbols: `render`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 187}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.5}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 1, 'imports_out': 8, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 6.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2
- Letter-vs-spirit surfaces: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/rooms/basin_floor_lab.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 70: "verified" if verdict == "methodology_sound" else "warning",
- **PG-control_room/rooms/basin_floor_lab.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 187: except (OSError, json.JSONDecodeError):

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.