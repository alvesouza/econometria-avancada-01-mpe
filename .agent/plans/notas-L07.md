# Notes for Class 7 (L07) — plan (2026-10-25)

Spec: `.claude/commands/notes.md` (binding) and `.claude/commands/companion.md` Steps 2–6.
Step 0 answered by the lead: **Full depth · Equation-led · Model curves (4–8 figures, exact
expressions, comparative statics in the key parameter) · 2 companions · PDF yes.**
Status **taught** (slides in `Aula/class-07/materials/`). Design copied from `Notas/L01`, `Notas/L02`
and `.agent/plans/notas-L01-L02.md` (conventions section applies verbatim; date 2026-10-25).
Shared plan: `.agent/plans/all-units-study-set.md`. Output only under `Notas/L07/` + this plan.

## Sources read this session

- Slides: `GLM3.pdf` (32 slides: general Ω, known Ω, Ω diagonal Case I h(z,α) with MH + airline
  example, Case II Student-t scale mixture, AR(1) errors "parsimonious Ω", SUR),
  `HLM.pdf` (33 slides: pooled / individual-effects / random-coefficients models, full
  conditionals, airline intercepts, eight schools, dugong growth curve),
  `limiteddependentvariablemodels.pdf` (16 slides: Tobit, data augmentation, linear Tobit,
  truncation-probability example, ordered probit, multinomial probit as SUR),
  `hierarchicalmodel.html` (Rmd: pregnant-women weight gains, I = 68, n = 427; pooled, individual
  and hierarchical regressions; data embedded — ported to Python).
- Books (printed pages opened with pdftotext): G §4.5–4.6 (pp. 50–53), §8.1–8.2 (pp. 111–129),
  exercises p. 132 (8.3, 8.5, 8.6, 8.7), p. 59 (4.6), §9.2–9.3 (pp. 139–149), exercises p. 151
  (9.2, 9.3); W §8.4 (pp. 254–262, eqs. 8.21–8.34, Example 8.6 / Table 8.1 p. 257), §12.3
  (pp. 381–386, eqs. 12.26–12.33, Example 12.4 / Table 12.1 p. 384), §17.1 (pp. 525–535, eqs.
  17.1–17.12, Example 17.1 Tables 17.1–17.2 pp. 533–534), §17.2 (pp. 536–543, eqs. 17.18–17.30,
  Example 17.2 Tables 17.3–17.4 pp. 540–541), §17.4 (pp. 547–553, eqs. 17.36–17.41), §14.2
  (pp. 441–444, eqs. 14.7–14.11); exercises W 12.C2 (p. 397), 12.C10 (p. 399), 17.3 (p. 559),
  17.C2, 17.C3 (p. 561), 17.C9 (p. 562), 14.C5 (p. 454); T §2.9 (pp. 90–93, eqs. 2.43–2.46);
  MS §6.4–6.5 (pp. 215–220, eqs. 6.27–6.30; offset +10), exercises 6.18 (p. 241), 6.21 (p. 242).
- Data: `pip install wooldridge` (allowed by the shared plan) gives MROZ, BARIUM, 401KSUBS, so
  W Tables 8.1, 12.1, 17.1, 17.3 are reproduced, not just cited.

## Notes

