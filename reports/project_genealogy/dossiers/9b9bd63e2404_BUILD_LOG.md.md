# Dossier: `BUILD_LOG.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/9b9bd63e2404_BUILD_LOG.md.json`
- JSON content_hash: `sha256:e8b846126d1b9fda6db9c158a78e2ef2bf0228234ec9516ba56b560f9e91a2a0`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 3052 / Bytes: 202388

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.
- **header_declared_intent** — # Build Log
*Append-only chronological timeline of cross-builder work. Both Codex Builder and Claude Builder append. Architect Claude reads. The PI relays appends between builders when usage permits.*
*Two entry types:*
- **Work entry** â€” `[timestamp] [builder] [task_id] [pillar/sub-task]`. Started X, touching Y, estimated Z minutes. Posted at start of substantive work.
- **Talk entry** â€” `[ti

## Current
- Status: `recovered`
- Observed doctrines: `D10, D11, D12, D14, D15, D17, D17.5, D18, D19, D20, D21, D22, D23, D24, D25, D26, D27, D28, D29, D30, D31, D7, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 2597}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D10', 'D11', 'D12', 'D14', 'D15', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D7', 'D9'], 'verified': ['D10', 'D11', 'D12', 'D14', 'D15', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D7', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Letter-vs-spirit surfaces: 1

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-BUILD_LOG.md-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 2597: except PermissionError:  # <--- BUG: too narrow
- **PG-BUILD_LOG.md-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 795
- **PG-BUILD_LOG.md-class-1** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 937
- **PG-BUILD_LOG.md-class-2** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 975
- **PG-BUILD_LOG.md-class-3** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 995
- **PG-BUILD_LOG.md-class-4** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 1003
- **PG-BUILD_LOG.md-class-5** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 1007
- **PG-BUILD_LOG.md-class-6** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 1015
- **PG-BUILD_LOG.md-class-7** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 2963

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.