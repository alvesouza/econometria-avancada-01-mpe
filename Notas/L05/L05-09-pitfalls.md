---
tags: [notes, lecture-05, causal-inference, pitfalls, true-false, self-test]
date: 2026-10-25
status: taught
source: "Notes L05-01 … L05-07; V/F style of rules/00_estilo_avaliacao.md (reciprocals and assumptions that break). All numbers come from the notes unless marked illustrative."
---

# Classes 5+6 · Pitfalls and a True/False self-test

> **Claim.** Most mistakes in causal inference are one of four: reading the wrong table (conditioning on a
> mediator or collider, or failing to condition on a confounder), confusing a mechanical identity with a causal
> one (OVB, regression on a randomised dummy), mistaking precision for identification (a tight interval around a
> biased number), and forgetting the assumption that does all the work (exclusion, common trends, continuity at
> the cutoff). Part I gives each confusion with the smallest counterexample; Part II is an original 25-item
> True/False test.
> Prev: [[L05-08-formulas]] · Next: [[L05-10-python]] · Map: [[L05-00-map]]

---

## Part I — the confusions

### 1 · "Control for everything" vs control for confounders only

More controls are not always better. **Counterexample:** in the drug table with post-treatment BP as the
stratifier (slide p. 7), stratifying removes the part of the effect that works through BP; in MHE Table 3.2.1 the
occupation dummies move the return from 0.087 to 0.066 by bad control, not by removing bias ([[L05-03-omitted-variables-bad-control]] §5).
Condition on **forks**; never on **chains out of the treatment** or **colliders**.

### 2 · A collider blocks; conditioning on it opens

Two independent causes $X,Z$ of $W$: $\operatorname{Corr}(X,Z)=0$, but $\operatorname{Corr}(X,Z\mid W)=-0.5$ when $W=X+Z+e$, $\operatorname{Var}(e)=1$
([[L05-01-simpson-dags]] (4)). Conditioning on a **descendant** of $W$ also opens the path ($-1/3$ with unit noise).

### 3 · d-separation is not "no arrow between them"

$Z$ and $Y$ in slide p. 12's second graph share no arrow, yet are dependent through the fork at $T$. Conversely
$Z$ and $Y$ in the first graph are linked by a path and are still independent, because the path has a collider.

### 4 · Simpson: the arithmetic never decides

The same four rates give the right answer in the stratified table for gender and in the pooled table for
post-treatment BP (slide p. 7). A pooled rate is a mix; which mix to use is a causal question about the arrows.

### 5 · Naive difference = ATE

It equals ATT + selection bias (MHE p. 11). In the drug data: naive −4.57 points, ATT +4.80, so selection bias −9.37
([[L05-02-potential-outcomes-identification]] §5.1). The ATE (+5.37) is a third number.

### 6 · QTE = quantile of individual effects

$F_1^{-1}(p)-F_0^{-1}(p)$ compares two **margins**. Illustrative counterexample: $Y(0)\in\{0,1\}$ equally likely and $Y(1)=1-Y(0)$:
both margins are identical, so the QTE is 0 at every $p$, yet every individual effect is $\pm1$.

### 7 · Ignorability can be tested with enough data

"The validity of ignorability cannot be assessed from the observed data, regardless of how large the sample size is"
(slide p. 16). Balance checks test observed covariates only.

### 8 · OVB means the long regression is causal

The OVB formula is "a mechanical link between coefficient vectors that applies to short and long regressions whether or
not the longer regression is causal" (MHE p. 44).

### 9 · Measurement error biases towards zero, always

Only under **classical** error in a **regressor**. Error in $y$ uncorrelated with $x$ leaves OLS consistent (W §9.4a); error
correlated with $x$ (W Example 9.6) can bias either way; and with other regressors, the other coefficients are biased in
directions "not easily derived" (W p. 291).

### 10 · Add the instrument to the regression

$y$ on $(x,z)$ gives $\beta_1+\sigma_{xy}/\sigma_x^2$ on $x$ — the same confounding (slide p. 19; G p. 173). The instrument works only
through the first stage.

### 11 · A significant first stage is a strong first stage

