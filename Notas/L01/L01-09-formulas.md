---
tags: [notes, lecture-01, formulas, reference, likelihood, mle, mse, bootstrap, regression, ar, var]
date: 2026-10-19
status: taught
source: "The eight section notes L01-01 … L01-08 (equation numbers are theirs); Class 1 goals in Map/class-plan.md; the site's Class 1 description in Aula/COURSE.md; every number re-checked by Notas/L01/L01_python_checks.py"
---

# Class 1 · Formulas — the exam specification, every result, every number

> Prev: [[L01-08-p-hacking-evidence]] · Next: [[L01-10-pitfalls]] · Map: [[L01-00-map]]

Equations are cited by the **section note's own numbering**: "L01-02 (9)" is equation (9) of
[[L01-02-poisson-mle-properties]]. Every number in §2 is asserted in
[[L01-11-python]] (script `L01_python_checks.py`).

---

## 0 · The exam specification, mapped

### 0.1 · The site's description of Class 1 (`Aula/COURSE.md`)

"Brief review of basic ingredients", in five items:

| # | Site item (verbatim) | Where it is settled |
|---|---|---|
| i | "Parametric models, likelihoods, estimators and their sampling distributions" | [[L01-01-likelihood-sampling-rules]] (one likelihood, three sampling distributions); [[L01-02-poisson-mle-properties]] (the Poisson MLE checklist); [[L01-03-coal-mining-change-point]] (a two-regime likelihood); [[L01-05-comparing-estimators-mse-bootstrap]] (exact, MC and bootstrap sampling distributions) |
| ii | "Gaussian linear regression: estimation and variable selection" | [[L01-06-gaussian-linear-regression]] §2–§4 (estimation), §5–§7 (selection, overfitting) |
| iii | "AR(1) model: estimation, unit root, equilibrium distribution" | [[L01-07-ar-var-review]] §5 (estimation), §7 (unit root), §6 (equilibrium) |
| iv | "AR(p) model: connection to Gaussian linear regression" | [[L01-07-ar-var-review]] §8 |
| v | "VAR(1) model: multivariate estimation, matrix notation" | [[L01-07-ar-var-review]] §9 |

### 0.2 · The goals in `Map/class-plan.md`, item by item

