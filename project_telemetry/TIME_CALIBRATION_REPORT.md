# Codex Builder Time Calibration Report

Status: living report
Owner: Codex Builder
Last updated: 2026-05-04

## Purpose

This report tracks how Builder estimates are becoming less distorted. The initial failure mode was simple: I treated broad campaign language as if it implied many hours, then repeatedly shipped concrete engineering slices in minutes. The useful correction is not to obsess over time; it is to estimate from the work's measurable shape:

- number of acceptance gates that require real code changes
- number of world systems touched
- amount of verification required
- expected rework from adversarial audit
- whether the task is design-only, repair/hardening, or new substrate construction

## Latest Calibration Point

TASK-023 was overestimated again after returning to regular speed, but the correction is now showing up in scope rather than caution. TASK-024 opened at 70 minutes instead of hundreds, while still carrying a 26-gate science milestone with schema migration, replication, L3 overlap, atlas seed, and full regression.

## Execution Context Change

As of TASK-022, the PI activated **Fast speed**. The product advertised roughly 1.5x execution speed at higher usage cost. This was recorded as a calibration context, not a quality exemption.

Operational impact:

- Estimates after TASK-022 should divide the normal calibrated wall-clock prior by roughly 1.5 unless the task is dominated by long-running tests or fixed external waits.
- Acceptance gates, regression, and audit discipline do not change.
- If Fast speed correlates with sloppiness, Claude audit and gate failures should surface it; the record should track that as a separate context effect rather than silently folding it into normal calibration.

As of TASK-023, the PI switched back to **regular speed** because TASK-022 cost roughly $22 and the speed/cost tradeoff was not worth it. Estimates from TASK-023 onward use the regular-speed prior again. TASK-022 actual wall-clock was 48.75 minutes under Fast speed; that point stays tagged with its execution context rather than merged into the regular-speed baseline.

| Task | Estimate | Actual | Ratio actual / estimate | Read |
|---|---:|---:|---:|---|
| TASK-016 | 180.00 min | 48.58 min | 0.2699 | Still overestimated, but task size was substantive. |
| TASK-017 | 60.00 min | 41.75 min | 0.6958 | Large improvement; estimate was anchored to HE1-HE9 plus full regression. |
| TASK-018 | 90.00 min | 84.03 min | 0.9337 | Calibrated: large foundation pass plus self-audit, blocker, and full regression. |
| TASK-019 | 60.00 min | 53.97 min | 0.8994 | Calibrated: Campaign 008 closure, D17.5 audits, W8/W11/W12/W13 deepening, D7 self-correction, full regression. |
| TASK-020 | 110.00 min | 60.00 min | 0.5455 | Drift-high but not pathological: Campaign 009 BFG vertical, D18 preregistration, KF calibration, falsifier audit, and full regression. |
| TASK-022 | 95.00 min | 48.75 min | 0.5132 | Fast-speed context; 32-gate Campaign 011 with full factory, doctrine, W7 densification, and split full-suite verification. |
| TASK-023 | 80.00 min | 25.90 min | 0.3238 | Regular-speed context restored; Campaign 012 real ITIS adapter, Factory scaffolding, calibration hardening, W7 naming, replication preregistration, and 252 tests. |
| TASK-024 | 70.00 min | pending | pending | Campaign 013 schema migration, floor-connectivity replication, first L3 insects x W7 overlap, atlas seed, and 265-test split regression. |

TASK-020 error was 50 minutes against a larger and novel formal-geometry vertical. That is worse than TASK-018/TASK-019 but still far from the early 10x to 50x failure mode. The correction is to keep estimating from gate shape plus verification cost, then let the next large campaign carry enough substance to make the estimate meaningful.

## What Changed

The estimate improved because TASK-017 had a concrete shape:

- known failing audit findings: W4 hardcodes, W5 EQU insertion, W3 Cahn-Hilliard mislabel
- explicit gates: HE1 through HE9
- known verification cost: targeted tests, full pytest, campaign report regeneration
- bounded rework domain: W3, W4, W5, D14 lint, Campaign 005 compatibility

This is a better estimator than "campaign feels big." It also avoids shrinking the work to hit a time bucket. The work stopped when the gates and regressions were green.

## Current Calibration Model

Use these priors until enough newer data replaces them:

| Task shape | Current estimate band | Notes |
|---|---:|---|
| Design-only campaign document | 5-15 min | More if it requires reading multiple specs or writing a task ledger. |
| Focused repair with full regression | 35-60 min | TASK-017 is the anchor. |
| One production world plus tests/reports | 45-75 min | More if numerical methods or stochastic calibration are involved. |
| Two to three coupled worlds plus shared reports | 75-120 min | Use only when gates are concrete and verification paths are known. |
| Full remaining Campaign 007 substrate stack | Closed by Campaign 008/TASK-019 | Keep D17.5 audits and strict floor reporting as guardrails. |
| Campaign 009 Basin-Floor Geometry vertical | 90-130 min first pass | Larger coupling than TASK-019: schemas, D18 preregistration, detector calibration, distance metrics, NFI/signature reports, falsifier audit, and full regression. |

The practical rule: estimate the next coherent gate-bearing vertical, not the whole project horizon.

## Biases Still Active

- I still overestimate when the task sounds like a whole campaign rather than a concrete implementation slice.
- I can underbuild if I define a "slice" as the stopping condition instead of acceptance gates.
- I can widen scope with many files while thinning depth unless each gate includes causation controls.
- I can create report artifacts that go green while stale reports drift red unless final artifact regeneration is explicit.

## Operating Rules

1. Estimate from gates, not vibes.
2. Include verification time explicitly.
3. Treat full regression and report regeneration as real work, not cleanup.
4. Record actuals quickly, but do not let time become the stopping signal.
5. For substrate work, do not count a world as done without positive, boundary, and counterfactual controls.
6. If a task finishes much faster than estimated, the next estimate should shrink only if the next gate shape is comparable. If the next task is broader or more coupled, increase scope rather than inventing a huge estimate.

## Next Estimate Guidance

For the next regular-speed campaign, estimate from gate type first. A bounded 20-30 gate milestone with mostly existing infrastructure and heavy report generation now belongs around 60-90 minutes, not 100-200 minutes. A genuinely new world/lens/source family still belongs higher, but only when the gate list requires new simulation or formal machinery rather than more artifacts around existing machinery.
