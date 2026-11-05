---
tags: [notes, lecture-05, causal-inference, instrumental-variables, 2sls, wald-estimator, weak-instruments, card]
date: 2026-10-25
status: taught
source: "notes-on-causal-inference.pdf pp. 17–20 (§9: IV DAG and examples p. 17; §9.1 bivariate Gaussian two-equation system, reduced form, two-stage estimator pp. 17–18; §9.2 regression of y on (x, z) pp. 18–19; §9.3 examples incl. Card's college proximity p. 19; §9.4 Bayesian IV papers p. 20). example1-iv-card.html + card.csv (3010 men, 1976). MHE §4.1 pp. 84–96 (eqs. 4.1.1–4.1.3 pp. 85–86, 2SLS 4.1.6–4.1.9 pp. 89–90, Wald 4.1.11–4.1.13 pp. 94–95, Table 4.1.2 p. 96); §4.4.1 Theorem 4.4.1 (LATE) p. 114, G only. W §15.1–15.3 pp. 462–478 (eqs. 15.9–15.13 pp. 465–466, 15.19–15.20 p. 469, Example 15.3 p. 470, Example 15.4 and Table 15.1 pp. 473–474, weak-instrument rule p. 478), §15.5a p. 481. G §11.2 pp. 173–174."
---

# Slides §9 · Instrumental variables: a variable that moves the treatment and nothing else identifies the effect as a ratio

> **Claim.** When the treatment $x$ shares unobserved causes with the outcome $y$, OLS converges to
> $\beta_1$ plus a confounding term. An **instrument** $z$ that shifts $x$ (**relevance**, $\delta_1\neq0$) and
> touches $y$ only through $x$ (**exclusion**, $\operatorname{Cov}(z,u)=0$) identifies
> $\beta_1=\operatorname{Cov}(z,y)/\operatorname{Cov}(z,x)$ — the **reduced form over the first stage**. With a binary
> instrument this is the **Wald estimator**; with covariates it is **2SLS**. Simply adding $z$ to the outcome
> regression does **not** work. The price is variance (the IV SE is $1/|\operatorname{corr}(x,z)|$ times larger) and
> fragility: a weak first stage magnifies any exclusion violation. **Card:** OLS 0.0747, IV 0.1315 (SE 0.0550),
> first-stage $F=13.26$.
> Prev: [[L05-04-errors-in-variables]] · Next: [[L05-06-difference-in-differences]] · Map: [[L05-00-map]]

