# Dossier: `factory_lowlevel/_math_primitives_catalog.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/eb80ef2e0e30_factory_lowlevel__math_primitives_catalog.py.json`
- JSON content_hash: `sha256:6e9460c704f26383a3f9767aad131f0496d8134c2eb98229d5764c7644348b44`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `factory`
- Generated status: `source`
- Lines: 919 / Bytes: 137809

## Birth
- Status: `recovered`
- First-seen commit: `0f5947c275a05c6cfc48e149ca4e3cd1733039bd`
- First-seen date: `2026-05-07T12:23:48-04:00`
- Spawn ticket: `TASK-CB-015`
- Cohort: `TASK-CB-015`

### Birth predicate atoms
- **factory_module_exposes_callable** — Module exposes runnable factory components consumed by the daemon/pipeline.
- **header_declared_intent** — CB-015 T3 — 200-entry math primitives catalog.

200 canonical dynamical-system primitives drawn from peer-reviewed
literature. Every entry has a DOI to a primary source — Strogatz,
Guckenheimer & Holmes, Sprott (1994 + 1997), Kuznetsov, Pomeau &
Manneville, Chua, Lorenz, Rössler, Chen, Lu, etc.

This module is imported by ``factory_lowlevel/adapters.py``'s
``MATH_PRIMITIVE_SEEDS`` so the catalog c

## Current
- Status: `recovered`
- Observed doctrines: `D1, D2, D3, D4`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D1', 'D2', 'D3', 'D4'], 'verified': ['D1', 'D2', 'D3', 'D4'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-factory_lowlevel/_math_primitives_catalog.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.