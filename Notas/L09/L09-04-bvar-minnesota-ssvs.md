---
tags: [notes, lecture-09, bvar, minnesota-prior, shrinkage, normal-wishart, ssvs, variable-selection, large-var]
date: 2026-10-25
status: taught
source: "BVAR-part11.pdf slides 13–16 (simulated VAR(2) posterior summaries), 22 (prior shrinkage, β = vec(B′)), 23 (Minnesota prior), 24 (specifying V_i0), 25–26 (other priors and their posteriors), 27–30 (Kadiyala–Karlsson example and conclusions), 45 (dimensionality); BVAR-part2.pdf slides 3–4 (why variable selection), 5–10 (ON/OFF switch, full conditionals), 11–13 (SSVS, semi-automatic default, prior on Ψ), 50 (Carriero et al.), 56–58 and 60 (Bańbura, Giannone and Reichlin 2010: data sets, Table II, Figure 1); Greenberg 1e §9.1 (pp. 134–137) for the conditionally conjugate Normal/Wishart algebra"
---

# Slides 22–30 and Part 2 slides 3–13, 56–60 · The Minnesota prior: shrink every equation toward a random walk, tighter for distant lags and other variables, and the posterior is ridge regression in closed form

> **Claim.** The Minnesota prior puts $\beta_i\sim N(\beta_{i0},V_{i0})$ on each equation, centred
> on a random walk (own first lag 1, everything else 0), with prior sd $\lambda/k$ on own lag $k$
> and $\theta\lambda\sigma_i/(k\sigma_j)$ on variable $j$'s lag $k$. With $\Sigma$ diagonal and
> known, **the posterior is equation-by-equation Gaussian:**
> $\bar V_i=(V_{i0}^{-1}+X'X/\sigma_i^2)^{-1}$, $\bar\beta_i=\bar V_i(V_{i0}^{-1}\beta_{i0}+X'y^{(i)}/\sigma_i^2)$ —
> a precision-weighted average of the prior centre and OLS. **$\lambda$ is the dial**: $\lambda\to0$
> returns the random walk, $\lambda\to\infty$ returns OLS. Large VARs work because $\lambda$ is
> tightened as the number of variables grows (Bańbura et al.).

