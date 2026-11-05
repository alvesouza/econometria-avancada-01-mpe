---
tags: [notes, lecture-03, formulas, reference, bayes, conjugacy, bayes-factor, monte-carlo, mcmc, shrinkage]
date: 2026-10-29
status: taught
source: "The ten section notes L03-01 … L03-10 (equation numbers are theirs); Classes 3+4 goals in Map/class-plan.md; the site's Classes 3+4 description in Aula/COURSE.md; every number re-checked by Notas/L03/L03_python_checks.py"
---

# Classes 3+4 · Formulas — the exam specification, every result, every number

> Prev: [[L03-10-sparsity-priors]] · Next: [[L03-12-pitfalls]] · Map: [[L03-00-map]]

Equations are cited by the **section note's own numbering**: "L03-03 (8)" is equation (8) of
[[L03-03-normal-measurement-physicists]]. Every number in §2 is asserted in [[L03-13-python]]
(script `L03_python_checks.py`).

---

## 0 · The exam specification, mapped

### 0.1 · The site's description (`Aula/COURSE.md`)

"Introduction to Bayesian learning: Prior, posterior, and predictive distributions; Sequential Bayesian
updating and conjugate analysis, Bayes factor, posterior model probability, model selection; Monte
Carlo & Markov Chain Monte Carlo methods; Sparsity in linear and log-linear models."

| # | Site item (verbatim) | Where it is settled |
|---|---|---|
| i | "Prior, posterior, and predictive distributions" | [[L03-01-bayes-rule-discrete]] §2–§3; [[L03-02-conjugate-sequential-updating]] §4; [[L03-03-normal-measurement-physicists]] §2–§3 |
| ii | "Sequential Bayesian updating and conjugate analysis" | [[L03-01-bayes-rule-discrete]] §4; [[L03-02-conjugate-sequential-updating]] §2–§6 |
| iii | "Bayes factor, posterior model probability, model selection" | [[L03-05-model-comparison-bayes-factors]] |
| iv | "Monte Carlo & Markov Chain Monte Carlo methods" | [[L03-06-monte-carlo-simulation]]; [[L03-07-markov-chains-gibbs]]; [[L03-08-metropolis-hastings-hmc]] |
| v | "Sparsity in linear and log-linear models" | [[L03-10-sparsity-priors]] (linear); the logit of [[L03-08-metropolis-hastings-hmc]] §6 is the log-linear (log-odds) case |

### 0.2 · The goals in `Map/class-plan.md`, item by item

| # | Goal | Note and section |
|---|---|---|
| 1 | prior × likelihood ∝ posterior | L03-01 §2 ((3), (6)) |
| 2 | the predictive distribution | L03-01 (4); L03-02 §4; L03-03 §2 |
| 3 | sequential updating (Beta–Bernoulli, Pareto–Uniform, discrete priors) | L03-01 §4, §7; L03-02 §3, §6 |
| 4 | conjugate analysis (normal with four priors, the physicists) | L03-02 §2, §5; L03-03 §3–§5 |
| 5 | Bayes estimators and loss functions | L03-04 §2–§9 |
| 6 | Bayes factors, posterior model probabilities, model selection | L03-05 §2–§8 |
| 7 | Monte Carlo and MCMC (Gibbs, MH, HMC/Stan) | L03-06; L03-07 §4–§8; L03-08 §2–§5, §8 (HMC named) |
| 8 | hierarchical Beta–Binomial and Gaussian models | L03-09 §4–§5 |
| 9 | sparsity priors (horseshoe, normal–gamma) | L03-10 §3–§7 |

**Final exam:** no code (`Map/class-plan.md`). Expect derivations of posteriors, predictives and full
conditionals, the reading of MCMC output, and Bayes-factor arithmetic.

---

## 1 · Definitions and results

### 1.1 · Bayes' rule and the predictive

