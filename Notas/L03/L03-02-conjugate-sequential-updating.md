---
tags: [notes, lecture-03, conjugacy, beta-bernoulli, gamma-poisson, pareto-uniform, predictive, sequential-updating, large-samples]
date: 2026-10-27
status: taught
source: "sequential-bayes-bernoulli-uniform-trials.html (Beta–Binomial and Pareto–Uniform sections); notas-bayesianas-slides.pdf slides 4–5 (Exp–Gamma); Greenberg 1e §2.2 (pp. 15–18, (2.4)–(2.5), Fig. 2.2), §3.1.3 (pp. 24–25), §3.1.4 (pp. 25–27, (3.2)), §3.2.3 (pp. 32–33); Bolfarine & Sandoval (2010) Ex. 4.4.1–4.4.2 (pp. 65–68), Ex. 5.5.2 (pp. 86–87, (5.5.2)–(5.5.3)); Tsay AFTS 3e §12.3.2 Results 12.3–12.6 (pp. 620–621)"
---

# Site page "Sequential Bayesian Learning", G §2.2, §3.1.3–3.1.4, §3.2.3 · Conjugate updating: the posterior adds the data to the prior's pseudo-data

> **Claim.** For a conjugate pair the posterior is the prior's family with **updated parameters**,
> and the update is a count: the Beta prior adds successes and failures, the Gamma prior adds events
> and exposure, the Pareto prior raises its lower bound to the sample maximum and adds $n$ to its
> shape. The posterior mean is a **weighted average** of the prior mean and the MLE, with the prior's
> weight falling like $1/n$. Because the update is a count, updating in batches or one observation at
> a time gives the same posterior. The **predictive** probability that the next Bernoulli trial
> succeeds equals the posterior mean of $\theta$. With a uniform prior the posterior **mode is the MLE**
> $s/n$; the mean $(1+s)/(2+n)$ is not.
> Prev: [[L03-01-bayes-rule-discrete]] · Next: [[L03-03-normal-measurement-physicists]] · Map: [[L03-00-map]]

**Notation.**

| Symbol | Meaning | Range / value |
|---|---|---|
| $x_1,\dots,x_n$ | data (Bernoulli, Poisson, exponential or uniform) | — |
| $s_n=\sum x_i$ | successes (Bernoulli) or total count (Poisson) | $0,\dots,n$ / $0,1,\dots$ |
| $\alpha_0,\beta_0$ | Beta prior parameters (Greenberg's $\alpha,\beta$; Bolfarine's $a,b$) | $>0$ |
| $\alpha_1,\beta_1$ | posterior parameters | $>0$ |
| $x_{(n)}$ | sample maximum | $>0$ |
| $\theta_0,\alpha_0$ (Pareto) | Pareto lower bound and shape | $>0$ |
| $B(a,b)$ | Beta function $\Gamma(a)\Gamma(b)/\Gamma(a+b)$ | — |

---

## 1 · U — the prior as data seen earlier

Greenberg's reading (p. 17): in a Beta$(\alpha_0,\beta_0)$ prior, $\alpha_0$ is "the number of heads
obtained in the experiment on which the prior is based" and $\beta_0$ the number of tails. After the
data, the posterior is what you would have believed had you seen both experiments. This is why
conjugate updating is sequential by construction, and why a prior can be judged by asking **how many
observations it is worth** ($\alpha_0+\beta_0$ for the Beta, $\beta_0$ periods of exposure for the
Gamma, as in [[../L01/L01-04-first-bayesian-poisson|L01-04]] where the Exp(1/2) prior was worth half
a year).

---

## 2 · C — Beta–Bernoulli (G §2.2; site page §1; B Ex. 4.4.1)

**Likelihood (Greenberg (2.4)).** For $n$ independent tosses,

$$p(x_1,\dots,x_n\mid\theta)=\prod_{i=1}^n\theta^{x_i}(1-\theta)^{1-x_i}=\theta^{s_n}(1-\theta)^{n-s_n}.\tag{1}$$

**Prior.** $\theta\sim\text{Beta}(\alpha_0,\beta_0)$:

