---
tags: [notes, lecture-05, causal-inference, measurement-error, errors-in-variables, attenuation-bias, instrumental-variables]
date: 2026-10-25
status: taught
source: "error-in-variables.pdf (1 page: y = beta x + eps, w = x + u, beta_naive = Cov(y, w)/Var(w) = beta sigma_x^2/(sigma_x^2 + sigma_u^2)). W §9.4 Properties of OLS under Measurement Error pp. 287–292 (9.4a error in y pp. 287–289; 9.4b error in an explanatory variable pp. 289–292, eqs. 9.27–9.33 attenuation p. 291, 9.34–9.36 with other regressors p. 291). MHE §4 intro p. 84 (regression coefficient biased towards zero; IV as the fix) and footnote 8 p. 95 (Wald 1940). W §15.4 IV Solutions to Errors-in-Variables Problems pp. 479–481."
---

# error-in-variables.pdf · W §9.4 · A noisy regressor shrinks the slope towards zero, by exactly the reliability ratio

> **Claim.** If the regressor is observed with classical noise, $w=x+u$, OLS of $y$ on $w$ estimates
> $\beta\,\sigma_x^2/(\sigma_x^2+\sigma_u^2)$: the slope is **attenuated** towards zero by the share of the observed
> variance that is signal. Noise in $y$ costs only precision; noise in $x$ costs consistency. Controls that
> explain part of the true regressor make attenuation **worse**, since they remove signal and leave the noise.
> A second, independent measurement used as an **instrument** restores $\beta$ — the first appearance of IV in the
> unit, and historically one of its origins (MHE p. 84).
> Prev: [[L05-03-omitted-variables-bad-control]] · Next: [[L05-05-instrumental-variables]] · Map: [[L05-00-map]]

**Notation** (the slide's; Wooldridge's letters in brackets).

- $x_i$ [$x_1^\ast$]: true regressor, variance $\sigma_x^2$; $w_i$ [$x_1$]: observed regressor; $u_i$ [$e_1$]: measurement error, mean 0, variance $\sigma_u^2$.
- $y_i=\beta x_i+\varepsilon_i$ [$y=\beta_0+\beta_1x_1^\ast+u$]: true model, $\varepsilon_i$ independent of $x_i$.
- $\lambda=\sigma_x^2/(\sigma_x^2+\sigma_u^2)\in(0,1]$: reliability (attenuation factor); $\kappa=\sigma_u^2/\sigma_x^2$: noise-to-signal ratio.
- $r_1^\ast$: error of the regression of $x_1^\ast$ on the other regressors (W 9.36), variance $\sigma_r^2$.

---

## 1 · C — the slide's derivation (error-in-variables.pdf)

**Model.** True: $y_i=\beta x_i+\varepsilon_i$. Observed: $w_i=x_i+u_i$, with $u_i$ independent of $x_i$ and $\varepsilon_i$.

**Naive slope.** Regressing $y$ on $w$ estimates

$$\hat\beta_{\text{naive}}\ \to\ \frac{\operatorname{Cov}(y,w)}{\operatorname{Var}(w)}.\tag{1}$$

**Numerator.** Substitute both definitions and use the independence of $x$, $u$, $\varepsilon$:

$$\operatorname{Cov}(y,w)=\operatorname{Cov}(\beta x+\varepsilon,\ x+u)=\beta\operatorname{Var}(x)+\beta\operatorname{Cov}(x,u)+\operatorname{Cov}(\varepsilon,x)+\operatorname{Cov}(\varepsilon,u)=\beta\sigma_x^2 .\tag{2}$$

**Denominator.**

$$\operatorname{Var}(w)=\operatorname{Var}(x)+\operatorname{Var}(u)=\sigma_x^2+\sigma_u^2 .\tag{3}$$

**Substitute (2) and (3) into (1):**

$$\hat\beta_{\text{naive}}\ \to\ \beta\,\frac{\sigma_x^2}{\sigma_x^2+\sigma_u^2}=\beta\lambda=\frac{\beta}{1+\kappa}.\tag{4}$$

"The slope is biased toward zero (attenuation bias)" (slide). Since $\lambda<1$ whenever $\sigma_u^2>0$, $|\beta\lambda|<|\beta|$
with the same sign: the estimate never flips sign, it only shrinks.