| Result | Statement | Derived in |
|---|---|---|
| Bayes' rule (G (2.1)) | $p(\theta\mid x)=p(x\mid\theta)p(\theta)/p(x)$ | L03-01 (3) |
| Predictive (total probability) | $p(x)=\sum_kp(x\mid\theta_k)p(\theta_k)$ or $\int p(x\mid\theta)p(\theta)d\theta$ | L03-01 (4) |
| Proportional form (G (2.3)) | $p(\theta\mid x)\propto p(x\mid\theta)p(\theta)$ | L03-01 (6) |
| Sequential updating (G (3.1)) | $p(\theta\mid y_1,y_2)\propto f(y_2\mid y_1,\theta)\,p(\theta\mid y_1)$ | L03-01 (9) |
| Posterior odds | posterior ratio = likelihood ratio × prior ratio | L03-01 §6 |

### 1.2 · Conjugate families

| Data | Prior | Posterior | Posterior mean | Note |
|---|---|---|---|---|
| Bernoulli, $s_n$ in $n$ | Beta$(\alpha_0,\beta_0)$ | Beta$(\alpha_0+s_n,\beta_0+n-s_n)$ | $w\frac{\alpha_0}{\alpha_0+\beta_0}+(1-w)\bar x$, $w=\frac{\alpha_0+\beta_0}{\alpha_0+\beta_0+n}$ | L03-02 (4)–(6) |
| Poisson | Gamma$(\alpha_0,\beta_0)$ | Gamma$(\alpha_0+s_n,\beta_0+n)$ | $(\alpha_0+s_n)/(\beta_0+n)$ | L03-02 §5 |
| Exponential$(\theta)$ | Gamma$(\alpha_0,\beta_0)$ | Gamma$(\alpha_0+n,\beta_0+\sum x_i)$ | $(\alpha_0+n)/(\beta_0+\sum x_i)$ | L03-02 §5; L03-04 (12)–(13) |
| $U(0,\theta)$ | Pareto$(\theta_0,\alpha_0)$ | Pareto$(\max\{x_{(n)},\theta_0\},\alpha_0+n)$ | $\alpha_1\theta_1/(\alpha_1-1)$; median $\theta_12^{1/\alpha_1}$ | L03-02 (14)–(15) |
| $N(\theta,\sigma^2)$, $\sigma$ known | $N(\mu_0,\tau_0^2)$ | $N(w\mu_0+(1-w)x,\ w\tau_0^2)$, $w=\frac{\sigma^2}{\sigma^2+\tau_0^2}$ | precisions add: $\tau_1^{-2}=\sigma^{-2}+\tau_0^{-2}$ | L03-03 (5)–(8) |
| Normal regression | $N(\beta_0,\sigma^2B_0)\times IG$ | $\bar\beta=B_1(X'y+B_0^{-1}\beta_0)$, $B_1=(X'X+B_0^{-1})^{-1}$ | multivariate $t$ marginal | L03-03 §7 |

| Result | Statement | Note |
|---|---|---|
| Uniform-prior Beta | mode $=s_n/n=$ MLE; mean $(1+s_n)/(2+n)$; variance (8) | L03-02 (7)–(8) |
| Bernoulli predictive | $P(x_{n+1}=1\mid x)=(\alpha_0+s_n)/(\alpha_0+\beta_0+n)$ = posterior mean | L03-02 (11) |
| Normal predictive | $x\sim N(\mu_0,\sigma^2+\tau_0^2)$ | L03-03 (2) |
| Large samples | posterior $\approx N(\hat\theta,v/n)$ if $p(\hat\theta)\ne0$ | L03-02 (16) |
| $t$ prior influence | $\psi(\theta)=(\nu+1)(\theta-\mu_0)/(\nu s^2+(\theta-\mu_0)^2)$: bounded, $\to0$ | L03-03 (12) |

### 1.3 · Bayes estimators

