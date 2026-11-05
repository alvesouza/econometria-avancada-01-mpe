---
tags: [notes, lecture-03, sparsity, ridge, lasso, horseshoe, normal-gamma, scale-mixture, shrinkage, bayesian-lasso, spike-and-slab]
date: 2026-10-29
status: taught
source: "sparse-priors.pdf (9 image pages: Carvalho, Polson & Scott 2010, Biometrika 97, §1.1 and Table 1/Fig. 2 (p. 468), Table 4 (p. 477, Vanguard funds); Griffin & Brown 2010, Bayesian Analysis 5, (1)–(3), Fig. 1, §5.3 Table 3, Fig. 7); sparseregression-simulation.pdf + sparseregression-simulation-R.txt (bayesreg: ridge, lasso, horseshoe); Izbicki & Mendonça (2020) §3.6 (pp. 42–43); ISLP §6.2 (pp. 240–251, (6.5), (6.7), Fig. 6.11)"
---

# Sparse-priors deck, sparse-regression simulation, AME §3.6, I §6.2 · Sparsity priors: shrink the noise, leave the signals alone

> **Claim.** With many coefficients and few of them non-zero, the prior should pull small estimates
> hard toward zero and leave large ones almost untouched. A normal prior cannot: its posterior mean is
> $y$ times a constant (ridge, which is the posterior **mode** under a Gaussian prior, as lasso is under
> a Laplace prior). **Scale mixtures of normals** give each coefficient its own variance. The
> **horseshoe** (half-Cauchy local scales) puts a Beta(1/2, 1/2) prior on the shrinkage factor
> $\kappa=1/(1+\lambda^2)$, with mass at both ends: $\kappa\approx1$ kills noise, $\kappa\approx0$ keeps signals. With
> $y\mid\theta\sim N(\theta,1)$ and $\tau=1$, an observation $y=6$ is estimated at **5.66** under the horseshoe, **4.59** under a
> Laplace prior of the same variance and **3** under the normal prior. In the lecturer's simulation
> ($n=200$, 3 signals among 50 coefficients) the horseshoe's null estimates are about **8 times**
> closer to zero than ridge's, with the signals equally well estimated.
> Prev: [[L03-09-hierarchical-models-shrinkage]] · Next: [[L03-11-formulas]] · Map: [[L03-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $\beta_j$ / $\theta_i$ | regression coefficient / normal mean | $\mathbb R$ |
| $\Psi_j$, $\lambda_j^2$ | coefficient-specific (local) variance | $>0$ |
| $\tau$ | global scale | $>0$ |
| $\kappa_i=1/(1+\lambda_i^2)$ | shrinkage factor (with $\sigma=\tau=1$) | $(0,1)$ |
| $C^+(0,a)$ | half-Cauchy with scale $a$ | — |
| $\text{Ga}(c,d)$ | gamma, shape $c$, rate $d$ (Griffin–Brown) | — |
| $\lambda$ (ridge/lasso) | penalty weight | $\ge0$ |

---

## 1 · U — the problem with one variance for everyone

A normal prior $\beta_j\sim N(0,v)$ shrinks every OLS coefficient by the same factor. If $v$ is small enough to
silence 97 null coefficients, it also drags the three real ones toward zero; if it is large enough to
spare the signals, it lets the noise through. Griffin and Brown (deck p. 5): a zero-mean normal prior
"performs poorly if there are large differences in the size of regression coefficients". The fix is to
let each coefficient carry its own variance, drawn from a distribution with **a lot of mass near zero
and heavy tails**.

---

## 2 · C — ridge and lasso as posterior modes (AME §3.6; I pp. 250–251)

Let $y_i\mid x_i,\beta\sim N(\beta'x_i,\sigma^2)$ with $\sigma^2$ known. The log posterior is the log-likelihood plus the log
prior:

$$\log\pi(\beta\mid y)=-\frac1{2\sigma^2}\sum_i(y_i-\beta'x_i)^2+\log\pi(\beta)+c.\tag{1}$$

**Gaussian prior** $\beta_j\stackrel{iid}{\sim}N(0,\tau^2)$: $\log\pi(\beta)=-\sum_j\beta_j^2/(2\tau^2)+c$. Multiply (1) by $-2\sigma^2$: maximising the posterior
is minimising

$$\sum_i(y_i-\beta'x_i)^2+\frac{\sigma^2}{\tau^2}\sum_j\beta_j^2,\tag{2}$$

the ridge criterion (I (6.5), p. 240) with $\lambda=\sigma^2/\tau^2$. The posterior is normal, so mode = mean.

**Laplace prior** $\pi(\beta_j)=\frac1{2b}e^{-|\beta_j|/b}$: $\log\pi(\beta)=-\sum_j|\beta_j|/b+c$, and the same step gives

$$\sum_i(y_i-\beta'x_i)^2+\frac{2\sigma^2}{b}\sum_j|\beta_j|,\tag{3}$$

the lasso criterion (I (6.7), p. 244) with $\lambda=2\sigma^2/b$. AME (p. 42): "under the Bayesian approach, the
tuning parameter $\lambda$ is defined by the prior distribution"; a tighter prior means a larger $\lambda$, and
choosing $\lambda$ by cross-validation "is equivalent to choosing the prior that gives the best predictive
power". Two cautions: the lasso's zeros are a property of the **mode**; the posterior **mean** under a
Laplace prior is never exactly zero. And the ISLP Fig. 6.11 picture makes the shapes plain: the
Laplace density has a sharp peak at 0, the normal a rounded one.

---

## 3 · C — scale mixtures of normals (Griffin–Brown §3, deck pp. 5–7)

$$\pi(\beta_j)=\int N(\beta_j\mid0,\Psi_j)\,dG(\Psi_j)\qquad\Longleftrightarrow\qquad\beta_j\mid\Psi_j\sim N(0,\Psi_j),\ \ \Psi_j\sim G.\tag{4}$$

Every such prior has heavier-than-normal tails (unless $G$ is a point mass). Special cases:

| Mixing distribution $G$ | Prior on $\beta_j$ |
|---|---|
| point mass at $v$ | normal (ridge) |
| $z_j\delta_{\sigma_\beta^2}+(1-z_j)\delta_0$, $P(z_j=1)=w$ | spike-and-slab: $w\,N(0,\sigma_\beta^2)+(1-w)\,\delta_0$ |
| exponential | double exponential (Bayesian lasso, Park and Casella 2008) |
| $\text{Ga}(\lambda,\ 1/(2\gamma^2))$ | normal–gamma |
| $\Psi_j=\lambda_j^2\tau^2$, $\lambda_j\sim C^+(0,1)$ | horseshoe |

(4) is the composition idea of [[L03-06-monte-carlo-simulation]] §4: the Student-$t$ was the case
$\Psi\sim$ inverse-gamma. It also makes Gibbs sampling easy: given the $\Psi_j$, the coefficients are normal.

**Normal–gamma moments.** With $\Psi\sim\text{Ga}(\lambda,1/(2\gamma^2))$, $E\Psi=2\lambda\gamma^2$ and $V\Psi=\lambda(2\gamma^2)^2$. By (4),

$$V(\beta)=E[V(\beta\mid\Psi)]=E\Psi=2\lambda\gamma^2,\qquad E\beta^4=E[3\Psi^2]=3\big[\lambda(2\gamma^2)^2+\lambda^2(2\gamma^2)^2\big],\tag{5}$$

so the kurtosis is $E\beta^4/V(\beta)^2=3(\lambda+\lambda^2)/\lambda^2=3+3/\lambda$: excess kurtosis $3/\lambda$, Griffin and Brown's
statement. As $\lambda$ falls, the prior "place[s] a lot of mass close to zero but at the same time [has]
heavy tails" (their Fig. 1: variance 2 with $\lambda=0.1,\ 0.333,\ 1$). A simulation check with $\lambda=0.333$ and
unit variance: sample excess kurtosis 8.9 against $3/0.333=9.0$. $\lambda=1$ is the Bayesian lasso.

---

## 4 · C — the horseshoe (Carvalho, Polson and Scott 2010, deck pp. 1–2)

For $y\mid\theta\sim N_p(\theta,\sigma^2I)$:

$$\theta_i\mid\lambda_i\sim N(0,\lambda_i^2),\qquad\lambda_i\mid\tau\sim C^+(0,\tau),\qquad\tau\mid\sigma\sim C^+(0,\sigma),\qquad p(\sigma^2)\propto1/\sigma^2.\tag{6}$$

"Each $\theta_i$ is mixed over its own $\lambda_i$, and each $\lambda_i$ has a half-Cauchy prior with common scale $\tau$."

**Posterior mean as shrinkage.** Fix $\sigma=\tau=1$. Given $\lambda_i$, the normal–normal update
([[L03-03-normal-measurement-physicists]] (8)) with prior variance $\lambda_i^2$ and data variance 1 gives
$E(\theta_i\mid y,\lambda_i)=(1-\kappa_i)y_i$ with $\kappa_i=1/(1+\lambda_i^2)$. Averaging over $\lambda_i\mid y$:

$$E(\theta_i\mid y)=\int_0^1(1-\kappa_i)\,y_i\,p(\kappa_i\mid y)\,d\kappa_i=\{1-E(\kappa_i\mid y)\}\,y_i.\tag{7}$$

$E(\kappa_i\mid y)$ "can be interpreted as the amount of shrinkage toward zero, a posteriori".

**Why "horseshoe".** With $\lambda\sim C^+(0,1)$, $p(\lambda)=\frac2{\pi(1+\lambda^2)}$. Change variables to $\kappa=1/(1+\lambda^2)$:
$\lambda=\sqrt{(1-\kappa)/\kappa}$ and $|d\lambda/d\kappa|=\frac12\kappa^{-3/2}(1-\kappa)^{-1/2}$. Substitute, using $1+\lambda^2=1/\kappa$:

$$p(\kappa)=\frac{2}{\pi}\,\kappa\cdot\frac12\kappa^{-3/2}(1-\kappa)^{-1/2}=\frac1\pi\kappa^{-1/2}(1-\kappa)^{-1/2},\tag{8}$$

the Beta(1/2, 1/2) density, U-shaped like a horseshoe. "The left side of the horseshoe, $\kappa_i\approx0$, yields
virtually no shrinkage, and describes signals. The right side, $\kappa_i\approx1$, yields near-total shrinkage and
describes noise."

**The posterior of $\kappa$.** Since $y_i\mid\kappa_i\sim N(0,1+\lambda_i^2)=N(0,1/\kappa_i)$, the likelihood is $\kappa_i^{1/2}e^{-\kappa_iy_i^2/2}$; times
(8):

$$p(\kappa_i\mid y)\propto(1-\kappa_i)^{-1/2}\,e^{-\kappa_iy_i^2/2}.\tag{9}$$

Small $|y_i|$: (9) keeps the pole at $\kappa=1$, so $E(\kappa\mid y)$ is near 1 and $\theta$ is shrunk hard. Large $|y_i|$: the
exponential kills $\kappa$ away from 0 and $E(\kappa\mid y)\to0$: the signal is left alone.

**Other priors through $\kappa$ (CPS Table 1, Fig. 2).** Double exponential: $p(\kappa)\propto\kappa^{-2}e^{-1/(2\kappa)}$, which
vanishes at $\kappa=0$, so even large signals keep some shrinkage. Cauchy: $\kappa^{-1/2}(1-\kappa)^{-3/2}e^{-\kappa/(2(1-\kappa))}$.
Strawderman–Berger: $\kappa^{-1/2}$. Normal–Jeffreys: $\kappa^{-1}(1-\kappa)^{-1}$ (improper at both ends). Only the
horseshoe is unbounded at both ends and integrable.

---

## 5 · Worked — shrinkage profiles

$y\mid\theta\sim N(\theta,1)$, three priors with unit variance where defined: normal $N(0,1)$; Laplace with
$b=1/\sqrt2$ (variance $2b^2=1$); horseshoe with $\tau=1$ and $\tau=0.1$. Posterior means by quadrature of (7)–(9):

| $y$ | Normal: $y/2$ | Laplace | Horseshoe $\tau=1$ |
|---|---|---|---|
| 2 | 1.000 | 0.904 | 1.063 |
| 6 | 3.000 | 4.586 | 5.656 |
| large | $y/2$ | $\approx y-\sqrt2$ | $\to y$ |

For large $y$ the Laplace prior subtracts a constant $1/b=\sqrt2$ (the slope of its log density), so big
signals stay biased by 1.41; the horseshoe's bias vanishes.

![Right panel of the shrinkage figure: posterior mean of theta against y from 0 to 8; the normal-prior line y/2, the Laplace curve approaching a line parallel to the 45-degree line about 1.4 below it, the horseshoe tau = 1 curve close to the 45-degree line from y = 4, and the horseshoe tau = 0.1 curve near zero up to y = 2.5 then rising steeply to meet the 45-degree line near y = 6. Left panel: hospital rates and their hierarchical posterior means.](figures/L03-shrinkage.png)
*Right: $E(\theta\mid y)$ under the four priors (quadrature of (7)–(9) and of the Laplace posterior). Left: [[L03-09-hierarchical-models-shrinkage]] §4.*

The comparative static in $\tau$: shrinking the global scale to 0.1 makes the horseshoe treat every
$|y|<2.5$ as noise (posterior mean below 10% of $y$ at $y=1$) while still letting $y=6$ through almost
unshrunk. That is the "global–local" design: $\tau$ sets how sparse the vector is believed to be, the
$\lambda_i$ let individual coefficients escape.

---

## 6 · Worked — the sparse-regression simulation (sparseregression-simulation-R.txt)

**Design (the R script).** $n=200$, $k_{max}=100$ standard-normal covariates, $\sigma=0.1$,
$\beta=(1,2,3,0,\dots,0)$, $y=X\beta+\varepsilon$; fit with the first $k\in\{10,20,40,50,100\}$ columns under ridge, lasso and
horseshoe priors (R package `bayesreg`, 1000 burn-in + 1000 draws), and box-plot the posterior draws of
$\beta_1,\beta_2,\beta_3$ and of the nulls. The PDF's boxplots show the three signals estimated to within about
$\pm0.01$ by all three priors, and the null coefficients spread over roughly $\pm0.04$ for ridge and lasso,
noticeably tighter for the horseshoe, more so as $k$ grows.

**NumPy port ([[L03-13-python]] §10).** `bayesreg` is R-only, so the three samplers are written out (no
intercept; the simulated covariates have mean zero). Each is a Gibbs sampler on the scale-mixture
representation (4) with $\beta_j\mid\cdot\sim N(0,\sigma^2D_j)$:

$$\beta\mid\cdot\sim N_k\big(A^{-1}X'y,\ \sigma^2A^{-1}\big),\quad A=X'X+D^{-1};\qquad\sigma^2\mid\cdot\sim IG\Big(\frac{n+k}2,\ \frac{\text{RSS}+\beta'D^{-1}\beta}2\Big).\tag{10}$$

The priors differ only in $D$ and its update:

- **ridge:** $D=\tau^2I$, $\tau\sim C^+(0,1)$, drawn through the auxiliary-variable form
  $\tau^2\mid\xi\sim IG(\frac12,\frac1\xi)$, $\xi\sim IG(\frac12,1)$ (Makalic and Schmidt 2016);
- **Bayesian lasso (Park–Casella):** $D=\text{diag}(\tau_j^2)$, $1/\tau_j^2\mid\cdot\sim\text{InvGauss}\big(\sqrt{\lambda^2\sigma^2/\beta_j^2},\ \lambda^2\big)$,
  $\lambda^2\mid\cdot\sim G(1+k,\ 0.1+\sum_j\tau_j^2/2)$;
- **horseshoe:** $D=\tau^2\text{diag}(\lambda_j^2)$ with $\lambda_j^2\mid\cdot\sim IG\big(1,\ \frac1{\nu_j}+\frac{\beta_j^2}{2\tau^2\sigma^2}\big)$,
  $\tau^2\mid\cdot\sim IG\big(\frac{k+1}2,\ \frac1\xi+\sum_j\frac{\beta_j^2}{2\sigma^2\lambda_j^2}\big)$, $\nu_j\mid\cdot\sim IG(1,1+1/\lambda_j^2)$, $\xi\mid\cdot\sim IG(1,1+1/\tau^2)$.

**Results (1500 draws after 500 burn-in, seeded).** All three priors put the posterior means of
$\beta_1,\beta_2,\beta_3$ within 0.03 of $(1,2,3)$. Median absolute posterior mean over the null coefficients:

| | ridge | lasso | horseshoe |
|---|---|---|---|
| $k=10$ | 0.0055 | 0.0052 | 0.0031 |
| $k=50$ | 0.0046 | 0.0045 | **0.00055** |

With 47 nulls the horseshoe's global scale $\tau$ learns that the vector is sparse and shrinks the noise
eight times harder than ridge, without touching the signals. (A coding trap met on the way: drawing one
gamma variate for the whole vector of $\lambda_j^2$ instead of one per coordinate makes the local scales move
together, and $\tau$ then drifts to zero.)

---

## 7 · Worked — reading the two papers' tables (deck pp. 3, 8–9)

**Vanguard mutual funds (CPS Table 4; Carvalho and Scott 2009).** $n=86$ weekly returns on $p=59$ funds;
out-of-sample prediction with five estimates of the $59\times59$ covariance matrix. Risk relative to Bayesian
model averaging (BMA = 1.00):

| | MLE | Lasso AND | Lasso OR | Horseshoe | BMA |
|---|---|---|---|---|---|
| squared-error loss | 10.63 | 1.25 | 2.12 | **1.07** | 1.00 |
| absolute-error loss | 3.51 | 1.22 | 1.47 | **1.04** | 1.00 |

With $p$ close to $n$ the MLE is useless (ten times the risk). The horseshoe, a single continuous prior,
comes within 4–7% of full model averaging over sparse graphical models and beats both lasso variants.

**NIR spectroscopy (Griffin–Brown §5.3, Table 3).** Predict fat content of 215 meat samples from 100
absorbance channels; training/monitoring/test split 129/43/43; "all data" uses $n=172$, "small" a random 60
(so $p>n$). Test RMSE:

| | All data | Small ($n=60<p$) |
|---|---|---|
| normal–gamma | **1.94** | **2.59** |
| lasso | 3.54 | 3.09 |

The posterior median of the shape $\lambda$ is 0.020 (95% interval 0.016–0.026): far below the lasso's
implicit $\lambda=1$, i.e. a much spikier, heavier-tailed prior (excess kurtosis $3/0.02=150$). Their Fig. 7
shows why: the normal–gamma posterior means are zero almost everywhere with a few large coefficients
around channels 30–40, while the lasso's oscillate across all 100 channels.

---

## 8 · G — spike-and-slab and model selection (named)

The spike-and-slab prior of §3 puts positive probability on exact zeros, so its posterior gives
$P(z_j=1\mid y)$, the probability that variable $j$ is in the model: variable selection as model comparison
([[L03-05-model-comparison-bayes-factors]]) over $2^k$ submodels, sampled by Gibbs on the $z_j$ or by
reversible jump (G §8.3, p. 130). Continuous shrinkage priors (normal–gamma, horseshoe) trade exact zeros
for much easier computation. Large Bayesian VARs (Class 9) use the same priors.

---

## Links

- Prev: [[L03-09-hierarchical-models-shrinkage]] (one common weight per group); next: the unit's
  formula sheet, [[L03-11-formulas]]. Pitfalls: [[L03-12-pitfalls]]; code: [[L03-13-python]] §10.
- Earlier: best subset, AIC/BIC and overfitting, [[../L01/L01-06-gaussian-linear-regression|L01 §6]];
  bias–variance, [[../L02/L02-01-prediction-error-bias-variance|L02 §1]].
- Rules: [[../../rules/07_bayes|rules/07]]; ridge/lasso as frequentist shrinkage, [[../../rules/06_classificacao_validacao|rules/06]].
- Reading: AME §3.6 (pp. 42–43); I §6.2 (pp. 240–251); the slides for the horseshoe and normal–gamma
  (no book on disk).
