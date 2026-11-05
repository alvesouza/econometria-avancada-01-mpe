---
tags: [notes, lecture-03, bayes-rule, prior, likelihood, posterior, predictive, sequential-updating, base-rate]
date: 2026-10-27
status: taught
source: "aprendizagembayesiana-bayesianingredients.pdf slides 1–25 (Diego); question0.pdf (18 slides) + question0-R.txt (three coins); examples-from-stone-2013.pdf (7 image pages: Stone 2013, Figs 1.2–1.7, 1.12); bernoulli-trials-discrete-prior.html; Greenberg 1e §2.1 (pp. 7–11), §2.2 (pp. 12–18, (2.1)–(2.3)), §3.1.3 (pp. 24–25, (3.1))"
---

# Ingredients deck slides 1–25, three coins, Stone · Bayes' rule on a finite parameter space: posterior = prior × likelihood / predictive

> **Claim.** When the unknown takes finitely many values, Bayes' rule is arithmetic: multiply each
> prior probability by the likelihood of what was seen, add the products to get the **predictive**
> probability of the data, and divide. Diego's positive test moves $P(\text{ill})$ from **0.70** to
> **0.847**, and a second, better test moves it to **0.993**. Three heads in a row leave coin 1
> (the fair one) with **0.0674**. The likelihood alone answers a different question: smallpox
> explains the spots better than chickenpox ($0.9>0.8$), yet chickenpox is **90 times** more probable
> because it is 100 times more common. Updating one datum at a time gives exactly the posterior of
> updating on all data at once.
> Prev: — · Next: [[L03-02-conjugate-sequential-updating]] · Map: [[L03-00-map]]

**Notation.**

| Symbol | Meaning | Range / value |
|---|---|---|
| $\theta$ | state of nature (the unknown) | finite set, e.g. $\{0,1\}$, {coin 1, 2, 3} |
| $x$, $y$ | observed data (test results, tosses) | discrete |
| $p(\theta)$ | prior probability | sums to 1 over $\theta$ |
| $p(x\mid\theta)$ | likelihood: probability of the data under $\theta$, read as a function of $\theta$ | $[0,1]$ |
| $p(x)$ | predictive (marginal) probability of the data | $\sum_\theta p(x\mid\theta)p(\theta)$ |
| $p(\theta\mid x)$ | posterior probability | sums to 1 over $\theta$ |
| $H$ | the information held at a given moment | — |

---

## 1 · U — two questions that look alike

Diego feels unwell. His doctor wants $P(\text{ill}\mid\text{test positive})$. The number that comes
out of the laboratory's validation study is $P(\text{test positive}\mid\text{ill})=0.95$. The deck's
slide 14 calls confusing the two "the common (and wrong!) answer". Bayes' rule is the bridge between
**forward probability** (from the state of nature to the data: what the laboratory measures) and
**inverse probability** (from the data back to the state: what the doctor needs). Stone's Fig. 1.12
draws the two directions as two loops: $\theta_{true}\to$ physics $\to x$ on top, and
$x\to$ model $\to$ likelihood $\to$ Bayes' rule $\to\theta_{est}$ on the bottom, with the prior
entering only on the way back.

> **The likelihood is a forward quantity read backwards.** It is a probability over data, but in
> Bayes' rule it is used as a function of $\theta$ with the data fixed. It does not sum to one over
> $\theta$ (Greenberg, p. 14). The prior is what turns it into a probability over $\theta$.

---

## 2 · C — Bayes' rule (Greenberg (2.1)–(2.3))

Start from the definition of conditional probability, Greenberg's Axiom 4: $P(A\mid B)=P(AB)/P(B)$.
Since $P(AB)=P(BA)$,

$$P(A\mid B)P(B)=P(B\mid A)P(A).\tag{1}$$

Divide both sides of (1) by $P(B)>0$:

$$P(A\mid B)=\frac{P(B\mid A)P(A)}{P(B)}.\tag{2}$$

Set $A=\theta$ and $B=x$ in (2). This is Greenberg's (2.1) for discrete data:

$$p(\theta\mid x)=\frac{p(x\mid\theta)\,p(\theta)}{p(x)}.\tag{3}$$

The denominator comes from the **law of total probability** (question0.pdf slides 12–14): the
events "$\theta=\theta_k$" partition the sample space, so

$$p(x)=\sum_k p(x\mid\theta_k)\,p(\theta_k).\tag{4}$$

