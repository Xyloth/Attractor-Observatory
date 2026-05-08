# Dossier: `papers/prereg/campaign_023/repair.signed.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/7b887cf86775_papers_prereg_campaign_023_repair.signed.json.json`
- JSON content_hash: `sha256:9809704443a3a360e899fbb61a2580d30b1a5948101a261169a2c87a6d4c708f`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `prereg`
- Generated status: `source`
- Lines: 35 / Bytes: 1528

## Birth
- Status: `recovered`
- First-seen commit: `b8473aa3ed840989f6dce967fc460df34c7eed60`
- First-seen date: `2026-05-06T19:23:03-04:00`
- Spawn ticket: `TASK-MOTIF-IMPL`
- Cohort: `TASK-MOTIF-IMPL`

### Birth predicate atoms
- **prereg_locks_instruments** — Prereg artifact locks basis/lens instruments with a content_hash.
- **header_declared_intent** — {
"campaign_id": "campaign_023",
"claim_promotion_allowed": false,
"content_hash": "sha256:8aee595eac5932d71d5dd9a436abdb8a9166c3598ab9592584a7f842fcbf965a",
"forbidden_adjustments": [
"no event-token predicate labels",
"no per-motif threshold tuning",
"no claim-bearing promotion"
],
"input_corpus_hash": "sha256:36821eaedae36fed52053755457d3ba9540240b954b8249390f0f1f96d5e5947",
"min_negative_per_s

## Current
- Status: `recovered`
- Observed doctrines: `D26`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D26'], 'verified': ['D26'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-papers/prereg/campaign_023/repair.signed.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.