$$p(\theta)=\frac{\theta^{\alpha_0-1}(1-\theta)^{\beta_0-1}}{B(\alpha_0,\beta_0)},\quad E(\theta)=\frac{\alpha_0}{\alpha_0+\beta_0},\quad V(\theta)=\frac{\alpha_0\beta_0}{(\alpha_0+\beta_0)^2(\alpha_0+\beta_0+1)},\quad\text{Mode}=\frac{\alpha_0-1}{\alpha_0+\beta_0-2}.\tag{2}$$

**Posterior.** Substitute (1) and (2) into $p(\theta\mid x)\propto p(x\mid\theta)p(\theta)$
([[L03-01-bayes-rule-discrete]] (6)), dropping $B(\alpha_0,\beta_0)$:

$$p(\theta\mid x)\ \propto\ \big(\theta^{s_n}(1-\theta)^{n-s_n}\big)\big(\theta^{\alpha_0-1}(1-\theta)^{\beta_0-1}\big)=\theta^{(\alpha_0+s_n)-1}(1-\theta)^{(\beta_0+n-s_n)-1}.\tag{3}$$

(3) is a Beta kernel:

$$\theta\mid x\ \sim\ \text{Beta}(\alpha_1,\beta_1),\qquad \alpha_1=\alpha_0+s_n,\quad\beta_1=\beta_0+n-s_n.\tag{4}$$

**Posterior mean as a weighted average (Greenberg (2.5)).** By (2) applied to (4),

$$E(\theta\mid x)=\frac{\alpha_0+s_n}{\alpha_0+\beta_0+n}.\tag{5}$$

Split the numerator into $\alpha_0$ and $s_n=n\bar x$:

$$E(\theta\mid x)=\underbrace{\frac{\alpha_0+\beta_0}{\alpha_0+\beta_0+n}}_{w}\cdot\frac{\alpha_0}{\alpha_0+\beta_0}+\underbrace{\frac{n}{\alpha_0+\beta_0+n}}_{1-w}\cdot\bar x.\tag{6}$$

*Check:* the first product is $\alpha_0/(\alpha_0+\beta_0+n)$, the second $s_n/(\alpha_0+\beta_0+n)$; they add to (5).

**Greenberg's Fig. 2.2 in numbers** (prior Beta(2,2), mean 0.5):

| Data | Posterior (4) | $w$ in (6) | $E(\theta\mid x)$ by (6) | MLE |
|---|---|---|---|---|
| $n=10$, $s=3$ | Beta(5, 9) | $4/14=0.2857$ | $0.2857(0.5)+0.7143(0.3)=0.1429+0.2143=0.3571$ | 0.3 |
| $n=50$, $s=15$ | Beta(17, 37) | $4/54=0.0741$ | $0.0741(0.5)+0.9259(0.3)=0.0370+0.2778=0.3148$ | 0.3 |

The same proportion of heads, five times the data: the prior's weight falls from 29% to 7%.

**Uniform prior (site page; B (4.4.10)–(4.4.11)).** $\alpha_0=\beta_0=1$ in (4)–(5) and (2):

$$\theta\mid x\sim\text{Beta}(1+s_n,1+n-s_n),\quad E(\theta\mid x)=\frac{1+s_n}{2+n},\quad\text{Mode}(\theta\mid x)=\frac{(1+s_n)-1}{(2+n)-2}=\frac{s_n}{n}=\hat\theta_{MLE},\tag{7}$$

$$V(\theta\mid x)=\frac{(1+s_n)(1+n-s_n)}{(2+n)^2(3+n)}.\tag{8}$$

With $s=1$ in $n=10$ (the sample of [[../L01/L01-01-likelihood-sampling-rules|L01-01]]): mode 0.100,
mean $2/12=0.167$, posterior sd $\sqrt{2\times10/(144\times13)}=0.103$.

![Three panels; the middle panel shows the Beta(2,2) prior, the dotted normalised likelihoods and the Beta(5,9) and Beta(17,37) posteriors with means 0.357 and 0.315; the right panel shows the Pareto posterior median and 10-90 percent band for theta against n from 5 to 50 for a seeded U(0,2) sample, above the running maximum and below the true value 2.](figures/L03-sequential-learning.png)
*Middle: Greenberg Fig. 2.2 recomputed from (4). Right: Pareto–Uniform update (13) on a seeded $U(0,2)$ sample, prior Pareto$(1.5,\,0.1)$ as on the site page. Left panel: [[L03-01-bayes-rule-discrete]] §5.*