$t=2$ rejects $\delta_1=0$ at 5% but fails the Stock–Yogo $|t|>3.2$ rule (W p. 478). With an exclusion violation $\varphi$, IV is off by
$\varphi/\delta_1$: weak $\delta_1$ magnifies it ([[L05-05-instrumental-variables]] §6 figure).

### 12 · IV is "less biased" than OLS

Only if exclusion holds exactly. With $\operatorname{Corr}(z,x)=0.2$, IV beats OLS on bias only if $\operatorname{Corr}(z,u)<\operatorname{Corr}(x,u)/5$ (W p. 470).

### 13 · DiD needs equal levels

It needs equal **trends** without treatment. NJ and PA differ by $-2.949$ FTE before (MHE: $-2.89$); the state effect absorbs that.
A differential trend $\Delta$ moves the estimate one-for-one ([[L05-06-difference-in-differences]] figure).

### 14 · The DiD regression's $\beta_2$ is the effect

$\beta_2$ is the treated–control gap **before** treatment; the effect is the interaction $\beta_3$ (W Table 13.3).

### 15 · RD identifies the average effect

It identifies $E[y_1-y_0\mid a=a_0]$, the effect **at the cutoff** (MHE 6.1.7). And because no age has both treated and untreated
units, it rests on extrapolating the trend into the cutoff.

### 16 · A jump in a polynomial fit is a discontinuity

A curved $E[y_0\mid a]$ fitted with lines produces a spurious jump (slide p. 30); high-order polynomials produce erratic ones (Gelman &
Imbens 2019, slide p. 38). Check windows, orders, placebo cutoffs and placebo outcomes — and do not pick the bandwidth that looks best:
the internal-cause placebo is "significant" for $b\in[0.90,1.10]$ ([[L05-07-regression-discontinuity]] §7).

---

## Part II — True/False self-test (original items)

**[E]** easy · **[M]** medium · **[P]** hard. Scoring as in [[../../rules/00_estilo_avaliacao|rules/00]]:
$\max\{0,\ \text{right}-\text{wrong}/2\}$ per block. Numbers marked "illustrative" are invented for the item; all others come
from the notes.

### Block A — Simpson and DAGs

**1. [E]** If a treatment raises the recovery rate within every stratum of a variable, it must raise the pooled recovery rate.
**False.** The pooled rate is a weighted average with group-specific weights (01 (1)); the drug wins within gender (93 vs 87, 73 vs
69) and loses pooled (78 vs 83) because 75% of drug takers but 23% of non-takers are women. The composition term −10.5 points beats the
within effect +5.9 (01 (2)).

**2. [M]** In a chain $X\to M\to Y$, conditioning on $M$ makes $X$ and $Y$ independent, so a regression of $Y$ on $X$ and $M$ estimates the
total effect of $X$ on $Y$.
**False.** The first half is Rule 1 (true); the conclusion is the reciprocal trap. Conditioning on the mediator blocks the causal path,
so the $X$ coefficient is the direct effect only (zero in a pure chain). That is why the BP table must be read pooled.

**3. [M]** Two variables that are marginally independent can become dependent after conditioning on a third variable.
**True.** Rule 3: for a collider $X\to W\leftarrow Z$ with $X\perp Z$, conditioning on $W$ (or a descendant) creates dependence; with unit
coefficients and noise, $\operatorname{Corr}(X,Z\mid W)=-0.5$ (01 (4)).

**4. [M]** In slide p. 12's second graph ($T\to Z$, $T\to Y$, $Z\to W\leftarrow X\to Y$, $W\to U$), conditioning on $\{T,U\}$ makes $Z$ and $Y$
independent.
**False.** $T$ blocks the fork path, but $U$ is a descendant of the collider $W$ and opens $Z\to W\leftarrow X\to Y$; $X$ is not conditioned on,
so the path is open. The slide lists $\{U,T\}$ among the d-connecting sets.

