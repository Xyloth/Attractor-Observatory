# Dossier: `public_tests/test_pg001_control_room_tab.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/ed91da906a56_public_tests_test_pg001_control_room_tab.py.json`
- JSON content_hash: `sha256:d884acb9e09219b98e1fc9de44a2cb37721f675611cd4098830a25eef07f3fce`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 138 / Bytes: 5125

## Birth
- Status: `recovered`
- First-seen commit: `01c6c38479151939d0f7c2be30f4d79df6f1bb7e`
- First-seen date: `2026-05-08T15:49:33-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — PG-001 Mission Control Project Genealogy tab tests.

PG19 — the tab renders deterministically from atlas_latest.json and
coherence_latest.json. Closing and reopening against the same artifacts
must produce an identical render.

The test uses Streamlit's :class:`AppTest` to invoke the room's
``render()`` callable in a deterministic harness and asserts:

* The tab loads without raising.
* When atlas

## Current
- Status: `recovered`
- Public symbols: `test_apptest_renders_empty_state_when_no_atlas, test_apptest_renders_with_published_artifacts, test_counts_in_tab_match_atlas_summary, test_room_constants_match_spec, test_room_module_imports_without_streamlit_runtime, test_room_render_is_deterministic_against_same_atlas`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 5, 'dereferenceable_evidence_refs': 5, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
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