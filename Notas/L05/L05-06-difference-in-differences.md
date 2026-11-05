---
tags: [notes, lecture-05, causal-inference, difference-in-differences, parallel-trends, card-krueger, minimum-wage]
date: 2026-10-25
status: taught
source: "notes-on-causal-inference.pdf pp. 21–25 (§10: Huntington-Klein's back-door story and DAGs pp. 21–22; §10.1 the two-strategy table and the regression y_ti = beta0 + beta1 P_t + beta2 T_i + beta3 P_t T_i + x'gamma + eps p. 22; §10.2 Card–Krueger data, classical R output p. 24, Bayesian R code p. 25). example2-DiD-card-krueger.html + card-krueger.txt (384 stores x 2 periods). MHE §5.2 pp. 169–176 (eqs. 5.2.1–5.2.2 p. 170, Table 5.2.1 p. 171, Fig. 5.2.1 p. 172, Card–Krueger 2000 follow-up p. 172, regression DD 5.2.3 and parameter map p. 175). W §13.2 pp. 407–411 (eqs. 13.10–13.11 p. 410, Table 13.3 p. 411)."
---

# Slides §10 · Difference-in-differences: subtract the control group's change, and assume it is the treated group's counterfactual change

> **Claim.** A before–after comparison of the treated mixes the policy with everything else that changed
> over time; a treated–control comparison mixes it with permanent group differences. The **difference of
> the two differences** removes both, under one assumption: **without the policy, both groups would have
> moved in parallel** (MHE eq. 5.2.1). The four cell means and the saturated regression with an interaction
> (MHE 5.2.3) give the same number. On the site's Card–Krueger file New Jersey's employment rose by 0.467
> FTE while Pennsylvania's fell by 2.283, so **DiD = 2.750** (SE 1.731, $t=1.59$): no sign that the higher
> minimum wage cut employment.
> Prev: [[L05-05-instrumental-variables]] · Next: [[L05-07-regression-discontinuity]] · Map: [[L05-00-map]]

**Notation.**

