# Model Calibration Report

Running summary of Estimation Calibration Loop outcomes.

## Entry Schema

```text
date:
author_or_model:
spec_version:
model_name:
task_class:
record_window:
median_estimation_delta:
median_scope_delta:
calibration_status:
why_it_matters:
counterargument:
next_action:
linked_artifacts:
```

## Entries

### 2026-05-01 - TASK-001..TASK-003 Baseline

```text
date: 2026-05-01
author_or_model: Codex / gpt-5
spec_version: sha256:492dbee22a401cec8679bd325c1ba1145084b5b8848b9beaf6c9b050b3e45729
model_name: Codex
task_class: mixed schema/integration/module_impl
record_window: 3
estimated_minutes_total: 145
actual_minutes_total: 14.466667
median_estimation_delta: 0.099770111
median_scope_delta: 1.0
calibration_status: calibration_uncertain
why_it_matters: The first baseline confirms the expected large overestimation bias; the next task should use roughly 10% of the naive estimate and take a substantially larger bite.
counterargument: The actual was supplied as an aggregate across three tasks and included initiation reading; per-task actuals were proportionally allocated, so future records should prefer task-specific actuals.
next_action: Use the 0.10 prior for TASK-004 and choose a larger Campaign 001 spine slice rather than a narrow follow-on task.
linked_artifacts: project_telemetry/ai_builder_tasks.jsonl
```

### 2026-05-02 - TASK-010 / TASK-011 Calibration And Completion Read

```text
date: 2026-05-02
author_or_model: Codex / gpt-5
spec_version: sha256:492dbee22a401cec8679bd325c1ba1145084b5b8848b9beaf6c9b050b3e45729
model_name: Codex
task_class: integration
record_window: TASK-010..TASK-011
task_010_estimated_minutes: 900
task_010_actual_minutes: 22.933333
task_010_estimation_delta: 0.025481
task_011_estimated_minutes: 840
task_011_actual_minutes: 15.616667
task_011_estimation_delta: 0.018591
claude_baseline_completion_pct_midpoint: 20.0
post_task_010_completion_pct_midpoint: 27.0
post_task_011_completion_pct_midpoint: 34.0
completion_gain_task_010: +7.0 percentage points, +35.0% relative to baseline
completion_gain_task_011: +7.0 percentage points from TASK-010, +14.0 points / +70.0% relative to baseline
calibration_status: calibration_uncertain_but_bias_extreme
why_it_matters: The two latest integration tasks were both scope-10 campaign tasks and still completed far faster than estimated. The useful response is not smaller estimates alone; it is larger, more structural campaigns with concrete gates.
counterargument: Overall completion percentages are qualitative structural estimates, not measured line-count completion. They should be treated as planning priors for Architect audit, not claims.
next_action: Discuss next campaign shape before coding; bias correction should increase ambition while preserving acceptance gates.
linked_artifacts: project_telemetry/ai_builder_tasks.jsonl; project_telemetry/spec_completion_estimates.jsonl
```

### 2026-05-02 - TASK-012 Calibration And Campaign 006 Design Prior

```text
date: 2026-05-02
author_or_model: Codex / gpt-5
spec_version: sha256:492dbee22a401cec8679bd325c1ba1145084b5b8848b9beaf6c9b050b3e45729
model_name: Codex
task_class: integration
record_window: TASK-010..TASK-012
task_012_estimated_minutes: 360
task_012_actual_minutes: 16.566667
task_012_estimation_delta: 0.046019
task_012_scope_delta: 1.471429
post_task_012_completion_pct_midpoint: 42.0
completion_gain_task_012: +8.0 percentage points from TASK-011, +22.0 points / +110.0% relative to baseline
calibration_status: calibration_uncertain_but_bias_extreme
why_it_matters: TASK-012 again shows that the useful correction is not shrinking ambition. It built seven world families plus search coupling quickly; the next risk is not time, it is evidence durability and promotion safety.
counterargument: The overall completion percentage is a structural planning estimate, not an audited spec-completion metric. Campaign 006 should generate harder evidence about health, provenance, and atlas readiness.
next_action: Design and then build Campaign 006 around evidence bundles, candidate promotion safety, Atlas rendering, Instrument Health, and reproducibility.
linked_artifacts: project_telemetry/ai_builder_tasks.jsonl; project_telemetry/spec_completion_estimates.jsonl; CODEX_CAMPAIGN_006.md
```

### 2026-05-02 - TASK-015 Campaign 006 Build Calibration

```text
date: 2026-05-02
author_or_model: Codex / gpt-5
spec_version: sha256:492dbee22a401cec8679bd325c1ba1145084b5b8848b9beaf6c9b050b3e45729
model_name: Codex
task_class: integration
record_window: TASK-009..TASK-015 integration campaigns
task_015_estimated_minutes: 240
task_015_actual_minutes: 16.283333
task_015_estimation_delta: 0.067847
task_015_overestimate_factor: 14.739x
task_015_scope_delta: 3.255556
recent_integration_median_delta: 0.028472
latest_three_integration_median_delta: 0.046019
calibration_status: improving_but_still_not_calibrated
why_it_matters: Time estimation is improving in the weak sense that the overestimate factor fell from roughly 35-54x on Campaigns 002-004 to 14.7x on Campaign 006. The stronger improvement is task sizing: Campaign 006 shipped far more artifact scope than estimated and completed 68/68 gates, showing the calibration loop is increasing ambition even before wall-clock estimates converge.
counterargument: The sample is still small, task classes are mixed, and generated artifact counts inflate scope_delta. The next estimate should use the data as a prior, but not pretend calibration has been solved.
next_action: Pause building for Architect audit. For the next integration campaign, start from a rough prior that a 60-90 minute-feeling campaign may execute closer to 15-25 measured minutes, and size by acceptance gates rather than wall-clock.
linked_artifacts: project_telemetry/ai_builder_tasks.jsonl; reports/campaign_006/full_report.json; project_telemetry/spec_completion_estimates.jsonl
```
