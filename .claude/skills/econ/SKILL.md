---
name: econ
description: Economic theory and econometrics applied to real decisions — estimator choice,
  identification, macro forecasting, market design, pricing under uncertainty. Use when
  estimating or reviewing an empirical result, choosing between OLS/IV/panel/DiD/RD,
  interpreting coefficients, or judging whether a claim is supportable.
---

# Economics and econometrics

## The two questions that decide everything

**For an estimate: what variation identifies the parameter?** Regression always returns
a number; only the design says whether it means anything. If the answer is "whatever
variation happens to be in the data", the coefficient is a conditional expectation and
must be reported as one.

**For a model: which assumption is load-bearing?** Primitives first — agents, actions,
information, preferences, technology, timing. Then separate the assumption that
produces the result from the ones that make the algebra tractable. A conclusion is only
as portable as its load-bearing assumption.

Everything below is downstream of those two.

## Route

| Question | Pack |
|---|---|
| Is this regression inference or prediction; which SEs; which penalty | `rules/regression.md` |
| Does this identify a causal effect — panel, DiD, RD, IV, matching | `rules/microeconometrics.md` |
| Units interact across space | `rules/microeconometrics.md` (spatial) |
| Time series, unit roots, cointegration, volatility | `rules/econometrics.md` |
| Macro forecasting, nowcasting, shock identification, cycle measurement | `rules/macroeconomics.md` |
| Choice, duality, welfare, market structure | `rules/microeconomics.md` |
| Pricing under uncertainty, SDF, no-arbitrage, incomplete markets | `rules/microeconomics.md` ref §7 |
| Auctions, mechanism design, matching, strategic pricing | `rules/game-theory.md` |
| Mispricing, limits to arbitrage, anomaly decay | `rules/behavioral-finance.md` |
| Turning any of it into positions | `/quant` |

Load the pack. Load `rules/references/<id>.md` only when you need the formula, the
threshold, or the code.

## Estimator selection

| Situation | Approach |
|---|---|
| Prediction is the goal | `regression` — regularize, cross-validate with the pipeline inside the fold, benchmark out of sample |
| Cross-section, believe conditional independence | OLS + robust SEs; sign the OVB you cannot rule out |
| Endogenous regressor, plausible instrument | IV/2SLS — first-stage F ≥ 10, argue exclusion; the estimand is a complier LATE |
| Repeated observations per unit | Panel FE; cluster at the assignment level |
| Policy change with a comparison group | DiD — parallel-trends evidence; heterogeneity-robust estimator if timing is staggered |
| Assignment by a cutoff | RD — local polynomial, density and balance tests, bandwidth sensitivity |
| Bounded, count, or censored outcome | Model the support; report marginal effects |
| One series over time | Unit roots before anything; spurious regression is the default failure |
| Many correlated series | Factor model rather than variable selection |

## Reporting

Give the **estimand, the identifying assumption, the sample, and the standard-error
choice** — in that order, before the coefficient. A number without those four is not
interpretable, and stating them is what separates an estimate from an output.

For non-linear or interacted models, report marginal effects at stated values. Report
intervals and effect sizes rather than p-values: at large `n` almost everything is
significant, and the question is whether the magnitude matters.

For any forecast, report the naive benchmark alongside it. A model that does not beat a
random walk out of sample has not been shown to do anything.

## Common failures worth checking first

| Symptom | Likely cause |
|---|---|
| Beautiful in-sample fit, useless live | Fitting in sample; leakage in preprocessing; latest-vintage data |
| Coefficient flips when a control is added | Collinearity, or the control is post-treatment |
| Significant everywhere | Large `n`; report magnitudes |
| Two trending series strongly related | Spurious regression — check cointegration |
| Standard errors implausibly small | Not clustered at the assignment level |
| Result only in one specification | It is a result about that specification |
| Macro backtest that stopped working | Revisions — the backtest used data nobody had |
