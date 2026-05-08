# Dossier: `docs/doctrine_d19_d21.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/dd1dde0ca8f9_docs_doctrine_d19_d21.md.json`
- JSON content_hash: `sha256:8e3366878f0a1f370409f12771ba2a98af5214785b00910d96ad469a82e795c9`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `doctrine`
- Generated status: `source`
- Lines: 22 / Bytes: 1095

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **binding_rule_named** — Document declares a binding doctrine rule with a numbered ID and ratification.
- **header_declared_intent** — # Doctrine D19-D21: Evidence Sourcing and Densification
Mode: foundational
Spec version: sha256:492dbee22a401cec8679bd325c1ba1145084b5b8848b9beaf6c9b050b3e45729
Signed-by: Codex Builder
D19 - Source-bound extraction. No biological, ecological, or trait-derived
variable may be promoted beyond exploratory status unless it is bound to a
source, provenance record, license class, extraction path, and a

## Current
- Status: `recovered`
- Observed doctrines: `D19, D20, D21`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D19', 'D20', 'D21'], 'verified': ['D19', 'D20', 'D21'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['.architect_state_checkpoint.md', 'CLAUDE_BUILDER_INITIATION.md', 'CLAUDE_FACTORY_INITIATION.md', 'CODEX_TASK_023_DRIVE.md', 'WAITING_TO_BE_PUBLISHED.md', 'docs/doctrine_registry.json', 'reports/campaign_011/cli_full_report.json', 'reports/campaign_011/full_report.json', 'reports/campaign_012/factory_initiation_pointer_audit.json', 'reports/campaign_012/factory_scaffolding.json'], 'weighted_value': 15.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-docs/doctrine_d19_d21.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.