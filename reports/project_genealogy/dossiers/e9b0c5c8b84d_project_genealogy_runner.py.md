# Dossier: `project_genealogy/runner.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/e9b0c5c8b84d_project_genealogy_runner.py.json`
- JSON content_hash: `sha256:7cd79f7e57df34c636f628666a3bbaa333cfcc22a395ca8a7e8a8068879e2f7b`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `audit_instrument`
- Generated status: `source`
- Lines: 230 / Bytes: 8824

## Birth
- Status: `recovered`
- First-seen commit: `2896e0e1027b545c467428fe13baa4e13b019772`
- First-seen date: `2026-05-08T15:49:14-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **audit_instrument_executes** — Module is part of the PG-001 audit instrument and exposes a callable surface.
- **header_declared_intent** — End-to-end runner for PG-001 passes.

Public entry points (called by ``project_genealogy.__main__``):

* ``run_prepass`` — write input_manifest.json
* ``run_pass1`` — build structural graph (in-memory; consumed by Pass 2/3)
* ``run_pass2`` — produce per-file dossiers
* ``run_pass3`` — assemble atlas + ``atlas_latest.json``
* ``run_pass4`` — produce coherence report + ``coherence_latest.json``
* ``

## Current
- Status: `recovered`
- Public symbols: `run_all, run_pass1, run_pass2, run_pass3, run_pass4, run_prepass`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 71}, {'id': 'error_branch', 'line': 92}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D19', 'D20'], 'verified': [], 'claimed_only': ['D11', 'D19', 'D20'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 2, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 1.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 2

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-project_genealogy/runner.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 71: except Exception as e:  # noqa: BLE001
- **PG-project_genealogy/runner.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 92: except Exception:  # noqa: BLE001
- **PG-project_genealogy/runner.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.