In the middle panel each dotted likelihood (normalised to integrate to one) sits almost on top of its
posterior; the prior only nudges the posterior toward 0.5, and less so for $n=50$. That is (6) seen as
densities: posterior $\approx$ likelihood when $w$ is small.

---

## 3 · C — sequential updating is exact (G §3.1.3, p. 25)

First experiment: $n_1$ trials, $s_1$ successes. By (4) the posterior is
Beta$(\alpha_0+s_1,\ \beta_0+n_1-s_1)$. Use it as the prior for the second experiment ($n_2$, $s_2$) and
apply (4) again:

$$\theta\mid s_1,s_2\sim\text{Beta}\big((\alpha_0+s_1)+s_2,\ (\beta_0+n_1-s_1)+(n_2-s_2)\big)=\text{Beta}\big(\alpha_0+(s_1+s_2),\ \beta_0+(n_1+n_2)-(s_1+s_2)\big),\tag{9}$$

which is the posterior from Beta$(\alpha_0,\beta_0)$ and all $n_1+n_2$ trials at once. The site page's
recursion `alphan = cumsum(x)+1; betan = 2:(n+1)-cumsum(x)` is (9) applied one trial at a time.

> **The order and grouping of the data do not matter; only the sufficient statistic does.** This is
> [[L03-01-bayes-rule-discrete]] (9) for a continuous $\theta$.

---

## 4 · C — the predictive probability of the next trial (G §3.2.3, pp. 32–33)

Introduce $\theta$ and integrate it out:

$$P(x_{n+1}=1\mid x)=\int_0^1P(x_{n+1}=1\mid\theta)\,p(\theta\mid x)\,d\theta=\int_0^1\theta\,\frac{\theta^{\alpha_1-1}(1-\theta)^{\beta_1-1}}{B(\alpha_1,\beta_1)}\,d\theta.\tag{10}$$

The integrand is the Beta$(\alpha_1+1,\beta_1)$ kernel, whose integral is $B(\alpha_1+1,\beta_1)$:

$$P(x_{n+1}=1\mid x)=\frac{B(\alpha_1+1,\beta_1)}{B(\alpha_1,\beta_1)}=\frac{\Gamma(\alpha_1+1)\Gamma(\alpha_1+\beta_1)}{\Gamma(\alpha_1)\Gamma(\alpha_1+\beta_1+1)}=\frac{\alpha_1}{\alpha_1+\beta_1}=\frac{\alpha_0+s_n}{\alpha_0+\beta_0+n},\tag{11}$$

using $\Gamma(a+1)=a\Gamma(a)$ twice. (11) equals the posterior mean (5): for a Bernoulli variable
$E(x\mid\theta)=P(x=1\mid\theta)=\theta$. With $\alpha_0=\beta_0=1$, (11) is Laplace's rule of
succession $(s_n+1)/(n+2)$. For Fig. 2.2's first case, $5/14=0.357$.

> **The predictive averages the model over the posterior; it does not plug in an estimate.** Plugging
> in the MLE would give $s_n/n$, which is 0 after $n$ failures, a forecast of certainty that no finite
> sample justifies.

---

## 5 · C — Gamma–Poisson and Gamma–Exponential (T Results 12.4–12.5; B Ex. 4.4.2; deck slides 4–5)

With a Gamma$(\alpha_0,\beta_0)$ prior (shape, rate), $p(\lambda)\propto\lambda^{\alpha_0-1}e^{-\beta_0\lambda}$:

| Data | Likelihood kernel | Posterior | Posterior mean |
|---|---|---|---|
| Poisson$(\lambda)$ | $\lambda^{s_n}e^{-n\lambda}$ | Gamma$(\alpha_0+s_n,\ \beta_0+n)$ | $\dfrac{\alpha_0+s_n}{\beta_0+n}$ |
| Exponential$(\theta)$, density $\theta e^{-\theta x}$ | $\theta^ne^{-\theta\sum x_i}$ | Gamma$(\alpha_0+n,\ \beta_0+\sum x_i)$ | $\dfrac{\alpha_0+n}{\beta_0+\sum x_i}$ |

