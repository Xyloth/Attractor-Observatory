# Dossier: `control_room/rooms/world_observatory.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/ad6210fac468_control_room_rooms_world_observatory.py.json`
- JSON content_hash: `sha256:e77b9a0646f6b2a43613c1c651d2c014f77367d6cee17690b6bf8708a8c6aa67`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 289 / Bytes: 12406

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
- Observed doctrines: `D17, D21`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 108}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': 1.0}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D21'], 'verified': ['D17', 'D21'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 1, 'imports_out': 10, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 8.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 6

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/rooms/world_observatory.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 108: except Exception as e:  # surface any render error visibly
- **PG-control_room/rooms/world_observatory.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 125: if d == "claim_ready_densified" or family in density_overrides
- **PG-control_room/rooms/world_observatory.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 129: falsified = sum(1 for _, _, _, d in WORLD_INVENTORY if d == "falsifier_active")
- **PG-control_room/rooms/world_observatory.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 164: status="verified" if density == "claim_ready_densified" else
- **PG-control_room/rooms/world_observatory.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 165: "warning" if density == "exploratory_densified" else
- **PG-control_room/rooms/world_observatory.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 166: "failed" if density == "falsifier_active" else

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.