# Dossier: `CODEX_CAMPAIGN_007.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/846fbd123486_CODEX_CAMPAIGN_007.md.json`
- JSON content_hash: `sha256:404213d4516e696c6f2c428eb54defd64ce2c508f66ef9f1a07c7953889f23c5`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 384 / Bytes: 37404

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.
- **header_declared_intent** — # Codex — Campaign 007: Truth Pass and Substrate Reconstruction
*Architect message. Read in full before resuming. Canon for the duration of TASK-016 and beyond until the campaign exits.*
---
## 1. Where you stand
In Campaigns 001–006 you delivered:
- A real kernel, real trace plane, real Estimation Loop, real Hardening pillar.
- W1 CRN with DOPRI5 + Gillespie at production quality.
- W2 Protocell

## Current
- Status: `recovered`
- Observed doctrines: `D10, D11, D12, D13, D7, D8, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D10', 'D11', 'D12', 'D13', 'D7', 'D8', 'D9'], 'verified': ['D10', 'D11', 'D12', 'D13', 'D7', 'D8', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-CODEX_CAMPAIGN_007.md-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 24
- **PG-CODEX_CAMPAIGN_007.md-class-1** (low, hypothesis): Detected pattern matching Class6 (engineered prediction polynomial) at line 42
- **PG-CODEX_CAMPAIGN_007.md-class-2** (low, hypothesis): Detected pattern matching Class6 (engineered prediction polynomial) at line 368

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.