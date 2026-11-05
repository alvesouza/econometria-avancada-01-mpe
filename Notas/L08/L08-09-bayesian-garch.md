---
tags: [notes, lecture-08, time-series, volatility, garch, bayesian, conjugate-prior, gibbs, metropolis-hastings, student-t]
date: 2026-10-25
status: taught
source: "bayes-garch.pdf (Lopes, May 2015; 22 slides: Petrobras log prices and returns 2000–2013, models M0–M3, training-sample priors, Gibbs output, bayesGARCH for GARCH(1,1)-t, Pr(α1+β > 1 | data) = 0.0034, posterior quantiles of the volatility); GARCH11-SVar1.html §4–4.1 (bayesGARCH vs fGarch on standardized Petrobras returns, 2000–2021); T §12.7 p. 637 (augmenting latent variables, the Gibbs logic); T §3.4 eq. (3.7) p. 121 (standardized Student-t)"
---

# Bayesian GARCH · conjugate warm-ups, a GARCH-t posterior, and what $\Pr(\alpha_1+\beta>1\mid\text{data})$ says

> **Claim.** **The deck builds up to Bayesian GARCH through three models that are conjugate**: iid $N(0,\sigma^2)$ (one inverse-gamma update), iid $N(\mu,\sigma^2)$ and an AR(1) on log prices (Gibbs with normal and inverse-gamma conditionals). Their priors are **elicited from a training sample** (2001–2006) and the posterior uses 2007–2013. **GARCH(1,1) with Student-$t$ errors is not conjugate**: $h_t$ depends on $(\alpha_0,\alpha_1,\beta)$ through a recursion, so the posterior is sampled by Metropolis–Hastings steps (`bayesGARCH`, Ardia and Hoogerheide 2010). The payoff is **probability statements about functions of the parameters**: $\Pr(\alpha_1+\beta>1\mid\text{data})=0.0034$ on Petrobras, and a posterior band for every $\sigma_t$. On the 2000–2021 Petrobras series the posterior means put persistence at 0.9791 against the MLE's 0.9837, because a posterior mean averages along a curved likelihood ridge that the mode does not see.
> Prev: [[L08-08-stochastic-volatility]] · Next: [[L08-10-formulas]] · Map: [[L08-00-map]]

