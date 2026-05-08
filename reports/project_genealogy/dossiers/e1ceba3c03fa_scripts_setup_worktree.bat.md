# Dossier: `scripts/setup_worktree.bat`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/e1ceba3c03fa_scripts_setup_worktree.bat.json`
- JSON content_hash: `sha256:17db3f3bc44e15d761d0faceca0135ce4e740a2e3797af258ec7cbb616fecb77`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `script`
- Generated status: `source`
- Lines: 72 / Bytes: 2772

## Birth
- Status: `recovered`
- First-seen commit: `f1d7305d60c15c1177908245f22443d22cf86bf5`
- First-seen date: `2026-05-07T08:59:39-04:00`
- Spawn ticket: `CB-013`
- Cohort: `CB-013`

### Birth predicate atoms
- **script_executes_purposefully** — Script automates a declared developer workflow.
- **header_declared_intent** — @echo off
REM ===========================================================================
REM CB-013 T1 — setup_worktree.bat
REM
REM Copies private (git-ignored) modules from the main checkout into a
REM newly-created git worktree so the daemon and the Control Room
REM can import them. The .gitignore implementation-module list keeps
REM these directories private to each working copy; fresh worktre

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