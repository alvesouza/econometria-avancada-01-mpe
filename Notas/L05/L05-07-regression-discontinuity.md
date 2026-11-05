---
tags: [notes, lecture-05, causal-inference, regression-discontinuity, sharp-rd, local-linear, mlda]
date: 2026-10-25
status: taught
source: "notes-on-causal-inference.pdf pp. 26–38 (§11, after Angrist & Pischke, Mastering 'Metrics ch. 4, pp. 147–164: birthdays and funerals pp. 26–27; D_a and sharp RD p. 28; y_a = alpha + rho D_a + gamma a + eps_a, rho-hat = 7.7, p. 29; nonlinearity mistaken for a discontinuity p. 30; linear vs quadratic-with-interactions p. 31; R script replicating Fig. 4.5 p. 33; Bayesian version pp. 34–35; non-parametric RDD p. 36; NBA draft pp. 36–37; references p. 38). example3-RDD-age-mva-internal.html + age-mva-internal.txt (48 monthly cells). MHE §6.1 pp. 189–195 (eqs. 6.1.1–6.1.7), §6.2 pp. 196–198 (fuzzy RD, eq. 6.2.5), G only."
---

# Slides §11 · Regression discontinuity: when a rule switches treatment on at a cutoff, the jump in the outcome is the effect at the cutoff

> **Claim.** In a **sharp** design treatment is a deterministic, discontinuous function of a running variable,
> $D_a=1(a\ge21)$, so treated and untreated never share a value of $a$ and ignorability holds trivially while
> **positivity fails by construction**. Identification comes instead from **continuity**: if $E[y_0\mid a]$ is smooth at the
> cutoff, the jump in $E[y\mid a]$ there is $E[y_1-y_0\mid a=a_0]$ (MHE eq. 6.1.7). Estimating it means modelling the trend
> on each side — linear, quadratic with interactions, or locally linear in a window — and the trend model is where RD
> goes wrong: curvature can masquerade as a jump. On the site's MLDA data, motor-vehicle deaths jump by **4.53 per
> 100,000** at 21 (SE 0.77; 3.41 residual sds), deaths from internal causes do not (0.39, SE 0.60).
> Prev: [[L05-06-difference-in-differences]] · Next: [[L05-08-formulas]] · Map: [[L05-00-map]]

**Notation** (the slides'; MHE's in brackets).

- $a$ [$x_i$]: running variable, age in years; $a_0$ [$x_0$]: cutoff, 21; $D_a$ [$d_i$]: treatment, legal access to alcohol.
- $y_a$ [$y_i$]: death rate per 100,000 in the 30-day cell at age $a$; $y_0,y_1$: potential outcomes without/with treatment.
- $\rho$: the jump (the causal effect at the cutoff); $\gamma$ [MHE $\beta$]: slope of the trend; $\gamma_1,\gamma_2,\delta_1,\delta_2$: quadratic and interaction terms of slide p. 31.
- $b$ [MHE $\Delta$]: bandwidth, half-width of the window $[a_0-b,a_0+b]$; $\hat\sigma$: residual standard deviation.

---

## 1 · U — birthdays and funerals (slides pp. 26–28)

"Human behavior is constrained by rules" (p. 26): class sizes capped at 32, pensions from age 62, the US
**minimum legal drinking age** of 21. Daily deaths of Americans aged 20–22 (1997–2003) spike on and right after
the 21st birthday: "This spike adds about 100 deaths to a baseline level of about 150 per day" (p. 27). By month of
age, "few rates to the left of the age-21 cutoff are above 95 … few of those to the right … are below 95" (p. 28).

---

## 2 · C — the sharp design (slide p. 28; MHE §6.1, p. 189)

$$D_a=\begin{cases}1&a\ge21\\0&a<21\end{cases}\qquad\text{(MHE 6.1.1: }d_i=1(x_i\ge x_0)).\tag{1}$$

