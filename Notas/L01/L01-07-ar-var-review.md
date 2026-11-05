---
tags: [notes, lecture-01, time-series, stationarity, acf, ljung-box, ar1, unit-root, equilibrium-distribution, var]
date: 2026-10-19
status: taught
source: "ar-ma.pdf pp. 1–17 (stationarity, ACF, Ljung–Box with the IBM example, white noise, linear time series, AR(1) moments and ACF); ar-var-R.txt (AR fits, VAR(1), IRF on Canada data); T §2.1–2.4 (pp. 30–57: eqs. 2.8–2.11 pp. 37–39, AR(1) ACF p. 40, conditional least squares pp. 49–50, half-life p. 56), §8.2 (pp. 399–403: eq. 8.8, Example 8.3 p. 400, §8.2.2 pp. 401–403); W §11.1 (eqs. 11.2–11.4, p. 347), §11.3 (eqs. 11.20–11.22, pp. 354–355)"
---

# AR(1), unit root and VAR(1) · the regression with a lagged response, and the distribution it settles into

> **Claim.** **An AR(1) is a linear regression of $y_t$ on $y_{t-1}$**, and with Gaussian shocks OLS on it is the conditional MLE. Its behaviour hangs on one number: **for $|\phi|<1$ the process forgets its start at rate $\phi^t$ and settles into the equilibrium (stationary) distribution $N\big(\mu,\ \sigma^2/(1-\phi^2)\big)$; at $\phi=1$ (a unit root) the variance grows like $t\sigma^2$ and there is no equilibrium at all.** The AR(p) is the same regression with $p$ lags. **The VAR(1) is its matrix version**: stationary when all eigenvalues of $\Phi$ lie inside the unit circle, with mean $(I-\Phi)^{-1}\phi_0$ and covariance solving $\Gamma_0=\Phi\Gamma_0\Phi'+\Sigma$, i.e. $\mathrm{vec}(\Gamma_0)=(I-\Phi\otimes\Phi)^{-1}\mathrm{vec}(\Sigma)$.
> Prev: [[L01-06-gaussian-linear-regression]] · Next: [[L01-08-p-hacking-evidence]] · Map: [[L01-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $r_t$ or $y_t$ | the series at time $t$ (Tsay writes $r_t$ for returns; Wooldridge $y_t$) | |
| $a_t$ | shock (innovation), white noise with variance $\sigma_a^2$ (written $\sigma^2$ where no confusion) | |
| $\mu$ | $E(r_t)$ under stationarity | |
| $\gamma_\ell=\mathrm{Cov}(r_t,r_{t-\ell})$ | lag-$\ell$ autocovariance; $\gamma_0=V(r_t)$ | |
| $\rho_\ell=\gamma_\ell/\gamma_0$ | lag-$\ell$ autocorrelation (ACF) | $[-1,1]$ |
| $\phi_0,\phi_1$ | AR(1) intercept and slope (persistence) | |
| $\psi_i$ | weights of the linear (MA($\infty$)) representation, $\psi_0=1$ | |
| $T$ | sample length | |
| $m$ | number of lags in the portmanteau test | |
| $k$ | dimension of the vector series (§9) | |
| $\phi_0,\Phi,\Sigma$ | VAR(1) intercept ($k\times1$), coefficient matrix ($k\times k$), shock covariance ($k\times k$) | |
| $\Gamma_\ell$ | lag-$\ell$ cross-covariance matrix of $r_t$ | |
| $\mathrm{vec}(A)$, $\otimes$ | columns of $A$ stacked; Kronecker product | |

---

## 1 · C — stationarity (deck pp. 5–7; T §2.1, p. 30)

**Strict stationarity:** the joint distribution of $(r_{t_1},\dots,r_{t_k})$ equals that of $(r_{t_1+t},\dots,r_{t_k+t})$ for every shift $t$, every $k$ and every choice of times — "a very strong condition that is hard to verify empirically."

**Weak stationarity:** (a) $E(r_t)=\mu$, constant; (b) $\mathrm{Cov}(r_t,r_{t-\ell})=\gamma_\ell$, depending only on the lag $\ell$. In a time plot: **the values fluctuate with constant variation around a fixed level.** It is what makes past data informative about the future.

Two properties of $\gamma_\ell$ (deck p. 7): $\gamma_0=V(r_t)$, and $\gamma_{-\ell}=\gamma_\ell$, because with $t_1=t+\ell$

$$\gamma_{-\ell}=\mathrm{Cov}(r_t,r_{t+\ell})=\mathrm{Cov}(r_{t+\ell},r_t)=\mathrm{Cov}(r_{t_1},r_{t_1-\ell})=\gamma_\ell.\tag{1}$$

---

## 2 · C — the ACF and the Ljung–Box test (deck pp. 8–11; T §2.2, pp. 30–36)

Under weak stationarity $V(r_t)=V(r_{t-\ell})=\gamma_0$, so

$$\rho_\ell=\frac{\mathrm{Cov}(r_t,r_{t-\ell})}{\sqrt{V(r_t)V(r_{t-\ell})}}=\frac{\gamma_\ell}{\gamma_0},\qquad \hat\rho_\ell=\frac{\sum_{t=\ell+1}^T(r_t-\bar r)(r_{t-\ell}-\bar r)}{\sum_{t=1}^T(r_t-\bar r)^2}.\tag{2}$$

**Portmanteau tests** of $H_0:\rho_1=\dots=\rho_m=0$ against "some $\rho_i\ne0$": Box–Pierce $Q^*(m)=T\sum_{\ell=1}^m\hat\rho_\ell^2$ and its finite-sample improvement, Ljung–Box,

$$Q(m)=T(T+2)\sum_{\ell=1}^m\frac{\hat\rho_\ell^2}{T-\ell}\ \overset{a}{\sim}\ \chi^2_m\ \text{under } H_0;\tag{3}$$

reject when $Q(m)$ exceeds the $1-\alpha$ quantile of $\chi^2_m$.

**Worked — IBM monthly simple returns (deck p. 11).** `Box.test(sibm, lag=30, type="Ljung")` gives $Q(30)=38.241$; with 30 df, $P(\chi^2_{30}>38.241)=0.1437$ (reproduced in Python): **no evidence of linear autocorrelation in returns.** The same test on squared returns gives $Q(30)=182.12$, $p<2.2\times10^{-16}$ ($\approx10^{-23}$): **returns are serially uncorrelated but not independent** — their size is predictable. That is volatility clustering, the subject of ARCH/GARCH and stochastic volatility in Class 8.

---

## 3 · C — white noise and linear time series (deck pp. 12–14; T §2.3, pp. 36–37)

**White noise:** iid with finite mean and variance; all ACFs zero. Gaussian white noise: $N(0,\sigma^2)$.

**Linear time series:** $r_t=\mu+\sum_{i=0}^\infty\psi_ia_{t-i}$, $\psi_0=1$, $\{a_t\}$ white noise. By independence of the $a$'s, $E(r_t)=\mu$ and $V(r_t)=\sigma_a^2\sum_i\psi_i^2$. The autocovariance (deck p. 14):

$$\gamma_\ell=E\Big[\Big(\sum_{i=0}^\infty\psi_ia_{t-i}\Big)\Big(\sum_{j=0}^\infty\psi_ja_{t-\ell-j}\Big)\Big]=\sum_{i,j}\psi_i\psi_jE(a_{t-i}a_{t-\ell-j})$$

Only terms with $t-i=t-\ell-j$, i.e. $i=j+\ell$, survive, each contributing $\sigma_a^2$:

$$\gamma_\ell=\sigma_a^2\sum_{j=0}^\infty\psi_j\psi_{j+\ell},\qquad \rho_\ell=\frac{\sum_{i\ge0}\psi_i\psi_{i+\ell}}{1+\sum_{i\ge1}\psi_i^2}.\tag{4}$$

> **Every model in this note is a recipe for the $\psi$ weights.**

---

## 4 · C — AR(1): mean, variance, ACF (deck pp. 15–17; T eqs. 2.8–2.11, pp. 37–40)

$$r_t=\phi_0+\phi_1r_{t-1}+a_t\tag{5}$$

"in the same form as the well-known simple linear regression model" (T, p. 37), with $E(r_t\mid r_{t-1})=\phi_0+\phi_1r_{t-1}$ and $V(r_t\mid r_{t-1})=\sigma_a^2$.

**Mean.** Take expectations of (5), $E(a_t)=0$: $E(r_t)=\phi_0+\phi_1E(r_{t-1})$. Under stationarity $E(r_t)=E(r_{t-1})=\mu$:

$$\mu=\phi_0+\phi_1\mu\iff\mu=\frac{\phi_0}{1-\phi_1}\quad(\phi_1\ne1).\tag{6}$$

Substituting $\phi_0=(1-\phi_1)\mu$ from (6) into (5):

$$r_t-\mu=\phi_1(r_{t-1}-\mu)+a_t.\tag{7}$$

**MA($\infty$) form.** Substitute (7) into itself repeatedly:

$$r_t-\mu=a_t+\phi_1\big(\phi_1(r_{t-2}-\mu)+a_{t-1}\big)=a_t+\phi_1a_{t-1}+\phi_1^2(r_{t-2}-\mu)=\dots=\sum_{i=0}^\infty\phi_1^ia_{t-i},\tag{8}$$

the linear form of §3 with $\psi_i=\phi_1^i$ (T eq. 2.11). So $r_{t-1}$ depends only on $a_{t-1},a_{t-2},\dots$, and $\mathrm{Cov}(r_{t-1},a_t)=0$.

**Variance.** Square (7) and take expectations; the cross term vanishes because $\mathrm{Cov}(r_{t-1},a_t)=0$:

$$V(r_t)=\phi_1^2V(r_{t-1})+\sigma_a^2.$$

Under stationarity $V(r_t)=V(r_{t-1})=\gamma_0$:

$$\gamma_0=\phi_1^2\gamma_0+\sigma_a^2\iff\gamma_0=\frac{\sigma_a^2}{1-\phi_1^2},\tag{9}$$

**which is a positive finite number only if $\phi_1^2<1$**: weak stationarity implies $|\phi_1|<1$; conversely $|\phi_1|<1$ makes (8) converge with finite, time-invariant moments. **Necessary and sufficient: $|\phi_1|<1$** (T, p. 39; W (11.3), p. 347).

**ACF.** Multiply (7) by $(r_{t-\ell}-\mu)$, $\ell\ge1$, and take expectations; $a_t$ is uncorrelated with the past:

$$\gamma_\ell=\phi_1E[(r_{t-1}-\mu)(r_{t-\ell}-\mu)]+E[a_t(r_{t-\ell}-\mu)]=\phi_1\gamma_{\ell-1}+0.\tag{10}$$

Iterating (10) down to $\gamma_0$: $\gamma_\ell=\phi_1^\ell\gamma_0$, so

$$\boxed{\;\rho_\ell=\phi_1^{\,\ell},\quad \ell=0,1,2,\dots\;}\tag{11}$$

**exponential decay at rate $\phi_1$** (alternating in sign when $\phi_1<0$; T Figure 2.3, p. 40). (The deck's p. 16 writes the $\ell=0$ case as $\gamma_0=\phi_1\gamma_1+\sigma_a^2$; with $\gamma_1=\phi_1\gamma_0$ this is (9) again.) **Wooldridge's number (W (11.4), p. 347):** with $\phi_1=0.9$, $\mathrm{Corr}(y_t,y_{t+5})=0.9^5=0.59049\approx.591$ — high persistence, yet the correlation fades.

---

## 5 · C — estimation: OLS is the conditional MLE (T pp. 49–50)

Assume Gaussian shocks. By (5), $r_t\mid r_{t-1}\sim N(\phi_0+\phi_1r_{t-1},\sigma_a^2)$, and by the Markov property the joint density factors as

$$p(r_1,\dots,r_T)=p(r_1)\prod_{t=2}^Tp(r_t\mid r_{t-1}).\tag{12}$$

**Conditioning on $r_1$** drops the first factor. The conditional log-likelihood is

$$\ell_c(\phi_0,\phi_1,\sigma_a^2)=-\frac{T-1}{2}\log(2\pi\sigma_a^2)-\frac{1}{2\sigma_a^2}\sum_{t=2}^T(r_t-\phi_0-\phi_1r_{t-1})^2,\tag{13}$$

which is (15) of [[L01-06-gaussian-linear-regression]] with $y=(r_2,\dots,r_T)'$ and $X$ having rows $(1,r_{t-1})$. By the argument there, **$(\hat\phi_0,\hat\phi_1)$ is the OLS regression of $r_t$ on $r_{t-1}$** — Tsay's "conditional least-squares method" — and "if the conditional-likelihood method is used, the estimates of $\phi_i$ remain unchanged" (T, p. 50); only the divisor of $\hat\sigma_a^2$ changes.

**The exact likelihood** keeps $p(r_1)$, which under stationarity is the equilibrium law of §6, $N\big(\mu,\sigma_a^2/(1-\phi_1^2)\big)$. That factor depends on $\phi_1$, so the exact MLE differs slightly from OLS — negligibly for large $T$ — and it **imposes $|\phi_1|<1$**, while OLS can return any value.

---

## 6 · C — the equilibrium (stationary) distribution

Start the Gaussian AR(1) at a fixed $y_0$ and iterate (7) $t$ times, stopping instead of going to infinity as in (8):

$$y_t-\mu=\phi^t(y_0-\mu)+\sum_{j=0}^{t-1}\phi^ja_{t-j}.\tag{14}$$

A fixed number plus a sum of independent normals is normal, with

$$E(y_t\mid y_0)=\mu+\phi^t(y_0-\mu),\qquad V(y_t\mid y_0)=\sigma^2\sum_{j=0}^{t-1}\phi^{2j}=\sigma^2\,\frac{1-\phi^{2t}}{1-\phi^2}\tag{15}$$

(geometric sum, $\phi^2\ne1$). Let $t\to\infty$ with $|\phi|<1$: $\phi^t\to0$ and $\phi^{2t}\to0$, so

$$\boxed{\;y_t\mid y_0\ \xrightarrow{d}\ N\Big(\mu,\ \frac{\sigma^2}{1-\phi^2}\Big)\quad\text{whatever } y_0\;}\tag{16}$$

**The start is forgotten geometrically.** (16) is also the only *invariant* normal law: if $y_{t-1}\sim N(\mu,v)$ then by (7) $y_t\sim N(\mu,\phi^2v+\sigma^2)$, which equals $N(\mu,v)$ exactly when $v=\phi^2v+\sigma^2$, i.e. $v=\sigma^2/(1-\phi^2)$ — (9) again.

**Half-life** (T, p. 56): the horizon $h$ at which the expected deviation from $\mu$ has halved, $\phi^h=\tfrac12$:

$$h=\frac{\ln0.5}{\ln|\phi|}.\tag{17}$$

**Worked, $\phi=0.9$, $\sigma=1$, $\mu=0$, $y_0=8$.** Equilibrium variance $1/(1-0.81)=1/0.19=5.263$ (sd 2.294). Half-life $\ln0.5/\ln0.9=-0.6931/-0.1054=6.58$ periods. At $t=10$, from (15): mean $0.9^{10}\times8=0.3487\times8=2.79$; variance $(1-0.9^{20})/0.19=(1-0.1216)/0.19=4.62$. For $\phi=0.5$ the half-life is exactly 1 and the equilibrium variance $1/0.75=1.333$.

![Left: densities of y_t given y_0 = 8 for phi = 0.9 at t = 1, 3, 10, 30, moving left and widening toward the equilibrium N(0, 5.26). Right: conditional variance against horizon for phi = 0.5 and 0.9, levelling off at 1.33 and 5.26, while for phi = 1 it grows linearly as t](figures/L01-ar1-equilibrium.png)
*Figure — exact laws (15)–(16): left, $y_t\mid y_0=8$ for $\phi=0.9$, $\sigma=1$; right, $V(y_t\mid y_0)/\sigma^2$ for $\phi=0.5, 0.9$ (dashed: limits $1/(1-\phi^2)$) and $t$ for $\phi=1$ (W (11.21)).*

On the left the density slides from near $y_0=8$ toward zero and spreads; by $t=30$ it is indistinguishable from the equilibrium curve ($0.9^{30}\times8=0.34$). On the right, the stationary variances level off — fast for $\phi=0.5$, after a few half-lives for $\phi=0.9$ — **while the unit-root line never does.**

---

## 7 · C — the unit root, $\phi=1$ (W §11.3, pp. 354–355)

With $\phi_1=1$ and $\phi_0=0$, (5) is the **random walk** $y_t=y_{t-1}+e_t$ (W (11.20)). Repeated substitution with $y_0$ fixed:

$$y_t=y_0+e_1+e_2+\dots+e_t,\qquad E(y_t)=y_0,\qquad V(y_t)=t\,\sigma_e^2\tag{18}$$

(W (11.21), p. 354): **the variance grows linearly in $t$, so the process cannot be stationary**, and (16) has no limit — $1-\phi^2=0$ in the denominator. Forecasts never revert:

$$E(y_{t+h}\mid y_t)=y_t\ \text{for all } h\ge1\quad(\text{W (11.22), p. 355}),\qquad\text{vs}\quad E(y_{t+h}\mid y_t)=\phi^hy_t\to0\ \text{when }|\phi|<1.\tag{19}$$

**Persistence does not fade either:** $\mathrm{Corr}(y_t,y_{t+h})=\sqrt{t/(t+h)}$ (W, p. 355), which depends on $t$ (not stationary) and, for $h=100$, exceeds 0.95 once $t>1000$: $\sqrt{1000/1100}=0.9535$.

![Three stacked panels driven by the same seeded Gaussian shocks over 200 periods: phi = 0.5 stays inside a band of plus or minus 2.31; phi = 0.9 wanders more widely inside plus or minus 4.59; phi = 1 drifts away and the plus or minus 2 sqrt(t) band widens to about 28](figures/L01-ar1-paths.png)
*Figure — one seeded simulation of 200 standard normal shocks fed through (5) with $\phi=0.5,0.9,1$ and $y_0=0$; shaded: $\pm2$ equilibrium sd from (9), or $\pm2\sqrt t$ from (18) for the random walk.*

Same shocks, three behaviours: at $\phi=0.5$ the path crosses zero constantly; at $\phi=0.9$ it makes long excursions but keeps returning (the half-life of 6.6 periods is visible as runs of that length); at $\phi=1$ every shock is permanent and the path drifts to about −15 with nothing pulling it back.

**Why it matters for estimation (named; Class 8).** At $\phi=1$, $\hat\phi$ from §5 is still consistent (faster, at rate $T$), but its $t$-statistic for $H_0:\phi=1$ no longer has a $N(0,1)$ limit — the Dickey–Fuller distribution — and regressing one random walk on another produces spurious significance (W §11.3 for the persistence, §18.2–18.3 for the tests and spurious regressions; `rules/04`).

---

## 8 · C — AR(p) as a regression (T eq. 2.9, pp. 49–50)

$$r_t=\phi_0+\phi_1r_{t-1}+\dots+\phi_pr_{t-p}+a_t,\qquad t=p+1,\dots,T\tag{20}$$

"is in the form of a multiple linear regression and can be estimated by the least-squares method" (T, p. 49): $y=(r_{p+1},\dots,r_T)'$, rows of $X$ equal to $(1,r_{t-1},\dots,r_{t-p})$, and $\hat\beta=(X'X)^{-1}X'y$ from [[L01-06-gaussian-linear-regression]] (7). There are $T-p$ observations and $p+1$ parameters, hence Tsay's $\hat\sigma_a^2=\sum\hat a_t^2/(T-2p-1)$ — the divisor $n-q$ of that note's (19).

**Stationary mean.** Taking expectations as in (6):

$$\mu=\frac{\phi_0}{1-\phi_1-\dots-\phi_p}.\tag{21}$$

**Worked — Tsay's AR(3) for monthly value-weighted index returns (T, p. 50):** $r_t=0.0091+0.116r_{t-1}-0.019r_{t-2}-0.104r_{t-3}+\hat a_t$, $\hat\sigma_a=0.054$. By (21):

$$\mu=\frac{0.0091}{1-0.116-(-0.019)-(-0.104)}=\frac{0.0091}{1.007}=0.00904,$$

about 0.9% a month: with these small coefficients the implied mean barely differs from the intercept. AR(2) moments and forecasts are T Exercise 2.2 (p. 104).

---

## 9 · C — VAR(1) in matrix form (T §8.2, pp. 399–403)

$$r_t=\phi_0+\Phi r_{t-1}+a_t,\qquad a_t\ \text{serially uncorrelated},\ E(a_t)=0,\ \mathrm{Cov}(a_t)=\Sigma\tag{22}$$

(T eq. 8.8). For $k=2$:

$$r_{1t}=\phi_{10}+\Phi_{11}r_{1,t-1}+\Phi_{12}r_{2,t-1}+a_{1t},\qquad r_{2t}=\phi_{20}+\Phi_{21}r_{1,t-1}+\Phi_{22}r_{2,t-1}+a_{2t}.$$

$\Phi_{12}$ is the effect of $r_{2,t-1}$ on $r_{1t}$ given $r_{1,t-1}$. $\Phi_{12}=0,\Phi_{21}\ne0$: one-way dependence from $r_1$ to $r_2$; both zero: uncoupled; both nonzero: **feedback**. Contemporaneous links live only in $\Sigma_{12}$ — the **reduced form**; a Cholesky factor of $\Sigma$ turns it into a recursive structural form (T §8.2.1; structural VARs and impulse responses are Class 9). **Each equation is an OLS regression on the same lagged regressors**, so equation-by-equation OLS estimates $\Phi$.

**Stationarity** (T, p. 402). Repeated substitution as in (8) gives $\tilde r_t=r_t-\mu=a_t+\Phi a_{t-1}+\Phi^2a_{t-2}+\dots$; the weights $\Phi^j$ must vanish, which happens **iff all eigenvalues of $\Phi$ are less than 1 in modulus** — the matrix version of $|\phi_1|<1$.

**Mean.** Expectations of (22) under stationarity:

$$\mu=\phi_0+\Phi\mu\iff(I-\Phi)\mu=\phi_0\iff\mu=(I-\Phi)^{-1}\phi_0.\tag{23}$$

**Covariance.** With $\tilde r_t=\Phi\tilde r_{t-1}+a_t$ and $\mathrm{Cov}(\tilde r_{t-1},a_t)=0$:

$$\Gamma_0=E(\tilde r_t\tilde r_t')=\Phi E(\tilde r_{t-1}\tilde r_{t-1}')\Phi'+E(a_ta_t')=\Phi\Gamma_0\Phi'+\Sigma.\tag{24}$$

Apply $\mathrm{vec}$ and the identity $\mathrm{vec}(ABC)=(C'\otimes A)\,\mathrm{vec}(B)$ with $A=\Phi$, $B=\Gamma_0$, $C=\Phi'$:

$$\mathrm{vec}(\Gamma_0)=(\Phi\otimes\Phi)\,\mathrm{vec}(\Gamma_0)+\mathrm{vec}(\Sigma)$$

$$\boxed{\;\mathrm{vec}(\Gamma_0)=(I_{k^2}-\Phi\otimes\Phi)^{-1}\mathrm{vec}(\Sigma)\;}\tag{25}$$

($I-\Phi\otimes\Phi$ is invertible because the eigenvalues of $\Phi\otimes\Phi$ are the products $\lambda_i\lambda_j$, all of modulus below 1.) Post-multiplying $\tilde r_t=\Phi\tilde r_{t-1}+a_t$ by $\tilde r_{t-\ell}'$ and taking expectations gives T (8.12):

$$\Gamma_\ell=\Phi\Gamma_{\ell-1}\ \Longrightarrow\ \Gamma_\ell=\Phi^\ell\Gamma_0,\quad\ell>0.\tag{26}$$

For $k=1$, (23), (25) and (26) collapse to (6), (9) and (10).

### 9.1 · Worked — T Example 8.3 (p. 400)

$$\phi_0=\begin{pmatrix}0.2\\0.4\end{pmatrix},\qquad\Phi=\begin{pmatrix}0.2&0.3\\-0.6&1.1\end{pmatrix},\qquad\Sigma=\begin{pmatrix}2&1\\1&1\end{pmatrix}.$$

**Stationary?** $\mathrm{tr}\,\Phi=1.3$, $\det\Phi=0.2(1.1)-0.3(-0.6)=0.22+0.18=0.40$; the eigenvalues solve $\lambda^2-1.3\lambda+0.40=0$:

$$\lambda=\frac{1.3\pm\sqrt{1.69-1.60}}{2}=\frac{1.3\pm0.3}{2}\in\{0.8,\ 0.5\}$$

both inside the unit circle — **stationary, although $\Phi_{22}=1.1>1$**: a single coefficient above one does not make a VAR explosive.

**Mean, by (23).** $I-\Phi=\begin{pmatrix}0.8&-0.3\\0.6&-0.1\end{pmatrix}$, $\det=0.8(-0.1)-(-0.3)(0.6)=-0.08+0.18=0.10$, so

$$(I-\Phi)^{-1}=\frac{1}{0.10}\begin{pmatrix}-0.1&0.3\\-0.6&0.8\end{pmatrix}=\begin{pmatrix}-1&3\\-6&8\end{pmatrix},\qquad\mu=\begin{pmatrix}-1(0.2)+3(0.4)\\-6(0.2)+8(0.4)\end{pmatrix}=\begin{pmatrix}1.0\\2.0\end{pmatrix}.$$

**Covariance, by (25).** $\Phi\otimes\Phi$ has blocks $\Phi_{ij}\Phi$; for instance the top-left block is $0.2\Phi=\begin{pmatrix}0.04&0.06\\-0.12&0.22\end{pmatrix}$. Then

$$I_4-\Phi\otimes\Phi=\begin{pmatrix}0.96&-0.06&-0.06&-0.09\\0.12&0.78&0.18&-0.33\\0.12&0.18&0.78&-0.33\\-0.36&0.66&0.66&-0.21\end{pmatrix},\qquad\mathrm{vec}(\Sigma)=\begin{pmatrix}2\\1\\1\\1\end{pmatrix},$$

and solving gives $\mathrm{vec}(\Gamma_0)=(25/9,\ 20/9,\ 20/9,\ 40/9)'$:

$$\Gamma_0=\begin{pmatrix}25/9&20/9\\20/9&40/9\end{pmatrix}=\begin{pmatrix}2.778&2.222\\2.222&4.444\end{pmatrix}.$$

**Check one entry of (24).** First, $\Gamma_0\binom{0.2}{0.3}=\binom{0.2(25/9)+0.3(20/9)}{0.2(20/9)+0.3(40/9)}=\binom{11/9}{16/9}$; then $(\Phi\Gamma_0\Phi')_{11}=(0.2,0.3)\binom{11/9}{16/9}=\frac{2.2+4.8}{9}=\frac79$; and $\frac79+\Sigma_{11}=\frac79+\frac{18}9=\frac{25}9\ \checkmark$.

**Lag 1, by (26):** $\Gamma_1=\Phi\Gamma_0=\begin{pmatrix}11/9&16/9\\7/9&32/9\end{pmatrix}$. The contemporaneous correlation is $\frac{20/9}{\sqrt{(25/9)(40/9)}}=\frac{20}{\sqrt{1000}}=0.632$. *(All entries computed exactly and by `numpy.linalg.solve` for this note.)*

---

## 10 · U — the site's R script (`ar-var-R.txt`)

Taken from Penn State's STAT510: AR(1) and AR(2) fits by `sarima` to three LA pollution–mortality series (`cmort`, `tempr`, `part` from `astsa`), a VAR(1) with constant and trend on the three jointly (`VAR(x, p=1, type="both")`), and a VAR(1) on the `vars` package's Canada data (productivity, employment, real wage, unemployment) with 52-step impulse responses and their bands. The file prints no output, so no numbers are taken from it. Python equivalents: `statsmodels.tsa.ar_model.AutoReg` (OLS = §5), `statsmodels.tsa.api.VAR` with `.irf(52)`; see [[L01-11-python]]. **The impulse responses and their identification belong to Class 9.**

---

## Links

- Neighbours: [[L01-06-gaussian-linear-regression]] (the regression machinery used in §5, §8, §9) · [[L01-08-p-hacking-evidence]].
- Unit: [[L01-00-map]] · [[L01-09-formulas]] · [[L01-10-pitfalls]] · [[L01-11-python]] · [[L01-02-poisson-mle-properties]] (conditional vs full likelihood, again).
- Class 2: [[../L02/L02-01-prediction-error-bias-variance|L02 §1]] (forecasting as prediction).
- Rules: [[../../rules/04_arima_raiz_unitaria|rules/04]] (ARIMA, unit roots — Class 8) · [[../../rules/05_espaco_estados_volatilidade|rules/05]] (VAR, IRF — Class 9).
- **Practice (number and printed page only):** T 2.2 (p. 104); W 11.C8 (p. 370); W 12.1 (p. 396); T 8.1 and T 8.2 (p. 462).
