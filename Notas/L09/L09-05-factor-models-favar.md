---
tags: [notes, lecture-09, factor-analysis, bayesian-factor-analysis, identification, favar, rmsfe]
date: 2026-10-25
status: taught
source: "BVAR-part2.pdf slides 14 (BFA literature), 15 (basic model), 16 (invariance, block lower triangular β), 17 (number of parameters and the bound on k), 18 (rank deficiency), 19 (ordering of the variables), 20 (priors), 21 (full conditionals), 22–25 (simulation exercise), 26–29 (exchange rates, Lopes and West 2004), 30–33 (parsimonious BFA, named), 34–37 (British Cohort Study, named), 44–49 (spatial DFM, named), 51–55 (forecasting with many predictors, FAVAR, RMSFE), 59 (Bańbura et al. Table III); sv-fsv-US-BR.html §3.2 (factanal on six stocks); Tsay AFTS 3e §9.1–9.2 (pp. 468–476, eqs. 9.1–9.5)"
---

# Part 2 slides 14–37, 51–55 · Factor models: $k$ common factors carry all the cross-correlation, $\Omega=\beta\beta'+\Sigma$; a FAVAR puts them in a VAR

> **Claim.** In the $k$-factor model $y_t=\beta f_t+\varepsilon_t$ the $m\times m$ covariance is
> $\Omega=\beta\beta'+\Sigma$ with $\Sigma$ diagonal: **common factors explain all the dependence**,
> and $m(m+1)/2$ covariances are described by $m(k+1)-k(k-1)/2$ parameters. Loadings are defined
> only up to an orthogonal rotation, so a block-lower-triangular $\beta$ is imposed — the same
> $k(k-1)/2$ count as the SVAR's rotation problem. Given $\beta$ and $\Sigma$, the factors have a
> Gaussian posterior and the Gibbs sampler cycles through three regressions. **A FAVAR** adds
> a few factors, extracted from hundreds of series, as regressors in a small VAR — the second
> answer (after shrinkage) to the curse of dimensionality.

