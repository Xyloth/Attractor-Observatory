# Dossier: `public_tests/test_cb013_launch_readiness.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/b31a1e069796_public_tests_test_cb013_launch_readiness.py.json`
- JSON content_hash: `sha256:0bdc67e384a804acb96980140eab1afb28c03773d43471fbd5fa81b5f87aa214`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 373 / Bytes: 13417

## Birth
- Status: `recovered`
- First-seen commit: `f1d7305d60c15c1177908245f22443d22cf86bf5`
- First-seen date: `2026-05-07T08:59:39-04:00`
- Spawn ticket: `CB-013`
- Cohort: `CB-013`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — Tests for CB-013 launch readiness mechanics.

Covers:
  * launch_safety.acquire_lock / release_lock
  * launch_safety.verify_resume (clean / mid-flight / aborted)
  * launch_safety.check_factory_store_integrity (uniqueness, orphan refs)
  * launch_safety.write_checkpoint (atomic + checkpoint_at field)
  * progress.load_target_densities (targets doc parsing + D22 absence)
  * progress.write_ingesti

## Current
- Status: `recovered`
- Public symbols: `test_acquire_lock_clean_first_start, test_acquire_lock_overrides_orphaned_lock, test_acquire_lock_refuses_when_holder_alive, test_check_factory_store_integrity_detects_duplicate_record_ids, test_check_factory_store_integrity_detects_orphan_evidence_edges, test_check_factory_store_integrity_passes_clean_store, test_load_target_densities_live_doc_has_15_worlds, test_load_target_densities_parses_canonical_block, test_load_target_densities_returns_empty_when_doc_missing, test_release_lock_idempotent_on_missing`
- Observed doctrines: `D22, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D22', 'D9'], 'verified': ['D22', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 5, 'dereferenceable_evidence_refs': 5, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
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
- **PG-public_tests/test_cb013_launch_readiness.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 245: assert payload["checkpoint_at"].endswith("Z")

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.