# Dossier: `papers/methods/CAMPAIGN_023_MOTIF_CONTRACT_IMPL.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/7cb6505c57e9_papers_methods_CAMPAIGN_023_MOTIF_CONTRACT_IMPL.md.json`
- JSON content_hash: `sha256:794cf3bd4aabd0ac05b93dcbf9608f3d16130652044d811a5ebe196cb5d08050`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 29 / Bytes: 2376

## Birth
- Status: `recovered`
- First-seen commit: `b8473aa3ed840989f6dce967fc460df34c7eed60`
- First-seen date: `2026-05-06T19:23:03-04:00`
- Spawn ticket: `TASK-MOTIF-IMPL`
- Cohort: `TASK-MOTIF-IMPL`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — # Campaign 023: MotifContract.v2 Implementation Rerun
Task: TASK-MOTIF-IMPL
Status: exploratory; no claim-bearing promotion.
## Method
- Predicates are semantic MotifContract.v2 predicates and do not read event-token names.
- Adversarial controls: event_token_rename, state_key_rename, payload_key_rename, generator_id_erasure.
- Substrate-blocked control: within-world-family shuffle, N=10000, seed=

## Current
- Status: `recovered`
- Observed doctrines: `D26`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D26'], 'verified': ['D26'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['reports/campaign_023/full_report.json'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/methods/CAMPAIGN_023_MOTIF_CONTRACT_IMPL.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.