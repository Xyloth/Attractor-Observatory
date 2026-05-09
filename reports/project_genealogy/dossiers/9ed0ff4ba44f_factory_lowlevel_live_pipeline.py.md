# Dossier: `factory_lowlevel/live_pipeline.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/9ed0ff4ba44f_factory_lowlevel_live_pipeline.py.json`
- JSON content_hash: `sha256:9ca0e3c266b4c73edeb697b6ac6405b3d759d461dc28a920808ce4d4dd0c7ced`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `factory`
- Generated status: `source`
- Lines: 674 / Bytes: 29852

## Birth
- Status: `recovered`
- First-seen commit: `ff7a2adff3a2bcf5dbddec8e613b3a17dc69edfd`
- First-seen date: `2026-05-06T14:39:23-04:00`
- Spawn ticket: `TASK-033`
- Cohort: `TASK-033`

### Birth predicate atoms
- **factory_module_exposes_callable** — Module exposes runnable factory components consumed by the daemon/pipeline.
- **header_declared_intent** — TASK-033 multi-world Factory live runner.

This module leaves the Campaign 016 W-1/W0 runner unchanged and adds an
exploratory, source-bound path for higher-world ingestion into W1/W3/W6/W9/W11.
Runtime remains daemon code, not AI-in-the-loop: adapters fetch/parse, the
router validates, world constructors simulate, and formal lenses evaluate.

## Current
- Status: `recovered`
- Public symbols: `available_adapters, run_live_factory_cycle, summarize_run`
- Observed doctrines: `D29`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 21}, {'id': 'error_branch', 'line': 61}, {'id': 'error_branch', 'line': 572}, {'id': 'error_branch', 'line': 619}, {'id': 'error_branch', 'line': 642}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': 3.0}`
- **doctrine_binding_quality**: `{'required': ['D29'], 'verified': ['D29'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 1, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': ['public_tests/test_live_pipeline_world_traces.py'], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 6.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 6

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-factory_lowlevel/live_pipeline.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 21: except ModuleNotFoundError as exc:  # pragma: no cover - exercised by public-surface installs.
- **PG-factory_lowlevel/live_pipeline.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 61: except ModuleNotFoundError as exc:  # pragma: no cover - exercised by public-surface installs.
- **PG-factory_lowlevel/live_pipeline.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 547: if "/traces/" in normalized or normalized.endswith("/traces") or "/daemon_traces/" in normalized:
- **PG-factory_lowlevel/live_pipeline.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 572: except (OSError, json.JSONDecodeError):
- **PG-factory_lowlevel/live_pipeline.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 619: except OSError:
- **PG-factory_lowlevel/live_pipeline.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 642: except OSError as exc:
- **PG-factory_lowlevel/live_pipeline.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.