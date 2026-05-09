# Dossier: `papers/methods/MULTISUBSTRATE_FLOOR_CONNECTIVITY.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/bc77a8574b79_papers_methods_MULTISUBSTRATE_FLOOR_CONNECTIVITY.md.json`
- JSON content_hash: `sha256:ed6ea2ef9d35c41846f246d6e4c77641130a5d648e56b3996fe736b501f62c2b`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `method`
- Generated status: `source`
- Lines: 152 / Bytes: 12719

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **method_documented** — Document records a method, prereg, or audit with locked instruments.
- **header_declared_intent** — # Multi-Substrate Floor Connectivity Test (v2: substrate-suitability-gated)
Task: TASK-CB-002 (Claude Builder Session 002)
Status: exploratory
Schema: `MultisubstrateFloorConnectivity.v2`
Content hash: `sha256:1dbe5ed2ee1ca02f71850a04f0c537de234e57b53c5e61d736d8e91f742a24fc`
Supersedes: TASK-CB-001 v1 report (`reports/campaign_013/multisubstrate_floor_connectivity.json`); v1 record preserved.
## S

## Current
- Status: `recovered`
- Observed doctrines: `D14, D15, D18, D21, D22, D7, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D15', 'D18', 'D21', 'D22', 'D7', 'D9'], 'verified': ['D14', 'D15', 'D18', 'D21', 'D22', 'D7', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md', 'CLAUDE_BUILDER_INITIATION.md', 'CODEX_AUDIT_002_CLAUDE_BUILDER_TASK_CB_002.md'], 'weighted_value': 4.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/methods/MULTISUBSTRATE_FLOOR_CONNECTIVITY.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.