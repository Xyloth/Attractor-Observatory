# Dossier: `public_tests/test_cb018_phase_2_density.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/d74ad005e99f_public_tests_test_cb018_phase_2_density.py.json`
- JSON content_hash: `sha256:7c1f562e7f11d3cb7a3f37e475737a68928e3007df3db3f2a6c27d7158ea1665`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 465 / Bytes: 20862

## Birth
- Status: `recovered`
- First-seen commit: `5343a1692a9fb5023a110a10d9de8ac74a1f75b5`
- First-seen date: `2026-05-07T16:23:01-04:00`
- Spawn ticket: `TASK-CB-018`
- Cohort: `TASK-CB-018`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — TASK-CB-018 Phase-2 mass-density expansion — per-adapter tests.

Pins the Phase-2 target counts and contract for each of the 16 adapters
expanded in CB-018. Each test does an offline cache-only fetch against
a tmp_path cache_dir and checks:

* Record count meets the offline-mode floor (full Phase-2 counts only
  emerge under --allow-network with a populated cache; offline mode
  hits the bundled-s

## Current
- Status: `recovered`
- Public symbols: `test_t10_movebank_swarm_phase_2, test_t11_allen_brain_cognitive_phase_2, test_t12_prebiotic_chemistry_phase_2, test_t13_biomodels_hypergraph_phase_2, test_t14_ncbi_quasispecies_phase_2, test_t15_ncbi_endosymbiosis_phase_2, test_t16_physiome_multiscale_phase_2, test_t17_aggregate_offline_cycle_no_exceptions, test_t1_nist_ionization_stages_extended_to_30, test_t1_nist_offline_fetch`
- Observed doctrines: `D19`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D19'], 'verified': ['D19'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 5, 'dereferenceable_evidence_refs': 5, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 3

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.