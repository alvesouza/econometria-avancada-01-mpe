---
tags: [map, cross-reference]
date: 2026-10-19
---

# Books Index

Printed page numbers. Page offsets (printed = PDF page − k): MHE k=16 (2008 pre-publication draft), Tsay k=27, Wooldridge 6e k=24, ISLR k=15→10 (varies by chapter). Greenberg 1e k=15 (substitute for the 2e named in the syllabus; see [[Livros/BOOKS]]).

# Angrist & Pischke, Mostly Harmless Econometrics (2009)
#book/mhe
> Link: [[Livros/Joshua D. Angrist, Jorn-Steffen Pischke-Mostly Harmless Econometrics_ An Empiricist's Companion (2008)|MHE]]
> Page numbers are the printed page numbers of the course PDF (a 2008 pre-publication edition). Printed page = PDF page − 16. Pagination may differ from the 2009 Princeton UP printing.

## Ch. 1 — Questions about Questions
**Pages:** pp. 3–7
**Subtopics:**
- Four FAQs: every research project should state the causal relationship of interest, the ideal experiment, the identification strategy and the mode of statistical inference (p. 3).
- Ideal experiment: describing the hypothetical randomized trial clarifies which forces are being manipulated and which are held fixed (pp. 4–5).
- FUQ'd questions: "fundamentally unidentified questions" that no experiment could answer, e.g. the effect of school start age on test scores (p. 5).
- Identification strategy and natural experiments: observational data are used to approximate the ideal experiment, e.g. quarter of birth as a source of variation in schooling (p. 6).
- Mode of inference: population, sample and assumptions behind standard errors, with robust standard errors as the default (p. 6).
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]

## Ch. 2 — The Experimental Ideal
**Pages:** pp. 9–18
### §2.1 — The Selection Problem (pp. 10–11)
**Subtopics:**
- Potential outcomes: y1i and y0i, the individual causal effect y1i − y0i, and the observed outcome yi = y0i + (y1i − y0i)di (Neyman–Rubin framework).
- Hospital allegory: a naive comparison of hospitalized and non-hospitalized people mixes the causal effect with differences in baseline health.
- Selection bias decomposition: the observed difference in means = average treatment effect on the treated + selection bias, E[y0i|di=1] − E[y0i|di=0].
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
### §2.2 — Random Assignment Solves the Selection Problem (pp. 12–15)
**Subtopics:**
- Randomization: independence of di from potential outcomes makes selection bias zero, so the difference in means equals the ATE (= TOT).
- Training programs and selection: Ashenfelter-style evidence that trainees are negatively selected, which motivates experiments.
- Tennessee STAR: covariate balance checks (Table 2.2.1) and experimental class-size effects (Table 2.2.2).
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
### §2.3 — Regression Analysis of Experiments (pp. 16–18)
**Subtopics:**
- Regression form of a treatment-control comparison: yi = α + ρdi + ηi, where selection bias = correlation between ηi and di.
- Covariates in experiments: controls are not needed for unbiasedness but can raise precision; adding them should leave ρ roughly unchanged when assignment is random.
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]

## Ch. 3 — Making Regression Make Sense
**Pages:** pp. 21–82
### §3.1 — Regression Fundamentals (pp. 22–37)
#### §3.1.1 — Economic Relationships and the Conditional Expectation Function (pp. 23–25)
**Subtopics:**
- CEF: E[yi|Xi] as the population summary of how yi changes with Xi; law of iterated expectations (Figure 3.1.1, the schooling–wage CEF).
- CEF decomposition property (Theorem 3.1.1): yi = E[yi|Xi] + εi, with εi mean-independent of Xi.
- CEF prediction property (Theorem 3.1.2): the CEF is the minimum-MSE predictor of yi given Xi.
- ANOVA theorem (Theorem 3.1.3): V(yi) = V(E[yi|Xi]) + E[V(yi|Xi)].
#### §3.1.2 — Linear Regression and the CEF (pp. 26–29)
**Subtopics:**
- Population regression coefficient β = E[XiXi']⁻¹E[Xiyi], and regression anatomy (Frisch–Waugh): βk = Cov(yi, x̃ki)/V(x̃ki).
- Linear CEF theorem (Theorem 3.1.4): if the CEF is linear (e.g. joint normality or a saturated model), regression is the CEF.
- Best linear predictor theorem (Theorem 3.1.5): Xi'β is the best linear predictor of yi.
- Regression-CEF theorem (Theorem 3.1.6): Xi'β is the minimum-MSE linear approximation to the CEF (Figure 3.1.2).
#### §3.1.3 — Asymptotic OLS Inference (pp. 30–35)
**Subtopics:**
- Sampling distribution of OLS: law of large numbers, central limit theorem, Slutsky's theorem and continuous mapping applied to β̂.
- Sandwich (heteroskedasticity-consistent / robust) variance versus the conventional homoskedastic formula.
- Delta method for standard errors of nonlinear functions of β̂.
- Grouped-data regression: weighted regression on cell means reproduces the micro-data coefficient (Figure 3.1.3).
- Linear probability model: residuals are necessarily heteroskedastic; robust standard errors that are smaller than conventional ones are a warning sign.
#### §3.1.4 — Saturated Models, Main Effects, and Other Regression Talk (pp. 36–37)
**Subtopics:**
- Saturated model: one parameter per value of the regressors, so the CEF is linear.
- Main effects versus interactions: a hierarchy running from the saturated model down to main-effects-only specifications.
### §3.2 — Regression and Causality (pp. 38–50)
#### §3.2.1 — The Conditional Independence Assumption (pp. 38–43)
**Subtopics:**
- CIA / selection on observables: {y0i, y1i} ⊥ di | Xi, so selection bias disappears conditional on covariates.
- Causal regression model: under the CIA plus a constant-effects linear model, the regression coefficient on si is causal.
- Discrete averaging: a regression with a multi-valued treatment yields a weighted average of unit causal effects.
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
#### §3.2.2 — The Omitted Variables Bias Formula (pp. 44–46)
**Subtopics:**
- OVB formula: short-regression coefficient = long coefficient + (effect of omitted variable) × (regression of omitted on included); "short equals long plus the effect of omitted times the regression of omitted on included".
- Link to regression anatomy; returns-to-schooling estimates with increasing sets of controls (Table 3.2.1, NLSY).
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
#### §3.2.3 — Bad Control (pp. 47–50)
**Subtopics:**
- Bad control: controlling for an outcome of the treatment (e.g. occupation when estimating returns to college) brings in a subtle form of selection bias.
- Proxy control: controlling for a variable measured after treatment, such as a late test score proxying for ability, also biases the coefficient, though it may beat no control at all.
- Timing rule: good controls are fixed before the treatment is determined.
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
### §3.3 — Heterogeneity and Nonlinearity (pp. 51–65)
#### §3.3.1 — Regression Meets Matching (pp. 51–58)
**Subtopics:**
- Matching estimands: under the CIA, TOT and ATE are covariate-cell-weighted averages of within-cell treatment–control differences.
- Regression as variance-weighted matching: a regression saturated in Xi weights cell effects by the conditional variance of treatment, P(1−P), while matching weights them by treated shares (Table 3.3.1, voluntary military service).
- Common support and approximate matching bias (Abadie–Imbens).
- Average derivative interpretation of regression with an ordered or continuous treatment.
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
#### §3.3.2 — Control for Covariates Using the Propensity Score (pp. 59–62)
**Subtopics:**
- Propensity-score theorem (Theorem 3.3.1): if the CIA holds given Xi, it holds given p(Xi).
- Propensity-score estimators: weighting (Horvitz–Thompson style) and matching or stratification on the estimated score.
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
#### §3.3.3 — Propensity-Score Methods vs. Regression (pp. 63–65)
**Subtopics:**
- When the covariate model is flexible, regression and propensity-score methods give similar answers; the key issue is the choice of controls, not the method.
- NSW / Dehejia–Wahba replication: covariate means and regression estimates with CPS and PSID comparison groups (Tables 3.3.2–3.3.3); the role of lagged earnings and the Ashenfelter dip.
### §3.4 — Regression Details (pp. 66–80)
#### §3.4.1 — Weighting Regression (pp. 66–68)
**Subtopics:**
- Sampling weights versus GLS/precision weights: weight to estimate a population-average estimand; weighting to fix heteroskedasticity is rarely worth it; compare weighted and unweighted results.
#### §3.4.2 — Limited Dependent Variables and Marginal Effects (pp. 69–79)
**Subtopics:**
- Regression on LDVs: the linear probability model approximates the CEF and its marginal effects; with a saturated or dummy treatment it is exact.
- Good COP, bad COP: conditional-on-positive effects mix a causal effect with selection bias (RAND Health Insurance Experiment, Table 3.4.1).
- Tobit and latent-index models: they target latent-variable effects; this is useful only when the data are truly censored.
- Probit/Tobit marginal effects are usually close to OLS estimates (Table 3.4.2, childbearing and female labor supply).
#### §3.4.3 — Why is Regression Called Regression and What Does Regression-to-the-mean Mean? (p. 80)
**Subtopics:**
- Galton's regression to the mean: with stationary variances, the regression slope is a correlation coefficient below one.
### §3.5 — Appendix: Derivation of the average derivative formula (pp. 81–82)
**Subtopics:**
- Average derivative formula: the regression slope on a continuous regressor is a weighted average of CEF derivatives.

## Ch. 4 — Instrumental Variables in Action: Sometimes You Get What You Need
**Pages:** pp. 83–163
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §4.1 — IV and causality (pp. 84–102)
**Subtopics:**
- IV setup: a constant-effects causal model with an omitted confounder (ability) and an instrument correlated with schooling but excluded from the outcome equation.
- First stage, reduced form, and IV = reduced form / first stage (indirect least squares); quarter-of-birth graphs (Figure 4.1.1).
- Measurement error motive: IV corrects attenuation bias from classical measurement error.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
#### §4.1.1 — Two-Stage Least Squares (pp. 89–93)
**Subtopics:**
- 2SLS: regress the outcome on first-stage fitted values plus covariates; the second-stage standard errors must be corrected; 2SLS as an IV estimator with fitted values as the instrument.
- Multiple instruments and covariates: QOB × year-of-birth interactions; 2SLS returns to schooling (Table 4.1.1).
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
#### §4.1.2 — The Wald Estimator (pp. 94–99)
**Subtopics:**
- Wald estimator: with a binary instrument, IV = (difference in outcome means)/(difference in treatment means); also the classic grouping fix for errors in variables.
- Applications: QOB returns to schooling (Table 4.1.2), the Vietnam draft lottery and veteran earnings (Table 4.1.3), twins and sibling sex composition for family size (Table 4.1.4).
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
#### §4.1.3 — Grouped Data and 2SLS (pp. 100–102)
**Subtopics:**
- Wald as the "mother of all IV estimators": 2SLS with dummy instruments = GLS on group means = the efficient linear combination of Wald estimators.
- Visual IV (VIV): plot grouped outcome means against grouped treatment means (Figure 4.1.2, draft lottery).
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §4.2 — Asymptotic 2SLS Inference (pp. 103–108)
#### §4.2.1 — The Limiting Distribution of the 2SLS Coefficient Vector (pp. 103–104)
**Subtopics:**
- 2SLS asymptotic distribution: robust (sandwich) and homoskedastic covariance matrices; residuals computed with the original regressors, not the first-stage fitted values.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
#### §4.2.2 — Over-identification and the 2SLS Minimand (pp. 105–108)
**Subtopics:**
- 2SLS minimand / GMM: 2SLS minimizes a quadratic form in sample moments.
- Over-identification test (Sargan/Hansen J): N × R² from regressing 2SLS residuals on instruments; chi-square with q − k degrees of freedom; it tests whether different Wald estimators agree.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §4.3 — Two-Sample IV and Split-Sample IV (pp. 109–110)
**Subtopics:**
- TSIV: estimate the reduced form and the first stage in different samples drawn from the same population (Angrist–Krueger).
- Split-sample IV (SSIV/USSIV): a first stage estimated in one half of the sample reduces the finite-sample bias of 2SLS.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §4.4 — IV with Heterogeneous Potential Outcomes (pp. 111–129)
#### §4.4.1 — Local Average Treatment Effects (pp. 112–116)
**Subtopics:**
- Potential treatments d1i, d0i and the double-indexed outcomes yi(d, z).
- LATE theorem (Theorem 4.4.1): under independence (A1), exclusion (A2), a first stage (A3) and Imbens–Angrist monotonicity (A4), Wald = E[y1i − y0i | d1i > d0i].
- Defiers break the link between LATE and the reduced form; a zero reduced form is not proof of a zero effect.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
#### §4.4.2 — The Compliant Subpopulation (pp. 117–118)
**Subtopics:**
- Compliers, always-takers and never-takers; TOT is a weighted average of effects on always-takers and compliers; the effect on the untreated mixes never-takers and compliers.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
#### §4.4.3 — IV in Randomized Trials (pp. 119–122)
**Subtopics:**
- Non-compliance; intention-to-treat (ITT) as the reduced form; ITT / compliance difference as the IV estimate (JTPA, Table 4.4.1).
- Bloom result (Theorem 4.4.2): with one-sided non-compliance (no always-takers), IV = effect of treatment on the treated.
- Minneapolis Domestic Violence Experiment: the flip side, with no never-takers.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
#### §4.4.4 — Counting and Characterizing Compliers (pp. 123–129)
**Subtopics:**
- Complier share = first stage; complier share of the treated and untreated (Table 4.4.2).
- Complier characteristics ratios: the relative likelihood that compliers have a given covariate (Table 4.4.3, twins vs. sex-composition instruments); external validity.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §4.5 — Generalizing LATE (pp. 130–140)
#### §4.5.1 — LATE with Multiple Instruments (p. 130)
**Subtopics:**
- 2SLS with several instruments is a weighted average of instrument-specific LATEs, with weights tied to first-stage strength.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
#### §4.5.2 — Covariates in the Heterogeneous-effects Model (pp. 131–135)
**Subtopics:**
- Saturate and weight (Theorem 4.5.1): 2SLS with saturated covariates and a saturated first stage is a weighted average of covariate-specific LATEs.
- Abadie kappa (Theorem 4.5.2): kappa weighting identifies any complier characteristic or complier causal response function.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
#### §4.5.3 — Average Causal Response with Variable Treatment Intensity (pp. 136–140)
**Subtopics:**
- Average causal response (ACR) theorem (Theorem 4.5.3): with a multi-valued treatment, Wald = a weighted average of unit causal effects, weighted by P(s1i ≥ j > s0i).
- Compulsory schooling instruments (Figure 4.5.1); the continuous-treatment analogue as a weighted average derivative (supply/demand with a weather instrument).
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §4.6 — IV Details (pp. 141–159)
#### §4.6.1 — 2SLS Mistakes (pp. 141–143)
**Subtopics:**
- Manual 2SLS gives wrong standard errors; covariates must appear in both stages.
- Forbidden regression: plugging nonlinear first-stage fitted values (probit, squares) into the second stage is inconsistent; use them as instruments instead.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
#### §4.6.2 — Peer Effects (pp. 144–146)
**Subtopics:**
- External returns: group averages of individual characteristics (e.g. state average schooling), instrumented with group-level instruments; measurement error can produce spurious external returns.
- Reflection problem / bad peer regressions: regressing own outcomes on peer-average outcomes is mechanically biased; use ex ante peer characteristics instead (Angrist–Lang busing).
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
#### §4.6.3 — Limited Dependent Variables Reprise (pp. 147–152)
**Subtopics:**
- With a binary endogenous treatment or outcome, 2SLS identifies LATE; bivariate probit relies on functional form; the Abadie kappa approach gives complier marginal effects (Table 4.6.1, third child and female labor supply).
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
#### §4.6.4 — The Bias of 2SLS (pp. 153–159)
**Subtopics:**
- Weak instruments: 2SLS is biased towards OLS; the approximate bias is inversely proportional to the population first-stage F (concentration parameter); many weak instruments worsen it.
- Just-identified IV is approximately median-unbiased; LIML is approximately median-unbiased with over-identification (Monte Carlo evidence, Figures 4.6.1–4.6.3).
- Practical checklist: report the first stage and its F (Stock–Yogo, F > 10 rule of thumb), pick the best single instrument, compare with LIML, and inspect the reduced form; Bound–Jaeger–Baker critique of QOB (Table 4.6.2).
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §4.7 — Appendix (pp. 160–163)
**Subtopics:**
- Derivation of the approximate bias of 2SLS, and how to compute the first-stage F for excluded instruments with multiple endogenous variables.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]

## Ch. 5 — Parallel Worlds: Fixed Effects, Differences-in-differences, and Panel Data
**Pages:** pp. 165–185
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
### §5.1 — Individual Fixed Effects (pp. 165–168)
**Subtopics:**
- Fixed-effects causal model: the CIA holds conditional on time-invariant unobserved αi; the within estimator (deviations from means) versus first differences, which coincide with T = 2.
- Incidental parameters problem: dummy-variable estimation of the FE model is equivalent to the within estimator for the slope coefficients.
- Union wage effects: cross-section versus panel fixed-effects estimates (Table 5.1.1).
- Measurement error is amplified by FE/differencing (attenuation bias); fixes include IV with repeated measures (twins, Ashenfelter–Krueger).
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §5.2 — Differences-in-differences: Pre and Post, Treatment and Control (pp. 169–181)
**Subtopics:**
- DiD in potential outcomes with state and time effects; the common trends (parallel trends) assumption and its scale dependence (logs vs. levels).
- Card–Krueger New Jersey minimum wage (Table 5.2.1, Figures 5.2.1–5.2.2); checking common trends with multiple periods (Pischke 2007, Figure 5.2.3).
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
#### §5.2.1 — Regression DD (pp. 174–181)
**Subtopics:**
- Regression DD: the saturated 2×2 model with treatment dummy, post dummy and their interaction; extension to many states and periods with state and year effects and continuous treatment intensity (Card 1992, Table 5.2.2).
- Granger-type causality test: leads and lags of treatment (Autor 2003, Figure 5.2.4).
- State-specific linear trends as a robustness check (Besley–Burgess, Table 5.2.3).
- Group-level shocks and inference concerns (see Ch. 8); triple differences (DDD).
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
### §5.3 — Fixed Effects versus Lagged Dependent Variables (pp. 182–183)
**Subtopics:**
- Lagged-dependent-variable model (CIA conditional on yit−1, e.g. the Ashenfelter dip) versus the fixed-effects model; the two are not nested.
- Nickell bias from combining FE and lagged outcomes in short panels; Arellano–Bond-type GMM fixes.
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
### §5.4 — Appendix: More on fixed effects and lagged dependent variables (pp. 184–185)
**Subtopics:**
- Bracketing property: if one model is correct, FE and lagged-dependent-variable estimates bound the true effect from opposite sides.
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]

## Ch. 6 — Getting a Little Jumpy: Regression Discontinuity Designs  #background
**Pages:** pp. 189–202
### §6.1 — Sharp RD (pp. 189–195)
- background: treatment is a deterministic function of a running variable; parametric/polynomial and nonparametric (local) estimation; Lee (2008) incumbency.
### §6.2 — Fuzzy RD is IV (pp. 196–202)
- background: a jump in the treatment probability at the cutoff used as an instrument; Angrist–Lavy Maimonides rule (Figure 6.2.1, Table 6.2.1).

## Ch. 7 — Quantile Regression  #background
**Pages:** pp. 203–220
### §7.1 — The Quantile Regression Model (pp. 204–213)
- background: check-function minimand, schooling coefficients across quantiles (Table 7.1.1); §7.1.1 censored QR (pp. 208–209); §7.1.2 QR approximation property, Theorem 7.1.1 (pp. 210–212); §7.1.3 tricky points (p. 213).
### §7.2 — Quantile Treatment Effects (pp. 214–220)
- background: §7.2.1 QTE estimator via Abadie-kappa-weighted QR (pp. 216–220); JTPA (Table 7.2.1).

## Ch. 8 — Nonstandard Standard Error Issues  #background
**Pages:** pp. 221–244
### §8.1 — The Bias of Robust Standard Errors (pp. 222–230)
- background: small-sample bias of HC0, HC1–HC3 alternatives, Monte Carlo (Table 8.1.1).
### §8.2 — Clustering and Serial Correlation in Panels (pp. 231–240)
- background: §8.2.1 Moulton factor and clustering (pp. 231–235, Table 8.2.1 STAR); §8.2.2 serial correlation in panels and DiD (pp. 236–237); §8.2.3 fewer than 42 clusters (pp. 238–240).
### §8.3 — Appendix: Derivation of the simple Moulton factor (pp. 241–242)
- background: derivation of the Moulton factor.


# Wooldridge, Introductory Econometrics, 6e
#book/wooldridge
> Link: [[Livros/Wooldridge J.M-Introductory econometrics. A modern approach-Cengage Learning (2016)|Wooldridge 6e]]
> Page numbers are printed book pages. PDF page index (0-based) = printed page + 23 (printed p. 1 = PDF page 25 in a 1-based viewer).

## Ch. 1 — The Nature of Econometrics and Economic Data
#background
**Pages:** pp. 1–18
### §1.1 — What is Econometrics? (pp. 1–2)
**Subtopics:**
- scope: econometrics as statistical methods for estimating economic relationships, testing theories, forecasting and evaluating policy with nonexperimental data.
### §1.2 — Steps in Empirical Economic Analysis (pp. 2–5)
**Subtopics:**
- economic vs econometric model: moving from a theoretical model to an estimable equation with an error term.
### §1.3 — The Structure of Economic Data (pp. 5–10)
**Subtopics:**
- data types: cross-sectional, time series, pooled cross sections and panel/longitudinal data.
### §1.4 — Causality and the Notion of Ceteris Paribus in Econometric Analysis (pp. 10–14)
**Subtopics:**
- ceteris paribus: causal effects as effects holding other factors fixed; counterfactual reasoning and why experiments are rarely available.
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]

## Ch. 2 — The Simple Regression Model
#background
**Pages:** pp. 20–59
### §2.1 — Definition of the Simple Regression Model (pp. 20–24)
**Subtopics:**
- zero conditional mean: E(u|x)=0 and the population regression function.
### §2.2 — Deriving the Ordinary Least Squares Estimates (pp. 24–32)
**Subtopics:**
- OLS: method-of-moments / least-squares derivation of slope and intercept.
### §2.3 — Properties of OLS on Any Sample of Data (pp. 32–36)
**Subtopics:**
- algebraic properties: residuals sum to zero, SST = SSE + SSR, R-squared.
### §2.4 — Units of Measurement and Functional Form (pp. 36–40)
**Subtopics:**
- functional form: rescaling, log-level, level-log and log-log (elasticity) models.
### §2.5 — Expected Values and Variances of the OLS Estimators (pp. 40–50)
**Subtopics:**
- SLR.1–SLR.5: unbiasedness theorem, sampling variance, estimating the error variance.
### §2.6 — Regression through the Origin and Regression on a Constant (pp. 50–51)
**Subtopics:**
- no-intercept regression: bias when the true intercept is nonzero.

## Ch. 3 — Multiple Regression Analysis: Estimation
#background
**Pages:** pp. 60–104
### §3.1 — Motivation for Multiple Regression (pp. 61–64)
**Subtopics:**
- controls: holding other factors fixed explicitly.
### §3.2 — Mechanics and Interpretation of Ordinary Least Squares (pp. 64–73)
**Subtopics:**
- partialling out: Frisch–Waugh interpretation, goodness of fit.
### §3.3 — The Expected Value of the OLS Estimators (pp. 73–81)
**Subtopics:**
- MLR.1–MLR.4, unbiasedness, omitted variable bias formula.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §3.4 — The Variance of the OLS Estimators (pp. 81–89)
**Subtopics:**
- sampling variance: R_j^2, multicollinearity, VIF, misspecified models.
### §3.5 — Efficiency of OLS: The Gauss-Markov Theorem (pp. 89–90)
**Subtopics:**
- Gauss–Markov theorem: OLS is BLUE under MLR.1–MLR.5.
### §3.6 — Some Comments on the Language of Multiple Regression Analysis (pp. 90–91)
**Subtopics:**
- terminology: estimator vs model distinction.

## Ch. 4 — Multiple Regression Analysis: Inference
#background
**Pages:** pp. 105–148
### §4.1 — Sampling Distributions of the OLS Estimators (pp. 105–108)
**Subtopics:**
- classical linear model: normality assumption MLR.6 and exact normal sampling distributions.
### §4.2 — Testing Hypotheses about a Single Population Parameter: The t Test (pp. 108–122)
**Subtopics:**
- t test: one- and two-sided alternatives, p-values, economic vs statistical significance.
### §4.3 — Confidence Intervals (pp. 122–124)
**Subtopics:**
- confidence intervals for a single coefficient.
### §4.4 — Testing Hypotheses about a Single Linear Combination of the Parameters (pp. 124–127)
**Subtopics:**
- linear combinations: reparametrization trick for testing β1 = β2.
### §4.5 — Testing Multiple Linear Restrictions: The F Test (pp. 127–137)
**Subtopics:**
- F test: exclusion restrictions, R-squared form, overall significance, general linear restrictions.
### §4.6 — Reporting Regression Results (pp. 137–139)
**Subtopics:**
- reporting: tables and standard errors.

## Ch. 5 — Multiple Regression Analysis: OLS Asymptotics
#background
**Pages:** pp. 149–165
### §5.1 — Consistency (pp. 150–154)
**Subtopics:**
- consistency of OLS under MLR.4′ (zero correlation); inconsistency (asymptotic bias) formula.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §5.2 — Asymptotic Normality and Large Sample Inference (pp. 154–161)
**Subtopics:**
- asymptotic normality theorem; LM (n·R²) statistic.
### §5.3 — Asymptotic Efficiency of OLS (pp. 161–162)
**Subtopics:**
- OLS asymptotically efficient among a class of estimators under Gauss–Markov.

## Ch. 6 — Multiple Regression Analysis: Further Issues
#background
**Pages:** pp. 166–204
### §6.1 — Effects of Data Scaling on OLS Statistics (pp. 166–171)
**Subtopics:**
- scaling and beta (standardized) coefficients.
### §6.2 — More on Functional Form (pp. 171–180)
**Subtopics:**
- logs, quadratics, interaction terms, average partial effects.
### §6.3 — More on Goodness-of-Fit and Selection of Regressors (pp. 180–186)
**Subtopics:**
- adjusted R-squared, nonnested model choice, over-controlling.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
### §6.4 — Prediction and Residual Analysis (pp. 186–194)
**Subtopics:**
- prediction intervals, residual analysis, predicting y when log(y) is the dependent variable.

## Ch. 7 — Multiple Regression Analysis with Qualitative Information: Binary (or Dummy) Variables
#background
**Pages:** pp. 205–242
### §7.1 — Describing Qualitative Information (pp. 205–206)
**Subtopics:**
- binary (dummy) variables.
### §7.2 — A Single Dummy Independent Variable (pp. 206–212)
**Subtopics:**
- intercept shifts; log dependent variable interpretation.
### §7.3 — Using Dummy Variables for Multiple Categories (pp. 212–217)
**Subtopics:**
- base group, dummy variable trap, ordinal information.
### §7.4 — Interactions Involving Dummy Variables (pp. 217–224)
**Subtopics:**
- slope differences; Chow test for differences across groups.
### §7.5 — A Binary Dependent Variable: The Linear Probability Model (pp. 224–229)
**Subtopics:**
- LPM: response probabilities, shortcomings (predictions outside [0,1], heteroskedasticity).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
### §7.6 — More on Policy Analysis and Program Evaluation (pp. 229–231)
**Subtopics:**
- program evaluation: control vs treatment groups, self-selection problem.
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
### §7.7 — Interpreting Regression Results with Discrete Dependent Variables (pp. 231–232)
**Subtopics:**
- interpreting coefficients when y is discrete (counts, averages).

## Ch. 8 — Heteroskedasticity
#background
**Pages:** pp. 243–273
### §8.1 — Consequences of Heteroskedasticity for OLS (pp. 243–244)
**Subtopics:**
- OLS still unbiased/consistent; usual standard errors invalid.
### §8.2 — Heteroskedasticity-Robust Inference after OLS Estimation (pp. 244–250)
**Subtopics:**
- White robust standard errors, robust F and LM statistics.
### §8.3 — Testing for Heteroskedasticity (pp. 250–254)
**Subtopics:**
- Breusch–Pagan test and White test (special form).
### §8.4 — Weighted Least Squares Estimation (pp. 254–265)
**Subtopics:**
- WLS / GLS with known heteroskedasticity form; feasible GLS.
### §8.5 — The Linear Probability Model Revisited (pp. 265–267)
**Subtopics:**
- WLS for the LPM.

## Ch. 9 — More on Specification and Data Issues
#topic/endogeneity-iv #topic/potential-outcomes
**Pages:** pp. 274–310
### §9.1 — Functional Form Misspecification (pp. 275–279)
**Subtopics:**
- functional form misspecification: omitted nonlinearities as a source of bias in the partial effects.
- RESET (9-1a): Ramsey's regression specification error test adding ŷ² and ŷ³, an F/LM test of functional form.
- nonnested alternatives (9-1b): Mizon–Richard encompassing test and Davidson–MacKinnon test for comparing nonnested models.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §9.2 — Using Proxy Variables for Unobserved Explanatory Variables (pp. 279–285)
**Subtopics:**
- plug-in solution to omitted variables: proxy variable assumptions (redundancy and the omitted variable uncorrelated with x given the proxy); IQ as proxy for ability.
- imperfect proxies: remaining bias when the proxy assumptions fail.
- lagged dependent variables as proxies (9-2a): controlling for historical factors that cause current differences.
- a different slant on multiple regression (9-2b): interpreting coefficients relative to the controls included.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §9.3 — Models with Random Slopes (pp. 285–287)
**Subtopics:**
- random coefficient model: OLS estimates the average partial effect (APE) when slopes are independent of x; induced heteroskedasticity.
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
### §9.4 — Properties of OLS under Measurement Error (pp. 287–293)
**Subtopics:**
- measurement error in the dependent variable (9-4a): OLS unbiased/consistent if the error is uncorrelated with regressors, only larger variance.
- measurement error in an explanatory variable (9-4b): classical errors-in-variables (CEV) assumption, attenuation bias plim β̂1 = β1·σ²x*/(σ²x*+σ²e); bias spreads to other coefficients in multiple regression.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §9.5 — Missing Data, Nonrandom Samples, and Outlying Observations (pp. 293–300)
**Subtopics:**
- missing data (9-5a): missing completely at random keeps OLS consistent; missing-data indicator method.
- nonrandom samples (9-5b): exogenous sample selection (on x) is harmless; endogenous sample selection (on y or u) biases OLS; stratified sampling.
- outliers and influential observations (9-5c): studentized residuals, sensitivity of OLS to extreme observations.
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
### §9.6 — Least Absolute Deviations Estimation (pp. 300–302)
**Subtopics:**
- LAD: estimates the conditional median; robust to outliers; differs from OLS unless the conditional distribution is symmetric.

## Ch. 10 — Basic Regression Analysis with Time Series Data
#topic/arima-unit-roots
**Pages:** pp. 312–343
### §10.1 — The Nature of Time Series Data (pp. 312–313)
**Subtopics:**
- stochastic process: a time series as one realization; temporal ordering.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
### §10.2 — Examples of Time Series Regression Models (pp. 313–317)
**Subtopics:**
- static models (10-2a): contemporaneous relationships (static Phillips curve).
- finite distributed lag models (10-2b): impact propensity, lag distribution and long-run propensity (LRP).
- a convention about the time index (10-2c).
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
### §10.3 — Finite Sample Properties of OLS under Classical Assumptions (pp. 317–323)
**Subtopics:**
- unbiasedness of OLS (10-3a): TS.1–TS.3, strict exogeneity E(u_t|X)=0 rules out feedback.
- variances and Gauss–Markov (10-3b): TS.4 homoskedasticity and TS.5 no serial correlation; OLS is BLUE.
- inference under the CLM (10-3c): TS.6 normality gives exact t and F tests.
### §10.4 — Functional Form, Dummy Variables, and Index Numbers (pp. 323–329)
**Subtopics:**
- logs and dummies in time series; event studies; index numbers, base periods and real vs nominal values.
### §10.5 — Trends and Seasonality (pp. 329–338)
**Subtopics:**
- trending series (10-5a): linear and exponential trends.
- trending variables in regression (10-5b): spurious relationships from common trends; include a time trend.
- detrending interpretation (10-5c): Frisch–Waugh view of including t.
- R-squared with trending dependent variable (10-5d): detrended R-squared.
- seasonality (10-5e): seasonal dummies and deseasonalizing.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

