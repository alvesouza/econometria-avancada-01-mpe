---
tags: [notes, lecture-01, bayes, poisson, exponential-prior, gamma-posterior, conjugacy, shrinkage, coal-mining]
date: 2026-10-19
status: taught
source: "class1-poisson-with-exponential-prior.pdf (handwritten, pp. 1–4, read as images); class1-poisson.html (1851–1891 data); Greenberg 1e §2.2 (pp. 12–18, (2.1)–(2.5)); Bolfarine & Sandoval (2010) §4.4 (p. 63, Thm 4.4.1; p. 67, Ex. 4.4.2, (4.4.12)) as G-layer link"
---

# First Bayesian example · Exponential prior + Poisson likelihood = Gamma posterior, shrunk toward the prior

> **Claim.** The prior $\lambda\sim$ Exp$(a)$ with $a=1/2$ encodes "about 2 disasters a year,
> variance 4". Multiplied by the Poisson likelihood $\lambda^{s_n}e^{-n\lambda}$, it gives a
> posterior with the kernel $\lambda^{s_n}e^{-(a+n)\lambda}$, which is
> **Gamma$(s_n+1,\ a+n)$**. On the 1851–1891 coal data ($n=41$, $s_n=127$) the posterior mean is
> $128/41.5=\mathbf{3.084}$, the mode $127/41.5=\mathbf{3.060}$ and the sd
> $\sqrt{128}/41.5=\mathbf{0.273}$, against the MLE $127/41=\mathbf{3.098}$. The prior is weak (it
> is worth half a year of data), but it still pulls both summaries **a little to the left of the
> MLE**. That pull is **shrinkage**.
> Prev: [[L01-03-coal-mining-change-point]] · Next: [[L01-05-comparing-estimators-mse-bootstrap]] · Map: [[L01-00-map]]

**Notation.**

| Symbol | Meaning | Range / value |
|---|---|---|
| $\lambda$ | Poisson rate (disasters per year) | $(0,\infty)$ |
| $a$ | rate parameter of the exponential prior | $a>0$; here $1/2$ |
| $y_1,\dots,y_n$ | yearly counts | $n=41$ (1851–1891) |
| $s_n=\sum y_i$ | total count | 127 |
| $p(\lambda)$, $p(\lambda\mid y)$ | prior, posterior density (Greenberg writes $\pi(\cdot)$) | — |
| $G(\alpha,\beta)$ | Gamma with shape $\alpha$ and **rate** $\beta$ | $\alpha,\beta>0$ |
| $\Gamma(\cdot)$ | gamma function, $\Gamma(k+1)=k!$ | — |

---

## 1 · U — some pre-existing knowledge about $\lambda$ (handwritten p. 1)

The page opens with a sketch. Before seeing the data, the researcher thinks $\lambda$ is
probably around 2–3, surely positive, and unlikely above 5. The Bayesian move is to **write that
belief down as a density** and let the data update it. The handwritten notes pick a
deliberately simple shape:

> "An easy to handle density is the Exponential density."

$$p(\lambda\mid a)=a\,e^{-a\lambda},\qquad\lambda>0.\tag{1}$$

(The handwritten page writes the kernel $e^{-a\lambda}$. The normalising factor $a$ is visible in
its p. 4 plot, where the prior starts at $0.5=a$ at $\lambda=0$.) The exponential's shape is not
the hump of the sketch. Its mode is 0. The choice trades shape for algebra, and §5 shows the price
is small here.

**One integral does all the work in this note:**

$$\int_0^\infty\lambda^ke^{-b\lambda}\,d\lambda=\frac{\Gamma(k+1)}{b^{k+1}},\qquad k>-1,\ b>0.\tag{2}$$

*Proof.* Substitute $u=b\lambda$, so $d\lambda=du/b$:
$\int_0^\infty(u/b)^ke^{-u}\,du/b=b^{-(k+1)}\int_0^\infty u^ke^{-u}du=\Gamma(k+1)/b^{k+1}$.

**Prior moments.** Apply (2) with $b=a$, taking $k=1$ for the mean and $k=2$ for the second moment:

$$E(\lambda)=a\cdot\frac{\Gamma(2)}{a^2}=\frac1a,\qquad E(\lambda^2)=a\cdot\frac{\Gamma(3)}{a^3}=\frac2{a^2},\qquad V(\lambda)=\frac2{a^2}-\frac1{a^2}=\frac1{a^2}.\tag{3}$$

> **Calibrating $a$ (handwritten p. 1).** "If we believe $E(\lambda)\approx2$ and are happy with
> $V(\lambda)\approx4$, then $a=1/2$ is a reasonable choice." Indeed (3) gives $1/a=2$ and
> $1/a^2=4$. The prior sd is 2, and the central 95% of the prior runs from
> $-2\log0.975=0.051$ to $-2\log0.025=7.38$. That is a vague statement about the rate.

---

## 2 · C — Bayes' theorem (Greenberg §2.2, pp. 13–14)

For a parameter $\theta$ and data $y$, Greenberg's (2.2) is

$$\pi(\theta\mid y)=\frac{f(y\mid\theta)\pi(\theta)}{f(y)},\qquad f(y)=\int f(y\mid\theta)\pi(\theta)\,d\theta,$$

and, since $f(y)$ does not involve $\theta$, his (2.3) is

$$\pi(\theta\mid y)\ \propto\ f(y\mid\theta)\,\pi(\theta).\tag{4}$$

> **Posterior ∝ likelihood × prior.** The likelihood is "not a p.d.f. for $\theta$" (Greenberg,
> p. 14). It is the data density read as a function of $\theta$, the same object the MLE
> maximises in [[L01-02-poisson-mle-properties]] (5). The prior supplies what the data do not,
> and the normaliser $f(y)$ can be recovered at the end from the kernel's family.

---

## 3 · C — the posterior is Gamma (handwritten p. 2)

"The Bayesian approach allows us to combine different sources of information":

$$\text{Likelihood: }\ L(\lambda\mid y_1,\dots,y_n)\ \propto\ \lambda^{s_n}e^{-n\lambda},\tag{5}$$

$$\text{Prior: }\ p(\lambda)\ \propto\ e^{-a\lambda}.$$

The likelihood is [[L01-02-poisson-mle-properties]] (5) without its constant; the prior is (1)
without its constant $a$.

Substitute both into (4):

$$p(\lambda\mid y)\ \propto\ \big(\lambda^{s_n}e^{-n\lambda}\big)\big(e^{-a\lambda}\big)=\lambda^{s_n}e^{-(a+n)\lambda}.\tag{6}$$

**Normalise.** By (2) with $k=s_n$ and $b=a+n$, the area under the kernel (6) is
$\Gamma(s_n+1)/(a+n)^{s_n+1}$. Divide by it:

$$p(\lambda\mid y)=\frac{(a+n)^{s_n+1}}{\Gamma(s_n+1)}\,\lambda^{(s_n+1)-1}e^{-(a+n)\lambda}.\tag{7}$$

Compare with the Gamma density on the handwritten p. 3,
$X\sim G(\alpha,\beta)\iff p(x)=\frac{\beta^\alpha}{\Gamma(\alpha)}x^{\alpha-1}e^{-\beta x}$:
(7) is that density with $\alpha=s_n+1$ and $\beta=a+n$.

$$\boxed{(\lambda\mid y_1,\dots,y_n)\ \sim\ G(s_n+1,\ a+n)}\tag{8}$$

> **Conjugacy, read off the parameters.** The prior Exp$(a)=G(1,a)$ is a Gamma. The posterior adds
> the **event count $s_n$ to the shape** and the **exposure $n$ to the rate**. So the prior acts
> like **1 disaster observed over $a=0.5$ years** of earlier data. This is Greenberg's reading of
> the beta prior's $\alpha_0,\beta_0$ as prior "heads" and "tails" (p. 17), transposed to counts.

---

## 4 · C — posterior summaries (handwritten p. 3)

The Gamma facts on the handwritten p. 3 follow from (2) exactly as (3) did:

$$E(X)=\frac\alpha\beta,\qquad V(X)=\frac{\alpha}{\beta^2},\qquad \text{Mode}(X)=\frac{\alpha-1}{\beta}\ \ (\alpha\ge1).\tag{9}$$