**5. [P]** In Harrison's DAG, adjusting for $Z_3$ alone is a valid back-door adjustment for the effect of $X$ on $Y$, because $Z_3$ lies on
every back-door path.
**False.** $Z_3$ lies on every back-door path, but on $X\leftarrow Z_1\to Z_3\leftarrow Z_2\to Y$ it is a **collider**: conditioning on it opens that
path. $\{Z_1,Z_3\}$ or $\{Z_2,Z_3\}$ are valid; in the slide's SEM $\{Z_3\}$ gives 6.0051 against the true 6 (01 §4).

### Block B — potential outcomes and identification

**6. [E]** Under random assignment the average treatment effect on the treated equals the average treatment effect.
**True.** Independence of $A$ from $(Y(0),Y(1))$ gives $E[Y(1)-Y(0)\mid A=1]=E[Y(1)-Y(0)]$ (MHE p. 12; 02 (9)).

**7. [M]** If hospitalised people report worse health than the non-hospitalised (2.79 vs 2.07 on a 1–5 scale where 5 is poor), the
selection-bias term in MHE's decomposition is negative in health terms.
**True.** People who go to hospital have worse $y_{0i}$ — they would be sicker without hospital too — so $E[y_{0i}\mid d_i=1]$ is worse than
$E[y_{0i}\mid d_i=0]$: MHE calls the selection bias "negative in this example" (p. 12), large enough to mask a positive effect.

**8. [M]** Ignorability $\{Y(0),Y(1)\}\perp A\mid L$ implies $Y\perp A\mid L$.
**False.** The observed $Y=Y(A)$ depends on $A$ through the treatment effect; ignorability concerns the **potential** outcomes. If $A$ has
any effect, $Y$ and $A$ are dependent given $L$ — which is how the effect is estimated.

**9. [M]** Positivity can fail even when ignorability holds.
**True.** They are separate conditions. A sharp RD is the extreme case: $D_a$ is a function of $a$, so ignorability given $a$ holds
trivially while $P(D=1\mid a)\in\{0,1\}$ violates positivity everywhere (07 §4).

**10. [P]** With a propensity score estimated as the treated share in each covariate cell, the IPW estimate of the ATE equals the
adjustment-formula estimate.
**True.** Weighting by $1/\hat e(l)$ re-creates the population cell weights in each arm; on the drug table both give 0.05367 (02 §6.1). With a
parametric propensity model the two differ in finite samples.

**11. [M]** The QTE at the median, $F_1^{-1}(0.5)-F_0^{-1}(0.5)$, is the median of the individual effects $Y(1)-Y(0)$.
**False.** It is a difference of marginal quantiles; the median of individual effects depends on the unobserved joint distribution. The
swap counterexample of Part I §6 has QTE 0 and individual effects $\pm1$.

### Block C — omitted variables, bad control, measurement error

**12. [E]** If the omitted variable is uncorrelated with the included regressor, the short and long coefficients on the included regressor
coincide.
**True.** $\delta=0$ in "short = long + γδ" (MHE 3.2.11; 03 (5)–(6)), whatever $\gamma$.

**13. [M]** In the site's simulation ($\beta=0.75$, $\gamma=1.2$), the long regression has a smaller sampling variance than the short one at every
$\operatorname{corr}(x,z)$.
**False.** At $\rho=0$ the long sd is 0.1925 vs 0.2952 short, but at $\rho=0.95$ it is 0.6163 vs 0.2018 (03 (8)–(9)): collinearity inflates the long
variance. The long regression still wins on MSE (0.380 vs 1.340) because the short bias $1.2\rho$ is larger.

**14. [M]** Controlling for a test score taken after schooling, as a proxy for ability, gives a schooling coefficient below the causal effect
when schooling raises the score.
**True.** By MHE (3.2.15) the coefficient is $\rho-\gamma\pi_1/\pi_2<\rho$ when $\gamma,\pi_1,\pi_2>0$; e.g. 0.09 instead of 0.10 (illustrative, 03 §5.1).

**15. [E]** Classical measurement error in the dependent variable biases the OLS slope towards zero.
**False.** Error in $y$ uncorrelated with the regressors goes into the error term: OLS stays unbiased, only less precise (W §9.4a). Attenuation
is a property of error in a **regressor**.

**16. [M]** If the noise variance in a regressor equals the variance of its true value, OLS converges to half the true slope.
**True.** $\lambda=\sigma_x^2/(\sigma_x^2+\sigma_u^2)=1/2$ (04 (4)).

