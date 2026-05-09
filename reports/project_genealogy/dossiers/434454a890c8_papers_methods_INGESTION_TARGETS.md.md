# Dossier: `papers/methods/INGESTION_TARGETS.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/434454a890c8_papers_methods_INGESTION_TARGETS.md.json`
- JSON content_hash: `sha256:8e47c806fea7898cf22ab8d4efe2eabff51468102635a6cf5d23c26bb4bf3b68`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 223 / Bytes: 16244

## Birth
- Status: `recovered`
- First-seen commit: `f1d7305d60c15c1177908245f22443d22cf86bf5`
- First-seen date: `2026-05-07T08:59:39-04:00`
- Spawn ticket: `CB-013`
- Cohort: `CB-013`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — ﻿# Ingestion Targets v2 â€” Phase 2 mass density
**Status:** **RATIFIED** â€” Phase 2 mass-density targets per PI delegated authority (CB-018).
Phase 1 (v1, ratified 2026-05-07T14:07:39Z, total 6,653 records) is
the prior substantive baseline. Phase 2 (v2, ratified 2026-05-07,
total ~60,000 records) drives unattended ingestion to ~9Ã— Phase 1
density across the lower worlds and orthogonal substant

## Current
- Status: `recovered`
- Observed doctrines: `D14, D17, D17.5, D22, D26`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17', 'D17.5', 'D22', 'D26'], 'verified': ['D14', 'D17', 'D17.5', 'D22', 'D26'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILDER_LAUNCH_PROTOCOL.md', 'BUILD_LOG.md'], 'weighted_value': 3.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/methods/INGESTION_TARGETS.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.