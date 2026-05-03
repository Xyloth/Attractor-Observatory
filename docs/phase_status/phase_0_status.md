# Phase 0 Status

Status after TASK-005.

## Foundations Roadmap

- Spec lineage: live.
- AI Operating System scaffold: live.
- Core kernel: live.
- Trace schema/writer/reader/verifier: live as Phase-0 JSON physical layout.
- Manifest/content hashing: live in core and trace writer.
- Provenance primitives: live in core.
- RNG discipline: live with Philox4x32-10 splitter and global RNG lint.
- Mode/status enforcement: live in core primitives.
- Full SystemTrace contract: partial. Current JSON representation preserves the v1.2 shape, but Parquet/Zarr storage and full schema registry are not yet implemented.

## Spine Demonstration

- Hello-world world: live.
- CRN W1 alpha: live with ODE and SSA back-ends.
- K2 closure calibration seed: live and expanded.
- Closure detector v0: live with K2 metrics.
- Graph-motif closure detector: live for triangulation.
- MotifObservation emission: live.
- CLI commands: live for CRN generation, verification, detection, observation, replay, storage, calibration, health, and pipeline execution.
- Atlas seed: live for closure observations.

## Phase Exit Position

Phase 0 is close but not exited. The project has a working spine layer and a
Phase-1 chemistry alpha, but still needs:

- Full trace schema freeze and registry review.
- Cold-container reproducibility bundle.
- PI-signed/audited MotifObservation.
- Instrument Health Vector thresholds formalized.
- Data-plane invariant review by Architect.

## Phase 1 Completion Status

- Closure recurrence experiment runner: live and passing.
- K1-K4 calibration framework: live.
- W1 CRN alpha: live with RAF subset measurement, ODE/SSA, replay, mass checks.
- W10 hypergraph reaction alpha: live.
- N1 seed-shuffle recurrence control: live.
- N2 catalyst-rewire adversarial null: live.
- N6 detector permutation seed: live.
- Preregistration manager and record: live.
- Claim ledger draft: live.
- AttractorStrength seed vector: live for R/P/B/I/S_obs.
- Phase-1 gauntlet: live and passing.
- CRN XML interchange bridge: live as minimal SBML-like surface.
- Round-trip and determinism checks: live and passing.

Builder assessment: Phase 1 is complete as an internal alpha capability and is
ready for Architect review. It is not claim-bearing/public-complete until
Architect review, Red Team pressure, PI signature, and the trace physical store
decision are resolved.
