# Dossier: `factory_lowlevel/persistence.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/c031b6a7ca30_factory_lowlevel_persistence.py.json`
- JSON content_hash: `sha256:b82a57980c41869a67ba317bc283fc5bdd43fdb2a1300305f6571d72de4b5775`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `factory`
- Generated status: `source`
- Lines: 601 / Bytes: 26672

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **factory_module_exposes_callable** — Module exposes runnable factory components consumed by the daemon/pipeline.

## Current
- Status: `recovered`
- Public symbols: `LowLevelFactoryStore, atomic_write_json, recover_json_artifact, recover_json_tree, safe_read_json, verify_world_traces, write_json`
- Observed doctrines: `D14, D17, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 90}, {'id': 'error_branch', 'line': 120}, {'id': 'error_branch', 'line': 445}, {'id': 'error_branch', 'line': 523}, {'id': 'error_branch', 'line': 557}], 'missing_bad_cases': [{'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 2.5}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17', 'D9'], 'verified': ['D14', 'D17', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md', 'papers/methods/INGESTION_CONVERGENCE_CB008.md', 'reports/campaign_022/convergence_session.json'], 'weighted_value': 4.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 2
- Letter-vs-spirit surfaces: 6

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-factory_lowlevel/persistence.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 90: except (OSError, json.JSONDecodeError) as exc:
- **PG-factory_lowlevel/persistence.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 120: except (KeyError, TypeError, ValueError):
- **PG-factory_lowlevel/persistence.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 318: relation=f"has_{axis[:-1] if axis.endswith('s') else axis}",
- **PG-factory_lowlevel/persistence.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 445: except OSError as exc:
- **PG-factory_lowlevel/persistence.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 523: except OSError as exc:
- **PG-factory_lowlevel/persistence.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 557: except (UnicodeDecodeError, json.JSONDecodeError) as exc:
- **PG-factory_lowlevel/persistence.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.