| # | File | Covers | Settles | Figures |
|---|---|---|---|---|
| 00 | `L07-00-map.md` | — | front door | — |
| 01 | `L07-01-general-covariance-gls.md` | GLM3 slides 3–15; W §8.4 (pp. 254–262); W Example 8.6 | $y\sim N(X\beta,\sigma^2\Omega)$; $P\Omega P'=I$ turns it into OLS on $(Py,PX)$; GLS = WLS for diagonal $\Omega$; full conditionals with $\Omega^{-1}$; Case I $h(z,\alpha)=\exp(z'\alpha)$ needs MH; FGLS (8.30)–(8.33) = the slide's initial value; airline posterior table; WLS on 401KSUBS (.787, SE .063) | `L07-gls-efficiency` (Var OLS / Var GLS of the slope vs $\alpha_1$) |
| 02 | `L07-02-student-t-errors.md` | GLM3 slides 16–21; G §4.5 (pp. 50–52), §8.1.2 (pp. 114–116) | $t_\nu$ as a scale mixture (derived by integrating $\omega$); full conditionals for $\omega_i,\beta,\sigma^2$; $E(\lambda_i\mid\cdot)=(\nu+1)/(\nu+\varepsilon_i^2/\sigma^2)$ downweights outliers; Exp prior on $\nu$ (P(ν≤10)=0.33, P(ν≥40)=0.20 at ν⁰=25); ν full conditional + MH; Geweke's moment conditions | `L07-t-scale-mixture` (densities, mixing density, weight vs residual for several ν) |
| 03 | `L07-03-ar1-errors.md` | GLM3 slides 22–28; W §12.3 (pp. 381–386); T §2.9 (pp. 90–93) | $\Omega_\rho$ and its inverse; quasi-differencing = GLS; Prais–Winsten vs Cochrane–Orcutt; the "small sin" conditional for ρ (truncated normal) and its inverse-CDF draw; barium PW (2.94, ρ̂ = .293) | `L07-ar1-gls` (ACF; Var ratios OLS/GLS and naive/true vs ρ) |
| 04 | `L07-04-hierarchical-linear-models.md` | HLM.pdf all; hierarchicalmodel.html; G §4.6 (pp. 52–53), §9.3 (pp. 144–149); MS §6.4 (pp. 215–218); W §14.2 (pp. 441–444) as frequentist neighbour | pooled / individual / random-coefficient models; full conditionals; **partial pooling** weight $T V_\alpha/(T V_\alpha+\sigma^2)$; eight schools exact $p(\tau\mid y)$ and shrinkage; pregnant women (pooled −4.526 + 0.476x; individual vs hierarchical); RE θ (14.10) | `L07-eight-schools-shrinkage`, `L07-pregnancy-hierarchical` |
| 05 | `L07-05-tobit.md` | LDV slides 4–10; G §8.2.1 (pp. 117–122); W §17.2 (pp. 536–543), §17.4 (pp. 547–553) | censoring vs truncation; likelihood; Chib (1992) data augmentation; full conditionals; slide example P(y=0)=Φ(−2a/2.062); $E(y\mid x)$, $E(y\mid y>0,x)$, (17.26), (17.30); OLS on censored data attenuates by $P(y>0)$ (Stein); Mroz Tobit (Table 17.3) by MLE and by Gibbs | `L07-tobit-moments` |
| 06 | `L07-06-probit-ordered-multinomial.md` | LDV slides 11–15; G §8.2.2–8.2.3 (pp. 122–129), §9.2 (pp. 139–144); W §17.1 (pp. 525–535); MS §6.5 (pp. 218–220) | latent-variable probit, σ = 1 identification; Albert–Chib Gibbs; probit vs logit (0.4 vs 1/4 → 1.6); Mroz probit (Table 17.1); ordered probit cut-point full conditional $U(\underline\gamma_j,\overline\gamma_j)$; multinomial probit as a SUR in utility differences; MVP | `L07-probit-logit-ordered` |
| 07 | `L07-07-formulas.md` | all | spec mapped; every result; every number | — |
| 08 | `L07-08-pitfalls.md` | all | confusions + original 30-item V/F | — |
| 09 | `L07-09-python.md` | all | `L07_python_checks.py` shown section by section, asserts vs sources | — |

Figures: 7, one script `Notas/L07/figures/make_figures.py` (imports `Notas/_figstyle.py`, asserts
≥ 1 plotted number per figure).

Out of scope (named only): dugong nonlinear growth curve (HLM slides 27–33, WinBUGS demo), SUR
estimation as a topic (Class 9, G §9.1) — used here only as the vehicle of the multinomial probit;
FE/RE/Hausman as a topic (not on the site schedule; W §14.2 cited as the neighbour); sample
selection (W §17.5); Poisson/GLMs (I §4.6, done in L02).

## Companions (control contracts; local files, not published)

