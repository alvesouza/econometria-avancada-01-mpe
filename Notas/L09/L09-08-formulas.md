---
tags: [notes, lecture-09, formulas, reference, var, irf, fevd, svar, bvar, minnesota, factor-model, favar, tvp-var, kalman, dcc, fsv]
date: 2026-10-25
status: taught
source: "The seven section notes L09-01 … L09-07 (equation numbers are theirs); Class 9 goals in Map/class-plan.md; the site's Class 9 description in Aula/COURSE.md; every number re-checked by Notas/L09/L09_python_checks.py and figures/make_figures.py"
---

# Class 9 · Formulas — the exam specification, every result, every number

> Prev: [[L09-07-fsv-dcc-covariances]] · Next: [[L09-09-pitfalls]] · Map: [[L09-00-map]]

Equations are cited by the **section note's own numbering**: "L09-02 (8)" is equation (8) of
[[L09-02-vma-irf-fevd]]. Every number in §2 is asserted in [[L09-10-python]] (script
`L09_python_checks.py`) or in `figures/make_figures.py`.

---

## 0 · The exam specification, mapped

### 0.1 · The site's description of Class 9 (`Aula/COURSE.md`)

"Introduction to multivariate time series econometrics", six items:

| # | Site item (verbatim) | Where it is settled |
|---|---|---|
| i | "Factor SV models" | [[L09-05-factor-models-favar]] §1–§3 (factor algebra); [[L09-07-fsv-dcc-covariances]] §5–§6 |
| ii | "Dynamic Conditional Correlation (DCC) models" | [[L09-07-fsv-dcc-covariances]] §3–§4, §7 |
| iii | "Vector autoregressive (VAR) models, impulses-response function, structural VAR (SVAR)" | [[L09-01-var-p-estimation-forecasting]]; [[L09-02-vma-irf-fevd]]; [[L09-03-structural-var]] |
| iv | "Large BVAR, Factor-augmented VAR (FAVAR)" | [[L09-04-bvar-minnesota-ssvs]] §6; [[L09-05-factor-models-favar]] §4 |
| v | "Time-varying parameter (TVP)-VAR" | [[L09-06-tvp-var-sv-state-space]] §3–§6 |
| vi | "Bayesian VAR (BVAR) and Bayesian FAVAR (BFAVAR)" | [[L09-04-bvar-minnesota-ssvs]] §2–§5; [[L09-05-factor-models-favar]] §3–§4 |

### 0.2 · The class plan's goals (`Map/class-plan.md`, Class 9)

| Goal | Note |
|---|---|
| VAR estimation | L09-01 §3–§4, §7 |
| impulse responses | L09-02 §1–§3 |
| structural VAR | L09-03 |
| large Bayesian VAR (Minnesota-type shrinkage) | L09-04 |
| factor-augmented VAR | L09-05 §4 |
| time-varying-parameter VAR with SV | L09-06 §2–§3 |
| factor stochastic volatility | L09-07 §5 |
| DCC vs FSV for time-varying covariances | L09-07 §4, §7 |

