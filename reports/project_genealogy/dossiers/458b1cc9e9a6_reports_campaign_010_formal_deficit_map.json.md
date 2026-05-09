# Dossier: `reports/campaign_010/formal_deficit_map.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/458b1cc9e9a6_reports_campaign_010_formal_deficit_map.json.json`
- JSON content_hash: `sha256:01c03856c9f0237eab46a2a73b5e2c249cf1df7b4ac070b09db8a91e46aae19f`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 1220 / Bytes: 42009

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.
- **header_declared_intent** — {
"campaign_013_replication": {
"artifact": "reports/campaign_013/replication_verdict.json",
"basis_hash": "sha256:ce9e243429a69b0b23c84ce6ca4685f89efbb83e94532ebdb125f80949092dbb",
"campaign_id": "campaign-013",
"empirical_p": 0.000999000999000999,
"formal_gap": 0.3549345653383201,
"mode": "candidate_replication",
"verdict": "replicated"
},
"campaign_020_substrate_blocked_sweep": {
"artifact": "r

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D11'], 'verified': [], 'claimed_only': ['D11'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['.architect_state_checkpoint.md', 'BUILD_LOG.md', 'CODEX_TASK_021_DRIVE.md', 'CODEX_TASK_024_DRIVE.md', 'papers/methods/METHODOLOGY_VALIDATION_CB003.md', 'reports/campaign_010/cli_full_report.json', 'reports/campaign_010/full_report.json', 'reports/campaign_013/full_report.json', 'reports/campaign_020/full_report.json', 'reports/campaign_023/full_report.json', 'reports/campaign_024/full_report.json', 'reports/campaign_026/full_report.json'], 'weighted_value': 18.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-reports/campaign_010/formal_deficit_map.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.