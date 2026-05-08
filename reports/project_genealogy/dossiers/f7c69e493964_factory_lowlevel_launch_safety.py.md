# Dossier: `factory_lowlevel/launch_safety.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/f7c69e493964_factory_lowlevel_launch_safety.py.json`
- JSON content_hash: `sha256:62a40867076ff510276533f8c45daa7dec09eb61ff4559cd1e5df63d1e864c40`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `factory`
- Generated status: `source`
- Lines: 547 / Bytes: 18968

## Birth
- Status: `recovered`
- First-seen commit: `f1d7305d60c15c1177908245f22443d22cf86bf5`
- First-seen date: `2026-05-07T08:59:39-04:00`
- Spawn ticket: `CB-013`
- Cohort: `CB-013`

### Birth predicate atoms
- **factory_module_exposes_callable** — Module exposes runnable factory components consumed by the daemon/pipeline.
- **header_declared_intent** — Launch-safety mechanics for the continuous Factory daemon.

CB-013 T4 hardening: lock file, signal handlers, atomic checkpoint
helpers, and resume-from-heartbeat verification. These are the
mechanics that make unattended ingestion safe to flip on:

  * **Lock file** — exclusive single-instance guarantee. Written at
    daemon startup, deleted on graceful shutdown. A second daemon
    seeing a live

## Current
- Status: `recovered`
- Public symbols: `LockAcquisition, ResumeVerdict, SignalState, acquire_lock, check_factory_store_integrity, install_signal_handlers, release_lock, verify_resume, write_checkpoint`
- Observed doctrines: `D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 117}, {'id': 'error_branch', 'line': 169}, {'id': 'error_branch', 'line': 176}, {'id': 'error_branch', 'line': 198}, {'id': 'error_branch', 'line': 203}, {'id': 'error_branch', 'line': 259}, {'id': 'error_branch', 'line': 276}, {'id': 'error_branch', 'line': 281}, {'id': 'error_branch', 'line': 365}, {'id': 'error_branch', 'line': 375}, {'id': 'error_branch', 'line': 445}, {'id': 'error_branch', 'line': 489}, {'id': 'error_branch', 'line': 503}, {'id': 'error_branch', 'line': 546}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 7.0}`
- **doctrine_binding_quality**: `{'required': ['D9'], 'verified': ['D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILDER_INGESTION_MONITORING_PLAYBOOK.md', 'BUILDER_LAUNCH_PROTOCOL.md', 'papers/methods/PROJECT_GENEALOGY_PG001_SPEC.md'], 'weighted_value': 4.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 14

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-factory_lowlevel/launch_safety.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 117: except (OSError, json.JSONDecodeError):
- **PG-factory_lowlevel/launch_safety.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 169: except (OSError, json.JSONDecodeError):
- **PG-factory_lowlevel/launch_safety.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 176: except OSError:
- **PG-factory_lowlevel/launch_safety.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 198: except (subprocess.TimeoutExpired, OSError):
- **PG-factory_lowlevel/launch_safety.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 203: except OSError:
- **PG-factory_lowlevel/launch_safety.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 259: except Exception:  # pragma: no cover - best-effort flush
- **PG-factory_lowlevel/launch_safety.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 276: except (AttributeError, ValueError):  # Windows pre-3.8 / threadsafe context
- **PG-factory_lowlevel/launch_safety.py-lvs-7** (info, hypothesis): Detected letter-coupled fix surface at line 281: except (AttributeError, ValueError):
- **PG-factory_lowlevel/launch_safety.py-lvs-8** (info, hypothesis): Detected letter-coupled fix surface at line 365: except (OSError, json.JSONDecodeError) as exc:
- **PG-factory_lowlevel/launch_safety.py-lvs-9** (info, hypothesis): Detected letter-coupled fix surface at line 375: except OSError:
- **PG-factory_lowlevel/launch_safety.py-lvs-10** (info, hypothesis): Detected letter-coupled fix surface at line 445: except (OSError, json.JSONDecodeError) as exc:
- **PG-factory_lowlevel/launch_safety.py-lvs-11** (info, hypothesis): Detected letter-coupled fix surface at line 489: except (OSError, json.JSONDecodeError):
- **PG-factory_lowlevel/launch_safety.py-lvs-12** (info, hypothesis): Detected letter-coupled fix surface at line 503: except (OSError, json.JSONDecodeError):
- **PG-factory_lowlevel/launch_safety.py-lvs-13** (info, hypothesis): Detected letter-coupled fix surface at line 546: except Exception:
- **PG-factory_lowlevel/launch_safety.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.