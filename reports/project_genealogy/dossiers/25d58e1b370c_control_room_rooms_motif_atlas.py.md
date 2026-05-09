# Dossier: `control_room/rooms/motif_atlas.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/25d58e1b370c_control_room_rooms_motif_atlas.py.json`
- JSON content_hash: `sha256:59acfda963845c426180de2c396c1084adba1fe6643c13057e99ed54887863ba`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 518 / Bytes: 22447

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
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 133}, {'id': 'error_branch', 'line': 168}, {'id': 'error_branch', 'line': 233}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 1.5}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 1, 'imports_out': 8, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 6.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2
- Letter-vs-spirit surfaces: 5

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/rooms/motif_atlas.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 133: except (OSError, json.JSONDecodeError) as exc:
- **PG-control_room/rooms/motif_atlas.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 168: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/motif_atlas.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 233: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/motif_atlas.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 273: elif verdict == "falsified":
- **PG-control_room/rooms/motif_atlas.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 279: elif mode_tag == "candidate" or formal_gap_score > 0.5:

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.