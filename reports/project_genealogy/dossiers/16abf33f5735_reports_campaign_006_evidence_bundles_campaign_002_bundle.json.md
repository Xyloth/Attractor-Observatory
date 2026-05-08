# Dossier: `reports/campaign_006/evidence_bundles/campaign_002_bundle.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/16abf33f5735_reports_campaign_006_evidence_bundles_campaign_002_bundle.json.json`
- JSON content_hash: `sha256:456e480d95b5125cdd28037291435120aff247015cf57b9a147cbb6972f07175`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 22 / Bytes: 681

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.
- **header_declared_intent** — {
"artifact_count": 1,
"bundle_id": "EB-CAMPAIGN_002",
"campaign_id": "campaign_002",
"claim_status": "candidate",
"content_hash": "sha256:cc12b0368e9f09817eff5792c158235a7e98f72962c3719fd9b63c7d92088c58",
"generation_command": "python make_campaign_002.py",
"license_class": "cc0",
"mode_tag": "exploratory",
"retention_class": "indexed",
"schema": "EvidenceBundle.application.v1",
"source_artifacts

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D11'], 'verified': [], 'claimed_only': ['D11'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-reports/campaign_006/evidence_bundles/campaign_002_bundle.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.