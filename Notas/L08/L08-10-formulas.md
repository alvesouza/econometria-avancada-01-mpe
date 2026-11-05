---
tags: [notes, lecture-08, formulas, reference, arma, unit-root, long-memory, seasonal, arch, garch, stochastic-volatility, bayesian-garch]
date: 2026-10-25
status: taught
source: "The nine section notes L08-01 … L08-09 (equation numbers are theirs); Class 8 goals in Map/class-plan.md; the site's Class 8 description in Aula/COURSE.md; every number re-checked by Notas/L08/L08_python_checks.py"
---

# Class 8 · Formulas — the exam specification, every result, every number

> Prev: [[L08-09-bayesian-garch]] · Next: [[L08-11-pitfalls]] · Map: [[L08-00-map]]

Equations are cited by the **section note's own numbering**: "L08-06 (25)" is equation (25) of
[[L08-06-arch-garch]]. Every number in §2 is asserted in [[L08-12-python]] (script
`L08_python_checks.py`) or in `figures/make_figures.py`.

---

## 0 · The exam specification, mapped

### 0.1 · The site's description of Class 8 (`Aula/COURSE.md`)

"Introduction to univariate time series econometrics", in five items:

| # | Site item (verbatim) | Where it is settled |
|---|---|---|
| i | "Autoregressive moving average models" | [[L08-01-ar2-arp-cycles-identification]] (AR(2), AR(p), cycles, PACF, AIC/BIC); [[L08-02-forecasting-ma-arma]] (forecasts, MA, ARMA, identification) |
| ii | "Unit root econometrics" | [[L08-03-unit-roots-dickey-fuller]] (random walk, drift, trend-stationarity, ARIMA, DF/ADF, spurious regression); [[L08-04-long-memory-arfima]] (fractional integration) |
| iii | "Seasonal models" | [[L08-05-seasonal-airline-model]] |
| iv | "ARCH/GARCH and related models" | [[L08-06-arch-garch]] (ARCH, GARCH, IGARCH); [[L08-07-garch-family-asymmetry-tails]] (GJR, TGARCH, APARCH, EGARCH, GARCH-M, non-Gaussian errors); [[L08-09-bayesian-garch]] (Bayesian GARCH) |
| v | "Stochastic volatility models" | [[L08-08-stochastic-volatility]] |

### 0.2 · The goals in `Map/class-plan.md`, item by item

| Goal | Note and section |
|---|---|
| AR, MA and ARMA: identification | L08-01 §8 (PACF), §9 (AIC/BIC); L08-02 §5 (MA ACF), §8 (identification table) |
| … estimation | L08-01 §10 (conditional LS); L08-02 §6 (conditional vs exact likelihood); L01-07 §5 (AR(1) OLS = MLE) |
| … $h$-step forecasts | L08-02 §2–§3, §7, §9 |
| business cycles from complex AR roots | L08-01 §4–§6 |
| random walk, drift, unit-root tests | L08-03 §1–§7 |
| long memory | L08-04 |
| seasonal (airline) models | L08-05 §3–§6 |
| ARCH/GARCH and variants | L08-06; L08-07 |
| stochastic volatility (Gaussian and Student-$t$) | L08-08 §2–§8 |
| GARCH(1,1) vs SV-AR(1) | L08-08 §4.2, §9; figure `L08-news-impact-sv-memory` (right panel) |
| Bayesian GARCH | L08-09 |

**Final exam** (30%, no code; `Map/class-plan.md`): derivations of AR/MA/ARMA moments, forecast
means and variances, ARCH/GARCH moments and forecasts, conjugate updates, and the reading of
printed `arima`/`garchFit`/`adf.test`/`bayesGARCH` output.

---

## 1 · Every definition and result

### 1.1 · AR(2), AR(p), PACF, criteria → [[L08-01-ar2-arp-cycles-identification]]

