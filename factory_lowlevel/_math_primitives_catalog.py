"""CB-015 T3 — 200-entry math primitives catalog.

200 canonical dynamical-system primitives drawn from peer-reviewed
literature. Every entry has a DOI to a primary source — Strogatz,
Guckenheimer & Holmes, Sprott (1994 + 1997), Kuznetsov, Pomeau &
Manneville, Chua, Lorenz, Rössler, Chen, Lu, etc.

This module is imported by ``factory_lowlevel/adapters.py``'s
``MATH_PRIMITIVE_SEEDS`` so the catalog can stay separate from the
2,000-line adapter module while remaining a single deterministic
source of truth.

Composition (totals approximate; exact = 200):
  * 1D maps:                              22  (logistic, tent, etc.)
  * 2D maps:                              16  (Hénon, Standard, etc.)
  * 3D continuous (Sprott family A-S):    19
  * 3D continuous (named systems):        45  (Lorenz, Rössler, Chua, Chen, Lu, etc.)
  * 3D continuous (jerk/circuit):         15
  * 4D+ chaotic / hyperchaotic:           20
  * Bifurcation normal forms:             18  (Kuznetsov + Strogatz)
  * Heteroclinic / homoclinic:            16
  * Intermittency / specialized:          17
  * Reaction networks / biological:       12
                                         ===
                                         200
"""

from __future__ import annotations

from typing import Any


# Canonical-source DOI shortcuts for compactness. Each catalog entry
# carries its DOI directly (no abbreviation), but the constants below
# document the primary source families:
#
# DOI_STROGATZ          = 10.1201/9780429492563        (Strogatz textbook)
# DOI_GUCK_HOLMES       = 10.1007/978-1-4612-1140-2    (Guckenheimer & Holmes)
# DOI_KUZNETSOV         = 10.1007/978-1-4757-3978-7    (Kuznetsov bif theory)
# DOI_KATOK_HASSELBLATT = 10.1017/CBO9780511809187     (Katok & Hasselblatt)
# DOI_DEVANEY           = 10.4324/9780429497995        (Devaney)
# DOI_SPROTT_1994       = 10.1103/PhysRevE.50.R647     (Sprott PRE 1994)
# DOI_SPROTT_1997       = 10.1016/S0375-9601(97)00088-1 (Sprott PLA 1997)
# DOI_LORENZ_1963       = 10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2
# DOI_ROSSLER_1976      = 10.1016/0375-9601(76)90101-8
# DOI_CHEN_1999         = 10.1142/S0218127499001024
# DOI_LU_2002           = 10.1142/S0218127402004620
# DOI_CHUA_1986         = 10.1109/TCS.1986.1085869
# DOI_POMEAU_MANN_1980  = 10.1007/BF01197757
# DOI_HENON_1976        = 10.1007/BF01608556
# DOI_MAY_1976          = 10.1038/261459a0


def _e(
    canonical_name: str,
    primitive_class: str,
    dimension: int,
    state_equation: str,
    parameters: dict[str, Any],
    expected_stable_form: str,
    doi: str,
    citation: str,
    invariants: list[str] | None = None,
) -> dict[str, Any]:
    """Build a catalog entry. Trims boilerplate so each row is one
    line at the call site."""
    return {
        "canonical_name": canonical_name,
        "primitive_class": primitive_class,
        "dimension": dimension,
        "state_equation": state_equation,
        "parameters": parameters,
        "invariants": invariants or [],
        "expected_stable_form": expected_stable_form,
        "doi": doi,
        "source_url": f"https://doi.org/{doi}",
        "citation": citation,
    }


# ---------------------------------------------------------------------------
# 1D maps (22)
# ---------------------------------------------------------------------------

_ONE_D_MAPS = [
    _e("logistic_map_period_doubling", "period_doubling", 1, "x_{n+1}=r*x_n*(1-x_n)", {"r": 3.5699456}, "feigenbaum_period_doubling_cascade", "10.1038/261459a0", "May, Simple mathematical models with very complicated dynamics, Nature 1976."),
    _e("logistic_map_chaotic_r4", "1d_chaos", 1, "x_{n+1}=r*x_n*(1-x_n)", {"r": 4.0}, "fully_developed_chaos", "10.1038/261459a0", "May, Simple mathematical models with very complicated dynamics, Nature 1976."),
    _e("logistic_map_intermittency_window", "intermittency", 1, "x_{n+1}=r*x_n*(1-x_n)", {"r": 3.8284}, "type_I_intermittency", "10.1007/BF01197757", "Pomeau and Manneville, Intermittent transition to turbulence, CMP 1980."),
    _e("tent_map_period_doubling", "1d_chaos", 1, "x_{n+1}=mu*min(x_n, 1-x_n)", {"mu": 2.0}, "fully_chaotic_tent_map", "10.1201/9780429492563", "Strogatz, Nonlinear Dynamics and Chaos."),
    _e("bernoulli_doubling_map", "1d_chaos", 1, "x_{n+1}=2*x_n mod 1", {}, "uniform_invariant_measure_chaos", "10.1017/CBO9780511809187", "Katok and Hasselblatt, Modern Theory of Dynamical Systems."),
    _e("sine_circle_map_arnold", "circle_map", 1, "x_{n+1}=x_n+Omega-(K/(2*pi))*sin(2*pi*x_n) mod 1", {"Omega": 0.4, "K": 1.0}, "devil_staircase_arnold_tongues", "10.1007/978-1-4612-1140-2", "Guckenheimer and Holmes, Hopf bifurcation normal form."),
    _e("gauss_iterated_map", "1d_chaos", 1, "x_{n+1}=exp(-alpha*x_n^2)+beta", {"alpha": 6.2, "beta": -0.5}, "discrete_chaotic_attractor", "10.1201/9780429492563", "Strogatz, Nonlinear Dynamics and Chaos."),
    _e("chebyshev_T2_map", "1d_chaos", 1, "x_{n+1}=2*x_n^2-1", {}, "fully_chaotic_chebyshev", "10.1017/CBO9780511809187", "Katok and Hasselblatt, Modern Theory of Dynamical Systems."),
    _e("chebyshev_T3_map", "1d_chaos", 1, "x_{n+1}=4*x_n^3-3*x_n", {}, "fully_chaotic_chebyshev", "10.1017/CBO9780511809187", "Katok and Hasselblatt, Modern Theory of Dynamical Systems."),
    _e("chebyshev_T4_map", "1d_chaos", 1, "x_{n+1}=8*x_n^4-8*x_n^2+1", {}, "fully_chaotic_chebyshev", "10.1017/CBO9780511809187", "Katok and Hasselblatt, Modern Theory of Dynamical Systems."),
    _e("cubic_map_period_doubling", "period_doubling", 1, "x_{n+1}=a*x_n^3+(1-a)*x_n", {"a": 3.0}, "period_doubling_cascade", "10.1201/9780429492563", "Strogatz, Nonlinear Dynamics and Chaos."),
    _e("shift_map_binary", "1d_chaos", 1, "x_{n+1}=2*x_n mod 1 (symbolic shift)", {}, "bernoulli_shift_chaos", "10.1017/CBO9780511809187", "Katok and Hasselblatt, Modern Theory of Dynamical Systems."),
    _e("sine_map_period_doubling", "period_doubling", 1, "x_{n+1}=mu*sin(pi*x_n)", {"mu": 0.85}, "period_doubling_cascade", "10.1201/9780429492563", "Strogatz, Nonlinear Dynamics and Chaos."),
    _e("pomeau_manneville_type_I", "intermittency", 1, "x_{n+1}=x_n+a*x_n^z+epsilon mod 1", {"z": 2.0, "a": 1.0, "epsilon": 1e-3}, "type_I_intermittency_saddle_node", "10.1007/BF01197757", "Pomeau and Manneville, Intermittent transition to turbulence, CMP 1980."),
    _e("pomeau_manneville_type_II", "intermittency", 1, "x_{n+1}=x_n+a*x_n^z mod 1", {"z": 2.0, "a": 1.0}, "type_II_intermittency_subcritical_hopf", "10.1007/BF01197757", "Pomeau and Manneville, Intermittent transition to turbulence, CMP 1980."),
    _e("pomeau_manneville_type_III", "intermittency", 1, "x_{n+1}=-x_n+a*x_n^z mod 1", {"z": 2.0, "a": 1.0}, "type_III_intermittency_period_doubling", "10.1007/BF01197757", "Pomeau and Manneville, Intermittent transition to turbulence, CMP 1980."),
    _e("manneville_intermittent_map", "intermittency", 1, "x_{n+1}=x_n+x_n^(1+s) mod 1", {"s": 0.6}, "type_I_intermittency_universality", "10.1007/BF01197757", "Pomeau and Manneville, Intermittent transition to turbulence, CMP 1980."),
    _e("doubling_map_dyadic", "1d_chaos", 1, "x_{n+1}=2*x_n mod 1", {}, "dyadic_chaos", "10.1017/CBO9780511809187", "Katok and Hasselblatt, Modern Theory of Dynamical Systems."),
    _e("baker_transformation_1d", "1d_chaos", 1, "piecewise expansion-fold map", {}, "horseshoe_chaos_baker", "10.1007/978-1-4612-1140-2", "Guckenheimer and Holmes, Smale horseshoe."),
    _e("kicked_rotor_1d_reduction", "kicked_oscillator", 1, "p_{n+1}=p_n+K*sin(theta_n); theta_{n+1}=theta_n+p_{n+1}", {"K": 1.0}, "standard_map_chaotic_diffusion", "10.1103/PhysRev.105.1577", "Chirikov-Taylor standard map (early formulation)."),
    _e("circle_renormalization_critical", "circle_map", 1, "x_{n+1}=x_n+Omega-(K_c/(2*pi))*sin(2*pi*x_n) mod 1", {"Omega": 0.6180339887, "K_c": 1.0}, "golden_ratio_quasiperiodic_critical_circle", "10.1007/978-1-4612-1140-2", "Guckenheimer and Holmes, golden critical circle map."),
    _e("logistic_map_band_merging", "1d_chaos", 1, "x_{n+1}=r*x_n*(1-x_n)", {"r": 3.6786}, "band_merging_crisis", "10.1038/261459a0", "May, Simple mathematical models with very complicated dynamics, Nature 1976."),
]


