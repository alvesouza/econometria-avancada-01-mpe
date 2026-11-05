# Notes for Classes 3+4 (L03): Introduction to Bayesian learning — plan (2026-10-25)

Spec: `.claude/commands/notes.md` (binding); companions `.claude/commands/companion.md` Steps 2–6.
Shared plan: `.agent/plans/all-units-study-set.md`. Design copied from `Notas/L01`, `Notas/L02`
and `.agent/plans/notas-L01-L02.md` (front matter, Claim, Notation table, `## k · U|C|G`, numbered
equations, worked examples, figure captions, companion callouts, `## Links`).

**Step 0 answers (given by the lead, not re-asked):** depth Full; equation-led; model curves,
4–8 figures, exact expressions, comparative statics; companions yes (2 for this unit); PDF yes.
Status `taught` (slides in `Aula/class-03-04/materials/`).

## Shared facts (do not re-derive)

- Sources read (text in the session scratchpad `.../scratchpad/L03/`):
  `aprendizagembayesiana-bayesianingredients.pdf` (56 slides: Diego, measurement error,
  physicists A/B/C, MC toy π); `notas-bayesianas-slides.pdf` (16 slides, PT: loss functions,
  Exp–Gamma); `question0.pdf` + `question0-R.txt` (three coins); `examples-from-stone-2013.pdf`
  (image PDF, 7 pages: smallpox/chickenpox, "four candles", forward/inverse probability);
  `sparse-priors.pdf` (image PDF, 9 pages: horseshoe CPS 2010, Table 1 κ-densities, Vanguard
  Table 4, normal-gamma Griffin–Brown 2010, NIR Table 3); `sparseregression-simulation.pdf` +
  `-R.txt` (bayesreg boxplots); site pages `sequential-bayes-bernoulli-uniform-trials.html`,
  `bernoulli-trials-discrete-prior.html`, `fisicos-ABCD.html`, `correlationcoefficient.html`,
  `ZIP-fishing.html`, `hierarchical-beta-binomial.html`, `hierarchical-gaussian-linear-model.html`,
  `Bayesian-logistic-regression.html`, `Bayesian-beta-regression.html`,
  `petrobras-gaussian-student-SV-models.html`, `exemplos-1-2-3-R-STAN.txt`.
- Book pages opened (printed; offsets from `.agent/notes/book-offsets.md`, verified):
  G (+15) pp. 12–19, 20–40, 41–59, 63–75, 76–89, 90–107, 111–130; B (+6) pp. 61–72, 85–89;
  T (+27) pp. 614–624, 636–638; MS (+10, measured: printed 460 = PDF 470) pp. 453–478, 487–489;
  AME (+18) pp. 42–43; ISLP Ch. 6 (+8, measured: printed 240 = PDF 248) pp. 240–251.
- Errata found while reading (to be reported in the map):
  1. Ingredients deck slide 40 prints Physicist B's prior as N(800, 40²) and slide 44 as
     N(800, 1600); the posterior N(840, 35.7²) on slide 40 and `fisicos-ABCD.html` (σ_B = 80)
     require N(800, 80²).
  2. `sequential-bayes-…html`, Pareto section: text gives E(θ|x) = θ₁α₁/(α₁+1); the code (and
     the Pareto mean) use θ₁α₁/(α₁−1). The prior density is typed α₀θ₀^α/(aθ^{α₀+1}).
  3. `fisicos-ABCD.html` writes prior D with N(μ_A, σ_A²) twice; its code uses A, B, C.
  4. `correlationcoefficient.html` states the arc-sine prior 1/(π√(1−ρ²)) but codes
     `prior = 1/sqrt(1+rho^2)`.
  5. `ZIP-fishing.html` says n = 42; its frequency table sums to 45, and the printed MLE
     (4.223, 0.526) and MM (7.159, 0.721) are reproduced with n = 45.
  6. `hierarchical-gaussian-linear-model.html` full conditionals: V_i is printed without the
     inverse and m_i without the 1/σ² on X_i'y_i (the code has both); β_i's prior is printed with
     τ_α.
  7. Stone Fig. 1.4 prints p(θ_s) = 0.0011 in the box but uses 0.001 in the arithmetic.
- Python only (numpy/scipy/matplotlib/statsmodels). Coal series reused from
  `Notas/L01/companions/check_companions.py` (`cc.Y`). Hierarchical-Gaussian data parsed from the
  site HTML at run time (no copy).
- Abbreviations as in `Map/class-plan.md`: G, T, B, MS, AME, I.

## Note list

