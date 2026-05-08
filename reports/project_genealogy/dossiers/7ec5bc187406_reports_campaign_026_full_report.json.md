# Dossier: `reports/campaign_026/full_report.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/7ec5bc187406_reports_campaign_026_full_report.json.json`
- JSON content_hash: `sha256:4289fa77178dc4310a60235896bbe2c88341492808135889681f1a85b6555535`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 33806 / Bytes: 1304648

## Birth
- Status: `recovered`
- First-seen commit: `60d3171a987fb3de940669461c63d084a8e3dd32`
- First-seen date: `2026-05-07T07:50:30-04:00`
- Spawn ticket: `TASK-FLOOR-BFG`
- Cohort: `TASK-FLOOR-BFG`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.
- **header_declared_intent** — {
"campaign_id": "campaign_026",
"cell_results": {
"control_theory": {
"ablation_passed": true,
"adversarial_and_ablation": {
"ablation": {
"passed": true,
"rows": [
{
"base_declined": false,
"passed": true,
"risky_control": "n_a",
"risky_control_passed": true,
"trace_id": "sha256:a3ac76ce30f531101d35d7af4c36956d",
"unchanged_without_predicate_outcome": true
},
{
"base_declined": false,
"passed":

## Current
- Status: `recovered`
- Observed doctrines: `D29, D31`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D29', 'D31'], 'verified': ['D29', 'D31'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['reports/campaign_010/formal_deficit_map.json'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-reports/campaign_026/full_report.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.