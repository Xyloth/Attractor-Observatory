# Dossier: `papers/prereg/campaign_020/externalized_memory.signed.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/5f9d33de1f96_papers_prereg_campaign_020_externalized_memory.signed.json.json`
- JSON content_hash: `sha256:a15bebe7935a62c74c51655fd6f1fd26258034c2ce6fb9caedeae201f9e27c58`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `prereg`
- Generated status: `source`
- Lines: 38 / Bytes: 1703

## Birth
- Status: `recovered`
- First-seen commit: `ff7a2adff3a2bcf5dbddec8e613b3a17dc69edfd`
- First-seen date: `2026-05-06T14:39:23-04:00`
- Spawn ticket: `TASK-033`
- Cohort: `TASK-033`

### Birth predicate atoms
- **prereg_locks_instruments** — Prereg artifact locks basis/lens instruments with a content_hash.
- **header_declared_intent** — {
"campaign_id": "campaign_020",
"claim_promotion_allowed": false,
"content_hash": "sha256:397380071bf815d9b383d26645ab6df218e2142e3fa7e16d8f694b045488af5f",
"coverage_threshold": 0.85,
"forbidden_adjustments": [
"no per-motif threshold tuning",
"no record cherry-picking",
"no claim-bearing promotion",
"no post-hoc primary-lens swap"
],
"input_corpus_hash": "sha256:d4e18a917aef2e563ffc73925a3c1070

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D18'], 'verified': [], 'claimed_only': ['D18'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['reports/campaign_020/full_report.json'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/prereg/campaign_020/externalized_memory.signed.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.