# Dossier: `factory_lowlevel/memory_guard.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/e4271e34fb6e_factory_lowlevel_memory_guard.py.json`
- JSON content_hash: `sha256:1999c16e1368e6ba64813bd5858259a3c27a02aecae0d79a49198777e806dcee`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `factory`
- Generated status: `source`
- Lines: 235 / Bytes: 9078

## Birth
- Status: `recovered`
- First-seen commit: `eada8c9bab091a8e21b021537c65a845709c2a6a`
- First-seen date: `2026-05-08T16:57:19-04:00`
- Spawn ticket: `TASK-CB-021`
- Cohort: `TASK-CB-021`

### Birth predicate atoms
- **factory_module_exposes_callable** — Module exposes runnable factory components consumed by the daemon/pipeline.
- **header_declared_intent** — CB-021 memory-safety guardrails for the Factory daemon.

The 2026-05-08 incident (factory-daemon-incident-report-2026-05-08.md)
documented the daemon eating 40-50 GB of RSS in one long-lived Python
process and white-screening the desktop. The architectural fixes
(sharded persistence, per-source child processes, SQLite migration)
are deferred to a separate ticket; this module ships the
*guardrails*

## Current
- Status: `recovered`
- Public symbols: `MemorySnapshot, check_memory_budget, consume_stop_flag, measure_memory, read_stop_flag`
- Observed doctrines: `D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 76}, {'id': 'error_branch', 'line': 78}, {'id': 'error_branch', 'line': 85}, {'id': 'error_branch', 'line': 92}, {'id': 'error_branch', 'line': 225}, {'id': 'error_branch', 'line': 234}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': 3.5}`
- **doctrine_binding_quality**: `{'required': ['D9'], 'verified': ['D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

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
- **PG-factory_lowlevel/memory_guard.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 76: except ImportError:
- **PG-factory_lowlevel/memory_guard.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 78: except Exception:
- **PG-factory_lowlevel/memory_guard.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 85: except Exception:
- **PG-factory_lowlevel/memory_guard.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 92: except Exception:
- **PG-factory_lowlevel/memory_guard.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 166: if line.startswith("VmRSS:"):
- **PG-factory_lowlevel/memory_guard.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 172: if line.startswith("MemAvailable:"):
- **PG-factory_lowlevel/memory_guard.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 225: except OSError:
- **PG-factory_lowlevel/memory_guard.py-lvs-7** (info, hypothesis): Detected letter-coupled fix surface at line 234: except OSError:
- **PG-factory_lowlevel/memory_guard.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.