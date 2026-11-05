---
tags: [notes, lecture-02, statistical-learning, formulas, reference]
date: 2026-10-19
status: taught
source: "Class 2 goals (Map/class-plan.md), site description and class note (Aula/COURSE.md), rules/06; every numbered equation of L02-01 … L02-06 with its source slide or page"
---

# Class 2 · Formulas — the exam specification mapped, every result, every number

> Prev: [[L02-06-gaussian-vs-poisson-regression]] · Next: [[L02-08-pitfalls]] · Map: [[L02-00-map]]

Equation numbers are **the section notes' own**: "01 (21)" is equation (21) of
[[L02-01-prediction-error-bias-variance]]. Unnumbered results are cited by section.

---

## 0 · The exam specification, mapped

Three sources state what Class 2 covers: the site's class title, the site's class note on the
motorcycle example ([[../../Aula/COURSE|Aula/COURSE]]), and the class goals in
[[../../Map/class-plan#Class 2: Introduction to statistical learning|Map/class-plan]]; the topic
pack [[../../rules/06_classificacao_validacao|rules/06]] adds the classification metrics. The exam
has no code, so each item is "derive it, compute it by hand, read it".

| # | Item (source) | Note, section | Be able to |
|---|---|---|---|
| 1 | *"Linear and log-linear regression modeling"* (site title) | [[L02-02-linear-log-linear-regression]] §2–§7 | read a coefficient in level-level, log-level, log-log, level-log form; exact vs approximate % (11)/(12); interactions (6) and quadratics (21)–(22) |
| 2 | *"Training and testing samples"* (site title); training vs test error (plan) | [[L02-01-prediction-error-bias-variance]] §6; [[L02-03-cross-validation-motorcycle]] §1, §4 | explain why training MSE (29) only falls; state its optimism (33) |
| 3 | *"Bias-variance trade-off"* (site title, plan) | [[L02-01-prediction-error-bias-variance]] §2–§5 | prove (6), (15), (20), (21); say what each term is random over; read the tanh table |
| 4 | *"Validation"* (site title); validation set (plan) | [[L02-03-cross-validation-motorcycle]] §4 | write (5); name its two drawbacks; read the 63-of-100 table |
| 5 | Replicated CV (plan; site class note) | [[L02-03-cross-validation-motorcycle]] §4, §6 | explain why 100 hold-out splits disagree (63/100) and 100 ten-fold runs barely do (99/100) |
| 6 | LOOCV (plan; site class note) | [[L02-03-cross-validation-motorcycle]] §5 | write (6); **derive the shortcut (7)** through (8)–(13); state when it fails; read (14) |
| 7 | 10-fold CV (plan; site class note) | [[L02-03-cross-validation-motorcycle]] §6 | write (15) and (16); explain the bias–variance ranking of hold-out, $k$-fold, LOOCV |
| 8 | Choose the polynomial order; "order 12 was the best" (site class note) | [[L02-03-cross-validation-motorcycle]] §2–§3, §6 | read adjusted $R^2$ and BIC (3); explain that every criterion lands on 12 and what that does *not* prove |
| 9 | *"bootstrap algorithm to obtain approximate confidence bands"* (site class note) | [[L02-03-cross-validation-motorcycle]] §7 | describe the pairs bootstrap, (17), the formula band (18), and why they differ under heteroskedasticity |
| 10 | Logistic regression (plan; syllabus topic 06) | [[L02-04-logistic-regression]] §2–§7 | (1)–(8) readings; **derive score (12), Hessian (13) and IRLS (16)–(17)**; plug-in probabilities; cut-off (19); deviance and LR tests |
| 11 | Performance metrics for classification (syllabus; rules/06: confusion matrix, ROC, AUC) | [[L02-04-logistic-regression]] §9; [[L02-05-discriminant-analysis]] §6, §11 | compute error, FPR, FNR, sensitivity, specificity, precision, FDR from a table; misallocation probabilities by $\Phi$; read a ROC curve |
| 12 | Discriminant analysis (plan) | [[L02-05-discriminant-analysis]] §2–§10 | Bayes and ML rules (2); $h(x)$ (4)–(8); the midpoint (9); the two Gaussian cut-offs; LDA (10)–(11); QDA (12); costs (14)–(15) |
| 13 | Gaussian vs Poisson regression for counts (plan) | [[L02-06-gaussian-vs-poisson-regression]] §2–§5 | write (2)–(4), solve the dummy case in closed form, compute SEs from the information, read $e^\beta$, check Var = mean, apply the $\hat\sigma$ correction |

---

## 1 · Every definition and result

### 1.1 · Prediction error and bias–variance → [[L02-01-prediction-error-bias-variance]]

| Eq. | Statement | Derived in |
|---|---|---|
| (1) | expected prediction error $E[(Y-\varphi(X))^2]$ | §2 |
| (2)–(5) | condition on $X$; minimise $g(t)=E[(Y-t)^2\mid X=x]$ pointwise: $g'(t)=0\iff t=E[Y\mid X=x]$, $g''=2>0$ | §2 |
| (6) | $\arg\min_\varphi E[(Y-\varphi(X))^2]=\psi(x)=E[Y\mid X=x]$ — **the regression function** | §2 |
| (7)–(9) | $R_{\text{pred}}(g)=R_{\text{reg}}(g)+E[V[Y\mid X]]$ (AME Teorema 1): predicting $Y$ and estimating $\psi$ are one problem | §2 |
| (10) | additive model $Y=\psi(X)+\varepsilon$, $E\varepsilon=0$, $\operatorname{Var}\varepsilon=\sigma^2$, all independent | §3 |
| (15) | $E[(Y-\hat\psi(x))^2\mid X=x]=\operatorname{EQM}[\hat\psi(x)]+\sigma^2$ — reducible + irreducible | §3 |
| (16) | integrated over $F_X$ | §3 |
| (17) | $\operatorname{Viés}=E\hat\psi(x)-\psi(x)$; $\operatorname{Var}=E[(\hat\psi(x)-E\hat\psi(x))^2]$, over training samples | §4 |
| (20) | $\operatorname{EQM}=\operatorname{Var}+\operatorname{Viés}^2$ | §4 |
| **(21)** | $E[(Y-\hat\psi(X))^2]=\int\operatorname{Viés}^2\,dF_X+\int\operatorname{Var}\,dF_X+\sigma^2$ | §4 |
| (23)–(24) | straight line on $1-x+2x^2$, $x\sim U(0,1)$: $\int\operatorname{Viés}^2=1/45$; $\overline{\operatorname{Var}}=\sigma^2\cdot2/n'$ (design held fixed) | §4.1 |
| (25) | the tanh world: $\psi(x)=45\tanh(x/1.9-7)+57$, $X\sim U(8,18)$, $\sigma=4$, $n=30$ | §5 |
| (27) | Monte Carlo estimators of bias² and variance (slide 25) | §5 |
| (28) | linear smoother: $E\hat\psi(x_0)=b(x_0)'(B'B)^{-1}B'\boldsymbol\psi$, $\operatorname{Var}=\sigma^2b(x_0)'(B'B)^{-1}b(x_0)$ | §5 |
| (29) | training MSE $\frac1n\sum(y_i-\hat\psi(x_i))^2$ | §6 |
| (32) | $E[\text{EQM}_{\text{train}}]=\|(I-H)\boldsymbol\psi\|^2/n+\sigma^2(1-\frac{d+1}n)$ (G) | §6 |
| (33) | optimism $=2\sigma^2(d+1)/n$ — the $C_p$/AIC penalty (G) | §6 |

### 1.2 · Coefficient readings → [[L02-02-linear-log-linear-regression]]

| Eq. | Statement | Derived in |
|---|---|---|
| (1) | level-level $\Delta y=\beta_j\Delta x_j$; rescaling $x$ by $c$ divides the slope by $c$ | §2 |
| (4) | $\bar R^2=1-(1-R^2)\frac{n-1}{n-k-1}$ | §2.1 |
| (6) | interaction: $\Delta y/\Delta x_2=\beta_2+\beta_3x_1$ — $\beta_2$ alone is the slope at $x_1=0$ | §3 |
| (8) | dummy × continuous: two slopes $\beta_2$, $\beta_2+\beta_3$; gap $\beta_1+\beta_3\,\text{yrs}$ | §3 |
| (9)–(10) | log-level: $\log y_1-\log y_0=\beta_1\Delta x$ | §4 |
| **(11)** | **exact** $\%\Delta y=100(e^{\beta_1\Delta x}-1)$ (W 6.8) | §4 |
| (12) | approximate $\%\Delta y\approx100\beta_1\Delta x$ (W 2.43); error $\approx100z^2/2$ | §4 |
| (13)–(15) | log-log: $\beta_1$ is the elasticity; $\%\Delta y\approx\beta_1\%\Delta x$; exact $100[(1+\%\Delta x/100)^{\beta_1}-1]$ | §5 |
| W Table 2.3 | level-log: $\Delta y=(\beta_1/100)\%\Delta x$ | §5 |
| (18) | standardised coefficient: $\partial\log y/\partial x_j=\beta_j^*s_y/s_{x_j}$ | §6 |
| (21)–(22) | quadratic slope $\hat\beta_1+2\hat\beta_2x$; turning point $|\hat\beta_1/(2\hat\beta_2)|$ | §7 |

### 1.3 · Validation, CV and the bootstrap → [[L02-03-cross-validation-motorcycle]]

| Eq. | Statement | Derived in |
|---|---|---|
| (1) | polynomial regression is linear in $\beta$ | §2 |
| (2) | standardising $ax+b$ ($a>0$) returns the standardised $x$ | §2 |
| (3) | $\bar R^2_d$; $\text{BIC}_d=\frac1n(\text{RSS}_d+\log(n)(d+1)\hat\sigma^2_d)$ | §3 |
| (5) | validation-set estimate $\frac1{|\mathcal V|}\sum_{\mathcal V}(y_i-\hat f_{\mathcal T}(x_i))^2$ | §4 |
| (6) | $CV_{(n)}=\frac1n\sum(y_i-\hat y_{(i)})^2$ | §5 |
| **(7)** | **$CV_{(n)}=\frac1n\sum\big(\frac{y_i-\hat y_i}{1-h_{ii}}\big)^2$ for least squares** (ISLP 5.2) | §5 |
| (8)–(9) | drop row $i$: $A-uu'$; Sherman–Morrison | §5 |
| (12) | $\hat\beta_{(i)}=\hat\beta-A^{-1}x_ie_i/(1-h_{ii})$ | §5 |
| (13) | left-out residual $=e_i/(1-h_{ii})$ | §5 |
| (14) | $\operatorname{Var}[CV_{(n)}]$: $n$ variances plus $n(n-1)$ large positive covariances | §5 |
| (15) | $CV_{(k)}=\frac1k\sum_j\text{MSE}_j$ (ISLP 5.3) | §6 |
| (16) | weighted $\widetilde{CV}_{(k)}=\sum_j\frac{n_j}{n}\text{MSE}_j$ (the site's code); equals (15) iff $n_j=n/k$ | §6 |
| (17) | bootstrap SE $\sqrt{\frac1{B-1}\sum_r(\hat f^{*r}(x)-\bar f^*(x))^2}$ (ISLP 5.8) | §7 |
| (18) | formula band $\hat f(x_0)\pm2\sqrt{\ell_0'\hat C\ell_0}$, $\hat C=\hat\sigma^2(X'X)^{-1}$ (ISLP 7.2) | §7 |
| — | $\sum_ih_{ii}=d+1$: average leverage $(d+1)/n$ | §5 |

### 1.4 · Logistic regression → [[L02-04-logistic-regression]]

| Eq. | Statement | Derived in |
|---|---|---|
| (1) | $\pi_i=e^{x_i'\beta}/(1+e^{x_i'\beta})=g(x_i'\beta)$ | §2 |
| (2)–(4) | $1-\pi_i=1/(1+e^{\eta_i})$; odds $=e^{\eta_i}$; **logit $=x_i'\beta$** | §2 |
| (5) | GLM: $E(y_i\mid x_i)=\pi_i$, $V=\pi_i(1-\pi_i)$, link = logit | §2 |
| (6) | odds ratio $e^{\beta_j}$ per unit of $x_j$, the same at every $x$ | §2.1 |
| (7)–(8) | $g'=g(1-g)$; partial effect $\beta_j\pi_i(1-\pi_i)\le\beta_j/4$ | §2.1 |
| (9)–(11) | likelihood; $\ell(\beta)=\sum[y_ix_i'\beta-\log(1+e^{x_i'\beta})]$ | §3 |
| **(12)** | **score $X'(y-\pi)$**; the intercept row gives mean $\hat\pi$ = share of ones | §3 |
| **(13)** | **Hessian $-X'WX$**, $W=\operatorname{diag}\{\pi_i(1-\pi_i)\}$: strictly concave | §3 |
| (14)–(15) | Newton–Raphson $\beta^{\text{new}}=\beta^{\text{old}}+(X'WX)^{-1}X'(y-\pi)$ | §4 |
| **(16)–(17)** | **IRLS: $\beta^{\text{new}}=(X'WX)^{-1}X'Wz$, $z_i=\eta_i+(y_i-\pi_i)/\{\pi_i(1-\pi_i)\}$** | §4 |
| (18) | the WLS objective $(z-X\beta)'W(z-X\beta)$ | §4 |
| — | $\widehat{\operatorname{Var}}(\hat\beta)=(X'\hat WX)^{-1}$; $z=\hat\beta_j/\text{SE}$ | §4 |
| (19) | probability cut-off $c$ ↔ covariate cut-off $x^*=(\operatorname{logit}c-\hat\beta_0)/\hat\beta_1$ | §5.2 |
| — | $LR=$ difference of deviances $\sim\chi^2_{\text{df}}$; McFadden $1-\ell_{ur}/\ell_0$ | §5.3 |
| (20)–(21) | plug-in vs posterior predictive (21 is Classes 3+4) | §6 |
| (22)–(23) | deviance residual; for 0/1 data $D=-2\ell(\hat\beta)$ | §7 |
| — | FNR $=FN/(FN+TP)$, FPR $=FP/(FP+TN)$, sensitivity, specificity, precision, **FDR $=FP/(FP+TP)$** | §9 |

### 1.5 · Discriminant analysis → [[L02-05-discriminant-analysis]]

| Eq. | Statement | Derived in |
|---|---|---|
| (1) | $P(y=k\mid x)=\pi_kp_k(x)/\sum_j\pi_jp_j(x)$ | §2 |
| **(2)** | **Bayes rule $\arg\max_k\pi_kp_k(x)$**; ML rule: equal priors | §2 |
| (3) | $P(\text{error})=\int[\phi_2\pi_1p_1+\phi_1\pi_2p_2]dx$ — minimised pointwise by (2) (AME Teorema 9) | §2.1 |
| (4)–(5) | $h(x)=\log p_1-\log p_2$; allocate to 1 iff $h(x)>\log(\pi_2/\pi_1)$ | §3 |
| (6) | $P(y=1\mid x)=g(h(x)+\log\frac{\pi_1}{\pi_2})$ | §3 |
| (7)–(8) | univariate Gaussians: $h$ quadratic, coefficients in $\mu_k,\sigma_k$ | §5 |
| (9) | equal variances: allocate to 1 iff $x<(\mu_1+\mu_2)/2$ (when $\mu_1<\mu_2$) | §5.1 |
| — | $p_{ij}$ by $\Phi$ over the regions | §6 |
| (10) | common $\Sigma$: ML rule = smallest Mahalanobis distance | §7 |
| **(11)** | **$h(x)=\alpha'(x-\bar\mu)$, $\alpha=\Sigma^{-1}(\mu_1-\mu_2)$** — linear | §7 |
| — | LDA posterior $g(\gamma_0+\alpha'x)$: the logit form, a different estimator | §7.1 |
| (12) | QDA: $\frac12\log\frac{|\Sigma_2|}{|\Sigma_1|}$ plus two class-specific quadratic forms | §8 |
| — | admissibility; all Bayes rules (ML included) are admissible | §9 |
| (13) | risk $R(d,k)=\sum_jc_{jk}p_{jk}$; Bayes risk $\sum_k\pi_kR(d,k)$ | §10 |
| **(14)** | **allocate to 1 iff $h(x)>\log\{\pi_2c_{12}/(\pi_1c_{21})\}$** | §10 |
| (15) | on the posterior scale: $P(y=1\mid x)>c_{12}/(c_{12}+c_{21})$ | §10 |
| — | equal-variance AUC $=\Phi\big((\mu_2-\mu_1)/\sqrt{2\sigma^2}\big)$ (G) | §11 |

### 1.6 · Gaussian vs Poisson regression → [[L02-06-gaussian-vs-poisson-regression]]

| Eq. | Statement | Derived in |
|---|---|---|
| (1) | Gaussian: $y_i=\beta_0+\beta_1w_i+\varepsilon_i$; with one dummy OLS = group means | §2 |
| (2) | Poisson: $\log\lambda_i=\alpha+\beta w_i$ | §3 |
| (3) | $\ell=\sum[y_i(\alpha+\beta w_i)-e^{\alpha+\beta w_i}-\log y_i!]$ | §3 |
| (4) | score $X'(y-\lambda)=0$ — the logit's shape; closed form $e^{\hat\alpha}=S_0/n_0$, $e^{\hat\alpha+\hat\beta}=S_1/n_1$ | §3 |
| — | information $\begin{pmatrix}S_0+S_1&S_1\\S_1&S_1\end{pmatrix}$: $\text{SE}(\hat\alpha)=1/\sqrt{S_0}$, $\text{SE}(\hat\beta)=\sqrt{1/S_0+1/S_1}$ | §3 |
| — | rate ratio $e^{\beta}$; exact % $100(e^\beta-1)$ | §4 |
| — | $\operatorname{Var}(y\mid x)=E(y\mid x)$; $\hat\sigma^2=\frac1{n-k-1}\sum\hat u_i^2/\hat y_i$; quasi-Poisson SE $\times\hat\sigma$ (W 17.35) | §5 |
| I (4.42) | GLM template $\eta(E[Y\mid X])=X'\beta$ (G) | §6 |

---

## 2 · Every number and worked case

### 2.1 · Note 01

| Case | Inputs | Result |
|---|---|---|
| tanh landmarks (26) | $x=8,\,13.3,\,18$ | $\psi=12.339,\ 57,\ 101.365$; slope at 13.3: $45/1.9=23.68$ |
| exact (21), polynomial OLS, 30 equispaced points, $\sigma=4$ | $d=1,3,5,6,7,10,15$ | test 91.83, 25.95, **19.81**, 20.03, 19.91, 21.38, 26.20; bias² 74.80, 7.98, 0.94, 0.70, 0.11, 0.007, 0.000; variance 1.03, 1.97, 2.87, 3.33, 3.80, 5.37, 10.20; training 93.87, 22.39, 13.79, 13.01, 11.85, 10.14, 7.47 |
| the optimum | | $d^*=5$; $0.94+2.87+16=19.81$; degrees 5–7 within 0.25 |
| the slide's spline (slide 27) | | about 7 df; prediction error bottoms near 20, floor 16 |
| optimism (33) | $d=5$, $n=30$, $\sigma^2=16$ | $2(16)(6)/30=6.4$ |
| line on $1-x+2x^2$ (§4.1) | $n'=900$, $\sigma=0.1$ | bias² $1/45=0.0222$; variance $0.01\cdot2/900=0.0000222$ — 1000× smaller |

### 2.2 · Note 02

| Case | Result |
|---|---|
| W units (2.39, 2.41) | slope 18.501 on `roe` → 1,850.1 on `roedec` |
| Credit (2), slide 44 | $t_{\text{Student}}=429.6/16.61=25.86$; $t_{\text{Cards}}=6.37$; $\bar R^2=0.9531$ |
| houseprice (5), slides 17, 29 | 1.886008 per m² → $0.092903\times1.886008=0.17522$ thousand R\$ per sqft = USD 54.75 |
| houseprice interactions, slide 29 | size effect 1.9375 / 2.2282 (brick) / 1.5760 (N2) / 1.8668 (both) |
| W Ex. 2.10, educ | 8.3% approx., **8.65%** exact |
| W (6.7), rooms ±1 | 30.6% approx.; **+35.8% / −26.4%** exact |
| W (6.7), stratio +1 / +5 | −5.2% / −26% approx.; −5.1% / −22.9% exact |
| W Ex. 2.11, sales +10% | 2.57% approx., **2.48%** exact |
| unemployment 8 → 9 | 1 point, 12.5%, 0.118 log points |
| Mroz page (19)–(20) | RSS $=735\times0.4511^2=149.57$; $R^2=0.8011$; $\bar R^2=0.7962$; $t_{\text{MTR}}=-21.64$; MLE SE factor $\sqrt{735/753}=0.98798$ |
| W (6.12), experience | turning point $0.298/0.0122=24.4$ years |
| W Ex. 6.2, rooms | turning point 4.4 rooms; +7.5% (5 → 6), +19.9% (6 → 7) |

### 2.3 · Note 03

| Case | Result |
|---|---|
| adjusted $R^2$ by order (slide 4) | 0.0769 (1), 0.1323 (2), 0.5259 (5), 0.6941 (8), 0.769 (10), 0.7686 (11), **0.7798 (12)**, 0.7688 (20) |
| $\hat\sigma^2$ at $d=12$ (4) | $1-0.7798=0.2202$; $\hat\sigma=0.4693$ |
| 100 hold-out splits (slide 7) | wins: 6:1, 8:2, 9:2, 10:15, 11:7, **12:63**, 13:10; orders 10–13: 95 |
| 10-fold × 100 (slide 10) | **12: 99**, 13: 1 |
| LOOCV minimum (slide 8) | $d=12$, about 0.48 on the "Root MSE" axis |
| leverage | mean $(d+1)/n$: $13/132=0.0985$ ($d=12$), $4/132=0.0303$ ($d=3$) |
| the site's folds | $\lfloor132/10\rfloor=13$: nine folds of 13, the last of 15 |
| fit sizes | hold-out ≈ 105, 10-fold ≈ 119, LOOCV 131 |
| bootstrap (slide 11) | $B=1000$ pairs resamples of the order-12 fit |
| stand-in (simulated, **not** mcycle) | at $d=12$: training 0.1737, hold-out 0.2220, LOOCV 0.2082, 10-fold 0.2117; 10-fold picks 12 in 82/100 runs, hold-out spreads (14: 31, 12: 30, 10: 23, 13: 10) |

### 2.4 · Note 04

| Case | Result |
|---|---|
| `default` counts | 9,667 no / 333 yes; mean $\hat\pi=0.0333$ |
| LPM (slide 13) | $-0.07519+0.0001299x$: negative below 578.8; 0.185 at 2000 |
| balance logit (slides 13, 15) | $-10.6513+0.0055x$ (SE 0.3612, 0.0002204; $z=-29.49$, 24.95); **0.58%** at 1000, **58.6%** at 2000 |
| odds ratio, partial effects | $e^{0.55}=1.733$ per USD 100; $\partial\pi/\partial x=0.001375$ at the cut-off, $0.0000315$ at 1000 (44×) |
| cut-offs (19), slide 17 | $c=0.1,\dots,0.9$: 1537, 1684, 1782, 1863, **1936.6**, 2010, 2091, 2189, 2336 |
| student table (slide 18) | 6850 / 2817 / 206 / 127; IRLS → **−3.50413, 0.40489** (SE 0.07071, 0.11502) in 6 iterations; $-2\ell=2908.683$; $\hat P$ **4.31%** / **2.92%**; OR 1.499 |
| balance + student (slide 20) | $-10.75+0.005738x-0.7149s$; **5.4%** (student) vs **10.5%** at 1500; cut-offs **1998.1** (student), **1873.5**; OR $e^{-0.7149}=0.489$ |
| deviances | null 2920.6; 1596.5 / 2908.7 / 1571.7; AIC 1600.5 / 2912.7 / 1577.7; LR 1324.1, 11.9, 24.8; McFadden 0.453, 0.004, 0.462 |
| spam `glm` (slides 36–38) | TN 1325, FP 80, FN 93, TP 803: error 7.52%, FNR 10.38%, FPR 5.69%, sensitivity 89.62%, specificity 94.31%, precision 90.94%, **FDR 9.06%** (slide's column 8.20%) |
| spam, other rows | ridge 8.17 / 14.29 / 4.27 / FDR 7.25; enet **6.52** / 10.49 / **3.99** / 6.53; lasso 6.65 / 10.60 / 4.13 / 6.75; bayes 7.39 / 10.16 / 5.62 / 8.94 |
| admission script | about one third admitted; MLE read off the figure ≈ $(-2.7,\,0.0027,\,0.6)$ (approximate) |

### 2.5 · Note 05

| Case | Result |
|---|---|
| Bernoulli (slide 43) | $h(0)=\log2=0.693$, $h(1)=\log\frac23=-0.405$; ML error $3/8$; Bayes rule switches at $\pi_1=1/3$ and $3/5$ |
| Gaussian, $\mu=(1,5)$, $\sigma=(6,2.5)$ (slide 46) | $h=0.066111x^2-0.772222x+1.110642$; cut-offs **1.680, 10.001**; $h(-20)=43.0$, $h(20)=12.1$; min $-1.144$ at 5.840 |
| misallocation (slide 50) | $p_{21}=0.3881$, $p_{12}=0.1148$, total **0.2515**; equal $\sigma=6$: cut-off 3, $p_{21}=p_{12}=$ **0.3694** |
| unequal costs, $c_{21}/c_{12}=2$ | threshold $\log\frac12$; cut-offs 3.228, 8.453; error 0.2855; expected cost 0.4095 vs 0.4455 for ML; ratio $>e^{1.144}=3.14$ empties $R_2$ |
| ISLP `default` LDA, cut-off 0.5 → 0.2 | missed 252 → 138 of 333; false alarms 23 → 235; error 2.75% → 3.73%; cost at 4:1, 1031 → 787 |
| iris, sepals (slide 54) | $|\hat\Sigma|=0.021122$; flower 51 → virginica (0.737), flower 101 → versicolor (2.506 vs 2.556), flower 1 → setosa; $\hat\alpha=(-7.800,12.081)$, score 7.738 |
| admission LDA/QDA (slides 58–65) | priors 0.3647, 0.3059, 0.3294; LDA posterior admit 0.5180, QDA 0.9227; apparent error 0.082 vs 0.035 |
| ROC | AUC 0.802 (unequal), 0.681 $=\Phi(0.4714)$ (equal); ML points (0.388, 0.885), (0.369, 0.631) |

### 2.6 · Note 06

| Case | Result |
|---|---|
| groups | weekday (Mon–Thu) 16 days, total 1744, mean **109.00**, var 147.73; "weekend" (Fri–Sun) 12 days, total 1000, mean **83.33**, var 130.42 |
| Gaussian | $\hat\beta_0=109$, $\hat\beta_1=-25.667$ (SE 4.525, $t=-5.67$); $s=11.85$, $s^2=140.4$; $R^2=0.553$ |
| Poisson | $\hat\alpha=\log109=$ **4.69135**, $\hat\beta=$ **−0.26850**; SE 0.02395, 0.03967; $z=-6.77$ |
| rate ratio | $e^{-0.26850}=0.7645$: **−23.5%**; $100\hat\beta=-26.85\%$ |
| fit and dispersion | deviance 38.324 on 26 df ($p=0.056$); null 85.141; LR 46.82; AIC 221.76; Pearson 37.546; $\hat\sigma^2=1.444$, $\hat\sigma=1.202$ |
| quasi-Poisson | SE 0.0477, $z=-5.63$; LR $46.82/1.444=32.4$ |

---

## 3 · Where these results come back

| Result | Next appearance |
|---|---|
| (21), MSE = variance + bias² | ridge/lasso and shrinkage priors (Classes 3+4); large BVAR (Class 9) |
| the logit likelihood (9)–(13), IRLS | Bayesian logit (Classes 3+4); probit, ordered and multinomial probit (Class 7) |
| the posterior predictive, note 04 (21) | Classes 3+4 |
| Bayes rule and loss, note 05 (13)–(15) | Bayes estimators and loss functions (Classes 3+4) |
| the Poisson GLM and overdispersion | zero-inflated Poisson (Classes 3+4); GLMs in Class 7 |
| confounding (the student sign flip) | omitted-variable bias, Classes 5+6 |

---

## Links

Map: [[L02-00-map]] · Pitfalls: [[L02-08-pitfalls]] · Code: [[L02-09-python]] · Class 1 formulas:
[[../L01/L01-09-formulas|L01-09]] · Rules: [[../../rules/06_classificacao_validacao|rules/06]].
