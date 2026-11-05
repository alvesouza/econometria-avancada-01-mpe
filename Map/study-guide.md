---
tags: [map, cross-reference]
date: 2026-10-19
---
# Study Guide

The order follows the lecturer's site ([[Aula/COURSE]]): 9 classes and a final exam, with no dates published. Per-class detail, including every slide, the lecturer's R examples and the Python packages to port them, is in [[Map/class-plan]]. Topic progressions and exercise IDs are in [[Map/topics-index]] and [[Map/exercises-index]]. Abbreviations: MHE, W = Wooldridge 6e, T = Tsay AFTS 3e, I = ISLP (2023; same chapters as ISLR 2e), G = Greenberg 1e, AME = Izbicki & Mendonça (2020), MS = Morettin & Singer (prelim. 2021), B = Bolfarine & Sandoval (2010).

## Class 1: Review: likelihood, regression, AR/VAR

### Before class
- Slides: [[Aula/class-01/materials/mle_sampling_rules.pdf|MLE and its estimators]], [[Aula/class-01/materials/multiplelinearregression.pdf|linear regression]] (pp. 1–22), [[Aula/class-01/materials/ar-ma.pdf|AR(1)]] (pp. 1–17).
- Read (assigned): B §1.1.4, §1.3, §2.1, §2.2, §3.1, §3.2 (pp. 2–45, selected).
- Read: W Ch. 2, §3.1–3.3, §5.1–5.2; T §2.1–2.4 (pp. 30–57), §8.1–8.2 (pp. 390–417); I §5.2 (pp. 212–215); AME §1.4–1.5 (pp. 9–24); MS §6.2–6.3 (pp. 184–215).
- Review: [[rules/04_arima_raiz_unitaria|AR / unit root formulas]], [[rules/05_espaco_estados_volatilidade|VAR formulas]]
- **Notes:** [[Notas/L01/L01-00-map|Class 1 notes]] (likelihood and sampling rules, Poisson MLE and the coal-mining change point, first Bayesian example, MSE and the bootstrap, OLS, AR/VAR, p-hacking)

### After class
- Practice: B 1.4, 1.9, 2.2, 3.6, T 2.2, W 11.C8, G 2.2 → then B 2.10, 3.13, I 5.2, 5.9, W 12.1.