**Notation** (the slides'; MHE and W letters where they differ).

- $x_i$: treatment (schooling; MHE $s_i$, W $y_2$); $y_i$: outcome (log wage); $z_i$: instrument; $i=1,\dots,n$.
- Outcome equation $y_i=\beta_0+\beta_1x_i+\varepsilon_i^y$; treatment (first-stage) equation $x_i=\delta_0+\delta_1z_i+\varepsilon_i^x$.
- $(\varepsilon_i^x,\varepsilon_i^y)$ bivariate normal, mean 0, variances $\sigma_x^2,\sigma_y^2$, covariance $\sigma_{xy}=\rho\sigma_x\sigma_y$; $z_i$ independent of both errors; $\sigma_z^2=\operatorname{Var}(z)$.
- Reduced form $y_i=\theta_0+\theta_1z_i+u_i$, $u_i\sim N(0,\tau^2)$.
- $\varphi$: direct effect of $z$ on $y$ (an exclusion violation, used in §6 and the companion); $p=P(z=1)$ for a binary instrument.
- MHE: $\rho$ is the causal schooling coefficient in (4.1.2); in this note $\rho$ is always the error correlation, MHE's coefficient is written $\beta_1$.

---

## 1 · U — the IV graph and the examples (slide p. 17)

$$\text{IV}\ \to\ T\ \to\ O,\qquad T\leftarrow C\rightarrow O .$$

"IV: Instrumental variable; T: Treatment/Program/Policy/Risk factors; C: Unmeasured confounders …; O: Outcome."
The instrument opens a causal path into $T$ and has **no** arrow into $O$ or $C$. The slide's table:

| Confounders (C) | Treatment (T) | Outcome (O) | IV |
|---|---|---|---|
| maternal characteristics | smoking during pregnancy | low birth weight | cigarette taxes |
| smoking, caffeine, alcohol | body mass index | Parkinson's disease | FTO gene variant |
| prognostic factors | catheter use | mortality | patients with catheter at facility |
| ability | education | earnings | mother's education |
| proximity | tutoring programme | GPA | library hours |

The path IV → T → O is a chain and IV ← … → O does not exist: IV and O are dependent **only** through T, which is
the whole argument.

---

## 2 · C — the two-equation system and the IV ratio (slides pp. 17–18)

$$y_i=\beta_0+\beta_1x_i+\varepsilon_i^y,\tag{1}$$
$$x_i=\delta_0+\delta_1z_i+\varepsilon_i^x .\tag{2}$$

The slide's two switches: $\rho=0\Rightarrow$ no endogeneity; $\delta_1=0\Rightarrow$ no instrument.

**Why OLS fails.** The OLS slope of $y$ on $x$ converges to $\operatorname{Cov}(x,y)/\operatorname{Var}(x)$. From (2), $\operatorname{Var}(x)=\delta_1^2\sigma_z^2+\sigma_x^2$ and
$\operatorname{Cov}(x,\varepsilon^y)=\operatorname{Cov}(\varepsilon^x,\varepsilon^y)=\rho\sigma_x\sigma_y$. Substitute (1) into the covariance:

$$\operatorname{plim}\hat\beta_1^{OLS}=\frac{\operatorname{Cov}(x,\ \beta_0+\beta_1x+\varepsilon^y)}{\operatorname{Var}(x)}=\beta_1+\frac{\rho\sigma_x\sigma_y}{\delta_1^2\sigma_z^2+\sigma_x^2}.\tag{3}$$

**Reduced form.** Substitute (2) into (1) (slide p. 18):

$$y_i=\beta_0+\beta_1\big[\delta_0+\delta_1z_i+\varepsilon_i^x\big]+\varepsilon_i^y=(\beta_0+\beta_1\delta_0)+(\beta_1\delta_1)z_i+(\beta_1\varepsilon_i^x+\varepsilon_i^y),$$

so

$$\theta_0=\beta_0+\beta_1\delta_0,\qquad\theta_1=\beta_1\delta_1,\qquad\tau^2=\beta_1^2\sigma_x^2+\sigma_y^2+2\beta_1\rho\sigma_x\sigma_y .\tag{4}$$

$u_i=\beta_1\varepsilon_i^x+\varepsilon_i^y$ is independent of $z_i$, so OLS of $y$ on $z$ is consistent for $\theta_1$, and OLS of $x$ on $z$ for $\delta_1$.

**The two-stage estimator** (slide p. 18): (1) obtain $\hat\delta_1$ from the treatment equation; (2) obtain $\hat\theta_1$ from the
outcome-on-instrument regression; (3) since $\theta_1=\beta_1\delta_1$ by (4), with $\delta_1\neq0$:

$$\hat\beta_1^{IV}=\frac{\hat\theta_1}{\hat\delta_1}=\frac{\widehat{\operatorname{Cov}}(z,y)/\widehat{\operatorname{Var}}(z)}{\widehat{\operatorname{Cov}}(z,x)/\widehat{\operatorname{Var}}(z)}=\frac{\widehat{\operatorname{Cov}}(z,y)}{\widehat{\operatorname{Cov}}(z,x)}\quad\Big(=\frac{\text{effect of }z\text{ on }y}{\text{effect of }z\text{ on }x}\Big).\tag{5}$$

**The covariance route** (W eq. 15.9, p. 465; MHE eq. 4.1.3, p. 86). Take the covariance of (1) with $z$:

$$\operatorname{Cov}(z,y)=\beta_1\operatorname{Cov}(z,x)+\operatorname{Cov}(z,\varepsilon^y).$$

Exogeneity sets the last term to 0 and relevance makes $\operatorname{Cov}(z,x)=\delta_1\sigma_z^2\neq0$, so

$$\beta_1=\frac{\operatorname{Cov}(z,y)}{\operatorname{Cov}(z,x)}.\tag{6}$$

The sample analogue (W eq. 15.10) is $\hat\beta_1=\sum(z_i-\bar z)(y_i-\bar y)/\sum(z_i-\bar z)(x_i-\bar x)$; with $z=x$ it is OLS (W p. 465).

> **Two assumptions, one checkable.** Relevance ($\delta_1\neq0$) is a regression of $x$ on $z$ — "something you can check
> in the data" (MHE p. 86). Exclusion ($\operatorname{Cov}(z,\varepsilon^y)=0$) involves the unobserved error and is argued, not tested.
> MHE adds that exclusion "really has two parts": $z$ as good as randomly assigned, and no effect on $y$ except
> through $x$ (p. 86).

(The slide's p. 18 sentence "$z_i\to x_i\to y_i$ is a fork" describes a **chain**; the conclusion, $y\perp z\mid x$ when
$\rho=0$, is Rule 1 of [[L05-01-simpson-dags]].)

---

## 3 · C — why adding $z$ to the outcome regression does not work (slides pp. 18–19; G p. 173)

**Condition one error on the other.** For the bivariate normal $(\varepsilon^x,\varepsilon^y)$ (slide p. 18):

$$\varepsilon_i^y\mid\varepsilon_i^x\sim N\Big(\frac{\sigma_{xy}}{\sigma_x^2}\varepsilon_i^x,\ \sigma_y^2(1-\rho^2)\Big)\quad\Longleftrightarrow\quad\varepsilon_i^y=\frac{\sigma_{xy}}{\sigma_x^2}\varepsilon_i^x+\omega_i,\ \omega_i\sim N(0,\sigma_y^2(1-\rho^2)).\tag{7}$$

**Replace $\varepsilon_i^x$ by its value from (2)**, $\varepsilon_i^x=x_i-\delta_0-\delta_1z_i$:

$$\varepsilon_i^y=\frac{\sigma_{xy}}{\sigma_x^2}\big[x_i-\delta_0-\delta_1z_i\big]+\omega_i .$$

**Substitute into (1) and collect** (slide p. 19):

$$y_i=\Big(\beta_0-\frac{\sigma_{xy}}{\sigma_x^2}\delta_0\Big)+\Big(\beta_1+\frac{\sigma_{xy}}{\sigma_x^2}\Big)x_i+\Big(-\frac{\sigma_{xy}}{\sigma_x^2}\delta_1\Big)z_i+\omega_i .\tag{8}$$

$\omega_i$ is independent of $(x_i,z_i)$, so (8) **is** the population regression of $y$ on $(x,z)$: the coefficient on $x$ is
$\beta_1+\sigma_{xy}/\sigma_x^2$, biased whenever $\rho\neq0$. "In words, by simply including the instrumental variable $z_i$ in the
outcome regression will not suffice to estimate $\beta_1$" (p. 19). Greenberg (§11.2, p. 173) reaches the same
expression and concludes that from $y\mid x$ alone "$\beta_s$ is not identifiable. We have no way of separating $\beta_s$ from
$\beta_s+\sigma_{12}/\sigma_{22}$." The instrument must be used **through the first stage**, not beside it.

---

## 4 · C — the Wald estimator (MHE §4.1.2, pp. 94–96)

Binary $z$ with $P(z=1)=p$, model $y_i=\alpha+\beta_1s_i+\eta_i$ (4.1.11).

**Covariance with a dummy.** $E[yz]=pE[y\mid z=1]$ and $E[y]=pE[y\mid z=1]+(1-p)E[y\mid z=0]$, so

$$\operatorname{Cov}(y,z)=E[yz]-E[y]E[z]=pE[y\mid z=1]-p\big\{pE[y\mid z=1]+(1-p)E[y\mid z=0]\big\}=\{E[y\mid z=1]-E[y\mid z=0]\}p(1-p).$$

The same holds for $\operatorname{Cov}(s,z)$. **Substitute both into (6)**; $p(1-p)$ cancels (MHE eq. 4.1.12):

$$\beta_1=\frac{E[y_i\mid z_i=1]-E[y_i\mid z_i=0]}{E[s_i\mid z_i=1]-E[s_i\mid z_i=0]}.\tag{9}$$

Direct route (4.1.13): $E[y_i\mid z_i]=\alpha+\beta_1E[s_i\mid z_i]$ because $E[\eta_i\mid z_i]=0$; difference at $z=1$ and $z=0$ and divide.

**Worked example, MHE Table 4.1.2** (p. 96; Angrist–Krueger quarter of birth, 1980 census, $n=329{,}509$):

| | born Q1–Q2 | born Q3–Q4 | difference |
|---|---|---|---|
| ln weekly wage | 5.8916 | 5.9051 | $-0.01349$ (0.00337) |
| years of education | 12.6881 | 12.8394 | $-0.1514$ (0.0162) |

$$\hat\beta_1^{Wald}=\frac{-0.01349}{-0.1514}=0.0891\ (0.0210),\qquad\text{vs OLS }0.0703\ (0.0005).$$

**On the Card data** without controls: $\bar y$ is 6.311401 near a college and 6.155494 not near; $\bar x$ is 13.527034 and 12.698015, so

$$\hat\beta^{Wald}=\frac{6.311401-6.155494}{13.527034-12.698015}=\frac{0.155907}{0.829019}=0.1881,$$

against a no-controls OLS of 0.0521 ([[L05-10-python]] §5). The controls of §7 matter: region and race shift both
college proximity and wages.

---

## 5 · C — two-stage least squares (MHE §4.1.1, pp. 89–91; W §15.2–15.3, pp. 471–477)

With exogenous covariates $X_i$ (W's $z_1,\dots,z_{k-1}$) and instrument(s) $z_i$:

$$y_i=X_i'\alpha+\beta_1s_i+\eta_i\quad\text{(structural, MHE 4.1.6)},\qquad s_i=X_i'\pi_{10}+\pi_{11}z_i+\xi_{1i}\quad\text{(first stage)}.\tag{10}$$

**Substitute the first stage into the structural equation** (MHE 4.1.7):

$$y_i=X_i'\alpha+\beta_1\big[X_i'\pi_{10}+\pi_{11}z_i+\xi_{1i}\big]+\eta_i=X_i'(\alpha+\beta_1\pi_{10})+(\beta_1\pi_{11})z_i+(\beta_1\xi_{1i}+\eta_i),$$

the **reduced form** with $z$-coefficient $\pi_{21}=\beta_1\pi_{11}$, so $\beta_1=\pi_{21}/\pi_{11}$ (indirect least squares, MHE 4.1.5).
**2SLS:** regress $s_i$ on $(X_i,z_i)$, form $\hat s_i$, then regress $y_i$ on $(X_i,\hat s_i)$ (MHE 4.1.9). With one instrument, 2SLS = IV =
ILS exactly ([[L05-10-python]] §5 checks all three on card.csv). The second-stage OLS standard errors are wrong (they
use $y-\hat\beta\hat s$ instead of $y-\hat\beta s$); software computes the right ones (MHE p. 91).

Requirements in W's statement (15.29)–(15.31): $\operatorname{Cov}(z_j,u_1)=0$ for all exogenous variables, and $\pi_k\neq0$ — the
**partial** correlation of the excluded instrument with $y_2$ given the included exogenous variables.

---

## 6 · C — the price and the fragility of IV (W pp. 466–470, 478)

**Asymptotic variance** under $E(u^2\mid z)=\sigma^2$ (W eq. 15.12):

$$\operatorname{Avar}(\hat\beta_1^{IV})=\frac{\sigma^2}{n\sigma_x^2\rho_{x,z}^2},\qquad\widehat{\operatorname{se}}=\sqrt{\frac{\hat\sigma^2}{\text{SST}_x\,R^2_{x,z}}}\ \ \text{(15.13)}.\tag{11}$$

OLS has $\sigma^2/\text{SST}_x$; IV divides further by $R^2_{x,z}<1$: "the IV variance is always larger than the OLS variance (when
OLS is valid)" (W p. 466). The SE ratio is $1/|\operatorname{corr}(x,z)|$.