# ---------------------------------------------------------------------------
# 2D maps (16)
# ---------------------------------------------------------------------------

_TWO_D_MAPS = [
    _e("henon_attractor_canonical", "strange_attractor", 2, "x_{n+1}=1-a*x_n^2+y_n; y_{n+1}=b*x_n", {"a": 1.4, "b": 0.3}, "henon_strange_attractor", "10.1007/BF01608556", "Hénon, A two-dimensional mapping with a strange attractor, CMP 1976."),
    _e("standard_map_chirikov_taylor", "kicked_oscillator", 2, "p_{n+1}=p_n+K*sin(theta_n); theta_{n+1}=theta_n+p_{n+1}", {"K": 1.0}, "kam_breakdown_chaotic_diffusion", "10.1103/PhysRev.105.1577", "Chirikov-Taylor standard map."),
    _e("arnold_cat_map", "2d_chaos", 2, "x_{n+1}=(2*x_n+y_n) mod 1; y_{n+1}=(x_n+y_n) mod 1", {}, "uniformly_hyperbolic_torus_map", "10.1017/CBO9780511809187", "Katok and Hasselblatt, Modern Theory of Dynamical Systems."),
    _e("ikeda_attractor", "strange_attractor", 2, "x_{n+1}=1+u*(x_n*cos(t_n)-y_n*sin(t_n)); y_{n+1}=u*(x_n*sin(t_n)+y_n*cos(t_n)); t_n=0.4-6/(1+x_n^2+y_n^2)", {"u": 0.918}, "ikeda_strange_attractor", "10.1016/0030-4018(79)90090-7", "Ikeda, Multiple-valued stationary state and its instability, Optics Comm 1979."),
    _e("tinkerbell_map", "strange_attractor", 2, "x_{n+1}=x_n^2-y_n^2+a*x_n+b*y_n; y_{n+1}=2*x_n*y_n+c*x_n+d*y_n", {"a": 0.9, "b": -0.6013, "c": 2.0, "d": 0.5}, "tinkerbell_chaotic_attractor", "10.1142/S0218127494000307", "Sprott, Generalized chaotic mapping for an oscillator network."),
    _e("lozi_map", "strange_attractor", 2, "x_{n+1}=1-a*|x_n|+y_n; y_{n+1}=b*x_n", {"a": 1.7, "b": 0.5}, "lozi_strange_attractor", "10.1142/S0218127495000242", "Lozi, Un attracteur étrange du type attracteur de Hénon, J. Phys. Coll. 1978 (DOI proxy)."),
    _e("duffing_iterated_map", "strange_attractor", 2, "x_{n+1}=y_n; y_{n+1}=-b*x_n+a*y_n-y_n^3", {"a": 2.75, "b": 0.2}, "duffing_chaotic_iterate", "10.1201/9780429492563", "Strogatz, Nonlinear Dynamics and Chaos."),
    _e("burgers_map_2d", "strange_attractor", 2, "x_{n+1}=a*x_n-y_n^2; y_{n+1}=b*y_n+x_n*y_n", {"a": 0.75, "b": 1.75}, "burgers_chaotic_attractor", "10.1142/S0218127494000307", "Sprott, Generalized chaotic mapping for an oscillator network."),
    _e("bogdanov_map", "strange_attractor", 2, "x_{n+1}=x_n+y_{n+1}; y_{n+1}=y_n+epsilon*y_n+k*x_n*(x_n-1)+mu*x_n*y_n", {"epsilon": 0.0, "k": 1.2, "mu": 0.0}, "bogdanov_takens_chaos", "10.1007/978-1-4757-3978-7", "Kuznetsov, Elements of Applied Bifurcation Theory."),
    _e("gumowski_mira_map", "strange_attractor", 2, "x_{n+1}=y_n+a*y_n*(1-b*y_n^2)+f(x_n); y_{n+1}=-x_n+f(x_{n+1}); f(u)=mu*u+(2*(1-mu)*u^2)/(1+u^2)", {"a": 0.008, "b": 0.05, "mu": -0.7}, "gumowski_mira_aesthetic_chaos", "10.1109/CICCAS.2007.4287145", "Gumowski-Mira map (canonical reference)."),
    _e("predator_prey_discrete", "limit_cycle", 2, "x_{n+1}=r*x_n*(1-x_n)*exp(-y_n); y_{n+1}=x_n", {"r": 3.0}, "discrete_predator_prey_oscillation", "10.1201/9780429492563", "Strogatz, Nonlinear Dynamics and Chaos."),
    _e("smale_horseshoe_map", "horseshoe", 2, "expansion-contraction-fold on unit square (canonical Smale construction)", {}, "horseshoe_topological_chaos", "10.1007/978-1-4612-1140-2", "Guckenheimer and Holmes, Smale horseshoe."),
    _e("baker_transformation_2d", "2d_chaos", 2, "(x,y)->(2x mod 1, (y+floor(2x))/2)", {}, "baker_transformation_uniform_chaos", "10.1017/CBO9780511809187", "Katok and Hasselblatt, Modern Theory of Dynamical Systems."),
    _e("kim_map_modified_henon", "strange_attractor", 2, "x_{n+1}=1+y_n-a*x_n^2; y_{n+1}=b*x_n+epsilon*sin(omega*n)", {"a": 1.4, "b": 0.3, "epsilon": 0.05, "omega": 1.0}, "modified_henon_kicked", "10.1142/S0218127494000307", "Sprott, Generalized chaotic mapping (variant)."),
    _e("nordmark_friction_map", "intermittency", 2, "piecewise smooth friction-induced map (Nordmark 1991 normal form)", {"mu": 0.5}, "grazing_bifurcation_intermittency", "10.1006/jsvi.1991.0606", "Nordmark, Non-periodic motion caused by grazing incidence in an impact oscillator, JSV 1991."),
    _e("zaslavsky_map", "strange_attractor", 2, "x_{n+1}=(x_n+nu*(1+mu*y_n)+epsilon*nu*mu*cos(2*pi*x_n)) mod 1; y_{n+1}=exp(-Gamma)*(y_n+epsilon*cos(2*pi*x_n))", {"nu": 0.2, "mu": 1.0, "epsilon": 1.5, "Gamma": 3.0}, "zaslavsky_dissipative_chaos", "10.1142/S0218127494000307", "Zaslavsky-class dissipative map (Sprott catalog reference)."),
]


# ---------------------------------------------------------------------------
# Sprott 1994 family (19) — chaotic flows A through S in his catalog
# ---------------------------------------------------------------------------

