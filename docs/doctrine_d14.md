# Doctrine D14: No Scenario-Internal Hardcoding

Mode: foundational
Spec version: sha256:492dbee22a401cec8679bd325c1ba1145084b5b8848b9beaf6c9b050b3e45729
Signed-by: Codex Builder

The world simulation may not write benchmark-specific answers into system state
through benchmark-conditional code paths. Scenarios may differ by parameters,
initial conditions, source and sink layouts, mutation rates, environment
schedules, and declared fields. Step/update/apply/mutation methods may not
contain `if scenario.benchmark == ...` branches that write the answer.

D14 is enforced by `reports/campaign_007/d14_audit.json`.
