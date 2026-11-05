---
tags: [notes, lecture-03, model-comparison, bayes-factor, marginal-likelihood, posterior-odds, jeffreys, bic, model-averaging, improper-priors]
date: 2026-10-27
status: taught
source: "Greenberg 1e §3.2.4 (pp. 33–38: (3.3)–(3.5), Table 3.1, the Michaela–Lila example, Table 3.2), §4.2 (pp. 43–44), §7.1.2 (pp. 95–96, named); question0.pdf and the Diego slides of aprendizagembayesiana-bayesianingredients.pdf reread as model choice; class plan goal 'Bayes factors, posterior model probabilities, model selection'"
---

# G §3.2.4 · Bayes factors: the marginal likelihood rewards fit and charges for every free parameter

> **Claim.** A model is a likelihood plus a prior. Its **marginal likelihood** $m(y)=\int f(y\mid\theta)\pi(\theta)d\theta$
> is the likelihood **averaged over the prior**, and posterior odds = prior odds × **Bayes factor**
> $B_{12}=m_1(y)/m_2(y)$. Greenberg's Michaela–Lila example compares "one coin probability" with "two":
> with $m=10$ tosses each and proportions 0.2 / 0.8, $\log_{10}B_{12}=-1.200$ (strong evidence for two
> probabilities); with 0.5 / 0.5, $+0.297$ for the simpler model, and $+0.756$ at $m=100$. The simpler
> model gains when the data agree with it because the bigger model spreads its prior over values the
> data rule out: in large samples $\log B_{12}\approx\log LR-\frac{d_1-d_2}2\log n$, a BIC-type penalty.
> Bayes factors need **proper** priors; an improper prior makes $B_{12}$ arbitrary.
> Prev: [[L03-04-bayes-estimators-loss]] · Next: [[L03-06-monte-carlo-simulation]] · Map: [[L03-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $M_i$ | model $i$: prior $p_i=P(M_i)$, parameters $\theta_i$ ($d_i$ of them), prior $\pi_i(\theta_i)$, likelihood $f_i(y\mid\theta_i)$ | $i=1,2,\dots$ |
| $m_i(y)$ | marginal likelihood of $M_i$ | $>0$ |
| $B_{12}$ | Bayes factor $m_1(y)/m_2(y)$ | $>0$ |
| $R_{12}$ | posterior odds $P(M_1\mid y)/P(M_2\mid y)$ | $>0$ |
| $m$ | tosses by each girl (Michaela–Lila) | integer |
| $s_1,s_2$ | heads by Michaela, by Lila | $0,\dots,m$ |
| $n$ | total sample size | here $2m$ |

---

## 1 · U — comparing explanations, not testing a point

A frequentist test asks whether the data would be unusual if $H_0$ were true, and refers a statistic to
its sampling distribution (G p. 36). The Bayesian question is different and symmetric: **which model,
given the data, is more probable?** It applies to non-nested models (a normal vs a Student-$t$
likelihood, $y$ vs $\log y$) as easily as to nested ones, and it can end in "both are still
plausible; wait for more data" (G p. 35). The three-coin problem of [[L03-01-bayes-rule-discrete]]
was already a model comparison: each coin is a model with no free parameter, and its marginal
likelihood is just its likelihood.

---

## 2 · C — posterior model probabilities (G (3.3)–(3.4))

Apply Bayes' rule to the model index and introduce the parameters, as for the predictive
([[L03-02-conjugate-sequential-updating]] (10)):

$$P(M_1\mid y)=\frac{p_1f_1(y\mid M_1)}{f(y)}=\frac{p_1\int f_1(y\mid\theta_1,M_1)\pi_1(\theta_1\mid M_1)d\theta_1}{f(y)},\tag{1}$$

$$f(y)=p_1\int f_1(y\mid\theta_1,M_1)\pi_1(\theta_1\mid M_1)d\theta_1+p_2\int f_2(y\mid\theta_2,M_2)\pi_2(\theta_2\mid M_2)d\theta_2.\tag{2}$$

Each integral in (2) is a **marginal likelihood** (G (3.4)):

$$m_i(y)=\int f_i(y\mid\theta_i,M_i)\,\pi_i(\theta_i\mid M_i)\,d\theta_i,\tag{3}$$

"the expected value of the likelihood function with respect to the prior distribution" (p. 34). It is
also the normalising constant of model $i$'s posterior, so the constants of $f$ and $\pi$ must be kept.

---

## 3 · C — posterior odds and the Bayes factor (G pp. 34–35)

Divide (1) for $M_1$ by (1) for $M_2$; $f(y)$ cancels:

$$R_{12}=\frac{P(M_1\mid y)}{P(M_2\mid y)}=\underbrace{\frac{p_1}{p_2}}_{\text{prior odds}}\times\underbrace{\frac{m_1(y)}{m_2(y)}}_{B_{12}}.\tag{4}$$

With two models, $P(M_1\mid y)=R_{12}/(1+R_{12})=1/\big(1+(p_2/p_1)/B_{12}\big)$.

**Jeffreys' guidelines (G Table 3.1, p. 35)**, for evidence in favour of $M_1$ (mirror the signs for $M_2$):

| $\log_{10}R_{12}$ | Interpretation |
|---|---|
| $>2$ | decisive support for $M_1$ |
| $3/2$ to $2$ | very strong evidence |
| $1$ to $3/2$ | strong evidence |
| $1/2$ to $1$ | substantial evidence |
| $0$ to $1/2$ | weak evidence |

Greenberg: "these values are arbitrary, as is the 5% level of significance". If $\log_{10}B_{12}=2$, the
prior odds would have to be below 1/100 for the posterior odds to favour $M_2$.

---

## 4 · Worked — Michaela and Lila (G pp. 37–38, Table 3.2)

Michaela tosses a coin $m$ times and gets $s_1$ heads; Lila tosses it $m$ times and gets $s_2$.
$M_1$: $\theta_1=\theta_2=\theta$ (the way they toss does not matter). $M_2$: $\theta_1\ne\theta_2$. Priors: Beta(1, 1), i.e.
uniform, on $\theta$ under $M_1$ and on each $\theta_j$ under $M_2$.

**$M_1$.** The likelihood of the $2m$ tosses is $\theta^{s_1+s_2}(1-\theta)^{2m-s_1-s_2}$; integrate against the
uniform prior with the Beta integral $\int_0^1\theta^{a-1}(1-\theta)^{b-1}d\theta=B(a,b)$:

$$m_1(y)=\int_0^1\theta^{s_1+s_2}(1-\theta)^{2m-s_1-s_2}d\theta=B(s_1+s_2+1,\ 2m-s_1-s_2+1)=\frac{\Gamma(2m\bar y+1)\Gamma(2m-2m\bar y+1)}{\Gamma(2m+2)},\tag{5}$$

Greenberg's expression with $\bar y=(s_1+s_2)/2m$.

**$M_2$.** The two probabilities are independent a priori and each appears in its own factor of the
likelihood, so the double integral factors (G (3.5)):

$$m_2(y)=B(s_1+1,m-s_1+1)\,B(s_2+1,m-s_2+1)=\frac{\Gamma(m\bar y_1+1)\Gamma(m-m\bar y_1+1)}{\Gamma(m+2)}\cdot\frac{\Gamma(m\bar y_2+1)\Gamma(m-m\bar y_2+1)}{\Gamma(m+2)}.\tag{6}$$

**One row in full ($m=10$, $s_1=2$, $s_2=8$).** By (5), $m_1=B(11,11)$, $\log_{10}m_1=-6.5888$. By (6),
$m_2=B(3,9)B(9,3)$, $\log_{10}m_2=-5.3892$. Then

$$\log_{10}B_{12}=-6.5888-(-5.3892)=-1.1996\approx\mathbf{-1.200}.$$

With even prior odds, $P(M_1\mid y)=1/(1+10^{1.1996})=0.059$: strong evidence that the girls toss
differently.

**Table 3.2 reproduced** (Lila's proportion $=1-$ Michaela's):

| Michaela | Lila | $\log_{10}B_{12}$, $m=10$ | $\log_{10}B_{12}$, $m=100$ |
|---|---|---|---|
| 0.1 | 0.9 | $-2.506$ | $-30.775$ |
| 0.2 | 0.8 | $-1.200$ | $-15.793$ |
| 0.3 | 0.7 | $-0.348$ | $-6.316$ |
| 0.4 | 0.6 | $0.138$ | $-0.975$ |
| 0.5 | 0.5 | $0.297$ | $0.756$ |

Every entry is recomputed from (5)–(6) in [[L03-13-python]] §5 and agrees to the printed three decimals.

![Left: log10 Bayes factor for M1 against Michaela's proportion of heads, with Lila's equal to one minus it, for m = 10 (a shallow arch peaking near 0.3 at 0.5) and m = 100 (a steep arch peaking at 0.76 at 0.5 and falling below -30 at 0.1); Table 3.2 values are marked as dots and dotted lines mark the Jeffreys thresholds. Right: log10 Bayes factor at equal proportions against m on a log scale, rising from 0.15 to 1.75, with the BIC-type line one half log10 of 2m running parallel about 0.4 above it.](figures/L03-bayes-factor-sample-size.png)
*Left: (5)–(6) evaluated on a continuum of proportions (the Gamma functions accept non-integers), Table 3.2 as dots. Right: $\log_{10}B_{12}$ at $s_1=s_2=m/2$ against $m$, with the large-sample approximation (8).*

Two comparative statics. Across proportions, $B_{12}$ is largest when both girls agree (0.5 / 0.5) and
collapses as they diverge; **more data sharpen the verdict in both directions** (the $m=100$ arch is
taller and steeper). Across sample sizes at perfect agreement, the evidence for the simpler model
keeps growing, like $\frac12\log_{10}m$: two free probabilities are never refuted by agreeing data, only
penalised for being unnecessary.

> **Interactive companion.** [The Bayes-Factor Dial](companions/companion-bayes-factor-coins.html) —
> move $m$, the two head counts, the prior Beta$(\alpha,\alpha)$ and the prior odds; watch
> $\log_{10}B_{12}$ against Lila's count with the Jeffreys bands, the Beta posteriors under each model, and
> the large-sample approximation. The buttons load the ten rows of Table 3.2.

---

## 5 · Worked — coins and tests as models

**Three coins** ([[L03-01-bayes-rule-discrete]] §5). With no free parameters, $m_k(HHH)=p_k^3$, so
$B_{31}=1/0.125=8$ and $B_{21}=0.729/0.125=5.832$; with equal prior odds these give the posteriors
0.5394, 0.3932 and 0.0674. Here the Bayes factor is the likelihood ratio, because there is nothing to
integrate.

**Diego** ([[L03-01-bayes-rule-discrete]] §3). "Ill" vs "healthy" are two models; the Bayes factor of
$X=1$ is $0.95/0.40=2.375$ ($\log_{10}=0.38$, weak evidence) and prior odds $0.7/0.3$ turn it into
posterior odds $5.54$, i.e. $P=0.847$.

---

## 6 · C — what the marginal likelihood penalises (G p. 37)

Exponentiate the second-order expansion of the log-likelihood around the MLE $\hat\theta_i$
([[L03-02-conjugate-sequential-updating]] (16), G (3.2)) and substitute into (3). For large $n$ the
exponential dominates the prior, so $\pi_i(\theta_i)\approx\pi_i(\hat\theta_i)$ on the region that matters:

$$m_i(y)\approx L_i(\hat\theta_i\mid y)\,\pi_i(\hat\theta_i)\int\exp\Big[-\frac n2(\theta_i-\hat\theta_i)'V_i^{-1}(\theta_i-\hat\theta_i)\Big]d\theta_i=L_i(\hat\theta_i\mid y)\,\pi_i(\hat\theta_i)\,(2\pi)^{d_i/2}n^{-d_i/2}|V_i|^{1/2}.\tag{7}$$

Take the log of the ratio of (7) for $i=1,2$:

$$\log B_{12}\approx\underbrace{\log\frac{L_1(\hat\theta_1\mid y)}{L_2(\hat\theta_2\mid y)}-\frac{d_1-d_2}{2}\log n}_{\text{grows with }n}+\underbrace{\log\frac{\pi_1(\hat\theta_1)}{\pi_2(\hat\theta_2)}+\frac12\log\frac{|V_1|}{|V_2|}+\frac{d_1-d_2}2\log(2\pi)}_{\text{bounded}}.\tag{8}$$

The first bracket is the log-likelihood ratio minus **half the log sample size per extra
parameter**: the Schwarz/BIC penalty of [[../L01/L01-06-gaussian-linear-regression|L01-06]], derived
rather than imposed.

**Check on Michaela–Lila.** $d_1-d_2=1-2=-1$ and $n=2m$, so the first bracket is
$\log LR+\frac12\log(2m)$. For (2, 8) at $m=10$: $\log_{10}LR=-1.674$ and the approximation gives
$-1.674+\frac12\log_{10}20=-1.024$, against the exact $-1.200$. At equal proportions $LR=1$, and with
uniform priors ($\pi=1$, $V=\theta(1-\theta)=1/4$) the bounded bracket evaluates to $-\frac12\log(2\pi)$; the exact
value tends to $\frac12\log_{10}(m/\pi)$, which stays $\frac12\log_{10}(2\pi)=0.399$ below the BIC line, the
constant gap in the right panel.

> **Occam's razor is built in.** $M_2$ can fit anything $M_1$ fits, so its maximised likelihood is
> always at least as high. Its marginal likelihood averages over a prior spread across $(\theta_1,\theta_2)$
> pairs the data contradict, and that average is lower whenever the extra freedom is not needed.

---

## 7 · C — Bayes factors need proper priors (G §4.2, p. 44)

An improper prior is defined only up to a constant: $c\,\pi(\theta)$ is "the same" prior for every $c>0$.
Substituting into (3) and (4):

$$B_{12}=\frac{c_1\int f_1(y\mid\theta_1)\pi_1(\theta_1)d\theta_1}{c_2\int f_2(y\mid\theta_2)\pi_2(\theta_2)d\theta_2},\tag{9}$$

and the arbitrary ratio $c_1/c_2$ sets $B_{12}$ to any value, "even if only one of the prior distributions
is improper". A posterior for $\theta$ within a model survives an improper prior (the constant cancels in
[[L03-01-bayes-rule-discrete]] (3)); a comparison between models does not. A related warning: a proper
but very diffuse prior makes $m_i$ small, so (8)'s $\log\pi_i(\hat\theta_i)$ term favours the smaller model
however good the bigger one's fit (the Jeffreys–Lindley effect of [[../L01/L01-08-p-hacking-evidence|L01-08]]).

---

## 8 · C — model averaging and invariance (G pp. 35–36)

**Prediction under model uncertainty.** Weight each model's predictive by its posterior probability:

$$f(y_f\mid y)=\sum_{i=1}^mP(M_i\mid y)\int f_i(y_f\mid\theta_i,y,M_i)\,\pi_i(\theta_i\mid y,M_i)\,d\theta_i.\tag{10}$$

Models with small $P(M_i\mid y)$ contribute little. The Vanguard table in [[L03-10-sparsity-priors]] uses
Bayesian model averaging (BMA) as the benchmark.

**Invariance to the scale of $y$.** If $M_1$ models $y$ and $M_2$ models $z=g(y)$ with $g$ monotone,
transforming $M_2$ back to the $y$ scale multiplies its density by the Jacobian $|dz/dy|$, and the same
factor appears in every comparison on the $y$ scale; comparing $y$ with $\log y$ is legitimate once both
densities are on the same scale (G p. 36).

---

## 9 · G — computing marginal likelihoods (named)

When the posterior is not of a known form, $m(y)$ is not available in closed form. Chib's method
(G §7.1.2, pp. 95–96) uses the identity $f(y)=f(y\mid\theta^*)\pi(\theta^*)/\pi(\theta^*\mid y)$ at a point $\theta^*$ and
estimates the denominator from Gibbs output; Chib–Jeliazkov (§7.2.2) does the same for MH output.
Greenberg's union-wage example (§8.1.1, p. 113) reports $\log_{10}B=5.390$ for including union
membership. Not examinable here.

---

## Links

- Prev: [[L03-04-bayes-estimators-loss]]; next: computing the integrals that have no closed form,
  [[L03-06-monte-carlo-simulation]]. Formulas: [[L03-11-formulas]]; pitfalls: [[L03-12-pitfalls]]; code:
  [[L03-13-python]] §5.
- Earlier: p-value vs Bayes factor at $X=1.8$, [[../L01/L01-08-p-hacking-evidence|L01 §8]]; BIC as a selection
  criterion, [[../L01/L01-06-gaussian-linear-regression|L01 §6]].
- Rules: [[../../rules/07_bayes|rules/07]].
- Practice (statements in the books): **G 3.7** (p. 40, verify (3.5)), **G 3.8** (p. 40, Bayes factors for
  two Poisson rates; listed in the class plan), **G 4.5** (p. 58, analytic marginal likelihood).