**17. [P]** Adding a correctly measured control that is correlated with a mismeasured regressor reduces the attenuation of the latter's
coefficient.
**False.** It does the opposite: the control removes signal from the regressor but none of the noise, so $\lambda_r=\sigma_r^2/(\sigma_r^2+\sigma_u^2)\le\lambda$
(W 9.36; 04 (8)): 0.390 vs 0.64 in the note's example.

### Block D — instrumental variables

**18. [E]** With one instrument and one endogenous regressor, the IV estimate equals the reduced-form coefficient divided by the first-stage
coefficient.
**True.** $\theta_1=\beta_1\delta_1$ (05 (4)–(5)); on Card $0.04207/0.31990=0.1315$, identical to 2SLS (05 §7).

**19. [M]** If $\operatorname{Cov}(z,x)\neq0$ and $\operatorname{Cov}(z,u)=0$, the IV estimator is unbiased in finite samples.
**False.** It is consistent, but "essentially never unbiased" when IV is needed (W p. 465); small samples can carry substantial bias.

**20. [M]** In Card's data the IV standard error of the return to schooling is about 16 times the OLS one, so the IV estimate is useless.
**False.** The ratio is $0.0549637/0.0034983=15.7$, the price of consistency (W eq. 15.12: IV divides by $R^2_{x,z}$). The interval (0.024, 0.239) still
excludes zero; it is wide, not useless.

**21. [P]** A first-stage $t$ statistic of 2.5 on the excluded instrument is enough, by the Stock–Yogo rule of thumb, to proceed with
standard IV inference.
**False.** The rule asks $|t|>\sqrt{10}\approx3.2$, i.e. $F>10$ (W p. 478); 2.5 rejects at 5% but is weak. Card's 3.64 passes, barely.

**22. [P]** With an instrument whose direct effect on the outcome is $\varphi=0.005$ (illustrative), the IV asymptotic bias falls as the first stage
gets weaker.
**False.** The bias is $\varphi/\delta_1$, which **grows** as $\delta_1\to0$; at the Card calibration IV is worse than OLS for $\delta_1$ below about 0.09
(05 §6).

### Block E — DiD and RDD

**23. [E]** In the regression $y=\beta_0+\beta_1P+\beta_2T+\beta_3PT+\varepsilon$, the coefficient $\beta_2$ measures the effect of the policy.
**False.** $\beta_2$ is the treated–control difference before the policy (−2.949 for NJ vs PA); the DiD effect is $\beta_3=2.750$ (06 §3–4).

**24. [M]** If New Jersey's employment would have grown 1 FTE per store faster than Pennsylvania's without the minimum-wage increase, the
DiD estimate of 2.750 overstates the policy effect by 1 FTE.
**True.** A differential trend $\Delta$ enters additively: the DiD estimates $\delta+\Delta$, so the effect is $2.750-1=1.750$ (06 §4 figure).

**25. [M]** A sharp RD design estimates the average effect of legal drinking on mortality for all young adults aged 19 to 23.
**False.** It estimates $E[y_1-y_0\mid a=21]$, the effect at the cutoff (MHE 6.1.7). Extending it to other ages needs the constant-effect
assumption of (6.1.2), which the design does not test.

---

## Links

- Unit: [[L05-00-map]] · [[L05-08-formulas]] · [[L05-10-python]].
- Existing self-tests on the potential-outcomes part: [[../../Simulados/quiz-class01-1-potential-outcomes-2026-10-10|quiz 1]] · [[../../Simulados/quiz-class01-2-random-assignment-2026-10-10|quiz 2]] · [[../../Simulados/quiz-class01-3-experiments-regression-2026-10-10|quiz 3]]; the notebook's §12–13 ([[../../Aula/class-05-06/potential-outcomes.ipynb|notebook]]).
- Rules: [[../../rules/00_estilo_avaliacao|rules/00]] (V/F scoring) · [[../../rules/01_endogeneidade_iv|rules/01]] · [[../../rules/02_causalidade_potential_outcomes|rules/02]] · [[../../rules/03_painel_did|rules/03]].
