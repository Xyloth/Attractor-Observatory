# Dossier: `project_genealogy/__init__.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/0ac5905682da_project_genealogy___init__.py.json`
- JSON content_hash: `sha256:7a68fe344d633d3f59b5d44f1019023c946e6be9e4967fbb784c1bc5af9b3dd1`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `audit_instrument`
- Generated status: `source`
- Lines: 49 / Bytes: 1698

## Birth
- Status: `recovered`
- First-seen commit: `b37c7b68e73883b45ef91df2e9d2bb5d799bdff6`
- First-seen date: `2026-05-08T15:48:24-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **audit_instrument_executes** — Module is part of the PG-001 audit instrument and exposes a callable surface.
- **header_declared_intent** — Project Genealogy PG-001 — source-bound, doctrine-aware genealogy.

Public surfaces:

* :mod:`project_genealogy.manifest` — pre-pass evidence-lock manifest.
* :mod:`project_genealogy.birth` — birth predicate reconstruction.
* :mod:`project_genealogy.current` — current predicate extraction.
* :mod:`project_genealogy.graph` — structural genealogy / atlas builder.
* :mod:`project_genealogy.drift` — d

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D19', 'D20'], 'verified': [], 'claimed_only': ['D11', 'D19', 'D20'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 13, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 26.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-project_genealogy/__init__.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.