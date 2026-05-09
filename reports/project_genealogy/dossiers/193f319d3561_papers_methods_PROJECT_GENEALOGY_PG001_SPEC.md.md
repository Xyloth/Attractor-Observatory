# Dossier: `papers/methods/PROJECT_GENEALOGY_PG001_SPEC.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/193f319d3561_papers_methods_PROJECT_GENEALOGY_PG001_SPEC.md.json`
- JSON content_hash: `sha256:632bf121ff18a80bd3d20a9b2f73b478115bd777f9e368addf84f8576855a047`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 1037 / Bytes: 51501

## Birth
- Status: `recovered`
- First-seen commit: `f2013deb7d742a77a649743982a787c18dabc36c`
- First-seen date: `2026-05-08T14:22:13-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — # Project Genealogy PG-001 Spec v2.1
Status: launch specification for PG-001
Authoring passes:
- v2 (OG Builder / Codex): pushbacks on v1, atom-decomposed birth predicate, DepthVector.v1, typed temporal multigraph, evidence-lock pre-pass, full schemas, falsifiability protocol, doctrine bindings, mistake-class targeting, 15 acceptance gates
- v2.1 (Architect Claude): Project Mission and coherence P

## Current
- Status: `recovered`
- Observed doctrines: `D10, D11, D12, D13, D17, D17.5, D18, D19, D20, D22, D23, D24, D25, D26, D27, D29, D30, D31, D7, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D10', 'D11', 'D12', 'D13', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D29', 'D30', 'D31', 'D7', 'D9'], 'verified': ['D10', 'D11', 'D12', 'D13', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D29', 'D30', 'D31', 'D7', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/methods/PROJECT_GENEALOGY_PG001_SPEC.md-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 683
- **PG-papers/methods/PROJECT_GENEALOGY_PG001_SPEC.md-class-1** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 954

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.