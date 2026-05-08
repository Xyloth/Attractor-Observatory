# Dossier: `scripts/SETUP_WORKTREE.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/03e4f5c910da_scripts_SETUP_WORKTREE.md.json`
- JSON content_hash: `sha256:dca89c88b7f4bf1f1cb0fb7349a737d2d90a38b7a15c4355dac5fc2d6c8ad8d4`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `script`
- Generated status: `source`
- Lines: 89 / Bytes: 3226

## Birth
- Status: `recovered`
- First-seen commit: `f1d7305d60c15c1177908245f22443d22cf86bf5`
- First-seen date: `2026-05-07T08:59:39-04:00`
- Spawn ticket: `CB-013`
- Cohort: `CB-013`

### Birth predicate atoms
- **script_executes_purposefully** — Script automates a declared developer workflow.

## Current
- Status: `recovered`
- Observed doctrines: `D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D9'], 'verified': ['D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.