---
tags: [notes, lecture-03, bayes-estimator, loss-function, posterior-mean, posterior-median, map, bayes-risk, credible-interval, hpd]
date: 2026-10-27
status: taught
source: "notas-bayesianas-slides.pdf ('Estimador Bayesiano e Funções de Perda', 16 slides, PT); Greenberg 1e §3.2.1 (pp. 29–31), §3.2.2 (p. 31); Bolfarine & Sandoval (2010) §4.3 (pp. 61–63, Def. 4.3.1–4.3.2, Ex. 4.3.2), §4.4 (pp. 63–70, Thm 4.4.1, Ex. 4.4.1–4.4.3, Thm 4.4.2), §5.5 (pp. 85–87, Def. 5.5.1, Ex. 5.5.1)"
---

# Bayes-estimator deck (16 slides), G §3.2.1–3.2.2, B §4.3–4.4, §5.5 · A point estimate is the answer to a loss function

> **Claim.** The posterior is the whole answer; a single number requires a **loss function**. The
> **Bayes estimator** minimises the posterior expected loss: quadratic loss gives the **posterior
> mean**, absolute loss the **median**, 0–1 loss the **mode** (MAP), and Greenberg's bilinear loss the
> quantile of order $a/(a+b)$. With a uniform prior and $s=1$ success in $n=10$ trials the posterior is
> Beta(2, 10): mode **0.100** (= MLE), median **0.148**, mean **0.167**, so the three losses give three
> different answers. Bayes estimators are usually **biased**, yet they minimise the **Bayes risk** and
> become the MLE as $n\to\infty$ or as the prior becomes vague. Interval summaries are **credible
> intervals**: probability statements about $\theta$ given the data, with the HPD interval the shortest.
> Prev: [[L03-03-normal-measurement-physicists]] · Next: [[L03-05-model-comparison-bayes-factors]] · Map: [[L03-00-map]]

**Notation** (the deck writes $\delta(x)$ and $\pi(\theta\mid x)$; Greenberg $\hat\theta$ and $\pi(\theta\mid y)$).

| Symbol | Meaning | Range |
|---|---|---|
| $L(\theta,a)$ | loss when the truth is $\theta$ and the estimate is $a$ | $\ge0$ |
| $\rho(a\mid x)$ | posterior expected loss $E[L(\theta,a)\mid x]$ | $\ge0$ |
| $\delta(x)$ | Bayes estimator, $\arg\min_a\rho(a\mid x)$ | — |
| $F(\cdot\mid x)$ | posterior cdf | $[0,1]$ |
| $R(\theta,d)$ | frequentist risk of the rule $d$, $E_\theta[L(\theta,d(X))]$ | — |
| $r(\pi,d)$ | Bayes risk $\int R(\theta,d)\pi(\theta)d\theta$ | — |

---

## 1 · U — why the posterior is not yet an answer

A posterior is a distribution. A forecaster who must publish one number, a regulator who must set one
threshold, an estimator plugged into the next model: each needs a single $a$. Which number depends on
**what an error costs**. Overestimating a bridge's load capacity costs more than underestimating it;
missing a fraud costs more than a false alarm. The loss function writes those costs down, and the
Bayes estimator is the number that does best **on average over what is still uncertain about
$\theta$**, given everything observed (deck slides 6–8).

---

## 2 · C — loss, expected loss, Bayes estimator (deck slides 6–8; G §3.2.1; B Def. 4.3.1–4.3.2)

For each true value $\theta$ and estimate $a$, $L(\theta,a)\ge0$ measures the loss. Before the data, the
**prior expected loss** of $a$ is $\int L(\theta,a)\pi(\theta)d\theta$ (slide 6). After observing $x$:

$$\rho(a\mid x)=E[L(\theta,a)\mid x]=\int_\Theta L(\theta,a)\,\pi(\theta\mid x)\,d\theta,\tag{1}$$

$$\delta(x)=\arg\min_a\ \rho(a\mid x).\tag{2}$$

(2) is the deck's definition of the Bayes estimator (slide 8). "The optimal estimator depends on the
choice of the loss function." Greenberg (p. 31) stresses that (2) is mechanical: given a loss, there
is nothing to invent, only a minimisation.

---

## 3 · C — quadratic loss gives the posterior mean (slide 9; G p. 30; B Thm 4.4.1)

$L(\theta,a)=(\theta-a)^2$. Write $\theta-a=(\theta-\bar\theta)+(\bar\theta-a)$ with $\bar\theta=E(\theta\mid x)$ and expand
inside (1):

$$\rho(a\mid x)=E[(\theta-\bar\theta)^2\mid x]+2(\bar\theta-a)E[\theta-\bar\theta\mid x]+(\bar\theta-a)^2.\tag{3}$$

