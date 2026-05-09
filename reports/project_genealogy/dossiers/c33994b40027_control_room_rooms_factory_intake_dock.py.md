# Dossier: `control_room/rooms/factory_intake_dock.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/c33994b40027_control_room_rooms_factory_intake_dock.py.json`
- JSON content_hash: `sha256:69a645a2547c4955df23bb65e99230ee46a0b43e2ad28f23c572587a9f82a21f`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 1039 / Bytes: 48538

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — Factory Intake Dock - Room 9 live multi-world console.

TASK-033 turns this room from a low-level preview into a daemon-backed FIRE
console. The UI aims source adapters at target worlds, starts the autonomous
Factory subprocess, polls live stage state, and renders the persisted run
record. No Control Room code fabricates records or writes Factory science
state; the subprocess owns ingestion/simula

## Current
- Status: `recovered`
- Public symbols: `render`
- Observed doctrines: `D17, D22, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 171}, {'id': 'error_branch', 'line': 235}, {'id': 'error_branch', 'line': 239}, {'id': 'error_branch', 'line': 455}, {'id': 'error_branch', 'line': 481}, {'id': 'error_branch', 'line': 539}, {'id': 'error_branch', 'line': 566}, {'id': 'error_branch', 'line': 902}, {'id': 'error_branch', 'line': 921}, {'id': 'error_branch', 'line': 941}, {'id': 'error_branch', 'line': 1032}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 5.5}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D22', 'D9'], 'verified': ['D17', 'D22', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 1, 'imports_out': 6, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 6.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2
- Letter-vs-spirit surfaces: 13

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/rooms/factory_intake_dock.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 107: default=[world for world in world_options if world in {"crn", "field", "ecosystem", "origins_chemistry", "quasispecies"}
- **PG-control_room/rooms/factory_intake_dock.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 171: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/factory_intake_dock.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 235: except Exception:
- **PG-control_room/rooms/factory_intake_dock.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 239: except Exception:
- **PG-control_room/rooms/factory_intake_dock.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 455: except (OSError, subprocess.SubprocessError):
- **PG-control_room/rooms/factory_intake_dock.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 481: except OSError:
- **PG-control_room/rooms/factory_intake_dock.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 539: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/factory_intake_dock.py-lvs-7** (info, hypothesis): Detected letter-coupled fix surface at line 566: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/factory_intake_dock.py-lvs-8** (info, hypothesis): Detected letter-coupled fix surface at line 902: except (OSError, json.JSONDecodeError) as exc:
- **PG-control_room/rooms/factory_intake_dock.py-lvs-9** (info, hypothesis): Detected letter-coupled fix surface at line 921: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/factory_intake_dock.py-lvs-10** (info, hypothesis): Detected letter-coupled fix surface at line 941: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/factory_intake_dock.py-lvs-11** (info, hypothesis): Detected letter-coupled fix surface at line 986: lambda i: (i.get("reason") or "").startswith("stale_cache:"),
- **PG-control_room/rooms/factory_intake_dock.py-lvs-12** (info, hypothesis): Detected letter-coupled fix surface at line 1032: except Exception:
- **PG-control_room/rooms/factory_intake_dock.py-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 798

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.