Each row is (3) with a Gamma kernel: multiply the kernels and add exponents. The Poisson row is Tsay's
Result 12.4 and Bolfarine's Ex. 4.4.2; the exponential row is Result 12.5 and the "Modelo
Exponencial-Gama" of the Bayes-estimator deck (slides 4–5), used in [[L03-04-bayes-estimators-loss]].
L01-04's coal example is the Poisson row with $\alpha_0=1$, $\beta_0=1/2$, $n=41$, $s_n=127$:
Gamma(128, 41.5), mean $128/41.5=3.084$.

---

## 6 · C — Pareto–Uniform (site page §2; B Ex. 5.5.2)

**Likelihood.** For $x_i\sim U(0,\theta)$ iid,

$$p(x_1,\dots,x_n\mid\theta)=\prod_{i=1}^n\frac1\theta I(x_i\le\theta)=\frac1{\theta^n}I(x_{(n)}\le\theta).\tag{12}$$

The likelihood is zero below the sample maximum and decreasing above it, so $\hat\theta_{MLE}=x_{(n)}$
(the boundary MLE of [[../L01/L01-05-comparing-estimators-mse-bootstrap|L01-05]]).

**Prior.** Pareto$(\theta_0,\alpha_0)$: $p(\theta)=\alpha_0\theta_0^{\alpha_0}\theta^{-(\alpha_0+1)}$ for
$\theta\ge\theta_0$, zero below. (The site page types the numerator as $\alpha_0\theta_0^\alpha$ and adds a
stray $a$ in the denominator.)

**Posterior.** Multiply (12) by the prior and keep the factors in $\theta$:

$$p(\theta\mid x)\ \propto\ \Big(\frac1{\theta^n}I(\theta\ge x_{(n)})\Big)\Big(\frac1{\theta^{\alpha_0+1}}I(\theta\ge\theta_0)\Big)=\frac1{\theta^{(\alpha_0+n)+1}}\,I\big(\theta\ge\max\{x_{(n)},\theta_0\}\big).\tag{13}$$

(13) is a Pareto kernel:

$$\theta\mid x\sim\text{Pareto}(\theta_1,\alpha_1),\qquad\theta_1=\max\{x_{(n)},\theta_0\},\quad\alpha_1=\alpha_0+n.\tag{14}$$

**Summaries.** For Pareto$(\theta_1,\alpha_1)$:

$$E(\theta\mid x)=\frac{\alpha_1\theta_1}{\alpha_1-1}\ (\alpha_1>1),\qquad\text{Median}=\theta_12^{1/\alpha_1},\qquad V(\theta\mid x)=\frac{\theta_1^2\alpha_1}{(\alpha_1-1)^2(\alpha_1-2)}\ (\alpha_1>2).\tag{15}$$

The mean follows from $\int_{\theta_1}^\infty\theta\,\alpha_1\theta_1^{\alpha_1}\theta^{-\alpha_1-1}d\theta=\alpha_1\theta_1^{\alpha_1}\theta_1^{1-\alpha_1}/(\alpha_1-1)$.
The site page's text writes $E(\theta\mid x)=\theta_1\alpha_1/(\alpha_1+1)$, which is smaller than $\theta_1$
and so outside the support; its code uses (15).

**Worked (seeded sample).** The site page draws $n=50$ from $U(0,2)$ with prior Pareto(1.5, 0.1).
Python cannot replay R's seed, so the notes use a seeded NumPy sample with the same design:
$x_{(50)}=1.8923$, so by (14) $\theta_1=\max\{1.8923,1.5\}=1.8923$ and $\alpha_1=0.1+50=50.1$. By (15):

$$E(\theta\mid x)=\frac{50.1\times1.8923}{49.1}=1.9308,\qquad\text{Median}=1.8923\times2^{1/50.1}=1.9186.$$

