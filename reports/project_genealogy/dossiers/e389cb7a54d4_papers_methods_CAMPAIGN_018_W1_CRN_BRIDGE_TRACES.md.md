# Dossier: `papers/methods/CAMPAIGN_018_W1_CRN_BRIDGE_TRACES.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/e389cb7a54d4_papers_methods_CAMPAIGN_018_W1_CRN_BRIDGE_TRACES.md.json`
- JSON content_hash: `sha256:8e09d0d139f5f76cdb49b7c75b028e612b4adf138c8f2964f7d9017c34d05f15`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 37 / Bytes: 2118

## Birth
- Status: `recovered`
- First-seen commit: `ff7a2adff3a2bcf5dbddec8e613b3a17dc69edfd`
- First-seen date: `2026-05-06T14:39:23-04:00`
- Spawn ticket: `TASK-033`
- Cohort: `TASK-033`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — # Campaign 018 - W1 CRN Bridge-Trace Generation
Campaign 018 tests the Campaign 017 CRN bridge prediction by generating real W1 CRN traces from every Campaign 016 low-level empirical record.
## Inputs And Discipline
- Source records: `reports/campaign_016/factory_store/empirical_records.json`.
- All 16 records project; no record-class cherry-picking or opt-out is allowed.
- Projection logic is det

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 1, 'missing_atoms': ['method_documented'], 'value': 0.5}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D18', 'D29'], 'verified': [], 'claimed_only': ['D11', 'D18', 'D29'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

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
- **PG-papers/methods/CAMPAIGN_018_W1_CRN_BRIDGE_TRACES.md-drift-bad** (high, confirmed): Bad drift: birth predicate atoms missing from current predicate (1 missing) or doctrine boundary crossings detected.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.