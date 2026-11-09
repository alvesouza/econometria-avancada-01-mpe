# HW2 (Advanced Econometrics 2026): solutions + guide — plan (2026-11-08)

Statement: `Listas/hw2/hw2-advancedeconometrics-2026.pdf` (Portuguese; outputs in English per global rule).
Data: Mental (Agresti), n = 40, y = impair, x1 = life, x2 = ses. Six models M1–M6.

## Deliverables (all in `Listas/hw2/`)

1. `hw2-advancedeconometrics-2026.ipynb` — detailed solution: full derivations, every item, cross-checks.
2. `hw2-advancedeconometrics-2026-short.ipynb` — short solution: same required steps and numbers
   (derivations the verbs ask for are kept, in compact form); prose and extra checks cut.
3. `hw2-advancedeconometrics-2026-guide.ipynb` — statement per item + code cells with comments only
   (how to solve), and a first section of guidelines drawn from `Pedro/Listas/Lista01-Pedro-Alves-review.md`.

## Method (numpy/scipy only; PyMC/ArviZ not installed)

- Standardise x with ddof=1. Priors: b0~N(25,5^2), bj~N(0,3^2), s2~IG(3,50), nu~Gamma(2, rate 0.1).
- Batched Gibbs sampler: B chains in parallel, each with a 0/1 data mask (B=4 chains for full fits,
  B=40 masks for exact LOO — one batched run per model replaces 40 refits).
  Gaussian: beta|s2, s2|beta. Student-t: beta|s2,w; s2|beta,w; nu by RW-MH on log nu targeting
  p(nu|beta,s2,y) (omega integrated out), then w|nu,beta,s2.
- Diagnostics: traces, ACF, multi-chain ESS (Geyer), split R-hat. Seed fixed; iterations/burn-in reported.
- Marginal likelihood: importance sampling with multivariate-t proposal at the posterior mode
  (unconstrained (beta, log s2, log nu), numerical Hessian). Cross-checks: bridge sampling, Laplace,
  and exact value for M1–M3 (beta integrated analytically, 1-D quadrature over s2). Harmonic mean shown
  only to illustrate why it is avoided (detailed version).
- 2(g): prior s.d. of b0, b1, b2 x3; rerun MCMC + marginal likelihoods; Lindley–Bartlett.
- Q3: exact LOO from the batched runs; predictive mean, median (root of mixture CDF), log predictive
  density. 3(d) LPD again under diffuse priors. 3(e): Gelfand–Dey–Chang CPO and PSIS-LOO (own PSIS).

## Verification

- Data reproduce the statement's summaries (mean 27.30, s.d. 5.46, 44.42/22.62, 56.60/25.28).
- IS vs exact log p(y|M) for M1–M3 agree to MC error; IS vs bridge for M4–M6.
- Notebooks run top to bottom with nbconvert --execute; every number in markdown matches a printed output.
