# Dossier: `public_tests/test_source_object_generation.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/b591947fee2d_public_tests_test_source_object_generation.py.json`
- JSON content_hash: `sha256:1b97ad863f23c310754ef6a73c0aa0a817a849a63ff98378560eab4edc9570e9`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 108 / Bytes: 4958

## Birth
- Status: `recovered`
- First-seen commit: `8b88da40e8ec798dfd3b49389e91ec980d9add21`
- First-seen date: `2026-05-07T07:51:11-04:00`
- Spawn ticket: `TASK-SOURCE-OBJ-GEN`
- Cohort: `TASK-SOURCE-OBJ-GEN`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.

## Current
- Status: `recovered`
- Public symbols: `test_measurability_recovery_plan_marks_only_generated_non_floor_sources_ready, test_source_object_adapters_emit_required_records_and_decoys, test_source_object_contracts_do_not_include_floor_connectivity, test_source_object_records_are_d26_d29_and_provenance_safe, test_source_object_report_goes_green`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D12', 'D29', 'D7'], 'verified': [], 'claimed_only': ['D12', 'D29', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 1

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-public_tests/test_source_object_generation.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 105: if line.startswith("| motif.") and "ready_for_round_2c_implementation" in line

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.