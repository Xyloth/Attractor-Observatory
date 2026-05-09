# Dossier: `public_tests/test_live_pipeline_world_traces.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/67ea1e0d4aaf_public_tests_test_live_pipeline_world_traces.py.json`
- JSON content_hash: `sha256:d8f3a6205b771a9aae0b8a292275e6bd9df516c9fcd3ff4fe706f5de9a8c71e4`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 57 / Bytes: 2467

## Birth
- Status: `recovered`
- First-seen commit: `85bb893baf5825dd00c4b143fb77d63c3055c1ee`
- First-seen date: `2026-05-08T08:17:16-04:00`
- Spawn ticket: `TASK-CB-019`
- Cohort: `TASK-CB-019`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.

## Current
- Status: `recovered`
- Public symbols: `test_live_pipeline_persists_verifiable_world_traces_idempotently`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D12', 'D29', 'D7'], 'verified': [], 'claimed_only': ['D12', 'D29', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 1, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 2.0}`

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