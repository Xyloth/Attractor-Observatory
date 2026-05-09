# Dossier: `Visuals/ui_kits/control_room/rooms/FalsifierAndDoctrine.jsx`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/c3b009e8ef4b_Visuals_ui_kits_control_room_rooms_FalsifierAndDoctrine.jsx.json`
- JSON content_hash: `sha256:305839e8154c8ef241675a8e82f505454532d4ad35d2144a32669656e0a37774`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `visual`
- Generated status: `source`
- Lines: 190 / Bytes: 10101

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **visual_asset_used** — Visual asset/document is referenced by control_room or public docs.

## Current
- Status: `recovered`
- Observed doctrines: `D10, D11, D12, D13, D14, D15, D16, D17, D17.5, D18, D20, D22, D7, D8, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D17.5', 'D18', 'D20', 'D22', 'D7', 'D8', 'D9'], 'verified': ['D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D17.5', 'D18', 'D20', 'D22', 'D7', 'D8', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-Visuals/ui_kits/control_room/rooms/FalsifierAndDoctrine.jsx-class-0** (low, hypothesis): Detected pattern matching Class3 (soft enforcement comments) at line 140

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.