The final exam has no coding: expect derivations (OLS = MLE for a VAR, $\Psi_s$ recursion, FEVD at
$h=1$, the Minnesota posterior, $\Omega=\beta\beta'+\Sigma$, the Kalman update, DCC reversion) and the
reading of printed output (VARorder, FEVdec, dccFit).

---

## 1 · Definitions and results

### 1.1 · VAR(p) (L09-01)

| # | Statement | Note |
|---|---|---|
| VAR(p) | $y_t=\mu+B_1y_{t-1}+\dots+B_py_{t-p}+u_t$, $u_t\sim N(0,\Sigma)$ i.i.d. | L09-01 (1) |
| Mean | $m=(I-B_1-\dots-B_p)^{-1}\mu$ | L09-01 (2) |
| Regression form | $y_t=Bx_t+u_t$; $Y=XB'+U$, $U\sim N(0,I_n,\Sigma)$; $\mathrm{vec}(Y)=(I_q\otimes X)\beta+u$, $u\sim N(0,\Sigma\otimes I_n)$ | L09-01 (3)–(5) |
| OLS = MLE | $S(B)=S(\hat B)+(\hat B-B)X'X(\hat B-B)'$ ⇒ $\hat B'=(X'X)^{-1}X'Y$ for every $\Sigma$; $\tilde\Sigma=S(\hat B)/n$ | L09-01 (9)–(11) |
| GLS = OLS | same regressors in every equation ⇒ $\hat\beta_{GLS}=(I_q\otimes(X'X)^{-1}X')y$ | L09-01 (12) |
| Sampling covariance | $\mathrm{Cov}(\hat\beta)=\Sigma\otimes(X'X)^{-1}$ | L09-01 (13) |
| Companion form | $Y_t=AY_{t-1}+U_t$, first block row $(B_1,\dots,B_p)$, identities below | L09-01 (14) |
| Stationarity | all eigenvalues of $A$ inside the unit circle ⇔ all roots of $\lvert I-B_1z-\dots-B_pz^p\rvert=0$ outside; $\det(\lambda I-A)=\lambda^{qp}\det(I-B_1\lambda^{-1}-\dots)$ | L09-01 (15) |
| Forecast | $y_t(h)=JA^hY_t$; $e_t(h)=\sum_{i<h}\Psi_iu_{t+h-i}$; $\mathrm{MSE}(h)=\sum_{i<h}\Psi_i\Sigma\Psi_i'$ | L09-01 (16)–(18) |
| Bayesian forecast | $\int F(A,y_t,h)\,p(B,\Sigma\mid\text{data})$, $F$ nonlinear in $B$ | L09-01 (19) |
| Order selection | $M(i)=-(T-k-i-\frac32)\ln(\lvert\tilde\Sigma_i\rvert/\lvert\tilde\Sigma_{i-1}\rvert)\sim\chi^2_{k^2}$; AIC/BIC/HQ with penalties $2k^2i/T$, $k^2i\ln T/T$, $2k^2i\ln\ln T/T$ | L09-01 (20)–(21) |

### 1.2 · Impulse responses and FEVD (L09-02)

| # | Statement | Note |
|---|---|---|
| VMA(∞) | $y_t=\sum_i\Psi_iu_{t-i}$, $\Psi_0=I$, $\Psi_s=\sum_{i=1}^pB_i\Psi_{s-i}$ | L09-02 (1)–(3) |
| IRF | $\partial y_{t+s}/\partial u_t'=\Psi_s$; $(i,j)$ = response of $i$ to a shock in $j$ | L09-02 (4) |
| Orthogonalised IRF | $\Sigma=PP'$ (lower Cholesky), $\varepsilon_t=P^{-1}u_t\sim N(0,I)$, $\Theta_s=\Psi_sP$, $\Theta_0=P$ | L09-02 (5)–(6) |
| FEVD | $\omega_{ij}(h)=\sum_{s<h}\Theta_s(i,j)^2/\sum_k\sum_{s<h}\Theta_s(i,k)^2$; $\omega_{21}(1)=\rho_{21}^2$ | L09-02 (7)–(8) |

### 1.3 · Structural VAR (L09-03)

| # | Statement | Note |
|---|---|---|
| SVAR | $A_0y_t=A_1y_{t-1}+\dots+u_t$, $u_t\sim N(0,I)$ | L09-03 (1) |
| Reduced form | $B_i=A_0^{-1}A_i$, $\Sigma=(A_0'A_0)^{-1}$; structural IRF $\Psi_sA_0^{-1}$ | L09-03 (3)–(5) |
| Observational equivalence | $(QA_0,QA)$, $Q$ orthogonal, gives the same $(B,\Sigma)$ | L09-03 (6)–(7) |
| Order condition | $q^2-q(q+1)/2=q(q-1)/2$ restrictions | L09-03 (8) |
| Exact identification | unique $(A_0,A)\in R$ with $g(A_0,A)=(B,\Sigma)$ for almost every $(B,\Sigma)$ (slide 34) | L09-03 §3 |
| Recursive = Cholesky | $A_0$ lower triangular ⇒ $A_0^{-1}=P$, structural IRF $=\Theta_s$ | L09-03 (9) |

### 1.4 · Bayesian VAR (L09-04)

| # | Statement | Note |
|---|---|---|
| Minnesota prior | mean: own lag 1 = 1, else 0; $\mathrm{Var}(B_k(i,i))=\lambda^2/k^2$, $\mathrm{Var}(B_k(i,j))=\theta^2\lambda^2\sigma_i^2/(k^2\sigma_j^2)$; $\Sigma$ diagonal, known | L09-04 (1)–(2) |
| Posterior | $\bar V_i=(V_{i0}^{-1}+X'X/\sigma_i^2)^{-1}$, $\bar\beta_i=\bar V_i(V_{i0}^{-1}\beta_{i0}+X'y^{(i)}/\sigma_i^2)$; $\lambda\to0$: prior; $\lambda\to\infty$: OLS | L09-04 (7)–(8) |
| Scalar weight | $\bar b=wb_0+(1-w)\hat b$, $w=\mathrm{Var}(\hat b)/(\mathrm{Var}(\hat b)+v_0)$ | L09-04 (9) |
| Diffuse prior | $\mathrm{vec}(B')\mid\Sigma,Y\sim N(\mathrm{vec}(\hat B'),\Sigma\otimes(X'X)^{-1})$; $\Sigma\mid Y\sim IW(S(\hat B),n-k)$ | L09-04 (11)–(12) |
| Normal-Wishart | $\gamma\mid\Psi\sim N(\tilde\gamma,\Psi\otimes\tilde\Omega)$ forces $\theta=1$ | L09-04 §4 |
| ON/OFF switch | $\gamma_j\mid\cdot\sim\mathrm{Bernoulli}(A_j/(A_j+B_j))$ | L09-04 (13) |
| SSVS | $\beta_j\mid\gamma_j\sim(1-\gamma_j)N(0,\tau_{0j}^2)+\gamma_jN(0,\tau_{1j}^2)$; $P(\gamma_j=1\mid\beta_j)$ by Bayes | L09-04 (14)–(15) |

### 1.5 · Factor models and FAVAR (L09-05)

| # | Statement | Note |
|---|---|---|
| Model | $y_t\mid f_t\sim N(\beta f_t,\Sigma)$, $f_t\sim N(0,I_k)$, $\Sigma$ diagonal | L09-05 (1) |
| Covariance | $\Omega=\beta\beta'+\Sigma$; $\mathrm{var}(y_{it})=\sum_l\beta_{il}^2+\sigma_i^2$, $\mathrm{cov}=\sum_l\beta_{il}\beta_{jl}$ | L09-05 (2)–(3) |
| Rotation | $(\beta P',Pf_t)$ observationally equivalent; block lower triangular $\beta$, $\beta_{ii}>0$ | L09-05 (4) |
| Bound on $k$ | $m(k+1)-k(k-1)/2\le m(m+1)/2$ ⇔ $k\le(2m+1-\sqrt{8m+1})/2$ | L09-05 (5)–(7) |
| Factor scores | $f_t\mid y_t\sim N(V_f\beta'\Sigma^{-1}y_t,V_f)$, $V_f=(I_k+\beta'\Sigma^{-1}\beta)^{-1}$ | L09-05 (9) |
| FAVAR | $y_t\mid\cdot\sim N(\sum B_iy_{t-i}+\sum A_if_{t-i},\Sigma)$, $x_t\mid f_t\sim N(\beta f_t,\Omega)$ | L09-05 (10) |
| RMSFE | $\sqrt{N_h^{-1}\sum_t(y_{i,t+h}-\tilde y_{i,t+h,j})^2}$ | L09-05 (11) |

### 1.6 · Time-varying VARs and the Kalman filter (L09-06)

| # | Statement | Note |
|---|---|---|
| VAR-GARCH | $\mathrm{vech}(\Sigma_t)=\alpha_0+\sum A_i\mathrm{vech}(\Sigma_{t-i})+\sum\Gamma_i\mathrm{vech}(u_{t-i}u_{t-i}')$ | L09-06 (1) |
| VAR-SV (Uhlig) | $\Sigma_{t+1}^{-1}=L_t\Theta_tL_t'/\lambda$, $\Theta_t\sim B_q((\nu+pq)/2,1/2)$; scalar martingale iff $\lambda=(\nu+p)/(\nu+p+1)$ | L09-06 (2)–(3) |
| TVP-VAR-SV (Primiceri) | $\Sigma_t=A_t^{-1}D_tA_t^{-1\prime}$; random walks for $B_t$, $\alpha_t$, $\log\sigma_t$ | L09-06 (4)–(6) |
| Local level | $y_t=\mu_t+e_t$, $\mu_{t+1}=\mu_t+\eta_t$ | L09-06 (7) |
| Kalman filter | $v_t=y_t-\mu_{t\mid t-1}$, $V_t=\Sigma_{t\mid t-1}+\sigma_e^2$, $K_t=\Sigma_{t\mid t-1}/V_t$, $\mu_{t\mid t}=\mu_{t\mid t-1}+K_tv_t$, $\Sigma_{t\mid t}=\Sigma_{t\mid t-1}(1-K_t)$, $\Sigma_{t+1\mid t}=\Sigma_{t\mid t}+\sigma_\eta^2$ | L09-06 (8)–(12) |
| Steady state | $p^*=(q+\sqrt{q^2+4q})/2$, $K^*=p^*/(p^*+1)$, $q=\sigma_\eta^2/\sigma_e^2$; $\theta_{\mathrm{ARIMA}(0,1,1)}=1-K^*$ | L09-06 (13)–(14) |
| TVP regression | $\mathrm{Var}(\beta_t\mid\beta_0)=t\Omega$; Greenberg's Gibbs (17) | L09-06 (16)–(17) |
| Discounting | $V_t=(\delta^{-1}-1)P_{t-1\mid t-1}$ | L09-06 (18) |

### 1.7 · Multivariate volatility (L09-07)

| # | Statement | Note |
|---|---|---|
| EWMA | $\hat\Sigma_t=(1-\lambda)a_{t-1}a_{t-1}'+\lambda\hat\Sigma_{t-1}$ | L09-07 (1)–(2) |
| Correlation split | $\Sigma_t=D_tR_tD_t$ | L09-07 (3) |
| Tse–Tsui DCC | $R_t=(1-\theta_1-\theta_2)\bar R+\theta_1R_{t-1}+\theta_2\Psi_{t-1}$ | L09-07 (4) |
| Engle DCC | $Q_t=(1-\theta_1-\theta_2)\bar Q+\theta_1\varepsilon_{t-1}\varepsilon_{t-1}'+\theta_2Q_{t-1}$, $R_t=J_tQ_tJ_t$ | L09-07 (5) |
| Reversion | $E(Q_{t+h}\mid F_t)-\bar Q\approx(\theta_1+\theta_2)^{h-1}(Q_{t+1}-\bar Q)$; half-life $\ln0.5/\ln(\theta_1+\theta_2)$ | L09-07 (6) |
| FSV | $y_t\mid f_t\sim N(\beta f_t,\Sigma_t)$, $f_t\sim N(0,H_t)$, AR(1) log-variances; $\mathrm{Var}(y_t)=\beta H_t\beta'+\Sigma_t$ | L09-07 (7)–(10) |
| FSV correlation | $\rho_{ij,t}=\mathrm{sign}(\beta_i\beta_j)/\sqrt{(1+a_{it}/h_t)(1+a_{jt}/h_t)}$, increasing in $h_t$ | L09-07 (11)–(12) |

---

## 2 · Every number

| Number | What it is | Note |
|---|---|---|
| 0.9099; 0.5329 | largest companion moduli, slide-13 VAR(2) | L09-01 §5.1 |
| $\lvert\Phi(1)\rvert=0.032$; $m=(6.875,14.375,30.94)$ | slide-13 VAR(2), if $\mu$ is the intercept | L09-01 §5.1 |
| 0.6107 | largest companion modulus, UK/US/CA VAR(3) | L09-01 §5.2 |
| 0.4308, 0.4380, 0.4887 | $\hat B_1$ entries (UK own; UK→US; US→CA) | L09-01 §4.4 |
| 1.0908 / 0.4280; 7.0436 / 5.5454 | Tsay VAR(1) mean = 6-step forecast; forecast-sd limits | L09-01 §6.1 |
| AIC → 2, BIC → 1, HQ → 1; $M(3)=10.49$ (p 0.31) | VARorder on the GDP data | L09-01 §7.1 |
| 15, 610, 25,807; 301 | parameter counts (slides 45, 27) | L09-01 §8 |
| $\Psi_2(1,1)=0.2495$ | VAR(3) | L09-02 §2.1 |
| $\Theta_1=(0.3088,0.6353;0.2050,0.4312)$; corr 0.642 | Tsay IBM/S&P orthogonalised IRF | L09-02 §3.1 |
| $\Theta_1(\mathrm{CA},\mathrm{US})=0.4496$ | VAR(3) | L09-02 §3.2 |
| 0.0758, 0.0230; 0.8774 / 0.0676 / 0.0550 | FEVD at $h=1$; UK at $h=20$ | L09-02 §4.1 |
| $L^{-1}=(1,0;-0.5,1)$, $G=\mathrm{diag}(2,0.5)$; $r_{2t}=0.3+0.5r_{1t}-\dots$ | T Ex. 8.3, ordering $(r_1,r_2)$ | L09-03 §4.1 |
| $r_{1t}=-0.2+1.0r_{2t}-\dots$ | T Ex. 8.3, ordering $(r_2,r_1)$ | L09-03 §4.1 |
| 13.6% vs 48.5% | share of $r_1$'s 10-step variance due to the $r_2$ shock, two orderings, Ex. 8.3 (Ordering Dial) | L09-03 §4.1 |
| 11 zeros vs 10; 18 vs 15 | Illustrations 1 and 2 | L09-03 §5 |
| 0.647 → 0.690 (λ=0.2) → 0.926 (λ=0.05) | Minnesota posterior mean of $B_1(1,1)$, $T=58$ | L09-04 §3.1 |
| 0.379 → 0.055 | $B_1(1,2)$: OLS vs λ=0.2 (truth 0.1) | L09-04 §3.1 |
| 0.069, 0.9996, $z^*=0.3035$ | SSVS inclusion at $z=0.2,0.5$; crossing | L09-04 §5 |
| 7.56 vs 0.46 | relative MSFE, CEE OLS $p=13$ vs LARGE BVAR, EMPL $h=1$ | L09-04 §6 |
| 3, 7, 14, 40 | $k_{\max}$ for $m=6,12,20,50$ | L09-05 §2 |
| 0.9901, 0.891, 0.70; 0.990 … 0.714 | slide-22 $\Omega$ entries; communalities | L09-05 §3.1 |
| $V_f$ diag 0.00923, 0.03671 | slide-22 factor-score posterior variances | L09-05 §3.1 |
| 1.030, 1.008, 1.020; 0.757 | exchange-rate communality + uniqueness; ITA–GER correlation | L09-05 §3.2 |
| 0.70 / 0.65 vs 0.46 | FAVAR (1, 3 factors, BVAR) vs LARGE BVAR, EMPL $h=1$ | L09-05 §4 |
| $q=0.0234$, $p^*=0.1652$, $K^*=0.1418$, $1-K^*=0.858$ | Tsay Ex. 11.1 | L09-06 §4.2 |
| $\sigma_e=0.4802$, $\sigma_\eta=0.0736$ | from $\hat\theta=0.858$, $\hat\sigma_a=0.5184$ | L09-06 §4.2 |
| $-92.506$ | $\log_{10}$ marginal likelihood, Greenberg's TVP Phillips curve | L09-06 §5 |
| 0.9493; 25.6; 13.3 days | W&T GARCH persistence, long-run variance, half-life | L09-07 §4.1 |
| 1.0029 | S&P GARCH persistence (above one) | L09-07 §4.1 |
| 0.7518 / 2.43 days; 0.9085 / 7.22 days | Tse–Tsui and Engle DCC persistence and half-life | L09-07 §4.1 |
| 0.9387; 0.4893 | FSV correlation at $h=1$ and $h=0.05$ (slide-22 pair) | L09-07 §5 |
| 0.989; 0.858 | 6-d FSV factors vs the 3-d US and BR factors | L09-07 §6 |
