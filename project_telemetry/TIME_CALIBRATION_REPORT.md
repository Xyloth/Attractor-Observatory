# Codex Builder Time Calibration Report

Status: living report
Owner: Codex Builder
Last updated: 2026-05-03

## Purpose

This report tracks how Builder estimates are becoming less distorted. The initial failure mode was simple: I treated broad campaign language as if it implied many hours, then repeatedly shipped concrete engineering slices in minutes. The useful correction is not to obsess over time; it is to estimate from the work's measurable shape:

- number of acceptance gates that require real code changes
- number of world systems touched
- amount of verification required
- expected rework from adversarial audit
- whether the task is design-only, repair/hardening, or new substrate construction

## Latest Calibration Point

TASK-019 confirmed that the estimator is now calibrated enough to watch for drift rather than to dominate planning.

| Task | Estimate | Actual | Ratio actual / estimate | Read |
|---|---:|---:|---:|---|
| TASK-016 | 180.00 min | 48.58 min | 0.2699 | Still overestimated, but task size was substantive. |
| TASK-017 | 60.00 min | 41.75 min | 0.6958 | Large improvement; estimate was anchored to HE1-HE9 plus full regression. |
| TASK-018 | 90.00 min | 84.03 min | 0.9337 | Calibrated: large foundation pass plus self-audit, blocker, and full regression. |
| TASK-019 | 60.00 min | 53.97 min | 0.8994 | Calibrated: Campaign 008 closure, D17.5 audits, W8/W11/W12/W13 deepening, D7 self-correction, full regression. |

TASK-019 error was 6.03 minutes. TASK-018 and TASK-019 were both in the [0.85, 1.0] band. Earlier campaign estimates were often off by 10x to 50x. The current useful estimator is now gate count plus verification cost plus expected audit rework, not broad campaign language. The loop's job now shifts from "stop overestimating" to "detect divergence."

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

For TASK-020, the estimate is 110 minutes. That number is a telemetry prior, not a stopping signal. Campaign 009 ends only when BFG-PR through BFG12 are green for the right reasons or when a named blocker records why a gate cannot honestly be completed.

The current Builder estimate for the next large implementation vertical should be based on the selected gates after the campaign is accepted, with 60-90 minutes as the likely first-pass band if it targets W6-W8 plus the shared reconstruction harness.
