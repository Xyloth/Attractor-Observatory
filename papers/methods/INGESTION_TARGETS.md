# Ingestion Targets v0.1 — per-world target density

**Status:** **DRAFT — flagged for PI ratification before launch.**

This document specifies the target record density per world that
unattended ingestion drives toward. The continuous daemon reads the
canonical block below to compute `percent_complete` per world per
session (see `factory_lowlevel/progress.py:load_target_densities`).

When the PI signs this version, change `Status` to `RATIFIED` and
record the signature in `papers/prereg/ingestion_targets/INGESTION_TARGETS_v0.1.signed.json`.

## Methodology for setting targets

Target density per world reflects an honest joint estimate of:

1. **Source availability** — how many records the bundled adapters
   plus the configured external sources (NIST, PubChem, KEGG, GBIF,
   NCBI, peer-reviewed catalogs) can deliver before saturation.
2. **Methodology coverage** — minimum density required for the
   substrate-blocked control battery (D26 binding) to be evaluable
   on this world. Below this floor, MotifContract.v2 lens cells stay
   `methodology_review_required=true`.
3. **Per-substance audit ceilings** (D17.5) — line-count expectations
   from the substance audit pages under `papers/methods/SUBSTANCE_AUDIT_W*.md`.
4. **Storage budget** — per-world budget cap from
   `factory_lowlevel/budget.py:DEFAULT_PER_WORLD_HARD_CAP_BYTES`
   (1 GiB default). High-volume sources (PubChem subset, NIST batch)
   compress under this budget.

D22 binding: when a world has no source we know how to reach, the
target is set to the ratified floor (3 records — the minimum for the
audit harness to evaluate substrate-blocked controls). The PI signs
off on this rather than the daemon manufacturing a higher target.

## Per-world targets

The block below is parsed by the daemon. Do not edit row format
without updating `progress.py:load_target_densities` to match.

<!-- ingestion-targets:start -->

| world_family               | target_density | rationale                                                              |
|----------------------------|---------------:|------------------------------------------------------------------------|
| atomic_molecular_primitives|           1500 | NIST 118 elements + PubChem CID 1-2000 filtered; CB-011 ran 1,394.     |
| math_primitives            |             20 | DOI catalog of canonical dynamical-system primitives; saturating.      |
| crn                        |             50 | KEGG E. coli MG1655 metabolic network + RAFs catalog.                  |
| protocell                  |             30 | Peer-reviewed protocell topology corpus; sparse.                       |
| field                      |             40 | Reaction-diffusion benchmark suite (Gray-Scott / Brusselator / etc.).  |
| morphogenesis              |             30 | Curated GRN catalog; smaller corpus than CRN.                          |
| digital                    |             30 | Avida-class digital evolution benchmarks; bounded.                     |
| ecosystem                  |             50 | GBIF Jornada Basin ecosystem occurrences; site-bounded.                |
| swarm                      |             30 | Insect-swarm + cellular-swarm benchmarks; sparse.                      |
| cognitive                  |             30 | Cognitive trace corpus; sparse, methodology-bound.                     |
| origins_chemistry          |             50 | Peer-reviewed prebiotic chemistry catalog; bounded by literature.      |
| hypergraph_reactions       |             30 | Hypergraph reaction-network benchmarks; sparse.                        |
| quasispecies               |             40 | NCBI HIV-1 reference quasispecies pilot + variant accessions.          |
| symbiogenesis              |             30 | Curated symbiogenesis benchmarks; minimum-floor signal substrate.      |
| multiscale                 |              3 | Falsifier-active world (D17). Ratified floor only — no inflation.      |

<!-- ingestion-targets:end -->

**Total target across worlds: 1,963 records** at v0.1.

## Aggregate ratification gates

Before flipping the daemon to unbounded mode, the following must hold:

1. PI signature on this v0.1 table (or amended successor).
2. `make_source_object_generation` green for the four non-floor
   source-object adapters.
3. `make_campaign_026` green (current `post_run_hash` matches the
   one in `BUILD_LOG.md` TASK-FLOOR-BFG entry).
4. `factory_daemon.bat` fail-fast check passes (T1 deliverable).
5. `BUILDER_INGESTION_MONITORING_PLAYBOOK.md` stop/resume drill
   executed once on a controlled `cycles=1` run.

## Re-ratification cadence

This table is reviewed monthly (or after any source-object adapter
change that materially affects available volume). Increase a target
only if (a) the source provably has more clean records to give and
(b) per-world budget allows.

## PI ratification signature block

Replace the placeholder when signed:

```json
{
  "status": "DRAFT",
  "ratified_by": null,
  "ratified_at": null,
  "spec_version": null,
  "content_hash": null,
  "notes": "v0.1 awaiting PI review. Builder (CB-013) drafted from CB-011 + CB-012 evidence + brief suggestion."
}
```

Builder note (CB-013): I flagged this for PI review per the brief's
`T3 — Ratification by PI` clause. Numbers above were derived from:

* W-1: CB-011 verified 1,394 records persisted; targeting +106 to
  round to 1,500 leaves headroom for source-limited audit re-runs.
* math_primitives: 6 records currently; +14 covers the Strogatz
  catalog index.
* W1-W13: targets aligned with MRP per-cell `target_density` values
  where MRP carries them; for cells that don't, I priced from
  per-substance audit notes.

Recommend the PI either ratify these or hand back amended targets
before the daemon flips on.
