# Dossier: `FAIR_DATA_STEWARDSHIP.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/85ca373c298d_FAIR_DATA_STEWARDSHIP.md.json`
- JSON content_hash: `sha256:f24cef2d5a59bdf83a6ce73fb2ea3bf15ef585eabfae23d540a163c1f8e25584`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 34 / Bytes: 1489

## Birth
- Status: `recovered`
- First-seen commit: `2f804f0a8b912a3afbec90dbb1cdaf92162a612f`
- First-seen date: `2026-05-06T21:25:06-04:00`
- Spawn ticket: `DX-002`
- Cohort: `DX-002`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.
- **header_declared_intent** — # FAIR Data Stewardship Statement
Status: public-surface policy, TASK-DX-002-FIX.
This repository is a curated public research surface. It is FAIR-aligned for public artifacts and explicitly private-bounded for generated traces and private runtime code.
## Findable
- Campaign reports live under `reports/campaign_*/full_report.json`.
- Methodology documents live under `papers/methods/`.
- Doctrine

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': [], 'verified': [], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
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