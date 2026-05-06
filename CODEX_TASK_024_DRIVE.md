# Codex — TASK-024: Campaign 013, Drive to Milestone

*Architect message. Read in full before resuming. Canon for the duration of TASK-024.*

---

## 1. Where you stand and what changes

TASK-023 closed Campaign 012 cleanly. 24/24 gates green, 252 pytests, ITIS adapter shipped under CC0, Factory scaffolding ready, KP corpora hardened, KE1 expanded with subtle misalignment cases, W7 templates renamed under axis-configuration discipline, floor-connectivity replication protocol pre-registered.

**The framing has changed.** The PI and Architect met. Two takeaways binding on this campaign:

**Takeaway 1: Stop adding infrastructure.** The doctrine arc, the substrate-neutral ontology, the Research Ingestion Factory, the Factory-Claude separate-instance pattern — each of these solved real problems but pushed back the original v1.0 thread (build worlds → mine motifs → compare to biology → find where math fails). We've built ~70-80% of v1.0's program with substantial discipline added on top, and the missing 20% is the part that gives the work scientific meaning: comparison to real biology. **No new doctrine after D21. No new schemas. No new lenses. No new worlds. No new ontology layers. No Factory Claude as separate instance.** If a real failure mode bypasses existing rules during this campaign, surface it in `decision_log.md` for post-milestone review; do not ship D22 mid-campaign.

**Takeaway 2: Drive to one real result, then write up.** Campaign 013 produces the floor_connectivity replication verdict and the first L3-style overlap result. Campaign 014 produces atlas + paper drafts + reproducibility bundle. **Then we stop building.** The Estimation Loop empirics, the doctrine arc, and one striking science result is enough material for the portfolio piece and for a methodology paper. Anything beyond Campaign 014 happens only if Campaign 013's results genuinely demand follow-up.

This driver reflects that framing. The campaign is bounded. The gates are the stopping signal. Estimation Loop continues; trust your prior.

## 2. Doctrine state

D7 through D21 remain binding, no additions. Two patterns to watch:

- **The "useful one more thing" temptation.** Mid-campaign, you may notice a place where one more piece of infrastructure would clean up an audit pathway or make a result tidier. The discipline this campaign requires is: log it in `decision_log.md` for post-milestone review and *keep going*. Tidiness is not a milestone deliverable; honest results are.
- **Honest negative results.** If the floor_connectivity replication weakens or falsifies the candidate, that is a real publishable result. Do not adjust the equivalence basis, the lens registry, or the corpus selection to recover the original signal. D18 is binding. The verdict the protocol returns is the verdict.

## 3. Mission — One real science result

**Campaign 013** — five pillars, ~26 acceptance gates. Self-contained, no external instance, uses the infrastructure shipped through Campaign 012.

The two scientific outputs this campaign must produce:

- **A floor_connectivity replication verdict.** The Campaign 010 candidate (`motif.floor_connectivity.draft`, formal_gap 0.308, N7 p 0.002) gets re-evaluated on independent evidence under the protocol pre-registered in Campaign 012. Verdict: *replicated* (gap and p hold), *weakened* (gap reduced or p increased), *falsified* (gap below threshold), or *different result* (gap robust but in a different motif × lens pair). Whichever lands, it lands honestly.
- **A first L3-style overlap report.** Real insect taxa from ITIS, mapped against W7 swarm motifs, with ITIS-hierarchy-as-baseline-phylogeny correction, with ITIS-family-level-resolution sampling bias acknowledged, with ≥1 honest motif × clade overlap result. Whether the result is positive overlap, null, or negative-with-evidence, it is an honest measurement against real biology.

### Pillar A — Pre-launch schema discipline (~5 gates)

Bump `BiologicalClaim` from v1.0 → v1.1 with the high-priority additions from `FACTORY_END_STATE_AND_SCHEMA_DISCIPLINE.md` §2.1, *before* scale ingestion runs. Existing 200 KE1 + 150 ITIS records migrate via pure-function migration. This is the bounded one-time cost of getting the schema right early.

