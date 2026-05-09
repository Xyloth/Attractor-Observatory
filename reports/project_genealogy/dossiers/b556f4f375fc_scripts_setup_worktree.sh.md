# Dossier: `scripts/setup_worktree.sh`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/b556f4f375fc_scripts_setup_worktree.sh.json`
- JSON content_hash: `sha256:3f445b79274ced93b2b355ab675c6380dbc08c7fba8951ae21c03b972cd03edd`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `script`
- Generated status: `source`
- Lines: 64 / Bytes: 2327

## Birth
- Status: `recovered`
- First-seen commit: `f1d7305d60c15c1177908245f22443d22cf86bf5`
- First-seen date: `2026-05-07T08:59:39-04:00`
- Spawn ticket: `CB-013`
- Cohort: `CB-013`

### Birth predicate atoms
- **script_executes_purposefully** — Script automates a declared developer workflow.
- **header_declared_intent** — #!/usr/bin/env bash
# ============================================================================
# CB-013 T1 — setup_worktree.sh
#
# POSIX equivalent of setup_worktree.bat. Copies private (git-ignored)
# modules from the main checkout into a newly-created git worktree so
# the daemon and the Control Room can import them.
#
# Usage from a fresh worktree:
#   scripts/setup_worktree.sh
#   scripts/

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': [], 'verified': [], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.