**Notation.** The deck writes the GARCH variance as $h_t$ (Tsay's $\sigma_t^2$; *not* `stochvol`'s log variance of [[L08-08-stochastic-volatility]]) and the GARCH coefficient as $\beta$ (Tsay's $\beta_1$).

| Symbol | Meaning | Range |
|---|---|---|
| $p_t$, $y_t=\ln p_t$ | Petrobras price and log price | |
| $r_t=y_t-y_{t-1}$ | log return | |
| $n_0$, $n$ | training sample (2001–2006) 1506 days; posterior sample (2007–2013) 1760 days | |
| $m_{\tilde r}$, $V_{\tilde r}$, $m_{\tilde r^2}$ | training mean and variance of $r_t$, training mean of $r_t^2$ | |
| $(a,b,s)$, $(s_a,s_b)$ | training OLS estimates of the AR(1) on log prices and their standard errors | |
| $\mathrm{IG}(a,b)$ | inverse gamma, density $\propto(\sigma^2)^{-(a+1)}e^{-b/\sigma^2}$, mean $b/(a-1)$ | $a,b>0$ |
| $\mu,\sigma^2$ | mean and variance of the iid models | |
| $\alpha,\beta$ in M2 | intercept and slope of $y_t\mid y_{t-1}$ | |
| $\alpha_0,\alpha_1,\beta$ in M3 | GARCH(1,1) constant, ARCH and GARCH coefficients | $\alpha_0>0$, $\alpha_1,\beta\ge0$ |
| $h_t$ | conditional variance of $r_t$ in M3 | $>0$ |
| $\nu$, $\varrho=(\nu-2)/\nu$ | Student-$t$ degrees of freedom and the scaling that makes $V(r_t\mid h_t)=h_t$ | $\nu>2$ |
| $\lambda,\delta$ | rate and shift of the translated-exponential prior on $\nu$ | $\lambda>0$, $\delta\ge2$ |
| $\varpi_t$ | auxiliary mixing variable of the $t$ as a scale mixture of normals | $>0$ |

---

## 1 · C — the data and the training-sample design (slides 1–8)

Petrobras log prices, 12/29/2000 to 12/31/2013 ($n=3268$ days), and log returns, 01/02/2001 to 12/31/2013 (3267 days). The scatter of $y_{t-1}$ against $y_t$ (slide 3) lies on the 45-degree line: log prices behave like a random walk ([[L08-03-unit-roots-dickey-fuller]]).

**Split.** The first $n_0=1506$ days (2001–2006) are used only to build the priors. The last $n=1760$ days (2007–2013) give the posterior. Training-sample summaries (slide 7):

$$(m_{\tilde r},V_{\tilde r})=(0.00112605,\ 0.0006609406),\qquad m_{\tilde r^2}=0.0006617694,$$

and OLS of $y_t$ on $(1,y_{t-1})$ in the training sample:

$$(a,b,s)=(0.0005451564,\ 1.0003342482,\ 0.02569926),\qquad(s_a,s_b)=(0.0018491322,\ 0.0009933758).$$

> **A training sample turns a subjective prior into a reproducible one.** The prior is the posterior of an earlier period, inflated so that the later data dominate. Every prior below multiplies a training variance by 100 or uses an inverse gamma with only 5 "prior observations".

**Three conjugate models** (slide 6):

- **M0**: $r_1,\dots,r_n$ iid $N(0,\sigma^2)$.
- **M1**: $r_1,\dots,r_n$ iid $N(\mu,\sigma^2)$.
- **M2**: $y_t\mid y_{t-1}\sim N(\alpha+\beta y_{t-1},\sigma^2)$, $t=2,\dots,n$, on log prices.

---

## 2 · C — M0: one inverse-gamma update, every step

**Prior** (slide 8): $\sigma^2\sim\mathrm{IG}(5,\ 4m_{\tilde r^2})$, that is

$$p(\sigma^2)\propto(\sigma^2)^{-(5+1)}\exp\Big\{-\frac{4m_{\tilde r^2}}{\sigma^2}\Big\}.\tag{1}$$

Its mean is $b/(a-1)$:

$$E(\sigma^2)=\frac{4m_{\tilde r^2}}{5-1}=m_{\tilde r^2}=0.0006617694,$$

so **the prior is centred at the training-sample mean square**, the training MLE of $\sigma^2$ under M0. Its variance is $b^2/[(a-1)^2(a-2)]$, so

$$\mathrm{sd}(\sigma^2)=\frac{E(\sigma^2)}{\sqrt{a-2}}=\frac{0.0006617694}{\sqrt3}=0.000382.$$

**Likelihood.** For iid $N(0,\sigma^2)$:

$$L(\sigma^2)=\prod_{t=1}^n(2\pi\sigma^2)^{-1/2}\exp\Big\{-\frac{r_t^2}{2\sigma^2}\Big\}\propto(\sigma^2)^{-n/2}\exp\Big\{-\frac{\sum_tr_t^2}{2\sigma^2}\Big\}.\tag{2}$$

Setting $d\ln L/d\sigma^2=-n/(2\sigma^2)+\sum r_t^2/(2\sigma^4)=0$ gives the MLE

$$\hat\sigma^2=\frac{1}{n}\sum_{t=1}^nr_t^2.\tag{3}$$

**Posterior.** Multiply (1) by (2) and collect powers of $\sigma^2$ and terms in $1/\sigma^2$:

$$p(\sigma^2\mid r)\propto(\sigma^2)^{-(5+1)}e^{-4m_{\tilde r^2}/\sigma^2}\cdot(\sigma^2)^{-n/2}e^{-\sum r_t^2/(2\sigma^2)}=(\sigma^2)^{-(5+n/2+1)}\exp\Big\{-\frac{4m_{\tilde r^2}+\sum r_t^2/2}{\sigma^2}\Big\},$$

which is the kernel of

$$\sigma^2\mid r\sim\mathrm{IG}\Big(5+\frac n2,\ 4m_{\tilde r^2}+\frac12\sum_{t=1}^nr_t^2\Big).\tag{4}$$

With $n=1760$: shape $5+880=885$.

**The posterior mean as a weighted average.** By (4) and $\sum r_t^2=n\hat\sigma^2$ from (3):

$$E(\sigma^2\mid r)=\frac{4m_{\tilde r^2}+\tfrac n2\hat\sigma^2}{5+\tfrac n2-1}=\frac{4}{4+\tfrac n2}\,m_{\tilde r^2}+\frac{\tfrac n2}{4+\tfrac n2}\,\hat\sigma^2.\tag{5}$$

With $n=1760$ the prior weight is $4/(4+880)=4/884=0.0045$: **0.45% prior, 99.55% data**. The prior counts as $2(a-1)=8$ observations, against 1760. This is the inverse-gamma version of the Gamma–Poisson shrinkage $a/(n+a)$ of [[../L01/L01-04-first-bayesian-poisson|L01-04]]. Slide 9 plots prior, posterior and MLE: the posterior is a narrow spike near 0.0011, on the MLE, while the prior, centred at the 2001–2006 value 0.00066, is far wider. The 2007–2013 returns were more volatile than the training years, and with 0.45% weight the prior cannot hold the posterior back.

---

## 3 · C — M1: Gibbs with two conjugate conditionals (slides 8, 10–11)

**Priors** (independent):

$$\mu\sim N\Big(m_{\tilde r},\ \frac{100V_{\tilde r}}{n_0-1}\Big),\qquad\sigma^2\sim\mathrm{IG}(5,\ 4V_{\tilde r}).\tag{6}$$

$V_{\tilde r}/(n_0-1)$ is about the squared standard error of the training mean, so the prior sd of $\mu$ is 10 such standard errors:

$$\tau_0^2=\frac{100\times0.0006609406}{1505}=4.3916\times10^{-5},\qquad\tau_0=0.006627,$$

about six times the training mean 0.001126. $E(\sigma^2)=4V_{\tilde r}/4=V_{\tilde r}$, as in M0.

**$\mu\mid\sigma^2,r$.** As a function of $\mu$, the likelihood is $\exp\{-\sum(r_t-\mu)^2/(2\sigma^2)\}\propto\exp\{-n(\mu-\bar r)^2/(2\sigma^2)\}$ (expand the square around $\bar r$; the remainder does not contain $\mu$). Times the normal prior, the exponent is $-\tfrac12[(\mu-\bar r)^2n/\sigma^2+(\mu-m_{\tilde r})^2/\tau_0^2]$. Completing the square as in L08-08 (17), with $A=n/\sigma^2$ and $C=1/\tau_0^2$:

$$\mu\mid\sigma^2,r\sim N\Big(\frac{n\bar r/\sigma^2+m_{\tilde r}/\tau_0^2}{n/\sigma^2+1/\tau_0^2},\ \frac{1}{n/\sigma^2+1/\tau_0^2}\Big).\tag{7}$$

The mean is **precision-weighted**: data precision $n/\sigma^2$ against prior precision $1/\tau_0^2$.

**$\sigma^2\mid\mu,r$.** Repeat §2 with $r_t-\mu$ in place of $r_t$:

$$\sigma^2\mid\mu,r\sim\mathrm{IG}\Big(5+\frac n2,\ 4V_{\tilde r}+\frac12\sum_t(r_t-\mu)^2\Big).\tag{8}$$

**The sampler.** Start at $\sigma^{2(0)}$; for $j=1,\dots,M$ draw $\mu^{(j)}$ from (7) given $\sigma^{2(j-1)}$, then $\sigma^{2(j)}$ from (8) given $\mu^{(j)}$. Slide 10 shows 100 000 iterations: traces that look like noise and ACFs at zero from lag 1, i.e. practically independent draws (the two blocks barely interact: with $\bar r\approx0$ small next to the spread of $r_t$, $\sum_t(r_t-\mu)^2$ is almost flat in $\mu$). Slide 11: the prior of $\mu$ spans about $\pm0.02$, the posterior about $\pm0.002$.

---

## 4 · C — M2: the AR(1) on log prices, a Bayesian unit-root look (slides 8, 12–13)

**Priors:**

$$\alpha\sim N(a,100s_a^2),\qquad\beta\sim N(b,100s_b^2),\qquad\sigma^2\sim\mathrm{IG}(5,4s^2).\tag{9}$$

Numbers: $\mathrm{sd}(\alpha)=10\times0.0018491=0.01849$; $\mathrm{sd}(\beta)=10\times0.00099338=0.00993$; $E(\sigma^2)=s^2=0.02569926^2=0.00066045$.

**Conditionals.** Given $\sigma^2$, M2 is a normal linear regression of $y_t$ on $x_t=(1,y_{t-1})'$, with a normal prior $N(m_0,D_0)$, $m_0=(a,b)'$, $D_0=\mathrm{diag}(100s_a^2,100s_b^2)$. The posterior has the same form as L08-08 (15) with $x_{o,t}=x_t/\sigma$:

$$(\alpha,\beta)'\mid\sigma^2,y\sim N\Big(D_*\big(\textstyle\sum_tx_ty_t/\sigma^2+D_0^{-1}m_0\big),\ D_*\Big),\qquad D_*^{-1}=\sum_tx_tx_t'/\sigma^2+D_0^{-1},\tag{10}$$

and, as in (8),

$$\sigma^2\mid\alpha,\beta,y\sim\mathrm{IG}\Big(5+\frac{n-1}2,\ 4s^2+\frac12\sum_{t=2}^n(y_t-\alpha-\beta y_{t-1})^2\Big).\tag{11}$$

**The unit-root reading.** The training OLS slope is $b=1.00033$, above 1, with $(b-1)/s_b=0.000334/0.000993=0.34$: nowhere near a rejection of $\beta=1$, and the Dickey–Fuller caveat of L08-03 applies to that $t$ anyway. The prior $N(1.00033,0.00993^2)$ gives $\Pr(\beta>1)=0.513$. A Bayesian does not need the Dickey–Fuller distribution: the posterior of $\beta$ is a statement about $\beta$ given the data, whatever the sampling distribution of $\hat\beta$ would be (Sims's argument, named). Slide 13 shows the posterior of $\beta$ as a spike at about 1 inside the prior's 0.97–1.03 spread. Slide 12 shows the cost: the draws of $\alpha$ and of $\beta$ have ACFs still near 0.5 at lag 50, while those of $\sigma^2$ are uncorrelated. With a near-unit-root regressor $y_{t-1}$ whose mean is far from 0, $\alpha$ and $\beta$ are almost collinear ($\hat\alpha\approx\bar y(1-\hat\beta)$), and a sampler that updates them one at a time crawls along that ridge.

---

## 5 · C — M3: GARCH(1,1) with Student-$t$ errors (slides 14–16)

**Model** (slide 14):

$$r_t\mid h_t\sim t_\nu(0,\varrho h_t),\qquad h_t=\alpha_0+\alpha_1r_{t-1}^2+\beta h_{t-1},\qquad\varrho=\frac{\nu-2}{\nu},\tag{12}$$

with $\alpha_0>0$, $\alpha_1\ge0$, $\beta>0$, and $h_0=0$ "for convenience" (so $r_0=0$, and $h_1=\alpha_0$ starts the recursion).

**Why $\varrho$.** A $t_\nu(0,s^2)$ variable is $s$ times a standard $t_\nu$, whose variance is $\nu/(\nu-2)$. With $s^2=\varrho h_t$:

$$V(r_t\mid h_t)=\varrho h_t\cdot\frac{\nu}{\nu-2}=\frac{\nu-2}{\nu}\,h_t\,\frac{\nu}{\nu-2}=h_t.\tag{13}$$

So $h_t$ is the conditional variance, exactly as in Tsay's standardized $t$ of T (3.7) (p. 121) with $\varepsilon_t=r_t/\sqrt{h_t}$.

**Likelihood.** The $t_\nu(0,s^2)$ density with $s^2=\varrho h_t$ and $\nu\varrho=\nu-2$:

$$f(r_t\mid h_t,\nu)=\frac{\Gamma\big(\tfrac{\nu+1}2\big)}{\Gamma\big(\tfrac\nu2\big)\sqrt{(\nu-2)\pi h_t}}\Big(1+\frac{r_t^2}{(\nu-2)h_t}\Big)^{-(\nu+1)/2},\tag{14}$$

and the conditional likelihood is $L(\alpha_0,\alpha_1,\beta,\nu)=\prod_{t=1}^nf(r_t\mid h_t,\nu)$ with $h_t$ from the recursion in (12): the same object fGarch maximises ([[L08-07-garch-family-asymmetry-tails]], [[L08-06-arch-garch]]).

**Priors** (slide 15; the `bayesGARCH` call on slide 16). With $\alpha=(\alpha_0,\alpha_1)'$:

$$\alpha\sim N_2(\mu_\alpha,\Sigma_\alpha)\,\mathbb 1\{\alpha>0\},\qquad\beta\sim N(\mu_\beta,\Sigma_\beta)\,\mathbb 1\{\beta>0\},\qquad p(\nu)=\lambda e^{-\lambda(\nu-\delta)}\mathbb 1\{\nu>\delta\}.\tag{15}$$

The translated exponential has $E(\nu)=\delta+1/\lambda$. The call used, `bayesGARCH(r, mu.alpha=c(0,0), Sigma.alpha=1000*diag(1,2), mu.beta=0, Sigma.beta=1000, lambda=0.01, delta=2)`, gives:

- normal priors with variance 1000 truncated to positive values: **flat on the region of interest** ($\alpha_1,\beta<1$ while the prior sd is 31.6);
- $\nu-2\sim\mathrm{Exp}(0.01)$: $E(\nu)=2+1/0.01=102$, sd 100. Vague, and $\nu>2$ keeps the variance finite. The deck notes that $\lambda=100$, $\delta=500$ forces $\nu\approx500$: the **normal case**.

> **The prior does not impose $\alpha_1+\beta<1$.** That is what makes $\Pr(\alpha_1+\beta>1\mid\text{data})$ a question the data answer (§7).

---

## 6 · C/G — why no conjugacy, and how `bayesGARCH` samples

In M0–M2 every conditional was normal or inverse gamma because the parameters entered the likelihood linearly (in the mean) or as a single scale. In (12), $h_t=\alpha_0\sum_{j<t}\beta^j+\alpha_1\sum_{j<t}\beta^jr_{t-1-j}^2$: **$\beta$ enters through powers, and every $h_t$ depends on all three coefficients**. No prior makes $p(\alpha_0,\alpha_1,\beta\mid r)$ a known family. Three routes:

1. **Random-walk Metropolis–Hastings** (C): propose $\theta^*=\theta^{(j-1)}+\text{noise}$, accept with probability $\min\{1,\ p(\theta^*\mid r)/p(\theta^{(j-1)}\mid r)\}$; the posterior is needed only up to its constant, i.e. (14) times (15), one pass of the recursion per evaluation. [[L08-12-python]] runs this sampler on simulated GARCH(1,1)-$t$ data.

```text
for j in 1..M:
    θ* = θ(j-1) + N(0, c·Σ)                      # proposal
    if θ* violates α0>0, α1≥0, β>0, ν>δ: reject
    log A = log p(r|θ*) + log p(θ*) - log p(r|θ(j-1)) - log p(θ(j-1))
    accept θ* with probability min(1, exp(log A))
```

2. **Griddy Gibbs** (Bauwens and Lubrano 1998): draw each coefficient from its conditional evaluated on a grid, as Tsay does for $h_t$ in L08-08 §6.2.
3. **Ardia and Hoogerheide (2010)**, the method in `bayesGARCH` [G]. Write the $t$ as a **scale mixture of normals**:

$$r_t\mid\varpi_t,h_t\sim N(0,\varpi_t\varrho h_t),\qquad\varpi_t\sim\mathrm{IG}\big(\tfrac\nu2,\tfrac\nu2\big).\tag{16}$$

Integrating $\varpi_t$ out returns $t_\nu(0,\varrho h_t)$. Given $\varpi=(\varpi_1,\dots,\varpi_n)$, each $\varpi_t$ has a conjugate IG conditional, and $(\alpha,\beta)$ are drawn by MH with proposals from an approximating GLS regression on the ARMA form of GARCH, $r_t^2=\alpha_0+(\alpha_1+\beta)r_{t-1}^2+w_t-\beta w_{t-1}$ ([[L08-06-arch-garch]]; Nakatsuma 2000). $\nu$ is drawn by an optimised rejection step. This is T §12.7's device again: augment latent variables until each block is easy.

**The run** (slide 17): 10 000 burn-in draws discarded, 10 000 kept, one chain, on the returns $r_0$ of the first part of the data.

---

## 7 · C — reading the output (slides 18–21)

**Traces and marginals** (slides 18–19). Posterior draws span roughly $\alpha_0\in(1,5)\times10^{-5}$, $\alpha_1\in(0.04,0.16)$, $\beta\in(0.82,0.94)$, $\nu\in(4,12)$. The ACFs of the draws decay slowly and reach zero only after roughly 100–150 lags: MH chains on GARCH are sticky, so 10 000 draws carry far fewer effective draws.

**The persistence** (slide 20). Each draw gives $\alpha_1^{(j)}+\beta^{(j)}$, and the histogram of these sums is the posterior of the persistence. The deck reports

$$\Pr(\alpha_1+\beta>1\mid\text{data})=\frac{1}{M}\sum_{j=1}^M\mathbb 1\{\alpha_1^{(j)}+\beta^{(j)}>1\}=0.0034,\tag{17}$$

34 of the 10 000 kept draws. Its Monte Carlo standard error is at least $\sqrt{0.0034\times0.9966/10\,000}=0.00058$ (iid draws; more with autocorrelation).

> **This is a direct probability that the model is covariance stationary: 99.66%.** A frequentist test of $H_0:\alpha_1+\beta=1$ gives a p-value, which is a probability about the data under $H_0$, not about the hypothesis (L01-08). And because the prior (15) was flat on both sides of the line, the 0.34% is the data's verdict, not the prior's.

**The volatility with uncertainty** (slide 21). For each draw $j$, run the recursion (12) to get $h_t^{(j)}$, $t=1,\dots,n$; the 2.5%, 50% and 97.5% quantiles of $\{\sqrt{h_t^{(j)}}\}_j$ at each $t$ are a posterior band for $\sigma_t$. GARCH11-SVar1.html §4 does exactly this (its loop `sig2s[,t] = draws[,1] + draws[,2]*ret[t-1]^2 + draws[,3]*sig2s[,t-1]`). Any function of the parameters (unconditional variance, half-life, a VaR) gets its posterior the same way: compute it draw by draw.

---

## 8 · C — Bayes vs ML on the same data (GARCH11-SVar1.html §3–4.1)

Petrobras 2000–2021, returns demeaned and standardized. `bayesGARCH` with the priors of §5, 40 000 iterations, the first 20 000 discarded; fGarch's ML with `cond.dist="std"`.

| | $\alpha_0$ | $\alpha_1$ | $\beta$ | $\nu$ |
|---|---|---|---|---|
| ML estimate (s.e.) | 0.014364 (0.003164) | 0.073478 (0.009216) | 0.910218 (0.011001) | 7.026 (0.622) |
| posterior mean (sd) | 0.019209 (0.003783) | 0.085027 (0.010200) | 0.894024 (0.012120) | 6.984 (0.601) |
| (mean − ML)/posterior sd | 1.28 | 1.13 | −1.34 | −0.07 |

Derived quantities, persistence first:

$$\text{Bayes: }0.085027+0.894024=0.979051,\qquad\text{ML: }0.073478+0.910218=0.983696.$$

Unconditional variance $\alpha_0/(1-\alpha_1-\beta)$:

$$\text{Bayes: }\frac{0.019209}{1-0.979051}=\frac{0.019209}{0.020949}=0.9169,\qquad\text{ML: }\frac{0.014364}{0.016304}=0.8810,$$

both near the sample variance 1 of standardized returns. Half-life $\ln0.5/\ln(\alpha_1+\beta)$: Bayes $-0.69315/-0.021171=32.7$ days, ML $-0.69315/-0.016438=42.2$ days. (Plugging posterior means into a nonlinear function is not the posterior mean of the function; the draw-by-draw rule of §7 is the right one. The posterior mean of the persistence itself *is* 0.979051, by linearity.)

**Why the means move away from the MLE.** With a flat prior the MLE is the posterior **mode**. The GARCH likelihood has a **curved ridge**: the data pin down the unconditional variance $\alpha_0/(1-\alpha_1-\beta)$ and the persistence much better than each coefficient, so $\alpha_0$ and $1-\alpha_1-\beta$ trade off along a ridge, and the posterior is skewed along it. Averaging over a skewed posterior moves the mean off the mode: here toward a larger $\alpha_0$, a larger $\alpha_1$ and a smaller $\beta$, together about one posterior sd each, and toward lower persistence. $\nu$, whose posterior is nearly symmetric, barely moves ($-0.07$ sd). Page §4.1 overlays the two $\sigma_t$ paths (full sample and last 500 days). Expect them close: the fitted $\sigma_t$ depends on the coefficients mostly through the well-determined directions (persistence, unconditional variance), not along the ridge.

*A reading note.* The page's Bayes table labels the columns "t value" and "Pr(>|t|)", computing $m/\mathrm{sd}$ and $2(1-\Phi(m/\mathrm{sd}))$. Those are frequentist labels on posterior summaries; the Bayesian statement is a credible interval or a posterior probability such as (17).

---

## 9 · U — what the Bayesian route buys here

| Question | ML | Bayes |
|---|---|---|
| Is the model covariance stationary? | test $\alpha_1+\beta=1$ (boundary, nonstandard) | $\Pr(\alpha_1+\beta<1\mid r)=0.9966$ |
| Uncertainty in $\sigma_t$, half-life, VaR | delta method, case by case | quantiles of draws, one rule for all |
| Prior information | none | training sample (M0–M2) |
| Small samples, parameters near a boundary | asymptotic normality fails | exact finite-sample posterior |
| Cost | one optimisation | MCMC, sticky chains, diagnostics |

The deck's references (slide 22), named: Bauwens and Lubrano (1998, Griddy Gibbs), Nakatsuma (2000, MH for ARMA-GARCH), Vrontos, Dellaportas and Politis (2000, full Bayesian GARCH and EGARCH), Asai (2006, comparison of MCMC methods), Ardia and Hoogerheide (2010, `bayesGARCH`), Virbickaite, Ausín and Galeano (2015, survey).

---

## Links

- Neighbours: [[L08-08-stochastic-volatility]] (SV by MCMC: the same latent-variable logic) · [[L08-10-formulas]].
- Unit: [[L08-00-map]] · [[L08-06-arch-garch]] (GARCH moments, the ARMA form behind the GLS proposal) · [[L08-07-garch-family-asymmetry-tails]] (Student-$t$ likelihood, fGarch's output) · [[L08-03-unit-roots-dickey-fuller]] (the unit root behind M2) · [[L08-11-pitfalls]] · [[L08-12-python]] (conjugate M0 update and random-walk MH for GARCH(1,1)-$t$, with asserts).
- Class 1: [[../L01/L01-04-first-bayesian-poisson|L01-04]] (the first conjugate update and the shrinkage weight) · [[../L01/L01-07-ar-var-review|L01-07]] (the AR(1) regression behind M2) · [[../L01/L01-08-p-hacking-evidence|L01-08]] (a p-value is not a posterior probability). Classes 3+4 (conjugate analysis, Gibbs sampling, Metropolis–Hastings) supply the machinery used here.
- Rules: [[../../rules/05_espaco_estados_volatilidade|rules/05]].
- **Practice (number and printed page only).** No Class 8 practice item is specifically Bayesian. The volatility items are T 3.14 (p. 171) and W 12.4 (p. 397); T 3.3 and 3.4 (p. 168) ask for the conditional likelihoods that §5's (14) writes down for the $t$ case. Solutions: `Listas/lista-L08-book-exercises.pdf`.