The middle expectation is $\bar\theta-\bar\theta=0$, so

$$\rho(a\mid x)=V(\theta\mid x)+(\bar\theta-a)^2.\tag{4}$$

(4) is minimised at $a=\bar\theta$:

$$\delta(x)=E(\theta\mid x),\qquad\min_a\rho(a\mid x)=V(\theta\mid x).\tag{5}$$

Greenberg reaches the same by differentiating under the integral: $-2\int(\theta-\hat\theta)\pi(\theta\mid y)d\theta=0$.
(4) is the posterior twin of MSE = variance + bias² ([[../L01/L01-05-comparing-estimators-mse-bootstrap|L01-05]]):
the expectation is over $\theta$ given $x$, not over $x$ given $\theta$.

---

## 4 · C — absolute loss gives the posterior median (slide 10; G Ex. 3.5 setting)

$L(\theta,a)=|\theta-a|$. Split (1) at $a$:

$$\rho(a\mid x)=\int_{-\infty}^a(a-\theta)\pi(\theta\mid x)d\theta+\int_a^\infty(\theta-a)\pi(\theta\mid x)d\theta.\tag{6}$$

Differentiate with respect to $a$ (Leibniz rule; the boundary terms are zero because the integrands
vanish at $\theta=a$):

$$\frac{d\rho}{da}=\int_{-\infty}^a\pi(\theta\mid x)d\theta-\int_a^\infty\pi(\theta\mid x)d\theta=F(a\mid x)-[1-F(a\mid x)]=2F(a\mid x)-1.\tag{7}$$

(7) is negative below the median and positive above it, so

$$\delta(x)=\text{Median}(\theta\mid x),\quad F(\delta\mid x)=\tfrac12.\tag{8}$$

The deck: "more robust than quadratic loss: it penalises errors linearly and is less sensitive to
extreme values."

---

## 5 · C — 0–1 loss gives the posterior mode (slide 11; G Ex. 3.6 setting)

$L(\theta,a)=1$ if $|\theta-a|\ge\varepsilon$ and 0 otherwise, for a small $\varepsilon>0$. Then

$$\rho(a\mid x)=P(|\theta-a|\ge\varepsilon\mid x)=1-\int_{a-\varepsilon}^{a+\varepsilon}\pi(\theta\mid x)d\theta\approx1-2\varepsilon\,\pi(a\mid x).\tag{9}$$

Minimising (9) means maximising the posterior density at $a$; as $\varepsilon\to0$,

$$\delta(x)=\text{Mode}(\theta\mid x)\quad\text{(the maximum a posteriori, MAP, estimate)}.\tag{10}$$

---

## 6 · C — bilinear loss gives a quantile (G p. 29, $L_3$)

Greenberg's bilinear loss charges $a$ per unit when the estimate is too low ($\theta>\hat\theta$) and $b$
per unit when it is too high. Repeating (6)–(7) with the two weights:

$$\frac{d\rho}{d\hat\theta}=-a\,[1-F(\hat\theta\mid x)]+b\,F(\hat\theta\mid x)=0\ \Longrightarrow\ F(\hat\theta\mid x)=\frac{a}{a+b}.\tag{11}$$

The Bayes estimator is the posterior quantile of order $a/(a+b)$; $a=b$ gives back the median. If
over-estimation is three times as costly as under-estimation ($a=1$, $b=3$), report the 25% quantile.

**Summary (deck slide 12).**

| Loss $L(\theta,a)$ | Bayes estimator $\delta(x)$ |
|---|---|
| quadratic $(\theta-a)^2$ | posterior mean |
| absolute $\lvert\theta-a\rvert$ | posterior median |
| 0–1, $\mathbf 1[\lvert\theta-a\rvert\ge\varepsilon]$ | posterior mode (MAP) |
| bilinear $a/b$ | posterior quantile $a/(a+b)$ |

---

## 7 · Worked — Beta(2, 10): one posterior, four answers

Uniform prior, $s=1$ success in $n=10$ trials ([[L03-02-conjugate-sequential-updating]] (7)):
$\theta\mid x\sim\text{Beta}(2,10)$.

| Estimator | Formula | Value |
|---|---|---|
| mode (0–1) | $(\alpha_1-1)/(\alpha_1+\beta_1-2)=1/10$ | **0.1000** = MLE $s/n$ |
| median (absolute) | $F^{-1}(0.5)$ | **0.1480** |
| mean (quadratic) | $\alpha_1/(\alpha_1+\beta_1)=2/12$ | **0.1667** |
| 25% quantile (bilinear, $a=1$, $b=3$) | $F^{-1}(0.25)$ | 0.0876 |
| minimum expected quadratic loss | $V(\theta\mid x)=\dfrac{2\times10}{12^2\times13}$ | 0.010684 |

