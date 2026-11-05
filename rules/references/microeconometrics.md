# microeconometrics — reference

Loaded on demand from `rules/microeconometrics.md`. Rules live there; this is the detail
needed to implement them.

## Choosing the estimator

### By identification strategy

| You have | Estimator | Estimand | Main threat |
|---|---|---|---|
| Randomization | OLS with controls | ATE | Attrition, non-compliance |
| Randomized encouragement | IV / 2SLS | LATE (compliers) | Exclusion restriction |
| Panel, time-invariant confounders | Fixed effects | Within-unit ATT | Time-varying confounders |
| Policy change, comparison group | DiD | ATT | Parallel trends |
| Assignment by a cutoff | RD | LATE at cutoff | Manipulation of the running variable |
| Only observables | Matching / IPW / doubly robust | ATE / ATT | Unobserved confounding |
| Dynamic panel | Arellano-Bond / system GMM | — | Instrument proliferation |

### By outcome type

| Outcome | Model | Report |
|---|---|---|
| Continuous, unbounded | OLS | Coefficients |
| Binary | Logit / probit | Average marginal effects |
| Multinomial, unordered | Multinomial logit; conditional logit for alternative-specific | AMEs; check IIA |
| Ordered | Ordered logit/probit | AMEs per category; test proportional odds |
| Count | Poisson → NB if overdispersed | Incidence rate ratios |
| Count with excess zeros | Zero-inflated or hurdle | Decide *which* — they differ in interpretation |
| Corner solution at 0 | Tobit | Marginal effects, conditional and unconditional |
| Non-negative with zeros, ratios | Poisson PML | Robust to distribution; handles zeros |
| Duration | Cox / parametric hazard | Hazard ratios; check proportional hazards |
| Fractional (0–1) | Fractional logit / beta | AMEs |

Multinomial logit assumes **IIA** — independence of irrelevant alternatives. Test it
(Hausman-McFadden); when it fails, use nested logit or mixed/random-parameters logit.

## Diagnostics with thresholds

| Check | Test | Act when |
|---|---|---|
| Weak instrument | First-stage F | F < 10 (rule of thumb); use Anderson-Rubin CIs when weak |
| Overidentification | Hansen J / Sargan | p < 0.05 ⇒ at least one moment invalid |
| Endogeneity | Durbin-Wu-Hausman | p < 0.05 ⇒ OLS inconsistent |
| FE vs RE | Hausman | p < 0.05 ⇒ use FE |
| Overdispersion | Variance vs mean; LR test vs Poisson | Overdispersed ⇒ negative binomial |
| Heteroskedasticity | Breusch-Pagan / White | Use robust SEs regardless — it costs nothing |
| Serial correlation in panels | Wooldridge test | Cluster by unit |
| Spatial autocorrelation | Moran's I on residuals | Significant ⇒ spatial model |
| Multicollinearity | VIF | VIF > 10 — but only a problem for the collinear coefficients |
| Balance (matching) | Standardized diff | \|SMD\| > 0.1 ⇒ imbalanced |
| Common support | Propensity overlap plot | Trim non-overlapping regions |

## Panel data

```
y_it = α_i + λ_t + β·x_it + ε_it
```

- **Within (FE)** — removes `α_i`. Uses only within-unit variation; time-invariant
  regressors are not identified.
- **First differences** — equivalent to FE at `T=2`; preferable when errors are a random
  walk, worse when they are serially uncorrelated.
- **Random effects** — efficient, but requires `E[α_i | x] = 0`.
- **Correlated random effects (Mundlak)** — include unit means of the regressors;
  recovers FE estimates while allowing time-invariant terms.

Cluster at the unit level for serial correlation within units. With few clusters, wild
cluster bootstrap; with a small number of treated clusters, the problem is severe and
inference should be explicitly conservative.

