# Campaign 018 - W1 CRN Bridge-Trace Generation

Campaign 018 tests the Campaign 017 CRN bridge prediction by generating real W1 CRN traces from every Campaign 016 low-level empirical record.

## Inputs And Discipline

- Source records: `reports/campaign_016/factory_store/empirical_records.json`.
- All 16 records project; no record-class cherry-picking or opt-out is allowed.
- Projection logic is deterministic and derived from record payload fields.
- Detector outputs remain `mode_tag: exploratory`; no claim-bearing promotion occurs.

## Projection Classes

- Atomic spectra: source energy-level counts become configuration-index species; adjacent energy gaps set reciprocal-scaled rates; the observed ionization edge closes the boundary back to ground.
- Small molecules: heavy-atom count sets species count; source topology proxy and complexity set connectivity/rates.
- Dynamical primitives: fixed points use depleting reactions, limit cycles and torus flows use phase-cycle CRNs, and strange-attractor families use chemical-oscillator surrogates.

## Detector Fire Rates

| detector | bridge fire rate | native W1 fire rate | verdict |
|---|---:|---:|---|
| closure | 9/16 (0.5625) | 3/4 (0.75) | bridge-meaningful |
| boundary | 0/16 (0.0) | 0/4 (0.0) | bridge-empty |
| repair | 0/16 (0.0) | 0/4 (0.0) | bridge-empty |
| externalized_memory | 0/16 (0.0) | 0/4 (0.0) | bridge-empty |
| replication_lineage | 0/16 (0.0) | 0/4 (0.0) | bridge-empty |
| self_boundary | 0/16 (0.0) | 0/4 (0.0) | bridge-empty |

## Honest Read

The math-shadow framing is partially supported: the CRN bridge carries interpretable closure signal, but it does not carry the non-closure motifs. The Campaign 017 projection nondeclines were not pure noise for closure, yet most of the broad lens compatibility remains a coverage artifact for this CRN-only bridge.

## Parked

- No bridge fire is claim-bearing.
- Boundary, repair, memory, and lineage motifs need native event surfaces before CRN bridges can fairly test them.
- If closure is promoted later, it needs adversarial controls against projection-induced RAF construction.