![Left: the Beta(2,10) posterior density, right-skewed with its peak at 0.1, with vertical lines at the mode 0.100, median 0.148 and mean 0.167. Right: posterior expected loss against the estimate a on 0 to 0.45 for quadratic, absolute and 0-1 loss, each rescaled to the interval 0 to 1; their minima, marked with dots, fall at 0.167, 0.148 and 0.100.](figures/L03-loss-functions.png)
*Left: the posterior $\text{Beta}(2,10)$ with its three classical summaries. Right: $\rho(a\mid x)$ of (1) for quadratic, absolute and 0–1 ($\varepsilon=0.01$) loss, computed by quadrature and rescaled; dots mark the minima (5), (8), (10).*

For a right-skewed posterior the ordering is **mode < median < mean**: the mean is pulled by the long
right tail, the mode ignores it. The 0–1 curve is the steepest and the narrowest: it only rewards
landing near the peak. The quadratic curve is the flattest near its minimum, which is why small
departures from the mean cost little. The same ordering holds for L01-04's coal posterior
Gamma(128, 41.5): mode 3.0602 < median 3.0763 < mean 3.0843, all three close because 41 years of data
make the posterior nearly symmetric.

---

## 8 · C — the Exponential–Gamma example (deck slides 4–5, 13–15)

$x_1,\dots,x_n\mid\theta\sim\text{Exp}(\theta)$ (density $\theta e^{-\theta x}$) and $\theta\sim\text{Gama}(\alpha_0,\beta_0)$. The
kernels (slide 4) are $\pi(\theta)\propto\theta^{\alpha_0-1}e^{-\beta_0\theta}$ and $L(\theta;x)\propto\theta^ne^{-\theta\sum x_i}$, so

$$\pi(\theta\mid x)\propto\theta^{(\alpha_0+n)-1}e^{-(\beta_0+\sum x_i)\theta},\qquad\theta\mid x\sim\text{Gama}\Big(\alpha_0+n,\ \beta_0+\sum x_i\Big).\tag{12}$$

Under quadratic loss, by (5),

$$\delta(x)=E(\theta\mid x)=\frac{\alpha_0+n}{\beta_0+\sum x_i},\qquad\hat\theta_{EMV}=\frac{n}{\sum x_i}=\frac1{\bar x}.\tag{13}$$

**Observation 1 (slide 13): the Bayes estimator is biased.** True, and the reason is the prior's
pull. But the slide's contrast "while the MLE is unbiased by construction" fails here: with
$S=\sum x_i\sim\text{Gama}(n,\theta)$,

$$E\Big[\frac1S\Big]=\int_0^\infty\frac1s\,\frac{\theta^n s^{n-1}e^{-\theta s}}{\Gamma(n)}ds=\frac{\theta^n\Gamma(n-1)}{\Gamma(n)\theta^{n-1}}=\frac{\theta}{n-1},\quad\text{so}\quad E(\hat\theta_{EMV})=\frac{n}{n-1}\theta\ne\theta.\tag{14}$$

Both estimators are biased; neither is unbiased "by construction". (Maximum likelihood guarantees
invariance and large-sample efficiency, not unbiasedness; L01-01 showed the same for the negative
binomial.)

**Observation 2 (slide 14): asymptotic efficiency.** As $n\to\infty$, the prior's contribution
$(\alpha_0,\beta_0)$ in (13) is swamped by $(n,\sum x_i)$, so $E(\theta\mid x)-\hat\theta_{EMV}\to0$ and the Bayes estimator
inherits the MLE's efficiency ([[L03-02-conjugate-sequential-updating]] §7).

**Vague prior (slide 15).** $\alpha_0\to0$, $\beta_0\to0$ in (13) gives $E(\theta\mid x)\to n/\sum x_i$. A seeded
illustration: $n=30$ draws with $\theta=2$, prior Gama(2, 1): $\delta=2.1636$ against $\hat\theta=2.1755$.

---

## 9 · C — Bayes risk: why the posterior mean is optimal before the data too (B §4.3–4.4)

The frequentist risk of a rule $d$ is $R(\theta,d)=E_\theta[L(\theta,d(X))]$, an average over data for fixed
$\theta$. Averaging it over the prior gives the **Bayes risk** (B Def. 4.3.1):

$$r(\pi,d)=\int R(\theta,d)\pi(\theta)d\theta=\int\!\!\int L(\theta,d(x))f(x\mid\theta)\pi(\theta)\,dx\,d\theta.\tag{15}$$