**Bias with an imperfect instrument** (W eqs. 15.19–15.20, p. 469):

$$\operatorname{plim}\hat\beta_{1,IV}=\beta_1+\frac{\operatorname{Corr}(z,u)}{\operatorname{Corr}(z,x)}\cdot\frac{\sigma_u}{\sigma_x},\qquad\operatorname{plim}\hat\beta_{1,OLS}=\beta_1+\operatorname{Corr}(x,u)\cdot\frac{\sigma_u}{\sigma_x}.\tag{12}$$

A small $\operatorname{Corr}(z,u)$ divided by a small $\operatorname{Corr}(z,x)$ can exceed the OLS bias: with $\operatorname{Corr}(z,x)=0.2$, IV is less biased
only if $\operatorname{Corr}(z,u)$ is under one fifth of $\operatorname{Corr}(x,u)$ (W p. 470; the book's sentence repeats "$\operatorname{Corr}(z,u)$" where it means
$\operatorname{Corr}(x,u)$). In the companion's parametrisation, a direct effect $\varphi$ of $z$ on $y$ gives
$\operatorname{plim}\hat\beta^{IV}=\beta_1+\varphi/\delta_1$.

**When relevance fails.** W Example 15.3 (p. 470): mother's packs per day on cigarette price, coefficient 0.0003 (s.e.
0.0008), $R^2=0.0000$; using price anyway gives a packs coefficient of $+2.99$ (s.e. 8.70) — "meaningless because
cigprice fails the one requirement of an IV that we can always test" (also the slide's example C, p. 19).

