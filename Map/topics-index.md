---
tags: [map, cross-reference]
date: 2026-10-19
---
# Topics Index

Printed page numbers. Lectures follow the lecturer's site ([[Aula/COURSE]], schedule in [[Map/class-plan]]). No lists, quizzes, tutorials or exams exist yet. Those rungs read "none yet" and are filled on the next `/study-map` run. Greenberg is the 1st edition (the syllabus names the 2e): [[Livros/BOOKS]]. Exercise IDs are detailed in [[Map/exercises-index]].

Book links:
- MHE = [[Livros/Joshua D. Angrist, Jorn-Steffen Pischke-Mostly Harmless Econometrics_ An Empiricist's Companion (2008)|MHE]]
- W = [[Livros/Wooldridge J.M-Introductory econometrics. A modern approach-Cengage Learning (2016)|Wooldridge 6e]]
- T = [[Livros/Ruey S. Tsay - Analysis of Financial Time Series, Third Edition (Wiley Series in Probability and Statistics)-John Wiley & Sons (2010)|Tsay AFTS 3e]]
- I = [[Livros/James, Witten, Hastie, Tibshirani, Taylor - An Introduction to Statistical Learning with Applications in Python (2023)|ISLP]] (ISLR 2e has the same chapters with R labs; the ISLR 1e index is kept in [[Map/books-index]] for reference)
- AME = [[Livros/Izbicki, Mendonça - Aprendizado de Máquina_ uma abordagem estatística (2020)|Izbicki & Mendonça]] (no end-of-chapter exercises)
- MS = [[Livros/Morettin, Singer - Estatística e Ciência de Dados (versão preliminar, abril 2021)|Morettin & Singer]] (preliminary version; no time-series chapter)
- B = [[Livros/Bolfarine, Sandoval - Introdução à Inferência Estatística (2010)|Bolfarine & Sandoval]]
- G = [[Livros/Edward Greenberg - Introduction to Bayesian Econometrics (2007, Cambridge University Press) - libgen.li|Greenberg 1e]]

---

## Topic: Potential outcomes & selection bias
#topic/potential-outcomes

**Complexity:** foundational
**Lecture:** Classes 5+6 (potential outcomes, SUTVA, ATE/CATE/QTE, DAGs, RDD). Already built: `Aula/class-05-06/potential-outcomes.ipynb` and three companions. See [[Map/class-plan]].
**Cross-topic links:** [[#Topic: Endogeneity & IV]], [[#Topic: Panel data & DiD]]
**Prerequisites:** OLS mechanics (W Ch. 2–3, background)

**Difficulty progression:**
1. 📖 Isolated concept (Easy): MHE Ch. 2, §2.1–2.3 (pp. 10–18): the selection problem, random assignment, regression analysis of experiments.
2. 📖 Regression and causality (Easy→Medium): MHE §3.2 (pp. 38–50): conditional independence assumption (CIA), OVB formula, bad controls. W §3.3 (omitted variable bias), W Ch. 16 §16.1–16.2 (pp. 500–504): simultaneity / reverse causality.
3. 📝 Rules (Medium): [[rules/02_causalidade_potential_outcomes|Formulas and patterns]]
4. ✏️ Direct exercises (Medium): W 9.C6, 9.C7 (proxy variables); MHE Tables 2.2.1–2.2.2 (STAR, foundational).
5. ✏️ Integrative exercises (Hard): MHE Tables 3.3.1–3.3.3 (matching vs. regression, NSW controls); W 9.6, 17.4 (sample selection / Heckit); G 11.1–11.4 (treatment model, foundational) → 11.5, 11.8 (advanced).
6. 🧪 Quiz: none yet
7. 📊 Exam: none yet
8. 👨‍🏫 Tutorial: none yet

**Cross-topic synthesis (Hard):**
- With [[#Topic: Endogeneity & IV]]: MHE §4.4 (pp. 111–129). IV with heterogeneous potential outcomes (LATE) restates selection bias in the potential-outcomes framework.
- With [[#Topic: Panel data & DiD]]: MHE §5.1–5.2 (pp. 165–181). Fixed effects and DiD remove time-invariant selection.
- With [[#Topic: Bayesian inference]]: G §11.1 (pp. 168–173), Bayesian treatment models. G §11.3 (pp. 175–179), incidental truncation / selection.

---

## Topic: Endogeneity & IV
#topic/endogeneity-iv

**Complexity:** intermediate
**Lecture:** Classes 5+6 (OVB, errors-in-variables, IV with Card's data). See [[Map/class-plan]].
**Cross-topic links:** [[#Topic: Potential outcomes & selection bias]], [[#Topic: Panel data & DiD]], [[#Topic: Monte Carlo & MCMC]]
**Prerequisites:** [[#Topic: Potential outcomes & selection bias]]

**Difficulty progression:**
1. 📖 Isolated concept (Easy): W §15.1–15.3 (pp. 462–479): omitted variables, IV estimation, 2SLS. W §9.4 (pp. 287–293): measurement error and attenuation bias.
2. 📖 Causal IV (Medium): MHE §4.1–4.2 (pp. 84–108): IV and causality, Wald estimator, asymptotic 2SLS inference.
3. 📝 Rules (Medium): [[rules/01_endogeneidade_iv|Formulas and patterns]]
4. ✏️ Direct exercises (Medium): W 15.1, 15.2, 15.4, 15.5, 15.C1, 15.C2, 15.C9; W 9.1–9.4 (measurement error / specification); MHE Tables 4.1.1–4.1.3 (QOB and draft-lottery Wald estimates).
5. ✏️ Integrative exercises (Hard): W 15.3, 15.6, 15.11 (advanced); W §15.5 tests (Hausman, overidentification); MHE Tables 4.4.1–4.4.3 (LATE, compliers), Table 4.6.2 (2SLS vs. LIML, first-stage F).
6. 🧪 Quiz: none yet
7. 📊 Exam: none yet
8. 👨‍🏫 Tutorial: none yet

**Cross-topic synthesis (Hard):**
- With [[#Topic: Potential outcomes & selection bias]]: MHE §4.4–4.5 (pp. 111–140). LATE theorem, monotonicity, generalizing LATE.
- With [[#Topic: Monte Carlo & MCMC]]: MHE Figures 4.6.1–4.6.3. Monte Carlo distributions of OLS, 2SLS and LIML with weak instruments (§4.6, pp. 141–159).
- With [[#Topic: Panel data & DiD]]: W §15.8 (pp. 487–488). 2SLS with panel data.
- With [[#Topic: Bayesian inference]]: G §11.2 (pp. 173–175), Bayesian endogenous covariates. G 11.6, 11.7 (advanced).

---

## Topic: Panel data & DiD
#topic/panel-did

**Complexity:** intermediate
**Lecture:** Classes 5+6 (DiD, Card–Krueger) and Class 7 (hierarchical models). FE/RE and the Hausman test are not on the site schedule. See [[Map/class-plan]].
**Cross-topic links:** [[#Topic: Potential outcomes & selection bias]], [[#Topic: Endogeneity & IV]], [[#Topic: Bayesian inference]] (hierarchical models)
**Prerequisites:** [[#Topic: Potential outcomes & selection bias]]

**Difficulty progression:**
1. 📖 Isolated concept (Easy): W §13.1–13.3 (pp. 403–417): pooled cross sections, policy analysis, two-period panels / first differences.
2. 📖 FE / RE (Medium): W §14.1–14.3 (pp. 435–448): fixed effects, random effects, correlated random effects. MHE §5.1 (pp. 165–168).
3. 📖 DiD (Medium): MHE §5.2 (pp. 169–181): DiD, parallel trends, regression DD. W §13.2, §13.4.
4. 📝 Rules (Medium): [[rules/03_painel_did|Formulas and patterns]]
5. ✏️ Direct exercises (Medium): W 13.1, 13.3, 13.C1, 13.C2, 13.C5, 14.C1, 14.C2; MHE Table 5.2.1 (Card–Krueger NJ/PA).
6. ✏️ Integrative exercises (Hard): W 14.1–14.3 (advanced); MHE Figure 5.2.4 (leads and lags), Table 5.2.3 (Besley–Burgess).
7. 🧪 Quiz: none yet
8. 📊 Exam: none yet
9. 👨‍🏫 Tutorial: none yet

**Cross-topic synthesis (Hard):**
- With [[#Topic: Bayesian inference]]: hierarchical (multilevel) models. G §4.5–4.6 (pp. 50–53) cover exchangeability and hierarchical priors. G §9.3 (pp. 144–149) covers Bayesian FE/RE panels with the Chib–Carlin Gibbs sampler. G §10.4 (pp. 165–166) covers dynamic panels. RE (W §14.2) is the frequentist counterpart. Exercises: G 4.6 → 4.7 → 9.3 → 9.2 → 10.3 → 9.4.
- With [[#Topic: Endogeneity & IV]]: MHE §5.3 (pp. 182–183). FE vs. lagged dependent variables.

---

## Topic: ARIMA & unit roots
#topic/arima-unit-roots

**Complexity:** intermediate
**Lecture:** Class 1 (AR(1), unit root, AR(p) as regression) and Class 8 (ARMA, unit roots, long memory, seasonal models). Cointegration is not on the site schedule. See [[Map/class-plan]].
**Cross-topic links:** [[#Topic: State space & volatility]]
**Prerequisites:** time-series regression basics (W Ch. 10–11)

**Difficulty progression:**
1. 📖 Isolated concept (Easy): T §2.1–2.3 (pp. 30–37): stationarity, ACF, white noise. W §11.1 (pp. 345–348): weak dependence.
2. 📖 ARMA (Medium): T §2.4–2.6 (pp. 37–71): AR, MA and ARMA identification, estimation, forecasting. T §2.8 (pp. 81–90): seasonal models.
3. 📖 Unit roots & long memory (Medium→Hard): T §2.7 (pp. 71–81): unit-root nonstationarity, ADF. W §18.2–18.3 (pp. 574–580): unit-root tests, spurious regression. T §2.11 (pp. 101–103): long memory / ARFIMA.
4. 📖 Cointegration (Hard): W §18.4 (pp. 580–586): cointegration and ECM. T §8.5–8.6 (pp. 428–442): cointegrated VAR, Johansen.
5. 📝 Rules (Medium): [[rules/04_arima_raiz_unitaria|Formulas and patterns]]
6. ✏️ Direct exercises (Medium): T 2.1, 2.2, 2.5, 2.10 (foundational), 2.3, 2.4, 2.6–2.9 (exam); W 10.C1–10.C4, 11.1, 11.C1.
7. ✏️ Integrative exercises (Hard): T 2.14, 8.4, 8.7; W 11.3, 11.7, 11.8; W Ch. 18 exercises (see [[Map/exercises-index]]).
8. 🧪 Quiz / 📊 Exam / 👨‍🏫 Tutorial: none yet

**Cross-topic synthesis (Hard):**
- With [[#Topic: State space & volatility]]: T §2.9 (pp. 90–97), regression with time-series errors. T §3.2 (pp. 111–113), mean equation + volatility equation.

---

## Topic: State space & volatility
#topic/state-space-volatility

**Complexity:** advanced
**Lecture:** Class 1 (VAR(1)), Class 8 (ARCH/GARCH, SV) and Class 9 (VAR/SVAR, BVAR, FAVAR, TVP-VAR, factor SV, DCC). A stand-alone Kalman-filter class is not on the site schedule. See [[Map/class-plan]].
**Cross-topic links:** [[#Topic: ARIMA & unit roots]], [[#Topic: Monte Carlo & MCMC]], [[#Topic: Bayesian inference]]
**Prerequisites:** [[#Topic: ARIMA & unit roots]]

**Difficulty progression:**
1. 📖 Isolated concept (Easy→Medium): T §3.4–3.5 (pp. 115–140): ARCH, GARCH. W §12.6 (pp. 391–396): ARCH in time-series regressions.
2. 📖 Stochastic volatility (Medium): T §3.12 (pp. 153–154).
3. 📖 Multivariate (Hard): T §8.1–8.2 (pp. 390–417), VAR. T Ch. 9 (pp. 468–489), factor models / PCA. T §10.1–10.4 (pp. 506–537), multivariate GARCH.
4. 📖 State space (Hard): T §11.1–11.4 (pp. 558–600): local trend, linear state-space form, Kalman filter and smoothing (time-varying parameters).
5. 📝 Rules (Medium): [[rules/05_espaco_estados_volatilidade|Formulas and patterns]]
6. ✏️ Direct exercises (Medium): T 3.1–3.9, 3.11–3.13; T 8.1, 9.1, 10.1, 11.1; W 12.6.
7. ✏️ Integrative exercises (Hard): T 3.10, 3.14, 3.15, 8.3, 9.7, 10.6–10.10; T 11.2–11.5.
8. 🧪 Quiz / 📊 Exam / 👨‍🏫 Tutorial: none yet

**Cross-topic synthesis (Hard):**
- With [[#Topic: Monte Carlo & MCMC]]: T §12.7–12.8 (pp. 636–660). Bayesian / MCMC estimation of stochastic volatility.
- With [[#Topic: Bayesian inference]]: T §11.4 (pp. 591–600). The Kalman filter as sequential Bayesian updating.

---

## Topic: Classification & validation
#topic/classification-validation

**Complexity:** foundational → intermediate
**Lecture:** Class 1 (bias–variance), Class 2 (CV, logistic regression, discriminant analysis) and Class 7 (probit, Tobit, ordered/multinomial probit). See [[Map/class-plan]].
**Cross-topic links:** [[#Topic: Monte Carlo & MCMC]] (bootstrap), [[#Topic: Bayesian inference]] (Bayes classifier)
**Prerequisites:** linear regression (I Ch. 3, background)

**Difficulty progression:**
1. 📖 Isolated concept (Easy): I §2.2 (pp. 27–40): quality of fit, the bias–variance trade-off (§2.2.2), the classification setting and the Bayes classifier (§2.2.3). AME Ch. 1 (pp. 3–24): risk, data splitting and bias–variance.
2. 📖 Logistic regression (Medium): I §4.3 (pp. 138–146); I §4.6 (pp. 167–173), GLMs and Poisson regression. W §17.1 (pp. 525–536): logit and probit. AME §8.1 (pp. 141–151). MS §6.5 (pp. 218–224), §8.2 (pp. 264–272).
3. 📖 Metrics (Medium): I §4.4.2 (pp. 150–156): confusion matrix, sensitivity/specificity, ROC/AUC. AME Ch. 7 (pp. 133–139) and §9.1 (pp. 169–172). MS §8.2–8.3 (pp. 264–282).
4. 📖 Validation (Medium): I §5.1 (pp. 202–212): validation set, LOOCV, k-fold, bias–variance for k-fold, CV for classification. AME §1.5.1 (pp. 14–21). MS §8.6, note on CV (pp. 285–287).
5. 📝 Rules (Medium): [[rules/06_classificacao_validacao|Formulas and patterns]]
6. ✏️ Direct exercises (Medium): I 2.1, 2.3, 4.1, 4.9, 5.3 (conceptual); W 17.2, 17.C1, 17.C4, 17.C5.
7. ✏️ Integrative exercises (Hard): I 4.13, 4.14, 4.16, 5.5, 5.7, 5.8, 7.9 (applied, Python labs); MS 6.19, 6.20 (foundational), 8.4, 8.6, 8.9, 8.11; I 4.2, 4.3, 4.10, 4.11, MS 8.1, 8.12 (advanced).
8. 🧪 Quiz / 📊 Exam / 👨‍🏫 Tutorial: none yet

**Cross-topic synthesis (Hard):**
- With [[#Topic: Bayesian inference]]: I §4.4 introduction (pp. 146–147), Bayes' theorem for classification. I 4.7. G §8.2 (pp. 117–129), Bayesian binary-response models. G 8.8 (logit posterior).
- With [[#Topic: Monte Carlo & MCMC]]: I §5.2 (pp. 212–215), the bootstrap. MS App. B (pp. 453–478): Monte Carlo, inverse-CDF, accept–reject, resampling.

---

## Topic: Bayesian inference
#topic/bayes

**Complexity:** intermediate
**Lecture:** Classes 3+4; first example in Class 1 (Poisson with exponential prior). Bayesian versions recur in Classes 7–9. See [[Map/class-plan]].
**Cross-topic links:** [[#Topic: Monte Carlo & MCMC]], [[#Topic: State space & volatility]], [[#Topic: Panel data & DiD]]
**Prerequisites:** probability (likelihood, conditional densities)

**Difficulty progression:**
1. 📖 Isolated concept (Easy): G §2.2 (pp. 12–18): prior, likelihood, posterior. B §4.1–4.4 (pp. 57–70): loss, risk, the Bayes principle, Bayes estimators under quadratic loss.
2. 📖 Posterior inference (Medium): G §3.1–3.2 (pp. 20–38): sequential updating, large-sample behaviour, identification, loss functions, predictive distribution, Bayes factors.
3. 📖 Priors (Medium): G §4.3 (pp. 44–47), conjugate priors (normal-inverse-gamma). G §4.9 (pp. 54–56), conditionally conjugate priors. T §12.3 (pp. 617–622).
4. 📝 Rules (Medium): [[rules/07_bayes|Formulas and patterns]]
5. ✏️ Direct exercises (Medium): G 2.2, 3.3, 3.4; T 12.1; I 4.7 (Bayes' theorem); B 4.3, 4.5, 4.9, 4.10, 5.11.
6. ✏️ Integrative exercises (Hard): G 3.2, 3.8, 4.5; G 8.1, 8.3, 8.4 (Bayesian regression, model comparison); G 10.2 (AR(p) predictive).
7. 🧪 Quiz / 📊 Exam / 👨‍🏫 Tutorial: none yet

**Cross-topic synthesis (Hard):**
- With [[#Topic: Monte Carlo & MCMC]]: T §12.2–12.3 (pp. 615–622). Gibbs sampling for posterior simulation.
- With [[#Topic: State space & volatility]]: sequential Bayes ↔ Kalman filter (T §11.4). G §10.2–10.3 (pp. 158–165): regime switching and time-varying parameters, estimated by Gibbs.
- With [[#Topic: Classification & validation]]: G §8.2 (pp. 117–129). Bayesian probit/logit (Albert–Chib) and Tobit. G 8.7–8.9, 9.5.

---

## Topic: Monte Carlo & MCMC
#topic/monte-carlo-mcmc

**Complexity:** advanced
**Lecture:** Classes 3+4 (MC, MCMC, HMC/Stan); bootstrap in Classes 1–2. SMC is not on the site schedule. See [[Map/class-plan]].
**Cross-topic links:** [[#Topic: Bayesian inference]], [[#Topic: State space & volatility]], [[#Topic: Endogeneity & IV]] (simulation studies)
**Prerequisites:** [[#Topic: Bayesian inference]]

**Difficulty progression:**
1. 📖 Isolated concept (Easy): G Ch. 5 (pp. 63–75), classical simulation (inverse-CDF, accept–reject, importance sampling). I §5.2 (pp. 212–215), the bootstrap. MS App. B (pp. 453–478): Monte Carlo, inverse-CDF, accept–reject, resampling.
2. 📖 Markov chains (Medium): G §6.1 (pp. 76–81), finite state spaces. T §12.1 (pp. 614–615).
3. 📖 MCMC (Medium): G §7.1–7.2 (pp. 91–102): Gibbs, Metropolis–Hastings, Chib's marginal likelihood. G §7.3 (pp. 102–103): numerical standard errors and convergence. T §12.2, §12.4 (pp. 615–617, 622–624).
4. 📖 Applications (Hard): G §8.1–8.2 (pp. 111–129), samplers for regression and limited dependent variables. T §12.5–12.9 (pp. 624–666), SV models and Markov switching.
5. 📖 Sequential Monte Carlo (Hard): **not covered by any book on disk.** Greenberg 1e has no particle filter or SMC; it estimates state-space and regime models by Gibbs (G §10.2–10.3). The 2nd edition or lecture slides are needed.
6. 📝 Rules (Medium): [[rules/08_monte_carlo_mcmc|Formulas and patterns]]
7. ✏️ Direct exercises (Medium): G 5.4, 6.2, 7.1; T 12.2, 12.3, 12.8; I 5.2, 5.4, 5.6, 5.9; MS B.16, B.19, C.5.
8. ✏️ Integrative exercises (Hard): G 7.5, 7.3, 7.8; G 8.5, 8.6, 9.1; T 12.4–12.7.
8. 🧪 Quiz / 📊 Exam / 👨‍🏫 Tutorial: none yet

**Cross-topic synthesis (Hard):**
- With [[#Topic: State space & volatility]]: T §12.7–12.8, MCMC estimation of stochastic volatility.
- With [[#Topic: Endogeneity & IV]]: MHE Figures 4.6.1–4.6.3, a Monte Carlo study of weak instruments.
