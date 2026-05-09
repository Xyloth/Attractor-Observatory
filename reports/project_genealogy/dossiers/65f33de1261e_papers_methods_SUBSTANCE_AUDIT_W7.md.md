# Dossier: `papers/methods/SUBSTANCE_AUDIT_W7.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/65f33de1261e_papers_methods_SUBSTANCE_AUDIT_W7.md.json`
- JSON content_hash: `sha256:b816ff0d696e409be4cdd6d3e5217f55cfc37733d4a5e6cca9783acce66cd9ed`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 44 / Bytes: 2863

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — # Substance Audit W7 Swarm
Campaign: 008
Doctrine: D17.5
Measured simulation logic: 478 lines against a 500-line proxy floor
## v1.0 Section 3 components
- Agent-environment coupling: agents sense pheromone, food, damage, nest, target, and communication fields on a spatial grid.
- Collective coordination: pheromone trails, communication pulses, local memory, role switching, and consensus targeting

## Current
- Status: `recovered`
- Observed doctrines: `D14, D17.5`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17.5'], 'verified': ['D14', 'D17.5'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BLOCKER-SH3-CAMPAIGN-008-STRICT-SUBSTANCE-FLOORS.md', 'CODEX_TASK_023_DRIVE.md', 'reports/campaign_012/cli_full_report.json', 'reports/campaign_012/full_report.json'], 'weighted_value': 6.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/methods/SUBSTANCE_AUDIT_W7.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.