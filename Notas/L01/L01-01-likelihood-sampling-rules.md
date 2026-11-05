---
tags: [notes, lecture-01, likelihood, mle, sampling-rules, likelihood-principle, fisher-information, delta-method, p-value]
date: 2026-10-19
status: taught
source: "mle_sampling_rules.pdf (slides 1–11); optimal-samplesize.html; bernoulli-iid-logistic-R.txt (Part one); Bolfarine & Sandoval (2010) §1.3 (pp. 4–6, (1.3.1)–(1.3.2)), §2.1 (pp. 15–18, Def. 2.1.1–2.1.3, Thm 2.1.1), §3.1 (pp. 35–37, Def. 3.1.1–3.1.2, (3.1.3)–(3.1.4), Ex. 3.1.2), §3.2.2 (pp. 44–45, (3.2.3)–(3.2.4)), §6.3 (p. 100, Def. 6.3.1); Greenberg 1e §2.2 (pp. 14–17, (2.3)–(2.5))"
---

# Sampling rules · Same likelihood, different sampling distributions

> **Claim.** Bernoulli trials, a binomial count and a negative-binomial waiting time give **the
> same likelihood** for $\theta$, up to a constant. So the **MLE, the observed information, the
> plug-in standard error, the Wald interval and the Bayesian posterior are all identical.**
> What differs is which of $(s,n)$ is random. That changes the **exact** distribution of
> $\hat\theta$, and with it **bias, exact variance, coverage and p-values.** With $s=1$ success in
> $n=10$ trials, $\hat\theta=0.1$ under both designs. Under inverse sampling, though, its
> mean is **0.256**, and the one-sided p-value against $\theta=0.5$ is **0.0020 instead of 0.0107**.
> Prev: [[L01-00-map]] · Next: [[L01-02-poisson-mle-properties]] · Map: [[L01-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $\theta$ | success probability | $(0,1)$ |
| $y_i$ | outcome of trial $i$ (1 = success) | $\{0,1\}$ |
| $n$ | number of trials | $1,2,\dots$ (fixed for Bernoulli/binomial, random $N$ for negative binomial) |
| $s$ | number of successes, $s=\sum_i y_i$ | $0,\dots,n$ (random $S$ for binomial, fixed for negative binomial) |
| $L(\theta)$, $\ell(\theta)$ | likelihood, log-likelihood | — |
| $J(\theta)=-\ell''(\theta)$ | observed information | $>0$ |
| $I(\theta)=E[J(\theta)]$ | expected (Fisher) information of the whole sample | $>0$ |
| $a,b$ | Beta prior parameters | $>0$ |

---

## 1 · U — one coin, two experimenters

Two researchers watch the same ten tosses, $y=(0,0,0,0,0,0,0,0,0,1)$. The first had decided in
advance to toss **ten times** and count heads. The second had decided to toss **until the first
head**, and it happened to arrive on toss ten. The data are identical, the likelihoods are
proportional, and the MLE is $1/10$ for both. **But they ran different experiments.** If either
of them repeated the experiment, the set of outcomes that *could* have happened would differ:
counts $0,1,\dots,10$ for the first, waiting times $1,2,3,\dots$ for the second.

> **Every frequentist property is a statement about outcomes that did not happen.**
> Bias, standard error, coverage and p-values average over the experiment's sample space. The
> likelihood only looks at the outcome that did happen. The rest of the deck sorts the
> quantities into those two kinds.

---

## 2 · C — three sampling rules, one likelihood (slide 1)

| Rule | Random quantity | Probability of the data |
|---|---|---|
| Bernoulli, $n$ fixed | $Y_1,\dots,Y_n$ iid Ber($\theta$) | $\prod_i\theta^{y_i}(1-\theta)^{1-y_i}$ |
| Binomial, $n$ fixed | $S\sim$ Bin$(n,\theta)$ | $\binom ns\theta^s(1-\theta)^{n-s}$ |
| Negative binomial, $s$ fixed | $N$ = trials until the $s$-th success | $\binom{n-1}{s-1}\theta^s(1-\theta)^{n-s}$ |

Collect the Bernoulli product by adding exponents:

$$L(\theta;y)=\theta^{\sum_iy_i}(1-\theta)^{\sum_i(1-y_i)}=\theta^{s}(1-\theta)^{n-s}.\tag{1}$$

The other two differ from (1) only by a factor that does not contain $\theta$:

$$L(\theta;s)=\binom ns\,\theta^s(1-\theta)^{n-s}\ \propto\ \theta^s(1-\theta)^{n-s},\tag{2}$$

$$L(\theta;n)=\binom{n-1}{s-1}\theta^s(1-\theta)^{n-s}\ \propto\ \theta^s(1-\theta)^{n-s}.\tag{3}$$

The negative-binomial coefficient counts the arrangements in which the $s$-th success falls
**exactly** on trial $n$: the last trial is a success, and $s-1$ successes fall among the first
$n-1$ trials.

> **Likelihood principle (slide 1).** (1), (2) and (3) are in the same equivalence class, so **any
> likelihood-based or Bayesian inference about $\theta$ is the same.** *But* the random quantity is
> different ($S$ against $N$), **so the sampling distribution of anything computed from $L$ is
> different.**

The likelihood here is Bolfarine's (1.3.1) (p. 5) and Def. 3.1.1 (p. 35): the joint probability
of the observed sample, read as a function of $\theta$.

---

## 3 · C — the MLE and the observed information are the same function of the data (slide 2)

Take logs of (1). The constants in (2)–(3) only add $\log\binom{\cdot}{\cdot}$, which vanishes on
differentiation:

$$\ell(\theta)=s\log\theta+(n-s)\log(1-\theta).\tag{4}$$

Differentiate (4) (the score):

$$\ell'(\theta)=\frac{s}{\theta}-\frac{n-s}{1-\theta}.\tag{5}$$

Set (5) to zero, which is Bolfarine's likelihood equation (3.1.3), p. 36:

$$\frac{s}{\hat\theta}=\frac{n-s}{1-\hat\theta}$$

$$s(1-\hat\theta)=(n-s)\hat\theta$$

$$s-s\hat\theta=n\hat\theta-s\hat\theta$$

$$\boxed{\hat\theta=\frac sn}\tag{6}$$

**Second-order check** (B (3.1.4)). Differentiate (5) once more and change sign:

$$J(\theta)=-\ell''(\theta)=\frac{s}{\theta^2}+\frac{n-s}{(1-\theta)^2}>0.\tag{7}$$

So (6) is a maximum. Evaluate (7) at (6), substituting $\hat\theta=s/n$ and $1-\hat\theta=(n-s)/n$:

$$J(\hat\theta)=\frac{s}{(s/n)^2}+\frac{n-s}{\big((n-s)/n\big)^2}=\frac{n^2}{s}+\frac{n^2}{n-s}=\frac{n^2(n-s)+n^2s}{s(n-s)}=\frac{n^3}{s(n-s)}.$$

Divide the numerator and the denominator by $n^2$:

$$\boxed{J(\hat\theta)=\frac{n^3}{s(n-s)}=\frac{n}{\hat\theta(1-\hat\theta)}}\tag{8}$$

At $s=1$, $n=10$: $J(\hat\theta)=1000/(1\cdot9)=111.1=10/(0.1\times0.9)$.

> **What is the same and what is not.** (4)–(8) contain only the numbers $(s,n)$, so they are
> identical in all three experiments. **Which of $(s,n)$ is random** is the only difference
> (slide 2):
>
> | | fixed | random | estimator |
> |---|---|---|---|
> | Bernoulli / binomial | $n$ | $S$ | $\hat\theta=S/n$ |
> | Negative binomial | $s$ | $N$ | $\hat\theta=s/N$ |

---

## 4 · C — binomial: $\hat\theta=S/n$ (slide 3)

**Exact distribution.** $S=\sum_iY_i\sim$ Bin$(n,\theta)$, and $\hat\theta$ takes the value $k/n$
exactly when $S=k$:

$$P\Big(\hat\theta=\frac kn\Big)=\binom nk\theta^k(1-\theta)^{n-k},\qquad k=0,1,\dots,n.\tag{9}$$

Since $E(S)=n\theta$ and $\operatorname{Var}(S)=n\theta(1-\theta)$ (B §1.1.3, p. 2),

$$E(\hat\theta)=\frac{n\theta}{n}=\theta\quad\text{(unbiased)},\qquad \operatorname{Var}(\hat\theta)=\frac{n\theta(1-\theta)}{n^2}=\frac{\theta(1-\theta)}{n}.\tag{10}$$

**Expected (Fisher) information.** Take the expectation of (7) with $S$ random, substituting
$E(S)=n\theta$ and $E(n-S)=n(1-\theta)$:

$$I(\theta)=E\Big[\frac{S}{\theta^2}+\frac{n-S}{(1-\theta)^2}\Big]=\frac{n\theta}{\theta^2}+\frac{n(1-\theta)}{(1-\theta)^2}=\frac n\theta+\frac n{1-\theta}=\frac{n}{\theta(1-\theta)}.\tag{11}$$

The variance (10) equals $1/I(\theta)$ from (11), so $S/n$ attains the Cramér–Rao bound (B Thm 2.1.1, p. 18).
**Asymptotics** (B (3.2.3), p. 44; here the CLT and the MLE theory coincide):

$$\hat\theta\ \stackrel a\sim\ N\Big(\theta,\ \frac{\theta(1-\theta)}{n}\Big).\tag{12}$$

> **Bernoulli or binomial makes no difference.** $S$ is sufficient, and the order of the $y_i$'s
> carries no information about $\theta$.

---

## 5 · C — negative binomial: $\hat\theta=s/N$ (slide 4)

**Exact distribution.** From (3) with $n$ replaced by the random $N=m$:

$$P(N=m)=\binom{m-1}{s-1}\theta^s(1-\theta)^{m-s},\qquad m=s,s+1,\dots\tag{13}$$

and $\hat\theta=s/m$ exactly when $N=m$, so $P(\hat\theta=s/m)$ is (13). **Its support is
$\{1,\ s/(s+1),\ s/(s+2),\dots\}$.** It never reaches 0 and piles up near 0.

**Fisher information.** Now $s$ is fixed and $N$ is random. Use $E(N)=s/\theta$, hence
$E(N-s)=s/\theta-s=s(1-\theta)/\theta$. Substitute into (7), with $n$ replaced by $N$:

$$I(\theta)=E\Big[\frac{s}{\theta^2}+\frac{N-s}{(1-\theta)^2}\Big]=\frac{s}{\theta^2}+\frac{s(1-\theta)/\theta}{(1-\theta)^2}=\frac{s}{\theta^2}+\frac{s}{\theta(1-\theta)}.$$

Put both terms over $\theta^2(1-\theta)$:

$$I(\theta)=\frac{s(1-\theta)+s\theta}{\theta^2(1-\theta)}=\frac{s}{\theta^2(1-\theta)}.\tag{14}$$

**Asymptotics** ($s\to\infty$):

$$\hat\theta\ \stackrel a\sim\ N\Big(\theta,\ \frac{\theta^2(1-\theta)}{s}\Big).\tag{15}$$

---

## 6 · C — the same answer via the delta method (slide 5)

$N$ is the sum of $s$ iid Geometric($\theta$) waiting times, each with mean $1/\theta$ and variance
$(1-\theta)/\theta^2$. By the CLT,

$$N\ \stackrel a\sim\ N\Big(\frac s\theta,\ \frac{s(1-\theta)}{\theta^2}\Big).\tag{16}$$

Take $g(x)=s/x$, so $g'(x)=-s/x^2$. Evaluate at the mean $x=s/\theta$:

$$g'\Big(\frac s\theta\Big)=-\frac{s}{(s/\theta)^2}=-\frac{s\theta^2}{s^2}=-\frac{\theta^2}{s}.\tag{17}$$

The delta method (B (3.2.4), p. 44) gives $\operatorname{Var}(g(N))\approx g'(\mu)^2\operatorname{Var}(N)$.
Substitute (17) and the variance in (16):

$$\operatorname{Var}(\hat\theta)\approx\Big(-\frac{\theta^2}{s}\Big)^2\cdot\frac{s(1-\theta)}{\theta^2}=\frac{\theta^4}{s^2}\cdot\frac{s(1-\theta)}{\theta^2}=\frac{\theta^2(1-\theta)}{s},$$

which is (15) again, and equals $1/I(\theta)$ from (14).

**Plug-in check (slide 5 remark).** Put $\hat\theta=s/n$ into (15), writing $\theta^2=(s/n)^2$:

$$\frac{\hat\theta^2(1-\hat\theta)}{s}=\frac{(s/n)^2(1-\hat\theta)}{s}=\frac{s}{n}\cdot\frac{1-\hat\theta}{n}=\frac{\hat\theta(1-\hat\theta)}{n}.\tag{18}$$

(18) is the plug-in variance from (12), and both equal $J(\hat\theta)^{-1}$ from (8).

> **The plug-in standard errors coincide, so the Wald intervals are identical. The exact
> distributions (9) and (13) are not.** The asymptotic standard error depends only on the
> likelihood's curvature, and the curvature does not depend on the sampling rule.

---

## 7 · C — bias: binomial against negative binomial (slide 6)

- **Binomial:** $E(S/n)=\theta$ exactly, by (10).
- **Negative binomial:** $1/x$ is strictly convex, so **Jensen** gives
  $$E\Big(\frac sN\Big)>\frac{s}{E(N)}=\frac{s}{s/\theta}=\theta.\tag{19}$$
  So $\hat\theta=s/N$ is **biased upward**.

**Closed form for $s=1$** (geometric). Put $s=1$ in (13): $P(N=m)=\theta(1-\theta)^{m-1}$. Then

$$E\Big(\frac1N\Big)=\sum_{m\ge1}\frac1m\,\theta(1-\theta)^{m-1}=\frac{\theta}{1-\theta}\sum_{m\ge1}\frac{(1-\theta)^m}{m}.$$

Use the series $\sum_{m\ge1}x^m/m=-\log(1-x)$ for $|x|<1$ with $x=1-\theta$, so $1-x=\theta$:

$$\boxed{E\Big(\frac1N\Big)=\frac{\theta}{1-\theta}\big(-\log\theta\big)=\frac{-\theta\log\theta}{1-\theta}}\tag{20}$$

**Worked number** at $\theta=0.1$, with $-\log0.1=2.302585$:

$$E(\hat\theta)=\frac{0.1\times2.302585}{0.9}=\frac{0.2302585}{0.9}=0.2558\ \approx\ \mathbf{0.256}.$$

That is **more than twice $\theta$.**

**Haldane (1945).** For $s\ge2$, the estimator $\tilde\theta=(s-1)/(N-1)$ is exactly unbiased.
*Proof (two lines, not on the slide).* Since
$\frac{s-1}{m-1}\binom{m-1}{s-1}=\binom{m-2}{s-2}$,

$$E\Big[\frac{s-1}{N-1}\Big]=\sum_{m\ge s}\binom{m-2}{s-2}\theta^s(1-\theta)^{m-s}=\theta\sum_{m'\ge s-1}\binom{m'-1}{s-2}\theta^{s-1}(1-\theta)^{m'-(s-1)}=\theta\cdot1,$$

with $m'=m-1$. The last sum is (13) for $s-1$ successes summed over its whole support.

> **Moral (slide 6): unbiasedness is a property of the sampling rule, not of the likelihood.**
> $s/N$ and $S/n$ are the same function of the data, the same MLE, and only one of them is
> unbiased.

---

## 8 · Worked — the deck's two data sets (slides 7–9)

Everything is evaluated at $\theta=\hat\theta$. The asymptotic se comes from (18):
$\sqrt{0.1\times0.9/10}=\sqrt{0.009}=0.0949$, and $\sqrt{0.4\times0.6/10}=\sqrt{0.024}=0.1549$.
The exact moments of $s/N$ are the sums $\sum_m (s/m)P(N=m)$ and $\sum_m (s/m)^2P(N=m)$ over (13),
computed in [[L01-11-python]].

| | $s=1,n=10$ Bin | NegBin | $s=4,n=10$ Bin | NegBin |
|---|---|---|---|---|
| $\hat\theta$ | 0.100 | 0.100 | 0.400 | 0.400 |
| Asymptotic se | 0.095 | 0.095 | 0.155 | 0.155 |
| Exact $E(\hat\theta)$ | 0.100 | **0.256** | 0.400 | **0.461** |
| Exact sd$(\hat\theta)$ | 0.095 | **0.281** | 0.155 | **0.178** |
| Wald 95% CI | (−0.086, 0.286) | same | (0.096, 0.704) | same |

**The Wald interval, arithmetic in view:**

$$0.1\pm1.96\times0.0949=0.1\pm0.1859=(-0.086,\ 0.286),\qquad 0.4\pm1.96\times0.1549=0.4\pm0.3036=(0.096,\ 0.704).$$

![Two panels of exact probability mass functions of theta-hat. Left: s=1, theta=0.1; the binomial S/n puts mass 0.35 at 0, 0.39 at 0.1 and 0.19 at 0.2, while the negative binomial s/N has a dense comb of small masses accumulating near 0 plus isolated masses at 1/3, 1/2 and 0.1 at 1; its mean 0.256 is marked. Right: s=4, theta=0.4; the binomial is roughly symmetric around 0.4, the negative binomial is right-skewed with mean 0.461 marked.](figures/L01-sampling-rules-pmf.png)
*The exact pmf (9) against (13) at $\theta=\hat\theta$, $n=10$. The dotted line is the negative-binomial mean (0.256 and 0.461). Source: `mle_sampling_rules.pdf` slides 7–8.*

With $s=1$ the binomial $\hat\theta$ lives on the grid $\{0,0.1,\dots,1\}$ and is centred at
0.1. The inverse-sampling $\hat\theta$ cannot be 0. It has 10% probability of being exactly 1
(a success on the first trial), and the rest is a comb accumulating near 0. That gives a mean
of 0.256 and an sd three times the asymptotic one. With $s=4$ the two shapes are closer, but the
negative binomial is still visibly right-skewed (mean 0.461).

> **Read the table bottom-up.** The asymptotic se is **blind to the sampling rule**; the exact
> distribution is not. And with $s=1$ the Wald interval **leaves $[0,1]$**, so the asymptotics are
> useless at this sample size whichever rule produced the data (slide 9).

---

## 9 · C — the classic consequence: p-values (slide 10)

Test $H_0:\theta=0.5$ against $H_1:\theta<0.5$ (Lindley & Phillips, 1976). The p-value is
Bolfarine's *nível descritivo* (Def. 6.3.1, p. 100): "o menor nível de significância $\alpha$
para o qual a hipótese nula $H_0$ seria rejeitada". It is the null probability of a result at
least as extreme as the one observed, and **"extreme" is defined by the sample space**:

- **Binomial** ($n=10$ fixed): extreme means **few successes**, $p=P(S\le s\mid n,\theta=0.5)$.
- **Negative binomial** ($s$ fixed): extreme means **many trials**, $p=P(N\ge n\mid s,\theta=0.5)$.

**$s=1$, $n=10$.** Binomial:

$$p=P(S\le1)=\frac{\binom{10}0+\binom{10}1}{2^{10}}=\frac{1+10}{1024}=\frac{11}{1024}=\mathbf{0.0107}.$$

Negative binomial: $N\ge10$ means the first 9 trials were all failures:

$$p=P(N\ge10)=0.5^{9}=\frac1{512}=\mathbf{0.0020}.$$

**$s=4$, $n=10$.** Binomial:

$$p=P(S\le4)=\frac{1+10+45+120+210}{1024}=\frac{386}{1024}=\mathbf{0.377}.$$

Negative binomial: $N\ge10$ means **at most 3** successes in the first 9 trials:

$$p=P\big(\text{Bin}(9,0.5)\le3\big)=\frac{1+9+36+84}{512}=\frac{130}{512}=\mathbf{0.254}.$$

| | $s=1,n=10$ | $s=4,n=10$ |
|---|---|---|
| Binomial p-value | 0.0107 | 0.377 |
| Neg. binomial p-value | 0.0020 | 0.254 |

> **Same data, same likelihood, different evidence "against" $H_0$**, because the reference set
> of unobserved outcomes depends on the experimenter's **intentions** (slide 10). At the 1% level
> the first experimenter does not reject and the second does, on identical tosses.

---

## 10 · C — the Bayesian contrast (slide 11; Greenberg §2.2)

With prior $\theta\sim$ Beta$(a,b)$, density $\propto\theta^{a-1}(1-\theta)^{b-1}$, Bayes'
theorem in proportional form (Greenberg (2.3), p. 14) gives, under **any** of (1)–(3):

$$\pi(\theta\mid\text{data})\ \propto\ \underbrace{c\cdot\theta^s(1-\theta)^{n-s}}_{(1),(2)\text{ or }(3)}\cdot\theta^{a-1}(1-\theta)^{b-1}\ \propto\ \theta^{a+s-1}(1-\theta)^{b+n-s-1},$$

where $c\in\{1,\binom ns,\binom{n-1}{s-1}\}$ **cancels in the normalisation**. Hence

$$\theta\mid\text{data}\ \sim\ \text{Beta}(a+s,\ b+n-s),\qquad E(\theta\mid\text{data})=\frac{a+s}{a+b+n}.\tag{21}$$

This is Greenberg's beta–Bernoulli result (p. 16) and his (2.5) (p. 17). It splits (21) as a
weighted average of the prior mean and the MLE:

$$\frac{a+s}{a+b+n}=\frac{a+b}{a+b+n}\cdot\frac{a}{a+b}+\frac{n}{a+b+n}\cdot\frac sn.\tag{22}$$

**Worked (uniform prior, $a=b=1$).** $s=1$: Beta$(1+1,\,1+9)=$ Beta$(2,10)$, mean $2/12=\mathbf{0.167}$.
$s=4$: Beta$(5,7)$, mean $5/12=\mathbf{0.417}$. By (22), with prior mean $1/2$ and weight
$2/12$: $\frac{2}{12}\cdot0.5+\frac{10}{12}\cdot0.1=0.0833+0.0833=0.167$. ✓

> **Take-home (slide 11).** The stopping rule is **irrelevant to the posterior**: it enters only
> through the constants $\binom ns$ or $\binom{n-1}{s-1}$, which cancel. **Likelihood-based
> conclusions obey the likelihood principle; the frequentist properties of $\hat\theta$ (bias,
> exact variance, p-values, coverage) do not.**

---

## 11 · Worked — the site's Bernoulli code (`bernoulli-iid-logistic-R.txt`, Part one)

Data $y=(1,1,1,1,0,0,0,1,1,1)$: $n=10$, $s=7$.

**MLE and Wald intervals.** $\hat\theta=7/10=0.7$, and by (18)
$\text{se}=\sqrt{0.7\times0.3/10}=\sqrt{0.021}=0.1449$:

| Level | $z$ | $0.7\pm z\times0.1449$ | Interval |
|---|---|---|---|
| 90% | 1.645 | $0.7\pm0.2384$ | (0.462, 0.938) |
| 95% | 1.960 | $0.7\pm0.2840$ | (0.416, 0.984) |
| 99% | 2.576 | $0.7\pm0.3733$ | (0.327, **1.073**) |

The 99% interval again leaves $[0,1]$.

**Bayes with Beta(3,3).** The prior mean is $0.5$ and the prior sd is $\sqrt{9/(36\cdot7)}=0.189$. By (21),
Beta$(3+7,\,3+3)=$ Beta$(10,6)$, with

$$E(\theta\mid y)=\frac{10}{16}=0.625,\qquad \text{sd}=\sqrt{\frac{10\cdot6}{16^2\cdot17}}=\sqrt{0.013787}=0.117,$$

and 95% credible interval (0.384, 0.837). The posterior predictive probability that the next
trial is a success is $\Pr(y_{11}=1\mid y)=E(\theta\mid y)=0.625$. Compared with the MLE 0.7, the
estimate is **shrunk toward the prior mean 0.5**, with weight $6/16$ on it by (22).

**Bridge to Class 2.** Part two of the same file gives each trial a regressor $x_i$ and lets
$\Pr(y_i=1\mid x_i)=1/(1+e^{-(\alpha+\beta x_i)})$. The $y_i$ are then **independent but not
identically distributed**, (1) no longer applies, and the MLE ($\hat\alpha=2.877$,
$\hat\beta=17.995$ in the file's comments) has no closed form. That is the logistic regression of
[[../L02/L02-04-logistic-regression|L02 §4]].

---

## 12 · U — how many trials? (`optimal-samplesize.html`)

The Wald margin of error is $E=z_{1-\alpha/2}\sqrt{\theta(1-\theta)/n}$. Solve for $n$:

$$n\ \ge\ \frac{z_{1-\alpha/2}^2\,\theta(1-\theta)}{E^2}.\tag{23}$$

$\theta(1-\theta)\le1/4$, with equality at $\theta=1/2$ (the parabola's vertex), so the worst case is
$n\ge z^2/(4E^2)$. With the page's rounding $z\approx2$ this becomes $n\ge1/E^2$:
**$n\ge400$ for $E=0.05$, and $n\ge10{,}000$ for $E=0.01$.** With $z=1.96$ exactly, (23) gives
$1.96^2\times0.25/0.05^2=384.1$, so $n=385$. The page's Bayesian alternative (the average-length
criterion of M'Lan, Joseph & Wolfson, 2008, with a Beta prior) is **named only**. It belongs
with the priors of Classes 3+4.

---

## 13 · G — what the deck does not settle

- **Which is "right"?** Nothing in this deck. The frequentist answer depends on the design by
  construction. The likelihood principle (Birnbaum, 1962) says it should not. The deck states the
  conflict and lets the numbers make it.
- **Optional stopping.** "Toss until the p-value drops below 0.05" is a sampling rule with its own
  sample space. The likelihood and the posterior ignore it, the nominal p-value does not. The
  p-hacking version of this point is [[L01-08-p-hacking-evidence]].
- **Exact intervals** (Clopper–Pearson for the binomial) repair the $s=1$ coverage problem. They
  are named only; they are not in the deck.

---

## Links

- Next: the same MLE checklist (sufficiency, unbiasedness, consistency, efficiency) for the
  Poisson, [[L01-02-poisson-mle-properties]]. Bias as one part of MSE:
  [[L01-05-comparing-estimators-mse-bootstrap]]. p-values against Bayes factors:
  [[L01-08-p-hacking-evidence]]. All results on one page: [[L01-09-formulas]]. Traps:
  [[L01-10-pitfalls]]. Code with asserts: [[L01-11-python]].
- Class 2: logistic regression drops the iid assumption, [[../L02/L02-04-logistic-regression|L02 §4]].
- Rules: [[../../rules/07_bayes|rules/07]] (conjugate Beta–Bernoulli); scope
  [[../../rules/09_course_program|rules/09]].
- Reading: B §1.3 (pp. 4–6), §2.1 (pp. 15–19), §3.1 (pp. 35–37, Ex. 3.1.2), §3.2.2 (pp. 44–45),
  §6.3 Def. 6.3.1 (p. 100); G §2.2 (pp. 12–18). Class plan: [[../../Map/class-plan#Class 1: Review of basic ingredients|Class 1]].
- Practice (statements in the books; see [[../../Map/exercises-index]]): **B 1.9** (p. 14),
  **B 2.2** (p. 32), **B 2.10** (p. 33), **B 2.11** (p. 33, the geometric case of §5–§7),
  **B 3.17** (p. 55).
