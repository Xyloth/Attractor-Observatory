# Dossier: `factory_daemon.bat`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/597b66abe84a_factory_daemon.bat.json`
- JSON content_hash: `sha256:e777576f0ddc79ffb3745a07ffc03185096c9474b2cea5962628f7cd6db1ecda`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `root_artifact`
- Generated status: `source`
- Lines: 48 / Bytes: 1850

## Birth
- Status: `recovered`
- First-seen commit: `b8473aa3ed840989f6dce967fc460df34c7eed60`
- First-seen date: `2026-05-06T19:23:03-04:00`
- Spawn ticket: `TASK-MOTIF-IMPL`
- Cohort: `TASK-MOTIF-IMPL`

### Birth predicate atoms
- **root_artifact_serves_repo** — Top-level artifact serves a repo-wide convention (license, citation, ignore, requirements, container).
- **header_declared_intent** — @echo off
REM ===========================================================================
REM factory_daemon.bat — Windows entry point for the continuous Factory daemon.
REM
REM CB-013 T1: fail-fast check for required runtime modules.
REM Without formalism/, worlds/, or trace/ on disk, the daemon's import
REM chain crashes with ModuleNotFoundError. Surface that BEFORE starting
REM the daemon proce

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