## Ch. 11 — Further Issues in Using OLS with Time Series Data
#topic/arima-unit-roots
**Pages:** pp. 344–371
### §11.1 — Stationary and Weakly Dependent Time Series (pp. 345–348)
**Subtopics:**
- stationarity (11-1a): strict vs covariance (weak) stationarity.
- weak dependence (11-1b): asymptotically uncorrelated series; MA(1) and stable AR(1) (|ρ1|<1) examples; trend-stationary processes.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
### §11.2 — Asymptotic Properties of OLS (pp. 348–354)
**Subtopics:**
- TS.1′–TS.5′: consistency under contemporaneous exogeneity with stationary, weakly dependent data; asymptotic normality; models with lagged dependent variables; efficient markets hypothesis example.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
### §11.3 — Using Highly Persistent Time Series in Regression Analysis (pp. 354–360)
**Subtopics:**
- highly persistent series (11-3a): random walk (unit root), random walk with drift; variance grows with t, shocks persist.
- transformations (11-3b): integrated of order one I(1), first differencing to get I(0).
- deciding whether a series is I(1) (11-3c): first-order autocorrelation as an informal guide.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
### §11.4 — Dynamically Complete Models and the Absence of Serial Correlation (pp. 360–363)
**Subtopics:**
- dynamic completeness: E(y_t|x_t, y_{t-1}, x_{t-1}, …) = E(y_t|x_t) implies no serial correlation; sequential exogeneity.
### §11.5 — The Homoskedasticity Assumption for Time Series Models (pp. 363–364)
**Subtopics:**
- conditional homoskedasticity with lagged dependent variables in the conditioning set.

## Ch. 12 — Serial Correlation and Heteroskedasticity in Time Series Regressions
#topic/arima-unit-roots #topic/state-space-volatility
**Pages:** pp. 372–400
### §12.1 — Properties of OLS with Serially Correlated Errors (pp. 373–376)
**Subtopics:**
- unbiasedness and consistency (12-1a): unaffected by serial correlation alone.
- efficiency and inference (12-1b): usual standard errors invalid under AR(1) errors (typically understated).
- goodness of fit (12-1c): R-squared still valid for stationary data.
- serial correlation with lagged dependent variables (12-1d): inconsistency when errors are correlated with y_{t-1}.
### §12.2 — Testing for Serial Correlation (pp. 376–381)
**Subtopics:**
- t test for AR(1) with strictly exogenous regressors (12-2a): regress û_t on û_{t-1}.
- Durbin–Watson test (12-2b): DW ≈ 2(1−ρ̂), bounds under CLM assumptions.
- AR(1) test without strict exogeneity (12-2c): Durbin's alternative, include regressors in auxiliary regression.
- higher-order serial correlation (12-2d): Breusch–Godfrey LM test for AR(q).
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
### §12.3 — Correcting for Serial Correlation with Strictly Exogenous Regressors (pp. 381–387)
**Subtopics:**
- BLUE with AR(1) errors (12-3a): quasi-differencing / GLS transformation.
- feasible GLS (12-3b): Cochrane–Orcutt and Prais–Winsten estimation.
- comparing OLS and FGLS (12-3c): differences signal failure of strict exogeneity.
- higher-order serial correlation (12-3d): AR(2) corrections.
### §12.4 — Differencing and Serial Correlation (pp. 387–388)
**Subtopics:**
- first differencing to remove strong serial correlation and unit roots in errors.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
### §12.5 — Serial Correlation-Robust Inference after OLS (pp. 388–391)
**Subtopics:**
- HAC standard errors: Newey–West serial-correlation- and heteroskedasticity-robust standard errors with a truncation lag.
### §12.6 — Heteroskedasticity in Time Series Regressions (pp. 391–396)
**Subtopics:**
- robust statistics (12-6a) and Breusch–Pagan testing in time series (12-6b).
- ARCH (12-6c): Engle's autoregressive conditional heteroskedasticity model, E(u_t²|past) = α0 + α1u²_{t-1}; dynamic heteroskedasticity even without serial correlation.
- heteroskedasticity and serial correlation together (12-6d): combining FGLS corrections.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

## Ch. 13 — Pooling Cross Sections across Time: Simple Panel Data Methods
#topic/panel-did #topic/potential-outcomes
**Pages:** pp. 402–433
### §13.1 — Pooling Independent Cross Sections across Time (pp. 403–407)
**Subtopics:**
- pooled cross sections: year dummies, interactions with time to track changing effects.
- Chow test for structural change across time (13-1a).
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
### §13.2 — Policy Analysis with Pooled Cross Sections (pp. 407–412)
**Subtopics:**
- natural (quasi-) experiments: treatment and control groups before/after.
- difference-in-differences estimator: δ̂1 = (ȳ_{T,after} − ȳ_{T,before}) − (ȳ_{C,after} − ȳ_{C,before}); incinerator (KIELMC) example; parallel-trends logic.
- difference-in-difference-in-differences (DDD) estimator.
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
### §13.3 — Two-Period Panel Data Analysis (pp. 412–417)
**Subtopics:**
- unobserved effects model: fixed effect a_i plus idiosyncratic error; heterogeneity bias in pooled OLS.
- first-differenced estimator: differencing removes a_i; requires strict exogeneity and variation in Δx.
- organizing panel data (13-3a).
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
### §13.4 — Policy Analysis with Two-Period Panel Data (pp. 417–420)
**Subtopics:**
- program evaluation with panel data: FD estimation of program effects (job training grants), DiD as a panel FD regression.
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
### §13.5 — Differencing with More Than Two Time Periods (pp. 420–424)
**Subtopics:**
- FD with T>2: time dummies, serial correlation in Δu, robust/clustered inference.
- pitfalls of first differencing (13-5a): little variation in Δx, measurement error amplification, failure of strict exogeneity.
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]

## Ch. 14 — Advanced Panel Data Methods
#topic/panel-did
**Pages:** pp. 434–460
### §14.1 — Fixed Effects Estimation (pp. 435–441)
**Subtopics:**
- within transformation: time-demeaning removes a_i; FE estimator, degrees of freedom NT−N−k.
- dummy variable regression (14-1a): LSDV gives identical slopes to FE.
- FE vs FD (14-1b): equal for T=2; efficiency depends on serial correlation of u_it.
- unbalanced panels (14-1c): attrition and selection.
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
### §14.2 — Random Effects Models (pp. 441–445)
**Subtopics:**
- random effects: a_i uncorrelated with all x; quasi-demeaning with θ = 1 − [σ²u/(σ²u+Tσ²a)]^{1/2}; GLS/FGLS.
- RE vs FE (14-2a): Hausman test.
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
### §14.3 — The Correlated Random Effects Approach (pp. 445–448)
**Subtopics:**
- CRE (Mundlak): include time averages x̄_i; reproduces FE slopes and allows time-constant regressors; regression-based Hausman test.
- unbalanced panels (14-3a).
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
### §14.4 — Applying Panel Data Methods to Other Data Structures (pp. 448–450)
**Subtopics:**
- cluster samples: siblings, schools within districts; cluster-robust standard errors.
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]

## Ch. 15 — Instrumental Variables Estimation and Two Stage Least Squares
#topic/endogeneity-iv
**Pages:** pp. 461–498
### §15.1 — Motivation: Omitted Variables in a Simple Regression Model (pp. 462–471)
**Subtopics:**
- IV conditions: instrument exogeneity Cov(z,u)=0 and instrument relevance Cov(z,x)≠0; IV estimator β̂1 = Cov(z,y)/Cov(z,x).
- inference with IV (15-1a): asymptotic variance σ²/(n σ²x ρ²xz); IV standard errors exceed OLS.
- poor instruments (15-1b): plim formula showing inconsistency Corr(z,u)/Corr(z,x)·σu/σx can exceed OLS bias with weak instruments.
- R-squared after IV (15-1c): can be negative and is not useful.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §15.2 — IV Estimation of the Multiple Regression Model (pp. 471–475)
**Subtopics:**
- structural equation and exclusion restrictions; reduced form equation for the endogenous regressor; rank condition (partial correlation of z with y2).
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §15.3 — Two Stage Least Squares (pp. 475–479)
**Subtopics:**
- 2SLS with one endogenous variable (15-3a): first stage on all exogenous variables, second stage on fitted values.
- multicollinearity and 2SLS (15-3b): larger variances from fitted values.
- weak instruments (15-3c): first-stage F statistic, Staiger–Stock rule of thumb F > 10.
- multiple endogenous variables (15-3d): order condition (at least as many excluded exogenous variables as endogenous regressors).
- multiple hypotheses after 2SLS (15-3e).
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §15.4 — IV Solutions to Errors-in-Variables Problems (pp. 479–481)
**Subtopics:**
- errors-in-variables: a second mismeasured indicator as instrument corrects CEV attenuation.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §15.5 — Testing for Endogeneity and Testing Overidentifying Restrictions (pp. 481–484)
**Subtopics:**
- endogeneity test (15-5a): Hausman (control-function / regression-based) test adding first-stage residuals v̂2.
- overidentification test (15-5b): Sargan/Hansen n·R² test from regressing 2SLS residuals on all exogenous variables, χ²(q).
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §15.6 — 2SLS with Heteroskedasticity (pp. 484–485)
**Subtopics:**
- heteroskedasticity-robust 2SLS standard errors and Breusch–Pagan-type test.
### §15.7 — Applying 2SLS to Time Series Equations (pp. 485–487)
**Subtopics:**
- 2SLS with time series: lagged exogenous variables as instruments, serial-correlation tests and corrections.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
### §15.8 — Applying 2SLS to Pooled Cross Sections and Panel Data (pp. 487–488)
**Subtopics:**
- IV with FD/FE: instruments for differenced endogenous variables (job-training grant example).
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]

## Ch. 16 — Simultaneous Equations Models
#topic/endogeneity-iv
**Pages:** pp. 499–523
### §16.1 — The Nature of Simultaneous Equations Models (pp. 500–503)
**Subtopics:**
- structural equations with autonomous ceteris paribus interpretation (labor supply/demand, murder rates and police).
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §16.2 — Simultaneity Bias in OLS (pp. 503–504)
**Subtopics:**
- simultaneity bias: reduced form shows y2 correlated with u1; sign of the bias.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §16.3 — Identifying and Estimating a Structural Equation (pp. 504–510)
**Subtopics:**
- identification in a two-equation system (16-3a): rank condition — the other equation must contain an exogenous variable excluded from the first.
- estimation by 2SLS (16-3b): Mroz labor supply example.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]
### §16.4 — Systems with More Than Two Equations (pp. 510–511)
**Subtopics:**
- identification with three or more equations (16-4a): order condition (necessary) vs rank condition (sufficient); overidentified/just identified.
- estimation (16-4b): equation-by-equation 2SLS; 3SLS mentioned.
### §16.5 — Simultaneous Equations Models with Time Series (pp. 511–514)
**Subtopics:**
- macro SEMs (Keynesian consumption/investment); exogeneity doubts; lagged variables as instruments; unit-root issues.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
### §16.6 — Simultaneous Equations Models with Panel Data (pp. 514–516)
**Subtopics:**
- differencing to remove unobserved effects, then IV with time-varying instruments.
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]

## Ch. 17 — Limited Dependent Variable Models and Sample Selection Corrections
#topic/classification-validation #topic/potential-outcomes
**Pages:** pp. 524–567
### §17.1 — Logit and Probit Models for Binary Response (pp. 525–536)
**Subtopics:**
- specifying logit and probit (17-1a): P(y=1|x) = G(xβ) with logistic or standard normal CDF; latent variable model.
- maximum likelihood estimation (17-1b): log-likelihood, consistency and asymptotic normality of MLE.
- testing multiple hypotheses (17-1c): Wald, likelihood ratio (LR = 2(ℒur − ℒr)) and LM tests.
- interpreting estimates (17-1d): partial effect at the average (PEA) vs average partial effect (APE); percent correctly predicted; pseudo R-squared (McFadden); comparing with LPM via scale factors.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
### §17.2 — The Tobit Model for Corner Solution Responses (pp. 536–543)
**Subtopics:**
- Tobit: corner solution responses, E(y|y>0,x) and E(y|x) with inverse Mills ratio.
- interpreting Tobit estimates (17-2a): scale factors for partial effects.
- specification issues (17-2b): Tobit restrictions on participation vs amount.
### §17.3 — The Poisson Regression Model (pp. 543–547)
**Subtopics:**
- count data: exponential mean, Poisson QMLE, overdispersion and adjusted standard errors.
### §17.4 — Censored and Truncated Regression Models (pp. 547–553)
**Subtopics:**
- censored regression (17-4a): data censoring (top-coding, durations), censored normal regression.
- truncated regression (17-4b): sample selected on y; truncated normal MLE.
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
### §17.5 — Sample Selection Corrections (pp. 553–558)
**Subtopics:**
- when OLS on the selected sample is consistent (17-5a): exogenous selection.
- incidental truncation (17-5b): Heckman two-step (Heckit) with probit selection equation and inverse Mills ratio; test for selection bias.
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]

## Ch. 18 — Advanced Time Series Topics
#topic/arima-unit-roots
**Pages:** pp. 568–604
### §18.1 — Infinite Distributed Lag Models (pp. 569–574)
**Subtopics:**
- infinite distributed lags: impact propensity and long-run propensity.
- geometric (Koyck) distributed lag (18-1a): reduces to a model with lagged y; IV estimation.
- rational distributed lag models (18-1b).
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
### §18.2 — Testing for Unit Roots (pp. 574–578)
**Subtopics:**
- Dickey–Fuller test: Δy_t = α + θy_{t-1} + e_t, H0: θ=0 with DF (non-normal) critical values.
- augmented Dickey–Fuller (ADF) test with lagged changes; DF test with a time trend.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
### §18.3 — Spurious Regression (pp. 578–580)
**Subtopics:**
- spurious regression: Granger–Newbold result that regressing independent I(1) series gives significant t statistics.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
### §18.4 — Cointegration and Error Correction Models (pp. 580–586)
**Subtopics:**
- cointegration (18-4a): y_t − βx_t is I(0); Engle–Granger test (DF on OLS residuals with special critical values); leads-and-lags estimator.
- error correction models (18-4b): short-run dynamics with the lagged error-correction term.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
### §18.5 — Forecasting (pp. 586–598)
**Subtopics:**
- forecasting models (18-5a): conditional expectation, information set, Granger causality, VAR.
- one-step-ahead forecasts (18-5b): forecast intervals.
- comparing forecasts (18-5c): out-of-sample RMSE and MAE.
- multiple-step-ahead forecasts (18-5d): iterating AR(1) forecasts, growing forecast variance.
- forecasting trending, seasonal and integrated processes (18-5e): random walk with drift forecasts.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

## Ch. 19 — Carrying out an Empirical Project
#background
**Pages:** pp. 605–627
### §19.1 — Posing a Question (pp. 605–607)
**Subtopics:**
- choosing a well-defined, answerable research question.
### §19.2 — Literature Review (pp. 607–608)
**Subtopics:**
- locating and using prior work.
### §19.3 — Data Collection (pp. 608–611)
**Subtopics:**
- deciding on the dataset; entering, storing and inspecting data.
### §19.4 — Econometric Analysis (pp. 611–614)
**Subtopics:**
- choosing methods; robustness and specification checks.
### §19.5 — Writing an Empirical Paper (pp. 614–621)
**Subtopics:**
- structure: introduction, conceptual framework, models and estimation, data, results, conclusions, style hints.

## Appendices
#background
**Pages:** pp. 628–749
- Appendix A — Basic Mathematical Tools (pp. 628–644): summation, linear/quadratic functions, logs, differential calculus.
- Appendix B — Fundamentals of Probability (pp. 645–673): random variables, joint/conditional distributions, expectation, normal and related distributions.
- Appendix C — Fundamentals of Mathematical Statistics (pp. 674–708): estimators, asymptotics, MLE, interval estimation, hypothesis testing.
- Appendix D — Summary of Matrix Algebra (pp. 709–719).
- Appendix E — The Linear Regression Model in Matrix Form (pp. 720–733).
- Appendix F — Answers to Chapter Questions (pp. 734–742).
- Appendix G — Statistical Tables (pp. 743–749).


# Tsay, Analysis of Financial Time Series, 3e
#book/tsay
> Link: [[Livros/Ruey S. Tsay - Analysis of Financial Time Series, Third Edition (Wiley Series in Probability and Statistics)-John Wiley & Sons (2010)|Tsay AFTS 3e]]

> Page numbers are printed book pages. PDF offset: printed page = PDF page (1-based) − 27 (Ch. 1 p. 1 is PDF page 28). Section starts were checked against the page text; end pages are the page where the next section begins (sections share boundary pages).

## Ch. 1 — Financial Time Series and Their Characteristics
**Pages:** pp. 1–28

### §1.1 — Asset Returns (pp. 2–7)
**Subtopics:**
- simple and multiperiod returns: one-period simple gross/net return, k-period compounding, annualized (average) returns.
- continuously compounded (log) returns: r_t = ln(1+R_t), additivity of multiperiod log returns.
- portfolio returns, dividend payments, excess returns: portfolio simple return as weighted average; log-return approximation; excess return over a risk-free asset.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §1.2 — Distributional Properties of Returns (pp. 7–22)
**Subtopics:**
- §1.2.1 Review of statistical distributions and their moments (p. 7): joint/marginal/conditional distributions, moments, sample skewness and kurtosis with their asymptotic tests, Jarque–Bera normality test.
- §1.2.2 Distributions of returns (p. 14): normal, lognormal, stable, scale mixture of normals; heavy tails of returns.
- §1.2.3 Multivariate returns (p. 18): mean vector and covariance matrix of a return vector and their sample estimates.
- §1.2.4 Likelihood function of returns (p. 19): factorization of the joint density into conditional densities; conditional normal log-likelihood.
- §1.2.5 Empirical properties of returns (p. 19): stylized facts — fat tails, slight skewness, near-zero mean, volatility clustering in daily/monthly returns.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §1.3 — Processes Considered (pp. 22–24)
**Subtopics:**
- scope of the book: return series, volatility process, extreme returns, and the relationships among several returns; Appendix: R packages (p. 24).

## Ch. 2 — Linear Time Series Analysis and Its Applications
**Pages:** pp. 29–108

### §2.1 — Stationarity (p. 30)
**Subtopics:**
- strict vs. weak stationarity: time-invariant joint distributions vs. constant mean and lag-dependent autocovariance.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §2.2 — Correlation and Autocorrelation Function (pp. 30–36)
**Subtopics:**
- correlation coefficient and sample ACF: lag-l autocorrelation, Bartlett's formula for its standard error.
- portmanteau tests: Box–Pierce Q*(m) and Ljung–Box Q(m) for joint zero autocorrelation.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §2.3 — White Noise and Linear Time Series (pp. 36–37)
**Subtopics:**
- white noise and linear processes: iid/Gaussian white noise; MA(∞) (Wold-type) representation r_t = μ + Σψ_i a_{t−i}, its mean, variance and ACF.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §2.4 — Simple AR Models (pp. 37–57)
**Subtopics:**
- §2.4.1 Properties of AR models (p. 38): AR(1)/AR(2)/AR(p) mean, variance, ACF; stationarity via characteristic roots; complex roots and business cycles.
- §2.4.2 Identifying AR models in practice (p. 46): PACF cutoff, AIC/BIC order selection, conditional LS estimation, model checking with Ljung–Box on residuals.
- §2.4.3 Goodness of fit (p. 53): R² and adjusted R² for stationary models.
- §2.4.4 Forecasting (p. 54): minimum MSE forecasts, multistep forecast errors, mean reversion and half-life.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §2.5 — Simple MA Models (pp. 57–64)
**Subtopics:**
- §2.5.1 Properties of MA models (p. 59): finite memory, ACF cutoff after lag q, invertibility.
- §2.5.2 Identifying MA order (p. 60): sample ACF cutoff.
- §2.5.3 Estimation (p. 61): conditional vs. exact likelihood.
- §2.5.4 Forecasting using MA models (p. 62): forecasts revert to the mean after q steps.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §2.6 — Simple ARMA Models (pp. 64–71)
**Subtopics:**
- §2.6.1 Properties of ARMA(1,1) (p. 64): mean, variance, ACF and PACF tail off.
- §2.6.2 General ARMA models (p. 66): ARMA(p,q) via lag polynomials.
- §2.6.3 Identifying ARMA models (p. 66): extended ACF (EACF) table, information criteria.
- §2.6.4 Forecasting using an ARMA model (p. 68): recursive multistep forecasts and forecast-error variance.
- §2.6.5 Three model representations (p. 69): ARMA, AR(∞) (π-weights) and MA(∞) (ψ-weights; impulse response) forms.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §2.7 — Unit-Root Nonstationarity (pp. 71–81)
**Subtopics:**
- §2.7.1 Random walk (p. 72): non-mean-reverting, forecast variance grows with horizon; permanent shocks.
- §2.7.2 Random walk with drift (p. 73): deterministic time trend in the mean via the drift.
- §2.7.3 Trend-stationary time series (p. 75): deterministic trend plus stationary deviations vs. stochastic trend.
- §2.7.4 General unit-root models (p. 75): ARIMA(p,1,q), differencing, overdifferencing.
- §2.7.5 Unit-root test (p. 76): Dickey–Fuller and augmented DF (ADF) tests, nonstandard distributions, choice of deterministic terms.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §2.8 — Seasonal Models (pp. 81–90)
**Subtopics:**
- §2.8.1 Seasonal differencing (p. 82): (1−B^s) differencing of quarterly earnings data.
- §2.8.2 Multiplicative seasonal models (p. 84): airline model (0,1,1)×(0,1,1)_s, its ACF and forecasting.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §2.9 — Regression Models with Time Series Errors (pp. 90–97)
**Subtopics:**
- regression with serially correlated errors: spurious-looking regression of 3-year on 1-year Treasury rates, differencing, joint estimation of regression and ARMA error model; Durbin–Watson statistic.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §2.10 — Consistent Covariance Matrix Estimation (pp. 97–101)
**Subtopics:**
- robust standard errors: White heteroscedasticity-consistent (HC) and Newey–West HAC covariance estimators for OLS coefficients.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §2.11 — Long-Memory Models (pp. 101–103)
**Subtopics:**
- fractional differencing: ARFIMA / (1−B)^d with −0.5<d<0.5, hyperbolic ACF decay, long-range dependence in absolute returns; Appendix: SCA commands (p. 103).
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

## Ch. 3 — Conditional Heteroscedastic Models
**Pages:** pp. 109–174

### §3.1 — Characteristics of Volatility (pp. 110–111)
**Subtopics:**
- volatility stylized facts: clustering, continuous evolution, mean reversion within a range, leverage (asymmetric) effect; implied volatility.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.2 — Structure of a Model (pp. 111–113)
**Subtopics:**
- mean and volatility equations: r_t = μ_t + a_t with conditional variance σ_t²; conditional heteroscedastic vs. stochastic volatility classes.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.3 — Model Building (pp. 113–115)
**Subtopics:**
- four-step volatility modeling procedure: mean equation, ARCH-effect test, joint estimation, model checking.
- §3.3.1 Testing for ARCH effect (p. 114): Ljung–Box Q(m) on squared residuals (McLeod–Li) and Engle's LM test.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.4 — The ARCH Model (pp. 115–131)
**Subtopics:**
- §3.4.1 Properties of ARCH models (p. 117): ARCH(1) unconditional variance, fourth moment condition, excess kurtosis.
- §3.4.2 Weaknesses (p. 119): symmetric response to shocks, restrictive parameters, no explanation of volatility source, overprediction.
- §3.4.3 Building an ARCH model (p. 119): PACF of a_t² for order, conditional MLE under normal, Student-t and skew-t / GED innovations, standardized-residual checks, forecasting.
- §3.4.4 Some examples (p. 123): ARCH fits to Intel monthly returns and USD/DM exchange rate.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.5 — The GARCH Model (pp. 131–140)
**Subtopics:**
- GARCH(m,s): ARMA representation for a_t², stationarity condition Σ(α+β)<1, GARCH(1,1) kurtosis and multistep volatility forecasts.
- §3.5.1 An illustrative example (p. 134): GARCH(1,1) for S&P 500 monthly excess returns, Gaussian vs. Student-t.
- §3.5.2 Forecasting evaluation (p. 139): realized-volatility proxies and the low R² of volatility forecasts.
- §3.5.3 A two-pass estimation method (p. 140): fit ARMA to squared residuals and map to GARCH parameters.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.6 — The Integrated GARCH Model (pp. 140–142)
**Subtopics:**
- IGARCH: unit-root GARCH (α+β=1), persistent shocks, link to RiskMetrics EWMA.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.7 — The GARCH-M Model (pp. 142–143)
**Subtopics:**
- GARCH-in-mean: risk premium c·σ_t² (or σ_t) in the mean equation and its test.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.8 — The Exponential GARCH Model (pp. 143–149)
**Subtopics:**
- EGARCH (Nelson): log-volatility with asymmetric g(ε) = θε + γ(|ε|−E|ε|), no positivity constraints; leverage effect.
- §3.8.1 Alternative model form (p. 144); §3.8.2 Illustrative example (p. 145, IBM monthly); §3.8.3 Second example (p. 145); §3.8.4 Forecasting using an EGARCH model (p. 147): multistep volatility forecasts.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.9 — The Threshold GARCH Model (pp. 149–150)
**Subtopics:**
- TGARCH / GJR: indicator term for negative shocks capturing leverage.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.10 — The CHARMA Model (pp. 150–152)
**Subtopics:**
- conditional heteroscedastic ARMA: volatility from random coefficients on lagged shocks.
- §3.10.1 Effects of explanatory variables (p. 152): exogenous regressors in the volatility.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.11 — Random Coefficient Autoregressive Models (pp. 152–153)
**Subtopics:**
- RCA: AR coefficients with random time-varying parts generate conditional heteroscedasticity.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.12 — Stochastic Volatility Model (pp. 153–154)
**Subtopics:**
- SV model: log-volatility follows its own AR process with an independent shock; estimation via quasi-likelihood / Kalman filter or MCMC (Ch. 12).
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.13 — Long-Memory Stochastic Volatility Model (pp. 154–155)
**Subtopics:**
- LMSV: fractionally integrated log-volatility to capture slow ACF decay of absolute returns.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §3.14 — Application (pp. 155–159)
**Subtopics:**
- practical volatility questions with GARCH-type models on monthly IBM and S&P 500 log returns (1926–1999): summer effect on volatility, effect of lagged market returns, comparison of fitted models.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.15 — Alternative Approaches (pp. 159–165)
**Subtopics:**
- §3.15.1 Use of high-frequency data (p. 159): realized volatility from intraday returns.
- §3.15.2 Use of daily open, high, low, close prices (p. 162): Parkinson, Garman–Klass, Rogers–Satchell, Yang–Zhang range-based estimators.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §3.16 — Kurtosis of GARCH Models (pp. 165–167)
**Subtopics:**
- excess kurtosis of GARCH(1,1) with non-Gaussian innovations: decomposition into innovation and volatility-dynamics parts; Appendix: RATS programs (p. 167).
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

## Ch. 4 — Nonlinear Models and Their Applications
#background
**Pages:** pp. 175–230

### §4.1 — Nonlinear Models (pp. 177–205)
**Subtopics:**
- bilinear (4.1.1, p. 177), TAR (4.1.2, p. 179), STAR (4.1.3, p. 184), Markov switching (4.1.4, p. 186), nonparametric kernel/local-linear methods (4.1.5, p. 189), functional-coefficient AR (4.1.6, p. 198), nonlinear additive AR (4.1.7, p. 198), nonlinear state-space (4.1.8, p. 199), neural networks (4.1.9, p. 199).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]] (Markov switching estimation, nonlinear state space)

### §4.2 — Nonlinearity Tests (pp. 205–214)
**Subtopics:**
- nonparametric tests (4.2.1, p. 206: McLeod–Li Q of squared residuals, BDS, rank-based), parametric tests (4.2.2, p. 209: RESET, F-test, threshold test), applications (4.2.3, p. 213).

### §4.3 — Modeling (pp. 214–215)
**Subtopics:**
- strategy for building nonlinear models.

### §4.4 — Forecasting (pp. 215–218)
**Subtopics:**
- parametric bootstrap forecasts (4.4.1, p. 215); forecast evaluation of nonlinear vs. linear models (4.4.2, p. 215).

### §4.5 — Application (pp. 218–222)
**Subtopics:**
- linear vs. TAR and Markov switching models for the quarterly U.S. civilian unemployment rate (asymmetric business-cycle dynamics); appendices with RATS and neural-network code (pp. 222–223).

## Ch. 5 — High-Frequency Data Analysis and Market Microstructure
#background
**Pages:** pp. 231–286

### §5.1 — Nonsynchronous Trading (pp. 232–235)
**Subtopics:**
- spurious serial correlation induced by nonsynchronous trading.

### §5.2 — Bid–Ask Spread (pp. 235–237)
**Subtopics:**
- bid–ask bounce and Roll's negative lag-1 autocorrelation.

### §5.3 — Empirical Characteristics of Transactions Data (pp. 237–244)
**Subtopics:**
- tick-level price changes, durations, diurnal patterns.

### §5.4 — Models for Price Changes (pp. 244–253)
**Subtopics:**
- ordered probit (5.4.1, p. 245); decomposition model (5.4.2, p. 248).

### §5.5 — Duration Models (pp. 253–264)
**Subtopics:**
- ACD model (5.5.1, p. 255), simulation (5.5.2, p. 257), estimation (5.5.3, p. 260).

### §5.6 — Nonlinear Duration Models (pp. 264–265)
**Subtopics:**
- threshold ACD.

### §5.7 — Bivariate Models for Price Change and Duration (pp. 265–270)
**Subtopics:**
- joint price-change/duration model (PCD).

### §5.8 — Application (pp. 270–276)
**Subtopics:**
- empirical application to transaction data; appendices on distributions, hazard function, RATS code (pp. 276–281).

## Ch. 6 — Continuous-Time Models and Their Applications
#background
**Pages:** pp. 287–324

### §6.1 — Options (p. 288)
**Subtopics:**
- option terminology (calls, puts, European/American).

### §6.2 — Some Continuous-Time Stochastic Processes (pp. 288–292)
**Subtopics:**
- Wiener (6.2.1, p. 289), generalized Wiener (6.2.2, p. 291), Ito process (6.2.3, p. 292).

### §6.3 — Ito's Lemma (pp. 292–297)
**Subtopics:**
- review of differentiation (6.3.1), stochastic differentiation (6.3.2), application to log prices (6.3.3), estimation of μ and σ (6.3.4, p. 295).

### §6.4 — Distributions of Stock Prices and Log Returns (pp. 297–298)
**Subtopics:**
- lognormal prices under geometric Brownian motion.

### §6.5 — Derivation of Black–Scholes Differential Equation (pp. 298–300)
**Subtopics:**
- riskless hedge portfolio and the Black–Scholes PDE.

### §6.6 — Black–Scholes Pricing Formulas (pp. 300–309)
**Subtopics:**
- risk-neutral world (6.6.1), formulas (6.6.2), lower bounds of European options (6.6.3, p. 304), discussion (6.6.4, p. 305).

### §6.7 — Extension of Ito's Lemma (pp. 309–310)
**Subtopics:**
- multivariate Ito's lemma.

### §6.8 — Stochastic Integral (pp. 310–311)
**Subtopics:**
- Ito integral basics.

### §6.9 — Jump Diffusion Models (pp. 311–318)
**Subtopics:**
- Kou double-exponential jump diffusion; option pricing under jump diffusion (6.9.1, p. 315).

### §6.10 — Estimation of Continuous-Time Models (pp. 318–319)
**Subtopics:**
- pointers to estimation methods (incl. MCMC); appendices on Black–Scholes integration and normal-CDF approximation.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

## Ch. 7 — Extreme Values, Quantiles, and Value at Risk
#background
**Pages:** pp. 325–388

### §7.1 — Value at Risk (pp. 326–328)
**Subtopics:**
- VaR definition as an upper-tail quantile of the loss distribution.

### §7.2 — RiskMetrics (pp. 328–333)
**Subtopics:**
- IGARCH(1,1)/EWMA volatility, square-root-of-time rule; discussion (7.2.1), multiple positions (7.2.2), expected shortfall (7.2.3).
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §7.3 — Econometric Approach to VaR Calculation (pp. 333–338)
**Subtopics:**
- ARMA-GARCH-based VaR; multiple periods (7.3.1, p. 336); expected shortfall under conditional normality (7.3.2, p. 338).
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §7.4 — Quantile Estimation (pp. 338–342)
**Subtopics:**
- empirical quantiles / order statistics (7.4.1); quantile regression (7.4.2, p. 341).

### §7.5 — Extreme Value Theory (pp. 342–353)
**Subtopics:**
- GEV distribution review (7.5.1), empirical estimation (7.5.2, p. 345), application to stock returns (7.5.3, p. 348).

### §7.6 — Extreme Value Approach to VaR (pp. 353–359)
**Subtopics:**
- EVT-based VaR; discussion (7.6.1), multiperiod VaR (7.6.2), return level (7.6.3).

### §7.7 — New Approach Based on the Extreme Value Theory (pp. 359–377)
**Subtopics:**
- peaks over threshold / generalized Pareto: statistical theory (7.7.1), mean excess function (7.7.2), modeling (7.7.3), VaR (7.7.4), alternative parameterization (7.7.5), explanatory variables (7.7.6), model checking (7.7.7), illustration (7.7.8).

