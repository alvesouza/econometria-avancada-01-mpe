---
tags: [practice, class-01, potential-outcomes]
date: 2026-10-09
---
# Practice plan: Class 1, potential outcomes and selection bias

Book exercises for Class 1 (MHE Ch. 1–2), ordered from easy to hard. This file gives **references only** (exercise number + printed page); the problem statements are in the books. Notes: `Aula/class-05-06/potential-outcomes.ipynb`. Topic rules: [[rules/02_causalidade_potential_outcomes]]. Index: [[Map/exercises-index]].

**Sources.** Wooldridge 6e (W) supplies the real exercises. MHE has no end-of-chapter exercises, so its three tables are used as "read and interpret" tasks. Greenberg 1e §11.1 appears only as a deferred row (it needs the Bayesian tools of Classes 14–16). All numbers and pages were checked in the converted book Markdown on 2026-10-09.

**Data for the computer exercises (R).** `install.packages("wooldridge")`, then `data("jtrain2")`, `data("jtrain3")`, `data("fertil2")`, `data("apple")`.

## Weights

| Subtopic | Weight | Exercises | Why this weight |
|---|---|---|---|
| A. Causal questions and the ideal experiment | 15% | 2 | MHE Ch. 1; quick to practise, short exam questions |
| B. Naive comparisons and selection bias | 35% | 4 | the core decomposition (MHE p. 11); the most links in `Map/topics-index` for this topic |
| C. Random assignment and regression analysis of experiments | 35% | 5 | MHE §2.2–2.3; balance checks, adding controls, experimental vs observational data |
| D. Heterogeneous effects: what OLS estimates | 10% | 1 | links ATE to regression; proof-style |
| Tangential: sample selection | 5% | 1 | a different "selection", often confused with treatment selection |

Levels: 6 foundations → 5 exam → 2 advanced (13 in total), plus 3 deferred.

---

### A. Causal questions and the ideal experiment, weight 15%

| Level | Source | Ch./Sec. | Exercise(s) | Page | What it trains |
|---|---|---|---|---|---|
| Foundations | W 6e | Ch. 1, Problems | 1.1 | 15 | Design the ideal class-size experiment; why observational data give a misleading correlation (MHE FAQ 2) |
| Foundations | W 6e | Ch. 1, Problems | 1.2 | 15 | State the ceteris paribus thought experiment for job training; why firms' training choices are not independent of worker traits |

### B. Naive comparisons and selection bias, weight 35%

| Level | Source | Ch./Sec. | Exercise(s) | Page | What it trains |
|---|---|---|---|---|---|
| Foundations | MHE | Ch. 2, §2.1 | NHIS table (hospital vs no hospital) | 10 | Read the naive gap and its *t*; argue the sign of selection bias before any algebra |
| Foundations | W 6e | Ch. 1, Computer Exercises | C4 (JTRAIN2) | 16 | Compute a treated-vs-untreated difference in means on experimental data; what would make it convincing |
| Foundations | W 6e | Ch. 1, Computer Exercises | C5 (FERTIL2) | 16 | A difference in means by electricity; why it is not a causal effect (self-selection, omitted factors) |
| Exam | W 6e | Ch. 7, §7-6, Problems | 7.6 | 234 | Sign the OLS bias when less able workers are more likely to be selected into training (selection bias = corr(*d*, error)) |

### C. Random assignment and regression analysis of experiments, weight 35%

| Level | Source | Ch./Sec. | Exercise(s) | Page | What it trains |
|---|---|---|---|---|---|
| Foundations | MHE | Ch. 2, §2.2 | Table 2.2.1 (STAR balance) | 14 | Run a balance check: which rows test randomisation, which test that treatment "took", and why attrition matters |
| Exam | MHE | Ch. 2, §2.2–2.3 | Table 2.2.2 (STAR estimates) | 15 | Explain why the estimate is stable across columns while the SE falls (2.19 → 1.21); role of school fixed effects |
| Exam | W 6e | Ch. 4, Problems | 4.12, part (ii) only | 145 | A low *R*² does not mean bias; what changes if spending were randomly assigned |
| Exam | W 6e | Ch. 6, §6-3, Computer Exercises | C11 (APPLE), parts (i)–(v) | 202 | Randomly assigned prices: unbiased slopes despite *R*² ≈ 0.04; extra controls move precision, not the estimates |
| Advanced | W 6e | Ch. 9, Computer Exercises | C10 (JTRAIN2 vs JTRAIN3) | 308 | Same programme, experimental vs observational data: controls barely matter in the experiment and change the estimate sharply in the observational sample. This is the whole of Class 1 in one exercise |

