# Dossier: `docs/doctrine_d27.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/c683cb824e7e_docs_doctrine_d27.md.json`
- JSON content_hash: `sha256:0377bcac1788632c73d081339f8f95f811e6e3a7a6fd47b2d9481c8fbba90016`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `doctrine`
- Generated status: `source`
- Lines: 34 / Bytes: 1317

## Birth
- Status: `recovered`
- First-seen commit: `2f804f0a8b912a3afbec90dbb1cdaf92162a612f`
- First-seen date: `2026-05-06T21:25:06-04:00`
- Spawn ticket: `DX-002`
- Cohort: `DX-002`

### Birth predicate atoms
- **binding_rule_named** — Document declares a binding doctrine rule with a numbered ID and ratification.
- **header_declared_intent** — # Doctrine D27 - Substantive Lens Recovery
Mode: foundational
Signed-by: James Dye (PI), Architect Claude, Codex 1.5x (TASK-MEAS-PLAN / TASK-DX-002-FIX)
D27 - A BAD motif-lens cell is not recovered by renaming a detector or moving
the same computation behind a new interface. A recovered lens must demonstrate a
substantive source-object split from the predicate, survive adversarial ablation,
and re

## Current
- Status: `recovered`
- Observed doctrines: `D27`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D27'], 'verified': ['D27'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['docs/doctrine_registry.json'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-docs/doctrine_d27.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.