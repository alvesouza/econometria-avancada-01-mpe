---
tags: [notes, lecture-02, poisson-regression, glm, count-data, rate-ratio, overdispersion]
date: 2026-10-19
status: taught
source: "Gaussian-vs-Poisson-regression.html (Lopes, 27/10/2025; data from Albert & Hu 2020, Probability and Bayesian Modeling, §8.8): 28 daily blog-visitor counts, lm and glm(poisson) outputs; I §4.6 (pp. 167–173: eqs. 4.35–4.42, rate-ratio reading p. 171, mean–variance and non-negativity p. 172, footnote 5 on overdispersion); W §17.3 (pp. 543–546: eqs. 17.31–17.35, exp(β)−1 reading p. 544, σ̂² adjustment p. 546)"
---

# Gaussian-vs-Poisson-regression.html · Counts with a log link: the blog-visitor example, rate ratios and the mean–variance check

> **Claim.** A count is modelled as Poisson with $\log\lambda_i=x_i'\beta$, so a coefficient is a
> **rate ratio** $e^{\beta_j}$, fitted means are always positive, and the variance is tied to the
> mean. On the site's 28 days of blog visits, Gaussian and Poisson regressions on a weekend dummy
> give the **same fitted means** (109 and 83.33 visitors) because the model is saturated in two
> groups; they differ in the **variance they assume** — constant 140.4 vs equal to the mean — and
> therefore in their standard errors. The data are mildly overdispersed ($\hat\sigma^2=1.44$), which
> widens the Poisson SE by 20% and changes no conclusion.
> Prev: [[L02-05-discriminant-analysis]] · Next: [[L02-07-formulas]] · Map: [[L02-00-map]]

**Notation.**

