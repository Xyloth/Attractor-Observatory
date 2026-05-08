# Dossier: `public_tests/test_public_contracts.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/04d937351ae6_public_tests_test_public_contracts.py.json`
- JSON content_hash: `sha256:458abf3e631fcf48f2b74b40d077b975bcf44e6fe52bc056ccac4cf26d0a0309`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 159 / Bytes: 6281

## Birth
- Status: `recovered`
- First-seen commit: `ff7a2adff3a2bcf5dbddec8e613b3a17dc69edfd`
- First-seen date: `2026-05-06T14:39:23-04:00`
- Spawn ticket: `TASK-033`
- Cohort: `TASK-033`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.

## Current
- Status: `recovered`
- Public symbols: `test_campaign019_is_live_ready_after_red_gate_repairs, test_doctrine_registry_covers_all_binding_and_candidate_doctrines, test_private_trace_evidence_is_marked_at_point_of_use, test_pubchem_parser_accepts_live_schema_aliases, test_public_docs_do_not_point_at_missing_portfolio_pngs, test_snapshot_has_d24_generation_binding_and_staleness_detection, test_spec_lineage_hashes_match_raw_bytes, test_telemetry_records_have_identity_and_one_active_estimate_per_task`
- Observed doctrines: `D17.5, D23, D24, D25, D26, D27, D28, D29, D30, D31`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D17.5', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31'], 'verified': ['D17.5', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

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
- **PG-public_tests/test_public_contracts.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 123: assert checked["freshness_status"].startswith("stale:")
- **PG-public_tests/test_public_contracts.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 144: statuses = [value for key, value in row.items() if key.lower().endswith("trace_path_status")]

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.