---
tags: [notes, lecture-09, multivariate-volatility, ewma, dcc, factor-stochastic-volatility, garch, time-varying-correlation]
date: 2026-10-25
status: taught
source: "BVAR-part2.pdf slides 38 (factor stochastic volatility, Pitt and Shephard 1999), 39 (correlated factor volatilities, Aguilar and West 2000), 40 (time-varying loadings, Lopes and Carvalho 2007), 41–43 (daily exchange rates, k = 3); sv-fsv-US-BR.html (SV-AR(1) via stochvol, rolling correlations, factanal, fsvsample on six stocks); wti-sp500-timevaryingcovariance.html (SVLT-AR(1), FSV(1), dccPre GARCH(1,1)-t, dccFit Tse–Tsui and Engle, MCHdiag); Tsay AFTS 3e §10 intro and §10.1 (pp. 506–507, eq. 10.2), §10.3.1 (p. 516, eq. 10.7), §10.4.3 (pp. 531–532), §10.6 (p. 543)"
---

# Part 2 slides 38–43 and the two site pages · Time-varying covariances: DCC models the correlations directly, factor SV gets them from the factor's volatility

> **Claim.** A $k$-dimensional conditional covariance has $k(k+1)/2$ moving entries, so every
> usable model imposes structure. **DCC** splits $\Sigma_t=D_tR_tD_t$: univariate GARCH for $D_t$,
> then one scalar recursion with two parameters for all the correlations. **Factor SV** keeps
> $y_t=\beta f_t+\varepsilon_t$ and lets the factor and idiosyncratic log-variances follow AR(1)s;
> then $\Sigma_t=\beta H_t\beta'+\Sigma_t^{\varepsilon}$ and, with one factor,
> $\rho_{ij,t}=\mathrm{sign}(\beta_i\beta_j)/\sqrt{(1+a_{it}/h_t)(1+a_{jt}/h_t)}$: **correlations rise
> exactly when the common factor is volatile** — a prediction, not a free parameter. On the site's
> W&T Offshore / S&P 500 data, the DCC correlation shock has a half-life of 7 days (Engle) or 2
> days (Tse–Tsui), and the S&P GARCH persistence is above one.