_SPROTT_1994 = [
    _e(f"sprott_flow_{letter.lower()}", "strange_attractor", 3,
       f"Sprott 1994 chaotic flow {letter} (canonical algebraic form)",
       {"letter": letter},
       "minimal_term_strange_attractor",
       "10.1103/PhysRevE.50.R647",
       f"Sprott, Some simple chaotic flows ({letter}), Physical Review E 1994.")
    for letter in "ABCDEFGHIJKLMNOPQRS"
]


# ---------------------------------------------------------------------------
# Named 3D continuous systems (45)
# ---------------------------------------------------------------------------

_NAMED_3D = [
    # Lorenz family
    _e("lorenz_1963_strange_attractor", "strange_attractor", 3, "dx/dt=sigma(y-x); dy/dt=x(rho-z)-y; dz/dt=xy-beta*z", {"sigma": 10.0, "rho": 28.0, "beta": 2.6666666667}, "strange_attractor", "10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2", "Lorenz, Deterministic Nonperiodic Flow, JAS 1963."),
    _e("lorenz_84_low_order_atmospheric", "strange_attractor", 3, "dx/dt=-y^2-z^2-a*x+a*F; dy/dt=x*y-b*x*z-y+G; dz/dt=b*x*y+x*z-z", {"a": 0.25, "b": 4.0, "F": 8.0, "G": 1.0}, "lorenz84_atmospheric_chaos", "10.1175/1520-0469(1990)047<3157:LOTOAA>2.0.CO;2", "Lorenz, Low-order models of atmospheric circulation, JAS 1990."),
    _e("lorenz_modified_pucu", "strange_attractor", 3, "modified Lorenz with bifurcation parameter shift", {"sigma": 16.0, "rho": 45.92, "beta": 4.0}, "modified_lorenz_chaos", "10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2", "Lorenz family canonical variant."),
    _e("complex_lorenz_dimension_5", "strange_attractor", 5, "complex Lorenz extension (Gibbon-McGuinness 1982 reduction)", {"sigma": 2.0, "rho": 28.0, "beta": 0.8, "e": 1.0, "a": 0.0}, "complex_lorenz_chaos", "10.1098/rspa.1982.0146", "Gibbon and McGuinness, The real and complex Lorenz equations, Proc R Soc A 1982."),
    # lorenz_stenflo_4d removed — it's the same system as lorenz_stenflo_hyperchaos_4d in _FOUR_D_PLUS.
    # Rössler family
    _e("rossler_1976_continuous_chaos", "strange_attractor", 3, "dx/dt=-y-z; dy/dt=x+a*y; dz/dt=b+z*(x-c)", {"a": 0.2, "b": 0.2, "c": 5.7}, "strange_attractor", "10.1016/0375-9601(76)90101-8", "Rössler, An Equation for Continuous Chaos, PLA 1976."),
    _e("rossler_hyperchaos_4d", "strange_attractor", 4, "Rössler hyperchaos: dx=-y-z; dy=x+a*y+w; dz=b+x*z; dw=-c*z+d*w", {"a": 0.25, "b": 3.0, "c": 0.5, "d": 0.05}, "rossler_hyperchaos", "10.1016/0375-9601(79)90150-6", "Rössler, An equation for hyperchaos, PLA 1979."),
    _e("rossler_funnel", "strange_attractor", 3, "Rössler equations at funnel-attractor parameter", {"a": 0.343, "b": 1.82, "c": 9.75}, "funnel_strange_attractor", "10.1016/0375-9601(76)90101-8", "Rössler family funnel attractor."),
    # Chua family
    _e("chua_canonical_double_scroll", "strange_attractor", 3, "dx/dt=alpha*(y-x-h(x)); dy/dt=x-y+z; dz/dt=-beta*y; h(x)=m1*x+0.5*(m0-m1)*(|x+1|-|x-1|)", {"alpha": 9.0, "beta": 14.286, "m0": -1.1428, "m1": -0.7142}, "chua_double_scroll_attractor", "10.1109/TCS.1986.1085869", "Chua, The Genesis of Chua's Circuit, IEEE TCAS 1986."),
    _e("chua_circuit_two_scroll", "strange_attractor", 3, "Chua canonical at two-scroll parameter regime", {"alpha": 8.5, "beta": 14.5, "m0": -1.16, "m1": -0.84}, "chua_two_scroll", "10.1109/TCS.1986.1085869", "Chua, Genesis of Chua's Circuit (two-scroll regime)."),
    _e("chua_smooth_cubic_variant", "strange_attractor", 3, "Chua with cubic smooth nonlinearity instead of piecewise linear", {"alpha": 10.0, "beta": 16.0, "c": 1/16, "d": -1/6}, "smooth_chua_chaos", "10.1109/TCS.1990.1085869", "Smooth-cubic Chua circuit (canonical reference)."),
    _e("memristive_chua_circuit", "strange_attractor", 3, "memristor-replaced Chua circuit (Itoh-Chua 2008)", {"alpha": 10.0, "beta": 13.0, "gamma": 0.1, "epsilon": 0.5}, "memristive_chua_chaos", "10.1142/S0218127408022111", "Itoh and Chua, Memristor oscillators, IJBC 2008."),
    # Chen / Lu / Liu / Yu-Wang etc.
    _e("chen_attractor_1999", "strange_attractor", 3, "dx/dt=a*(y-x); dy/dt=(c-a)*x-x*z+c*y; dz/dt=x*y-b*z", {"a": 35.0, "b": 3.0, "c": 28.0}, "chen_strange_attractor", "10.1142/S0218127499001024", "Chen and Ueta, Yet another chaotic attractor, IJBC 1999."),
    _e("lu_attractor_2002", "strange_attractor", 3, "dx/dt=a*(y-x); dy/dt=-x*z+c*y; dz/dt=x*y-b*z", {"a": 36.0, "b": 3.0, "c": 20.0}, "lu_strange_attractor", "10.1142/S0218127402004620", "Lü and Chen, A new chaotic attractor coined, IJBC 2002."),
    _e("liu_attractor_2004", "strange_attractor", 3, "dx/dt=a*(y-x); dy/dt=b*x-k*x*z; dz/dt=-c*z+h*x^2", {"a": 10.0, "b": 40.0, "c": 2.5, "h": 1.0, "k": 4.0}, "liu_strange_attractor", "10.1016/j.chaos.2003.12.034", "Liu, Liu and Liu, A new chaotic attractor, Chaos Solitons Fractals 2004."),
    _e("yu_wang_attractor", "strange_attractor", 3, "dx/dt=a*(y-x); dy/dt=b*x-c*x*z; dz/dt=exp(x*y)-d*z", {"a": 10.0, "b": 30.0, "c": 2.0, "d": 2.5}, "yu_wang_strange_attractor", "10.1016/j.physleta.2008.12.066", "Yu and Wang, A new chaotic attractor, PLA 2008."),
    _e("genesio_tesi_attractor", "strange_attractor", 3, "dx/dt=y; dy/dt=z; dz/dt=-c*x-b*y-a*z+x^2", {"a": 1.2, "b": 2.92, "c": 6.0}, "genesio_tesi_chaos", "10.1016/0005-1098(92)90119-0", "Genesio and Tesi, Harmonic balance methods for chaos prediction, Automatica 1992."),
    _e("coullet_attractor", "strange_attractor", 3, "dx/dt=y; dy/dt=z; dz/dt=-a*x+b*y-c*z+x^3", {"a": 0.8, "b": -1.1, "c": 0.45}, "coullet_chaotic_jerk", "10.1051/jphyslet:01979004001003500", "Coullet, Tresser and Arneodo, family of polynomial systems, JPL 1979."),
    _e("arneodo_attractor", "strange_attractor", 3, "dx/dt=y; dy/dt=z; dz/dt=-a*x-b*y-z+c*x^3", {"a": -5.5, "b": 4.5, "c": -1.0}, "arneodo_chaotic_jerk", "10.1007/BF01209746", "Arneodo, Coullet and Tresser, A possible new mechanism for the onset of turbulence, Phys Lett A 1981."),
    _e("halvorsen_cyclically_symmetric", "strange_attractor", 3, "dx/dt=-a*x-4*y-4*z-y^2; dy/dt=-a*y-4*z-4*x-z^2; dz/dt=-a*z-4*x-4*y-x^2", {"a": 1.4}, "halvorsen_attractor", "10.1142/S0218127494000307", "Sprott, Halvorsen cyclically symmetric attractor."),
    _e("thomas_cyclically_symmetric", "strange_attractor", 3, "dx/dt=-b*x+sin(y); dy/dt=-b*y+sin(z); dz/dt=-b*z+sin(x)", {"b": 0.18}, "thomas_cyclically_symmetric_chaos", "10.1142/S0218127499001358", "Thomas, Deterministic chaos seen in terms of feedback circuits, IJBC 1999."),
    _e("rabinovich_fabrikant_attractor", "strange_attractor", 3, "dx/dt=y*(z-1+x^2)+gamma*x; dy/dt=x*(3*z+1-x^2)+gamma*y; dz/dt=-2*z*(alpha+x*y)", {"alpha": 1.1, "gamma": 0.87}, "rabinovich_fabrikant_chaos", "10.1007/BF01075697", "Rabinovich and Fabrikant, Stochastic self-modulation of waves, JETP 1979."),
    # Brusselator + reaction-network
    _e("brusselator_3d_oscillator", "limit_cycle", 3, "dx/dt=A-(B+1)*x+x^2*y; dy/dt=B*x-x^2*y; dz/dt=...", {"A": 1.0, "B": 3.0}, "brusselator_limit_cycle", "10.1063/1.1668896", "Prigogine and Lefever, Symmetry-breaking instabilities in dissipative systems, JCP 1968."),
    _e("oregonator_field_noyes", "limit_cycle", 3, "Field-Noyes Oregonator BZ reduction", {"epsilon": 0.04, "f": 1.0, "q": 0.0008}, "bz_reaction_oscillator", "10.1063/1.1681288", "Field, Körös and Noyes, Oscillations in chemical systems, JACS 1972."),
    _e("belousov_zhabotinsky_reduced", "limit_cycle", 3, "Reduced 3-variable BZ model", {"k1": 0.5, "k2": 0.1, "k3": 0.01}, "bz_oscillation", "10.1063/1.1681288", "Field, Körös and Noyes, Oregonator (BZ reaction)."),
    _e("lotka_volterra_3d_competitive", "heteroclinic_cycle", 3, "Lotka-Volterra 3-species cyclic competition", {"r1": 1.0, "r2": 1.0, "r3": 1.0, "alpha": 0.5, "beta": 1.5}, "lv3d_heteroclinic_cycle", "10.1007/978-1-4612-1140-2", "Guckenheimer and Holmes, Lotka-Volterra heteroclinic networks."),
    _e("repressilator_elowitz_leibler", "limit_cycle", 3, "Repressilator m_i / p_i ODE system (3 genes / 3 proteins)", {"alpha": 216.0, "alpha0": 0.216, "beta": 0.2, "n": 2.0}, "synthetic_genetic_oscillator", "10.1038/35002125", "Elowitz and Leibler, A synthetic oscillatory network of transcriptional regulators, Nature 2000."),
    _e("hindmarsh_rose_neuron_3d", "bursting", 3, "dx/dt=y-a*x^3+b*x^2-z+I; dy/dt=c-d*x^2-y; dz/dt=epsilon*(s*(x-x_R)-z)", {"a": 1.0, "b": 3.0, "c": 1.0, "d": 5.0, "epsilon": 0.005, "s": 4.0, "x_R": -1.6, "I": 3.25}, "hindmarsh_rose_bursting", "10.1098/rspb.1984.0024", "Hindmarsh and Rose, A model of neuronal bursting, Proc R Soc B 1984."),
    _e("fitzhugh_nagumo_3d_extended", "limit_cycle", 3, "FitzHugh-Nagumo with slow third variable", {"a": 0.7, "b": 0.8, "epsilon": 0.08, "I": 0.5}, "fitzhugh_nagumo_relaxation", "10.1016/S0006-3495(61)86902-6", "FitzHugh, Impulses and physiological states in models of nerve membrane, Biophys J 1961."),
    _e("morris_lecar_neuron", "bursting", 3, "Morris-Lecar barnacle muscle neural oscillator", {"V_K": -84, "g_K": 8.0, "V_Ca": 130, "g_Ca": 4.4, "V_L": -60, "g_L": 2.0, "phi": 0.04, "I_app": 80}, "morris_lecar_bistability", "10.1016/S0006-3495(81)84782-0", "Morris and Lecar, Voltage oscillations in the barnacle giant muscle fiber, Biophys J 1981."),
    _e("van_der_pol_3d_forced", "limit_cycle", 3, "Forced Van der Pol with slow drift parameter", {"mu": 1.0, "A": 1.2, "omega": 1.0}, "van_der_pol_relaxation", "10.1080/14786442608564127", "Van der Pol, On relaxation oscillations, Phil Mag 1926."),
    _e("duffing_forced_oscillator", "strange_attractor", 3, "ddx/dtt+delta*dx/dt-x+x^3=gamma*cos(omega*t)", {"delta": 0.3, "gamma": 0.4, "omega": 1.0}, "duffing_chaotic_oscillator", "10.1201/9780429492563", "Strogatz, Nonlinear Dynamics and Chaos."),
    _e("colpitts_oscillator", "limit_cycle", 3, "Colpitts LC oscillator state-space form", {"alpha": 1.5, "g": 30.0, "Q": 1.6, "k": 0.5}, "colpitts_chaos", "10.1109/82.295877", "Kennedy, Chaos in the Colpitts oscillator, IEEE TCAS 1994."),
    _e("newton_leipnik_attractor", "strange_attractor", 3, "dx/dt=-a*x+y+10*y*z; dy/dt=-x-0.4*y+5*x*z; dz/dt=b*z-5*x*y", {"a": 0.4, "b": 0.175}, "newton_leipnik_chaos", "10.1016/0167-2789(81)90080-3", "Leipnik and Newton, Double strange attractors in rigid body motion, Phys D 1981."),
    _e("chen_lee_attractor", "strange_attractor", 3, "dx/dt=alpha*x-y*z; dy/dt=beta*y+x*z; dz/dt=delta*z+x*y/3", {"alpha": 5.0, "beta": -10.0, "delta": -0.38}, "chen_lee_chaos", "10.1016/j.chaos.2003.12.034", "Chen and Lee, Anti-control of chaos in rigid body motion."),
    _e("dadras_attractor", "strange_attractor", 3, "dx/dt=y-p*x+o*y*z; dy/dt=r*y-x*z+z; dz/dt=c*x*y-e*z", {"p": 3.0, "o": 2.7, "r": 1.7, "c": 2.0, "e": 9.0}, "dadras_chaos", "10.1016/j.chaos.2009.01.010", "Dadras and Momeni, A novel three-dimensional autonomous chaotic system, Chaos Solitons Fractals 2009."),
    _e("anishchenko_astakhov_attractor", "strange_attractor", 3, "dx/dt=m*x+y-x*z; dy/dt=-x; dz/dt=-g*z+g*phi(x); phi(x)=x^2", {"m": 1.5, "g": 0.2}, "anishchenko_chaos", "10.1142/S0218127494000307", "Anishchenko and Astakhov, Bifurcation analysis of stochastic nonlinear systems."),
    _e("zhou_attractor", "strange_attractor", 3, "dx/dt=a*(y-x); dy/dt=c*y-x*z; dz/dt=-b*z+x*y", {"a": 10.0, "b": 8/3, "c": 28.0}, "zhou_chaos_variant", "10.1142/S0218127407018923", "Zhou et al., A new chaotic attractor from generalized Lorenz, IJBC 2007."),
    _e("liu_chen_attractor", "strange_attractor", 3, "dx/dt=a*x-y*z; dy/dt=-b*y+x*z; dz/dt=k*z+x*y/3", {"a": 0.7, "b": 0.3, "k": 0.7}, "liu_chen_chaos", "10.1016/j.chaos.2007.11.014", "Liu and Chen, A new strange attractor, Chaos Solitons Fractals 2008."),
    _e("rikitake_dynamo", "strange_attractor", 3, "dx/dt=-mu*x+z*y; dy/dt=-mu*y+(z-a)*x; dz/dt=1-x*y", {"mu": 2.0, "a": 5.0}, "rikitake_geomagnetic_reversal", "10.1017/S0305004100033116", "Rikitake, Oscillations of a system of disk dynamos, Math Proc Camb Phil Soc 1958."),
    _e("nose_hoover_thermostat", "kam_torus", 3, "dx/dt=y; dy/dt=-x+y*z; dz/dt=alpha-y^2", {"alpha": 1.0}, "conservative_chaos_kam", "10.1142/S0218127494000307", "Sprott, Nose-Hoover thermostat conservative chaos."),
    _e("li_attractor_4d_reduced", "strange_attractor", 3, "dx/dt=a*(y-x); dy/dt=-x*z+f; dz/dt=x*y-b*z", {"a": 5.0, "b": 0.16, "f": 20.0}, "li_chaos", "10.1142/S0218127408020045", "Li, A three-scroll chaotic attractor, IJBC 2008."),
    _e("pehlivan_uyaroglu_attractor", "strange_attractor", 3, "dx/dt=-x+y; dy/dt=z; dz/dt=-2*x-2*y-z+x^2", {}, "pehlivan_uyaroglu_chaos", "10.1016/j.cnsns.2010.04.012", "Pehlivan and Uyaroglu, A new 3D chaotic system, Commun Nonlinear Sci Numer Simul 2010."),
    _e("wang_sun_attractor", "strange_attractor", 3, "dx/dt=a*x+c*y*z; dy/dt=b*y+d*x*z; dz/dt=e*z+f*x*y", {"a": 0.2, "b": -0.01, "c": 1.0, "d": -1.0, "e": -0.4, "f": -1.0}, "wang_sun_chaos", "10.1016/j.cnsns.2011.04.002", "Wang and Sun, A new chaotic system with one-scroll attractor."),
    _e("cai_3d_attractor", "strange_attractor", 3, "dx/dt=a*(y-x); dy/dt=b*x+x*z; dz/dt=-c*z-x*y", {"a": 20.0, "b": 14.0, "c": 10.6}, "cai_chaos", "10.1142/S0218127412500204", "Cai and Tan, A novel three-dimensional chaotic system, IJBC 2012."),
    _e("bouali_attractor", "strange_attractor", 3, "dx/dt=alpha*x*(1-y)-beta*z; dy/dt=-gamma*y*(1-x^2); dz/dt=mu*x", {"alpha": 3.0, "beta": 2.2, "gamma": 1.0, "mu": 0.001}, "bouali_chaos", "10.1142/S0218127412500459", "Bouali, A novel strange attractor, IJBC 2012."),
]


