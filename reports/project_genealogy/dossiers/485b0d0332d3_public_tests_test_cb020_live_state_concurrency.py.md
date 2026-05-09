# Dossier: `public_tests/test_cb020_live_state_concurrency.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/485b0d0332d3_public_tests_test_cb020_live_state_concurrency.py.json`
- JSON content_hash: `sha256:bd89600747abcba30e91828a5f9eacc2b78881e11d887c6afe95dbebcc0fce04`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 406 / Bytes: 16371

## Birth
- Status: `recovered`
- First-seen commit: `115afac08968801fe78a00023a84ef87c1b96a12`
- First-seen date: `2026-05-08T14:35:00-04:00`
- Spawn ticket: `TASK-CB-020`
- Cohort: `TASK-CB-020`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — TASK-CB-020 — concurrency stress for live-state file writes.

Reproduces the race that quarantined 6 of 17 sources during the CB-019
daemon relaunch (08:23 EST 2026-05-08, PID 27516):

  ``OSError [Errno 22] Invalid argument: 'control_room/cache/factory_runs/latest_state.json'``
  ``PermissionError [WinError 5] Access is denied: '.evidence_graph.json.tmp' -> 'evidence_graph.json'``

Root cause: St

## Current
- Status: `recovered`
- Public symbols: `test_atomic_write_json_concurrent_writer_reader, test_atomic_write_json_exhausts_retry_budget_then_raises, test_atomic_write_json_propagates_real_oserror, test_atomic_write_json_retries_on_permission_error, test_atomic_write_json_retries_on_transient_oserror, test_atomic_write_json_three_writers_two_readers_worst_case, test_safe_write_json_canonical_path_succeeds_on_first_atomic, test_safe_write_json_catches_oserror_not_just_permission_error, test_safe_write_json_orphan_fallback_writes_to_canonical_path`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 95}, {'id': 'error_branch', 'line': 109}, {'id': 'error_branch', 'line': 169}, {'id': 'error_branch', 'line': 186}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D12', 'D29', 'D7'], 'verified': [], 'claimed_only': ['D12', 'D29', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 5, 'dereferenceable_evidence_refs': 5, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 4

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-public_tests/test_cb020_live_state_concurrency.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 95: except BaseException as exc:  # noqa: BLE001
- **PG-public_tests/test_cb020_live_state_concurrency.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 109: except BaseException as exc:  # noqa: BLE001
- **PG-public_tests/test_cb020_live_state_concurrency.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 169: except BaseException as exc:  # noqa: BLE001
- **PG-public_tests/test_cb020_live_state_concurrency.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 186: except BaseException as exc:  # noqa: BLE001

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.