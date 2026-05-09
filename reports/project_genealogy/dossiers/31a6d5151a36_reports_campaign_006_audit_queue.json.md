# Dossier: `reports/campaign_006/audit_queue.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/31a6d5151a36_reports_campaign_006_audit_queue.json.json`
- JSON content_hash: `sha256:1a8a1fcb172af2d6b09cbce1d7b8a40921e683a3e730325c00a0c5fea3405ff8`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 13 / Bytes: 431

## Birth
- Status: `recovered`
- First-seen commit: `215dbc12c2f8c0699a0993fe85164d27f61d6e0f`
- First-seen date: `2026-05-09T07:17:33-04:00`
- Spawn ticket: `TASK-CB-022`
- Cohort: `TASK-CB-022`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.
- **header_declared_intent** — [
{
"audit_id": "CB022-B4-campaign006-private-run-paths",
"doctrine": [
"D17",
"D23",
"D29"
],
"reason": "Campaign 006 reports cite runs/campaign006 private trace artifacts absent from the shipped surface; references are explicitly marked private_unshipped instead of restored from private runtime storage.",
"severity": "medium",
"status": "routed_for_historical_artifact_review"
}
]

## Current
- Status: `recovered`
- Observed doctrines: `D17, D23, D29`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D23', 'D29'], 'verified': ['D17', 'D23', 'D29'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['reports/task_cb022_evidence_discipline/path_reference_markers.json'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-reports/campaign_006/audit_queue.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.