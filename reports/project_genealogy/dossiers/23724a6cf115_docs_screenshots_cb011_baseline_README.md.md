# Dossier: `docs/screenshots/cb011_baseline/README.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/23724a6cf115_docs_screenshots_cb011_baseline_README.md.json`
- JSON content_hash: `sha256:408ed6271a78f99e74ddf2e182e3bb16d323ab291275f8286ed94d5018151350`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `docs`
- Generated status: `source`
- Lines: 56 / Bytes: 3572

## Birth
- Status: `recovered`
- First-seen commit: `eba9d36d2bd24e11b9fcf23fc9e58e74b8cad85e`
- First-seen date: `2026-05-07T07:46:38-04:00`
- Spawn ticket: `CB-011`
- Cohort: `CB-011`

### Birth predicate atoms
- **doc_serves_handbook** — Doc serves the project handbook (doctrine support, methodology, audit notes).
- **header_declared_intent** — # CB-011 Screenshot Baseline
Directory reserved for full-room screenshot baselines from the
CB-011 polish round. Capture at 1480 px viewport (the canonical
`max-width` set in `control_room/design_tokens.py`).
## Capture targets
| Filename                           | Room                  | Notes                                              |
|------------------------------------|------------------

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11'], 'verified': [], 'claimed_only': ['D11'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.