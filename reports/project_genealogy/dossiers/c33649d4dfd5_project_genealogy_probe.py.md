# Dossier: `project_genealogy/probe.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/c33649d4dfd5_project_genealogy_probe.py.json`
- JSON content_hash: `sha256:d82e10f01ac37a5f3a89cc451fc1d98368dd72f53024ff01bb8064225b4bdc7c`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `audit_instrument`
- Generated status: `source`
- Lines: 114 / Bytes: 4346

## Birth
- Status: `recovered`
- First-seen commit: `76085687c8c8f33c41cb35b5af5dfadeaf23ca3d`
- First-seen date: `2026-05-08T15:48:58-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **audit_instrument_executes** — Module is part of the PG-001 audit instrument and exposes a callable surface.
- **header_declared_intent** — Removal probe — mechanical liveness assessment.

Per spec §"Removal Probe Protocol", `cleanup_candidate_status ∈
{removable_clean, removable_with_warnings, not_removable}` requires a
recorded ``removal_probe`` with command and outcome. Without that, the
status defaults to ``unknown``.

PG-001 v1 declares a global probe-budget of zero per-file seconds (see
manifest's ``THRESHOLD_POLICY['probe']``).

## Current
- Status: `recovered`
- Public symbols: `run_probe`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D19', 'D20'], 'verified': [], 'claimed_only': ['D11', 'D19', 'D20'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-project_genealogy/probe.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.