- $y_i\in\{0,1,2,\dots\}$: visitors on day $i=1,\dots,28$ (June 2018).
- $w_i\in\{0,1\}$: the page's `weekend` dummy, $w_i=1$ for $t\le3$ (see §1).
- $\lambda_i=E(y_i\mid w_i)>0$: Poisson mean; $\alpha,\beta$: intercept and slope of $\log\lambda_i=\alpha+\beta w_i$ (the page's letters).
- $\beta_0,\beta_1$: OLS intercept and slope of the Gaussian model; $s$: its residual standard error.
- $n_0=16,\ S_0=1744$: number of weekdays and their total; $n_1=12,\ S_1=1000$: same for the weekend group.
- $\sigma^2$: dispersion factor in $\operatorname{Var}(y\mid x)=\sigma^2E(y\mid x)$ (W eq. 17.35).

---

## 1 · U — the data and the question

Visitors to a baseball-analytics blog, 28 consecutive days (the page's vector `y`):

`95 81 85 100 111 130 113 | 92 65 78 96 118 120 104 | 91 91 79 106 91 114 110 | 98 61 84 96 126 119 90`

The page labels the weekdays `fri, sat, sun, mon, tue, wed, thu` and sets `weekend = 1` for
$t\le3$ — **Friday, Saturday and Sunday** (1 June 2018 was a Friday). Group summaries (page output,
recomputed):

| group | days | total | mean | sd | variance | variance / mean |
|---|---|---|---|---|---|---|
| weekday (Mon–Thu), $w=0$ | 16 | 1744 | **109.00** | 12.15 | 147.73 | 1.36 |
| "weekend" (Fri–Sun), $w=1$ | 12 | 1000 | **83.33** | 11.42 | 130.42 | 1.57 |

The question: how much lower is traffic on weekend days, and how sure are we? A count is
non-negative, integer, and typically noisier when its mean is higher — three things the Gaussian
linear model ignores (I §4.6.1, pp. 167–169; W p. 543).

---

## 2 · C — the Gaussian regression

$$y_i=\beta_0+\beta_1w_i+\varepsilon_i,\qquad\varepsilon_i\sim N(0,\sigma_\varepsilon^2)\ \text{iid}.\tag{1}$$

**With one dummy, OLS reproduces the group means.** The normal equations
$\sum_i(y_i-\beta_0-\beta_1w_i)=0$ and $\sum_iw_i(y_i-\beta_0-\beta_1w_i)=0$ give, subtracting the second from the first,
$\sum_{w_i=0}(y_i-\beta_0)=0$, so $\hat\beta_0=S_0/n_0$; the second alone gives $\hat\beta_0+\hat\beta_1=S_1/n_1$:

$$\hat\beta_0=\frac{1744}{16}=109.000,\qquad\hat\beta_1=\frac{1000}{12}-109=83.333-109=-25.667 .$$

**Standard errors** (pooled residual variance, $28-2=26$ df). The page prints $s=11.85$:

$$\text{SE}(\hat\beta_1)=s\sqrt{\frac1{n_0}+\frac1{n_1}}=11.8495\sqrt{\frac1{16}+\frac1{12}}=11.8495\,(0.38188)=4.525,\qquad\text{SE}(\hat\beta_0)=\frac{s}{\sqrt{n_0}}=\frac{11.8495}{4}=2.962 .$$

$t=-25.667/4.525=-5.67$ ($p=5.8\times10^{-6}$), $R^2=0.553$ — all as printed. **Reading:**
weekend days have 25.7 fewer visitors, in absolute terms, with one common spread
$s^2=140.4$ for both groups.

---

## 3 · C — the Poisson regression

**Model** (I eqs. 4.35–4.37, pp. 169–170; W eqs. 17.31–17.32, p. 544):

$$y_i\mid w_i\sim\text{Poisson}(\lambda_i),\qquad P(y_i=k)=\frac{e^{-\lambda_i}\lambda_i^{\,k}}{k!},\qquad\log\lambda_i=\alpha+\beta w_i .\tag{2}$$

**Log-likelihood** (I eq. 4.38, p. 170; W eq. 17.33, p. 545). Take logs of the pmf and sum:

$$\ell(\alpha,\beta)=\sum_{i=1}^{28}\big[y_i\log\lambda_i-\lambda_i-\log y_i!\big]=\sum_{i=1}^{28}\big[y_i(\alpha+\beta w_i)-e^{\alpha+\beta w_i}-\log y_i!\big].\tag{3}$$

**Score.** Differentiate (3); $\partial e^{\alpha+\beta w_i}/\partial\alpha=\lambda_i$ and $\partial e^{\alpha+\beta w_i}/\partial\beta=w_i\lambda_i$:

$$\frac{\partial\ell}{\partial\alpha}=\sum_i(y_i-\lambda_i)=0,\qquad\frac{\partial\ell}{\partial\beta}=\sum_iw_i(y_i-\lambda_i)=0 .\tag{4}$$

In matrix form $X'(y-\lambda)=0$ — **the same shape as the logit score** (note 04 eq. 12): both
are canonical-link GLMs.

**Solve (4) in closed form.** The second equation involves only weekend days, where $\lambda_i=e^{\alpha+\beta}$:

$$S_1-n_1e^{\alpha+\beta}=0\ \Rightarrow\ e^{\hat\alpha+\hat\beta}=\frac{1000}{12}=83.333 .$$

Subtract it from the first; what remains are the weekdays, where $\lambda_i=e^{\alpha}$:

$$S_0-n_0e^{\alpha}=0\ \Rightarrow\ e^{\hat\alpha}=\frac{1744}{16}=109 .$$

Take logs:

$$\hat\alpha=\log109=\mathbf{4.69135},\qquad\hat\beta=\log\frac{83.333}{109}=\log0.764526=\mathbf{-0.26850},$$

the page's estimates. With no covariate at all, (4) would give $\hat\lambda=\bar y$ — the Poisson MLE of
[[../L01/L01-02-poisson-mle-properties|L01 §2]]; here each group gets its own $\bar y$.

**Hessian and standard errors.** Differentiate (4) again:

$$-\frac{\partial^2\ell}{\partial\theta\,\partial\theta'}=\sum_i\lambda_i\begin{pmatrix}1&w_i\\w_i&w_i\end{pmatrix}=\begin{pmatrix}n_0e^{\alpha}+n_1e^{\alpha+\beta}&n_1e^{\alpha+\beta}\\n_1e^{\alpha+\beta}&n_1e^{\alpha+\beta}\end{pmatrix}.$$

At the MLE, $n_0e^{\hat\alpha}=1744$ and $n_1e^{\hat\alpha+\hat\beta}=1000$:

$$\hat I=\begin{pmatrix}2744&1000\\1000&1000\end{pmatrix},\qquad|\hat I|=2744(1000)-1000^2=1{,}744{,}000,$$

$$\hat I^{-1}=\frac1{1{,}744{,}000}\begin{pmatrix}1000&-1000\\-1000&2744\end{pmatrix}\ \Rightarrow\ \text{SE}(\hat\alpha)=\sqrt{\frac{1}{1744}}=0.02395,\quad\text{SE}(\hat\beta)=\sqrt{\frac1{1744}+\frac1{1000}}=0.03967,$$

the printed 0.02395 and 0.03967: **each SE is built from the group totals alone**. $z=-0.26850/0.03967=-6.77$.
(The page's "Number of Fisher Scoring iterations: 4" is IRLS with $W=\operatorname{diag}(\lambda_i)$ and
$z_i=\eta_i+(y_i-\lambda_i)/\lambda_i$ — note 04 §4 with the log link.)

---

## 4 · C — reading the two slopes

**Gaussian:** additive, in visitors: $\hat\beta_1=-25.667$ per day.

**Poisson:** multiplicative. From (2), $\lambda(w=1)/\lambda(w=0)=e^{\alpha+\beta}/e^{\alpha}=e^{\beta}$ —
the **rate ratio** (I p. 171: "an increase in $X_j$ by one unit is associated with a change in $E(Y)$ by a factor of $\exp(\beta_j)$"):

$$e^{\hat\beta}=e^{-0.26850}=0.7645\quad\Rightarrow\quad\text{weekend traffic is }100(0.7645-1)=-23.5\%\text{ of weekday traffic.}$$

W's shortcut $100\hat\beta=-26.85\%$ (p. 544) is the log approximation; for a dummy the exact change
is $100[\exp(\hat\beta)-1]=-23.55\%$ (same page), and at $|\beta|\approx0.27$ the two differ by 3.30 points.

**Same means, different variance.** The page's comparison table:

| model | weekday mean | weekend mean |
|---|---|---|
| Gaussian: $\hat\beta_0$, $\hat\beta_0+\hat\beta_1$ | 109.0000 | 83.333 |
| Poisson: $e^{\hat\alpha}$, $e^{\hat\alpha+\hat\beta}$ | 109.0002 | 83.33345 |

(The fourth-decimal gaps come from exponentiating the five-decimal printed coefficients.) With
**two groups and two parameters both models are saturated in the means**; what differs is the
variance each assumes, hence $t=-5.67$ vs $z=-6.77$:

| | Gaussian (1) | Poisson (2) |
|---|---|---|
| $\operatorname{Var}(y\mid w=0)$ | $s^2=140.4$ | $\lambda=109$ |
| $\operatorname{Var}(y\mid w=1)$ | $s^2=140.4$ | $\lambda=83.3$ |
| fitted values | can be negative in general | always $>0$ (I p. 172) |
| slope reading | $-25.7$ visitors | $\times0.7645$ ($-23.5\%$) |

---

## 5 · C — the mean–variance check and overdispersion

**The Poisson model says $\operatorname{Var}(y\mid x)=E(y\mid x)$** (W eq. 17.34, p. 545; I p. 172).
The sample says 147.7 vs 109 and 130.4 vs 83.3 — ratios 1.36 and 1.57.

**Dispersion estimate** (W p. 546): $\hat\sigma^2=\frac1{n-k-1}\sum_i\hat u_i^2/\hat y_i$ with $\hat u_i=y_i-\hat\lambda_i$,
i.e. the Pearson $\chi^2$ over its df:

$$\hat\sigma^2=\frac{37.546}{26}=1.444,\qquad\hat\sigma=1.202 .$$

**Quasi-Poisson correction** (W eq. 17.35 and p. 546): multiply the SEs by $\hat\sigma$:

$$\text{SE}_Q(\hat\beta)=1.202(0.03967)=0.0477,\qquad z_Q=\frac{-0.26850}{0.0477}=-5.63 .$$

**Deviance view.** Residual deviance 38.324 on 26 df (ratio 1.47); $P(\chi^2_{26}>38.324)=0.056$ —
borderline evidence of lack of fit. The LR test of the weekend effect: $85.141-38.324=46.82$ on 1 df
(W eq. 17.12; under (17.35) divide by $\hat\sigma^2$: $46.82/1.444=32.4$). AIC 221.76.

![Left: the 28 daily counts by day with weekday and Friday-to-Sunday markers, the common fitted step function 109/83.3, the constant-width Gaussian band and the mean-dependent Poisson band; right: group variance against group mean with the lines Var = mean, Var = 1.444 mean and Var = 140.4](figures/L02-gaussian-vs-poisson-fit.png)
*Left: both models fit the same step; the bands (±1.96 sd) differ. Right: the two groups' (mean, variance) against each model's variance function. Data and outputs: Gaussian-vs-Poisson-regression.html.*

On the left the Gaussian band has the same width in both groups, while the Poisson band is
narrower for the lower weekend mean ($\sqrt{83.3}=9.1$ vs $\sqrt{109}=10.4$); the weekday 130 and
the weekend 65 and 61 sit outside the Poisson band ($109\pm20.5$ and $83.3\pm17.9$) — three of 28 where
about 1.4 are expected, which is the overdispersion. On the
right both sample points lie **above** the Poisson line Var = mean and close to the quasi-Poisson
line $1.444\lambda$; the Gaussian constant 140.4 sits between them.

> **With means near 100 the Poisson and Gaussian models nearly agree** — a Poisson with a large
> mean is close to a normal. The log link earns its keep with **small counts**, where linear fits go
> negative (9.6% of I's Bikeshare fitted values, p. 168) and the variance visibly grows with the
> mean (I p. 172, recalling Fig. 4.14). **And Poisson SEs are only right if Var = mean**: always check,
> and inflate by $\hat\sigma$ when it fails (I footnote 5, p. 172: overdispersion "causes the Z-values to be inflated").

---

## 6 · G — one template for linear, logistic and Poisson regression (I §4.6.3, pp. 172–173)

$$\eta\big(E(Y\mid X)\big)=\beta_0+\beta_1X_1+\dots+\beta_pX_p\qquad\text{(I eq. 4.42, p. 173)}$$

| model | distribution | link $\eta(\mu)$ | variance function | score | note |
|---|---|---|---|---|---|
| linear | Gaussian | $\mu$ | $\sigma^2$ (constant) | $X'(y-X\beta)/\sigma^2$ | [[../L01/L01-06-gaussian-linear-regression\|L01 §6]] |
| logistic | Bernoulli | $\log\{\mu/(1-\mu)\}$ | $\mu(1-\mu)$ | $X'(y-\pi)$ | [[L02-04-logistic-regression]] |
| Poisson | Poisson | $\log\mu$ | $\mu$ | $X'(y-\lambda)$ | this note |

Each link is the **canonical** one for its distribution, which is why the score is always
"$X'$(data − fitted mean)" and why Newton–Raphson, Fisher scoring and IRLS coincide.

---

## 7 · G — the page's Bayesian part, named only

The page continues with independent normal priors $\alpha\sim N(4.7,0.1^2)$, $\beta\sim N(-0.3,0.1^2)$,
a grid posterior and sampling–importance resampling (SIR), ending with posterior densities of the
weekday and weekend rates. **Classes 3+4** (`rules/07_bayes.md`, `rules/08_monte_carlo_mcmc.md`).

---

## Links

- Neighbours: [[L02-05-discriminant-analysis]] · [[L02-07-formulas]] (next).
- Unit: [[L02-00-map]] · [[L02-01-prediction-error-bias-variance]] · [[L02-02-linear-log-linear-regression]] (log-level readings; here the log is on the *mean*, not on $y$) · [[L02-03-cross-validation-motorcycle]] · [[L02-04-logistic-regression]] (same score, same IRLS) · [[L02-08-pitfalls]] · [[L02-09-python]] (Poisson GLM via statsmodels with asserts).
- Class 1: [[../L01/L01-02-poisson-mle-properties|L01 §2]] (Poisson MLE $\hat\lambda=\bar y$, Fisher information $n/\lambda$ — here $\text{SE}(\hat\alpha)=1/\sqrt{S_0}$ is the same object on the log scale) · [[../L01/L01-03-coal-mining-change-point|L01 §3]] (overdispersion test on counts).
- Later: GLMs again in Class 7 (`Map/class-plan.md`).
- Rules pack: [[../../rules/06_classificacao_validacao|rules/06]].
- **Practice** (statements in the book): W 17.C4 (p. 561), W 17.C5 (p. 561).
