---
tags: [notes, lecture-08, time-series, unit-root, random-walk, drift, trend-stationary, arima, dickey-fuller, adf, spurious-regression]
date: 2026-10-25
status: taught
source: "unitroot.pdf slides 1–31 (random walk, mean reversion, predictability, memory, RW with drift, constant term, trend stationarity, ARIMA(p,1,q), DF, ADF, AR(3) rewrite, US GDP, S&P 500); unitroot.html (simulations, adf.test outputs); Tsay AFTS 3e §2.7 pp. 71–81 (eqs. 2.35–2.40, eq. 2.37 3M returns, Example 2.2 GDP, S&P 500 example); Wooldridge 6e §18.2–18.3 pp. 574–580 (eqs. 18.17–18.30, Tables 18.2–18.3, Examples 18.2–18.4)"
---

# §2.7 · Unit roots — shocks that never die, forecasts that never revert, and a $t$ ratio that is not normal

> **Claim.** **A random walk is the AR(1) at $\phi_1=1$: every shock is permanent ($\psi_i=1$), the point forecast never moves from today's value, and the forecast-error variance grows like $\ell\sigma^2$.** Adding a drift $\mu$ makes the constant a *slope*, not a mean; a trend-stationary series has the same straight-line mean but a *bounded* variance. **Whether a series has a unit root is tested with the Dickey–Fuller $t$ ratio, whose null distribution is skewed left and has its own critical values ($-2.86$ at 5% with a constant, $-3.41$ with a trend), not $-1.645$.** Using normal critical values rejects a true unit root almost half the time. US GDP and the S&P 500 do not reject; their differences do. Regressing one independent random walk on another "finds" a relationship most of the time.
> Prev: [[L08-02-forecasting-ma-arma]] · Next: [[L08-04-long-memory-arfima]] · Map: [[L08-00-map]]

Builds on [[../L01/L01-07-ar-var-review|L01-07]] §7, where the random walk $y_t=y_0+e_1+\dots+e_t$, its variance $t\sigma^2$, the non-reverting forecast and $\mathrm{Corr}(y_t,y_{t+h})=\sqrt{t/(t+h)}$ were derived (L01-07 (18)–(19)). This note does not repeat them; it uses them.

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $p_t$ | log price (Tsay) or any $I(1)$ candidate | |
| $a_t$, $e_t$ | white-noise shock (Tsay: $a_t$ in models, $e_t$ in test regressions), variance $\sigma^2$ | |
| $\mu$ | drift: $E(p_t-p_{t-1})$ in a random walk with drift | |
| $h$, $\ell$ | forecast origin, horizon | $\ell\ge1$ |
| $\hat p_h(\ell)$, $e_h(\ell)$ | $\ell$-step forecast and its error | |
| $\psi_i$ | MA($\infty$) weights | |
| $\phi_0,\phi_1$ | constant and slope in the DF regressions (2.38)–(2.39) | |
| $\rho$ | AR(1) coefficient in Wooldridge's (18.17); $\theta=\rho-1$ | |
| $c=\beta-1$ | coefficient of $x_{t-1}$ in the $\Delta$ form of the ADF regression (Tsay); $u$ in the figure | $c\le0$ |
| $\beta$ | **two uses:** Tsay (2.40) levels coefficient ($H_0:\beta=1$); the slides' $\Delta$-form $\beta=-\phi(1)$ ($H_0:\beta=0$). Stated each time | |
| $\phi(B)=1-\phi_1B-\dots-\phi_pB^p$ | AR polynomial; $\phi(1)=1-\sum\phi_i$ | |
| $c_t$ | deterministic term: $0$, $\omega_0$, or $\omega_0+\omega_1t$ | |
| $I(d)$ | integrated of order $d$: stationary after $d$ differences | |

---

## 1 · C — the random walk as a forecasting model (slides 4–12; T §2.7.1, pp. 72–73)

The random walk (T eq. 2.35):

$$p_t=p_{t-1}+a_t,\qquad p_0\ \text{given},\quad a_t\ \text{white noise}.\tag{1}$$

