---
tags: [notes, lecture-09, pitfalls, true-false, self-test, var, irf, svar, bvar, factor-model, kalman, dcc, fsv]
date: 2026-10-25
status: taught
source: "The seven section notes L09-01 … L09-07; V/F conventions of rules/00_estilo_avaliacao.md (macro-1 style); every number re-checked by Notas/L09/L09_python_checks.py. The self-test is original; no textbook exercise is reproduced."
---

# Class 9 · Pitfalls — the confusions, each with its minimal counterexample, and an original True/False self-test

> Prev: [[L09-08-formulas]] · Next: [[L09-10-python]] · Map: [[L09-00-map]]

Every number below is asserted in [[L09-10-python]] or in the companion check. Equations are
cited by the section note's own numbering.

---

## Part I — the confusions this material produces

### 1 · A coefficient above one vs a non-stationary VAR

**The confusion.** "$\Phi_{22}=1.1>1$, so the VAR is explosive."

**Counterexample** (T Ex. 8.3; [[../L01/L01-07-ar-var-review|L01 §9.1]]). The eigenvalues of
$\Phi=\begin{pmatrix}0.2&0.3\\-0.6&1.1\end{pmatrix}$ are 0.8 and 0.5: stationary. Conversely, the
slide-13 VAR(2) has no entry above 0.9 but a companion root of 0.91 and $|\Phi(1)|=0.032$.

> **Stationarity is read off the companion eigenvalues (L09-01 (14)–(15)), never off an entry.**

### 2 · Reduced-form vs orthogonalised impulse responses

**The confusion.** $\Psi_s(i,j)$ is "the effect of a shock to $j$".

**Counterexample** (Tsay IBM/S&P, L09-02 §3.1). Innovations correlate 0.642; a unit IBM innovation
"holding the S&P innovation constant" is a pattern the data rarely produce. The orthogonalised
$\Theta_0=\begin{pmatrix}6.9973&0\\3.5432&4.2280\end{pmatrix}$ attributes the common part to whichever
series comes first.

> **$\Psi_s$ answers a counterfactual with correlated shocks held fixed; $\Theta_s=\Psi_sP$ answers
> one with orthogonal shocks — and needs an ordering (L09-02 (6)).**

### 3 · The ordering as a detail vs an identifying assumption

**The confusion.** "Cholesky is just a numerical device."

**Counterexample** (T Ex. 8.3, L09-03 §4.1). Ordering $(r_1,r_2)$: $r_{2t}=0.3+0.5r_{1t}-\dots$; ordering
$(r_2,r_1)$: $r_{1t}=-0.2+1.0r_{2t}-\dots$. The share of $r_1$'s 10-step variance due to the $r_2$ shock
is 13.6% or 48.5%.

> **A recursive ordering is a statement about who reacts to whom within the period (L09-03 (9)).
> At $\rho=0$, and only then, it is harmless.**

### 4 · The order condition vs identification

**The confusion.** "I have $q(q-1)/2$ zeros, so $A_0$ is identified."