Prev: [[L09-04-bvar-minnesota-ssvs]] · Next: [[L09-06-tvp-var-sv-state-space]] · Map: [[L09-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $y_t$ | $m\times1$ observed vector (slides also write $p$ for $m$) | |
| $f_t$ | $k\times1$ common factors, $N(0,I_k)$ | $k<m$ |
| $\beta$ | $m\times k$ loadings | block lower triangular, $\beta_{ii}>0$ |
| $\Sigma=\mathrm{diag}(\sigma_1^2,\dots,\sigma_m^2)$ | idiosyncratic variances | $>0$ |
| $\Omega$ | $\mathrm{Var}(y_t)$ | |
| $h_i^2=\sum_l\beta_{il}^2/\Omega_{ii}$ | communality of series $i$ | $[0,1]$ |
| $V_f$ | posterior covariance of $f_t$ given $(y_t,\beta,\Sigma)$ | |
| $x_t$ | $r\times1$ large panel of predictors (FAVAR) | $r$ in the hundreds |

---

## 1 · C — the basic model (slide 15; T eq. 9.2, p. 469)

"For any specified positive integer $k\le m$, the standard $k$-factor model relates each $y_t$ to an
underlying $k$-vector of random variables $f_t$, the common factors, via"

$$y_t\mid f_t\sim N(\beta f_t,\Sigma),\qquad f_t\sim N(0,I_k),\qquad\Sigma\ \text{diagonal}.\tag{1}$$

Equivalently $y_t=\beta f_t+\varepsilon_t$ with $\varepsilon_t\sim N(0,\Sigma)$ independent of $f_t$.
Then, using $\mathrm{Cov}(f_t)=I_k$ and $\mathrm{Cov}(f_t,\varepsilon_t)=0$:

$$\Omega=\mathrm{Var}(y_t)=\beta\,\mathrm{Var}(f_t)\,\beta'+\mathrm{Var}(\varepsilon_t)=\beta\beta'+\Sigma,\tag{2}$$

element by element (slide 15):

$$\mathrm{var}(y_{it})=\sum_{l=1}^k\beta_{il}^2+\sigma_i^2,\qquad\mathrm{cov}(y_{it},y_{jt})=\sum_{l=1}^k\beta_{il}\beta_{jl}\quad(i\ne j).\tag{3}$$

Conditionally on $f_t$, $\mathrm{var}(y_{it}\mid f)=\sigma_i^2$ and $\mathrm{cov}(y_{it},y_{jt}\mid f)=0$:
"Common factors explain all the dependence structure among the $m$ variables." Tsay's general
form (eq. 9.2) allows a mean $\alpha$ and correlated factors, $\mathrm{Cov}(r_t)=\beta\Sigma_f\beta'+D$;
when the factors are **observed** (the market return, macro series), it is a multivariate
regression estimated by OLS (T §9.2, p. 470, $\hat\xi=(G'G)^{-1}G'R$; the market model eq. 9.5) — the
same algebra as [[L09-01-var-p-estimation-forecasting]] §4.

---

## 2 · C — rotation, identification and the bound on $k$ (slides 16–19)

**Invariance.** For any orthogonal $k\times k$ matrix $P$, set $\beta^*=\beta P'$ and $f_t^*=Pf_t$:

$$\beta^*f_t^*=\beta P'Pf_t=\beta f_t,\qquad\mathrm{Var}(f_t^*)=PI_kP'=I_k,\qquad\beta^*\beta^{*\prime}=\beta P'P\beta'=\beta\beta'.\tag{4}$$

The data cannot tell $(\beta,f)$ from $(\beta P',Pf)$ — exactly the problem of
[[L09-03-structural-var]] (6)–(7), now for loadings. "Classical approach: $\beta'\Sigma^{-1}\beta=I$
[diagonal]. Our approach: $\beta$ is a block lower triangular" (slide 16): $\beta_{ij}=0$ for
$j>i$ in the first $k$ rows, $\beta_{ii}>0$. That removes $k(k-1)/2$ entries, the dimension of the
rotation group, and "provides both identification and, often, useful interpretation" — series 1
loads only on factor 1, so factor 1 is named after series 1.

**Parameter count** (slide 17). $\beta$ has $mk$ entries minus $k(k-1)/2$ zeros; $\Sigma$ adds $m$:

$$m(k+1)-\frac{k(k-1)}2\quad\text{vs}\quad\frac{m(m+1)}2\ \text{in an unrestricted }\Omega.\tag{5}$$

A factor model must not have more parameters than $\Omega$ has entries:

$$\frac{m(m+1)}2-m(k+1)+\frac{k(k-1)}2\ge0.\tag{6}$$

Multiply (6) by 2 and collect powers of $k$:

$$k^2-(2m+1)k+(m^2-m)\ge0.$$

The roots are $k=\frac{(2m+1)\pm\sqrt{(2m+1)^2-4(m^2-m)}}2=\frac{(2m+1)\pm\sqrt{8m+1}}2$, and $k<m$
requires the smaller root:

$$k\le\frac{2m+1-\sqrt{8m+1}}2.\tag{7}$$

| $m$ | $(2m+1-\sqrt{8m+1})/2$ | $k_{\max}$ (slide 17) |
|---|---|---|
| 6 | $(13-7)/2=3.00$ | 3 |
| 12 | $(25-9.849)/2=7.58$ | 7 |
| 20 | $(41-12.69)/2=14.15$ | 14 |
| 50 | $(101-20.02)/2=40.49$ | 40 |

At $m=6$, $k=3$: $21-6(4)+3=0$, an exact fit with no restriction left on $\Omega$. "Even for small
$m$, the bound will often not matter as relevant $k$ values will not be so large."

**Rank deficiency** (slide 18, G): if $\beta$ has rank $r<k$ there are $Q$ with $\beta Q=0$, $Q'Q=I$, and
$\beta\beta'+\Sigma=(\beta+MQ')(\beta+MQ')'+(\Sigma-MM')$ for orthogonal $M$ — a second source of
non-identification, tied to uncertainty about $k$ (Frühwirth-Schnatter and Lopes 2009 use it to
search over $k$, slides 30–33).

**Ordering** (slide 19): reordering the series ($Ay_t$) changes which series define the factors, but
an orthonormal $P$ with $A\beta P$ lower triangular always exists, so "the order of the variables in
$y_t$ is irrelevant assuming that $k$ is properly chosen" (Lopes and West 2004).

![Left: implied one-factor correlation between two series against the factor log-variance, an S-shaped curve rising from 0 to its limit; the slide-22 pair (loadings 0.99 and 0.90, idiosyncratic variances 0.01 and 0.10) is at 0.939 when the factor variance is 1. Right: the largest admissible number of factors against the number of series, a step function through the slide's points 6 to 3, 12 to 7, 20 to 14 and 50 to 40](figures/L09-factor-correlation.png)
*Figure — left: $\rho_{ij}=\beta_i\beta_jh/\sqrt{(\beta_i^2h+\sigma_i^2)(\beta_j^2h+\sigma_j^2)}$, the correlation (3) when $\mathrm{Var}(f)=h$, for slide 22's series pairs (1, 3) and (2, 4); right: bound (7) with slide 17's four cases.*

Right panel: the bound grows almost linearly, $k_{\max}\approx m-\sqrt{2m}$, so it binds only for
very small panels. Left panel: with the factor variance at 1 (the static model (1)), series 1 and
3 of the simulation have correlation 0.939; letting the factor variance move is the factor
stochastic volatility model of [[L09-07-fsv-dcc-covariances]], and the curve says what it implies:
**correlations rise when the common factor is volatile and collapse toward zero when it is calm.**

---

## 3 · C — priors and full conditionals (slides 20–21)

Priors (slide 20): $\beta_{ij}\sim N(0,C_0)$ for free off-diagonal entries,
$\beta_{ii}\sim N(0,C_0)\mathbb 1(\beta_{ii}>0)$, $\sigma_i^2\sim IG(\nu/2,\nu s^2/2)$ with $s^2$ the prior
mode. The improper $p(\sigma_i^2)\propto1/\sigma_i^2$ is avoided: it "lead[s] to the Bayesian analogue of
the so-called Heywood problem" (an idiosyncratic variance collapsing to zero).

**Factor scores.** For one $t$, the kernel of $p(f_t\mid y_t,\beta,\Sigma)$ is the likelihood times the
$N(0,I)$ prior:

$$-2\log p(f_t\mid\cdot)=(y_t-\beta f_t)'\Sigma^{-1}(y_t-\beta f_t)+f_t'f_t+c=f_t'(I_k+\beta'\Sigma^{-1}\beta)f_t-2f_t'\beta'\Sigma^{-1}y_t+c'.\tag{8}$$

Completing the square as in [[L09-04-bvar-minnesota-ssvs]] (5)–(7):

$$\boxed{f_t\mid y_t,\beta,\Sigma\sim N\big(V_f\beta'\Sigma^{-1}y_t,\ V_f\big),\qquad V_f=(I_k+\beta'\Sigma^{-1}\beta)^{-1}}\tag{9}$$

(slide 21). **Idiosyncratic variances**: given $f$, series $i$ is a regression with $T$ residuals
$d_i=(y_i-f\beta_i')'(y_i-f\beta_i')$, so $\sigma_i^2\mid\cdot\sim IG((\nu+T)/2,(\nu s^2+d_i)/2)$.
**Loadings**: row $i$ is a Bayesian regression of $y_i$ on the factors, $\beta_i\sim N(M_i,C_i)$ with
$C_i^{-1}=C_0^{-1}I+\sigma_i^{-2}f'f$ and $M_i=C_i(C_0^{-1}\mu_0+\sigma_i^{-2}f'y_i)$, truncated to $\beta_{ii}>0$
in the first $k$ rows. Cycling (9) → loadings → variances is the Gibbs sampler.

### 3.1 · Worked — slide 22's simulation exercise

$T=500$, $m=5$, $k=2$,

$$\beta=\begin{pmatrix}0.99&0\\0&0.99\\0.90&0\\0&0.90\\0.50&0.50\end{pmatrix},\qquad\Sigma=\mathrm{diag}(0.01,\ 0.05,\ 0.10,\ 0.15,\ 0.20).$$

By (3): $\Omega_{11}=0.99^2+0.01=0.9901$, $\Omega_{13}=0.99(0.90)=0.891$, $\Omega_{15}=0.99(0.50)=0.495$,
$\Omega_{55}=0.25+0.25+0.20=0.70$, $\Omega_{12}=0$ (series 1 and 2 load on different factors).
Communalities $\sum_l\beta_{il}^2/\Omega_{ii}$: $0.990,\ 0.951,\ 0.890,\ 0.844,\ 0.714$.

The factor-score precision in (9):

$$\beta'\Sigma^{-1}\beta=\begin{pmatrix}\frac{0.99^2}{0.01}+\frac{0.90^2}{0.10}+\frac{0.5^2}{0.20}&\frac{0.5(0.5)}{0.20}\\\cdot&\frac{0.99^2}{0.05}+\frac{0.90^2}{0.15}+\frac{0.5^2}{0.20}\end{pmatrix}=\begin{pmatrix}98.01+8.10+1.25&1.25\\1.25&19.60+5.40+1.25\end{pmatrix}=\begin{pmatrix}107.36&1.25\\1.25&26.25\end{pmatrix}.$$

Add $I_2$ and invert ($\det=108.36(27.25)-1.25^2=2951.5$):

$$V_f=\frac{1}{2951.5}\begin{pmatrix}27.25&-1.25\\-1.25&108.36\end{pmatrix}=\begin{pmatrix}0.00923&-0.00042\\-0.00042&0.03671\end{pmatrix}.$$

Posterior sds $0.096$ and $0.192$: with idiosyncratic variances this small, **the factors are almost
observed** — factor 1 more precisely, because series 1's noise variance (0.01) is the smallest.
The recovered loadings, variances and factors are on slides 23–25 (figures).

### 3.2 · Worked — exchange rates (slides 26–28; Lopes and West 2004)

Standardised first differences of monthly log exchange rates against the pound, 1/1975–12/1986:
US, CAN, JAP, FRA, ITA, GER; $k=2$. Posterior means, first ordering:

| | US | CAN | JAP | FRA | ITA | GER |
|---|---|---|---|---|---|---|
| $\beta_{\cdot1}$ | 0.99 | 0.95 | 0.46 | 0.39 | 0.41 | 0.40 |
| $\beta_{\cdot2}$ | 0.00 | 0.05 | 0.42 | 0.91 | 0.77 | 0.77 |
| $\sigma_i^2$ | 0.05 | 0.13 | 0.62 | 0.04 | 0.25 | 0.28 |

**Check against (3)**: the data are standardised, so $\sum_l\beta_{il}^2+\sigma_i^2$ should be near 1.
US: $0.9801+0+0.05=1.030$; JAP: $0.2116+0.1764+0.62=1.008$; FRA: $0.1521+0.8281+0.04=1.020$. Factor 1
is a **dollar-bloc factor** (US, CAN), factor 2 a **European factor** (FRA, ITA, GER); the yen loads on
both and keeps 62% idiosyncratic. Implied correlation ITA–GER by (3):
$0.41(0.40)+0.77(0.77)=0.164+0.593=0.757$. The second ordering (JAP second) gives loadings within
0.02 of these: slide 19's ordering result in practice.

The site page `sv-fsv-US-BR.html` (§3.2) runs `factanal(ret, factors=2)` on Apple, Microsoft,
Amazon, Petrobras, Vale and CSN daily returns: the correlations of the two factor scores with
the returns are $(0.3,0.3,0.2,0.8,0.9,0.9)$ and $(0.8,0.9,0.8,0.4,0.4,0.3)$ — a **Brazil factor** and
a **US factor**.

---

## 4 · C — forecasting with many predictors: the FAVAR (slides 51–55)

Korobilis (2008): "the issue of improving the forecasting performance of VARs when the set of
available predictors is inconveniently large", $x_t=(x_{t1},\dots,x_{tr})$, $r$ in the hundreds
(slide 51). Reduce $x_t$ to $k\ll r$ factors and put them in the VAR (slide 52):

$$(y_t\mid y_{t-1:t-p},\Theta)\sim N\Big(\sum_{i=1}^pB_iy_{t-i}+\sum_{i=0}^sA_if_{t-i},\ \Sigma\Big),\qquad(x_t\mid f_t,\Theta)\sim N(\beta f_t,\Omega),\tag{10}$$

$\Theta=(B_1,\dots,B_p,A_0,\dots,A_s,\Sigma,\beta,\Omega)$. The second block is (1) for the big panel; the
first is a VAR in the few series of interest augmented by the factors — "closely related to the
factor augmented VAR (FAVAR) of Bernanke et al. (2005)". The VAR stays small (a few $y$'s, a few
$f$'s) while the information set is hundreds of series. Data (slide 53): Stock and Watson (2005),
132 US series, JAN60–DEC03 (output, employment, sales, housing, inventories, prices, money,
interest rates, exchange rates, …).

**Forecast evaluation** (slide 54). For series $i$, horizon $h$, model $j$, with $\tilde y_{i,t+h,j}$ the
posterior predictive mean and forecast origins 1982:12 to 2003:12$-h$ ($N_h$ of them):

$$\mathrm{RMSFE}_{ihj}=\sqrt{\frac1{N_h}\sum_{t=1982:12}^{2003:12-h}\big(y_{i,t+h}-\tilde y_{i,t+h,j}\big)^2},\tag{11}$$

reported relative to a benchmark (slide 55). (The slide prints the sum without the $1/N_h$; in a
ratio of two models over the same origins the factor cancels.)

**FAVAR vs large BVAR** — Bańbura et al., Table III (slide 59), MSFE relative to the random walk,
1971–2003, $h=1$:

| | FAVAR 1 factor, BVAR | FAVAR 3 factors, $p=13$ OLS | FAVAR 3 factors, BVAR | LARGE BVAR |
|---|---|---|---|---|
| EMPL | 0.70 | 3.02 | 0.65 | **0.46** |
| CPI | 0.65 | 2.39 | 0.58 | **0.50** |
| FFR | 0.89 | 2.40 | 0.85 | **0.75** |

The factors help (0.65 vs the 7-variable CEE BVAR's 0.67 for employment, [[L09-04-bvar-minnesota-ssvs]] §6)
but **the shrunk 131-variable BVAR beats the FAVAR** at $h=1$ for all three series; OLS with 13
lags is again far worse than the random walk. Large TVP-BVARs and fully Bayesian FAVARs
(Koop–Korobilis 2012; Ahmadi–Uhlig 2009) are in [[L09-06-tvp-var-sv-state-space]] §6.

---

## 5 · G — named only

- **Parsimonious BFA** (Frühwirth-Schnatter and Lopes 2009, slides 30–33): generalised lower
  triangular loadings, birth/death of loadings and columns, inference on $k$.
- **British Cohort Study** (Conti, Heckman, Frühwirth-Schnatter, Lopes and Piatek 2011, slides 34–37):
  BFA on cognitive and health measurements; 5,105 women and 5,420 men.
- **Spatial dynamic factor models** (Lopes, Salazar and Gamerman 2008, slides 44–49):
  $y_t\sim N(\beta f_t,\Sigma)$, $f_t\sim N(\Gamma f_{t-1},\Lambda)$, columns of $\beta$ Gaussian processes over
  space; SO$_2$ at US monitoring stations, interpolation and forecasting.
- **Principal components** as the non-Bayesian factor extractor (Tsay §9.4) and Stock–Watson's
  two-step FAVAR: outside the slides' scope here.

---

## Links

- Neighbours: [[L09-04-bvar-minnesota-ssvs]] (shrinkage, the other answer) · [[L09-07-fsv-dcc-covariances]] (factors with stochastic volatility).
- Unit: [[L09-00-map]] · [[L09-08-formulas]] · [[L09-09-pitfalls]] · [[L09-10-python]].
- Rotation problem twin: [[L09-03-structural-var]] §3.
- Rules: [[../../rules/05_espaco_estados_volatilidade|rules/05]].
- **Interactive companion.** [The Factor-Volatility Dial](companions/companion-fsv-correlation.html) — the left panel of the figure, live: move loadings, idiosyncratic variances and the factor log-variance.
- **Practice (number and printed page only):** T 9.7 (p. 503).
