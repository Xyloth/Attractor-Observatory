# Campaign 026: Floor BFG Under D31

Task: TASK-FLOOR-BFG
Status: exploratory; no claim-bearing promotion.

## D31 Split

- Predicate rows read signed `outcome_summary` only.
- Lens rows read `trajectory_geometry` only, except the explicitly risky information variant's perturbation magnitude covariate.
- Predicate rows, lens rows, validation predicate rows, and validation lens rows are disjoint perturbation rows.
- Unit-level substrate-blocked shuffle: N=10000, within world family.

## Results

| Lens | Recovery class | Main verdict | Validation verdict | Adversarial | Ablation |
|---|---|---|---|---:|---:|
| `graph` | `NEW-ABST` | `signal_was_substrate_id` | `signal_was_substrate_id` | True | True |
| `crnt` | `DOMAIN-DECLINE` | `not_evaluable` | `not_evaluable` | True | True |
| `dynamical_systems` | `NEW-ABST` | `signal_survives_shuffle` | `signal_survives_shuffle` | True | True |
| `topology` | `NEW-ABST` | `signal_was_substrate_id` | `signal_was_substrate_id` | True | True |
| `petri` | `NEW-ABST` | `signal_survives_shuffle` | `signal_survives_shuffle` | True | True |
| `statistical_mechanics` | `PARTIAL-RISKY` | `signal_survives_shuffle` | `signal_survives_shuffle` | True | True |
| `control_theory` | `NEW-ABST` | `signal_survives_shuffle` | `signal_survives_shuffle` | True | True |
| `information` | `PARTIAL-RISKY` | `signal_survives_shuffle` | `signal_survives_shuffle` | True | True |

## Hashes

- Preregistration: `sha256:f0ceb553584dc974aed66024dcd6d9dacd1f2f5a8736cc94c8accaafc8a80ed4`
- Post-run: `sha256:b746ea0efe781d82a136631857bd18b2bd610cef5191a4b19cf9079886c37eab`

D31 keeps the same-system limitation visible: row-level predicate/lens evidence is disjoint, but final interpretation remains exploratory until external Destroyer review.
