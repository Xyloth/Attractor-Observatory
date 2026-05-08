# Dossier: `Visuals/ui_kits/control_room/mockData.js`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/983e368295d5_Visuals_ui_kits_control_room_mockData.js.json`
- JSON content_hash: `sha256:d70f96f65c6e143fa9de84784e767e8b26f1aca84ccc5b12a7488ebd9f2206b2`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `visual`
- Generated status: `source`
- Lines: 114 / Bytes: 10940

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
- Observed doctrines: `D10, D11, D12, D13, D14, D15, D16, D17, D17.5, D18, D19, D20, D21, D22, D23, D7, D8, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 0, 'missing_atoms': ['visual_asset_used'], 'value': 0.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D7', 'D8', 'D9'], 'verified': ['D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D7', 'D8', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Missing birth atoms: `visual_asset_used`

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-Visuals/ui_kits/control_room/mockData.js-class-0** (low, hypothesis): Detected pattern matching Class3 (soft enforcement comments) at line 81
- **PG-Visuals/ui_kits/control_room/mockData.js-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.