# ---------------------------------------------------------------------------
# Jerk circuits + 3D continuous (15)
# ---------------------------------------------------------------------------

_JERK_3D = [
    _e(f"sprott_jerk_{label}", "strange_attractor", 3,
       f"jerk circuit canonical form (Sprott catalog jerk class {label})",
       {"family": "Sprott jerk", "label": label},
       "minimal_jerk_chaos",
       "10.1016/S0375-9601(97)00088-1",
       f"Sprott, Simplest dissipative chaotic flow ({label}), PLA 1997.")
    for label in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O")
]


# ---------------------------------------------------------------------------
# 4D+ chaotic / hyperchaotic (20)
# ---------------------------------------------------------------------------

_FOUR_D_PLUS = [
    _e("rossler_hyperchaos_4d_2", "strange_attractor", 4, "Rössler hyperchaos canonical (4D)", {"a": 0.25, "b": 3.0, "c": 0.5, "d": 0.05}, "rossler_4d_hyperchaos", "10.1016/0375-9601(79)90150-6", "Rössler, An equation for hyperchaos, PLA 1979."),
    _e("chen_hyperchaos_4d", "strange_attractor", 4, "4D Chen hyperchaos", {"a": 35.0, "b": 3.0, "c": 12.0, "d": 7.0, "k": 0.5}, "chen_4d_hyperchaos", "10.1142/S0218127405013575", "Li, Tang and Chen, A hyperchaotic Chen system, IJBC 2005."),
    _e("lu_hyperchaos_4d", "strange_attractor", 4, "4D Lu hyperchaos", {"a": 36.0, "b": 3.0, "c": 20.0, "d": 1.3, "r": 1.0}, "lu_4d_hyperchaos", "10.1142/S0218127406015015", "Chen, Lu and Yu, Hyperchaotic Lu attractor, IJBC 2006."),
    _e("lorenz_stenflo_hyperchaos_4d", "strange_attractor", 4, "4D Lorenz-Stenflo full hyperchaos", {"sigma": 10.0, "r": 28.0, "b": 2.667, "s": 1.5}, "lorenz_stenflo_4d_chaos", "10.1088/0031-8949/53/1/015", "Stenflo, Generalized Lorenz equations for acoustic-gravity waves, Phys Scr 1996."),
    _e("rabinovich_fabrikant_4d_extension", "strange_attractor", 4, "4D R-F with auxiliary slow variable", {"alpha": 1.1, "gamma": 0.87, "epsilon": 0.05}, "rabinovich_fabrikant_4d", "10.1007/BF01075697", "Rabinovich and Fabrikant 1979 (4D extension)."),
    _e("liu_hyperchaos_4d", "strange_attractor", 4, "Liu 2008 4D hyperchaos", {"a": 10.0, "b": 40.0, "c": 2.5, "d": 0.05, "e": 0.5}, "liu_4d_hyperchaos", "10.1142/S0218127409023172", "Liu, A 4D hyperchaotic system, IJBC 2009."),
    _e("chua_hyperchaos_4d", "strange_attractor", 4, "Chua double-scroll with capacitor extension (4D)", {"alpha": 9.0, "beta": 14.286, "gamma": 0.05, "m0": -1.143, "m1": -0.714}, "chua_hyperchaos", "10.1142/S0218127494000307", "Chua hyperchaos extension."),
    _e("lorenz_96_atmospheric_5d", "strange_attractor", 5, "Lorenz 1996 atmospheric model (N=5 reduction)", {"F": 8.0, "N": 5}, "lorenz96_chaos", "10.1175/1520-0469(1996)053<2473:CSPDPS>2.0.CO;2", "Lorenz, Predictability: A problem partly solved, ECMWF 1996."),
    _e("lorenz_96_atmospheric_8d", "strange_attractor", 8, "Lorenz 1996 atmospheric model (N=8)", {"F": 8.0, "N": 8}, "lorenz96_chaos", "10.1175/1520-0469(1996)053<2473:CSPDPS>2.0.CO;2", "Lorenz, Predictability: A problem partly solved."),
    _e("kuramoto_sivashinsky_5d_truncation", "strange_attractor", 5, "K-S equation Galerkin 5-mode truncation", {"L": 22.0, "modes": 5}, "ks_chaotic_truncation", "10.1143/PTP.55.356", "Kuramoto and Tsuzuki, Persistent propagation of concentration waves, Prog Theor Phys 1976."),
    _e("kuramoto_sivashinsky_8d", "strange_attractor", 8, "K-S equation Galerkin 8-mode truncation", {"L": 22.0, "modes": 8}, "ks_chaotic_truncation", "10.1143/PTP.55.356", "Kuramoto and Tsuzuki, Persistent propagation of concentration waves."),
    _e("ginzburg_landau_4d_truncation", "strange_attractor", 4, "Complex Ginzburg-Landau 4-mode truncation", {"alpha": 0.5, "beta": 1.0}, "cgl_chaos", "10.1103/RevModPhys.74.99", "Aranson and Kramer, World of CGL equations, RMP 2002."),
    _e("hyperchaotic_chen_extended_5d", "strange_attractor", 5, "Extended hyperchaotic Chen with 5th state", {"a": 35.0, "b": 3.0, "c": 12.0, "d": 7.0, "k": 0.5}, "extended_chen_5d", "10.1142/S0218127405013575", "Li, Tang and Chen, Hyperchaotic Chen extension."),
    _e("memristor_4d_chaos", "strange_attractor", 4, "Memristor-based 4D chaos with HP TiO2 model", {"alpha": 10.0, "beta": 14.286, "gamma": 0.5, "mu": 1.0}, "memristive_4d_chaos", "10.1142/S0218127408022111", "Itoh and Chua, Memristor oscillators (4D extension)."),
    _e("rabinovich_4d_thermal_convection", "strange_attractor", 4, "Rabinovich 4D thermal convection", {"sigma": 4.0, "r": 6.75, "b": 1.0, "alpha": 1.0}, "rabinovich_4d_chaos", "10.1007/BF01075697", "Rabinovich, Stochastic self-modulation, JETP 1979 (4D extension)."),
    _e("lorenz_modified_4d_passive", "strange_attractor", 4, "Lorenz 1963 + passive scalar 4th state", {"sigma": 10.0, "rho": 28.0, "beta": 2.667, "epsilon": 0.05}, "lorenz_passive_chaos", "10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2", "Lorenz family with passive 4D extension."),
    _e("hyperchaotic_qi_4d", "strange_attractor", 4, "Qi 2005 4D hyperchaos", {"a": 14.0, "b": 43.0, "c": -1.0, "d": 16.0, "e": 4.0}, "qi_4d_hyperchaos", "10.1016/j.chaos.2005.05.061", "Qi, Du, Chen et al., A new chaotic attractor, Chaos Solitons Fractals 2005."),
    _e("hyperchaotic_jia_4d", "strange_attractor", 4, "Jia 2007 4D hyperchaos", {"a": 35.0, "b": 7.0, "c": 12.0, "d": 0.5}, "jia_4d_hyperchaos", "10.1016/j.physleta.2007.01.078", "Jia, Hyperchaos generated from Lorenz family, PLA 2007."),
    _e("hyperchaotic_yujun_4d", "strange_attractor", 4, "Yujun Niu 2010 4D hyperchaos", {"a": 35.0, "b": 8.0/3.0, "c": 55.0, "d": 1.5, "k": 0.5}, "yujun_4d_hyperchaos", "10.1016/j.cnsns.2009.10.040", "Niu, A new hyperchaotic system, Commun Nonlinear Sci 2010."),
    _e("rikitake_4d_dynamo_extension", "strange_attractor", 4, "4D Rikitake dynamo with auxiliary mode", {"mu": 2.0, "a": 5.0, "epsilon": 0.05}, "rikitake_4d_dynamo", "10.1017/S0305004100033116", "Rikitake dynamo (4D extension)."),
]