(4) is the **predictive probability of the data**: what the model and the prior together predict
before $x$ is seen. The ingredients deck writes (3) in words on slide 18:

$$\text{posterior}=\frac{\text{prior}\times\text{likelihood}}{\text{predictive}}.\tag{5}$$

Because $p(x)$ does not depend on $\theta$, (3) is often written as Greenberg's (2.3):

$$p(\theta\mid x)\ \propto\ p(x\mid\theta)\,p(\theta),\tag{6}$$

and the constant is recovered at the end by making the posterior sum to one.

---

## 3 · Worked — Diego, one test (slides 4–19)

**Model.** $\theta=1$ if Diego is ill, $\theta=0$ if not. The test $X$ has

| | $\theta=0$ (healthy) | $\theta=1$ (ill) |
|---|---|---|
| $P(X=1\mid\theta)$ | 0.40 (false positive) | 0.95 |
| $P(X=0\mid\theta)$ | 0.60 | 0.05 (false negative) |
| prior $p(\theta)$ | 0.30 | 0.70 |

**Maximum likelihood (slides 8–9).** $X=1$ is more likely under $\theta=1$:

$$\frac{P(X=1\mid\theta=1)}{P(X=1\mid\theta=0)}=\frac{0.95}{0.40}=2.375,\qquad\text{so }\hat\theta_{MLE}=1.$$

**Predictive (slide 12).** Substitute the table into (4):

$$P(X=1)=(0.40)(0.30)+(0.95)(0.70)=0.120+0.665=0.785.\tag{7}$$

**Posterior (slide 16).** Substitute (7) and the table into (3):

$$P(\theta=1\mid X=1)=0.70\times\frac{0.95}{0.785}=0.70\times1.210191=\mathbf{0.8471338}.\tag{8}$$

The factor $0.95/0.785=1.210$ is the **likelihood relative to the predictive**: the datum raises
the probability of every state under which it was more likely than average.

**If instead $X=0$ (slide 19).** The likelihood ratio is $0.60/0.05=12$, so $\hat\theta_{MLE}=0$, and

$$P(X=0)=(0.60)(0.30)+(0.05)(0.70)=0.180+0.035=0.215,$$

$$P(\theta=0\mid X=0)=0.30\times\frac{0.60}{0.215}=0.30\times2.790698=\mathbf{0.8372093}.$$

(The slide prints 0.8373093. The product of its own two factors is 0.8372093, so the printed
value has a typo in the fourth decimal.)

---

## 4 · C — sequential learning: yesterday's posterior is today's prior (slides 20–25; Greenberg §3.1.3)

The doctor orders a second test $Y$, more reliable than $X$: $P(Y=0\mid\theta=1)=0.01$ and
$P(Y=1\mid\theta=0)=0.04$. The tests are conditionally independent given $\theta$.

**General statement (Greenberg (3.1)).** For two data sets $y_1,y_2$:

$$p(\theta\mid y_1,y_2)\propto f(y_1,y_2\mid\theta)p(\theta)=f(y_2\mid y_1,\theta)f(y_1\mid\theta)p(\theta)=f(y_2\mid y_1,\theta)\,p(\theta\mid y_1)\cdot f(y_1),\tag{9}$$

where the last step uses (6) for $p(\theta\mid y_1)$, and $f(y_1)$ is a constant. With conditional
independence, $f(y_2\mid y_1,\theta)=f(y_2\mid\theta)$, so (9) is Bayes' rule with **$p(\theta\mid y_1)$
in the place of the prior**.

**Predictive for $Y$ given $X=1$ (slide 21).** Apply (4) with the posterior (8) as the weights:

$$P(Y=1\mid X=1)=(0.04)(0.1528662)+(0.99)(0.8471338)=0.0061146+0.8386625=0.8447771.\tag{10}$$

**Posterior after both (slide 22).** Apply (3) with prior (8) and predictive (10):

$$P(\theta=1\mid X=1,Y=1)=0.8471338\times\frac{0.99}{0.8447771}=0.8471338\times1.171907=\mathbf{0.992762}.\tag{11}$$

**Batch check.** Using both tests at once, the likelihood of $(X=1,Y=1)$ is $0.95\times0.99=0.9405$
under $\theta=1$ and $0.40\times0.04=0.016$ under $\theta=0$:

$$P(\theta=1\mid X=1,Y=1)=\frac{0.70\times0.9405}{0.70\times0.9405+0.30\times0.016}=\frac{0.65835}{0.65835+0.0048}=\frac{0.65835}{0.66315}=0.992762.$$

