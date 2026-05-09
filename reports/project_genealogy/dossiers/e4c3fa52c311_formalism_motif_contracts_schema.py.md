# Dossier: `formalism/motif_contracts/schema.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/e4c3fa52c311_formalism_motif_contracts_schema.py.json`
- JSON content_hash: `sha256:ce17ad0b019416d902ebdeeebaeb0aa563b6304833579b31b60c0ea03628e72d`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `other`
- Generated status: `source`
- Lines: 270 / Bytes: 9244

## Birth
- Status: `recovered`
- First-seen commit: `20c8c938e8f7e7abf1af4a8348c0983ddae455de`
- First-seen date: `2026-05-09T07:11:04-04:00`
- Spawn ticket: `TASK-CB-022`
- Cohort: `TASK-CB-022`

### Birth predicate atoms
- **tracked_artifact_present** — File is tracked under git but does not match a higher-priority family.

## Current
- Status: `recovered`
- Public symbols: `IndependenceVerdict, LensContract, MotifContractV2, PredicateResult, SourceObjectEntry, VerdictState, canonical_json, content_hash, derive_independence_verdict`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': [], 'verified': [], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.