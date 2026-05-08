# Dossier: `papers/methods/FLOOR_CORPUS_FOUNDRY_C014.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/e3b414778c0e_papers_methods_FLOOR_CORPUS_FOUNDRY_C014.md.json`
- JSON content_hash: `sha256:380cc54d29b9c7f9d6e61fca271727b7df3f5ba7f9a3d11d0e03c07eb6f9132e`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 74 / Bytes: 4128

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — # Campaign 014: Floor Corpus Foundry v0
> **DX-002 public runtime boundary:** References to `formalism/*`, `trace/*`, `worlds/*`, `motifs/*`, or `validation/*` in this document are narrative or private-runtime evidence unless a shipped public file is explicitly linked. The executable implementation is held outside the public branch; citations to private paths are governed by D29 and should be read

## Current
- Status: `recovered`
- Observed doctrines: `D14, D18, D21, D29`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D18', 'D21', 'D29'], 'verified': ['D14', 'D18', 'D21', 'D29'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['papers/methods/FLOOR_CONNECTIVITY_PREDICATE_SPLIT.md', 'reports/campaign_014/full_report.json'], 'weighted_value': 3.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/methods/FLOOR_CORPUS_FOUNDRY_C014.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.