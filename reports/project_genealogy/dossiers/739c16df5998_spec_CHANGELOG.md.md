# Dossier: `spec/CHANGELOG.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/739c16df5998_spec_CHANGELOG.md.json`
- JSON content_hash: `sha256:247c2db3ab9843202a2badc98acb13305302f902da2612a0d9409e3feaf45c45`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `spec`
- Generated status: `source`
- Lines: 67 / Bytes: 3428

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **spec_states_acceptance** — Spec carries acceptance gates with measurable comparisons.
- **header_declared_intent** — # Spec Changelog
This changelog records the content-addressed lineage for the Attractor Observatory specs. `The Attractor Observatory v1.2.md` is the active canonical spec. When documents conflict, v1.2 wins; when v1.2 is silent, defer to v1.1, then v1.0.
Hash policy: SHA-256 over raw file bytes as present in this workspace at TASK-001 time.
## Active Spec
- Active: `spec-v1.2`
- File: `The Attrac

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D12', 'D9'], 'verified': [], 'claimed_only': ['D12', 'D9'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.