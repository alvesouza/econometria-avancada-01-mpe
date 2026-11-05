---
tags: [notes, lecture-07, pitfalls, true-false, review]
date: 2026-10-25
status: taught
source: "L07-01 … L07-06 (numbers as worked there); counterexamples checked in L07_python_checks.py section 7; V/F style of rules/00_estilo_avaliacao.md (reciprocal falsehoods, one claim per item)"
---

# Class 7 · Pitfalls — fourteen confusions, and a 30-item True/False self-test

> Prev: [[L07-07-formulas]] · Next: [[L07-09-python]] · Map: [[L07-00-map]]

Every counterexample uses a number derived in a section note; the new ones are checked in
`L07_python_checks.py` §7 ([[L07-09-python]] §7).

---

## Part I — the confusions

**1 · "Heteroskedasticity biases OLS."** No: OLS stays unbiased; its *variance formula* is wrong and it is
inefficient. Counterexample: W Example 8.6, OLS 0.821 vs WLS 0.787 — both estimate the same slope;
what differs is the SE (0.104 vs 0.063) ([[L07-01-general-covariance-gls]] §3).

**2 · "Robust standard errors make OLS as good as GLS."** They make OLS *inference* valid, not OLS
*efficient*. At $\alpha_1=1$ the true OLS slope variance is 4.38 times GLS's whatever SE you report (01 §4.1).

**3 · "WLS weights are $1/\sqrt{h_i}$."** The *variables* are divided by $\sqrt{h_i}$; the *squared residuals*
are weighted by $1/h_i$ (W p. 256). And the constant column is divided too — the transformed regression has
no column of ones (01 (9)).

**4 · "σ² in a t model is the error variance."** It is the scale; the variance is $\sigma^2\nu/(\nu-2)$. G's
Vella–Verbeek σ² falls from 0.165 to 0.105 under $t_5$, yet $0.105\times5/3=0.175$: the spread hardly changed
([[L07-02-student-t-errors]] §6).

**5 · "The ω_i are random effects to be estimated and reported."** They are a computational device: the
model is the marginal t; the $\omega_i$ are integrated out by ignoring their draws (G p. 114). Their
posterior means are still useful diagnostics — an outlier's weight 0.018 (02 §5).

**6 · "A large ν posterior is evidence of normality."** ν is weakly identified; the slide-21 chain wanders
over 5–60 with ACF 0.5 at lag 30, and one outlier drags the posterior mean to 3.8 (02 §5). Look at the
prior too: Exp(25) already puts 0.20 on ν ≥ 40.

**7 · "With AR(1) errors OLS standard errors are always too small."** Only if the regressor is persistent in
the same direction: true/naive variance $=(1+\rho\phi)/(1-\rho\phi)$, equal to 1 when φ = 0 and **below** 1 when
ρφ < 0. The efficiency loss of OLS remains even when the SE is right (9.53 at ρ = 0.9, φ = 0)
([[L07-03-ar1-errors]] §3).

**8 · "Cochrane–Orcutt and Prais–Winsten are different estimators of different things."** Same model, same
ρ iteration; PW keeps the first observation rescaled by $\sqrt{1-\rho^2}$. Barium: 2.94 vs 2.95 (03 §2).

**9 · "Shrinkage pulls estimates toward zero."** Toward the estimated population mean: school C (−2.75)
moves **up** to 7.02 at τ = 5.23 ([[L07-04-hierarchical-linear-models]] §5).

**10 · "Hierarchical = random effects = consistent no matter what."** The exchangeable prior, like RE,
assumes unit effects unrelated to the regressors (W 14.8); FE (individual effects with a flat prior) does
not (04 §8).

**11 · "The site's band is a predictive interval."** It is the posterior of $\alpha_i+\beta_ix$; a new
measurement adds $N(0,\sigma_y^2)$ (04 §6).

**12 · "The Tobit coefficient is the marginal effect on hours."** It is the effect on $E(y^*)$; on $E(y\mid x)$ it is
$\beta_j\Phi(z)$, at the averages 0.645 × β, on average 0.589 × β for Mroz ([[L07-05-tobit]] §5, §7).

**13 · "Censored = truncated."** Censored samples keep the units (with $y$ at the limit); truncated samples
lose them, $x$ included. The slides' "probability of truncation" is a censoring probability (05 §1). OLS
is biased in both, differently: full censored sample → slope $\beta P(y>0)=1.50$; positive part only → 1.902
(05 §6, §8).