**Worked numbers.** $\sigma_x=\sigma_u=1$: $\lambda=1/(1+1)=0.5$ — half the slope. $\beta=1.5$, $\sigma_x=1$, $\sigma_u=0.75$:
$\lambda=1/(1+0.5625)=0.64$, so OLS converges to $1.5(0.64)=0.96$ ([[L05-10-python]] §4 gets 0.959 on 400,000 draws).

---

## 2 · C — Wooldridge's two polar assumptions (W §9.4b, pp. 289–291)

W writes $e_1=x_1-x_1^\ast$ (9.28) and substitutes $x_1^\ast=x_1-e_1$ into $y=\beta_0+\beta_1x_1^\ast+u$ (9.27):

$$y=\beta_0+\beta_1x_1+(u-\beta_1e_1).\tag{5}$$

Whether OLS on (5) works depends on the correlation of $x_1$ with the composite error $u-\beta_1e_1$:

| Assumption | Statement | Consequence |
|---|---|---|
| (9.29) | $\operatorname{Cov}(x_1,e_1)=0$: error uncorrelated with the **observed** measure | $u-\beta_1e_1$ uncorrelated with $x_1$: OLS **consistent**, only the error variance rises to $\sigma_u^2+\beta_1^2\sigma_{e_1}^2$ (W p. 290) |
| (9.31) **CEV** | $\operatorname{Cov}(x_1^\ast,e_1)=0$: error uncorrelated with the **true** value (the slide's case) | $\operatorname{Cov}(x_1,e_1)=\sigma_{e_1}^2$ (9.32), so OLS is inconsistent |

**CEV algebra** (W eq. 9.33, p. 291). The composite error's covariance with $x_1$, by (9.32):

$$\operatorname{Cov}(x_1,u-\beta_1e_1)=-\beta_1\operatorname{Cov}(x_1,e_1)=-\beta_1\sigma_{e_1}^2 .$$

Then

$$\operatorname{plim}\hat\beta_1=\beta_1+\frac{\operatorname{Cov}(x_1,u-\beta_1e_1)}{\operatorname{Var}(x_1)}=\beta_1-\frac{\beta_1\sigma_{e_1}^2}{\sigma_{x_1^\ast}^2+\sigma_{e_1}^2}=\beta_1\left(\frac{\sigma_{x_1^\ast}^2}{\sigma_{x_1^\ast}^2+\sigma_{e_1}^2}\right),\tag{6}$$

the slide's (4) in W's letters. "If the variance of $x_1^\ast$ is large relative to the variance in the measurement
error, then the inconsistency in OLS will be small" (p. 291).

### 2.1 · Error in the dependent variable is harmless for consistency (W §9.4a, pp. 287–289)

If $y=y^\ast+e_0$ with $e_0$ uncorrelated with the regressors, $y=\beta_0+\beta_1x+(u+e_0)$: OLS stays unbiased and
consistent; only $\operatorname{Var}(u+e_0)=\sigma_u^2+\sigma_0^2>\sigma_u^2$ inflates the standard errors (W p. 288).
W's Example 9.6 (p. 289) shows the exception: if the error in $y$ is correlated with a regressor (grant recipients
under-reporting scrap), the coefficient is biased.

---

## 3 · C — other regressors make it worse (W eq. 9.36, p. 291)

With $y=\beta_0+\beta_1x_1^\ast+\beta_2x_2+\beta_3x_3+u$ and only $x_1^\ast$ mismeasured (CEV),

$$\operatorname{plim}\hat\beta_1=\beta_1\left(\frac{\sigma_{r_1^\ast}^2}{\sigma_{r_1^\ast}^2+\sigma_{e_1}^2}\right),\tag{7}$$

where $r_1^\ast$ is the error in $x_1^\ast=\alpha_0+\alpha_1x_2+\alpha_2x_3+r_1^\ast$. If the other regressors explain a share $R^2$ of
$\operatorname{Var}(x_1^\ast)$, then $\sigma_{r}^2=(1-R^2)\sigma_x^2$ while the noise $\sigma_{e_1}^2$ is untouched, so (7) is (4) with the signal cut:

$$\lambda_r=\frac{(1-R^2)\sigma_x^2}{(1-R^2)\sigma_x^2+\sigma_u^2}=\frac{1-R^2}{1-R^2+\kappa}\le\lambda .\tag{8}$$

**Worked numbers** ([[L05-10-python]] §4): $x^\ast=0.8x_2+r$, $\operatorname{Var}(r)=0.36$, $\sigma_u=0.75$: $\lambda_r=0.36/(0.36+0.5625)=0.390$, against
$\lambda=0.64$ without the control. "Generally, measurement error in a single variable causes inconsistency in all
estimators" (W p. 291): the other coefficients are biased too, in directions not easily derived.

![Left: the attenuation factor plim(beta-hat)/beta against the noise-to-signal ratio from 0 to 4, falling from 1 as 1/(1 + kappa), with lower dashed and dotted curves for controls that explain R² = 0.5 and 0.8 of the true regressor, a flat line at 1 for IV with an independent second measurement, and the point (1, 0.5) marked. Right: one seeded sample of 300 points with beta = 1, plotting y against the true x and against the noisy w, with fitted slopes 0.98 and 0.52](figures/L05-attenuation.png)
*Left: (4) and (8) as exact curves; right: a seeded illustration (not the slide's data, which has none). error-in-variables.pdf; W eqs. 9.33 and 9.36.*

On the left, attenuation depends only on the noise-to-signal ratio: at $\kappa=1$ half the slope is lost, at
$\kappa=4$ four fifths. Each control that soaks up signal pushes the curve down. On the right the noisy cloud is
**wider horizontally** than the true one (variance $1+1=2$ instead of 1) with the same vertical relation to the
signal, so the fitted line through it is flatter: 0.52 against 0.98 in this draw, plim 0.5.

---

## 4 · C — the cure: an instrument that is a second measurement (W §15.4, pp. 479–481; MHE p. 84)

Suppose a second report $w_2=x+u_2$ with $u_2$ independent of $u_1$, $x$ and $\varepsilon$. Use $w_2$ as an instrument for
$w_1=x+u_1$ (IV formula, W eq. 15.9; note 05):

$$\frac{\operatorname{Cov}(w_2,y)}{\operatorname{Cov}(w_2,w_1)}=\frac{\operatorname{Cov}(x+u_2,\ \beta x+\varepsilon)}{\operatorname{Cov}(x+u_2,\ x+u_1)}=\frac{\beta\sigma_x^2}{\sigma_x^2}=\beta .\tag{9}$$

The noise cancels because the two errors are independent: the instrument is correlated with the true signal
(relevance) and uncorrelated with the composite error $\varepsilon-\beta u_1$ (exogeneity). W's examples: parents' education
for a mismeasured `educ` (p. 480); two test scores as indicators of ability (Example 15.6, p. 481). MHE p. 84:
"Today, we are more likely to find IV used to address measurement error problems than to estimate the parameters of
an SEM"; Wald (1940) proposed the grouping estimator for exactly this problem (MHE footnote 8, p. 95). MHE p. 169
gives the panel version: Ashenfelter and Krueger (1994) instrument each twin's schooling with the brother's report.

> **Measurement error is endogeneity in disguise.** In (5) the regressor is correlated with its own error term,
> $\operatorname{Cov}(x_1,u-\beta_1e_1)=-\beta_1\sigma_{e_1}^2$ — exactly the condition note 05 handles with instruments.

---

## Links

- Neighbours: [[L05-03-omitted-variables-bad-control]] · [[L05-05-instrumental-variables]] (next: the IV estimator in general; (9) is its special case).
- Unit: [[L05-06-difference-in-differences]] (differencing removes fixed effects but amplifies measurement error: MHE p. 169) · [[L05-08-formulas]] · [[L05-09-pitfalls]] · [[L05-10-python]] §4.
- Class 1: [[../L01/L01-06-gaussian-linear-regression|L01 §6]] (OLS slope as $\operatorname{Cov}/\operatorname{Var}$).
- Rules pack: [[../../rules/01_endogeneidade_iv|rules/01]] (measurement error and attenuation bias).
- **Practice** (statements in the book): W 15.C3 (p. 492) and 15.C5 (p. 493) use the CARD data of note 05; W Example 15.6 (p. 481) is the worked two-indicator case.
