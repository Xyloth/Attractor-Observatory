# Dossier: `atlas/status_viewer/generated/campaign_006/queries.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/fa091a06be8e_atlas_status_viewer_generated_campaign_006_queries.json.json`
- JSON content_hash: `sha256:0a5eebf777ec8b09c9eefdd08cd21a52fad7be3a4ae256fb4e678c89ab6e4797`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `atlas`
- Generated status: `generated`
- Lines: 89 / Bytes: 3441

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **atlas_artifact_versioned** — Atlas/registry artifact carries version or content_hash and references real artifacts.

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 0, 'missing_atoms': ['atlas_artifact_versioned'], 'value': 0.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D23'], 'verified': [], 'claimed_only': ['D11', 'D23'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Missing birth atoms: `atlas_artifact_versioned`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-atlas/status_viewer/generated/campaign_006/queries.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.