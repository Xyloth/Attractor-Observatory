# D31 - BFG Measurement Split

**Status:** ratified during TASK-FLOOR-BFG / Campaign 026.  
**Mode:** foundational.  
**Failure mode caught:** Basin-Floor Geometry self-match, where a floor-connectivity predicate and a basin-geometry lens both read perturbation-outcome equivalence fibers and then substrate-blocked control validates circular evidence.

## Binding Text

> floor_connectivity-class predicates require a signed predicate-side outcome artifact, a field-disjoint lens-side trajectory artifact, grouped-stratified validation holdout, and enforced read separation. Heldout validation prevents tuning leakage; it does not by itself upgrade same-row field splits to CLEAN.

Campaign 026 operationalizes the rule as a stricter measurement split:

- predicate rows read `perturbation_event.outcome_summary` only;
- lens rows read `perturbation_event.trajectory_geometry` only, except explicitly risky covariates named in the contract;
- predicate rows, lens rows, validation predicate rows, and validation lens rows carry disjoint `perturbation_id` values;
- the preprocessing classifier emits signed outcome summaries before lens evaluation;
- floor lens modules cannot import the classifier and cannot read or name `outcome_summary`;
- predicate modules cannot read or name `trajectory_geometry`;
- predicate outputs and lens outputs join only in `formalism.floor_bfg.floor_join`.

## Operational Consequence

A same-row field split is never sufficient for final BFG evidence. Final substrate-blocked controls operate on unit-level predicate verdicts derived from predicate rows and independently derived unit-level lens vectors from lens rows. Validation holdout uses the same split.

CRNT can honestly domain-decline when no reaction-network object exists at the BFG basin-geometry layer. Petri is not permanently declined: a recovery-transition-net variant can be evidence only if it reads trajectory transitions rather than fiber labels.

## Enforcement

Campaign 026 adds an AST-level read-separation audit. Failure of any of these checks is a D31 methodology failure:

- any floor lens imports the BFG classifier;
- any floor lens reads or names `outcome_summary`;
- any floor predicate reads or names `trajectory_geometry`;
- any final run joins predicate and lens outputs outside the approved join module;
- any validation row is used by both predicate and lens.

## Claim Boundary

D31 does not make floor-connectivity claim-bearing. C026 output remains `mode_tag: exploratory`; promotion requires a later Destroyer pass and the usual D21/D26/D27 gates.
