# Dossier: `papers/methods/CAMPAIGN_026_FLOOR_BFG_D31.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/741dc2b7bb59_papers_methods_CAMPAIGN_026_FLOOR_BFG_D31.md.json`
- JSON content_hash: `sha256:23c739f651fba705e22fcf3f1ac584d615f2057a3bd4fd1bd5404c05c314aa67`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 31 / Bytes: 1779

## Birth
- Status: `recovered`
- First-seen commit: `60d3171a987fb3de940669461c63d084a8e3dd32`
- First-seen date: `2026-05-07T07:50:30-04:00`
- Spawn ticket: `TASK-FLOOR-BFG`
- Cohort: `TASK-FLOOR-BFG`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — # Campaign 026: Floor BFG Under D31
Task: TASK-FLOOR-BFG
Status: exploratory; no claim-bearing promotion.
## D31 Split
- Predicate rows read signed `outcome_summary` only.
- Lens rows read `trajectory_geometry` only, except the explicitly risky information variant's perturbation magnitude covariate.
- Predicate rows, lens rows, validation predicate rows, and validation lens rows are disjoint pertu

## Current
- Status: `recovered`
- Observed doctrines: `D31`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D31'], 'verified': ['D31'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['reports/campaign_026/full_report.json'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/methods/CAMPAIGN_026_FLOOR_BFG_D31.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.