# Dossier: `papers/prereg/campaign_026/floor_bfg_d31.signed.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/f38188bcec81_papers_prereg_campaign_026_floor_bfg_d31.signed.json.json`
- JSON content_hash: `sha256:36df60b559e538f9e3c1e0159a69784ff7a872dcd92135486f6a220d15b1d8fa`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `prereg`
- Generated status: `source`
- Lines: 48 / Bytes: 2405

## Birth
- Status: `recovered`
- First-seen commit: `60d3171a987fb3de940669461c63d084a8e3dd32`
- First-seen date: `2026-05-07T07:50:30-04:00`
- Spawn ticket: `TASK-FLOOR-BFG`
- Cohort: `TASK-FLOOR-BFG`

### Birth predicate atoms
- **prereg_locks_instruments** — Prereg artifact locks basis/lens instruments with a content_hash.
- **header_declared_intent** — {
"campaign_id": "campaign_026",
"claim_promotion_allowed": false,
"content_hash": "sha256:f0ceb553584dc974aed66024dcd6d9dacd1f2f5a8736cc94c8accaafc8a80ed4",
"forbidden_adjustments": [
"no same-row predicate/lens evaluation",
"no lens import of preprocessing classifier",
"no adjacent_fiber without formal adjacency",
"no claim-bearing promotion"
],
"formalism": "D31 BFG Measurement Split",
"input_c

## Current
- Status: `recovered`
- Observed doctrines: `D29, D31`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D29', 'D31'], 'verified': ['D29', 'D31'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-papers/prereg/campaign_026/floor_bfg_d31.signed.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.