It is the AR(1) of L01-07 (5) with $\phi_0=0$, $\phi_1=1$, which violates $|\phi_1|<1$: "a unit-root nonstationary time series" (T p. 72).

**Point forecasts.** At origin $h$, (1) at $t=h+1$ gives $p_{h+1}=p_h+a_{h+1}$; take $E(\cdot\mid F_h)$ with $E(a_{h+1}\mid F_h)=0$:

$$\hat p_h(1)=p_h.\tag{2}$$

For two steps, write $p_{h+2}=p_{h+1}+a_{h+2}$ and condition:

$$\hat p_h(2)=E(p_{h+1}\mid F_h)+E(a_{h+2}\mid F_h)=\hat p_h(1)+0=p_h,$$

and by induction

$$\hat p_h(\ell)=p_h\quad\text{for all }\ell\ge1.\tag{3}$$

**The process is not mean reverting**: compare L01-07 (19), where a stationary AR(1) forecast decays as $\phi^\ell$ toward $\mu$.

**MA representation and forecast errors.** Substituting (1) into itself, as in L01-07 (8) with $\phi_1=1$:

$$p_t=a_t+a_{t-1}+a_{t-2}+\cdots,\qquad \psi_i=1\ \text{for all } i.\tag{4}$$

The forecast error is the sum of the shocks not yet seen. From (1) iterated $\ell$ times, $p_{h+\ell}=p_h+a_{h+1}+\dots+a_{h+\ell}$; subtract (3):

$$e_h(\ell)=p_{h+\ell}-\hat p_h(\ell)=a_{h+\ell}+a_{h+\ell-1}+\dots+a_{h+1},\tag{5}$$

$$V[e_h(\ell)]=\ell\,\sigma^2\ \longrightarrow\ \infty\quad(\ell\to\infty).\tag{6}$$

(6) is T eq. (2.34) with all $\psi_i=1$: $\sigma^2\sum_{i=0}^{\ell-1}\psi_i^2=\sigma^2\ell$. "The usefulness of point forecast $\hat p_h(\ell)$ diminishes as $\ell$ increases, which again implies that the model is not predictable" (slide 9; T p. 73).

**Memory.** $\psi_i=1$ in (4) means a shock from any date enters today's level with weight one: "in economics, the shocks are said to have a permanent effect on the series" (T p. 73). The sample ACF of a random walk approaches 1 at every fixed lag as $T$ grows (slide 11 shows it at lag 200 from 100,000 simulated steps). This is what makes the ACF useless for identifying anything once the series is $I(1)$.

> **Stationary: shocks fade at rate $\psi_i\to0$, forecasts revert, the forecast variance converges to $\gamma_0$. Unit root: $\psi_i=1$, forecasts are flat at $p_h$, the variance grows without bound.**

**U — the slides' coin walk (slides 5–6, `unitroot.html`).** With $a_t\in\{-1,+1\}$ equally likely ($\sigma^2=1$), the four panels show the first 50, 100, 200 and 1000 steps of one path. Each zoom-out looks like a new "trend": by (6) the typical distance from the start after 1000 steps is $\sqrt{1000}\approx32$, and nothing pulls the walk back to 0.

---

## 2 · C — random walk with drift: the constant becomes a slope (slides 13–15; T §2.7.2, pp. 73–75)

$$p_t=\mu+p_{t-1}+a_t\qquad(\text{T eq. 2.36}).\tag{7}$$

Repeated substitution, one line at a time:

$$p_1=\mu+p_0+a_1,$$

$$p_2=\mu+p_1+a_2=\mu+(\mu+p_0+a_1)+a_2=2\mu+p_0+a_2+a_1,$$

$$p_3=\mu+p_2+a_3=\mu+(2\mu+p_0+a_2+a_1)+a_3=3\mu+p_0+a_3+a_2+a_1,$$

$$p_t=p_0+\mu t+\sum_{i=1}^ta_i.\tag{8}$$

So, conditional on $p_0$,

$$E(p_t)=p_0+\mu t,\qquad V(p_t)=t\sigma^2,\qquad \mathrm{sd}(p_t)=\sigma\sqrt t.\tag{9}$$

