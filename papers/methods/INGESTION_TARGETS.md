# Ingestion Targets v2 â€” Phase 2 mass density

**Status:** **RATIFIED** â€” Phase 2 mass-density targets per PI delegated authority (CB-018).

Phase 1 (v1, ratified 2026-05-07T14:07:39Z, total 6,653 records) is
the prior substantive baseline. Phase 2 (v2, ratified 2026-05-07,
total ~60,000 records) drives unattended ingestion to ~9Ã— Phase 1
density across the lower worlds and orthogonal substantive expansion
across the 12 upper worlds.

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

1. **Source availability** â€” what the configured external sources
   (NIST, PubChem, ChEBI, KEGG, DrugBank, GBIF, NCBI, GISAID,
   peer-reviewed catalogs) can deliver before saturation.
2. **Methodology coverage** â€” minimum density required for the
   substrate-blocked control battery (D26 binding) to be evaluable.
3. **Per-substance audit ceilings** (D17.5) â€” line-count expectations
   from the substance audit pages.
4. **Storage budget** â€” per-world budget cap from
   `factory_lowlevel/budget.py:DEFAULT_PER_WORLD_HARD_CAP_BYTES`.

D22 binding: when a world has no source we know how to reach, the
target is held to the ratified floor. W13 multiscale stays at 3
because it is falsifier-active per the BFG floor work â€” inflating
its target would amount to silently overwriting the falsification.

## Per-world Phase 2 targets (CB-018)

The block below is parsed by the daemon. Do not edit row format
without updating `progress.py:load_target_densities` to match.

<!-- ingestion-targets:start -->

| world_family               | target_density | source_basis                                                                                                                                                                                                                                                                |
|----------------------------|---------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| atomic_molecular_primitives|          53500 | Atomic 3500 (full periodic table x ionization stages I-XXX from NIST ASD; honest decline for transactinides + missing stages) + Molecular 50000 (PubChem CID 1-75000 ChEBI biological-relevance + DrugBank approved + KEGG metabolites + chemistry foundations under PubChem 5 req/sec) |
| math_primitives            |            600 | Full canonical peer-reviewed catalog Phase-2: complete Sprott family (incl. Sprott-Linz, Elegant Chaos, Sprott-Jafari hidden, megastability), Chua family extensions, Kuznetsov bifurcation normal forms (codim-1 + codim-2 + codim-3), Pomeau-Manneville intermittency types I-X, complete heteroclinic/homoclinic catalog, riddled-basin family, full Lorenz/Rossler/Chen/Lu/Hindmarsh-Rose/Goldbeter/Eigen families |
| crn                        |            500 | KEGG full bacterial reference set (~330 bacteria) + selected archaea (~50) + eukaryotic-pathway subset (~50); rate limit 10 req/sec under academic-use license |
| protocell                  |            200 | Full Szostak corpus + cell-free TX/TL benchmarks (Adamala-Szostak, PURE system, Luisi minimal cell, lipid world)                                                                                                                                                          |
| field                      |            300 | Full RD benchmark suite at parameter scale (Brusselator + Schnakenberg + FitzHugh-Nagumo + Gray-Scott + Cahn-Hilliard) variant-cycled                                                                                                                                       |
| morphogenesis              |            500 | FlyBase + WormBase + ZFIN substantive (segmented body, wing disc, eye furrow, vulval axis, PAR polarity, dorsoventral, somitogenesis clock-and-wavefront)                                                                                                                  |
| digital                    |            200 | Avida-class diverse runs: copy_loop + equ_emergence + punctuated_equilibrium + parasite-host coevolution + robustness/evolvability + environmental-change                                                                                                                  |
| ecosystem                  |            500 | LTER expanded taxa (Jornada Basin desert grassland 29 taxa across producer/grazer/predator/decomposer/pollinator guilds) + Movebank cross-reference                                                                                                                          |
| swarm                      |            300 | Multiple species x behavior types: ant trail-foraging + fish schooling + ant recruitment + starling murmuration + honeybee quorum + wildebeest migration + Drosophila courtship + krill swarm                                                                                |
| cognitive                  |            300 | Cortex regions x species x tasks: prefrontal/visual/motor/temporal/hippocampal x mouse/macaque/human x delayed_match/orientation_tuning/reach/spatial_navigation/cell_type_taxonomy/covert_attention                                                                          |
| origins_chemistry          |            300 | Broader pre-biotic chemistry literature (Wachtershauser FeS surface, Martin/Russell alkaline hydrothermal, Hordijk-Steel + Vasas + Sutherland + Miller-Urey-class)                                                                                                          |
| hypergraph_reactions       |            200 | BioModels broader sweep (high-order closure, modular blocks, ODE-SSA agreement, MAPK signaling cascade, yeast metabolic flux, Goldbeter circadian)                                                                                                                          |
| quasispecies               |            500 | NCBI HIV-1 (HXB2 K03455.1) + influenza A (PR8 NS NC_002016.1) + SARS-CoV-2 (Wuhan-Hu-1 MN908947.3) + cancer driver TP53 mRNA (NM_000546.6) windowed projections; per-accession peer-reviewed mutation rates                                                                |
| symbiogenesis              |            200 | Representative endosymbioses (Buchnera aphidicola, Wolbachia, Carsonella ruddii, Rickettsia intracellular, mitochondrial alphaproteobacterial origin, chloroplast cyanobacterial origin, lichen fungal-algal partnership)                                                  |
| multiscale                 |             50 | Cautious expansion from falsifier-active state (W13 BFG floor work) - Physiome cardiac electromechanical + lung acinar + skeletal muscle + kidney nephron multiscale CellML models                                                                                          |