Fields added in v1.1:
- `spatial_context` (geographic_range, biome, biogeographic_region — null where source doesn't carry)
- `temporal_context` (fossil intervals, modern_status — null for synthetic)
- `life_stage_context` (life_stage, developmental_phase)
- `scope_level` (population_level / individual_observation / inferred / theoretical)
- `observation_setting` (wild / captive / inferred_from_morphology / behavioral_assay / etc.)
- `taxon_synonym_chain` with `accepted_name_at_extraction_time` and `accepted_name_currently`
- `source_authority_class` (peer_reviewed / curated_database / etc.)
- `claim_publication_year`
- `normalization_version`
- `schema_version_at_extraction`

Migration discipline: pure functions, tested against fixtures, derivable fields populated from cache where possible, non-derivable fields null with `requires_replay: true` flag where appropriate.

### Pillar B — Floor connectivity replication (~7 gates)

Execute the protocol from `papers/methods/FLOOR_CONNECTIVITY_REPLICATION_PROTOCOL.md`. The discipline is D18 (no equivalence-basis drift): the basis hash, lens registry version, and N7 methodology are all locked from Campaign 009 / 010. The replication runs against an *independent* evidence corpus (held-out partitions + W7 exploratory_densified data) with no protocol changes.

Verdict reported honestly:
- **Replicated** if formal_gap > 0.20 (declared threshold) AND N7 empirical_p < 0.05 on the independent corpus.
- **Weakened** if formal_gap is reduced (e.g., 0.15-0.20) or N7 p increased (0.05-0.10) but signal direction holds.
- **Falsified** if formal_gap < 0.15 OR N7 p > 0.10.
- **Different result** if a different motif × lens pair surfaces above thresholds while floor_connectivity falls.

The verdict updates `formal_deficit_map.json` and `papers/falsifiers/`. If falsified, the candidate goes to the falsifier ledger with a substantive MD explaining what was falsified and why.

### Pillar C — First L3 overlap (insects × W7 motifs) (~9 gates)

The science result of Campaign 013. Real insect taxa from ITIS, mapped against W7 motifs, with honest controls.

**Step 1 — Scale-ingest insects from ITIS.** You wrote the adapter; run it at scale. ≥1000 BiologicalClaim records about insect taxa at family level (and order level where available). All under CC0, full provenance. Schema v1.1 from Pillar A. Records flow through the audit pipeline; raw_extracted by default.

**Step 2 — Normalize against ontology.** Process-role and interaction-channel normalizers fire on each claim. Map surface labels in the ITIS records (where they occur — ITIS is mostly taxonomic, but it carries some trait flags) to ontology references. Many records will normalize sparsely (ITIS doesn't carry rich behavioral data); that's expected and acceptable.

**Step 3 — Run W7 detection on the densified templates.** The 12 W7 organism templates from Campaign 011 are the simulation side. Run motif detection on them under the substrate-blind projection from Campaign 009.

**Step 4 — Cross-reference.** For each motif, list:
- W7 templates exhibiting the motif at confidence ≥ τ
- ITIS taxa with claim records that suggest the motif (via process-role normalization or via direct trait flags)
- Phylogenetic distribution of the suggesting taxa across ITIS hierarchy (family / order / class)

**Step 5 — Phylogenetic correction.** Use the ITIS taxonomic hierarchy as a baseline phylogeny. Compute a hierarchy-controlled overlap statistic: for each motif, count not raw taxon co-occurrence but *family-level independent occurrences* (i.e., adjust for the fact that all taxa within one family share a recent common ancestor, so the observation count should reflect the number of *families* exhibiting the trait, not the number of species). This is a v0 phylogenetic correction; document the limitation that ITIS hierarchy is taxonomic, not phylogenetic.

**Step 6 — Sampling bias acknowledgement.** ITIS represents some clades better than others (Lepidoptera and Hymenoptera are well-represented; many other insect orders are sparse). Report the analysis with and without subsampling correction.

**Step 7 — Honest verdict per motif.** For each W7 motif tested, the report states:
- *Positive overlap*: the motif appears in W7 simulation, the corresponding process roles appear in real insect biology across multiple families, the family-level independence count exceeds the null at p < 0.05.
- *Null*: the motif is detected in some sampled W7 templates and some sampled real taxa, but the overlap is not greater than expected by chance under the family-level null.
- *Negative with evidence*: the motif is detected in W7 templates but not in any sampled real insect taxa, OR vice versa. Explicit negative-evidence claim, citing which families were checked and what trait records show.
- *Insufficient data*: the sampling is too sparse for an honest verdict; documented as such.

**Step 8 — Claim status assignment.** Per D21, claim-bearing observations require `density_class >= claim_ready_densified` for the world. W7 is currently `exploratory_densified`. The L3 overlap report's records carry `mode_tag: exploratory`. Promotion to claim-bearing is *not* a Campaign 013 deliverable; this is honest first-overlap analysis under exploratory tagging.

### Pillar D — Atlas seed (~3 gates)

The atlas exists as a directory but has no integrated rendering. Seed it with the first 5-10 motif-instance entries from Campaigns 002, 009, 010, and 013 results. Schema:

```
AtlasEntry = {
  entry_id:                AtlasEntryID,
  motif_id:                MotifID,
  motif_registry_version:  SemVer,
  closure_rank:            enum {C0, C1, C2, C3, C4, C5, C6, C7, C8} | null,
  stabilization_strategy:  enum (energy_capture / boundary_maintenance / flow_routing /
                                  memory / repair / replication / coordination / prediction /
                                  externalization),
  simulation_examples:     list[TraceID],
  biological_examples:     list[BiologicalClaimID],
  formal_lens_coverage:    dict[LensID, CoverageScore],
  attractor_strength:      AttractorStrengthVector,
  formal_gap_score:        float,
  open_questions:          list[str],
  mode_tag:                enum {foundational, exploratory, claim-bearing},
  spec_version:            ContentHash,
}
```

Atlas integrity: every entry's provenance chain leads to verified traces and audited claims. The atlas is exploratory by default; claim-bearing entries require PI signature.

### Pillar E — Regression and final report (~2 gates)

Full regression: Campaigns 002 through 012 all green. ≥260 pytests passing. Campaign 013 full_report.json status `green` with all gates passed. `make_campaign_013.py` regenerates from cold.

## 4. Acceptance gates

| Gate | Pillar | Threshold | Source |
|---|---|---|---|
| SD1 | A | `BiologicalClaim` v1.1 schema declared with §2.1 high-priority fields; round-trip exact; backward-compat tests pass | `biology/evidence_ingestion/schemas/biological_claim.py`, tests |
| SD2 | A | Migration function `migrate_1_0_to_1_1` implemented as a pure function; tested against fixture records; derivable-vs-non-derivable fields documented | `biology/evidence_ingestion/migrations/`, tests |
| SD3 | A | All existing 350 records (200 KE1 + 150 ITIS) migrated to v1.1; non-derivable fields flagged `requires_replay: true`; cache integrity invariants pass | `reports/campaign_013/schema_migration.json` |
| SD4 | A | Schema versioning CI lint operational: every BiologicalClaim record carries `schema_version_at_extraction`; lint catches missing or incorrect versions | lint + tests |
| SD5 | A | Cache integrity invariants verified post-migration: every Layer 2 record cites a Layer 1 cache hit; provenance chains intact | `reports/campaign_013/cache_integrity.json` |
| FC1 | B | Replication protocol loaded from Campaign 012; basis hash confirmed unchanged (sha256:ce9e24...); lens registry version confirmed unchanged | `reports/campaign_013/replication_basis_lock.json` |
| FC2 | B | Independent evidence corpus assembled: ≥30 evidence rows from held-out Campaign 008/009/010 partitions + W7 exploratory_densified data, with no overlap with Campaign 010's original deficit-map evidence | `reports/campaign_013/replication_corpus.json` |
| FC3 | B | N7 lens-permutation null re-run at N=1000 on independent corpus; null distribution computed under the locked equivalence basis | `reports/campaign_013/replication_n7.json` |
| FC4 | B | Formal gap re-computed under same equivalence basis on independent corpus | `reports/campaign_013/replication_gap.json` |
| FC5 | B | Verdict reported: replicated / weakened / falsified / different-result, with honest threshold check (formal_gap > 0.20 AND N7 p < 0.05 = replicated; etc.) | `reports/campaign_013/replication_verdict.json` |
| FC6 | B | Updates to `formal_deficit_map.json` reflect the verdict; if falsified, falsifier ledger entry with substantive MD; if replicated, candidate's evidence chain extended | `reports/campaign_010/formal_deficit_map.json` updated, `papers/falsifiers/` updated |
| FC7 | B | If verdict is falsified or weakened: TRUTH_PASS.md updated with the downgrade and provenance | `papers/methods/TRUTH_PASS.md` |
| L3-1 | C | Insect family-level slice ingested from ITIS at scale: ≥1000 BiologicalClaim v1.1 records under CC0 with full provenance | `reports/campaign_013/itis_insect_extraction.json` |
| L3-2 | C | Process-role and interaction-channel normalizations fired on each claim; sparse normalizations reported honestly (many ITIS records carry only taxonomy, not behavior) | `reports/campaign_013/itis_normalization_summary.json` |
| L3-3 | C | W7 motif detection on the 12 templates under substrate-blind projection; results table with confidence per template per motif | `reports/campaign_013/w7_motif_detection.json` |
| L3-4 | C | Cross-reference table: per motif, W7 templates exhibiting the motif × ITIS taxa with corresponding process-role evidence × phylogenetic distribution by family/order | `reports/campaign_013/cross_reference.json` |
| L3-5 | C | Phylogenetic correction: family-level independent-occurrence count computed; null distribution computed under shuffled phylogeny; ITIS-hierarchy-as-baseline limitation documented | `reports/campaign_013/phylogenetic_correction.json` |
| L3-6 | C | Sampling bias correction: analysis reported with and without ITIS coverage adjustment; documented under-sampled clades | `reports/campaign_013/sampling_bias.json` |
| L3-7 | C | Per-motif verdict: positive overlap / null / negative-with-evidence / insufficient-data, with cited evidence; ≥1 motif lands an honest verdict | `reports/campaign_013/l3_overlap_report.json` |
| L3-8 | C | Claim status assignment: all L3 records carry `mode_tag: exploratory` per D21 (W7 is exploratory_densified, not claim_ready_densified); no claim-bearing promotions | provenance graph + tests |
| L3-9 | C | First L3 overlap report committed at `papers/methods/L3_OVERLAP_INSECTS_W7.md` with honest verdicts, controls, limitations | document |
| AT1 | D | Atlas DB schema for `AtlasEntry` implemented; round-trip exact | `atlas/db.py`, tests |
| AT2 | D | First 5-10 atlas entries seeded from Campaign 002 / 009 / 010 / 013 results with full provenance chains | `atlas/entries/`, `reports/campaign_013/atlas_seed.json` |
| AT3 | D | Atlas integrity check: every entry's provenance chain leads to verified traces and audited claims; CI lint catches broken chains | lint + tests |
| RG | E | Full regression: Campaigns 002, 005, 006, 007, 008, 009, 010, 011, 012 all green; ≥260 pytests passing; D14, D17.5, D18, D19, D20, D21 lints zero violations | `reports/campaign_013/regression.json` |
| FR | E | `reports/campaign_013/full_report.json` shows status `green` with all gates passed; `make_campaign_013.py` regenerates from cold | `make_campaign_013.py` |

26 gates total. Bounded. Sized for regular-speed completion at your current pace.

## 5. Sequencing recommendation

Reorder with rationale if you have a better sequence.

1. **SD1–SD5 — Schema migration first.** The v1.0 → v1.1 bump is the foundation. All subsequent work happens under v1.1. Bounded one-time cost; defer at your peril.
2. **L3-1 — Scale ITIS ingestion.** With v1.1 schema in place, run the adapter at scale on insect families. ≥1000 records. This is the biggest bulk-time gate and gates Pillar C's downstream work.
3. **L3-2 — Normalization.** Process-role and channel normalizers fire on the ingested claims. Sparse coverage is fine; honest reporting matters.
4. **FC1–FC7 — Floor connectivity replication.** Independent of L3 work; can run in parallel with L3-1 ingestion. Verdict reported honestly.
5. **L3-3, L3-4 — W7 detection + cross-reference.** Once normalizations exist and W7 templates are renamed (Campaign 012), this is mechanical: detection table + cross-reference table.
6. **L3-5, L3-6 — Phylogenetic and sampling controls.** These are real numerical work but bounded. Document limitations honestly.
7. **L3-7, L3-8, L3-9 — Verdicts, claim status, report.** First L3 overlap report committed. ≥1 motif lands an honest verdict (positive, null, negative-with-evidence, or insufficient-data).
8. **AT1–AT3 — Atlas seed.** Schema, first entries, integrity check.
9. **RG + FR — Full regression and final report.**

## 6. Forbidden patterns for TASK-024

- **No new infrastructure.** No new doctrine, schemas, lenses, worlds, ontology layers, calibration corpora, factory adapters beyond what exists. If you observe a real failure mode that bypasses D7-D21, surface in `decision_log.md` for post-milestone review; *keep going* on this campaign.
- **No equivalence-basis drift in replication.** D18 binding. The Campaign 009 BFG-PR basis hash is locked; lens registry version is locked; N7 methodology is locked. The replication's verdict is whatever those locked instruments produce on the independent corpus.
- **No engineered L3 verdict.** Honest negative is publishable. Honest null is publishable. Adjust the analysis to recover an inconvenient verdict and you've D9'd the science layer.
- **No claim-bearing promotions.** W7 is `exploratory_densified`, not `claim_ready_densified`. All Campaign 013 records carry `mode_tag: exploratory` per D21. If you find yourself wanting to upgrade a record, the answer is: defer to post-milestone.
- **No skipping the schema migration.** Pillar A is the foundation. Don't run scale ingestion against v1.0 schema; the migration cost compounds with every additional record.
- **No new external sources.** Lane 1 only, ITIS only (CC0). No NCBI Taxonomy adapter, no OTL adapter, no GBIF adapter. The point is to land one result with what we have, not to expand the source corpus.
- **No regression of D14, D17.5, D18, D19, D20, D21 lints.** Existing doctrine remains binding. Zero violations.

## 7. How to begin

1. **Open the TASK-024 Estimation Loop record.** Class: `integration`. Scope: 8. Complexity: 8 (similar to Campaign 012; smaller than 011). Estimated minutes: report your prior median × your honest belief. The campaign is bounded; don't undershoot, don't pad.

2. **Re-read `FACTORY_END_STATE_AND_SCHEMA_DISCIPLINE.md` §2.1** for the high-priority schema field list, and §3 for the migration policy.

3. **Re-read `papers/methods/FLOOR_CONNECTIVITY_REPLICATION_PROTOCOL.md`** to confirm the locked instruments (basis hash, lens registry version, N7 methodology).

4. **Pillar A first.** Schema migration is the foundation. Do not run Pillar C (scale ingestion) against v1.0 schema.

5. **Pillar B (replication) and Pillar L3-1 (scale ingestion) can run in parallel.** Independent code paths. Either order works; pick whichever's cleaner for your session structure.

6. **Drive through the campaign.** The 26 gates are the stopping signal. Acceptance outcome `pass` only when all 26 are green and the numbers are written into `reports/campaign_013/full_report.json`. Until then `in_progress`.

## 8. Three things to keep in front of you

1. **Honest verdicts produce striking results.** A floor_connectivity replication that *falsifies* the candidate is more striking than a half-engineered "candidate weakly replicated." A first L3 overlap that lands *negative-with-evidence* on a motif is more striking than a hand-tuned "moderate overlap." The portfolio piece, the methodology paper, and the science paper all benefit from honest verdicts. Engineered passes corrupt all three.

2. **The schema bump is non-negotiable.** Every claim ingested under v1.0 today is a claim that needs migration tomorrow. Doing the migration when there are 350 records is bounded; doing it when there are 50,000 is not. This is the archive-before-extract discipline applied to schema choices: get them right early.

3. **Campaign 014 is the publishing campaign, not another build campaign.** After this lands, the next work is atlas rendering, paper drafts, reproducibility bundles, and the portfolio piece. Plan accordingly: produce results in this campaign that are *worth* writing up, in formats (JSON reports, methods documents, MD verdicts) that paper-draft work can consume directly.

## 9. Closing

You shipped the factory's first real-source adapter, hardened the calibration corpora, fixed the W7 template naming discipline, and pre-registered the floor_connectivity replication protocol. You're now driving to the science result the project was built to produce.

Campaign 013 lands one honest replication verdict and one honest L3 overlap result. Whatever they say, they say honestly under the doctrine and instruments we've spent twenty-three tasks building. After this closes, Campaign 014 writes up what we have. Then we stop building and start showing what we found.

The trace is the artifact. Calibration is the floor. The gates are the stopping signal. **Honest verdicts are the milestone.**

— The Architect, on behalf of the project, under spec v1.2 plus binding doctrine D7–D21.
