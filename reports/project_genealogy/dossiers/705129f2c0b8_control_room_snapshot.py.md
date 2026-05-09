# Dossier: `control_room/snapshot.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/705129f2c0b8_control_room_snapshot.py.json`
- JSON content_hash: `sha256:c510851ea3398791b55d2e81aad3addf3189732bcdeb24f6aafc75d4d2810750`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `generated`
- Lines: 681 / Bytes: 28473

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — Snapshot endpoint for AI consumption.

Per CB-007 §5: a fresh AI agent (post-compaction Architect Claude,
fresh Codex 1.5x session, etc.) should be able to read ONE snapshot
file at session start instead of parsing 50 source files. This module
composes the structured digest from every adapter and writes it to
``control_room/snapshots/state_<UTC-timestamp>.json``.

Snapshots are append-only by file

## Current
- Status: `recovered`
- Public symbols: `bind_snapshot_freshness, build_snapshot, diff_snapshots, load_latest, load_prior, write_snapshot`
- Observed doctrines: `D17, D22, D23, D30`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 1, 'missing_atoms': ['control_room_surface_renders'], 'value': 0.5}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 164}, {'id': 'error_branch', 'line': 177}, {'id': 'error_branch', 'line': 187}, {'id': 'error_branch', 'line': 469}, {'id': 'error_branch', 'line': 593}, {'id': 'error_branch', 'line': 643}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 3.0}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D22', 'D23', 'D30'], 'verified': ['D17', 'D22', 'D23', 'D30'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 9, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 6.0}`

## Drift
- Status: `review_required`
- Missing birth atoms: `control_room_surface_renders`
- Doctrine boundary crossings: 1
- Letter-vs-spirit surfaces: 6

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-control_room/snapshot.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 164: except (OSError, UnicodeDecodeError):
- **PG-control_room/snapshot.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 177: except (OSError, json.JSONDecodeError):
- **PG-control_room/snapshot.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 187: except (OSError, json.JSONDecodeError):
- **PG-control_room/snapshot.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 469: except (OSError, json.JSONDecodeError):
- **PG-control_room/snapshot.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 593: except ImportError as exc:
- **PG-control_room/snapshot.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 643: except ImportError as exc:
- **PG-control_room/snapshot.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.