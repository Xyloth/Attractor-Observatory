# Spec Changelog

This changelog records the content-addressed lineage for the Attractor Observatory specs. `The Attractor Observatory v1.2.md` is the active canonical spec. When documents conflict, v1.2 wins; when v1.2 is silent, defer to v1.1, then v1.0.

Hash policy: SHA-256 over raw file bytes as present in this workspace at TASK-001 time.

## Active Spec

- Active: `spec-v1.2`
- File: `The Attractor Observatory v1.2.md`
- SHA-256: `492dbee22a401cec8679bd325c1ba1145084b5b8848b9beaf6c9b050b3e45729`

## Lineage

### v1.0 - ambition substrate

- File: `The Attractor Observatory v1.0.txt`
- Author role: GPT seed
- SHA-256: `5478d60f7d409ac3b0a6152730a510b36a605f0def7cc13f131478ea2f814762`
- Role in lineage: original ambition substrate.
- Major content: north-star claim, world ensemble, trace-first architecture, motif grammar, AttractorStrength intuition, biology grounding, atlas, and formal-deficit ladder.

### v1.1 - rigor substrate

- File: `The Attractor Observatory v1.1.md`
- Author role: Claude architect
- Parent: v1.0
- SHA-256: `24e4ac46c0fb0859ca41ff4994bd1f2ba5b9cbe04a1388fa4bfe69afc7d99d3e`
- Role in lineage: implementation-grade rigor substrate.
- Major content: versioned `SystemTrace`, manifest and trace schemas, validation gauntlet, null hierarchy, calibration corpora, formal coverage tests, biology-bias controls, risk register, and v1.1 task atoms.

### Seed v1.2 - doctrine critique

- File: `Seed v1.2.txt`
- Author role: GPT theorist
- Parent: v1.1
- SHA-256: `cc1d73731d5cbe8e0eb0a4886ef9be3ff3636b4c52bfaa5adb804bc449823f12`
- Role in lineage: critique and merge seed.
- Major content: No Artificial Ceiling Doctrine integration, exploratory vs. claim-bearing split, AI-builder telemetry, Research Memory Ledger, emergent motif pipeline, biology shadow track, negative-space registry, vector/Pareto scoring, residual structure tests, and Campaign 001 framing.

### v1.2 - active canonical synthesis

- File: `The Attractor Observatory v1.2.md`
- Author role: Claude architect
- Parents: v1.0, v1.1, Seed v1.2
- SHA-256: `492dbee22a401cec8679bd325c1ba1145084b5b8848b9beaf6c9b050b3e45729`
- Role in lineage: active canonical spec.
- Major content: three-mode artifact system, work-vs-contract doctrine boundary, AI Operating System, Estimation Calibration Loop, component map update, SystemTrace v1.0 additions, failure store, mode promotion, K1-K10 calibration, Instrument Health Vector, Campaign 001, and v1.2 task doctrine.

## Supporting Context

These files are content-addressed as supporting context, not numbered spec versions:

- `NO ARTIFICIAL CEILING DOCTRINE.txt`: `7c634bab4bbe18cdd01304f581c44c4a370d77d2a74f12ae029c0444bf0b24ba`
- `CODEX_INITIATION.md`: `1f2cd546de9631b0881ffd48f02c11f290e80219285745def22481b31c8db464`

## TASK-001 Signature

TASK-001 was signed by Builder/Codex using a SHA-256 self-attestation because no external private key or PI signature was available in this workspace.

- Signature scheme: `sha256-self-attestation`
- Signature hash: `b08184d68fbea0d785824750a3a686839b2a199fd780c0b5ec6fd2a26920f000`
- Signature input: the four spec content hashes, active spec id, signer, and timestamp recorded in `spec/lineage.json`.

## Repository Note

No `.git` repository metadata was present when TASK-001 began. Until a repository is initialized or attached, content-addressed hashes in `spec/lineage.json` are the source of truth for lineage integrity.