**Weak instruments.** Staiger–Stock / Stock–Yogo rule (W p. 478): proceed with standard IV inference if the first-stage
$|t|>\sqrt{10}\approx3.2$ (one instrument) or $F>10$ (several), "not the overall F statistic", only the excluded instruments.

![Left: probability limits against the error correlation rho from −0.9 to 0.9 at the Card calibration: IV is a flat line at 0.1315, OLS and the long regression of y on (x, z) are rising lines that nearly coincide, crossing IV at rho = 0; the Card point sits at rho = −0.285 with OLS 0.0747. Right: absolute asymptotic bias against the first-stage coefficient delta1 with a direct effect phi = 0.005: the IV bias phi/delta1 explodes as delta1 goes to zero while the OLS bias stays near 0.057; the F = 10 boundary at delta1 = 0.276 and Card's 0.320 are marked](figures/L05-iv-plims.png)
*Exact plims (3), (5)/(12) and the $x$-coefficient of (8), calibrated to card.csv moments after partialling out the site's 14 controls (so the dots reproduce 0.0747 and 0.1315). Slides pp. 18–19; W eqs. 15.19–15.20.*

Reading the left panel: IV is flat because it does not depend on $\rho$; OLS crosses it only at $\rho=0$. The long
regression is no better than OLS — here they almost coincide because the instrument explains only
$\delta_1^2\sigma_z^2=0.017$ of a schooling variance of 3.746. The Card point sits at $\rho=-0.285$: the data imply OLS **below** IV.
On the right, with an exclusion violation of only 0.005 log points, IV is less biased than OLS to the right of
$\delta_1\approx0.09$ and much worse to the left; Card's first stage (0.320) is barely past the $F=10$ line (0.276 at
$n=3010$).