| Loss | Bayes estimator | Note |
|---|---|---|
| $(\theta-a)^2$ | posterior mean; minimum expected loss $=V(\theta\mid x)$ | L03-04 (4)–(5) |
| $\lvert\theta-a\rvert$ | posterior median ($d\rho/da=2F-1$) | L03-04 (7)–(8) |
| 0–1 | posterior mode (MAP) | L03-04 (9)–(10) |
| bilinear $(a,b)$ | quantile $a/(a+b)$ | L03-04 (11) |
| Bayes risk | $r(\pi,d)=\int\rho(d(x)\mid x)g(x)dx$, minimised by the Bayes estimator | L03-04 (15)–(16) |
| Exp MLE bias | $E(n/\sum x_i)=n\theta/(n-1)$ | L03-04 (14) |
| Credible / HPD interval | $\int_{t_1}^{t_2}\pi(\theta\mid x)d\theta=1-\epsilon$; HPD = shortest, equal densities at the ends | L03-04 §10 |

### 1.4 · Model comparison

| Result | Statement | Note |
|---|---|---|
| Marginal likelihood (G (3.4)) | $m_i(y)=\int f_i(y\mid\theta_i)\pi_i(\theta_i)d\theta_i$ | L03-05 (3) |
| Posterior odds | $R_{12}=\frac{p_1}{p_2}B_{12}$, $B_{12}=m_1/m_2$; $P(M_1\mid y)=1/(1+(p_2/p_1)/B_{12})$ | L03-05 (4) |
| Michaela–Lila | $m_1=B(s_1+s_2+1,2m-s_1-s_2+1)$, $m_2=B(s_1+1,m-s_1+1)B(s_2+1,m-s_2+1)$ | L03-05 (5)–(6) |
| Large-sample | $\log B_{12}\approx\log LR-\frac{d_1-d_2}2\log n+O(1)$ | L03-05 (8) |
| Improper priors | $B_{12}$ scales by the arbitrary $c_1/c_2$ | L03-05 (9) |
| Model averaging | $f(y_f\mid y)=\sum_iP(M_i\mid y)f_i(y_f\mid y)$ | L03-05 (10) |

### 1.5 · Monte Carlo

| Result | Statement | Note |
|---|---|---|
| MC average, n.s.e. | $\bar g_M=\frac1M\sum g(X^{(i)})$, n.s.e. $=\sqrt{\widehat V/M}$ | L03-06 (1)–(2) |
| Hit-or-miss $\pi$ | se $=4\sqrt{p(1-p)/M}$, $p=\pi/4$ | L03-06 (3) |
| Inverse cdf | $F^{-1}(U)\sim F$; truncation $F^{-1}(F(c_1)+U[F(c_2)-F(c_1)])$ | L03-06 (4) |
| $t$ as scale mixture | $u\mid\lambda\sim N(0,\sigma^2/\lambda)$, $\lambda\sim G(\nu/2,\nu/2)$ ⟹ $u\sim t_\nu(0,\sigma^2)$ | L03-06 (5)–(6) |
| Accept–reject | accept if $u\le f/(cg)$; acceptance $1/c$ | L03-06 (7) |
| Importance sampling | $\frac1G\sum g(X)f(X)/h(X)$; self-normalised (10); variance needs heavy-tailed $h$ | L03-06 (9)–(11) |
| SIR | resample proposals with weights $\propto f/g$ | L03-06 §7 |
| ZIP MLE | $\hat\lambda/(1-e^{-\hat\lambda})=\sum y/(n-n_0)$, $\hat\pi=1-\bar y/\hat\lambda$ | L03-06 (14) |

### 1.6 · MCMC

