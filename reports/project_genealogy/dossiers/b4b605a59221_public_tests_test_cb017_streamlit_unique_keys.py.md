# Dossier: `public_tests/test_cb017_streamlit_unique_keys.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/b4b605a59221_public_tests_test_cb017_streamlit_unique_keys.py.json`
- JSON content_hash: `sha256:e5ed5d77a957a2e9627e45750a6990ed550f8d9d036e8558839be103913aa2d5`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 521 / Bytes: 18919

## Birth
- Status: `recovered`
- First-seen commit: `7b7f2db989b96ab9db88855077015a5373ad3c2e`
- First-seen date: `2026-05-07T13:37:03-04:00`
- Spawn ticket: `TASK-CB-017`
- Cohort: `TASK-CB-017`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — Tests for CB-017 Streamlit duplicate-element-id hotfix.

Symptom: ``World Observatory → math primitives drill-down`` raised
``StreamlitDuplicateElementId`` because ``_render_math_primitives``
emitted ``st.plotly_chart`` per record without a ``key=`` argument.
Streamlit auto-generates element IDs from chart parameters, so
multiple charts whose serialized parameters happen to hash alike
collide.

Fi

## Current
- Status: `recovered`
- Public symbols: `test_lint_finds_violation_in_synthetic_module, test_lint_helper_walker_finds_synthetic_pattern, test_lint_ignores_chart_with_key, test_no_chart_call_in_loop_without_key, test_no_helper_called_from_loop_emits_chart_without_key, test_render_atomic_molecular_two_atoms_no_collision, test_render_math_primitives_two_records_no_collision`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 232}, {'id': 'error_branch', 'line': 248}, {'id': 'error_branch', 'line': 267}, {'id': 'error_branch', 'line': 284}, {'id': 'error_branch', 'line': 303}, {'id': 'error_branch', 'line': 345}, {'id': 'error_branch', 'line': 408}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D12', 'D29', 'D7'], 'verified': [], 'claimed_only': ['D12', 'D29', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 5, 'dereferenceable_evidence_refs': 5, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 7

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-public_tests/test_cb017_streamlit_unique_keys.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 232: except SyntaxError:
- **PG-public_tests/test_cb017_streamlit_unique_keys.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 248: except ValueError:
- **PG-public_tests/test_cb017_streamlit_unique_keys.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 267: except SyntaxError:
- **PG-public_tests/test_cb017_streamlit_unique_keys.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 284: except ValueError:
- **PG-public_tests/test_cb017_streamlit_unique_keys.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 303: except Exception:
- **PG-public_tests/test_cb017_streamlit_unique_keys.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 345: except Exception:
- **PG-public_tests/test_cb017_streamlit_unique_keys.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 408: except Exception:

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.