**The mean grows like $t$, the sd like $\sqrt t$**: the trend eventually dominates the noise. They are equal when $\mu t=\sigma\sqrt t$, i.e. at

$$t^*=\Big(\frac{\sigma}{\mu}\Big)^2.\tag{10}$$

**Worked — 3M monthly log returns (T eq. 2.37, p. 74; slides 14–15).** $r_t=0.0103+a_t$, $\hat\sigma=0.0637$, $T=755$ months. The standard error of the mean is $0.0637/\sqrt{755}=0.0637/27.48=0.002318$ (Tsay rounds it to 0.0023), so

$$t=\frac{0.0103}{0.002318}=4.44,$$

the drift is significant at any usual level. By (10), $t^*=(0.0637/0.0103)^2=(6.184)^2=38.2$ months: after about three years the drift is larger than one sd of the accumulated noise. The slides simulate $n=10{,}000$ steps with $a_t\sim N(0,0.0637^2)$, with and without $\mu=0.0103$: at $t=10{,}000$ the drift has added $0.0103\times10{,}000=103$ to the log price, against a noise sd of $0.0637\times\sqrt{10{,}000}=6.37$. In Tsay's Figure 2.10 the log price of 3M follows the line $0.0103\,t$ closely for that reason.

**Trend-stationary alternative (slide 17; T §2.7.3, p. 75).**

$$p_t=\beta_0+\beta_1t+r_t,\qquad r_t\ \text{stationary (e.g. AR(}p\text{))}.\tag{11}$$

| | Mean | Variance | A shock at $t$ |
|---|---|---|---|
| RW with drift (7) | $p_0+\mu t$ | $t\sigma^2$, grows | permanent ($\psi_i=1$) |
| Trend-stationary (11) | $\beta_0+\beta_1t$ | $V(r_t)$, finite and constant | dies out ($\psi_i\to0$ in $r_t$) |

Both have a straight-line mean; only the variance tells them apart. Remove the trend from (11) by regression and $r_t$ is stationary; remove a trend from (8) and $\sum a_i$ is still a random walk. **Differencing** is the right transformation for (7), **detrending** for (11).

![Left: forecast bands against horizon up to 120 months. The random walk with drift has mean 0.0103 times l and a +/- 2 sigma sqrt(l) band that keeps widening to about +/- 1.40 at l = 120; the trend-stationary model with AR(1) phi = 0.9 deviations has the same mean line but a band that stops widening at +/- 2 times 0.146. Right: the density of the Dickey-Fuller t ratio from 20,000 seeded simulations with T = 250, centred near -1.5 and skewed left, against the N(0,1) density; the 5% critical value -2.86 is far left of -1.645](figures/L08-unit-root-bands-df.png)
*Figure — left: exact $\pm2$ sd forecast bands from (9) and from an AR(1) about the trend, L01-07 (15), with the 3M calibration $\mu=0.0103$, $\sigma=0.0637$ (T eq. 2.37). Right: the DF $t$ ratio of §5, simulated (seed 2026, $T=250$, 20,000 replications), against $N(0,1)$; W Table 18.2 (p. 575).*

On the left the two models share the mean line, but the random-walk band keeps opening ($2\times0.0637\sqrt{120}=1.40$ at ten years) while the trend-stationary band stops at $2\times0.0637/\sqrt{1-0.81}=0.29$ after a few half-lives. Ten years of data can be consistent with both, which is why the test of §5 has low power against $\phi$ near 1. The right panel is read in §5.

---

## 3 · C — what the constant term means (slide 16; T p. 74)

| Model | The constant is | Formula |
|---|---|---|
| MA($q$), T eq. (2.22) | the **mean** | $E(r_t)=c_0$ |
| stationary AR($p$) or ARMA($p,q$) | **related to the mean** | $\mu=\phi_0/(1-\phi_1-\dots-\phi_p)$ (L01-07 (21)) |
| random walk with drift (7) | the **time slope** | $E(p_t)=p_0+\mu t$ by (9) |

