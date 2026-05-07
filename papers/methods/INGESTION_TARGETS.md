# Ingestion Targets v1 — Phase 1 substantive

**Status:** **RATIFIED** — Phase 1 substantive targets per PI delegation.

This document specifies the target record density per world that
unattended ingestion drives toward. The continuous daemon reads the
canonical block below to compute `percent_complete` per world per
session (see `factory_lowlevel/progress.py:load_target_densities`).

## PI directive

> "I want all the molecular structure. I want all the math primitives,
> like every one in existence. I don't wanna stretch the ingestion
> system early, but yeah, we don't want toy size."

PI delegation captured: *"And anything I didn't answer, I trust your
judgment, bro."*

Architect ratified Phase 1 targets per the substantive-not-toy
directive. Phase 2 + Phase 3 sections below document the long arc
toward the magnum-opus state.

## Methodology for setting targets

Target density per world reflects an honest joint estimate of:

1. **Source availability** — what the configured external sources
   (NIST, PubChem, ChEBI, KEGG, DrugBank, GBIF, NCBI, GISAID,
   peer-reviewed catalogs) can deliver before saturation.
2. **Methodology coverage** — minimum density required for the
   substrate-blocked control battery (D26 binding) to be evaluable.
3. **Per-substance audit ceilings** (D17.5) — line-count expectations
   from the substance audit pages.
4. **Storage budget** — per-world budget cap from
   `factory_lowlevel/budget.py:DEFAULT_PER_WORLD_HARD_CAP_BYTES`.

D22 binding: when a world has no source we know how to reach, the
target is held to the ratified floor. W13 multiscale stays at 3
because it is falsifier-active per the BFG floor work — inflating
its target would amount to silently overwriting the falsification.

## Per-world Phase 1 targets

The block below is parsed by the daemon. Do not edit row format
without updating `progress.py:load_target_densities` to match.

<!-- ingestion-targets:start -->

| world_family               | target_density | source_basis                                                                                                                                                  |
|----------------------------|---------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| atomic_molecular_primitives|           5600 | Atomic 600 (full periodic table neutral spectra ×118 + canonical ionization states ~500) + Molecular 5000 (ChEBI biological-relevance + KEGG metabolites + DrugBank approved + chemistry foundations) |
| math_primitives            |            200 | Full canonical peer-reviewed catalog: 1D/2D maps, autonomous ODEs (Lorenz/Rössler/Chua/Sprott/Chen/Lu families), 4D chaos, bifurcation normal forms, heteroclinic/homoclinic, limit-cycle/torus/strange-attractor families, intermittency, riddled basins |
| crn                        |             50 | KEGG top-50 reference organisms                                                                                                                                |
| protocell                  |             50 | Szostak lab archives + peer-reviewed protocell-membrane perturbation studies                                                                                   |
| field                      |            100 | Brusselator / Schnakenberg / FitzHugh-Nagumo / Gray-Scott / Cahn-Hilliard at parameter scale                                                                   |
| morphogenesis              |            100 | FlyBase + WormBase + ZFIN representative subset                                                                                                                |
| digital                    |             50 | Avida-class executable-genome traces (Lenski archive)                                                                                                          |
| ecosystem                  |            100 | LTER substantive subset + Movebank representative                                                                                                              |
| swarm                      |             50 | Movebank ant/fish-school + published swarm behavioral data                                                                                                     |
| cognitive                  |             50 | Allen Brain Atlas representative                                                                                                                                |
| origins_chemistry          |            100 | Peer-reviewed pre-biotic chemistry catalogs (Hordijk-Steel + Vasas + Sutherland + Miller-Urey-class)                                                            |
| hypergraph_reactions       |             50 | BioModels reaction-network hypergraphs                                                                                                                          |
| quasispecies               |            100 | NCBI HIV-1 longitudinal + GISAID flu pilot                                                                                                                      |
| symbiogenesis              |             50 | NCBI endosymbiosis genome data                                                                                                                                  |
| multiscale                 |              3 | Held low — W13 is falsifier-active per BFG floor work (D17 binding; falsification is publishable, never silently overwritten)                                 |

<!-- ingestion-targets:end -->

**Total Phase 1 target across worlds: 6,653 records** at v1.

(Brief stated 6,753 in its summary line; the row-by-row sum is 6,653.
Builder kept the per-row numbers as PI directed and corrected the
tally line to match. The 100-record difference is a tally typo, not a
target change.)

The W-1 atomic_molecular_primitives row carries 5,600 = 600 atomic
+ 5,000 molecular as a single combined target because the world model
unifies them at the persistence layer. Per-record-type breakdowns
appear in `reports/factory_daemon_progress/atomic_molecular_primitives.json`
under `sources_completed` once ingestion runs.