### D. Heterogeneous effects: what OLS estimates, weight 10%

| Level | Source | Ch./Sec. | Exercise(s) | Page | What it trains |
|---|---|---|---|---|---|
| Advanced | W 6e | Ch. 9, §9-3, Problems | 9.6 | 305 | Proof: with random slopes uncorrelated with *x*, OLS consistently estimates the *average* effect (the regression analogue of ATE under random assignment) |

### Tangential: sample selection (not treatment selection), weight 5%

| Level | Source | Ch./Sec. | Exercise(s) | Page | What it trains |
|---|---|---|---|---|---|
| Exam | W 6e | Ch. 9, §9-5b, Problems | 9.5 | 305 | Whether non-reporting colleges make the *sample* nonrandom (exogenous sample selection). Contrast it with selection into *treatment*, MHE's selection bias |

### Deferred to Classes 14–16

| Level | Source | Ch./Sec. | Exercise(s) | Page | What it trains |
|---|---|---|---|---|---|
| Advanced (later) | Greenberg 1e | Ch. 11, §11.1 | 11.1, 11.2, 11.3 | 180–181 | Verify the conditional distributions of the Bayesian treatment model (Gibbs sampler). Needs priors and posteriors (Class 14) and MCMC (Class 15) |

---

## Suggested order

1. **Warm-up (≈ 1 h):** W 1.1, 1.2, then the MHE NHIS table. Write down the sign of the selection bias in each case before computing anything.
2. **Compute naive gaps (≈ 1 h, R):** W C1.4, C1.5. For each, state what $E[y_0 \mid d=1] - E[y_0 \mid d=0]$ would have to be for the gap to be causal.
3. **Read experiments (≈ 1.5 h):** MHE Tables 2.2.1 → 2.2.2, then W 4.12(ii) and C6.11. The common lesson: under random assignment, controls change the SE, not the estimate.
4. **Exam-level bias argument (≈ 30 min):** W 7.6.
5. **Synthesis (≈ 2 h, R):** W C9.10, the experimental vs observational comparison.
6. **Proof (≈ 45 min):** W 9.6.
7. **Contrast (≈ 20 min):** W 9.5, sample vs treatment selection.

