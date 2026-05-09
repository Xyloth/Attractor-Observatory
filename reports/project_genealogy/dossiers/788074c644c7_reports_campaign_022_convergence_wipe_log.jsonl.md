# Dossier: `reports/campaign_022/convergence_wipe_log.jsonl`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/788074c644c7_reports_campaign_022_convergence_wipe_log.jsonl.json`
- JSON content_hash: `sha256:933f5ab828373e592248ab106e5eac79b874ae3f77b4df3c47b729ed7efdc3df`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 1 / Bytes: 646

## Birth
- Status: `recovered`
- First-seen commit: `e857373697552dd0ce702266d931384299ea053b`
- First-seen date: `2026-05-06T14:39:36-04:00`
- Spawn ticket: `CB-008`
- Cohort: `CB-008`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.
- **header_declared_intent** — {"counts_before_wipe": {"audit_queue.json": 0, "empirical_records.json": 16, "evidence_graph.json": 19, "normalized_refs.json": 16, "snapshot.json": "snapshot", "source_cache_index.json": 3}, "reason": "CB-008 cycle 2 prep \u2014 Bug A (PubChem SMILES schema), Bug B (provenance schema), Bug C (silent garbage), Bug E (no traces) fixed; baseline contained schema-violating records and zero traces. Wi

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D11'], 'verified': [], 'claimed_only': ['D11'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-reports/campaign_022/convergence_wipe_log.jsonl-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.