# Dossier: `reports/campaign_011/full_report.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/af709cd20020_reports_campaign_011_full_report.json.json`
- JSON content_hash: `sha256:b7e1491938ea059bb58e5eae5fea5d8608a55dfe1360da7fb3d9945febe5d462`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 349 / Bytes: 9904

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
"calibration": "reports/campaign_011/calibration_full.json",
"doctrine": "docs/doctrine_d19_d21.md",
"factory": "reports/campaign_011/ingestion_factory.json",
"ontology": "reports/campaign_011/ontology_full.json",
"w7": "reports/campaign_011/w7_densification_report.json"
},
"campaign_id": "campaign-011",
"gate_count": 32,
"gates": {
"D19": {
"false_claim_rejection_rate": 1.0,
"pas

## Current
- Status: `recovered`
- Observed doctrines: `D19, D20, D21`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D19', 'D20', 'D21'], 'verified': ['D19', 'D20', 'D21'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['CLAUDE_FACTORY_INITIATION.md', 'CODEX_TASK_022_DRIVE.md', 'reports/campaign_011/fair_metadata.json', 'reports/campaign_011/prov_o.jsonld', 'reports/campaign_012/factory_initiation_pointer_audit.json', 'reports/campaign_012/factory_scaffolding.json'], 'weighted_value': 9.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-reports/campaign_011/full_report.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.