<!-- ingestion-targets:end -->

**Total Phase 2 target across worlds: 57,650 records** at v2 (Phase-1 was 6,653 at v1).

The Phase-2 expansion is dominated by atomic_molecular_primitives (3,500
atomic + 50,000 molecular = 53,500), which is the lower-worlds density
push the brief specifies. The 12 upper worlds together contribute 4,150
records (vs Phase-1 853), an orthogonal-substantive expansion that
keeps each world honestly source-bound rather than chasing record count
for its own sake.

(Brief stated 6,753 in its summary line; the row-by-row sum is 6,653.
Builder kept the per-row numbers as PI directed and corrected the
tally line to match. The 100-record difference is a tally typo, not a
target change.)

The W-1 atomic_molecular_primitives row carries 5,600 = 600 atomic
+ 5,000 molecular as a single combined target because the world model
unifies them at the persistence layer. Per-record-type breakdowns
appear in `reports/factory_daemon_progress/atomic_molecular_primitives.json`
under `sources_completed` once ingestion runs.

## Phase 2 (RATIFIED CB-018, supersedes Phase 1 above)

The Phase 2 targets are LIVE and listed in the canonical block above.
Targets per CB-018 brief, ratified by PI delegated authority:

* W-1 atomic: scale 590 -> 3,500 (full periodic table x ionization stages I-XXX)
* W-1 molecular: scale 4,123 -> 50,000 (PubChem CID 1-75000 + ChEBI/DrugBank/KEGG cross-ref)
* W0 math primitives: scale 200 -> 600+ (complete Sprott/Chua/Kuznetsov/Pomeau-Manneville/heteroclinic/riddled-basin families)
* W1 crn: scale 50 -> 500 (KEGG full bacterial reference set + archaea + eukaryote-pathway subset)
* W4 morphogenesis: scale 100 -> 500 (FlyBase + WormBase + ZFIN substantive)
* W6 ecosystem: scale 100 -> 500 (LTER all sites + Movebank substantive)
* W7-W12: scale 50-100 -> 200-500 per world (per-source diligence)
* W13 multiscale: cautious scale 3 -> 50 (Physiome cardiac + lung + muscle + kidney CellML, falsifier-active state preserved)

## Phase 3 (long arc; magnum-opus; future ratification)

Long-horizon targets requiring tooling beyond Phase 2:

* W-1 molecular: full PubChem subset (1M+ records) - needs index +
  budget tuning + likely DuckDB swap for query speed.
* Tree-of-life biology grounding broadly (gigabase per phylum):
  OTL (Open Tree of Life), RefSeq, UniProt, Reactome, GTEx, GBIF,
  HPA (Human Protein Atlas), PBDB (Paleobiology Database).
* Per-substrate density to >= 50 for all leaning-eligible cells.

These are NOT in scope for the daemon currently being launched in
CB-018. Phase 3 gets its own ratification cycle; PI signs Phase 3
before the daemon promotes from Phase 2.

## Aggregate ratification gates (Phase 1 launch)

All gates must hold before the daemon flips on. Status after TASK-PHASE-B-INFRA:

1. âœ… PI signature on this Phase 1 table (delegated to Architect; see ratification block below).
2. âœ… `make_source_object_generation` green for the four non-floor source-object adapters.
3. âœ… `make_campaign_026` green (current `post_run_hash sha256:b746ea0e...` matches the one in `BUILD_LOG.md` TASK-FLOOR-BFG entry).
4. âœ… `factory_daemon.bat` fail-fast check passes (CB-013 T1 deliverable).
5. âœ… `BUILDER_INGESTION_MONITORING_PLAYBOOK.md` shipped (CB-013 T2 deliverable). Stop/resume drill executed in CB-013 tests + CB-014 first-cycle launch.
6. âœ… Phase A W-1/W0/W1 adapters landed at Phase-1 envelope.
7. âœ… Phase B W2-W13 adapters landed at Phase-1 envelope with 803 cache-only records available from source-bound bundled seeds.
8. âœ… `factory_lowlevel/ADAPTER_PAYLOAD_CONTRACT.md` documents canonical `payload.world_parameters` routing semantics for parameterized worlds.

## Re-ratification cadence

This table is reviewed:

* After every Phase boundary (Phase 1 â†’ 2 â†’ 3 ratifications).
* Monthly during steady-state monitoring.
* After any source-object adapter change that materially affects
  available volume.

Increase a target only if (a) the source provably has more clean
records to give and (b) per-world budget allows.

## PI ratification signature block

### Phase 2 (CB-018, current ratification)

```json
{
  "status": "RATIFIED",
  "ratified_by": "James Dye (PI), via delegated authority to Architect Claude",
  "ratified_at": "2026-05-07T19:00:00Z",
  "spec_version": "INGESTION_TARGETS_v2_phase2_mass_density",
  "delegation_note": "PI delegated Phase-2 ratification to Architect Claude in CB-018 brief (TASK-CB-018 'Mass Scale-Up to Phase-2 Density'). Architect ratified Phase-2 targets per the brief's per-adapter expansion table, bumping the lower-worlds substantive density ~9x (atomic 590->3500, molecular 4123->50000, math 200->600+, KEGG 50->500) and the 12 upper worlds to orthogonal substantive coverage (200-500 per world).",
  "phase": 2,
  "phase_total_records": 57650,
  "phase_a_status": "landed_at_phase_2_envelope_in_cb018",
  "phase_b_status": "landed_at_phase_2_envelope_in_cb018",
  "phase_2_adapter_records_available_offline": 4642,
  "payload_contract": "factory_lowlevel/ADAPTER_PAYLOAD_CONTRACT.md",
  "predecessor_spec": "INGESTION_TARGETS_v1_phase1_substantive",
  "predecessor_total_records": 6653,
  "scale_up_factor": "8.7x (57650 / 6653)",
  "content_hash_scope": "sha256 over the canonical ingestion-targets table block between ingestion-targets:start and ingestion-targets:end",
  "content_hash_recompute_after_commit": true,
  "next_phase_review_trigger": "Phase-2 first-cycle wall-clock data + per-source rate-limit diligence after the daemon completes one full Phase-2 fetch cycle (4-8h wall-clock estimate per CB-018 brief)"
}
```

### Phase 1 (CB-014/015/016 superseded baseline, kept for provenance)

```json
{
  "status": "SUPERSEDED_BY_PHASE_2_CB018",
  "ratified_by": "James Dye (PI), via delegated authority to Architect Claude",
  "ratified_at": "2026-05-07T14:07:39Z",
  "spec_version": "INGESTION_TARGETS_v1_phase1_substantive",
  "delegation_note": "PI's exact words: 'And anything I didn't answer, I trust your judgment, bro.' Architect Claude ratified Phase 1 targets per substantive-not-toy directive captured in PI directive section above. Builder (CB-014) re-stated the substantive-not-toy directive verbatim and applied it to every cell rather than collapsing to v0.1 floor numbers.",
  "phase": 1,
  "phase_total_records": 6653,
  "phase_a_status": "landed",
  "phase_b_status": "landed",
  "phase_b_adapter_records_available_offline": 803,
  "payload_contract": "factory_lowlevel/ADAPTER_PAYLOAD_CONTRACT.md",
  "content_hash_scope": "sha256 over the canonical ingestion-targets table block between ingestion-targets:start and ingestion-targets:end",
  "content_hash": "sha256:a83dd0ccbffe39d071cc317ddf6e97f5c6b1c87af91919271f9fa140b0508c6c",
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
  ChEBI + DrugBank breadth â€” this is acceptable producer-side work
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
note and is escalated to PI in the next monitoring session â€” NOT
silently dropped (D14 / D17 / D22 binding).