Prev: [[L09-03-structural-var]] · Next: [[L09-05-factor-models-favar]] · Map: [[L09-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $\beta_i$ | coefficients of equation $i$ (constant, then lags), row $i$ of $(\mu,B)$; $\beta=(\beta_1',\dots,\beta_q')'$ (slide 22) | |
| $\beta_{i0},\ V_{i0}$ | prior mean and (diagonal) prior covariance of $\beta_i$ | |
| $\lambda$ | overall tightness | $>0$ |
| $\theta$ | relative tightness of other variables' lags | $(0,1]$ |
| $k$ | lag index | $1,\dots,p$ |
| $\sigma_i^2$ | error variance of equation $i$, fixed and known ($\Sigma=\mathrm{diag}(\sigma_1^2,\dots,\sigma_q^2)$, slide 24) | $>0$ |
| $X$, $y^{(i)}$ | common regressor matrix, equation $i$'s response vector | |
| $\bar\beta_i,\ \bar V_i$ | posterior mean and covariance | |
| $\gamma_j$ | inclusion indicator of coefficient $j$ (SSVS) | $\{0,1\}$ |

---

## 1 · U — why shrink

Part 2, slide 3: "VAR flexibility → over-parameterization → poor forecasts. First solution:
Minnesota prior of Doan et al. (1984)." The count is in [[L09-01-var-p-estimation-forecasting]] §8:
Kadiyala–Karlsson's 7-variable VAR(6) has 43 coefficients per equation and 133 observations. OLS
is unbiased and useless; a prior that says "most of these are small, and distant lags are
smaller" trades a little bias for a lot of variance — the MSE trade of
[[../L01/L01-05-comparing-estimators-mse-bootstrap|L01-05]] and the bias–variance logic of
[[../L02/L02-01-prediction-error-bias-variance|L02-01]], with the prior as the regulariser.

---

## 2 · C — the Minnesota prior (slides 23–24)

Litterman's (1980, 1986) prior (slide 23): $\beta_i\sim N(\beta_{i0},V_{i0})$, "with $V_{i0}$ chosen to
'center' the individual equations around the random walk with drift"

$$y_{ti}=\mu_i+y_{t-1,i}+u_{ti}.\tag{1}$$

**Prior mean.** Coefficient on own first lag $=1$; all other lag coefficients $=0$; the constant
gets a flat (very large variance) prior.

**Prior variances** (slide 24; $V_{i0}$ diagonal):

$$\mathrm{Var}\big(B_k(i,i)\big)=\frac{\lambda^2}{k^2},\qquad\mathrm{Var}\big(B_k(i,j)\big)=\frac{\theta^2\lambda^2}{k^2}\times\frac{\sigma_i^2}{\sigma_j^2},\quad j\ne i.\tag{2}$$

Read each factor:

| Factor | What it encodes (slide 23) |
|---|---|
| $\lambda$ | how far any coefficient may stray from the random walk |
| $1/k^2$ | "shrinking the number of lags $p$ towards one": the prior sd falls like $1/k$ |
| $\theta<1$ | "own lags should explain more of the variation than the lags of other variables" |
| $\sigma_i^2/\sigma_j^2$ | units: $B_k(i,j)$ converts $y_j$ into $y_i$, so its scale is $\sigma_i/\sigma_j$ |

"Shrinking the diagonal elements of $B_1$ toward one, shrinking the remaining coefficients of
$B_1,\dots,B_p$ toward zero" (slide 23). In practice $\sigma_i^2$ is replaced by the residual variance
of a univariate AR($p$) for series $i$ (Litterman's convention), which is what "fixed and known"
amounts to.

---

## 3 · C — the closed-form posterior

**Factorisation.** With $\Sigma$ diagonal, the VAR likelihood ([[L09-01-var-p-estimation-forecasting]] (6))
splits by equation:

$$p(Y\mid\beta)\propto\prod_{i=1}^q\exp\Big\{-\frac{1}{2\sigma_i^2}(y^{(i)}-X\beta_i)'(y^{(i)}-X\beta_i)\Big\}.\tag{3}$$

The prior is independent across equations, so the posterior is too: $p(\beta\mid Y)=\prod_ip(\beta_i\mid y^{(i)})$.

**One equation.** Drop the index $i$. Minus twice the log posterior kernel:

$$-2\log p(\beta\mid y)=\frac{(y-X\beta)'(y-X\beta)}{\sigma^2}+(\beta-\beta_0)'V_0^{-1}(\beta-\beta_0)+c.\tag{4}$$

Expand both quadratics and collect powers of $\beta$:

$$=\beta'\Big(\frac{X'X}{\sigma^2}+V_0^{-1}\Big)\beta-2\beta'\Big(\frac{X'y}{\sigma^2}+V_0^{-1}\beta_0\Big)+c'.\tag{5}$$

Name $\bar V^{-1}=X'X/\sigma^2+V_0^{-1}$ and $\bar\beta=\bar V(X'y/\sigma^2+V_0^{-1}\beta_0)$; then (5) is

$$(\beta-\bar\beta)'\bar V^{-1}(\beta-\bar\beta)-\bar\beta'\bar V^{-1}\bar\beta+c',\tag{6}$$

a Gaussian kernel in $\beta$:

$$\boxed{\beta_i\mid y\sim N(\bar\beta_i,\bar V_i),\qquad\bar V_i=\Big(V_{i0}^{-1}+\frac{X'X}{\sigma_i^2}\Big)^{-1},\qquad\bar\beta_i=\bar V_i\Big(V_{i0}^{-1}\beta_{i0}+\frac{X'y^{(i)}}{\sigma_i^2}\Big)}\tag{7}$$

(slide 26, row "Minnesota": $\gamma_i\mid y\sim N(\tilde\gamma_i,\tilde\Sigma_i)$). Substituting
$X'y^{(i)}=X'X\hat\beta_i$ (the OLS normal equations) into (7):

