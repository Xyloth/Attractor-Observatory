# Dossier: `reports/campaign_012/full_report.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/8d32711053c3_reports_campaign_012_full_report.json.json`
- JSON content_hash: `sha256:f3ce57cbb42253867d0db739f51d190f7d6509dc3a7dfe5dbbcb1f7cca1e82d6`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 323 / Bytes: 9842

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.
- **header_declared_intent** — {
"artifacts": {
"calibration_hardening": "reports/campaign_012/calibration_hardening.json",
"factory_scaffolding": "reports/campaign_012/factory_scaffolding.json",
"real_lane1": "reports/campaign_012/real_lane1_extraction.json",
"replication_protocol": "papers/methods/FLOOR_CONNECTIVITY_REPLICATION_PROTOCOL.md",
"w7_templates": "reports/campaign_012/w7_template_renaming.json"
},
"campaign_id": "c

## Current
- Status: `recovered`
- Observed doctrines: `D23, D29`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D23', 'D29'], 'verified': ['D23', 'D29'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['CODEX_TASK_023_DRIVE.md', 'reports/campaign_012/fair_metadata.json', 'reports/campaign_012/prov_o.jsonld', 'reports/task_cb022_evidence_discipline/path_reference_markers.json'], 'weighted_value': 6.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-reports/campaign_012/full_report.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.