**14 · "Probit coefficients are comparable to logit ones."** Only after scaling: logit ≈ 1.6 × probit (Mroz
0.221/0.131 = 1.69; scale factors 0.391/0.243 = 1.61). The probabilities agree; the coefficients do not
([[L07-06-probit-ordered-multinomial]] §1–§2).

---

## Part II — True/False self-test (original)

Score per `rules/00_estilo_avaliacao.md`: correct − wrong/2. Tags: **[E]** essential, **[M]** medium, **[P]** probing.

### Block A — general covariance and heteroskedasticity

**1. [E]** If $P\Omega P'=I$, OLS on $(Py,PX)$ equals $(X'\Omega^{-1}X)^{-1}X'\Omega^{-1}y$ for every such $P$.
**True.** $\Omega^{-1}=P'P$ and only $P'P$ appears in the OLS formula on the rotated data (01 (4)–(5)).

**2. [E]** Under heteroskedasticity with known $h_i$, OLS is biased, which is why WLS is used.
**False.** OLS remains unbiased; WLS is used for efficiency and for valid usual standard errors (01 §1, W p. 255).

**3. [M]** In the full conditional of β, setting $V_0^{-1}=0$ gives a posterior mean equal to the GLS estimator.
**True.** $V_1^{-1}\beta_1=\sigma^{-2}X'\Omega^{-1}y$ and $V_1^{-1}=\sigma^{-2}X'\Omega^{-1}X$ (01 (8)).

**4. [M]** For $h(z,\alpha)=\exp(z'\alpha)$ with a normal prior on α, the full conditional of α is normal.
**False.** α appears in $-\frac12\sum z_i'\alpha$ and inside $e^{-z_i'\alpha}$: no conjugate form, hence MH (01 (12)).

**5. [P]** In FGLS, the intercept of the regression of $\log\hat u^2$ on $x$ estimates $\log\sigma^2$ consistently.
**False.** It absorbs $E\log v$ (−1.27 for normal errors); harmless, because a constant factor in $h$ cancels from WLS (01 §4.1).

**6. [M]** A WLS standard error 40% smaller than the robust OLS one proves the variance model is correct.
**False.** The WLS SE is computed *assuming* $h=inc$; if $h$ is wrong, it is wrong too (W p. 257, 01 §4.1).

### Block B — Student-t errors

**7. [E]** If $\epsilon\mid\omega\sim N(0,\sigma^2\omega)$ and $\omega\sim IG(\nu/2,\nu/2)$, then $\epsilon\sim t_\nu(0,\sigma^2)$.
**True.** Integrating the $IG((\nu+1)/2,(\nu+\epsilon^2/\sigma^2)/2)$ kernel leaves $(1+\epsilon^2/(\nu\sigma^2))^{-(\nu+1)/2}$ (02 (1)–(3)).

**8. [E]** If $\omega_i^{-1}\sim IG(\nu/2,\nu/2)$, the marginal of $\epsilon_i$ is $t_\nu$.
**False.** The reciprocal relation: $\omega_i\sim IG$, equivalently $\omega_i^{-1}\sim$ Gamma (the slide-6 slip, 02 §2).

**9. [M]** In the Gibbs sampler, an observation with $|\epsilon_i|<\sigma$ gets an expected weight above 1.
**True.** $(\nu+1)/(\nu+\epsilon_i^2/\sigma^2)>1\iff\epsilon_i^2<\sigma^2$ (02 (5)).

**10. [M]** The full conditional of ν is a gamma distribution when ν has an exponential prior.
**False.** ν enters through $[(\nu/2)^{\nu/2}/\Gamma(\nu/2)]^n$; the conditional (02 (6)) is non-standard — MH.

**11. [P]** With a flat prior on β and $\nu\sim\mathrm{Exp}(25)$, the posterior median of β exists but the posterior mean may not.
**True.** Geweke: the mean needs $P(\nu\le2)=0$, and the exponential puts mass there; quantiles always exist (02 §4).

**12. [M]** Under $t_5$ errors the scale σ² equals the error variance.
**False.** Variance $=\sigma^2\cdot5/3$ (02 §6).

### Block C — AR(1) errors