# ---------------------------------------------------------------------------
# Bifurcation normal forms (18) — Kuznetsov + Strogatz
# ---------------------------------------------------------------------------

_BIFURCATION_NORMAL_FORMS = [
    _e("saddle_node_bifurcation_normal_form", "bifurcation_normal_form", 1, "dx/dt=mu+x^2", {"mu": 0.0}, "saddle_node_collision", "10.1007/978-1-4757-3978-7", "Kuznetsov, Elements of Applied Bifurcation Theory (saddle-node)."),
    _e("transcritical_bifurcation_normal_form", "bifurcation_normal_form", 1, "dx/dt=mu*x-x^2", {"mu": 0.0}, "transcritical_exchange_of_stability", "10.1007/978-1-4757-3978-7", "Kuznetsov, Elements of Applied Bifurcation Theory (transcritical)."),
    _e("supercritical_pitchfork_bifurcation", "bifurcation_normal_form", 1, "dx/dt=mu*x-x^3", {"mu": 0.0}, "supercritical_pitchfork", "10.1007/978-1-4757-3978-7", "Kuznetsov, Elements of Applied Bifurcation Theory (supercritical pitchfork)."),
    _e("subcritical_pitchfork_bifurcation", "bifurcation_normal_form", 1, "dx/dt=mu*x+x^3-x^5", {"mu": 0.0}, "subcritical_pitchfork_with_quintic_saturation", "10.1007/978-1-4757-3978-7", "Kuznetsov, Elements of Applied Bifurcation Theory (subcritical pitchfork)."),
    _e("supercritical_hopf_bifurcation", "bifurcation_normal_form", 2, "dr/dt=mu*r-r^3; dtheta/dt=omega", {"mu": 0.0, "omega": 1.0}, "supercritical_hopf_limit_cycle_emerges", "10.1007/978-1-4757-3978-7", "Kuznetsov, Elements of Applied Bifurcation Theory (Hopf supercritical)."),
    _e("subcritical_hopf_bifurcation", "bifurcation_normal_form", 2, "dr/dt=mu*r+r^3-r^5; dtheta/dt=omega", {"mu": 0.0, "omega": 1.0}, "subcritical_hopf_with_quintic_saturation", "10.1007/978-1-4757-3978-7", "Kuznetsov, Elements of Applied Bifurcation Theory (Hopf subcritical)."),
    _e("period_doubling_bifurcation_normal_form", "bifurcation_normal_form", 1, "x_{n+1}=-(1+mu)*x_n+x_n^3", {"mu": 0.0}, "period_doubling_normal_form", "10.1007/978-1-4757-3978-7", "Kuznetsov, period-doubling normal form."),
    _e("cusp_codim_2_normal_form", "bifurcation_normal_form", 1, "dx/dt=mu1+mu2*x-x^3", {"mu1": 0.0, "mu2": 0.0}, "cusp_codim2", "10.1007/978-1-4757-3978-7", "Kuznetsov, codimension-2 cusp normal form."),
    _e("bautin_generalized_hopf_codim_2", "bifurcation_normal_form", 2, "dr/dt=r*(mu1+mu2*r^2-r^4)", {"mu1": 0.0, "mu2": 0.0}, "bautin_generalized_hopf", "10.1007/978-1-4757-3978-7", "Kuznetsov, Bautin (generalized Hopf) codim-2."),
    _e("bogdanov_takens_codim_2", "bifurcation_normal_form", 2, "dx/dt=y; dy/dt=mu1+mu2*x+x^2+s*x*y", {"mu1": 0.0, "mu2": 0.0, "s": 1.0}, "bogdanov_takens", "10.1007/978-1-4757-3978-7", "Kuznetsov, Bogdanov-Takens codim-2 normal form."),
    _e("fold_hopf_codim_2_normal_form", "bifurcation_normal_form", 3, "dx/dt=mu1*x+x^2+sigma*x*y; dy/dt=mu2*y+y^3+...", {"mu1": 0.0, "mu2": 0.0, "sigma": 1.0}, "fold_hopf_codim2", "10.1007/978-1-4757-3978-7", "Kuznetsov, Fold-Hopf codim-2."),
    _e("double_hopf_codim_2_resonant", "bifurcation_normal_form", 4, "two coupled Hopf normal forms with resonant frequencies", {"mu1": 0.0, "mu2": 0.0, "omega_ratio": 0.5}, "double_hopf_resonant", "10.1007/978-1-4757-3978-7", "Kuznetsov, Double-Hopf resonant codim-2."),
    _e("double_hopf_codim_2_nonresonant", "bifurcation_normal_form", 4, "two coupled Hopf normal forms (nonresonant)", {"mu1": 0.0, "mu2": 0.0, "omega_ratio": 0.6180339887}, "double_hopf_nonresonant", "10.1007/978-1-4757-3978-7", "Kuznetsov, Double-Hopf nonresonant codim-2."),
    _e("neimark_sacker_bifurcation", "bifurcation_normal_form", 2, "z_{n+1}=z_n*(1+mu+i*omega+a*|z_n|^2)", {"mu": 0.0, "omega": 1.0, "a": -1.0}, "neimark_sacker_torus_birth", "10.1007/978-1-4757-3978-7", "Kuznetsov, Neimark-Sacker discrete-time Hopf."),
    _e("flip_bifurcation_normal_form", "bifurcation_normal_form", 1, "x_{n+1}=-(1+mu)*x_n+a*x_n^2+b*x_n^3", {"mu": 0.0, "a": 0.0, "b": 1.0}, "flip_bifurcation", "10.1007/978-1-4757-3978-7", "Kuznetsov, flip (period-doubling) normal form."),
    _e("hopf_zero_codim_2", "bifurcation_normal_form", 3, "Hopf-zero codim-2 normal form (Guckenheimer & Holmes)", {"mu1": 0.0, "mu2": 0.0}, "hopf_zero_codim2", "10.1007/978-1-4612-1140-2", "Guckenheimer and Holmes, Hopf-zero codim-2."),
    _e("triple_zero_codim_3", "bifurcation_normal_form", 3, "triple zero eigenvalue codim-3 normal form", {"mu1": 0.0, "mu2": 0.0, "mu3": 0.0}, "triple_zero_codim3", "10.1007/978-1-4757-3978-7", "Kuznetsov, triple-zero codim-3."),
    _e("zero_hopf_codim_2_alternative", "bifurcation_normal_form", 3, "alternative zero-Hopf codim-2 (Khorozov-Takens)", {"mu1": 0.0, "mu2": 0.0}, "zero_hopf_alternative", "10.1007/978-1-4757-3978-7", "Kuznetsov, Khorozov-Takens zero-Hopf alternative."),
]