### §7.8 — The Extremal Index (pp. 377–384)
**Subtopics:**
- D(u_n) condition (7.8.1), estimating the extremal index (7.8.2), VaR for a stationary series (7.8.3).

## Ch. 8 — Multivariate Time Series Analysis and Its Applications
**Pages:** pp. 389–466

### §8.1 — Weak Stationarity and Cross-Correlation Matrices (pp. 390–399)
**Subtopics:**
- §8.1.1 Cross-correlation matrices (p. 390): lag-l cross-covariance/correlation matrices, lead–lag interpretation.
- §8.1.2 Linear dependence (p. 392): concurrent vs. lagged relationships, feedback.
- §8.1.3 Sample cross-correlation matrices (p. 392): simplified (+, −, .) notation for significance.
- §8.1.4 Multivariate portmanteau tests (p. 397): Hosking / Li–McLeod multivariate Q_k(m).
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §8.2 — Vector Autoregressive Models (pp. 399–417)
**Subtopics:**
- §8.2.1 Reduced and structural forms (p. 399): VAR(1), Cholesky orthogonalization to a structural (recursive) form, identification by ordering.
- §8.2.2 Stationarity condition and moments of a VAR(1) (p. 401): eigenvalues of Φ inside the unit circle, mean and covariance.
- §8.2.3 Vector AR(p) models (p. 403): companion form, moment equations.
- §8.2.4 Building a VAR(p) model (p. 405): sequential LR test (M(i) statistic), AIC/BIC/HQ order selection, OLS/ML estimation, residual checks, forecasting.
- §8.2.5 Impulse response function (p. 413): MA(∞) ψ-weights, orthogonalized impulse responses, forecast-error variance decomposition.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §8.3 — Vector Moving-Average Models (pp. 417–422)
**Subtopics:**
- VMA(q): cross-correlation cutoff after lag q, invertibility, conditional vs. exact likelihood.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §8.4 — Vector ARMA Models (pp. 422–428)
**Subtopics:**
- VARMA(p,q): identifiability problems and exchangeable models; estimation and an interest-rate example.
- §8.4.1 Marginal models of components (p. 427): each component follows a univariate ARMA of higher order.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §8.5 — Unit-Root Nonstationarity and Cointegration (pp. 428–432)
**Subtopics:**
- cointegration concept: linear combination of I(1) series that is stationary; common trends.
- §8.5.1 An error correction form (p. 431): ECM representation Δx_t = αβ'x_{t−1} + … (Engle–Granger).
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §8.6 — Cointegrated VAR Models (pp. 432–442)
**Subtopics:**
- §8.6.1 Specification of the deterministic function (p. 434): five cases of constants/trends (restricted constant, etc.).
- §8.6.2 Maximum-likelihood estimation (p. 435): Johansen reduced-rank regression.
- §8.6.3 Cointegration test (p. 436): Johansen trace and maximum-eigenvalue tests.
- §8.6.4 Forecasting of cointegrated VAR models (p. 437).
- §8.6.5 An example (p. 438): weekly 3-month and 6-month Treasury bill rates (VAR, Johansen test, VECM).
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §8.7 — Threshold Cointegration and Arbitrage (pp. 442–446)
**Subtopics:**
- index-futures arbitrage with cost-of-carry: §8.7.1 multivariate threshold model (p. 444), §8.7.2 the data (p. 445), §8.7.3 estimation (p. 445).
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §8.8 — Pairs Trading (pp. 446–456)
**Subtopics:**
- §8.8.1 Theoretical framework (p. 446): cointegrated log prices and a mean-reverting spread w_t.
- §8.8.2 Trading strategy (p. 448): open/unwind trades at deviations Δ from μ_w net of cost η.
- §8.8.3 Simple illustration (p. 449); appendices on matrices, multivariate normal, SCA commands (pp. 456–461).
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

## Ch. 9 — Principal Component Analysis and Factor Models
**Pages:** pp. 467–504

### §9.1 — A Factor Model (pp. 468–470)
**Subtopics:**
- general factor model r_it = α_i + β_i'f_t + ε_it: covariance structure Σ_r = βΣ_fβ' + D; macroeconomic, fundamental and statistical families.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §9.2 — Macroeconometric Factor Models (pp. 470–476)
**Subtopics:**
- §9.2.1 Single-factor model (p. 470): market model, β/σ²/R² by OLS, global minimum variance portfolio to compare covariance matrices.
- §9.2.2 Multifactor models (p. 474): Chen–Roll–Ross style macro surprises (VAR residuals of CPI and civilian employment growth) as factors.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §9.3 — Fundamental Factor Models (pp. 476–483)
**Subtopics:**
- §9.3.1 BARRA factor model (p. 477): observed asset attributes (industry dummies) as betas, factor realizations by cross-sectional WLS.
- §9.3.2 Fama–French approach (p. 482): size and book-to-market hedge portfolios as factors.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §9.4 — Principal Component Analysis (pp. 483–489)
**Subtopics:**
- §9.4.1 Theory of PCA (p. 483): eigen-decomposition of covariance/correlation matrix, variance explained.
- §9.4.2 Empirical PCA (p. 485): sample PCA of stock returns, scree plot.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §9.5 — Statistical Factor Analysis (pp. 489–498)
**Subtopics:**
- orthogonal factor model with loadings L and specific variances.
- §9.5.1 Estimation (p. 490): principal-component and maximum-likelihood methods, LR test for number of factors.
- §9.5.2 Factor rotation (p. 492): varimax.
- §9.5.3 Applications (p. 492): factor analysis of monthly stock returns.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §9.6 — Asymptotic Principal Component Analysis (pp. 498–501)
**Subtopics:**
- APCA for k ≫ T (Connor–Korajczyk) using the T×T cross-product matrix.
- §9.6.1 Selecting the number of factors (p. 499): Connor–Korajczyk test and Bai–Ng information criteria.
- §9.6.2 An example (p. 500): 40 stocks, 36 months.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

## Ch. 10 — Multivariate Volatility Models and Their Applications
**Pages:** pp. 505–556

### §10.1 — Exponentially Weighted Estimate (pp. 506–510)
**Subtopics:**
- multivariate EWMA covariance Σ_t = (1−λ)a_{t−1}a'_{t−1} + λΣ_{t−1}, λ estimated by likelihood.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §10.2 — Some Multivariate GARCH Models (pp. 510–516)
**Subtopics:**
- §10.2.1 Diagonal VEC model (p. 510): DVEC(m,s) element-wise GARCH, positive-definiteness issue.
- §10.2.2 BEKK model (p. 513): Σ_t = A0A0' + A1a a'A1' + B1Σ B1', positive definite by construction.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §10.3 — Reparameterization (pp. 516–521)
**Subtopics:**
- §10.3.1 Use of correlations (p. 516): variances plus correlations (Fisher-transformed).
- §10.3.2 Cholesky decomposition (p. 517): Σ_t = L_tG_tL_t', orthogonalized shocks b_t, simple likelihood without constraints.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §10.4 — GARCH Models for Bivariate Returns (pp. 521–537)
**Subtopics:**
- §10.4.1 Constant-correlation models (p. 521): Bollerslev CCC-GARCH.
- §10.4.2 Time-varying correlation models (p. 525): logistic/Fisher-transformed ρ_t and Cholesky-based q_t models.
- §10.4.3 Dynamic correlation models (p. 531): Tse–Tsui and Engle DCC.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §10.5 — Higher Dimensional Volatility Models (pp. 537–543)
**Subtopics:**
- sequential Cholesky-based strategy: add assets one at a time, build volatility of orthogonal shocks.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §10.6 — Factor–Volatility Models (pp. 543–546)
**Subtopics:**
- volatility driven by a few common factors from PCA of the volatility/shock process (Engle–Ng–Rothschild style).
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §10.7 — Application (pp. 546–548)
**Subtopics:**
- portfolio VaR for Cisco and Intel with three volatility-modeling approaches.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §10.8 — Multivariate t Distribution (pp. 548–549)
**Subtopics:**
- standardized multivariate Student-t innovations; Appendix: remarks on estimation and RATS code (p. 549).
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

## Ch. 11 — State-Space Models and Kalman Filter
**Pages:** pp. 557–612

### §11.1 — Local Trend Model (pp. 558–576)
**Subtopics:**
- local level (random walk plus noise) model y_t = μ_t + e_t, μ_{t+1} = μ_t + η_t; link to ARIMA(0,1,1); Alcoa realized-volatility example.
- §11.1.1 Statistical inference (p. 561): filtering, prediction, smoothing defined.
- §11.1.2 Kalman filter (p. 562): prediction/update recursions, Kalman gain.
- §11.1.3 Properties of forecast error (p. 564): innovations v_t are independent; prediction-error decomposition.
- §11.1.4 State smoothing (p. 566): backward smoothing recursions.
- §11.1.5 Missing values (p. 570): skip the update step.
- §11.1.6 Effect of initialization (p. 571): diffuse initialization.
- §11.1.7 Estimation (p. 572): ML via prediction-error decomposition.
- §11.1.8 S-Plus commands used (p. 572): SsfPack code.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §11.2 — Linear State-Space Models (pp. 576–577)
**Subtopics:**
- general linear Gaussian state-space form: transition and measurement equations with system matrices.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §11.3 — Model Transformation (pp. 577–591)
**Subtopics:**
- §11.3.1 CAPM with time-varying coefficients (p. 577): random-walk α_t and β_t (time-varying parameters).
- §11.3.2 ARMA models (p. 580): Akaike, Harvey and Aoki state-space representations.
- §11.3.3 Linear regression model (p. 586): coefficients as states, recursive least squares.
- §11.3.4 Linear regression with ARMA errors (p. 588).
- §11.3.5 Scalar unobserved component model (p. 590): trend + seasonal + irregular.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §11.4 — Kalman Filter and Smoothing (pp. 591–600)
**Subtopics:**
- §11.4.1 Kalman filter (p. 591): general recursions.
- §11.4.2 State estimation error and forecast error (p. 594).
- §11.4.3 State smoothing (p. 595): fixed-interval smoother.
- §11.4.4 Disturbance smoothing (p. 597): smoothed disturbances for outlier/break detection.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §11.5 — Missing Values (pp. 600–601)
**Subtopics:**
- handling missing observations in the general Kalman filter.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §11.6 — Forecasting (pp. 601–602)
**Subtopics:**
- multistep forecasts as missing future observations.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §11.7 — Application (pp. 602–609)
**Subtopics:**
- unobserved-components model (trend + seasonal) for quarterly J&J earnings; filtered and smoothed components.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

## Ch. 12 — Markov Chain Monte Carlo Methods with Applications
**Pages:** pp. 613–672

### §12.1 — Markov Chain Simulation (pp. 614–615)
**Subtopics:**
- MCMC idea: build a Markov chain whose stationary distribution is the posterior; transition kernels, convergence.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §12.2 — Gibbs Sampling (pp. 615–617)
**Subtopics:**
- Gibbs sampler: iterate draws from full conditional distributions; burn-in, convergence diagnostics.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §12.3 — Bayesian Inference (pp. 617–622)
**Subtopics:**
- §12.3.1 Posterior distributions (p. 617): posterior ∝ likelihood × prior.
- §12.3.2 Conjugate prior distributions (p. 618): normal–normal, inverted chi-squared for variance, normal regression and multivariate (Wishart) results.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §12.4 — Alternative Algorithms (pp. 622–624)
**Subtopics:**
- §12.4.1 Metropolis algorithm (p. 622): symmetric proposal, acceptance probability.
- §12.4.2 Metropolis–Hastings algorithm (p. 623): asymmetric proposals.
- §12.4.3 Griddy Gibbs (p. 623): grid-based inverse-CDF draws for nonstandard conditionals.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §12.5 — Linear Regression with Time Series Errors (pp. 624–628)
**Subtopics:**
- Gibbs sampling for regression with AR errors: conditional posteriors of β, φ, σ² under conjugate priors (Treasury rate example).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Rules: [[rules/07_bayes|Bayesian inference]]

### §12.6 — Missing Values and Outliers (pp. 628–636)
**Subtopics:**
- §12.6.1 Missing values (p. 629): missing data as parameters drawn from their conditional posterior in an AR(p).
- §12.6.2 Outlier detection (p. 632): additive outliers with Bernoulli indicators via Gibbs sampling.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Rules: [[rules/07_bayes|Bayesian inference]]

### §12.7 — Stochastic Volatility Models (pp. 636–649)
**Subtopics:**
- §12.7.1 Estimation of univariate models (p. 637): Jacquier–Polson–Rossi single-move Gibbs with griddy Gibbs for volatilities; comparison with GARCH.
- §12.7.2 Multivariate stochastic volatility models (p. 643): Cholesky-based bivariate SV and time-varying beta.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §12.8 — New Approach to SV Estimation (pp. 649–660)
**Subtopics:**
- forward filtering backward sampling (FFBS / Carter–Kohn) within the Kalman filter, with a mixture-of-normals approximation of the log χ² error, to draw the volatility path jointly; extensions to leverage and jumps.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]

### §12.9 — Markov Switching Models (pp. 660–666)
**Subtopics:**
- two-state Markov switching with different risk premia and GARCH dynamics, estimated by Gibbs sampling (McCulloch–Tsay).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §12.10 — Forecasting (pp. 666–669)
**Subtopics:**
- simulation-based predictive distributions from each Gibbs iteration; SV vs. GARCH volatility forecasts incorporating parameter uncertainty.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Rules: [[rules/07_bayes|Bayesian inference]]

### §12.11 — Other Applications (pp. 669–670)
**Subtopics:**
- further uses of MCMC: bid/ask quote determinants, hierarchical models for transactions, diffusion estimation, VaR from predictive distributions.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]


# James, Witten, Hastie & Tibshirani, An Introduction to Statistical Learning, 1e
#book/islr
> Link: [[Livros/(Springer Texts in Statistics) Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani - An Introduction to Statistical Learning with Applications in R-Springer (2014)|ISLR 1e]]

> Page numbers are printed book pages (taken from the book's table of contents). The PDF drops blank pages, so the PDF-to-printed offset drifts: 1-based PDF page − 15 (ch. 1–2), − 14 (ch. 3–4), − 13 (ch. 5), − 12 (ch. 6–7), − 11 (ch. 8), − 10 (ch. 9–10).

## Ch. 2 — Statistical Learning
**Pages:** pp. 15–57

### §2.1 — What Is Statistical Learning? (pp. 15–29)
**Subtopics:**
- Model Y = f(X) + ε: statistical learning as estimating the systematic part f from data; ε is mean-zero error independent of X.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

#### §2.1.1 — Why Estimate f? (pp. 17–21)
**Subtopics:**
- Prediction vs inference: prediction treats f̂ as a black box; inference asks which predictors matter and how.
- Reducible vs irreducible error: E(Y − Ŷ)² = [f(X) − f̂(X)]² + Var(ε); Var(ε) bounds achievable accuracy.

#### §2.1.2 — How Do We Estimate f? (pp. 21–24)
**Subtopics:**
- Parametric methods: assume a functional form (e.g., linear) and fit by least squares; risk of misspecification.
- Non-parametric methods: thin-plate splines etc. need no form assumption but need many observations; overfitting the noise.

#### §2.1.3 — The Trade-Off Between Prediction Accuracy and Model Interpretability (pp. 24–26)
**Subtopics:**
- Flexibility vs interpretability: lasso/OLS (interpretable, rigid) vs splines, bagging, boosting, SVMs (flexible, opaque); flexible is not always more accurate.

#### §2.1.4 — Supervised Versus Unsupervised Learning (pp. 26–28)
**Subtopics:**
- Supervised (response observed) vs unsupervised (no response; e.g., cluster analysis) vs semi-supervised settings.

#### §2.1.5 — Regression Versus Classification Problems (pp. 28–29)
**Subtopics:**
- Quantitative vs qualitative responses; method choice depends on response type more than predictor type.

### §2.2 — Assessing Model Accuracy (pp. 29–42)
**Subtopics:**
- No free lunch: no single method dominates on all data sets, so model selection is needed.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

#### §2.2.1 — Measuring the Quality of Fit (pp. 29–33)
**Subtopics:**
- Training vs test MSE: training MSE falls monotonically with flexibility, test MSE is U-shaped; overfitting defined by this gap.
- Degrees of freedom as a summary of flexibility; cross-validation previewed as the way to estimate test MSE.

#### §2.2.2 — The Bias-Variance Trade-Off (pp. 33–37)
**Subtopics:**
- Bias–variance decomposition: expected test MSE at x₀ = Var(f̂(x₀)) + [Bias(f̂(x₀))]² + Var(ε).
- More flexible methods have higher variance and lower bias; the U-shaped test MSE is the net effect.

#### §2.2.3 — The Classification Setting (pp. 37–42)
**Subtopics:**
- Training and test error rates as the average of indicator I(yᵢ ≠ ŷᵢ).
- Bayes classifier: assign to argmax_j Pr(Y = j | X = x₀); Bayes decision boundary; Bayes error rate 1 − E[max_j Pr(Y = j | X)] as the irreducible error.
- K-nearest neighbors: estimates conditional class probabilities by neighbor fractions; small K = flexible/low bias/high variance, large K = smooth; training vs test error against 1/K.

### §2.3 — Lab: Introduction to R (pp. 42–52)
**Subtopics:**
- §2.3.1 Basic Commands (p. 42): vectors, matrices, rnorm, set.seed, mean/var/sd.
- §2.3.2 Graphics (p. 45): plot, contour, image, persp.
- §2.3.3 Indexing Data (p. 47): matrix subsetting.
- §2.3.4 Loading Data (p. 48): read.table/read.csv, Auto data, missing values.
- §2.3.5 Additional Graphical and Numerical Summaries (pp. 49–52): boxplots, histograms, pairs, summary.

### §2.4 — Exercises (pp. 52–57)
**Subtopics:**
- Conceptual 1–7 (flexibility, bias–variance curves, parametric vs non-parametric, KNN by hand); Applied 8–10 (College, Auto, Boston data).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

## Ch. 3 — Linear Regression
**Pages:** pp. 59–126

### §3.1 — Simple Linear Regression (pp. 61–71)
**Subtopics:**
- §3.1.1 Estimating the Coefficients (p. 61): least squares minimizes RSS; closed-form β̂₀, β̂₁.
- §3.1.2 Assessing the Accuracy of the Coefficient Estimates (p. 63): population vs least squares line, unbiasedness, SE(β̂₀), SE(β̂₁), 95% CI, t-statistic and p-value for H₀: β₁ = 0.
- §3.1.3 Assessing the Accuracy of the Model (pp. 68–71): residual standard error (RSE) and R²; in simple regression R² = Cor(X, Y)².

### §3.2 — Multiple Linear Regression (pp. 71–82)
**Subtopics:**
- §3.2.1 Estimating the Regression Coefficients (p. 72): multiple vs simple regression coefficients differ (newspaper example: marginal association disappears once radio is controlled).
- §3.2.2 Some Important Questions (pp. 75–82): F-statistic for H₀: all βⱼ = 0 and for subsets of q coefficients; variable selection (forward, backward, mixed; Cp, AIC, BIC, adjusted R²); model fit (RSE, R²); confidence vs prediction intervals.

### §3.3 — Other Considerations in the Regression Model (pp. 82–102)
**Subtopics:**
- §3.3.1 Qualitative Predictors (p. 82): dummy variables, baseline level, coding choices.
- §3.3.2 Extensions of the Linear Model (p. 86): relaxing additivity with interaction terms (synergy), hierarchical principle; polynomial regression for non-linearity.
- §3.3.3 Potential Problems (pp. 92–102): non-linearity (residual plots), correlated errors (time series tracking, understated SEs), heteroscedasticity (funnel shape, log/√Y transforms, weighted least squares), outliers (studentized residuals), high-leverage points (leverage statistic hᵢ), collinearity (VIF).

### §3.4 — The Marketing Plan (pp. 102–104)
**Subtopics:**
- Answers the seven Advertising questions from the chapter opening using the tools of §3.1–3.3.

### §3.5 — Comparison of Linear Regression with K-Nearest Neighbors (pp. 104–109)
**Subtopics:**
- KNN regression vs parametric OLS: OLS wins when the true f is close to linear; KNN degrades as p grows (curse of dimensionality).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §3.6 — Lab: Linear Regression (pp. 109–120)
**Subtopics:**
- §3.6.1 Libraries (p. 109); §3.6.2 Simple Linear Regression (p. 110): lm, confint, predict intervals, diagnostic plots; §3.6.3 Multiple Linear Regression (p. 113): vif; §3.6.4 Interaction Terms (p. 115); §3.6.5 Non-linear Transformations of the Predictors (p. 115): I(X^2), anova comparison, poly; §3.6.6 Qualitative Predictors (p. 117): contrasts; §3.6.7 Writing Functions (pp. 119–120).

### §3.7 — Exercises (pp. 120–126)
**Subtopics:**
- Conceptual 1–7 (p-values, KNN, interactions, training vs test RSS, regression through origin, R² = cor²); Applied 8–15 (Auto, Carseats, simulated data, collinearity, Boston).

## Ch. 4 — Classification
**Pages:** pp. 127–173

### §4.1 — An Overview of Classification (pp. 128–129)
**Subtopics:**
- Qualitative responses; Default data (default as a function of balance and income) as the running example.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §4.2 — Why Not Linear Regression? (pp. 129–130)
**Subtopics:**
- Coding a multi-class response as numbers imposes an arbitrary ordering; for binary 0/1 the linear probability fit estimates Pr(Y = 1 | X) but can fall outside [0, 1].
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §4.3 — Logistic Regression (pp. 130–138)
**Subtopics:**
- Models Pr(Y = 1 | X) directly, keeping predictions inside [0, 1].
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

#### §4.3.1 — The Logistic Model (pp. 131–133)
**Subtopics:**
- Logistic function p(X) = e^{β₀+β₁X}/(1 + e^{β₀+β₁X}); odds p/(1 − p) and log-odds (logit) linear in X; one-unit change in X multiplies the odds by e^{β₁}.

#### §4.3.2 — Estimating the Regression Coefficients (pp. 133–134)
**Subtopics:**
- Maximum likelihood: likelihood ℓ(β₀, β₁) = ∏ p(xᵢ) ∏ (1 − p(xᵢ′)); z-statistics and p-values for coefficients.

#### §4.3.3 — Making Predictions (pp. 134–135)
**Subtopics:**
- Plugging β̂ into the logistic function to get predicted probabilities; dummy predictors (student status).

#### §4.3.4 — Multiple Logistic Regression (pp. 135–137)
**Subtopics:**
- Several predictors; confounding: student coefficient is positive alone but negative once balance is controlled (Simpson-type reversal).

#### §4.3.5 — Logistic Regression for >2 Response Classes (pp. 137–138)
**Subtopics:**
- Multiple-class extensions exist but discriminant analysis is the more popular choice in that case.

### §4.4 — Linear Discriminant Analysis (pp. 138–151)
**Subtopics:**
- Models the class-conditional distribution of X and flips it with Bayes' theorem; preferred when classes are well separated, n is small, or K > 2.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Rules: [[rules/07_bayes|Bayesian inference]]

#### §4.4.1 — Using Bayes' Theorem for Classification (pp. 138–139)
**Subtopics:**
- Posterior Pr(Y = k | X = x) = π_k f_k(x) / Σ_l π_l f_l(x), with prior π_k and class density f_k; plug-in estimates approximate the Bayes classifier.

#### §4.4.2 — Linear Discriminant Analysis for p = 1 (pp. 139–142)
**Subtopics:**
- Gaussian classes with common σ²: discriminant δ_k(x) = x·μ_k/σ² − μ_k²/(2σ²) + log π_k, linear in x; estimates of μ_k, σ², π_k; boundary at (μ₁ + μ₂)/2 when priors are equal.

#### §4.4.3 — Linear Discriminant Analysis for p > 1 (pp. 142–149)
**Subtopics:**
- Multivariate Gaussian with class-specific means and common covariance Σ; linear discriminant functions.
- Confusion matrix on the Default data; trivial null classifier benchmark; sensitivity vs specificity; lowering the posterior threshold below 0.5 trades overall error for fewer missed defaulters.
- ROC curve and AUC as threshold-free summaries; false/true positive rates, precision terminology (Tables 4.6–4.7).

#### §4.4.4 — Quadratic Discriminant Analysis (pp. 149–151)
**Subtopics:**
- Class-specific covariance Σ_k gives quadratic boundaries; LDA vs QDA as a bias–variance trade-off (Kp(p+1)/2 covariance parameters).

### §4.5 — A Comparison of Classification Methods (pp. 151–154)
**Subtopics:**
- Logistic regression vs LDA (same linear log-odds, different fitting); KNN (non-parametric, no coefficients) vs QDA (middle ground); six simulated scenarios showing when each wins.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §4.6 — Lab: Logistic Regression, LDA, QDA, and KNN (pp. 154–168)
**Subtopics:**
- §4.6.1 The Stock Market Data (p. 154): Smarket data.
- §4.6.2 Logistic Regression (p. 156): glm(family = binomial), predicted probabilities, confusion matrix, training vs held-out 2005 data.
- §4.6.3 Linear Discriminant Analysis (p. 161): lda(), posterior thresholds.
- §4.6.4 Quadratic Discriminant Analysis (p. 163): qda().
- §4.6.5 K-Nearest Neighbors (p. 163): knn() from class.
- §4.6.6 An Application to Caravan Insurance Data (pp. 165–168): standardizing predictors for KNN; precision among predicted buyers; logistic threshold 0.25.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §4.7 — Exercises (pp. 168–173)
**Subtopics:**
- Conceptual 1–9 (logit equivalence, LDA/QDA derivations, curse of dimensionality, odds, Bayes theorem); Applied 10–13 (Weekly, Auto, R functions, Boston).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

## Ch. 5 — Resampling Methods
**Pages:** pp. 175–201

### §5.1 — Cross-Validation (pp. 176–187)
**Subtopics:**
- Model assessment (estimating test error) vs model selection (choosing flexibility).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

#### §5.1.1 — The Validation Set Approach (pp. 176–178)
**Subtopics:**
- Random split into training and validation halves; drawbacks: high variability across splits and overestimation of test error (fits on fewer observations).

#### §5.1.2 — Leave-One-Out Cross-Validation (pp. 178–181)
**Subtopics:**
- CV₍ₙ₎ = (1/n) Σ MSEᵢ; less bias, no split randomness; least-squares shortcut CV₍ₙ₎ = (1/n) Σ [(yᵢ − ŷᵢ)/(1 − hᵢ)]² using leverage.

#### §5.1.3 — k-Fold Cross-Validation (pp. 181–183)
**Subtopics:**
- CV₍k₎ = (1/k) Σ MSEᵢ over k folds (k = 5 or 10); cheaper than LOOCV; locating the minimum of the test MSE curve matters more than its level.

#### §5.1.4 — Bias-Variance Trade-Off for k-Fold Cross-Validation (pp. 183–184)
**Subtopics:**
- LOOCV is nearly unbiased but has higher variance (averaged fits are highly correlated); k = 5 or 10 balances the two.

#### §5.1.5 — Cross-Validation on Classification Problems (pp. 184–187)
**Subtopics:**
- CV error as the average misclassification indicator Errᵢ = I(yᵢ ≠ ŷᵢ); choosing polynomial degree in logistic regression and K in KNN; training error is a poor guide.

### §5.2 — The Bootstrap (pp. 187–190)
**Subtopics:**
- Resampling with replacement to approximate the sampling distribution of an estimator; portfolio example α = (σ²_Y − σ_XY)/(σ²_X + σ²_Y − 2σ_XY).
- Bootstrap standard error SE_B(α̂) as the standard deviation of B bootstrap replicates; comparison with the "true" simulation-based SE.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §5.3 — Lab: Cross-Validation and the Bootstrap (pp. 190–197)
**Subtopics:**
- §5.3.1 The Validation Set Approach (p. 191): sample() split, polynomial fits on Auto.
- §5.3.2 Leave-One-Out Cross-Validation (p. 192): cv.glm(), delta.
- §5.3.3 k-Fold Cross-Validation (p. 193): cv.glm(K = 10).
- §5.3.4 The Bootstrap (pp. 194–197): boot() for the statistic α and for linear-regression coefficient SEs; bootstrap SEs vs formula SEs when model assumptions fail.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §5.4 — Exercises (pp. 197–201)
**Subtopics:**
- Conceptual 1–4 (α derivation, bootstrap inclusion probability, k-fold CV, prediction SD); Applied 5–9 (Default, Weekly, simulated data, Boston).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

## Ch. 6 — Linear Model Selection and Regularization
**Pages:** pp. 203–264

### §6.1 — Subset Selection (pp. 205–214)
**Subtopics:**
- background: best subset, forward/backward/hybrid stepwise; choosing the model via Cp, AIC, BIC, adjusted R² or validation/CV (one-standard-error rule).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §6.2 — Shrinkage Methods (pp. 214–228)
**Subtopics:**
- background: ridge (ℓ₂) and lasso (ℓ₁) penalties, variable selection by the lasso, Bayesian interpretation (Gaussian vs Laplace prior), tuning λ by cross-validation.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §6.3 — Dimension Reduction Methods (pp. 228–238)
**Subtopics:**
- background: principal components regression and partial least squares.

### §6.4 — Considerations in High Dimensions (pp. 238–244)
**Subtopics:**
- background: p > n, failure of least squares and of R²/training error, regularization in high dimensions.

### §6.5 — Lab 1: Subset Selection Methods (pp. 244–251)
**Subtopics:**
- background: regsubsets, stepwise, choosing models by validation set and CV.

### §6.6 — Lab 2: Ridge Regression and the Lasso (pp. 251–256)
**Subtopics:**
- background: glmnet, cv.glmnet.

### §6.7 — Lab 3: PCR and PLS Regression (pp. 256–259)
**Subtopics:**
- background: pcr(), plsr().

## Ch. 7 — Moving Beyond Linearity
**Pages:** pp. 265–301

### §7.1 — Polynomial Regression (pp. 266–268)
**Subtopics:**
- background: polynomial terms in linear and logistic regression; pointwise SE bands.

### §7.2 — Step Functions (pp. 268–270)
**Subtopics:**
- background: piecewise-constant fits via cutpoints/indicator variables.

### §7.3 — Basis Functions (pp. 270–271)
**Subtopics:**
- background: polynomials and step functions as fixed basis expansions fit by least squares.

### §7.4 — Regression Splines (pp. 271–277)
**Subtopics:**
- background: piecewise polynomials, continuity constraints, cubic and natural splines, knot placement by CV.

### §7.5 — Smoothing Splines (pp. 277–280)
**Subtopics:**
- background: roughness penalty, effective degrees of freedom, λ chosen by LOOCV.

### §7.6 — Local Regression (pp. 280–282)
**Subtopics:**
- background: locally weighted fits with span s.

### §7.7 — Generalized Additive Models (pp. 282–287)
**Subtopics:**
- background: additive non-linear functions of each predictor, for regression and logistic classification.

### §7.8 — Lab: Non-linear Modeling (pp. 287–297)
**Subtopics:**
- background: poly(), anova model comparison, bs()/ns(), smooth.spline, loess, gam().

## Ch. 8 — Tree-Based Methods
**Pages:** pp. 303–335

### §8.1 — The Basics of Decision Trees (pp. 303–316)
**Subtopics:**
- background: regression and classification trees, recursive binary splitting, cost-complexity pruning, Gini index and entropy.

### §8.2 — Bagging, Random Forests, Boosting (pp. 316–324)
**Subtopics:**
- background: bagging (bootstrap aggregation) with out-of-bag error, random forests (m ≈ √p), boosting.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §8.3 — Lab: Decision Trees (pp. 324–332)
**Subtopics:**
- background: tree(), cv.tree(), randomForest(), gbm().

## Ch. 9 — Support Vector Machines
**Pages:** pp. 337–372

### §9.1 — Maximal Margin Classifier (pp. 338–344)
**Subtopics:**
- background: hyperplanes, separating hyperplane, maximal margin, support vectors.

### §9.2 — Support Vector Classifiers (pp. 344–349)
**Subtopics:**
- background: soft margin with budget C, slack variables.

### §9.3 — Support Vector Machines (pp. 349–355)
**Subtopics:**
- background: kernels (polynomial, radial) for non-linear boundaries; Heart data ROC comparison.

### §9.4 — SVMs with More than Two Classes (pp. 355–356)
**Subtopics:**
- background: one-versus-one and one-versus-all.

### §9.5 — Relationship to Logistic Regression (pp. 356–359)
**Subtopics:**
- background: hinge loss vs logistic loss in a loss + penalty form.

### §9.6 — Lab: Support Vector Machines (pp. 359–368)
**Subtopics:**
- background: svm(), tune(); §9.6.3 ROC Curves (p. 365) with ROCR.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

## Ch. 10 — Unsupervised Learning
**Pages:** pp. 373–418

### §10.1 — The Challenge of Unsupervised Learning (pp. 373–374)
**Subtopics:**
- background: no response, no direct validation.

### §10.2 — Principal Components Analysis (pp. 374–385)
**Subtopics:**
- background: loadings and scores, scaling, proportion of variance explained, scree plot.

### §10.3 — Clustering Methods (pp. 385–401)
**Subtopics:**
- background: K-means, hierarchical clustering (dendrograms, linkage, dissimilarity measures), practical issues.

### §10.4 — Lab 1: Principal Components Analysis (pp. 401–404)
**Subtopics:**
- background: prcomp(), biplot.

### §10.5 — Lab 2: Clustering (pp. 404–407)
**Subtopics:**
- background: kmeans(), hclust().

### §10.6 — Lab 3: NCI60 Data Example (pp. 407–413)
**Subtopics:**
- background: PCA and clustering on gene-expression data.




# Greenberg, Introduction to Bayesian Econometrics, 1e
#book/greenberg
> Link: [[Livros/Edward Greenberg - Introduction to Bayesian Econometrics (2007, Cambridge University Press) - libgen.li|Greenberg 1e]]
> Page offset: printed = PDF page − 15 (verified from printed folios: PDF 18 = p. 3, PDF 56 = p. 41, PDF 126 = p. 111)
> Edition note: the syllabus names the 2nd ed. (2012); this 1st ed. (Cambridge UP, 2008) is the substitute. Page numbers below are 1st-edition printed pages.
> Coverage note: no Kalman filter by name and no sequential Monte Carlo / particle filter anywhere in the book; state-space models (§10.2–10.3) are handled entirely by Gibbs sampling.

## Part I — Fundamentals of Bayesian Inference (p. 1)

## Ch. 1 — Introduction
**Pages:** pp. 3–6

### §1.1 — Econometrics (pp. 3–4)
**Subtopics:**
- econometrics as inference: regressors, response variables, and the role of probability models for economic data.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §1.2 — Plan of the Book (pp. 4–5)
**Subtopics:**
- roadmap: fundamentals (Part I), simulation by MCMC (Part II), applications (Part III).

### §1.3 — Historical Note and Further Reading (pp. 5–6)
**Subtopics:**
- history of Bayesian statistics: Bayes, Laplace, Jeffreys, Zellner, and the MCMC revolution of the early 1990s.

## Ch. 2 — Basic Concepts of Probability and Inference
**Pages:** pp. 7–19

### §2.1 — Probability (pp. 7–12)
**Subtopics:**
- §2.1.1 frequentist probabilities (pp. 8–9): probability as the limit of relative frequencies in repeated trials, and its limits for one-off events.
- §2.1.2 subjective probabilities (pp. 9–12): probability as degree of belief, coherency and the Dutch-book (betting) argument for the probability axioms.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §2.2 — Prior, Likelihood, and Posterior (pp. 12–18)
**Subtopics:**
- Bayes' theorem: posterior ∝ likelihood × prior, π(θ|y) ∝ f(y|θ)π(θ).
- likelihood function: the data density read as a function of θ.
- prior distribution and hyperparameters.
- beta-binomial conjugate analysis: coin-tossing (Bernoulli) example with a beta prior and beta posterior.
- posterior mean as a weighted average of the prior mean and the MLE.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §2.3 — Summary (pp. 18–19)
**Subtopics:**
- recap: subjective probability and the Bayesian updating rule.

### §2.4 — Further Reading and References (p. 19)
**Subtopics:**
- references on subjective probability (Howson and Urbach; Hacking).

### §2.5 — Exercises (p. 19)
**Subtopics:**
- exercises 2.1–2.4: the addition rule via coherency, and conjugate priors (gamma–Poisson, gamma–exponential, Pareto–uniform). See [[greenberg-exercises]].

## Ch. 3 — Posterior Distributions and Inference
**Pages:** pp. 20–40

### §3.1 — Properties of Posterior Distributions (pp. 20–29)
**Subtopics:**
- §3.1.1 the likelihood function (pp. 20–22): choosing a likelihood, and Jaynes's maximum-entropy argument for normality.
- §3.1.2 vectors of parameters (pp. 22–24): joint and marginal posterior distributions, and the Dirichlet–multinomial model.
- §3.1.3 Bayesian updating (pp. 24–25): sequential Bayes, where today's posterior is tomorrow's prior, and batch and sequential updating give the same result.
- §3.1.4 large samples (pp. 25–28): as n grows the likelihood dominates the prior, and the posterior concentrates around the MLE with an approximately normal shape.
- §3.1.5 identification (pp. 28–29): for unidentified parameters the data do not update the prior (the conditional posterior equals the conditional prior).
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §3.2 — Inference (pp. 29–38)
**Subtopics:**
- §3.2.1 point estimates (pp. 29–31): Bayes estimators under loss functions (quadratic → posterior mean, absolute → median, zero–one → mode), contrasted with frequentist estimator criteria.
- §3.2.2 interval estimates (pp. 31–32): credibility intervals and highest posterior density intervals.
- §3.2.3 prediction (pp. 32–33): the posterior predictive distribution f(y_{n+1}|y) = ∫ f(y_{n+1}|θ) π(θ|y) dθ.
- §3.2.4 model comparison (pp. 33–38): marginal likelihood, Bayes factors, posterior odds, Jeffreys's scale of evidence, and how sample size and parameter dimension affect the Bayes factor.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §3.3 — Summary (p. 38)
**Subtopics:**
- recap of posterior properties and of point, interval, predictive and model-comparison inference.

### §3.4 — Further Reading and References (pp. 38–39)
**Subtopics:**
- critiques of hypothesis testing, and Bayes factors versus AIC and the Schwarz criterion (O'Hagan).

### §3.5 — Exercises (pp. 39–40)
**Subtopics:**
- exercises 3.1–3.8: Dirichlet posteriors, predictive distributions, updating, loss functions, Bayes factors. See [[greenberg-exercises]].

## Ch. 4 — Prior Distributions
**Pages:** pp. 41–59

### §4.1 — Normal Linear Regression Model (pp. 41–43)
**Subtopics:**
- normal linear regression likelihood: y ~ N_n(Xβ, σ²I), with an exogeneity assumption on the covariates.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §4.2 — Proper and Improper Priors (pp. 43–44)
**Subtopics:**
- improper (flat, Jeffreys-type) priors: they can still give a proper posterior, but they are not usable for Bayes factors.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §4.3 — Conjugate Priors (pp. 44–47)
**Subtopics:**
- normal-inverse-gamma conjugate prior for (β, σ²): N_K(β̄, σ²B₁) × IG(α₁/2, δ₁/2) posterior.
- analytic marginal posteriors: σ²|y is inverse gamma and β|y is multivariate Student-t, the last analytically tractable model in the book.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §4.4 — Subject-Matter Considerations (pp. 47–50)
**Subtopics:**
- eliciting priors from economic theory and earlier studies: union wage premium example (Vella–Verbeek data).
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §4.5 — Exchangeability (pp. 50–52)
**Subtopics:**
- exchangeability and de Finetti's representation theorem as a justification for priors.
- heteroskedastic regression: u_i|λ_i ~ N(0, σ²/λ_i) with λ_i ~ G(ν/2, ν/2), which gives Student-t errors as a scale mixture of normals.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Rules: [[rules/03_painel_did|Panel data & DiD]]

### §4.6 — Hierarchical Models (pp. 52–53)
**Subtopics:**
- hierarchical priors: the hyperparameters receive their own prior (for example a prior on the t degrees of freedom ν), and hyperparameters are not identified by the data.
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
- Rules: [[rules/07_bayes|Bayesian inference]]

### §4.7 — Training Sample Priors (pp. 53–54)
**Subtopics:**
- training-sample priors: part of the data is used to form the prior for the rest.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §4.8 — Sensitivity and Robustness (p. 54)
**Subtopics:**
- prior sensitivity analysis: how the union coefficient changes with the prior mean and variance (Table 4.1).
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §4.9 — Conditionally Conjugate Priors (pp. 54–56)
**Subtopics:**
- independent normal and inverse-gamma priors: β|σ²,y is normal and σ²|β,y is inverse gamma, but the joint posterior is non-standard, which motivates the Gibbs sampler.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §4.10 — A Look Ahead (pp. 56–57)
**Subtopics:**
- why non-standard posteriors call for simulation methods (Part II).

### §4.11 — Further Reading and References (pp. 57–58)
**Subtopics:**
- references on prior elicitation, exchangeability and hierarchical models.

### §4.12 — Exercises (pp. 58–59)
**Subtopics:**
- exercises 4.1–4.7: normal-inverse-gamma algebra, diffuse-prior limits, analytic marginal likelihood, exchangeability. See [[greenberg-exercises]].

## Part II — Simulation (p. 61)

## Ch. 5 — Classical Simulation
**Pages:** pp. 63–75

### §5.1 — Probability Integral Transformation Method (pp. 63–65)
**Subtopics:**
- inverse-CDF method (Algorithm 5.1): X = F⁻¹(U) with U ~ U(0,1), including draws from a truncated distribution.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §5.2 — Method of Composition (pp. 65–66)
**Subtopics:**
- method of composition: draw from a mixture or marginal by first drawing the mixing variable and then the conditional.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §5.3 — Accept–Reject Algorithm (pp. 66–70)
**Subtopics:**
- accept–reject (Algorithm 5.2): a majorizing (dominating) density and a constant c; examples are the Beta (Algorithm 5.3), normal (Algorithm 5.4) and truncated exponential (Algorithm 5.5) distributions.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §5.4 — Importance Sampling (pp. 70–72)
**Subtopics:**
- importance sampling: weighting draws from an importance function, illustrated by bivariate normal rectangle probabilities with a truncated-normal importance density, which is the precursor of GHK.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §5.5 — Multivariate Simulation (p. 72)
**Subtopics:**
- multivariate normal draws via the Cholesky factor.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §5.6 — Using Simulated Output (pp. 72–74)
**Subtopics:**
- Monte Carlo integration: posterior means, quantiles and histograms from draws, and the numerical standard error (n.s.e.) √(Var/G) for i.i.d. draws.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §5.7 — Further Reading and References (pp. 74–75)
**Subtopics:**
- references (Devroye, Robert–Casella), and the GHK algorithm (Geweke–Hajivassiliou–Keane).

### §5.8 — Exercises (p. 75)
**Subtopics:**
- exercises 5.1–5.7: inverse CDF, composition, accept–reject, importance sampling. See [[greenberg-exercises]].

## Ch. 6 — Basics of Markov Chains
**Pages:** pp. 76–89

### §6.1 — Finite State Spaces (pp. 76–81)
**Subtopics:**
- Markov property and homogeneous chains: the transition matrix P and n-step transitions Pⁿ.
- invariant distribution π′ = π′P (an eigenvector with unit root), accessibility, communication, irreducibility and periodicity.
- convergence theorems: Theorems 6.1–6.2, where an irreducible aperiodic finite chain has Pⁿ → 1π′.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §6.2 — Countable State Spaces (pp. 81–85)
**Subtopics:**
- random walk chains, recurrence, transience and positive recurrence (Theorems 6.3–6.4).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §6.3 — Continuous State Spaces (pp. 85–87)
**Subtopics:**
- transition kernels and invariant densities, π-irreducibility, Harris recurrence, and total-variation convergence (Theorems 6.5–6.7), plus the burn-in period.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §6.4 — Further Reading and References (p. 87)
**Subtopics:**
- references (Norris; Meyn and Tweedie; Bhattacharya and Waymire).

### §6.5 — Exercises (pp. 87–89)
**Subtopics:**
- exercises 6.1–6.8: state classification, invariant distributions, simulated chains, convergence speed via eigenvalues, gambler's ruin. See [[greenberg-exercises]].

## Ch. 7 — Simulation by MCMC Methods
**Pages:** pp. 90–107

### §7.1 — Gibbs Algorithm (pp. 91–96)
**Subtopics:**
- §7.1.1 basic algorithm (pp. 91–95): the Gibbs sampler with two blocks (Algorithm 7.1) and d blocks (Algorithm 7.2); convergence conditions (Theorem 7.1); normal mean and precision example (Algorithm 7.3); the Poisson switch-point model.
- §7.1.2 calculation of marginal likelihood (pp. 95–96): Chib's method, f(y) = f(y|θ*)π(θ*)/π(θ*|y), with π(θ*|y) estimated from Gibbs output (Rao–Blackwellization).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (related, not assigned): the Poisson switch-point model is the "next step" of the coal-mining deck
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Rules: [[rules/07_bayes|Bayesian inference]]

### §7.2 — Metropolis–Hastings Algorithm (pp. 96–102)
**Subtopics:**
- §7.2.1 basic algorithm (pp. 96–101): Metropolis–Hastings (Algorithm 7.4) with acceptance probability α(x,y) and detailed balance (Theorem 7.2); random-walk and independence proposals; tailored proposals; Beta(3,4) example (Algorithm 7.5); MH within blocks (Algorithm 7.6); Gibbs as a special case of MH.
- §7.2.2 calculation of marginal likelihood (pp. 101–102): the Chib–Jeliazkov extension of Chib's method to MH output.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Rules: [[rules/07_bayes|Bayesian inference]]

### §7.3 — Numerical Standard Errors and Convergence (pp. 102–103)
**Subtopics:**
- MCMC numerical standard errors: autocorrelation-adjusted n.s.e., batch means, inefficiency factor, autocorrelation time, relative numerical efficiency.
- convergence diagnostics: burn-in, trace and autocorrelation plots, and the coda software.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §7.4 — Further Reading and References (pp. 103–105)
**Subtopics:**
- data augmentation and Gibbs history (Tanner–Wong, Gelfand–Smith), Rao–Blackwellizing, ARMH, Tierney (1994), and Robert and Casella on convergence.

### §7.5 — Exercises (pp. 105–107)
**Subtopics:**
- exercises 7.1–7.8: Gibbs for normal and switch-point models, random-walk and independence MH, tailored MH-within-Gibbs. See [[greenberg-exercises]].

## Part III — Applications (p. 109)

## Ch. 8 — Linear Regression and Extensions
**Pages:** pp. 111–133

### §8.1 — Continuous Dependent Variables (pp. 111–117)
**Subtopics:**
- §8.1.1 normally distributed errors (pp. 111–114): Gibbs sampler for the normal linear regression model under the conditionally conjugate prior (Algorithm 8.1), with union-data results and autocorrelation diagnostics.
- §8.1.2 Student-t distributed errors (pp. 114–117): data augmentation with latent precisions λ_i ~ G(ν/2, ν/2) (scale mixture of normals) in a three-block Gibbs sampler, with model comparison by marginal likelihood.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §8.2 — Limited Dependent Variables (pp. 117–129)
**Subtopics:**
- §8.2.1 Tobit model for censored data (pp. 117–122): Gibbs with latent y* drawn from truncated normals (Chib 1992; Algorithm 8.2), Mroz data.
- §8.2.2 binary probit model (pp. 122–126): the Albert–Chib data-augmentation Gibbs sampler (Algorithm 8.3), with latent utilities drawn from truncated normals.
- §8.2.3 binary logit model (pp. 126–129): the posterior has no conjugate or latent-data simplification, so it is sampled by Metropolis–Hastings with random-walk or independence proposals.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §8.3 — Further Reading and References (pp. 129–132)
**Subtopics:**
- references on Student-t links, ordered models, and the ideal-point (Clinton et al.) model.

### §8.4 — Exercises (pp. 132–133)
**Subtopics:**
- exercises 8.1–8.10: regression applications, t errors, Tobit/probit with t errors, logit, Poisson count model. See [[greenberg-exercises]].

## Ch. 9 — Multivariate Responses
**Pages:** pp. 134–152

### §9.1 — SUR Model (pp. 134–139)
**Subtopics:**
- seemingly unrelated regressions (Zellner): Gibbs with a normal prior for β and a Wishart prior for Σ⁻¹ (Algorithm 9.1), Grunfeld investment data, and model comparison by marginal likelihood.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Rules: [[rules/07_bayes|Bayesian inference]]

### §9.2 — Multivariate Probit Model (pp. 139–144)
**Subtopics:**
- multivariate probit: latent-data SUR with correlation-matrix identification, MH for the correlations with a tailored proposal (Algorithm 9.2).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §9.3 — Panel Data (pp. 144–149)
**Subtopics:**
- Bayesian panel model with fixed and random effects: y_i = X_iβ + W_ib_i + u_i, b_i ~ N(0, D) as a hierarchical model, with the Mundlak connection.
- Chib–Carlin Gibbs sampler (Algorithm 9.3): β drawn marginalized over b_i, a Wishart draw for D⁻¹, Vella–Verbeek union data.
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §9.4 — Further Reading and References (pp. 149–151)
**Subtopics:**
- ordered probit, multinomial and mixed probit and logit, and panel references (Arellano, Hsiao, Baltagi, Chib).

### §9.5 — Exercises (pp. 151–152)
**Subtopics:**
- exercises 9.1–9.5: SUR with t errors, binary and censored panel models, panel with t effects, multivariate logit. See [[greenberg-exercises]].

## Ch. 10 — Time Series
**Pages:** pp. 153–167

### §10.1 — Autoregressive Models (pp. 153–158)
**Subtopics:**
- regression with AR(p) errors: stationarity restriction, exact likelihood with the initial-observations block Σ_p, a state-space form for the AR(p) model.
- MH-within-Gibbs for (β, σ², φ): β is normal and σ⁻² is gamma; φ comes from a normal proposal, with non-stationary draws rejected, followed by an MH step; expectations-augmented Phillips curve with a training-sample prior; AR(1) versus independent errors compared by marginal likelihood.
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §10.2 — Regime-Switching Models (pp. 158–161)
**Subtopics:**
- Hamilton hidden Markov (Markov-switching) model: discrete prediction and update filter steps, then states drawn by backward sampling of p(s_t|Y_t, s_{t+1}) (Albert–Chib, Chib 1996); label switching resolved by the restriction μ₁ > 0; recession probabilities for US GDP.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §10.3 — Time-Varying Parameters (pp. 161–165)
**Subtopics:**
- state-space time-varying-parameter regression: random-walk coefficients β_t, with a joint draw of all β_t (and a note on recursive sampling for large KT), Phillips-curve example; no Kalman filter is derived.
**Linked materials:**
- Rules: [[rules/05_espaco_estados_volatilidade|State space & volatility]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §10.4 — Time Series Properties of Models for Panel Data (pp. 165–166)
**Subtopics:**
- dynamic panel model y_it = β₁y_{i,t−1} + b_i + u_it, recast as the static model of §9.3 with |β₁| < 1, and panel models with autocorrelated errors (Chib).
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]]
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]]

