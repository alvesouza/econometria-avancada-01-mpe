# Notes for Class 1 (L01) and Class 2 (L02) — plan (2026-10-19)

Spec: `C:\Users\pedro\.claude\commands\notes.md` (binding). Style reference: `../Finanças 01 - MPE/Notas/S04/`
(map `S04-00-mapa.md`, section note `S04-07-estimacao-ols-inferencia.md`, `S04-12-armadilhas-vf.md`, `S04-13-computacao-python.md`).
Both units are **`status: taught`** (slides on the site). Companions: **on, every unit**.

## Shared facts (do not re-derive)

- Sources live in `Aula/class-01/materials/` and `Aula/class-02/materials/`; index `Aula/COURSE.md`; per-class readings `Map/class-plan.md`; book sections with printed pages `Map/books-index.md`.
- Page offsets: `.agent/notes/book-offsets.md` (PDF = printed + offset). Quote only pages you opened.
- Coal-mining series (112 years, verified against the deck): `.agent/notes/coal-mining-data.md`.
- Abbreviations (as in `Map/study-guide.md`): B = Bolfarine & Sandoval (2010), W = Wooldridge 6e, T = Tsay AFTS 3e, I = ISLP (2023), G = Greenberg 1e, AME = Izbicki & Mendonça (2020), MS = Morettin & Singer.
- Code is **Python** (numpy/scipy/matplotlib; statsmodels is installed; scikit-learn is NOT). The lecturer's R is reference only. Run with `python` (system 3.12; startup can be slow).
- The handwritten site notes (`class1-poisson.pdf`, `class1-poisson-with-exponential-prior.pdf`, `Class1-comparing-estimators-MSE.pdf`) OCR as noise: open them as images (Read tool on the PDF) if needed; the AI-assisted decks (`poisson-with-breakpoint.pdf`, `comparing-estimators-MSE-slides.pdf`) cover the same ground typeset.
- Existing project material to link (never rebuild): `rules/04`, `rules/05`, `rules/06`, `rules/07`, `rules/08`; `Map/class-plan.md`; `Map/exercises-index.md`. The `Listas/`, `Simulados/`, `Videos/class-01-potential-outcomes`, `Leituras/class-01-narrated.txt` items are **potential outcomes** (now Classes 5+6), not this Class 1: do not link them as Class 1 material.
- Scope: `rules/09_course_program.md` and the class blocks of `Map/class-plan.md`. Ridge/lasso/elastic net/normal-gamma/horseshoe (later pages of `multiplelinearregression.pdf`) and the Bayesian logit are **Classes 3+4**: name them only (G layer), do not develop.

## Conventions every note follows

- Front matter: `tags`, `date: 2026-10-19`, `status: taught`, `source` (deck file + slide numbers; book section + printed pages).
- Title `# <section ids> · <what it settles>`; **Claim** block; `Prev · Next · Map` line; a **Notation** list.
- Sections `## k · U|C|G — title`. U = intuition; C = examinable (slides + main book, numbered as in the source); G = named or proved, not examinable.
- Every derivation step on its own line; equations numbered `(1)`, `(2)` … per note and cited ("substituting (3) into (1)"); substitutions shown in place before simplifying; numbers plugged in shown with enough decimals.
- At least one worked example with the arithmetic in view, using the deck's own numbers.
- Figures: `![alt](figures/LNN-<slug>.png)`, italic caption *what to see + source*, one paragraph reading it.
- Companion callouts: `> **Interactive companion.** [Title](companions/companion-<model>.html) — what to move, what to watch.`
- `## Links` at the end: neighbours, other unit (`[[../L02/L02-0k-...|L02 §k]]`), `rules/` pack, practice **by exercise number and printed page** (never the statement).
- English prose; Portuguese titles/quotes verbatim. `$...$` math only.

## Figures

