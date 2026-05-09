# Dossier: `public_tests/test_phase_b_adapters.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/f69670344ae1_public_tests_test_phase_b_adapters.py.json`
- JSON content_hash: `sha256:53b4730302723dbe50ea5a27880a76bd85763bde2915dafeda64878aa79bd078`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 141 / Bytes: 6530

## Birth
- Status: `recovered`
- First-seen commit: `40abab3b87f50c32c3f42496752308ecd6eb11e6`
- First-seen date: `2026-05-07T15:04:02-04:00`
- Spawn ticket: `TASK-PHASE-B-INFRA`
- Cohort: `TASK-PHASE-B-INFRA`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.

## Current
- Status: `recovered`
- Public symbols: `test_force_refresh_clears_state_with_audit_payload, test_phase_b_adapters_hit_ratified_phase2_targets_offline, test_phase_b_overlap_adapters_declare_distinct_simulation_cut, test_phase_b_records_match_router_contract_and_provenance, test_w0_w1_payload_contract_routes_phase_a_records`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D12', 'D29', 'D7'], 'verified': [], 'claimed_only': ['D12', 'D29', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

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