### §10.5 — Further Reading and References (pp. 166–167)
**Subtopics:**
- state-space references (Carlin et al., Carter–Kohn, Frühwirth-Schnatter, de Jong–Shephard, Kim–Nelson), and label switching.

### §10.6 — Exercises (p. 167)
**Subtopics:**
- exercises 10.1–10.4: AR(p) state-space form, AR(p) predictive distribution, SUR with AR(1) errors. See [[greenberg-exercises]].

## Ch. 11 — Endogenous Covariates and Sample Selection
**Pages:** pp. 168–181

### §11.1 — Treatment Models (pp. 168–173)
**Subtopics:**
- potential outcomes y₀ᵢ, y₁ᵢ with a binary treatment sᵢ, average treatment effect ATE = x′(β₁ − β₀), and confounders.
- Chib's Gibbs algorithm for the treatment model (Algorithm 11.1): latent probit assignment equation, without modelling the unidentified correlation of u₀ᵢ and u₁ᵢ.
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]

### §11.2 — Endogenous Covariates (pp. 173–175)
**Subtopics:**
- Bayesian instrumental variables: a jointly normal (u, x_s) structure, the identification problem (only β_s + σ₁₂/σ₂₂ is identified without instruments), and a Gibbs sampler with a Wishart prior on Σ.
**Linked materials:**
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]

### §11.3 — Incidental Truncation (pp. 175–179)
**Subtopics:**
- Bayesian Heckman sample-selection model: latent selection equation s* with an exclusion-restriction instrument z, Gibbs sampling with latent data, Mroz wage data.
**Linked materials:**
- Rules: [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]
- Rules: [[rules/01_endogeneidade_iv|Endogeneity & IV]]

### §11.4 — Further Reading and References (pp. 179–180)
**Subtopics:**
- references: Heckman–Vytlacil (treatment effects), Poirier–Tobias, Wooldridge, Heckman (1979).

### §11.5 — Exercises (pp. 180–181)
**Subtopics:**
- exercises 11.1–11.8: verifying conditionals, and binary, Student-t and Tobit variants of the treatment, IV and selection models. See [[greenberg-exercises]].

## Appendix A — Probability Distributions and Matrix Theorems
**Pages:** pp. 182–191

### §A.1 — Probability Distributions (pp. 182–191)
**Subtopics:**
- distribution reference: Bernoulli, binomial, negative binomial, multinomial, Poisson, uniform, gamma, inverse gamma, beta, Dirichlet, normal, multivariate and matricvariate normal (marginals, conditionals, completing the square), truncated normal, univariate and multivariate t, Wishart, inverse Wishart, and the multiplication rule.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §A.2 — Matrix Theorems (p. 191)
**Subtopics:**
- background: partitioned inverse, the Woodbury-type identity (A.18) used in conjugate derivations, and vec/Kronecker rules.

## Appendix B — Computer Programs for MCMC Calculations
**Pages:** pp. 192–193

### §B — Computer Programs (pp. 192–193)
**Subtopics:**
- background: programming MCMC in Matlab/Gauss (parameterization pitfalls for the gamma, inverse-gamma and normal distributions) and free Gibbs software such as BACC.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]


# James, Witten, Hastie, Tibshirani & Taylor, An Introduction to Statistical Learning with Applications in Python (ISLP), 2023
#book/islp
> Link: [[Livros/James, Witten, Hastie, Tibshirani, Taylor - An Introduction to Statistical Learning with Applications in Python (2023)|ISLP]]