The third line follows from the second: as $\sum\phi_i\to1$ the denominator vanishes and the "mean" ceases to exist; the constant becomes the slope instead. Tsay adds the contrast with regression: in $r_t=\phi_0+\phi_1r_{t-1}+a_t$ the coefficient must satisfy $|\phi_1|\le1$ for the model to be meaningful, while in $y_t=\beta_0+\beta_1x_t+a_t$ the slope can be any real number (T p. 74).

---

## 4 · C — ARIMA($p$,1,$q$) and differencing (slides 18–19; T §2.7.4, pp. 75–76)

Allowing the AR polynomial of an ARMA to have a root at 1 gives an ARIMA model. **Definition (T p. 76):** $y_t$ is ARIMA($p$,1,$q$) if

$$c_t=y_t-y_{t-1}=(1-B)y_t\ \text{is a stationary and invertible ARMA}(p,q).\tag{12}$$

Write the stationary ARMA for $c_t$ as $\phi(B)c_t=\theta_0+\theta(B)a_t$ and substitute $c_t=(1-B)y_t$:

$$\phi(B)(1-B)\,y_t=\theta_0+\theta(B)a_t.\tag{13}$$

The AR polynomial of $y_t$ is $\phi(B)(1-B)$, which vanishes at $B=1$: a unit root. Like (4), the $\psi$ weights of $y_t$ do not decay, so ARIMA processes have "strong memory" (slide 18). The canonical case: log prices are ARIMA, **log returns** $r_t=\ln P_t-\ln P_{t-1}$ are stationary.

**Double unit roots.** If $y_t$ and $c_t$ are both unit-root nonstationary but $s_t=c_t-c_{t-1}=(1-B)^2y_t=y_t-2y_{t-1}+y_{t-2}$ is stationary, $y_t$ is $I(2)$, and ARIMA($p$,2,$q$) if $s_t$ is ARMA($p,q$). A nonzero mean of $s_t$ then implies a **quadratic** time trend in $y_t$ (one more level of integration than (8)). Tsay's candidate is the US GDP deflator (T p. 76; that is Exercise 2.15, not on our list).

---

## 5 · C — the Dickey–Fuller test (slides 20–23; T §2.7.5, pp. 76–77; W §18.2, pp. 574–576)

### 5.1 · The regressions and the hypothesis

$$p_t=\phi_1p_{t-1}+e_t\qquad(\text{T eq. 2.38}),\tag{14}$$

$$p_t=\phi_0+\phi_1p_{t-1}+e_t\qquad(\text{T eq. 2.39}),\tag{15}$$

$$H_0:\phi_1=1\quad\text{vs}\quad H_a:\phi_1<1.\tag{16}$$

The alternative is one-sided: $\phi_1>1$ would be explosive. Wooldridge writes (15) as $y_t=\alpha+\rho y_{t-1}+e_t$ (18.17) and subtracts $y_{t-1}$ from both sides, with $\theta=\rho-1$:

$$\Delta y_t=\alpha+\theta y_{t-1}+e_t\qquad(\text{W 18.21}),\qquad H_0:\theta=0\ \text{vs}\ H_1:\theta<0.\tag{17}$$

Testing $\rho=1$ in levels and $\theta=0$ in differences is the same test: the two regressions have the same residuals, and $\hat\theta=\hat\rho-1$ with the same standard error. **Note what is null:** the unit root ($I(1)$). "We do not take the null to be $I(0)$ … because $\{y_t\}$ is $I(0)$ for any value of $\rho$ strictly between $-1$ and $1$" (W p. 575).

### 5.2 · The $t$ ratio, derived

For (14) with $p_0=0$, least squares gives

$$\hat\phi_1=\frac{\sum_{t=1}^Tp_{t-1}p_t}{\sum_{t=1}^Tp_{t-1}^2},\qquad \hat\sigma_e^2=\frac{\sum_{t=1}^T(p_t-\hat\phi_1p_{t-1})^2}{T-1}.\tag{18}$$

Subtract 1 and put it over the common denominator:

$$\hat\phi_1-1=\frac{\sum p_{t-1}p_t-\sum p_{t-1}^2}{\sum p_{t-1}^2}=\frac{\sum p_{t-1}(p_t-p_{t-1})}{\sum p_{t-1}^2}.$$