**13. [E]** With AR(1) errors, $\mathrm{Cov}(\epsilon_t,\epsilon_{t+k})=\rho^k\sigma^2/(1-\rho^2)$ for $|\rho|<1$.
**True.** (03 (1)–(2)).

**14. [M]** $\Omega_\rho$ is tridiagonal.
**False.** Its *inverse* is tridiagonal; $\Omega_\rho$ itself is full, entries $\rho^{|i-j|}/(1-\rho^2)$ (03 (3)).

**15. [M]** Cochrane–Orcutt and Prais–Winsten differ only in the treatment of the first observation.
**True.** PW keeps $\sqrt{1-\rho^2}(y_1,x_1)$; CO drops it (03 §2, W p. 383).

**16. [P]** If the regressor is serially uncorrelated, AR(1) errors leave OLS both efficient and with correct usual standard errors.
**False.** The SE is (asymptotically) right — ratio 1 — but GLS is still more efficient: 9.53 at ρ = 0.9 (03 (10)–(11)).

**17. [M]** After conditioning on the first error, the full conditional of ρ under a truncated-normal prior is a truncated normal.
**True.** The likelihood becomes that of a regression of $\epsilon_t$ on $\epsilon_{t-1}$ (03 (13)).

### Block D — hierarchical models

**18. [E]** In the individual-effects model with a hierarchical prior, the posterior mean of $\alpha_i$ moves toward $\mu_\alpha$ more when $T$ is small.
**True.** Weight on own data $w=TV_\alpha/(TV_\alpha+\sigma^2)$ falls with $T$ (04 (6)).

**19. [M]** In the update of $\mu_\alpha$, the precision of each $\alpha_i$ is $\sigma^{-2}$.
**False.** It is $V_\alpha^{-1}$ — the slide-13 slip (04 (7)).

**20. [M]** In the eight-schools model, every posterior mean $E(\theta_i\mid y,\tau)$ lies between $y_i$ and $\hat\mu(\tau)$.
**True.** It is the convex combination $(1-B_i)y_i+B_i\hat\mu$ (04 (14)).

**21. [P]** Shrinkage always moves the extreme schools toward zero.
**False.** Toward $\hat\mu\approx8$: school C (−2.75) moves up (04 §5, Part I.9).

**22. [M]** The individual-effects model with a vague non-hierarchical prior reproduces the dummy-variable (fixed-effects) regression.
**True.** Each $\alpha_i$ is learned from its own unit only (04 §2, W p. 438).

**23. [P]** The site's 95% band for woman 1 at $x=40.143$ covers a new weight measurement with 95% probability.
**False.** It omits the $\sigma_y$ noise: it is a band for the mean line (04 §6).

### Block E — Tobit

**24. [E]** In the Tobit, $P(y=0\mid x)=1-\Phi(x'\beta/\sigma)$.
**True.** (05 (2), W 17.21).

**25. [M]** In the Tobit, $\partial E(y\mid x)/\partial x_j=\beta_j$.
**False.** It is $\beta_j\Phi(x'\beta/\sigma)$ (05 (12)); β is the latent-scale effect.

**26. [M]** In Chib's data augmentation, the latent value of a censored observation is drawn from a normal truncated to $(-\infty,0]$.
**True.** (05 (6)).

**27. [P]** With $x\sim N(a,1)$, OLS of the censored $y$ on $x$ estimates $\beta$ times the share of uncensored observations.
**True.** Stein's lemma: $\mathrm{Cov}(x,\max(0,y^*))=\mathrm{Cov}(x,y^*)P(y^*>0)$ (05 (14)).

### Block F — probit family

**28. [E]** In the probit, $(\beta,\sigma)$ and $(2\beta,2\sigma)$ give the same likelihood, so σ is fixed at 1.
**True.** Only $x'\beta/\sigma$ enters (06 (1)).

**29. [M]** In the ordered probit Gibbs sampler, each cut-point is drawn from a normal distribution.
**False.** From a uniform between the largest latent value of its lower category and the smallest of its upper one (06 (8)).

**30. [P]** In the multinomial probit, fixing one variance of Ω is needed even after differencing utilities from a base alternative.
**True.** Differencing removes the location; $(c\beta,c^2\Omega)$ still gives the same choices — the scale (06 §4).

## Links

- Unit: [[L07-00-map]] · [[L07-07-formulas]] · [[L07-09-python]] §7 (the counterexamples' code).
- Style: [[../../rules/00_estilo_avaliacao|rules/00]].
