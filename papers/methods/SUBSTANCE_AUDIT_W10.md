# Substance Audit W10 Hypergraph Reactions

Campaign: 008
Doctrine: D17.5
Measured simulation logic: 443 lines against a 400-line proxy floor

## v1.0 Section 3 components

- Hyperedges: reactions consume and produce arbitrary-order reactant/product sets rather than reducing the system to pairwise edges.
- Catalysis and modules: catalytic conditions and modular block activation are represented in the edge definitions and diagnostics.
- Backends: ODE and SSA stepping are both implemented for the same hypergraph reaction model.
- Structure diagnostics: reaction-dependency graphs, feedback components, stoichiometric deltas, flux entropy, and bottleneck proxies are measured from active hyperedges.
- Controls: catalyst removal and pairwise reduction degrade closure/high-order signal without altering the gate logic.
- Invariants: nonnegative species, extent limits, closure score, modularity score, and high-order diagnostics are trace-exported.

## Implementation pointers

- `worlds/hypergraph_reactions/model.py:HypergraphScenario` declares initial state, hyperedges, backend, catalyst-removal, and pairwise-reduction controls.
- `HypergraphReactionWorld.step` dispatches real ODE or SSA stepping over the active hyperedges.
- `_active_edges`, `_propensity`, `_ode_step`, `_ssa_step`, `_limiting_extent`, `_reaction_dependency_graph`, `_feedback_component_score`, `_structural_diagnostics`, `_closure_score`, and `_modularity_score` are the substantive mechanics.
- `_hypergraph_diagnostics`, `_benchmark_success`, and `export_trace` expose closure, modular blocks, ODE/SSA agreement, high-order signal, and invariants.

## Behavior gate evidence

- W10 positive benchmarks cover `high_order_closure`, `modular_blocks`, `ode_ssa_agreement`, and `hyperedge_order_effect`.
- Controls require catalyst removal to lower closure and pairwise reduction to lower high-order signal.
- Campaign 008 requires all positive W10 traces, controls, event types, and invariants to pass.

## Invariant evidence

- Trace exports include reaction events, catalysis events, hyperedge firing, module activation, extent-limited updates, and nonnegative state.
- The validation report requires every W10 positive trace invariant to pass.
- D14 lint reports zero benchmark-conditional state-writing violations for W10.

## Substance judgment

W10 now exceeds its proxy floor. It implements high-order reaction structure, catalytic closure, reaction-dependency feedback, ODE/SSA comparison, controls, and invariant checking.

Architect verdict: meets_spec_with_caveats
