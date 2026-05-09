# Dossier: `public_tests/test_pg001_schema.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/38c563b68529_public_tests_test_pg001_schema.py.json`
- JSON content_hash: `sha256:cc0862d322979a52118682d98cb54e3887d66f95fa83c263e486a6ed96e059f9`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 241 / Bytes: 10123

## Birth
- Status: `recovered`
- First-seen commit: `01c6c38479151939d0f7c2be30f4d79df6f1bb7e`
- First-seen date: `2026-05-08T15:49:33-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — PG-001 schema validation public tests.

Tests assert the published artifacts under ``reports/project_genealogy/``
are well-formed and self-consistent. They run against whatever atlas the
repo currently ships; if the artifacts are absent, the tests are skipped
with the empty-state reason recorded.

Schema scope:
* Manifest carries audited file list and mission atoms with source refs.
* Every dossie

## Current
- Status: `recovered`
- Public symbols: `test_atlas_present_and_references_dossier_hashes, test_atlas_summary_counts_match_nodes, test_coherence_binds_atlas_and_mission_atoms, test_decline_taxonomy_used_only_from_canonical_set, test_doctrine_index_resolves_to_audited_files, test_dossier_schema_and_manifest_binding, test_findings_carry_reproducer_or_decline, test_manifest_has_mission_atoms_with_source_refs, test_manifest_present_and_versioned, test_manifest_threshold_policy_locked_before_findings`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D12', 'D29', 'D7'], 'verified': [], 'claimed_only': ['D12', 'D29', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 5, 'dereferenceable_evidence_refs': 5, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 7

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-public_tests/test_pg001_schema.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 45: assert manifest["content_hash"].startswith("sha256:")
- **PG-public_tests/test_pg001_schema.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 82: assert atlas["content_hash"].startswith("sha256:")
- **PG-public_tests/test_pg001_schema.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 89: assert node["dossier_hash"].startswith("sha256:")
- **PG-public_tests/test_pg001_schema.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 159: if status in {"removable_clean", "removable_with_warnings", "not_removable"}:
- **PG-public_tests/test_pg001_schema.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 163: elif status == "probe_declined":
- **PG-public_tests/test_pg001_schema.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 191: assert rb["atlas_hash"].startswith("sha256:")
- **PG-public_tests/test_pg001_schema.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 192: assert rb["input_manifest_hash"].startswith("sha256:")

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.