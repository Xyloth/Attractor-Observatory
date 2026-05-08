# Dossier: `reports/campaign_006/full_report.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/69e5e39d8b36_reports_campaign_006_full_report.json.json`
- JSON content_hash: `sha256:870d2ce3464a161ac49d2f991edcd9dd39e8de5431673fa5fcf168e524ee76ff`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 2004 / Bytes: 62782

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.
- **header_declared_intent** — {
"campaign_id": "campaign-006",
"elapsed_seconds": 1.6999728999999206,
"gate_count": 68,
"gates": {
"G10_w11_eigen_reference": {
"corrupted_reference_failed": true,
"passed": true,
"reference_check_count": 15,
"regimes": [
"ambiguous",
"failure",
"success"
]
},
"G11_w12_beta": {
"claim_status": "exploratory",
"event_types": [
"cheating_event",
"engulfment_event",
"integration_failure_event",
"res

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D11'], 'verified': [], 'claimed_only': ['D11'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['CODEX_CAMPAIGN_006.md', 'reports/campaign_006/fair_metadata.json', 'reports/campaign_006/prov_o.jsonld'], 'weighted_value': 4.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-reports/campaign_006/full_report.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.