| # | File | Covers (sources) | Settles | Figures |
|---|---|---|---|---|
| 00 | `L03-00-map.md` | — | front door | — |
| 01 | `L03-01-bayes-rule-discrete.md` | ingredients slides 1–25; `question0.pdf` (18 slides) + R; Stone (2013) pp. 1–7 of the deck; `bernoulli-trials-discrete-prior.html`; G §2.1–2.2 (pp. 7–18), §3.1.3 (pp. 24–25) | posterior = prior × likelihood / predictive; Diego 0.785 → 0.847, Y: 0.8448 → 0.9928, Y alone 0.9830; coins 0.618, 0.0674/0.3932/0.5394, fourth head; base rates (Stone 0.988 vs 0.011); sequential = batch; discrete prior {0.3, 0.5, 0.8} | `L03-sequential-learning` (a) |
| 02 | `L03-02-conjugate-sequential-updating.md` | `sequential-bayes-…html`; G §2.2 (pp. 15–18, (2.4)–(2.5)), §3.1.3, §3.1.4 (pp. 25–27), §3.2.3 (pp. 32–33), Ex. 2.4 named; B Ex. 4.4.1–4.4.2 (pp. 65–68), Ex. 5.5.2 (pp. 86–87); T Results 12.3–12.6 (pp. 620–621) | Beta–Bernoulli (α₀+s, β₀+n−s), weighted-average mean, uniform prior → mode = MLE, predictive (α₀+s)/(α₀+β₀+n); Gamma–Poisson, Gamma–Exponential; Pareto–Uniform (max(θ₀,x₍ₙ₎), α₀+n); large-n normality | `L03-sequential-learning` (b), (c) |
| 03 | `L03-03-normal-measurement-physicists.md` | ingredients slides 26–52; `fisicos-ABCD.html`; G §3.2.3, Ex. 3.3 named, §4.2 (pp. 43–44); B Ex. 4.4.3 (pp. 68–69), Ex. 5.5.1 (p. 86); T Result 12.1 (pp. 618–619) | predictive N(μ₀, σ²+τ₀²); posterior N(μ₁, τ₁²), weight w = σ²/(σ²+τ₀²); A: 890 (17.9), B: 840 (35.8); Student-t prior C and mixture D by quadrature: 891.2, 876.2; bounded influence of a t prior | `L03-normal-four-priors` |
| 04 | `L03-04-bayes-estimators-loss.md` | `notas-bayesianas-slides.pdf` (16 slides); G §3.2.1–3.2.2 (pp. 29–31); B §4.3–4.4 (pp. 61–70), §5.5 (pp. 85–87) | posterior expected loss; quadratic → mean, absolute → median, 0–1 → mode, bilinear → quantile a/(a+b); Exp–Gamma; Bayes estimators biased but consistent; credible vs HPD intervals | `L03-loss-functions` |
| 05 | `L03-05-model-comparison-bayes-factors.md` | G §3.2.4 (pp. 33–38), §4.2 (pp. 43–44), §7.1.2 named; coins and Diego as model choice | marginal likelihood (3.4), posterior odds, Bayes factor, Jeffreys Table 3.1, Laplace/BIC approximation, Michaela–Lila Table 3.2 reproduced, improper priors make BF arbitrary, model averaging | `L03-bayes-factor-sample-size` |
| 06 | `L03-06-monte-carlo-simulation.md` | ingredients slides 53–56; G Ch. 5 (pp. 63–75); MS App. B §B.2, §B.6 (pp. 456–471); `fisicos-ABCD.html` (SIR), `correlationcoefficient.html`, `ZIP-fishing.html` | MC integration and n.s.e.; PIT; composition (t as scale mixture); accept–reject (Beta(3,3): c = 1.875, 0.5333; N from Laplace: c = √(2e/π) = 1.3155, 0.6577); importance sampling 0.8268 vs 0.8302; SIR; ZIP MLE 4.223/0.526 and grid posterior; correlation posterior | `L03-monte-carlo-accept-reject` |
| 07 | `L03-07-markov-chains-gibbs.md` | G Ch. 6 (pp. 76–87), §7.1 (pp. 91–95), §7.3 (pp. 102–103); T §12.1–12.3 (pp. 614–621); MS §C.5 (pp. 487–488) | transition matrix (6.2), invariant (1/3, 2/3), P¹⁰, P²⁰; Gibbs invariance proof; normal mean–precision Gibbs (7.1)–(7.2); switch-point model (7.3)–(7.4) on the coal data with the L01-04 prior; exact p(k|y) vs Gibbs; bivariate-normal mixing (lag-1 autocorrelation ρ²); burn-in, n.s.e., batch means, inefficiency | `L03-gibbs-switch-point`, `L03-mcmc-mixing` (a) |
| 08 | `L03-08-metropolis-hastings-hmc.md` | G §7.2 (pp. 96–101), §8.2.3 (pp. 126–129); T §12.4 (pp. 622–624), §12.7 (pp. 636–638); `Bayesian-logistic-regression.html`; `exemplos-1-2-3-R-STAN.txt`; `petrobras-…html`; `Bayesian-beta-regression.html` (named) | reversibility, α(x,y) (7.6), Algorithm 7.4; random-walk and independence kernels; Beta(3,4) example (0.57, 0.4296 vs 0.4286); Gibbs = MH with α = 1; RW acceptance (2/π)arctan(2/s) for a N(0,1) target; Bayesian logit (GLM −11.30/0.0596/4.06 vs UPG −10.82/0.06/3.82); HMC/NUTS and SV named (G) | `L03-mcmc-mixing` (b) |
| 09 | `L03-09-hierarchical-models-shrinkage.md` | G §4.5–4.6 (pp. 50–53); `hierarchical-beta-binomial.html` (13 hospitals, Stan); `hierarchical-gaussian-linear-model.html` (68 women, Gibbs) | exchangeability; three-level model; Beta–Binomial with (μ, η): exact grid posterior vs Stan (μ median 0.0715, η median 225.7); borrowing strength; Gaussian random-coefficient Gibbs full conditionals; pooled OLS −4.526/0.476/3.612 | `L03-shrinkage` (a) |
| 10 | `L03-10-sparsity-priors.md` | `sparse-priors.pdf` (9 pages); `sparseregression-simulation.pdf` + R; AME §3.6 (pp. 42–43); I §6.2 (pp. 240–251) | ridge = posterior mode under a Gaussian prior, lasso under a Laplace prior; scale mixtures of normals; horseshoe κ ~ Be(1/2,1/2), E(θ|y) = (1−E(κ|y))y; normal–gamma variance 2λγ², excess kurtosis 3/λ; shrinkage profiles; Vanguard and NIR tables read | `L03-shrinkage` (b) |
| 11 | `L03-11-formulas.md` | all | goals mapped; every result; every number | — |
| 12 | `L03-12-pitfalls.md` | all | confusions + original 25–30 item V/F | — |
| 13 | `L03-13-python.md` | all | reference code = `L03_python_checks.py`, asserts vs the decks' numbers | — |

