# Dossier: `papers/prereg/deficit_map_v0.signed.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/9cdfec786f84_papers_prereg_deficit_map_v0.signed.json.json`
- JSON content_hash: `sha256:a4ece357e719cb3df0fec346b6dc703598989267dd238d20e267a86a97f26194`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `prereg`
- Generated status: `source`
- Lines: 11898 / Bytes: 616267

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **prereg_locks_instruments** — Prereg artifact locks basis/lens instruments with a content_hash.
- **header_declared_intent** — {
"campaign_id": "campaign-010",
"component_weights": {
"compression_score": 0.15,
"encoding_success": 0.2,
"invariance_preservation": 0.2,
"prediction_component": 0.25,
"reconstruction_score": 0.2
},
"content_hash": "sha256:204712c952011141f5c7eb2f1cf63187a5edbbdc742abefcc29adb74580e6866",
"coverage_components": [
"encoding_success",
"reconstruction_score",
"prediction_component",
"invariance_pre

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D18'], 'verified': [], 'claimed_only': ['D18'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md', 'CODEX_AUDIT_001_CLAUDE_BUILDER_TASK_CB_001.md', 'CODEX_AUDIT_002_CLAUDE_BUILDER_TASK_CB_002.md', 'CODEX_TASK_021_DRIVE.md', 'TASK-CB-003_METHODOLOGY_VALIDATION.md', 'reports/campaign_010/cli_full_report.json', 'reports/campaign_010/formal_deficit_map.json', 'reports/campaign_010/full_report.json'], 'weighted_value': 12.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/prereg/deficit_map_v0.signed.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.