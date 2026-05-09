# Dossier: `papers/falsification/DX-003/round_7_reproducers/telemetry_identity_probe.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/dbbeba9518e2_papers_falsification_DX-003_round_7_reproducers_telemetry_identity_probe.py.json`
- JSON content_hash: `sha256:63eee0c6c687c9282672d6975330f36e054406d386813fe87c988eace2a1a6d2`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `paper`
- Generated status: `source`
- Lines: 91 / Bytes: 5141

## Birth
- Status: `recovered`
- First-seen commit: `a434ca4f20e84c1af1a60954ab5d4ace4a5772d3`
- First-seen date: `2026-05-08T18:19:27-04:00`
- Spawn ticket: `DX-003`
- Cohort: `DX-003`

### Birth predicate atoms
- **paper_artifact_in_falsifier_or_prereg** — Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 14}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D18'], 'verified': [], 'claimed_only': ['D17', 'D18'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2
- Letter-vs-spirit surfaces: 4

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-papers/falsification/DX-003/round_7_reproducers/telemetry_identity_probe.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 14: except Exception as e:
- **PG-papers/falsification/DX-003/round_7_reproducers/telemetry_identity_probe.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 30: if str(r.get('acceptance_outcome','')).startswith('pass') and r.get('actual_minutes') is None and r.get('record_type') i
- **PG-papers/falsification/DX-003/round_7_reproducers/telemetry_identity_probe.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 36: m=re.search(pattern, readme)
- **PG-papers/falsification/DX-003/round_7_reproducers/telemetry_identity_probe.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 49: missing_from_build=[tid for tid in unique_tasks if tid and tid.startswith('TASK-') and tid not in mentioned]

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.