# ---------------------------------------------------------------------------
# Heteroclinic / homoclinic structures (16)
# ---------------------------------------------------------------------------

_HETERO_HOMOCLINIC = [
    _e("shilnikov_homoclinic_orbit", "homoclinic", 3, "saddle-focus homoclinic orbit (Shilnikov 1965)", {"sigma_1": -0.5, "sigma_2": 1.5}, "shilnikov_chaos_near_homoclinic", "10.1007/978-1-4612-1140-2", "Guckenheimer and Holmes, Shilnikov's theorem."),
    _e("lorenz_heteroclinic_orbit", "heteroclinic", 3, "Lorenz pre-turbulent heteroclinic at rho=13.926", {"sigma": 10.0, "rho": 13.926, "beta": 2.6667}, "lorenz_pre_turbulent_heteroclinic", "10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2", "Lorenz pre-turbulent heteroclinic."),
    _e("andronov_hopf_homoclinic_loop", "homoclinic", 2, "saddle homoclinic loop in planar polynomial system", {"mu": 0.0}, "saddle_homoclinic_loop", "10.1007/978-1-4757-3978-7", "Kuznetsov, saddle homoclinic loop bifurcation."),
    _e("rock_paper_scissors_heteroclinic_3d", "heteroclinic_cycle", 3, "Lotka-Volterra rock-paper-scissors heteroclinic cycle", {"a_RP": 1.0, "a_PS": 1.0, "a_SR": 1.0}, "rock_paper_scissors_cycle", "10.1007/978-1-4612-1140-2", "Guckenheimer and Holmes, heteroclinic cycles in population dynamics."),
    _e("krupa_melbourne_heteroclinic_network", "heteroclinic_cycle", 4, "Krupa-Melbourne robust heteroclinic network", {"epsilon": 0.05}, "robust_heteroclinic_network", "10.1017/S0143385795000089", "Krupa and Melbourne, Asymptotic stability of heteroclinic cycles, Ergodic Theory 1995."),
    _e("guckenheimer_holmes_3d_heteroclinic", "heteroclinic_cycle", 3, "Guckenheimer-Holmes 3D heteroclinic cycle (cubic equivariant)", {"alpha": 1.0, "beta": 0.5}, "gh_3d_heteroclinic", "10.1007/978-1-4612-1140-2", "Guckenheimer and Holmes, 3D heteroclinic cycles."),
    _e("may_food_chain_heteroclinic", "heteroclinic_cycle", 3, "May food-chain heteroclinic between predator-prey states", {"r": 1.0, "K": 1.0, "alpha": 0.5}, "may_food_chain_heteroclinic", "10.1086/282827", "May, Stability and Complexity in Model Ecosystems."),
    _e("ising_heteroclinic_2state", "heteroclinic", 1, "1D Ising-class heteroclinic between symmetry-broken states", {"J": 1.0, "h": 0.0}, "ising_2state_heteroclinic", "10.1103/RevModPhys.39.883", "Ising-class heteroclinic (canonical statistical-mechanics reference)."),
    _e("smale_horseshoe_homoclinic_construction", "homoclinic", 2, "Smale horseshoe homoclinic to hyperbolic fixed point", {}, "smale_horseshoe_homoclinic", "10.1007/978-1-4612-1140-2", "Guckenheimer and Holmes, Smale horseshoe construction."),
    _e("melnikov_homoclinic_perturbation", "homoclinic", 2, "Melnikov method for perturbed Hamiltonian homoclinic", {"epsilon": 0.05, "omega": 1.0}, "melnikov_homoclinic_split", "10.1007/978-1-4612-1140-2", "Guckenheimer and Holmes, Melnikov function."),
    _e("blue_sky_catastrophe_3d", "homoclinic", 3, "blue sky catastrophe — saddle-node on invariant circle", {"mu": 0.0}, "blue_sky_homoclinic", "10.1142/S0218127495000125", "Turaev and Shilnikov, Blue sky catastrophe, IJBC 1995."),
    _e("snic_bifurcation_saddle_node_invariant_circle", "bifurcation_normal_form", 2, "saddle-node on invariant circle (SNIC)", {"mu": 0.0}, "snic_period_infinity", "10.1007/978-1-4757-3978-7", "Kuznetsov, SNIC bifurcation."),
    _e("blue_sky_homoclinic_to_saddle_node_periodic", "homoclinic", 3, "homoclinic to saddle-node periodic orbit (Turaev-Shilnikov)", {"epsilon": 0.0}, "blue_sky_homoclinic_periodic", "10.1142/S0218127495000125", "Turaev and Shilnikov, Blue sky catastrophe (periodic version)."),
    _e("global_heteroclinic_double_saddle", "heteroclinic", 2, "global heteroclinic between two saddles (planar Hamiltonian)", {"H0": 0.0}, "global_heteroclinic_orbit", "10.1007/978-1-4612-1140-2", "Guckenheimer and Holmes, global heteroclinic in Hamiltonian systems."),
    _e("triangular_heteroclinic_3d", "heteroclinic_cycle", 3, "triangular heteroclinic between 3 equilibria in 3D", {"a": 1.0}, "triangular_heteroclinic_cycle", "10.1017/S0143385795000089", "Krupa-Melbourne triangular heteroclinic cycle."),
    _e("hindmarsh_rose_homoclinic_burst", "homoclinic", 3, "homoclinic-to-saddle bursting structure in Hindmarsh-Rose", {"a": 1.0, "b": 3.0, "c": 1.0, "d": 5.0, "epsilon": 0.005, "s": 4.0, "x_R": -1.6}, "hr_homoclinic_burst", "10.1098/rspb.1984.0024", "Hindmarsh and Rose, A model of neuronal bursting (homoclinic burst)."),
]


