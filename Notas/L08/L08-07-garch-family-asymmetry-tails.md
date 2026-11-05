---
tags: [notes, lecture-08, time-series, volatility, gjr, tgarch, aparch, egarch, garch-m, student-t, ged, leverage, news-impact]
date: 2026-10-25
status: taught
source: "garchmodeling.html (TS-GARCH, T-GARCH, GJR-GARCH, APARCH and its special cases, EGARCH via rugarch, GARCH(1,1) with Student-t, skewed t, t with ν = 7, Laplace/GED; Petrobras 2000–2021, n = 5167); T §3.4 (eqs. 3.7–3.10, pp. 121–122), §3.7 (eq. 3.23, p. 142), §3.8 (eqs. 3.24–3.25, pp. 143–148), §3.9 (eqs. 3.34–3.35, p. 149), §3.16 (pp. 165–166)"
---

# 3.7–3.9, 3.16 · The GARCH family: leverage, log-variance, risk premia and fat-tailed innovations

> **Claim.** GARCH treats $+a$ and $-a$ alike. **Asymmetric models give bad news a bigger coefficient.** GJR/TGARCH do it with an indicator, APARCH with $(\lvert a\rvert-\gamma a)^\delta$, EGARCH with a signed term in $\ln\sigma_t^2$. **What the site's output reports is not always what its formula says**: fGarch's `leverage=TRUE` fits the APARCH form, so the printed $\gamma_1=0.208$ for Petrobras means bad-news and good-news coefficients $0.135$ and $0.058$ (ratio 2.33), not "$\alpha+\gamma$ against $\alpha$". GARCH-M puts $\sigma_t^2$ in the mean (a risk premium). **Fat-tailed innovations matter more than any asymmetry**: the Student-$t$ fit adds 141 log-likelihood points to Gaussian GARCH, against 22 for GJR. Tiao's formula splits the total kurtosis into the part the innovations bring and the part the volatility dynamics bring.
> Prev: [[L08-06-arch-garch]] · Next: [[L08-08-stochastic-volatility]] · Map: [[L08-00-map]]

**Notation.** As in [[L08-06-arch-garch]]: $a_t=\sigma_t\varepsilon_t$, $\varepsilon_t$ iid, mean 0, variance 1; $\sigma_\infty^2$ the unconditional variance. In addition:

| Symbol | Meaning | Range |
|---|---|---|
| $\omega$ | the site's constant (Tsay's $\alpha_0$) | |
| $\gamma$ | asymmetry parameter (meaning depends on the model, §2–§4) | |
| $\delta$ | APARCH power | $\delta>0$ |
| $N_{t-1}$ | indicator $1\{a_{t-1}<0\}$ (T eq. 3.34) | $\{0,1\}$ |
| $g(\varepsilon)$ | EGARCH's weighted innovation | |
| $\theta$ | EGARCH sign coefficient (rugarch's $\alpha_1$) | |
| $c$ | GARCH-M risk-premium parameter | |
| $K$ | excess kurtosis of $\varepsilon_t$ | $K=6/(\nu-4)$ for $t_\nu$ |
| $K_a$, $K_a^{(g)}$ | excess kurtosis of $a_t$, and its value with Gaussian $\varepsilon_t$ | |
| $\nu$, $\xi$ | Student-$t$ degrees of freedom; skew parameter | $\nu>2$; $\xi>0$ |

---

## 1 · U — the news-impact curve

Fix yesterday's volatility at its unconditional level, $\sigma_{t-1}=\sigma_\infty$, and plot today's variance against yesterday's standardized shock $\varepsilon_{t-1}$. That is the **news-impact curve** (NIC). For GARCH(1,1), L08-06 (23) gives

$$NIC(\varepsilon)=\alpha_0+\alpha_1\sigma_\infty^2\varepsilon^2+\beta_1\sigma_\infty^2,\tag{1}$$

a parabola symmetric about 0. The leverage fact (L08-06 §1, fact 4) says the left branch should be steeper. Each model below bends one branch.

---

## 2 · C — threshold models: GJR, TGARCH, TS-GARCH (garchmodeling.html; T §3.9, p. 149)

**GJR / TGARCH($m,s$)** (Glosten–Jagannathan–Runkle 1993, Zakoian 1994; T eq. 3.34):

$$\sigma_t^2=\alpha_0+\sum_{i=1}^s(\alpha_i+\gamma_iN_{t-i})a_{t-i}^2+\sum_{j=1}^m\beta_j\sigma_{t-j}^2,\qquad N_{t-i}=1\{a_{t-i}<0\}.\tag{2}$$

A positive $a_{t-1}$ contributes $\alpha_1a_{t-1}^2$, a negative one $(\alpha_1+\gamma_1)a_{t-1}^2$, with $\gamma_1>0$ for leverage. Threshold 0 separates the regimes.

**Worked — IBM monthly log returns 1926–2003 (T eq. 3.35).** With GED innovations (shape 1.51):

$$\sigma_t^2=3.45\times10^{-4}+(0.0658+0.0843N_{t-1})a_{t-1}^2+0.8182\,\sigma_{t-1}^2.$$

Good news: 0.0658. Bad news: $0.0658+0.0843=0.1501$, **2.3 times larger**. Checks $Q(12)=18.34$ ($p=0.106$) for $\tilde a_t$, $Q(12)=5.36$ ($p=0.95$) for $\tilde a_t^2$; the leverage term is significant at 5%.

The site's page writes (2) for GJR and its $\sigma_t$ analogue for T-GARCH,

$$\sigma_t=\omega+\alpha_1\lvert a_{t-1}\rvert+\gamma_1\lvert a_{t-1}\rvert N_{t-1}+\beta_1\sigma_{t-1},\tag{3}$$

and the **Taylor–Schwert** model is (3) with $\gamma_1=0$: $\sigma_t=\omega+\alpha_1\lvert a_{t-1}\rvert+\beta_1\sigma_{t-1}$. Standard deviations, not variances, follow the recursion.

---

## 3 · C — APARCH, and what fGarch actually estimates (garchmodeling.html; Ding, Granger and Engle 1993)

The **asymmetric power** GARCH:

$$\sigma_t^\delta=\omega+\alpha_1\big(\lvert a_{t-1}\rvert-\gamma_1a_{t-1}\big)^\delta+\beta_1\sigma_{t-1}^\delta,\qquad \delta>0,\ \gamma_1\in(-1,1).\tag{4}$$

**The term $\lvert a\rvert-\gamma a$, split by sign.** For $a\ge0$, $\lvert a\rvert-\gamma a=a(1-\gamma)$. For $a<0$, $\lvert a\rvert=-a$, so $\lvert a\rvert-\gamma a=-a-\gamma a=\lvert a\rvert(1+\gamma)$. Therefore

$$\big(\lvert a\rvert-\gamma a\big)^\delta=\begin{cases}(1-\gamma)^\delta\lvert a\rvert^\delta,& a\ge0\ \text{(good news)}\\ (1+\gamma)^\delta\lvert a\rvert^\delta,& a<0\ \text{(bad news)}.\end{cases}\tag{5}$$

**Special cases** (the page's list, with the sign of $\gamma$ made explicit):

| Model | $\delta$ | $\gamma_1$ | $\beta_1$ |
|---|---|---|---|
| ARCH | 2 | 0 | 0 |
| GARCH | 2 | 0 | free |
| TS-GARCH | 1 | 0 | free |
| T-GARCH (asymmetric, in $\sigma$) | 1 | $\in(0,1)$ | free |
| GJR (asymmetric, in $\sigma^2$) | 2 | $\in(0,1)$ | free |

**The mapping.** `garchFit(~garch(1,1), delta=2, leverage=TRUE)` and `delta=1, leverage=TRUE` fit (4) with $\delta$ fixed. So the printed `gamma1` is **APARCH's $\gamma_1$**, not the indicator coefficient of (2) and (3). With $\delta=2$, (5) turns (4) into (2) with

$$\alpha_1^{GJR}=\alpha_1(1-\gamma_1)^2,\qquad \alpha_1^{GJR}+\gamma_1^{GJR}=\alpha_1(1+\gamma_1)^2,$$

$$\gamma_1^{GJR}=\alpha_1\big[(1+\gamma_1)^2-(1-\gamma_1)^2\big]=\alpha_1\big[(1+2\gamma_1+\gamma_1^2)-(1-2\gamma_1+\gamma_1^2)\big]=4\alpha_1\gamma_1.\tag{6}$$

**Persistence.** With symmetric $\varepsilon$, $E(\lvert\varepsilon\rvert\varepsilon)=0$, so

$$E\big(\lvert\varepsilon\rvert-\gamma\varepsilon\big)^2=E(\varepsilon^2)-2\gamma E(\lvert\varepsilon\rvert\varepsilon)+\gamma^2E(\varepsilon^2)=1+\gamma^2,$$

and taking expectations of (4) with $\delta=2$ as in L08-06 (22):

$$\sigma_\infty^2=\frac{\omega}{1-\alpha_1(1+\gamma_1^2)-\beta_1}.\tag{7}$$

**Worked — Petrobras GJR, $\delta=2$ (garchmodeling.html).** $\hat\omega=2.327\times10^{-5}$, $\hat\alpha_1=0.09234$, $\hat\gamma_1=0.20835$, $\hat\beta_1=0.88178$, log-lik 11174.01.

- Good news: $0.09234\times(1-0.20835)^2=0.09234\times0.62671=$ **0.05787**.
- Bad news: $0.09234\times(1+0.20835)^2=0.09234\times1.46011=$ **0.13483**. Ratio $1.46011/0.62671=2.33$.
- Indicator coefficient (6): $4\times0.09234\times0.20835=$ **0.07696**, and indeed $0.05787+0.07696=0.13483$.
- Persistence: $0.09234\times(1+0.04341)+0.88178=0.09635+0.88178=$ **0.97813**.

Reading the page's formula literally ($\alpha_1+\gamma_1=0.30$ against $\alpha_1=0.09$) would give persistence $0.09234+0.20835/2+0.88178=1.078$, **a non-stationary model that was never fitted**.

**Worked — Petrobras T-GARCH, $\delta=1$.** $\hat\omega=0.000725$, $\hat\alpha_1=0.09641$, $\hat\gamma_1=0.34588$, $\hat\beta_1=0.90265$. In the $\sigma_t$ recursion, a bad shock enters with $\alpha_1(1+\gamma_1)=0.09641\times1.34588=$ **0.12976** and a good one with $\alpha_1(1-\gamma_1)=0.09641\times0.65412=$ **0.06306**: ratio 2.06 in the standard deviation.

**Worked — Petrobras APARCH, $\delta$ estimated.** $\hat\delta=1.436$, $\hat\gamma_1=0.2713$, $\hat\alpha_1=0.0990$, $\hat\beta_1=0.8927$. By (5), the bad/good ratio in $\sigma^\delta$ is $(1.2713/0.7287)^{1.436}=1.7446^{1.436}=\exp(1.436\times0.5566)=\exp(0.7993)=2.22$. The power sits between the $\sigma$ ($\delta=1$) and $\sigma^2$ ($\delta=2$) versions, and the log-likelihood (11170.95) is lower than GJR's (11174.01) despite one more parameter, which says the two are close optima and $\delta=2$ is not rejected.

---

## 4 · C — EGARCH (T §3.8, pp. 143–148; garchmodeling.html via rugarch)

Nelson (1991) builds asymmetry into a **weighted innovation** (T eq. 3.24):

$$g(\varepsilon_t)=\theta\varepsilon_t+\gamma\big[\lvert\varepsilon_t\rvert-E\lvert\varepsilon_t\rvert\big],\qquad E[g(\varepsilon_t)]=0.\tag{8}$$

Split by sign, with $\lvert\varepsilon\rvert=\varepsilon$ for $\varepsilon\ge0$ and $-\varepsilon$ for $\varepsilon<0$:

$$g(\varepsilon_t)=\begin{cases}(\theta+\gamma)\varepsilon_t-\gamma E\lvert\varepsilon_t\rvert,&\varepsilon_t\ge0\\ (\theta-\gamma)\varepsilon_t-\gamma E\lvert\varepsilon_t\rvert,&\varepsilon_t<0,\end{cases}\tag{9}$$

so the slope is $\theta+\gamma$ on good news and $\theta-\gamma$ on bad news; $\theta<0$ makes the bad-news branch steeper. For Gaussian $\varepsilon$, $E\lvert\varepsilon\rvert=\sqrt{2/\pi}=0.7979$. For the standardized $t_\nu$ of L08-06 (16) (T p. 143):

$$E\lvert\varepsilon_t\rvert=\frac{2\sqrt{\nu-2}\,\Gamma\big(\frac{\nu+1}2\big)}{(\nu-1)\Gamma\big(\frac\nu2\big)\sqrt\pi}.\tag{10}$$

At $\nu=7.04$ (the Petrobras $t$ fit) this is $0.7595$: the heavier tails put more mass near 0 and in the tails, so the mean absolute value falls below the Gaussian 0.7979.

The EGARCH($m,s$) model (T eq. 3.25) is an ARMA in $\ln\sigma_t^2$ driven by $g$:

$$a_t=\sigma_t\varepsilon_t,\qquad \ln\sigma_t^2=\alpha_0+\frac{1+\beta_1B+\dots+\beta_{s-1}B^{s-1}}{1-\alpha_1B-\dots-\alpha_mB^m}\,g(\varepsilon_{t-1}).\tag{11}$$

**Why the log.** $\sigma_t^2=\exp(\cdot)>0$ for any coefficients, so **no positivity constraints** are needed. Since $E g=0$, the unconditional mean of $\ln\sigma_t^2$ is $\alpha_0$.

**rugarch's EGARCH(1,1)**, the one the page fits:

$$\ln\sigma_t^2=\omega+\alpha_1\varepsilon_{t-1}+\gamma_1\big(\lvert\varepsilon_{t-1}\rvert-E\lvert\varepsilon_{t-1}\rvert\big)+\beta_1\ln\sigma_{t-1}^2.\tag{12}$$

Its $\alpha_1$ is Nelson's $\theta$. Taking expectations with $\lvert\beta_1\rvert<1$:

$$E\ln\sigma_t^2=\frac{\omega}{1-\beta_1}.\tag{13}$$

**The bad/good ratio.** Compare a shock $\varepsilon_{t-1}=-c$ with $+c$, same $\sigma_{t-1}$. In (12) the $\gamma_1$ terms are equal and cancel:

$$\ln\sigma_t^2(-c)-\ln\sigma_t^2(+c)=\alpha_1(-c)-\alpha_1(c)=-2\alpha_1c\quad\Longrightarrow\quad\frac{\sigma_t^2(-c)}{\sigma_t^2(+c)}=e^{-2\alpha_1c}.\tag{14}$$

**Worked — Petrobras EGARCH(1,1) (garchmodeling.html, with a mean $\mu=0.00028$, insignificant).** $\hat\omega=-0.15392$, $\hat\alpha_1=-0.05549$, $\hat\beta_1=0.97741$, $\hat\gamma_1=0.18138$, log-lik 11173.14.

- By (13): $E\ln\sigma_t^2=-0.15392/(1-0.97741)=-0.15392/0.02259=-6.814$, so $e^{-6.814/2}=0.0331$, a typical daily volatility of 3.3%, matching GARCH's 0.0336.
- Relative to a zero shock, by (12): $\varepsilon=-1$ raises $\ln\sigma_t^2$ by $-\alpha_1+\gamma_1=0.05549+0.18138=0.23687$; $\varepsilon=+1$ by $\alpha_1+\gamma_1=-0.05549+0.18138=0.12589$.
- By (14): at $c=1$, $e^{0.11098}=1.117$; at $c=2$, $e^{0.22196}=1.249$. **A two-sigma drop raises next-day variance 25% more than a two-sigma rise.**
- $\hat\beta_1=0.977$: log-volatility persistence close to GARCH's 0.980.

**Diagnostics printed by rugarch** (read briefly). Weighted Ljung–Box on $\tilde a_t$: lag-1 statistic 12.77, $p=0.0004$, so some serial correlation is left in the **mean** (the model has none). On $\tilde a_t^2$: $p$ from 0.11 to 0.48, so the volatility dynamics are captured. ARCH LM: $p\ge0.49$. Sign bias: negative-size bias $t=2.04$ ($p=0.042$), joint $p=0.049$, so a little asymmetry is left. Nyblom joint statistic 1.68 > 1.47 (5% critical value): parameter instability over 20 years. Adjusted Pearson goodness of fit: $p\approx10^{-9}$, **the Gaussian innovation is rejected**, which leads to §6.

**Forecasting (G, T p. 148).** Exponentiating (12) one step ahead gives $\sigma_{h+1}^2$ exactly. Two steps ahead requires $E_h\exp[g(\varepsilon_{h+1})]$, which for Gaussian $\varepsilon$ is $\exp(-\gamma\sqrt{2/\pi})\big[e^{(\theta+\gamma)^2/2}\Phi(\theta+\gamma)+e^{(\theta-\gamma)^2/2}\Phi(\gamma-\theta)\big]$; the $j$-step forecast follows by recursion. Not examinable.

![Left: next-period variance relative to the unconditional variance against yesterday's standardized shock for Petrobras GARCH, GJR and EGARCH fits; GARCH is a symmetric parabola, GJR is steeper on the negative side, EGARCH is an asymmetric exponential curve that rises more for negative shocks. Right: autocorrelation of squared shocks against lag for GARCH(1,1) and SV-AR(1), both decaying at about 0.984](figures/L08-news-impact-sv-memory.png)
*Figure — left: news-impact curves $\sigma_t^2/\sigma_\infty^2$ at $\sigma_{t-1}=\sigma_\infty$ for the Petrobras fits of garchmodeling.html: GARCH (1), GJR in its fitted APARCH form (4) with $\delta=2$ and $\sigma_\infty^2$ from (7), EGARCH (12) at $\ln\sigma_{t-1}^2$ equal to (13). The right panel belongs to [[L08-08-stochastic-volatility]].*

GARCH's parabola is symmetric. GJR keeps the parabola shape but makes the left branch 2.33 times steeper, so a $-4\sigma$ day lifts variance far more than a $+4\sigma$ day. EGARCH is an exponential in $\lvert\varepsilon\rvert$, flatter near 0 and asymmetric by the factor (14). Near $\varepsilon=0$ all three agree: they differ only in how they treat large news.

---

## 5 · C — GARCH-M: volatility in the mean (T §3.7, p. 142)

$$r_t=\mu+c\,\sigma_t^2+a_t,\qquad a_t=\sigma_t\varepsilon_t,\qquad \sigma_t^2=\alpha_0+\alpha_1a_{t-1}^2+\beta_1\sigma_{t-1}^2.\tag{15}$$

$c$ is the **risk-premium parameter**: $c>0$ means expected return rises with volatility. Variants use $c\,\sigma_t$ or $c\ln\sigma_t^2$. Because $\sigma_t^2$ is serially correlated, (15) **makes $r_t$ serially correlated**, which is another source of the small autocorrelations in historical returns.

**Worked — S&P 500 monthly excess returns 1926–1991 (Tsay, S-Plus):** $r_t=0.0055+1.09\sigma_t^2+a_t$, $\sigma_t^2=8.76\times10^{-5}+0.123a_{t-1}^2+0.849\sigma_{t-1}^2$. The premium is positive but $t=1.09/0.818=1.33$: not significant at 5%. At the unconditional variance 0.00314 of L08-06 §4.4, it adds $1.09\times0.00314=0.0034$ a month to the expected excess return.

---

## 6 · C — non-Gaussian innovations and the kurtosis decomposition (T eqs. 3.7–3.10, pp. 121–122; §3.16, pp. 165–166)

**Distributions on offer** (fGarch's `cond.dist`): `norm`, `std` (standardized $t$, L08-06 (16)), `sstd` (skew-$t$), `ged`, `snorm`, `sged`.

- **Skew-$t$** (Fernández–Steel, T eq. 3.9): the standardized $t$ is stretched by $\xi$ above the mode and by $1/\xi$ below it, then re-centred and re-scaled to mean 0, variance 1. $\xi^2$ is the ratio of probability mass above to below the mode: $\xi<1$ means a longer left tail.
- **GED** (T eq. 3.10): $f(x)=\dfrac{\nu\exp\big(-\frac12\lvert x/\lambda\rvert^\nu\big)}{\lambda\,2^{1+1/\nu}\Gamma(1/\nu)}$, $\lambda=\big[2^{-2/\nu}\Gamma(1/\nu)/\Gamma(3/\nu)\big]^{1/2}$. $\nu=2$ is the normal, $\nu<2$ has heavier tails, and $\nu=1$ is the **Laplace** (double exponential).

**Why a heavy-tailed $\varepsilon$ lowers $\hat\alpha_1$ (T p. 126).** Under Gaussian $\varepsilon$, every large $\lvert a_t\rvert$ must be explained by a large $\sigma_t$, so the fit pushes $\alpha_1$ up. A $t$ innovation can produce the outlier itself. Intel: $\hat\alpha_1=0.356\to0.2845$ ([[L08-06-arch-garch]] §3.4); Petrobras: $0.1032\to0.0743$ below.

**Tiao's formula (T p. 166).** With $E(\varepsilon_t^4)=K+3$, the excess kurtosis of $a_t$ from L08-06 (24) can be written as

$$K_a=\frac{K+K_a^{(g)}+\frac56KK_a^{(g)}}{1-\frac16KK_a^{(g)}},\qquad K_a^{(g)}=\frac{6\alpha_1^2}{1-2\alpha_1^2-(\alpha_1+\beta_1)^2}.\tag{16}$$

**Total tails = innovation tails $K$ + dynamics tails $K_a^{(g)}$ + an interaction.** With $\alpha_1=0$, $K_a^{(g)}=0$ and $K_a=K$. For the standardized $t_\nu$, $E(\varepsilon^4)=3+6/(\nu-4)$, so $K=6/(\nu-4)$ for $\nu>4$, and substituting into (16):

$$K_a=\frac{6+(\nu+1)K_a^{(g)}}{\nu-4-K_a^{(g)}},\qquad\text{finite iff}\quad 1-2\alpha_1^2\frac{\nu-1}{\nu-4}-(\alpha_1+\beta_1)^2>0.\tag{17}$$

**Worked — Petrobras GARCH(1,1)-$t$ (garchmodeling.html):** $\hat\alpha_1=0.07429$, $\hat\beta_1=0.90947$, $\hat\nu=7.04$ (precisely 7.0426), log-lik 11292.37.

- Persistence $0.07429+0.90947=0.98376$; $\pi^2=0.96778$; $2\alpha_1^2=2(0.0055190)=0.011038$.
- Dynamics part, (16): $1-0.011038-0.96778=0.021184$, so $K_a^{(g)}=6(0.0055190)/0.021184=0.033114/0.021184=$ **1.563**.
- Innovation part: $K=6/(7.0426-4)=6/3.0426=$ **1.972**.
- Existence, (17): $2\alpha_1^2(\nu-1)/(\nu-4)=0.011038\times6.0426/3.0426=0.011038\times1.98600=0.021922$, and $1-0.021922-0.96778=0.0103>0$: **the fourth moment exists, barely.**
- Total, (17): $\dfrac{6+8.0426\times1.5631}{3.0426-1.5631}=\dfrac{6+12.571}{1.4795}=\dfrac{18.571}{1.4795}=$ **12.55**. Neither part alone (1.56 or 1.97) comes close: the interaction dominates when the moment condition is nearly binding.

**The other non-Gaussian fits (same page).** Skew-$t$: $\hat\xi=0.9407$ (se 0.017, so $\xi^2=0.885$: slightly more mass below the mode), $\hat\nu=7.01$, $\hat\alpha_1=0.07299$, $\hat\beta_1=0.91130$, log-lik 11297.85. $t$ with $\nu$ fixed at 7: virtually identical to the free fit (log-lik 11292.37), since $\hat\nu=7.04$ anyway. Laplace (GED shape fixed at 1): $\hat\alpha_1=0.09340$, $\hat\beta_1=0.90081$, log-lik 11192.49. *The page's legend labels the $\nu=7$ fit "GARCH t(3)".*

### 6.1 · Reading the log-likelihood ladder

AIC $=-2\ell+2q$ ($q$ = number of estimated parameters; no mean term except EGARCH's $\mu$):

| Model | $q$ | log-lik | AIC | gain over GARCH |
|---|---|---|---|---|
| ARCH(1) | 2 | 10672.32 | −21340.6 | −479.4 |
| TS-GARCH | 3 | 11107.02 | −22208.0 | −44.7 |
| GARCH(1,1) | 3 | 11151.72 | −22297.4 | 0 |
| T-GARCH | 4 | 11121.07 | −22234.1 | −30.7 |
| APARCH | 5 | 11170.95 | −22331.9 | +19.2 |
| EGARCH (with $\mu$) | 5 | 11173.14 | −22336.3 | +21.4 |
| GJR | 4 | 11174.01 | −22340.0 | +22.3 |
| GARCH, Laplace | 3 | 11192.49 | −22379.0 | +40.8 |
| GARCH-$t$, $\nu=7$ fixed | 3 | 11292.37 | −22578.7 | +140.7 |
| GARCH-$t$ | 4 | 11292.37 | −22576.7 | +140.7 |
| GARCH skew-$t$ | 5 | 11297.85 | **−22585.7** | +146.1 |

Three readings. (i) **Modelling $\sigma$ instead of $\sigma^2$ hurts here** (TS-GARCH and T-GARCH below GARCH): $\delta=2$ suits Petrobras, as APARCH's $\hat\delta=1.44$ with a lower likelihood than GJR confirms. (ii) **Asymmetry is worth about 22 points for one parameter** (GJR), a clear AIC gain. (iii) **The innovation distribution is worth 141 points** for one parameter, six times the asymmetry; skew adds 5.5 more. The rugarch EGARCH reports Akaike $-4.3229$ per observation, and $-4.3229\times5167=-22336.4$ reproduces its row. The page's $\sigma_t$ comparison shows all these models tracing nearly the same volatility path: they disagree about tails and asymmetry, not about when volatility is high.

---

## Links

- Neighbours: [[L08-06-arch-garch]] (GARCH(1,1), kurtosis (24)–(25), forecasts) · [[L08-08-stochastic-volatility]] (the right panel of the figure; a second shock in the variance).
- Unit: [[L08-00-map]] · [[L08-09-bayesian-garch]] (GARCH(1,1)-$t$ by MCMC) · [[L08-10-formulas]] · [[L08-11-pitfalls]] · [[L08-12-python]].
- Class 1: [[../L01/L01-07-ar-var-review|L01-07]] §2 (uncorrelated ≠ independent).
- Rules: [[../../rules/05_espaco_estados_volatilidade|rules/05]] (ARCH/GARCH variants).
- **Practice (number and printed page only):** T 3.14 (p. 171). Related, from the ARCH/GARCH block: T 3.4 (p. 168, Student-$t$ likelihood). Solutions: `Listas/lista-L08-book-exercises.pdf`.