The sequential and batch answers agree to every digit, as (9) says they must.

**The deck's summary (slide 23).**

| Information $H$ | $P(\theta=1\mid H)$ |
|---|---|
| before $X$ and $Y$ | 0.70 |
| after $X=1$ | 0.847 |
| after $X=1$, $Y=1$ | 0.993 |
| after $Y=1$ alone | $\dfrac{0.99\times0.70}{0.99\times0.70+0.04\times0.30}=\dfrac{0.693}{0.705}=0.982979$ |

> **"Don't consider test X, unless it is 'cost' free" (slide 25).** $Y$ alone gets to 98.3%; adding
> $X$ buys one more point. The value of a datum is how far it moves the posterior, and that depends
> on what is already known.

---

## 5 · Worked — three coins (question0.pdf, question0-R.txt)

Coins with $P(\text{head})=0.5,\ 0.9,\ 1.0$, picked at random: $p(\text{coin }k)=1/3$. Three tosses give
three heads.

**Likelihoods (slide 6).** $(0.5)^3=0.125$, $(0.9)^3=0.729$, $(1.0)^3=1.000$.

**Predictive (slide 14).** By (4):

$$P(HHH)=(0.125)\tfrac13+(0.729)\tfrac13+(1.000)\tfrac13=\frac{1.854}{3}=0.618.\tag{12}$$

**Posteriors (slides 15–17).** By (3):

$$P(\text{coin 1}\mid HHH)=\frac{(0.125)(1/3)}{0.618}=\frac{0.0416667}{0.618}=\mathbf{0.0674},$$

$$P(\text{coin 2}\mid HHH)=\frac{0.243}{0.618}=\mathbf{0.3932},\qquad P(\text{coin 3}\mid HHH)=\frac{0.333333}{0.618}=\mathbf{0.5394}.$$

**"What if a fourth flip turned out head as well?" (slide 18).** Treat the three-head posterior as
the prior, by (9):

$$P(\text{coin }k\mid H^4)\propto p_k\times P(\text{coin }k\mid HHH):\quad 0.5(0.0674)=0.0337,\ \ 0.9(0.3932)=0.3539,\ \ 1.0(0.5394)=0.5394.$$

The sum is 0.9270, so the posteriors are $0.0364,\ 0.3818,\ 0.5819$. The batch route gives the same:
$p_k^4/\sum_j p_j^4=0.0625/1.7186$, $0.6561/1.7186$, $1/1.7186$.

![Three panels. Left: posterior probability of each coin against the number of heads in a row from 0 to 10; coin 1 falls from 1/3 to near zero, coin 2 rises to a peak near 0.39 at n=2 to 3 and then declines to 0.26, coin 3 rises steadily to 0.74; values at n=3 are labelled 0.0674, 0.3932, 0.5394. Middle: Beta(2,2) prior, dotted normalised likelihoods and Beta posteriors for n=10, s=3 (mean 0.357) and n=50, s=15 (mean 0.315). Right: Pareto posterior median and 10-90% band for theta against sample size, above the running maximum, approaching the true value 2 from below.](figures/L03-sequential-learning.png)
*Left panel: (3) with $p(\text{coin }k)=1/3$ and likelihood $p_k^n$, the R script `question0-R.txt` evaluated exactly. Middle and right: the conjugate updates of [[L03-02-conjugate-sequential-updating]].*

Read the left panel from left to right. Every head multiplies coin 1's weight by 0.5, coin 2's by 0.9
and coin 3's by 1, and renormalises. Coin 2 first gains (it explains heads better than coin 1) and
then loses (coin 3 explains them better still). Coin 3 can never be ruled in with certainty by heads
alone, because coin 2 also produces them: after ten heads it holds 0.741. One tail would settle it,
because its likelihood under coin 3 is 0.

---

## 6 · Worked — base rates (Stone 2013, Figs 1.2–1.7)

**Spots (Fig. 1.4).** Symptoms $x$; chickenpox $\theta_c$ with $p(x\mid\theta_c)=0.8$ and
$p(\theta_c)=0.1$; smallpox $\theta_s$ with $p(x\mid\theta_s)=0.9$ and $p(\theta_s)=0.001$. Stone takes
$p(x)=0.081$:

