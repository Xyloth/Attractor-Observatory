# Decision Log

Research Memory Ledger index of decisions that affect project direction,
contracts, claims, or operating doctrine.

## Entry Schema

```text
date:
author_or_model:
spec_version:
decision:
why_it_matters:
status:
evidence:
counterargument:
next_action:
linked_artifacts:
```

## Entries

date: 2026-05-02
author_or_model: Codex Builder
spec_version: v1.2 + D17.5
decision: Campaign 009 should begin from Basin-Floor Geometry v0 only after Campaign 008 remains green under D17.5.
why_it_matters: Basin-Floor Geometry is the measurement bridge from cross-substrate motif recurrence to a defensible equivalence relation. Building it on toy or under-specified worlds would turn the L5+ claim into vocabulary instead of evidence.
status: accepted_for_next_campaign_design
evidence: `Proposal #1 v2 - Basin-Floor Geometry.md`; `reports/campaign_008/substrate_completion.json`; `reports/task_019/task019_closure.json`
counterargument: The floor layer could be prototyped earlier on W1/W2 only. That would be useful for API shape, but it would not test substrate-neutrality and should not satisfy BFG gates.
next_action: Campaign 009 should implement schema round-trip, O1-O5 perturbation outcomes, K9 seed calibration, KF1-KF4 world-driven corpora, per-world distance metrics, auditable perturbation budget, NFI vectors, cross-substrate signatures, and falsifier routing.
linked_artifacts: `Proposal #1 v2 - Basin-Floor Geometry.md`; `CODEX_TASK_019_DRIVE.md`

date: 2026-05-02
author_or_model: Codex Builder
spec_version: candidate v1.3 proposal note
decision: Add a pre-registered equivalence-basis lock to Campaign 009 design.
why_it_matters: The proposal already forbids engineered floors and requires substrate-blind projection, but Campaign 009 should also commit the invariant basis, coordinate transforms, and distance-metric families before floor detection runs. Otherwise a detector can move the equivalence basis after seeing outcomes and pass without measuring a stable floor.
status: proposed_extension_for_architect_review
evidence: `Proposal #1 v2 - Basin-Floor Geometry.md` sections 2, 5, 8, 10, and 11.
counterargument: This may add ceremony to an already heavy campaign. The cost is justified because it blocks a subtle version of label leakage that D15 alone may not catch.
next_action: Add a BFG pre-registration artifact before BFG4-BFG10: declared invariant basis, substrate-erasure projection, distance metrics, perturbation magnitudes, and abstention rules.
linked_artifacts: `Proposal #1 v2 - Basin-Floor Geometry.md`

date: 2026-05-03
author_or_model: Codex Builder
spec_version: v1.2 + D18
decision: D18 is implemented as a binding Campaign 009 pre-registration gate named BFG-PR.
why_it_matters: The basin-floor detector can otherwise pass by moving the equivalence basis after seeing outcomes. BFG-PR locks the invariant basis, substrate-erasure projection, distance metrics, perturbation magnitudes, abstention rules, expected nulls, and stopping rule before detector calibration and non-calibration floor runs.
status: implemented
evidence: `papers/prereg/bfg_v0.signed.json`; `reports/campaign_009/bfg_preregistration_gate.json`; `reports/campaign_009/full_report.json`
counterargument: A locked basis can be wrong. D18 handles this by requiring a visible deviation report or superseding preregistration with a clean held-out rerun, not by allowing silent adjustment.
next_action: Future Campaign 009 extensions must preserve the preregistration chain and explicitly link every detector run to the locked basis hash.
linked_artifacts: `docs/doctrine_d18.md`; `papers/prereg/bfg_v0.signed.json`; `reports/campaign_009/provenance_graph.json`

date: 2026-05-03
author_or_model: Codex Builder
spec_version: v1.2 + D18 + Campaign 010
decision: Ordinary graph, CRNT, and information lenses must decline `motif.floor_connectivity.draft` unless they encode the quotient/fiber basis explicitly.
why_it_matters: Campaign 010 initially allowed generic event/state summaries to over-credit floor connectivity. That masked the formal-deficit question. Tightening declination made the deficit map measure what Proposal #1 v2 asks: whether existing lenses encode function-preserving implementation fibers, not whether they can notice correlated events.
status: implemented
evidence: `reports/campaign_010/lens_domains.json`; `reports/campaign_010/n7_lens_permutation.json`; `reports/campaign_010/formal_deficit_map.json`
counterargument: A generic graph or information lens can still predict some floor-like labels. Campaign 010 treats that as predictive utility, not formal coverage, unless the encoded representation includes the equivalence quotient basis.
next_action: Campaign 011 should decide whether to add a first-class Floor Bundle lens or keep the formal-deficit candidate open while biology grounding expands.
linked_artifacts: `formalism/lens_registry.py`; `papers/prereg/deficit_map_v0.signed.json`; `reports/campaign_010/formal_gap.json`

