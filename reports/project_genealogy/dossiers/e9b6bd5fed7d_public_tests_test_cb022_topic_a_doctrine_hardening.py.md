# Dossier: `public_tests/test_cb022_topic_a_doctrine_hardening.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/e9b6bd5fed7d_public_tests_test_cb022_topic_a_doctrine_hardening.py.json`
- JSON content_hash: `sha256:d5575d7b285f2afb1f15ee692a8c8d383d90e2023db64c745fb25d3f49be5754`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 110 / Bytes: 5270

## Birth
- Status: `recovered`
- First-seen commit: `20c8c938e8f7e7abf1af4a8348c0983ddae455de`
- First-seen date: `2026-05-09T07:11:04-04:00`
- Spawn ticket: `TASK-CB-022`
- Cohort: `TASK-CB-022`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.

## Current
- Status: `recovered`
- Public symbols: `test_d31_audit_catches_dynamic_import_and_split_outcome_summary, test_d31_runtime_import_hook_blocks_dynamic_classifier_import, test_metadata_identity_erasure_catches_world_family_cheat, test_source_object_canonicalization_catches_aliases_ancestors_and_wildcards, test_value_label_erasure_catches_numeric_label_channel_cheat`
- Observed doctrines: `D31`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D31'], 'verified': ['D31'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
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