Under $H_0$, (14) says $p_t-p_{t-1}=e_t$; substituting in place:

$$\hat\phi_1-1=\frac{\sum p_{t-1}\,(e_t)}{\sum p_{t-1}^2}.\tag{19}$$

The OLS standard error is $\mathrm{std}(\hat\phi_1)=\hat\sigma_e/\sqrt{\sum p_{t-1}^2}$. Dividing (19) by it:

$$\text{DF }t\text{ ratio}=\frac{\hat\phi_1-1}{\mathrm{std}(\hat\phi_1)}=\frac{\sum_{t=1}^Tp_{t-1}e_t}{\hat\sigma_e\sqrt{\sum_{t=1}^Tp_{t-1}^2}}\qquad(\text{T p. 77}).\tag{20}$$

### 5.3 · Why (20) is not $N(0,1)$

**W's argument (p. 575).** In (17), under $H_0$ the regressor $y_{t-1}$ is $I(1)$, "and so the usual central limit theorem that underlies the asymptotic standard normal distribution for the $t$ statistic does not apply." The sums in (20) are dominated by the late, large values of the walk ($\sum p_{t-1}^2$ is of order $T^2$, not $T$).

**U — one exact line that shows the skew.** Square (14) under $H_0$: $p_t^2=(p_{t-1}+e_t)^2=p_{t-1}^2+2p_{t-1}e_t+e_t^2$. Sum over $t=1,\dots,T$; the $p_{t-1}^2$ terms telescope, with $p_0=0$:

$$p_T^2=2\sum_{t=1}^Tp_{t-1}e_t+\sum_{t=1}^Te_t^2\quad\Longrightarrow\quad\sum_{t=1}^Tp_{t-1}e_t=\tfrac12\Big(p_T^2-\sum_{t=1}^Te_t^2\Big).\tag{21}$$

Divide by $T\sigma^2$. By L01-07 (18), $p_T\sim N(0,T\sigma^2)$ for Gaussian shocks, so $p_T^2/(T\sigma^2)\sim\chi^2_1$; and $\sum e_t^2/(T\sigma^2)\to1$. The numerator of (20) therefore behaves like $\tfrac12(\chi^2_1-1)$, which is **negative whenever $\chi^2_1<1$, probability 0.683**. Under the null, $\hat\phi_1<1$ about two times in three: the estimate is biased toward stationarity, and the $t$ ratio is shifted left. **G:** the limit is a functional of standard Brownian motion $W$, $t\Rightarrow\tfrac12[W(1)^2-1]\big/\sqrt{\int_0^1W(r)^2dr}$ (Chan and Wei 1988; Phillips 1987; T p. 77); named, not examinable.

### 5.4 · Three cases (T p. 77)

| Regression | True $\phi_0$ | Null law of the $t$ ratio |
|---|---|---|
| (14), no constant | 0 | DF (Brownian functional), critical values by simulation |
| (15), constant | 0 (driftless walk) | **another** nonstandard law (W Table 18.2) |
| (15), constant | $\ne0$ (walk with drift) | asymptotically **normal**, but "large sample sizes are needed" |

The third case is why the deterministic term has to match the alternative being considered, §6.

### 5.5 · Critical values (W Tables 18.2–18.3, pp. 575–577)

| Significance | 1% | 2.5% | 5% | 10% |
|---|---|---|---|---|
| constant, no trend (W Table 18.2) | $-3.43$ | $-3.12$ | $-2.86$ | $-2.57$ |
| constant + trend (W Table 18.3) | $-3.96$ | $-3.66$ | $-3.41$ | $-3.12$ |
| our simulation, constant, $T=250$ | $-3.45$ | $-3.16$ | $-2.87$ | $-2.58$ |

Reject $H_0$ when $t<c$. "If we use the standard normal critical value to test for a unit root, we would reject $H_0$ much more often than 5% of the time when $H_0$ is true" (W p. 575). **Worked (the figure, right panel):** in the seeded simulation, $P(t<-1.645\mid H_0)=0.465$. Using the normal 5% value is a **46.5% test**. A trend in the regression pushes the critical values further left because "detrending a unit root process tends to make it look more like an I(0) process" (W p. 577).

