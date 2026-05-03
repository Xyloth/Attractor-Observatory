# CODEX Campaign 004: Discovery, Calibration, and Negative-Space Engine

## Doctrine

This campaign treats v1.2 as the floor. It does not end at a coherent
narrative. It ends when every gate below is evaluated with generated artifacts
and either green or escalated as a named blocker.

No partial/foundation-slice exit is available for TASK-011.

## Scientific Questions

1. Can the named but incomplete K5-K10 calibration corpora become executable
   guardrails instead of roadmap placeholders?
2. Can the Observatory discover motif candidates from substrate-blind evidence
   projections without accidentally promoting them to registered motifs?
3. Can negative-space become structured research output, with search effort and
   explanations, rather than a Markdown note?
4. Can biology shadow anchors pressure the trace/motif/lens schema in a way
   that produces explicit failures and contract proposals?
5. Can world-usefulness and Pareto context scoring guide what to build next
   without collapsing the vector evidence into a misleading scalar?

## Pillar 1: K5-K10 Calibration Completion

G1. K5 ambiguous corpus has at least 24 scenarios and >=80% of detector
confidences fall in [0.4, 0.6].

G2. K6 out-of-distribution corpus has at least 16 scenarios and >=90% abstain
or flag rate.

G3. K7 multi-scale corpus has at least 12 scenarios and cross-scale composition
pass rate >=0.85.

G4. K8 same-process/different-appearance corpus has at least 12 pairs and
substrate-blind similarity >=0.75 for >=85% of pairs.

G5. K10 non-stationary corpus has at least 12 traces and temporal phase
accuracy >=0.85.

G6. K1-K10 registry completeness report is generated and every corpus has
schema-validated scenarios.

## Pillar 2: Emergent Candidate Pipeline

G7. Substrate-blind projection produces feature vectors for W1/W2/W3/W5 and
contains no world-family identity fields.

G8. Candidate discovery emits at least 4 MotifCandidate records with required
v1.2 fields.

G9. At least 3 candidates have held-out recurrence >=0.60 across regenerated
seeds.

G10. At least 3 candidates have compression_gain > 0.05 against a store-all
baseline.

G11. Novelty and nearest-registered-motif scores are computed for every
candidate; no candidate is a duplicate of closure/boundary/memory.

G12. Promotion pathway is enforced: raw candidates can become audited
candidates, but none become registered motifs without Architect/PI signature.

G13. Red-team decoys are run against the candidate pipeline and false promotion
rate is 0.

G14. Motif candidate journal and machine-readable candidate JSONL are written.

## Pillar 3: Negative Space, Biology Shadow, and Guidance

G15. Structured negative-space index contains all five v1.2 categories and at
least 8 entries with search effort, biology coverage, explanations, and status.

G16. Negative-space adversarial search attempts are recorded; at least one entry
is found/resolved and at least one remains confirmed_absent or inconclusive.

G17. World usefulness vectors are computed for W1/W2/W3/W5 with the five v1.2
components: motif_yield, calibration_value, cross_family_value,
biological_relevance, formal_lens_stress.

G18. Pareto fronts are computed in at least four claim contexts, with no scalar
projection used for decisions.

G19. Biology shadow anchor set produces operational predicates, representability
scores, formal-lens support, and contract-change proposals for failures.

G20. Method-health dashboard includes Campaign 004 gates, K5-K10 status,
candidate promotion hygiene, negative-space coverage, and builder calibration.

G21. Campaign 002 and Campaign 003 still regenerate green after Campaign 004.

G22. Full pytest suite passes.

## Builder Expansion Authority

The builder should improve any gate that can pass by a weak substitution. In
particular:

- use computed feature projections rather than constants;
- make candidate records useful for later promotion review;
- prefer explicit failure artifacts over hidden TODOs;
- add tests that would catch regression to placeholder reports;
- add CLI or one-command report generation where useful.

## Done

`reports/campaign_004/full_report.json` exists and reports all gates green,
`python make_campaign_004.py` regenerates it, full pytest passes, and TASK-011
is updated in the builder ledger. If any gate cannot be completed, a
`BLOCKER-G##.md` file must exist with blocker, owner, and requested review.