$$p(\theta_c\mid x)=\frac{0.8\times0.1}{0.081}=0.988,\qquad p(\theta_s\mid x)=\frac{0.9\times0.001}{0.081}=0.011.\tag{13}$$

The likelihood favours smallpox; the posterior favours chickenpox by a factor
$0.988/0.011\approx90$. The ratio of posteriors is the ratio of likelihoods times the ratio of
priors: $(0.8/0.9)\times(0.1/0.001)=0.889\times100=88.9$. (The figure's prior box prints
$p(\theta_s)=0.0011$; its arithmetic uses 0.001. $p(x)=0.081$ is rounded: the two diseases alone give
$0.08+0.0009=0.0809$, which yields 0.989 and 0.011.)

**"Four candles" (Figs 1.5–1.7).** The acoustic signal fits "fork handles" a little better
($0.7$ vs $0.6$), but "four candles" is nine times more frequent ($0.9$ vs $0.1$):
$p(x)=0.6(0.9)+0.7(0.1)=0.54+0.07=0.61$, so $p(\text{candles}\mid x)=0.54/0.61=0.885$ and
$p(\text{handles}\mid x)=0.07/0.61=0.115$.

> **The posterior ratio is the likelihood ratio times the prior ratio.** A datum that is only
> slightly more likely under a rare state cannot overcome a large difference in base rates.

---

## 7 · C — a discrete prior for a Bernoulli probability (bernoulli-trials-discrete-prior.html)

The same arithmetic works when $\theta$ is a probability restricted to a few values. The site page
uses $\theta\in\{0.3,0.5,0.8\}$ with prior $\{0.4,0.5,0.1\}$ and $n$ Bernoulli trials with
$s_n$ successes. The likelihood of the sequence is $\theta^{s_n}(1-\theta)^{n-s_n}$, so by (3)

$$P(\theta=\theta_j\mid x_{1:n})=\frac{p_j\,\theta_j^{s_n}(1-\theta_j)^{n-s_n}}{\sum_{l=1}^3p_l\,\theta_l^{s_n}(1-\theta_l)^{n-s_n}},\tag{14}$$

which is the line `prob[i,] = ptheta*theta^s[i]*(1-theta)^(i-s[i])` of the R code, renormalised.

Two facts are visible in (14). First, it depends on the data only through $(s_n,n)$: the order of the
successes is irrelevant (sufficiency). Second, the prior only shifts the starting point. With 40
successes in 50 trials, (14) gives $P(\theta=0.8\mid x)=0.99967$ even though the prior gave
$\theta=0.8$ only 10%: the likelihood ratio $(0.8/0.5)^{40}(0.2/0.5)^{10}=1.5\times10^{4}$ swamps the
prior odds of $0.1/0.5$. (The page simulates with `set.seed(12345)` in R; Python cannot reproduce that
stream, so the notes quote the formula and this deterministic case, not the page's path.)

---

## 8 · G — subjective probability and coherence (Greenberg §2.1.2, pp. 8–11)

Greenberg grounds the prior in **subjective probability**: a probability is the price at which you
would buy or sell a bet that pays 1 if the event occurs. **Coherence** (no set of bets that loses for
sure) forces these prices to obey the axioms of probability, so Bayes' rule applies to beliefs as it
does to frequencies. The frequentist reading (§2.1.1) cannot give $\theta$ a distribution, because a
parameter is not the outcome of a repeated experiment. Named here for orientation; the coherence
argument is not examinable.

---

## Links

- Next: the same rule with a continuous $\theta$ and conjugate families,
  [[L03-02-conjugate-sequential-updating]]. Comparing coins as **models**: [[L03-05-model-comparison-bayes-factors]] §5.
  Formulas: [[L03-11-formulas]]; pitfalls: [[L03-12-pitfalls]]; code: [[L03-13-python]] §1.
- Earlier: the first Bayesian example (Exp prior, Poisson data), [[../L01/L01-04-first-bayesian-poisson|L01 §4]];
  a p-value is not $P(H_0\mid x)$, [[../L01/L01-08-p-hacking-evidence|L01 §8]].
- Rules: [[../../rules/07_bayes|rules/07]] (prior, posterior, predictive, sequential Bayes).
- Reading: G §2.1–2.2 (pp. 7–18), §3.1.3 (pp. 24–25).
- Practice (statements in the books): **G 2.1** (p. 19, coherence) is background; the class list
  starts at **G 2.2** (p. 19), see [[L03-02-conjugate-sequential-updating]].
