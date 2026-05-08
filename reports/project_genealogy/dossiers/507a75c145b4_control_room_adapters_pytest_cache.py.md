# Dossier: `control_room/adapters/pytest_cache.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/507a75c145b4_control_room_adapters_pytest_cache.py.json`
- JSON content_hash: `sha256:7aa853cb9011b25391c2bac79476c15365f51d39a117683e28e749849741f68e`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 114 / Bytes: 4432

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — Parse the pytest cache directory if present.

The pytest cache (``.pytest_cache/``) carries lastfailed, nodeids, and
v/cache/ metadata. We extract the lastfailed list and a count of
known nodeids; this is enough for the Pulse Deck to surface "tests
that failed last run." Absent cache → ``status: missing``.

CB-011 fix #2 — Stale cache detection.
James reported the dashboard saying "4 pytest failed

## Current
- Status: `recovered`
- Public symbols: `parse_pytest_cache`
- Observed doctrines: `D17`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 1, 'missing_atoms': ['control_room_surface_renders'], 'value': 0.5}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 70}, {'id': 'error_branch', 'line': 76}, {'id': 'error_branch', 'line': 87}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 1.5}`
- **doctrine_binding_quality**: `{'required': ['D17'], 'verified': ['D17'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-control_room/adapters/pytest_cache.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 70: except (OSError, json.JSONDecodeError):
- **PG-control_room/adapters/pytest_cache.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 76: except OSError:
- **PG-control_room/adapters/pytest_cache.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 87: except (OSError, json.JSONDecodeError):
- **PG-control_room/adapters/pytest_cache.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.