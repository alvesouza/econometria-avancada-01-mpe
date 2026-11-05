# Notes for Class 8 (L08) — univariate time series — plan (2026-10-25)

Spec: `.claude/commands/notes.md` (binding) and `.claude/commands/companion.md` Steps 2–6.
Design copied from `Notas/L01/`, `Notas/L02/`, plan `.agent/plans/notas-L01-L02.md` (conventions
section there applies verbatim). Shared plan: `.agent/plans/all-units-study-set.md`.

**Step 0 answers (given by the lead, not asked):** Depth **Full** (every step, U/C/G, all support
notes) · Math ↔ theory **Equation-led** · Graphs **Model curves, 8 figures, exact expressions,
comparative statics in the key parameter** · Companions **yes, 2** · PDF **yes**
(`python -I ~/.claude/commands/templates/notes_pdf.py Notas/L08`). Status **taught**.

## Shared facts (do not re-derive)

- Sources: `Aula/class-08/materials/` — `ar-ma.pdf` (52 slides; pp. 1–17 are L01-07's AR(1)
  review, pp. 18–52 are new here), `unitroot.pdf` (38), `seasonal.pdf` (28), `bayes-garch.pdf`
  (22), and the Rmd pages `ar-ma.html`, `ar2-forecast.html`, `unitroot.html`,
  `airpassengers-seasonalmodels.html`, `garchmodeling.html`, `sp500-gaussian-student-SV-models.html`,
  `GARCH11-SVar1.html`, `garch-sv-petrobras.html`. Text extracts (pdftotext / tag-stripped) are in
  the scratchpad `…/scratchpad/L08/*.txt`. The slide PDFs lose Greek letters in extraction: take
  formulas from Tsay at the cited page.
- Book pages opened in this session (PDF = printed + offset; T +27, W +24):
  T §2.4.1 AR(2)/AR(p) pp. 40–46 (eqs. 2.12–2.15, Ex. 2.1 GNP pp. 42–45, Fig. 2.4 p. 43);
  §2.4.2 PACF, AIC/BIC pp. 46–49 (eq. 2.16, Table 2.1 p. 47); §2.4.3–2.4.4 R², forecasting
  pp. 53–57 (Table 2.2); §2.5 MA pp. 57–64 (eqs. 2.17–2.24); §2.6 ARMA pp. 64–71 (eqs.
  2.25–2.34, Table 2.4 EACF); §2.7 unit roots pp. 71–81 (eqs. 2.35–2.40, Ex. 2.2 GDP, S&P 500);
  §2.8 seasonal pp. 81–90 (eqs. 2.41–2.42, Ex. 2.3 J&J, Ex. 2.4 Decile 1 January effect);
  §2.11 long memory pp. 101–103 (eqs. 2.52–2.53); exercises pp. 104–106.
  T Ch. 3: §3.1–3.3 pp. 110–115; §3.4 ARCH pp. 115–131 (eqs. 3.5–3.13, Ex. 3.1 Intel, Ex. 3.2);
  §3.5 GARCH pp. 131–140 (eqs. 3.14–3.21, Ex. 3.3 S&P 500, Table 3.1, two-pass p. 140);
  §3.6 IGARCH pp. 140–142 (eq. 3.22); §3.7 GARCH-M p. 142 (eq. 3.23); §3.8 EGARCH pp. 143–148
  (eqs. 3.24–3.25, forecasting p. 148); §3.9 TGARCH p. 149 (eqs. 3.34–3.35); §3.12 SV pp. 153–154
  (eq. 3.40, JPR moments p. 154); §3.13 LMSV p. 154 (eq. 3.41); §3.16 kurtosis pp. 165–166;
  exercises pp. 168–171. T §12.7 SV by MCMC pp. 636–643 (eqs. 12.20–12.27, Ex. 12.3).
  W §10.5e seasonality pp. 336–338; W §11.1 pp. 345–348 (eqs. 11.1–11.4); W §12.6 pp. 391–396
  (eqs. 12.46–12.50, Ex. 12.8); W §18.2–18.3 pp. 574–580 (eqs. 18.17–18.30, Tables 18.2–18.3,
  Exs. 18.2–18.4).
