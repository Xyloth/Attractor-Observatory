# Dossier: `factory_lowlevel/hardening.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/01a389fab74d_factory_lowlevel_hardening.py.json`
- JSON content_hash: `sha256:2fa479d988d91452df5a02cdd131a086ede38648e3da2cc781a64a115f1244db`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `factory`
- Generated status: `source`
- Lines: 640 / Bytes: 25911

## Birth
- Status: `recovered`
- First-seen commit: `ff7a2adff3a2bcf5dbddec8e613b3a17dc69edfd`
- First-seen date: `2026-05-06T14:39:23-04:00`
- Spawn ticket: `TASK-033`
- Cohort: `TASK-033`

### Birth predicate atoms
- **factory_module_exposes_callable** — Module exposes runnable factory components consumed by the daemon/pipeline.

## Current
- Status: `recovered`
- Public symbols: `FactoryRunLock, HardeningAuditQueue, LiveModeConfig, PartialResponseError, SchemaMismatchError, TransientFetchError, cache_age_seconds, cadence_to_seconds, fetch_with_policy, load_source_cache_entries`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 145}, {'id': 'error_branch', 'line': 317}, {'id': 'error_branch', 'line': 326}, {'id': 'error_branch', 'line': 334}, {'id': 'error_branch', 'line': 344}, {'id': 'error_branch', 'line': 492}, {'id': 'error_branch', 'line': 579}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': 4.0}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17.5', 'D7'], 'verified': [], 'claimed_only': ['D14', 'D17.5', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 8

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-factory_lowlevel/hardening.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 145: except FileExistsError:
- **PG-factory_lowlevel/hardening.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 317: except PartialResponseError as exc:
- **PG-factory_lowlevel/hardening.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 326: except SchemaMismatchError as exc:
- **PG-factory_lowlevel/hardening.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 334: except TimeoutError as exc:
- **PG-factory_lowlevel/hardening.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 344: except TransientFetchError as exc:
- **PG-factory_lowlevel/hardening.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 398: if str(warning).startswith("detector_anomaly:"):
- **PG-factory_lowlevel/hardening.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 492: except TypeError:
- **PG-factory_lowlevel/hardening.py-lvs-7** (info, hypothesis): Detected letter-coupled fix surface at line 579: except (KeyError, ValueError, TypeError) as exc:
- **PG-factory_lowlevel/hardening.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.