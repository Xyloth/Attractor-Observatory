# Dossier: `reports/campaign_013/full_report.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/bfd17963128a_reports_campaign_013_full_report.json.json`
- JSON content_hash: `sha256:69facb8cc8020566e48694f7552dc43ad444268b0cab65ae1c0228b35830e566`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 429 / Bytes: 12483

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
"atlas_seed": "reports/campaign_013/atlas_seed.json",
"l3_overlap": "papers/methods/L3_OVERLAP_INSECTS_W7.md",
"replication_verdict": "reports/campaign_013/replication_verdict.json",
"schema_migration": "reports/campaign_013/schema_migration.json"
},
"campaign_id": "campaign-013",
"gate_count": 26,
"gates": {
"AT1": {
"entry_count": 6,
"passed": true
},
"AT2": {
"entry_count": 6,

## Current
- Status: `recovered`
- Observed doctrines: `D14, D17.5, D18, D19, D20, D21`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17.5', 'D18', 'D19', 'D20', 'D21'], 'verified': ['D14', 'D17.5', 'D18', 'D19', 'D20', 'D21'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['.architect_state_checkpoint.md', 'CODEX_TASK_024_DRIVE.md', 'reports/campaign_013/fair_metadata.json', 'reports/campaign_013/prov_o.jsonld'], 'weighted_value': 6.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-reports/campaign_013/full_report.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.