| Result | Statement | Note |
|---|---|---|
| Invariant distribution | $\pi P=\pi$; $\pi(y)=\int\pi(x)p(x,y)dx$ | L03-07 (2), (4) |
| Ergodic average (Thm 6.3) | $\frac1n\sum f(X_m)\to E_\pi f$ | L03-07 (5) |
| Gibbs invariance | $\int f(y_1\mid x_2)f(y_2\mid y_1)f(x)dx=f(y)$ | L03-07 (7) |
| Normal mean/precision Gibbs | $h\mid\mu\sim G(\frac{\alpha_0+n}2,\frac{\delta_0+\sum(y_i-\mu)^2}2)$; $\mu\mid h\sim N(\frac{h_0\mu_0+hn\bar y}{h_0+hn},(h_0+hn)^{-1})$ | L03-07 (9)–(10) |
| Switch point | $\lambda_1\mid k\sim G(\alpha_0+S_k,\beta_0+k)$, $\lambda_2\mid k\sim G(\alpha_0+S_n-S_k,\beta_0+n-k)$, $P(k\mid\lambda)\propto e^{k(\lambda_2-\lambda_1)}(\lambda_1/\lambda_2)^{S_k}$; exact $P(k\mid y)$ (15) | L03-07 (13)–(15) |
| Gibbs on $N_2(0,\rho)$ | $x_1$ chain is AR(1) with $\rho^2$; $\rho_h=\rho^{2h}$; IF $=(1+\rho^2)/(1-\rho^2)$ | L03-07 (17)–(19) |
| Batch-means n.s.e. | $\sqrt{\frac1N\frac1{N-1}\sum(\bar Z_b-\bar Z)^2}$ | L03-07 (20) |
| Reversibility | $f(x)p(x,y)=f(y)p(y,x)$ ⟹ $f$ invariant | L03-08 (1) |
| MH acceptance (G (7.6)) | $\alpha=\min\{\frac{f(y)q(y,x)}{f(x)q(x,y)},1\}$; RW: $f(y)/f(x)$; independence: $\frac{f(y)/q(y)}{f(x)/q(x)}$ | L03-08 (4)–(6) |
| RW acceptance on $N(0,1)$ | $\frac2\pi\arctan(2/s)$ | L03-08 (9) |
| Gibbs = MH | $\alpha=1$ when the proposal is the full conditional | L03-08 (10) |

### 1.7 · Hierarchical models and sparsity