> Page numbers are printed book pages (from the book's table of contents, checked against the running heads with pdftotext). First printing, July 5, 2023. The PDF drops the blank page before most chapter openers, so the PDF-to-printed offset drifts: 1-based PDF page − 11 (ch. 1), − 10 (ch. 2), − 9 (ch. 3–4), − 8 (ch. 5–7), − 7 (ch. 8–10), − 6 (ch. 11–13 and the index).

**Differences from ISLR 1e** (section numbers below are ISLP's):
- Ch. 2–3: same section numbers; page numbers shift down (e.g. §2.2 starts p. 27, not p. 29). The labs are rewritten in Python: §2.3 now has nine subsections (§2.3.1 Getting Started … §2.3.9), §3.6 adds §3.6.4 Multivariate Goodness of Fit and drops Writing Functions.
- Ch. 4: §4.3.5 becomes "Multinomial Logistic Regression" (baseline and softmax coding). §4.4 is renamed "Generative Models for Classification": the 1e §4.4.1 (Bayes' theorem) is folded into the §4.4 introduction, so LDA p = 1 is §4.4.1 (1e §4.4.2), LDA p > 1 is §4.4.2 (1e §4.4.3), QDA is §4.4.3 (1e §4.4.4), and §4.4.4 Naive Bayes is new. §4.5 splits into §4.5.1 An Analytical Comparison and §4.5.2 An Empirical Comparison. **§4.6 Generalized Linear Models (Poisson regression, Bikeshare data) is new.** The lab moves from §4.6 to §4.7 (adds Naive Bayes and Bikeshare linear/Poisson regression) and the exercises from §4.7 to §4.8.
- Ch. 5: same section numbers; in the lab, LOOCV and k-fold are merged into §5.3.2 Cross-Validation, so the bootstrap lab is §5.3.3 (1e §5.3.4).
- Ch. 6: the three labs (1e §6.5–6.7) are merged into one §6.5 Lab: Linear Models and Regularization Methods (§6.5.1–6.5.3), so the exercises move from 1e §6.8 to §6.6.
- Ch. 7: same section numbers; lab §7.8 is reorganised into four subsections; exercises remain §7.9.
- Ch. 8: §8.2 adds §8.2.4 Bayesian Additive Regression Trees and §8.2.5 Summary of Tree Ensemble Methods.
- New chapters: Ch. 10 Deep Learning, Ch. 11 Survival Analysis and Censored Data, Ch. 13 Multiple Testing. Unsupervised learning moves from 1e Ch. 10 to Ch. 12 (PCA 1e §10.2 → §12.2; new §12.3 Missing Values and Matrix Completion; clustering 1e §10.3 → §12.4).

## Ch. 1 — Introduction
**Pages:** pp. 1–13

## Ch. 2 — Statistical Learning
**Pages:** pp. 15–67

### §2.1 — What Is Statistical Learning? (pp. 15–27)
**Subtopics:**
- Model Y = f(X) + ε (2.1): statistical learning as estimating the systematic part f from data; ε is mean-zero error independent of X.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §2.1.1 — Why Estimate f? (pp. 17–20)
**Subtopics:**
- Prediction vs inference: prediction treats f̂ as a black box (2.2); inference asks which predictors matter and how.
- Reducible vs irreducible error (2.3): E(Y − Ŷ)² = [f(X) − f̂(X)]² + Var(ε); Var(ε) bounds achievable accuracy.

#### §2.1.2 — How Do We Estimate f? (pp. 20–23)
**Subtopics:**
- Parametric methods: assume a functional form, e.g. linear (2.4), and fit by least squares; risk of misspecification.
- Non-parametric methods: thin-plate splines need no form assumption but need many observations; overfitting the noise.

#### §2.1.3 — The Trade-Off Between Prediction Accuracy and Model Interpretability (pp. 23–25)
**Subtopics:**
- Flexibility vs interpretability: subset selection/lasso and least squares (interpretable, rigid) vs GAMs, trees, bagging, boosting, SVMs and deep learning (flexible, opaque); flexible is not always more accurate.

#### §2.1.4 — Supervised Versus Unsupervised Learning (pp. 25–27)
**Subtopics:**
- Supervised (response observed) vs unsupervised (no response; e.g. cluster analysis) vs semi-supervised settings.

#### §2.1.5 — Regression Versus Classification Problems (p. 27)
**Subtopics:**
- Quantitative vs qualitative responses; method choice depends on the response type more than on the predictor type.

### §2.2 — Assessing Model Accuracy (pp. 27–40)
**Subtopics:**
- No free lunch: no single method dominates on all data sets, so model selection is needed.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §2.2.1 — Measuring the Quality of Fit (pp. 28–31)
**Subtopics:**
- Training MSE (2.5) vs test MSE Ave(y₀ − f̂(x₀))² (2.6): training MSE falls monotonically with flexibility, test MSE is U-shaped; overfitting defined by this gap.
- Degrees of freedom as a summary of flexibility; cross-validation previewed as the way to estimate test MSE.

#### §2.2.2 — The Bias-Variance Trade-Off (pp. 31–34)
**Subtopics:**
- Bias–variance decomposition (2.7): E(y₀ − f̂(x₀))² = Var(f̂(x₀)) + [Bias(f̂(x₀))]² + Var(ε).
- More flexible methods have higher variance and lower bias; the U-shaped test MSE is the net effect.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §2.2.3 — The Classification Setting (pp. 34–40)
**Subtopics:**
- Training error rate (1/n) Σ I(yᵢ ≠ ŷᵢ) (2.8) and test error rate Ave(I(y₀ ≠ ŷ₀)) (2.9).
- Bayes classifier: assign to argmax_j Pr(Y = j | X = x₀) (2.10); Bayes decision boundary; Bayes error rate 1 − E[max_j Pr(Y = j | X)] (2.11) as the irreducible error.
- K-nearest neighbors (2.12): estimates conditional class probabilities by neighbor fractions; small K = flexible/low bias/high variance, large K = smooth; training vs test error against 1/K.

### §2.3 — Lab: Introduction to Python (pp. 40–63)
**Subtopics:**
- §2.3.1 Getting Started (p. 40): Ch2-statlearn-lab.ipynb, Jupyter.
- §2.3.2 Basic Commands (p. 40): print(), lists, strings.
- §2.3.3 Introduction to Numerical Python (p. 42): numpy arrays, shape, sum, np.corrcoef(), random draws with np.random.default_rng(), mean/var/std.
- §2.3.4 Graphics (p. 48): matplotlib subplots(), scatter, contour, imshow.
- §2.3.5 Sequences and Slice Notation (p. 51): np.linspace(), np.arange(), slices.
- §2.3.6 Indexing Data (p. 51): row/column indexing with lists, np.ix_(), Boolean indexing.
- §2.3.7 Loading Data (p. 55): pd.read_csv(), Auto data, missing values, dropna(), loc[] and iloc[].
- §2.3.8 For Loops (p. 59): loops, zip(), string formatting.
- §2.3.9 Additional Graphical and Numerical Summaries (pp. 61–63): boxplots, histograms, scatter_matrix(), describe().
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §2.4 — Exercises (pp. 63–67)
**Subtopics:**
- Conceptual 1–7 (flexibility, bias–variance curves, parametric vs non-parametric, KNN by hand); Applied 8–10 (College, Auto, Boston data, in pandas).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

## Ch. 3 — Linear Regression
**Pages:** pp. 69–134

### §3.1 — Simple Linear Regression (pp. 70–80)
**Subtopics:**
- Model Y ≈ β₀ + β₁X (3.1) fit by least squares on the Advertising data.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §3.1.1 — Estimating the Coefficients (pp. 71–72)
**Subtopics:**
- Least squares minimizes RSS (3.3); closed-form β̂₁ = Σ(xᵢ − x̄)(yᵢ − ȳ)/Σ(xᵢ − x̄)², β̂₀ = ȳ − β̂₁x̄ (3.4).

#### §3.1.2 — Assessing the Accuracy of the Coefficient Estimates (pp. 72–77)
**Subtopics:**
- Population regression line Y = β₀ + β₁X + ε (3.5) vs least squares line; unbiasedness by analogy with SE(μ̂)² = σ²/n (3.7).
- SE(β̂₀)², SE(β̂₁)² (3.8); approximate 95% CI β̂₁ ± 2·SE(β̂₁) (3.9); t-statistic t = (β̂₁ − 0)/SE(β̂₁) (3.14) and p-value for H₀: β₁ = 0.

#### §3.1.3 — Assessing the Accuracy of the Model (pp. 77–80)
**Subtopics:**
- Residual standard error RSE = √(RSS/(n − 2)) (3.15) as absolute lack of fit; R² = 1 − RSS/TSS (3.17); in simple regression R² = Cor(X, Y)² (3.18).

### §3.2 — Multiple Linear Regression (pp. 80–91)
**Subtopics:**
- Y = β₀ + β₁X₁ + ⋯ + β_pX_p + ε (3.19); βⱼ is the average effect of Xⱼ holding the other predictors fixed.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §3.2.1 — Estimating the Regression Coefficients (pp. 81–83)
**Subtopics:**
- Least squares minimizes RSS (3.22); multiple vs simple regression coefficients differ (newspaper's marginal association disappears once radio is controlled, via correlation among predictors).

#### §3.2.2 — Some Important Questions (pp. 83–91)
**Subtopics:**
- One: is at least one predictor useful? F = [(TSS − RSS)/p]/[RSS/(n − p − 1)] (3.23) for H₀: all βⱼ = 0; partial F (3.24) for a subset of q coefficients; why individual t-tests mislead when p is large.
- Two: deciding on important variables: forward, backward and mixed selection; Mallow's Cp, AIC, BIC, adjusted R² (backward selection impossible when p > n).
- Three: model fit via RSE (3.25) and R² (R² always rises when variables are added).
- Four: predictions: reducible error, model bias, confidence vs prediction intervals.

### §3.3 — Other Considerations in the Regression Model (pp. 91–109)
**Subtopics:**
- Qualitative predictors, relaxing the linear-additive assumptions, and diagnosing the six potential problems of a linear fit.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §3.3.1 — Qualitative Predictors (pp. 91–94)
**Subtopics:**
- Predictors with Only Two Levels: dummy variable (3.26)–(3.27), baseline level, 0/1 vs ±1 coding changes interpretation not fit.
- Qualitative Predictors with More than Two Levels: one fewer dummy than levels (3.28)–(3.30); F-test for the joint null; coding choices.

#### §3.3.2 — Extensions of the Linear Model (pp. 94–100)
**Subtopics:**
- Removing the Additive Assumption: interaction term X₁X₂ (3.31)–(3.33) (synergy in TV × radio); hierarchical principle; interactions with qualitative variables (3.34)–(3.35).
- Non-linear Relationships: polynomial regression mpg = β₀ + β₁·horsepower + β₂·horsepower² + ε (3.36) is still a linear model.
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §3.3.3 — Potential Problems (pp. 100–109)
**Subtopics:**
- 1. Non-linearity of the Data: residual plots against fitted values; transform predictors (log X, √X, X²).
- 2. Correlation of Error Terms: tracking in time series residuals; understated standard errors and narrow intervals.
- 3. Non-constant Variance of Error Terms: funnel-shaped residuals; log Y or √Y transforms; weighted least squares.
- 4. Outliers: studentized residuals above 3 in absolute value; effect on RSE and R².
- 5. High Leverage Points: leverage statistic hᵢ (3.37), average leverage (p + 1)/n; studentized residual vs leverage plot.
- 6. Collinearity: inflates SE(β̂ⱼ) and reduces power; correlation matrix misses multicollinearity; VIF(β̂ⱼ) = 1/(1 − R²_{Xⱼ|X₋ⱼ}), worrying above 5–10.
**Linked materials:**
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]]

### §3.4 — The Marketing Plan (pp. 109–111)

### §3.5 — Comparison of Linear Regression with K-Nearest Neighbors (pp. 111–116)
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §3.6 — Lab: Linear Regression (pp. 116–127)

### §3.7 — Exercises (pp. 127–134)
**Subtopics:**
- Conceptual 1–7 (p-values, KNN, interactions, training vs test RSS, regression through origin, R² = cor²); Applied 8–15 (Auto, Carseats, simulated data, collinearity, Boston).

## Ch. 4 — Classification
**Pages:** pp. 135–199

### §4.1 — An Overview of Classification (pp. 135–136)
**Subtopics:**
- Qualitative responses; Default data (default as a function of balance and income) as the running example.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §4.2 — Why Not Linear Regression? (pp. 136–138)
**Subtopics:**
- Coding a multi-class response as numbers imposes an arbitrary ordering; for binary 0/1 the linear probability fit estimates Pr(Y = 1 | X) but can fall outside [0, 1].
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §4.3 — Logistic Regression (pp. 138–146)
**Subtopics:**
- Models Pr(Y = 1 | X) directly, keeping predictions inside [0, 1].
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §4.3.1 — The Logistic Model (pp. 139–140)
**Subtopics:**
- Linear probability model p(X) = β₀ + β₁X (4.1) vs logistic function p(X) = e^{β₀+β₁X}/(1 + e^{β₀+β₁X}) (4.2); odds p/(1 − p) = e^{β₀+β₁X} (4.3) and log-odds (logit) linear in X (4.4); a one-unit change in X multiplies the odds by e^{β₁}.

#### §4.3.2 — Estimating the Regression Coefficients (pp. 140–141)
**Subtopics:**
- Maximum likelihood: ℓ(β₀, β₁) = ∏_{i: yᵢ=1} p(xᵢ) ∏_{i′: yᵢ′=0} (1 − p(xᵢ′)) (4.5); z-statistics and p-values for coefficients.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §4.3.3 — Making Predictions (pp. 141–142)
**Subtopics:**
- Plugging β̂ into the logistic function to get predicted probabilities; dummy predictors (student status).

#### §4.3.4 — Multiple Logistic Regression (pp. 142–144)
**Subtopics:**
- Log-odds linear in p predictors (4.6)–(4.7); confounding: the student coefficient is positive alone but negative once balance is controlled (Figure 4.3); predicted default 0.058 (student) vs 0.105 (non-student) (4.8)–(4.9).

#### §4.3.5 — Multinomial Logistic Regression (pp. 144–146)
**Subtopics:**
- K > 2 classes with baseline class K: Pr(Y = k | X = x) (4.10)–(4.11); log odds against the baseline are linear in x (4.12); fitted values do not depend on the baseline, coefficient interpretation does.
- Softmax coding treats all K classes symmetrically (4.13); log odds ratio between two classes (4.14); reappears in Chapter 10.

### §4.4 — Generative Models for Classification (pp. 146–161)
**Subtopics:**
- Model the class-conditional distribution of X, then flip it with Bayes' theorem: Pr(Y = k | X = x) = π_k f_k(x)/Σ_l π_l f_l(x) (4.15), with prior π_k and class density f_k.
- Why not just logistic regression: unstable estimates under strong class separation, better accuracy with small n and near-normal X, natural extension to K > 2.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Rules: [[rules/07_bayes|Bayesian inference]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §4.4.1 — Linear Discriminant Analysis for p = 1 (pp. 147–150)
**Subtopics:**
- Gaussian classes with common σ² (4.16)–(4.17); discriminant δ_k(x) = x·μ_k/σ² − μ_k²/(2σ²) + log π_k (4.18), linear in x; boundary x = (μ₁ + μ₂)/2 with equal priors (4.19).
- Plug-in estimates μ̂_k, pooled σ̂² (4.20), π̂_k = n_k/n (4.21) and the estimated discriminant (4.22).

#### §4.4.2 — Linear Discriminant Analysis for p > 1 (pp. 150–156)
**Subtopics:**
- Multivariate Gaussian density (4.23) with class-specific means and common covariance Σ; δ_k(x) = xᵀΣ⁻¹μ_k − ½μ_kᵀΣ⁻¹μ_k + log π_k (4.24); Bayes boundaries (4.25).
- Confusion matrix on the Default data (Table 4.4); trivial null classifier benchmark; sensitivity vs specificity; lowering the threshold from 0.5 (4.26) to 0.2 (4.27) trades overall error for fewer missed defaulters (Table 4.5).
- ROC curve and AUC (0.95 for LDA on Default) as threshold-free summaries; true/false positive rates, precision, power and Type I/II error terminology (Tables 4.6–4.7).

#### §4.4.3 — Quadratic Discriminant Analysis (pp. 156–158)
**Subtopics:**
- Class-specific covariance Σ_k gives a quadratic discriminant (4.28); LDA vs QDA as a bias–variance trade-off (Kp(p + 1)/2 covariance parameters).

#### §4.4.4 — Naive Bayes (pp. 158–161)
**Subtopics:**
- Predictors independent within each class: f_k(x) = f_k1(x₁) × ⋯ × f_kp(x_p) (4.29), posterior (4.30); one-dimensional densities via a Gaussian, histogram or kernel density, or class proportions for qualitative X.
- Biased but low-variance; on Default (n = 10,000, p = 2) it does not beat LDA (Tables 4.8–4.9); pays off when p is large or n is small.

### §4.5 — A Comparison of Classification Methods (pp. 161–167)
**Subtopics:**
- No method dominates; the choice depends on the true class distributions, n and p (bias–variance).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §4.5.1 — An Analytical Comparison (pp. 161–164)
**Subtopics:**
- Log posterior odds against baseline K (4.31): linear for LDA (4.32), quadratic for QDA (4.33), additive (GAM form) for naive Bayes (4.34).
- LDA is a special case of QDA; any linear-boundary classifier is a special case of naive Bayes; Gaussian naive Bayes is LDA with diagonal Σ; logistic regression has LDA's linear form but fits by maximum likelihood (better when normality fails).
- KNN: non-parametric, wins for highly non-linear boundaries only with large n and small p; QDA as the middle ground; no coefficient table.

#### §4.5.2 — An Empirical Comparison (pp. 164–167)
**Subtopics:**
- Six simulated scenarios (p = 2, 100 training sets each): linear Bayes boundaries (1–3) favour LDA/logistic, non-linear ones (4–6) favour QDA, naive Bayes or KNN-CV; KNN-1 can be worst; adding polynomial terms moves logistic/LDA towards QDA.

### §4.6 — Generalized Linear Models (pp. 167–173)
**Subtopics:**
- Responses that are neither qualitative nor continuous quantitative: counts (bikers per hour in the Bikeshare data).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]]

#### §4.6.1 — Linear Regression on the Bikeshare Data (pp. 167–169)
**Subtopics:**
- Least squares fit (Table 4.10, Figure 4.13): sensible month/hour patterns but 9.6% negative fitted values, variance rising with the mean (heteroscedasticity), and a continuous model for an integer response; log(Y) fixes some issues but complicates interpretation and fails at Y = 0.

#### §4.6.2 — Poisson Regression on the Bikeshare Data (pp. 169–172)
**Subtopics:**
- Poisson distribution Pr(Y = k) = e^{−λ}λᵏ/k! (4.35) with E(Y) = Var(Y) = λ; log link log λ(X) = β₀ + β₁X₁ + ⋯ + β_pX_p (4.36)–(4.37); maximum likelihood (4.38).
- Interpretation: a one-unit increase in Xⱼ multiplies E(Y) by exp(βⱼ) (cloudy vs clear: exp(−0.08) = 0.923); built-in mean–variance relationship; no negative fitted values (Table 4.11, Figure 4.15); overdispersion inflates the z-values (footnote 5).

#### §4.6.3 — Generalized Linear Models in Greater Generality (pp. 172–173)
**Subtopics:**
- Common recipe: Y from an exponential-family distribution (Gaussian, Bernoulli, Poisson; also exponential, Gamma, negative binomial) and a link η with η(E(Y | X)) = β₀ + Σ βⱼXⱼ (4.39)–(4.42); links μ, log(μ/(1 − μ)) and log μ.

### §4.7 — Lab: Logistic Regression, LDA, QDA, and KNN (pp. 173–193)
**Subtopics:**
- §4.7.1 The Stock Market Data (p. 173): Smarket data via ISLP load_data().
- §4.7.2 Logistic Regression (p. 174): sm.GLM(family=sm.families.Binomial()), predicted probabilities, confusion_table(), training vs held-out 2005 data.
- §4.7.3 Linear Discriminant Analysis (p. 179): sklearn LinearDiscriminantAnalysis, predict_proba() and posterior thresholds.
- §4.7.4 Quadratic Discriminant Analysis (p. 181): QuadraticDiscriminantAnalysis.
- §4.7.5 Naive Bayes (p. 182): GaussianNB.
- §4.7.6 K-Nearest Neighbors (p. 183): KNeighborsClassifier; Caravan insurance data, StandardScaler(), precision among predicted buyers, logistic threshold 0.25.
- §4.7.7 Linear and Poisson Regression on the Bikeshare Data (pp. 188–193): sm.OLS with sum-to-zero contrasts, sm.GLM(family=sm.families.Poisson()), comparison of fitted values.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §4.8 — Exercises (pp. 193–199)
**Subtopics:**
- Conceptual 1–12 (logit equivalence, LDA/QDA derivations, curse of dimensionality, odds, Bayes' theorem, analytical forms of (4.32)–(4.33), baseline vs softmax coding); Applied 13–16 (Weekly, Auto, Python functions, Boston), now including naive Bayes.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

## Ch. 5 — Resampling Methods
**Pages:** pp. 201–228

### §5.1 — Cross-Validation (pp. 202–212)
**Subtopics:**
- Model assessment (estimating test error) vs model selection (choosing flexibility) when no designated test set exists.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §5.1.1 — The Validation Set Approach (pp. 202–204)
**Subtopics:**
- Random split into training and validation halves (Auto: linear vs quadratic vs cubic mpg ~ horsepower); drawbacks: high variability across splits and overestimation of test error (fits on fewer observations).

#### §5.1.2 — Leave-One-Out Cross-Validation (pp. 204–206)
**Subtopics:**
- CV₍ₙ₎ = (1/n) Σ MSEᵢ (5.1); less bias, no split randomness; least-squares shortcut CV₍ₙ₎ = (1/n) Σ [(yᵢ − ŷᵢ)/(1 − hᵢ)]² (5.2) using leverage hᵢ.

#### §5.1.3 — k-Fold Cross-Validation (pp. 206–208)
**Subtopics:**
- CV₍k₎ = (1/k) Σ MSEᵢ over k folds (5.3), typically k = 5 or 10; LOOCV is the case k = n; cheaper than LOOCV; locating the minimum of the test MSE curve matters more than its level (Figure 5.6).

#### §5.1.4 — Bias-Variance Trade-Off for k-Fold Cross-Validation (pp. 208–209)
**Subtopics:**
- LOOCV is nearly unbiased but has higher variance (averaged fits are highly correlated); k = 5 or 10 balances the two.

#### §5.1.5 — Cross-Validation on Classification Problems (pp. 209–212)
**Subtopics:**
- CV error as the average misclassification indicator Errᵢ = I(yᵢ ≠ ŷᵢ) (5.4); choosing polynomial degree in logistic regression (5.5) and K in KNN; training error is a poor guide.

### §5.2 — The Bootstrap (pp. 212–215)
**Subtopics:**
- Portfolio example: α = (σ²_Y − σ_XY)/(σ²_X + σ²_Y − 2σ_XY) minimizes Var(αX + (1 − α)Y) (5.6), plug-in α̂ (5.7); "true" SE(α̂) ≈ 0.083 from 1,000 simulated data sets.
- Resampling with replacement from the observed data; bootstrap standard error SE_B(α̂) as the standard deviation of B replicates (5.8), here 0.087.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §5.3 — Lab: Cross-Validation and the Bootstrap (pp. 215–224)
**Subtopics:**
- §5.3.1 The Validation Set Approach (p. 216): train_test_split(), polynomial fits on Auto, evalMSE().
- §5.3.2 Cross-Validation (p. 217): sklearn_sm() wrapper, cross_validate() with cv = n (LOOCV), KFold(n_splits=10), ShuffleSplit() for repeated validation splits.
- §5.3.3 The Bootstrap (pp. 220–224): alpha_func() and boot_SE() on Portfolio (bootstrap SE(α̂) = 0.0912); bootstrap SEs of linear and quadratic regression coefficients vs sm.OLS formula SEs when model assumptions fail.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §5.4 — Exercises (pp. 224–228)
**Subtopics:**
- Conceptual 1–4 (α derivation, bootstrap inclusion probability, k-fold CV, prediction SD); Applied 5–9 (Default, Weekly, simulated data, Boston).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

## Ch. 6 — Linear Model Selection and Regularization
**Pages:** pp. 229–288

### §6.1 — Subset Selection (pp. 231–240)
**Subtopics:**
- Fit the linear model (6.1) on a subset of the p predictors chosen for prediction accuracy and interpretability.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §6.1.1 — Best Subset Selection (pp. 231–233)
**Subtopics:**
- Algorithm 6.1: best model of each size by RSS/R², then choose among M₀, …, M_p by validation error, Cp (AIC), BIC or adjusted R²; 2ᵖ models make it infeasible beyond p ≈ 40; deviance replaces RSS for logistic regression.

#### §6.1.2 — Stepwise Selection (pp. 233–235)
**Subtopics:**
- Forward stepwise (Algorithm 6.2, 1 + p(p + 1)/2 models, usable when p > n), backward stepwise (Algorithm 6.3, needs n > p), Hybrid Approaches; not guaranteed to find the best subset.

#### §6.1.3 — Choosing the Optimal Model (pp. 235–240)
**Subtopics:**
- Cp, AIC, BIC, and Adjusted R²: Cp = (1/n)(RSS + 2dσ̂²) (6.2), unbiased for test MSE; AIC proportional to Cp for Gaussian least squares; BIC = (1/n)(RSS + log(n)dσ̂²) (6.3) penalizes size more heavily; adjusted R² = 1 − [RSS/(n − d − 1)]/[TSS/(n − 1)] (6.4).
- Validation and Cross-Validation: direct test-error estimates with fewer assumptions; one-standard-error rule picks the smallest model within one SE of the minimum.

### §6.2 — Shrinkage Methods (pp. 240–253)
**Subtopics:**
- Fit all p predictors with a penalty that shrinks coefficients toward zero, trading a little bias for a large variance reduction.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

#### §6.2.1 — Ridge Regression (pp. 240–244)
**Subtopics:**
- Minimize RSS + λ Σ βⱼ² (6.5) (ℓ₂ penalty, intercept unpenalized); λ = 0 gives least squares, λ → ∞ the null model; coefficient paths against λ and ‖β̂_λ^R‖₂/‖β̂‖₂.
- Not scale equivariant: standardize predictors first (6.6).
- Why Does Ridge Regression Improve Over Least Squares?: bias–variance trade-off; gains largest when least squares has high variance (p close to n); far cheaper than best subset.

#### §6.2.2 — The Lasso (pp. 244–252)
**Subtopics:**
- Minimize RSS + λ Σ |βⱼ| (6.7) (ℓ₁ penalty) sets some coefficients exactly to zero: sparse, interpretable models (variable selection).
- Another Formulation for Ridge Regression and the Lasso: constrained forms with budget s (6.8)–(6.9), link to best subset (6.10); The Variable Selection Property of the Lasso: diamond vs circle constraint regions and RSS ellipses (Figure 6.7).
- Comparing the Lasso and Ridge Regression: lasso wins when few predictors matter, ridge when many have similar effects; neither dominates, use CV.
- A Simple Special Case for Ridge Regression and the Lasso (n = p, X = I, least squares β̂ⱼ = yⱼ (6.11)): ridge shrinks proportionally β̂ⱼ = yⱼ/(1 + λ) (6.12), (6.14); lasso soft-thresholds by λ/2 (6.13), (6.15).
- Bayesian Interpretation of Ridge Regression and the Lasso: posterior mode under a Gaussian prior is ridge (also the posterior mean), under a double-exponential (Laplace) prior is the lasso (Figure 6.11).
**Linked materials:**
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

#### §6.2.3 — Selecting the Tuning Parameter (pp. 252–253)
**Subtopics:**
- Choose λ (or s) by cross-validation over a grid, then refit on all observations (Figures 6.12–6.13).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §6.3 — Dimension Reduction Methods (pp. 253–262)

### §6.4 — Considerations in High Dimensions (pp. 262–267)

### §6.5 — Lab: Linear Models and Regularization Methods (pp. 267–283)

### §6.6 — Exercises (pp. 283–288)
**Subtopics:**
- Conceptual 1–7 (subset vs stepwise nesting, lasso/ridge bias–variance, special case (6.12)–(6.15), Bayesian lasso/ridge derivation); Applied 8–11 (simulated stepwise/lasso, College, best subset on simulated data, Boston).

## Ch. 7 — Moving Beyond Linearity
**Pages:** pp. 289–329

### §7.1 — Polynomial Regression (pp. 290–292)
**Subtopics:**
- yᵢ = β₀ + β₁xᵢ + β₂xᵢ² + ⋯ + β_dxᵢᵈ + εᵢ (7.1) is a linear model in xᵢ, …, xᵢᵈ fit by least squares; d rarely above 3 or 4 because high-degree curves behave wildly, especially near the boundary of X.
- Pointwise standard error of f̂(x₀) (7.2) from the coefficient covariance matrix, Var[f̂(x₀)] = ℓ₀ᵀĈℓ₀ (footnote 1); ±2 SE bands as an approximate 95% interval (Wage vs age, degree 4).
- Polynomial logistic regression for Pr(wage > 250 | age) (7.3); wide intervals because only 79 of 3,000 are high earners.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §7.2 — Step Functions (pp. 292–293)

### §7.3 — Basis Functions (pp. 293–294)

### §7.4 — Regression Splines (pp. 294–300)

### §7.5 — Smoothing Splines (pp. 300–303)

### §7.6 — Local Regression (pp. 303–305)

### §7.7 — Generalized Additive Models (pp. 305–309)

### §7.8 — Lab: Non-Linear Modeling (pp. 309–325)
**Subtopics:**
- §7.8.1 Polynomial Regression and Step Functions (p. 310) is the Python lab for §7.1 (poly() fits, anova_lm() comparison of degrees, polynomial logistic regression with sm.GLM(family=sm.families.Binomial()) for wage > 250).
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §7.9 — Exercises (pp. 325–329)
**Subtopics:**
- Conceptual 1–5 (truncated power basis, penalized smoothing sketches, basis-function curves); Applied 6–12 (Wage polynomial degree and cuts by CV, Auto, Boston nox ~ dis with poly() and bs(), College GAM, backfitting).

## Ch. 8 — Tree-Based Methods
**Pages:** pp. 331–366

## Ch. 9 — Support Vector Machines
**Pages:** pp. 367–398

## Ch. 10 — Deep Learning
**Pages:** pp. 399–467

## Ch. 11 — Survival Analysis and Censored Data
**Pages:** pp. 469–502

## Ch. 12 — Unsupervised Learning
**Pages:** pp. 503–556

### §12.1 — The Challenge of Unsupervised Learning (pp. 503–504)

### §12.2 — Principal Components Analysis (pp. 504–515)
**Subtopics:**
- PCA finds a low-dimensional set of directions that capture as much of the variation in the n × p data as possible; used for visualization, data summary and as input to PCR (§6.3.1).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §12.2.1 — What Are Principal Components? (pp. 505–508)
**Subtopics:**
- First principal component Z₁ = φ₁₁X₁ + ⋯ + φ_p1X_p (12.1), scores zᵢ₁ (12.2) chosen to maximize sample variance subject to Σⱼ φⱼ₁² = 1 (12.3); later components (12.4) are uncorrelated with (orthogonal to) earlier ones; loadings via the eigen/singular value decomposition.
- USArrests example: first loading weights the three crime variables, second loads on UrbanPop; biplot of scores and loadings (Figure 12.1).

#### §12.2.2 — Another Interpretation of Principal Components (pp. 508–510)
**Subtopics:**
- Principal components span the M-dimensional subspace closest to the observations; xᵢⱼ ≈ Σₘ zᵢₘφⱼₘ (12.5) is the best rank-M approximation, solving the least squares problem (12.6) with minimum value (12.7).

#### §12.2.3 — The Proportion of Variance Explained (pp. 510–512)
**Subtopics:**
- Total variance Σⱼ (1/n)Σᵢ xᵢⱼ² (12.8), variance of the mth component (12.9), PVE of component m (12.10); decomposition (12.11) shows PVE equals the R² of the rank-M approximation; min(n − 1, p) components with PVEs summing to one.
- USArrests: first two components explain 62.0% and 24.7% (almost 87%); scree plot and cumulative PVE (Figure 12.3).

#### §12.2.4 — More on PCA (pp. 512–515)
**Subtopics:**
- Scaling the Variables: results depend on scale, so standardize to unit SD unless all variables share units (Assault dominates unscaled, Figure 12.4).
- Uniqueness of the Principal Components: loadings and scores are unique up to a sign flip.
- Deciding How Many Principal Components to Use: no single answer; eyeball the scree plot for an elbow; CV is available only when the scores feed a supervised method such as PCR.

#### §12.2.5 — Other Uses for Principal Components (p. 515)
**Subtopics:**
- Use the first M score vectors as features in regression, classification and clustering (less noisy than the full data).

### §12.3 — Missing Values and Matrix Completion (pp. 515–520)

### §12.4 — Clustering Methods (pp. 520–535)

### §12.5 — Lab: Unsupervised Learning (pp. 535–552)
**Subtopics:**
- §12.5.1 Principal Components Analysis (p. 535) is the Python lab for §12.2.

### §12.6 — Exercises (pp. 552–556)

## Ch. 13 — Multiple Testing
**Pages:** pp. 557–596


# Izbicki & Mendonça, Aprendizado de Máquina: uma abordagem estatística, 1st ed. (2020)
#book/ame
> Link: [[Livros/Izbicki, Mendonça - Aprendizado de Máquina_ uma abordagem estatística (2020)|AME]]

> Page numbers are printed book pages (taken from the book's table of contents, checked against the page footers). PDF-to-printed offset is constant: printed page = 1-based PDF page − 18 (front matter i–xvi plus two cover leaves; printed p. 1 = PDF p. 19, p. 242 = PDF p. 260). The book is in Portuguese; code is in R. There are no end-of-chapter exercises.

## Ch. 1 — Introdução
**Pages:** pp. 3–25

### §1.1 — Notação e Suposições (pp. 4–5)
**Subtopics:**
- Regression function r(x) := E[Y | X = x] as the target; quantitative Y = regression (Part I), qualitative Y = classification (Part II).
- i.i.d. sample (X₁, Y₁), …, (Xₙ, Yₙ) ∼ (X, Y) assumed throughout (relaxed in §9.3); notation xᵢ,ⱼ for covariate j of observation i (Tabela 1.1).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.2 — Predição versus Inferência: Por que estimar r(x)? (pp. 5–8)
**Subtopics:**
- Examples: life expectancy vs GDP per capita (211 countries), galaxy redshift from images, Isomap face data, song release year (YearPredictionMSD).
- Inferential goal (which predictors matter, effect of changing one) vs predictive goal (build g: ℝᵈ → ℝ with g(xₙ₊₁) ≈ yₙ₊₁ on new i.i.d. data).
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.3 — As Duas Culturas (pp. 8–9)
**Subtopics:**
- Breiman (2001): data modeling culture (assume the model is true, test assumptions, interpret βᵢ) vs algorithmic modeling culture (prediction, no assumption the model is correct); the book takes the second view.
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.4 — A Função de Risco (pp. 9–12)
**Subtopics:**
- Quadratic prediction risk R_pred(g) = E[(Y − g(X))²] on a new observation; general risk = expected loss (absolute loss |Y − g(X)| as an alternative).
- Teorema 1: R_pred(g) = R_reg(g) + E[V[Y | X]], with R_reg(g) = E[(r(X) − g(X))²]; hence argmin_g R_pred = r(x), the regression function is the best predictor.
- Conditional risk (g fixed) vs expected risk (averaged over training samples) (Observação 1.3); law of large numbers links the average loss on new data to R(g).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]; [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.5 — Seleção de Modelos: Super e Sub-Ajuste (pp. 12–24)
**Subtopics:**
- Polynomial fits of degree p ∈ {1, 4, 50} to the life-expectancy data: underfitting (p = 1) vs overfitting (p = 50); model selection picks g ∈ G with low estimated risk.
- Interpolation need not imply overfitting (Belkin et al.; Observação 1.4).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §1.5.1 — Data Splitting e Validação Cruzada (pp. 14–21)
**Subtopics:**
- Training MSE EQM(g) = n⁻¹ Σ (Yᵢ − g(Xᵢ))² (Eq. 1.1) is over-optimistic; hold-out estimator R̂(g) on a random validation split (e.g., 70/30) is consistent (Eq. 1.2).
- LOOCV R̂(g) = n⁻¹ Σ (Yᵢ − g₋ᵢ(Xᵢ))² and k-fold CV over folds L₁, …, L_k (k = n recovers LOOCV); hold-out is consistent for the conditional risk, LOOCV is approximately unbiased for the expected risk (Observação 1.5).
- Training vs validation vs test: validation picks tuning parameters, test compares the winners; CLT confidence interval for the risk on the test set, R̂(g) ± 2√(σ̂²/m) (Eq. 1.3), guides the split size.
- Exemplo 1.6 (training vs validation MSE against p) and Exemplo 1.7: a misspecified quadratic beats the true quintic model (lower variance; risk 1.7 vs 22354.08 over 1000 replications).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §1.5.1.1 — Penalização: uma alternativa (pp. 21–22)
**Subtopics:**
- R(g) ≈ EQM(g) + P(g): AIC penalty P(g) = 2pσ̂²/n, BIC penalty P(g) = log(n)pσ̂²/n; AIC curve on the life-expectancy data mirrors the validation curve (Figura 1.9).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]; [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §1.5.2 — Balanço entre Viés e Variância (pp. 22–24)
**Subtopics:**
- Decomposition E[(Y − g(X))² | X = x] = V[Y | X = x] + (r(x) − E[g(x)])² + V[g(x)]: irreducible variance, squared bias, estimator variance.
- Many parameters = low bias / high variance, few = the reverse; predictive inference accepts bias for lower variance and risk (Figura 1.10).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]; [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.6 — Tuning Parameters (p. 24)
**Subtopics:**
- The polynomial degree p is a tuning parameter controlling the bias–variance balance; the book always chooses tuning parameters by cross-validation or data splitting.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.7 — Resumo (pp. 24–25)
**Subtopics:**
- Recap: inference vs prediction, two cultures, risk = bias² + variance + noise, risk estimation by CV/data splitting and by penalization.

## Ch. 2 — Métodos Paramétricos
**Pages:** pp. 27–31

### §2.1 — O Método dos Mínimos Quadrados (pp. 28–30)
**Subtopics:**
- Linear predictor g(x) = βᵀx with x₀ ≡ 1 (covariates may be transformations, e.g., xᵢ², xᵢxⱼ); least squares β̂ = argmin Σ (Yᵢ − β₀ − … − β_d x_{i,d})² (Eq. 2.2) with closed form β̂ = (XᵀX)⁻¹XᵀY (Eq. 2.3).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §2.1.1 — Mínimos Quadrados quando a Suposição de Linearidade Falha (pp. 29–30)
**Subtopics:**
- Best linear predictor (oracle) β* = argmin_β E[(Y − βᵀX)²] = Σ⁻¹α with Σ = E[XXᵀ] (Eq. 2.4).
- Teorema 2: β̂ →ᴾ β* and R(g_β̂) →ᴾ R(g_β*) even when r(x) is not linear (weak LLN plus Mann–Wald).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §2.1.2 — Regressão Linear no R (p. 30)
**Subtopics:**
- lm(resposta ~ ., data) and predict(ajuste, newdata) (Python port: statsmodels OLS / scikit-learn LinearRegression).

### §2.2 — Resumo (p. 31)
**Subtopics:**
- OLS converges to the best linear predictor; with many covariates it overfits, and for d > n XᵀX is not invertible, motivating Ch. 3.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

## Ch. 3 — Métodos Paramétricos em Altas Dimensões
**Pages:** pp. 33–52

### §3.1 — Busca pelo Melhor Subconjunto de Covariáveis (pp. 33–35)
**Subtopics:**
- L0-penalized least squares β̂_L0 = argmin Σ (yₖ − β₀ − Σ βᵢxₖ,ᵢ)² + λ Σ I(βᵢ ≠ 0) (Eq. 3.1); λ = 0 gives OLS, λ → ∞ gives (ȳ, 0); intercept not penalized.
- With λ = 2σ̂²/n the problem is AIC selection over all 2ᵈ models; trade more bias for less variance; computationally infeasible for large d (Figura 3.1).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §3.2 — Regressão Stepwise (pp. 35–37)
**Subtopics:**
- Forward stepwise: add one variable per step by lowest estimated risk (AIC or CV), then pick the best model; fits 1 + d(d + 1)/2 models instead of 2ᵈ.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §3.3 — Lasso (pp. 37–40)
**Subtopics:**
- Lasso (Tibshirani, 1996): β̂_L1,λ = argmin Σ (yₖ − β₀ − Σ βⱼxₖ,ⱼ)² + λ Σ |βⱼ| (Eq. 3.2); L1 norm as a smooth measure of complexity vs L0 (Tabela 3.1).
- λ = 0 gives OLS, large λ shrinks all βⱼ to 0 (low variance, high bias); λ chosen by cross-validation (Figura 3.3).
- Advantages: convex problem, whole path in λ computed fast (LARS, glmnet; Friedman et al., 2010); sparse solutions are easy to interpret.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]; [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

#### §3.3.1 — Garantias Teóricas (pp. 39–40)
**Subtopics:**
- Teorema 3 (Greenshtein & Ritov, 2004): for bounded data, with probability ≥ 1 − δ, the constrained lasso's excess risk over the sparse oracle β*_L (‖β‖₁ ≤ L) is at most √(16(L + 1)⁴B²/n · log(√2·d/δ)), i.e., of order (L + 1)²B√(log(d/δ)/n); smaller L = easier to reach the oracle but a worse oracle.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §3.4 — Regressão Ridge (pp. 40–41)
**Subtopics:**
- Ridge (Hoerl & Kennard, 1970): L2 penalty λ Σ βⱼ² (Eq. 3.3) with closed form β̂_L2,λ = (XᵀX + λI₀)⁻¹XᵀY, I₀ the identity with I₀(1, 1) = 0 (Eq. 3.4).
- Shrinkage without zeros: under XᵀX = I, β̂_ridge = β̂/(1 + λ) and V[β̂ᵢ,ridge] = V[β̂ᵢ]/(1 + λ)²; λ by cross-validation; kernel ridge regression in §4.6.3.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]; [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

### §3.5 — Formulação Alternativa (pp. 41–42)
**Subtopics:**
- Constrained forms: lasso ⇔ min RSS s.t. Σ |βⱼ| ≤ B (Eq. 3.5); best subset s.t. Σ I(βⱼ ≠ 0) ≤ B₁; ridge s.t. Σ βⱼ² ≤ B₂; lasso and AIC select variables, ridge does not.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §3.6 — Interpretação Bayesiana (pp. 42–43)
**Subtopics:**
- With Yᵢ | xᵢ, β ∼ N(βᵀxᵢ, σ²) independent and σ² known, ridge and lasso are posterior modes (MAP estimators).
- Gaussian prior β ∼ N(0, σ_β² I_d) gives ridge with λ = σ²/σ_β²; i.i.d. Laplace(0, τ_β) prior (τ_β a precision) gives lasso with λ = σ²τ_β.
- Tighter prior = larger λ = more shrinkage; choosing λ by CV equals choosing the prior with the best predictive power (refs. Bishop, 2006; Park & Casella, 2008, Bayesian lasso).
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]; [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

### §3.7 — Regressão ridge e lasso no R (p. 43)
**Subtopics:**
- cv.glmnet(x, y, alpha = 1) for the lasso, alpha = 0 for ridge (Python port: scikit-learn LassoCV / RidgeCV).

### §3.8 — Exemplos (pp. 43–51)
**Subtopics:**
- Exemplo 3.1: simulation with n = 500, 20 covariates, 5 active; OLS risk 14.63 vs best-subset AIC 0.30 (1 h 20 min), forward stepwise 0.30, ridge 0.33, lasso 0.25 selecting exactly x₁–x₅ (Tabela 3.2).
- Exemplo 3.2: prostate cancer (lpsa, 97 men, train column split); coefficient paths against λ for ridge and lasso (Figuras 3.4–3.5), validation MSE with standard errors (Tabela 3.5).
- Exemplo 3.3: Amazon Fine Food Reviews, sparse document-term matrix; lasso MSE 1.136 < ridge 1.205 ≪ OLS 7.675, lasso keeps 558 words (Tabela 3.6).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §3.9 — Resumo (pp. 51–52)
**Subtopics:**
- L0 (best subset/stepwise), L1 (lasso, sparse) and L2 (ridge, shrinkage) penalties all cut variance at the cost of bias; non-parametric methods do the reverse (Figura 3.8).

## Ch. 4 — Métodos Não Paramétricos
**Pages:** pp. 53–106

### §4.1 — Séries Ortogonais (pp. 53–56)
**Subtopics:**
- Expand r(x) in an orthonormal basis of L²([0, 1]) (Fourier, polynomial/Hermite) with βⱼ = E[Yψⱼ(X)]; unbiased β̂ⱼ = n⁻¹ Σ Yᵢψⱼ(Xᵢ) and truncation g(x) = Σ_{j≤J} β̂ⱼψⱼ(x) (Eq. 4.1), J the bias–variance tuning parameter; tensor-product bases for d > 1.

### §4.2 — Splines (pp. 56–57)
**Subtopics:**
- Piecewise polynomials of order k with continuous derivatives at knots t₁ < … < t_p; r(x) approximated by a linear combination of spline basis functions fitted by least squares.

### §4.3 — k Vizinhos Mais Próximos (pp. 57–59)
**Subtopics:**
- KNN regression g(x) = k⁻¹ Σ_{i∈N_x} yᵢ (Eq. 4.2), a local average; k is the bias–variance tuning parameter chosen by cross-validation.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §4.4 — Nadaraya-Watson (pp. 59–61)
**Subtopics:**
- Kernel-weighted average g(x) = Σ wᵢ(x)yᵢ with wᵢ(x) = K(x, xᵢ)/Σⱼ K(x, xⱼ); uniform, Gaussian, triangular and Epanechnikov kernels; bandwidth h tuned by CV.

### §4.5 — Regressão Polinomial Local (pp. 61–62)
**Subtopics:**
- Kernel-weighted least squares fit of a degree-p polynomial around each x (Nadaraya–Watson is p = 0; local linear is p = 1).

### §4.6 — Métodos baseados em RKHSs (pp. 62–74)
**Subtopics:**
- Penalized risk minimization argmin_{g∈H} Σ L(g(xₖ), yₖ) + P(g) over a reproducing kernel Hilbert space; §4.6.1 A matemática do RKHS (Mercer kernels, ‖g‖_{H_K}); §4.6.2 representer theorem g(x) = Σ αₖK(xₖ, x) (Teorema 6).
- §4.6.3 Exemplo 1: Kernel Ridge Regression (pp. 67–73): quadratic loss generalizes ridge, closed-form α = (K + λI)⁻¹y; smoothing splines as a special case; the kernel trick; efficient implementation.
- §4.6.4 Exemplo 2: Support Vector Regression Machine (pp. 73–74): ε-insensitive loss (|y − g(x)| − ε)₊, solved numerically (e1071::svm).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §4.7 — Modelos Aditivos (pp. 74–77)
**Subtopics:**
- g(x) = α + Σⱼ gⱼ(xⱼ) with smooth univariate gⱼ, identified by α = Ȳ and Σᵢ gⱼ(Xᵢ,ⱼ) = 0; fitted by backfitting; interpretability between linear and fully non-parametric models.

### §4.8 — Árvores de Regressão (pp. 77–82)
**Subtopics:**
- Recursive binary partitioning (nodes, leaves), leaf prediction = mean of the training responses (Eq. 4.19), splits by squared error (Eq. 4.20); grow a large tree then prune by validation risk (rpart).

### §4.9 — Bagging e Florestas Aleatórias (pp. 82–89)
**Subtopics:**
- Averaging two unbiased, uncorrelated, equal-variance predictors halves the variance term: E[(Y − ḡ(x))² | x] = V[Y | x] + ½V[gᵢ(x) | x] (Eq. 4.21).
- Bagging: grow B unpruned trees on B bootstrap samples (random draws with replacement of size n) and average g(x) = B⁻¹ Σ g_b(x); variable importance by mean RSS reduction of the splits on each covariate (varImpPlot).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §4.9.1 — Florestas Aleatórias (pp. 85–89)
**Subtopics:**
- Decorrelate the bagged trees by drawing m < d candidate covariates at each split (m ≈ d/3 as a rule of thumb, m = d is bagging); m tuned by CV (randomForest, CO2 data).

### §4.10 — Boosting (pp. 89–91)
**Subtopics:**
- Start from g ≡ 0 and repeatedly fit a shallow tree to the residuals, adding it scaled by the learning rate λ ∈ (0, 1); B, λ and tree size are tuning parameters.

### §4.11 — Redes Neurais Artificiais (pp. 91–99)
**Subtopics:**
- Feed-forward network with hidden layers and activation functions as a non-linear estimator of r(x); §4.11.1 Estimação: Backpropagation (gradient descent layer by layer on the MSE); §4.11.2 Deep Learning (stochastic gradient descent, GPUs, keras; Exemplo 4.3 bike sharing training vs validation risk by epoch).

### §4.12 — Exemplo (pp. 99–102)
**Subtopics:**
- Exemplo 4.4: Amazon reviews revisited with KNN, XGBoost and a pruned tree on validation MSE; XGBoost is best, comparable to lasso and ridge from Exemplo 3.3 (Tabelas 4.1–4.2).

### §4.13 — Um Pouco de Teoria (pp. 102–106)
**Subtopics:**
- §4.13.1 k-vizinhos Mais Próximos: for L-Lipschitz r, Teorema 7 bounds E[(r̂ₖ(X) − r(X))²] ≤ K(k/n)^{2/d} + σ²/k (bias vs variance), optimal k ≍ n^{2/(2+d)}.
- §4.13.2 Séries Ortogonais: with m integrable derivatives, Teorema 8 gives risk ≤ K₁J^{−2m} + K₂J/n, i.e., the minimax rate n^{−2m/(2m+1)} (n^{−2m/(2m+d)} in d dimensions).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §4.14 — Resumo (p. 106)
**Subtopics:**
- Non-parametric methods trade parametric rates n⁻¹ for slower rates n^{−α/(α+d)} in exchange for flexibility; worse as d grows (Ch. 5).

## Ch. 5 — Métodos Não Paramétricos em Altas Dimensões
**Pages:** pp. 107–117

### §5.1 — Taxas de convergência e a maldição da dimensionalidade (pp. 107–110)
**Subtopics:**
- Curse of dimensionality: minimax risk of order n^{−α/(α+d)}, so the sample size needed grows exponentially in d; §5.1.1 Esparsidade (r depends on few covariates) and §5.1.2 Redundâcia (X on a low-dimensional manifold) as escape assumptions.

### §5.2 — k Vizinhos Mais Próximos e Regressão Linear Local (pp. 110–111)
**Subtopics:**
- Both adapt automatically to the intrinsic dimension u of the data, with rate n^{−4/(4+u)} instead of n^{−4/(4+d)}.

### §5.3 — Support Vector Regression (p. 111)
**Subtopics:**
- SVR with a Gaussian kernel also performs well under redundancy.

### §5.4 — Séries Ortogonais (pp. 111–115)
**Subtopics:**
- §5.4.1 Bases espectrais: data-driven orthonormal basis from the eigenfunctions of a Mercer-kernel operator; §5.4.2 O estimador: spectral series g(x) = Σ_{j≤J} β̂ⱼψ̂ⱼ(x) with β̂ⱼ = n⁻¹ Σ Yᵢψ̂ⱼ(Xᵢ) (Lee & Izbicki, 2016).

### §5.5 — Florestas Aleatórias (p. 115)
**Subtopics:**
- Convergence rate depends only on the number of relevant covariates (Biau, 2012).

### §5.6 — SpAM - Modelos Aditivos Esparsos (pp. 115–116)
**Subtopics:**
- Additive model with lasso-type constraint Σ |βⱼ| ≤ L on the component weights (Ravikumar et al., 2009); wine data example (Figura 5.3).

### §5.7 — Resumo (pp. 116–117)
**Subtopics:**
- Sparsity and redundancy are the assumptions that make high-dimensional non-parametric regression feasible; several Ch. 4 methods adapt to them automatically.

## Ch. 6 — Outros Aspectos de Regressão
**Pages:** pp. 119–129

### §6.1 — Interpretabilidade (ExplainableML) (pp. 119–124)
**Subtopics:**
- Why interpretability matters (trust, insight, detecting selection bias); §6.1.1 LIME - Local Interpretable Model-agnostic Explanations (local weighted lasso around x*); §6.1.2 PDP e ICE (partial dependence hᵢ(x) = n⁻¹ Σⱼ g(…, x, …) and individual conditional expectation curves, preferably on held-out data).

### §6.2 — Estimação de Densidades Condicionais (pp. 124–127)
**Subtopics:**
- Estimating the full f(y | x) rather than E[Y | x]; FlexCode expands f(y | x) = Σ βᵢ(x)φᵢ(y) in an orthonormal basis and estimates each βᵢ(x) by regression (Izbicki & Lee, 2017).

### §6.3 — Inferência Conformal (pp. 127–129)
**Subtopics:**
- Distribution-free prediction bands with P(Yₙ₊₁ ∈ C(Xₙ₊₁)) ≥ 1 − α under i.i.d. data only; split conformal: fit r̂ on one half, compute split residuals |y − r̂(x)| on the other, cut at an order statistic.
- Conditional coverage is impossible without strong assumptions; CD-split and Dist-split (conditional-density scores) control it asymptotically (predictionBands package; Exemplo 6.3 bike sharing).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

## Ch. 7 — Introdução
**Pages:** pp. 133–139 (Parte II — Classificação, p. 131)

### §7.1 — Função de Risco (pp. 134–136)
**Subtopics:**
- 0-1 loss and classification risk R(g) := E[I(Y ≠ g(X))] = P(Y ≠ g(X)) (Eq. 7.1); the quadratic risk makes no sense for qualitative Y.
- Teorema 9: the Bayes classifier g(x) = argmax_d P(Y = d | x) minimizes the 0-1 risk; in the binary case g(x) = c₁ ⇔ P(Y = c₁ | x) ≥ 1/2 (other cut-offs in §9.1).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §7.2 — Estimação do Risco e Seleção de Modelos (pp. 136–137)
**Subtopics:**
- Hold-out estimate of the error rate R̂(g) = (n − s)⁻¹ Σ_{i>s} I(Yᵢ ≠ g(Xᵢ)) (Eq. 7.2); choose g ∈ G with the smallest estimated risk by data splitting or cross-validation.
- Teorema 10 (Hoeffding + union bound): for a finite class of N classifiers, with probability ≥ 1 − ε, |R(ĝ) − R(g*)| ≤ 2√(log(2N/ε)/(2(n − s))); more candidates = weaker guarantee, so the test set should compare only a few tuned winners.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §7.3 — Balanço entre Viés e Variância (pp. 137–138)
**Subtopics:**
- Excess risk R(g) − R* = T₁ + T₂ with T₁ = R(g) − R_or (variance analogue, large for rich G) and T₂ = R_or − R* (squared-bias analogue, oracle R_or = inf_{g∈G} R(g) vs Bayes risk R*).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §7.4 — Outras medidas de desempenho (pp. 138–139)
**Subtopics:**
- Rare-disease example: the trivial classifier g ≡ 0 has low 0-1 risk but is useless.
- Confusion matrix (VN, FN, FP, VP; Tabela 7.1); sensitivity/recall S = VP/(VP + FN), specificity E = VN/(VN + FP), PPV/precision VP/(VP + FP), NPV VN/(VN + FN), F1 = harmonic mean of S and PPV.
- Sensitivity estimates P(g(X) = 1 | Y = 1) and specificity P(g(X) = 0 | Y = 0); compute them on validation/test data, not training data; essential for imbalanced data.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

## Ch. 8 — Métodos de classificação
**Pages:** pp. 141–168

### §8.1 — Classificadores Plug-in (pp. 141–151)
**Subtopics:**
- Plug-in rule: estimate P(Y = c | x) for every class, then g(x) = argmax_c P̂(Y = c | x) (binary: g(x) = 1 ⇔ P̂(Y = 1 | x) > 1/2).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §8.1.1 — Métodos de regressão (p. 142)
**Subtopics:**
- P(Y = c | x) = E[I(Y = c) | x], so any Part I regression method (linear, lasso, trees, …) on Z = I(Y = c) gives a plug-in classifier; linear fits can leave [0, 1] (linear probability model).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §8.1.2 — Regressão logística (pp. 142–144)
**Subtopics:**
- Logistic model P(Y = 1 | x) = e^{β₀+Σβᵢxᵢ}/(1 + e^{β₀+Σβᵢxᵢ}), used as a working model rather than assumed true.
- Estimation by maximum (conditional) likelihood L = Π P(Yₖ = 1 | xₖ, β)^{yₖ}(1 − P(Yₖ = 1 | xₖ, β))^{1−yₖ}, maximized numerically (glm, family = binomial).
- Penalized (lasso/ridge) logistic regression via glmnet(…, family = "binomial") and cv.glmnet; multi-class via one logistic regression per class Z = I(Y = c).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]; [[Map/class-plan#Class 7: More econometric models|Class 7]]

#### §8.1.3 — Bayes Ingênuo (pp. 144–147)
**Subtopics:**
- Bayes' theorem P(Y = c | x) = f(x | Y = c)P(Y = c)/Σₛ f(x | Y = s)P(Y = s); naive Bayes assumes conditional independence f(x | Y = s) = Πⱼ f(xⱼ | Y = s).
- Gaussian components Xⱼ | Y = s ∼ N(μⱼ,ₛ, σ²ⱼ,ₛ) with MLE class means and variances; multinomial components for discrete X; compute in logs to avoid underflow (Observação 8.1); special case of Bayesian networks.
- Exemplo 8.1 (Spambase, n = 4601, 57 word frequencies): test risk linear 0.111, logistic 0.086, naive Bayes 0.188 (Tabela 8.1).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §8.1.4 — Análise Discriminante (pp. 147–151)
**Subtopics:**
- X | Y = c multivariate normal; plug the estimated class densities into the Bayes rule.
- §8.1.4.1 Análise Discriminante Linear (pp. 147–149): common covariance, X | Y = c ∼ N(μ_c, Σ); MLEs μ̂_c and pooled Σ̂; log-ratio of class densities is linear in x, so the boundary is a hyperplane aᵀx ≥ K′ (MASS::lda).
- §8.1.4.2 Análise Discriminante Quadrática (pp. 149–151): class-specific Σ_c gives a quadratic boundary; Exemplo 8.2 (simulated) where QDA beats LDA (MASS::qda).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §8.2 — Support Vector Machines (SVM) (pp. 151–156)
**Subtopics:**
- Maximal-margin hyperplane for separable data (support vectors), soft margin with slack εᵢ and budget C; kernel trick f(x) = β₀ + Σ_{k∈S} αₖK(x, xₖ); RKHS view with hinge loss (1 − y g(x))₊ (e1071::svm, tune).

### §8.3 — Árvores de Classificação (pp. 156–158)
**Subtopics:**
- Leaf prediction = mode (Eq. 8.5); splits by the Gini index Σ_R Σ_c p_{R,c}(1 − p_{R,c}) (worked hospital/tomograph example, Exemplo 8.3); pruning by validation error rate (rpart).

### §8.4 — Bagging e Florestas Aleatórias (pp. 158–159)
**Subtopics:**
- Majority vote g(x) = mode{g_b(x)} over bootstrap trees (randomForest, ranger).

### §8.5 — Boosting (pp. 159–161)
**Subtopics:**
- AdaBoost.M1: reweight misclassified points, classifier weight α_b = log((1 − err_b)/err_b), final g(x) = sign(Σ α_b g_b(x)) (gbm, distribution = "adaboost").

### §8.6 — Método dos k Vizinhos Mais Próximos (p. 161)
**Subtopics:**
- KNN classifier g(x) = mode of the labels of the k nearest neighbours (FNN::knn).

### §8.7 — Redes Neurais Artificiais (pp. 161–163)
**Subtopics:**
- One output per class with softmax activation; cross-entropy loss −n⁻¹ ΣΣ I(yₖ = c) log g_{β;c}(xₖ).

### §8.8 — Exemplos (pp. 163–168)
**Subtopics:**
- Exemplo 8.4: Amazon reviews (score 5 vs rest; 40,000 train / 10,000 validation); logistic MLE, ridge, lasso (cut-off = training share of class 1), tree, random forest, XGBoost compared by accuracy, sensitivity and specificity (Tabela 8.3; XGBoost best accuracy 81.7%, tree worst specificity 34.1%).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

## Ch. 9 — Outros Aspectos de Classificação
**Pages:** pp. 169–186

### §9.1 — Assimetria na Função de Perda, Conjuntos de Dados Desbalanceados e Outros Cortes (pp. 169–172)
**Subtopics:**
- With rare events and weak covariates the Bayes rule I(P(Y = 1 | x) ≥ 0.5) collapses to g ≡ 0; use cut-offs g(x) = I(P̂(Y = 1 | x) ≥ K).
- ROC curve: sensitivity against specificity across K, drawn on validation/test data (Figura 9.1); common choice maximizes sensitivity + specificity.
- Cost-weighted risk l₁P(error, Y = 0) + l₀P(error, Y = 1) is minimized by g(x) = I(P(Y = 1 | x) > l₁/(l₀ + l₁)); with l₀ = π₀, l₁ = π₁ the cut-off is the class prevalence P̂(Y = 1).
- Alternatives for non-probabilistic classifiers: observation weights, over/under-sampling; the root problem is unequal costs, not imbalance.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §9.2 — Classificação vs Estimação de Probabilidades (p. 172)
**Subtopics:**
- A good plug-in classifier only needs the sign of P̂ − C right, not P̂ ≈ P; when probabilities matter (ranking, conformal inference) tune with proper scores: cross-entropy (log-likelihood) or Brier score.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §9.3 — Dataset Shift e Viés de Seleção (pp. 172–177)
**Subtopics:**
- Labelled and target samples not identically distributed, often from selection bias (bright galaxies easier to label, Amazon vs Twitter domains).
- §9.3.1 Covariate Shift (pp. 173–176): Y | X equal in both sets; target risk E[L(g(X_L), Y_L)β(X_L)] with importance weights β(x) = f_U(x)/f_L(x) (Eq. 9.1), estimated by density ratios or by a logistic regression of the "labelled" indicator S on x; weighted risk estimation and weighted fitting (glmnet weights).
- §9.3.2 Prior Shift (pp. 176–177): X | Y equal, class prevalences differ (case–control studies); Saerens et al. (2002) reweighting of P(Y_L = 1 | x) by P(Y_U = i)/P(Y_L = i); estimating P(Y_U = 1) from a classifier's rates (Forman, 2006).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]; [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]

### §9.4 — Combinando Classificadores (pp. 177–179)
**Subtopics:**
- Blending / stacked ensembling: meta-classifier fitted on held-out predictions (ensemble set); Exemplo 9.1 (spam) logistic stacking of LDA, L1-logistic, random forest and SVM, risk 0.061 vs best single 0.067 (Tabelas 9.1–9.2).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §9.5 — Teoria do Aprendizado Estatístico (pp. 179–186)
**Subtopics:**
- Empirical risk minimization ĝ = argmin_{g∈G} R_tr(g) and the oracle g* = argmin_{g∈G} R(g); bounding sup_g |R_tr(g) − R(g)| bounds R(ĝ) − R(g*) ≤ 2ε.
- Teorema 11 (VC): P(sup_f |P_n(f) − P(f)| > ε) ≤ 4s(F, 2n)e^{−nε²/8}; shattering number s(F, n), VC dimension, Sauer's lemma s(F, n) ≤ (en/d)^d; ERM is consistent iff the VC dimension is finite.
- Exemplo 9.5: VC theory justifies tuning-parameter choice by data splitting.
- §9.5.1 Prova do teorema VC (pp. 184–186): Hoeffding's inequality (Teorema 13, Corolário 1), symmetrization lemma (Lema 3), union bound over s(F, 2n) patterns.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §9.6 — Resumo (p. 186)
**Subtopics:**
- 0-1 risk plus sensitivity/specificity and cost-weighted risks; Bayes classifier motivates plug-in methods; tools for non-i.i.d. prediction settings.

## Ch. 10 — Redução de Dimensionalidade e Mudança de Representação
**Pages:** pp. 189–208 (Parte III — Aprendizado não supervisionado, p. 187)

### §10.1 — Componentes Principais (PCA - Principal Component Analysis) (pp. 190–198)
**Subtopics:**
- Principal components as variance-maximizing, mutually uncorrelated linear combinations Z₁ = φ₁₁X₁ + … + φ_d1X_d of centred covariates; eigen-decomposition XᵀX = UΣUᵀ, scores Z = XU.
- §10.1.1 Interpretação alternativa: escalonamento multidimensional (PCA preserves pairwise Euclidean distances best among linear maps; Zip Code digits, Exemplo 10.1); §10.1.2 Aplicação: compressão de imagens (reconstruction from the first m components).

### §10.2 — Kernel PCA (KPCA) (pp. 198–201)
**Subtopics:**
- Non-linear components via the kernel trick: eigenvectors of the Gram matrix instead of XᵀX.

### §10.3 — Projeções Aleatórias (pp. 201–202)
**Subtopics:**
- Random Gaussian projections zᵢ = Σ s_{i,k}xₖ/√m; Teorema 14 (Johnson–Lindenstrauss): m ≥ 32 log n/ε² preserves all pairwise distances within (1 ± ε) with high probability.

### §10.4 — Autoencoders (pp. 202–208)
**Subtopics:**
- Neural networks whose output reproduces the input through a narrow hidden layer, trained on reconstruction error; worked example with reconstruction error plots (Figura 10.10).

## Ch. 11 — Análise de Agrupamento
**Pages:** pp. 209–222

### §11.1 — K-Médias (pp. 210–215)
**Subtopics:**
- Minimize the within-cluster sum of squares Σₖ |Cₖ|⁻¹ Σ_{i,j∈Cₖ} d²(xᵢ, xⱼ) for a fixed K; Lloyd's algorithm as an iterative approximation without global guarantees.

### §11.2 — Agrupamento Espectral (pp. 215–219)
**Subtopics:**
- Diffusion maps: a Markov random walk on the data built from a Mercer kernel defines a diffusion distance that captures connectivity better than Euclidean distance; k-means run on the diffusion-map coordinates (leading eigenvectors) separates non-convex clusters that plain k-means misses (Figura 11.4).

### §11.3 — Métodos Hierárquicos (pp. 219–222)
**Subtopics:**
- Agglomerative merging of the closest clusters into a dendrogram (no K needed in advance); single, complete, average and centroid linkage (hclust, cutree, factoextra::fviz_dend).

## Ch. 12 — Regras de Associação
**Pages:** pp. 223–228

### Ch. 12 (no numbered sections) (pp. 223–228)
**Subtopics:**
- Market-basket rules A ⇒ B on binary purchase data; support of an itemset P(∩_{i∈S} Xᵢ = 1), Apriori algorithm (Agrawal et al., 1993) exploiting monotone support; confidence P̂(B | A) and lift P̂(B | A)/P̂(B) (arules, Groceries data).

## Ch. 13 — Sistemas de Recomendação
**Pages:** pp. 229–234

### §13.1 — Filtro Colaborativo Baseado no Usuário (pp. 230–231)
**Subtopics:**
- KNN over users: Pearson-correlation similarity on co-rated items, predict Rⱼ,ₗ as the mean rating of the k most similar users who rated item l.

### §13.2 — Filtro Colaborativo Baseado no Produto (p. 231)
**Subtopics:**
- Same idea over items: average of user j's ratings of the k items most similar to l.

### §13.3 — FunkSVD (pp. 231–232)
**Subtopics:**
- Latent-factor model Rⱼ,ₗ ≈ uⱼᵀvₗ fitted by stochastic gradient descent on the observed ratings.

### §13.4 — Seleção de Modelos (pp. 232–234)
**Subtopics:**
- Data splitting over users with hidden ratings; MSE, RMSE, MAE; top-N recommendation confusion matrix with accuracy, precision and recall (Tabela 13.2), compared on MovieLense (recommenderlab).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

## Apêndice A — Apêndice
**Pages:** pp. 237–242 (Parte IV — Apêndice, p. 235)

### §A.1 — Imagens (pp. 237–240)
**Subtopics:**
- Raster images as pixel matrices (binary, greyscale, RGB channels) turned into covariate vectors.

### §A.2 — Textos (pp. 240–241)
**Subtopics:**
- Bag-of-words representation and the document-term matrix (Tabela A.1) used in the Amazon examples.

### §A.3 — Matrizes esparsas (pp. 241–242)
**Subtopics:**
- Sparse (row, column, value) storage of mostly-zero matrices; glmnet accepts sparse input, lm does not.


# Bolfarine & Sandoval, Introdução à Inferência Estatística (2010)
#book/bolfarine
> Link: [[Livros/Bolfarine, Sandoval - Introdução à Inferência Estatística (2010)|Bolfarine & Sandoval]]

> Page numbers are printed book pages. PDF-to-printed offset: printed = PDF page − 6, constant through the whole file (verified from printed folios: PDF 8 = p. 2, PDF 49 = p. 43, PDF 126 = p. 120).
> TOC warning: the printed "CONTEÚDO" (PDF pp. 3–4) carries page numbers from a different layout and does not match the folios (e.g. it gives §1.4 at p. 17, §3.1 at p. 46, §4.1 at p. 49, "REFERÊNCIAS" at p. 155). All pages below are read from the running heads, not the TOC. The TOC also lists an "ÍNDICE REMISSIVO" (p. 156) that is not in this PDF; the text ends with "Referências" (pp. 119–120). Pages 56, 90 and 118 are blank.
> Language note: Portuguese text; titles below are verbatim. The preface is dated "São Paulo, setembro de 2000".

## Ch. 1 — Elementos Básicos
**Pages:** pp. 1–14

### §1.1 — Alguns Modelos Especiais (pp. 1–3)
**Subtopics:**
- §1.1.1 O modelo normal (p. 1): N(μ, σ²) density, support the whole real line, E[X] = μ, Var[X] = σ².
- §1.1.2 O modelo exponencial (pp. 1–2): Exp(θ) density θe^(−θx), mean 1/θ, variance 1/θ², and the memoryless property for lifetimes.
- §1.1.3 O modelo binomial (p. 2): Binomial(n, θ) as a sum of n independent Bernoulli(θ) variables, mean nθ, variance nθ(1 − θ).
- §1.1.4 O modelo de Poisson (pp. 2–3): Poisson(θ) probability function e^(−θ)θ^x/x!, with E[X] = Var[X] = θ, for counts in a fixed time interval.
- §1.1.5 O modelo uniforme (p. 3): U(0, θ) written with an indicator function; its support depends on θ, unlike the four models above.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] — **Assigned reading (Class 1)**: §1.1.4 only (pp. 2–3); §1.1.5 backs the U(0, θ) estimators in the MSE deck (related, not assigned).

### §1.2 — Tipos de Problemas (p. 4)
**Subtopics:**
- Definition 1.2.1: statistical inference as specifying values of an unknown θ from observed data; estimation versus hypothesis testing.

### §1.3 — Amostras, Estatísticas e Estimadores (pp. 4–13)
**Subtopics:**
- definitions of population, random sample (i.i.d. draws), and the likelihood function L(θ; x) = ∏ f(xᵢ|θ) (1.3.1).
- statistic, parameter space Θ, estimator of θ and of g(θ) (Definitions 1.3.3–1.3.6).
- mean squared error and its decomposition MSE = Var + bias² (1.3.2); unbiased and asymptotically unbiased estimators.
- the sample mean is unbiased; the variance estimator with divisor n is biased but asymptotically unbiased (1.3.3).
- comparing estimators by MSE: better estimator, inadmissible estimator, optimal estimator and the uniformly minimum-variance unbiased estimator.
- the sample mean is the minimum-variance linear unbiased estimator (convex weights, also via Lagrange multipliers).
- normal variance: S² (unbiased) versus σ̂² (biased) — σ̂² has the smaller MSE.
- Bernoulli: X̄ versus the constant-MSE estimator (Y + √n/2)/(n + √n); neither dominates (Figure 1.1).
- U(0, θ): X̄ (biased, mean θ/2) versus the maximum X(n), MSE comparison table (Table 1.1); X(n) is better for every θ and n > 1.
- discrete uniform (taxi/urn) problem: estimating N with X̄, X(n), 2X̄ − 1 and an exactly unbiased N̂₅.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] — **Assigned reading (Class 1)**

### §1.4 — Exercícios (pp. 13–14)
**Subtopics:**
- exercises 1.1–1.13: MSE decomposition, bias of σ̂², order statistics of the uniform, MSE comparisons. See [[bolfarine-exercises]].

## Ch. 2 — Estimadores Eficientes e Estatísticas Suficientes
**Pages:** pp. 15–34

### §2.1 — Estimadores Eficientes (pp. 15–19)
**Subtopics:**
- efficiency of an unbiased estimator, e(θ̂) = LI(θ)/Var[θ̂], with LI(θ) the lower bound for the variance of unbiased estimators (Definition 2.1.1).
- regularity conditions: support not depending on θ, and differentiation under the integral sign.
- score function ∂ log f(X|θ)/∂θ and its zero expectation (2.1.4).
- Fisher information I_F(θ) = E[(∂ log f/∂θ)²] = −E[∂² log f/∂θ²], and additivity: n I_F(θ) for a random sample (2.1.6).
- Theorem 2.1.1, the information inequality (Cramér–Rao lower bound) Var[θ̂] ≥ 1/(n I_F(θ)), proved via the correlation between θ̂ and the score.
- the sample mean is efficient for the normal mean (Example 2.1.1) and for the Poisson mean (Example 2.1.2).
- the bound checks efficiency; it is not a method for constructing estimators.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] — **Assigned reading (Class 1)**

### §2.2 — Estatísticas Suficientes (pp. 20–23)
**Subtopics:**
- Definition 2.2.1: T is sufficient for θ when the conditional distribution of the sample given T does not depend on θ.
- ΣXᵢ is sufficient for Bernoulli θ (Example 2.2.1) and for Poisson θ (Example 2.2.3); X₁ + 2X₂ + X₃ is not sufficient for Bernoulli θ (Example 2.2.2).
- Theorem 2.2.1, the Neyman factorization criterion L(θ; x) = h(x) g_θ(T(x)), proved for the discrete case.
- factorization applied: Poisson (ΣXᵢ), U(0, θ) (X(n)), N(μ, 1) (ΣXᵢ).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] — **Assigned reading (Class 1)**