**Dynamic panels.** OLS with a lagged dependent variable and fixed effects is biased
(`O(1/T)`). Arellano-Bond uses lagged levels as instruments for differences; system GMM
adds lagged differences as instruments for levels. Both proliferate instruments — collapse
the instrument set and report the count. More instruments than clusters invalidates the
Hansen test, which then reports a suspiciously perfect p-value near 1.

## Difference-in-differences

Canonical 2×2:

```
y_it = α + β·treat_i + γ·post_t + δ·(treat_i × post_t) + ε_it       δ = ATT
```

Requirements, in order of how often they are the problem:

1. **Parallel trends** — plot an event study with leads and lags. Flat, insignificant
   leads support it; they do not prove it.
2. **No anticipation** — check the periods immediately before treatment.
3. **Stable composition** — units do not enter and leave with treatment.
4. **SUTVA** — no spillover to controls. Spatially adjacent controls frequently violate
   this; see the spatial section.

**Staggered adoption** is where the standard approach breaks. Two-way fixed effects with
heterogeneous treatment effects uses already-treated units as controls, producing
negative weights and possible sign reversal. Use a heterogeneity-robust estimator
(Callaway-Sant'Anna, Sun-Abraham, Borusyak et al., de Chaisemartin-D'Haultfœuille) and
report the weight diagnostic (Goodman-Bacon decomposition).

## Regression discontinuity

```
y_i = α + τ·1[x_i ≥ c] + f(x_i - c) + ε_i        estimated locally around c
```

- Local linear or quadratic; **never** a high-order global polynomial — it produces
  artefacts at the boundary.
- Data-driven bandwidth (Imbens-Kalyanaraman / Calonico-Cattaneo-Titiunik) with bias
  correction and robust CIs.
- **McCrary density test** for manipulation of the running variable.
- Covariate balance at the cutoff; placebo cutoffs away from `c`.
- Fuzzy RD when the cutoff shifts probability rather than determining treatment — it is
  IV with the indicator as instrument.
- Report sensitivity to bandwidth and polynomial order. Results that survive only one
  choice are not results.

## Spatial models

Weights matrix `W`: `w_ij > 0` if `j` is a neighbour of `i`, `w_ii = 0`, usually
row-standardized so each row sums to 1.

| Definition | Use |
|---|---|
| Contiguity (rook/queen) | Administrative regions |
| k-nearest neighbours | Irregular density; guarantees each unit has neighbours |
| Distance band | A meaningful interaction radius exists |
| Inverse distance / kernel | Smooth decay |
| Economic proximity (trade, flows) | When the mechanism is not geographic |

`W` is an assumption. Report results under at least two specifications.

| Model | Equation | When |
|---|---|---|
| **SAR** (lag) | `y = ρWy + Xβ + ε` | Outcome spills over — neighbours' outcomes affect yours |
| **SEM** (error) | `y = Xβ + u`, `u = λWu + ε` | Unobservables correlated across space |
| **SDM** (Durbin) | `y = ρWy + Xβ + WXθ + ε` | Neighbours' *characteristics* matter; safest default |
| **SLX** | `y = Xβ + WXθ + ε` | Spillover in covariates only; OLS-estimable |
| **SAC/SARAR** | Lag + error | Both; weakly identified in practice |

Start from SDM: it nests SAR and SEM, and its restrictions are testable (LM/LR).

**Effect decomposition.** In a SAR/SDM model, `∂y/∂x` is not `β`. The reduced form is
`y = (I - ρW)^-1 (Xβ + WXθ) + ...`, so:

- **Direct** — the average own effect, including feedback through neighbours and back.
- **Indirect (spillover)** — the average effect of a change in one unit on all others.
- **Total** = direct + indirect.

Report all three with inference. Reporting `β` alone from a SAR model is a
misinterpretation of the model you fitted.

Panel extensions add spatial and temporal lags; identification needs the spatial and
temporal dimensions to be separable, which should be argued rather than assumed.

**MAUP** — the modifiable areal unit problem. Results depend on both the scale and the
zoning of aggregation. Test with alternative aggregations; if the conclusion moves, the
conclusion is about the geography, not the phenomenon.
