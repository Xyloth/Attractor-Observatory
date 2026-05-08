# Dossier: `control_room/README.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/c31018c4578c_control_room_README.md.json`
- JSON content_hash: `sha256:bc3056e223bcbabd568ebb13ec4ad4331791c4b7f04258e89f18729c207c55cb`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 99 / Bytes: 3706

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — # Observatory Control Room
Sidecar visualization layer for Attractor Observatory. Read-heavy,
branch-isolated, non-claim-bearing. Phase 0 (TASK-CB-004) ships the
foundation: app shell, design tokens, empty-state component (D22),
adapter layer, and read-only enforcement.
## Run it
```bash
pip install -r requirements.txt
streamlit run control_room/app.py
```
The app launches a local dark-mode dashbo

## Current
- Status: `recovered`
- Observed doctrines: `D21, D22, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 1, 'missing_atoms': ['control_room_surface_renders'], 'value': 0.5}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D21', 'D22', 'D7'], 'verified': ['D21', 'D22', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Missing birth atoms: `control_room_surface_renders`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/README.md-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 16
- **PG-control_room/README.md-class-1** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 39
- **PG-control_room/README.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.