| Result | Statement | Where |
|---|---|---|
| AR(2) mean | $\mu=\phi_0/(1-\phi_1-\phi_2)$, if $\phi_1+\phi_2\neq1$ | (2) |
| Moment equations / Yule–Walker | $\gamma_\ell=\phi_1\gamma_{\ell-1}+\phi_2\gamma_{\ell-2}$, $\rho_\ell=\phi_1\rho_{\ell-1}+\phi_2\rho_{\ell-2}$ ($\ell>0$) (T 2.13) | (4), (6) |
| First autocorrelations | $\rho_1=\phi_1/(1-\phi_2)$; $\rho_2=\phi_1^2/(1-\phi_2)+\phi_2$ | (7), (8) |
| Variance | $\gamma_0=\dfrac{(1-\phi_2)\sigma^2}{(1+\phi_2)[(1-\phi_2)^2-\phi_1^2]}$ | (9) |
| Characteristic equation | $1-\phi_1x-\phi_2x^2=0$; stationary iff both solutions have $\lvert x\rvert>1$ (T 2.14) | (10)–(11) |
| Triangle | $\phi_2<1-\phi_1$, $\phi_2<1+\phi_1$, $\phi_2>-1$ | (15)–(18) |
| Complex roots, cycle | complex iff $\phi_1^2+4\phi_2<0$; $k=2\pi/\cos^{-1}[\phi_1/(2\sqrt{-\phi_2})]$ | (13)–(14) |
| AR(p) | stationary iff all solutions of $1-\phi_1x-\dots-\phi_px^p=0$ exceed 1 in modulus | (21)–(22) |
| PACF | $\hat\phi_{\ell,\ell}$ from the AR($\ell$) regression; for AR(p): $\hat\phi_{p,p}\to\phi_p$, $\hat\phi_{\ell,\ell}\to0$ and $V\approx1/T$ for $\ell>p$ | (23), §8 |
| AIC, BIC | AIC $=-\frac2T\ln L+\frac2T\,k$; Gaussian AR($\ell$): $\ln\tilde\sigma_\ell^2+2\ell/T$ and $\ln\tilde\sigma_\ell^2+\ell\ln T/T$ (T 2.16) | (24)–(25) |

### 1.2 · Forecasts, MA, ARMA → [[L08-02-forecasting-ma-arma]]

