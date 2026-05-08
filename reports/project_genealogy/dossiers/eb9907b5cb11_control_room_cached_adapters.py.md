# Dossier: `control_room/cached_adapters.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/eb9907b5cb11_control_room_cached_adapters.py.json`
- JSON content_hash: `sha256:b5bdd25a526ac8755aa9ad9e786f4ca274d0363992c9b1d7ecf0e649720ad331`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 71 / Bytes: 2581

## Birth
- Status: `recovered`
- First-seen commit: `eba9d36d2bd24e11b9fcf23fc9e58e74b8cad85e`
- First-seen date: `2026-05-07T07:46:38-04:00`
- Spawn ticket: `CB-011`
- Cohort: `CB-011`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — Streamlit-cached wrappers around the expensive adapter calls.

CB-011 fix #8/#10 — smoothness: James reported lag on room switching.
Profiling showed every render of every room calls
``parse_build_log()``, ``parse_campaign_reports()``, ``build_snapshot()``,
and ``load_records_for_world()`` from disk. With the W-1 mass-ingest
adding 1,394 records and the BUILD_LOG growing to 41 entries with
prose b

## Current
- Status: `recovered`
- Public symbols: `cached_audit_inbox_summary, cached_build_log, cached_campaign_reports, cached_factory_store, cached_methods_falsifiers, cached_records_for_world`
- Observed doctrines: `D17`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 1, 'missing_atoms': ['control_room_surface_renders'], 'value': 0.5}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 32}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.5}`
- **doctrine_binding_quality**: `{'required': ['D17'], 'verified': ['D17'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Missing birth atoms: `control_room_surface_renders`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/cached_adapters.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 32: except Exception:
- **PG-control_room/cached_adapters.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.