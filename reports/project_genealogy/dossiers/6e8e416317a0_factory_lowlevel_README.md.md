# Dossier: `factory_lowlevel/README.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/6e8e416317a0_factory_lowlevel_README.md.json`
- JSON content_hash: `sha256:2fc821109028003f595b4a41e50ddba18cdb8afca3d481a124117646b83f08a9`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `factory`
- Generated status: `source`
- Lines: 107 / Bytes: 3169

## Birth
- Status: `recovered`
- First-seen commit: `b8473aa3ed840989f6dce967fc460df34c7eed60`
- First-seen date: `2026-05-06T19:23:03-04:00`
- Spawn ticket: `TASK-MOTIF-IMPL`
- Cohort: `TASK-MOTIF-IMPL`

### Birth predicate atoms
- **factory_module_exposes_callable** — Module exposes runnable factory components consumed by the daemon/pipeline.
- **header_declared_intent** — # Low-Level Factory
The Factory is a daemon-safe ingestion path for source-bound empirical records.
It does not use AI at runtime. Adapters fetch or load authoritative seed
payloads, normalize records, route them into compatible worlds, simulate traces,
evaluate motif lenses, and persist exploratory outputs with provenance.
## World Coverage
TASK-035 extends the Factory routing surface to all 15 c

## Current
- Status: `recovered`
- Observed doctrines: `D23`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 1, 'missing_atoms': ['factory_module_exposes_callable'], 'value': 0.5}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D23'], 'verified': ['D23'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

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
- **PG-factory_lowlevel/README.md-drift-bad** (high, confirmed): Bad drift: birth predicate atoms missing from current predicate (1 missing) or doctrine boundary crossings detected.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.