# Dossier: `control_room/heartbeat.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/8f77bf4b66e5_control_room_heartbeat.py.json`
- JSON content_hash: `sha256:e044caf263ff327307bb593c8993725f2169ddf6bc879df060cbb8e9e6c5a6bd`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 223 / Bytes: 9520

## Birth
- Status: `recovered`
- First-seen commit: `ff7a2adff3a2bcf5dbddec8e613b3a17dc69edfd`
- First-seen date: `2026-05-06T14:39:23-04:00`
- Spawn ticket: `TASK-033`
- Cohort: `TASK-033`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — Agent heartbeat ledger.

Lightweight presence tracking for AI agents working in the repo. Each
agent (Architect Claude, Codex, Claude Builder, Codex 1.5x, Destroyer
Claude — slot reserved, see below) flips a bit on entry and on exit:

* On entry, the agent calls ``mark_entered(agent_id, task_id)``.
* On exit, the agent calls ``mark_exited(agent_id)``.

The Control Room reads ``read_heartbeat()`` o

## Current
- Status: `recovered`
- Public symbols: `mark_entered, mark_exited, mark_seen, read_heartbeat, render_sidebar_panel`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 64}, {'id': 'error_branch', 'line': 147}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 1.0}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2
- Letter-vs-spirit surfaces: 2

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-control_room/heartbeat.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 64: except (OSError, json.JSONDecodeError):
- **PG-control_room/heartbeat.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 147: except ValueError:
- **PG-control_room/heartbeat.py-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 20

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.