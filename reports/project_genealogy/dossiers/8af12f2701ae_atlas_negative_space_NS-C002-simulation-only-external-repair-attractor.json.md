# Dossier: `atlas/negative_space/NS-C002-simulation-only-external-repair-attractor.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/8af12f2701ae_atlas_negative_space_NS-C002-simulation-only-external-repair-attractor.json.json`
- JSON content_hash: `sha256:8206d355ff8c1c76e867f3f75526d235788ecfd1b8b90dfcdc960383371e9506`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `atlas`
- Generated status: `source`
- Lines: 14 / Bytes: 666

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **atlas_artifact_versioned** — Atlas/registry artifact carries version or content_hash and references real artifacts.
- **header_declared_intent** — {
"campaign_id": "campaign-002",
"entry_id": "NS-C002-simulation-only-external-repair-attractor",
"evidence": [
"reports/campaign_002/boundary_detector_calibration.json"
],
"kind": "simulation_only_attractor",
"owner": "Architect",
"rationale": "K1 same-appearance active-boundary decoys can persist through puncture via external repair. This is stable in W2 but is not a self-maintained individualit

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 1, 'missing_atoms': ['atlas_artifact_versioned'], 'value': 0.5}`
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
- **PG-atlas/negative_space/NS-C002-simulation-only-external-repair-attractor.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.