- Practice list (number and printed page only): T 2.1, 2.2, 2.3 (p. 104), 2.4, 2.5, 2.6
  (p. 105); W 18.C13 (p. 604); T 3.3, 3.4 (p. 168), 3.6 (p. 169), 3.11, 3.12 (p. 170), 3.14
  (p. 171); W 12.4 (p. 397). Solutions are built in parallel by another agent at
  `Listas/lista-L08-book-exercises.*` — cite that path in code format (not a link: it may not
  exist yet when the link checker runs).
- Data on disk (read-only, owned by the exercise agent): `Listas/data/` holds Tsay files
  (`m-deciles08.txt`, `d-gmsp9908.txt`, `d-ibm3dx7008.txt`, …). AirPassengers (144 values) is
  printed on `seasonal.pdf` slide 17 — embedded in code, sum 40363.
- Python only (numpy, scipy, statsmodels; no `arch`, no PyMC). GARCH MLE: `scipy.optimize` with
  the variance recursion as `scipy.signal.lfilter([1],[1,-β], ω+α a²_{t-1})`. SV: simulation and a
  NumPy sampler only.
- Rules packs `rules/04_arima_raiz_unitaria.md` and `rules/05_espaco_estados_volatilidade.md` are
  **placeholders** (no signed comparative statics to check against); signs come from Tsay.
- Already in L01 (link, never repeat): stationarity, ACF, Ljung–Box (IBM Q(30) = 38.241, squared
  182.12), white noise, linear series and ψ-weights, AR(1) moments/ACF/estimation/equilibrium law,
  random walk V = tσ², AR(p) as regression, VAR(1) → `Notas/L01/L01-07-ar-var-review.md`
  (its equations (1)–(26)).

## Numbers fixed for the whole unit (computed 2026-10-25, scratchpad `nums.py`, `air.py`, `garch.py`)