One script per unit, `Notas/LNN/figures/make_figures.py`, importing `Notas/_figstyle.py` (`sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))`; `apply()`; `save(fig, "LNN-<slug>")`), ending in `assert` checks (≥ 1 plotted number per figure).
**Parallel-writing rule:** each section writer puts its figure functions in `Notas/LNN/figures/_part_<x>.py` (a function `build()` that makes and saves its figures and runs its asserts). The lead merges the parts into the single `make_figures.py` afterwards and deletes them.

## L01 — Class 1: Review of basic ingredients

| # | File | Covers (sources) | Settles | Figures |
|---|---|---|---|---|
| 00 | `L01-00-map.md` | — | front door | — |
| 01 | `L01-01-likelihood-sampling-rules.md` | `mle_sampling_rules.pdf` (all 11 slides); `optimal-samplesize.html`; `bernoulli-iid-logistic-R.txt` (iid vs covariate-dependent Bernoulli, as a bridge to L02-04); B §1.3 (pp. 4–13), §3.1 (pp. 35–42), §6.3 p-value def. (pp. 94–100) | same likelihood, different sampling distributions; Bernoulli/binomial/neg. binomial MLE, observed vs Fisher info, delta method, Haldane bias, Lindley–Phillips p-values, Beta posterior unchanged | `L01-sampling-rules-pmf` (exact pmf of θ̂ under Bin vs NegBin at s=1,4, n=10) |
| 02 | `L01-02-poisson-mle-properties.md` | `poisson-with-breakpoint.pdf` slides 1–12; `class1-poisson.pdf`; `class1-poisson.html` (pmf numbers 0.271, 0.857); B §1.1.4 (pp. 2–3), §2.1 (pp. 15–19, Ex. 2.1.2), §2.2 (pp. 20–23, Ex. 2.2.3), §3.1–3.2 (pp. 35–45), §3.7 (p. 52) | Poisson MLE = ȳ: sufficiency, unbiasedness, consistency, CRLB efficiency; MC table (s² only 20% efficient) | `L01-poisson-pmf`, `L01-poisson-mle-sampling` (MC sampling dist. n=10,50,200 with N(λ, λ/n)) , `L01-poisson-running-mean` |
| 03 | `L01-03-coal-mining-change-point.md` | `poisson-with-breakpoint.pdf` slides 13–21; data `.agent/notes/coal-mining-data.md`; B §3.4 (pp. 46–49, profile likelihood), §6.5 (pp. 103–114, GLRT, Wilks); G §7.1.1 (pp. 91–95) forward link | overdispersion test; two-regime fit; profile likelihood of τ; LR = 70.0; w(τ) table; why profiling ≠ integrating | `L01-coal-series` (counts + three MLE lines), `L01-coal-profile-likelihood` |
| 04 | `L01-04-first-bayesian-poisson.md` | `class1-poisson-with-exponential-prior.pdf` (handwritten: read as image); G §2.2 (pp. 12–18); B §4.3–4.4 (pp. 61–70) as G-layer link | Exp(a) prior with a = 1/2 (E = 2, V = 4) → Gamma(s+1, a+n) posterior; 1851–1891 data n = 41, s = 127: mean 128/41.5 = 3.084, mode 127/41.5 = 3.060, sd √128/41.5 = 0.273 vs MLE 3.098; shrinkage | `L01-poisson-prior-posterior` |
| 05 | `L01-05-comparing-estimators-mse-bootstrap.md` | `comparing-estimators-MSE-slides.pdf` (20 slides); `Class1-comparing-estimators-MSE.pdf`; `comparing-estimators.html` (mean / weighted mean / trimmed mean / median); `bootstrap-example.html`; `correlation-bivariate-gaussian.html`; B §1.1.5 (p. 3), §1.3 Table 1.1 (pp. 4–13), §2.2 factorization for U(0,θ), §3.1 boundary MLE; I §5.2 (pp. 212–215) | MSE = Var + bias²; four U(0,θ) estimators and the ranking θ̂4 < θ̂2 < θ̂3 < θ̂1 (n ≥ 3); 1/n vs 1/n² rates; MC check; nonparametric bootstrap fails for x(n) (P = 1−(1−1/n)^n → 0.632); parametric bootstrap fix | `L01-mse-four-estimators` (MSE vs n, θ = 3), `L01-bootstrap-max-pointmass` |
| 06 | `L01-06-gaussian-linear-regression.md` | `multiplelinearregression.pdf` pp. 1–22 (OLS, matrix form, hat matrix, R², adj. R², Cp, AIC, BIC, best subset; houseprice, Credit); `normallinearregression-R.txt` (Koop–Tobias returns to schooling); `overfitting_a_linear_model.html`; `regressao_abstencao_2026.pdf` (municipal abstention regressions: worked reading of coefficients, HC1 SEs, joint F tests, R² gain); W Ch. 2, §3.1–3.3, §5.1–5.2, §6.3; AME §1.4–1.5, Ch. 2, §3.1–3.2 | OLS = MLE under Gaussian errors; β̂ = (X'X)⁻¹X'y as a projection; σ̂²; model-selection criteria and why R² cannot select; overfitting | `L01-r2-vs-criteria` (from a reproducible simulation, labelled as such), `L01-overfitting-train-test` |
| 07 | `L01-07-ar-var-review.md` | `ar-ma.pdf` pp. 1–17 (stationarity, ACF, Ljung–Box, white noise, linear TS, AR(1) moments and ACF); `ar-var-R.txt` (AR fits, VAR(1), IRF on Canada data); T §2.1–2.4 (pp. 30–57), §8.1–8.2 (pp. 390–417); W §11.1, §11.3 (unit root intuition) | AR(1): OLS = conditional MLE, stationarity |φ| < 1, equilibrium distribution N(μ, σ²/(1−φ²)), unit root φ = 1; AR(p) as a regression; VAR(1) in matrix form, its stationary mean and covariance (vec formula) | `L01-ar1-paths` (φ = 0.5, 0.9, 1), `L01-ar1-equilibrium` |
| 08 | `L01-08-p-hacking-evidence.md` | `part1-p-hacking.pdf`, `p_hacking_slides-economics.pdf` | 1 − 0.95³² ≈ 0.81; X = 1.8 example: p = 0.036 but BF₁₀ ≈ 0.45, P(H1|x) = 0.31; prior odds ≈ 20:1 needed for 0.9; replication evidence (cite the deck's references only) | `L01-p-vs-bayes-factor` |
| 09 | `L01-09-formulas.md` | all | exam spec mapped; every definition/result; every number | — |
| 10 | `L01-10-pitfalls.md` | all | confusions + original 20–30 item V/F (`rules/00_estilo_avaliacao.md`, macro-1 style) | — |
| 11 | `L01-11-python.md` | all | reference code with asserts against the decks' numbers | — |

Not developed (named only): `hierarchical-beta-binomial.html` → Classes 3+4.

## L02 — Class 2: Introduction to statistical learning

| # | File | Covers (sources) | Settles | Figures |
|---|---|---|---|---|
| 00 | `L02-00-map.md` | — | front door | — |
| 01 | `L02-01-prediction-error-bias-variance.md` | `Fundamentos.pdf` (Marques: supervised learning, regression function = E[Y|X], prediction vs inference, reducible/irreducible error, bias–variance decomposition with proof, the tanh simulation f(x) = 45 tanh(x/1.9 − 7) + 57, X ~ U(8,18), σ = 4, n = 30, smoothing-spline gl); `bias-variance-R.txt`; I §2.1–2.2 (pp. 15–40); AME §1.4–1.5 | E[(Y − f̂(X))²] = ∫bias² + ∫var + σ²; flexibility trade-off | `L02-tanh-regression-function`, `L02-bias-variance-curves` |
| 02 | `L02-02-linear-log-linear-regression.md` | `multiplelinearregression.pdf` (as Class 2 lists it; the regression examples), `capm-regression-R.txt`, `regressaomultipla-return-to-education.html`, `salaries-for-professors.txt`; W §2.4 (log functional forms), §6.2 | level-level / log-level / log-log readings; worked return-to-education numbers from the site's page | `L02-log-linear-readings` |
| 03 | `L02-03-cross-validation-motorcycle.md` | `motorcyle-polynomialregression.pdf`, `motorcycle-polynomialregression.html` (orders 1–13, adj. R², BIC, 80/20 split with 100 replications, LOOCV, 10-fold, bootstrap bands; order 12 chosen); I §5.1 (pp. 202–212), §5.2, §7.1 (pp. 290–292); AME §1.5.1 | training vs test error; validation set, replicated CV, LOOCV (with the hat-matrix shortcut), k-fold; bootstrap confidence bands | `L02-cv-curves` (on a reproducible stand-in if the mcycle data are not on disk: say so), `L02-loocv-shortcut` |
| 04 | `L02-04-logistic-regression.md` | `logisticregression-discriminantanalysis.pdf` logistic part (GLM, likelihood, score, Newton–Raphson/IRLS, `default` data: −10.6513 + 0.0055·balance, 0.58% at 1000, 58.6% at 2000, 50% cut-off at 1936; student-only model; balance+student 5.4% vs 10.5%; spam confusion matrix, FN/FP/FDR); `graduate-school-admission.txt/.pdf`; I §4.3 (pp. 138–...); W §17.1 | logit model, MLE by IRLS, reading coefficients/odds, cut-offs, confusion matrix | `L02-logistic-default` |
| 05 | `L02-05-discriminant-analysis.md` | same deck, discriminant part (Bayes and ML discriminant rules, Bernoulli example, Gaussian 1-D example μ1 = 1, μ2 = 5, σ1 = 6, σ2 = 2.5 vs equal σ, LDA via Mahalanobis, QDA, admissibility theorems, unequal costs, iris, admission); I §4.4–4.5; AME Ch. 7 (pp. 133–139), §8.1 (pp. 141–151), §9.1 (pp. 169–172, ROC) | Bayes rule maximises posterior; equal-variance Gaussians → linear rule; unequal → quadratic; costs shift the threshold to log(π2c12/(π1c21)) | `L02-gaussian-discriminant-regions`, `L02-roc` |
| 06 | `L02-06-gaussian-vs-poisson-regression.md` | `Gaussian-vs-Poisson-regression.html`; I §4.6 (pp. 167–173); back-link L01-02 | why counts need a log link; reading Poisson coefficients as rate ratios; mean–variance check | `L02-gaussian-vs-poisson-fit` |
| 07 | `L02-07-formulas.md` | all | spec, definitions, numbers | — |
| 08 | `L02-08-pitfalls.md` | all | confusions + V/F | — |
| 09 | `L02-09-python.md` | all | CV by hand, LOOCV shortcut, IRLS logit, LDA/QDA, Poisson GLM via statsmodels; asserts vs the deck's numbers | — |

## Companions (control contracts)

### L01-a `Notas/L01/companions/companion-poisson-change-point.html` — "The Change-Point Dial"
Model: $y_t\sim$ Poisson$(\lambda_1)$ for $t\le\tau$, Poisson$(\lambda_2)$ for $t>\tau$; $\hat\lambda_j=s_j/n_j$; profile log-lik $\ell_p(\tau)=s_1\log\hat\lambda_1-n_1\hat\lambda_1+s_2\log\hat\lambda_2-n_2\hat\lambda_2$ (0·log 0 = 0); single-rate $\ell(\hat\lambda)$; LR $=2\{\ell_p(\tau)-\ell(\hat\lambda)\}$; $w(\tau)=e^{\ell_p(\tau)}/\sum_{\tau'\in W}e^{\ell_p(\tau')}$; Wald CI $\hat\lambda\pm z\sqrt{\hat\lambda/n}$; dispersion $(n-1)s^2/\bar y\sim\chi^2_{n-1}$. Source: `poisson-with-breakpoint.pdf` slides 14, 17–20. Data embedded (Jarrett 1979).

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| Cut year | τ | last year of the high-rate regime | a … b−1 | 1 | 1891 | year | slides 17–19 | split line, both rate lines, all read-outs |
| First year | a | start of the sample used | 1851–1900 | 1 | 1851 | year | data span | sample, profile curve |
| Last year | b | end of the sample used | 1901–1962 | 1 | 1962 | year | data span | sample, profile curve |
| Weight window | h | w(τ) normalised over τ ∈ [1890−h, 1890+h] ∩ [a, b−1] | 1–40 | 1 | 5 | years | slide 17 ("5 years on each side of 1890") | w(τ) read-out, shaded window |
| Confidence | 1−α | Wald interval level | 0.80–0.99 | 0.01 | 0.95 | — | slide 14 | CI bands |

Panels: (1) yearly counts with $\hat\lambda_1,\hat\lambda_2$ and CI bands; (2) profile log-lik (minus its max) over all admissible τ, current τ and argmax marked. Answer read-out: **LR statistic** (70.0 at defaults) with w(τ) = 0.251; also $\hat\lambda_1,\hat\lambda_2$, ratio, dispersion index and p-value per segment. Landmarks: argmax τ (1891 at defaults), τ = 1890 (the deck's 40/72 split). Page must say the LR is not referred to $\chi^2_1$ (τ is searched).

### L01-b `Notas/L01/companions/companion-four-estimators-mse.html` — "The Four Estimators"
Model: $x_i\sim U(0,\theta)$; $\hat\theta_1=\bar x$, $\hat\theta_2=x_{(n)}$, $\hat\theta_3=2\bar x$, $\hat\theta_4=\frac{n+1}{n}x_{(n)}$; MSE₁ $=\theta^2\frac{1+3n}{12n}$, MSE₂ $=\frac{2\theta^2}{(n+1)(n+2)}$, MSE₃ $=\frac{\theta^2}{3n}$, MSE₄ $=\frac{\theta^2}{n(n+2)}$; family $c\,x_{(n)}$: MSE $=\theta^2[c^2\frac{n}{n+2}-2c\frac{n}{n+1}+1]$, minimised at $c^*=\frac{n+2}{n+1}$; bootstrap point mass $1-(1-1/n)^n$. Source: `comparing-estimators-MSE-slides.pdf` slides 3–5, 12, 18; B §1.3 Table 1.1.

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| Upper bound | θ | true U(0,θ) bound | 0.5–10 | 0.1 | 3.0 | — | slide 6, MC slides | MSE levels (ranking scale-free) |
| Sample size | n | observations | 1–100 | 1 | 10 | — | slide 9 | MSE curves' marker, ranking, bootstrap mass |
| Scale on max | c | estimator $c\,x_{(n)}$ | 0.80–1.40 | 0.001 | 1.000 | — | G-layer extension, stated on page | panel 2 marker, MSE(c) read-out |

Buttons snap c to 1 (MLE), (n+1)/n (unbiased), (n+2)/(n+1) (min-MSE). Panels: (1) MSE vs n (log y) for the four, current n marked; (2) MSE(c x₍ₙ₎) vs c with the three landmarks. Answer read-out: **the ranking** (with ties: all four equal at n = 1; MSE₂ = MSE₃ at n = 2). Defaults reproduce 2.325, 0.136, 0.300, 0.075.

### L02-a `Notas/L02/companions/companion-bias-variance-polynomial.html` — "The Flexibility Dial"
Model: $Y=f(X)+\varepsilon$, $f(x)=45\tanh(x/1.9-7)+57$, $x\in[8,18]$, $\varepsilon\sim N(0,\sigma^2)$ (Fundamentos.pdf slide 21). Learner: OLS polynomial of degree d on a **fixed equispaced design** of n points in [8,18] (stated on page: Fundamentos uses a smoothing spline and random X; the polynomial is the motorcycle deck's learner). Exact, conditional on the design: $E\hat f(x)=b(x)'(B'B)^{-1}B'f$, Var $=\sigma^2 b(x)'(B'B)^{-1}b(x)$ (orthonormal basis via QR on x scaled to [−1,1]); averaged over a 400-point uniform grid. Expected test error = avg bias² + avg var + σ²; expected training error = σ²(1 − (d+1)/n) + ‖(I−H)f‖²/n.

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| Degree | d | polynomial order (flexibility) | 0 – min(15, n−2) | 1 | 3 | — | motorcycle deck | fitted mean, band, marker on curves |
| Training size | n | design points | 10–200 | 1 | 30 | — | Fundamentos slide 21 | band width, variance curve |
| Noise sd | σ | irreducible noise | 0.5–15 | 0.5 | 4 | thousand R$/yr | Fundamentos slide 21 | band, variance and error floor |

Panels: (1) f, E f̂ and ±2 sd band over x; (2) avg bias², avg variance, test and training error vs d (0 … min(15, n−2)), current and optimal d marked. Answer read-out: **expected test error** and the optimal degree.

### L02-b `Notas/L02/companions/companion-gaussian-discriminant.html` — "The Two-Gaussian Classifier"
Model: $x\mid y=k\sim N(\mu_k,\sigma_k^2)$, priors $\pi_1,\pi_2=1-\pi_1$, costs $c_{21}$ (allocate to 2 | truly 1), $c_{12}$; Bayes rule allocates to 1 iff $h(x)=\log p_1(x)-\log p_2(x)>\log\frac{\pi_2c_{12}}{\pi_1c_{21}}$; regions from the quadratic $h$ (one or two cut-offs, or none); error probabilities by $\Phi$. Source: `logisticregression-discriminantanalysis.pdf`, discriminant part (Gaussian example μ1 = 1, μ2 = 5, σ1 = 6, σ2 = 2.5; equal-variance case σ = 6; unequal costs slide); I §4.4.

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| Mean, class 1 | μ1 | | −5–10 | 0.1 | 1 | — | deck example | density, cut-offs |
| Mean, class 2 | μ2 | | −5–10 | 0.1 | 5 | — | deck example | density, cut-offs |
| SD, class 1 | σ1 | | 0.5–10 | 0.1 | 6 | — | deck example | shape; quadratic vs linear |
| SD, class 2 | σ2 | | 0.5–10 | 0.1 | 2.5 | — | deck example | shape |
| Prior, class 1 | π1 | | 0.01–0.99 | 0.01 | 0.50 | — | ML rule = equal priors | threshold |
| Cost ratio | c21/c12 | relative cost of missing class 1 | 0.1–10 (log slider; 1 exactly reachable) | — | 1 | — | deck "unequal costs" | threshold |

Panels: (1) π_k p_k(x) with allocation regions shaded and cut-offs marked; (2) P(y = 1 | x) with the cost-adjusted threshold. Answer read-out: **total misclassification probability** π1 p21 + π2 p12 (and expected cost). Landmark: σ1 = σ2 with equal priors and costs → single cut-off at (μ1+μ2)/2.

Companion checks: `Notas/LNN/companions/check_companions.py` — Python recomputation at three control vectors (both ends + default) compared with the page's JS run under `node` (stub-DOM harness; see `Aula/class-05-06/` companions' history in `.agent/notes/class-01.md`). Pages are **local files**, not published.

## Wiring and verification (lead)
- Merge `figures/_part_*.py` → `make_figures.py`; run; every embedded PNG exists.
- `Notas/00-index.md`; `Map/study-guide.md` `- **Notes:**` lines under Classes 1 and 2.
- Link checker script over `Notas/` (wiki-links and relative links).
- No exercise statements reproduced.
