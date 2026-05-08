# Dossier: `papers/methods/INGESTION_CONVERGENCE_CB008.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/207e4900f7b3_papers_methods_INGESTION_CONVERGENCE_CB008.md.json`
- JSON content_hash: `sha256:c3378e23682190ee582db215478202871a1cb82bd8a133a7345a7db2754a559e`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 253 / Bytes: 12362

## Birth
- Status: `recovered`
- First-seen commit: `e857373697552dd0ce702266d931384299ea053b`
- First-seen date: `2026-05-06T14:39:36-04:00`
- Spawn ticket: `CB-008`
- Cohort: `CB-008`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — # Ingestion Convergence Loop — CB-008 Methods
**Task ID:** TASK-CB-008
**Class:** ingestion_convergence_self_paced
**Branch:** `feature/cb-008-ingestion-convergence`
**Builder:** Claude (Builder), claude-sonnet-4.7-20260501
**Start EST:** 2026-05-06 05:46:44
**Stop EST:** 2026-05-06 (see `reports/campaign_022/convergence_session.json`)
**Timer cap:** 60 minutes
**Outcome:** **CONVERGED** — three c

## Current
- Status: `recovered`
- Observed doctrines: `D14, D17, D19, D22, D7, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17', 'D19', 'D22', 'D7', 'D9'], 'verified': ['D14', 'D17', 'D19', 'D22', 'D7', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-papers/methods/INGESTION_CONVERGENCE_CB008.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.