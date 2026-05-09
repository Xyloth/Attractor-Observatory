# Dossier: `formalism/motif_contracts/contracts.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/accce5c74b55_formalism_motif_contracts_contracts.py.json`
- JSON content_hash: `sha256:c767cc51307ea993be63688b6b61ee83a4c32f9d071f16ae92ab875c4d16f17b`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `other`
- Generated status: `source`
- Lines: 267 / Bytes: 23269

## Birth
- Status: `recovered`
- First-seen commit: `215dbc12c2f8c0699a0993fe85164d27f61d6e0f`
- First-seen date: `2026-05-09T07:17:33-04:00`
- Spawn ticket: `TASK-CB-022`
- Cohort: `TASK-CB-022`

### Birth predicate atoms
- **tracked_artifact_present** — File is tracked under git but does not match a higher-priority family.
- **header_declared_intent** — Locked MotifContract.v2 registry used by TASK-MOTIF-IMPL.

## Current
- Status: `recovered`
- Public symbols: `all_contracts, contract_payloads, epi, lens, som`
- Observed doctrines: `D26, D31`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D26', 'D31'], 'verified': ['D26', 'D31'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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