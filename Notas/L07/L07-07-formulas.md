---
tags: [notes, lecture-07, formulas, reference]
date: 2026-10-25
status: taught
source: "Class 7 goals (Map/class-plan.md), the three decks' outlines, rules/03 and rules/06; every numbered equation of L07-01 … L07-06 with its source slide or page"
---

# Class 7 · Formulas — the exam specification mapped, every result, every number

> Prev: [[L07-06-probit-ordered-multinomial]] · Next: [[L07-08-pitfalls]] · Map: [[L07-00-map]]

Equation numbers are **the section notes' own**: "03 (10)" is equation (10) of [[L07-03-ar1-errors]].

---

## 0 · The exam specification, mapped

Sources: the class goals in [[../../Map/class-plan#Class 7: More econometric models|Map/class-plan]], the outlines of
the three decks, and the topic packs [[../../rules/03_painel_did|rules/03]] and [[../../rules/06_classificacao_validacao|rules/06]].
The exam has no code: "derive it, compute it by hand, read it".

| # | Item (source) | Note, section | Be able to |
|---|---|---|---|
| 1 | GLM with general covariance (GLM3 outline) | [[L07-01-general-covariance-gls]] §2 | show $P\Omega P'=I$ gives (3); derive GLS (5); derive the conditionals (7)–(8) |
| 2 | Heteroskedastic errors, WLS/GLS (plan) | 01 §3–§4; W §8.4 | write (9)–(10); read W Table 8.1; write (11)–(12) and say why α needs MH; FGLS steps |
| 3 | Student-t errors, scale mixtures (plan; GLM3 Case II) | [[L07-02-student-t-errors]] §2–§4 | derive (3) from (1); write (4), (5), (6); compute prior probabilities of ν; state Geweke's conditions |
| 4 | Autoregressive errors (plan; GLM3 "parsimonious Ω") | [[L07-03-ar1-errors]] §1–§4 | derive (1)–(2); verify (3)–(4); quasi-difference (5)–(6); PW vs CO; derive (13); use (15) |
| 5 | Hierarchical / multilevel linear models, partial pooling (plan; HLM) | [[L07-04-hierarchical-linear-models]] §2–§6 | write (1)–(3); derive (5)–(6), (7), (8)–(10); compute (12)–(14) for a school; read the pregnancy outputs |
| 6 | Nutrition of pregnant women example (plan) | 04 §6 | read the pooled printout; explain the shrinkage figure; criticise the "predictive" band |
| 7 | Tobit (plan; LDV outline) | [[L07-05-tobit]] §1–§7 | likelihood (3)–(4); augmentation (5)–(6); conditionals (7)–(8); derive (9)–(12); slide 9's (13); (14) |
| 8 | Probit (plan; W §17.1; G §8.2.2) | [[L07-06-probit-ordered-multinomial]] §1–§2 | (1); identification; (2)–(3); Albert–Chib (4)–(5); read W Table 17.1 with scale factors |
| 9 | Ordered probit (plan; LDV slides 11–12) | 06 §3 | (6); identification; (7); derive (8) |
| 10 | Multinomial probit (plan; LDV slides 13–15) | 06 §4 | choice rule (9); SUR stacking; conditionals and (10); scale identification |
| 11 | Frequentist neighbours (plan: panel FE/RE note) | 04 §8 | (16) equicorrelation; (17) RE θ; FE = individual effects with a flat prior |

---

## 1 · Every definition and result

### 1.1 · General covariance → [[L07-01-general-covariance-gls]]

| Eq. | Statement | Source |
|---|---|---|
| (1) | $y=X\beta+\epsilon$, $\epsilon\sim N(0,\sigma^2\Omega)$ | GLM3 slide 3 |
| (2)–(3) | $P\Omega P'=I\Rightarrow\mathrm{Var}(P\epsilon)=\sigma^2I$: standard regression of $Py$ on $PX$ | slide 4 |
| (5) | $\hat\beta_{GLS}=(X'\Omega^{-1}X)^{-1}X'\Omega^{-1}y$, Var $=\sigma^2(X'\Omega^{-1}X)^{-1}$; $\Omega^{-1}=P'P$ | derived |
| (7) | $\sigma^2\mid\beta\sim IG(\nu_1/2,\nu_1s_1^2/2)$, $\nu_1=\nu_0+n$, $\nu_1s_1^2=\nu_0s_0^2+(y-X\beta)'\Omega^{-1}(y-X\beta)$ | slide 5 |
| (8) | $\beta\mid\sigma^2\sim N(\beta_1,V_1)$, $V_1^{-1}=V_0^{-1}+\sigma^{-2}X'\Omega^{-1}X$, $V_1^{-1}\beta_1=V_0^{-1}\beta_0+\sigma^{-2}X'\Omega^{-1}y$ | slide 5; G (8.2) |
| (9)–(10) | WLS: divide every column (constant too) by $\sqrt{h_i}$; minimise $\sum(y_i-x_i'\beta)^2/h_i$ | W (8.25)–(8.27) |
| (11)–(12) | $p(\alpha\mid\cdot)\propto p(\alpha)\prod h_i^{-1/2}e^{-e_i^2/(2\sigma^2h_i)}$; non-standard → MH | slide 7 |
| — | FGLS: $\log\hat u^2$ on $x$, $\hat h=\exp(\hat g)$, WLS with $1/\hat h$ | W (8.30)–(8.33) |

### 1.2 · Student-t errors → [[L07-02-student-t-errors]]

| Eq. | Statement | Source |
|---|---|---|
| (1)–(3) | $N(0,\sigma^2\omega)\times IG(\nu/2,\nu/2)$ integrated over ω = $t_\nu(0,\sigma^2)$ | slide 16; G p. 52 |
| (4) | $\omega_i\mid\cdot\sim IG\big(\frac{\nu+1}2,\frac{\nu+\epsilon_i^2/\sigma^2}2\big)$ | slide 18; G p. 115 |
| (5) | $E(\omega_i^{-1}\mid\cdot)=(\nu+1)/(\nu+\epsilon_i^2/\sigma^2)$ | derived |
| — | β, σ² conditionals: 01 (7)–(8) with $\Omega=\mathrm{diag}(\omega_i)$ | G p. 115 |
| (6) | $p(\nu\mid\omega)\propto[(\nu/2)^{\nu/2}/\Gamma(\nu/2)]^n\exp\{-[1/\nu^0+\frac12\sum(\ln\omega_i+\omega_i^{-1})]\nu\}$ → MH | slide 18 |
| — | $\nu\sim\mathrm{Exp}(\text{mean }\nu^0)$; flat β prior: posterior mean needs $P(\nu\le2)=0$, variance $P(\nu\le4)=0$ | slide 17 |

### 1.3 · AR(1) errors → [[L07-03-ar1-errors]]

| Eq. | Statement | Source |
|---|---|---|
| (1)–(2) | $\gamma_0=\sigma^2/(1-\rho^2)$; $\mathrm{Cov}(\epsilon_t,\epsilon_{t+k})=\rho^k\gamma_0$ | slide 22; W (12.27) |
| (3)–(4) | $\Omega_\rho^{-1}$ tridiagonal $(1,1+\rho^2,\dots,1;-\rho)$ $=P'P$, Prais–Winsten $P$ | derived |
| (5)–(6) | $\sqrt{1-\rho^2}y_1$; $y_t-\rho y_{t-1}=(x_t-\rho x_{t-1})'\beta+u_t$ | W (12.28)–(12.32) |
| (7)–(9) | large-$n$ OLS variance with $\phi$, naive variance, GLS variance | derived (G) |
| (10)–(11) | true/naive $=(1+\rho\phi)/(1-\rho\phi)$; OLS/GLS $=$ (10) $\times(1+\rho^2-2\rho\phi)/(1-\rho^2)$ | derived (G) |
| (12) | exact $p(\rho\mid\epsilon,\sigma^2)$, MH | slide 24 (corrected) |
| (13) | small sin: $\rho\sim N_{[-1,1]}(\rho_1,\bar V_\rho)$, $\bar V_\rho=(V_\rho^{-1}+\sigma^{-2}\tilde\epsilon'\tilde\epsilon)^{-1}$, $\rho_1=\bar V_\rho(V_\rho^{-1}\rho_0+\sigma^{-2}\tilde\epsilon'\epsilon)$ | slide 25 |
| (14)–(15) | $y=\mu+\sigma\Phi^{-1}(uB+(1-u)A)$ draws $N_{[a,b]}(\mu,\sigma^2)$ | slide 26 |

### 1.4 · Hierarchical models → [[L07-04-hierarchical-linear-models]]

| Eq. | Statement | Source |
|---|---|---|
| (1)–(3) | pooled $N(X_i\beta,\sigma^2I)$; individual effects $N(1_T\alpha_i+\tilde X_i\tilde\beta,\sigma^2I)$; random coefficients $N(X_i\beta_i,\sigma^2I)$ | HLM slides 4–6 |
| (4) | dummy design $X^*$ (individual effects, non-hierarchical prior) | slide 9 (corrected) |
| (5) | $\tilde V_\alpha^{-1}=V_\alpha^{-1}+\sigma^{-2}T$, $\tilde V_\alpha^{-1}\tilde\mu_{i\alpha}=V_\alpha^{-1}\mu_\alpha+\sigma^{-2}1_T'(y_i-\tilde X_i\tilde\beta)$ | slide 12 |
| **(6)** | $\tilde\mu_{i\alpha}=w\bar r_i+(1-w)\mu_\alpha$, $w=TV_\alpha/(TV_\alpha+\sigma^2)$ — **partial pooling** | derived |
| (7) | $\tilde V_\mu^{-1}=V_\mu^{-1}+NV_\alpha^{-1}$, $\tilde V_\mu^{-1}\mu_1=V_\mu^{-1}\mu_0+V_\alpha^{-1}\sum\alpha_i$; $V_\alpha$: IG with $\eta_0+N$, $\eta_0\sigma_0^2+\sum(\alpha_i-\mu_\alpha)^2$ | slide 13 (corrected) |
| (8)–(10) | $\beta_i$, $\beta_0$, $V_0^{-1}$ (Wishart) conditionals | slides 15–16 (corrected) |
| (11)–(15) | eight schools: $y_i\mid\mu,\tau\sim N(\mu,\sigma_i^2+\tau^2)$; $\hat\mu,V_\mu$; $B_i=\sigma_i^2/(\sigma_i^2+\tau^2)$; $E(\theta_i\mid y,\tau)=(1-B_i)y_i+B_i\hat\mu$; $p(\tau\mid y)$ | slide 23, derived |
| (16) | random intercept: Var $=\sigma_a^2+\sigma^2$, Cov $=\sigma_a^2$ | MS (6.28) |
| (17) | RE: $\theta=1-[\sigma_u^2/(\sigma_u^2+T\sigma_a^2)]^{1/2}$ | W (14.10) |

### 1.5 · Tobit → [[L07-05-tobit]]

| Eq. | Statement | Source |
|---|---|---|
| (1)–(4) | $\sigma^{-1}\phi((y-x'\beta)/\sigma)$ for $y>0$; $\Phi(-x'\beta/\sigma)$ for $y=0$; log-likelihood | slide 6; G p. 118; W (17.20)–(17.22) |
| (5)–(6) | augmented posterior; $y_i^*\sim TN_{(-\infty,0]}(x_i'\beta,\sigma^2)$ for zeros | slide 7; G (8.6), Alg. 8.2 |
| (7)–(8) | $\beta\mid\cdot\sim N(V_\beta(V_0^{-1}\beta_0+\sigma^{-2}X'y^*),V_\beta)$, $V_\beta^{-1}=V_0^{-1}+\sigma^{-2}X'X$; σ² IG on $y^*$ | slide 8 (corrected) |
| (9) | $E(y\mid y>0,x)=x'\beta+\sigma\lambda(x'\beta/\sigma)$ | W (17.24) |
| (10) | $E(y\mid x)=\Phi(z)x'\beta+\sigma\phi(z)$ | W (17.25) |
| (11) | $\partial E(y\mid y>0,x)/\partial x_j=\beta_j\{1-\lambda(z)[z+\lambda(z)]\}$ | W (17.26) |
| (12) | $\partial E(y\mid x)/\partial x_j=\beta_j\Phi(z)$ | W (17.30) |
| (13) | slide 9: $P(y=0)=\Phi(-2a/2.062)$ | slide 9 |
| (14) | normal $x$: OLS slope $=\beta P(y>0)$ | derived (Stein, G) |

### 1.6 · Probit family → [[L07-06-probit-ordered-multinomial]]

| Eq. | Statement | Source |
|---|---|---|
| (1) | $P(y=1)=\Phi(x'\beta)$; σ not identified → 1 | G (8.7)–(8.9); W (17.2), (17.6) |
| (2) | $\partial P/\partial x_k=\phi(x'\beta)\beta_k\le0.3989\beta_k$ | W (17.7); G p. 124 |
| (3) | $\beta^{logit}\approx1.6\beta^{probit}$ | G p. 128 |
| (4)–(5) | Albert–Chib: $y_i^*$ truncated at 0 by $y_i$; $\beta\sim N(B_1(X'y^*+B_0^{-1}\beta_0),B_1)$, $B_1=(X'X+B_0^{-1})^{-1}$ | G Alg. 8.3 |
| (6) | ordered: $P(y=j)=\Phi(\gamma_j-x'\beta)-\Phi(\gamma_{j-1}-x'\beta)$; $\gamma_1=0$ | slide 11 |
| (7)–(8) | $y_i^*\sim TN_{(\gamma_{j-1},\gamma_j]}$; $\gamma_j\sim U(\underline\gamma_j,\overline\gamma_j)$ | slide 12 |
| (9)–(10) | MNP: $y_{ij}^*=x_{ij}'\beta_j+\epsilon_{ij}$; choice = argmax (0 if all < 0); β normal, Ω inverse Wishart, $y_i^*$ truncated MVN | slides 13–15 |

---

## 2 · Every number and worked case

| Case | Inputs | Result | Note |
|---|---|---|---|
| W Ex. 8.6 | nettfa on inc, $n=2017$, weights $1/inc$ | OLS 0.821 (0.104), −10.57; WLS 0.787 (0.063), −9.58 (1.65); $R^2$ 0.0827 / 0.0709 | 01 §3 |
| GLS cost | $h=e^{x}$, normal design | Var OLS/GLS slope 4.38 | 01 §4.1 |
| Case I re-run | $n=100$, α = (1, 1), β = (2, 4) | β̄ = (2.20, 3.97), ᾱ = (0.93, 1.12), acceptance 0.55 | 01 §4 |
| Airline | slide 14 | β₂ 1.117, β₃ −0.504, β₄ 1.895, α₁ −3.968, α₂ 7.085 (3.293); $e^{-3.968}=0.0189$; $e^{0.7085}=2.03$ | 01 §5 |
| ν prior | Exp(25) | 0.3297, 0.2019 | 02 §4 |
| t re-run | slide 19 design + outlier | β̄ (0.43, 0.87, 1.93) vs OLS (0.54, 1.07, 2.03); ν̄ 3.8; outlier weight 0.018 | 02 §5 |
| Vella–Verbeek | G pp. 112–116 | β_U 0.129 (0.036) / 0.128 (0.033); σ² 0.165 / 0.105; log₁₀ BF 4.83 | 02 §6 |
| Barium | W Table 12.1 | OLS 3.12 (0.48); PW 2.94 (0.63), −37.08, ρ̂ 0.293, t −1.69; CO 2.95 | 03 §2 |
| AR ratios | ρ = 0.9 | φ = 0.9: true/naive 9.53; φ = 0: OLS/GLS 9.53 | 03 §3 |
| AR re-run | slide 27 design | β̄ (1.97, 4.06), σ̄² 1.03, ρ̄ 0.871 | 03 §5 |
| T §2.9 | interest rates | $r_3=0.832+0.930r_1$ ($R^2$ 96.5%); $c_3=0.792c_1$ | 03 §2 |
| Eight schools | slide 23 | pooled 7.87 (4.17); τ: mode 0, median 5.23, mean 6.59, 95% [0.24, 20.87]; A at τ = 5.2: μ̂ 8.027, B 0.8914, 10.24; Bayes A 11.64, C 6.35 | 04 §5 |
| Pregnancy | site Rmd | pooled −4.52639 (0.48680) + 0.47633 (0.01897)x, σ̂ 3.612, $R^2$ 0.5974; individual means −4.412, 0.470; Gibbs α −4.363, β 0.4687, σ_y 1.119, σ_α 3.210, σ_β 0.1253; woman 1 at 40.143: 17.68 [15.68, 19.86] | 04 §6 |
| Weights | T = 6 | w = 0.980; RE θ = 0.859 | 04 §6, §8 |
| MS calves | (6.27)/(6.28) | α̂ 69.9, β̂ 4.7; SE 7.8 → 5.6, 0.4 → 0.1 | 04 §8 |
| G panel | Table 9.5 | β_U 0.090 (0.006, 0.179); experience 0.058 | 04 §8 |
| Slide 9 | β = 2, σ² = 0.25 | P(y = 0) 0.500, 0.249, 0.104; OLS slopes 1.00, 1.50, 1.79 | 05 §6 |
| Mroz Tobit | W Table 17.3 | educ 80.65 (21.58), kidslt6 −894.02 (111.88), σ̂ 1122.02, ℓ −3819.09; APE 0.589 → 47.5; PEA 0.645; OLS 28.76 | 05 §7 |
| G Mroz | Table 8.1 | P(0 hours) 0.431 vs 0.328; mean 214 vs 587 h | 05 §7 |
| Truncated OLS | slide 9 design | slope 1.902 | 05 §8 |
| Mroz probit/logit | W Table 17.1 | educ 0.131 / 0.221; ℓ −401.30 / −401.77; scale 0.391 / 0.243 = 1.61; APE 0.301 | 06 §2 |
| G computer | Table 8.2 | −0.705, 0.879, 0.524; priors −1.2816, 0.1492, 1.0616, 0.0225, 1.0283 | 06 §2 |
| Ordered re-run | γ = (0, 1, 2) | β̄ (0.50, 0.89), γ̄₂ 1.10, γ̄₃ 2.08; lag-1 corr 0.99 | 06 §3 |
| MNP re-run | Ω known | (0.45, 1.10, −0.11, −0.71) vs (0.3, 1.0, −0.2, −0.8) | 06 §4 |
| Rubinfeld MVP | G Table 9.4 | β₂₂ 1.113, β₂₃ −1.437, σ₁₂ 0.085 | 06 §5 |
| MS inhibin | (6.29) | −2.310 (0.947), 0.026 (0.009); OR 1.026 per unit | 06 §6 |