| # | Goal | Note and section |
|---|---|---|
| 1 | Write a likelihood and derive the MLE | L01-01 §2–§3 (Bernoulli, binomial, negative binomial); L01-02 §3–§4 (Poisson); L01-05 §6 (uniform: boundary MLE); L01-06 §4 (Gaussian regression); L01-07 §5 (AR(1), conditional) |
| 2 | Sufficiency, unbiasedness, consistency, efficiency (Cramér–Rao) | L01-02 §3 (sufficiency, by definition and by factorisation), §5 (unbiased, consistent), §6 (CRLB, efficiency); L01-05 §6 ($x_{(n)}$ sufficient) |
| 3 | Check them by Monte Carlo | L01-02 §8 (slide 10's table, ±0.25 coverage); L01-05 §7 (four estimators at $\theta=3$, $n=10$) |
| 4 | Compare estimators by MSE (the four $U(0,\theta)$ estimators) | L01-05 §2–§5 (MSE = Var + bias², ranking for $n\ge3$), §8 (G: the best $c\,x_{(n)}$ is biased) |
| 5 | Nonparametric vs parametric bootstrap, and why the nonparametric one fails for the maximum | L01-05 §9 (nonparametric), §10 (the point mass $1-(1-1/n)^n\to0.632$), §11 (parametric fix) |
| 6 | Overdispersion and a Poisson change point (coal-mining disasters, profile likelihood, LR test) | L01-03 §2–§3 (dispersion test), §4–§5 (profile likelihood, $w(\tau)$), §6 (LR = 70.0 and why not $\chi^2_1$) |
| 7 | Gaussian linear regression in matrix form and variable selection | L01-06 §2 (normal equations, projection), §4 (OLS = MLE), §5–§6 ($R^2$, $\bar R^2$, $C_p$, AIC, BIC, best subset), §7 (overfitting), §8 (reading real output) |
| 8 | AR(1) estimation, the stationary (equilibrium) distribution and the unit-root case | L01-07 §4 (moments, ACF), §5 (OLS = conditional MLE), §6 (equilibrium law, half-life), §7 (random walk) |
| 9 | AR(p) as a regression | L01-07 §8 |
| 10 | VAR(1) in matrix notation | L01-07 §9 (stationarity by eigenvalues, mean, vec covariance; Tsay Ex. 8.3) |
| 11 | p-hacking and reproducibility | L01-08 §2–§3 (size, family-wise rate, Bonferroni), §4–§5 (p-value vs Bayes factor vs posterior), §6 (the evidence in economics) |
| — | Also on the Class 1 site list: the first Bayesian example | L01-04 (Exp prior → Gamma posterior, shrinkage) |
| — | Also on the Class 1 site list: sampling rules and the likelihood principle | L01-01 (same likelihood, different p-values; Beta posterior unchanged) |

**Exam format** (`Map/class-plan.md`, "Final exam"): no coding. Expect **derivations** (likelihoods,
MLEs, information, posteriors, AR moments) and **reading printed output** (the abstention table of
L01-06 §8 is the model).

---

## 1 · Every definition and result

### 1.1 · Likelihood and sampling rules → [[L01-01-likelihood-sampling-rules]]

| Eq. | Statement | Where |
|---|---|---|
| (1)–(3) | Bernoulli, binomial and negative-binomial data all give $L(\theta)\propto\theta^s(1-\theta)^{n-s}$ | §2 |
| Def. | **Likelihood principle**: proportional likelihoods give the same likelihood-based and Bayesian inference | §2 (slide 1) |
| (4)–(6) | $\ell=s\log\theta+(n-s)\log(1-\theta)$; score $s/\theta-(n-s)/(1-\theta)$; $\hat\theta=s/n$ | §3 |
| (7)–(8) | $J(\theta)=\frac{s}{\theta^2}+\frac{n-s}{(1-\theta)^2}$; $J(\hat\theta)=\frac{n}{\hat\theta(1-\hat\theta)}$, the same under every rule | §3 |
| (9)–(11) | Binomial: $P(\hat\theta=k/n)=\binom nk\theta^k(1-\theta)^{n-k}$; $E(\hat\theta)=\theta$, $V=\theta(1-\theta)/n$; $I(\theta)=n/[\theta(1-\theta)]$ (CRLB attained) | §4 |
| (12) | $\hat\theta\stackrel a\sim N(\theta,\theta(1-\theta)/n)$ | §4 |
| (13)–(15) | Negative binomial: $P(N=m)=\binom{m-1}{s-1}\theta^s(1-\theta)^{m-s}$; $I(\theta)=s/[\theta^2(1-\theta)]$; $\hat\theta\stackrel a\sim N(\theta,\theta^2(1-\theta)/s)$ | §5 |
| (16)–(18) | Delta method on $N\stackrel a\sim N(s/\theta,s(1-\theta)/\theta^2)$ gives (15); plug-in variances coincide: $\hat\theta(1-\hat\theta)/n$ | §6 |
| (19)–(20) | $E(s/N)>\theta$ (Jensen); for $s=1$, $E(1/N)=-\theta\log\theta/(1-\theta)$ | §7 |
| Haldane | $(s-1)/(N-1)$ is exactly unbiased for $s\ge2$ | §7 |
| Def. | p-value = *nível descritivo* (B Def. 6.3.1, p. 100); binomial $P(S\le s)$, negative binomial $P(N\ge n)$ | §9 |
| (21)–(22) | Beta$(a,b)$ prior → Beta$(a+s,b+n-s)$ under every rule; posterior mean = weighted average of prior mean and $s/n$ | §10 |
| (23) | $n\ge z^2\theta(1-\theta)/E^2$; worst case $\theta=1/2$ | §12 |

### 1.2 · The Poisson MLE → [[L01-02-poisson-mle-properties]]

| Eq. | Statement | Where |
|---|---|---|
| (1)–(3) | $\Pr(y\mid\lambda)=\lambda^ye^{-\lambda}/y!$; $E(y)=V(y)=\lambda$ (equidispersion) | §1 |
| (4)–(5) | $L(\lambda)=c\,\lambda^{s_n}e^{-n\lambda}$ | §3 |
| Def. 2.2.1 / Thm 2.2.1 | **Sufficiency**: the law of the sample given $T$ is free of $\lambda$; the factorisation criterion | §3 |
| (6) | $Y\mid T=t\sim$ multinomial$(t;1/n,\dots,1/n)$, free of $\lambda$ | §3 |
| (7)–(10) | $\ell=\log c+s_n\log\lambda-n\lambda$; $\hat\lambda=\bar y$; $\ell''=-s_n/\lambda^2<0$ (no MLE if $s_n=0$) | §4 |
| (11)–(12) | $E(\hat\lambda)=\lambda$; $V(\hat\lambda)=\lambda/n\to0$ | §5 |
| (13) | Chebyshev: $P(\lvert\hat\lambda-\lambda\rvert>\epsilon)\le\lambda/(n\epsilon^2)$ → **consistency** (B Def. 3.7.1) | §5 |
| (14) | $\hat\lambda\stackrel a\sim N(\lambda,\lambda/n)$; SE $=\sqrt{\hat\lambda/n}$ | §5 |
| (15)–(18) | **CRLB** $=1/I(\lambda)$, $I(\lambda)=n/\lambda$; $e(\hat\lambda)=1$: **efficient** (B Def. 2.1.1, Thm 2.1.1) | §6 |
| (19) | $V(s^2)=\lambda/n+2\lambda^2/(n-1)$ | §7 |
| (20)–(21) | $e(s^2)=\frac{1}{1+2\lambda n/(n-1)}\to\frac1{1+2\lambda}$ | §7 |

### 1.3 · Coal mining, change point, LR → [[L01-03-coal-mining-change-point]]

| Eq. | Statement | Where |
|---|---|---|
| (1) | Dispersion test $D=(n-1)s^2/\bar y\stackrel a\sim\chi^2_{n-1}$; upper tail = overdispersion | §3 |
| (2) | Law of total variance: $V(y)=E(\lambda)+\pi(1-\pi)(\lambda_1-\lambda_2)^2$ — a mixture is overdispersed | §3 |
| (3)–(4) | Two-regime model and its log-likelihood | §4 |
| (5) | $\hat\lambda_j(\tau)=s_j/n_j$ | §4 |
| (6) | **Profile likelihood** $\ell_p(\tau)=s_1\log\hat\lambda_1+s_2\log\hat\lambda_2-191$ (+ const.) (B §3.4, p. 47) | §4 |
| (7) | $w(\tau)=e^{\ell_p(\tau)}/\sum_{W}e^{\ell_p(\tau')}$ = posterior of $\tau$ under a uniform prior **with rates profiled out** | §4 |
| (8)–(9) | $\text{LR}=2\{\ell_p(\hat\tau)-\ell(\hat\lambda)\}=2[s_1\log(\hat\lambda_1/\hat\lambda)+s_2\log(\hat\lambda_2/\hat\lambda)]$ | §6 |
| GLRT / Wilks | $\lambda(x)=\sup_{\Theta_0}L/\sup_\Theta L$ (B (6.5.1)); $-2\log\lambda\to\chi^2$ under regularity (B Thm 6.5.1) — **fails here**: $\tau$ searched, unidentified under $H_0$, discrete | §6 |
| (10) | G: integrated $p(\tau\mid y)\propto\prod_j a\,\Gamma(s_j+1)/(n_j+a)^{s_j+1}$ | §8 |

### 1.4 · The first Bayesian example → [[L01-04-first-bayesian-poisson]]

| Eq. | Statement | Where |
|---|---|---|
| (1), (3) | Prior $p(\lambda)=ae^{-a\lambda}$; $E=1/a$, $V=1/a^2$ | §1 |
| (2) | $\int_0^\infty\lambda^ke^{-b\lambda}d\lambda=\Gamma(k+1)/b^{k+1}$ | §1 |
| (4) | Bayes: posterior ∝ likelihood × prior (G (2.3)) | §2 |
| (6)–(8) | Kernel $\lambda^{s_n}e^{-(a+n)\lambda}$ ⇒ $\lambda\mid y\sim G(s_n+1,a+n)$ (shape, **rate**) | §3 |
| (9) | Gamma: $E=\alpha/\beta$, $V=\alpha/\beta^2$, mode $(\alpha-1)/\beta$ | §4 |
| (10)–(12) | $E(\lambda\mid y)=\frac{s_n+1}{a+n}$; mode $\frac{s_n}{a+n}$; $V=\frac{s_n+1}{(a+n)^2}$ | §4 |
| (13)–(14) | **Shrinkage**: $E(\lambda\mid y)=\frac{a}{n+a}\cdot\frac1a+\frac{n}{n+a}\cdot\bar y$; mode $=\frac{n}{n+a}\bar y$ | §6 |

### 1.5 · MSE, Monte Carlo, bootstrap → [[L01-05-comparing-estimators-mse-bootstrap]]

| Eq. | Statement | Where |
|---|---|---|
| (1)–(3) | $\text{MSE}=E[(\hat\theta-\theta)^2]=V(\hat\theta)+B(\hat\theta)^2$ (B Def. 1.3.7, (1.3.2)) | §2 |
| (4)–(8) | $U(0,\theta)$: $E(x)=\theta/2$, $V(x)=\theta^2/12$; $E(\bar x)=\theta/2$, $V(\bar x)=\theta^2/(12n)$ | §3 |
| (9)–(14) | $x_{(n)}/\theta\sim$ Beta$(n,1)$; $E(x_{(n)})=\frac{n}{n+1}\theta$, $V(x_{(n)})=\frac{n\theta^2}{(n+1)^2(n+2)}$ | §3 |
| (15)–(18) | MSEs: $\frac{1+3n}{12n}\theta^2$, $\frac{2\theta^2}{(n+1)(n+2)}$, $\frac{\theta^2}{3n}$, $\frac{\theta^2}{n(n+2)}$ | §3–§4 |
| (19)–(22) | **Ranking** $\hat\theta_4<\hat\theta_2<\hat\theta_3<\hat\theta_1$ for $n\ge3$; all equal at $n=1$; $\hat\theta_2=\hat\theta_3$ at $n=2$ | §5 |
| (23)–(25) | $L(\theta)=\theta^{-n}\mathbb 1(\theta\ge x_{(n)})$; **boundary MLE** $x_{(n)}$ (score never zero); $x_{(n)}$ sufficient | §6 |
| (26) | MC: $\widehat{\text{MSE}}=\frac1N\sum_j(\hat\theta^{(j)}-\theta)^2$ | §7 |
| (27)–(29) | G: $\text{MSE}(c\,x_{(n)})$ minimised at $c^*=\frac{n+2}{n+1}$, value $\theta^2/(n+1)^2$ | §8 |
| (30) | Bootstrap SE (ISLP (5.8)) | §9 |
| (31)–(32) | $P(x^*_{(n)}=x_{(n)})=1-(1-1/n)^n\to1-e^{-1}=0.632$: **nonparametric bootstrap inconsistent for the max** | §10 |
| — | Parametric bootstrap: resample $U(0,\hat\theta_4)$; reproduces the plug-in SD | §11 |

### 1.6 · Gaussian linear regression → [[L01-06-gaussian-linear-regression]]

| Eq. | Statement | Where |
|---|---|---|
| (1)–(2) | Simple OLS; on standardised data the slope is $r_{xy}$ | §1 |
| (3)–(7) | $y=X\beta+\varepsilon$; normal equations $X'X\hat\beta=X'y$; $\hat\beta=(X'X)^{-1}X'y$ | §2 |
| (8) | $\text{RSS}(\beta)=\text{RSS}(\hat\beta)+\lVert X(\hat\beta-\beta)\rVert^2$: global minimum | §2 |
| (9)–(12) | $P=X(X'X)^{-1}X'$ symmetric, idempotent, $\text{tr}P=q$; $X'e=0$; $\text{RSS}=y'(I-P)y$; $e=(I-P)\varepsilon$ | §2.1 |
| (13)–(14) | $\hat\beta=\beta+(X'X)^{-1}X'\varepsilon$; $V(\hat\beta\mid X)=\sigma^2(X'X)^{-1}$ | §3 |
| (15)–(17) | Gaussian log-likelihood; $\hat\beta_{MLE}=\hat\beta_{ols}$; $\hat\sigma^2_{MLE}=\text{RSS}/n$ | §4 |
| (18)–(19) | $E(\text{RSS})=\sigma^2(n-q)$; unbiased $\hat\sigma^2=\text{RSS}/(n-q)$ | §4 |
| (20)–(21) | $R^2=1-\text{RSS}/\text{TSS}$; never falls when regressors are added | §5 |
| (22)–(23) | $\bar R^2=1-(1-R^2)\frac{n-1}{n-k-1}$ (W (6.21)–(6.22)); rises iff the added $\lvert t\rvert>1$ (group: $F>1$) | §5 |
| (24) | $C_p=\frac1n(\text{RSS}+2d\hat\sigma^2)$, $\text{AIC}=C_p/\hat\sigma^2$, $\text{BIC}=\frac1n(\text{RSS}+\log(n)d\hat\sigma^2)$ | §6 |
| (25) | Interaction model sizes $p_k=1+\sum_{j\le k}\binom{13}{j}$ | §7 |
| (26)–(27) | $E(\text{MSE}_{in})=\sigma^2(1-p/n)$, $E(\text{MSE}_{out})=\sigma^2(1+p/n)$: optimism $2p\sigma^2/n$ | §7 |
| (28) | Municipal abstention specification | §8 |
| W (4.41) | $F=\frac{(R^2_{ur}-R^2_r)/q}{(1-R^2_{ur})/(n-k-1)}$ (homoskedastic form) | §8.3 |
| (29) | HC1: $\frac{n}{n-q}(X'X)^{-1}\big(\sum e_i^2x_ix_i'\big)(X'X)^{-1}$ | §8.5 |

### 1.7 · AR, unit root, VAR → [[L01-07-ar-var-review]]

| Eq. | Statement | Where |
|---|---|---|
| Def. | Strict vs **weak** stationarity (constant mean, $\gamma_\ell$ depends on the lag only) | §1 |
| (1)–(2) | $\gamma_{-\ell}=\gamma_\ell$; $\rho_\ell=\gamma_\ell/\gamma_0$ and its sample version | §1–§2 |
| (3) | Ljung–Box $Q(m)=T(T+2)\sum_{\ell\le m}\hat\rho_\ell^2/(T-\ell)\stackrel a\sim\chi^2_m$ | §2 |
| (4) | Linear series: $\gamma_\ell=\sigma_a^2\sum_j\psi_j\psi_{j+\ell}$ | §3 |
| (5)–(9) | AR(1): $\mu=\phi_0/(1-\phi_1)$; MA($\infty$) weights $\phi_1^i$; $\gamma_0=\sigma_a^2/(1-\phi_1^2)$; **stationary iff $\lvert\phi_1\rvert<1$** | §4 |
| (10)–(11) | $\gamma_\ell=\phi_1\gamma_{\ell-1}$; $\rho_\ell=\phi_1^\ell$ | §4 |
| (12)–(13) | Conditional Gaussian likelihood = OLS of $r_t$ on $(1,r_{t-1})$; exact MLE adds $p(r_1)$ | §5 |
| (14)–(16) | $y_t\mid y_0\sim N\big(\mu+\phi^t(y_0-\mu),\ \sigma^2\frac{1-\phi^{2t}}{1-\phi^2}\big)\to N\big(\mu,\frac{\sigma^2}{1-\phi^2}\big)$: **equilibrium distribution** | §6 |
| (17) | Half-life $h=\ln0.5/\ln\lvert\phi\rvert$ | §6 |
| (18)–(19) | Random walk: $V(y_t)=t\sigma^2$; $E(y_{t+h}\mid y_t)=y_t$; $\text{Corr}(y_t,y_{t+h})=\sqrt{t/(t+h)}$ | §7 |
| (20)–(21) | AR(p) as a multiple regression; $\mu=\phi_0/(1-\sum\phi_i)$; $\hat\sigma_a^2=\sum\hat a_t^2/(T-2p-1)$ | §8 |
| (22) | VAR(1): $r_t=\phi_0+\Phi r_{t-1}+a_t$, $\text{Cov}(a_t)=\Sigma$; equation-by-equation OLS | §9 |
| — | Stationary iff all eigenvalues of $\Phi$ have modulus $<1$ | §9 |
| (23) | $\mu=(I-\Phi)^{-1}\phi_0$ | §9 |
| (24)–(25) | $\Gamma_0=\Phi\Gamma_0\Phi'+\Sigma$; $\text{vec}(\Gamma_0)=(I_{k^2}-\Phi\otimes\Phi)^{-1}\text{vec}(\Sigma)$ | §9 |
| (26) | $\Gamma_\ell=\Phi^\ell\Gamma_0$ | §9 |

### 1.8 · p-hacking and evidence → [[L01-08-p-hacking-evidence]]

| Eq. | Statement | Where |
|---|---|---|
| (1) | $P_{H_0}(p\le\alpha)=\alpha$ — for **one** pre-specified test | §2 |
| (2)–(3) | Independent tests: $P(\text{at least one rejection})=1-(1-\alpha)^m$ | §3 |
| (4) | Bonferroni: test at $\alpha/m$; family-wise rate $\le\alpha$ with no independence | §3 |
| (5)–(6) | $p=1-\Phi(1.8)$; the reversed test's $p=\Phi(-2.2)$ | §4 |
| (7)–(8) | $BF_{01}=\phi(1.8)/\phi(-2.2)=e^{0.8}$; $\log BF_{10}(x)=4x-8$ | §4 |
| (9)–(11) | $P(H_1\mid x)=1\big/\big(1+BF_{01}\,P(H_0)/P(H_1)\big)$ | §4–§5 |
| (12)–(13) | Prior odds needed for $P(H_1\mid x)=0.9$: $P(H_1)/P(H_0)=9\,BF_{01}$ | §5 |

---

## 2 · Every number and worked case

### 2.1 · Sampling rules (L01-01)

| Case | Numbers |
|---|---|
| $s=1$, $n=10$ | $\hat\theta=0.1$; $J(\hat\theta)=1000/9=111.1$; asymptotic se 0.095; Wald 95% $(-0.086,0.286)$ |
| | exact $E(s/N)=0.1\times2.302585/0.9=$ **0.256**, sd **0.281** (binomial: 0.100, 0.095) |
| | p-values for $H_0:\theta=0.5$ vs $<$: binomial $11/1024=$ **0.0107**; negative binomial $0.5^9=$ **0.0020** |
| $s=4$, $n=10$ | $\hat\theta=0.4$; se 0.155; Wald $(0.096,0.704)$; exact NegBin mean **0.461**, sd **0.178** |
| | p-values: binomial $386/1024=$ **0.377**; negative binomial $130/512=$ **0.254** |
| Uniform prior | Beta(2,10), mean **0.167**; Beta(5,7), mean **0.417** |
| Site Bernoulli code | $s=7$, $n=10$: Wald 90% (0.462, 0.938), 95% (0.416, 0.984), 99% (0.327, **1.073**); Beta(3,3) → Beta(10,6): mean **0.625**, sd 0.117, 95% (0.384, 0.837); logistic part: $\hat\alpha=2.877$, $\hat\beta=17.995$ (file's comments) |
| Sample size | $E=0.05$: $n\ge400$ with $z\approx2$; $n=385$ with $z=1.96$ ($384.1$); $E=0.01$: $10{,}000$ |

### 2.2 · Poisson MLE (L01-02)

| Case | Numbers |
|---|---|
| pmf | $\Pr(y=2\mid2)=$ **0.271**; $\Pr(y\le3\mid2)=$ **0.857**; $\Pr(y\le3\mid1)=0.981$; $\Pr(y=3\mid2)=0.18045$ (handwritten 0.181) |
| Efficiency of $s^2$, $\lambda=2$ | theory $V(s^2)$: 1.089, 0.203, 0.050 at $n=10,50,200$; efficiency **0.184, 0.197, 0.199** → **0.2** |
| Deck MC (slide 10) | $\bar y$ mean 2.003/1.994/1.998, var 0.193/0.038/0.011 (theory 0.200/0.040/0.010); $s^2$ var 1.245/0.187/0.051, efficiency 0.161/0.214/0.197 |
| ±0.25 coverage | deck MC 0.420/0.799/0.984; exact **0.424/0.789/0.987**; normal 0.424/0.789/0.988; Chebyshev bound −2.2/0.36/0.84 |
| Figure seeds | MC variances 0.182, 0.041, 0.011 (figure `L01-poisson-mle-sampling`) |

### 2.3 · Coal mining (L01-03)

| Case | Numbers |
|---|---|
| Data | $n=112$, $s=191$; first 40 years 125, first 41 years 127; 33 zero years; 20 years with $\ge4$ |
| 1851–1962 | $\hat\lambda=$ **1.705**, SE 0.123, CI (1.464, 1.947); $s^2=2.714$; $s^2/\bar y=1.592$; $D=176.7$, $p<0.001$ |
| 1851–1890 | **3.125**, SE 0.280, CI (2.577, 3.673); $s^2=2.574$; index 0.824; $D=32.1$, $p=0.774$ |
| 1891–1962 | **0.917**, SE 0.113, CI (0.696, 1.138); $s^2=1.063$; index 1.160; $D=82.4$, $p=0.168$ |
| Mixture | $V=1.705+1.120=2.825$; sample split $301.3=175.9+125.4$ |
| Fit of one rate | zeros 0.182 fitted vs 0.295 observed; $\ge4$: 0.094 vs 0.179 |
| Relative log-lik at 1.705 | $-18.92$ (1851–1890), $-15.81$ (1891–1962) |
| Profile at $\tau=1891$ | $n_1/n_2=41/71$, $\hat\lambda_1=3.098$, $\hat\lambda_2=0.901$, ratio **3.436**; $\ell_p=-54.055$; $\ell(\hat\lambda)=-89.049$ |
| LR | **69.99 ≈ 70.0**; at fixed $\tau=1890$: 69.47, $\chi^2_1$ $p\approx8\times10^{-17}$; $\chi^2_2$ tail at 70.0: $6\times10^{-16}$ |
| $w(\tau)$, 1885–1895 | 0.008, 0.091, 0.105, 0.038, 0.154, 0.194, **0.251**, 0.098, 0.039, 0.016, 0.007; 1889–1892 together **0.696**; normaliser 3.983 (rounded gaps) / 3.985 (exact) |
| Integrated, $a=1/2$ (G) | 0.008, 0.089, 0.104, 0.038, 0.153, 0.194, **0.251**, 0.099, 0.040, 0.017, 0.007 |

### 2.4 · First Bayesian example (L01-04)

| Case | Numbers |
|---|---|
| Prior $a=1/2$ | $E=2$, $V=4$, sd 2; central 95%: (0.051, 7.38) |
| 1851–1891, $n=41$, $s_n=127$ | posterior $G(128,41.5)$: mean $128/41.5=$ **3.084**, mode $127/41.5=$ **3.060**, sd $\sqrt{128}/41.5=$ **0.273**; MLE $127/41=$ **3.098** |
| Intervals | Wald (2.559, 3.636), SE 0.275; equal-tail posterior (2.573, 3.641) |
| Shrinkage | prior weight $0.5/41.5=0.01205$; $0.01205\times2+0.98795\times3.09756=3.08434$ |
| All 112 years | posterior mean $192/112.5=1.707$ vs MLE 1.705 |

### 2.5 · MSE and the bootstrap (L01-05)

| Case | Numbers |
|---|---|
| MSE in units of $\theta^2$ | $n=1$: all $1/3$; $n=2$: $7/24$, $1/6$, $1/6$, $1/8$; $n=3$: $10/36$, $1/10$, $1/9$, $1/15$; $n=10$: $31/120$, $1/66$, $1/30$, $1/120$ |
| $\theta=3$, $n=10$, theory | means 1.500, 2.727, 3.000, 3.000; SDs 0.274, 0.249, 0.548, 0.274; MSEs **2.325, 0.136, 0.300, 0.075** |
| Deck MC (slide 12) | means 1.497, 2.717, 2.994, 2.989; SDs 0.278, 0.264, 0.555, 0.290; MSEs 2.336, 0.149, 0.308, 0.084 |
| Limit of MSE($\bar x$) | $\theta^2/4=2.25$ |
| Best $c\,x_{(n)}$ (G) | $c^*=12/11=1.0909$; $\text{MSE}=9/121=0.0744<0.075$ |
| Bootstrap point mass | $n=10$: **0.651** (deck 0.666); $n=50$: 0.636 (0.622); $n=100$: 0.634 (0.632); limit **0.632** |
| Bootstrap SDs (slide 14) | $n=10$: 0.117, 0.062, 0.234, 0.068 vs theory 0.274, 0.249, 0.548, 0.274; $n=50$: 0.113, 0.041, 0.226, 0.042 vs 0.122, 0.058, 0.245, 0.059; $n=100$: 0.089, 0.036, 0.177, 0.036 vs 0.087, 0.029, 0.173, 0.030 |
| Parametric (slide 19) | $n=10$, $\hat\theta_4=2.568$: 0.237, 0.213, 0.475, 0.234 (plug-in 0.234, 0.213, 0.469, 0.234); $n=50$, 2.926: 0.119, 0.054, 0.238, 0.055; $n=100$, 3.029: 0.084, 0.031, 0.167, 0.032 |
| Weighted mean, $n=21$ | $\sum a_i^2=891/14641=0.0609$ vs $1/21=0.0476$; efficiency 0.78 |
| Median under $t_4$ | $f(0)=0.375$, asymptotic variance $1.78/n$ vs $2/n$ for $\bar x$; normal-case efficiency $2/\pi=0.64$; Beta(3,9) median 0.236 vs mean 0.25 |
| `bootstrap-example.html` | $\bar x=0.10006$, $\hat\sigma_{MLE}=0.9129307$; $t$ interval $[-0.15939,0.35951]$; $\sigma^2$ interval $[0.593,1.321]$ |
| B Table 1.1 (corrected) | MSE[$x_{(n)}$] $=\theta^2/66$ at $n=10$, $\theta^2/231$ at $n=20$; ratio column 0.36, 0.18, 0.059, 0.017 |

### 2.6 · Regression (L01-06)

| Case | Numbers |
|---|---|
| Houseprice ($n=128$) | size alone $R^2=31\%$, resid. SD 71.4; + brick 47%, 62.1; + neighbourhood **69%, 48.1**; $n/(n-6)=1.049$; $2^6=64$ (or $2^7=128$) subsets; $\log128=4.85$ |
| Wooldridge p. 181 | $R^2=0.30$, $n=51$, $k=10$ → $\bar R^2=0.125$; $R^2=0.10$ → $-0.125$ |
| Best-subset simulation (seed 128) | $R^2$ 0.337 → 0.644; $\bar R^2$ peaks at $d=5$ (0.627); $C_p$ picks $d=4$ (1.1356 vs 1.1361); BIC picks $d=3$ (1.211) |
| Boston overfitting | $p_k=14, 92, 378, 1093, 2380$; $R^2_{in}$ 0.7303 → 1.0000; $R^2_{out}$ 0.7469 → 0.0519; RMSE$_{out}$ 4.48 → 47.13 (×10.5) |
| Abstention, model (4) | persistence 0.684 (SE 0.009), $t=76.0$, CI [0.666, 0.702]; size dummies 0.069/0.439/0.960/1.140, $t=1.03/3.92/6.32/3.60$ |
| Abstention, tests | size: robust $F=13.22$ (UF), 10.84 (region); $R^2$-form 11.4, range [5.7, 17.1]; $F_{4,5531}$ 5% critical 2.37; UF vs region: 22 restrictions, $F=31.08$ / 32.09 |
| Abstention, fit | $R^2$ 0.682, 0.727, 0.755, 0.728, 0.757; $\bar R^2$ 0.754 → 0.756; model (0) at the means $=20.728$ |

### 2.7 · AR and VAR (L01-07)

| Case | Numbers |
|---|---|
| IBM returns | Ljung–Box $Q(30)=38.241$, $p=0.1437$; squared returns $Q(30)=182.12$, $p\approx10^{-23}$ |
| Wooldridge | $\phi=0.9$: $\text{Corr}(y_t,y_{t+5})=0.59049$; random walk $\sqrt{1000/1100}=0.9535$ |
| $\phi=0.9$, $\sigma=1$, $y_0=8$ | equilibrium variance **5.263** (sd 2.294); half-life **6.58**; at $t=10$: mean 2.79, variance 4.62; $\pm2$ sd band $\pm4.59$ |
| $\phi=0.5$ | half-life 1; equilibrium variance 1.333; band $\pm2.31$ |
| Tsay AR(3) | $\mu=0.0091/1.007=0.00904$ |
| Tsay Ex. 8.3 | eigenvalues 0.8, 0.5 (stationary although $\Phi_{22}=1.1$); $\mu=(1,2)'$; $\Gamma_0=\frac19\begin{pmatrix}25&20\\20&40\end{pmatrix}$; $\Gamma_1=\frac19\begin{pmatrix}11&16\\7&32\end{pmatrix}$; correlation 0.632 |

### 2.8 · p-hacking (L01-08)

| Case | Numbers |
|---|---|
| Family-wise rate | $m=1,5,10,32,162$: 0.050, 0.226, 0.401, **0.806**, 0.9998; Bonferroni $0.05/32=0.0016$ |
| $X=1.8$ | $p=$ **0.0359**; reversed $p=0.0139$; $BF_{01}=e^{0.8}=$ **2.2255** ($BF_{10}=0.449$); $P(H_1\mid x)=$ **0.310** |
| Prior odds needed | $9\times2.2255=$ **20.03** (deck 20.07); $P(H_1)=20/21=0.952$ |
| Disagreement band | $x\in(1.645,2)$: $p<0.05$ yet $BF_{10}<1$ |
| Replication (deck) | 36% psychology; 61% experimental economics; 62% *Nature/Science*; replicated effects ≈ 50% of originals |

---

## Links

Map: [[L01-00-map]] · Pitfalls: [[L01-10-pitfalls]] · Code: [[L01-11-python]] · Class 2 formulas:
[[../L02/L02-07-formulas|L02 §7]] · Scope: [[../../rules/09_course_program|rules/09]] · Course plan:
[[../../Map/class-plan#Class 1: Review of basic ingredients|Class 1]].