The slide's three properties: treatment is a **deterministic** function of $a$ ("once we know $a$, we know $D_a$"),
a **discontinuous** one ("no matter how close $a$ gets to the cutoff, $D_a$ remains unchanged until the cutoff is
reached"), and $a$ is the **running variable**. Sharp RD: "treatment switches cleanly off or on as the running
variable passes a cutoff". (The site's code sets `over21[age>21]=1`; no cell sits exactly at 21, so $>$ and $\ge$ agree.)

**Why regression still matters** (slide p. 29). "Mortality clearly changes with the running variable, $a$, for reasons
unrelated to the MLDA": internal-cause deaths rise through the late teens, external-cause deaths fall. "RD gets its
name from the practice of using regression models to implement this control."

---

## 3 · C — the linear model (slide p. 29; MHE eq. 6.1.2, p. 190)

**Assume** a linear untreated trend and a constant effect (MHE p. 190):

$$E[y_0\mid a]=\alpha+\gamma a,\qquad y_1=y_0+\rho .\tag{2}$$

**Observed mean.** By (1) the observed outcome is $y=y_0+(y_1-y_0)D_a=y_0+\rho D_a$; take expectations given $a$ and substitute (2):

$$E[y_a\mid a]=\alpha+\gamma a+\rho D_a\quad\Longrightarrow\quad y_a=\alpha+\rho D_a+\gamma a+\varepsilon_a .\tag{3}$$

"The negative slope, captured by $\gamma$, reflects smoothly declining death rates among young people as they mature.
The parameter $\rho$ captures the jump in deaths at age 21. The regression generates an estimate of $\rho$ equal to 7.7"
(p. 29) — for **all** deaths in Mastering 'Metrics. The site's file has the two components of Fig. 4.5, motor-vehicle
accidents (MVA) and internal causes, worked in §6.

> **What makes (3) identify anything.** $D_a$ is perfectly determined by $a$, yet not collinear with it: RD
> "distinguish[es] the nonlinear and discontinuous function, $1(x_i\ge x_0)$, from the smooth and (in this case) linear
> function, $x_i$" (MHE p. 190). Everything rests on the trend being correctly modelled on both sides.

---

## 4 · C — identification without functional form (MHE eq. 6.1.7, p. 193)

If $E[y_0\mid a]$ and $E[y_1\mid a]$ are continuous at $a_0$, then just below the cutoff everyone is untreated and just above
everyone is treated:

$$E[y\mid a_0-\Delta<a<a_0]\simeq E[y_0\mid a=a_0],\qquad E[y\mid a_0<a<a_0+\Delta]\simeq E[y_1\mid a=a_0].$$

**Subtract and let the window shrink:**

$$\lim_{\Delta\to0}\Big\{E[y\mid a_0<a<a_0+\Delta]-E[y\mid a_0-\Delta<a<a_0]\Big\}=E[y_1-y_0\mid a=a_0].\tag{4}$$

The estimand is an **average effect at the cutoff**, valid without the constant-effect assumption in (2) (MHE p. 193) —
and only there: RD says nothing about 25-year-olds. Since no age has both treated and untreated cells, RD "turns on our
willingness to extrapolate across covariate values, at least in a neighborhood of the discontinuity" (MHE p. 190).

---

## 5 · C — polynomials and interactions (slides pp. 30–31; MHE eqs. 6.1.4–6.1.6, p. 192)

**Different trends on each side.** Model both conditional means with polynomials in $\tilde a=a-a_0$:

$$E[y_0\mid a]=\alpha+\gamma_1\tilde a+\gamma_2\tilde a^2,\qquad E[y_1\mid a]=\alpha+\rho+\gamma_1^{(1)}\tilde a+\gamma_2^{(1)}\tilde a^2 .$$

**Combine** with $E[y\mid a]=E[y_0\mid a]+E[y_1-y_0\mid a]D_a$ (MHE p. 192):

$$E[y\mid a]=\alpha+\gamma_1\tilde a+\gamma_2\tilde a^2+D_a\big[\rho+(\gamma_1^{(1)}-\gamma_1)\tilde a+(\gamma_2^{(1)}-\gamma_2)\tilde a^2\big].$$

**Name the differences** $\delta_k=\gamma_k^{(1)}-\gamma_k$ — the slide's quadratic regression with interactions (p. 31):

$$y_a=\alpha+\rho D_a+\gamma_1(a-a_0)+\gamma_2(a-a_0)^2+\delta_1[(a-a_0)D_a]+\delta_2[(a-a_0)^2D_a]+\varepsilon_a .\tag{5}$$

Centring at $a_0$ makes $\rho$ the jump **at the cutoff** (at $\tilde a=c>0$ the effect is $\rho+\delta_1c+\delta_2c^2$, MHE p. 192). The
site's code does not centre: it regresses on `age`, `age2`, `over21*age`, `over21*age2` and recovers the jump as
`right - left` $=\hat\beta_{over21}+21\hat\beta_{over21\cdot age}+441\hat\beta_{over21\cdot age^2}$, the same number.

**The danger** (slide p. 30; MHE Fig. 6.1.1 panel C, p. 191): "nonlinearity mistaken for a discontinuity" — a sharp
turn in a smooth $E[y_0\mid a]$, fitted with straight lines, produces a spurious jump. Gelman and Imbens (2019, slide p. 38)
warn the other way: high-order global polynomials give erratic jumps. Hence windows (§7).

---

## 6 · C — the worked example: the site's MLDA data

48 monthly cells, ages 19.07 to 22.93, deaths per 100,000. Fits on all cells ([[L05-10-python]] §7 reproduces every number):

**Linear (3), MVA:** $\widehat{mva}=95.4814-3.1488\,a+4.534\,D_a$. The two fitted limits at 21:

$$\text{left}=95.4814-3.1488(21)=95.4814-66.1248=29.3566,\qquad\text{right}=29.3566+4.534=33.8906 .$$

| Outcome, model | $\hat\rho$ (SE) | $\hat\sigma$ | $\hat\rho/\hat\sigma$ (site: "stdevs") | $t$ |
|---|---|---|---|---|
| MVA, linear (3) | **4.534** (0.768) | 1.3293 | $4.534/1.3293=$ **3.411** | 5.90 |
| MVA, quadratic with interactions (5) | 4.663 (1.155) | 1.3292 | **3.508** | 4.04 |
| Internal, linear | 0.392 (0.596) | 1.0318 | **0.380** | 0.66 |
| Internal, quadratic with interactions | 1.073 | 1.0458 | **1.026** | — |

**Readings.**

- **MVA jumps, robustly.** Linear and quadratic agree (4.53 vs 4.66); the curvature terms cost precision (SE 0.77 → 1.15)
  without moving the estimate. A 4.5-point rise on a left limit of 29.4 is about 15%.
- **Internal causes do not, on the full sample.** Deaths from disease should not respond to legal drinking; a jump of
  0.39 (SE 0.60) there is a built-in **placebo outcome** that supports the design. (The quadratic gives 1.07, and some
  narrow windows give more — §7.)
- **The slide's "stdevs" legend** divides the jump by the residual sd, a scale-free size (not a $t$ statistic). In the
  slide's p. 33 code the linear DIC legend uses `delta/sigma1` — the MVA jump over the DIC sd, 4.394; the site page
  corrects it to `delta1/sigma1` = 0.380.

---

## 7 · C — local linear regression and the bandwidth (slide p. 36; MHE p. 193)

"For observations in $[a_0-b,a_0+b]$, for small $b$, nonlinear trends need not concern us at all. Strategy: comparing
averages in a narrow window just to the left and just to the right of the cutoff. High variance: very narrow window →
few observations → too imprecise estimates. Trade-off: bias reduction near the boundary against the increased variance"
(slide p. 36). The estimator is (3) — or (5) with linear terms only — on the cells with $|a-a_0|\le b$. MHE (p. 193)
describes it as weighted least squares with more weight near the cutoff; the uniform window is the simplest kernel.

**MVA, linear with separate slopes, by bandwidth** ([[L05-10-python]] §7):

| $b$ (years) | $\hat\rho$ | SE |
|---|---|---|
| 0.5 | 4.772 | 1.291 |
| 1.0 | 4.759 | 1.123 |
| 2.0 (all cells) | 4.534 | 0.751 |

**Placebo cutoffs** (same estimator, $b=1$, at ages where no rule changes): $a_0=20$: $0.828$ (SE 1.096); $a_0=22$: $-0.103$
(SE 1.106). Neither is distinguishable from zero.

> **The jump survives every specification.** Narrowing the window from all 48 cells to one year either side moves
> $\hat\rho$ by a quarter of a death and widens the SE by half; fake cutoffs show nothing. That stability, not any one
> number, is the RD evidence (MHE p. 193: "Hopefully, as you zero in on $x_0$ with fewer and fewer controls, the
> estimated effect of $d_i$ remains stable").

![Left: monthly death rates against age from 19 to 23, motor-vehicle accidents near 27–36 and internal causes near 16–24, circles left of 21 and squares right, with solid linear and dashed quadratic-with-interactions fits on each side; the MVA fit jumps up at 21, the internal-cause fit barely moves. Right: local linear estimates of the jump with ±1.96 SE bands against the bandwidth from 0.4 to 2 years: the MVA estimate stays between about 4.2 and 5.7 with a band that narrows as the window widens; the internal-cause estimate falls from about 1.4 to 0.4 with a band covering zero](figures/L05-rdd-mlda.png)
*Left: (3) and (5) fitted to age-mva-internal.txt (the site's two figures in one). Right: local linear with separate slopes on $|a-21|\le b$, $b=0.40,0.45,\dots,2.00$. Slides pp. 29–36; MHE eqs. 6.1.2, 6.1.6.*

On the left the discontinuity is visible by eye for MVA and absent for internal causes, and the two specifications
nearly coincide. On the right the bias–variance trade-off of slide p. 36 is literal: narrow windows give wide bands.
The MVA band stays well above zero at every bandwidth (its lower edge never falls below 1.5). The internal-cause band
covers zero at most bandwidths but **not** for $b$ between 0.90 and 1.10 (22–26 cells), where $\hat\rho\approx1.6$–$1.9$ with a
lower edge of 0.17–0.28: scanning 33 bandwidths of a noisy placebo outcome turns up a "significant" window. Report the
whole curve, not the bandwidth that looks best.

> **Interactive companion.** [The Discontinuity Window](companions/companion-rdd-window.html) — choose the outcome, the
> bandwidth $b$, the polynomial order, separate slopes on/off and the cutoff $a_0$ (move it off 21 for a placebo test);
> watch the fitted pieces, $\hat\rho\pm1.96$SE, the jump in residual sds, and $\hat\rho$ against every bandwidth. Buttons reset
> to the site's linear and quadratic fits.

---

## 8 · G — beyond the sharp parametric design

- **The slides' Bayesian version** (pp. 34–35): draws $\beta\sim N(\hat\beta,\hat\sigma^2(X'X)^{-1})$ (with $\hat\sigma^2$ the ML variance) and
  plots the posteriors of the left and right limits at 21 for each model. A flat-prior normal approximation; Classes 3+4.
- **Fuzzy RD is IV** (MHE §6.2, pp. 196–198): when crossing the cutoff changes only the **probability** of treatment, the
  jump in $y$ divided by the jump in $P(d=1\mid x)$ (MHE eq. 6.2.5) is a Wald estimator ([[L05-05-instrumental-variables]] §4)
  with $1(x\ge x_0)$ as the instrument. Named only; not on the slides.
- **Bayesian nonparametric RD** (slides pp. 36–37): Branson et al. (2019), Gaussian-process regression on 1,238 NBA
  draftees — "the treatment effect of being a second-round pick significantly reduces the number of games played".
  Data-driven bandwidths (Imbens–Kalyanaraman 2012; Calonico–Cattaneo–Titiunik 2014) are in the reference list (p. 38).
  Named only.

---

## Links

- Neighbours: [[L05-06-difference-in-differences]] · [[L05-08-formulas]] (next).
- Unit: [[L05-02-potential-outcomes-identification]] (positivity fails by design; (4) is a CATE at $a=a_0$) · [[L05-05-instrumental-variables]] (fuzzy RD) · [[L05-09-pitfalls]] · [[L05-10-python]] §7.
- Class 2: [[../L02/L02-03-cross-validation-motorcycle|L02 §3]] (polynomial order and over-fitting: the same trade-off as the bandwidth here).
- Rules pack: [[../../rules/02_causalidade_potential_outcomes|rules/02]]; RDD is a site topic beyond the syllabus table and in scope ([[../../Map/class-plan|Map/class-plan]], end notes).
- **Practice** (worked examples in the book): MHE Figure 6.1.2 (p. 195, Lee 2008 elections) and Table 6.2.1 (p. 202, Angrist–Lavy class size, fuzzy RD).
