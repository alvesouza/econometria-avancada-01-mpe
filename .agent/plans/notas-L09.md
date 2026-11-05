# Notes for Class 9 (L09): Multivariate time series — plan (2026-10-25)

Spec, binding: `.claude/commands/notes.md` (+ `.claude/commands/companion.md` Steps 2–6). Shared plan:
`.agent/plans/all-units-study-set.md`. Design copied from `Notas/L01/` and `.agent/plans/notas-L01-L02.md`.
Step 0 answered by the lead: **Full depth · equation-led · model curves (4–8 figures, exact expressions,
comparative statics) · 1–2 companions · PDF yes.** Status **taught** (slides on disk).

## Sources (read, with the pages actually opened)

- Slides: `Aula/class-09/materials/BVAR-part11.pdf` (48 slides, "Lecture 4: Bayesian VAR") — VAR set-up pp. 4–7,
  forecast p. 8, stationarity p. 9, VMA p. 10, FEVD p. 11, IRF p. 12, simulated VAR(2) pp. 13–17, Zivot–Wang
  example pp. 18–21, Minnesota pp. 22–24, other priors pp. 25–26, K&K example pp. 27–30, SVAR pp. 31–37,
  VAR-GARCH pp. 38–39, VAR-SV p. 40, TVP-VAR-SV pp. 41–44, dimensionality p. 45.
  `BVAR-part2.pdf` (67 slides, "Lecture 5: BVAR Extensions") — variable selection/SSVS pp. 3–13, factor analysis
  pp. 14–37, FSV pp. 38–43, spatial DFM pp. 44–49 (named only), large BVAR forecasting p. 50, many predictors /
  FAVAR pp. 51–55, Bańbura et al. pp. 56–60, large TVP-BVAR p. 61.
- Site pages (R, reference): `VAR-Example.html` (VAR(3) UK/US/CA, OLS step by step, MTS output, VARorder, FEVD,
  IRF); `sv-fsv-US-BR.html` (SV, FA, FSV on 6 stocks); `wti-sp500-timevaryingcovariance.html` (FSV vs DCC, GARCH-t).
- Books (offset T +27, G +15): T §8.2.1 (pp. 399–401, Ex. 8.3), §8.2.3–8.2.5 (pp. 403–417), §9.1–9.2 (pp. 468–476),
  §10.1 (pp. 506–507), §10.3.1 (p. 516), §10.4.3 (pp. 531–532), §10.6 (p. 543), §11.1 (pp. 558–563), §11.3.1
  (pp. 577–578); G §9.1 (pp. 134–137), §10.3 (pp. 161–164). Exercise pages: T 8.1 p. 462, 8.2 pp. 462–463,
  8.3–8.7 p. 463, T 9.7 p. 503, T 10.1–10.6 p. 554, G 10.4 p. 167.
- L01 VAR(1) review is linked, not repeated: `Notas/L01/L01-07-ar-var-review.md` §9.

## Notes

| # | File | Covers | Settles | Figures |
|---|---|---|---|---|
| 00 | `L09-00-map.md` | — | front door | — |
| 01 | `L09-01-var-p-estimation-forecasting.md` | part11 pp. 4–9, 45; T §8.2.3–8.2.4; G §9.1; VAR-Example §2–3.1 | VAR(p) as multivariate regression; OLS = conditional MLE equation by equation; vec/Kronecker form; companion form and the eigenvalue test; h-step forecast and its MSE; order selection; parameter counts | `L09-companion-eigenvalues` |
| 02 | `L09-02-vma-irf-fevd.md` | part11 pp. 10–12, 17, 20–21; T §8.2.5; VAR-Example §3.2–4 | Ψ recursion; IRF; Cholesky-orthogonalised IRF (Tsay IBM/SP5 numbers); FEVD (reproduces the MTS table) | `L09-irf-var3-gdp`, `L09-fevd-var3-gdp` |
| 03 | `L09-03-structural-var.md` | part11 pp. 31–37; T §8.2.1 Ex. 8.3 | SVAR ↔ reduced form; order condition $q(q-1)/2$; recursive identification and its ordering dependence; counting zeros in Illustrations 1–2 | `L09-cholesky-ordering` |
| 04 | `L09-04-bvar-minnesota-ssvs.md` | part11 pp. 13–16, 22–30; part2 pp. 3–13, 50, 56–58, 60 | Minnesota prior and its closed-form posterior (Σ fixed, diagonal); λ comparative statics; other priors; SSVS; large BVAR evidence | `L09-minnesota-shrinkage` |
| 05 | `L09-05-factor-models-favar.md` | part2 pp. 14–37, 51–55, 59; T §9.1–9.2 | factor model, Ω = ββ′+Σ, rotation and identification, bound on k, full conditionals, exchange-rate example; FAVAR, RMSFE | `L09-factor-correlation` |
| 06 | `L09-06-tvp-var-sv-state-space.md` | part11 pp. 38–44; part2 p. 61; T §11.1, §11.3.1; G §10.3 | VAR-GARCH, VAR-SV (Uhlig), TVP-VAR-SV (Primiceri); state-space form; Kalman filter; steady-state gain = 1−θ (Tsay Ex. 11.1); discounting | `L09-kalman-gain-snr` |
| 07 | `L09-07-fsv-dcc-covariances.md` | part2 pp. 38–43; T §10.1, §10.3.1, §10.4.3, §10.6; the two site pages | Σ_t = D_tR_tD_t; EWMA; DCC (Engle, Tse–Tsui); FSV and its implied correlation; the WTI/S&P numbers | `L09-dcc-garch-persistence` |
| 08 | `L09-08-formulas.md` | all | spec mapped, results, numbers | — |
| 09 | `L09-09-pitfalls.md` | all | confusions + original V/F (24 items) | — |
| 10 | `L09-10-python.md` + `L09_python_checks.py` | all | reference code with asserts | — |