| Quantity | Value | Source |
|---|---|---|
| AR(2) φ = (1.75, −0.80): complex roots, modulus of solutions 1.1180, cycle k = 30.09; ρ1 = 0.9722, ρ2 = 0.9014; γ0 = 50.704σ², sd 7.1207 | ar-ma.pdf slides 20–22; ar2-forecast.html (sd 7.12069) |
| AR(2) φ = (0.90, 0.05): real solutions 1.0499 and −19.05; ρ1 = 0.9474; γ0 = 9.7812, sd 3.1275 | slides 20–22 |
| ar2-forecast: y_n = −5.487150, y_{n−1} = −3.508837; E(1..4) = −6.7954, −7.5023, −7.6927, −7.4603; V(1..4) = 1, 4.0625, 9.1814, 15.7318; ψ = 1, 1.75, 2.2625, 2.5594 | page, recomputed |
| GNP AR(3) (2.15): factor (1+0.521B)(1−0.869B+0.274B²); k = 10.62 quarters (Tsay), 10.656 from R's unrounded roots 1.590253 ± 1.063882i, modulus 1.913308; mean 0.0077 → φ0 = 0.0047355 | T pp. 43–45 |
| Tsay Fig. 2.4(b) φ = (0.6, −0.4): disc −1.24, k = 5.836 | T p. 42 |
| DF t, constant, T = 250, 20 000 seeded reps (seed 2026): quantiles −3.45, −3.16, −2.87, −2.58 (W Table 18.2: −3.43, −3.12, −2.86, −2.57); P(t < −1.645 \| H0) = 0.465 | scratch MC |
| ADF GDP: −1.701 (p 0.4297, S-Plus, Tsay) / −1.6109 (p 0.4569, R fUnitRoots, slides "−1.61, 0.45") / −0.37047 (p 0.9872, `tseries::adf.test`, includes a trend, site page); S&P 500: −1.998 (p 0.602), site page `adf.test(sp5,k=2)` −2.0179 (p 0.5708) | T pp. 78–81; unitroot.html |
| ARFIMA ρ1 = d/(1−d): d = 0.1 → 0.111, 0.25 → 0.333, 0.4 → 0.667 | T p. 102 |
| Airline J&J (θ, Θ) = (0.678, 0.314), s = 4: ρ1 = −0.4645, ρ4 = −0.2858, ρ3 = ρ5 = 0.1328 | T p. 85 |
| AirPassengers airline on log data, statsmodels SARIMAX: n = 96 → (−0.3944, −0.6133), llf 148.76, AIC −291.52, BIC −284.26 (slide: −0.3941, −0.6129, BIC −284.27); n = 108 → (−0.3876, −0.5886), BIC −336.92 (page −0.3864, −0.5885, −336.93) and BIC-best of the 16 = (0,1,1)(0,1,1); n = 144 → (−0.4017, −0.5571), AIC −483.39 (slide −0.4018, −0.5569, −483.4). Out-of-sample 1958–60 RMSE: airline 36.6 vs trend+11 dummies (log) 63.3 | seasonal.pdf, airpassengers page |
| Airline AirPassengers ACF of w (θ, Θ) = (0.3864, 0.5885), s = 12: ρ1 = −0.3362, ρ12 = −0.4371, ρ11 = ρ13 = 0.1470 | derived |
| Intel ARCH(1) (3.12): α0 = 0.0111, α1 = 0.3560; uncond. sd √(0.0111/0.644) = 0.1313 (Tsay prints 0.1315); kurtosis 3(1−α²)/(1−3α²) = 4.227 | T p. 125 |
| Tsay Ex. 3.3 GARCH(1,1) (3.19): α0 = 0.000086, α1 = 0.1216, β1 = 0.8511; α+β = 0.9727 (**Tsay prints 0.9772 on p. 137: transposed digits**); uncond var 0.003150 (Tsay 0.00314), sd 0.0561 (Table 3.1 ∞: 0.0560); half-life of variance ln 0.5/ln 0.9727 = 25.04 months; Gaussian kurtosis 6.654 (excess 3.654) | T pp. 136–138 |
| Petrobras 2000–2021 (garchmodeling.html, n = 5167): ARCH(1) ω = 0.00070027, α = 0.36979 (uncond sd 0.0333); GARCH(1,1) normal ω = 2.255e−5, α = 0.10317, β = 0.87681 → persistence 0.97997, uncond sd 0.03356, half-life 34.3 days, excess kurtosis 3.48; GARCH-t ν = 7.04, α = 0.07429, β = 0.90947 → persistence 0.98376, half-life 42.3; GJR (fGarch `leverage=TRUE, delta=2`, which is the **APARCH form** σ²_t = ω + α(|a_{t−1}| − γa_{t−1})² + βσ²_{t−1}, not the page's indicator formula) α = 0.09234, γ = 0.20835, β = 0.88178 → GJR-equivalent α(1−γ)² = 0.05787 for good news, α(1+γ)² = 0.13483 for bad news, indicator coefficient 4αγ = 0.07696, persistence α(1+γ²) + β = 0.97813; T-GARCH (δ = 1) α = 0.09641, γ = 0.34588, β = 0.90265; APARCH δ = 1.436, γ = 0.2713; EGARCH ω = −0.15392, α = −0.05549, β = 0.97741, γ = 0.18138 | page |
| Petrobras 2000–2025 (garch-sv-petrobras.html, simple returns, n = 6363): ARCH α = 0.33114; GARCH normal (1.8817e−5, 0.081406, 0.89841) persistence 0.97982; GARCH-t (1.1404e−5, 0.059208, 0.92773, ν 6.234) persistence 0.98694 | page |
| GARCH11-SVar1 (standardized PBR returns): ML GARCH-t (0.014364, 0.073478, 0.910218, ν 7.026); Bayes GARCH-t posterior means (0.019209, 0.085027, 0.894024, ν 6.984); SV-t posterior means μ = −0.419, φ = 0.9842, σ = 0.1388, ν = 12.13. Lag-1 ACF of a²: GARCH 0.2037 vs SV (Gaussian ε) 0.1828; SV var of h 0.6146, kurtosis (Gaussian ε) 5.547 | page; derived (T p. 154 formula) |
| Tsay Ex. 12.3 SV posterior: μ = 0.409, α0 = 0.454, α1 = 0.837, σv² = 0.086 → μh = 2.785, σh² = 0.2872, E(a²) = 18.71 (%²), sd 4.33%, kurtosis 3e^{σh²} = 3.998 | T p. 642, formula p. 154 |
| bayes-garch.pdf (Petrobras 2001–2013; prior from n0 = 1506 days, posterior on n = 1760): M0 σ² ~ IG(5, 4·m_{r̃²}), m_{r̃²} = 0.0006617694; M1 μ ~ N(0.00112605, 100·0.0006609406/1505), σ² ~ IG(5, 4·0.0006609406); M2 AR(1) on log prices, OLS (a, b, s) = (0.00054516, 1.00033425, 0.02569926), (s_a, s_b) = (0.00184913, 0.00099338); M3 GARCH(1,1)-t, Pr(α1+β > 1 \| data) = 0.0034; bayesGARCH priors N2(0, 1000 I)·1{α>0}, N(0, 1000)·1{β>0}, ν − 2 ~ Exp(λ = 0.01), δ = 2 | slides 6–20 |

Errata found (to report in the map): Tsay p. 137 "0.9772" for 0.1216 + 0.8511 = 0.9727;
`ar2-forecast.html` writes Var(y_t) = ((1−φ2)/(1+φ2))·{(1−φ2)² − φ1²}σ² (the braces must divide;
its own R code divides and prints 7.12069) and labels the h = 4 lines "E(y_{n+3}…)", with a stray
"2φφ2²" for "2φ1φ2²"; `GARCH11-SVar1.html` §3 is titled "Gaussian errors" but fits
`cond.dist="std"`, and its SV table prints a "p-value" of 1.9987 for μ (2(1−Φ(t)) with t < 0);
`sp500-gaussian-student-SV-models.html` lists SVtl with ε ~ N(0,1) (should be t_ν); garchmodeling's
glossary writes σ²_t = ω + α ε²_{t−1} with ε the standardized error (should be y_{t−1} = σ_{t−1}ε_{t−1})
and its legend "GARCH t(3)" is the ν = 7 fit; its T-GARCH and GJR formulas use an indicator I(ε<0) but `garchFit(..., leverage=TRUE)` estimates the APARCH parametrisation α(|ε| − γε)^δ, so the printed gamma1 is APARCH's γ (GJR-equivalent indicator coefficient 4αγ = 0.0770 for δ = 2); the unit-root deck quotes ADF −1.61/0.45 while the
site page's `tseries::adf.test` prints −0.37/0.987 (trend included).

## Conventions every note follows

As in `.agent/plans/notas-L01-L02.md` "Conventions every note follows", with `date: 2026-10-25`,
`status: taught`, tags `lecture-08`. Figures embedded as `![alt](figures/L08-<slug>.png)` + italic
caption + one reading paragraph. Equations numbered per note, `(1)`, `(2)`…; cross-note citations
"L08-06 (9)"; L01 equations cited as "L01-07 (11)". Tsay's MA sign convention r_t = c0 + a_t − θ1 a_{t−1}
throughout (R and statsmodels print +θ: say so where a printed number is used). GARCH notation:
a_t = σ_t ε_t, σ²_t = α0 + α1 a²_{t−1} + β1 σ²_{t−1} (Tsay); the site pages write ω, α1, β1 and h_t
— map once per note.

## L08 — note list

| # | File | Covers (sources) | Settles | Figures |
|---|---|---|---|---|
| 00 | `L08-00-map.md` | — | front door | — |
| 01 | `L08-01-ar2-arp-cycles-identification.md` | ar-ma.pdf slides 18–37 (AR(2) moments, stationarity region code, two φ sets, theoretical vs empirical ACF at n = 10 000…200, GNP AR(3), AR(p), PACF, AIC, BIC); ar-ma.html (GNP output, roots, k = 10.656); T §2.4.1–2.4.2 pp. 40–49 | AR(2) mean, Yule–Walker (2.13), γ0 formula; triangle φ2 < 1 − φ1, φ2 < 1 + φ1, φ2 > −1; complex iff φ1² + 4φ2 < 0; k = 2π/cos⁻¹[φ1/(2√−φ2)]; GNP 10.62 quarters; AR(p) characteristic equation; PACF cut-off with SE 1/√T; AIC/BIC and Table 2.1 (AIC → 9, BIC → 1) | `L08-ar2-triangle-acf` |
| 02 | `L08-02-forecasting-ma-arma.md` | ar-ma.pdf slides 38–52 (forecasting, mean reversion, half-life, MA(1)/MA(q), ACF of MA(1)/(2), estimation, MA forecasts, summary); ar2-forecast.html (exact h-step distributions + MC); T §2.4.4 pp. 54–57, §2.5 pp. 57–64, §2.6 pp. 64–71; W §11.1 (11.1) p. 346 | ℓ-step forecast recursion; e_h(ℓ) = Σψ_i a; Var = σ²Σψ²_i (2.34) → γ0; the page's E/V for h = 1..4 and the 7.12 limit; MA(q) ACF cut-off, |ρ1| ≤ ½, invertibility; conditional vs exact likelihood; ARMA(1,1) ACF; three representations; identification table | `L08-identification-acf-pacf`, `L08-ar2-forecast-fan` |
| 03 | `L08-03-unit-roots-dickey-fuller.md` | unitroot.pdf slides 1–31; unitroot.html; T §2.7 pp. 71–81; W §18.2–18.3 pp. 574–580 | RW forecasts and Var = ℓσ²; drift = slope (3M 0.0103, σ 0.0637); trend-stationary vs RW with drift; constant term's three meanings; ARIMA(p,1,q), differencing; DF t ratio and its non-normal law; ADF regression (2.40) and the AR(3) reparametrisation; critical values; GDP and S&P 500 examples incl. the three printed ADF numbers; spurious regression (66.2% / 84.7%) | `L08-unit-root-bands-df` |
| 04 | `L08-04-long-memory-arfima.md` | unitroot.pdf slides 32–38; T §2.11 pp. 101–103; T §3.13 (3.41) p. 154 (LMSV, named) | (1−B)^d binomial expansion; ψ_k, π_k; ρ_k product formula, ρ1 = d/(1−d), ρ_k ~ k^{2d−1}; PACF d/(k−d); spectrum ω^{−2d}; ARFIMA; why |returns| look long-memory | `L08-long-memory-acf` |
| 05 | `L08-05-seasonal-airline-model.md` | seasonal.pdf slides 1–28; airpassengers-seasonalmodels.html; T §2.8 pp. 81–90; W §10.5e pp. 336–338 | seasonal differencing; airline model (2.41), Var(w) and ACF at lags 1, s−1, s, s+1; multiplicative vs non-multiplicative (2.42); SARIMA(p,d,q)×(P,D,Q)_s; ARIMA(1,1,1)×(1,1,1)12 = ARMA(26,13) expansion; J&J fit; Decile 1 (exact vs conditional likelihood, January dummy 0.1253); AirPassengers: BIC choice, fits, RMSE(h) study, deterministic trend + dummies vs airline | `L08-airline-acf` |
| 06 | `L08-06-arch-garch.md` | garchmodeling.html (ARCH, GARCH); garch-sv-petrobras.html (ARCH, GARCH, GARCH-t); T §3.1–3.6 pp. 110–142, §3.16 pp. 165–166; W §12.6 pp. 391–396 | volatility facts; mean/volatility equations (3.2)–(3.4); ARCH tests (McLeod–Li, Engle LM); ARCH(1) mean, variance, 4th moment, kurtosis; conditional likelihood (normal, t (3.7)–(3.8)); GARCH as ARMA for a² (3.15); GARCH(1,1) unconditional variance, kurtosis, forecasts (3.17); Intel, S&P 500, Petrobras numbers; IGARCH (3.22) and RiskMetrics; half-life of variance | `L08-garch-persistence-kurtosis` |
| 07 | `L08-07-garch-family-asymmetry-tails.md` | garchmodeling.html (TS-GARCH, T-GARCH, GJR, APARCH nesting, EGARCH, t, skew-t, GED, ν = 7 fixed); T §3.4 (3.7)–(3.10) pp. 121–122, §3.7–3.9 pp. 142–149 | leverage and the news-impact curve; GJR/TGARCH (3.34); EGARCH g(ε) (3.24), E|ε| = √(2/π); APARCH special cases; GARCH-M (3.23); non-Gaussian innovations and Tiao's kurtosis formula; reading the Petrobras table (log-lik 10672 → 11151 → 11174 → 11292) | `L08-news-impact-sv-memory` (left panel) |
| 08 | `L08-08-stochastic-volatility.md` | sp500-gaussian-student-SV-models.html (iid Gaussian vs t, SV/SVt/SVl/SVtl, stochvol priors); GARCH11-SVar1.html (SV-t vs GARCH); garch-sv-petrobras.html (SV); T §3.12 pp. 153–154, §12.7 pp. 636–643 | SV-AR(1) in Tsay's and stochvol's notation; moments (JPR) incl. kurtosis 3e^{σh²}, ACF of a²; why the likelihood is an n-dimensional integral; Gibbs: β | H, h_t | rest (12.23), (α, σv²) | H; Tsay Ex. 12.3; GARCH vs SV comparison on Petrobras | `L08-news-impact-sv-memory` (right panel) |
| 09 | `L08-09-bayesian-garch.md` | bayes-garch.pdf (22 slides); GARCH11-SVar1.html §4–4.1; T §12.7 intro p. 637 for the MCMC logic | M0 conjugate IG update (worked), M1 and M2 Gibbs, prior elicitation from a training sample; GARCH(1,1)-t with ϱ = (ν−2)/ν scaling; bayesGARCH priors (truncated normals, translated exponential); why no conjugacy → MH; Pr(α1+β > 1) = 0.0034; Bayes vs ML on PBR | — |
| 10 | `L08-10-formulas.md` | all | spec (COURSE.md items i–v, class-plan goals) mapped; definitions/results; every number | — |
| 11 | `L08-11-pitfalls.md` | all | 15+ confusions with counterexamples; original 30-item V/F (macro-1 style, `rules/00_estilo_avaliacao.md`) | — |
| 12 | `L08-12-python.md` + `L08_python_checks.py` | all | AR(2) moments/roots/forecasts; PACF by Durbin–Levinson vs statsmodels; DF MC; ARFIMA ACF; airline fit vs the slides; Decile-1 January dummy vs Tsay; GARCH MLE (normal, t) by scipy on simulated and S&P data; SV simulation moments vs formulas; conjugate M0 update; random-walk MH for GARCH-t | — |

Section-note writers: equations numbered from (1) in each note; give each worked example the
arithmetic in view, using the numbers in the table above (do not re-derive them).

## Figures (`Notas/L08/figures/make_figures.py`, one script, asserts per figure)

| Figure | Content (exact expressions) | Note |
|---|---|---|
| `L08-ar2-triangle-acf` | left: stationarity triangle, parabola φ2 = −φ1²/4, points (1.75, −0.8), (0.9, 0.05), GNP factor (0.869, −0.274), Tsay Fig. 2.4(b) (0.6, −0.4), with k labels; right: theoretical ACF of the two slide models to lag 100 | 01 |
| `L08-identification-acf-pacf` | ACF and PACF (Durbin–Levinson on the exact ACF) of AR(2) (0.6, −0.4)… AR(1) φ = 0.8, MA(1) θ = 0.6, ARMA(1,1) (0.8, 0.4), lags 1–12 | 02 |
| `L08-ar2-forecast-fan` | ar2-forecast page: E(y_{n+h}) and 5–95% bands from ψ weights, h = 1..50, converging to 0 ± 1.645·7.12 | 02 |
| `L08-unit-root-bands-df` | left: ±2 sd forecast bands vs ℓ for AR(1) φ = 0.9, RW, RW with drift (3M μ = 0.0103, σ = 0.0637) vs trend-stationary; right: DF t density by seeded MC (T = 250) vs N(0,1), critical −2.86 vs −1.645 | 03 |
| `L08-long-memory-acf` | ρ_k for d = 0.1, 0.25, 0.4 vs AR(1) with the same ρ1, linear and log–log (slope 2d−1) | 04 |
| `L08-airline-acf` | exact ACF of w_t for J&J (s = 4) and AirPassengers (s = 12) fits | 05 |
| `L08-garch-persistence-kurtosis` | left: σ_h(ℓ) term structure (Tsay Ex. 3.3, PBR normal, IGARCH) ; right: (α1, β1) plane with α+β = 1, Gaussian 4th-moment boundary 1 − 2α² − (α+β)² = 0 and the t(7) boundary, fitted points | 06 |
| `L08-news-impact-sv-memory` | left: news-impact σ²_t vs a_{t−1} for PBR GARCH, GJR, EGARCH (at unconditional σ); right: ACF of a²_t, GARCH(1,1) ρ1 = α(1−αβ−β²)/(1−2αβ−β²), ρk = (α+β)^{k−1}ρ1 vs SV corr = (e^{σh²φ^k} − 1)/(3e^{σh²} − 1), PBR calibrations | 07, 08 |

## Companions (control contracts)

### L08-a `Notas/L08/companions/companion-ar2-dynamics.html` — "The AR(2) Triangle"
Model: y_t = φ1 y_{t−1} + φ2 y_{t−2} + ε_t, ε ~ N(0, σ²) (ar2-forecast.html; ar-ma.pdf slides 18–22;
T §2.4.1 pp. 40–46). Roots of 1 − φ1x − φ2x² = 0; stationary iff both |x| > 1 ⇔ triangle;
complex iff φ1² + 4φ2 < 0, k = 2π/cos⁻¹(φ1/(2√−φ2)); ρ1 = φ1/(1−φ2), ρℓ = φ1ρℓ−1 + φ2ρℓ−2;
γ0 = (1−φ2)σ²/[(1+φ2)((1−φ2)² − φ1²)]; forecasts E_h by the recursion, Var_h = σ²Σ_{j<h}ψ_j².

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| Lag-1 coefficient | φ1 | weight on y_{t−1} | −2.5–2.5 | 0.001 | 1.750 | — | slides 20–22, ar2-forecast | point in triangle, ACF, fan, roots |
| Lag-2 coefficient | φ2 | weight on y_{t−2} | −1.5–1.5 | 0.001 | −0.800 | — | same | same |
| Shock sd | σ | innovation sd | 0.1–5 | 0.1 | 1.0 | — | ar2-forecast (sig = 1) | fan width, γ0 |
| Last value | y_n | forecast origin value | −20–20 | 0.001 | −5.487 | — | ar2-forecast (−5.487150) | fan start |
| Previous value | y_{n−1} | one before | −20–20 | 0.001 | −3.509 | — | ar2-forecast (−3.508837) | fan start |
| Horizon | H | forecast steps | 1–100 | 1 | 50 | periods | ar2-forecast (s = 50) | fan length, read-out at H |

Presets (buttons, exact): slide (1.75, −0.80), slide (0.90, 0.05), GNP factor (0.869, −0.274),
Tsay Fig. 2.4(b) (0.6, −0.4). Panels: (1) triangle with parabola, regions labelled, point; (2) ACF
lags 0–60 (or "no stationary ACF" outside); (3) forecast fan 5/50/95% with the stationary 90% band.
Answer read-out: **stationarity verdict with the root moduli** (and cycle length when complex).
Others: ρ1, ρ2, γ0 and sd, E/V at h = 1..4 (page reproduces −6.795, −7.502, −7.693, −7.460 and
1, 4.063, 9.181, 15.732), sd at H vs stationary sd 7.121. Boundaries: on an edge the page says
"unit root" and γ0 = ∞, never NaN.

### L08-b `Notas/L08/companions/companion-garch-volatility.html` — "The Volatility Dial"
Model: a_t = σ_t ε_t, σ²_t = α0 + α1 a²_{t−1} + β1 σ²_{t−1}; ε iid N(0,1) or standardized t_ν
(T eqs. 3.14–3.17, 3.22; §3.16 pp. 165–166; garchmodeling.html). σ²_h(ℓ) = σ²∞ + (α1+β1)^{ℓ−1}(σ²_h(1) − σ²∞)
with σ²∞ = α0/(1−α1−β1); IGARCH: σ²_h(ℓ) = σ²_h(1) + (ℓ−1)α0; half-life ln 0.5/ln(α1+β1);
Ka(g) = 6α1²/(1 − 2α1² − (α1+β1)²); t: Ka = [6 + (ν+1)Ka(g)]/[ν − 4 − Ka(g)] when
1 − 2α1²(ν−1)/(ν−4) − (α1+β1)² > 0.

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| ARCH coefficient | α1 | reaction to last squared shock | 0–0.5 | 0.0001 | 0.1216 | — | T (3.19) p. 136 | point in plane, kurtosis, persistence |
| GARCH coefficient | β1 | carry-over of last variance | 0–0.9999 | 0.0001 | 0.8511 | — | T (3.19) | same |
| Constant | α0 | variance floor | 0.0001–5 | 0.0001 | 0.8600 | %² per period | T (3.19): 0.000086 = 0.86 %² | σ∞, term-structure level |
| 1-step volatility | σ_h(1) | forecast at the origin | 0.5–20 | 0.01 | 5.36 | % per period | T Table 3.1 p. 138 | term-structure start |
| Innovation tails | ν (or Normal) | standardized t df; toggle Normal | 4.1–30 | 0.1 | Normal | — | T (3.7), §3.16 | kurtosis read-out, t-boundary curve |
| Horizon | L | last forecast horizon plotted | 1–500 | 1 | 60 | periods | — | term-structure length, σ_h(L) |

Presets: Tsay Ex. 3.3 (default), Tsay IGARCH (α1 0.1941, β1 0.8059, α0 1.19 %²), PBR 2000–2021
normal (0.10317, 0.87681, α0 0.2255 %², σ_h(1) at σ∞), PBR GARCH-t (0.07429, 0.90947, 0.15546 %²,
ν 7.04). Panels: (1) σ_h(ℓ) vs ℓ with σ∞ line (or IGARCH straight line in variance); (2) (α1, β1)
plane with α+β = 1, Gaussian and t kurtosis boundaries, point. Answer read-out: **half-life of a
volatility shock (periods) with the persistence α1+β1**. Others: σ∞, σ_h(L), Ka (or "infinite
4th moment"), regime word (covariance-stationary / IGARCH / explosive). Landmarks: α+β = 1 exactly
reachable (0.1941 + 0.8059), defaults reproduce Table 3.1 to ±0.0001.

Check: `Notas/L08/companions/check_companions.py` (pattern of `Notas/L01/companions/check_companions.py`):
Python read-outs at three vectors (low ends, default, high ends) + degenerate vectors vs the page's
`<script id="model">` under node; stub-DOM sweep (no NaN/undefined), Reset restores defaults.

## Execution

Lead (this agent): plan, `make_figures.py`, map, formulas, pitfalls, python note + script, PDF,
verification. Section notes 01–09 and the two companions written by forks of this agent that share
this plan; the lead reads and wires their output.

## Verification
- `python Notas/L08/figures/make_figures.py` (asserts); every embedded PNG exists.
- `python tools/check_note_links.py Notas/L08` clean.
- `python Notas/L08/companions/check_companions.py` passes.
- `python Notas/L08/L08_python_checks.py` ends `ALL L08 CHECKS PASSED`.
- `python -I ~/.claude/commands/templates/notes_pdf.py Notas/L08`; no `Missing character`;
  `pdffonts` no Type 3.
- Row for `Notas/00-index.md` reported to the lead (not edited here).
