---
tags: [notes, lecture-08, time-series, volatility, arch, garch, igarch, kurtosis, volatility-forecast, petrobras]
date: 2026-10-25
status: taught
source: "garchmodeling.html (ARCH and GARCH sections, Petrobras 2000–2021, n = 5167); garch-sv-petrobras.html (ARCH, GARCH, GARCH-t, Petrobras 2000–2025); T §3.1–3.3 (pp. 110–115), §3.4 (pp. 115–131: eqs. 3.5–3.13, Ex. 3.1 Intel, Ex. 3.2), §3.5 (pp. 131–140: eqs. 3.14–3.21, Ex. 3.3 S&P 500, Table 3.1 p. 138, two-pass p. 140), §3.6 (pp. 140–142: eq. 3.22), §3.16 (pp. 165–166); W §12.6 (pp. 391–396: eqs. 12.46–12.50, Ex. 12.8)"
---

# 3.1–3.6 · ARCH and GARCH: a variance that is forecastable, a kurtosis that is not normal

> **Claim.** **Returns can be serially uncorrelated and still dependent: their conditional variance moves.** ARCH writes that variance as a linear function of past squared shocks, $\sigma_t^2=\alpha_0+\sum\alpha_ia_{t-i}^2$. That one equation produces volatility clusters and, even with Gaussian innovations, **unconditional kurtosis above 3**: $3(1-\alpha_1^2)/(1-3\alpha_1^2)$ for ARCH(1). **GARCH adds the lagged variance and is an ARMA model for $a_t^2$**: $\sigma_\infty^2=\alpha_0/(1-\alpha_1-\beta_1)$, and forecasts decay to it at rate $\alpha_1+\beta_1$. The empirical regularity is $\alpha_1+\beta_1$ close to 1 (0.9727 for Tsay's S&P 500, 0.980 for Petrobras), so a volatility shock has a half-life of months or weeks. At $\alpha_1+\beta_1=1$ (IGARCH) the variance has a unit root, the unconditional variance does not exist, and RiskMetrics' exponential smoothing is the special case $\alpha_0=0$.
> Prev: [[L08-05-seasonal-airline-model]] · Next: [[L08-07-garch-family-asymmetry-tails]] · Map: [[L08-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $r_t$ | log return at $t$ (garch-sv-petrobras.html uses simple returns) | |
| $F_{t-1}$ | information at $t-1$ | |
| $\mu_t=E(r_t\mid F_{t-1})$ | conditional mean (mean equation) | |
| $a_t=r_t-\mu_t$ | shock, innovation | |
| $\sigma_t^2=V(r_t\mid F_{t-1})$ | conditional variance (volatility equation); $\sigma_t$ the volatility | $>0$ |
| $\varepsilon_t=a_t/\sigma_t$ | standardized innovation, iid, mean 0, variance 1 | |
| $\alpha_0,\alpha_i,\beta_j$ | constant, ARCH and GARCH coefficients | $\alpha_0>0$; $\alpha_i,\beta_j\ge0$ |
| $m,s$ | ARCH and GARCH orders | |
| $\eta_t=a_t^2-\sigma_t^2$ | "variance surprise", martingale difference | |
| $\sigma_\infty^2$ | unconditional variance $E(a_t^2)$ | |
| $\sigma_h^2(\ell)$ | $\ell$-step variance forecast at origin $h$ | |
| $K$ | excess kurtosis of $\varepsilon_t$: $E(\varepsilon_t^4)=K+3$ | $K=0$ normal |
| $\nu$ | degrees of freedom of the standardized Student-$t$ | $\nu>2$ |

**Mapping to the site pages.** garchmodeling.html writes $y_t=\sigma_t\varepsilon_t$ and $\sigma_t^2=\omega+\alpha_1\varepsilon_{t-1}^2+\beta_1\sigma_{t-1}^2$: its $\omega$ is Tsay's $\alpha_0$, and the $\varepsilon_{t-1}$ inside the recursion must be read as the **raw residual** $a_{t-1}=y_{t-1}$ (fGarch filters the residuals, not the standardized ones). Taken literally, $\sigma_t^2=\omega+\alpha_1\varepsilon_{t-1}^2$ with $\varepsilon$ standardized would make $\sigma_t^2$ independent of the level of past volatility. Some authors write $h_t$ for $\sigma_t^2$ (T p. 117; bayes-garch.pdf does).

---

## 1 · U — what volatility does (T §3.1, pp. 110–111)

Volatility is **not observed**: one return per day carries no variance by itself. Implied volatility (VIX) rests on an option-pricing model. Tsay lists four regularities that any model must reproduce:

1. **clusters**: high-volatility periods and calm periods;
2. **continuity**: volatility evolves smoothly, jumps are rare;
3. **mean reversion within a range**: volatility does not diverge, so it is "often stationary";
4. **leverage**: a big price drop raises volatility more than a big rise of the same size.

ARCH/GARCH capture 1–3. Fact 4 needs the asymmetric models of [[L08-07-garch-family-asymmetry-tails]]. The motivating evidence is already in L01: IBM monthly returns pass Ljung–Box at lag 30, while their squares give $Q(30)=182.12$ → [[../L01/L01-07-ar-var-review|L01-07]] §2.

---

## 2 · C — the structure of a volatility model (T §3.2–3.3, pp. 111–115)

The conditional mean and variance of $r_t$ given $F_{t-1}$ are

$$\mu_t=E(r_t\mid F_{t-1}),\qquad \sigma_t^2=V(r_t\mid F_{t-1})=E[(r_t-\mu_t)^2\mid F_{t-1}].\tag{1}$$

The **mean equation** is a simple stationary ARMA with regressors (T eq. 3.3):

$$r_t=\mu_t+a_t,\qquad \mu_t=\sum_{i=1}^p\phi_iy_{t-i}-\sum_{i=1}^q\theta_ia_{t-i},\qquad y_t=r_t-\phi_0-\sum_{i=1}^k\beta_ix_{it}.\tag{2}$$

Because $\mu_t$ is known at $t-1$, substituting (2) into (1) gives (T eq. 3.4)

$$\sigma_t^2=V(\mu_t+a_t\mid F_{t-1})=V(a_t\mid F_{t-1}).\tag{3}$$

**A volatility model is an equation for (3).** GARCH makes $\sigma_t^2$ an exact function of $F_{t-1}$. Stochastic volatility adds its own shock ([[L08-08-stochastic-volatility]]).

**Four steps** (T p. 113): (i) fit the mean equation and remove linear dependence; (ii) test the residuals for ARCH effects; (iii) if present, specify a volatility model and estimate mean and volatility **jointly**; (iv) check and refine.

### 2.1 · C — testing for ARCH effects (T §3.3.1, p. 114)

**McLeod–Li:** apply Ljung–Box $Q(m)$ (L01-07 (3)) to the series $a_t^2$.

**Engle's LM test:** run the auxiliary regression

$$a_t^2=\alpha_0+\alpha_1a_{t-1}^2+\dots+\alpha_ma_{t-m}^2+e_t,\qquad t=m+1,\dots,T,\tag{4}$$

and test $H_0:\alpha_1=\dots=\alpha_m=0$ with

$$F=\frac{(SSR_0-SSR_1)/m}{SSR_1/(T-2m-1)},\qquad SSR_0=\sum_{t=m+1}^T(a_t^2-\bar\omega)^2,\quad \bar\omega=\frac1T\sum_{t=1}^Ta_t^2,\quad SSR_1=\sum_{t=m+1}^T\hat e_t^2.\tag{5}$$

Tsay states that (5) is asymptotically $\chi^2_m$. Strictly it is $m\cdot F$ (equivalently $T R^2$ of (4)) that has the $\chi^2_m$ limit; the software prints that statistic against $\chi^2_m$.

**Worked — Intel monthly log returns 1973–2008, $T=432$ (T pp. 114–115).** Returns: $Q(12)=18.26$, $p=0.108$, no serial correlation, so $a_t=r_t-\bar r$. Squares: $Q(12)=89.85$, $p=5.3\times10^{-14}$. LM statistic 53.62 on $\chi^2_{12}$, $p\approx0$. **Uncorrelated but not independent.**

---

## 3 · C — the ARCH model (T §3.4, pp. 115–123)

An **ARCH($m$)** model (Engle, 1982; T eq. 3.5):

$$a_t=\sigma_t\varepsilon_t,\qquad \sigma_t^2=\alpha_0+\alpha_1a_{t-1}^2+\dots+\alpha_ma_{t-m}^2,\qquad \varepsilon_t\ \text{iid},\ E\varepsilon_t=0,\ V\varepsilon_t=1,\tag{6}$$

with $\alpha_0>0$ and $\alpha_i\ge0$, which keep $\sigma_t^2>0$. A large $a_{t-1}^2$ makes $\sigma_t^2$ large, which makes a large $\lvert a_t\rvert$ **more likely** but not certain: that is the cluster.

### 3.1 · Moments of ARCH(1) (T pp. 117–118)

Take $m=1$: $\sigma_t^2=\alpha_0+\alpha_1a_{t-1}^2$.

**Mean.** By iterated expectations, with $\sigma_t$ known at $t-1$ and $E\varepsilon_t=0$:

$$E(a_t)=E[E(a_t\mid F_{t-1})]=E[\sigma_tE(\varepsilon_t)]=0.\tag{7}$$

**Variance.** $E(a_t^2\mid F_{t-1})=\sigma_t^2E(\varepsilon_t^2)=\sigma_t^2$, so

$$V(a_t)=E(a_t^2)=E[E(a_t^2\mid F_{t-1})]=E(\alpha_0+\alpha_1a_{t-1}^2)=\alpha_0+\alpha_1E(a_{t-1}^2).$$

Under stationarity $E(a_t^2)=E(a_{t-1}^2)=V(a_t)$:

$$V(a_t)=\alpha_0+\alpha_1V(a_t)\iff V(a_t)=\frac{\alpha_0}{1-\alpha_1},\qquad 0\le\alpha_1<1.\tag{8}$$

**Fourth moment.** With Gaussian $\varepsilon_t$, $E(\varepsilon_t^4)=3$:

$$E(a_t^4\mid F_{t-1})=\sigma_t^4E(\varepsilon_t^4)=3\sigma_t^4=3(\alpha_0+\alpha_1a_{t-1}^2)^2.\tag{9}$$

Expand the square and take expectations:

$$E(a_t^4)=3E\big(\alpha_0^2+2\alpha_0\alpha_1a_{t-1}^2+\alpha_1^2a_{t-1}^4\big)=3\big[\alpha_0^2+2\alpha_0\alpha_1V(a_t)+\alpha_1^2E(a_{t-1}^4)\big].$$

Under fourth-order stationarity $m_4=E(a_t^4)=E(a_{t-1}^4)$; substitute (8) for $V(a_t)$:

$$m_4=3\Big[\alpha_0^2+2\alpha_0\alpha_1\Big(\frac{\alpha_0}{1-\alpha_1}\Big)+\alpha_1^2m_4\Big].\tag{10}$$

Collect the $m_4$ terms:

$$m_4(1-3\alpha_1^2)=3\alpha_0^2\Big(1+\frac{2\alpha_1}{1-\alpha_1}\Big)=3\alpha_0^2\,\frac{1+\alpha_1}{1-\alpha_1}$$

$$m_4=\frac{3\alpha_0^2(1+\alpha_1)}{(1-\alpha_1)(1-3\alpha_1^2)}.\tag{11}$$

Since $m_4>0$, it exists only if $1-3\alpha_1^2>0$, i.e. $\alpha_1^2<1/3$ ($\alpha_1<0.577$). **Kurtosis**, dividing (11) by the square of (8):

$$\frac{m_4}{[V(a_t)]^2}=\frac{3\alpha_0^2(1+\alpha_1)}{(1-\alpha_1)(1-3\alpha_1^2)}\cdot\frac{(1-\alpha_1)^2}{\alpha_0^2}=\frac{3(1+\alpha_1)(1-\alpha_1)}{1-3\alpha_1^2}=3\,\frac{1-\alpha_1^2}{1-3\alpha_1^2}>3.\tag{12}$$

> **Gaussian conditionally, fat-tailed unconditionally.** A mixture of normals with random variances has heavier tails than a normal, so ARCH "produces outliers" more often than Gaussian white noise (T p. 118). Every $\alpha_1\in(0,1/\sqrt3)$ gives kurtosis above 3.

### 3.2 · Weaknesses (T p. 119)

(1) Positive and negative shocks enter through $a_{t-1}^2$, so they have the **same** effect (no leverage). (2) It is restrictive: for ARCH(1) with a finite fourth moment, $\alpha_1^2<1/3$, which limits the kurtosis it can generate. (3) It describes, it does not explain. (4) It responds slowly to large isolated shocks and tends to **over-predict** volatility afterwards.

### 3.3 · Order, likelihood, checking, forecasts (T pp. 119–123)

**Order.** Define $\eta_t=a_t^2-\sigma_t^2$. Substituting $\sigma_t^2=a_t^2-\eta_t$ into (6):

$$a_t^2=\alpha_0+\alpha_1a_{t-1}^2+\dots+\alpha_ma_{t-m}^2+\eta_t,\tag{13}$$

an AR($m$) for $a_t^2$ with uncorrelated (but not iid) errors. So **the PACF of $a_t^2$ suggests $m$** (T p. 120), as the PACF suggested $p$ in [[L08-01-ar2-arp-cycles-identification]].

**Gaussian conditional likelihood.** The joint density factors into one-step conditionals; dropping the density of the first $m$ shocks (T p. 120):

$$f(a_{m+1},\dots,a_T\mid\alpha,a_1,\dots,a_m)=\prod_{t=m+1}^T\frac{1}{\sqrt{2\pi\sigma_t^2}}\exp\Big(-\frac{a_t^2}{2\sigma_t^2}\Big),\tag{14}$$

$$\ell(\alpha)=-\frac12\sum_{t=m+1}^T\Big[\ln(2\pi)+\ln\sigma_t^2+\frac{a_t^2}{\sigma_t^2}\Big],\tag{15}$$

where $\sigma_t^2$ is computed recursively from (6). There is no closed form: (15) is maximised numerically ([[L08-12-python]] does it with `scipy.optimize`).

**Standardized Student-$t$ (T eq. 3.7).** If $x_\nu\sim t_\nu$, then $V(x_\nu)=\nu/(\nu-2)$ for $\nu>2$, so $\varepsilon_t=x_\nu/\sqrt{\nu/(\nu-2)}$ has variance 1. Change variables $x=\varepsilon\sqrt{\nu/(\nu-2)}$ in the $t_\nu$ density, using $x^2/\nu=\varepsilon^2/(\nu-2)$ and the Jacobian $\sqrt{\nu/(\nu-2)}$:

$$f(\varepsilon\mid\nu)=\frac{\Gamma\big(\frac{\nu+1}2\big)}{\sqrt{\nu\pi}\,\Gamma\big(\frac\nu2\big)}\Big(1+\frac{\varepsilon^2}{\nu-2}\Big)^{-\frac{\nu+1}2}\sqrt{\frac{\nu}{\nu-2}}=\frac{\Gamma\big(\frac{\nu+1}2\big)}{\Gamma\big(\frac\nu2\big)\sqrt{(\nu-2)\pi}}\Big(1+\frac{\varepsilon^2}{\nu-2}\Big)^{-\frac{\nu+1}2}.\tag{16}$$

**The rescaling matters**: it keeps $\sigma_t^2$ the conditional *variance*, so the volatility equation means the same thing under both distributions. With $a_t=\sigma_t\varepsilon_t$, $f(a_t\mid F_{t-1})=f(a_t/\sigma_t\mid\nu)/\sigma_t$, and for fixed $\nu$ the log-likelihood is, up to a constant (T eq. 3.8),

$$\ell(\alpha)=-\sum_{t=m+1}^T\Big[\frac{\nu+1}2\ln\Big(1+\frac{a_t^2}{(\nu-2)\sigma_t^2}\Big)+\frac12\ln\sigma_t^2\Big].\tag{17}$$

Estimating $\nu$ jointly adds $(T-m)\big[\ln\Gamma(\frac{\nu+1}2)-\ln\Gamma(\frac\nu2)-\frac12\ln((\nu-2)\pi)\big]$. Prespecified values are usually between 4 and 8. Skew-$t$ (T eq. 3.9, Fernández–Steel) and GED (T eq. 3.10) are the other options; they are read in [[L08-07-garch-family-asymmetry-tails]] §5.

**Checking.** If the model is right, $\tilde a_t=a_t/\hat\sigma_t$ is iid: Ljung–Box on $\tilde a_t$ checks the mean equation, on $\tilde a_t^2$ the volatility equation, and skewness, kurtosis and a QQ plot check the distribution (T pp. 122–123).

**Forecasts** (T eq. 3.11). At origin $h$, $\sigma_h^2(1)=\alpha_0+\alpha_1a_h^2+\dots+\alpha_ma_{h+1-m}^2$, and in general

$$\sigma_h^2(\ell)=\alpha_0+\sum_{i=1}^m\alpha_i\,\sigma_h^2(\ell-i),\qquad \sigma_h^2(\ell-i)=a_{h+\ell-i}^2\ \text{if}\ \ell-i\le0,\tag{18}$$

the AR forecast recursion of [[L08-02-forecasting-ma-arma]] applied to (13).

### 3.4 · Worked — Intel ARCH (T Ex. 3.1, pp. 123–126)

ARCH(3), Gaussian: $\sigma_t^2=0.0106+0.2131a_{t-1}^2+0.0770a_{t-2}^2+0.0599a_{t-3}^2$, with $\alpha_2,\alpha_3$ insignificant ($t=1.60$ and $0.87$). Dropping them (T eq. 3.12):

$$r_t=0.0126+a_t,\qquad \sigma_t^2=0.0111+0.3560\,a_{t-1}^2,\tag{19}$$

with standard errors 0.0053, 0.0010, 0.0761. Checks: $Q(10)=12.64$ ($p=0.24$) for $\tilde a_t$, $Q(10)=14.75$ ($p=0.14$) for $\tilde a_t^2$. Adequate.

- Mean return 1.26% a month.
- $\hat\alpha_1^2=0.356^2=0.1267<1/3$: the fourth moment exists.
- Unconditional sd by (8): $\sqrt{0.0111/(1-0.356)}=\sqrt{0.0111/0.644}=\sqrt{0.017236}=0.1313$. Tsay prints "$\approx0.1315$" from unrounded estimates.
- Kurtosis by (12): $3(1-0.126736)/(1-3\times0.126736)=3(0.873264)/0.619792=4.227$.

**$t$ innovations** (T eq. 3.13): $r_t=0.0169+a_t$, $\sigma_t^2=0.0120+0.2845a_{t-1}^2$, $\hat\nu=6.01$ (se 1.50). Unconditional sd $\sqrt{0.0120/0.7155}=0.1295$. **The heavy-tailed $\varepsilon_t$ takes over part of the kurtosis, and $\hat\alpha_1$ falls from 0.356 to 0.2845.** Here $Q(12)=35.42$ ($p=0.0004$) for $\tilde a_t^2$, driven by a lag-12 ACF of 0.188, which points to GARCH.

---

## 4 · C — GARCH (T §3.5, pp. 131–138)

ARCH often needs many lags (an ARCH(9) for the S&P 500 monthly series, T p. 131). Bollerslev's (1986) **GARCH($m,s$)** (T eq. 3.14):

$$a_t=\sigma_t\varepsilon_t,\qquad \sigma_t^2=\alpha_0+\sum_{i=1}^m\alpha_ia_{t-i}^2+\sum_{j=1}^s\beta_j\sigma_{t-j}^2,\qquad \sum_{i=1}^{\max(m,s)}(\alpha_i+\beta_i)<1.\tag{20}$$

### 4.1 · GARCH is ARMA for $a_t^2$

$\eta_t=a_t^2-\sigma_t^2$ is a martingale difference: $E(\eta_t\mid F_{t-1})=\sigma_t^2E(\varepsilon_t^2-1)=0$, so $E\eta_t=0$ and $\mathrm{Cov}(\eta_t,\eta_{t-j})=0$ for $j\ge1$. It is not iid. Substitute $\sigma_{t-i}^2=a_{t-i}^2-\eta_{t-i}$ ($i=0,\dots,s$) into (20):

$$a_t^2-\eta_t=\alpha_0+\sum_{i=1}^m\alpha_ia_{t-i}^2+\sum_{j=1}^s\beta_j(a_{t-j}^2-\eta_{t-j}),$$

$$a_t^2=\alpha_0+\sum_{i=1}^{\max(m,s)}(\alpha_i+\beta_i)a_{t-i}^2+\eta_t-\sum_{j=1}^s\beta_j\eta_{t-j}.\tag{21}$$

That is T eq. (3.15), an ARMA($\max(m,s),s$) for $a_t^2$: **AR coefficients $\alpha_i+\beta_i$, MA coefficients $\beta_j$.** The ARMA mean formula of [[L08-02-forecasting-ma-arma]] gives

$$\sigma_\infty^2=E(a_t^2)=\frac{\alpha_0}{1-\sum_{i=1}^{\max(m,s)}(\alpha_i+\beta_i)}.\tag{22}$$

### 4.2 · GARCH(1,1): kurtosis (T §3.16, pp. 165–166)

$$\sigma_t^2=\alpha_0+\alpha_1a_{t-1}^2+\beta_1\sigma_{t-1}^2,\qquad 0\le\alpha_1,\beta_1\le1,\quad \alpha_1+\beta_1<1.\tag{23}$$

Let $E(\varepsilon_t^4)=K+3$, $v=E(\sigma_t^2)=\alpha_0/(1-\alpha_1-\beta_1)$ by (22), and $s_4=E(\sigma_t^4)$. Then $E(a_t^4)=(K+3)s_4$ and, since $\sigma_{t-1}$ is known before $\varepsilon_{t-1}$ is drawn, $E(\sigma_{t-1}^2a_{t-1}^2)=E(\sigma_{t-1}^4\varepsilon_{t-1}^2)=s_4$. Square (23):

$$\sigma_t^4=\alpha_0^2+\alpha_1^2a_{t-1}^4+\beta_1^2\sigma_{t-1}^4+2\alpha_0\alpha_1a_{t-1}^2+2\alpha_0\beta_1\sigma_{t-1}^2+2\alpha_1\beta_1\sigma_{t-1}^2a_{t-1}^2.$$

Take expectations, stationarity giving $E\sigma_t^4=E\sigma_{t-1}^4=s_4$:

$$s_4=\alpha_0^2+\alpha_1^2(K+3)s_4+\beta_1^2s_4+2\alpha_0(\alpha_1+\beta_1)v+2\alpha_1\beta_1s_4.$$

The $s_4$ coefficients add to $(K+3)\alpha_1^2+\beta_1^2+2\alpha_1\beta_1=(\alpha_1+\beta_1)^2+(K+2)\alpha_1^2$. Write $\pi=\alpha_1+\beta_1$:

$$s_4\big[1-\pi^2-(K+2)\alpha_1^2\big]=\alpha_0^2+2\alpha_0\pi\Big(\frac{\alpha_0}{1-\pi}\Big)=\alpha_0^2\,\frac{1+\pi}{1-\pi},$$

$$s_4=\frac{\alpha_0^2(1+\pi)}{(1-\pi)\big[1-\pi^2-(K+2)\alpha_1^2\big]}.\tag{24}$$

Kurtosis of $a_t$, dividing $(K+3)s_4$ by $v^2=\alpha_0^2/(1-\pi)^2$:

$$\frac{E(a_t^4)}{[E(a_t^2)]^2}=\frac{(K+3)(1+\pi)(1-\pi)}{1-\pi^2-(K+2)\alpha_1^2}=\frac{(K+3)(1-\pi^2)}{1-\pi^2-(K+2)\alpha_1^2}.$$

With Gaussian $\varepsilon_t$ ($K=0$) the excess kurtosis is

$$K_a^{(g)}=\frac{3(1-\pi^2)}{1-\pi^2-2\alpha_1^2}-3=\frac{6\alpha_1^2}{1-2\alpha_1^2-(\alpha_1+\beta_1)^2},\tag{25}$$

finite iff $1-2\alpha_1^2-(\alpha_1+\beta_1)^2>0$ (T p. 132). **$\alpha_1$, not $\beta_1$, creates the fat tails**: with $\alpha_1=0$, $K_a^{(g)}=0$. With $\beta_1=0$, (25) collapses to (12): $6\alpha_1^2/(1-3\alpha_1^2)$ is the excess of $3(1-\alpha_1^2)/(1-3\alpha_1^2)$.

### 4.3 · GARCH(1,1): forecasts (T pp. 133)

Write $a_t^2=\sigma_t^2\varepsilon_t^2$ in (23), one period ahead:

$$\sigma_{t+1}^2=\alpha_0+(\alpha_1+\beta_1)\sigma_t^2+\alpha_1\sigma_t^2(\varepsilon_t^2-1).\tag{26}$$

At origin $h$, $\sigma_h^2(1)=\alpha_0+\alpha_1a_h^2+\beta_1\sigma_h^2$ is known. Set $t=h+1$ in (26) and take $E(\cdot\mid F_h)$, using $E(\varepsilon_{h+1}^2-1\mid F_h)=0$; repeat:

$$\sigma_h^2(\ell)=\alpha_0+(\alpha_1+\beta_1)\,\sigma_h^2(\ell-1),\qquad \ell>1,\tag{27}$$

an AR(1) recursion with coefficient $\pi=\alpha_1+\beta_1$ (T eq. 3.17). Iterate (27) $\ell-1$ times and sum the geometric series:

$$\sigma_h^2(\ell)=\alpha_0\big[1+\pi+\dots+\pi^{\ell-2}\big]+\pi^{\ell-1}\sigma_h^2(1)=\frac{\alpha_0(1-\pi^{\ell-1})}{1-\pi}+\pi^{\ell-1}\sigma_h^2(1).$$

Substitute $\alpha_0/(1-\pi)=\sigma_\infty^2$ from (22):

$$\sigma_h^2(\ell)=\sigma_\infty^2+\pi^{\ell-1}\big[\sigma_h^2(1)-\sigma_\infty^2\big]\ \xrightarrow{\ \ell\to\infty\ }\ \sigma_\infty^2\quad(\pi<1).\tag{28}$$

**Half-life of a volatility shock**: the horizon at which the gap $\sigma_h^2(\ell)-\sigma_\infty^2$ has halved, $\pi^{\ell}=\tfrac12$:

$$\ell_{1/2}=\frac{\ln0.5}{\ln(\alpha_1+\beta_1)},\tag{29}$$

the AR(1) half-life of L01-07 (17) applied to (27).

![Left: sigma_h(l) over sigma_infinity for three volatility models started at twice the unconditional level; Tsay's S&P 500 GARCH (persistence 0.9727) decays fastest, Petrobras (0.9800) more slowly, while the IGARCH line rises linearly in variance. Right: the (alpha1, beta1) plane with the IGARCH line alpha1 + beta1 = 1, the Gaussian fourth-moment boundary and the stricter Student-t7 boundary; Tsay 3.3, Petrobras normal and t fits sit just inside both, the Intel ARCH(1) fit on the beta1 = 0 axis](figures/L08-garch-persistence-kurtosis.png)
*Figure — left: (28) with $\sigma_h(1)=2\sigma_\infty$, so $\sigma_h^2(\ell)/\sigma_\infty^2=1+3\pi^{\ell-1}$, and (32) for the IGARCH fit; right: $\alpha_1+\beta_1=1$, the boundary of (25), and the $t_7$ boundary $1-2\alpha_1^2(\nu-1)/(\nu-4)-(\alpha_1+\beta_1)^2=0$ (T p. 166). Source: T Ex. 3.3 (pp. 136–141), garchmodeling.html.*

The term structure is (28) exactly: at $\ell=2$ the Tsay curve is $\sqrt{1+3(0.9727)}=1.98$, and it takes about 25 months to close half the gap in variance. All three empirical points sit **just inside** the Gaussian kurtosis boundary and close to the IGARCH line. That is the typical picture: high persistence, and a fourth moment that barely exists. Under $t_7$ innovations the admissible region shrinks, because the innovations bring their own kurtosis.

> **Interactive companion.** [The Volatility Dial](companions/companion-garch-volatility.html) — move $\alpha_1$, $\beta_1$, $\alpha_0$, the 1-step volatility $\sigma_h(1)$, the innovation tails ($\nu$ or Normal) and the horizon $L$. Watch the variance term structure close on $\sigma_\infty$, the **half-life** read-out, and the point in the $(\alpha_1,\beta_1)$ plane against the IGARCH line and the kurtosis boundaries. The defaults reproduce Tsay's Table 3.1.

### 4.4 · Worked — S&P 500 monthly excess returns 1926–1991, $T=792$ (T Ex. 3.3, pp. 134–139)

The PACF of $r_t^2$ shows strong dependence. An AR(3) mean with GARCH(1,1) gives insignificant AR terms, so the refined model is (T eq. 3.19)

$$r_t=0.0076+a_t,\qquad \sigma_t^2=0.000086+0.1216\,a_{t-1}^2+0.8511\,\sigma_{t-1}^2,\tag{30}$$

with standard errors 0.0015, 0.000024, 0.0197, 0.0190. Checks: $Q(12)=11.99$ ($p=0.45$) for $\tilde a_t$, $Q(12)=13.11$ ($p=0.36$) for $\tilde a_t^2$.

- **Persistence**: $\hat\alpha_1+\hat\beta_1=0.1216+0.8511=0.9727$. *Tsay prints "0.9772" on p. 137, a transposition of the last two digits.*
- **Unconditional variance** by (22): $0.000086/(1-0.9727)=0.000086/0.0273=0.003150$, sd $\sqrt{0.003150}=0.0561$. Tsay rounds to 0.00314, whose square root 0.0560 is the "$\infty$" entry of Table 3.1.
- **Half-life** by (29): $\ln0.5/\ln0.9727=(-0.69315)/(-0.02768)=25.04$ months.
- **Kurtosis** by (25): $2\alpha_1^2=2(0.1216)^2=0.02957$, $\pi^2=0.9727^2=0.94615$, denominator $1-0.02957-0.94615=0.02428$. So $K_a^{(g)}=6(0.014787)/0.02428=0.08872/0.02428=3.654$ and the kurtosis is 6.654. **Close to the boundary: a small change in $\alpha_1$ moves the denominator a lot.**
- **Forecasts** (Table 3.1, origin $h=792$, December 1991): volatility 0.0536, 0.0537, 0.0537, 0.0538, 0.0538 for $\ell=1,\dots,5$, and 0.0560 at $\infty$. Because $\sigma_h(1)$ starts **below** $\sigma_\infty$, (28) rises toward it, slowly ($\pi^4=0.895$).

**$t$ innovations.** With $\nu=5$ fixed (T eq. 3.20): $\sigma_t^2=0.00012+0.1121a_{t-1}^2+0.8432\sigma_{t-1}^2$, persistence $0.9553$ ("$\approx0.95$, close to 1", hence "essentially IGARCH" in Tsay's words). With $\nu$ estimated (T eq. 3.21): $\hat\nu=7.02$ (se 1.78), the same volatility equation, and $\nu=5$ is not rejected: $(7.02-5)/1.78=1.13$.

**Two caveats (T pp. 139–140).** (i) **Forecast evaluation**: $a_{h+1}^2$ is an unbiased but very noisy proxy of $\sigma_{h+1}^2$ (one draw of a random variable cannot estimate its variance), so a low $R^2$ of $a_{h+\ell}^2$ on $\sigma_h^2(\ell)$ is expected and does not condemn the model. (ii) **Two-pass estimation**: fit the mean, then fit (21) as an ARMA(1,1) to $\hat a_t^2$. Tsay's SCA fit $a_t^2=0.00014+0.9583a_{t-1}^2+\eta_t-0.8456\eta_{t-1}$ gives $\hat\beta_1=0.8456$ and $\hat\alpha_1=0.9583-0.8456=0.1127$, close to (30). It is an approximation with unexplored properties.

### 4.5 · Worked — Petrobras daily log returns, August 2000 – February 2021 (garchmodeling.html, $n=5167$)

No mean term (`include.mean=FALSE`), Gaussian $\varepsilon$.

| Model | $\hat\alpha_0$ ($\omega$) | $\hat\alpha_1$ | $\hat\beta_1$ | log-lik |
|---|---|---|---|---|
| ARCH(1) | 0.00070027 | 0.36979 | — | 10672.32 |
| GARCH(1,1) | 0.00002255 | 0.10317 | 0.87681 | 11151.72 |

- ARCH(1): unconditional sd by (8), $\sqrt{0.00070027/0.63021}=\sqrt{0.0011112}=0.0333$ (3.3% a day); kurtosis by (12), $3(1-0.13674)/(1-0.41023)=4.391$.
- GARCH(1,1): persistence $0.10317+0.87681=0.97997$. Unconditional variance $0.00002255/0.020027=0.0011259$, sd **0.03356**. Half-life $\ln0.5/\ln0.97997=(-0.69315)/(-0.020231)=$ **34.3 trading days**. Excess kurtosis by (25): $2\alpha_1^2=0.021287$, $\pi^2=0.960347$, denominator $0.018367$, so $6(0.010643)/0.018367=$ **3.48**.
- One extra parameter raises the log-likelihood by 479.4: LR $=2(11151.72-10672.32)=958.8$. ARCH(1) is nested at $\beta_1=0$, a boundary point, so $\chi^2_1$ is only a rough guide here; a statistic this large settles the question anyway.

**The 2025 update (garch-sv-petrobras.html, simple returns to November 2025, $n=6363$):** ARCH(1) $\hat\alpha_1=0.33114$ (uncond. sd $\sqrt{0.00066851/0.66886}=0.0316$); GARCH normal $(1.8817\times10^{-5},\,0.081406,\,0.89841)$, persistence 0.97982, sd 0.0305; GARCH-$t$ $(1.1404\times10^{-5},\,0.059208,\,0.92773)$, $\hat\nu=6.23$, persistence **0.98694**, sd 0.0295. The $t$ fit again has a smaller $\alpha_1$ and a larger $\beta_1$ than the Gaussian one.

---

## 5 · C — IGARCH and RiskMetrics (T §3.6, pp. 140–142)

If the AR polynomial of (21) has a unit root, $\alpha_1+\beta_1=1$, the model is **integrated** GARCH:

$$a_t=\sigma_t\varepsilon_t,\qquad \sigma_t^2=\alpha_0+\beta_1\sigma_{t-1}^2+(1-\beta_1)a_{t-1}^2,\qquad 0<\beta_1<1.\tag{31}$$

Tsay's S&P 500 IGARCH: $r_t=0.0067+a_t$, $\sigma_t^2=0.000119+0.8059\sigma_{t-1}^2+0.1941a_{t-1}^2$. The coefficients are close to (30), but **the unconditional variance (22) no longer exists** (denominator 0), which is hard to defend for an excess return. Tsay suggests occasional level shifts in volatility as a cause.

**Forecasts.** Put $\alpha_1+\beta_1=1$ in (27): $\sigma_h^2(\ell)=\alpha_0+\sigma_h^2(\ell-1)$. Iterating:

$$\sigma_h^2(\ell)=\sigma_h^2(1)+(\ell-1)\alpha_0,\qquad \ell\ge1,\tag{32}$$

(T eq. 3.22): a straight line with slope $\alpha_0$. **A shock to $\sigma_h^2(1)$ is permanent**, as a shock to a random walk is ([[L08-03-unit-roots-dickey-fuller]]). The variance process is a martingale; it can be strictly but not weakly stationary (Nelson, 1990).

**RiskMetrics** is (31) with $\alpha_0=0$: $\sigma_t^2=(1-\beta_1)a_{t-1}^2+\beta_1\sigma_{t-1}^2$. Substitute the same equation for $\sigma_{t-1}^2$:

$$\sigma_t^2=(1-\beta_1)a_{t-1}^2+\beta_1\big[(1-\beta_1)a_{t-2}^2+\beta_1\sigma_{t-2}^2\big]=(1-\beta_1)a_{t-1}^2+(1-\beta_1)\beta_1a_{t-2}^2+\beta_1^2\sigma_{t-2}^2,$$

and repeat:

$$\sigma_t^2=(1-\beta_1)\big(a_{t-1}^2+\beta_1a_{t-2}^2+\beta_1^2a_{t-3}^2+\cdots\big),\tag{33}$$

**exponential smoothing** of $a_t^2$ with discount factor $\beta_1$; the weights $(1-\beta_1)\beta_1^{j-1}$ sum to 1. By (32) with $\alpha_0=0$, every horizon's forecast equals $\sigma_h^2(1)$.

---

## 6 · C — ARCH in a regression (W §12.6, pp. 391–396)

Wooldridge's angle is the regression error. **Heteroskedasticity** in a time-series regression leaves OLS unbiased/consistent but invalidates the usual standard errors; heteroskedasticity-robust ones work as in cross-sections, provided there is **no serial correlation** (test for that first). The Breusch–Pagan regression (W eq. 12.46) $u_t^2=\delta_0+\delta_1x_{t1}+\dots+\delta_kx_{tk}+v_t$ needs homoskedastic, serially uncorrelated $v_t$.

**Worked — W Ex. 12.8, NYSE weekly returns, $n=689$.** The EMH regression $return_t=\beta_0+\beta_1return_{t-1}+u_t$ gives $t_{\beta_1}=1.55$: no predictability in the mean. Breusch–Pagan on $return_{t-1}$:

$$\hat u_t^2=4.66-1.104\,return_{t-1},\qquad (0.43)\ (0.201),\qquad R^2=0.042,$$

so $t=-1.104/0.201=-5.5$: **the variance depends on the past even though the mean does not**, and it is higher after low returns (the leverage pattern of §1).

**ARCH(1) for errors** (W eq. 12.49): $E(u_t^2\mid u_{t-1},\dots)=a_0+a_1u_{t-1}^2$, which is the conditional variance only if $E(u_t\mid u_{t-1},\dots)=0$. Written as

$$u_t^2=a_0+a_1u_{t-1}^2+v_t,\qquad E(v_t\mid u_{t-1},\dots)=0\tag{34}$$

(W eq. 12.50), it is an AR(1) in $u_t^2$, stable for $a_1<1$ — equation (13) with $m=1$. Under ARCH errors with otherwise Gauss–Markov assumptions, **OLS is still BLUE and the usual statistics are asymptotically valid**. ARCH still matters for two reasons: weighted least squares or maximum likelihood based on (34) gives asymptotically **more efficient** estimators, and volatility itself is the object of interest in finance.

---

## Links

- Neighbours: [[L08-05-seasonal-airline-model]] · [[L08-07-garch-family-asymmetry-tails]] (asymmetry, EGARCH, GARCH-M, non-Gaussian errors, Tiao's kurtosis formula).
- Unit: [[L08-00-map]] · [[L08-02-forecasting-ma-arma]] (the ARMA mean and forecast recursion used in (21)–(28)) · [[L08-03-unit-roots-dickey-fuller]] (the unit root behind IGARCH) · [[L08-08-stochastic-volatility]] (the alternative with its own shock) · [[L08-09-bayesian-garch]] (the same GARCH(1,1)-$t$ by MCMC) · [[L08-10-formulas]] · [[L08-11-pitfalls]] · [[L08-12-python]] (GARCH MLE with `scipy.optimize`).
- Class 1: [[../L01/L01-07-ar-var-review|L01-07]] §2 (squared-return Ljung–Box), §6 (half-life).
- Rules: [[../../rules/05_espaco_estados_volatilidade|rules/05]] (ARCH/GARCH).
- **Practice (number and printed page only):** T 3.3 and 3.4 (p. 168); T 3.6 (p. 169); T 3.11 and 3.12 (p. 170); W 12.4 (p. 397). Solutions: `Listas/lista-L08-book-exercises.pdf`.
