# Dossier: `docs/SAMPLE_CODE.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/7971969458e4_docs_SAMPLE_CODE.md.json`
- JSON content_hash: `sha256:d6dbaa7b3654c2e94e4b0c54652e599ae23dca5d8e70f8a7c4c496b1e467cf33`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `docs`
- Generated status: `source`
- Lines: 313 / Bytes: 17350

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **doc_serves_handbook** — Doc serves the project handbook (doctrine support, methodology, audit notes).

## Current
- Status: `recovered`
- Observed doctrines: `D14`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14'], 'verified': ['D14'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 2, 'dereferenceable_evidence_refs': 2, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['CONTRIBUTING.md'], 'weighted_value': 1.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 1
- Letter-vs-spirit surfaces: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-docs/SAMPLE_CODE.md-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 294: The earlier version of this function had per-benchmark arms that wrote to cell proteins directly: `if benchmark == "segm
- **PG-docs/SAMPLE_CODE.md-class-0** (low, hypothesis): Detected pattern matching Class6 (engineered prediction polynomial) at line 263
- **PG-docs/SAMPLE_CODE.md-class-1** (low, hypothesis): Detected pattern matching Class4 (scenario-internal benchmark branching) at line 294

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.