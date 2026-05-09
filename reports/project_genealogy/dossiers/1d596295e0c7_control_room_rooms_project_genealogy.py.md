# Dossier: `control_room/rooms/project_genealogy.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/1d596295e0c7_control_room_rooms_project_genealogy.py.json`
- JSON content_hash: `sha256:361285f186b91ed9e9ca006f51fc68c1e5a013d84954eee0fd3d990d9ae7ff54`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `control_room`
- Generated status: `source`
- Lines: 580 / Bytes: 21706

## Birth
- Status: `recovered`
- First-seen commit: `01c6c38479151939d0f7c2be30f4d79df6f1bb7e`
- First-seen date: `2026-05-08T15:49:33-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **control_room_surface_renders** — Module renders a Control Room surface with honest empty state.
- **header_declared_intent** — Project Genealogy — Mission Control room (PG-001 v1).

The room renders the published ``ProjectGenealogyAtlas.v1`` and
``ProjectCoherenceReport.v1`` artifacts from
``reports/project_genealogy/`` per the spec's
§"Mission Control Integration". It does not run the audit; reruns are
CLI-only in v1 (``python -m project_genealogy run-all``).

D22 binding: when atlas or coherence artifacts are missing, t

## Current
- Status: `recovered`
- Public symbols: `render`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 113}, {'id': 'error_branch', 'line': 552}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 1.0}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 1, 'imports_out': 6, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 6.5}`

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
- **PG-control_room/rooms/project_genealogy.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 113: except (OSError, json.JSONDecodeError):
- **PG-control_room/rooms/project_genealogy.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 552: except (OSError, json.JSONDecodeError):

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.