# Campaign 020: Substrate-Blocked Sweep on Five Remaining Motifs

Task: TASK-031
Status: exploratory; no claim-bearing promotion.

## Method

- Corpus floor: >= 8 locked-positive and >= 8 locked-negative traces per qualified substrate.
- Permutation: within-substrate label shuffle, N=10000, seed=20020.
- Statistic: mean preregistered primary-lens score on locked positives minus mean score on locked negatives.
- Verdict: signal survives only when observed gap is above the shuffled 95% CI upper bound.
- Preregistration: one signed file per motif in `papers/prereg/campaign_020/`, written before that motif's permutation.

## Results

| Motif | Requested alias | Primary lens | Qualified worlds | Observed gap | Shuffled mean | CI high | p | Verdict |
|---|---|---|---|---:|---:|---:|---:|---|
| `motif.autocatalytic_closure.draft` | `motif.autocatalytic_closure.draft` | `graph` | `crn` | 0.600000 | 0.000720 | 0.300000 | 0.000200 | `signal_survives_shuffle` |
| `motif.externalized_memory.draft` | `motif.externalized_memory.draft` | `graph` | `cognitive` | 0.500000 | 0.000600 | 0.250000 | 0.000200 | `signal_survives_shuffle` |
| `motif.repair.draft` | `motif.repair.draft` | `graph` | `protocell`, `swarm` | 0.500000 | 0.001187 | 0.187500 | 0.000100 | `signal_survives_shuffle` |
| `motif.replication_lineage.draft` | `motif.replication_lineage.draft` | `graph` | `digital`, `morphogenesis`, `protocell`, `quasispecies` | 0.600000 | -0.000401 | 0.150000 | 0.000100 | `signal_survives_shuffle` |
| `motif.self_maintained_boundary.draft` | `motif.self_boundary.draft` | `graph` | `protocell` | 0.500000 | 0.000600 | 0.250000 | 0.000200 | `signal_survives_shuffle` |

## Aggregate Interpretation

5 of 5 motifs survived the substrate-blocked shuffle. Per the task's expected-outcome rule, 3+ survivors is suspect and should trigger Architect review before any adversarial or promotion campaign. The likely review target is shared event-token dependence between locked labels and graph-lens features.

The sweep is deliberately not a promotion step. The high survivor count is useful, but also a warning: the primary lens for every target motif is the Campaign 010 graph lens, and the locked labels are event-predicate labels. That makes substrate blocking necessary but not sufficient; adversarial controls must test whether each motif survives degenerate event-token decoys and synonym/renaming controls before any L5 movement.

## Parked Worlds

Domain worlds listed by Campaign 010 high-coverage lenses but lacking a Campaign 020 deterministic positive/negative generator were not silently treated as evidence. They are listed in the JSON qualification blocks as `domain_worlds_without_campaign020_generator` and remain future corpus-expansion work.