## Phase 2 (after Phase 1 validates clean)

Targets PI has delegated for the next round once Phase 1 cycles
clean three times in a row with no methodology violations:

* W-1 molecular: scale to 50,000 (full ChEBI + DrugBank + KEGG full)
* W1 crn: scale to 200 (KEGG full bacterial reference set)
* W4 morphogenesis: scale to 500 (FlyBase + WormBase + ZFIN substantive)
* W6 ecosystem: scale to 500 (LTER all sites + Movebank substantive)
* W7-W12: scale to 200-500 per world (per-source diligence)

## Phase 3 (long arc; magnum-opus)

Long-horizon targets requiring tooling beyond Phase 2:

* W-1 molecular: full PubChem subset (1M+ records) — needs index
  + budget tuning + likely DuckDB swap for query speed
* Tree-of-life biology grounding broadly (gigabase per phylum)
* Per-substrate density to ≥ 50 for all leaning-eligible cells

These are NOT in scope for the daemon currently being launched.
Phase 2 and Phase 3 each get their own ratification cycle; PI signs
each phase before the daemon promotes from one to the next.

## Aggregate ratification gates (Phase 1 launch)

All five must hold before the daemon flips on. Status as of CB-014:

1. ✅ PI signature on this Phase 1 table (delegated to Architect; see ratification block below).
2. ✅ `make_source_object_generation` green for the four non-floor source-object adapters.
3. ✅ `make_campaign_026` green (current `post_run_hash sha256:b746ea0e...` matches the one in `BUILD_LOG.md` TASK-FLOOR-BFG entry).
4. ✅ `factory_daemon.bat` fail-fast check passes (CB-013 T1 deliverable).
5. ✅ `BUILDER_INGESTION_MONITORING_PLAYBOOK.md` shipped (CB-013 T2 deliverable). Stop/resume drill executed in CB-013 tests + CB-014 first-cycle launch.

## Re-ratification cadence

This table is reviewed:

* After every Phase boundary (Phase 1 → 2 → 3 ratifications).
* Monthly during steady-state monitoring.
* After any source-object adapter change that materially affects
  available volume.

Increase a target only if (a) the source provably has more clean
records to give and (b) per-world budget allows.

## PI ratification signature block

```json
{
  "status": "RATIFIED",
  "ratified_by": "James Dye (PI), via delegated authority to Architect Claude",
  "ratified_at": "2026-05-07T14:07:39Z",
  "spec_version": "INGESTION_TARGETS_v1_phase1_substantive",
  "delegation_note": "PI's exact words: 'And anything I didn't answer, I trust your judgment, bro.' Architect Claude ratified Phase 1 targets per substantive-not-toy directive captured in PI directive section above. Builder (CB-014) re-stated the substantive-not-toy directive verbatim and applied it to every cell rather than collapsing to v0.1 floor numbers.",
  "phase": 1,
  "phase_total_records": 6653,
  "next_phase_review_trigger": "three consecutive clean Phase 1 cycles with zero methodology violations"
}
```

Builder note (CB-014): targets above were calibrated against:

* W-1 atomic / molecular: CB-011 ran 1,394 W-1 records persisted on a
  toy-size pull (NIST seed elements + PubChem CID 1-2000 subset).
  The Phase 1 target 5,600 = 600 atomic + 5,000 molecular reflects
  the substantive-not-toy directive: full periodic table coverage for
  atomic, ChEBI biological + KEGG metabolites + DrugBank approved
  for molecular. Adapter expansion may be required to reach the
  ChEBI + DrugBank breadth — this is acceptable producer-side work
  for Phase 1 and tracked under follow-up tickets, not within the
  daemon-launch ticket itself.
* W0 math primitives: 200 covers the Strogatz + Guckenheimer-Holmes
  catalog plus the Sprott / Chen / Lu / Chua family additions.
  6 records present on disk; expansion to 200 is per-record curation
  work that fits the same source-bound provenance pattern the
  existing math primitive seed corpus uses.
* W1-W12 simulation worlds: targets aligned with the Phase 1 numbers
  PI provided. Where the source is named ("KEGG top-50 reference
  organisms", "Allen Brain Atlas representative"), the source_basis
  column documents the canonical resource the Phase 1 ingestion will
  draw from.
* W13: held at 3, as in v0.1, per the falsifier-active state.

If the daemon's Phase 1 cycle observes that any source named in the
basis column is unreachable, rate-limited, or returns under the
target volume, that goes to BUILD_LOG as a Phase 1 source-availability
note and is escalated to PI in the next monitoring session — NOT
silently dropped (D14 / D17 / D22 binding).
