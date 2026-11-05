---
tags: [notes, lecture-08, pitfalls, true-false, self-test, review]
date: 2026-10-25
status: taught
source: "The nine section notes L08-01 … L08-09; V/F conventions of rules/00_estilo_avaliacao.md (macro-1 style); numbers re-checked by Notas/L08/L08_python_checks.py. The self-test is original; no textbook exercise is reproduced."
---

# Class 8 · Pitfalls — the confusions, each with its minimal counterexample, and an original True/False self-test

> Prev: [[L08-10-formulas]] · Next: [[L08-12-python]] · Map: [[L08-00-map]]

Equations are cited by the section note's own numbering; every number is asserted in
[[L08-12-python]] or in `figures/make_figures.py`.

---

## Part I — the confusions this material produces

### 1 · A coefficient above 1 vs a nonstationary process

**The confusion.** "$\phi_1=1.75>1$, so the AR(2) explodes."

**Counterexample** (slides' $\phi=(1.75,-0.80)$; L08-01 (15)–(18)). $\phi_2=-0.80<1-1.75=-0.75$,
$-0.80<1+1.75$, $-0.80>-1$: inside the triangle. Both solutions of $1-1.75x+0.8x^2=0$ have
modulus 1.118 > 1, and $\gamma_0=50.7\sigma^2$ is finite.

> **Stationarity is a property of the roots, not of any single coefficient** (as with $\Phi_{22}=1.1$ in
> L01-07 §9.1). → [[L08-01-ar2-arp-cycles-identification]] §5.

### 2 · Characteristic roots vs solutions of the characteristic equation

**The confusion.** Mixing "the roots must lie outside the unit circle" with "inside".

**Resolution** (L08-01 (10)–(12)). Tsay calls the **inverses** of the solutions of $1-\phi_1x-\phi_2x^2=0$
the characteristic roots: stationarity needs the **solutions** outside ($\lvert x\rvert>1$) and the
**characteristic roots** inside ($\lvert\omega\rvert<1$). For $(1.75,-0.80)$: $\lvert x\rvert=1.118$,
$\lvert\omega\rvert=0.894$. Same statement, two languages; say which one you use.

### 3 · Complex roots vs oscillating data

**The confusion.** "A smooth, highly persistent ACF means real roots."

**Counterexample.** $(1.75,-0.80)$ has $\rho_1=0.972$ and a smooth ACF, yet the roots are complex
($1.75^2+4(-0.80)=-0.1375<0$): the cycle has length 30.1 and shows only as a dip to $\rho_{15}=-0.187$.
The near-unit real root of $(0.90,0.05)$ gives an ACF that never turns negative.
→ figure `L08-ar2-triangle-acf`.

### 4 · ACF cut-off vs PACF cut-off

**The confusion.** "The ACF dies at lag 2, so fit an AR(2)."

**Resolution** (L08-02 §8). A cut-off in the **ACF** identifies an **MA**; a cut-off in the **PACF** identifies
an **AR**. AR(2) $(0.6,-0.4)$: ACF damped waves, PACF 0.4286, −0.4, then exactly 0. MA(1) $\theta=0.6$:
ACF −0.441 then 0, PACF decays. ARMA cuts off in neither.

### 5 · An MA(1) with $\lvert\rho_1\rvert=0.6$

**The confusion.** Matching any lag-1 autocorrelation with an MA(1).

**Counterexample** (L08-02 (17)). $\lvert\rho_1\rvert=\lvert\theta_1\rvert/(1+\theta_1^2)\le\frac12$, with equality at
$\lvert\theta_1\rvert=1$. A sample $\hat\rho_1=0.6$ with nothing after it is not an MA(1). And $\theta=0.5$ and
$\theta=2$ give the same $\rho_1=-0.4$: only the **invertible** one ($\lvert\theta\rvert<1$) is reported.

### 6 · Sign conventions in printed MA coefficients

**The confusion.** Plugging R's `ma1 = −0.3864` into Tsay's $(1-\theta B)$ as $\theta=-0.3864$.

**Resolution** (L08-02, L08-05 §3.1). Tsay writes $a_t-\theta a_{t-1}$; R, `forecast` and statsmodels print the
coefficient of $+a_{t-1}$. R's −0.3864 is Tsay's $\theta=+0.3864$. The AirPassengers ACF
$\rho_1=-0.336$ comes out negative either way only if the conversion is done right.

### 7 · A long-horizon forecast interval vs the forecast of a stationary series

**The confusion.** "Forecast uncertainty always grows without bound."

**Counterexample** (L08-02 (28) vs L08-03 (6)). Stationary AR(2): $V[e_h(\ell)]=\sigma^2\sum_{j<\ell}\psi_j^2\to\gamma_0$
(sd 7.12 for the ar2-forecast model). Random walk: $V=\ell\sigma^2\to\infty$. Bounded vs unbounded is
exactly the stationary/unit-root distinction. → figure `L08-unit-root-bands-df`, left.

### 8 · Failing to reject a unit root vs accepting it

**The confusion.** "ADF p = 0.45, so GDP has a unit root."

**Counterexample** (W Ex. 18.2; L08-03 §6.3). For T-bills, $t=-2.46$ does not reject $\rho=1$, but a
standard $t$ test of $\rho=0.9$ gives $t=(0.909-0.9)/0.037=0.24$ and does not reject either. Both cannot be "accepted".
With $T=35$ (W Ex. 18.4), $\hat\rho=0.79$ still fails to reject: the test has low power near 1.

### 9 · Normal critical values for a DF statistic

**The confusion.** Rejecting $H_0:\phi=1$ when $t<-1.645$.

**Counterexample** (seeded MC, $T=250$; L08-03 §5.5). Under a true unit root the DF $t$ has 5% quantile
−2.87 (W: −2.86). Using −1.645 rejects a true unit root **46.5%** of the time.

### 10 · Same test name, different regressions

**The confusion.** "Tsay reports ADF = −1.701 for GDP but the site page prints −0.370: one is wrong."

**Resolution** (L08-03 §7). `tseries::adf.test` always includes a constant **and a trend**; Tsay's and the
deck's runs use a constant only (−1.701 / −1.61). Different deterministic terms, different null
distributions, same conclusion (no rejection).

### 11 · Trend-stationary vs random walk with drift

**The confusion.** "Both trend upward, so detrending and differencing are interchangeable."

**Counterexample** (L08-03 (9), (11)). RW with drift: variance $t\sigma^2$, shocks permanent; trend-stationary:
variance $V(r_t)$ constant, shocks transitory. At $\ell=120$ months (3M calibration) the ±2 sd band is
±1.40 vs ±0.29. Detrending a RW leaves a nonstationary residual; differencing a trend-stationary series
creates a non-invertible MA unit root.

### 12 · A significant regression between two trending series

**The confusion.** $t=5$ and $R^2=0.9$ between two price levels ⇒ a relation.

**Counterexample** (Granger–Newbold; W §18.3). Two **independent** random walks, $n=50$: the nominal 5%
$t$ test rejects 66% of the time (our MC: 66%), 84.7% at $n=250$. Under $H_0$ the error is itself a random walk.

### 13 · Long memory vs unit root

**The confusion.** "A slowly decaying ACF means a unit root."

**Counterexample** (L08-04 (7)–(11)). ARFIMA with $d=0.4$ is **stationary**, yet $\rho_{100}=0.267$, while an
AR(1) with the same $\rho_1=2/3$ has $\rho_{100}\approx10^{-18}$. A unit root gives sample ACFs near 1 at all
fixed lags; long memory gives small ACFs that decay hyperbolically ($k^{2d-1}$).

### 14 · Multiplicative vs additive seasonal MA

**The confusion.** "The airline model is just an MA with lags 1 and 12."

**Counterexample** (L08-05 (12)–(14)). $(1-\theta B)(1-\Theta B^{12})$ adds the term $\theta\Theta B^{13}$:
nonzero $\rho_{11}=\rho_{13}=\rho_1\rho_{12}=0.147$ (AirPassengers). The non-multiplicative
$1-\theta B-\Theta B^{12}$ has $\rho_{13}=0$. Same two parameters, different ACF.

### 15 · Uncorrelated vs independent returns

**The confusion.** "Ljung–Box on returns does not reject, so returns are iid."

**Counterexample** (L01-07 §2; L08-06 §2.1). IBM: $Q(30)=38.2$ (p 0.14) on returns, 182.1 on squares;
Intel: $Q(12)=18.26$ (p 0.11) on returns, 89.85 on $a_t^2$. Serially uncorrelated, conditionally
heteroskedastic: that is exactly an ARCH process.

### 16 · Conditional vs unconditional variance (and kurtosis)

**The confusion.** "Gaussian innovations ⇒ Gaussian returns."

**Counterexample** (L08-06 (12), (25)). ARCH(1) with $\alpha_1=0.356$ and $N(0,1)$ innovations has
unconditional kurtosis 4.23; Tsay's GARCH(1,1) has 6.65. Conditionally normal, unconditionally fat-tailed.

### 17 · Persistence vs the size of the ARCH coefficient

**The confusion.** "$\alpha_1=0.12$ is small, so volatility shocks die fast."

**Counterexample** (L08-06 (28)–(29)). The decay rate is $\alpha_1+\beta_1=0.9727$: half-life 25 months
(Petrobras: 0.980, 34 days). $\alpha_1$ sets the immediate reaction; $\beta_1$ carries it.

### 18 · IGARCH vs "very persistent" GARCH

**The confusion.** "$\alpha_1+\beta_1=0.98$ is basically IGARCH."

**Resolution** (L08-06 (31)–(32)). At 0.98 forecasts still revert to $\sigma_\infty^2$ (half-life 34); at exactly 1
there is no $\sigma_\infty^2$ and forecasts rise linearly by $\alpha_0$ per step. A Bayesian reports
$\Pr(\alpha_1+\beta>1\mid\text{data})$ (0.0034 for Petrobras 2007–2013) instead of guessing.

### 19 · The printed `gamma1` of `garchFit(leverage=TRUE)`

**The confusion.** Reading the glossary page's formula $\sigma_t^2=\omega+\alpha\varepsilon^2+\gamma\varepsilon^2 I(\varepsilon<0)+\beta\sigma^2$ with its printed numbers.

**Counterexample** (L08-07 (4)–(7)). With $\alpha=0.0923$, $\gamma=0.2084$, $\beta=0.8818$, the literal reading has
persistence $\alpha+\gamma/2+\beta=1.078>1$. `fGarch` fits the APARCH form $\alpha(\lvert a\rvert-\gamma a)^2$:
bad news 0.1348, good news 0.0579, persistence 0.978.

### 20 · Heavier-tailed innovations vs a smaller ARCH effect

**The confusion.** "The $t$ fit has a smaller $\alpha_1$, so less volatility clustering."

**Resolution** (T p. 126; L08-07 §6). Under normal errors the model inflates $\alpha_1$ to manufacture the
tails; with $t$ errors part of the kurtosis comes from $\varepsilon$ (Intel: 0.356 → 0.285; Petrobras
0.103 → 0.074). Total kurtosis rises (PBR GARCH-$t$: 12.55).

### 21 · Observation-driven vs parameter-driven volatility

**The confusion.** "SV is GARCH with a log."

**Resolution** (L08-08 §1, §5). In GARCH, $\sigma_t^2$ is a known function of past data; in SV it has its own
shock, so the likelihood integrates over the whole volatility path (MCMC). That extra shock is why
the SV fit needs fewer tail degrees of freedom (Petrobras: $\nu=12$ vs GARCH-$t$ 7).

### 22 · A posterior "p-value"

**The confusion.** GARCH11-SVar1.html prints "Pr(>|t|) = 1.9987" for $\mu$ in the SV table.

**Resolution** (L08-08 §9; L08-09 §8). It is $2(1-\Phi(t))$ with $t<0$: not a probability. Posterior
summaries answer $\Pr(\mu<0\mid\text{data})$ directly; frequentist labels on MCMC output mislead.

---

## Part II — True/False self-test (original)

**Scoring** ([[../../rules/00_estilo_avaliacao|rules/00]]): V/F score
$=\max\{0,\ \text{correct}-\text{wrong}/2\}\times$ item value; blank items do not count as wrong.
Difficulty: **[E]** easy · **[M]** medium · **[P]** hard. Numbers are illustrative unless a note is cited.
Answers follow each block.

### Block A — AR, MA, ARMA

**Setting (items 1–6).** A central-bank analyst fits $y_t=1.2y_{t-1}-0.5y_{t-2}+a_t$, $\sigma=1$, to quarterly
output-gap data, and a colleague proposes $y_t=a_t+0.9a_{t-1}$ instead.

1. **[E]** The AR(2) is stationary.
2. **[M]** The AR(2) implies stochastic cycles of average length about 11 quarters.
3. **[M]** The AR(2)'s lag-1 autocorrelation is 0.8.
4. **[M]** The colleague's MA(1) has lag-1 autocorrelation 0.9.
5. **[P]** The MA(1) $y_t=a_t+(1/0.9)a_{t-1}$ has the same ACF as the colleague's model, so the data cannot tell them apart; the convention is to report the invertible one.
6. **[M]** The 10-quarter-ahead forecast-error variance of the AR(2) exceeds its unconditional variance.

**Answers.**

1. **True.** $\phi_2=-0.5<1-1.2=-0.2$, $-0.5<2.2$, $-0.5>-1$: inside the triangle (L08-01 (18)).
2. **True.** $\phi_1^2+4\phi_2=1.44-2=-0.56<0$: complex. $\cos^{-1}[1.2/(2\sqrt{0.5})]=\cos^{-1}(0.8485)=0.5576$, so
   $k=2\pi/0.5576=11.27$ quarters (L08-01 (14)).
3. **True.** $\rho_1=\phi_1/(1-\phi_2)=1.2/1.5=0.8$ (L08-01 (7)).
4. **False.** $\rho_1=0.9/(1+0.81)=0.497$, below the $\frac12$ bound; no MA(1) reaches 0.9 (L08-02 (17)).
5. **True.** $\theta$ and $1/\theta$ give the same $\theta/(1+\theta^2)$: $1.111/(1+1.235)=0.497$. Only $\lvert\theta\rvert<1$ is
   invertible (L08-02 (19)).
6. **False.** $V[e_h(\ell)]=\sigma^2\sum_{j<\ell}\psi_j^2$ increases **to** $\gamma_0$ and never exceeds it (L08-02 (28)).

### Block B — identification and forecasting

7. **[E]** For an AR(3), the theoretical PACF is zero from lag 4 on.
8. **[M]** BIC penalises each parameter by $\ln T/T$ per observation, so with $T=996$ it tends to choose smaller models than AIC.
9. **[M]** For an MA(2), all forecasts beyond two steps equal the unconditional mean.
10. **[P]** The ACF of an ARMA(1,1) with $\phi_1=0.8$ decays geometrically at rate 0.8 from lag 1, exactly as an AR(1) with $\phi=0.8$.

**Answers.**

7. **True.** $\phi_{\ell,\ell}=0$ for $\ell>p$ (T p. 47; L08-01 §8).
8. **True.** Per parameter: 2 for AIC vs $\ln996=6.90$ for BIC; Table 2.1 has AIC → 9, BIC → 1 (L08-01 (25)).
9. **True.** $\hat r_h(\ell)=c_0$ for $\ell>q$ (T p. 63; L08-02 §7).
10. **False.** $\rho_\ell=\phi_1\rho_{\ell-1}$ only from $\ell\ge2$; $\rho_1$ differs ($0.5231$ for $(0.8,0.4)$ vs $0.8$) (L08-02 (25)).

### Block C — unit roots and long memory

**Setting (items 11–16).** A pension fund's analyst runs `adf.test` on 60 years of log house prices
and gets $t=-2.1$, p = 0.53.

11. **[E]** The analyst may conclude that house prices have a unit root.
12. **[M]** Had the analyst compared $t=-2.1$ with −1.645, he would have rejected a unit root, and that rejection would have been too frequent under the null.
13. **[M]** If log prices follow a random walk with drift, the conditional variance of the 20-year-ahead forecast is 20 times that of the 1-year-ahead forecast (annual data).
14. **[P]** In the ADF regression of an AR(3), the coefficient on $x_{t-1}$ in the $\Delta$ form equals $\phi_1+\phi_2+\phi_3-1$, so a unit root means $\phi_1+\phi_2+\phi_3=1$.
15. **[M]** A stationary ARFIMA(0, 0.3, 0) has an ACF that decays faster than any AR(1)'s at long lags.
16. **[M]** Regressing the log house-price index on an unrelated random walk would yield a significant slope more often than 5% of the time.

**Answers.**

11. **False.** Non-rejection is not acceptance; DF tests have little power near 1 (W p. 576; L08-03 §6.3).
12. **True.** $-2.1<-1.645$ rejects; under a true unit root that rule rejects about 46% of the time (L08-03 §5.5).
13. **True.** $V[e_h(\ell)]=\ell\sigma^2$: $20\sigma^2$ vs $\sigma^2$ (L08-03 (6)); the drift shifts the mean only.
14. **True.** L08-03 (25)–(27): $\beta=-\phi(1)$, zero iff $\sum\phi_i=1$.
15. **False.** It decays hyperbolically, $\rho_k\sim ck^{-0.4}$, **slower** than any geometric $\phi^k$ (L08-04 (11)).
16. **True.** Spurious regression: 66% rejections at $n=50$ (W §18.3; L08-03 §8).

### Block D — seasonal models

17. **[E]** In the airline model with $s=12$, the ACF of $w_t=(1-B^{12})(1-B)x_t$ is nonzero only at lags 1, 11, 12, 13.
18. **[M]** In the airline model, $\rho_{13}=\rho_1\rho_{12}$.
19. **[P]** When the exact-likelihood estimates of a seasonal AR and a seasonal MA factor are both close to 1 and nearly cancel, the seasonality is better modelled with dummy variables.
20. **[M]** Taking logs of AirPassengers before fitting the airline model is meant to turn a multiplicative seasonal pattern into an additive one.

**Answers.**

17. **True.** L08-05 (6)–(12).
18. **True.** $\gamma_{13}=\theta\Theta\sigma^2$ and the product form of the variance give $\rho_{13}=\rho_1\rho_{12}$ (L08-05 (12)).
19. **True.** Decile 1: seasonal AR 0.951 and MA 0.997 cancel, and a January dummy (0.1253) removes lags 12, 24, 36 (T Ex. 2.4; L08-05 §5).
20. **True.** Amplitude grows with the level; the log stabilises it (airpassengers page; T p. 83).

### Block E — ARCH and GARCH

**Setting (items 21–26).** A bank's risk desk fits a Gaussian GARCH(1,1) to daily returns:
$\alpha_0=0.02$, $\alpha_1=0.10$, $\beta_1=0.85$ (returns in %).

21. **[E]** The unconditional daily variance is 0.4 (%²).
22. **[M]** A volatility shock has a half-life of about 13.5 days.
23. **[M]** The unconditional kurtosis of returns is finite and above 3.
24. **[P]** If today's 1-day-ahead variance forecast is 1.4, the 3-day-ahead forecast is 1.1.
25. **[M]** Because the innovations are Gaussian, the unconditional distribution of returns is Gaussian.
26. **[M]** The model implies that a −3% shock and a +3% shock raise tomorrow's variance by the same amount.

**Answers.**

21. **True.** $0.02/(1-0.95)=0.4$ (L08-06 (22)).
22. **True.** $\ln0.5/\ln0.95=13.5$ (L08-06 (29)).
23. **True.** $1-2(0.01)-0.95^2=0.0775>0$; $K_a^{(g)}=0.06/0.0775=0.774$, kurtosis 3.77 (L08-06 (25)).
24. **False.** $\sigma^2(\ell)=0.4+0.95^{\ell-1}(1.4-0.4)$, and $0.95^2=0.9025$, so $\sigma^2(3)=0.4+0.9025\times1.0=1.3025$,
   not 1.1. The gap to $\sigma_\infty^2$ shrinks by only 5% per day (L08-06 (28)).
25. **False.** Conditionally Gaussian, unconditionally fat-tailed (item 23).
26. **True.** GARCH depends on $a_{t-1}^2$ only; asymmetry needs GJR/EGARCH (L08-07 §1).

### Block F — asymmetry, SV, Bayes

27. **[M]** In an EGARCH with $\log\sigma_t^2=\omega+\alpha z_{t-1}+\gamma(\lvert z_{t-1}\rvert-E\lvert z\rvert)+\beta\log\sigma_{t-1}^2$, a negative $\alpha$ means bad news raises volatility more than good news.
28. **[M]** In an SV-AR(1) with Gaussian $\varepsilon$, the unconditional kurtosis is $3e^{\sigma_h^2}$, where $\sigma_h^2$ is the stationary variance of the log variance.
29. **[P]** The SV likelihood can be evaluated by the same one-pass recursion as the GARCH likelihood, once the parameters are given.
30. **[M]** With an IG(5, b) prior and $n=1760$ observations, the prior's weight in the posterior mean of $\sigma^2$ is below 1%.

**Answers.**

27. **True.** The bad/good ratio at $\lvert z\rvert=c$ is $e^{-2\alpha c}>1$ when $\alpha<0$ (Petrobras: 1.117 at $c=1$) (L08-07 (14)).
28. **True.** $E a^4/(E a^2)^2=3e^{2\mu_h+2\sigma_h^2}/e^{2\mu_h+\sigma_h^2}$ (L08-08 (7)).
29. **False.** The volatility path is latent with its own shock; the likelihood is an $n$-dimensional integral (L08-08 (10)), handled by MCMC or filtering.
30. **True.** Weight $(a-1)/(a-1+n/2)=4/884=0.45\%$ (L08-09 (5)).

---

## Part III — the distinctions that cost most points

| Pair | One-line test |
|---|---|
| solutions vs characteristic roots | outside vs inside the unit circle — say which |
| ACF vs PACF cut-off | MA vs AR |
| bounded vs growing forecast variance | stationary vs unit root |
| fail to reject vs accept | DF power is low near 1 |
| DF vs normal critical values | −2.86 vs −1.645 at 5% |
| hyperbolic vs geometric decay | long memory vs ARMA |
| multiplicative vs additive seasonal MA | $\rho_{s+1}=\rho_1\rho_s$ vs 0 |
| conditional vs unconditional kurtosis | GARCH turns normal shocks into fat tails |
| $\alpha_1$ vs $\alpha_1+\beta_1$ | reaction vs persistence |
| printed `gamma1` vs GJR's $\gamma$ | APARCH form in `fGarch` |
| GARCH vs SV | observation- vs parameter-driven |

---

## Links

- Unit: [[L08-00-map]] · [[L08-10-formulas]] · [[L08-12-python]]
- Notes: [[L08-01-ar2-arp-cycles-identification]] · [[L08-02-forecasting-ma-arma]] · [[L08-03-unit-roots-dickey-fuller]] · [[L08-04-long-memory-arfima]] · [[L08-05-seasonal-airline-model]] · [[L08-06-arch-garch]] · [[L08-07-garch-family-asymmetry-tails]] · [[L08-08-stochastic-volatility]] · [[L08-09-bayesian-garch]]
- Class 1 pitfalls on stationarity: [[../L01/L01-10-pitfalls|L01-10]] §10, §13
