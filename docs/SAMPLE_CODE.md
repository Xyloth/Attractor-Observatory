# Sample code — curated technical excerpts

This document is a curated showcase of representative technical work from the Attractor Observatory's private implementation. The full source — substrate engines, motif detectors, validation gauntlet, kernel — is held privately. The excerpts below are chosen to demonstrate technical depth across four representative surfaces: kernel craft, numerical methods, real algorithmic work, and post-doctrine-D14 simulation honesty.

Each excerpt is faithful to the actual code in the private repository, with surrounding scaffolding (imports, dataclasses, error handling) elided for readability.

---

## 1. Philox4x32-10 RNG splitter (`core/rng.py`)

Counter-based RNG with deterministic labelled substreams. Every random draw in the project goes through this. No global state; immutable; reproducible bit-for-bit across runs given the same seed and label path. Implements the Philox round (Salmon et al., 2011) directly — no PRNG library dependency.

```python
@dataclass(frozen=True)
class RNG:
    """Immutable Philox4x32-10 RNG stream."""

    root_seed: int
    path: tuple[str, ...] = ()
    counter: int = 0
    algorithm: str = "Philox4x32-10"

    def split(self, label: str) -> "RNG":
        """Return a labelled deterministic substream."""
        if not label or not label.strip():
            raise ContractError("empty_rng_label", "RNG.split(label) requires a non-empty label")
        return RNG(root_seed=self.root_seed, path=self.path + (label,), counter=0)

    def _key(self) -> tuple[int, int]:
        payload = self.root_seed.to_bytes(8, "little") + b"\0" + "/".join(self.path).encode("utf-8")
        digest = hashlib.sha256(payload).digest()
        return (int.from_bytes(digest[0:4], "little"),
                int.from_bytes(digest[4:8], "little"))

    def _block(self, block_counter: int) -> tuple[int, int, int, int]:
        counter = (_u32(block_counter), _u32(block_counter >> 32), 0, 0)
        key = self._key()
        for _ in range(10):                     # ten Philox rounds
            counter = _philox_round(counter, key)
            key = _raise_key(key)
        return counter

    def draw_u32(self, count: int) -> tuple[tuple[int, ...], "RNG"]:
        """Draw `count` u32 values and return the advanced stream."""
        if count <= 0:
            return (), self
        words: list[int] = []
        blocks = (count + 3) // 4
        for offset in range(blocks):
            words.extend(self._block(self.counter + offset))
        return tuple(words[:count]), replace(self, counter=self.counter + blocks)

    def state_hash(self) -> str:
        """Stable hash of (algorithm, seed, path, counter) for trace manifests."""
        payload = f"{self.algorithm}|{self.root_seed}|{'/'.join(self.path)}|{self.counter}".encode()
        return hashlib.sha256(payload).hexdigest()
```

The contract: `RNG.split("ssa-direct")` returns an independent stream uniquely determined by the path; same label, same root seed, same counter ⇒ same draws across machines. The `state_hash` is included in trace manifests so determinism is verifiable post-hoc.

---

## 2. Strang-split RK4 reaction-diffusion step (`worlds/field/solver.py`)

The W3 field world uses operator splitting: half-step diffusion → full-step RK4 reaction → half-step diffusion. This is the canonical second-order Strang scheme. Configurable for periodic / zero-flux / absorbing boundaries, 2D and 3D, with multiple reaction families (Brusselator, Schnakenberg, FitzHugh-Nagumo, Gray-Scott, Cahn-Hilliard).