### §2.3 — Estatísticas Conjuntamente Suficientes (pp. 23–25)
**Subtopics:**
- Theorem 2.3.1, the factorization criterion for a parameter vector: jointly sufficient statistics of dimension r.
- (ΣXᵢ, ΣXᵢ²) jointly sufficient for (μ, σ²) in the normal model.
- equivalent statistics (one-to-one maps) are sufficient together: (X̄, S²) for the normal model, (Σ log Xᵢ, X̄) for the gamma model.

### §2.4 — Famílias Exponenciais (pp. 25–29)
**Subtopics:**
- Definition 2.4.1, the one-parameter exponential family f(x|θ) = exp{c(θ)T(x) + d(θ) + S(x)}, with support not depending on θ.
- Bernoulli and N(μ, 1) written in exponential-family form.
- Theorem 2.4.1: a random sample from an exponential family is again an exponential family, so ΣT(Xᵢ) is sufficient.
- Definition 2.4.2, the k-parameter exponential family; N(μ, σ²) as a two-parameter member.
- bivariate normal as a five-parameter exponential family; sample means, variances and the Pearson correlation as functions of the sufficient statistic.

### §2.5 — Estimadores Baseados em Estatísticas Suficientes (pp. 29–32)
**Subtopics:**
- conditioning an unbiased estimator on a sufficient statistic, θ̂ = E[S|T], keeps it unbiased.
- Rao–Blackwell theorem: Var[E[S|T]] ≤ Var[S], via the law of total variance.
- Poisson example: Rao–Blackwellizing the indicator of {X₁ = 0} gives ((n − 1)/n)^ΣXᵢ for e^(−θ).
- complete statistics (Definition 2.5.1); ΣXᵢ complete for Bernoulli, X₁ − X₂ not complete.
- Theorem 2.5.2: the natural statistic of a k-parameter exponential family is sufficient and complete when the range of c(θ) contains a k-dimensional rectangle.
- Lehmann–Scheffé theorem (Theorem 2.5.3): E[S|T] with T sufficient and complete is the unique UMVUE ("ENVVUM"); X̄ is the UMVUE of the Poisson mean.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (related, not assigned)

### §2.6 — Exercícios (pp. 32–34)
**Subtopics:**
- exercises 2.1–2.12: Cramér–Rao bounds, sufficiency, exponential families, Rao–Blackwell and UMVUEs, including a regression model Yᵢ ~ N(βxᵢ, σ²). See [[bolfarine-exercises]].