The companions are useful between steps 2 and 3: [The Eight-Person Table](https://claude.ai/artifact/KTnW6qcwYkexQ1sz9PYzzo), [Selection Bias Decomposer](https://claude.ai/artifact/NQH4xcffymY5roEKXjkpWv), [Bigger Sample, Same Bias](https://claude.ai/artifact/9wN4ftRgB32YbgFeYa1jG9).

---

## Consolidated Reading

### MHE — Angrist & Pischke
| Topic | Chapter / Section | Pages | Priority |
|---|---|---|---|
| The four research FAQs, ideal experiments, FUQ'd questions | Ch. 1 Questions about Questions | p. 3–7 | Foundations |
| Selection problem, potential outcomes, decomposition | Ch. 2, §2.1 The Selection Problem | p. 9–12 | Foundations |
| Random assignment, STAR | Ch. 2, §2.2 Random Assignment Solves the Selection Problem | p. 12–16 | Exam |
| Regression analysis of experiments | Ch. 2, §2.3 Regression Analysis of Experiments | p. 16–18 | Exam |

### Wooldridge 6e
| Topic | Chapter / Section | Pages | Priority |
|---|---|---|---|
| Causality and ceteris paribus; Ch. 1 exercises | Ch. 1, §1-4 + Problems/Computer Exercises | p. 10–16 | Foundations |
| Low *R*² vs unbiasedness (Problem 4.12) | Ch. 4, Problems | p. 145 | Exam |
| Goodness of fit, adding regressors to reduce error variance; C6.11 | Ch. 6, §6-3 | p. 180–186 | Exam |
| C6.11 (APPLE) | Ch. 6, Computer Exercises | p. 202 | Exam |
| Policy analysis, program evaluation, self-selection | Ch. 7, §7-6 | p. 229–230 | Exam |
| Problem 7.6 | Ch. 7, Problems | p. 234 | Exam |
| Random slopes | Ch. 9, §9-3 | p. 285–286 | Advanced |
| Nonrandom samples | Ch. 9, §9-5b | p. 294–296 | Exam |
| Problems 9.5, 9.6; C9.10 | Ch. 9, Problems/Computer Exercises | p. 305–308 | Advanced |

### Greenberg 1e (deferred)
| Topic | Chapter / Section | Pages | Priority |
|---|---|---|---|
| Treatment models (Bayesian) and exercises 11.1–11.3 | Ch. 11, §11.1 + Exercises | p. 168–173, 180–181 | Advanced |

## Consolidated Exercises

| # | Exercise | Book | Page | Topic | Level |
|---|---|---|---|---|---|
| 1 | NHIS table | MHE | p. 10 | Naive comparisons and selection bias | Foundations |
| 2 | Table 2.2.1 | MHE | p. 14 | Random assignment: balance | Foundations |
| 3 | Table 2.2.2 | MHE | p. 15 | Regression analysis of experiments | Exam |
| 4 | 1.1 | Wooldridge 6e | p. 15 | Ideal experiment | Foundations |
| 5 | 1.2 | Wooldridge 6e | p. 15 | Ideal experiment / selection | Foundations |
| 6 | C1.4 | Wooldridge 6e | p. 16 | Naive comparison, experimental data | Foundations |
| 7 | C1.5 | Wooldridge 6e | p. 16 | Naive comparison, self-selection | Foundations |
| 8 | 4.12 (ii) | Wooldridge 6e | p. 145 | Random assignment vs *R*² | Exam |
| 9 | C6.11 | Wooldridge 6e | p. 202 | Regression analysis of experiments | Exam |
| 10 | 7.6 | Wooldridge 6e | p. 234 | Sign of selection bias | Exam |
| 11 | 9.5 | Wooldridge 6e | p. 305 | Tangential: sample selection | Exam |
| 12 | 9.6 | Wooldridge 6e | p. 305 | Heterogeneous effects, OLS = average effect | Advanced |
| 13 | C9.10 | Wooldridge 6e | p. 308 | Experimental vs observational data | Advanced |
| 14 | 11.1 | Greenberg 1e | p. 180 | Deferred: Bayesian treatment model | Advanced |
| 15 | 11.2 | Greenberg 1e | p. 180 | Deferred: Bayesian treatment model | Advanced |
| 16 | 11.3 | Greenberg 1e | p. 181 | Deferred: Bayesian treatment model | Advanced |

## Study Roadmap

| Priority | Topic | Reading | Exercises | Suggested time |
|:---:|---|---|---|:---:|
| 1 | Causal questions, the selection problem | MHE p. 3–12; W §1-4 p. 10–14 | W 1.1, 1.2; MHE NHIS table | 1–1.5 h |
| 2 | Naive gaps in data | W Ch. 1 p. 15–16; W §7-6 p. 229–230 | W C1.4, C1.5, 7.6 | 1.5 h |
| 3 | Random assignment and regression | MHE p. 12–18; W §6-3 p. 180–186 | MHE Tables 2.2.1–2.2.2; W 4.12(ii), C6.11 | 1.5–2 h |
| 4 | Synthesis | W p. 308 | W C9.10 | 2 h |
| 5 | Heterogeneity and the contrast case | W §9-3 p. 285–286; §9-5b p. 294–296 | W 9.6, 9.5 | 1 h |
| later | Bayesian treatment model (Classes 14–16) | Greenberg §11.1 p. 168–173 | G 11.1–11.3 | — |
