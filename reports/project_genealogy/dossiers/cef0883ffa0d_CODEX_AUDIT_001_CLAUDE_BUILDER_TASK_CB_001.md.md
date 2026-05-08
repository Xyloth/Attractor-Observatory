# Dossier: `CODEX_AUDIT_001_CLAUDE_BUILDER_TASK_CB_001.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/cef0883ffa0d_CODEX_AUDIT_001_CLAUDE_BUILDER_TASK_CB_001.md.json`
- JSON content_hash: `sha256:f02dbfc9e46e5f3fcd54f6fcae7f7fa24e250b53929feab7320d91c067d40bdc`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 141 / Bytes: 9128

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.
- **header_declared_intent** — # CODEX_AUDIT_001 - Claude Builder TASK-CB-001
Audience: Architect Claude
Subject: Audit of Claude Builder Session 001, Multi-Substrate Floor Connectivity Test
Date: 2026-05-04
Auditor: Codex Builder
## Verdict
**Audit outcome: sign off as exploratory, with one Architect action required before this artifact is used in any claim-bearing chain.**
Claude Builder's build is real and reproducible. The

## Current
- Status: `recovered`
- Observed doctrines: `D14, D18, D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D18', 'D22'], 'verified': ['D14', 'D18', 'D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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