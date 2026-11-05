---
tags: [notes, lecture-08, time-series, volatility, stochastic-volatility, sv, mcmc, gibbs, student-t, leverage]
date: 2026-10-25
status: taught
source: "sp500-gaussian-student-SV-models.html (S&P 500, May 2017–May 2022: iid Gaussian vs iid Student-t vs SV/SVt/SVl/SVtl, stochvol default priors); GARCH11-SVar1.html §5–5.2 (Petrobras standardized returns, SV-AR(1) with t errors vs GARCH(1,1)-t); garch-sv-petrobras.html §5 (svsample on simple returns); T §3.12 eq. (3.40) and the Jacquier–Polson–Rossi moments (pp. 153–154), §3.13 eq. (3.41) (p. 154); T §12.7.1 eqs. (12.20)–(12.27) and Example 12.3 (pp. 636–643)"
---

# Stochastic volatility · a second shock for the variance, its moments, and why it needs MCMC

> **Claim.** **A stochastic-volatility (SV) model gives the log variance its own AR(1) shock**, $\ln\sigma_t^2=\alpha_0+\alpha_1\ln\sigma_{t-1}^2+v_t$, instead of GARCH's exact function of past squared returns. **With Gaussian shocks every moment is a lognormal moment**: $E(a_t^2)=e^{\mu_h+\sigma_h^2/2}$, kurtosis $3e^{\sigma_h^2}>3$, and $\mathrm{corr}(a_t^2,a_{t-i}^2)=(e^{\sigma_h^2\alpha_1^i}-1)/(3e^{\sigma_h^2}-1)$, which decays at rate $\alpha_1$, like GARCH's at rate $\alpha_1+\beta_1$. **The price is the likelihood**: $\sigma_t$ is not known given the past, so $f(R\mid\theta)$ is an $n$-dimensional integral over the volatility path. **Bayesian MCMC treats the path as unknowns** and samples it one $h_t$ at a time from (12.23), a density built from three factors. On Petrobras, SV and GARCH share the same persistence (0.984); SV needs thinner-tailed errors ($\nu\approx12$ against 7) because its own volatility shock already supplies kurtosis.
> Prev: [[L08-07-garch-family-asymmetry-tails]] · Next: [[L08-09-bayesian-garch]] · Map: [[L08-00-map]]

**Notation.** Two sources, two meanings of $h_t$. **Tsay §12.7 writes $h_t$ for the variance $\sigma_t^2$; the site pages and the R package `stochvol` write $h_t$ for the log variance $\ln\sigma_t^2$.** This note keeps both, and says which at every use.

| Symbol | Meaning | Range |
|---|---|---|
| $r_t$, $a_t$ | return and its shock (mean removed); Tsay's notation | |
| $y_t$ | the site's (demeaned) return | |
| $\varepsilon_t$ | standardized return shock, iid $N(0,1)$ (or $t_\nu$ in SVt) | |
| $\sigma_t^2$ | conditional variance of $a_t$ given the volatility | $>0$ |
| $\alpha_0,\alpha_1,\sigma_v^2$ | Tsay's log-variance AR(1): intercept, persistence, shock variance | $\lvert\alpha_1\rvert<1$ |
| $v_t$ | log-variance shock, iid $N(0,\sigma_v^2)$, independent of $\varepsilon_t$ | |
| $\mu_h,\sigma_h^2$ | stationary mean and variance of $\ln\sigma_t^2$ | |
| $h_t$ (stochvol) | $\ln\sigma_t^2$; $\mu,\phi,\sigma$ its level, persistence and shock sd | $\lvert\phi\rvert<1$, $\sigma>0$ |
| $h_t$ (Tsay §12.7) | $\sigma_t^2$ itself | |
| $\rho$ | $\mathrm{corr}(\varepsilon_t,u_t)$, the leverage parameter | $(-1,1)$ |
| $\nu$ | Student-$t$ degrees of freedom | $>2$ |
| $H=(h_1,\dots,h_n)'$ | the volatility path, treated as unknowns | |
| $\theta$ | the static parameters | |

---

## 1 · U — what SV adds to GARCH

Tsay sorts volatility models into two families (T §3.2, p. 113). In the first, "an exact function" governs $\sigma_t^2$. That is GARCH: given $F_{t-1}$, $\sigma_t^2=\alpha_0+\alpha_1a_{t-1}^2+\beta_1\sigma_{t-1}^2$ is a known number. In the second, "a stochastic equation" describes it. That is SV, where $\sigma_t^2$ has a shock of its own, unknown even after seeing every past return.

| | GARCH(1,1) | SV-AR(1) |
|---|---|---|
| volatility driven by | past observations: **observation-driven** | its own shock $v_t$: **parameter-driven** |
| shocks per observation | one ($\varepsilon_t$) | two ($\varepsilon_t$, $v_t$) |
| $\sigma_t^2$ given $F_{t-1}$ | known | random |
| positivity | needs $\alpha_0>0$, $\alpha_1,\beta_1\ge0$ | automatic (logs) |
| likelihood | product of one-step densities, exact | $n$-dimensional integral (§5) |
| estimation | MLE (L08-06) | quasi-likelihood via the Kalman filter, or MCMC (§6) |

