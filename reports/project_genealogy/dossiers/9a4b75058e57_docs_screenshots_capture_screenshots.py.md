# Dossier: `docs/screenshots/capture_screenshots.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/9a4b75058e57_docs_screenshots_capture_screenshots.py.json`
- JSON content_hash: `sha256:b7a76a35df162e01fa14de185b04afd653839cee7040db6b7c20a03a42e0b4bd`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `docs`
- Generated status: `source`
- Lines: 97 / Bytes: 3409

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **doc_serves_handbook** — Doc serves the project handbook (doctrine support, methodology, audit notes).
- **header_declared_intent** — Capture polished room screenshots from the running Streamlit app.

Connects to the Control Room at localhost:8765 (started by the Launcher
or `streamlit run`), navigates to each room via the URL anchor wired in
CB-007 (``?room=<id>``), and saves a screenshot to this directory.

Usage::

    python docs/screenshots/capture_screenshots.py

Requires dependencies from ``requirements.txt`` plus Chromiu

## Current
- Status: `recovered`
- Public symbols: `main`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 22}, {'id': 'error_branch', 'line': 73}, {'id': 'error_branch', 'line': 87}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11'], 'verified': [], 'claimed_only': ['D11'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['Control_Room_README.md'], 'weighted_value': 1.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 1
- Letter-vs-spirit surfaces: 4

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-docs/screenshots/capture_screenshots.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 22: except ImportError:  # pragma: no cover - exercised only when optional dependency is absent.
- **PG-docs/screenshots/capture_screenshots.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 73: except Exception as exc:
- **PG-docs/screenshots/capture_screenshots.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 87: except Exception as exc:
- **PG-docs/screenshots/capture_screenshots.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 96: if __name__ == "__main__":

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.