# Dossier: `papers/methods/MEASURABILITY_RECOVERY_PLAN_v1.signed.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/5c52e55da708_papers_methods_MEASURABILITY_RECOVERY_PLAN_v1.signed.json.json`
- JSON content_hash: `sha256:0288241318f3d88eaf1dc3044c3dcb1e0b6e0a42a1ba0493290b73cb196a8867`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 22 / Bytes: 873

## Birth
- Status: `recovered`
- First-seen commit: `2f804f0a8b912a3afbec90dbb1cdaf92162a612f`
- First-seen date: `2026-05-06T21:25:06-04:00`
- Spawn ticket: `DX-002`
- Cohort: `DX-002`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — {
"schema": "MeasurabilityRecoveryPlanSignature.v1",
"task_id": "TASK-MEAS-PLAN",
"artifact": "papers/methods/MEASURABILITY_RECOVERY_PLAN_v1.md",
"artifact_raw_sha256": "sha256:86cd22a55b870299422aa7f34701937369e350f567f9daa5d8b64b16d2aee1f5",
"signed_at_est": "2026-05-06 20:30:08 EST",
"signed_by": "Codex 1.5x",
"basis": {
"campaign_024_bad_cell_count": 33,
"all_bad_cells_classified_once": true,

## Current
- Status: `recovered`
- Observed doctrines: `D31`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D31'], 'verified': ['D31'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/methods/MEASURABILITY_RECOVERY_PLAN_v1.signed.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.