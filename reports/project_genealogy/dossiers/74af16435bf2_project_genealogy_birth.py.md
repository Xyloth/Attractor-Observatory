# Dossier: `project_genealogy/birth.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/74af16435bf2_project_genealogy_birth.py.json`
- JSON content_hash: `sha256:e915f19c1a236e20da407935078561d59217dacd611ef383fda0cf4410a53ecc`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `audit_instrument`
- Generated status: `source`
- Lines: 579 / Bytes: 20354

## Birth
- Status: `recovered`
- First-seen commit: `2d3b03b3ca5b35945309f2264f5c8cf30d450697`
- First-seen date: `2026-05-08T15:48:43-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **audit_instrument_executes** — Module is part of the PG-001 audit instrument and exposes a callable surface.

## Current
- Status: `recovered`
- Public symbols: `commit_message, find_renames_for_file, first_commit_for_file, header_marker_block, python_module_docstring, reconstruct_birth`
- Observed doctrines: `D11, D12, D14, D17, D17.5, D18, D19, D20, D22, D23, D24, D29, D30, D7, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 122}, {'id': 'error_branch', 'line': 162}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D12', 'D14', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D22', 'D23', 'D24', 'D29', 'D30', 'D7', 'D9'], 'verified': ['D11', 'D12', 'D14', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D22', 'D23', 'D24', 'D29', 'D30', 'D7', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Letter-vs-spirit surfaces: 5

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-project_genealogy/birth.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 107: if line.startswith("R") and "\t" in line:
- **PG-project_genealogy/birth.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 118: if not rel_path.endswith(".py"):
- **PG-project_genealogy/birth.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 122: except OSError:
- **PG-project_genealogy/birth.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 130: if not s or s.startswith("#") or s.startswith("from __future__"):
- **PG-project_genealogy/birth.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 162: except OSError:
- **PG-project_genealogy/birth.py-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 259
- **PG-project_genealogy/birth.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.