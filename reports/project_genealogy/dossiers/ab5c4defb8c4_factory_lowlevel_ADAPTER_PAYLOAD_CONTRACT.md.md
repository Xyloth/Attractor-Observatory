# Dossier: `factory_lowlevel/ADAPTER_PAYLOAD_CONTRACT.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/ab5c4defb8c4_factory_lowlevel_ADAPTER_PAYLOAD_CONTRACT.md.json`
- JSON content_hash: `sha256:6985147acf4990a4681d147605f8b6c325452c905fb446f4d0534820a508193e`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `factory`
- Generated status: `source`
- Lines: 62 / Bytes: 5012

## Birth
- Status: `recovered`
- First-seen commit: `40abab3b87f50c32c3f42496752308ecd6eb11e6`
- First-seen date: `2026-05-07T15:04:02-04:00`
- Spawn ticket: `TASK-PHASE-B-INFRA`
- Cohort: `TASK-PHASE-B-INFRA`

### Birth predicate atoms
- **factory_module_exposes_callable** — Module exposes runnable factory components consumed by the daemon/pipeline.
- **header_declared_intent** — # Factory Adapter Payload Contract
Status: Phase-B canonical contract. Mode: exploratory, source-bound.
This contract closes the CB-016 W0/W1 routing incident class: adapters and routers must agree on where simulation parameters live before records enter world construction.
## Canonical Direction
Codex chooses direction **B** as the forward contract: simulation parameters live under `EmpiricalReco

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 1, 'missing_atoms': ['factory_module_exposes_callable'], 'value': 0.5}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17.5', 'D7'], 'verified': [], 'claimed_only': ['D14', 'D17.5', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md', 'papers/methods/INGESTION_TARGETS.md'], 'weighted_value': 3.0}`

## Drift
- Status: `bad_drift`
- Missing birth atoms: `factory_module_exposes_callable`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-factory_lowlevel/ADAPTER_PAYLOAD_CONTRACT.md-drift-bad** (high, confirmed): Bad drift: birth predicate atoms missing from current predicate (1 missing) or doctrine boundary crossings detected.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.