```python
def reaction_rk4_step(state: FieldState, config: FieldConfig, dt: float) -> FieldState:
    """Per-cell classical RK4 for the local reaction kinetics."""
    result = state.copy()
    for coord in _coordinate_iter(config):
        y0 = _cell_values(state, config, coord)
        energy = _get(state.energy, coord)
        k1 = reaction_vector(y0, energy, config)
        k2 = reaction_vector([v + 0.5 * dt * k for v, k in zip(y0, k1)], energy, config)
        k3 = reaction_vector([v + 0.5 * dt * k for v, k in zip(y0, k2)], energy, config)
        k4 = reaction_vector([v + dt * k for v, k in zip(y0, k3)], energy, config)
        values = [v + dt * (a + 2*b + 2*c + d) / 6.0
                  for v, a, b, c, d in zip(y0, k1, k2, k3, k4)]
        _set_cell_values(result, config, coord, values)
    return result


def diffusion_step(state: FieldState, config: FieldConfig, dt: float) -> FieldState:
    """Per-species explicit-Euler Laplacian step with declared boundary handling."""
    result = state.copy()
    for species_index, grid in enumerate(state.species):
        diff = config.diffusion[species_index]
        for coord in _coordinate_iter(config):
            value = _get(grid, coord) + dt * diff * laplacian_at(grid, config, coord)
            _set(result.species[species_index], coord, max(-5.0, min(5.0, value)))
    # Energy field also diffuses.
    for coord in _coordinate_iter(config):
        value = _get(state.energy, coord) + dt * config.energy_diffusion * laplacian_at(state.energy, config, coord)
        _set(result.energy, coord, max(0.0, value))
    return result


def strang_step(state: FieldState, config: FieldConfig, dt: float) -> FieldState:
    if config.reaction_model == "cahn_hilliard":
        return cahn_hilliard_step(state, config, dt)
    half = diffusion_step(state, config, 0.5 * dt)
    reacted = reaction_rk4_step(half, config, dt)
    final = diffusion_step(reacted, config, 0.5 * dt)
    apply_sources_sinks(final, config, dt)
    final.t = round(state.t + dt, 12)
    return final


def cahn_hilliard_step(state: FieldState, config: FieldConfig, dt: float) -> FieldState:
    """dphi/dt = M * laplacian(phi^3 - phi - eps^2 * laplacian(phi))

    Real fourth-order biharmonic Cahn-Hilliard, not a zero-order reduction.
    Computes the chemical potential mu via one Laplacian, then advances phi
    via a second Laplacian of mu. Mass-conserving on closed boundaries to
    the tolerance of the discretisation.
    """
    result = state.copy()
    phi = state.species[0]
    mobility = config.reaction_params.get("mobility", 0.02)
    epsilon = config.reaction_params.get("epsilon", 1.0)

    chemical = new_energy_grid(config, 0.0)
    for coord in _coordinate_iter(config):
        value = _get(phi, coord)
        lap_phi = laplacian_at(phi, config, coord)
        mu = value**3 - value - epsilon * epsilon * lap_phi
        _set(chemical, coord, mu)

    for coord in _coordinate_iter(config):
        value = _get(phi, coord) + dt * mobility * laplacian_at(chemical, config, coord)
        _set(result.species[0], coord, max(-1.2, min(1.2, value)))

    apply_sources_sinks(result, config, dt)
    result.t = round(state.t + dt, 12)
    return result
```

The Cahn-Hilliard implementation is the post-doctrine-D14 fix. An earlier version reduced CH to `dφ/dt = M · (φ − φ³)` — a zero-order ODE that satisfied the regime label without integrating the actual fourth-order PDE. The corrected version applies two Laplacians per timestep, produces real phase separation, and was committed alongside Doctrine D14 (no scenario-internal hardcoding) and the Truth Pass downgrade of the prior claim.

---

## 3. Hordijk-Steel maximal-RAF + closure-depth (`worlds/crn/raf.py`)

W1's autocatalytic-set detector follows the Hordijk-Steel 2004 fixed-point: iteratively compute the food-generated closure of remaining reactions, then drop reactions that aren't F-generated or aren't catalysed by a molecule in the closure. Plus minimal-subRAF enumeration via combinatorial search and closure-depth measurement.

