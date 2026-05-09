# Dossier: `project_telemetry/ai_builder_tasks.jsonl`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/103a14979228_project_telemetry_ai_builder_tasks.jsonl.json`
- JSON content_hash: `sha256:662164c6a0492c11a4f5e82e06b6f3397acd9a23668f61feee884155eeb48b61`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `telemetry`
- Generated status: `source`
- Lines: 112 / Bytes: 266669

## Birth
- Status: `recovered`
- First-seen commit: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`
- First-seen date: `2026-05-03T09:50:51-04:00`
- Spawn ticket: ``
- Cohort: `6f9bc89ea7eee60546eb6eb83d69eb3a01ecd01e`

### Birth predicate atoms
- **telemetry_record_appended** — File appends a telemetry record under a stable schema.

## Current
- Status: `recovered`
- Observed doctrines: `D11, D13, D14, D15, D16, D17, D17.5, D18, D19, D20, D21, D22, D23, D24, D25, D26, D27, D28, D29, D30, D31, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D13', 'D14', 'D15', 'D16', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D7'], 'verified': ['D11', 'D13', 'D14', 'D15', 'D16', 'D17', 'D17.5', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
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
- **PG-project_telemetry/ai_builder_tasks.jsonl-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 3
- **PG-project_telemetry/ai_builder_tasks.jsonl-class-1** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 11
- **PG-project_telemetry/ai_builder_tasks.jsonl-class-2** (low, hypothesis): Detected pattern matching Class3 (soft enforcement comments) at line 22
- **PG-project_telemetry/ai_builder_tasks.jsonl-class-3** (low, hypothesis): Detected pattern matching Class3 (soft enforcement comments) at line 23
- **PG-project_telemetry/ai_builder_tasks.jsonl-class-4** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 45
- **PG-project_telemetry/ai_builder_tasks.jsonl-class-5** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 50
- **PG-project_telemetry/ai_builder_tasks.jsonl-class-6** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 100

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.