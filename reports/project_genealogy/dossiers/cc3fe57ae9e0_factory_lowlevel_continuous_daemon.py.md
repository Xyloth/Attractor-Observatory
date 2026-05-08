# Dossier: `factory_lowlevel/continuous_daemon.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/cc3fe57ae9e0_factory_lowlevel_continuous_daemon.py.json`
- JSON content_hash: `sha256:4df1814bbd2dfc2c484d3862b54f14fd245c7c16a80b12c59150a2bacedc87e0`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `factory`
- Generated status: `source`
- Lines: 492 / Bytes: 19137

## Birth
- Status: `recovered`
- First-seen commit: `b8473aa3ed840989f6dce967fc460df34c7eed60`
- First-seen date: `2026-05-06T19:23:03-04:00`
- Spawn ticket: `TASK-MOTIF-IMPL`
- Cohort: `TASK-MOTIF-IMPL`

### Birth predicate atoms
- **factory_module_exposes_callable** — Module exposes runnable factory components consumed by the daemon/pipeline.
- **header_declared_intent** — Continuous-cycle launcher for unattended Factory ingestion.

CB-013 hardening: lock file, SIGINT/SIGTERM handlers, atomic
checkpoint, resume-from-heartbeat verification. See
``launch_safety.py`` for the underlying mechanics — this module wires
them into ``run_continuous_daemon``.

## Current
- Status: `recovered`
- Public symbols: `cadence_seconds, main, run_continuous_daemon`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 216}, {'id': 'error_branch', 'line': 230}, {'id': 'error_branch', 'line': 276}, {'id': 'error_branch', 'line': 359}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': 2.5}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17.5', 'D7'], 'verified': [], 'claimed_only': ['D14', 'D17.5', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 10

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-factory_lowlevel/continuous_daemon.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 44: if normalized in {"hourly", "per_hour", "1h"}:
- **PG-factory_lowlevel/continuous_daemon.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 46: if normalized in {"daily", "per_day", "1d"}:
- **PG-factory_lowlevel/continuous_daemon.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 48: if normalized in {"weekly", "per_week", "1w"}:
- **PG-factory_lowlevel/continuous_daemon.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 50: if normalized in {"monthly", "per_month", "1mo"}:
- **PG-factory_lowlevel/continuous_daemon.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 52: if normalized in {"manual", "manual_spec_review", "dry_run"}:
- **PG-factory_lowlevel/continuous_daemon.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 216: except (OSError, json.JSONDecodeError):
- **PG-factory_lowlevel/continuous_daemon.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 230: except Exception:  # pragma: no cover — progress write must never break the daemon
- **PG-factory_lowlevel/continuous_daemon.py-lvs-7** (info, hypothesis): Detected letter-coupled fix surface at line 276: except ValueError:
- **PG-factory_lowlevel/continuous_daemon.py-lvs-8** (info, hypothesis): Detected letter-coupled fix surface at line 359: except Exception as exc:  # pragma: no cover - deterministic tests cover success; failures are runtime environment.
- **PG-factory_lowlevel/continuous_daemon.py-lvs-9** (info, hypothesis): Detected letter-coupled fix surface at line 491: if __name__ == "__main__":
- **PG-factory_lowlevel/continuous_daemon.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.