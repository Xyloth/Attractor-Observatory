# Dossier: `papers/methods/CAMPAIGN_021_MULTI_WORLD_FACTORY.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/aa31ad5ac50a_papers_methods_CAMPAIGN_021_MULTI_WORLD_FACTORY.md.json`
- JSON content_hash: `sha256:03107fa0bc27e537b6a4f9029de06601545a62a22a3b95c7ba6604fdf916a84e`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 84 / Bytes: 2998

## Birth
- Status: `recovered`
- First-seen commit: `ff7a2adff3a2bcf5dbddec8e613b3a17dc69edfd`
- First-seen date: `2026-05-06T14:39:23-04:00`
- Spawn ticket: `TASK-033`
- Cohort: `TASK-033`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — # Campaign 021 - Multi-World Factory Pilot
Task: TASK-033
Mode: exploratory
Claim promotion: closed pending C020 ontology/methodology repair
## Scope
Campaign 021 extends the autonomous Factory from the W-1/W0 floor into five
higher worlds:
- W1 CRN from KEGG E. coli K-12 MG1655 metabolic-network metadata
- W3 Field from peer-reviewed reaction-diffusion benchmark parameters
- W6 Ecosystem from GBI

## Current
- Status: `recovered`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
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
- **PG-papers/methods/CAMPAIGN_021_MULTI_WORLD_FACTORY.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.