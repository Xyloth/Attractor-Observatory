# Dossier: `project_genealogy/atlas.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/d442c7ec6b5e_project_genealogy_atlas.py.json`
- JSON content_hash: `sha256:8faa5dd02752726cde135cd0e2c323ffc32c8e285baca7222378d86717564e4b`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `audit_instrument`
- Generated status: `source`
- Lines: 204 / Bytes: 8519

## Birth
- Status: `recovered`
- First-seen commit: `2896e0e1027b545c467428fe13baa4e13b019772`
- First-seen date: `2026-05-08T15:49:14-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **audit_instrument_executes** — Module is part of the PG-001 audit instrument and exposes a callable surface.

## Current
- Status: `recovered`
- Public symbols: `build_atlas, write_atlas`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 91}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D19', 'D20'], 'verified': [], 'claimed_only': ['D11', 'D19', 'D20'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 3, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 1

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-project_genealogy/atlas.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 91: except (OSError, json.JSONDecodeError):
- **PG-project_genealogy/atlas.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.