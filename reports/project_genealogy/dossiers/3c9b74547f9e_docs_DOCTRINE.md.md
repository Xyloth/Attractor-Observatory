# Dossier: `docs/DOCTRINE.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/3c9b74547f9e_docs_DOCTRINE.md.json`
- JSON content_hash: `sha256:b46f02f6195cfeb2502f3db9b852637514f55ed3f58e51af53bdcada2d5376df`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `doctrine`
- Generated status: `source`
- Lines: 297 / Bytes: 21104

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **binding_rule_named** — Document declares a binding doctrine rule with a numbered ID and ratification.

## Current
- Status: `recovered`
- Observed doctrines: `D10, D11, D12, D13, D14, D15, D16, D17, D17.5, D18, D19, D20, D21, D22, D23, D24, D25, D26, D27, D28, D29, D30, D31, D7, D8, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D7', 'D8', 'D9'], 'verified': ['D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D7', 'D8', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['.architect_state_checkpoint.md', 'BUILD_LOG.md', 'CLAUDE_BUILDER_INITIATION.md', 'CLAUDE_FACTORY_INITIATION.md', 'CONTRIBUTING.md', 'FAIR_DATA_STEWARDSHIP.md', 'README.md', 'WAITING_TO_BE_PUBLISHED.md', 'docs/doctrine_registry.json', 'papers/methods/PROJECT_GENEALOGY_PG001_SPEC.md', 'reports/campaign_012/factory_initiation_pointer_audit.json', 'reports/campaign_012/factory_scaffolding.json', 'reports/task_032_dx001_disposition.json'], 'weighted_value': 19.5}`

## Drift
- Status: `positive_deepening`
- Letter-vs-spirit surfaces: 1

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-docs/DOCTRINE.md-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 59: **Failure mode caught:** `biology/shadow.py` was once `representability_score = 0.82 if trait in {hardcoded set of 5} el
- **PG-docs/DOCTRINE.md-class-0** (low, hypothesis): Detected pattern matching Class6 (engineered prediction polynomial) at line 51
- **PG-docs/DOCTRINE.md-class-1** (low, hypothesis): Detected pattern matching Class4 (scenario-internal benchmark branching) at line 95
- **PG-docs/DOCTRINE.md-class-2** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 163
- **PG-docs/DOCTRINE.md-class-3** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 165

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.