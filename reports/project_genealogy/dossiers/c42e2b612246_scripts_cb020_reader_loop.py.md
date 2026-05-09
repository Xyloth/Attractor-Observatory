# Dossier: `scripts/cb020_reader_loop.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/c42e2b612246_scripts_cb020_reader_loop.py.json`
- JSON content_hash: `sha256:459c7630aabad3c37609a00a27b7792229a40ce45b5a0a52bef8e48060599316`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `script`
- Generated status: `source`
- Lines: 87 / Bytes: 3199

## Birth
- Status: `recovered`
- First-seen commit: `eada8c9bab091a8e21b021537c65a845709c2a6a`
- First-seen date: `2026-05-08T16:57:19-04:00`
- Spawn ticket: `TASK-CB-021`
- Cohort: `TASK-CB-021`

### Birth predicate atoms
- **script_executes_purposefully** — Script automates a declared developer workflow.
- **header_declared_intent** — CB-020 reader-loop: Streamlit autorefresh load proxy.

Polls the live-state files at Streamlit-class frequency (every 0.3s,
~10x faster than Streamlit's default 3s autorefresh) so the daemon's
write path is contended throughout the verify cycle. If the CB-020
fix is real, the daemon completes cleanly under this load.

Reads via the F3-compliant pattern: ``path.read_text(encoding="utf-8-sig")``,
si

## Current
- Status: `recovered`
- Public symbols: `main`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 66}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': [], 'verified': [], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Letter-vs-spirit surfaces: 4

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-scripts/cb020_reader_loop.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 59: if counter_name == "n_state":
- **PG-scripts/cb020_reader_loop.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 61: elif counter_name == "n_run":
- **PG-scripts/cb020_reader_loop.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 66: except BaseException as exc:  # noqa: BLE001
- **PG-scripts/cb020_reader_loop.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 86: if __name__ == "__main__":

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.