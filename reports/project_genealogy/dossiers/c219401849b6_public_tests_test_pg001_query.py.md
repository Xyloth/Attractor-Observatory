# Dossier: `public_tests/test_pg001_query.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/c219401849b6_public_tests_test_pg001_query.py.json`
- JSON content_hash: `sha256:89339cbcaf4b0904fb7ae3b4f758e8158db8ae10f9fd16688cd40bfe663d1995`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 136 / Bytes: 4026

## Birth
- Status: `recovered`
- First-seen commit: `01c6c38479151939d0f7c2be30f4d79df6f1bb7e`
- First-seen date: `2026-05-08T15:49:33-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — PG-001 query API public tests.

Exercises the documented Python API and the CLI examples from the spec's
§"Query API Surface". Tests assume the published atlas exists; if not,
they skip with a reason (PG-001 may not have run on this branch).

## Current
- Status: `recovered`
- Public symbols: `test_cli_files_runs_against_atlas, test_cli_orphans_runs, test_query_depth_outliers_shape, test_query_doctrine_collisions_returns_canonical_shape, test_query_files_filter_returns_required_columns, test_query_files_path_glob, test_query_findings_reproducer_filter, test_query_index_loads, test_query_orphans_kinds_distinct`

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
- **PG-public_tests/test_pg001_query.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 50: assert r["path"].startswith("docs/")
- **PG-public_tests/test_pg001_query.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 51: assert r["path"].endswith(".md")

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.