Prev: [[L09-06-tvp-var-sv-state-space]] · Next: [[L09-08-formulas]] · Map: [[L09-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $a_t$ | $k\times1$ return innovation, $E(a_t\mid F_{t-1})=0$ | |
| $\Sigma_t=\mathrm{Cov}(a_t\mid F_{t-1})$ | conditional covariance | p.d. |
| $D_t=\mathrm{diag}(\sigma_{11,t}^{1/2},\dots,\sigma_{kk,t}^{1/2})$ | conditional sds | |
| $R_t$ ($\rho_t$ in Tsay) | conditional correlation matrix | unit diagonal |
| $\varepsilon_t=D_t^{-1}a_t$ | standardised innovations | |
| $\theta_1,\theta_2$ | DCC scalars | $\ge0$, $\theta_1+\theta_2<1$ |
| $\lambda$ | EWMA decay | $(0,1)$ |
| $f_t,\ \beta$ | factors and loadings (as in [[L09-05-factor-models-favar]]) | |
| $h_t=\sigma^2_{p+1,t}$ | factor variance (one factor), $\lambda_t=\log h_t$ | $>0$ |
| $\sigma_{it}^2$, $\eta_{it}=\log\sigma_{it}^2$ | idiosyncratic variances and log-variances | |
| $a_{it}=\sigma_{it}^2/\beta_i^2$ | idiosyncratic-to-loading ratio | $\ge0$ |

---

## 1 · C — the problem (T p. 506)

"Multivariate volatility modeling is concerned with the time evolution of $\Sigma_t$ ... the curse of
dimensionality quickly becomes a major obstacle in applications because there are $k(k+1)/2$
quantities in $\Sigma_t$ for a $k$-dimensional return series. To illustrate, there are 15
conditional variances and covariances in $\Sigma_t$ for a five-dimensional return series." The
full VEC/VAR-GARCH ([[L09-06-tvp-var-sv-state-space]] (1)) gives each of them its own equation;
everything below is a way not to.

---

## 2 · C — the exponentially weighted benchmark (T §10.1, eq. 10.2, p. 506)

$$\hat\Sigma_t=\frac{1-\lambda}{1-\lambda^{t-1}}\sum_{j=1}^{t-1}\lambda^{j-1}a_{t-j}a_{t-j}',\qquad0<\lambda<1.\tag{1}$$

The weights sum to one: $\sum_{j=1}^{t-1}\lambda^{j-1}=(1-\lambda^{t-1})/(1-\lambda)$. For large $t$
($\lambda^{t-1}\approx0$), split off the $j=1$ term and re-index the rest ($j=i+1$):

$$\hat\Sigma_t=(1-\lambda)a_{t-1}a_{t-1}'+\lambda\Big[(1-\lambda)\sum_{i=1}^{t-2}\lambda^{i-1}a_{t-1-i}a_{t-1-i}'\Big]=(1-\lambda)a_{t-1}a_{t-1}'+\lambda\hat\Sigma_{t-1}.\tag{2}$$

One parameter for all $k(k+1)/2$ entries, positive definite by construction. It is an IGARCH:
no mean reversion, the persistence is exactly one.

---

## 3 · C — correlations separately: $\Sigma_t=D_tR_tD_t$ (T eq. 10.7, p. 516)

$$\Sigma_t=D_tR_tD_t,\qquad[\Sigma_t]_{ij}=\sigma_{ii,t}^{1/2}\,\rho_{ij,t}\,\sigma_{jj,t}^{1/2}.\tag{3}$$

The $k$ variances can be modelled one series at a time (GARCH, SV — Class 8). What remains is
$R_t$: $k(k-1)/2$ correlations, symmetric, unit diagonal, positive definite.

---

## 4 · C — dynamic conditional correlation (T §10.4.3, pp. 531–532)

**Tse and Tsui (2002):**

$$R_t=(1-\theta_1-\theta_2)\bar R+\theta_1R_{t-1}+\theta_2\Psi_{t-1},\tag{4}$$

with $\bar R$ a fixed correlation matrix (often the sample one) and $\Psi_{t-1}$ the sample correlation
of the standardised shocks over the last $m$ days.

**Engle (2002):**

$$Q_t=(1-\theta_1-\theta_2)\bar Q+\theta_1\varepsilon_{t-1}\varepsilon_{t-1}'+\theta_2Q_{t-1},\qquad R_t=J_tQ_tJ_t,\quad J_t=\mathrm{diag}(q_{11,t}^{-1/2},\dots,q_{kk,t}^{-1/2}),\tag{5}$$

in Tsay's order ($\theta_1$ on the news term). $J_t$ rescales $Q_t$ into a correlation matrix;
$0<\theta_1+\theta_2<1$ keeps it positive definite. "An obvious drawback of the prior two models is that
$\theta_1$ and $\theta_2$ are scalar so that all the conditional correlations have the same dynamics"
(T p. 531).

**Mean reversion.** Write $s=\theta_1+\theta_2$. Take $E(\cdot\mid F_t)$ of (5) at $t+2$:

$$E(Q_{t+2}\mid F_t)=(1-s)\bar Q+\theta_1E(\varepsilon_{t+1}\varepsilon_{t+1}'\mid F_t)+\theta_2Q_{t+1}.$$

$E(\varepsilon_{t+1}\varepsilon_{t+1}'\mid F_t)=R_{t+1}$, not $Q_{t+1}$; with the usual approximation
$R_{t+1}\approx Q_{t+1}$:

$$E(Q_{t+2}\mid F_t)-\bar Q\approx s\,(Q_{t+1}-\bar Q)\quad\Longrightarrow\quad E(Q_{t+h}\mid F_t)-\bar Q\approx s^{h-1}(Q_{t+1}-\bar Q).\tag{6}$$

The same algebra is exact for (4) in expectation if $E\Psi_{t}\approx R_t$, and exact for a GARCH(1,1)
variance: $E(\sigma^2_{t+h}\mid F_t)-\bar\sigma^2=(\alpha+\beta)^{h-1}(\sigma^2_{t+1}-\bar\sigma^2)$, with
$\bar\sigma^2=\omega/(1-\alpha-\beta)$. Half-life: $h_{1/2}=\ln0.5/\ln s$.

### 4.1 · Worked — W&T Offshore vs the S&P 500 (wti-sp500-timevaryingcovariance.html)

Daily percentage returns, 2014-04-05 to 2023-04-04, 2263 observations after dropping missing values.
(The ticker "WTI" here is **W&T Offshore, Inc.**, an oil-and-gas stock, not the crude-oil benchmark.)

**Step 1, univariate GARCH(1,1)-t** (`dccPre`, `cond.dist="std"`):

| | $\omega$ | $\alpha_1$ | $\beta_1$ | $\nu$ | $\alpha_1+\beta_1$ |
|---|---|---|---|---|---|
| W&T Offshore | 1.2985 | 0.1061 | 0.8432 | 5.46 | 0.9493 |
| S&P 500 | 0.0203 | 0.1964 | 0.8065 | 5.60 | **1.0029** |

W&T: $\bar\sigma^2=1.2985/(1-0.9493)=1.2985/0.0507=25.6$, a long-run daily sd of 5.06%;
half-life $\ln0.5/\ln0.9493=13.3$ days. **S&P: $\alpha_1+\beta_1=1.0029>1$** — no finite unconditional
variance, the fitted variance does not revert (the 2020 crash dominates the sample). With
$\nu\approx5.5$ the Student-$t$ kurtosis $3(\nu-2)/(\nu-4)=3(3.46)/1.46=7.1$: heavy tails.

**Step 2, correlations** (`dccFit` on the standardised residuals; MTS prints the two scalars and the
$t$ degrees of freedom):

| model | first $\theta$ | second $\theta$ | $\nu$ | sum $s$ | half-life $\ln0.5/\ln s$ |
|---|---|---|---|---|---|
| Tse–Tsui (default) | 0.7018 | 0.0500 | 6.11 | 0.7518 | 2.43 days |
| Engle | 0.8704 | 0.0381 | 6.14 | 0.9085 | 7.22 days |

By magnitude the first printed scalar is the weight on the lagged correlation term (it plays
$\theta_2$ in Tsay's (5) ordering) and the second the weight on the news term; the sum $s$ and the
half-life do not depend on the labelling. **Engle's correlation shocks persist three times as long
as Tse–Tsui's.** Diagnostics (`MCHdiag`): the portmanteau $Q(m)$ on $e_t$ has p-values 0.23 and 0.26,
but the rank-based test rejects (0.0022 and 0.0018), and the robust $Q_k(m)$ rejects for Engle at 5%
(0.033) — some dependence is left.

![Left: share of a correlation shock remaining after h trading days, (theta1+theta2) to the power h, for Engle DCC (0.9085, half-life 7.2 days) and Tse-Tsui DCC (0.7518, half-life 2.4 days); right: GARCH variance-shock persistence (alpha+beta) to the h for W&T Offshore (0.9493, decaying) and the S&P 500 (1.0029, rising slightly above 1)](figures/L09-dcc-garch-persistence.png)
*Figure — reversion multipliers from (6) with the dccFit and dccPre estimates of the site page; dotted lines mark the half-lives.*

The left panel says how fast a correlation surprise is forgotten: after two weeks (10 days) Engle
keeps $0.9085^{10}=0.38$ of it, Tse–Tsui $0.7518^{10}=0.06$. The right panel shows the S&P variance
curve **above one and rising** — a fitted model that predicts today's volatility shock never fades,
which is the IGARCH edge of (2).

---

## 5 · C — factor stochastic volatility (Part 2, slide 38; Pitt and Shephard 1999)

$$y_t\mid f_t\sim N(\beta f_t,\Sigma_t),\qquad f_t\sim N(0,H_t),\tag{7}$$

$$\Sigma_t=\mathrm{diag}(\sigma_{1t}^2,\dots,\sigma_{pt}^2),\qquad H_t=\mathrm{diag}(\sigma_{p+1,t}^2,\dots,\sigma_{p+k,t}^2),\tag{8}$$

$$\eta_{it}=\log\sigma_{it}^2\sim N(\alpha_i+\gamma_i\eta_{i,t-1},\xi_i^2),\qquad\lambda_{jt}=\log\sigma_{p+j,t}^2\sim N(\mu_j+\phi_j\lambda_{j,t-1},\tau_j^2).\tag{9}$$

It is the static factor model of [[L09-05-factor-models-favar]] (1) with $p+k$ univariate SV-AR(1)
processes (Class 8) for the variances. Exactly as there, (2) of that note becomes

$$\mathrm{Var}(y_t\mid H_t,\Sigma_t)=\beta H_t\beta'+\Sigma_t.\tag{10}$$

**One factor, two series.** With $h_t=H_t$ (scalar), by (10):

$$[\mathrm{Var}]_{ii}=\beta_i^2h_t+\sigma_{it}^2,\qquad[\mathrm{Var}]_{ij}=\beta_i\beta_jh_t,$$

$$\rho_{ij,t}=\frac{\beta_i\beta_jh_t}{\sqrt{(\beta_i^2h_t+\sigma_{it}^2)(\beta_j^2h_t+\sigma_{jt}^2)}}.\tag{11}$$

Divide numerator and denominator by $|\beta_i\beta_j|h_t$ and write $a_{it}=\sigma_{it}^2/\beta_i^2$:

$$\rho_{ij,t}=\frac{\mathrm{sign}(\beta_i\beta_j)}{\sqrt{(1+a_{it}/h_t)(1+a_{jt}/h_t)}}.\tag{12}$$

Both factors under the root fall as $h_t$ rises, so **$|\rho_{ij,t}|$ is increasing in $h_t$**, from 0
($h_t\to0$) to 1 ($h_t\to\infty$). Correlations go up in turbulent markets **because** the common
factor's variance goes up — the FSV account of "correlations rise in crises", with no correlation
parameter at all.

**Worked — slide 22's series 1 and 3** ($\beta=0.99,\ 0.90$; $\sigma^2=0.01,\ 0.10$):
$a_1=0.01/0.9801=0.010203$, $a_3=0.10/0.81=0.123457$.

- $h=1$: $\rho=1/\sqrt{1.010203\times1.123457}=1/\sqrt{1.134920}=1/1.065326=0.9387$.
- $h=0.05$ ($\lambda_t=\log0.05=-3.0$): $\rho=1/\sqrt{(1+0.20406)(1+2.46914)}=1/\sqrt{1.20406\times3.46914}=1/\sqrt{4.17706}=0.4893$.

A twentyfold fall in the factor variance halves the correlation. The curve is the left panel of
the figure in [[L09-05-factor-models-favar]] §2.

> **Interactive companion.** [The Factor-Volatility Dial](companions/companion-fsv-correlation.html) — move the factor log-variance $\lambda_t$ and watch $\rho_t$ travel along (11); change the loadings and idiosyncratic variances to see which pairs are most sensitive.

**Extensions on the slides.**

- **Correlated factor volatilities** (Aguilar and West 2000, slide 39): $\lambda_t\sim N(\mu+\Phi\lambda_{t-1},U)$
  with $U$ a full covariance matrix, $\Phi=\mathrm{diag}(\phi_1,\dots,\phi_k)$.
- **Time-varying loadings** (Lopes and Carvalho 2007, slide 40): the $d=pk-k(k-1)/2$ free loadings
  follow AR(1)s, $\beta_{ij,t}\sim N(\mu_{ij}+\phi_{ij}\beta_{ij,t-1},\sigma_{ij}^2)$.
- **Daily exchange rates** (slides 41–43): DEM, GBP, JPY, FRF, CAD, ESP against the dollar,
  1/1/1992–10/31/1995, $k=3$ with time-varying loadings and vague priors; slide 43 plots, per
  currency, the share of variance due to each factor and to the idiosyncratic term over time.
- **Tsay §10.6** ("factor–volatility models"): pick the first few principal components of $a_t$
  and model their volatilities — the non-Bayesian route to the same structure.

**Parameter counts** for $k$ series (one factor, AR(1) log-variances with 3 parameters each):

| model | parameters | grows like |
|---|---|---|
| full VEC GARCH(1,1) | $d+2d^2$, $d=k(k+1)/2$ | $k^4$ |
| DCC (Engle) with GARCH(1,1) margins | $3k$ + 2 (+ $\bar Q$ estimated by moments) | $k$ (+ $k^2$ moments) |
| one-factor FSV | $3(k+1)$ + $k$ loadings | $k$ |

---

## 6 · C — the site's two FSV pages

**Six stocks, US and Brazil** (`sv-fsv-US-BR.html`): Apple, Microsoft, Amazon, Petrobras, Vale, CSN,
1/1/2006–3/24/2021, $n=3831$ demeaned log returns. Univariate SV-AR(1) by `stochvol`,
$y_t=e^{h_t/2}\varepsilon_t$, $h_t=\mu+\phi(h_{t-1}-\mu)+\sigma\eta_t$, priors $\mu\sim N(0,100^2)$,
$(\phi+1)/2\sim\mathrm{Beta}(5,1.5)$, $\sigma^2\sim IG(1/2,1/2)$ (as printed), $h_0\sim N(\mu,\sigma^2/(1-\phi^2))$.
Then 50-day rolling correlations, a static two-factor `factanal` (a Brazil and a US factor,
[[L09-05-factor-models-favar]] §3.2), and `fsvsample` with 2 factors on all six and 1 factor on each
country's three. Correlations between the factor paths:

| | 6-d FSV factor 1 | 6-d FSV factor 2 |
|---|---|---|
| 3-d US FSV factor | **0.989** | 0.073 |
| 3-d BR FSV factor | 0.636 | **0.858** |

(The two country-level factors correlate 0.562 with each other.) The joint model rediscovers the two country factors (in the opposite order to `factanal`: FSV
identifies factors by the lower-triangular $\beta$, whose first row is Apple). The page then compares
FSV's time-varying correlations with the 50-day rolling ones and the static sample correlation,
and the 6-d, 3-d and 1-d volatility estimates (figures only).

**W&T Offshore and the S&P 500** (§4.1 page): `svtlsample` (SV with leverage and $t$ errors) per
series, `fsvsample(return, factors=1)` for the pair, posterior densities of the two loadings (between
0.4 and 2.0), FSV sds against the SV ones, and the FSV correlation against Engle's DCC
correlation on $[0,1]$ with guides at 0.2, 0.5, 0.8 (figures only).

---

## 7 · C — DCC vs FSV, side by side

| | DCC | FSV |
|---|---|---|
| object modelled | $R_t$ directly, (4)–(5) | $H_t$, $\Sigma_t$; $R_t$ implied by (11) |
| what moves a correlation | products of yesterday's standardised shocks | the factor's volatility (and the idiosyncratic ones) |
| all pairs share dynamics? | yes (scalar $\theta$'s) | no: each pair's sensitivity is set by $a_{it},a_{jt}$ |
| positive definiteness | by $\theta_1+\theta_2<1$ and $\bar Q$ p.d. | by construction, (10) |
| estimation | two-step QMLE (dccPre, dccFit) | MCMC (fsvsample) |
| dimension | $\bar Q$ has $k(k-1)/2$ entries | linear in $k$ |
| interpretation | statistical | economic (market/country factors) |

---

## Links

- Neighbours: [[L09-06-tvp-var-sv-state-space]] (VAR-GARCH, SV in a VAR) · [[L09-08-formulas]].
- Factor algebra: [[L09-05-factor-models-favar]] §1–§3.
- Unit: [[L09-00-map]] · [[L09-09-pitfalls]] · [[L09-10-python]].
- Rules: [[../../rules/05_espaco_estados_volatilidade|rules/05]] (GARCH, SV, factor SV).
- **Practice (number and printed page only):** T 10.1, 10.2, 10.3, 10.4, 10.5, 10.6 (p. 554).