### Connections
- Prerequisite for: every later class. AR(1) leads to [[#Class 8: Univariate time series|Class 8]], VAR(1) to [[#Class 9: Multivariate time series|Class 9]], and the Poisson-with-prior example to [[#Classes 3+4: Bayesian learning|Classes 3+4]].

## Class 2: Statistical learning

### Before class
- Slides: [[Aula/class-02/materials/motorcyle-polynomialregression.pdf|motorcycle example]], [[Aula/class-02/materials/logisticregression-discriminantanalysis.pdf|logistic regression and discriminant analysis]].
- Read: I §2.2 (pp. 27–40), §4.3–4.6 (pp. 138–173), §5.1 (pp. 202–212), §7.1 (pp. 290–292); W §17.1, §17.3; AME §1.5.1, Ch. 7, §8.1 (pp. 14–21, 133–151); MS Ch. 8 (pp. 263–290).
- Review: [[rules/06_classificacao_validacao|Key formulas]]
- **Notes:** [[Notas/L02/L02-00-map|Class 2 notes]] (bias–variance, log-linear regression, cross-validation, logistic regression, discriminant analysis, Poisson regression)

### After class
- Practice: I 2.1, 2.3, 4.1, 4.9, 5.3 → then I 4.13, 4.14, 5.5, 5.8, 7.9; MS 8.4, 8.9; W 17.C1, 17.C4.

### Connections
- Depends on: [[#Class 1: Review: likelihood, regression, AR/VAR|Class 1]] (bias–variance, bootstrap)
- Prerequisite for: [[#Class 7: More econometric models|Class 7]] (probit and Tobit), and the Bayesian logit in [[#Classes 3+4: Bayesian learning|Classes 3+4]]

## Classes 3+4: Bayesian learning

### Before class
- Slides: [[Aula/class-03-04/materials/aprendizagembayesiana-bayesianingredients.pdf|Bayesian ingredients]], [[Aula/class-03-04/materials/notas-bayesianas-slides.pdf|Bayes estimators and losses (PT)]], [[Aula/class-03-04/materials/sparse-priors.pdf|sparse priors]].
- Read: G Ch. 2–4 (pp. 7–59); G Ch. 5–7 (pp. 63–107); T §12.1–12.4 (pp. 614–624).
- Review: [[rules/07_bayes|Bayes formulas]], [[rules/08_monte_carlo_mcmc|MC / MCMC formulas]]

### After class
- Practice: G 2.2, 2.4, 3.3, 3.4 → 3.2, 3.8, 4.5; G 5.4, 6.2, 7.1 → 7.3, 7.5, 7.8; T 12.1–12.3.

### Connections
- Depends on: [[#Class 1: Review: likelihood, regression, AR/VAR|Class 1]] (likelihoods)
- Prerequisite for: hierarchical models ([[#Class 7: More econometric models|Class 7]]), Bayesian GARCH/SV ([[#Class 8: Univariate time series|Class 8]]), and BVAR/FSV ([[#Class 9: Multivariate time series|Class 9]])

## Classes 5+6: Causal inference

### Before class
- Slides: [[Aula/class-05-06/materials/notes-on-causal-inference.pdf|notes on causality]], [[Aula/class-05-06/materials/error-in-variables.pdf|error-in-variables]].
- Read: MHE Ch. 2, §3.2, §4.1, §4.4, §5.2, Ch. 6 (pp. 10–202, selected); W §9.4, §15.1–15.5, §13.2. DAGs: Neal (2020) or *The Mixtape* (links in [[Aula/COURSE]]).
- Review: [[rules/02_causalidade_potential_outcomes|potential outcomes]], [[rules/01_endogeneidade_iv|IV]], [[rules/03_painel_did|DiD]]
- Already built: [[Aula/class-05-06/potential-outcomes.ipynb|potential-outcomes notebook]] and its three companions in `Aula/class-05-06/`.

### After class
- Practice: MHE Tables 2.2.1–2.2.2, 4.1.1–4.1.3, 5.2.1, Table 6.2.1; W 15.C3, 15.C5, 13.2, 13.6, 13.C3 → then G 11.1–11.4.

### Connections
- Depends on: [[#Class 1: Review: likelihood, regression, AR/VAR|Class 1]] (regression)
- Prerequisite for: [[#Class 7: More econometric models|Class 7]] (hierarchical and panel structure)

## Class 7: More econometric models

### Before class
- Slides: [[Aula/class-07/materials/GLM3.pdf|general linear models]], [[Aula/class-07/materials/HLM.pdf|hierarchical linear models]], [[Aula/class-07/materials/limiteddependentvariablemodels.pdf|limited dependent variables]].
- Read: W Ch. 8, §12.1–12.3, §17.1–17.2, §17.4; G §4.5–4.6, §8.1–8.2, §9.2–9.3.
- Review: [[rules/03_painel_did|hierarchical models and panels]], [[rules/06_classificacao_validacao|probit/logit]]

### After class
- Practice: W 12.C2, 12.C10, 17.C2, 17.C3; G 8.3, 8.5, 4.6, 9.2 → then G 8.6, 9.3; W 17.3, 14.C5.

### Connections
- Depends on: [[#Classes 3+4: Bayesian learning|Classes 3+4]] (Gibbs with latent data), [[#Class 2: Statistical learning|Class 2]] (logit)

## Class 8: Univariate time series

### Before class
- Slides: [[Aula/class-08/materials/ar-ma.pdf|AR/MA]], [[Aula/class-08/materials/unitroot.pdf|unit root and long memory]], [[Aula/class-08/materials/seasonal.pdf|seasonal]], [[Aula/class-08/materials/bayes-garch.pdf|Bayesian GARCH]].
- Read: T Ch. 2 (pp. 30–103, emphasis §2.4–2.8, §2.11); T Ch. 3 (pp. 109–174); T §12.7; W §18.2–18.3.
- Review: [[rules/04_arima_raiz_unitaria|ARIMA / unit root]], [[rules/05_espaco_estados_volatilidade|GARCH / SV]]

### After class
- Practice: T 2.1, 2.2, 2.6, 3.3, 3.6 → then T 2.3, 2.4, 2.5, 3.11, 3.12, 3.14; W 18.C13.

### Connections
- Depends on: [[#Class 1: Review: likelihood, regression, AR/VAR|Class 1]] (AR(1)), [[#Classes 3+4: Bayesian learning|Classes 3+4]] (MCMC for SV)
- Prerequisite for: [[#Class 9: Multivariate time series|Class 9]]

## Class 9: Multivariate time series

### Before class
- Slides: [[Aula/class-09/materials/BVAR-part11.pdf|VAR]], [[Aula/class-09/materials/BVAR-part2.pdf|BVAR, FAVAR, TVP-VAR]].
- Read: T §8.1–8.2, Ch. 9 §9.1–9.2, Ch. 10 §10.1–10.5, §11.1–11.3; G §10.3.
- Review: [[rules/05_espaco_estados_volatilidade|Key formulas]]

### After class
- Practice: T 8.1, 8.2, 10.1 → then T 8.5, 8.7, 9.7, 10.6; G 10.4.

### Connections
- Depends on: [[#Class 8: Univariate time series|Class 8]], [[#Classes 3+4: Bayesian learning|Classes 3+4]]

## Final exam
- Revise all rule files. No code in the exam, so practise derivations and reading estimation output (the lecturer's examples print R output). Off-schedule syllabus items (panel FE/RE, cointegration, Kalman filter, SMC) are listed at the end of [[Map/class-plan]].