The 5% and 95% posterior quantiles are $\theta_1(0.95)^{-1/\alpha_1}=1.8942$ and
$\theta_1(0.05)^{-1/\alpha_1}=2.0089$; the true $\theta=2$ lies inside.

> **The posterior never goes below the data's maximum, and the MLE never goes above it.** Every
> posterior summary sits at or above $x_{(n)}$, which is the bias correction the frequentist
> $\frac{n+1}{n}x_{(n)}$ of L01-05 makes by hand. The right panel of the figure shows the band hugging
> $x_{(n)}$ from above and narrowing like $1/n$.

**Bayesian interval (B Ex. 5.5.2, (5.5.3)).** For coverage $1-\epsilon$ (Bolfarine's $\gamma=1-\alpha$),
solving $P(\theta\le t_1\mid x)=\epsilon/2$ and $P(\theta\ge t_2\mid x)=\epsilon/2$ with the Pareto cdf
$1-(\theta_1/t)^{\alpha_1}$ gives the equal-tail interval
$\big[\theta_1(1-\epsilon/2)^{-1/\alpha_1},\ \theta_1(\epsilon/2)^{-1/\alpha_1}\big]$ (with $\epsilon=0.10$, the
1.8942–2.0089 above). It is not the HPD interval, which here starts at $\theta_1$ because the density is
decreasing.

---

## 7 · C — large samples (G §3.1.4, pp. 25–27)

Write the posterior as $p(\theta\mid y)\propto p(\theta)\exp[n\bar l(\theta\mid y)]$, where $\bar l$ is the
mean log-likelihood contribution. A second-order expansion of $\bar l$ around the MLE $\hat\theta$, where
the first derivative vanishes, gives

$$p(\theta\mid y)\ \approx\ p(\theta)\exp\Big[-\frac{n}{2v}(\theta-\hat\theta)^2\Big],\qquad v=[-\bar l''(\hat\theta\mid y)]^{-1},\tag{16}$$

so for large $n$ the posterior is approximately $N(\hat\theta,v/n)$, provided **$p(\hat\theta)\ne0$**.
Three consequences (Greenberg p. 27): the prior's role shrinks; the posterior concentrates at the
true value (the Bayesian counterpart of consistency); and it is approximately normal around the MLE.
For the Beta–Bernoulli, (8) gives $V(\theta\mid x)\approx\bar x(1-\bar x)/n$, the inverse Fisher
information of L01-01. The proviso matters for the Pareto prior: a lower bound $\theta_0$ above the
true $\theta$ gives the true value zero posterior probability for every $n$.

---

## 8 · G — other conjugate pairs (named)

Dirichlet–multinomial (G §3.1.2, pp. 23–24): $D(\alpha)$ prior, posterior $D(\alpha+y)$, marginal of
$\theta_1$ a Beta. Beta–negative binomial (T Result 12.6, p. 621). Normal–normal and
normal–inverse-gamma: [[L03-03-normal-measurement-physicists]]. Inverse chi-squared for a variance
(T Result 12.8): used inside the Gibbs samplers of [[L03-07-markov-chains-gibbs]].

---

## Links

- Prev: [[L03-01-bayes-rule-discrete]]; next: the normal model, where the weight $w$ becomes a ratio of
  variances, [[L03-03-normal-measurement-physicists]]. Point estimates from these posteriors:
  [[L03-04-bayes-estimators-loss]]. Formulas: [[L03-11-formulas]]; code: [[L03-13-python]] §2.
- Earlier: Exp–Gamma on the coal data, [[../L01/L01-04-first-bayesian-poisson|L01 §4]]; the $U(0,\theta)$
  estimators, [[../L01/L01-05-comparing-estimators-mse-bootstrap|L01 §5]].
- Rules: [[../../rules/07_bayes|rules/07]] (conjugate families, sequential updating).
- Practice (statements in the books): **G 2.2** (p. 19, gamma–Poisson), **G 2.4** (p. 19,
  Pareto–uniform), **G 3.2** (p. 39, Poisson predictive), **G 3.4** (p. 39, sequential Poisson
  updating), **B 4.10** (p. 72, Pareto prior for $U(0,\theta)$), **T 12.1** (p. 670).
