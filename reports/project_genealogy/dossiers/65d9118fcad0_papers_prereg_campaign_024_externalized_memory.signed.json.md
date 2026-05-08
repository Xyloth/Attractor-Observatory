# Dossier: `papers/prereg/campaign_024/externalized_memory.signed.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/65d9118fcad0_papers_prereg_campaign_024_externalized_memory.signed.json.json`
- JSON content_hash: `sha256:3d5cc38c7f21f6339a37235151c381e92d87cc774e9cbaf05fdb3b62641cef41`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `prereg`
- Generated status: `source`
- Lines: 38 / Bytes: 1703

## Birth
- Status: `recovered`
- First-seen commit: `b8473aa3ed840989f6dce967fc460df34c7eed60`
- First-seen date: `2026-05-06T19:23:03-04:00`
- Spawn ticket: `TASK-MOTIF-IMPL`
- Cohort: `TASK-MOTIF-IMPL`

### Birth predicate atoms
- **prereg_locks_instruments** — Prereg artifact locks basis/lens instruments with a content_hash.
- **header_declared_intent** — {
"campaign_id": "campaign_024",
"claim_promotion_allowed": false,
"content_hash": "sha256:d816ed02b7e0dd6b24ff0f2dfb66867710b67757f33bba491550ea5eaeddad94",
"forbidden_adjustments": [
"no event-token predicates",
"no event-token lenses",
"no generator-id metadata",
"no C020 floor label-function score",
"no claim-bearing promotion"
],
"input_corpus_hash": "sha256:8466261cf9f7b500dbac1cf0ed27b67fb2

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D18'], 'verified': [], 'claimed_only': ['D18'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/prereg/campaign_024/externalized_memory.signed.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.