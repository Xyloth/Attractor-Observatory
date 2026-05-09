# Dossier: `papers/falsification/DX-003/round_4_reproducers/path_reference_audit_strict_summary.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/6b54ea5e9604_papers_falsification_DX-003_round_4_reproducers_path_reference_audit_strict_summary.json.json`
- JSON content_hash: `sha256:8fbc787fd6532b8bff3bab155f59724c8e63c5b1200b68ee88dd41cb04029518`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `paper`
- Generated status: `source`
- Lines: 330 / Bytes: 10596

## Birth
- Status: `recovered`
- First-seen commit: `9240e0e2b5cb9eb9f7827edc57a7ffd2a95986c8`
- First-seen date: `2026-05-08T18:04:47-04:00`
- Spawn ticket: `DX-003`
- Cohort: `DX-003`

### Birth predicate atoms
- **paper_artifact_in_falsifier_or_prereg** — Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.
- **header_declared_intent** — {
"examples": [
{
"container": "reports/campaign_006/beta_worlds.json",
"json_path": "rows.0.trace_path",
"marked_private": false,
"value": "runs\\campaign006\\W4_positive_6060_base.json"
},
{
"container": "reports/campaign_006/beta_worlds.json",
"json_path": "rows.1.trace_path",
"marked_private": false,
"value": "runs\\campaign006\\W4_boundary_6061_base.json"
},
{
"container": "reports/campaign_0

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D18'], 'verified': [], 'claimed_only': ['D17', 'D18'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.