Write $f(x\mid\theta)\pi(\theta)=\pi(\theta\mid x)g(x)$ (B (4.4.3)) and swap the integrals:

$$r(\pi,d)=\int\Big[\int L(\theta,d(x))\pi(\theta\mid x)d\theta\Big]g(x)\,dx=\int\rho(d(x)\mid x)\,g(x)\,dx.\tag{16}$$

(16) is minimised by minimising the bracket for every $x$, which is (2): **the Bayes estimator
minimises the Bayes risk** (B Def. 4.3.2, Thm 4.4.1 for quadratic loss).

**Worked (B Ex. 4.4.1).** Bernoulli data, uniform prior, quadratic loss: $\delta=(S+1)/(n+2)$ (B (4.4.11)).
Its risk is variance plus squared bias:

$$R(\theta,\delta)=\frac{n\theta(1-\theta)}{(n+2)^2}+\Big(\frac{n\theta+1}{n+2}-\theta\Big)^2=\frac{n\theta(1-\theta)+(1-2\theta)^2}{(n+2)^2}.\tag{17}$$

Integrating (17) over $\theta\sim U(0,1)$ ($E\theta=\frac12$, $E\theta^2=\frac13$):

$$r(\pi,\delta)=\frac{n/6+1/3}{(n+2)^2}=\frac{1}{6(n+2)},\qquad r(\pi,\bar X)=\int_0^1\frac{\theta(1-\theta)}{n}d\theta=\frac1{6n}.\tag{18}$$

For $n=10$: $1/72=0.0139$ against $1/60=0.0167$. The biased estimator has the smaller average risk.

**Two more facts (B pp. 64–70).** The Bayes estimator depends on the data only through a sufficient
statistic (Thm 4.4.2). And it is **not invariant**: if $\hat\theta$ is the Bayes estimator of $\theta$,
$g(\hat\theta)$ need not be the Bayes estimator of $g(\theta)$, because $E[g(\theta)\mid x]\ne g(E[\theta\mid x])$ for
nonlinear $g$ (the MLE is invariant; [[../L01/L01-01-likelihood-sampling-rules|L01-01]]).

---

## 10 · C — interval estimates: credible and HPD (G §3.2.2; B §5.5)

A $100(1-\epsilon)\%$ **credible interval** $[t_1,t_2]$ satisfies $\int_{t_1}^{t_2}\pi(\theta\mid x)d\theta=1-\epsilon$
(B Def. 5.5.1). It is a probability statement about $\theta$ given the observed data. A confidence
interval is a statement about the procedure over repeated samples (G p. 31). Among all intervals with
the same content the shortest is the **highest posterior density** (HPD) interval, whose endpoints
have equal density.

**Beta(2, 10), 95%.** Equal tails: $(F^{-1}(0.025),F^{-1}(0.975))=(0.0228,\ 0.4128)$, length 0.390.
HPD: $(0.0063,\ 0.3675)$, length 0.361, with $\pi(0.0063\mid x)=\pi(0.3675\mid x)$. The HPD moves toward the
mode because the posterior is skewed. For a symmetric posterior (normal, B Ex. 5.5.1) the two coincide:
$\bar\theta\pm1.96\,\text{sd}$.

---

## 11 · G — minimax (named)

Bolfarine §4.2 (pp. 60–61) ranks rules by their worst-case risk $\max_\theta R(\theta,d)$ instead of the
average (15); Ex. 4.2.2 finds $d(X)=X$ minimax for a Poisson mean under $(\theta-a)^2/\theta$, and Ex. 4.3.2 the
Bayes rule $X/2$ within $\{cX\}$ under an Exp(1) prior. Not examinable here.

---

## Links

- Prev: [[L03-03-normal-measurement-physicists]] (a symmetric posterior: mean = median = mode); next:
  choosing between models instead of values, [[L03-05-model-comparison-bayes-factors]].
  Formulas: [[L03-11-formulas]]; pitfalls: [[L03-12-pitfalls]]; code: [[L03-13-python]] §4.
- Earlier: MSE = variance + bias², [[../L01/L01-05-comparing-estimators-mse-bootstrap|L01 §5]];
  posterior mean vs mode on the coal data, [[../L01/L01-04-first-bayesian-poisson|L01 §4]].
- Rules: [[../../rules/07_bayes|rules/07]].
- Practice (statements in the books): **G 3.5** (p. 39, median under absolute loss), **G 3.6** (p. 39,
  0–1 loss and the mode), **B 4.3** (p. 71), **B 4.5** (p. 71), **B 4.9** (p. 72), **B 4.10** (p. 72),
  **B 5.11** (p. 89, symmetric Bayesian interval).
