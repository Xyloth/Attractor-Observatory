# Dossier: `control_room/launcher.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/71d384d6b906_control_room_launcher.py.json`
- JSON content_hash: `sha256:cb6f6fa04da1f84cc5580c5ef03b9c9a0537ef2bdb15d6c0a08609fb4a77e240`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 288 / Bytes: 11044

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
- Public symbols: `main`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 0, 'missing_atoms': ['control_room_surface_renders'], 'value': 0.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 60}, {'id': 'error_branch', 'line': 92}, {'id': 'error_branch', 'line': 105}, {'id': 'error_branch', 'line': 130}, {'id': 'error_branch', 'line': 143}, {'id': 'error_branch', 'line': 244}, {'id': 'error_branch', 'line': 251}, {'id': 'error_branch', 'line': 261}, {'id': 'error_branch', 'line': 283}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': 5.0}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md', 'Control_Room_README.md', 'reports/task_032_dx001_disposition.json'], 'weighted_value': 4.5}`

## Drift
- Status: `review_required`
- Missing birth atoms: `control_room_surface_renders`
- Doctrine boundary crossings: 2
- Letter-vs-spirit surfaces: 10

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-control_room/launcher.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 60: except OSError:
- **PG-control_room/launcher.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 92: except (OSError, subprocess.SubprocessError) as exc:
- **PG-control_room/launcher.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 105: except (OSError, subprocess.SubprocessError) as exc:
- **PG-control_room/launcher.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 130: except (OSError, subprocess.SubprocessError):
- **PG-control_room/launcher.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 143: except (urllib.error.URLError, ConnectionError, TimeoutError, OSError):
- **PG-control_room/launcher.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 244: except KeyboardInterrupt:
- **PG-control_room/launcher.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 251: except ImportError:
- **PG-control_room/launcher.py-lvs-7** (info, hypothesis): Detected letter-coupled fix surface at line 261: except KeyboardInterrupt:
- **PG-control_room/launcher.py-lvs-8** (info, hypothesis): Detected letter-coupled fix surface at line 283: except Exception:
- **PG-control_room/launcher.py-lvs-9** (info, hypothesis): Detected letter-coupled fix surface at line 287: if __name__ == "__main__":
- **PG-control_room/launcher.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.