| Result | Statement | Note |
|---|---|---|
| Hierarchy (G (4.10)–(4.12)) | $y\sim f(y\mid\theta)$, $\theta\sim\pi(\theta\mid\theta_0)$, $\theta_0\sim\pi(\theta_0\mid\theta_{00})$; $\theta_0$ not identified | L03-09 (1) |
| Beta–Binomial marginal | $p(y_i\mid\mu,\eta)=\binom{n_i}{y_i}B(\mu\eta+y_i,(1-\mu)\eta+n_i-y_i)/B(\mu\eta,(1-\mu)\eta)$ | L03-09 (3) |
| Partial pooling | $E(p_i\mid\mu,\eta,y)=w_i\mu+(1-w_i)y_i/n_i$, $w_i=\eta/(\eta+n_i)$ | L03-09 (5) |
| Random coefficients | $(\alpha_i,\beta_i)\mid\cdot\sim N_2(m_i,V_i)$, $V_i=(A^{-1}+X_i'X_i/\sigma^2)^{-1}$ | L03-09 (8) |
| Ridge / lasso as MAP | $\lambda=\sigma^2/\tau^2$ (Gaussian prior); $\lambda=2\sigma^2/b$ (Laplace) | L03-10 (2)–(3) |
| Scale mixture | $\beta\mid\Psi\sim N(0,\Psi)$, $\Psi\sim G$ | L03-10 (4) |
| Normal–gamma | variance $2\lambda\gamma^2$, excess kurtosis $3/\lambda$ | L03-10 (5) |
| Horseshoe | $E(\theta\mid y)=(1-E(\kappa\mid y))y$; $\kappa\sim$ Beta(1/2, 1/2); $p(\kappa\mid y)\propto(1-\kappa)^{-1/2}e^{-\kappa y^2/2}$ | L03-10 (7)–(9) |

---

## 2 · Every number

| Quantity | Value | Note |
|---|---|---|
| Diego: $P(X=1)$; $P(\text{ill}\mid X=1)$ | 0.785; **0.8471** | L03-01 (7)–(8) |
| Diego: $P(\text{healthy}\mid X=0)$ | 0.8372 (slide: 0.8373) | L03-01 §3 |
| Diego: $P(Y=1\mid X=1)$; after $X,Y$; $Y$ alone | 0.8448; **0.9928**; 0.9830 | L03-01 (10)–(11) |
| Three coins: $P(HHH)$; posteriors | 0.618; **0.0674, 0.3932, 0.5394** | L03-01 (12) |
| Three coins after 4 heads; coin 3 after 10 | 0.0364, 0.3818, 0.5819; 0.741 | L03-01 §5 |
| Stone: chickenpox vs smallpox | 0.988 vs 0.011 (ratio ≈ 89) | L03-01 (13) |
| "Four candles" | 0.885 vs 0.115 | L03-01 §6 |
| G Fig. 2.2 posterior means | $5/14=0.357$; $17/54=0.315$ | L03-02 §2 |
| Pareto example (seeded) | $\theta_1=1.8923$, $\alpha_1=50.1$, mean 1.9308, median 1.9186, 90% (1.8942, 2.0089) | L03-02 §6 |
| Physicists A, B | $N(890,17.89^2)$, $N(840,35.78^2)$; $w=0.8$, $0.2$ | L03-03 §4 |
| Predictive sds A, B | 44.72, 89.44 | L03-03 §2 |
| C, D posterior means (medians) | 891.12 (892.41); 876.08 (884.30) | L03-03 §5 |
| Normal vs $t$ prior at $x=1100$ | 940.0 vs 1022.0 | L03-03 §6 |
| Beta(2,10): mode, median, mean | 0.100, 0.148, 0.167; min quadratic loss 0.0107 | L03-04 §7 |
| Beta(2,10) 95%: equal-tail, HPD | (0.0228, 0.4128), (0.0063, 0.3675) | L03-04 §10 |
| Bayes risk, $n=10$, uniform prior | $1/72=0.0139$ vs MLE $1/60=0.0167$ | L03-04 (18) |
| Table 3.2 | $-2.506,\dots,0.297$ ($m=10$); $-30.775,\dots,0.756$ ($m=100$) | L03-05 §4 |
| $m=10$, (2, 8): $\log_{10}m_1$, $\log_{10}m_2$ | $-6.5888$, $-5.3892$; BF $-1.200$; BIC $-1.024$ | L03-05 §4, §6 |
| $\hat\pi$ se at $M=1000$, $10^4$ | 0.0519, 0.0164 | L03-06 (3) |
| Accept–reject Beta(3,3) | $c=1.875$, acceptance 0.5333 | L03-06 §5 |
| Normal from Laplace | $c=1.3155$, acceptance 0.7602 (G prints 0.6577) | L03-06 (8) |
| Importance sampling target | 0.8302 (infinite-variance estimator) | L03-06 §6 |
| ZIP | $n=45$; MLE (4.223, 0.526); MM (7.159, 0.721) | L03-06 §7.2 |
| Correlation, uniform prior | 2.5/50/97.5%: 0.105, 0.567, 0.784 | L03-06 §7.1 |
| $P^{10}$; $\pi$ | (0.339, 0.661; 0.330, 0.670); (1/3, 2/3) | L03-07 §2 |
| Switch point | mode 1891, $P=0.240$; $E(\lambda_1\mid y)=3.106$, $E(\lambda_2\mid y)=0.930$ | L03-07 §6 |
| Inefficiency factors | 1.67, 9.5, 999.5 for $\rho=0.5,0.9,0.999$ | L03-07 (19) |
| Beta(3,4) independence MH | acceptance 0.5726 exact (G: 0.57); mean $3/7=0.4286$ | L03-08 §3 |
| RW acceptance at $s=2.38$ | 0.445 | L03-08 (9) |
| Site logit: GLM vs Bayes | $-11.304$/0.0596/4.055 vs $-10.82$/0.06/3.82 | L03-08 §6 |
| Hospitals: $\mu$ median; $E(\mu\mid y)$ | 0.0714 (Stan 0.0715); 0.0723 | L03-09 §4 |
| Pooled weight-gain OLS | $-4.526+0.476x$, sd 3.612; hierarchical $\sigma=1.10$ | L03-09 §5 |
| Shrinkage at $y=6$ | normal 3.00, Laplace 4.59, horseshoe 5.66 | L03-10 §5 |
| Vanguard risk ratios (SE) | MLE 10.63, horseshoe 1.07, BMA 1.00 | L03-10 §7 |
| NIR RMSE | normal–gamma 1.94 / 2.59 vs lasso 3.54 / 3.09 | L03-10 §7 |
