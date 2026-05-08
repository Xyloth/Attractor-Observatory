# Dossier: `public_tests/test_cb016_persistence_load_on_init.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/48dcdbb41205_public_tests_test_cb016_persistence_load_on_init.py.json`
- JSON content_hash: `sha256:0d24905a700a39cf57822cec698b267050ef3c0c6ed33b9ec802a10f640c8218`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 310 / Bytes: 12768

## Birth
- Status: `recovered`
- First-seen commit: `38d6923d95056690442d2121b1c9c67146da3fa2`
- First-seen date: `2026-05-07T13:08:59-04:00`
- Spawn ticket: `TASK-CB-016`
- Cohort: `TASK-CB-016`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — Tests for CB-016 persistence load-on-init fix.

The CB-015 T8 incident found that ``LowLevelFactoryStore.__init__``
initialized empty in-memory dicts and did NOT load existing JSON
files from disk. Result: every ``run_live_factory_cycle`` call
overwrote the persisted store with only that run's records, wiping
prior cycles.

CB-016 fix: ``__init__`` calls ``_load_existing_from_disk`` after
dict con

## Current
- Status: `recovered`
- Public symbols: `test_load_on_init_empty_store_starts_empty, test_load_on_init_malformed_json_emits_audit_entry, test_load_on_init_per_row_malformation_skipped, test_load_on_init_reads_existing_records, test_load_on_init_recovers_actual_cb015_store, test_load_on_init_three_source_sequential_all_coexist, test_load_on_init_two_source_sequential_write_both_coexist, test_load_on_init_upsert_same_record_id`
- Observed doctrines: `D14, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D9'], 'verified': ['D14', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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