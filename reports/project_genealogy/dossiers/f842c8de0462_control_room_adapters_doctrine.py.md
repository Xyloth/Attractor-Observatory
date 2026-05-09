# Dossier: `control_room/adapters/doctrine.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/f842c8de0462_control_room_adapters_doctrine.py.json`
- JSON content_hash: `sha256:66a8fbcd84e32c1634f29f798925e9ff577edb169b2e2fcb2e66ac85a30f58b9`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 79 / Bytes: 3035

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
- Public symbols: `parse_doctrine`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 0, 'missing_atoms': ['control_room_surface_renders'], 'value': 0.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 32}, {'id': 'error_branch', 'line': 49}, {'id': 'error_branch', 'line': 57}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 1.5}`
- **doctrine_binding_quality**: `{'required': ['D22', 'D24', 'D30'], 'verified': [], 'claimed_only': ['D22', 'D24', 'D30'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Missing birth atoms: `control_room_surface_renders`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 3

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/adapters/doctrine.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 32: except (OSError, json.JSONDecodeError) as exc:
- **PG-control_room/adapters/doctrine.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 49: except (OSError, UnicodeDecodeError):
- **PG-control_room/adapters/doctrine.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 57: except (OSError, UnicodeDecodeError):
- **PG-control_room/adapters/doctrine.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.