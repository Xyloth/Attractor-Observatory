# Dossier: `control_room/rooms/_world_drilldown.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/57e7137e69c4_control_room_rooms__world_drilldown.py.json`
- JSON content_hash: `sha256:103b9d8a6d5c5eebc7db11cb0b3245b3380126555440e48782e2ab39ddd10800`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 576 / Bytes: 26289

## Birth
- Status: `recovered`
- First-seen commit: `ff7a2adff3a2bcf5dbddec8e613b3a17dc69edfd`
- First-seen date: `2026-05-06T14:39:23-04:00`
- Spawn ticket: `TASK-033`
- Cohort: `TASK-033`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.

## Current
- Status: `recovered`
- Public symbols: `load_records_for_world, render_world_drilldown`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 51}, {'id': 'error_branch', 'line': 194}, {'id': 'error_branch', 'line': 473}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': 2.0}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

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
- **PG-control_room/rooms/_world_drilldown.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 51: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/_world_drilldown.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 103: if world_family == "math_primitives":
- **PG-control_room/rooms/_world_drilldown.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 105: elif world_family == "atomic_molecular_primitives":
- **PG-control_room/rooms/_world_drilldown.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 194: except Exception:
- **PG-control_room/rooms/_world_drilldown.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 473: except Exception:

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.