# Dossier: `papers/methods/SUBSTANCE_AUDIT_W6.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/698541ec3964_papers_methods_SUBSTANCE_AUDIT_W6.md.json`
- JSON content_hash: `sha256:901cbe358b987b52bf38bf67a199b1c2b7d6ff5f35319e677a08aad30078bbf0`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 39 / Bytes: 2586

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — # Substance Audit W6 Ecosystem
Campaign: 008
Doctrine: D17.5
Measured simulation logic: 484 lines against a 500-line proxy floor
## v1.0 Section 3 components
- Multi-trophic patch population dynamics: producers, grazers, predators, decomposers, and regenerating abiotic resource are updated in every patch.
- Spatial coupling: dispersal and interaction-radius pressure couple neighboring patches with

## Current
- Status: `recovered`
- Observed doctrines: `D14, D17.5`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17.5'], 'verified': ['D14', 'D17.5'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BLOCKER-SH3-CAMPAIGN-008-STRICT-SUBSTANCE-FLOORS.md'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/methods/SUBSTANCE_AUDIT_W6.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.