---

## 6 · C — the augmented DF test (slides 24–27; T eq. 2.40, p. 77; W eqs. 18.23–18.25)

### 6.1 · From AR($p$) to the $\Delta$ form

**AR(3), derived step by step** (slide 25). Start from

$$y_t=\phi_0+\phi_1y_{t-1}+\phi_2y_{t-2}+\phi_3y_{t-3}+e_t.\tag{22}$$

Express the far lags through $y_{t-1}$ and differences, $\Delta y_s=y_s-y_{s-1}$:

$$y_{t-2}=y_{t-1}-\Delta y_{t-1},\qquad y_{t-3}=y_{t-2}-\Delta y_{t-2}=y_{t-1}-\Delta y_{t-1}-\Delta y_{t-2}.\tag{23}$$

Substitute (23) into (22):

$$y_t=\phi_0+\phi_1y_{t-1}+\phi_2\big(y_{t-1}-\Delta y_{t-1}\big)+\phi_3\big(y_{t-1}-\Delta y_{t-1}-\Delta y_{t-2}\big)+e_t.$$

Collect terms:

$$y_t=\phi_0+(\phi_1+\phi_2+\phi_3)\,y_{t-1}-(\phi_2+\phi_3)\,\Delta y_{t-1}-\phi_3\,\Delta y_{t-2}+e_t.$$

Subtract $y_{t-1}$ from both sides:

$$\Delta y_t=\phi_0+\beta\,y_{t-1}+\tilde\phi_1\Delta y_{t-1}+\tilde\phi_2\Delta y_{t-2}+e_t,\tag{24}$$

$$\beta=\phi_1+\phi_2+\phi_3-1,\qquad\tilde\phi_1=-(\phi_2+\phi_3),\qquad\tilde\phi_2=-\phi_3.\tag{25}$$

(The slide prints the right-hand side as "$\tilde\phi_2\Delta y_{t-2}+\tilde\phi_2\Delta y_{t-2}$"; the first term is $\tilde\phi_1\Delta y_{t-1}$, as (24) shows.) **General AR($p$)** (slide 24): $\Delta y_t=\phi_0+\beta y_{t-1}+\sum_{i=1}^{p-1}\tilde\phi_i\Delta y_{t-i}+e_t$ with

$$\beta=-\phi(1)=\phi_1+\dots+\phi_p-1.\tag{26}$$

**A (single) unit root means $\phi(1)=0$**, i.e. $1$ solves the characteristic equation $1-\phi_1x-\dots-\phi_px^p=0$ (L08-01), i.e. $\beta=0$, i.e.

$$\phi_1+\phi_2+\dots+\phi_p=1.\tag{27}$$

### 6.2 · The ADF regression and statistic

Tsay writes the regression in levels:

$$x_t=c_t+\beta x_{t-1}+\sum_{i=1}^{p-1}\phi_i\Delta x_{t-i}+e_t,\qquad H_0:\beta=1\ \text{vs}\ H_a:\beta<1\qquad(\text{T eq. 2.40}),\tag{28}$$

$$\text{ADF}=\frac{\hat\beta-1}{\mathrm{std}(\hat\beta)},\qquad c_t\in\{0,\ \omega_0,\ \omega_0+\omega_1t\}.\tag{29}$$

Equivalently $\Delta x_t=c_t+c\,x_{t-1}+\sum\phi_i\Delta x_{t-i}+e_t$ with $c=\beta-1$ and $H_0:c=0$ vs $c<0$. **Here $\beta$ in (28) is the levels coefficient (null 1); the $\beta$ of (26) is the $\Delta$-form coefficient (null 0).** The slides use both names; the statistic is the same.

The lagged differences "clean up any serial correlation in $\Delta y_t$" (W p. 576). Too few lags: wrong size even asymptotically; too many: lower power. The $t$ statistics on the $\Delta y_{t-i}$ terms do have the usual asymptotic $t$ law, so standard tests can choose the lag length (W p. 577).