| Result | Statement | Where |
|---|---|---|
| Optimal forecast | $\hat r_h(\ell)=E(r_{h+\ell}\mid F_h)$ minimises the conditional MSE | (1)–(2) |
| AR recursion | $\hat r_h(\ell)=\phi_0+\sum\phi_i\hat r_h(\ell-i)$, $\hat r_h(j)=r_{h+j}$ for $j\le0$; $e_h(2)=a_{h+2}+\phi_1a_{h+1}$ | (3)–(6) |
| AR(2) forecasts | $E(y_{n+2})=(\phi_1^2+\phi_2)y_n+\phi_1\phi_2y_{n-1}$; $V_2=(1+\phi_1^2)\sigma^2$; $V_3=[1+\phi_1^2+(\phi_1^2+\phi_2)^2]\sigma^2$ | (7)–(10) |
| MA(q) | $r_t=c_0+a_t-\sum\theta_ia_{t-i}$ (Tsay's sign); $E=c_0$, $V=(1+\sum\theta_i^2)\sigma^2$; always stationary | (15)–(16) |
| MA ACF | MA(1): $\rho_1=-\theta_1/(1+\theta_1^2)$, $\lvert\rho_1\rvert\le\frac12$; MA(2): $\rho_1=\frac{-\theta_1+\theta_1\theta_2}{1+\theta_1^2+\theta_2^2}$, $\rho_2=\frac{-\theta_2}{1+\theta_1^2+\theta_2^2}$; zero beyond $q$ | (17)–(18) |
| Invertibility | MA(1) invertible iff $\lvert\theta_1\rvert<1$ ($\theta$ and $1/\theta$ give the same ACF) | (19) |
| MA forecasts | MA(1): $\hat r_h(1)=c_0-\theta_1a_h$, $\hat r_h(\ell)=c_0$ for $\ell\ge2$ | (20) |
| ARMA(1,1) | $\gamma_0=\frac{1-2\phi_1\theta_1+\theta_1^2}{1-\phi_1^2}\sigma^2$; $\rho_1=\frac{(\phi_1-\theta_1)(1-\phi_1\theta_1)}{1-2\phi_1\theta_1+\theta_1^2}$; $\rho_\ell=\phi_1\rho_{\ell-1}$, $\ell\ge2$ | (21)–(25) |
| Forecast-error variance | $V[e_h(\ell)]=(1+\psi_1^2+\dots+\psi_{\ell-1}^2)\sigma^2\to\gamma_0$ (T 2.34) | (26)–(28) |
| Identification | AR(p): PACF cuts off at $p$; MA(q): ACF cuts off at $q$; ARMA: neither (EACF) | §8 |

### 1.3 · Unit roots → [[L08-03-unit-roots-dickey-fuller]]

| Result | Statement | Where |
|---|---|---|
| Random walk | $\hat p_h(\ell)=p_h$; $e_h(\ell)=\sum_{j=1}^\ell a_{h+j}$; $V=\ell\sigma^2$; $\psi_i=1$ | (1)–(6) |
| RW with drift | $p_t=p_0+\mu t+\sum a_i$: mean $p_0+\mu t$, sd $\sigma\sqrt t$; crossover $t^*=(\sigma/\mu)^2$ | (7)–(10) |
| Trend-stationary | $p_t=\beta_0+\beta_1t+r_t$: mean $\beta_0+\beta_1t$, variance $V(r_t)$ constant | (11) |
| Constant term | MA: the mean; stationary AR/ARMA: $\phi_0=\mu(1-\sum\phi_i)$; RW with drift: the slope | §3 |
| ARIMA(p,1,q) | $(1-B)y_t$ is a stationary invertible ARMA(p,q) | (12)–(13) |
| DF | $p_t=\phi_1p_{t-1}+e_t$ (or with $\phi_0$); $H_0:\phi_1=1$ vs $<1$; $t=\sum p_{t-1}e_t/(\hat\sigma_e\sqrt{\sum p_{t-1}^2})$, non-normal law | (14)–(21) |
| ADF | $\Delta x_t=c_t+\beta x_{t-1}+\sum\tilde\phi_i\Delta x_{t-i}+e_t$; AR(3): $\beta=\phi_1+\phi_2+\phi_3-1$, $\tilde\phi_1=-(\phi_2+\phi_3)$, $\tilde\phi_2=-\phi_3$; unit root iff $\sum\phi_i=1$ | (22)–(29) |
| Critical values (W Tables 18.2–18.3) | no trend: −3.43, −3.12, −2.86, −2.57 (1, 2.5, 5, 10%); trend: −3.96, −3.66, −3.41, −3.12 | §5.5 |
| Spurious regression | regressing one independent RW on another: residual is a RW, $t$ diverges, $R^2$ random | (30) |

### 1.4 · Long memory → [[L08-04-long-memory-arfima]]

| Result | Statement | Where |
|---|---|---|
| Fractional difference | $(1-B)^dx_t=a_t$, $-\frac12<d<\frac12$; $(1-B)^d=1-dB-\frac{d(1-d)}2B^2-\dots$ | (1)–(3) |
| Representations | $\psi_k=\frac{(k+d-1)!}{k!(d-1)!}$ (stationary if $d<\frac12$); $\pi_k=\frac{(k-d-1)!}{k!(-d-1)!}$ (invertible if $d>-\frac12$) | (4)–(6) |
| ACF | $\rho_k=\prod_{j=1}^k\frac{j-1+d}{j-d}$; $\rho_1=\frac d{1-d}$; $\rho_k\sim\frac{(-d)!}{(d-1)!}k^{2d-1}$ | (7)–(11) |
| PACF, spectrum | $\phi_{k,k}=d/(k-d)$; $f(\omega)\sim\omega^{-2d}$ as $\omega\to0$ | §4 |

### 1.5 · Seasonal models → [[L08-05-seasonal-airline-model]]

| Result | Statement | Where |
|---|---|---|
| Seasonal difference | $\Delta_sx_t=(1-B^s)x_t$; $\Delta_s\Delta x_t=x_t-x_{t-1}-x_{t-s}+x_{t-s-1}$ | (1)–(3) |
| Airline model | $(1-B^s)(1-B)x_t=(1-\theta B)(1-\Theta B^s)a_t$ (T 2.41) | (4)–(5) |
| Its autocovariances | $\gamma_0=(1+\theta^2)(1+\Theta^2)\sigma^2$, $\gamma_1=-\theta(1+\Theta^2)\sigma^2$, $\gamma_s=-\Theta(1+\theta^2)\sigma^2$, $\gamma_{s\pm1}=\theta\Theta\sigma^2$ | (6)–(10) |
| ACF | $\rho_1=-\theta/(1+\theta^2)$, $\rho_s=-\Theta/(1+\Theta^2)$, $\rho_{s\pm1}=\rho_1\rho_s$, all others 0 | (11)–(12) |
| Non-multiplicative | $w_t=(1-\theta B-\Theta B^s)a_t$: $\rho_{s+1}=0$ | (13)–(14) |
| SARIMA | $\phi_P(B^s)\phi(B)\Delta_s^D\Delta^dx_t=\theta_0+\theta_Q(B^s)\theta(B)a_t$; ARIMA(1,1,1)×(1,1,1)$_{12}$ = constrained ARMA(26,13) | (15)–(18) |
| Deterministic seasonality | $\Theta=1$: seasonal dummies (W §10.5e) | (19) |

### 1.6 · ARCH and GARCH → [[L08-06-arch-garch]]

| Result | Statement | Where |
|---|---|---|
| Structure | $r_t=\mu_t+a_t$, $\sigma_t^2=V(a_t\mid F_{t-1})$ | (1)–(3) |
| ARCH test | Engle LM: regress $a_t^2$ on $m$ lags, $F$; McLeod–Li: $Q(m)$ on $a_t^2$ | (4)–(5) |
| ARCH(m) | $a_t=\sigma_t\varepsilon_t$, $\sigma_t^2=\alpha_0+\sum\alpha_ia_{t-i}^2$ (T 3.5) | (6) |
| ARCH(1) moments | $E a_t=0$; $V=\alpha_0/(1-\alpha_1)$; $m_4=\frac{3\alpha_0^2(1+\alpha_1)}{(1-\alpha_1)(1-3\alpha_1^2)}$; kurtosis $3\frac{1-\alpha_1^2}{1-3\alpha_1^2}>3$, needs $\alpha_1^2<\frac13$ | (7)–(12) |
| Likelihoods | Gaussian $-\frac12\sum[\ln\sigma_t^2+a_t^2/\sigma_t^2]$; standardized $t$ density (T 3.7) and (3.8) | (14)–(17) |
| GARCH(m,s) | $\sigma_t^2=\alpha_0+\sum\alpha_ia_{t-i}^2+\sum\beta_j\sigma_{t-j}^2$; ARMA form for $a_t^2$ with $\eta_t=a_t^2-\sigma_t^2$ (T 3.15) | (20)–(21) |
| Unconditional variance | $\sigma_\infty^2=\alpha_0/[1-\sum(\alpha_i+\beta_i)]$ | (22) |
| GARCH(1,1) kurtosis | $K_a^{(g)}=\dfrac{6\alpha_1^2}{1-2\alpha_1^2-(\alpha_1+\beta_1)^2}$ (Gaussian ε) | (24)–(25) |
| Forecasts | $\sigma_h^2(\ell)=\alpha_0+(\alpha_1+\beta_1)\sigma_h^2(\ell-1)$; $=\sigma_\infty^2+(\alpha_1+\beta_1)^{\ell-1}[\sigma_h^2(1)-\sigma_\infty^2]$ (T 3.17) | (26)–(28) |
| Half-life | $\ln0.5/\ln(\alpha_1+\beta_1)$ | (29) |
| IGARCH | $\alpha_1+\beta_1=1$: $\sigma_h^2(\ell)=\sigma_h^2(1)+(\ell-1)\alpha_0$ (T 3.22); $\alpha_0=0$: RiskMetrics exponential smoothing | (31)–(33) |
| ARCH in a regression | $u_t^2=\alpha_0+\alpha_1u_{t-1}^2+v_t$ (W 12.50): OLS still consistent, WLS/ML more efficient | (34) |

### 1.7 · Asymmetry and tails → [[L08-07-garch-family-asymmetry-tails]]

| Result | Statement | Where |
|---|---|---|
| News impact | $\sigma_t^2$ as a function of $a_{t-1}$ at $\sigma_{t-1}=\sigma_\infty$ | (1) |
| GJR/TGARCH | $\sigma_t^2=\alpha_0+(\alpha_1+\gamma_1N_{t-1})a_{t-1}^2+\beta_1\sigma_{t-1}^2$, $N=1\{a<0\}$ (T 3.34) | (2) |
| APARCH | $\sigma_t^\delta=\omega+\alpha(\lvert a_{t-1}\rvert-\gamma a_{t-1})^\delta+\beta\sigma_{t-1}^\delta$; what `fGarch` `leverage=TRUE` fits | (4)–(5) |
| δ = 2 mapping | good news $\alpha(1-\gamma)^2$, bad news $\alpha(1+\gamma)^2$, indicator coefficient $4\alpha\gamma$; $\sigma_\infty^2=\omega/[1-\alpha(1+\gamma^2)-\beta]$ | (6)–(7) |
| EGARCH | $g(\varepsilon)=\theta\varepsilon+\gamma[\lvert\varepsilon\rvert-E\lvert\varepsilon\rvert]$, $E\lvert\varepsilon\rvert=\sqrt{2/\pi}$ (normal); $\ln\sigma_t^2$ ARMA in $g$ (T 3.24–3.25); bad/good ratio $e^{-2\alpha c}$ in rugarch's form | (8)–(14) |
| GARCH-M | $r_t=\mu+c\sigma_t^2+a_t$ (T 3.23) | (15) |
| Tiao's kurtosis | $K_a=\dfrac{K+K_a^{(g)}+\frac56KK_a^{(g)}}{1-\frac16KK_a^{(g)}}$; $t_\nu$: $K=\frac6{\nu-4}$, $K_a=\frac{6+(\nu+1)K_a^{(g)}}{\nu-4-K_a^{(g)}}$ | (16)–(17) |

### 1.8 · Stochastic volatility → [[L08-08-stochastic-volatility]]

| Result | Statement | Where |
|---|---|---|
| SV-AR(1) | $a_t=\sigma_t\varepsilon_t$, $\ln\sigma_t^2=\alpha_0+\alpha_1\ln\sigma_{t-1}^2+v_t$ (T 3.40); `stochvol`: $y_t=e^{h_t/2}\varepsilon_t$, $h_{t+1}=\mu+\phi(h_t-\mu)+\sigma u_t$ | (1)–(2) |
| Log-variance law | $N(\mu_h,\sigma_h^2)$, $\mu_h=\alpha_0/(1-\alpha_1)$, $\sigma_h^2=\sigma_v^2/(1-\alpha_1^2)$ | (3)–(4) |
| Moments | $E a^2=e^{\mu_h+\sigma_h^2/2}$; $E a^4=3e^{2\mu_h+2\sigma_h^2}$; kurtosis $3e^{\sigma_h^2}$ | (5)–(7) |
| ACF of $a^2$ | $\dfrac{e^{\sigma_h^2\alpha_1^i}-1}{3e^{\sigma_h^2}-1}$ | (8)–(9) |
| Likelihood | $f(R\mid\theta)=\int f(R\mid H)f(H\mid\theta)\,dH$, $n$-dimensional | (10) |
| Linearisation | $\ln a_t^2=\ln\sigma_t^2+\ln\varepsilon_t^2$, $E\ln\varepsilon^2=-1.2704$, $V=\pi^2/2$ | (11) |
| Gibbs | $\beta\mid H$ weighted regression; $h_t\mid h_{t\pm1}$ (T 12.23) with $\mu_t=\frac{\alpha_0(1-\alpha_1)+\alpha_1(\ln h_{t+1}+\ln h_{t-1})}{1+\alpha_1^2}$, variance $\frac{\sigma_v^2}{1+\alpha_1^2}$; $\alpha\mid H$ AR regression; $\sigma_v^2\mid H$ inverted $\chi^2$ | (12)–(21) |

### 1.9 · Bayesian GARCH → [[L08-09-bayesian-garch]]

| Result | Statement | Where |
|---|---|---|
| M0 update | $\sigma^2\sim IG(a,b)$, $r_i\sim N(0,\sigma^2)$ ⇒ $IG(a+n/2,\ b+\sum r_i^2/2)$; posterior mean = weighted average with prior weight $(a-1)/(a-1+n/2)$ | (1)–(5) |
| M1 Gibbs | $\mu\mid\sigma^2$ normal, precision-weighted; $\sigma^2\mid\mu$ inverse gamma | (6)–(8) |
| M2 | Bayesian regression of $y_t$ on $y_{t-1}$: normal and inverse-gamma conditionals | (9)–(11) |
| M3 | $r_t\sim t_\nu(0,\varrho h_t)$, $\varrho=(\nu-2)/\nu$ so $V(r_t\mid h_t)=h_t$; truncated-normal priors on $(\alpha,\beta)$, $p(\nu)=\lambda e^{-\lambda(\nu-\delta)}1\{\nu>\delta\}$ | (12)–(15) |
| Scale mixture | $r_t\mid\varpi_t\sim N(0,\varpi_t\varrho h_t)$, $\varpi_t\sim IG(\nu/2,\nu/2)$ | (16) |
| Stationarity, Bayesian | $\Pr(\alpha_1+\beta>1\mid\text{data})$ read off the draws | (17) |

---

## 2 · Every number and worked case

### 2.1 · AR(2) and AR(p) (L08-01)

| Case | Numbers |
|---|---|
| $\phi=(1.75,-0.80)$ | complex (disc −0.1375), solution modulus 1.118, $k=30.09$; $\rho_1=0.9722$, $\rho_2=0.9014$, min $\rho_{15}=-0.1866$; $\gamma_0=50.704\sigma^2$, sd 7.1207 |
| $\phi=(0.90,0.05)$ | real solutions 1.0499 and −19.05; $\rho_1=0.9474$; $\gamma_0=9.7812$, sd 3.1275 |
| GNP AR(3) (T 2.15) | $(1+0.521B)(1-0.869B+0.274B^2)$; disc −0.341; $k=10.62$ quarters (R's roots: 10.656); $\phi_0=0.6150\times0.0077=0.0047355$ |
| Tsay Fig. 2.4(b) $(0.6,-0.4)$ | disc −1.24, $k=5.84$; PACF 0.4286, −0.4, then 0 |
| PACF SE | $1/\sqrt{996}=0.0317$; GNP band $\pm2/\sqrt{176}=\pm0.151$ |
| Table 2.1 | AIC → AR(9) (−5.849); BIC → AR(1) (−5.833), AR(3) −5.831 |

### 2.2 · Forecasts, MA, ARMA (L08-02)

| Case | Numbers |
|---|---|
| ar2-forecast ($y_n=-5.487150$, $y_{n-1}=-3.508837$) | $E$: −6.7954, −7.5023, −7.6927, −7.4603; $V$: 1, 4.0625, 9.1814, 15.7318; $\psi$: 1, 1.75, 2.2625, 2.5594; sd(50) 7.1206 → 7.12069; 90% limits ±11.71 |
| MA(1) | $\theta=0.6$: $\rho_1=-0.4412$; $\theta=0.5$ and $2$: $-0.4$; bound $\frac12$ at $\lvert\theta\rvert=1$ |
| ARMA(1,1) $(0.8,0.4)$ | $\gamma_0=1.4444$, $\rho_1=0.5231$, $\rho_2=0.4185$; $\psi$: 1, 0.4, 0.32, 0.256 |

### 2.3 · Unit roots (L08-03)

| Case | Numbers |
|---|---|
| 3M drift | $\mu=0.0103$ (se 0.002318), $t=4.44$, $\sigma=0.0637$, crossover 38.2 months |
| DF MC ($T=250$, seed 2026) | quantiles −3.45, −3.16, −2.87, −2.58; −1.645 rejects a true unit root 46.5% of the time |
| W examples | T-bill $t=-2.46$ ($\hat\rho=0.909$, not rejected); inflation $-3.01$ (rejected at 5%); GDP with trend $-2.41$ (not rejected) |
| US GDP ADF | Tsay −1.701 (p 0.4297), $\hat\rho=0.9992$; R/slides −1.61 (0.45); site page `tseries` −0.370 (0.987) |
| S&P 500 ADF | −1.998 (p 0.602); site page $k=2$: −2.018 (0.571); differences −37.5 (p ≤ 0.01) |
| Spurious regression | 66.2% ($n=50$), 84.7% ($n=250$) false rejections |

### 2.4 · Long memory (L08-04)

| $d$ | Numbers |
|---|---|
| 0.25 | $\rho_1,\rho_2,\rho_3=0.3333, 0.2381, 0.1948$; $\phi_{22}=0.1429$ |
| 0.4 | $\rho_1=2/3$; $\rho_{100}=0.2673$ vs AR(1) $(2/3)^{100}\approx2.5\times10^{-18}$; log–log slope $2d-1=-0.2$ |

### 2.5 · Seasonal (L08-05)

| Case | Numbers |
|---|---|
| J&J airline $(0.678,0.314)$, $s=4$ | $\hat\sigma=0.089$, $Q(12)=10.0$ (p 0.44); $\rho_1=-0.4645$, $\rho_4=-0.2858$, $\rho_{3}=\rho_5=0.1328$ |
| Decile 1 | exact: seasonal AR 0.951, MA 0.997 (cancel); January dummy 0.1253 (se 0.0115), intercept 0.0029, $R^2=0.2016$ |
| AirPassengers airline | $n=96$: (−0.3941, −0.6129), BIC −284.27; $n=108$: (−0.3864, −0.5885), BIC −336.93 (best of 16); $n=144$: (−0.4018, −0.5569), AIC −483.4; ACF $\rho_1=-0.3362$, $\rho_{12}=-0.4371$, $\rho_{11}=\rho_{13}=0.1470$ |
| Out of sample 1958–60 | RMSE airline 36.6 vs trend + 11 dummies 63.3 (our computation) |

### 2.6 · ARCH/GARCH (L08-06)

| Case | Numbers |
|---|---|
| Intel ARCH tests | $Q(12)=18.26$ (p 0.11) on $r$; 89.85 on $a^2$; LM 53.62 |
| Intel ARCH(1) (3.12) | $\alpha_0=0.0111$, $\alpha_1=0.356$; uncond. sd 0.1313 (Tsay prints 0.1315); kurtosis 4.227 |
| Tsay Ex. 3.3 (3.19) | (0.000086, 0.1216, 0.8511); persistence **0.9727** (Tsay prints 0.9772); $\sigma_\infty^2=0.003150$, sd 0.0561; half-life 25.04 months; kurtosis 6.654; Table 3.1 0.0536 … 0.0560 |
| IGARCH (Tsay) | (0.000119, 0.1941, 0.8059): forecasts rise by 0.000119 per step |
| Two-pass | $\hat\alpha_1=0.9583-0.8456=0.1127$ |
| Petrobras 2000–2021 | ARCH(1) sd 0.0333; GARCH (2.255e−5, 0.10317, 0.87681): persistence 0.97997, sd 0.03356, half-life 34.3 days, excess kurtosis 3.48; LR 958.8 |
| Petrobras 2000–2025 | GARCH normal persistence 0.97982; GARCH-$t$ 0.98694, $\nu=6.23$ |

### 2.7 · Asymmetry and tails (L08-07)

| Case | Numbers |
|---|---|
| PBR GJR (APARCH δ = 2) | good 0.05787, bad 0.13483, indicator 0.07696; persistence 0.97813 (literal reading 1.078) |
| PBR T-GARCH (δ = 1) | bad 0.12976, good 0.06306 (ratio 2.06) |
| PBR EGARCH | $\alpha=-0.05549$, $\gamma=0.18138$, $\beta=0.97741$; bad/good ratio 1.117 at $c=1$, 1.249 at $c=2$ |
| $E\lvert\varepsilon\rvert$ | $\sqrt{2/\pi}=0.7979$; standardized $t_{7.04}$: 0.7595 |
| PBR GARCH-$t$ kurtosis | $K_a^{(g)}=1.563$, $K=1.972$, total excess 12.55 |
| GARCH-M (Tsay) | $c=1.09$ (se 0.818), $t=1.33$ |
| AIC ladder | GARCH −22297.4 … skew-$t$ best (−22585.7) |

### 2.8 · Stochastic volatility (L08-08)

| Case | Numbers |
|---|---|
| Tsay Ex. 12.3 | posterior (0.409, 0.454, 0.837, 0.086); $\mu_h=2.785$, $\sigma_h^2=0.2872$, $E a^2=18.71$ %², sd 4.33%, kurtosis 3.998, lag-1 corr 0.0906 |
| PBR SV-$t$ | $\mu=-0.419$, $\phi=0.9842$, $\sigma=0.1388$, $\nu=12.13$; $\sigma_h^2=0.6146$; kurtosis (Gaussian ε) 5.547; corr$(a_t^2,a_{t-1}^2)$ 0.1828 vs GARCH 0.2037 |
| S&P 500 iid | Gaussian $\hat\sigma=0.012729$; $t$: scale 0.005922, $\hat\nu=2$ |

### 2.9 · Bayesian GARCH (L08-09)

| Case | Numbers |
|---|---|
| M0 prior | IG(5, 4 × 0.0006617694): mean 0.0006617694, sd 0.000382; prior weight with $n=1760$: $4/884=0.45\%$ |
| M1, M2 priors | sd($\mu$) 0.006627; sd($\alpha$) 0.01849, sd($\beta$) 0.00993 |
| M3 | $\Pr(\alpha_1+\beta>1\mid\text{data})=0.0034$; prior $E\nu=\delta+1/\lambda=102$ |
| Bayes vs ML (PBR standardized) | persistence 0.97905 vs 0.98370; half-life 32.7 vs 42.2 days |

---

## Links

- Unit: [[L08-00-map]] · [[L08-11-pitfalls]] · [[L08-12-python]]
- Class 1 review: [[../L01/L01-07-ar-var-review|L01-07]] (AR(1), random walk, VAR(1))
- Rules: [[../../rules/04_arima_raiz_unitaria|rules/04]] · [[../../rules/05_espaco_estados_volatilidade|rules/05]]
