# Dossier: `control_room/components/chrome.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/439744915b57_control_room_components_chrome.py.json`
- JSON content_hash: `sha256:2957ae47182d97072cbc50790e507ff2399dc690cd5aad62d446995390fc3cc7`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 399 / Bytes: 17199

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.

## Current
- Status: `recovered`
- Public symbols: `agent_chip, doctrine_tablet, event_row, gate_grid, metric_card, needs_attention, panel, pill_class, render_html, room_emblem`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 85}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.5}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2
- Letter-vs-spirit surfaces: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/components/chrome.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 85: except (OSError, UnicodeDecodeError):
- **PG-control_room/components/chrome.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 338: f'background:{"var(--verified)" if status == "green" else "var(--warning)" if status in ("in_progress", "yellow") else "
- **PG-control_room/components/chrome.py-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 15
- **PG-control_room/components/chrome.py-class-1** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 164

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.