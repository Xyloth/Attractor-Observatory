# Dossier: `reports/campaign_007/truth_pass_application.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/29e620c5a1c9_reports_campaign_007_truth_pass_application.json.json`
- JSON content_hash: `sha256:cc305e4aec4185cae7b371ffa476c35bbd6d5881e164fe80427d36768d601ace`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 46 / Bytes: 1899

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.
- **header_declared_intent** — {
"applications": [
{
"artifact": "validation\\claim_ledger\\claims.jsonl",
"artifact_private_boundary_reason": "D23/D29: referenced runtime artifact is private or unshipped on the public surface",
"artifact_status": "private_unshipped",
"evidence_private": true,
"modification": "status=exploratory; public_allowed=false; D11 weakness note",
"private_boundary_reason": "D23/D29: referenced runtime a

## Current
- Status: `recovered`
- Observed doctrines: `D11, D23, D29`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D23', 'D29'], 'verified': ['D11', 'D23', 'D29'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['CODEX_CAMPAIGN_007.md', 'reports/campaign_002/full_report.json', 'reports/campaign_006/full_report.json', 'reports/campaign_007/truth_pass.json', 'reports/task_cb022_evidence_discipline/path_reference_markers.json'], 'weighted_value': 7.5}`

## Drift
- Status: `positive_deepening`

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.