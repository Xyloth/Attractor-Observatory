# Dossier: `reports/campaign_016/full_report.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/fab410004653_reports_campaign_016_full_report.json.json`
- JSON content_hash: `sha256:baf4da0af39f06cbd6e0d6701ad2b91ef08f743a47bf380014eeec3d24f0fe64`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 8379 / Bytes: 304196

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.
- **header_declared_intent** — {
"campaign_id": "campaign-016",
"content_hash": "sha256:237057f6937b5d4c1240c88b244745ddf93747dabdfeb1b6533cfd5d074080e9",
"created_at": "2026-05-06T22:03:32Z",
"daemon_session": {
"idempotent_duplicate_run_id": false,
"recorded_at": "2026-05-06T22:03:32Z",
"requires_ai_runtime": false,
"routed_worlds": [
{
"empirical_record_count": 10,
"empirical_record_ids": [
"sha256:23ed8706c34591b284d96185d0

## Current
- Status: `recovered`
- Observed doctrines: `D21`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D21'], 'verified': ['D21'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md', 'papers/methods/CAMPAIGN_017_LOW_LEVEL_DENSITY_AND_PREDICTION.md'], 'weighted_value': 3.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-reports/campaign_016/full_report.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.