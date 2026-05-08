# Dossier: `public_tests/test_cb011_polish_audit.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/c3e6e3c63b26_public_tests_test_cb011_polish_audit.py.json`
- JSON content_hash: `sha256:1edac77bd7b0baa0f36c03f99786a50598c8ab579f10de590810401f2de17780`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 256 / Bytes: 10843

## Birth
- Status: `recovered`
- First-seen commit: `eba9d36d2bd24e11b9fcf23fc9e58e74b8cad85e`
- First-seen date: `2026-05-07T07:46:38-04:00`
- Spawn ticket: `CB-011`
- Cohort: `CB-011`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — Tests for CB-011 polish + audit fixes.

Covers:
  * Issue 4 — W-1 records adapter scans ALL stores under reports/
  * Issue 1 — BUILD_LOG parser produces structured entries (no docstring leak)
  * Issue 2 — pytest cache stale_cache flag fires when mtime is old
  * Issue 5 — other-world drilldown loader returns records for non-W-1 worlds
  * Issue 7 — FIRE button confirmation marker is well-formed

## Current
- Status: `recovered`
- Public symbols: `test_build_log_handles_missing_file_gracefully, test_build_log_parses_to_structured_entries, test_bulk_resolve_buckets_classify_known_patterns, test_bulk_resolve_first_match_wins_no_double_counting, test_cached_adapters_module_exposes_expected_wrappers, test_cached_records_for_world_returns_same_payload_as_underlying, test_fire_button_confirmation_marker_well_formed, test_other_world_drilldown_loader_returns_records_when_present, test_pytest_stale_cache_flag_does_not_fire_when_fresh, test_pytest_stale_cache_flag_fires_when_mtime_old`
- Observed doctrines: `D17, D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D22'], 'verified': ['D17', 'D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 5, 'dereferenceable_evidence_refs': 5, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.