Out of scope / named only: SMC (not on site), reversible jump, Chib marginal-likelihood
computation (named), SV estimation details (Class 8), Bayesian VAR (Class 9).

## Figures (8), `Notas/L03/figures/make_figures.py`

| Figure | Exact expression | Comparative static | Assert |
|---|---|---|---|
| `L03-sequential-learning` | (a) coin posteriors ∝ (1/3)p_k^n; (b) Beta(2,2) prior, likelihood, Beta posterior for G Fig. 2.2 (n=10, s=3; n=50, s=15); (c) Pareto posterior quantiles vs n (seeded U(0,2) sample, θ₀=1.5, α₀=0.1) | n | 0.0674, 0.3932, 0.5394; E = 5/14, 17/54 |
| `L03-normal-four-priors` | priors A–D, likelihood x=850, σ=40; posteriors by quadrature; posterior mean vs x for A and C | x | 890, 840, C 891.2, D 876.2 |
| `L03-loss-functions` | expected posterior loss for quadratic, absolute, 0–1 (ε) under Beta(2,10) (uniform prior, n=10, s=1) | loss | mean 1/6, mode 0.1, median |
| `L03-bayes-factor-sample-size` | log10 B12 vs Michaela's proportion (Lila = 1 − it) for m = 10, 100, 1000 | m | Table 3.2 |
| `L03-monte-carlo-accept-reject` | (a) Beta(3,3) under 1.875·U(0,1); (b) running π̂ (seeded) inside ±2√(π(4−π)/M) | M | 1.875, 0.5333 |
| `L03-gibbs-switch-point` | exact p(k|y) and Gibbs histogram; λ₁, λ₂ marginals | — | mode 1891; TV < 0.02 |
| `L03-mcmc-mixing` | (a) Gibbs bivariate normal: lag-1 autocorrelation ρ², inefficiency (1+ρ²)/(1−ρ²); (b) RW-MH acceptance (2/π)arctan(2/s) with simulated points | ρ, s | 0.4448 at s=2.38 |
| `L03-shrinkage` | (a) hospitals y/n vs E(p_i|y) (grid); (b) E(θ|y) vs y under normal, Laplace, horseshoe priors (τ=σ=1, quadrature) | prior | μ median ≈ 0.0715 |