## Ch. 3 — Métodos de Estimação
**Pages:** pp. 35–55

### §3.1 — O Método de Máxima Verossimilhança (pp. 35–42)
**Subtopics:**
- likelihood L(θ; x) = ∏ f(xᵢ|θ) and log-likelihood l(θ; x) (Definition 3.1.1); the MLE maximizes L (Definition 3.1.2).
- likelihood equation l′(θ; x) = 0 with the second-order check l″(θ̂; x) < 0 (3.1.3–3.1.4).
- MLE of the normal mean is X̄ (Example 3.1.1) and of the Bernoulli θ is X̄ (Example 3.1.2).
- U(0, θ): the likelihood equation fails and the MLE X(n) is found by inspecting L (boundary maximum; the MLE is biased).
- discrete parameter space: choosing θ ∈ {1/3, 2/3} by comparing likelihood values (Example 3.1.4).
- non-unique MLE for U(θ − 1/2, θ + 1/2): any point in [x(n) − 1/2, x(1) + 1/2] (Example 3.1.5).
- numerical MLE: Newton–Raphson iteration on the score U(θ), and Fisher scoring (replacing U′ by −n I_F); worked example with f(x|θ) = (1 + θx)/2, data generated by the inverse-CDF method (Tables 3.1–3.2).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] — **Assigned reading (Class 1)**

### §3.2 — Propriedades dos Estimadores de Máxima Verossimilhança (pp. 42–45)
**Subtopics:**
- Theorem 3.2.1: the MLE, if it exists, is a function of any sufficient statistic.
- §3.2.1 Invariância (pp. 43–44): Theorem 3.2.2, MLE invariance — g(θ̂) is the MLE of g(θ); examples θ(1 − θ) for Bernoulli, Φ(−μ) for the normal, e^(−θ) for the exponential.
- §3.2.2 Distribuição em grandes amostras (pp. 44–45): asymptotic normality of the MLE, √n(θ̂ − θ) → N(0, 1/I_F(θ)), and the delta-method version for g(θ̂) (3.2.3–3.2.4); the MLE is asymptotically unbiased and efficient; Bernoulli and Poisson e^(−X̄) examples.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] — **Assigned reading (Class 1)**

### §3.3 — Verossimilhança para Amostras Independentes (pp. 45–46)
**Subtopics:**
- the joint likelihood of independent samples is the product of their likelihoods (log-likelihoods add).
- common mean from N(μ, 4) and N(μ, 9) samples: the MLE is the precision-weighted mean, a function of the sufficient statistic.

### §3.4 — O Caso Multiparamétrico (pp. 46–49)
**Subtopics:**
- likelihood equations for θ = (θ₁, …, θ_r); boundary or support-dependent cases need inspection of L.
- profile likelihood: solve for θ₁ as a function of θ₂ and maximize the profiled g(θ₂; x).
- normal MLEs μ̂ = X̄ and σ̂² = Σ(Xᵢ − X̄)²/n via the profile likelihood.
- two normal samples with a common variance: the MLE of σ² pools both sums of squares over n + m.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (related, not assigned): profile likelihood of the coal-mining cut point

### §3.5 — Família Exponencial e o Método de Máxima Verossimilhança (pp. 49–50)
**Subtopics:**
- in an exponential family the MLE solves E[T(X)] = T(X) (3.5.1), and E[T_j(X)] = T_j(X) in k dimensions (3.5.2).
- Hardy–Weinberg proportions: θ̂ = (2N₁ + N₂)/2n.
- bivariate normal MLEs recovered from the moment equations of the sufficient statistic.

### §3.6 — O Método dos Momentos (pp. 50–51)
**Subtopics:**
- method of moments: equate sample moments m_r to population moments μ_r, r = 1, …, k.
- taxi problem: N̂ = 2X̄ − 1, which is not a function of the sufficient statistic X(n).
- gamma(α, β): moment estimators α̂ = X̄²/σ̂², β̂ = X̄/σ̂², used as starting values for the numerical MLE.

### §3.7 — Estimadores Consistentes (p. 52)
**Subtopics:**
- consistency as convergence in probability, lim P(|θ̂ − θ| > ε) = 0 (Definition 3.7.1).
- Chebyshev's inequality shows X̄ is consistent for the mean.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (related, not assigned)

### §3.8 — Exercícios (pp. 52–55)
**Subtopics:**
- exercises 3.1–3.21: MLEs and their large-sample distributions, invariance, method of moments, Weibull and Gumbel-type numerical MLEs, consistency, and MLE versus least squares in simple regression. See [[bolfarine-exercises]].

## Ch. 4 — Introdução à Teoria das Decisões. Os Princípios Minimax e de Bayes
**Pages:** pp. 57–72

### §4.1 — Os Elementos Básicos (pp. 57–60)
**Subtopics:**
- elements of a decision problem: parameter space Θ, action space A, decision function d, and loss l(θ, a) (quadratic, absolute, and c(θ)|θ − a|^r).
- risk function R(θ, d) = E[l(θ, d(X))] (Definition 4.1.1), the "better than" ordering and inadmissibility (Definition 4.1.2).
- coin example with Θ = {1/3, 2/3}: risks of four decision rules (Table 4.1); d₄ is inadmissible.

### §4.2 — O Princípio Minimax (pp. 60–61)
**Subtopics:**
- minimax rule: minimize the maximum risk (Definition 4.2.1).
- coin example: d₁ is minimax; Poisson with loss (θ − a)²/θ: d(X) = X is minimax in the class {cX}.

### §4.3 — O Princípio de Bayes (pp. 61–63)
**Subtopics:**
- prior distribution π(θ) and Bayes risk r(π, d) = E_π[R(θ, d)] (Definition 4.3.1); Bayes decision rule (Definition 4.3.2).
- coin example: the Bayes rule depends on the prior weight p and need not be unique.
- Poisson with an Exp(1) prior: Bayes rule X/2 within the class {cX}.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]] (related, not assigned)

### §4.4 — Estimadores de Bayes com Perda Quadrática (pp. 63–70)
**Subtopics:**
- Theorem 4.4.1: under quadratic loss the Bayes estimator is the posterior mean E[θ|X] (Bayes estimator under quadratic loss); posterior π(θ|x) = f(x|θ)π(θ)/g(x), marginal g(x).
- Bayes estimators are not invariant, unlike MLEs.
- beta–Bernoulli conjugacy: posterior Beta(Σxᵢ + a, n − Σxᵢ + b), posterior mean (Σxᵢ + a)/(n + a + b); uniform prior gives (ΣXᵢ + 1)/(n + 2), with risk and Bayes risk 1/(6(n + 2)).
- gamma–Poisson conjugacy: posterior Gamma(Σxᵢ + a, n + b) and its risk.
- normal–normal conjugacy with known variance: the posterior mean is a convex combination of X̄ and the prior mean a; prior influence fades as n grows or as b → ∞.
- Theorem 4.4.2: the Bayes estimator depends on the data only through a sufficient statistic.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]] (related, not assigned)

### §4.5 — Exercícios (pp. 70–72)
**Subtopics:**
- exercises 4.1–4.12: risks, minimax and Bayes rules in restricted classes, conjugate posteriors (Pareto–uniform, gamma–exponential, gamma–Poisson) and Bayes estimators. See [[bolfarine-exercises]].

## Ch. 5 — Estimação por Intervalo
**Pages:** pp. 73–89

### §5.1 — Amostras de Populações Normais (pp. 73–75)
**Subtopics:**
- Theorem 5.1: for a normal sample, X̄ and S² are independent, (n − 1)S²/σ² ~ χ²_{n−1}, and √n(X̄ − μ)/S ~ t_{n−1}; proofs by moment generating functions.

### §5.2 — O Método da Quantidade Pivotal (pp. 75–80)
**Subtopics:**
- pivotal quantity Q(X; θ) whose distribution is free of θ (Definition 5.2.1), and inversion into a confidence interval with coefficient γ = 1 − α.
- exponential: 2θΣXᵢ ~ χ²_{2n} gives an exact interval; simulated data by the inverse-CDF method (Tables 5.1–5.2).
- uniform: X(n)/θ is pivotal; equal-tail interval and the frequentist reading of the confidence coefficient.

### §5.3 — Intervalos para Populações Normais (pp. 80–83)
**Subtopics:**
- §5.3.1 O caso de uma única amostra (pp. 80–81): z-interval for μ with σ² known, t-interval with σ² unknown, and χ² interval for σ².
- §5.3.2 Duas amostras independentes (pp. 82–83): interval for μ₁ − μ₂ with pooled variance S_p² (t_{n+m−2}), and the F-based interval for σ₁²/σ₂².

### §5.4 — Intervalos de Confiança Aproximados (pp. 83–85)
**Subtopics:**
- approximate pivots from the asymptotic normality of the MLE, with I_F(θ) replaced by I_F(θ̂) (5.4.1), and a delta-method pivot for g(θ) (5.4.2).
- Bernoulli: Wald interval for θ and for θ(1 − θ); exponential: approximate interval for θ, compared with the exact one.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (related, not assigned)

### §5.5 — Intervalos de Confiança Bayesianos (pp. 85–87)
**Subtopics:**
- Bayesian (credible) interval: posterior probability γ over [t₁, t₂] (Definition 5.5.1); the shortest one is the highest posterior density (HPD) interval.
- normal mean with a N(μ₀, 1) prior: symmetric HPD interval.
- uniform with a Pareto prior: equal-tail interval from the Pareto posterior, which is not HPD.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]] (related, not assigned)

### §5.6 — Exercícios (pp. 87–89)
**Subtopics:**
- exercises 5.1–5.14: pivotal quantities, normal-theory intervals, approximate MLE-based intervals, and Bayesian intervals for Poisson and gamma posteriors. See [[bolfarine-exercises]].

## Ch. 6 — Testes de Hipóteses
**Pages:** pp. 91–117

### §6.1 — Idéias Básicas (pp. 91–92)
**Subtopics:**
- informal motivation for testing (a jury trial, a vaccine trial) and the two possible errors.

### §6.2 — Formulação Estatística (pp. 92–94)
**Subtopics:**
- statistical hypothesis, simple versus composite hypotheses (Definition 6.2.1), and a test as a decision function with acceptance and critical regions (Definition 6.2.2).
- type I and type II error probabilities α and β as risks under 0–1 loss (Table 6.1); power π(θ₁) = 1 − β (Definition 6.2.3).
- normal-mean example: choosing the cutoff c for a level-0.05 test.

### §6.3 — Hipótese Nula Simples contra Alternativa Simples. Testes Mais Poderosos (pp. 94–100)
**Subtopics:**
- Lemma 6.3.1: the test minimizing aα + bβ rejects when L₁(x)/L₀(x) ≥ a/b.
- Neyman–Pearson lemma (Lemma 6.3.2): the likelihood-ratio critical region is most powerful at its level.
- most powerful tests for the normal mean (ΣXᵢ ≥ c), the normal variance with known mean (χ²), and Bernoulli θ (binomial cutoff, normal approximation).
- p-value ("nível descritivo") as the smallest level at which H₀ is rejected (Definition 6.3.1).

### §6.4 — Testes Uniformemente Mais Poderosos (pp. 100–103)
**Subtopics:**
- §6.4.1 Hipótese nula simples contra alternativa composta (pp. 100–102): uniformly most powerful (UMP) tests (Definition 6.4.1); one-sided normal and Bernoulli examples; no UMP test exists for a two-sided alternative; power function (Definition 6.4.2, Figure 6.1).
- §6.4.2 Hipóteses compostas (pp. 102–103): Theorem 6.4.1 — in an exponential family the one-sided UMP test for θ = θ₀ is also UMP for θ ≤ θ₀ (and symmetrically).

### §6.5 — Testes da Razão de Verossimilhanças Generalizada (pp. 103–114)
**Subtopics:**
- generalized likelihood ratio test (GLRT, "TRVG"): λ(x) = sup_{Θ₀} L / sup_Θ L, and the five-step recipe using the unrestricted and restricted MLEs.
- two-sided z-test and its power function (Figure 6.2); t-test for μ with σ² unknown; χ² test for σ²; a shifted-exponential location test.
- Theorem 6.5.1: −2 log λ(X) is asymptotically χ² with degrees of freedom equal to the difference in free parameters (Wilks); Poisson example.
- two-sample tests: pooled t-test for equal normal means, F-test for equal variances, asymptotic test for two Bernoulli proportions.
- multinomial (three-type) MLEs and the Hardy–Weinberg GLRT; Pearson chi-square statistic as its large-sample equivalent.
- duality between tests and confidence intervals.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (related, not assigned): LR test of one vs two Poisson rates in the coal-mining deck

### §6.6 — Testes Bayesianos (p. 114)
**Subtopics:**
- Bayesian test of a point null by checking whether θ₀ lies in the Bayesian (credible) interval; normal mean with a N(0, 1) prior.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]] (related, not assigned)

### §6.7 — Exercícios (pp. 115–117)
**Subtopics:**
- exercises 6.1–6.17: most powerful and UMP tests, power functions, GLRTs for one and two samples, multinomial goodness of fit, and the paired t-test. See [[bolfarine-exercises]].

## Referências (pp. 119–120)
**Subtopics:**
- seven references: Bickel & Doksum (1977), Bussab & Morettin (1987), DeGroot (1989), Feller (1976), James (1981), Lehmann (1986), Sen & Singer (1993).


# Morettin & Singer, Estatística e Ciência de Dados (preliminary version, April 2021)
#book/morettin-singer
> Link: [[Livros/Morettin, Singer - Estatística e Ciência de Dados (versão preliminar, abril 2021)|Morettin & Singer]]

> Page numbers are printed book pages (checked against the running heads of the PDF text). PDF-to-printed offset: constant, 1-based PDF page − 10 = printed page (printed p. 1 = PDF p. 11; roman front matter on PDF pp. 1–10). Preliminary version: numbering may differ from the 2022 LTC print edition.

> Coverage notes: the book has no time-series chapter (only AR(1) errors and the Durbin–Watson test in §6.2) and no dedicated Bayesian chapter (the Bayes classifier in §8.3.1 and posterior/data-augmentation material in Appendices B–C). Cross-validation is introduced in §1.3 and §1.6.1 and formalized in Nota 1 of §8.6 (the cross-references in §1.3 and §8.1 say "Nota de Capítulo 2", a numbering slip); the bootstrap appears inside bagging (§10.3.1) and the Ch. 10 notes.

## Ch. 1 — Estatística, Ciência de Dados e Megadados
**Pages:** pp. 1–20

### §1.1 — Introdução (pp. 1–4)
**Subtopics:**
- Data Science as statistics plus computation (Tukey, Breiman, Donoho, Efron & Hastie); the sample mean (1.1) and its standard error (1.2) as an example of algorithm plus inference.

### §1.2 — Aprendizado com Estatística (p. 4)
**Subtopics:**
- Supervised learning (prediction of a numeric response, classification of a qualitative one) vs unsupervised learning (association, grouping, dimension reduction); statistical inference as the broader aim.
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.3 — Aprendizado automático (pp. 4–6)
**Subtopics:**
- Machine learning vs "artificial intelligence" (Jordan 2019's three senses of AI; Turing 1950; Dartmouth 1955); classical rule-based programming vs training on data.
- Training vs validation sets; repeated random splitting with averaged prediction error as cross-validation (points to Note 2 of Ch. 8); refit the chosen model on the full data; prediction goal differs from interpreting coefficients.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.4 — Uma cronologia do desenvolvimento da Estatística (pp. 6–8)
**Subtopics:**
- §1.4.1 Probabilidades (p. 7) and §1.4.2 Estatística (p. 7): from Bayes and Laplace to Fisher and Neyman–Pearson; logistic regression, GLMs (Nelder & Wedderburn 1970), GAMs, bootstrap (Efron), ridge (Hoerl & Kennard 1970), CART, LASSO (Tibshirani 1996).
- §1.4.3 Estatística e computação (p. 8): computing eras and the R/CRAN ecosystem.

### §1.5 — Notação e tipos de dados (pp. 8–10)
**Subtopics:**
- Data matrix X (n × p), response vector y, data pairs (xᵢ, yᵢ); regimes n ≫ p, p ≫ n, both large; high-dimensional data; structured vs unstructured big data.

### §1.6 — Paradigmas para o aprendizado com Estatística (pp. 10–15)
**Subtopics:**
- Framework for supervised and unsupervised learning used by the rest of the book.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §1.6.1 — Aprendizado supervisionado (pp. 10–14)
**Subtopics:**
- Model yᵢ = f(xᵢ) + eᵢ (1.3) with E(eᵢ) = 0; reducible vs irreducible error, E(ŷᵢ − yᵢ)² = E[f(xᵢ) − f̂(xᵢ)]² + Var(eᵢ) (1.4).
- Parametric vs non-parametric estimation of f (kernels, local polynomials/lowess, splines, orthogonal bases); flexibility vs interpretability; overfitting.
- Training MSE (1.5), RMSE, and validation MSE (1.6) for model choice; cross-validation previewed (points to Note 1 of Ch. 8).
- Bias–variance decomposition E[y₀ − f̂(x₀)]² = Var[f̂(x₀)] + [Bias(f̂(x₀))]² + Var(e₀) (1.7); U-shaped validation error against model size.
- Classification: risk L(g) = P{g(X) ≠ Y}, training error rate (1.8) and validation error rate (1.9); Bayes classifier maximizing P(y = j | x = x₀) (1.10) and the Bayes error rate.
- K-nearest-neighbour estimate of the conditional class probabilities; choice of K.

#### §1.6.2 — Aprendizado não supervisionado (pp. 14–15)
**Subtopics:**
- Cluster analysis with Euclidean (and non-Euclidean) distances, divisive vs agglomerative; dimension reduction (principal and independent components) as preprocessing for regression.

### §1.7 — Este livro (pp. 15–17)
**Subtopics:**
- Data science as a multidisciplinary pipeline (question, data, organization, description, method, algorithm, presentation); chapter plan; R packages used (caret, MASS, mgcv, nlme, randomForest, xgboost, …).

### §1.8 — Conjuntos de dados (pp. 17–18)
**Subtopics:**
- Table 1.1: the data sets used in examples and exercises, downloadable as .xls files from the authors' site.

### §1.9 — Notas de capítulo (pp. 19–20)
**Subtopics:**
- Reproductions of the first page of Turing (1950) and of the 1955 Dartmouth AI proposal.

## Ch. 2 — Preparação dos dados
**Pages:** pp. 23–41

### §2.1 — Considerações preliminares (pp. 23–26)
**Subtopics:**
- Populations vs samples; observational, sample-survey and experimental studies; units of investigation and variables; explanatory vs response variables.

### §2.2 — Planilhas de dados (pp. 26–31)
**Subtopics:**
- Building a data spreadsheet: data dictionary (operational definitions, mnemonic labels, units/categories), one row per unit, wide vs long layout for longitudinal data.

### §2.3 — Construção de tabelas (pp. 31–33)
**Subtopics:**
- Rules for tables: few decimals, self-explanatory titles, totals, ordering, row vs column percentages.

### §2.4 — Construção de gráficos (pp. 33–34)
**Subtopics:**
- Rules for graphs: titles, axis labels with units, scales, axis breaks, legends, avoiding area comparisons and chartjunk.

### §2.5 — Notas de capítulo (pp. 34–38)
**Subtopics:**
- Notes 1–4: data warehouses; operational definition of variables; order of magnitude, precision and rounding; proportions and percentages.

### §2.6 — Exercícios (pp. 38–41)
**Subtopics:**
- 9 exercises on preparing data dictionaries and spreadsheets (morfina, esforco, cidades data).

## Ch. 3 — Análise de dados de uma variável
**Pages:** pp. 43–91

### §3.1 — Introdução (pp. 43–44)
**Subtopics:**
- Aims of univariate description: frequency distribution, typical values, location, dispersion, shape.

### §3.2 — Distribuições de frequências (pp. 44–54)
**Subtopics:**
- §3.2.1 Variáveis qualitativas (p. 46): absolute/relative frequency tables, bar and pie charts; §3.2.2 Variáveis quantitativas (p. 48): class grouping, histograms, stem-and-leaf and dot plots (FGV questionnaire, ceagfgv data).

### §3.3 — Medidas resumo (pp. 54–62)
**Subtopics:**
- §3.3.1 Medidas de posição (p. 54): mean, median, trimmed mean, quantiles; §3.3.2 Medidas de dispersão (p. 56): variance (unbiased S²), standard deviation, mean absolute deviation, interquartile range; §3.3.3 Medidas de forma (p. 59): Fisher–Pearson skewness and kurtosis coefficients, symmetry plots.

### §3.4 — Boxplots (pp. 62–64)
**Subtopics:**
- Boxplot construction from Q1, median, Q3 and whiskers at 1.5 × IQR; outliers; side-by-side comparison of distributions.

### §3.5 — Modelos probabilísticos (pp. 64–67)
**Subtopics:**
- Probability models linking sample and population; discrete and continuous distributions; histogram approximated by a density.

### §3.6 — Dados amostrais (pp. 67–68)
**Subtopics:**
- Simple random sample (i.i.d. draws); correlated data as one trajectory of a stochastic process.

### §3.7 — Gráficos QQ (pp. 68–73)
**Subtopics:**
- Empirical distribution function; normal QQ plots comparing sample and theoretical quantiles; chi-squared QQ plots for skewed data.

### §3.8 — Desvio padrão e erro padrão (pp. 73–76)
**Subtopics:**
- Sampling distribution of the mean: E(X̄) = µ, Var(X̄) = σ²/n, approximate normality (CLT, illustrated by simulation); standard deviation vs standard error.

### §3.9 — Intervalo de confiança (pp. 76–78)
**Subtopics:**
- Approximate 95% confidence intervals X̄ ± 1.96 S/√n for a mean and p̂ ± 1.96 √(p̂(1 − p̂)/n) for a proportion; margin of error and interpretation.

### §3.10 — Transformação de variáveis (pp. 78–80)
**Subtopics:**
- Box–Cox family of power transformations to symmetrize skewed data and stabilize variance (log, square root, cube root).

### §3.11 — Notas de capítulo (pp. 80–83)
**Subtopics:**
- Notes 1–6: continuous variables; histogram bin width (Freedman–Diaconis); definition of the histogram; an alternative estimator of the standard deviation; standardization; confidence bands for QQ plots.

### §3.12 — Exercícios (pp. 83–91)
**Subtopics:**
- 33 exercises on frequency tables, summary measures, boxplots, QQ plots and transformations.

## Ch. 4 — Análise de dados de duas variáveis
**Pages:** pp. 93–144

### §4.1 — Introdução (pp. 93–94)
**Subtopics:**
- Association between two variables; three cases (qualitative–qualitative, quantitative–quantitative, mixed); explanatory vs response roles.

### §4.2 — Duas variáveis qualitativas (pp. 94–107)
**Subtopics:**
- Contingency tables, Pearson's chi-squared statistic and contingency coefficients; attributable risk, relative risk and odds ratio in prospective vs retrospective studies.
- Diagnostic tests (pp. 104–107): sensitivity, specificity, false positives/negatives, positive and negative predictive values and accuracy from the 2 × 2 table; predictive values depend on prevalence.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §4.3 — Duas variáveis quantitativas (pp. 107–119)
**Subtopics:**
- Scatter plots, covariance, Pearson and Spearman correlation; profile plots; agreement between observers with QQ plots and Tukey mean–difference (Bland–Altman) plots.

### §4.4 — Uma variável qualitativa e outra quantitativa (pp. 119–126)
**Subtopics:**
- Comparing distributions across groups with side-by-side boxplots and summary measures; one-way ANOVA model as a preview of regression.

### §4.5 — Notas de capítulo (pp. 126–135)
**Subtopics:**
- Notes 1–8: conditional probability and odds ratios; measures of dependence; linear dependence; robust dependence measures; PP plots; "significant" differences; confidence intervals for relative risk, odds ratio and sensitivity; a naive interpretation of the p-value.

### §4.6 — Exercícios (pp. 135–144)
**Subtopics:**
- 28 exercises on contingency tables, odds ratios, correlation, Bland–Altman plots and diagnostic-test characteristics.

## Ch. 5 — Análise de dados de várias variáveis
**Pages:** pp. 145–180

### §5.1 — Introdução (pp. 145–146)
**Subtopics:**
- Multivariate data matrices and joint distributions of p variables.

### §5.2 — Gráficos para três variáveis (pp. 146–159)
**Subtopics:**
- Draftsman's display (scatter-plot matrix with correlations), symbolic scatter plots, lowess-smoothed panels (ggplot2); main effects and interaction in two-factor designs with mean-profile plots and two-way ANOVA (pp. 153–159).

### §5.3 — Gráficos para quatro ou mais variáveis (pp. 159–160)
**Subtopics:**
- Draftsman's displays for four or more variables (tree-bark element concentrations).

### §5.4 — Medidas resumo multivariadas (pp. 160–161)
**Subtopics:**
- Mean vector, covariance and correlation matrices of a data matrix.

### §5.5 — Tabelas de contingência de múltiplas entradas (pp. 161–164)
**Subtopics:**
- Three-way contingency tables; joint, marginal and conditional independence; stratified odds ratios combined by Mantel–Haenszel.

### §5.6 — Notas de capítulo (pp. 164–175)
**Subtopics:**
- Notes 1–4: matrix notation for multivariate summaries; lowess smoothing; mean-deviation parametrization of ANOVA models; the Mantel–Haenszel statistic.

### §5.7 — Exercícios (pp. 175–180)
**Subtopics:**
- 11 exercises on multivariate graphs, interaction plots and multi-way tables.

## Ch. 6 — Análise de Regressão
**Pages:** pp. 181–242

> Ch. 6 has no numbered subsections; its regression results are split between the sections and the numbered chapter notes of §6.6, which are indexed below as subsections (note titles verbatim).

### §6.1 — Introdução (pp. 181–184)
**Subtopics:**
- Simple linear regression yᵢ = α + βxᵢ + eᵢ (6.1) with E(eᵢ) = 0 as a model for E(y | x); centring the regressor (6.2) to make α interpretable.
- "Linear" means linear in the parameters: (6.3) is non-linear, the quadratic (6.4) is a linear (polynomial) model.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §6.2 — Regressão linear simples (pp. 184–203)
**Subtopics:**
- Least squares Q(α, β) (6.5); closed-form β̂ (6.6) and α̂ = ȳ − β̂x̄ (6.7); unbiased S² = SQRes/(n − 2) (6.8); fitted values and residuals; R² = SQReg/SQTot; reading lm() output.
- Residual plots and standardized (studentized) residuals eᵢ* = êᵢ/(S√(1 − hᵢᵢ)) (6.9) with leverage hᵢᵢ = 1/n + (xᵢ − x̄)²/Σ(xᵢ − x̄)²; heteroscedasticity (CO data, polynomial fit); outliers (wind data); influential/high-leverage points and Cook's distance plots.
- QQ plots of residuals (t with n − 2 df vs normal quantiles); large-sample normality of β̂ without normal errors.
- Autocorrelated errors in a growth curve (6.10) with AR(1) errors eₜ = ρeₜ₋₁ + uₜ (6.11); Durbin–Watson statistic D (6.12) ≈ 2 − 2r₁ (6.13); remedies: generalized least squares or time-series methods.
- Multiplicative model yᵢ = βxᵢ^γ eᵢ (6.14) linearized by logs (6.15)–(6.17); t-test of H₀: γ = 1 and the reduced through-origin model (6.18)–(6.20) (dental plaque data).
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]] (residual autocorrelation and Durbin–Watson only)
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]] (heteroscedastic and AR(1) errors, GLS)
- Class: [[Map/class-plan#Class 8: Univariate time series|Class 8]] (AR(1) errors in regression only)

### §6.3 — Regressão linear múltipla (pp. 203–215)
**Subtopics:**
- Model (6.21), residuals (6.22), matrix form y = Xβ + e (6.23); least squares Q(β) = e′e (6.25) and β̂ = (X′X)⁻¹X′y (6.26); E(β̂) = β, Var(β̂) = σ²(X′X)⁻¹; S² = SSR/[n − (p + 1)]; normal and CLT-based inference.
- Treadmill example VO₂ ~ IMC + carga (6.24): coefficient interpretation "holding the other regressor fixed", residual plots vs each regressor and fitted values, Cook's distance cut-off 4/n, refit without influential points.
- Confidence interval for E(y | x₀) via x₀′(X′X)⁻¹x₀ vs prediction interval adding S² (R code).
- Collinearity (production data, r = 0.93): a "wrong-sign" coefficient that is not significant; R² always increases with regressors, adjusted R² penalizes; added-variable (partial regression) plot whose slope equals the multiple-regression coefficient (Frisch–Waugh logic).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §6.4 — Regressão para dados longitudinais (pp. 215–218)
**Subtopics:**
- Repeated weights of calves: pooled regression (6.27) vs linear mixed model with random intercept yᵢⱼ = α + β(xⱼ − 12) + aᵢ + eᵢⱼ (6.28); intra-unit correlation σₐ²/(σₐ² + σ²); same point estimates, smaller standard errors; profile and draftsman's plots.
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]] (random-intercept model only)
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]] (hierarchical / mixed linear model)

### §6.5 — Regressão logística (pp. 218–224)
**Subtopics:**
- Binary response: logit model log[P(Y = 1 | x)/P(Y = 0 | x)] = α + βx (6.29) and logistic form (6.30); α as baseline log-odds, β as log odds ratio per unit of x.
- Maximum likelihood: likelihood ∏ p(xᵢ)^{yᵢ}[1 − p(xᵢ)]^{1−yᵢ}, score equations with no closed form, Newton–Raphson / Fisher scoring; glm(family = binomial) output (deviance, AIC); CIs for odds and odds ratios by exponentiating Wald limits (delta method for their SEs).
- Predicted probabilities (6.31) and classification by a threshold (0.7 vs default 0.5) with a confusion table and proportion correctly classified.
- Odds ratios are invariant to prospective vs retrospective sampling; grouped categorical data (6.32) fitted by generalized least squares (coronary-lesion data, Tables 6.11–6.13); multinomial (polytomous) logistic regression mentioned but not covered.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]]

### §6.6 — Notas de capítulo (pp. 224–234)
**Subtopics:**
- Nine technical notes backing §6.2–6.5 (inference, prediction, R², influence, delta method, logistic goodness of fit, resistant and basis-function regression).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### Nota 1 — Inferência baseada em modelos de regressão linear simples (pp. 224–225)
**Subtopics:**
- β̂ = Σwᵢyᵢ is linear in y; unbiasedness, Var(α̂), Var(β̂), Cov(α̂, β̂); t statistics with n − 2 df under normality; Gauss–Markov theorem (BLUE without normality); asymptotic normality via the CLT; robust estimators for heavy tails.

#### Nota 2 — Estimação e previsão sob modelos de regressão linear simples (p. 226)
**Subtopics:**
- Var(ŷ₀) = σ²[1/n + (x₀ − x̄)²/Σ(xᵢ − x̄)²]; confidence interval for E(Y | X = x₀) vs prediction interval for a new Y₀ (adds σ²); CI width → 0 while PI width → 2 × 1.96σ as n grows.

#### Nota 3 — Coeficiente de determinação (pp. 226–228)
**Subtopics:**
- Decomposition SQTot = SQRes + SQReg; SQReg = β̂²Σ(xᵢ − x̄)²; R² = SQReg/SQTot; adjusted R² = 1 − [SQRes/(n − p − 1)]/[SQTot/(n − 1)].

#### Nota 4 — Distância de Cook (p. 228)
**Subtopics:**
- Dᵢ = (ŷ − ŷ₍₋ᵢ₎)′(ŷ − ŷ₍₋ᵢ₎)/[(p + 1)S²] and its closed form in terms of eᵢ² and hᵢᵢ without refitting.

#### Nota 5 — Influência local e alavancagem (pp. 229–230)
**Subtopics:**
- Effect of a perturbation Δyⱼ on β̂ (6.33) and α̂ (6.34); leverage hⱼⱼ as the effect of Δyⱼ on ŷⱼ, growing with |xⱼ − x̄|.

#### Nota 6 — Método Delta (p. 230)
**Subtopics:**
- Var[g(β̂)] ≈ [g′(β)]²σ²_β̂ and the multivariate gradient form; used for SEs of exp(α̂), exp(β̂).

#### Nota 7 — Análise do ajuste de modelos de regressão logística (pp. 230–232)
**Subtopics:**
- Covariate patterns; Pearson residuals and Pearson statistic Q_P ~ χ²_{M−(p+1)}; Hosmer–Lemeshow statistic C with g = 10 risk-decile groups ~ χ²_{g−2}; deviance residuals.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]]

#### Nota 8 — Regressão resistente (pp. 232–233)
**Subtopics:**
- Median-based resistant line from three groups (left, centre, right): b₀ = (y_D − y_E)/(x_D − x_E), a₀ averaged; Example 6.11 vs least squares on the wind data.

