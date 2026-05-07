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
| `motif.autocatalytic_closure.draft` | `sha256:c54b3c4d36ac4191b235db4d6958c2888aa78ac6fbe513a7f9e091d51923cb9e` | `graph` | 10000 | 0.600000 | 0.200000 | `signal_survives_shuffle` |
| `motif.repair.draft` | `sha256:d294462ebd7eb3a3e0badeba60669154eb0f612144ce039404e6d9be984ed727` | `graph` | 10000 | 0.500000 | 0.133333 | `signal_survives_shuffle` |
| `motif.externalized_memory.draft` | `sha256:b9437939983325d322dec3210e50b4098ac06c0c10412e5c114f34e9597b39c6` | `graph` | 10000 | 0.500000 | 0.166667 | `signal_survives_shuffle` |
| `motif.replication_lineage.draft` | `sha256:5ce35bc9b64c16a61977b14a4801f6db0b85cdd8e1a0a900c746294d4dd93a45` | `graph` | 10000 | 0.600000 | 0.200000 | `signal_survives_shuffle` |
| `motif.self_maintained_boundary.draft` | `sha256:9d30531db762cfef54982ef0d0456716bfe4500590399c0a46fd8628435af628` | `graph` | 10000 | 0.500000 | 0.166667 | `signal_survives_shuffle` |
| `motif.floor_connectivity.draft` | `sha256:ab9bfc44126df9267758f4f45f1098b32a319cf22a2854126d40aff792d63b2e` | `campaign009_bfg_calibrated_detector` | 10000 | 0.198880 | 0.072361 | `signal_survives_shuffle` |

## Aggregate

6 motifs survived, 0 died, and 0 were inconclusive/not evaluable under MotifContract.v2 plus D26 screens. The survivor count is high enough to require Architect/PI review before any promotion; the most likely remaining risk is detector-side generator-token or benchmark-correlation dependence, not predicate event-token leakage.

D26 is implemented here as an operational source-object-map screen. A surviving detector result remains exploratory until a Destroyer pass validates the detector itself against token and schema decoys.