- $y_{ist}$: full-time-equivalent (FTE) employment of store $i$ in state $s$ and period $t$.
- $T_i$ (`treatment`): 1 for New Jersey (treated), 0 for Pennsylvania (control); $P_t$ (`time`): 1 for November 1992 (after), 0 for February 1992 (before).
- $\bar y_{T,t}$: mean of group $T$ in period $t$ (the site's `pretreatment.treated` etc.).
- MHE: $\gamma_s$ state effect, $\lambda_t$ period effect, $d_{st}$ the treatment dummy ($=T_iP_t$); MHE calls the causal effect $\beta$ in (5.2.2), written $\delta$ here to keep $\beta$ for the regression (6).
- W: $dT$, $d2$, $\delta_0,\beta_1,\delta_1$ in (13.10).
- $\Delta$: a differential trend (treated minus control) that would have occurred without the policy.

---

## 1 · U — two back doors, one design (slides pp. 21–22)

The slides follow Huntington-Klein: an office switches from cubicles to an open plan on 1 January 2017;
productivity $Y$ rises, but "the economy also improved from 2016 to 2017" (p. 21). With a DAG
$X\to Y$, $X\leftarrow\text{Time}\to Y$, the before–after difference picks up "the way that $Y$ may have changed over
Time for reasons unrelated to Treatment". Adding a never-treated **control group** closes the Time back door
but opens another: treatment $T$ now also depends on being **in the treated group** (ITG), and the groups may
differ: $T\leftarrow\text{Time}\to Y$ and $T\leftarrow\text{ITG}\to Y$ (p. 22). "We can close both back-door paths through Time
and In Treated Group using Difference-in-Differences" — difference within group over time, then across groups.

---

## 2 · C — the identifying assumption (MHE §5.2, p. 170)

Potential outcomes $y_{1ist}$ (high minimum wage) and $y_{0ist}$ (low). **Common trends**:

$$E(y_{0ist}\mid s,t)=\gamma_s+\lambda_t .\tag{1}$$

"In the absence of a minimum wage change, employment is determined by the sum of a time-invariant state effect
and a year effect that is common across states." With a constant effect $E(y_{1ist}-y_{0ist}\mid s,t)=\delta$:

$$y_{ist}=\gamma_s+\lambda_t+\delta d_{st}+\varepsilon_{ist},\qquad E(\varepsilon_{ist}\mid s,t)=0 .\tag{2}$$

**Control state's change.** Pennsylvania is never treated ($d=0$ both periods); from (2):

$$E(y\mid PA,Nov)-E(y\mid PA,Feb)=(\gamma_{PA}+\lambda_{Nov})-(\gamma_{PA}+\lambda_{Feb})=\lambda_{Nov}-\lambda_{Feb}.\tag{3}$$

**Treated state's change.** New Jersey has $d=1$ in November only:

$$E(y\mid NJ,Nov)-E(y\mid NJ,Feb)=(\gamma_{NJ}+\lambda_{Nov}+\delta)-(\gamma_{NJ}+\lambda_{Feb})=\lambda_{Nov}-\lambda_{Feb}+\delta .\tag{4}$$

**Difference (4) minus (3):** the state effects cancelled inside each change and the common trend cancels now:

$$[E(y\mid NJ,Nov)-E(y\mid NJ,Feb)]-[E(y\mid PA,Nov)-E(y\mid PA,Feb)]=\delta .\tag{5}$$

(MHE prints the population DD on p. 170 with the brackets in the opposite order — the PA change minus the NJ change —
which as written equals $-\beta$, not $\beta$; the order in (5) is the one MHE uses for the regression parameter on p. 175.)

> **"The key identifying assumption here is that employment trends would be the same in both states in the absence
> of treatment"** (MHE p. 171). Groups may differ in level ($\gamma_s$); they may not differ in trend. Like ignorability,
> this is about an unobserved counterfactual — New Jersey's November employment without the increase.

---

## 3 · C — the slides' two strategies and the regression (slide p. 22; W Table 13.3)

**Strategy 1:** change of the treated over time minus change of the control over time. **Strategy 2:** treated–control
gap after minus treated–control gap before. They are the same four numbers rearranged (W p. 410: "the estimate does not
depend on how we do the differencing").

**Regression** (slide p. 22; W eq. 13.10; MHE eq. 5.2.3):

$$y_{ti}=\beta_0+\beta_1P_t+\beta_2T_i+\beta_3P_tT_i+x_{ti}'\gamma+\varepsilon_{ti}.\tag{6}$$

**Cell means without covariates.** Set $P_t,T_i\in\{0,1\}$ in (6):

| | Before ($P=0$) | After ($P=1$) | After − Before |
|---|---|---|---|
| Control ($T=0$) | $\beta_0$ | $\beta_0+\beta_1$ | $\beta_1$ |
| Treated ($T=1$) | $\beta_0+\beta_2$ | $\beta_0+\beta_1+\beta_2+\beta_3$ | $\beta_1+\beta_3$ |
| Treated − Control | $\beta_2$ | $\beta_2+\beta_3$ | $\beta_3$ |

(W Table 13.3, p. 411, with $\delta_0=\beta_1$, $\beta_1^W=\beta_2$, $\delta_1=\beta_3$.) **Four cells, four parameters: the model is
saturated**, so OLS reproduces the four sample means exactly and

$$\hat\beta_3=(\bar y_{1,1}-\bar y_{1,0})-(\bar y_{0,1}-\bar y_{0,0})\qquad\text{(W eq. 13.11)}.\tag{7}$$

The regression adds standard errors, more groups and periods, and covariates (slide p. 23).

---

## 4 · C — the worked example: the site's Card–Krueger file

"On April 1, 1992, New Jersey raised the state minimum wage from \$4.25 to \$5.05 while the minimum wage in Pennsylvania
stays the same at \$4.25" (slide p. 24); 384 restaurants observed in February and November 1992, 768 rows; 309 NJ
stores, 75 PA. (`treatment = 1` is New Jersey: its pre-period mean matches MHE's NJ column. The slide's phrase "NJ (0) and
PA (1)" is a slip.)

**Cell means** (site output; [[L05-10-python]] §6):

| | February 1992 | November 1992 | change |
|---|---|---|---|
| PA (control) | 23.380 | 21.097 | $B=21.097-23.380=-2.283$ |
| NJ (treated) | 20.431 | 20.897 | $A=20.897-20.431=+0.467$ |
| NJ − PA | $20.431-23.380=-2.949$ | $20.897-21.097=-0.199$ | |

**Strategy 1:** $A-B=0.4666667-(-2.2833333)=2.7500000$ (the site prints `0.4666667 -2.2833333 2.7500000`).
**Strategy 2:** $-0.199-(-2.949)=2.750$.

**Regression** (site `lm(outcome ~ time + treatment + interaction)`): 

| | Estimate | SE | $t$ | $p$ |
|---|---|---|---|---|
| (Intercept) $=\bar y_{0,0}$ | 23.380 | 1.098 | 21.29 | <2e-16 |
| time $=B$ | −2.283 | 1.553 | −1.47 | 0.142 |
| treatment $=$ NJ−PA before | −2.949 | 1.224 | −2.41 | 0.016 |
| interaction $=$ DiD | **2.750** | **1.731** | 1.59 | 0.113 |

Residual SE 9.511 on 764 df, $R^2=0.0076$. Every coefficient is a cell-mean contrast from the table in §3.

**Compare MHE Table 5.2.1** (p. 171, Card–Krueger's own Table 3, all available observations): PA 23.33 → 21.17
($-2.16$), NJ 20.44 → 21.03 ($+0.59$); DiD printed **2.76** (s.e. 1.36); from the rounded entries
$0.59-(-2.16)=2.75$. The site's balanced 384-store file gives almost the same point estimate with a larger SE
(1.731: the pooled-OLS formula ignores that each store appears twice).

> **The sign is the finding.** A competitive labour market predicts employment **falls** in New Jersey relative to
> Pennsylvania; the DiD is **positive**, "the opposite of what we might expect if a higher minimum wage pushes
> businesses up the labor demand curve" (MHE p. 171). Statistically, the 95% interval $2.75\pm1.96(1.731)=(-0.64,6.14)$
> includes 0 but excludes any sizeable job loss.

![Left: the four cell means — Pennsylvania falling from 23.38 to 21.10, New Jersey rising from 20.43 to 20.90 — with New Jersey's counterfactual dashed line falling parallel to Pennsylvania's to 18.15 and a double arrow of 2.75 between counterfactual and actual. Right: the effect implied by DiD minus an assumed differential trend Delta, a falling line from 4.75 at Delta = −2 to −3.25 at Delta = 6, with a ±1.96 × 1.731 band, crossing zero at Delta = 2.75](figures/L05-did-card-krueger.png)
*Left: card-krueger.txt cell means and the common-trend counterfactual $20.431+(-2.283)=18.147$ (MHE Fig. 5.2.1, p. 172, drawn with the data). Right: if (1) fails by a differential trend $\Delta$, the estimate of (5) is $\delta+\Delta$, so the effect is $2.75-\Delta$.*

The dashed line is the whole assumption made visible: New Jersey would have lost 2.28 FTE per store, as
Pennsylvania did. On the right, the band already contains zero at $\Delta=0$ (the interval $(-0.64,6.14)$); a differential
trend of $\Delta=2.75$ — the size of the estimate itself — centres it on zero, and only $\Delta>6.14$ would turn the data into
significant evidence of job **loss**. Card and Krueger's
(2000) payroll data (MHE p. 172, Fig. 5.2.2) show substantial differential swings between the two states in other
years, so "Pennsylvania may not provide a very good measure of counterfactual employment rates in New Jersey".

---

## 5 · C — checking and extending (MHE pp. 172–178)

- **Pre-trends.** With several pre-periods, (1) predicts parallel lines before the policy; MHE's Bavaria example (Fig.
  5.2.3, p. 174) is the encouraging case.
- **More groups, continuous intensity.** $y_{ist}=\gamma_s+\lambda_t+\beta(fa_s\cdot d_t)+\varepsilon_{ist}$ (MHE 5.2.4, p. 175): Card (1992)
  uses the fraction of teenagers affected by the federal minimum as treatment intensity.
- **Logs vs levels** (MHE footnote 7, p. 171): "if there is a common trend in logs, there will not be one in levels and
  vice versa" — the assumption is scale-dependent.

---

## 6 · G — the slides' Bayesian version (slide p. 25)

The R code draws $\beta\sim N\big(\hat\beta,\ s^2(X'X)^{-1}\big)$ with $s^2=\text{SSR}/(n-4)$ and plots the four cell posteriors and the
posterior of $\beta_4$ (the interaction): a flat-prior normal approximation, so the posterior is centred at 2.750 with sd
1.731, and $P(\beta_4>0\mid y)\approx\Phi(2.750/1.731)=\Phi(1.589)=0.944$ ([[L05-10-python]] §6). (The snippet uses a
`beta1` computed earlier in the session.) Posterior simulation and priors are **Classes 3+4**.

---

## Links

- Neighbours: [[L05-05-instrumental-variables]] · [[L05-07-regression-discontinuity]] (next).
- Unit: [[L05-01-simpson-dags]] (back-door paths) · [[L05-02-potential-outcomes-identification]] (DiD's estimand is an ATT: the effect on New Jersey stores) · [[L05-04-errors-in-variables]] (differencing and measurement error) · [[L05-08-formulas]] · [[L05-09-pitfalls]] · [[L05-10-python]] §6.
- Class 7: panel fixed effects and hierarchical models generalise $\gamma_s+\lambda_t$ (`Map/class-plan.md`, Class 7 note on FE/RE).
- Rules pack: [[../../rules/03_painel_did|rules/03]] (difference-in-differences and parallel trends).
- **Practice** (statements in the books): W 13.2 (p. 425), W 13.6 (p. 426), W 13.C3 (p. 427, KIELMC incinerator, the data of W Example 13.3); MHE Table 5.2.1 (p. 171) as a worked example.
