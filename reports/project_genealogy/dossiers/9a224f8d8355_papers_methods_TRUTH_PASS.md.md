# Dossier: `papers/methods/TRUTH_PASS.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/9a224f8d8355_papers_methods_TRUTH_PASS.md.json`
- JSON content_hash: `sha256:2212ff82d5ece5d510ef6a999d260bb84dcb66c981d85e8f22395a53a3485d13`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 13 / Bytes: 525

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D18', 'D29'], 'verified': [], 'claimed_only': ['D11', 'D18', 'D29'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['.architect_state_checkpoint.md', 'CODEX_CAMPAIGN_007.md', 'CODEX_TASK_019_DRIVE.md', 'CODEX_TASK_021_DRIVE.md', 'CODEX_TASK_024_DRIVE.md', 'README.md', 'WAITING_TO_BE_PUBLISHED.md', 'docs/DOCTRINE.md', 'reports/campaign_010/cli_full_report.json', 'reports/campaign_010/full_report.json', 'reports/campaign_010/truth_pass_refresh.json', 'reports/task_019/task019_closure.json'], 'weighted_value': 18.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/methods/TRUTH_PASS.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.