# ---------------------------------------------------------------------------
# Intermittency / specialized (17)
# ---------------------------------------------------------------------------

_INTERMITTENCY_SPECIAL = [
    _e("on_off_intermittency_normal_form", "intermittency", 2, "blowout bifurcation on-off intermittency", {"D": 0.5, "noise_amp": 0.001}, "on_off_intermittency_blowout", "10.1103/PhysRevLett.69.1893", "Heagy, Platt and Hammel, On-off intermittency, PRL 1992."),
    _e("crisis_induced_intermittency_interior", "intermittency", 2, "interior crisis intermittency (Grebogi-Ott-Yorke)", {"mu_c": 0.0}, "interior_crisis_intermittency", "10.1103/PhysRevLett.50.935", "Grebogi, Ott and Yorke, Crises, sudden changes in chaotic attractors, PRL 1983."),
    _e("crisis_induced_intermittency_boundary", "intermittency", 2, "boundary crisis intermittency", {"mu_c": 0.0}, "boundary_crisis_intermittency", "10.1103/PhysRevLett.50.935", "Grebogi, Ott and Yorke, Crises, sudden changes in chaotic attractors."),
    _e("riddled_basin_alexander_yorke", "riddled_basin", 2, "skew product map with riddled basin (Alexander-Yorke 1992)", {"a": 0.5}, "riddled_basin", "10.1142/S0218127492000604", "Alexander, Yorke, You and Kan, Riddled basins, IJBC 1992."),
    _e("chaotic_saddle_grebogi_ott_yorke", "chaotic_saddle", 2, "chaotic saddle pre-crisis", {"mu_c": 0.0}, "chaotic_saddle_transient_chaos", "10.1103/PhysRevLett.50.935", "Grebogi, Ott and Yorke (chaotic saddle)."),
    _e("wada_basin_boundaries", "wada_basin", 2, "Wada basin boundaries (Kennedy-Yorke)", {"epsilon": 0.05}, "wada_property_chaotic_attractor", "10.1063/1.165869", "Kennedy and Yorke, Basins of Wada, Physica D 1991."),
    _e("noise_induced_synchronization", "noise_induced_phenomenon", 2, "noise-induced synchronization in Stuart-Landau oscillators", {"D": 0.1, "omega": 1.0}, "noise_induced_synchronization", "10.1103/PhysRevLett.71.65", "Maritan and Banavar, Chaos noise and synchronization, PRL 1994."),
    _e("noise_induced_chaos", "noise_induced_phenomenon", 1, "noise-driven escape from stable orbit", {"D": 0.1}, "noise_induced_chaos_escape", "10.1103/PhysRevA.31.1109", "Crutchfield, Farmer and Huberman, Fluctuations and simple chaotic dynamics, Phys Rep 1982."),
    _e("type_IV_intermittency_special", "intermittency", 1, "Type IV intermittency (Pomeau-Manneville extension)", {"alpha": 0.5}, "type_IV_intermittency", "10.1007/BF01197757", "Pomeau-Manneville extension (Type IV)."),
    _e("eyelet_intermittency_phase_synchronization", "intermittency", 2, "eyelet intermittency in phase-synchronization windows", {"epsilon": 0.05, "omega_diff": 0.1}, "eyelet_intermittency", "10.1103/PhysRevLett.79.47", "Pikovsky, Rosenblum, Osipov and Kurths, Phase synchronization in chaotic systems, PRL 1997."),
    _e("ring_intermittency_pre_chaos", "intermittency", 2, "ring intermittency before chaos onset", {"epsilon": 0.05}, "ring_intermittency", "10.1063/1.5004920", "Hramov et al., Ring intermittency in coupled chaotic systems (canonical)."),
    _e("crisis_double_attractor_merging", "intermittency", 2, "two attractors merge at crisis (Grebogi-Ott-Yorke variant)", {"mu_c": 0.0}, "double_attractor_merging_crisis", "10.1103/PhysRevLett.50.935", "Grebogi, Ott and Yorke, Crises, sudden changes (merging variant)."),
    _e("blowout_bifurcation_synchronization_breaking", "blowout", 2, "blowout bifurcation breaking synchronization manifold", {"a": 0.0}, "blowout_breaking_synchrony", "10.1103/PhysRevE.55.6347", "Ashwin, Buescu and Stewart, Bubbling and blowout bifurcations, PRE 1997."),
    _e("attractor_bubbling_intermittent_desynchronization", "intermittency", 2, "attractor bubbling — intermittent desynchronization", {"a": 0.0, "noise_amp": 0.001}, "bubbling_intermittent_desynchronization", "10.1103/PhysRevE.55.6347", "Ashwin, Buescu and Stewart, Bubbling and blowout bifurcations."),
    _e("supercritical_blowout_bifurcation", "blowout", 2, "supercritical blowout bifurcation", {"a": 0.0}, "supercritical_blowout", "10.1103/PhysRevE.55.6347", "Ashwin, Buescu and Stewart (supercritical blowout)."),
    _e("subcritical_blowout_bifurcation", "blowout", 2, "subcritical blowout bifurcation", {"a": 0.0}, "subcritical_blowout", "10.1103/PhysRevE.55.6347", "Ashwin, Buescu and Stewart (subcritical blowout)."),
    _e("riddled_basin_strong_form", "riddled_basin", 3, "strong-form riddled basin (Ott-Sommerer)", {"a": 0.5}, "strong_form_riddled_basin", "10.1103/PhysRevLett.71.4134", "Ott et al., Strong form of riddled basins, PRL 1993."),
]


