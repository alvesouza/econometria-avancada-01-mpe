---
tags: [notes, lecture-03, hierarchical-model, exchangeability, beta-binomial, partial-pooling, shrinkage, random-coefficients, gibbs, stan]
date: 2026-10-29
status: taught
source: "Greenberg 1e §4.5 (pp. 50–52, (4.8)–(4.9)), §4.6 (pp. 52–53, (4.10)–(4.12)), §4.9 (pp. 54–56); hierarchical-beta-binomial.html (13 Manhattan hospitals, AMI deaths 2015, Stan output; after Albert, Bayesian Hierarchical Modeling §10.3); hierarchical-gaussian-linear-model.html (68 pregnant women, weight gain, Gibbs sampler; Gamerman and Lopes 2006, Ex. 5.6)"
---

# G §4.5–4.6, the two hierarchical site pages · Hierarchical models: estimate each unit by borrowing strength from the others

> **Claim.** When units (hospitals, women, funds) are similar but not identical, treat their
> parameters as **exchangeable** draws from a common distribution whose parameters are themselves
> estimated. Each unit's posterior mean is then a weighted average of its own estimate and the group
> mean, with weight $\eta/(\eta+n_i)$ on the group: small units are pulled hardest. For 13 Manhattan
> hospitals the death rates range from **2.9% to 13.0%** separately; partially pooled, from **5.7% to
> 8.9%**, around $E(\mu\mid y)=7.2\%$. An exact grid computation reproduces the lecturer's Stan output
> (posterior median of $\mu$ 0.0714 vs 0.0715). For 68 women's weight-gain curves the Gibbs sampler of
> the random-coefficient model separates within-woman noise ($\sigma\approx1.10$ kg) from between-woman
> spread, which a pooled regression lumps into one residual sd of 3.61 kg.
> Prev: [[L03-08-metropolis-hastings-hmc]] · Next: [[L03-10-sparsity-priors]] · Map: [[L03-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $y_i,n_i$ | deaths and heart-attack cases at hospital $i$ | $i=1,\dots,13$ |
| $p_i$ | death probability of hospital $i$ | $(0,1)$ |
| $\mu$ | mean of the population of hospital rates | $(0,1)$ |
| $\eta$ | precision of that population, $a+b$ of the Beta (a prior sample size) | $>0$ |
| $w_i$ | weight on $\mu$ in $E(p_i\mid\cdot)$, $\eta/(\eta+n_i)$ | $(0,1)$ |
| $y_{ij},x_{ij}$ | weight gain (kg) and week of visit $j$ of woman $i$ | $i\le68$, $j\le n_i$ |
| $\alpha_i,\beta_i$ | woman $i$'s intercept and slope | $\mathbb R$ |
| $\alpha,\beta,\tau_\alpha,\tau_\beta$ | population means and precisions of the coefficients | — |

---

## 1 · U — three ways to estimate 13 rates (hierarchical-beta-binomial.html §1)

The page's data: 13 Manhattan hospitals, 2366 heart-attack cases, 163 deaths. Mount Sinai Roosevelt
loses 6 of 46 patients (13.0%), "more than four times the rate of Harlem Hospital Center at 2.857%"
(1 of 35). Three analyses:

- **Complete pooling:** one $p$ for all: $163/2366=6.89\%$. Ignores real differences between hospitals.
- **No pooling:** 13 separate binomials. A hospital with 35 cases gets an estimate as noisy as its
  sample, and nothing learned about the other 12 hospitals is used.
- **Partial pooling (hierarchical):** the $p_i$ are draws from a common Beta whose mean and spread are
  estimated. Each estimate leans on the group in proportion to how little data the hospital has.

---

## 2 · C — exchangeability (G §4.5)

Random variables $z_1,\dots,z_n$ are **exchangeable** if their joint distribution is unchanged by any
permutation of the indices (G p. 50); iid variables are exchangeable, but exchangeable variables need
not be independent. Applied to parameters: if nothing but the data distinguishes hospital 3 from
hospital 7, the prior should treat $(p_1,\dots,p_{13})$ symmetrically, and the natural way is iid draws
**given** hyperparameters, with uncertainty about those hyperparameters making the $p_i$ dependent
a priori. Greenberg's heteroskedastic regression (4.8)–(4.9) is the same idea for variances: each
observation's precision $\lambda_i$ is a draw from $G(\nu/2,\nu/2)$, and marginally the errors are
Student-$t$ ([[L03-06-monte-carlo-simulation]] (6)).

---

## 3 · C — the hierarchical model (G §4.6)

Greenberg's three levels (4.10)–(4.12):

$$y\sim f(y\mid\theta),\qquad\theta\sim\pi(\theta\mid\theta_0),\qquad\theta_0\sim\pi(\theta_0\mid\theta_{00}),\tag{1}$$

with $\theta_{00}$ fixed. Two remarks (G p. 53). First, $\theta_0$ is not identified by the data:
$f(y\mid\theta,\theta_0)=f(y\mid\theta)$, so the data inform $\theta_0$ only through $\theta$. Second, $\theta_0$ can be integrated out,
$\pi(\theta\mid\theta_{00})=\int\pi(\theta\mid\theta_0)\pi(\theta_0\mid\theta_{00})d\theta_0$; the hierarchy is a way to **build** a prior with
dependence across units and to compute with it, not a different model.

---

## 4 · Worked — the Beta–Binomial for the hospitals (hierarchical-beta-binomial.html)

**Model (the page's Stan file).**

$$y_i\mid p_i\sim\text{Bin}(n_i,p_i),\qquad p_i\mid\mu,\eta\sim\text{Beta}(\mu\eta,\ (1-\mu)\eta),\qquad\mu\sim U(0,1),\qquad p(\eta)=\frac{n_1}{(n_1+\eta)^2},\ n_1=10.\tag{2}$$

The Beta has mean $\mu$ and variance $\mu(1-\mu)/(\eta+1)$, so $\eta$ acts as a prior sample size: large $\eta$
means the hospitals are nearly identical. The prior on $\eta$ is proper ($\int_0^\infty n_1/(n_1+\eta)^2d\eta=1$) with median
$n_1=10$ and a heavy right tail.

**Integrate the $p_i$ out.** For one hospital, Beta–binomial conjugacy ([[L03-02-conjugate-sequential-updating]] (4))
gives the marginal likelihood

$$p(y_i\mid\mu,\eta)=\binom{n_i}{y_i}\frac{B(\mu\eta+y_i,\ (1-\mu)\eta+n_i-y_i)}{B(\mu\eta,\ (1-\mu)\eta)},\tag{3}$$

so the posterior of the two hyperparameters is

$$p(\mu,\eta\mid y)\propto\frac{n_1}{(n_1+\eta)^2}\prod_{i=1}^{13}\frac{B(\mu\eta+y_i,\ (1-\mu)\eta+n_i-y_i)}{B(\mu\eta,\ (1-\mu)\eta)}.\tag{4}$$

(4) is two-dimensional: it can be evaluated **exactly on a grid** (here $1000\times1400$ points in
$\mu\times\log\eta$), with no MCMC at all.

**Each hospital, given the hyperparameters.** Conjugacy again:

$$p_i\mid\mu,\eta,y\sim\text{Beta}(\mu\eta+y_i,\ (1-\mu)\eta+n_i-y_i),\qquad E(p_i\mid\mu,\eta,y)=\frac{\mu\eta+y_i}{\eta+n_i}=w_i\,\mu+(1-w_i)\frac{y_i}{n_i},\quad w_i=\frac{\eta}{\eta+n_i}.\tag{5}$$

The second form splits $\mu\eta+y_i$ exactly as [[L03-02-conjugate-sequential-updating]] (6). Averaging (5) over (4)
gives $E(p_i\mid y)$.

**Stan vs the exact grid.** The page ran NUTS with 4 chains × 5000 post-warm-up draws (20,000 in all).

| Quantity | Stan 5% / 50% / 95% (page §6) | Exact grid 5% / 50% / 95% |
|---|---|---|
| $\mu$ | 0.0595 / 0.0715 / 0.0874 | 0.0599 / 0.0714 / 0.0874 |
| $\eta$ | 49.2 / 225.7 / 2234 | 49.9 / 229.4 / 2759 |
| sd of the Beta, $\sqrt{\mu(1-\mu)/(\eta+1)}$ | 0.0054 / 0.0170 / 0.0381 | 0.0048 / 0.0169 / 0.0376 |

The centre agrees to Monte Carlo error. The upper tail of $\eta$ does not: Stan reports $n_{eff}=766$ for
$\eta$ and a posterior sd of 1008 around a mean of 556, so its 95% quantile is noisy, while the grid's is
exact. **Heavy-tailed hyperparameters are where MCMC output needs the most checking.**

**Shrinkage in numbers.** At the posterior median $\eta\approx229$:

| Hospital | $y_i/n_i$ | $n_i$ | $w_i=\eta/(\eta+n_i)$ | $E(p_i\mid y)$ (exact) |
|---|---|---|---|---|
| Harlem | 1/35 = 0.0286 | 35 | 0.87 | 0.0649 |
| Bellevue | 4/129 = 0.0310 | 129 | 0.64 | 0.0566 |
| NYP Lower Manhattan | 4/41 = 0.0976 | 41 | 0.85 | 0.0765 |
| NYP Allen | 13/105 = 0.1238 | 105 | 0.69 | 0.0887 |
| Mount Sinai Roosevelt | 6/46 = 0.1304 | 46 | 0.83 | 0.0833 |
| NYP Columbia | 25/353 = 0.0708 | 353 | 0.39 | 0.0709 |

The 13 separate rates have sd 0.0300; the 13 posterior means, 0.0090. Every posterior mean lies
between its own $y_i/n_i$ and $E(\mu\mid y)=0.0723$.

![Left: thirteen lines join each hospital's raw death proportion y/n (left column, from 0.029 to 0.130, marker size by number of cases) to its hierarchical posterior mean E(p|y) (right column, from 0.057 to 0.089), with a dashed line at E(mu|y) = 0.0723; small hospitals move furthest and two lines cross. Right: posterior mean of theta against an observation y from 0 to 8 under a normal N(0,1) prior (straight line y/2), a Laplace prior with variance 1, and horseshoe priors with tau = 1 and tau = 0.1; the horseshoe curves stay near zero for small y and join the 45-degree line for large y.](figures/L03-shrinkage.png)
*Left: (5) averaged over the exact posterior (4) for the 13 hospitals (hierarchical-beta-binomial.html §8, recomputed). Right: shrinkage profiles of [[L03-10-sparsity-priors]].*

Read the left panel as the page's §8 plot. Large hospitals (big dots) barely move: NYP Columbia, with
353 cases and a rate already at the centre, stays at 0.071. The small ones move most. Lines cross:
Harlem (1 death in 35) starts below Bellevue (4 in 129) and ends above it (0.0649 vs 0.0566), and
Roosevelt starts above NYP Allen and ends below it (0.0833 vs 0.0887). Ranking hospitals by raw rates and
by posterior means does not give the same league table, because a small hospital's extreme rate is
mostly noise. The hierarchical model does not decide this by fiat:
$\eta$, and hence how much to pool, is estimated from how dispersed the 13 rates are relative to binomial
noise.

---

## 5 · Worked — the hierarchical Gaussian linear model (hierarchical-gaussian-linear-model.html)

**Data.** Weight gain (kg) of $I=68$ pregnant women at 5 to 7 prenatal visits (UFRJ maternity clinic;
Gamerman and Lopes 2006, Ex. 5.6): 8, 33 and 27 women have 5, 6 and 7 visits, $n=427$ pairs $(x_{ij},y_{ij})$,
$x$ in weeks.

**No pooling and full pooling.** The page first fits 68 separate regressions (intercepts, slopes and
residual sds vary widely) and then one pooled regression:
$\hat y=-4.526+0.476x$, residual sd 3.612 (verified in [[L03-13-python]] §9 from the page's own data).

**The model (page §5).**

$$y_{ij}\sim N(\alpha_i+\beta_ix_{ij},\ \sigma^2),\qquad\alpha_i\sim N(\alpha,1/\tau_\alpha),\quad\beta_i\sim N(\beta,1/\tau_\beta),\tag{6}$$

$$\alpha\sim N(0,1/P_\alpha),\ \beta\sim N(0,1/P_\beta),\ \tau_\alpha,\tau_\beta\sim G(a,b),\ \sigma^2\sim IG(a,b),\qquad P_\alpha=P_\beta=a=b=1.\tag{7}$$

There are $p=5+2I=141$ unknowns; the joint posterior has no closed form, but every full conditional
does ("the Gibbs sampler becomes the standard solution").

**Full conditionals.** Each follows from keeping the factors of (6)–(7) that contain the block
([[L03-07-markov-chains-gibbs]] §4).

- *$(\alpha_i,\beta_i)$:* a normal regression of woman $i$'s $n_i$ points with prior precision $A^{-1}=\text{diag}(\tau_\alpha,\tau_\beta)$
  centred at $(\alpha,\beta)$; by [[L03-03-normal-measurement-physicists]] §7,

$$(\alpha_i,\beta_i)\mid\cdot\sim N_2(m_i,V_i),\qquad V_i=\big(A^{-1}+X_i'X_i/\sigma^2\big)^{-1},\quad m_i=V_i\big(A^{-1}(\alpha,\beta)'+X_i'y_i/\sigma^2\big).\tag{8}$$

  (The page's text prints $V_i$ without the inverse and $X_i'y_i$ without the $1/\sigma^2$; its code has both.)

- *$\alpha$ (and $\beta$):* the 68 intercepts are 68 "observations" of $\alpha$ with precision $\tau_\alpha$:

$$\alpha\mid\cdot\sim N\Big(\frac{\tau_\alpha\sum_i\alpha_i}{\tau_\alpha I+P_\alpha},\ \frac1{\tau_\alpha I+P_\alpha}\Big).\tag{9}$$

- *$\tau_\alpha$ (and $\tau_\beta$):* $\tau_\alpha\mid\cdot\sim G\big(a+I/2,\ b+\sum_i(\alpha_i-\alpha)^2/2\big)$.
- *$\sigma^2$:* $\sigma^2\mid\cdot\sim IG\big(a+n/2,\ b+\sum_i\sum_j(y_{ij}-\alpha_i-\beta_ix_{ij})^2/2\big)$.

(The page writes $\beta_i$'s prior density with $1/\tau_\alpha$ in the joint posterior; it should be $1/\tau_\beta$.)

**Results (NumPy port, 3000 draws after 500 burn-in, posterior medians).** $\alpha=-3.66$, $\beta=0.465$ kg per week,
between-woman sds $1/\sqrt{\tau_\alpha}=3.39$ and $1/\sqrt{\tau_\beta}=0.217$, within-woman sd $\sigma=1.10$. The pooled residual sd
3.61 mixed two things the hierarchy separates: measurement-to-measurement noise around each woman's
line (1.10) and real differences between women's lines. The page's §5.6 plots each woman's
posterior median coefficients against her OLS ones: points move toward the population line, most for
women whose own fit is least certain.

---

## 6 · C — shrinkage as the common thread

Every shrinkage formula in this unit has the form

$$\text{estimate}_i=w_i\times(\text{prior or group centre})+(1-w_i)\times(\text{unit's own estimate}),\qquad w_i=\frac{\text{prior precision}}{\text{prior precision}+\text{data precision}_i}.\tag{10}$$

| Where | Prior / group centre | $w_i$ |
|---|---|---|
| Beta–Bernoulli ([[L03-02-conjugate-sequential-updating]] (6)) | $\alpha_0/(\alpha_0+\beta_0)$ | $(\alpha_0+\beta_0)/(\alpha_0+\beta_0+n)$ |
| Normal measurement ([[L03-03-normal-measurement-physicists]] (8)) | $\mu_0$ | $\sigma^2/(\sigma^2+\tau_0^2)$ |
| Hospitals, (5) | $\mu$ (estimated) | $\eta/(\eta+n_i)$ |
| Random coefficients, (8) | $(\alpha,\beta)$ (estimated) | matrix weight $V_iA^{-1}$ |
| Ridge ([[L03-10-sparsity-priors]] §2) | 0 | $\lambda/(d_j^2+\lambda)$ per principal direction |

What the hierarchy adds is that the centre and the weight are **learned from the ensemble** instead of
fixed by the analyst. The sparsity priors of [[L03-10-sparsity-priors]] go one step further and make
the weight different for each coefficient.

---

## Links

- Prev: [[L03-08-metropolis-hastings-hmc]] (Stan's NUTS fitted the hospital model); next: priors that
  shrink noise and leave signals alone, [[L03-10-sparsity-priors]]. Formulas: [[L03-11-formulas]];
  pitfalls: [[L03-12-pitfalls]]; code: [[L03-13-python]] §9.
- Later: hierarchical models, Tobit and probit in Class 7 (G §8.1–8.2 in the Class 7 readings).
- Rules: [[../../rules/07_bayes|rules/07]], [[../../rules/08_monte_carlo_mcmc|rules/08]];
  random effects and panels, [[../../rules/03_painel_did|rules/03]].
- Practice (statements in the books): **G 8.1** (p. 132, Gibbs regression on birth-weight data), **G 4.7**
  (p. 59, an exchangeable but dependent urn; background).