**Deterministic term.** Use $c_t=\omega_0+\omega_1t$ when the series trends (alternative: trend-stationary (11)). Without the trend, "if we carry out the usual DF or augmented DF test on a trending but I(0) series, we will probably have little power for rejecting a unit root" (W p. 577). Then the critical values of W Table 18.3 apply.

### 6.3 · Worked — Wooldridge's three examples

**T-bill rate (W Example 18.2, p. 576, eq. 18.22).** $\widehat{\Delta r3_t}=0.625-0.091\,r3_{t-1}$, standard errors $(0.261)$ and $(0.037)$, $n=123$. So $\hat\rho=1+\hat\theta=1-0.091=0.909$ and

$$t=\frac{-0.091}{0.037}=-2.46>-2.57,$$

fail to reject even at 10%. **Failing to reject is not accepting.** A standard $t$ test of $\rho=0.9$ (valid, since $y_t$ is $I(0)$ under that null) gives $(0.909-0.9)/0.037=0.24$: no evidence against $\rho=0.9$ either, and "it makes no sense to accept $\rho=1$ and $\rho=.9$" (W p. 576). With $\rho=0.9$, observations ten periods apart have correlation $0.9^{10}=0.35$, not nearly one.

**US inflation (W Example 18.3, p. 577).** $\widehat{\Delta inf_t}=1.36-0.310\,inf_{t-1}+0.138\,\Delta inf_{t-1}$, s.e. $(0.517)(0.103)(0.126)$, $n=47$:

$$t=\frac{-0.310}{0.103}=-3.01<-2.86\quad\Rightarrow\quad\text{reject at 5\%},\qquad\hat\rho=0.690.$$

Dropping the insignificant lag gives $\hat\theta=-0.335$, $t=-3.13$: slightly stronger.

**US log GDP with a trend (W Example 18.4, p. 578, eq. 18.26).** $\widehat{gGDP_t}=1.65+0.0059\,t-0.210\log(GDP_{t-1})+0.264\,gGDP_{t-1}$, s.e. $(0.67)(0.0027)(0.087)(0.165)$, $n=35$:

$$t=\frac{-0.210}{0.087}=-2.41>-3.12\ (10\%,\ \text{Table 18.3})\quad\Rightarrow\quad\text{do not reject},$$

although $\hat\rho=1-0.21=0.79$. With $n=35$, a near-unit root cannot be told from a unit root. Without the trend, $\hat\theta=-0.023$, $t=-1.92$: "the estimate of $\rho$ is much closer to one, but this is misleading due to the omitted time trend" (W p. 578).

---

## 7 · C — the decks' examples: US GDP and the S&P 500 (slides 28–31; T Example 2.2, pp. 78–81; `unitroot.html`)

**US quarterly log GDP, 1947.I–2008.IV.** The level trends upward with sample ACF near 1; the difference (growth) varies around a fixed mean. With $p=10$ lags (chosen from the PACF of the differences), Tsay reports the ADF **$-1.701$, p-value 0.4297** (S-Plus, constant), with coefficient on the lagged level $-0.0008$ (s.e. 0.0005), so

$$\hat\beta=1+\hat c=1-0.0008=0.9992\qquad(\text{T p. 78}).$$

The R run in Tsay's book (`fUnitRoots`) prints $-1.6109$, p 0.4569; the slides round it to "$-1.61$ with a p-value 0.45". The site page runs `tseries::adf.test(gdp, k=10)` and prints **Dickey–Fuller $=-0.37047$, p-value 0.9872**. The difference is the regression, not the data: `adf.test` always includes a constant **and a linear trend**, so its statistic is compared with the trend critical values (W Table 18.3). Three numbers, one conclusion: **the unit root is not rejected.**