#### Nota 9 — Formulação geral do modelo de regressão (pp. 233–234)
**Subtopics:**
- yᵢ = f(xᵢ, β) + eᵢ (6.35) with basis expansions f(x, β) = Σβⱼφⱼ(x): polynomials, splines, Gaussian, sigmoid, Fourier, wavelets; links to regularization (Ch. 11) and neural networks (Ch. 14).

### §6.7 — Exercícios (pp. 234–242)
**Subtopics:**
- 22 exercises: least squares derivations and diagnostics (1–17), logistic regression and odds ratios (18–22). The text of §6.5 cites "Exercício 20/21" for results that are Exercises 19/20 in the list (preliminary-version numbering slip).

## Ch. 7 — Análise de Sobrevivência
**Pages:** pp. 243–260

### §7.1 — Introdução (pp. 243–247)
**Subtopics:**
- Time-to-event data with right censoring, response pair (T, δ); survival function S(t), hazard function and cumulative hazard; exponential, Weibull and lognormal hazard shapes.

### §7.2 — Estimação da função de sobrevivência (pp. 247–253)
**Subtopics:**
- Kaplan–Meier (product-limit) estimator from numbers at risk and failures; mean survival as the area under the curve; median survival time; survfit()/ggsurvplot() examples (Examples 7.1–7.3).

### §7.3 — Comparação de curvas de sobrevivência (pp. 253–254)
**Subtopics:**
- Log-rank test: hypergeometric expected failures and variances at each failure time, approximate χ²₁ statistic (survdiff()).

### §7.4 — Regressão para dados de sobrevivência (pp. 254–256)
**Subtopics:**
- Parametric accelerated failure time models log T = α + x′β + σe (exponential, Weibull, lognormal; survreg()); Cox proportional hazards model and checking proportionality (coxph(), cox.zph()).
**Linked materials:**
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]] (duration models)

### §7.5 — Notas de capítulo (p. 256)
**Subtopics:**
- Notes 1–2: types of censoring (right, left, interval); alternatives when hazards are not proportional.

### §7.6 — Exercícios (pp. 256–260)
**Subtopics:**
- 6 exercises on coding censored data, Kaplan–Meier curves, log-rank tests and Cox regression.

## Ch. 8 — Classificação por meio de técnicas clássicas
**Pages:** pp. 263–290

### §8.1 — Introdução (pp. 263–264)
**Subtopics:**
- Classifier g: ℝᵖ → {−1, 1}, risk L(g) = P{g(X) ≠ Y} and training error rate (8.1); validation (test) error rate; refit the chosen classifier on training + validation data; cross-validation when only one data set exists.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §8.2 — Classificação por regressão logística (pp. 264–272)
**Subtopics:**
- Logit model for TMJ disc displacement (8.2) with a centred predictor: ML estimates, CIs for odds and odds ratios, predicted probability θ̂.
- Cut-off choice: 2 × 2 decision table (Table 8.2), sensitivity n₁₁/(n₁₁ + n₂₁) and specificity n₂₂/(n₁₂ + n₂₂); ROC curve (pROC) and the cut-off closest to the top-left corner; accuracy, false-positive and false-negative rates.
- Two predictors (8.3): marginal significance and correlated predictors ("confounding").
- Machine-learning comparison of four logistic models by 5-fold CV repeated 5 times (VC5/5) and LOOCV accuracy with caret (trainControl/train); Cohen's kappa; set.seed for reproducible splits (Table 8.6).
- Why multinomial logistic regression is less used than LDA for K > 2 (instability with well-separated classes).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §8.3 — Análise discriminante linear (pp. 272–282)
**Subtopics:**
- Classification into K ≥ 2 classes under Bayesian (known densities) and frequentist (Fisher) views.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

#### §8.3.1 — Classificador de Bayes (pp. 272–280)
**Subtopics:**
- Posterior class probabilities pₖ(x) = πₖfₖ(x)/Σπₗfₗ(x) (8.4); misclassification probabilities (8.5) and expected misclassification cost (8.6); Bayes rule maximizes πₖfₖ(x) (8.8), likelihood-ratio form for K = 2 (8.9).
- Gaussian classes with common Σ: linear discriminant (8.11), δₖ(x) = µₖ′Σ⁻¹x − ½µₖ′Σ⁻¹µₖ + log πₖ (8.12), p = 1 case (8.13)–(8.14), Bayes boundaries (8.15); plug-in estimates π̂ₖ = nₖ/n, class means, pooled S (8.17); Fisher's linear discriminant function (8.18).
- Examples: two normals with misclassification probability 0.159 (Ex. 8.2); lda() on inibina (Ex. 8.3), 70/30 train–validation split on disc data (Ex. 8.4, 9.4% error), three facial types with posterior probabilities and "proportion of trace" (Ex. 8.5).
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]] (Bayes' theorem for class posteriors only)

#### §8.3.2 — Classificador linear de Fisher (pp. 280–282)
**Subtopics:**
- Choose W = d′x maximizing (d′δ)²/(d′Σd) (8.21) ⇒ d = Σ⁻¹(µ₁ − µ₂) (8.22)–(8.23); Mahalanobis distance; midpoint threshold (8.24)–(8.25); equivalent to Bayes LDA with equal priors (Ex. 8.6).

### §8.4 — Classificador do vizinho mais próximo (pp. 282–284)
**Subtopics:**
- Bayes classifier and Bayes error rate 1 − E[maxⱼ P(Y = j | X)]; KNN estimate (8.27); choice of K = 1…5 by LOOCV with caret (Ex. 8.7); confusionMatrix output: accuracy CI, no-information rate, kappa, McNemar p-value, sensitivity, specificity, PPV, NPV, balanced accuracy.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §8.5 — Algumas extensões (pp. 284–285)
**Subtopics:**
- Quadratic discriminant analysis with class-specific Σₖ (8.28): more parameters, lower bias and higher variance than LDA; regularized discriminant analysis (Friedman 1989) shrinking Σₖ toward the pooled matrix and the mean eigenvalue (8.29)–(8.30), λ and γ chosen by LOOCV; qda(), rda(); LDA vs QDA accuracy on the disc data (Ex. 8.8).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §8.6 — Notas de capítulo (pp. 285–288)
**Subtopics:**
- Three notes on model assessment: cross-validation, McNemar's test, comparison of classifiers.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### Nota 1 — Validação cruzada (pp. 285–287)
**Subtopics:**
- Prediction error E(y₀ − ŷ)²; in-sample residual MSE is optimistic; LOOCV (Efron & Tibshirani 1993) MSE₍₋ᵢ₎ (8.31) and its leverage shortcut Σ[(yᵢ − ŷᵢ)/(1 − hᵢ)]²/n (8.32); k-fold CV (k = 5 or 10) averaging fold MSEs (8.33); validation error rate for classifiers (8.34).

#### Nota 2 — Teste de McNemar (pp. 287–288)
**Subtopics:**
- Marginal homogeneity in a paired 2 × 2 table, M = (n₁₂ − n₂₁)²/(n₁₂ + n₂₁) ~ χ²₁ (8.35); exact binomial version and Edwards' continuity correction; Dietterich (1998): McNemar keeps type I error, unlike paired t tests on resampled splits.

#### Nota 3 — Comparação de classificadores (p. 288)
**Subtopics:**
- Comparing two classifiers on a validation set by a correct/wrong cross-table and McNemar's test; limitations (single training set, smaller evaluation size).

### §8.7 — Exercícios (pp. 289–290)
**Subtopics:**
- 20 exercises: LDA/QDA derivations (1, 2, 12, 17, 19), cross-validated comparisons of logistic, LDA, KNN (3–11, 13), Bayes classifiers for exponential and normal populations by simulation (14–16, 20), odds-ratio CI (18).

## Ch. 9 — Algoritmos de Suporte Vetorial
**Pages:** pp. 291–317

### §9.1 — Introdução (pp. 291–292)
**Subtopics:**
- Support vector machines (Vapnik and co-authors; Cortes & Vapnik 1995) for binary classification; comparison with GLMs, GAMs, neural networks and trees on interpretability, accuracy and computation.

### §9.2 — Fundamentação dos algoritmos de suporte vetorial (pp. 292–294)
**Subtopics:**
- Data space, response y ∈ {−1, 1}; three cases (linearly separable, not separable, non-linear boundary); kernels (Gaussian, polynomial, …) to enlarge the feature space; tuning by cross-validation.

### §9.3 — Classificador de margem máxima (pp. 294–297)
**Subtopics:**
- Separating hyperplane f(x) = α + β′x and classification by its sign; maximal-margin hyperplane and support vectors; optimization with Lagrange multipliers (Ex. 9.1).

### §9.4 — Classificador de margem flexível (pp. 297–302)
**Subtopics:**
- Soft-margin (support vector) classifier (9.4) with slack variables ξᵢ and budget C; C chosen by cross-validation with tune() (e1071); facial-type data (Ex. 9.2) with C and gamma by 10-fold CV.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §9.5 — Classificador de margem não linear (pp. 302–305)
**Subtopics:**
- Kernel trick: the classifier depends only on inner products with support vectors; polynomial (degree 3, Ex. 9.3) and radial kernels.

### §9.6 — Regressão por algoritmos de suporte vetorial (pp. 305–309)
**Subtopics:**
- ε-insensitive support vector regression (9.8) with slack variables; linear and radial kernels, ε and cost tuned by CV (distance-vs-age data, Ex. 9.4–9.5).

### §9.7 — Notas de capítulo (pp. 309–316)
**Subtopics:**
- Notes 1–6: separating hyperplane; maximal-margin classifier (Bishop 2006, Lagrangian dual); soft-margin classifier; non-linear-margin classifier; more than two classes; SVM for regression.

### §9.8 — Exercícios (pp. 316–317)
**Subtopics:**
- 8 exercises on margins, the role of C in the bias–variance trade-off, kernels and simulated non-linear boundaries.

## Ch. 10 — Árvores e Florestas
**Pages:** pp. 319–344

> Trees are outside the syllabus; §10.3.1 and Notas 3 and 5 of §10.5 are indexed at subsection depth because they hold the book's only treatment of the bootstrap.

### §10.1 — Introdução (pp. 319–320)
**Subtopics:**
- CART (Breiman et al.): partition of the predictor space into rectangles, mode/mean as prediction; recursive binary splitting as a top-down greedy algorithm.

### §10.2 — Classificação por árvores (pp. 320–327)
**Subtopics:**
- Node class proportions p̂ₘₖ (10.1), majority class and node error rate; ctree() on facial types (Ex. 10.1); rpart() on coronary-lesion data with built-in cross-validation (rel error, xerror, xstd), the one-standard-error pruning rule and the complexity parameter CP (Ex. 10.2); overfitting and pruning as a variance–bias trade.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §10.3 — Bagging, boosting e florestas (pp. 327–334)
**Subtopics:**
- Ensembles to reduce the high variance of single trees.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

#### §10.3.1 — Bagging (pp. 327–329)
**Subtopics:**
- Bootstrap aggregating: B bootstrap replicates of the training set, f̂_bag(x) = (1/B)Σf̂ᵇ(x) for regression and majority vote for classification; weak vs strong learners; B ≈ 200; subagging (Bühlmann & Yu 2002); bagging() with nbagg = 200 on the coronary data (Ex. 10.3).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]] (bootstrap resampling)
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §10.3.2 — Boosting (pp. 329–332)
**Subtopics:**
- Sequential reweighting of misclassified cases; weighted vote c_boost(x) (10.2); additive model of weak learners (10.3) and L2-boosting under squared loss (10.4)–(10.5); AdaBoost algorithm (stumps, α(b) = log[(1 − err)/err]); tuning B by CV, shrinkage λ and depth d; adabag (Ex. 10.4).

#### §10.3.3 — Florestas aleatórias (pp. 332–334)
**Subtopics:**
- Bagging plus a random subset of m ≈ √p predictors at each split; out-of-bag (OOB) error; decorrelated trees reduce variance; randomForest with 70/30 train–validation split (Ex. 10.5).

### §10.4 — Árvores para regressão (pp. 334–338)
**Subtopics:**
- Regression trees minimizing squared error, CP and 1 − R² for pruning (rsq.rpart), RMSE (anthracosis data, Ex. 10.6); trees for prediction may omit variables that matter for inference.

### §10.5 — Notas de capítulo (pp. 338–343)
**Subtopics:**
- Five notes: node-impurity criteria, pruning, bootstrap, regression trees, bagging theory.

#### Nota 1 — Critérios para avaliação de árvores de classificação (pp. 338–339)
**Subtopics:**
- Gini index Gₘ = Σp̂ₘₖ(1 − p̂ₘₖ), cross-entropy, and Breiman's relative variable importance from impurity decreases.

#### Nota 2 — Poda de árvores (p. 339)
**Subtopics:**
- Pre- vs post-pruning; cost-complexity criterion CP(α) = Σⱼ Σ_{xᵢ∈Rⱼ}(yᵢ − ŷ_{Rⱼ})² + α|A| (10.6) with α chosen by cross-validation.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

#### Nota 3 — Bootstrap (pp. 339–340)
**Subtopics:**
- Efron's (1979) nonparametric bootstrap: resample n points with replacement, B replicates of the estimator (10.7), bootstrap standard error as their sample standard deviation (example: the sample median); general θ̂ = t(X); B = 200 as a rule of thumb (Efron & Tibshirani 1993).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### Nota 4 — Árvores para regressão (p. 340)
**Subtopics:**
- Piecewise-constant model y = Σfⱼ I(x ∈ Rⱼ) (10.8); the region mean minimizes the sum of squares.

#### Nota 5 — Bagging: noções sobre a teoria (pp. 340–343)
**Subtopics:**
- Breiman (1996): aggregated predictor f_A(x) = E_P[f(x, T)]; Jensen's inequality gives MSEP ≥ MSEP(A) (10.9)–(10.10); bagging helps unstable procedures (trees, subset selection, neural networks) but not stable ones (KNN); the bootstrap aggregate uses the empirical distribution P_T; classification case can turn poor predictors worse.

### §10.6 — Exercícios (pp. 343–344)
**Subtopics:**
- 11 exercises on classification and regression trees, pruning, bagging, boosting (gbm) and random forests.

## Ch. 11 — Regularização e Modelos Aditivos Generalizados
**Pages:** pp. 345–364

### §11.1 — Introdução (p. 345)
**Subtopics:**
- Model selection for prediction of a continuous response: fit candidates on training data, compare MSE/RMSE/R² on validation data, usually by cross-validation.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §11.2 — Regularização (pp. 345–353)
**Subtopics:**
- Overfitting illustrated by polynomials of degree 0, 1, 3, 9 fitted to sin(2πx) + noise (Bishop 2006); penalized loss functions; sparse vs non-sparse solutions; constraint-region geometry (Figure 11.2).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (variable selection)
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]] (frequentist counterpart of sparsity priors)

#### §11.2.1 — Regularização L2 (Ridge) (pp. 346–348)
**Subtopics:**
- Ridge (Hoerl & Kennard 1970) for multicollinearity and overfitting: β̂_Ridge(λ) = argmin Σ(yₜ − β′xₜ)² + λΣβⱼ² (11.2) = (X′X + λI)⁻¹X′y (11.3); constrained form Σβⱼ² ≤ m (11.4); intercept not penalized.
- Properties: biased for non-zero coefficients, consistent only under conditions on λ, p, n; no variable selection; λ by cross-validation or information criteria.

#### §11.2.2 — Regularização L1 (Lasso) (pp. 348–349)
**Subtopics:**
- Lasso (11.5) with constraint Σ|βⱼ| ≤ m (11.6): shrinks redundant coefficients exactly to zero (sparsity, variable selection), biased for non-zero coefficients; soft-threshold solution β̂ⱼ = sign(Zⱼ)(|Zⱼ| − λ/2)₊ (11.7) in the orthonormal case.

#### §11.2.3 — Outras propostas (pp. 349–353)
**Subtopics:**
- Elastic net (11.8) mixing L2 and L1 penalties (α = λ₂/(λ₁ + λ₂)); adaptive lasso (11.9) with weights |β̂ⱼ|^−τ, consistent under mild conditions; glmnet also covers logistic, multinomial, Poisson and Cox models.
- Example 11.1 (anthracosis data): OLS vs cv.glmnet ridge (α = 0), lasso (α = 1, drops tmunic and distmin) and elastic net (α = 0.5); CV curves of MSE against log λ, lambda.min and CV RMSE.

### §11.3 — Modelos aditivos generalizados (GAM ) (pp. 353–361)
**Subtopics:**
- Additive model (11.10) with unspecified smooth fᵢ; GAM as an extension of GLMs, g(µᵢ) = β₀ + Σβⱼfⱼ(xᵢⱼ) (11.11); basis expansions (11.13); piecewise cubic polynomials (11.14), cubic splines with k knots and k + 4 df (11.15), truncated-power basis, natural splines; knots by cross-validation.
- Smoothing splines minimizing Σ[yᵢ − f(xᵢ)]² + λ∫f″(u)²du (11.16), λ by CV; local regression (span s = k/n, weighted least squares); backfitting.
- Example 11.2 (esforco data, mgcv gam()): linear fit vs GAM with s() terms, effective degrees of freedom, GCV, gam.check() diagnostics, analysis of deviance between nested models, prediction with standard errors.
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]] (flexible polynomial/spline fits)

### §11.4 — Notas de capítulo (pp. 361–363)
**Subtopics:**
- Three notes: ridge bias, choice of λ, generalized linear models.

#### Nota 1 — Viés da regularização Ridge. (p. 361)
**Subtopics:**
- β̂_Ridge(λ) = (I + λR⁻¹)⁻¹β̂_MQ with R = X′X (11.17), so E[β̂_Ridge(λ)] = (I + λR⁻¹)⁻¹β ≠ β (11.18).

#### Nota 2 — Escolha do parâmetro λ (p. 361)
**Subtopics:**
- SVD form of ridge with shrinkage factors dⱼ²/(dⱼ² + λ); effective degrees of freedom gl(λ) = tr[X(X′X + λI)⁻¹X′] = Σdⱼ²/(dⱼ² + λ); AIC, BIC and Hannan–Quinn criteria over a λ grid.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (model selection)

#### Nota 3 — Modelos Lineares Generalizados (pp. 362–363)
**Subtopics:**
- Exponential family f(y | θ, φ) (11.19): E(y) = b′(θ), Var(y) = a(φ)b″(θ) = a(φ)V(µ) with variance function (11.20); normal and binomial members; link g(µ) = x′β (identity → linear model, logit → logistic regression); log-likelihood (11.21) maximized by Newton–Raphson / Fisher scoring with score u(β) and information I(β).
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]] (logistic and Poisson regression as GLMs)
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]]

### §11.5 — Exercícios (pp. 363–364)
**Subtopics:**
- 4 exercises: regression on Telebrás vs IBV prices, ridge/lasso/elastic net on earlier examples, gamma-log GAM.

## Ch. 12 — Análise de Agrupamentos
**Pages:** pp. 367–382

### §12.1 — Introdução (pp. 367–369)
**Subtopics:**
- Cluster analysis (data segmentation) as unsupervised learning; Euclidean and non-Euclidean spaces; distances between units (height, weight, age data, Table 12.1).

### §12.2 — Estratégias de agrupamento (pp. 369–370)
**Subtopics:**
- Combinatorial, model-based (mixture densities) and bump-hunting algorithms (Hastie et al. 2009); hierarchical vs partition algorithms.

### §12.3 — Algoritmos hierárquicos (pp. 370–373)
**Subtopics:**
- Agglomerative clustering by centroid distance worked step by step; dendrograms (Ex. 12.1).

### §12.4 — Algoritmos de partição: K–médias (pp. 373–379)
**Subtopics:**
- K-means minimizing within-cluster sums of squares (Hartigan–Wong, Lloyd, MacQueen, Forgy algorithms); kmeans(); choice of K; simulated and traffic-data examples (Ex. 12.2–12.5).

### §12.5 — Notas de capítulo (pp. 379–382)
**Subtopics:**
- Notes 1–4: distances for non-Euclidean spaces (edit distance); single, complete and average linkage; cophenetic matrix and cophenetic correlation; other algorithms.

### §12.6 — Exercícios (p. 382)
**Subtopics:**
- 7 exercises on hierarchical and K-means clustering, linkage choices, edit distance and the cophenetic correlation.

## Ch. 13 — Redução de dimensionalidade
**Pages:** pp. 383–414

### §13.1 — Introdução (p. 383)
**Subtopics:**
- Principal components, factor analysis and independent components reduce dimension while preserving the covariance structure; factors as regressors in later analyses.

### §13.2 — Análise de Componentes Principais (pp. 383–390)
**Subtopics:**
- Orthogonal rotation of axes that sequentially maximizes explained variance (eigen-decomposition of the covariance or correlation matrix); component scores, elbow (scree) plot, biplot (Ex. 13.1).

### §13.3 — Análise fatorial (pp. 390–403)
**Subtopics:**
- Orthogonal factor model with loadings Λ and specific variances ψ; principal-factor and maximum-likelihood estimation; rotations (Varimax, Quartimax, Equimax); number of factors by elbow plot, parallel analysis and optimal coordinates; factor scores; factanal() on suicide data.

### §13.4 — Análise de componentes independentes (pp. 403–411)
**Subtopics:**
- ICA for non-Gaussian sources (Hyvärinen & Oja 2000): centring, whitening and dimension reduction; non-Gaussianity via excess kurtosis and negentropy; the FastICA fixed-point algorithm.

### §13.5 — Notas de capítulo (pp. 411–413)
**Subtopics:**
- Notes 1–4: deriving principal components with a Lagrangian; decomposition of symmetric matrices; the Wishart distribution and the system (13.7); determining the number of factors.

### §13.6 — Exercícios (pp. 413–414)
**Subtopics:**
- 9 exercises on principal components, factor analysis and ICA derivations and applications.

## Ch. 14 — Redes neurais
**Pages:** pp. 417–434

### §14.1 — Introdução (pp. 417–418)
**Subtopics:**
- Neurons and activation functions; single-layer, multilayer feed-forward and recurrent networks.

### §14.2 — Perceptron (pp. 418–421)
**Subtopics:**
- Rosenblatt's perceptron as a linear classifier updated on misclassified points; simulated data and the disc-displacement data (Ex. 14.1–14.2).

### §14.3 — Redes com camadas escondidas (pp. 421–423)
**Subtopics:**
- One-hidden-layer network: inputs x, hidden units y, outputs z, weights α and β; one output for regression, K outputs for classification.

### §14.4 — O algoritmo retropropagação (backpropagation) (pp. 423–430)
**Subtopics:**
- Fitting by minimizing SSE (regression) or cross-entropy (classification) with gradient descent / stochastic gradient descent via backpropagation; neuralnet examples with one and two hidden layers (Ex. 14.3–14.4); one-against-all and one-against-one strategies for K > 2 classes.

### §14.5 — Aprendizado profundo (Deep learning ) (pp. 430–431)
**Subtopics:**
- Deep learning as many-layer networks learning a hierarchy of representations; multilayer perceptron; historical waves (Goodfellow et al. 2016); MNIST.

### §14.6 — Notas de capítulo (pp. 431–433)
**Subtopics:**
- Notes 1–3: the Mark I perceptron; perceptron convergence; the backpropagation algorithm.

### §14.7 — Exercícios (pp. 433–434)
**Subtopics:**
- 3 exercises: network equations from fitted weights, and loss functions for K binary vs K mutually exclusive classes (softmax, cross-entropy).

## App. A — Otimização numérica
**Pages:** pp. 437–451

### §A.1 — Introdução (pp. 437–440)
**Subtopics:**
- Gradient vs non-gradient optimization; iterative schemes with a convergence tolerance; main use is maximizing a likelihood (MLE) or a posterior density (posterior mode); gradient, Hessian and Fisher information.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §A.2 — O método de Newton-Raphson (pp. 440–442)
**Subtopics:**
- Newton–Raphson from a quadratic approximation: θ⁽ⁱ⁺¹⁾ = θ⁽ⁱ⁾ − H⁻¹g; worked univariate example (Ex. A.1–A.2).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §A.3 — O método scoring (p. 442)
**Subtopics:**
- Fisher scoring replaces the Hessian by minus the expected information, θ⁽ⁱ⁺¹⁾ = θ⁽ⁱ⁾ + I(θ⁽ⁱ⁾)⁻¹g (A.11); slower but sometimes easier; Cauchy location MLE (Ex. A.3).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]] (GLM / probit fitting)

### §A.4 — O método de Gauss-Newton (pp. 442–444)
**Subtopics:**
- Non-linear least squares solved as a sequence of linearized regressions (Ex. A.4).

### §A.5 — Métodos Quase-Newton (pp. 444–445)
**Subtopics:**
- Hessian approximations (BFGS, variable-metric/secant methods): cheaper steps, more iterations.

### §A.6 — Aspectos computacionais (pp. 445–449)
**Subtopics:**
- optim() methods (Nelder–Mead, BFGS, CG, L-BFGS-B, SANN), packages optimization and maxLik (maxNR()); examples including MLE of a normal mean and variance (Ex. A.5–A.8).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §A.7 — Notas de capítulo (pp. 449–450)
**Subtopics:**
- Notes 1–2: non-gradient algorithms (genetic algorithms, Nelder–Mead simplex, simulated annealing); constrained optimization.

### §A.8 — Exercícios (pp. 450–451)
**Subtopics:**
- 12 exercises: steepest descent and quadratic hill climbing, Newton–Raphson and scoring for Cauchy and multinomial MLEs, non-linear regression, maxLik/optimization packages.

## App. B — Noções de simulação
**Pages:** pp. 453–478

### §B.1 — Introdução (pp. 453–456)
**Subtopics:**
- Monte Carlo origins (Metropolis & Ulam 1949); area of a figure by uniform points; random vs pseudo-random numbers (middle-square, congruential generators, runif()); static (Monte Carlo, acceptance–rejection, weighted resampling), imputation (EM, data augmentation) and dynamic (Gibbs, Metropolis–Hastings = MCMC) simulation.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §B.2 — Método Monte Carlo (pp. 456–457)
**Subtopics:**
- E_F[h(X)] ≈ (1/n)Σh(Xᵢ) (B.1), strong-law convergence and O(n^{−1/2}) standard error (B.2); π/4 by simulating √(1 − X²) (Ex. B.4); sampling marginals by composition (mixtures) (B.4).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]] (Monte Carlo)

### §B.3 — Simulação de variáveis discretas (pp. 457–459)
**Subtopics:**
- Inverse-cdf method for discrete distributions (B.5)–(B.6); Bernoulli, binomial and Poisson generators via the recursion pⱼ₊₁ = λpⱼ/(j + 1) (B.7)–(B.8); R r-functions and Excel tools.

### §B.4 — Simulação de variáveis contínuas (pp. 459–464)
**Subtopics:**
- Probability integral transform (Theorem B.1, x = F⁻¹(u)); exponential −β log u; normal via Φ⁻¹ and the Box–Muller transform (B.13); chi-squared as sums of squared normals; t, F, gamma, beta in R.

### §B.5 — Simulação de vetores aleatórios (pp. 464–467)
**Subtopics:**
- Joint = marginal × conditional; bivariate uniform (Monte Carlo area) and independent bivariate normal examples.

### §B.6 — Métodos de reamostragem (pp. 467–472)
**Subtopics:**
- Sampling from a target π via an easy density g plus a correction step.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Rules: [[rules/07_bayes|Bayesian inference]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

#### §B.6.1 — Amostragem por aceitação-rejeição (pp. 468–470)
**Subtopics:**
- Envelope π(x) ≤ Ag(x); accept x* if u ≤ π(x*)/[Ag(x*)]; acceptance probability 1/A (B.14), geometric number of trials with mean A; only the kernel of π is needed; Beta(2,2) from uniforms (Ex. B.15).

#### §B.6.2 — Reamostragem ponderada (pp. 470–472)
**Subtopics:**
- Sampling–importance resampling with weights wᵢ ∝ π(xᵢ)/g(xᵢ); importance sampling estimators (B.15)–(B.16) and the self-normalized estimator (B.17) with Geweke's (1989) consistency conditions and standard error; posterior mean of θ in the genetic-linkage model under a flat prior using a Beta(35, 39) proposal, θ̂ = 0.6180 (Ex. B.16).

### §B.7 — Notas de capítulo (pp. 472–476)
**Subtopics:**
- Five notes: MCMC overview, Gibbs sampler, Metropolis–Hastings, Box–Muller, gamma simulation.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

#### Nota 1 — Métodos MCMC (p. 472)
**Subtopics:**
- Markov chains whose stationary distribution is the target (Metropolis et al. 1953; Hastings 1970; Geman & Geman 1984; Gelfand & Smith 1990); references including Gamerman & Lopes (2006).

#### Nota 2 — O Amostrador de Gibbs (pp. 472–473)
**Subtopics:**
- Two-variable Gibbs sequence (B.19) and Rao–Blackwellized marginal density estimates (B.20)–(B.21) (Casella & George 1992); general case with full conditionals π(θᵢ | θ₋ᵢ) (B.22) and the transition kernel of the homogeneous chain (B.23)–(B.24).

#### Nota 3 — O algoritmo de Metropolis-Hastings (pp. 474–475)
**Subtopics:**
- Reversibility π(θ)p(θ, φ) = π(φ)p(φ, θ); kernel q·α (B.25) with acceptance probability α = min{1, π(φ)q(φ, θ)/[π(θ)q(θ, φ)]} (B.26); acceptance rates of 20–50%; symmetric (Metropolis), random-walk and independence chains; Metropolis-within-Gibbs; irreducibility and aperiodicity (Chib & Greenberg 1995).

#### Nota 4 — Transformação de Box-Müller. (pp. 475–476)
**Subtopics:**
- Polar-coordinate derivation: R² ~ Exp(2) and θ ~ U(0, 2π) independent give two independent N(0, 1) draws.

#### Nota 5 — Simulação de uma distribuição gama. (p. 476)
**Subtopics:**
- Gamma(r, β) with integer r as a sum of r independent exponentials.

### §B.8 — Exercícios (pp. 476–478)
**Subtopics:**
- 20 exercises: pseudo-random generators (1–6), inverse-cdf simulation of discrete and continuous laws (7–15), acceptance–rejection (16, 18–20), Monte Carlo probability for a correlated bivariate normal (17).

## App. C — Algoritmos para dados aumentados
**Pages:** pp. 479–489

### §C.1 — Introdução (p. 479)
**Subtopics:**
- Latent (unobserved) data introduced to ease likelihood or posterior computation; complete vs incomplete data (cumulative fish-trap counts, Ex. C.1); multiple imputation (Rubin 1977, 1987; Little & Rubin 1987).
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §C.2 — O algoritmo EM (pp. 480–485)
**Subtopics:**
- Observed-data likelihood as an integral of the complete-data likelihood (C.1); genetic-linkage multinomial (C.2)–(C.3): E step with binomial conditional expectations, M step (C.4)–(C.5), iterations from θ⁽⁰⁾ = 0.5 to θ̂ = 0.62682 (Table C.1).
- General E step Q(θ, θ⁽ⁱ⁾) = E[ℓ(θ | x) | y, θ⁽ⁱ⁾] (C.6), M step, convergence check; posterior-mode version (C.7); Example C.3.
- Monotonicity (Proposition C.1, Dempster, Laird & Rubin 1977) via the Q − H + K decomposition (C.8)–(C.9); generalized EM; Wu (1983) convergence to a stationary point (Proposition C.2), multiple starting values, linear convergence rate and Louis's acceleration.
- Censored regression of log failure times of motors on temperature (Schmee & Hahn 1979; Tanner 1996): truncated-normal E step with the inverse Mills ratio H(x) = φ(x)/[1 − Φ(x)] (C.10)–(C.14); estimates after 11 iterations (Ex. C.4).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (likelihood maximization)
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]] (censored / Tobit-type regression)

### §C.3 — O algoritmo EM Monte Carlo (pp. 485–486)
**Subtopics:**
- MCEM (Wei & Tanner 1990): Monte Carlo average over simulated latent data in the E step, growing m and monitoring θ⁽ⁱ⁾ against i; genetic-linkage iterations (Table C.3, Ex. C.5).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §C.4 — Cálculo de erros padrões (pp. 486–487)
**Subtopics:**
- Standard errors after EM: direct/numerical Hessian; Louis's method and the missing-information principle (C.15) — observed = complete − missing information (Proposition C.3); genetic-linkage case 435.3 − 57.8 = 377.5, s.e.(θ̂) ≈ 0.05; simulation approximations.

### §C.5 — O Algoritmo de dados aumentados (pp. 487–489)
**Subtopics:**
- Tanner–Wong data augmentation: posterior identity (C.16) and predictive identity (C.17) iterated by simulation (S) and integration (I) steps, giving a mixture estimate of p(θ | y); relation to the Gibbs sampler and the chained-data algorithm; Beta–binomial mixture for the genetic-linkage posterior (Ex. C.6).
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

### §C.6 — Exercícios (p. 489)
**Subtopics:**
- 8 exercises: EM for exponential families, censored regression updates, MCEM, EM standard errors by simulation, chained-data (Gibbs) algorithm with burn-in, SI algorithm, EM for censored exponential data.
