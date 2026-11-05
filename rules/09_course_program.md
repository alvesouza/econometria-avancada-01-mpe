# Course programme — Econometria Avançada (MPE, Insper)

> Tier-2 file, loaded on demand. Source: syllabus `Captura de tela 2026-10-07 225720.png` (currículo 202431, 30 h).
> Official schedule (lecturer's site, re-checked 2026-10-19): `Aula/COURSE.md`; plan with sections and pages `Map/class-plan.md`. Site topics beyond the topic table below (RDD, DAGs, sparsity, Tobit/ordered probit, seasonal, BVAR/FAVAR/DCC) are in scope; see the end of `Map/class-plan.md`.

## Class × bibliography (site schedule)

B = Bolfarine & Sandoval (2010), AME = Izbicki & Mendonça (2020): both on the site's list, not in the syllabus. Other abbreviations as in the topic table.

| Class | Block | Topics | Primary | Supporting |
|---|---|---|---|---|
| 1 | Review | — (background), 04, 05 | B Ch. 1–3 (assigned by the site); B §6.5 (LR test) | W Ch. 2–3, §5.1–5.2, §6.3; T §2.1–2.4, §8.1–8.2; I §5.2 (bootstrap); G §2.2, §7.1.1 (Poisson switch point, Bayesian follow-up); AME §1.4–1.5, Ch. 2–3 |
| 2 | Statistical learning | 06 | I §2.2, Ch. 4, §5.1–5.2, §7.1 | W §17.1, §17.3; AME §1.5.1, Ch. 7, §8.1, §9.1 |
| 3+4 | Bayesian learning | 07, 08 | G Ch. 2–8 | T Ch. 12; B Ch. 4–5; I §6.2 (ridge/lasso); AME §3.6 |
| 5+6 | Causal inference | 02, 01, 03 (DiD) | MHE Ch. 2–6 | W §9.4, Ch. 15, §13.2; G Ch. 11; DAGs: Neal (2020), Mixtape (web) |
| 7 | More econometric models | 03 (hierarchical), 06 (probit/Tobit) | W Ch. 8, §12.1–12.3, Ch. 17; G §8.1–8.2 | G §4.5–4.6, §9.2–9.3; I §4.6; T §2.9; W Ch. 14, MHE §5.1 (FE/RE) |
| 8 | Univariate time series | 04, 05 | T Ch. 2–3 | W §10.5, §11.1, §12.6, Ch. 18; T §12.7 |
| 9 | Multivariate time series | 05 | T Ch. 8–11 | G §9.1, §10.3; BVAR/FAVAR/TVP-VAR: slides only |

## Objective (syllabus)

Introduce basic microeconometrics, macroeconometrics, statistical learning and Bayesian learning needed for the master's programme.

## Topic × bibliography

| Topic | Syllabus item | MHE (Angrist & Pischke) | Wooldridge (6e on disk; syllabus 5e) | Tsay AFTS (3e) | ISLP (2023; ISLR 1e same chapters) | Greenberg (1e on disk; syllabus 2e) |
|---|---|---|---|---|---|---|
| 01 | Regression with endogeneity; IV; potential outcomes; measurement error | Ch. 2, Ch. 4 (4.1–4.6) | Ch. 9.4, Ch. 15 | — | — | §11.2 (Bayesian IV) |
| 02 | Neyman–Rubin model; selection bias; reverse causality; omitted variables | Ch. 2, Ch. 3 (3.2) | Ch. 3.3, Ch. 16 | — | — | §11.1, §11.3 (treatment, selection) |
| 03 | Panel data, hierarchical models, FE/RE; difference-in-differences | Ch. 5 | Ch. 13, Ch. 14 | — | — | §4.5–4.6, §9.3, §10.4 |
| 04 | ARIMA; long memory; unit root; integration / cointegration | — | Ch. 10–11, Ch. 18 | Ch. 2, Ch. 8 (cointegration) | — | — |
| 05 | State-space models; GARCH / stochastic volatility; VAR; factor models; time-varying parameters | — | Ch. 12 (ARCH) | Ch. 3, 8, 9, 10, 11 | — | §10.2–10.3 (regime switching, TVP) |
| 06 | Logistic regression; classification metrics; train/test; cross-validation; bias–variance | — | Ch. 17.1 | — | Ch. 2.2, 4.3, 5.1 | §8.2 (Bayesian probit/logit) |
| 07 | Prior, posterior and predictive distributions; sequential Bayes; conjugate analysis | — | — | Ch. 12 (12.1–12.3) | — | Ch. 2–4 (core reference) |
| 08 | Monte Carlo; MCMC; sequential Monte Carlo | — | — | Ch. 12 | Ch. 5.2 (bootstrap) | Ch. 5–7 (no SMC) |

Chapter numbers in the Wooldridge column refer to the **6th edition** (the copy in `Livros/`). Exercise numbers may differ from the 5th edition named in the syllabus.

## Bibliography

**Basic**
- Angrist, J. D.; Pischke, J.-S. *Mostly Harmless Econometrics: An Empiricist's Companion*. Princeton UP, 2009. — primary text for topics 01–03.

**Complementary**
- Tsay, R. S. *Analysis of Financial Time Series*, 3rd ed. Wiley, 2010. — topics 04, 05, 08.
- James, G.; Witten, D.; Hastie, T.; Tibshirani, R. *An Introduction to Statistical Learning with Applications in R*, 1st ed. Springer, 2013. — topic 06. The 2nd ed. (2023) and the Python edition **ISLP** (2023) are also in `Livros/`; ISLP is the code companion.
- Greenberg, E. *Introduction to Bayesian Econometrics*, 2nd ed. Cambridge UP, 2012. — topics 07–08. **1st ed. (2008) used instead.**
- Wooldridge, J. M. *Introductory Econometrics: A Modern Approach*, 5th ed. — **6th ed. used instead** (Cengage, 2016).

Found/missing status and source paths: `Livros/BOOKS.md`.

## Directory structure

| Dir | Purpose |
|---|---|
| `Aula/` | lecture slides and class scripts |
| `Listas/` | exercise lists; `lista-exam.tex` template |
| `Livros/` | textbooks + `BOOKS.md` |
| `Monitoria/` | tutorial material |
| `Simulados/` | quiz MD files for `quiz.html` |
| `Resolucao/` | generated solutions |
| `Leituras/` | chapter extracts and TTS scripts |
| `Map/` | Obsidian cross-reference maps |
| `NotebookLM/` | prompts (`slides/`, `audio/`, `video/`) and `sources/` |
| `Videos/` | one subdir per `/explainer` video |
| `rules/` | `00`–`09` course rules; other files are Efficient Token packs |

## Rules index

| File | Content |
|---|---|
| `rules/00_estilo_avaliacao.md` | exam / list style and rubric |
| `rules/01_endogeneidade_iv.md` | topic 01 |
| `rules/02_causalidade_potential_outcomes.md` | topic 02 |
| `rules/03_painel_did.md` | topic 03 |
| `rules/04_arima_raiz_unitaria.md` | topic 04 |
| `rules/05_espaco_estados_volatilidade.md` | topic 05 |
| `rules/06_classificacao_validacao.md` | topic 06 |
| `rules/07_bayes.md` | topic 07 |
| `rules/08_monte_carlo_mcmc.md` | topic 08 |