## Companions (control contracts)

### L03-a `Notas/L03/companions/companion-normal-prior-conflict.html` — "The Prior-Conflict Dial"
Model: $x\mid\theta\sim N(\theta,\sigma^2)$; prior Normal $N(\mu_0,\tau_0^2)$ or Student-$t_\nu(\mu_0,s^2)$ with the
same variance, $s^2=\tau_0^2(\nu-2)/\nu$; posterior by quadrature on a 4001-point grid (exact
closed form for the normal, used as a check). Source: ingredients slides 34–52; `fisicos-ABCD.html`; G §3.2.3.

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| Observation | x | the measurement | 600–1100 | 1 | 850 | — | slide 39 | likelihood, both posteriors, mean-vs-x marker |
| Measurement sd | σ | sd of x given θ | 5–120 | 1 | 40 | — | slide 28 | likelihood width, weights |
| Prior mean | μ₀ | physicist's best guess | 600–1100 | 1 | 900 | — | slide 31 | priors, conflict |
| Prior sd | τ₀ | prior uncertainty | 5–200 | 1 | 20 | — | slide 31 | prior widths, weights |
| Student-t df | ν | tail thickness of prior C | 3–60 | 1 | 5 | — | slide 45 | t prior, its posterior |

Panels: (1) prior N, prior t, likelihood, two posteriors over θ; (2) posterior mean vs x for both
priors with the 45° line and current x. Answer read-out: **posterior mean under each prior** and
the normal weight $w=\sigma^2/(\sigma^2+\tau_0^2)$; also posterior sd, $P(\theta<x\mid x)$, conflict
$|x-\mu_0|/\sqrt{\sigma^2+\tau_0^2}$. Landmarks: x = μ₀ (no conflict: both posteriors centred
near μ₀), defaults reproduce 890.0 / 17.9 (A) and 891.2 (C).

### L03-b `Notas/L03/companions/companion-bayes-factor-coins.html` — "The Bayes-Factor Dial"
Model (G §3.2.4, pp. 37–38): M1 $\theta_1=\theta_2=\theta$, M2 $\theta_1\ne\theta_2$; Beta(α, α) priors
(α = 1 is Greenberg's); $m_1=B(\alpha+s_1+s_2,\alpha+2m-s_1-s_2)/B(\alpha,\alpha)$,
$m_2=\prod_j B(\alpha+s_j,\alpha+m-s_j)/B(\alpha,\alpha)$; $\log_{10}B_{12}$; posterior
$P(M_1\mid y)=1/(1+(p_2/p_1)/B_{12})$; Laplace/BIC approximation shown for comparison.

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| Tosses each | m | tosses by each girl | 1–200 | 1 | 10 | — | Table 3.2 | everything |
| Michaela's heads | s₁ | heads by Michaela | 0–m | 1 | 2 | — | Table 3.2 | BF, curve marker |
| Lila's heads | s₂ | heads by Lila | 0–m | 1 | 8 | — | Table 3.2 | BF, curve |
| Prior Beta(α, α) | α | prior concentration on each θ | 0.1–20 (log) | — | 1 | — | p. 37 (α = 1) | BF level |
| Prior odds | p₁/p₂ | P(M1)/P(M2) | 0.01–100 (log) | — | 1 | — | (3.3) | posterior P(M1|y) |

Panels: (1) log10 B12 against Lila's heads s₂ = 0…m with Jeffreys bands; (2) the two marginal
likelihoods' building blocks: posterior densities of θ under M1 and θ₁, θ₂ under M2. Answer
read-out: **log10 B12** with the Jeffreys label; also P(M1|y), BIC approximation. Landmarks:
the Table 3.2 rows (m = 10: (1,9) −2.506, (2,8) −1.200, (5,5) 0.297), s₁ = s₂.

Verification: `Notas/L03/companions/check_companions.py` (Python recomputation vs the page's
`<script id="model">` under node at both ends + default + landmark vectors; stub-DOM sweep; reset).

## Verification

`python Notas/L03/figures/make_figures.py`; `python Notas/L03/L03_python_checks.py`;
`python Notas/L03/companions/check_companions.py`; `python tools/check_note_links.py Notas/L03`;
`python -I ~/.claude/commands/templates/notes_pdf.py Notas/L03` (no `Missing character`;
`pdffonts` no Type 3). No exercise statement reproduced. Row for `Notas/00-index.md` in the report
(the lead edits indexes).
