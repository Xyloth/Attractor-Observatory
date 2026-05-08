# Dossier: `control_room/rooms/factory_intake_dock.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/c33994b40027_control_room_rooms_factory_intake_dock.py.json`
- JSON content_hash: `sha256:d60a0d2a8c9b2303960c2dbbe580aa059ee395a66e377e3d9bae602ff6d2ccc4`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 1031 / Bytes: 47933

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
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 171}, {'id': 'error_branch', 'line': 235}, {'id': 'error_branch', 'line': 239}, {'id': 'error_branch', 'line': 428}, {'id': 'error_branch', 'line': 447}, {'id': 'error_branch', 'line': 473}, {'id': 'error_branch', 'line': 531}, {'id': 'error_branch', 'line': 558}, {'id': 'error_branch', 'line': 894}, {'id': 'error_branch', 'line': 913}, {'id': 'error_branch', 'line': 933}, {'id': 'error_branch', 'line': 1024}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 6.0}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D22', 'D9'], 'verified': ['D17', 'D22', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 1, 'imports_out': 6, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 6.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2
- Letter-vs-spirit surfaces: 14

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
- **PG-control_room/rooms/factory_intake_dock.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 428: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/factory_intake_dock.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 447: except (OSError, subprocess.SubprocessError):
- **PG-control_room/rooms/factory_intake_dock.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 473: except OSError:
- **PG-control_room/rooms/factory_intake_dock.py-lvs-7** (info, hypothesis): Detected letter-coupled fix surface at line 531: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/factory_intake_dock.py-lvs-8** (info, hypothesis): Detected letter-coupled fix surface at line 558: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/factory_intake_dock.py-lvs-9** (info, hypothesis): Detected letter-coupled fix surface at line 894: except (OSError, json.JSONDecodeError) as exc:
- **PG-control_room/rooms/factory_intake_dock.py-lvs-10** (info, hypothesis): Detected letter-coupled fix surface at line 913: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/factory_intake_dock.py-lvs-11** (info, hypothesis): Detected letter-coupled fix surface at line 933: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/factory_intake_dock.py-lvs-12** (info, hypothesis): Detected letter-coupled fix surface at line 978: lambda i: (i.get("reason") or "").startswith("stale_cache:"),
- **PG-control_room/rooms/factory_intake_dock.py-lvs-13** (info, hypothesis): Detected letter-coupled fix surface at line 1024: except Exception:
- **PG-control_room/rooms/factory_intake_dock.py-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 790

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.