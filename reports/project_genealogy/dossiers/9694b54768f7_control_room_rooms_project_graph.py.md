# Dossier: `control_room/rooms/project_graph.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/9694b54768f7_control_room_rooms_project_graph.py.json`
- JSON content_hash: `sha256:66812f216157b5fd6a884f290cf686bf37c20569242cc9a000610d51a96412d3`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 681 / Bytes: 30351

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
- Public symbols: `render`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 471}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': 1.0}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 1, 'imports_out': 10, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 7.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2
- Letter-vs-spirit surfaces: 11

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-control_room/rooms/project_graph.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 273: status_name = "verified" if density == "claim_ready_densified" else "warning" if density == "exploratory_densified" else
- **PG-control_room/rooms/project_graph.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 333: if motif_label == "floor_conn":
- **PG-control_room/rooms/project_graph.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 337: elif motif_label == "memory":
- **PG-control_room/rooms/project_graph.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 340: elif motif_label == "boundary":
- **PG-control_room/rooms/project_graph.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 342: elif motif_label == "lineage":
- **PG-control_room/rooms/project_graph.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 345: elif motif_label == "closure":
- **PG-control_room/rooms/project_graph.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 369: status_name = "verified" if mode == "foundational" else "warning"
- **PG-control_room/rooms/project_graph.py-lvs-7** (info, hypothesis): Detected letter-coupled fix surface at line 471: except (OSError, UnicodeDecodeError):
- **PG-control_room/rooms/project_graph.py-lvs-8** (info, hypothesis): Detected letter-coupled fix surface at line 481: cm = re.search(r"campaign_(\d+)", target_path)
- **PG-control_room/rooms/project_graph.py-lvs-9** (info, hypothesis): Detected letter-coupled fix surface at line 639: if node_type == "agent":
- **PG-control_room/rooms/project_graph.py-lvs-10** (info, hypothesis): Detected letter-coupled fix surface at line 647: size=22 if node_type in {"campaign", "world"} else 16,

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.