> **Interactive companion.** [The Instrument Dial](companions/companion-iv-plims.html) — move $\beta_1$, the endogeneity $\rho$,
> the first stage $\delta_1$, an exclusion violation $\varphi$ and $n$; watch the OLS, IV and long-regression plims with
> their 95% bands, the IV bias $\varphi/\delta_1$, and the first-stage $F$ against 10. Defaults reproduce Card.

---

## 7 · C — the worked example: Card's college proximity (slide p. 19; example1-iv-card.html; W Example 15.4)

Outcome `lwage`, treatment `educ`, instrument `nearc4` (grew up near a four-year college), controls `exper`,
`expersq`, `black`, `smsa`, `south`, `smsa66`, `reg662`–`reg669`; $n=3010$ (the site's printout, reproduced in
[[L05-10-python]] §5).

| Step | Estimate (s.e.) | Source |
|---|---|---|
| OLS, `educ` | 0.0746933 (0.0034983) | site; W Table 15.1: .075 (.003) |
| First stage, `nearc4` on `educ` | 0.320 (0.088), $t=3.64$, $R^2=0.477$ | W p. 473 |
| First-stage $F=t^2$ | $3.64^2\approx13.256$ | site "Weak instruments 13.256" |
| Reduced form, `nearc4` on `lwage` | 0.04207 | computed |
| ILS $=$ IV | $0.04207/0.31990=0.1315$ | (5) |
| IV (2SLS), `educ` | 0.1315038 (0.0549637) | site; W Table 15.1: .132 (.055) |
| 95% CI | $0.1315\pm1.96(0.0550)=(0.024,\ 0.239)$ | W p. 474 |
| Wu–Hausman | 1.168 ($p=0.280$) | site |
| BIC-selected controls: IV | 0.1365294 (0.0495914), $F=16.621$ | site §4 |