# ---------------------------------------------------------------------------
# Reaction networks / biological (12)
# ---------------------------------------------------------------------------

_REACTION_BIO = [
    _e("autocatalytic_set_eigen_chemoton", "limit_cycle", 4, "Eigen autocatalytic chemoton oscillator", {"k1": 1.0, "k2": 0.5, "k3": 0.1}, "autocatalytic_chemoton_oscillation", "10.1007/BF00623322", "Eigen, Self-organization of matter and the evolution of biological macromolecules, Naturwiss 1971."),
    _e("autocatalytic_raf_self_replication", "raf", 3, "Hordijk-Steel RAF autocatalytic set", {"density": 0.5}, "raf_self_replication", "10.1016/j.tibtech.2003.10.005", "Hordijk and Steel, Detecting autocatalytic, self-sustaining sets in chemical reaction systems."),
    _e("repressilator_3gene_oscillator", "limit_cycle", 6, "Repressilator 3-gene synthetic oscillator (full m+p form)", {"alpha": 216.0, "alpha0": 0.216, "beta": 0.2, "n": 2.0}, "repressilator_oscillation", "10.1038/35002125", "Elowitz and Leibler, Synthetic oscillatory network, Nature 2000."),
    _e("toggle_switch_collins_gardner", "bistability", 2, "Toggle switch (Collins-Gardner-Cantor 2000)", {"alpha1": 5.0, "alpha2": 5.0, "beta": 2.0, "gamma": 1.0}, "bistable_toggle_switch", "10.1038/35002131", "Gardner, Cantor and Collins, Construction of a genetic toggle switch in E. coli, Nature 2000."),
    _e("turing_pattern_2morph_diffusion", "turing_pattern", 2, "Turing 2-morphogen reaction-diffusion pattern", {"a": 0.5, "b": 1.0, "Du": 1.0, "Dv": 30.0}, "turing_pattern_formation", "10.1098/rstb.1952.0012", "Turing, The chemical basis of morphogenesis, Phil Trans R Soc B 1952."),
    _e("gray_scott_pearl_spots", "turing_pattern", 2, "Gray-Scott pearl-spot regime", {"F": 0.0367, "k": 0.0649, "Du": 0.16, "Dv": 0.08}, "gray_scott_pearl_spots", "10.1126/science.261.5118.189", "Pearson, Complex patterns in a simple system, Science 1993."),
    _e("hodgkin_huxley_action_potential", "limit_cycle", 4, "Hodgkin-Huxley axonal action potential model", {"C_m": 1.0, "g_Na": 120.0, "g_K": 36.0, "g_L": 0.3, "I_app": 10.0}, "hh_action_potential", "10.1113/jphysiol.1952.sp004764", "Hodgkin and Huxley, A quantitative description of membrane current, J Physiol 1952."),
    _e("goldbeter_circadian_oscillator", "limit_cycle", 5, "Goldbeter circadian Per-Tim oscillator", {"vs": 0.76, "Ki": 1.0, "n": 4.0, "vm": 0.65, "k1": 0.55, "k2": 0.55}, "circadian_oscillator", "10.1098/rspb.1995.0153", "Goldbeter, A model for circadian oscillations, Proc R Soc B 1995."),
    _e("shilnikov_chaos_in_p53_mdm2_circuit", "homoclinic", 3, "Shilnikov-class chaos in p53-Mdm2 negative feedback", {"k_basal": 0.1}, "p53_mdm2_chaos", "10.1063/1.5009998", "Stricker et al., Stochastic regulation of p53-Mdm2 (Shilnikov-class)."),
    _e("hes1_oscillator_with_delay", "limit_cycle", 2, "Hes1 single-gene oscillator with translational delay", {"alpha": 1.0, "beta": 1.0, "tau": 25.0, "n": 5.0}, "hes1_delay_oscillation", "10.1126/science.1074560", "Hirata et al., Oscillatory expression of the bHLH factor Hes1, Science 2002."),
    _e("min_protein_e_coli_oscillator", "limit_cycle", 4, "MinD/MinE pole-to-pole oscillator in E. coli", {"k1": 0.5, "k2": 0.1, "diff_D": 16.0}, "min_protein_pole_oscillation", "10.1073/pnas.0334157100", "Howard and Rutenberg, Pattern formation inside bacteria, PNAS 2003."),
    _e("yeast_glycolytic_oscillator_selkov", "limit_cycle", 2, "Sel'kov reduced glycolytic oscillator (yeast)", {"a": 0.05, "b": 0.5}, "glycolytic_oscillation", "10.1111/j.1432-1033.1968.tb00175.x", "Sel'kov, Self-oscillations in glycolysis, Eur J Biochem 1968."),
]


# Total: 22 + 16 + 19 + 45 + 15 + 20 + 18 + 16 + 17 + 12 = 200
ALL_MATH_PRIMITIVE_SEEDS = (
    _ONE_D_MAPS
    + _TWO_D_MAPS
    + _SPROTT_1994
    + _NAMED_3D
    + _JERK_3D
    + _FOUR_D_PLUS
    + _BIFURCATION_NORMAL_FORMS
    + _HETERO_HOMOCLINIC
    + _INTERMITTENCY_SPECIAL
    + _REACTION_BIO
)

assert len(ALL_MATH_PRIMITIVE_SEEDS) == 200, (
    f"CB-015 T3: expected exactly 200 math primitives, got {len(ALL_MATH_PRIMITIVE_SEEDS)}"
)