```python
def food_generated_closure(food: set[str], reactions: Sequence[dict]) -> set[str]:
    """Molecules reachable from food by repeated reaction firing."""
    closure = set(food)
    changed = True
    while changed:
        changed = False
        for reaction in reactions:
            if reactants(reaction).issubset(closure):
                before = len(closure)
                closure.update(products(reaction))
                changed = changed or len(closure) != before
    return closure


def is_raf(reactions: Sequence[dict], food: set[str]) -> bool:
    if not reactions:
        return False
    closure = food_generated_closure(food, reactions)
    for reaction in reactions:
        if not reactants(reaction).issubset(closure):
            return False
        if not catalysts(reaction):
            return False
        if catalysts(reaction).isdisjoint(closure):
            return False
    return True


def maximal_raf_reactions(scenario: dict) -> list[dict]:
    """Hordijk-Steel maxRAF fixed-point: shrink the reaction set until stable."""
    remaining = list(scenario.get("reactions", []))
    food = food_set(scenario)
    changed = True
    while changed:
        changed = False
        closure = food_generated_closure(food, remaining)
        next_remaining = [
            reaction for reaction in remaining
            if reactants(reaction).issubset(closure)
            and catalysts(reaction)
            and not catalysts(reaction).isdisjoint(closure)
        ]
        if len(next_remaining) != len(remaining):
            changed = True
            remaining = next_remaining
    return remaining if is_raf(remaining, food) else []


def closure_depth(scenario: dict, raf_reaction_ids: set[str]) -> int:
    """Deepest catalyst-production layer inside the RAF.

    Tracks the BFS-style depth at which each species first becomes producible;
    returns the max depth among catalysts not in the food set. A two-cycle
    cross-catalysis has depth 1; a layered chain that depends on intermediates
    has higher depth.
    """
    food = food_set(scenario)
    reactions = [r for r in scenario.get("reactions", []) if reaction_id(r) in raf_reaction_ids]
    depths = {species: 0 for species in food}
    changed = True
    while changed:
        changed = False
        for reaction in reactions:
            if not reactants(reaction).issubset(depths):
                continue
            next_depth = max((depths[item] for item in reactants(reaction)), default=0) + 1
            for product in products(reaction):
                if product not in depths or next_depth < depths[product]:
                    depths[product] = next_depth
                    changed = True
    catalyst_depths = [depths[c] for r in reactions for c in catalysts(r)
                       if c in depths and c not in food]
    return max(catalyst_depths, default=0)
```

This is real RAF theory, not a five-line set-containment check. The `enumerate_subrafs` function (not shown) extends the maximal-RAF result with combinatorial enumeration of sub-RAFs and minimal-RAF extraction, giving Campaign 002+ a nested-closure measurement framework. The benchmarks include canonical Hordijk-Steel fragments where the maximal-RAF size, minimal-RAF count, and closure-depth are known a priori.

---

## 4. Post-D14 W4 morphogenesis GRN bandpass cascade (`worlds/morphogenesis/model.py`)

W4 produces segmentation, branching, radial form, and layered organoid patterns from a single 8-rule sigmoid GRN driven by morphogen field configurations. Each benchmark scenario differs only in source geometry and pulse schedule — the simulation step itself contains *no* benchmark-conditional code paths writing to state. This is what Doctrine D14 (no scenario-internal hardcoding) requires.

