# Contributing

This repository is a curated public showcase of the Attractor Observatory's documentation, doctrine, AI-collaboration framework, methodology, and numerical evidence. The full implementation — substrate engines, motif detectors, validation gauntlet, kernel — is held privately. Direct contributions to the implementation happen in the private repository. The framework documented here is reusable under MIT.

If you arrive as a researcher, hiring manager, AI-safety reader, or collaborator, here is how to engage with the project.

## What you can do from the public repository

**Read the project as a case study.** The five-minute tour is in [`docs/TOUR.md`](docs/TOUR.md); the deeper read order is in the README. The story is the value: the science, the doctrine that catches AI-builder failure modes, the empirical Estimation Calibration Loop, the Truth Pass discipline, the Substance Audit pattern, the role decision-rights structure.

**Reuse the AI-collaboration framework.** Doctrine D7–D18, the Estimation Calibration Loop, the Truth Pass discipline, the Substance Audit pattern, the three-mode artifact tagging, and the role decision-rights structure are all documented in `docs/` and the v1.2 spec. They are designed to be lifted into other AI-collaboration projects. The MIT license covers them.

**Cite the project.** Use [`CITATION.cff`](CITATION.cff). The authors are listed by role: human PI, Claude (Architect), GPT (Theorist), Codex (Builder).

**Open an issue.** If something in the public surface is unclear, contradictory, or appears to be a false claim, file a GitHub issue. Issues that point to specific spec text or specific report numerical evidence are most useful.

## What you cannot do from the public repository

**Run the campaigns.** The reproducibility scripts (`make_campaign_NNN.py`), the World contract implementations, the motif detectors, and the validation gauntlet are in the private repository. The campaign summary JSONs in `reports/` show the *outputs* of cold-start regeneration but the regeneration itself is not runnable here.

**Submit pull requests against the implementation.** The implementation is private. PRs that modify documentation, fix typos in spec versions, or extend the curated code excerpts in `docs/SAMPLE_CODE.md` are welcome.

## Collaboration access

Collaborators who want to engage with the full implementation — to run campaigns, to extend worlds, to contribute motif detectors, to propose new lenses, to participate in Campaign 009 (Basin-Floor Geometry) or Phase 6 (Biology Grounding) — should contact the Project PI. The doctrine (D7 through D18) is binding on collaborators in the private repo.

## If you reuse the framework

The doctrine is binding on this project, not on yours. The doctrine works best when its rules are kept faithfully — D7 through D18 are derived from observed failures, not aesthetic preferences — but you can lift any subset.

The Estimation Calibration Loop is the most directly portable artifact. The schema for a single record is documented in `docs/AI_COLLABORATION.md`; the empirical convergence pattern is visible in `project_telemetry/ai_builder_tasks.jsonl`. If you run the Loop on a fresh AI-collaboration project for ~20 tasks, you will likely see similar dynamics: ~10× overestimation initially, scope under-execution as scope is expanded, gradual convergence to delta near 1.0 once both wall-clock and substance per file land in the same band.

The Truth Pass and Substance Audits are slightly heavier instruments and require an Architect role with sign-off authority to be effective. They become valuable once the project is large enough that historical claims accumulate and line-count proxies start diverging from spec coverage.

## Read first if you are a contributor (private repo)

The discipline binding on private-repo contributors is in:

1. **`NO ARTIFICIAL CEILING DOCTRINE.txt`** — operating principle.
2. **`The Attractor Observatory v1.2.md`** — active spec.
3. **`docs/DOCTRINE.md`** — D7 through D18 with the failure mode each rule catches.
4. **`docs/AI_COLLABORATION.md`** — roles, Estimation Loop, Truth Pass.
5. The latest campaign driver (`CODEX_TASK_NNN_DRIVE.md`) for the specific task atom you are working on.

## Authorship and attribution

This project is unusual in being built primarily by AI agents under a human PI. CITATION.cff names the human PI as accountable author and the AI agents by role. Per-task attribution lives in `project_telemetry/ai_builder_tasks.jsonl` (`model_name`, `model_version`). Per-spec attribution lives in `spec/lineage.json`.

If you contribute substantively as a human or as another AI agent (in either the private or public repository), add yourself to CITATION.cff with a role tag and a one-line description of your contribution.
