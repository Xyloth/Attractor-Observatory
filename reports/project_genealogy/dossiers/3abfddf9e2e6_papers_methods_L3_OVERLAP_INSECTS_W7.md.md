# Dossier: `papers/methods/L3_OVERLAP_INSECTS_W7.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/3abfddf9e2e6_papers_methods_L3_OVERLAP_INSECTS_W7.md.json`
- JSON content_hash: `sha256:4e311f04a8271f9fc1def3162c41963afb3960f94b52fc1231207cd92308b9a4`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 39 / Bytes: 1695

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.

## Current
- Status: `recovered`
- Observed doctrines: `D21`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 0, 'missing_atoms': ['method_documented'], 'value': 0.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D21'], 'verified': ['D21'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['CODEX_TASK_024_DRIVE.md', 'reports/campaign_013/full_report.json'], 'weighted_value': 3.0}`

## Drift
- Status: `bad_drift`
- Missing birth atoms: `method_documented`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/methods/L3_OVERLAP_INSECTS_W7.md-drift-bad** (high, confirmed): Bad drift: birth predicate atoms missing from current predicate (1 missing) or doctrine boundary crossings detected.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.