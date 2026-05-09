# Dossier: `formalism/floor_bfg/read_separation.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/bbac849b832d_formalism_floor_bfg_read_separation.py.json`
- JSON content_hash: `sha256:23f52580ebb6b0b8bfc70abe89a65575000539506293fddf0d86a811b6872e34`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `other`
- Generated status: `source`
- Lines: 181 / Bytes: 7678

## Birth
- Status: `recovered`
- First-seen commit: `20c8c938e8f7e7abf1af4a8348c0983ddae455de`
- First-seen date: `2026-05-09T07:11:04-04:00`
- Spawn ticket: `TASK-CB-022`
- Cohort: `TASK-CB-022`

### Birth predicate atoms
- **tracked_artifact_present** — File is tracked under git but does not match a higher-priority family.
- **header_declared_intent** — AST-level D31 read-separation checks.

## Current
- Status: `recovered`
- Public symbols: `assert_d31_read_separation, d31_import_denylist`
- Observed doctrines: `D29, D31`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D29', 'D31'], 'verified': ['D29', 'D31'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Letter-vs-spirit surfaces: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-formalism/floor_bfg/read_separation.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 77: if func_name in {"importlib.import_module", "__import__"}:
- **PG-formalism/floor_bfg/read_separation.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 80: if func_name == "getattr" and len(args) >= 2:

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.