$$\bar\beta_i=\bar V_i\Big(V_{i0}^{-1}\beta_{i0}+\frac{X'X}{\sigma_i^2}\hat\beta_i\Big),\tag{8}$$

a **matrix-weighted average** of the prior mean and OLS, with weights the two precisions (which
sum to $\bar V_i^{-1}$). It is generalised ridge regression: ridge with penalty $\sigma_i^2V_{i0}^{-1}$
centred at $\beta_{i0}$ instead of 0 (ridge itself is Classes 3+4).

**The two limits in $\lambda$.** By (2), $V_{i0}\propto\lambda^2$ entrywise (except the constant).

- $\lambda\to0$: $V_{i0}^{-1}\to\infty$, $\bar V_i\to V_{i0}\to0$, and $\bar\beta_i\to\beta_{i0}$ — **the random walk** (1).
- $\lambda\to\infty$: $V_{i0}^{-1}\to0$, $\bar V_i\to\sigma_i^2(X'X)^{-1}$, and $\bar\beta_i\to\hat\beta_i$ — **OLS**, with the frequentist covariance.

**The scalar case** shows the weight. One regressor with $\sum_tx_t^2=s_{xx}$, prior $N(b_0,v_0)$:

$$\bar b=\frac{v_0^{-1}b_0+(s_{xx}/\sigma^2)\hat b}{v_0^{-1}+s_{xx}/\sigma^2}=w\,b_0+(1-w)\hat b,\qquad w=\frac{\sigma^2/s_{xx}}{\sigma^2/s_{xx}+v_0}=\frac{\mathrm{Var}(\hat b)}{\mathrm{Var}(\hat b)+v_0}.\tag{9}$$

**The prior wins in proportion to how noisy OLS is relative to the prior variance.** Distant
lags ($v_0=\lambda^2/k^2$ small) and short samples ($s_{xx}$ small) shrink most.

### 3.1 · Worked — the slide-13 VAR(2), 58 observations

A seeded simulation (seed 9; 200 burn-in, 60 kept, $p=2$ leaves $T=58$) from slide 13's
$\mu,B_1,B_2,\Sigma$ ([[L09-01-var-p-estimation-forecasting]] §5.1). Univariate AR(2) residual
variances: $\hat\sigma^2=(0.266,\ 0.126,\ 0.805)$ (true diagonal $0.26,\ 0.09,\ 0.81$). Prior with
$\theta=0.5$ (the slides give no value; 0.5 is illustrative), constant variance $10^6$.

**Prior sds for equation 1 at $\lambda=0.2$**, by (2):

| coefficient | formula | value |
|---|---|---|
| own lag 1, $B_1(1,1)$ | $\lambda/1$ | 0.200 |
| own lag 2, $B_2(1,1)$ | $\lambda/2$ | 0.100 |
| $B_1(1,2)$ | $\theta\lambda\,\sigma_1/\sigma_2=0.5(0.2)\sqrt{0.266/0.126}=0.1(1.455)$ | 0.145 |
| $B_1(1,3)$ | $0.5(0.2)\sqrt{0.266/0.805}=0.1(0.575)$ | 0.057 |

**Posterior means of equation 1** by (7) (computed in [[L09-10-python]] §4):

| | $B_1(1,1)$ | $B_1(1,2)$ | $B_1(1,3)$ | $B_2(1,1)$ |
|---|---|---|---|---|
| truth (slide 13) | 0.7 | 0.1 | 0.0 | −0.2 |
| prior mean | 1 | 0 | 0 | 0 |
| $\lambda=0.05$ | 0.926 | 0.000 | −0.010 | −0.018 |
| $\lambda=0.2$ | 0.690 | 0.055 | −0.043 | −0.115 |
| $\lambda=1$ | 0.649 | 0.284 | −0.038 | −0.262 |
| OLS ($\lambda\to\infty$) | 0.647 | 0.379 | −0.021 | −0.292 |

With 58 observations OLS puts 0.379 on $B_1(1,2)$ (truth 0.1); at $\lambda=0.2$ the posterior
mean is 0.055 — **closer to the truth than OLS** for that coefficient, and the own-lag
coefficient 0.690 is within 0.01 of 0.7. At $\lambda=0.05$ the prior wins everywhere and the
own lag sits at 0.926, near the random walk.

![Left: prior standard deviation against lag k for own lags (lambda over k) and other variables' lags (theta lambda over k) at lambda 0.2 and 0.4; right: posterior means of four coefficients of equation 1 against lambda on a log scale, moving from the prior values 1 and 0 at small lambda to the OLS values (dotted) at large lambda](figures/L09-minnesota-shrinkage.png)
*Figure — left: prior sds (2) with $\theta=0.5$, $\sigma_i=\sigma_j$; right: posterior means (7) for equation 1 against $\lambda$, seeded simulation from the slide-13 VAR(2), $T=58$; dotted lines are OLS.*

The left panel is the prior's shape: sds fall like $1/k$ and cross-variable lags sit at half the
own-lag sd. On the right, the transition happens between $\lambda\approx0.03$ and $\lambda\approx1$;
each coefficient leaves its prior value at its own $\lambda$, where its data precision overtakes
its prior precision ((9): $w=1/2$ when $\mathrm{Var}(\hat b)=v_0$) — the own lags first, $B_1(1,2)$
last. **Choosing $\lambda$ is choosing where on these curves to stand**;
Bańbura et al. choose it by in-sample fit relative to the cross-section (§6).

---

## 4 · C — other priors on $(B,\Sigma)$ (slides 25–26)

Kadiyala and Karlsson (1993, 1997) extend the Minnesota prior (slide 25), which fixes $\Sigma$.
In slide 26's notation ($\Gamma$ = coefficient matrix, $Z$ = regressors, $\Psi$ = error covariance,
$m$ = number of series):

| Prior | Prior | Posterior |
|---|---|---|
| Minnesota | $\gamma_i\sim N(\tilde\gamma_i,\tilde\Sigma_i)$, $\Psi$ fixed and diagonal | $\gamma_i\mid y\sim N(\bar\gamma_i,\bar\Sigma_i)$ — (7) |
| Diffuse (Jeffreys) | $p(\gamma,\Psi)\propto\lvert\Psi\rvert^{-(m+1)/2}$ | $\Gamma\mid y\sim MT\big(Z'Z,(Y-Z\hat\Gamma)'(Y-Z\hat\Gamma),\hat\Gamma,T-k\big)$ |
| Normal-Wishart | $\gamma\mid\Psi\sim N(\tilde\gamma,\Psi\otimes\tilde\Omega)$, $\Psi\sim iW(\tilde\Psi,\alpha)$ | $\Gamma\mid y\sim MT(\bar\Omega^{-1},\bar\Psi,\bar\Gamma,T+\alpha)$ |
| Normal-Diffuse | $\gamma\sim N(\tilde\gamma,\tilde\Sigma)$, $p(\Psi)\propto\lvert\Psi\rvert^{-(m+1)/2}$ | no closed form (kernel on slide 26) → Gibbs |
| Extended Natural Conjugate | slide 26 | slide 26 |

**The diffuse case, derived** (it is the site's band recipe). Multiply the likelihood
([[L09-01-var-p-estimation-forecasting]] (6), (10)) by $|\Sigma|^{-(q+1)/2}$:

$$p(B,\Sigma\mid Y)\propto|\Sigma|^{-(n+q+1)/2}\exp\Big\{-\tfrac12\mathrm{tr}\big(\Sigma^{-1}S(\hat B)\big)\Big\}\exp\Big\{-\tfrac12\mathrm{tr}\big(\Sigma^{-1}(\hat B-B)X'X(\hat B-B)'\big)\Big\}.\tag{10}$$

For fixed $\Sigma$ the second exponential is the matrix-normal kernel, i.e.

$$\mathrm{vec}(B')\mid\Sigma,Y\sim N\big(\mathrm{vec}(\hat B'),\ \Sigma\otimes(X'X)^{-1}\big),\tag{11}$$

whose normalising constant is $\propto|\Sigma|^{k/2}$ ($k$ = regressors per equation). Integrating
$B$ out of (10) leaves $|\Sigma|^{-(n-k+q+1)/2}\exp\{-\frac12\mathrm{tr}(\Sigma^{-1}S(\hat B))\}$:

$$\Sigma\mid Y\sim IW\big(S(\hat B),\ n-k\big).\tag{12}$$

Drawing $\Sigma$ from (12) then $B$ from (11) is exact posterior simulation; the site's
VAR-Example bands fix $\Sigma=\hat\Sigma$ and draw only (11). Part 2 slides 8–9 give the same pair
as full conditionals ($\beta\mid\Sigma,y\sim N(\mu_1,V_1)$ with $V_1^{-1}=V_0^{-1}+\sum_t\tilde z_t'\Sigma^{-1}\tilde z_t$;
$\Sigma\mid\beta,y\sim IW(T,S)$), and Greenberg's SUR Gibbs sampler (Algorithm 9.1, p. 137) is the
general version with equation-specific regressors.

**Why Normal-Wishart cannot be Minnesota.** In $\Psi\otimes\tilde\Omega$ the prior covariance of
equation $i$'s coefficients is $\psi_{ii}\tilde\Omega$: the **same** relative tightness across
regressors in every equation. Minnesota's $\theta<1$ makes "own" and "other" depend on the
equation, which a Kronecker product cannot do — so NW imposes $\theta=1$. Kadiyala–Karlsson's
verdict (slide 30): "our preferred choice is the Normal-Wishart when the prior beliefs are of the
Litterman type", and "for more general prior beliefs ... the Normal-Diffuse and EN priors are
strong alternatives".

**The K&K example** (slides 27–29): Litterman's seven US series (RGNPG, INFLA, UNEMP, M1, INVEST,
CPRATE, CBI), quarterly 1948:1–1981:1, out-of-sample 1980:2–1986:4, $q=7$, $p=6$, 301 parameters;
RMSE comparison on slide 29 (figure).

---

## 5 · C — variable selection: the ON/OFF switch and SSVS (Part 2, slides 5–13)

**ON/OFF switch** (slides 5–6). Write the VAR as a SUR, $y_t=z_t\beta+u_t$ with
$z_t=I_q\otimes(y_{t-1}',\dots,y_{t-p}')$ ($q\times s$, $s=q^2p$), and switch coefficients with
$\Gamma=\mathrm{diag}(\gamma_{11},\dots,\gamma_{q,pq})$: $y_t=z_t\Gamma\beta+u_t$, so $B_{ij}=0$ when
$\gamma_{ij}=0$. "$2^s$ VAR models: variable selection = model selection." Priors (slide 7):
$\beta\sim N(0,V_0)$, $p(\Sigma)\propto|\Sigma|^{-(q+1)/2}$, $\gamma_j\mid\gamma_{-j}\sim\mathrm{Bernoulli}(\pi_{0j})$.
Gibbs full conditionals (slides 8–10): with $\tilde z_t=z_t\Gamma$, $\beta$ is Normal (as above),
$\Sigma$ is inverse Wishart, and

$$\gamma_j\mid\gamma_{-j},\beta,\Sigma,y\sim\mathrm{Bernoulli}\Big(\frac{A_j}{A_j+B_j}\Big),\quad A_j=p(y\mid\beta,\Sigma,\gamma_{-j},\gamma_j=1)\pi_{0j},\quad B_j=p(y\mid\beta,\Sigma,\gamma_{-j},\gamma_j=0)(1-\pi_{0j})\tag{13}$$

(the slide prints "$\gamma_j=1$" inside $B_j$ too; it must be $\gamma_j=0$).

**SSVS** (slides 11–12; George and McCulloch 1993, 1997; Jochmann et al. 2011). Instead of an
exact zero, a **spike-and-slab** prior:

$$\beta_j\mid\gamma_j\sim(1-\gamma_j)N(0,\tau_{0j}^2)+\gamma_jN(0,\tau_{1j}^2),\qquad\gamma_j\sim\mathrm{Bernoulli}(q_j),\tag{14}$$

$\tau_{0j}^2$ small ("coefficient is virtually zero"), $\tau_{1j}^2$ large ("relatively non-informative").
Default semi-automatic choice (George et al. 2008, slide 12): $\tau_{kj}=c_k\cdot\widehat{\mathrm{var}}(\beta_j)$
from an unrestricted VAR, $c_0\ll c_1$; Jochmann et al. set $c_0=0.1$, $c_1=10$. Here $\gamma_j$ given
$\beta_j$ needs only the two densities. By Bayes:

$$P(\gamma_j=1\mid\beta_j)=\frac{q_j\,\phi(\beta_j;0,\tau_{1j}^2)}{q_j\,\phi(\beta_j;0,\tau_{1j}^2)+(1-q_j)\,\phi(\beta_j;0,\tau_{0j}^2)}.\tag{15}$$

**Worked.** Take $q_j=\tfrac12$ and read the $\tau$'s as $c_0=0.1$ and $c_1=10$ times a
coefficient's OLS standard error $s_j$; write $z=\beta_j/s_j$. With $\phi(\beta;0,(cs)^2)=\frac1{cs}\phi(z/c)$,
the $s$ cancels in (15):

$$P(\gamma_j=1\mid z)=\frac{0.1\,\phi(z/10)}{0.1\,\phi(z/10)+10\,\phi(10z)}.$$

At $z=0.2$: $0.1\phi(0.02)=0.1(0.39886)=0.039886$, $10\phi(2)=10(0.053991)=0.53991$, so
$P=0.039886/0.579796=0.069$. At $z=0.5$: $10\phi(5)=10(1.4867\times10^{-6})=1.4867\times10^{-5}$,
so $P=0.039844/(0.039844+0.0000149)=0.9996$. The two densities cross where
$\frac{z^2}2(c_0^{-2}-c_1^{-2})=\ln(c_1/c_0)$:

$$z^*=\sqrt{\frac{2\ln(c_1/c_0)}{c_0^{-2}-c_1^{-2}}}=\sqrt{\frac{2\ln100}{100-0.01}}=\sqrt{\frac{9.2103}{99.99}}=0.3035.$$

**A draw of $\beta_j$ beyond 0.30 OLS standard errors is classified "in" almost surely** — the spike
is so narrow that SSVS keeps far more than a $t$-test at 1.96 would. The ratio $c_1/c_0$, not a
significance level, sets the threshold.

**Prior on $\Psi$** (slide 13): with $\Sigma^{-1}=\Psi\Psi'$ ($\Psi$ lower triangular, the Cholesky
root of the precision), $\psi_{jj}^2\sim G(a_j,b_j)$ and spike-and-slab on the off-diagonal
$\psi_{ij}$ — the same idea applied to contemporaneous correlations.

---

## 6 · C — large BVARs work (Part 2, slides 50, 56–60)

- **Carriero, Kapetanios and Marcellino (2009)**, $q=33$ exchange rates against the dollar: the BVAR
  improves on the random walk for most rates, gains "typically in the range of 2%–3%", "6%–9%" for
  euro–dollar and pound–dollar; a trading rule on BVAR forecasts beats the RW (slide 50).
- **Bańbura, Giannone and Reichlin (2010)** (slides 56–60): "When the degree of shrinkage is set in
  relation to the cross-sectional dimension, the forecasting performance of small monetary VARs can
  be improved by adding additional macroeconomic variables and sectoral information"; "Large VARs
  with shrinkage produce credible impulse responses". Data: SMALL (3), CEE (7), MEDIUM (20), LARGE
  (131 Stock–Watson indicators).

Table II (slide 58), MSFE relative to a random walk with drift, 1971–2003, $h=1$:

| | SMALL $p=13$ OLS | SMALL BVAR | CEE $p=13$ OLS | CEE $p$=BIC | CEE BVAR | LARGE BVAR |
|---|---|---|---|---|---|---|
| EMPL | 1.14 | 1.14 | **7.56** | 0.76 | 0.67 | **0.46** |
| CPI | 0.89 | 0.89 | 5.61 | 0.55 | 0.52 | 0.50 |
| FFR | 1.86 | 1.86 | 6.39 | 1.21 | 0.89 | 0.75 |

Unshrunk OLS with 13 lags in 7 variables forecasts employment with **7.56 times** the RW's MSFE;
the BVAR with all 131 variables reaches 0.46. More variables help **only with shrinkage**. Figure 1
(slide 60): the responses to a monetary-policy shock (employment falls, the federal funds rate
jumps then decays) keep their shape from SMALL to LARGE, with the prior on the sum of coefficients
($\tau=10\lambda$) added. FAVAR comparisons (Table III) are in [[L09-05-factor-models-favar]] §6.

---

## 7 · U — Python

(7) is ten lines of NumPy (`minnesota_posterior` in `figures/make_figures.py`, reused in
[[L09-10-python]] §4). No PyMC is needed for the Minnesota or diffuse cases: (7), (11)–(12) are
exact. The Normal-Diffuse prior and SSVS need a Gibbs loop over (13)/(15) and the Normal/IW
conditionals — the same loop structure as Greenberg's Algorithm 9.1.

---

## Links

- Neighbours: [[L09-03-structural-var]] · [[L09-05-factor-models-favar]] (the other answer to dimensionality).
- Earlier units: [[../L01/L01-04-first-bayesian-poisson|L01-04]] (a first prior pulling an MLE) · [[../L01/L01-05-comparing-estimators-mse-bootstrap|L01-05]] (biased but lower MSE) · [[../L02/L02-01-prediction-error-bias-variance|L02-01]] (bias–variance).
- Unit: [[L09-00-map]] · [[L09-08-formulas]] · [[L09-09-pitfalls]] · [[L09-10-python]].
- Rules: [[../../rules/05_espaco_estados_volatilidade|rules/05]].
- **Practice (number and printed page only):** G 10.4 (p. 167) — the SUR Gibbs structure of §4–§5 with autocorrelated errors.
