# Dossier: `Visuals/preview/empty-state.html`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/213e58f1871c_Visuals_preview_empty-state.html.json`
- JSON content_hash: `sha256:151083ae4855f586e933ae9f16124ca2e6d814851841e54aee30a7ab10c1bce7`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `visual`
- Generated status: `source`
- Lines: 9 / Bytes: 714

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **visual_asset_used** — Visual asset/document is referenced by control_room or public docs.
- **header_declared_intent** — <!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="_card.css"></head><body><div class="card">
<div class="kicker">empty-state · D22 binding · single source of truth</div>
<div class="empty-state">
<div class="empty-label">no data</div>
<div class="empty-reason">Pulse Deck is a Phase 0 placeholder. Phase 1 will populate this room with project health score, active branch,

## Current
- Status: `recovered`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-Visuals/preview/empty-state.html-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 5

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.