The mode comes from setting the derivative of $\log p(x)=(\alpha-1)\log x-\beta x+\text{const}$ to zero:
$(\alpha-1)/x-\beta=0$.

Substitute $\alpha=s_n+1$, $\beta=a+n$ from (8) into (9), then put $a=1/2$:

$$E(\lambda\mid y)=\frac{s_n+1}{a+n}\stackrel{a=1/2}{=}\frac{s_n+1}{n+1/2},\tag{10}$$

$$\text{Mode}(\lambda\mid y)=\frac{(s_n+1)-1}{a+n}=\frac{s_n}{a+n}\stackrel{a=1/2}{=}\frac{s_n}{n+1/2},\tag{11}$$

$$V(\lambda\mid y)=\frac{s_n+1}{(a+n)^2}\stackrel{a=1/2}{=}\frac{s_n+1}{(n+1/2)^2}.\tag{12}$$

---

## 5 · Worked — coal mining, 1851–1891 (handwritten pp. 3–4)

The data are the 41 counts on the site's R page (`class1-poisson.html`): $n=41$, $s_n=127$
(mean 3.097561). Substitute into (10)–(12):

$$E(\lambda\mid n,s_n)=\frac{127+1}{41+0.5}=\frac{128}{41.5}=3.0843\approx\mathbf{3.084},$$

$$\text{Mode}(\lambda\mid n,s_n)=\frac{127}{41.5}=3.0602\approx\mathbf{3.060},$$

$$\sqrt{V(\lambda\mid n,s_n)}=\frac{\sqrt{128}}{41.5}=\frac{11.3137}{41.5}=0.2726\approx\mathbf{0.273}.$$

"Recall that"

$$\hat\lambda_{MLE}=\frac{s_n}{n}=\frac{127}{41}=\mathbf{3.098}.$$

| | MLE | Posterior mode | Posterior mean |
|---|---|---|---|
| Formula | $s_n/n$ | $s_n/(n+a)$ | $(s_n+1)/(n+a)$ |
| Value | 3.098 | 3.060 | 3.084 |
| Spread | SE $\sqrt{3.098/41}=0.275$ | | posterior sd 0.273 |
| 95% interval | Wald (2.559, 3.636) | | equal-tail (2.573, 3.641) |

The last row is computed here, not on the handwritten page: Wald from
[[L01-02-poisson-mle-properties]] (14), and the posterior interval from the 2.5% and 97.5% quantiles
of $G(128,41.5)$. **Numerically the two intervals almost coincide.** Their *readings* differ: a
probability statement about $\lambda$ given the data, against a coverage statement about the
procedure.

![Prior, normalised likelihood and posterior densities for the Poisson rate on 0 to 6: the Exp(1/2) prior decays from 0.5 at zero; the likelihood, normalised as Gamma(128, 41), and the Gamma(128, 41.5) posterior are nearly identical narrow peaks of height about 1.46 near 3.1; vertical lines mark the MLE 3.098 and the slightly smaller posterior mean 3.084.](figures/L01-poisson-prior-posterior.png)
*Prior (1) with $a=1/2$, likelihood (5) normalised to a density, and posterior (8) for $n=41$, $s_n=127$. Source: handwritten pp. 3–4; Greenberg Fig. 2.2 (p. 18) for the layout.*

The posterior is a slightly shifted copy of the normalised likelihood. Over the region where the
likelihood lives, roughly 2.3–4, the prior is almost flat (it falls from 0.16 to 0.07), so it can
only tilt the likelihood a little toward smaller values. Compare Greenberg's Figure 2.2, where
$n=10$ leaves the prior visible and $n=50$ buries it.

> **"In this example, the prior information is small when compared to the information in the
> likelihood. Still $E(\lambda\mid y_1,\dots,y_n)$ and $\text{Mode}(\lambda\mid y_1,\dots,y_n)$ are a
> little bit to the left of $\hat\lambda_{MLE}$. This is what we call shrinkage."** (handwritten
> p. 4)

---

## 6 · C — shrinkage as a weighted average

Split (10) the way Greenberg splits the beta-binomial mean in his (2.5) (p. 17):

