# Dossier: `papers/prereg/task_meas_plan/MEASURABILITY_RECOVERY_PLAN_v1.structure.signed.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/35c10ef96852_papers_prereg_task_meas_plan_MEASURABILITY_RECOVERY_PLAN_v1.structure.signed.json.json`
- JSON content_hash: `sha256:83e28d27671e40d79c8f5f7200bf235219150de58b3fc3890a22ff9e605fd376`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `prereg`
- Generated status: `source`
- Lines: 52 / Bytes: 1588

## Birth
- Status: `recovered`
- First-seen commit: `2f804f0a8b912a3afbec90dbb1cdaf92162a612f`
- First-seen date: `2026-05-06T21:25:06-04:00`
- Spawn ticket: `DX-002`
- Cohort: `DX-002`

### Birth predicate atoms
- **prereg_locks_instruments** — Prereg artifact locks basis/lens instruments with a content_hash.
- **header_declared_intent** — {
"schema": "MeasurabilityRecoveryPlanPreregistration.v1",
"task_id": "TASK-MEAS-PLAN",
"artifact": "papers/methods/MEASURABILITY_RECOVERY_PLAN_v1.md",
"registered_at_est": "2026-05-06 20:26:37 EST",
"mode_tag": "planning_only",
"implementation_allowed": false,
"source_artifacts": [
"reports/campaign_024/lens_coupling_audit.json",
"papers/methods/LENS_RECOVERY_v1_DRAFT.md",
"papers/methods/MOTIF_C

## Current
- Status: `recovered`
- Observed doctrines: `D27`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D27'], 'verified': ['D27'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md', 'papers/methods/MEASURABILITY_RECOVERY_PLAN_v1.md'], 'weighted_value': 3.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/prereg/task_meas_plan/MEASURABILITY_RECOVERY_PLAN_v1.structure.signed.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.