Scope: SSVS and spatial dynamic factor models are on the slides; SSVS is developed (C, slides only), SDFM named.
Cointegration/ECM (T 8.7(d)–(e)) is outside Class 9 (syllabus note in `Map/class-plan.md`): named only.

## Companions (control contracts)

### L09-a `companions/companion-var-irf-ordering.html` — "The Ordering Dial"
Model: bivariate VAR(1) $r_t=\Phi r_{t-1}+a_t$, $\Sigma=\begin{pmatrix}\sigma_1^2&\rho\sigma_1\sigma_2\\ \cdot&\sigma_2^2\end{pmatrix}$,
$\sigma_1^2=2,\sigma_2^2=1$ fixed (T Ex. 8.3, p. 400). Ψ_h = Φ^h; Θ_h = Φ^h L (L lower Cholesky of Σ in the chosen
order); FEVD share $\omega_{ij}(H)=\sum_{h<H}\Theta_{h,ij}^2/\sum_{h<H}\sum_k\Theta_{h,ik}^2$; eigenvalues of Φ.

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| Own lag, 1 | Φ11 | effect of $r_{1,t-1}$ on $r_{1t}$ | −1.5–1.5 | 0.05 | 0.20 | — | T Ex. 8.3 | IRFs, eigenvalues |
| Cross lag 2→1 | Φ12 | effect of $r_{2,t-1}$ on $r_{1t}$ | −1.5–1.5 | 0.05 | 0.30 | — | T Ex. 8.3 | IRFs, eigenvalues |
| Cross lag 1→2 | Φ21 | effect of $r_{1,t-1}$ on $r_{2t}$ | −1.5–1.5 | 0.05 | −0.60 | — | T Ex. 8.3 | IRFs, eigenvalues |
| Own lag, 2 | Φ22 | effect of $r_{2,t-1}$ on $r_{2t}$ | −1.5–1.5 | 0.05 | 1.10 | — | T Ex. 8.3 | IRFs, eigenvalues |
| Innovation correlation | ρ | corr$(a_{1t},a_{2t})$ | −0.95–0.95 | 0.05 | 0.70 ($=1/\sqrt2$ rounded; Ex. 8.3 exact 0.7071 by button) | — | T Ex. 8.3 | gap between orderings |
| Ordering | — | which variable is first in the Cholesky factor | (1,2) / (2,1) | — | (1,2) | — | T p. 413 | solid vs dashed IRFs, FEVD |

Answer read-out: **FEVD share of $r_1$'s 10-step forecast-error variance due to the second-ordered shock**, both orderings side
by side; also eigenvalue moduli + verdict, impact matrix Θ0. Landmarks: ρ = 0 (orderings coincide), max modulus = 1.
Button "Ex. 8.3 exact" sets ρ = 1/√2.

### L09-b `companions/companion-fsv-correlation.html` — "The Factor-Volatility Dial"
Model: one-factor FSV at a date t: $y_t\mid f_t\sim N(\beta f_t,\Psi)$, $f_t\sim N(0,h_t)$, $\Psi=\mathrm{diag}(\psi_1,\psi_2)$;
$\Sigma_t=h_t\beta\beta'+\Psi$; $\rho_t=\beta_1\beta_2h_t/\sqrt{(\beta_1^2h_t+\psi_1)(\beta_2^2h_t+\psi_2)}$ (part2 pp. 15, 38).

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| Loading 1 | β1 | | −1.5–1.5 | 0.01 | 0.99 | — | part2 p. 22, row 1 | curve, ellipse |
| Loading 2 | β2 | | −1.5–1.5 | 0.01 | 0.90 | — | part2 p. 22, row 3 | curve, ellipse |
| Idiosyncratic var. 1 | ψ1 | | 0–1 | 0.01 | 0.01 | — | part2 p. 22 | curve, ellipse |
| Idiosyncratic var. 2 | ψ2 | | 0–1 | 0.01 | 0.10 | — | part2 p. 22 | curve, ellipse |
| Factor log-variance | λ_t = log h_t | | −6–3 | 0.05 | 0 | — | part2 p. 38; static FA h = 1 | point on curve, ellipse |

Answer read-out: **ρ_t** (0.939 at defaults); also Σ_t entries and the factor share of each variance. Landmarks: λ = 0
(static FA calibration), the half-limit point where ρ is half its h→∞ limit. Degenerate: zero variance → "undefined".

Checks: `companions/check_companions.py` — imports `node`, `fx`, `STUB` from `Notas/L01/companions/check_companions.py`
(reuse), compares Python vs the page's `<script id="model">` at three vectors (both ends + default) plus degenerate ones,
sweeps every control under a stub DOM, asserts no NaN and Reset.

## Verification
`python Notas/L09/figures/make_figures.py`; `python Notas/L09/L09_python_checks.py`;
`python Notas/L09/companions/check_companions.py`; `python tools/check_note_links.py Notas/L09`;
`python -I ~/.claude/commands/templates/notes_pdf.py Notas/L09` (no `Missing character`), `pdffonts` no Type 3.
Lead adds the `Notas/00-index.md` row (not edited here).
