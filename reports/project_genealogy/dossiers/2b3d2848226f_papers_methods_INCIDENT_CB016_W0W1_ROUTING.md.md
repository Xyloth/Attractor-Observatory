# Dossier: `papers/methods/INCIDENT_CB016_W0W1_ROUTING.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/2b3d2848226f_papers_methods_INCIDENT_CB016_W0W1_ROUTING.md.json`
- JSON content_hash: `sha256:d23c474edc405dc913c960d37d00fc0115fc7bab9c283ebe4f8f888671d6d55e`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 121 / Bytes: 4826

## Birth
- Status: `recovered`
- First-seen commit: `5fb61becaaedfcf649f4a83ffd26635b780cdf18`
- First-seen date: `2026-05-07T13:18:05-04:00`
- Spawn ticket: `TASK-CB-016`
- Cohort: `TASK-CB-016`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — # INCIDENT — CB-016 — W0 / W1 Router Schema Mismatch
**Status:** OPEN, surfaced for separate ticket. Records persist
clean; routing-stage rejection prevents simulation only. D17 honest
non-evidence behavior preserved.
## Summary
After CB-016 persistence load-on-init fix, the cache replay
recovered all four CB-015 sources' records into a single coherent
`factory_store/empirical_records.json` (4,378

## Current
- Status: `recovered`
- Observed doctrines: `D14, D17, D19, D22, D26, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17', 'D19', 'D22', 'D26', 'D9'], 'verified': ['D14', 'D17', 'D19', 'D22', 'D26', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-papers/methods/INCIDENT_CB016_W0W1_ROUTING.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.