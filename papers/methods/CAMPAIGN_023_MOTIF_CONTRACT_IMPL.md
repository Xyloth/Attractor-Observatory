# Campaign 023: MotifContract.v2 Implementation Rerun

Task: TASK-MOTIF-IMPL
Status: exploratory; no claim-bearing promotion.

## Method

- Predicates are semantic MotifContract.v2 predicates and do not read event-token names.
- Adversarial controls: event_token_rename, state_key_rename, payload_key_rename, generator_id_erasure.
- Substrate-blocked control: within-world-family shuffle, N=10000, seed=23023.
- Verdict direction: signal survives only when observed gap is above the shuffled 95% CI upper bound.
- C020 floor label-function keys are deprecated for floor connectivity.

## Results

| Motif | Contract hash | Primary detector | N | Observed gap | CI high | Verdict |
|---|---|---|---:|---:|---:|---|
| `motif.autocatalytic_closure.draft` | `sha256:c07b6715e97247247c9348830170958bc8f157821e7426a23eeb568392d0641e` | `graph` | 10000 | 0.600000 | 0.200000 | `signal_survives_shuffle` |
| `motif.repair.draft` | `sha256:e436836f95cfb5ec09d9b0bc3492a63c6e4c68ed567e99d2b60802bd8306cd8b` | `graph` | 10000 | 0.500000 | 0.133333 | `signal_survives_shuffle` |
| `motif.externalized_memory.draft` | `sha256:de8c058fca42cdfd06c8ebd4162a163de51ca84e3565d01b6da3c1e57359edb4` | `graph` | 10000 | 0.500000 | 0.166667 | `signal_survives_shuffle` |
| `motif.replication_lineage.draft` | `sha256:155cf6a4aac0254687b5fb5d2492ba469e7833416508068e16b84041e904e495` | `graph` | 10000 | 0.600000 | 0.200000 | `signal_survives_shuffle` |
| `motif.self_maintained_boundary.draft` | `sha256:c36f0b5d3fb431801ad9b1cf66891117b3680d739a79f6bad2e64911722d62fc` | `graph` | 10000 | 0.500000 | 0.166667 | `signal_survives_shuffle` |
| `motif.floor_connectivity.draft` | `sha256:09f36d87830ce82b6b193f5f87cc08cb9ddc7dc28fa59607f28d09cf0ed50109` | `campaign009_bfg_calibrated_detector` | 10000 | 0.198880 | 0.072361 | `signal_survives_shuffle` |

## Aggregate

6 motifs survived, 0 died, and 0 were inconclusive/not evaluable under MotifContract.v2 plus D26 screens. The survivor count is high enough to require Architect/PI review before any promotion; the most likely remaining risk is detector-side generator-token or benchmark-correlation dependence, not predicate event-token leakage.

D26 is implemented here as an operational source-object-map screen. A surviving detector result remains exploratory until a Destroyer pass validates the detector itself against token and schema decoys.