**Counterexample.** Counting is necessary, not sufficient: the zeros must leave no rotation other than
$Q=I$ (up to sign) that preserves them (slide 34's definition). And slide 32's commodity-price
example shows only two zeros for $q=3$ — one short.

> **Count first (L09-03 (8)), then check that the restrictions actually pin the rotation down.**

### 5 · OLS equation by equation vs "ignoring the correlation between equations"

**The confusion.** "Equation-by-equation OLS throws away $\Sigma$; SUR must be better."

**Counterexample** (L09-01 (12)). With the same regressors in every equation, GLS on the stacked
system returns OLS exactly. SUR gains only after restrictions make the regressors differ (the site's
`refVAR`).

> **$\Sigma$ drops out of $\hat B$ when $X$ is common (L09-01 (11)–(12)); it still enters
> $\mathrm{Cov}(\hat\beta)=\Sigma\otimes(X'X)^{-1}$.**

### 6 · AIC vs BIC lag choice

**The confusion.** "The criteria disagree, so one is wrong."

**Counterexample** (VARorder on the GDP data, L09-01 §7.1). AIC picks 2, BIC and HQ pick 1; $M(i)$ stops
at 2. BIC's penalty $\ln T$ exceeds AIC's 2 once $T>7.4$, so BIC can never choose more lags than AIC.

> **They answer different questions (prediction vs consistent selection) with different penalties
> (L09-01 (21)).**

### 7 · Shrinkage as bias vs shrinkage as a better estimator

**The confusion.** "The Minnesota posterior is biased toward a random walk, so OLS is safer."

**Counterexample** (L09-04 §3.1, $T=58$). OLS puts 0.379 on $B_1(1,2)$ (truth 0.1); the posterior mean at
$\lambda=0.2$ is 0.055. Bańbura et al.: CEE OLS with 13 lags has MSFE 7.56 times the random walk's,
the 131-variable BVAR 0.46.

> **Shrinkage trades bias for variance; with many coefficients per observation, it wins (L09-04 (9)).**

### 8 · $\lambda$ as "prior strength" vs a variance scale

**The confusion.** "Large $\lambda$ means a strong prior."

**Counterexample** (L09-04 (2), (7)). $\lambda$ multiplies the prior **standard deviations**: $\lambda\to\infty$
returns OLS, $\lambda\to0$ returns the random walk.

> **Small $\lambda$ = tight prior.**

### 9 · Normal-Wishart vs Minnesota

**The confusion.** "Normal-Wishart is the Minnesota prior with $\Sigma$ unknown."

**Counterexample** (L09-04 §4). $\Psi\otimes\tilde\Omega$ gives every equation the same relative
tightness across regressors, so it cannot make other variables' lags tighter than own lags: $\theta=1$.

### 10 · Factors identified vs loadings identified

**The confusion.** "The estimated loadings are the factor structure."

**Counterexample** (L09-05 (4)). $(\beta P',Pf_t)$ fits identically for any orthogonal $P$; only
$\beta\beta'$ is identified. The site's FSV names the US factor first because Apple is row 1;
`factanal` names the Brazil factor first.

> **Lower-triangular $\beta$ (or another normalisation) is a convention that names the factors.**

### 11 · More factors always fit better vs the identification bound

**The confusion.** "With $m=6$ series, use as many factors as you like."

**Counterexample** (L09-05 (7)). $k\le3$ at $m=6$; at $k=3$ the factor model has 21 parameters, as many
as an unrestricted $\Omega$ — no restriction left.

### 12 · The Kalman gain as a tuning knob vs a derived quantity

**The confusion.** "Pick $K$ to smooth more or less."

**Counterexample** (Tsay Ex. 11.1, L09-06 §4.2). $K^*$ is fixed by $q=\sigma_\eta^2/\sigma_e^2$: 0.1418,
which equals $1-\hat\theta=0.142$ from the ARIMA(0,1,1) fit.

> **The filter's smoothing weight is the model's signal-to-noise ratio (L09-06 (13)).**

### 13 · Time-varying parameters as "more realistic, hence better"

**The confusion.** "Coefficients surely move, so a TVP model must win."

**Counterexample** (G §10.3). Greenberg's Phillips curve: the constant-coefficient AR(1) has the larger
marginal likelihood. Each random-walk state adds variance $t\Omega$ (L09-06 (16)).

### 14 · DCC's parameters as pair-specific

**The confusion.** "DCC lets each correlation have its own dynamics."

**Counterexample** (T p. 531). $\theta_1,\theta_2$ are scalars: every pair reverts at the same rate
$(\theta_1+\theta_2)^h$. FSV pairs differ through $a_{it},a_{jt}$ (L09-07 (12)).

### 15 · Correlations rising in crises as a separate phenomenon

**The confusion.** "Correlations and volatilities need separate models."

**Counterexample** (L09-07 (12)). In a one-factor model $|\rho_t|$ increases with the factor variance
automatically: 0.939 at $h=1$, 0.489 at $h=0.05$ for the slide-22 pair.

### 16 · GARCH persistence below one by assumption

**The confusion.** "Fitted GARCH models always mean-revert."

**Counterexample** (site page, L09-07 §4.1). The S&P 500 fit has $\alpha_1+\beta_1=1.0029$: no finite
unconditional variance, shocks never fade.

### 17 · Ticker vs asset

**The confusion.** "WTI" on the site page is crude oil.

**Counterexample.** It is W&T Offshore, Inc. (`names = c("W&T Offshore, Inc.","S&P 500")`).

### 18 · Labels in the site scripts

**The confusion.** Taking the plot titles of `VAR-Example.html` at face value.

**Counterexample** (L09-02 §2.1, §4.1). The IRF titles swap shock and response, and the FEVD plot
labels row 2 "CAN" although the order is (uk, us, ca).

---

## Part II — True/False self-test (original)

**Scoring** ([[../../rules/00_estilo_avaliacao|rules/00]]): V/F score
$=\max\{0,\ \text{correct}-\text{wrong}/2\}\times$ item value; blank items do not count as wrong.
Difficulty: **[E]** easy · **[M]** medium · **[P]** hard. Numbers are illustrative unless a note is
cited. Answers follow each block.

### Block A — VAR, IRF, FEVD

**Setting (items 1–6).** A central-bank analyst fits a VAR(2) to quarterly Brazilian inflation,
the Selic rate and output growth (in that order), 100 quarters, by OLS equation by equation.

1. **[E]** Because each equation was estimated separately, the coefficient estimates would change if the analyst re-estimated the system by GLS using the residual covariance matrix.
2. **[M]** If one coefficient of $\hat B_1$ equals 1.05, the fitted VAR is necessarily explosive.
3. **[M]** The fitted VAR is stationary if and only if all six eigenvalues of its companion matrix have modulus below one.
4. **[E]** The $(2,1)$ element of $\Psi_4$ is the response of the Selic rate, four quarters later, to a unit inflation innovation, other innovations held fixed.
5. **[M]** Under the Cholesky ordering above, the one-quarter-ahead forecast-error variance of inflation is entirely attributed to the inflation shock.
6. **[P]** Re-ordering the variables as (Selic, inflation, output) leaves the orthogonalised impulse responses unchanged whenever the residual correlation between inflation and the Selic rate is positive.

**Answers.**
1. **F.** Same regressors in every equation ⇒ GLS = OLS (L09-01 (12)).
2. **F.** Stationarity depends on the companion eigenvalues, not on single entries (Pitfall 1).
3. **V.** $q p=3\times2=6$ eigenvalues; L09-01 (14)–(15).
4. **V.** L09-02 (4): $\Psi_s(i,j)$ is the response of $i$ to $j$.
5. **V.** $\Theta_0=P$ is lower triangular: the first variable's 1-step error loads only on shock 1 (L09-02 §4).
6. **F.** The orderings coincide only when the correlation is zero (Pitfall 3; L09-03 §4.1).

### Block B — structural identification

**Setting (items 7–10).** A four-variable SVAR $A_0y_t=A_1y_{t-1}+u_t$, $u_t\sim N(0,I)$.

7. **[E]** The reduced-form covariance is $\Sigma=(A_0'A_0)^{-1}$.
8. **[M]** At least six restrictions on $A_0$ are needed for exact identification.
9. **[M]** Any two matrices $A_0$ and $QA_0$, with $Q$ orthogonal, imply different likelihood values.
10. **[P]** Imposing that $A_0$ be lower triangular with a positive diagonal makes $A_0^{-1}$ the Cholesky factor of $\Sigma$, and the structural IRFs coincide with the orthogonalised IRFs.

**Answers.**
7. **V.** L09-03 (4).
8. **V.** $q(q-1)/2=6$ (L09-03 (8)).
9. **F.** They give the same $(B,\Sigma)$, hence the same likelihood (L09-03 (6)–(7)).
10. **V.** L09-03 (9).

### Block C — Bayesian VAR

**Setting (items 11–15).** A Minnesota-prior BVAR for 20 Brazilian macro series, $p=4$, with
$\Sigma$ fixed at univariate AR residual variances.

11. **[E]** As the overall tightness $\lambda$ goes to zero, the posterior mean of each equation approaches a random walk for its own variable.
12. **[M]** The prior standard deviation of the fourth own lag is one quarter of that of the first own lag.
13. **[M]** With $\theta<1$, the prior can be written as Normal-Wishart, $\beta\mid\Sigma\sim N(\beta_0,\Sigma\otimes\Omega_0)$.
14. **[P]** For a single coefficient with an orthogonal regressor, the weight on the prior mean is $\mathrm{Var}(\hat b)/(\mathrm{Var}(\hat b)+v_0)$, so it rises with the sample size.
15. **[M]** Under SSVS with $c_0=0.1$ and $c_1=10$ times the OLS standard error, a draw of a coefficient equal to 0.5 standard errors is classified as included with probability above 0.99.

**Answers.**
11. **V.** L09-04 (7): $V_{i0}\to0$, $\bar\beta_i\to\beta_{i0}$.
12. **V.** sd $=\lambda/k$: $\lambda/4$ vs $\lambda$ (L09-04 (2)).
13. **F.** Kronecker structure forces $\theta=1$ (Pitfall 9).
14. **F.** $\mathrm{Var}(\hat b)=\sigma^2/s_{xx}$ falls with $T$, so the prior weight falls (L09-04 (9)).
15. **V.** 0.9996 (L09-04 §5); the crossing is at 0.30.

### Block D — factors, TVP, covariances

**Setting (items 16–24).** A risk desk models daily returns of Itaú, Bradesco, Petrobras and Vale.

16. **[E]** In a one-factor model with $f_t\sim N(0,1)$ and diagonal idiosyncratic covariance, the covariance between Itaú and Bradesco equals the product of their loadings.
17. **[M]** With four series, a three-factor model is admissible under the parameter-count bound.
18. **[M]** Rotating the loadings by an orthogonal matrix changes the implied covariance matrix of the returns.
19. **[M]** In a one-factor SV model, if the factor's log-variance falls sharply on a calm day, the implied correlation between two positively loaded banks falls.
20. **[E]** In an Engle DCC with $\theta_1+\theta_2=0.9085$, half of a correlation shock is gone after about 7 trading days.
21. **[M]** In a DCC, the bank–bank and bank–oil correlations can revert at different speeds.
22. **[P]** For a local-level model of log realised volatility with $\sigma_\eta^2/\sigma_e^2=0.0234$, the steady-state Kalman filter puts about 86% weight on the latest observation.
23. **[M]** A random-walk TVP coefficient has prior variance growing linearly with time.
24. **[P]** A fitted GARCH(1,1) with $\alpha_1+\beta_1=1.003$ has a finite unconditional variance $\omega/(1-\alpha_1-\beta_1)$.

**Answers.**
16. **V.** L09-05 (3).
17. **F.** $k\le(2m+1-\sqrt{8m+1})/2=(9-\sqrt{33})/2=1.63$, so $k\le1$ at $m=4$ (L09-05 (7)).
18. **F.** $\beta P'P\beta'=\beta\beta'$ (L09-05 (4)).
19. **V.** $|\rho_t|$ increases in $h_t$ (L09-07 (12)).
20. **V.** $\ln0.5/\ln0.9085=7.22$ (L09-07 §4.1).
21. **F.** Scalar $\theta$'s: one speed for all pairs (Pitfall 14).
22. **F.** $K^*=0.142$: about 14% on the latest observation, 86% on the previous estimate (L09-06 §4.2).
23. **V.** $\mathrm{Var}(\beta_t\mid\beta_0)=t\Omega$ (L09-06 (16)).
24. **F.** $1-\alpha_1-\beta_1<0$: no finite unconditional variance (Pitfall 16).

---

## Part III — the distinctions that cost most points

| Pair | The difference |
|---|---|
| $\Psi_s$ vs $\Theta_s$ | unit correlated innovation vs one-sd orthogonal shock |
| Order condition vs identification | counting restrictions vs pinning down the rotation |
| OLS vs SUR in a VAR | identical with common regressors; differ after zero restrictions |
| $\lambda$ small vs large | prior (random walk) vs OLS |
| Minnesota vs Normal-Wishart | $\theta<1$ allowed vs $\theta=1$ forced |
| Loadings vs $\beta\beta'$ | identified only up to rotation vs identified |
| $K_t$ vs $K^*$ | initial path vs steady state set by $q$ |
| DCC vs FSV correlation | own recursion with scalar $\theta$'s vs implied by factor volatility |