"Adding the innovation $v_t$ substantially increases the flexibility of the model in describing the evolution of $\sigma_t^2$, but it also increases the difficulty in parameter estimation" (T, p. 153).

---

## 2 · C — the model, in Tsay's form and in `stochvol`'s form (T §3.12, p. 153; site pages)

**Tsay (3.40)** with $m=1$:

$$a_t=\sigma_t\varepsilon_t,\qquad(1-\alpha_1B)\ln\sigma_t^2=\alpha_0+v_t,\tag{1}$$

that is, $\ln\sigma_t^2=\alpha_0+\alpha_1\ln\sigma_{t-1}^2+v_t$, with $\varepsilon_t$ iid $N(0,1)$, $v_t$ iid $N(0,\sigma_v^2)$, the two independent, and $\lvert\alpha_1\rvert<1$. The log keeps $\sigma_t^2>0$ with no constraint on the coefficients, as in EGARCH (L08-07).

**The site and `stochvol`** (sp500-gaussian-student-SV-models.html §5):

$$y_t=e^{h_t/2}\varepsilon_t,\qquad h_{t+1}=\mu+\phi(h_t-\mu)+\sigma u_t,\qquad\mathrm{corr}(\varepsilon_t,u_t)=\rho.\tag{2}$$

Here $h_t=\ln\sigma_t^2$, since $e^{h_t/2}=\sigma_t$. Matching (1) to (2): $\phi=\alpha_1$, $\sigma^2=\sigma_v^2$, and $\alpha_0=(1-\phi)\mu$, so $\mu$ is the *mean* of the log variance (the "intercept versus mean" distinction of L01-07 (6)–(7)).

**The four models of `stochvol`**, as the page lists them:

| Model | $\varepsilon_t$ | $u_t$ | $\rho$ | $\nu$ |
|---|---|---|---|---|
| SV | $N(0,1)$ | $N(0,1)$ | 0 | — |
| SVt | $t_\nu(0,1)$ | $N(0,1)$ | 0 | unknown |
| SVl (leverage) | $N(0,1)$ | $N(0,1)$ | unknown | — |
| SVtl | $t_\nu(0,1)$ | $N(0,1)$ | unknown | unknown |

*Erratum.* The page's SVtl line reads "$\varepsilon_t\sim N(0,1)$", the SVl specification copied. The $t$ in SVtl, and the unknown $\nu$ in the same line, mean $\varepsilon_t\sim t_\nu$.

**Leverage.** With $\rho<0$, a negative return shock $\varepsilon_t$ comes with a positive $u_t$ on average, so $h_{t+1}$ rises after bad news. This is SV's version of the asymmetry that GJR and EGARCH build into the variance equation (L08-07). The timing matters: $u_t$ moves $h_{t+1}$, the *next* variance, so the correlation is not a contemporaneous link between the return and its own variance.

---

## 3 · C — the stationary law of the log variance (T p. 154)

$\ln\sigma_t^2$ in (1) is a Gaussian AR(1). By L01-07 (16), for $\lvert\alpha_1\rvert<1$ it settles into

$$\ln\sigma_t^2\sim N\Big(\frac{\alpha_0}{1-\alpha_1},\ \frac{\sigma_v^2}{1-\alpha_1^2}\Big)\equiv N(\mu_h,\sigma_h^2).\tag{3}$$

In `stochvol`'s notation (2), $\mu_h=\mu$ and $\sigma_h^2=\sigma^2/(1-\phi^2)$. Its autocovariance at lag $i$ is, by L01-07 (11),

$$\mathrm{Cov}(\ln\sigma_t^2,\ln\sigma_{t-i}^2)=\alpha_1^i\sigma_h^2.\tag{4}$$

This is also the law `stochvol` uses to start the chain: $h_1\sim N(\mu,\sigma^2/(1-\phi^2))$ (§8).

---

## 4 · C — moments of $a_t$: kurtosis and the ACF of $a_t^2$ (T p. 154, derived)

The one tool is the **lognormal moment**. If $X\sim N(m,s^2)$ then $E(e^{kX})=e^{km+k^2s^2/2}$ (the normal moment-generating function at $k$).

**Second moment.** $\varepsilon_t$ is independent of $\sigma_t$ and $E(\varepsilon_t^2)=1$:

$$E(a_t^2)=E(\sigma_t^2)E(\varepsilon_t^2)=E\big(e^{\ln\sigma_t^2}\big)$$

Apply the lognormal moment with $k=1$, $m=\mu_h$, $s^2=\sigma_h^2$ from (3):

$$E(a_t^2)=\exp\big(\mu_h+\sigma_h^2/2\big).\tag{5}$$

**Fourth moment.** $E(\varepsilon_t^4)=3$ for a standard normal:

$$E(a_t^4)=E(\sigma_t^4)E(\varepsilon_t^4)=3E\big(e^{2\ln\sigma_t^2}\big)$$

Apply the lognormal moment with $k=2$:

$$E(a_t^4)=3\exp\big(2\mu_h+2\sigma_h^2\big).\tag{6}$$

*Erratum, T p. 154.* The book prints "$E(a_t^4)=3\exp(2\mu_h^2+2\sigma_h^2)$". The square on $\mu_h$ is a typo: by (6) the exponent is linear in $\mu_h$, and only the linear version makes the kurtosis below free of $\mu_h$, as a ratio of scale-free moments must be.

**Kurtosis.** Divide (6) by the square of (5):

$$\frac{E(a_t^4)}{[E(a_t^2)]^2}=\frac{3\exp(2\mu_h+2\sigma_h^2)}{\exp(2\mu_h+\sigma_h^2)}=3e^{\sigma_h^2}>3.\tag{7}$$

> **SV has fat tails even with Gaussian $\varepsilon_t$.** A normal with a random variance is a scale mixture of normals, and every such mixture has kurtosis above 3. The excess is $3(e^{\sigma_h^2}-1)$: it grows with the variability of the log variance, not with its level.

With Student-$t$ shocks of kurtosis $\kappa_\varepsilon=E(\varepsilon_t^4)$, the same steps give kurtosis $\kappa_\varepsilon e^{\sigma_h^2}$. For a standardized $t_\nu$, $\kappa_\varepsilon=3(\nu-2)/(\nu-4)$, $\nu>4$ (from T §3.16, p. 166: excess $6/(\nu-4)$).

**Autocorrelation of $a_t^2$.** For $i\ge1$, $\varepsilon_t$ and $\varepsilon_{t-i}$ are independent of each other and of the volatility path:

$$E(a_t^2a_{t-i}^2)=E(\sigma_t^2\sigma_{t-i}^2)E(\varepsilon_t^2)E(\varepsilon_{t-i}^2)=E\big(e^{\ln\sigma_t^2+\ln\sigma_{t-i}^2}\big).$$

The sum of the two logs is normal with mean $2\mu_h$ and, by (3)–(4), variance $\sigma_h^2+\sigma_h^2+2\alpha_1^i\sigma_h^2$:

$$E(a_t^2a_{t-i}^2)=\exp\big(2\mu_h+\sigma_h^2(1+\alpha_1^i)\big).\tag{8}$$

Subtract the product of means, $[E(a_t^2)]^2=\exp(2\mu_h+\sigma_h^2)$ from (5):

$$\mathrm{Cov}(a_t^2,a_{t-i}^2)=\exp(2\mu_h+\sigma_h^2)\big(e^{\sigma_h^2\alpha_1^i}-1\big).$$

The variance is (6) minus the same product:

$$\mathrm{Var}(a_t^2)=3\exp(2\mu_h+2\sigma_h^2)-\exp(2\mu_h+\sigma_h^2)=\exp(2\mu_h+\sigma_h^2)\big(3e^{\sigma_h^2}-1\big).$$

The ratio cancels $\exp(2\mu_h+\sigma_h^2)$:

$$\boxed{\;\mathrm{corr}(a_t^2,a_{t-i}^2)=\frac{e^{\sigma_h^2\alpha_1^i}-1}{3e^{\sigma_h^2}-1}\;}\tag{9}$$

which is T's formula on p. 154. For small $\sigma_h^2\alpha_1^i$, $e^{x}-1\approx x$, so (9) $\approx\sigma_h^2\alpha_1^i/(3e^{\sigma_h^2}-1)$: **geometric decay at rate $\alpha_1$**, the same shape as GARCH(1,1)'s $\rho_k=\rho_1(\alpha_1+\beta_1)^{k-1}$ (L08-06). With $t$ shocks, replace the 3 in the denominator by $\kappa_\varepsilon$.

### 4.1 · Worked — Tsay Example 12.3 (monthly S&P 500 log returns in %, 1962–2009; T p. 642)