**Readings.**

- **IV is almost twice OLS** (W p. 474) and its SE is $0.0549637/0.0034983=15.7$ times larger. The slide rounds to
  0.075 and 0.132, SEs 0.003 and 0.055 ("twenty times as big!"), CIs (0.069, 0.081) and (0.022, 0.242) — the latter is
  $0.132\pm2(0.055)$. "Larger CIs: price paid for consistent estimator of the return to (endogenous) education" (p. 19).
- **First stage passes the rule of thumb** ($t=3.64>3.2$, $F=13.26>10$), but not by much — see the right panel above.
- **Wu–Hausman** (W §15.5a, p. 481) adds the first-stage residual $\hat v_2$ to the OLS equation and tests it: $t^2=1.168$,
  $p=0.28$. OLS and IV are not statistically distinguishable here, despite the factor of two, because the IV interval is so wide.
- **Why might IV exceed OLS?** Omitted ability (MHE p. 45) predicts OLS **above** the truth; the data say the opposite
  (implied $\rho=-0.285$). Measurement error in `educ` (note 04) biases OLS down, and IV with an instrument independent of
  that error removes it (W p. 480). The heterogeneous-effects reading is in §8.

---

## 8 · G — heterogeneous effects: LATE (MHE §4.4.1, Theorem 4.4.1, p. 114)

With individual effects and potential treatments $d_{1i},d_{0i}$ (treatment status if $z_i=1$ or $0$), assume (A1)
independence of $z_i$ from all potential outcomes and treatments, (A2) exclusion $y_i(d,0)=y_i(d,1)$, (A3) a first stage
$E[d_{1i}-d_{0i}]\neq0$, (A4) monotonicity $d_{1i}\ge d_{0i}$ for all $i$ (or the reverse). Then

$$\frac{E[y_i\mid z_i=1]-E[y_i\mid z_i=0]}{E[d_i\mid z_i=1]-E[d_i\mid z_i=0]}=E[y_{1i}-y_{0i}\mid d_{1i}>d_{0i}],$$

the average effect on **compliers** — those whose treatment the instrument changes. Proved in MHE pp. 114–115; not on
the slides, so not examinable here beyond the statement. For Card, the compliers are men whose schooling depended on
having a college nearby, plausibly those with high marginal returns.

**Bayesian IV** (Greenberg §11.2, pp. 173–174: the system (11.9)–(11.10) with a Wishart prior and a Gibbs sampler;
slide p. 20: Hahn, He and Lopes 2018, Lopes and Polson 2014): Classes 3+4 tools, named only.

---

## Links

- Neighbours: [[L05-04-errors-in-variables]] (IV as the cure for attenuation, (9) there) · [[L05-06-difference-in-differences]] (next).
- Unit: [[L05-01-simpson-dags]] (chains, forks; the IV graph) · [[L05-03-omitted-variables-bad-control]] (the bias IV removes is (6) there) · [[L05-07-regression-discontinuity]] (fuzzy RD is IV with the cutoff as instrument) · [[L05-08-formulas]] · [[L05-09-pitfalls]] · [[L05-10-python]] §5.
- Class 2: [[../L02/L02-02-linear-log-linear-regression|L02 §2]] (log-level reading: 0.1315 ≈ 13.2% per year, exactly $e^{0.1315}-1=14.1\%$).
- Rules pack: [[../../rules/01_endogeneidade_iv|rules/01]] (2SLS and the Wald estimator; LATE; weak instruments).
- **Practice** (statements in the books): W 15.C3 (p. 492) and W 15.C5 (p. 493), both on CARD; MHE Table 4.1.1 (p. 92), Table 4.1.2 (p. 96), Table 4.1.3 (p. 97) as worked examples; G 11.1–11.4 (pp. 180–181) for the Bayesian versions.
