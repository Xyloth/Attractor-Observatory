# Dossier: `reports/campaign_022/convergence_session.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/8254144d96ab_reports_campaign_022_convergence_session.json.json`
- JSON content_hash: `sha256:0957bf2e0b480751f06d43d4eae427c764fca39be1514fd0c1630483eca4abe0`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 131 / Bytes: 6605

## Birth
- Status: `recovered`
- First-seen commit: `e857373697552dd0ce702266d931384299ea053b`
- First-seen date: `2026-05-06T14:39:36-04:00`
- Spawn ticket: `CB-008`
- Cohort: `CB-008`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.
- **header_declared_intent** — {
"branch": "feature/cb-008-ingestion-convergence",
"bugs_fixed": [
{
"evidence": "5/5 molecules had canonical_smiles=='' in baseline; bond_topology_proxy was all zeros; this is the 'PubChem topology bug pattern' the brief explicitly named",
"fix_location": "factory_lowlevel/adapters.py:_query_url + _record_from_row",
"id": "A",
"name": "PubChem SMILES schema drift",
"root_cause": "PubChem PUG-RES

## Current
- Status: `recovered`
- Observed doctrines: `D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D9'], 'verified': ['D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['papers/methods/INGESTION_CONVERGENCE_CB008.md'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-reports/campaign_022/convergence_session.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.