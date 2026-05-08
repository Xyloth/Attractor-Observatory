# Dossier: `reports/campaign_006/evidence_bundles/campaign_006_bundle.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/bc67447439a3_reports_campaign_006_evidence_bundles_campaign_006_bundle.json.json`
- JSON content_hash: `sha256:a9893a4f6cbf5f446a6023f0ac8c2b6f3db046dc2f75f992644d73dc29e77c6b`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 212 / Bytes: 8262

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.
- **header_declared_intent** — {
"artifact_count": 29,
"bundle_id": "EB-CAMPAIGN_006",
"campaign_id": "campaign_006",
"claim_status": "candidate",
"content_hash": "sha256:deed23f04c52b96a119cab36698357b9a3add366721153cdfcce55d0f201c126",
"generation_command": "python make_campaign_006.py",
"license_class": "cc0",
"mode_tag": "exploratory",
"retention_class": "indexed",
"schema": "EvidenceBundle.application.v1",
"source_artifact

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D11'], 'verified': [], 'claimed_only': ['D11'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['reports/campaign_006/formal_biology.json', 'reports/campaign_006/full_report.json', 'reports/campaign_006/negative_space.json'], 'weighted_value': 4.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-reports/campaign_006/evidence_bundles/campaign_006_bundle.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.