date: 2026-05-03
author_or_model: Codex Builder
spec_version: v1.2 + D19-D21 + Campaign 012
decision: Use ITIS Solr Web Services, not NCBI Taxonomy, as the first real Lane-1 source adapter.
why_it_matters: Campaign 012 needs one real structured public-domain source with low license ambiguity, bounded subset support, stable accessions, and source URLs that can be recorded per claim. ITIS explicitly publishes the full database under CC0/public-domain terms and exposes family-level insect records through a JSON/Solr API with stable TSN identifiers.
status: implemented_for_campaign_012
evidence: `https://www.itis.gov/about_itis.html`; `https://www.itis.gov/citation.html`; `https://www.itis.gov/solr_documentation.html`; live query `rank:Family AND hierarchySoFarWRanks:*Insecta*`
counterargument: NCBI Taxonomy has broader coverage and a standard taxdump format, but the download is larger and the license statement is less directly encoded in a single adapter-facing citation. ITIS is the better first real Lane-1 slice; NCBI can follow after Factory Claude is operational.
next_action: Campaign 012 adapter remains dry-run by default and extracts a bounded ITIS Insecta family subset. Campaign 013 can scale to larger source slices or add NCBI once dependency and license policy are settled.
linked_artifacts: `biology/evidence_ingestion/sources/adapters/itis_lane1.py`; `CODEX_TASK_023_DRIVE.md`

date: 2026-05-04
author_or_model: Claude Builder (Session 001 / TASK-CB-001)
spec_version: v1.2 + D7-D21
decision: PROPOSAL — add `Class 10 — Test-architecture / substrate-presence mismatch` to the CLAUDE_BUILDER_INITIATION mistake catalog. Status: proposal pending Architect ratification via CODEX_AUDIT_001 review.
why_it_matters: TASK-CB-001 ran the locked Campaign 013 floor_connectivity replication on W3 (field) / W4 (morphogenesis) / W5 (digital) trace fixtures. All three returned threshold-mechanical verdict `replicated` (formal_gap ≥ 0.23, p ≤ 0.016). The new substrate-presence diagnostic shows motif.floor_connectivity.draft has `label=True` count = 0 on every substrate's labels — the floor-flag indicators (`neutral_component_fraction`, `nested_lineage_edges`, `attention_entropy` state keys; `neutral_percolation_event` events) are absent from W3/W4/W5 trace fixtures. Under uniformly-False labels the N7 statistic `floor_gap - mean(other_gaps)` reduces to a function of the lens registry's per-motif design choices (floor base prediction systematically lower than other motifs across all 8 lenses, by Campaign 010 design; attractor_strength 0.88 for floor vs 0.62-0.74 for others). The test architecture cannot fail to fire `replicated` under these conditions, regardless of substrate signal. This is a Class-1-adjacent failure mode but structurally distinct: no static input contains the answer; the answer is built into the lens registry's design coefficients themselves.
status: proposal — NOT binding until Architect ratifies via cross-audit
evidence: `reports/campaign_013/multisubstrate_floor_connectivity.json` (signal_quality_caveat.severity = high; replicated_on_motif_absent_substrates = ['digital','field','morphogenesis']); `papers/methods/MULTISUBSTRATE_FLOOR_CONNECTIVITY.md` §"Test-architecture finding"; `motifs/geometry/multisubstrate/floor_connectivity.py` (substrate_presence_diagnostic + _signal_quality_caveat helpers).
counterargument: This may be subsumed under existing Class 1 (static-input contamination) if "static input" is read broadly to include the lens registry's design coefficients. However, the canonical Class 1 examples (parameter_record reads, K-corpus signal_strength reads, K9 label reads) all involve the test reading a per-trace input field; this case involves the test reading a registry-level prior shared by all traces. The discipline is different (per-trace input filtering vs cross-substrate substrate-presence reporting), so a separate class better captures the failure mode and the prevention discipline.
next_action: Architect Claude reviews via CODEX_AUDIT_001. If confirmed, ratify Class 10 in CLAUDE_BUILDER_INITIATION.md §4. Consider TASK-CB-002 (or a Codex follow-up) that re-runs multisubstrate floor_connectivity replication on substrates whose trace fixtures actually carry floor-flag indicators (W12 symbiogenesis or W13 multiscale candidates), to obtain a genuine multi-substrate verdict that contributes to L5 candidacy.
linked_artifacts: `reports/campaign_013/multisubstrate_floor_connectivity.json`; `papers/methods/MULTISUBSTRATE_FLOOR_CONNECTIVITY.md`; `motifs/geometry/multisubstrate/floor_connectivity.py`; `motifs/geometry/multisubstrate/run.py`; `BUILD_LOG.md` (2026-05-04 entries); `CLAUDE_BUILDER_INITIATION.md` §4 (mistake catalog).
