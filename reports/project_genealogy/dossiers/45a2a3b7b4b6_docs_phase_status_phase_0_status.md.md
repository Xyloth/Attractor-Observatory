# Dossier: `docs/phase_status/phase_0_status.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/45a2a3b7b4b6_docs_phase_status_phase_0_status.md.json`
- JSON content_hash: `sha256:51adb55fc57ef3726d7155b7d503a8f93da8b486b88788107e75ae7bd36b6b9a`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `docs`
- Generated status: `source`
- Lines: 58 / Bytes: 2368

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **doc_serves_handbook** — Doc serves the project handbook (doctrine support, methodology, audit notes).
- **header_declared_intent** — # Phase 0 Status
Status after TASK-005.
## Foundations Roadmap
- Spec lineage: live.
- AI Operating System scaffold: live.
- Core kernel: live.
- Trace schema/writer/reader/verifier: live as Phase-0 JSON physical layout.
- Manifest/content hashing: live in core and trace writer.
- Provenance primitives: live in core.
- RNG discipline: live with Philox4x32-10 splitter and global RNG lint.
- Mode/st

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11'], 'verified': [], 'claimed_only': ['D11'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.