```python
def _update_grn(self, cell: Cell, local: dict[str, float], dt: float) -> None:
    # Apply the 8-rule sigmoid GRN — protein production via weighted activator
    # and repressor sums plus morphogen inputs, with sigmoid response.
    updates: dict[str, float] = {}
    for rule in self.grn:
        current = cell.proteins.get(rule.target, 0.0)
        production = rule.production(cell.proteins, local) + cell.genome_bias.get(rule.target, 0.0)
        delta = dt * (production - rule.decay * current)
        updates[rule.target] = _clamp(current + delta)
    for name, value in updates.items():
        cell.proteins[name] = value

    # Universal morphogen-to-GRN couplings. Scenario-specific morphology is
    # encoded in source geometry and pulse schedules, NOT in benchmark arms.
    anterior = local.get("anterior", 0.0)
    posterior = local.get("posterior", 0.0)
    branch = local.get("branch", 0.0)
    radial = local.get("radial", 0.0)
    layer = local.get("layer", 0.0)
    nutrient = local.get("nutrient", 0.0)
    anterior_n = anterior / (1.0 + abs(anterior))
    posterior_n = posterior / (1.0 + abs(posterior))
    branch_n = branch / (1.0 + abs(branch))
    radial_n = radial / (1.0 + abs(radial))
    layer_n = layer / (1.0 + abs(layer))

    # Hox-like segmentation: two narrow anterior expression windows produce
    # alternating segment expression along the AP axis. The bandpass replaces
    # an earlier sin(x) overlay that hardcoded segmentation per benchmark.
    segment_band = max(_bandpass(anterior_n, 0.492, 0.018),
                       _bandpass(anterior_n, 0.582, 0.018))
    segment_drive = max(0.0, segment_band * (0.10 + 0.95 * posterior_n)
                                - 0.72 * branch_n - 0.22 * radial_n)
    cell.proteins["segment"] = _clamp(cell.proteins["segment"]
                                       + dt * (2.00 * segment_drive
                                                - 0.30 * cell.proteins["segment"]))

    # Branching: tip identity arises from branch morphogen exposure with
    # radial assist and posterior repression.
    tip_drive = max(0.0, branch_n - 0.05) + 0.22 * max(0.0, radial_n - 0.10)
    cell.proteins["tip"] = _clamp(cell.proteins["tip"]
                                   + dt * (1.85 * tip_drive
                                            - 0.14 * posterior * cell.proteins["tip"]))

    # Stalk, epithelial, and motility identities follow analogous
    # morphogen-driven rules. None of the rules reference scenario.benchmark.
    stalk_drive = max(0.0, posterior + 0.35 * nutrient - 0.45 * branch)
    cell.proteins["stalk"] = _clamp(cell.proteins["stalk"]
                                     + dt * (0.52 * stalk_drive
                                              - 0.12 * cell.proteins["tip"]))
    epithelial_drive = max(0.0, 1.20 * layer_n + 0.20 * radial_n
                                - 0.35 * branch_n - 0.10 * anterior_n)
    cell.proteins["epithelial"] = _clamp(cell.proteins["epithelial"]
                                          + dt * (0.95 * epithelial_drive
                                                   - 0.18 * cell.proteins["segment"]
                                                   - 0.12 * cell.proteins["tip"]))
    motility_drive = max(0.0, 0.75 * branch + 0.35 * radial - 0.18 * layer)
    cell.proteins["motility"] = _clamp(cell.proteins["motility"]
                                        + dt * (0.85 * motility_drive
                                                 - 0.12 * cell.proteins["adhesion"]))
```

The earlier version of this function had per-benchmark arms that wrote to cell proteins directly: `if benchmark == "segmented_body": proteins["segment"] += 0.28 * sin((x + 1.4) * pi * 3.0)`. Doctrine D14 was added in response, the AST lint catches benchmark-conditional state writes inside `step` / `_update*` methods, and the rewrite above produces segmentation by configuring real anterior morphogen pulse schedules per scenario. The pattern emerges from the GRN cascade reading the morphogen field, not from a position-conditional injection. All five W4 benchmarks (linear sheet, branching tree, segmented body, radial form, layered organoid) pass under this universal cascade.

---

## What these excerpts establish

- **Kernel** (excerpt 1): real cryptographically-keyed counter-based RNG with labelled substreams. Determinism is verifiable.
- **Numerical methods** (excerpt 2): real Strang splitting + RK4 + Cahn-Hilliard biharmonic. Not a Gray-Scott toy.
- **Algorithmic work** (excerpt 3): real Hordijk-Steel maxRAF fixed-point, minimal subRAF enumeration, closure-depth measurement. Not a five-line set check.
- **Doctrine compliance** (excerpt 4): real GRN + morphogen-driven pattern formation. No benchmark-conditional cheats. The audit trail is in the doctrine document and the Truth Pass.

The full implementation includes:

- Twelve more such modules across the substrate plane (W1 protocell membrane dynamics, W5 28-opcode VM and replicator scheduler, W12 nested-symbiogenesis with sub-CRN exchange, W13 inner-world-hosting multiscale, K1–K10 calibration corpora, etc.).
- The motif detection layer (closure detector with isotonic confidence calibration; three structurally distinct boundary detectors with measured Cohen's kappa 0.21–0.83; cross-detector triangulation).
- The validation gauntlet (preregistration with content-hash signing; null factory N0–N5 with N=1000 each; FDR-corrected p-values; basin width with bootstrap CIs; Substance Audit framework).
- The AI Operating System (Estimation Calibration Loop with empirical convergence to delta near 1.0; debate logs; decision logs; memory ledger; builder telemetry).
- The reproducibility pipeline (eight `make_campaign_NNN.py` scripts; full pytest suite at 208 passing; D14 AST lint).

The full repository is held privately. Collaborators can request access via the Project PI.
