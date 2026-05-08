# Dossier: `factory_lowlevel/progress.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/d07e75412ab4_factory_lowlevel_progress.py.json`
- JSON content_hash: `sha256:745141d5671c441f1f63a446d4f488783693f8b652eaf8ceac5338fb5fde1ed7`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `factory`
- Generated status: `source`
- Lines: 227 / Bytes: 8445

## Birth
- Status: `recovered`
- First-seen commit: `f1d7305d60c15c1177908245f22443d22cf86bf5`
- First-seen date: `2026-05-07T08:59:39-04:00`
- Spawn ticket: `CB-013`
- Cohort: `CB-013`

### Birth predicate atoms
- **factory_module_exposes_callable** — Module exposes runnable factory components consumed by the daemon/pipeline.
- **header_declared_intent** — Per-world ingestion progress tracking.

CB-013 T5: writes ``reports/<task_id>/ingestion_progress.json`` per
world per session so the BUILDER_INGESTION_MONITORING_PLAYBOOK can
report "W1 at 47%, last cycle clean, 5 routine audits" without
parsing the full session ledger.

Schema (``IngestionProgress.v1``)::

    {
        "schema": "IngestionProgress.v1",
        "world_family": "crn",
        "ses

## Current
- Status: `recovered`
- Public symbols: `load_target_densities, read_ingestion_progress, write_ingestion_progress`
- Observed doctrines: `D22`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 74}, {'id': 'error_branch', 'line': 184}, {'id': 'error_branch', 'line': 199}, {'id': 'error_branch', 'line': 218}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 2.0}`
- **doctrine_binding_quality**: `{'required': ['D22'], 'verified': ['D22'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['papers/methods/INGESTION_TARGETS.md'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 5

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-factory_lowlevel/progress.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 74: except OSError:
- **PG-factory_lowlevel/progress.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 86: m = re.match(r"\|\s*([a-z_][a-z0-9_]*)\s*\|\s*(\d+)\s*\|", line)
- **PG-factory_lowlevel/progress.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 184: except (OSError, json.JSONDecodeError):
- **PG-factory_lowlevel/progress.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 199: except (OSError, json.JSONDecodeError):
- **PG-factory_lowlevel/progress.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 218: except (OSError, json.JSONDecodeError):
- **PG-factory_lowlevel/progress.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.