# Dossier: `control_room/app.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/49736f39db69_control_room_app.py.json`
- JSON content_hash: `sha256:a8b3110db391b9b3f80bff61fd976725e6fada257f93cd94c6a4fce33db4aa72`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 238 / Bytes: 8683

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — Streamlit entry for the Observatory Control Room.

Run::

    streamlit run control_room/app.py

The app shell is dark-mode by default per proposal §6, applies the
design tokens from ``control_room.design_tokens``, and renders sidebar
navigation across all 11 rooms (proposal §7 + Project Graph). Phase 0
shipped the foundation; Phase 1+2 wired real rooms; Phase 3 (CB-007)
ships polish, click-to-nav

## Current
- Status: `recovered`
- Public symbols: `main`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 1, 'missing_atoms': ['control_room_surface_renders'], 'value': 0.5}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 61}, {'id': 'error_branch', 'line': 92}, {'id': 'error_branch', 'line': 176}, {'id': 'error_branch', 'line': 228}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': 2.5}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 2, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md', 'Control_Room_README.md'], 'weighted_value': 4.0}`

## Drift
- Status: `review_required`
- Missing birth atoms: `control_room_surface_renders`
- Doctrine boundary crossings: 2
- Letter-vs-spirit surfaces: 5

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-control_room/app.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 61: except (OSError, subprocess.SubprocessError):
- **PG-control_room/app.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 92: except Exception:
- **PG-control_room/app.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 176: except Exception:
- **PG-control_room/app.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 228: except Exception as exc:  # noqa: BLE001 -- snapshot must not break render
- **PG-control_room/app.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 237: if __name__ == "__main__":
- **PG-control_room/app.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.