$$\frac{s_n+1}{n+a}=\underbrace{\frac{a}{n+a}}_{\text{prior weight}}\cdot\underbrace{\frac1a}_{\text{prior mean}}+\underbrace{\frac{n}{n+a}}_{\text{data weight}}\cdot\underbrace{\frac{s_n}{n}}_{\hat\lambda_{MLE}}.\tag{13}$$

*Check:* $\frac{a}{n+a}\cdot\frac1a=\frac1{n+a}$ and $\frac{n}{n+a}\cdot\frac{s_n}{n}=\frac{s_n}{n+a}$, which add to (10).

**Coal numbers.** The prior weight is $0.5/41.5=0.01205$ and the data weight $41/41.5=0.98795$:

$$0.01205\times2+0.98795\times3.09756=0.02410+3.06024=3.08434.\ \checkmark$$

The **mode** shrinks toward the prior's mode, which is 0:

$$\frac{s_n}{n+a}=\frac{n}{n+a}\cdot\frac{s_n}{n}=0.98795\times3.09756=3.06024.\tag{14}$$

> **Both summaries sit left of the MLE because the prior centre (2 for the mean, 0 for the mode)
> is left of 3.098.** The pull is proportional to the prior weight $a/(n+a)$, which **vanishes
> like $1/n$**. With 41 years of data and a prior worth half a year, it is about 1%.

**Why this matters later.** The same "prior weight versus data weight" structure is behind every
shrinkage estimator in the course: the normal-mean posterior, ridge, and the hierarchical
models of Classes 3+4. There the prior weight is **not** negligible.

---

## 7 · G — links outward (named, not examinable here)

- **Which summary to report?** The posterior mean (10) is the Bayes estimator under quadratic
  loss (Bolfarine Thm 4.4.1, p. 63). The mode (11) is the maximum a posteriori value. Loss
  functions and their estimators are Greenberg §3.2.1 (Classes 3+4).
- **General conjugate result.** With a $\text{Gama}(a,b)$ prior (B (4.4.12), shape $a$, rate $b$),
  B Ex. 4.4.2 (p. 67) gets $\lambda\mid X\sim\text{Gama}(\sum x_i+a,\ n+b)$ and
  $E[\lambda\mid X]=(\sum x_i+a)/(n+b)$. Our case is shape 1 and rate $a$. (**Letter clash:** the
  handwritten $a$ is Bolfarine's $b$.)
- **More data do not cure a wrong model.** On all 112 years ($s_n=191$), (10) gives
  $192/112.5=1.707$, next to the MLE 1.705. Both are confident estimates of a single rate that
  [[L01-03-coal-mining-change-point]] showed does not exist. The prior regularises estimates;
  it does not test the likelihood.
- **Next.** The posterior predictive for next year's count (a negative binomial; Greenberg
  §3.2.3), and the change-point posterior that integrates the two rates with these same Gamma
  integrals ([[L01-03-coal-mining-change-point]] §8, (10)), are Classes 3+4.

---

## Links

- Prev: the two-regime model this prior will later be attached to,
  [[L01-03-coal-mining-change-point]]. Next: judging estimators by MSE (bias is allowed if variance
  falls), [[L01-05-comparing-estimators-mse-bootstrap]]. The Beta–Bernoulli analogue and the
  likelihood principle: [[L01-01-likelihood-sampling-rules]] §10. Formulas: [[L01-09-formulas]];
  pitfalls: [[L01-10-pitfalls]]; code: [[L01-11-python]].
- Rules: [[../../rules/07_bayes|rules/07]] (prior, posterior, conjugacy); scope
  [[../../rules/09_course_program|rules/09]].
- Reading: G §2.2 (pp. 12–18); B §4.3–4.4 (pp. 61–70) as the decision-theory view.
- Practice (statements in the books; see [[../../Map/exercises-index]]): **G 2.2** (p. 19,
  gamma–Poisson; posterior mean as a weighted average), **G 3.2** (p. 39, Poisson–gamma
  predictive), **B 4.9** (p. 72), **B 5.11** (p. 89, Bayesian interval with an Exp(1) prior).
