# Dossier: `papers/methods/SUBSTANCE_AUDIT_W13.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/1d9a14ed3f6f_papers_methods_SUBSTANCE_AUDIT_W13.md.json`
- JSON content_hash: `sha256:836bf209d156a241b75e8d456b655ba281d1faa17c16dd47de971ad702935fcf`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 39 / Bytes: 2653

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — # Substance Audit W13 Multiscale
Campaign: 008
Doctrine: D17.5
Measured simulation logic: 442 lines against an 800-line proxy floor
## v1.0 Section 3 components
- Real inner-world hosting: macro entities host live W1 CRN and W2 protocell worlds rather than scalar placeholders.
- Upscale operators: inner-world closure, boundary, mass, and division signals are projected into macro population/resourc

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
- **PG-papers/methods/SUBSTANCE_AUDIT_W13.md-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 9
- **PG-papers/methods/SUBSTANCE_AUDIT_W13.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.