# Dossier: `public_tests/test_cb021_memory_guard.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/13d7df7aea78_public_tests_test_cb021_memory_guard.py.json`
- JSON content_hash: `sha256:25dd9526602d738534d46c94a3ddfe601772a7b1308d04eb0e5bb20dfa65400c`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 318 / Bytes: 12906

## Birth
- Status: `recovered`
- First-seen commit: `eada8c9bab091a8e21b021537c65a845709c2a6a`
- First-seen date: `2026-05-08T16:57:19-04:00`
- Spawn ticket: `TASK-CB-021`
- Cohort: `TASK-CB-021`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — TASK-CB-021 — memory-safety guardrails after 2026-05-08 OOM incident.

The incident report (factory-daemon-incident-report-2026-05-08.md)
documented the daemon eating 40-50 GB of RSS in one long-lived Python
process and white-screening the desktop. Architectural fixes (sharded
persistence, per-source child processes, SQLite migration) deferred
to a separate ticket; CB-021 ships *guardrails* so the

## Current
- Status: `recovered`
- Public symbols: `test_check_memory_budget_aborts_on_high_min_free, test_check_memory_budget_aborts_on_low_max_rss, test_check_memory_budget_unmeasured_returns_ok, test_check_memory_budget_within_default, test_consume_stop_flag_idempotent, test_continuous_daemon_calls_memory_budget_check, test_continuous_daemon_calls_stop_flag_check, test_heartbeat_payload_includes_pid_rss_free, test_live_state_payload_includes_rss, test_measure_memory_returns_real_values`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D12', 'D29', 'D7'], 'verified': [], 'claimed_only': ['D12', 'D29', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 5, 'dereferenceable_evidence_refs': 5, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 2

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-public_tests/test_cb021_memory_guard.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 105: assert reason.startswith("memory_budget_exceeded:")
- **PG-public_tests/test_cb021_memory_guard.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 117: assert reason.startswith("memory_budget_exceeded:")

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.