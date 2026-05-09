# Dossier: `docs/doctrine_d29.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/4e6e5ccbcec1_docs_doctrine_d29.md.json`
- JSON content_hash: `sha256:1de6b0cb88f1d4e15370bb5877d57275121d607679d013bf0808e889d188f184`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `doctrine`
- Generated status: `source`
- Lines: 27 / Bytes: 1277

## Birth
- Status: `recovered`
- First-seen commit: `2f804f0a8b912a3afbec90dbb1cdaf92162a612f`
- First-seen date: `2026-05-06T21:25:06-04:00`
- Spawn ticket: `DX-002`
- Cohort: `DX-002`

### Birth predicate atoms
- **binding_rule_named** — Document declares a binding doctrine rule with a numbered ID and ratification.
- **header_declared_intent** — # Doctrine D29 - Runnable Evidence
Mode: foundational
Signed-by: Codex 1.5x (TASK-DX-002-FIX), under PI/Architect ratification
D29 - Reports naming enforcement modules, executable lenses, runtime paths, or
implementation files must either ship the named code in the public branch, mark
each citation as `evidence_private: true` / `private_unshipped` at point of use,
or downgrade the citation to narr

## Current
- Status: `recovered`
- Observed doctrines: `D29`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D29'], 'verified': ['D29'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['docs/doctrine_registry.json'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-docs/doctrine_d29.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.