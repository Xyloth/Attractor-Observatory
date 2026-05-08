# Dossier: `reports/source_object_generation/source_cache/source_object_entity_observations/source_objects.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/38b81f34fbf8_reports_source_object_generation_source_cache_source_object_entity_observations_source_objects.json.json`
- JSON content_hash: `sha256:a0ce54a9e22ac7c736acaa812d93a11cad1aa97b9cc6156fbe7333de135cc1df`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 1 / Bytes: 1579

## Birth
- Status: `recovered`
- First-seen commit: `8b88da40e8ec798dfd3b49389e91ec980d9add21`
- First-seen date: `2026-05-07T07:51:11-04:00`
- Spawn ticket: `TASK-SOURCE-OBJ-GEN`
- Cohort: `TASK-SOURCE-OBJ-GEN`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D11'], 'verified': [], 'claimed_only': ['D11'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
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
- **PG-reports/source_object_generation/source_cache/source_object_entity_observations/source_objects.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.