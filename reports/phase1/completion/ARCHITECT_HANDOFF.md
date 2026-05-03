# Architect Handoff: Phase 1 Chemistry Completion

Status: `complete_internal_alpha`

This handoff is for Architect review. It is not a public claim-bearing result.

## What Is Now Live

- W1 CRN alpha with ODE and SSA back-ends, mass invariant checks, trace export,
  RAF subset measurement, replay verification, and determinism comparison.
- W10 hypergraph reaction alpha exporting the same trace contract.
- K1-K4 calibration framework with K2 closure scenarios evaluated.
- Closure detector v0, graph-motif detector, triangulation, and ablation profile.
- Null factory seed: N1 seed-shuffle, N2 catalyst-rewire, N6 detector permutation.
- Phase-1 closure recurrence experiment with preregistration, null comparison,
  AttractorStrength seed vector, gauntlet, and claim ledger draft.
- Minimal CRN XML interchange bridge.
- Completion report and reproduction commands.

## Primary Artifacts

- Completion report: `reports/phase1/completion/phase1_completion_report.json`
- Closure recurrence report: `reports/phase1/closure_recurrence/report.json`
- Calibration report: `reports/phase1/calibration_report.json`
- W10 trace: `reports/phase1/w10_hypergraph_trace.json`
- Preregistration: `papers/prereg/phase1_closure_recurrence.json`
- Reproduction commands: `ops/repro/phase1_complete/commands.ps1`

## Review Triggers

- The physical trace store is still JSON, not Parquet/Zarr.
- The N2 catalyst-rewire null is intentionally adversarial and should be
  assessed for whether it is too destructive or appropriately hard.
- W10 is alpha: it pressures the trace contract but is not production chemistry.
- Current claims remain internal candidate status. PI signature and Red Team
  pressure are still required for claim-bearing promotion.