Posterior means: $\alpha_0=0.454$, $\alpha_1=0.837$, $\sigma_v^2=0.086$ (Tsay's $\ln h_t=\ln\sigma_t^2$). By (3):

$$\mu_h=\frac{0.454}{1-0.837}=\frac{0.454}{0.163}=2.785,\qquad\sigma_h^2=\frac{0.086}{1-0.837^2}=\frac{0.086}{1-0.700569}=\frac{0.086}{0.299431}=0.2872.$$

By (5): $E(a_t^2)=\exp(2.785+0.2872/2)=\exp(2.785+0.1436)=\exp(2.929)=18.71$ (%²), so the unconditional sd is $\sqrt{18.71}=4.33\%$ a month. By (7): kurtosis $3e^{0.2872}=3\times1.3327=3.998$. By (9) at $i=1$: $(e^{0.2872\times0.837}-1)/(3\times1.3327-1)=(e^{0.2404}-1)/2.998=0.2717/2.998=0.0906$.

The Gaussian GARCH(1,1) of the same data (T (12.26), p. 640) has $h_t=0.878+0.125a_{t-1}^2+0.837h_{t-1}$ (Tsay's $h_t=\sigma_t^2$): persistence $0.125+0.837=0.962$, unconditional variance $0.878/0.038=23.1$ (%²), sd 4.81%. The two models agree on the order of magnitude of volatility.

### 4.2 · Worked — Petrobras SV-t (GARCH11-SVar1.html §5)

Posterior means on standardized returns: $\mu=-0.419$, $\phi=0.9842$, $\sigma=0.1388$, $\nu=12.13$. By (3) in `stochvol` form:

$$\sigma_h^2=\frac{0.1388^2}{1-0.9842^2}=\frac{0.019253}{0.031326}=0.6146.$$

With Gaussian $\varepsilon_t$, (7) gives kurtosis $3e^{0.6146}=3\times1.849=5.547$, and (9) gives the lag-1 correlation

$$\frac{e^{0.6146\times0.9842}-1}{3e^{0.6146}-1}=\frac{e^{0.6049}-1}{3\times1.8490-1}=\frac{0.8311}{4.5469}=0.1828.$$

The GARCH(1,1)-$t$ fitted by ML to the same series ($\alpha_1=0.073478$, $\beta_1=0.910218$) has $\rho_1=\alpha_1(1-\alpha_1\beta_1-\beta_1^2)/(1-2\alpha_1\beta_1-\beta_1^2)=0.2037$ (L08-06), and decays at $\alpha_1+\beta_1=0.9837$, against SV's $\phi=0.9842$.

![Two panels. Left (belongs to L08-07): news-impact curves of GARCH, GJR and EGARCH fitted to Petrobras. Right: autocorrelation of squared shocks against lag 1 to 100; the GARCH(1,1) curve starts at 0.204 and the SV-AR(1) curve at 0.183, both decaying at about 0.984 per lag and staying roughly parallel, near 0.04 and 0.03 at lag 100](figures/L08-news-impact-sv-memory.png)
*Figure — right panel: $\mathrm{corr}(a_t^2,a_{t-k}^2)$ for GARCH(1,1), $\rho_1(\alpha_1+\beta_1)^{k-1}$, and for SV-AR(1), equation (9), at the Petrobras calibrations of GARCH11-SVar1.html. The left panel is read in [[L08-07-garch-family-asymmetry-tails]].*

The two curves are almost parallel on the right: the persistence parameters (0.9837 and 0.9842) set the decay, and only the level of the first autocorrelation differs. **Squared-return autocorrelations alone cannot tell the two models apart.** What separates them is how the kurtosis is produced (§9) and whether the variance is known one step ahead (§1).

---

## 5 · C — why the likelihood is hard (T §12.7, p. 637)

Write $R=(r_1,\dots,r_n)'$ and the latent path $H=(h_1,\dots,h_n)'$ (Tsay's $h_t=\sigma_t^2$). Given $H$, the returns are independent normals. Given $\theta$, $H$ is a Gaussian AR(1) in logs. The likelihood of $\theta$ alone integrates the path out:

$$f(R\mid\theta)=\int f(R\mid H,\theta)\,f(H\mid\theta)\,dH,\tag{10}$$

"a mixture over the $n$-dimensional $H$ distribution" (T p. 637). For daily data $n$ is in the thousands, and there is no closed form, so (10) cannot be maximised as the GARCH likelihood is.

**Two ways out.**

1. **Quasi-likelihood by linearisation** (named in T p. 153; Harvey, Ruiz and Shephard 1994). Square and take logs of $a_t=\sigma_t\varepsilon_t$:

$$\ln a_t^2=\ln\sigma_t^2+\ln\varepsilon_t^2.\tag{11}$$

$\ln\varepsilon_t^2$ is a $\ln\chi_1^2$ variable with mean $\psi(1/2)+\ln2=-1.2704$ and variance $\pi^2/2=4.935$. So (11) plus (1) is a linear state-space model: an observed series equal to an AR(1) state plus non-Gaussian noise. The Kalman filter treats the noise as Gaussian and gives a quasi-likelihood. It is consistent but inefficient, because $\ln\chi_1^2$ is far from normal (long left tail), and it fails when some $a_t=0$. T (3.41)'s long-memory SV uses the same decomposition (p. 154). [G]
2. **Bayesian MCMC** (Jacquier, Polson and Rossi 1994; T §12.7): put $H$ among the unknowns and sample $(\theta,H)$ jointly from the posterior (§6). The integral (10) is never computed: the sampler draws $H$ and averages over the draws.

---

## 6 · C — the Gibbs sampler of Tsay §12.7.1 (pp. 637–640)

The model of T (12.20)–(12.21), in Tsay's notation ($h_t=\sigma_t^2$):

$$r_t=\beta_0+\beta_1x_{1t}+\dots+\beta_px_{pt}+a_t,\qquad a_t=\sqrt{h_t}\,\varepsilon_t,\tag{12}$$

$$\ln h_t=\alpha_0+\alpha_1\ln h_{t-1}+v_t,\qquad v_t\sim N(0,\sigma_v^2).\tag{13}$$

Priors are independent across the mean and volatility blocks, $p(\beta,\omega)=p(\beta)p(\omega)$ with $\omega=(\alpha_0,\alpha_1,\sigma_v^2)$. The sampler cycles through three conditionals: $f(\beta\mid R,X,H,\omega)$, $f(H\mid R,X,\beta,\omega)$, $f(\omega\mid R,X,\beta,H)$.

### 6.1 · $\beta\mid H$: weighted regression

Given $H$, (12) is a regression with known heteroskedasticity. Divide by $\sqrt{h_t}$:

$$r_{o,t}=x_{o,t}'\beta+\varepsilon_t,\qquad r_{o,t}=r_t/\sqrt{h_t},\quad x_{o,t}=x_t/\sqrt{h_t},\tag{14}$$

a homoskedastic regression with unit error variance. With prior $\beta\sim N(\beta_o,A_o)$ the posterior is $N(\beta_*,A_*)$ (T p. 638):

$$A_*^{-1}=\sum_tx_{o,t}x_{o,t}'+A_o^{-1},\qquad\beta_*=A_*\Big(\sum_tx_{o,t}r_{o,t}+A_o^{-1}\beta_o\Big).\tag{15}$$

In Example 12.3 the mean equation is $r_t=\mu+a_t$ ($x_t=1$), so (15) reads: precision $\sum_t1/h_t+1/4$ (prior $\mu\sim N(0,4)$), mean $\big(\sum_tr_t/h_t\big)\big/\big(\sum_t1/h_t+1/4\big)$, a precision-weighted average in which quiet months count more.

### 6.2 · $h_t\mid h_{t-1},h_{t+1}$: three factors (equation (12.23))

Only three densities in the joint posterior contain $h_t$ ($1<t<n$): $a_t$'s, which has variance $h_t$; the transition into $\ln h_t$ from $\ln h_{t-1}$; and the transition out of $\ln h_t$ to $\ln h_{t+1}$. So

$$f(h_t\mid\cdot)\propto f(a_t\mid h_t)\,f(h_t\mid h_{t-1},\omega)\,f(h_{t+1}\mid h_t,\omega).\tag{16}$$

Take the factors one at a time, writing $x=\ln h_t$.

- $a_t\mid h_t\sim N(0,h_t)$: $\ f(a_t\mid h_t)\propto h_t^{-1/2}\exp\{-a_t^2/(2h_t)\}$.
- $\ln h_t\mid\ln h_{t-1}\sim N(\alpha_0+\alpha_1\ln h_{t-1},\sigma_v^2)$ by (13). That is a density in $x$. As a density in $h_t$ it picks up the Jacobian $dx/dh_t=h_t^{-1}$: $\ f(h_t\mid h_{t-1})\propto h_t^{-1}\exp\{-(x-a)^2/(2\sigma_v^2)\}$ with $a=\alpha_0+\alpha_1\ln h_{t-1}$.
- $\ln h_{t+1}\mid\ln h_t\sim N(\alpha_0+\alpha_1x,\sigma_v^2)$: $\ f(h_{t+1}\mid h_t)\propto\exp\{-(\ln h_{t+1}-\alpha_0-\alpha_1x)^2/(2\sigma_v^2)\}$, with no Jacobian in $h_t$ (that one belongs to $h_{t+1}$).

Rewrite the third exponent as a square in $x$. Factor out $\alpha_1$:

$$(\ln h_{t+1}-\alpha_0-\alpha_1x)^2=\alpha_1^2(x-b)^2,\qquad b=\frac{\ln h_{t+1}-\alpha_0}{\alpha_1}.$$

The two exponents then sum to $-[(x-a)^2A+(x-b)^2C]/(2\sigma_v^2)$ with $A=1$ and $C=\alpha_1^2$. **Combine the two squares** (T p. 638, a scalar version of Box and Tiao's Lemma 1). Expand:

$$(x-a)^2A+(x-b)^2C=(A+C)x^2-2(Aa+Cb)x+Aa^2+Cb^2.$$

Complete the square with $c=(Aa+Cb)/(A+C)$:

$$=(A+C)(x-c)^2+Aa^2+Cb^2-(A+C)c^2,$$

and the constant simplifies:

$$Aa^2+Cb^2-\frac{(Aa+Cb)^2}{A+C}=\frac{(A+C)(Aa^2+Cb^2)-(Aa+Cb)^2}{A+C}=\frac{AC(a-b)^2}{A+C}.$$

So

$$(x-a)^2A+(x-b)^2C=(x-c)^2(A+C)+(a-b)^2\frac{AC}{A+C}.\tag{17}$$

The last term does not contain $h_t$ and drops into the proportionality constant. Substituting $A=1$, $a=\alpha_0+\alpha_1\ln h_{t-1}$, $C=\alpha_1^2$, $b=(\ln h_{t+1}-\alpha_0)/\alpha_1$ into $c$:

$$c=\frac{(\alpha_0+\alpha_1\ln h_{t-1})+\alpha_1^2\cdot\dfrac{\ln h_{t+1}-\alpha_0}{\alpha_1}}{1+\alpha_1^2}=\frac{\alpha_0+\alpha_1\ln h_{t-1}+\alpha_1\ln h_{t+1}-\alpha_1\alpha_0}{1+\alpha_1^2},$$

$$\mu_t\equiv c=\frac{\alpha_0(1-\alpha_1)+\alpha_1(\ln h_{t+1}+\ln h_{t-1})}{1+\alpha_1^2},\qquad\sigma^2\equiv\frac{\sigma_v^2}{A+C}=\frac{\sigma_v^2}{1+\alpha_1^2}.\tag{18}$$

Multiplying the three factors, $h_t^{-1/2}\cdot h_t^{-1}=h_t^{-1.5}$:

$$f(h_t\mid\cdot)\propto h_t^{-1.5}\exp\Big\{-\frac{a_t^2}{2h_t}-\frac{(\ln h_t-\mu_t)^2}{2\sigma^2}\Big\},\tag{19}$$

which is T (12.23). **Read (18):** the transition terms alone say $\ln h_t\sim N(\mu_t,\sigma^2)$, a smoother between its two neighbours (T p. 640 recovers it as the least-squares estimate of a "missing" $\ln h_t$ in an AR(1)). The factor $h_t^{-1/2}e^{-a_t^2/(2h_t)}$ then pulls $h_t$ toward $a_t^2$: a large return today raises today's volatility draw. (19) is not a standard density. Tsay draws from it by **Griddy Gibbs** (evaluate on a grid, sample from the discretised CDF); Jacquier, Polson and Rossi use a **Metropolis** step.

**End points** (T p. 639). For $t=1$, fix $h_1$ (or predict $h_0$ backwards using time reversibility, $\ln h_0$ from a 2-step backcast); for $t=n$ use only $\ln h_n\sim N(\alpha_0+\alpha_1\ln h_{n-1},\sigma_v^2)$, or forecast $h_{n+1}$.

### 6.3 · $\omega\mid H$: an AR(1) regression and an inverted $\chi^2$

Given $H$, (13) is a Gaussian AR(1) in $\ln h_t$, so L01-07 §5's regression applies. With $z_t=(1,\ln h_{t-1})'$, $\alpha=(\alpha_0,\alpha_1)'$ and prior $\alpha\sim N(\alpha_o,C_o)$ (T pp. 638–639):

$$C_*^{-1}=\sum_{t=2}^n\frac{z_tz_t'}{\sigma_v^2}+C_o^{-1},\qquad\alpha_*=C_*\Big(\sum_{t=2}^n\frac{z_t\ln h_t}{\sigma_v^2}+C_o^{-1}\alpha_o\Big).\tag{20}$$

With $v_t=\ln h_t-\alpha_0-\alpha_1\ln h_{t-1}$ and prior $m\lambda/\sigma_v^2\sim\chi_m^2$:

$$\frac{m\lambda+\sum_{t=2}^nv_t^2}{\sigma_v^2}\ \Big|\ H,\alpha\ \sim\ \chi^2_{m+n-1}.\tag{21}$$

> **Every block is a regression once $H$ is given.** The latent path turns one intractable likelihood into three conjugate updates plus a one-dimensional draw per $h_t$.

### 6.4 · Example 12.3, the run (T pp. 640–642)

Data: 575 monthly S&P 500 log returns (%), January 1962 to December 2009. Model (12.27): $r_t=\mu+a_t$, $\ln h_t=\alpha_0+\alpha_1\ln h_{t-1}+v_t$. Priors: $\mu\sim N(0,4)$; $\alpha\sim N[(0,0.6)',\mathrm{diag}(0.25,0.04)]$; $10\times0.1/\sigma_v^2\sim\chi_{10}^2$ ($m=10$, $\lambda=0.1$). Start: the GARCH(1,1) volatilities of (12.26). $h_t$ by Griddy Gibbs with 400 grid points. 2500 iterations, the first 500 discarded.

| | $\mu$ | $\alpha_0$ | $\alpha_1$ | $\sigma_v^2$ |
|---|---|---|---|---|
| posterior mean | 0.409 | 0.454 | 0.837 | 0.086 |
| posterior sd | 0.157 | 0.068 | 0.025 | 0.007 |

$\alpha_1=0.837$ confirms "strong serial dependence in the volatility series", and is smaller than Jacquier, Polson and Rossi's daily estimate (T p. 642). Its implied moments are §4.1's. *Minor inconsistency in Tsay:* the text says the posterior mean of $h_t$ is taken "over the 5000 iterations", while the run keeps 2000 and the captions of Figures 12.5–12.6 say 2000.

---

## 7 · C — the Student-$t$ question on the S&P 500 (sp500-gaussian-student-SV-models.html §1–4)

Daily S&P 500 log returns, May 2017 to May 2022, demeaned ($y_t$).

**Model 1, iid $N(0,\sigma^2)$.** The MLE of $\sigma$ is $\hat\sigma_1=\sqrt{\sum y_t^2/n}=0.012729$.

**Model 2, iid $\sigma t_\nu$** (not standardized: $y_t/\sigma\sim t_\nu$). The page profiles the log-likelihood $\sum_t\ln f_{t_\nu}(y_t/\sigma)-n\ln\sigma$ over a grid of 1000 values of $\sigma\in[0.001,0.15]$, for $\nu\in\{1,\dots,30,35,\dots,100,200,\dots,1000\}$, and keeps the best pair: $\hat\nu=2$, $\hat\sigma_2=0.005922$.

Reading it:

- $\hat\sigma_2$ is a **scale, not a standard deviation**. A $t_2$ has infinite variance, so $\hat\sigma_2<\hat\sigma_1$ says nothing about which model sees less risk.
- $\hat\nu=2$ means the iid model needs tails heavy enough to have **no finite variance**. That is the iid model's way of absorbing the 2020 COVID cluster: an iid law can only fit a cluster of large returns by making large returns likely every day.
- The page's quantile plot puts the empirical quantiles of the returns beside those of $N(0,\hat\sigma_1^2)$ and of $\hat\sigma_2t_2$ at tail probabilities 0.01, 0.03, …, 0.99: the comparison to read is in the outer quantiles, where a Gaussian with the sample variance has the least mass.

**The SV reading.** Volatility clustering is serial dependence in the scale, not a property of the marginal. Once $h_t$ moves, each day's conditional law can be close to normal, and the marginal still has kurtosis $3e^{\sigma_h^2}$ by (7). That is why the page then fits SV, SVt, SVl and SVtl and compares the four volatility paths with $0.1\lvert r_t\rvert$.

---

## 8 · C — `stochvol`'s default priors (sp500 page §5.2; Kastner 2016)

$$\mu\sim N(0,100^2),\quad\frac{\phi+1}{2}\sim\mathrm{Beta}(5,1.5),\quad\sigma^2\sim\mathrm{Gamma}\big(\tfrac12,\tfrac12\big),\quad h_1\sim N\Big(\mu,\frac{\sigma^2}{1-\phi^2}\Big),\quad\frac{\rho+1}{2}\sim\mathrm{Beta}(4,4),\quad\nu\sim\mathrm{Exp}(0.1).\tag{22}$$

What each says:

- **$\mu$**: flat on the scale of log variances.
- **$\phi$**: the Beta is on $(\phi+1)/2\in(0,1)$, so $\phi\in(-1,1)$: **stationarity is imposed by the prior**. $E[(\phi+1)/2]=5/6.5=0.769$, so $E(\phi)=2(0.769)-1=0.538$. The mode of the Beta is $(5-1)/(5+1.5-2)=4/4.5=0.889$, so the prior mode of $\phi$ is $0.778$. The prior leans toward persistence, and the data move it to 0.98.
- **$\sigma^2$**: `stochvol`'s `priorsigma` $=B_\sigma$ means $\sigma^2\sim B_\sigma\chi^2_1=\mathrm{Gamma}\big(\tfrac12,\ \text{rate }\tfrac1{2B_\sigma}\big)$, equivalently $\sigma\sim\lvert N(0,B_\sigma)\rvert$. The default $B_\sigma=1$ gives the page's $\mathrm{Gamma}(1/2,1/2)=\chi_1^2$. A half-normal on $\sigma$ keeps mass near 0, which lets the data shrink toward constant volatility (Kastner's argument against an inverse-gamma prior here). [G]
- **$h_1$**: the stationary law (3).
- **$\rho$**: $\mathrm{Beta}(4,4)$ on $(\rho+1)/2$ is symmetric, so $E(\rho)=0$. Its variance is $4\cdot4/(8^2\cdot9)=0.0278$, so $\mathrm{sd}(\rho)=2\sqrt{0.0278}=0.333$.
- **$\nu$**: exponential with rate 0.1, $E(\nu)=10$.

**How `stochvol` samples** [G]: it uses the linearisation (11) with $\ln\varepsilon_t^2$ approximated by a finite mixture of normals (the auxiliary-mixture sampler), draws the whole path $H$ in one block, and alternates centred and non-centred parametrisations (ASIS, Kastner and Frühwirth-Schnatter 2014). This explains the warning in garch-sv-petrobras.html: the simple returns contain values "very close to zero", $\ln y_t^2\to-\infty$, so the package adds an offset of $3.1\times10^{-6}$, and suggests demeaning first.

---

## 9 · C — GARCH vs SV on Petrobras (GARCH11-SVar1.html)

Petrobras ADR, August 2000 to March 2021, log returns demeaned and divided by their sd (so $V=1$ in sample). Three fits:

| | $\alpha_0$ / $\mu$ | $\alpha_1$ / $\phi$ | $\beta_1$ / $\sigma$ | $\nu$ | persistence |
|---|---|---|---|---|---|
| GARCH(1,1)-$t$, ML (fGarch) | 0.014364 | 0.073478 | 0.910218 | 7.026 | 0.9837 |
| GARCH(1,1)-$t$, Bayes (bayesGARCH), posterior means | 0.019209 | 0.085027 | 0.894024 | 6.984 | 0.9791 |
| SV-AR(1)-$t$ (`svtsample`), posterior means | $\mu=-0.419$ | $\phi=0.9842$ | $\sigma=0.1388$ | 12.13 | 0.9842 |

**The volatility paths** (page §5.1) are overlaid over the full sample and over the last 1000 days (the data are downloaded by the page and not on disk, so this note does not reproduce the plot). The structural difference to look for: GARCH's $\sigma_t^2$ jumps by $\alpha_1a_{t-1}^2$ the day *after* a large return and then decays at $\alpha_1+\beta_1$, while SV's posterior $h_t$ is a smoother of its two neighbours, (18), pulled toward $a_t^2$ on the *same* day, (19).

**Why $\nu$ differs, 7 against 12.** Both models must reproduce the same sample kurtosis of the returns. In SV the volatility shock alone supplies the factor $e^{\sigma_h^2}=1.849$ of (7). With $\nu=12.13$ the $t$ shocks supply $\kappa_\varepsilon=3(12.13-2)/(12.13-4)=3\times10.13/8.13=3.738$, and the total is $3.738\times1.849=6.91$. GARCH's $\alpha_1a_{t-1}^2$ feedback also fattens tails, but only through $\alpha_1$ (L08-06: Gaussian excess $6\alpha_1^2/(1-2\alpha_1^2-(\alpha_1+\beta_1)^2)=1.50$ at the ML values), so GARCH loads more of the kurtosis on $\varepsilon_t$: $\nu=7$, and total kurtosis 11.87 by Tiao's formula (L08-07).

> **Fat tails can come from the shock or from the volatility.** SV splits them between two sources, GARCH mostly loads them on the shock. A fitted $\nu$ is not comparable across the two models.

**The page's residual check** (§5.2): returns divided by each model's median $\sigma_t$, with histograms and normal QQ plots. A well-specified model leaves standardized returns that look iid $t_\nu$ (or normal for SV, whose extra kurtosis lives in $h_t$).

*Errata in GARCH11-SVar1.html.* Section 3 is titled "standard GARCH(1,1) with Gaussian errors", but the call is `garchFit(..., cond.dist="std")`, a Student-$t$ fit (hence the "shape" 7.026). Its SV table prints a "p-value" of 1.9987 for $\mu$. The code computes $2(1-\Phi(m/se))$ with $m/se=-3.22<0$; the two-sided value is $2\Phi(-3.22)=0.0013$. (A p-value for a posterior mean is a frequentist reading of a Bayesian summary anyway.)

---

## 10 · G — beyond the class

- **Long-memory SV** (T (3.41), p. 154): $\sigma_t=\sigma\exp(u_t/2)$ with $(1-B)^du_t=\eta_t$; by (11), $\ln a_t^2$ is a Gaussian long-memory signal plus non-Gaussian white noise. Median $\hat d\approx0.38$ in the studies Tsay cites. Long memory is in [[L08-04-long-memory-arfima]].
- **Particle filters** evaluate (10) by sequential Monte Carlo (named only: the syllabus lists SMC, no book on disk covers it).
- **Multivariate and factor SV**: Class 9 (`Aula/class-09/materials/sv-fsv-US-BR.html`).

---

## Links

- Neighbours: [[L08-07-garch-family-asymmetry-tails]] (EGARCH's log variance, leverage, Tiao's kurtosis) · [[L08-09-bayesian-garch]] (Bayesian GARCH, the observation-driven counterpart).
- Unit: [[L08-00-map]] · [[L08-06-arch-garch]] (GARCH moments and the ACF of $a_t^2$) · [[L08-10-formulas]] · [[L08-11-pitfalls]] · [[L08-12-python]] (SV simulation: moments (5)–(9) checked by Monte Carlo).
- Class 1: [[../L01/L01-07-ar-var-review|L01-07]] (the AR(1) equilibrium law (16) behind (3), the regression of §5 behind (20)) · [[../L01/L01-04-first-bayesian-poisson|L01-04]] (the first conjugate update). Classes 3+4 (Gibbs sampling, Metropolis–Hastings) supply the MCMC machinery used in §6.
- Rules: [[../../rules/05_espaco_estados_volatilidade|rules/05]] (state space, volatility).
- **Practice (number and printed page only).** No Class 8 practice item is specifically about SV. The volatility items are T 3.14 (p. 171) and W 12.4 (p. 397); the rest of the volatility list is in [[L08-06-arch-garch]]. Solutions: `Listas/lista-L08-book-exercises.pdf`.
