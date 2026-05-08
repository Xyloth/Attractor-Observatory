# Dossier: `papers/methods/METHODOLOGY_VALIDATION_CB003.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/9297c00a2d04_papers_methods_METHODOLOGY_VALIDATION_CB003.md.json`
- JSON content_hash: `sha256:bf287656777415969d74fd7feee07065d581f4ab0d66cd28f8f16c58191e36e0`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 130 / Bytes: 11161

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — # Methodology Validation: TASK-CB-003
Task: TASK-CB-003 (Claude Builder Session 003)
Status: exploratory
Locked instruments: Campaign 009 BFG-PR basis `sha256:ce9e24...`; Campaign 010 lens registry `sha256:7c325d...`. Verified before each control ran.
## Headline finding
- **Adversarial control** (motif.replication_lineage.draft × graph, K2 coverage 0.959240): **`methodology_sound`**. formal_gap =

## Current
- Status: `recovered`
- Observed doctrines: `D14, D18, D21, D22, D7, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D18', 'D21', 'D22', 'D7', 'D9'], 'verified': ['D14', 'D18', 'D21', 'D22', 'D7', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['.architect_state_checkpoint.md', 'BUILD_LOG.md', 'TASK-CB-003_METHODOLOGY_VALIDATION.md'], 'weighted_value': 4.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/methods/METHODOLOGY_VALIDATION_CB003.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.