# Dossier: `public_tests/test_cb009_atlas_bundle_inbox.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/cf7b373af998_public_tests_test_cb009_atlas_bundle_inbox.py.json`
- JSON content_hash: `sha256:3ccc9968ec0a0a8a0a6507121274972ef426800bff39808aa1ca66175ec3d096`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 369 / Bytes: 15443

## Birth
- Status: `recovered`
- First-seen commit: `8cd23263e328b4544d0b30269ef6f75e76293e26`
- First-seen date: `2026-05-06T17:55:52-04:00`
- Spawn ticket: `CB-009`
- Cohort: `CB-009`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — Tests for the CB-009 Control Room extensions: Atlas periodic table,
paper bundle generator, and audit-queue inbox.

All tests are deterministic and read-only against bundled fixtures
(or write only into ``tmp_path``). No Streamlit runtime is invoked —
we exercise the pure-Python helpers directly so the suite stays fast
and CI-friendly.

## Current
- Status: `recovered`
- Public symbols: `test_audit_drilldown_finds_underlying_empirical_record, test_audit_drilldown_returns_none_for_unknown_record, test_audit_inbox_loads_items_from_all_campaigns, test_audit_inbox_normalizes_heterogeneous_item_shapes, test_audit_inbox_summary_counts_match_unresolved_filter, test_audit_resolution_is_read_only_sidecar, test_paper_bundle_campaign_kind_assembles_real_files, test_paper_bundle_generator_assembles_real_files, test_paper_bundle_includes_all_provenance_campaigns, test_paper_bundle_manifest_carries_bundle_content_hash`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 345}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 5, 'dereferenceable_evidence_refs': 5, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
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
- **PG-public_tests/test_cb009_atlas_bundle_inbox.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 151: f["path"].split("/")[1].split("_")[1] if f["path"].startswith("campaigns/") else None
- **PG-public_tests/test_cb009_atlas_bundle_inbox.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 168: assert result["manifest"]["bundle_content_hash"].startswith("sha256:")
- **PG-public_tests/test_cb009_atlas_bundle_inbox.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 243: assert payload["resolved_at"].endswith("Z")
- **PG-public_tests/test_cb009_atlas_bundle_inbox.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 324: atlas_files = [f for f in manifest["files"] if f["path"].startswith("atlas_entries/")]
- **PG-public_tests/test_cb009_atlas_bundle_inbox.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 345: except (OSError, json.JSONDecodeError):

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.