# Dossier: `public_tests/test_cb022_topic_b_evidence_discipline.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/c0c4355f3d1d_public_tests_test_cb022_topic_b_evidence_discipline.py.json`
- JSON content_hash: `sha256:0f3f0b2ebb2af266614aad87796f4bd87c31dca36a077af27e32ccd2ba7b3b2f`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 119 / Bytes: 4899

## Birth
- Status: `recovered`
- First-seen commit: `215dbc12c2f8c0699a0993fe85164d27f61d6e0f`
- First-seen date: `2026-05-09T07:17:33-04:00`
- Spawn ticket: `TASK-CB-022`
- Cohort: `TASK-CB-022`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.

## Current
- Status: `recovered`
- Public symbols: `test_campaign006_missing_run_paths_are_routed_to_audit_queue, test_every_source_bound_motif_contract_claim_clears_tier3_or_is_diagnostic, test_substance_gate_separates_identifier_shape_resolution_and_support, test_tracked_json_path_references_resolve_or_have_private_boundary_marker`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 84}, {'id': 'error_branch', 'line': 115}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D12', 'D29', 'D7'], 'verified': [], 'claimed_only': ['D12', 'D29', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 5

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-public_tests/test_cb022_topic_b_evidence_discipline.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 73: or lower_value.startswith("python ")
- **PG-public_tests/test_cb022_topic_b_evidence_discipline.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 78: if text.startswith("python "):
- **PG-public_tests/test_cb022_topic_b_evidence_discipline.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 84: except ValueError:
- **PG-public_tests/test_cb022_topic_b_evidence_discipline.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 111: if not rel.endswith(".json") or rel.startswith(("papers/falsification/DX-003/", ".claude/")):
- **PG-public_tests/test_cb022_topic_b_evidence_discipline.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 115: except (OSError, json.JSONDecodeError):

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.