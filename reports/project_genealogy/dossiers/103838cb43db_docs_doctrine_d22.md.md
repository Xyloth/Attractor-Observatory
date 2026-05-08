# Dossier: `docs/doctrine_d22.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/103838cb43db_docs_doctrine_d22.md.json`
- JSON content_hash: `sha256:0a74c6e225ee5d2a1adc24c515b40773ea8d1afb5707f7348b644db5841fffae`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `doctrine`
- Generated status: `source`
- Lines: 103 / Bytes: 5123

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **binding_rule_named** — Document declares a binding doctrine rule with a numbered ID and ratification.
- **header_declared_intent** — # Doctrine D22 — Empty rooms beat stocked rooms with mock data
Mode: foundational
Spec version: sha256:492dbee22a401cec8679bd325c1ba1145084b5b8848b9beaf6c9b050b3e45729
Signed-by: Architect Claude (TASK-CB-004 / Campaign 015 Phase 0)
Class watch: Class 12 candidate — Decorative Completeness
D22 — Honest absence over decorative completeness. When a Control Room view
(or any read-only project surface

## Current
- Status: `recovered`
- Observed doctrines: `D11, D17, D21, D22, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D17', 'D21', 'D22', 'D7'], 'verified': ['D11', 'D17', 'D21', 'D22', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md', 'docs/doctrine_registry.json'], 'weighted_value': 3.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-docs/doctrine_d22.md-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 12
- **PG-docs/doctrine_d22.md-class-1** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 18
- **PG-docs/doctrine_d22.md-class-2** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 34
- **PG-docs/doctrine_d22.md-class-3** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 72
- **PG-docs/doctrine_d22.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.