**S&P 500 log index, 3 Jan 1950 – 16 Apr 2008, 14,462 days.** To test "random walk with drift" against trend stationarity, $c_t=\omega_0+\omega_1t$ and $p=15$: ADF **$-1.998$, p 0.602** (T p. 79). The constant (0.0019, $t=2.39$) is significant, the trend (t ratio 1.85, p 0.064) only at 10%: "the log series of the S&P 500 index contains a unit root and a positive drift, but there is no strong evidence of a time trend" (T p. 80). The R value in the book is $-1.9946$ (p 0.5807). The site page picks $k=2$ by `ar(diff(sp5))` (AR order 2, coefficients 0.0721 and $-0.0387$, mean daily return 0.000299) and prints `adf.test(sp5, k=2)` $=-2.0179$, p 0.5708; the PDF deck's $k=10$ run gives $-1.9482$, p 0.6004. **On the differences**, `adf.test(diff(sp5), k=10)` gives $-37.537$ with "p-value = 0.01": `tseries` truncates p-values at 0.01, so read it as $p\le0.01$. Log prices are $I(1)$, log returns $I(0)$.

> **Read an ADF output with three questions: which deterministic terms, how many lags, which table.** The three GDP statistics ($-1.70$, $-1.61$, $-0.37$) differ because the regressions differ.

---

## 8 · C — spurious regression (W §18.3, pp. 578–580)

Let $x_t=x_{t-1}+a_t$ and $y_t=y_{t-1}+e_t$ (W 18.27–18.28) with independent iid shocks and $x_0=y_0=0$: the two series are independent. Regress $y_t$ on $x_t$ (W 18.29) and test $\beta_1=0$ at 5%. Granger and Newbold (1974) found frequent "significance"; in Davidson and MacKinnon's simulation the usual $t$ test rejects **66.2% of the time at $n=50$ and 84.7% at $n=250$** (W p. 579): it gets worse with more data.

**Why.** Under $H_0:\beta_1=0$ the model $y_t=\beta_0+\beta_1x_t+u_t$ (W 18.30) can hold only with $\beta_0=0$ and

$$u_t=y_t=\sum_{j=1}^te_j,\tag{30}$$

a **random walk error**: the errors are not even weakly dependent, so neither the $t$ statistic (which diverges as $n\to\infty$) nor $R^2$ (which converges to a random variable, not to a population value) has its usual behaviour (W pp. 579–580). Adding a time trend does not fix it. The safe course is to difference $I(1)$ variables first (§4); then $\Delta y_t$ on $\Delta x_t$ is a regression of white noise on white noise.

**G — named only:** when some combination $y_t-bx_t$ is $I(0)$ the two $I(1)$ series are *cointegrated* and the levels regression is meaningful (W §18.4). Cointegration is in the syllabus table but not on the class schedule ([[../../Map/class-plan|Map/class-plan]], "Syllabus items not on the site schedule").

---

## 9 · U — reading it as an economist

A unit root in log GDP means a recession's output loss is never made up: the level forecast is today's level plus drift, (3) with (8). A trend-stationary GDP returns to its old trend line. The tests cannot reliably choose between them on post-war data (W Example 18.4: $\hat\rho=0.79$, not rejected), which is why the decks state conclusions as "cannot be rejected" and work with growth rates. For asset prices, the unit root is the statement that returns are unpredictable in level terms, which is where the volatility models of [[L08-06-arch-garch]] start: the *returns* are serially uncorrelated, their *squares* are not.

---

## Links

- Neighbours: [[L08-02-forecasting-ma-arma]] (the $\psi$-weight forecast variance (2.34) that (6) specialises) · [[L08-04-long-memory-arfima]] (memory between $\psi_i\to0$ geometrically and $\psi_i=1$).
- Unit: [[L08-00-map]] · [[L08-10-formulas]] · [[L08-11-pitfalls]] · [[L08-12-python]] (the DF simulation and `adfuller` on simulated series).
- Class 1: [[../L01/L01-07-ar-var-review|L01-07]] §6–§7 (equilibrium law, random walk variance $t\sigma^2$, persistence $\sqrt{t/(t+h)}$).
- Rules: [[../../rules/04_arima_raiz_unitaria|rules/04]] (ARIMA, unit roots).
- **Practice (number and printed page only):** W 18.C13 (p. 604). Worked solutions: `Listas/lista-L08-book-exercises.pdf`.
