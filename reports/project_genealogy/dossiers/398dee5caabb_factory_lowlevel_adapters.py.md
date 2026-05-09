# Dossier: `factory_lowlevel/adapters.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/398dee5caabb_factory_lowlevel_adapters.py.json`
- JSON content_hash: `sha256:6403267064ad56b802dbd42d8cc64ade5d4d17d0e2fbe59668a7d2256537440f`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `factory`
- Generated status: `source`
- Lines: 3708 / Bytes: 197571

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
- Public symbols: `AdapterAudit, AdapterResult, AllenBrainCognitiveAdapter, AvidaDigitalTraceAdapter, BioModelsHypergraphAdapter, BoundaryRegionSamplesAdapter, CuratedWorldSeedAdapter, EntityObservationsAdapter, ExternalChannelSamplesAdapter, FlyBaseMorphogenProfileAdapter`
- Observed doctrines: `D17, D22, D26, D39, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'error_branch', 'line': 36}, {'id': 'error_branch', 'line': 191}, {'id': 'error_branch', 'line': 534}, {'id': 'error_branch', 'line': 718}, {'id': 'error_branch', 'line': 1405}, {'id': 'error_branch', 'line': 1416}, {'id': 'error_branch', 'line': 1829}, {'id': 'error_branch', 'line': 1992}, {'id': 'error_branch', 'line': 2198}, {'id': 'error_branch', 'line': 2913}, {'id': 'error_branch', 'line': 3443}, {'id': 'error_branch', 'line': 3479}, {'id': 'error_branch', 'line': 3488}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': 7.0}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D22', 'D26', 'D39', 'D9'], 'verified': ['D17', 'D22', 'D26', 'D39', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md', 'papers/methods/INGESTION_CONVERGENCE_CB008.md', 'papers/methods/PROJECT_GENEALOGY_PG001_SPEC.md', 'reports/campaign_022/convergence_session.json'], 'weighted_value': 6.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 31

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-factory_lowlevel/adapters.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 36: except ValueError:
- **PG-factory_lowlevel/adapters.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 191: except Exception as exc:  # pragma: no cover - network fallback is environment dependent.
- **PG-factory_lowlevel/adapters.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 534: except Exception as exc:  # pragma: no cover - network fallback is environment dependent.
- **PG-factory_lowlevel/adapters.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 718: except Exception as exc:  # pragma: no cover - network fallback is environment dependent.
- **PG-factory_lowlevel/adapters.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 1405: except OSError:
- **PG-factory_lowlevel/adapters.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 1416: except Exception as exc:  # pragma: no cover - network path
- **PG-factory_lowlevel/adapters.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 1820: if retrieval_mode_aggregate == "bundled_authoritative_seed":
- **PG-factory_lowlevel/adapters.py-lvs-7** (info, hypothesis): Detected letter-coupled fix surface at line 1829: except Exception as exc:  # pragma: no cover - network fallback environment-dependent.
- **PG-factory_lowlevel/adapters.py-lvs-8** (info, hypothesis): Detected letter-coupled fix surface at line 1992: except Exception as exc:  # pragma: no cover - network fallback is environment dependent.
- **PG-factory_lowlevel/adapters.py-lvs-9** (info, hypothesis): Detected letter-coupled fix surface at line 2198: except Exception as exc:  # pragma: no cover - source availability is environment dependent.
- **PG-factory_lowlevel/adapters.py-lvs-10** (info, hypothesis): Detected letter-coupled fix surface at line 2913: except Exception as exc:  # pragma: no cover - source availability is environment dependent.
- **PG-factory_lowlevel/adapters.py-lvs-11** (info, hypothesis): Detected letter-coupled fix surface at line 3109: if decoy_kind == "same_magnitude_no_recovery":
- **PG-factory_lowlevel/adapters.py-lvs-12** (info, hypothesis): Detected letter-coupled fix surface at line 3111: elif decoy_kind == "exogenous_reset":
- **PG-factory_lowlevel/adapters.py-lvs-13** (info, hypothesis): Detected letter-coupled fix surface at line 3113: elif decoy_kind == "passive_stability":
- **PG-factory_lowlevel/adapters.py-lvs-14** (info, hypothesis): Detected letter-coupled fix surface at line 3115: elif decoy_kind == "matched_trace_length_control":
- **PG-factory_lowlevel/adapters.py-lvs-15** (info, hypothesis): Detected letter-coupled fix surface at line 3199: if decoy_kind == "declared_edges_randomized_sequences":
- **PG-factory_lowlevel/adapters.py-lvs-16** (info, hypothesis): Detected letter-coupled fix surface at line 3201: elif decoy_kind == "similar_sequences_no_temporal_order":
- **PG-factory_lowlevel/adapters.py-lvs-17** (info, hypothesis): Detected letter-coupled fix surface at line 3203: elif decoy_kind == "population_growth_without_descent":
- **PG-factory_lowlevel/adapters.py-lvs-18** (info, hypothesis): Detected letter-coupled fix surface at line 3284: if decoy_kind == "internal_recurrence_no_external_channel":
- **PG-factory_lowlevel/adapters.py-lvs-19** (info, hypothesis): Detected letter-coupled fix surface at line 3287: elif decoy_kind == "external_noise_same_entropy":
- **PG-factory_lowlevel/adapters.py-lvs-20** (info, hypothesis): Detected letter-coupled fix surface at line 3291: elif decoy_kind == "renamed_channel_payload_keys":
- **PG-factory_lowlevel/adapters.py-lvs-21** (info, hypothesis): Detected letter-coupled fix surface at line 3354: if decoy_kind == "closed_shell_no_internal_maintenance":
- **PG-factory_lowlevel/adapters.py-lvs-22** (info, hypothesis): Detected letter-coupled fix surface at line 3356: elif decoy_kind == "external_reset_only":
- **PG-factory_lowlevel/adapters.py-lvs-23** (info, hypothesis): Detected letter-coupled fix surface at line 3358: elif decoy_kind == "randomized_region_adjacency":
- **PG-factory_lowlevel/adapters.py-lvs-24** (info, hypothesis): Detected letter-coupled fix surface at line 3411: if pathway_id.startswith("path:"):
- **PG-factory_lowlevel/adapters.py-lvs-25** (info, hypothesis): Detected letter-coupled fix surface at line 3425: sequence = "".join(line.strip().upper() for line in raw.splitlines() if line.strip() and not line.startswith(">"))
- **PG-factory_lowlevel/adapters.py-lvs-26** (info, hypothesis): Detected letter-coupled fix surface at line 3426: return "".join(base for base in sequence if base in {"A", "C", "G", "T"})
- **PG-factory_lowlevel/adapters.py-lvs-27** (info, hypothesis): Detected letter-coupled fix surface at line 3430: return "".join("0" if base in {"A", "C"} else "1" for base in sequence if base in {"A", "C", "G", "T"})
- **PG-factory_lowlevel/adapters.py-lvs-28** (info, hypothesis): Detected letter-coupled fix surface at line 3443: except (TypeError, ValueError):
- **PG-factory_lowlevel/adapters.py-lvs-29** (info, hypothesis): Detected letter-coupled fix surface at line 3479: except (TypeError, ValueError) as exc:
- **PG-factory_lowlevel/adapters.py-lvs-30** (info, hypothesis): Detected letter-coupled fix surface at line 3488: except (TypeError, ValueError) as exc:
- **PG-factory_lowlevel/adapters.py-class-0** (low, hypothesis): Detected pattern matching Class6 (engineered prediction polynomial) at line 3282
- **PG-factory_lowlevel/adapters.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.