### L07-a `companions/companion-partial-pooling.html` — "The Partial-Pooling Dial"
Model (HLM slide 23): $y_i\mid\theta_i\sim N(\theta_i,\sigma_i^2)$, $\theta_i\sim N(\mu,\tau^2)$,
$\mu\sim N(0,10^6)$, $\tau\sim U(0,A)$; eight schools data. Conditional on τ:
$V_\mu^{-1}=10^{-6}+\sum_i(\sigma_i^2/\kappa+\tau^2)^{-1}$, $\hat\mu=V_\mu\sum_iy_i/(\sigma_i^2/\kappa+\tau^2)$,
$E(\theta_i\mid y,\tau)=(1-B_i)y_i+B_i\hat\mu$, $B_i=(\sigma_i^2/\kappa)/(\sigma_i^2/\kappa+\tau^2)$,
$\mathrm{Var}(\theta_i\mid y,\tau)=(1-B_i)\sigma_i^2/\kappa+B_i^2V_\mu$; $p(\tau\mid y)\propto
1\{\tau<A\}\,N_8(y\mid 0,D_\tau+10^6\mathbf 1\mathbf 1')$ on a grid; fully Bayes $E(\theta_i\mid y)=
\int E(\theta_i\mid y,\tau)p(\tau\mid y)d\tau$.

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| Between-school sd | τ | spread of true effects | 0 – 40 | 0.1 | posterior median at defaults, rounded to 0.1 (computed) | points | slide 23 | shrinkage paths marker, all conditional read-outs |
| Highlighted school | i | which school is read out | A – H | 1 | A | — | slide 23 | highlighted path, read-outs |
| Data precision | κ | each $\sigma_i^2$ divided by κ (more students per school) | 0.25 – 16, log slider, 1 exactly reachable | — | 1 | — | stated on page (thought experiment) | shrinkage, $p(\tau\mid y)$ |
| Prior upper bound | A | $\tau\sim U(0,A)$ | 5 – 100 | 1 | 100 | points | slide 23 hyperprior | $p(\tau\mid y)$, fully Bayes read-outs |

Panels: (1) $E(\theta_i\mid y,\tau)$ vs τ for all eight (no pooling at right, complete pooling at
τ = 0), current τ marked; (2) $p(\tau\mid y)$ with median and current τ. Answer read-out:
**$E(\theta_i\mid y,\tau)$ and its shrinkage $B_i$**; also $\hat\mu(\tau)$, fully Bayes
$E(\theta_i\mid y)$, posterior median of τ. Landmarks: τ = 0 (complete pooling, all equal
$\hat\mu$), κ = 1 (the data), τ at the posterior median.

### L07-b `companions/companion-tobit-censoring.html` — "The Censoring Dial"
Model (LDV slide 9; W §17.2): $y^*=\beta x+u$, $u\sim N(0,\sigma^2)$, $x\sim N(a,1)$, $y=\max(0,y^*)$.
$P(y=0)=\Phi(-a\beta/\sqrt{\beta^2+\sigma^2})$; at a point $x_0$, $z=\beta x_0/\sigma$:
$P(y>0\mid x_0)=\Phi(z)$, $E(y\mid y>0,x_0)=\beta x_0+\sigma\lambda(z)$, $E(y\mid x_0)=\Phi(z)\beta x_0+\sigma\phi(z)$,
$\partial E(y\mid x)/\partial x=\beta\Phi(z)$ (17.30), $\partial E(y\mid y>0,x)/\partial x=\beta\{1-\lambda(z)[z+\lambda(z)]\}$ (17.26);
population OLS slope of $y$ on $x$ = $\beta\,P(y>0)$ (Stein's lemma; derived in note 05).

| Control | Symbol | What it is | Range | Step | Default | Unit | Source | What visibly moves |
|---|---|---|---|---|---|---|---|---|
| Mean of x | a | location of the covariate | −4 – 4 | 0.1 | 0.7 | — | slide 9 (a = 0, 0.7, 1.3) | P(y = 0), density panel, OLS slope |
| Slope | β | latent slope | 0.1 – 4 | 0.1 | 2 | — | slide 9 | all curves |
| Error sd | σ | latent noise | 0.1 – 3 | 0.05 | 0.5 | — | slide 9 (σ² = 0.25) | curves, censoring |
| Evaluation point | x₀ | where partial effects are read | −3 – 3 | 0.05 | 0 | — | stated | markers, pointwise read-outs |

Panels: (1) $E(y^*\mid x)$, $E(y\mid x)$, $E(y\mid y>0,x)$ vs x with x₀ marked; (2) the marginal
distribution of y: point mass at 0 and the continuous density on y > 0. Answer read-out:
**P(y = 0)** (0.25 at defaults; landmarks a = 0 → 0.5, a = 0.7 → 0.25, a = 1.3 → 0.10); also the
OLS slope $\beta(1-P_0)$ vs β, and the pointwise quantities.

Checks: `companions/check_companions.py` (pattern of `Notas/L02/companions/check_companions.py`):
page JS under node vs Python at three control vectors (both ends + defaults) plus landmarks;
every control sweeps; reset restores defaults; no NaN.

## Verification
`python Notas/L07/figures/make_figures.py`; `python Notas/L07/L07_python_checks.py`;
`python Notas/L07/companions/check_companions.py`; `python tools/check_note_links.py Notas/L07`;
`python -I ~/.claude/commands/templates/notes_pdf.py Notas/L07` (no `Missing character`), `pdffonts`
no Type 3. Index row for `Notas/00-index.md` handed to the lead.
