# Dossier: `control_room/rooms/portfolio_demo.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/f069c0421c33_control_room_rooms_portfolio_demo.py.json`
- JSON content_hash: `sha256:ecfee7efafab9887254ff07359e4294ae0937dd6b6f9a600ef5430dd294f123e`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 888 / Bytes: 41696

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — Portfolio / Demo Mode — proposal §7.10.

Full CB-007 implementation. The room is the public face of the
Observatory: a curated 6-scene demo walk-through that explains the
project to a recruiter, hiring manager, or external collaborator in
under 60 seconds.

Components:

1. Project overview slide — single composed view with the project thesis.
2. Architecture diagram — inline SVG of the four planes

## Current
- Status: `recovered`
- Public symbols: `render, write_readme_assets_manifest`
- Observed doctrines: `D14, D17, D22, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 251}, {'id': 'error_branch', 'line': 268}, {'id': 'error_branch', 'line': 286}, {'id': 'error_branch', 'line': 346}, {'id': 'error_branch', 'line': 354}, {'id': 'error_branch', 'line': 361}, {'id': 'error_branch', 'line': 459}, {'id': 'error_branch', 'line': 480}, {'id': 'error_branch', 'line': 493}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': 5.0}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17', 'D22', 'D7'], 'verified': ['D14', 'D17', 'D22', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 1, 'imports_out': 11, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 7.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2
- Letter-vs-spirit surfaces: 12

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/rooms/portfolio_demo.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 251: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/portfolio_demo.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 268: except OSError:
- **PG-control_room/rooms/portfolio_demo.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 286: except OSError:
- **PG-control_room/rooms/portfolio_demo.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 346: except OSError:
- **PG-control_room/rooms/portfolio_demo.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 354: except OSError:
- **PG-control_room/rooms/portfolio_demo.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 361: except OSError:
- **PG-control_room/rooms/portfolio_demo.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 412: if p.is_dir() and p.name.startswith("campaign_"):
- **PG-control_room/rooms/portfolio_demo.py-lvs-7** (info, hypothesis): Detected letter-coupled fix surface at line 459: except OSError:
- **PG-control_room/rooms/portfolio_demo.py-lvs-8** (info, hypothesis): Detected letter-coupled fix surface at line 480: except OSError:
- **PG-control_room/rooms/portfolio_demo.py-lvs-9** (info, hypothesis): Detected letter-coupled fix surface at line 493: except OSError:
- **PG-control_room/rooms/portfolio_demo.py-lvs-10** (info, hypothesis): Detected letter-coupled fix surface at line 561: if kind == "motif":
- **PG-control_room/rooms/portfolio_demo.py-lvs-11** (info, hypothesis): Detected letter-coupled fix surface at line 600: if kind == "motif":
- **PG-control_room/rooms/portfolio_demo.py-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 31

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.