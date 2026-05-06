# L3 Overlap: Insects x W7 Swarm Motifs

Campaign: 013
Mode: exploratory

## Data

- ITIS family-level Insecta claims ingested: 1000
- License class: cc0
- BiologicalClaim schema: BiologicalClaim.v1.1
- W7 templates tested: 12

## Normalization Verdict

Process-role normalizer fired on 1000 claims and produced 0 behavior-bearing mappings.
Interaction-channel normalizer fired on 1000 claims and produced 0 channel mappings.

That zero is the result: ITIS is a taxonomic source, not a behavioral trait source. The analysis does not infer eusociality, stigmergy, memory, repair, or coordination from family names.

## Verdicts

| Motif | Verdict | W7 hits | ITIS behavior taxa | Family-corrected p |
|---|---|---:|---:|---:|
| `motif.autocatalytic_closure.draft` | null | 0 | 0 | 1.000 |
| `motif.self_maintained_boundary.draft` | insufficient-data | 5 | 0 | 1.000 |
| `motif.repair.draft` | insufficient-data | 7 | 0 | 1.000 |
| `motif.replication_lineage.draft` | insufficient-data | 5 | 0 | 1.000 |
| `motif.externalized_memory.draft` | insufficient-data | 6 | 0 | 1.000 |
| `motif.floor_connectivity.draft` | insufficient-data | 12 | 0 | 1.000 |

## Controls

- Phylogenetic correction uses ITIS hierarchy as a v0 family/order baseline; this is taxonomic, not a dated phylogeny.
- Shuffled hierarchy nulls used N=1000 per motif across 853 checked families.
- Sampling-bias pass found 28 orders; sparse orders are listed in `reports/campaign_013/sampling_bias.json`.

## Claim Status

All L3 records remain `mode_tag: exploratory` because W7 is `exploratory_densified`, not `claim_ready_densified` under D21. This report is a first overlap measurement, not a claim-bearing biological result.
