# Dossier: `project_genealogy/graph.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/fab23c405472_project_genealogy_graph.py.json`
- JSON content_hash: `sha256:d657d67d1c712d9e305e4d64eb916a93108449973a9534e937d496764320346a`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `audit_instrument`
- Generated status: `source`
- Lines: 402 / Bytes: 15506

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
- Public symbols: `StructuralGraph, build_structural_graph, edge_id, import_to_repo_path`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 374}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D19', 'D20'], 'verified': [], 'claimed_only': ['D11', 'D19', 'D20'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

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
- **PG-project_genealogy/graph.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 259: if not rel.startswith("public_tests/"):
- **PG-project_genealogy/graph.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 374: except OSError:
- **PG-project_genealogy/graph.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.