# Floor Connectivity Replication Protocol

Campaign: 013 preregistration beachhead

Target motif: `motif.floor_connectivity.draft`

This protocol pre-registers the replication path for the Campaign 010 formal-deficit candidate. Campaign 012 does not run replication.

## Locked Basis

- Campaign 009 BFG-PR equivalence basis hash: `sha256:ce9e243429a69b0b23c84ce6ca4685f89efbb83e94532ebdb125f80949092dbb`
- Lens registry content hash: `sha256:7c325d9367d873ede832f78a73ddffd2f9e5f5ca879a09a296bc19b2e950a7e8`
- Equivalence basis drift is forbidden under D18. Any change requires a new preregistration and a new held-out run.

## Independent Evidence Corpus

- `reports/campaign_011/w7_densification_report.json`: exploratory_densified W7 source-bound axis coverage; used in Campaign 010 deficit map: False
- `reports/campaign_012/real_lane1_extraction.json`: real ITIS Lane-1 taxonomic source basis for independent biological grounding; used in Campaign 010 deficit map: False
- `reports/campaign_009/floor_calibration_full.json`: cross-campaign trace candidates for independent held-out partitioning; used in Campaign 010 deficit map: partition_filter_required

## Analysis Path

1. Select an independent held-out evidence partition that excludes Campaign 010 deficit-map training rows.
2. Project evidence using the same substrate-blind equivalence basis from Campaign 009 BFG-PR.
3. Evaluate the same 8-lens registry used by Campaign 010, with honest declination preserved.
4. Run N7 lens-permutation null with N >= 1000 under the same statistic.
5. Declare replication only if `formal_gap > 0.30`, AttractorStrength remains above the declared threshold, and N7 empirical p < 0.05 under the unchanged basis.

## Stopping Rule

Run the declared partition once. Do not alter the equivalence basis, lens registry, or threshold after observing the result.
