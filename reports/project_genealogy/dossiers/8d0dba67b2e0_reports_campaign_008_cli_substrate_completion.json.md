# Dossier: `reports/campaign_008/cli_substrate_completion.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/8d0dba67b2e0_reports_campaign_008_cli_substrate_completion.json.json`
- JSON content_hash: `sha256:25abebe02d67256bfcc6f7c2dc03277cc508c92c0f4fd15e24e76e96f453b3d0`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 908 / Bytes: 28612

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.
- **header_declared_intent** — {
"artifacts": {
"blocker_SH3": "BLOCKER-SH3-CAMPAIGN-008-STRICT-SUBSTANCE-FLOORS.md",
"calibration": "reports/campaign_008/calibration_real_k3_k10.json",
"d14": "reports/campaign_008/d14_world_audit.json",
"methods": "papers\\methods\\CAMPAIGN_008_METHODS.md"
},
"campaign_id": "campaign-008",
"gate_count": 35,
"gates": {
"KR1": {
"corpus_id": "K3",
"ece": 0.06,
"passed": true,
"roc_auc": 0.88,
"s

## Current
- Status: `recovered`
- Observed doctrines: `D17.5, D23, D29`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D17.5', 'D23', 'D29'], 'verified': ['D17.5', 'D23', 'D29'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BLOCKER-SH3-CAMPAIGN-008-STRICT-SUBSTANCE-FLOORS.md', 'reports/task_cb022_evidence_discipline/path_reference_markers.json'], 'weighted_value': 3.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-reports/campaign_008/cli_substrate_completion.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.