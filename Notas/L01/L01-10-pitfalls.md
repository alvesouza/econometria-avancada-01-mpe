---
tags: [notes, lecture-01, pitfalls, true-false, self-test, review]
date: 2026-10-19
status: taught
source: "The eight section notes L01-01 … L01-08; V/F conventions of rules/00_estilo_avaliacao.md (macro-1 style); every number re-checked by Notas/L01/L01_python_checks.py (§1–§9). The self-test is original; no textbook exercise is reproduced."
---

# Class 1 · Pitfalls — the confusions, each with its minimal counterexample, and an original True/False self-test

> Prev: [[L01-09-formulas]] · Next: [[L01-11-python]] · Map: [[L01-00-map]]

Every number below is asserted in [[L01-11-python]]. Equations are cited by the section note's
own numbering.

---

## Part I — the confusions this material produces

### 1 · Unbiased vs low MSE

**The confusion.** "Unbiased" is treated as "best".

**Counterexample** ($U(0,\theta)$, $\theta=3$, $n=10$; L01-05 (16)–(18)). The **biased** MLE
$x_{(n)}$ has MSE 0.136. The **unbiased** $2\bar x$ has MSE 0.300. Within the family $c\,x_{(n)}$,
the unbiased choice $c=11/10$ gives $\theta^2/120$, and the **biased** $c^*=12/11$ gives
$\theta^2/121$ (L01-05 (29)).

> **MSE = variance + bias² (L01-05 (2)). Unbiasedness removes one term. It does not minimise the
> sum.** → [[L01-05-comparing-estimators-mse-bootstrap]] §2, §8.

### 2 · Same likelihood vs same sampling distribution

**The confusion.** If two experiments give proportional likelihoods, every inference must agree.

**Counterexample** ($s=1$ success in $n=10$ trials; L01-01 §8–§9). Both give $\hat\theta=0.1$,
the same $J(\hat\theta)$, the same Wald interval and the same Beta posterior. But:

| | Binomial ($n$ fixed) | Negative binomial ($s$ fixed) |
|---|---|---|
| $E(\hat\theta)$ at $\theta=0.1$ | 0.100 | **0.256** |
| p-value, $H_0:\theta=0.5$ vs $<$ | 0.0107 | **0.0020** |

> **What depends only on the observed likelihood agrees: the MLE, $J(\hat\theta)$, the Wald
> interval and the posterior. What averages over unobserved outcomes disagrees: bias, exact
> variance, coverage and p-values.** → [[L01-01-likelihood-sampling-rules]] §3, §10.

### 3 · Observed vs expected information

**The confusion.** "The information" is treated as a property of the data alone.

**Counterexample.** $J(\theta)=-\ell''(\theta)$ is computed from the realised likelihood, and it is
the same function under every sampling rule (L01-01 (7)–(8)). $I(\theta)=E[J(\theta)]$ averages
over the design. At $\theta=0.5$, a binomial with $n=10$ has $I=10/0.25=40$, so the asymptotic sd
is 0.158. A negative binomial with $s=1$ has $I=1/(0.25\times0.5)=8$, so the sd is 0.354
(L01-01 (11), (14)). The **plug-ins** coincide at $\hat\theta$, (18). The functions of $\theta$ do not.

> **$J$ is random and design-free. $I$ is fixed and design-dependent. Using $J(\hat\theta)$ for
> the standard error is what makes the Wald interval blind to the stopping rule.**

### 4 · p-value vs $P(H_0\mid x)$

**The confusion.** "$p=0.036$" is read as "a 3.6% chance that $H_0$ is true".

**Counterexample** ($X\sim N(\theta,1)$, $H_0:\theta=0$ vs $H_1:\theta=4$, $x=1.8$; L01-08 (5)–(10)).
$p=0.036$, yet with equal priors $P(H_0\mid x)=1-0.310=\mathbf{0.690}$. The data favour $H_0$:
$BF_{01}=e^{0.8}=2.23$.

> **The p-value is a tail area under $H_0$. It never looks at $H_1$, so it cannot be a posterior
> probability.** Every $x\in(1.645,\,2)$ is "significant" and also favours $H_0$, by (8).
> → [[L01-08-p-hacking-evidence]] §4.

### 5 · Profiling vs integrating

**The confusion.** $w(\tau)$ in L01-03 (7) is treated as "the posterior of the change point".

**Counterexample** (toy series $y=(6,1,1,1,1,1,1,1)$, uniform prior on the cut, Exp(1/2) priors
on both rates for the integrated version, L01-03 (10)). The weight on "the break is after year 1"
is **0.783 profiled** and **0.653 integrated**. The one-year segment fits its own count exactly
($\hat\lambda_1=6$). Profiling keeps that perfect fit and ignores how uncertain a rate estimated
from one observation is. Integrating charges for that uncertainty. On the coal data both routes
give 0.251 at 1891, because both segments are long (L01-03 §8).

> **Profiling plugs in the peak height. Integrating keeps the area. They agree only when every
> segment is long and the prior is weak.**

### 6 · Overdispersion vs a change point

**The confusion.** "$s^2/\bar y=1.59$, $p<0.001$, so the rate changed."

**Counterexample.** $s^2/\bar y$ does not depend on the **order** of the years. Shuffle the 112
coal counts and the dispersion index is still exactly 1.592, with $p<0.001$. But the best-cut LR
of the shuffled series has a 95% quantile of about **14** across permutations, against **70.0**
in calendar order. Overdispersion also arises from year-to-year rate heterogeneity with no break
at all.

> **Overdispersion says "not one Poisson rate". Only the time structure (profile likelihood,
> segment fits) says "a change around 1890".** → [[L01-03-coal-mining-change-point]] §3, §5.

### 7 · A searched LR referred to $\chi^2_1$

**The confusion.** LR = 70.0, so $p=P(\chi^2_1>70)$.

**Counterexample.** Simulate iid Poisson(1.705) series of length 112, so there is **no** change,
and maximise the LR over all 111 cuts. The 95% quantile is **9.9**, not $\chi^2_1$'s 3.84. A
nominal 5% test with the $\chi^2_1$ cut-off would reject far too often. Here 70.0 lies above
every one of 4,000 null and 4,000 permutation draws, so the conclusion survives. The $\chi^2_1$
p-value does not.

> **Wilks needs a regular problem. A searched, discrete, unidentified-under-$H_0$ $\tau$ is not
> one.** → [[L01-03-coal-mining-change-point]] §6.

### 8 · $R^2$ vs out-of-sample fit

**The confusion.** A higher $R^2$ means a better model.

**Counterexample** (Boston, interaction order $k=5$, $p=2380>n=253$; L01-06 §7).
$R^2_{in}=1.0000$, $R^2_{out}=0.052$, and the test RMSE is 47.13 against 4.48 for the plain model.

> **$R^2$ cannot fall when a column is added (L01-06 (21)), so it cannot choose between nested
> models. The training error is optimistic by $2p\sigma^2/n$ (L01-06 (26)–(27)).**

### 9 · Significant vs important

**The confusion.** A joint $F$ of 13.22 ($p<0.0001$) means the variables matter a lot.

**Counterexample** (abstention, model (4) vs (2); L01-06 §8.3). The size dummies are jointly
significant, yet $\bar R^2$ moves from 0.754 to **0.756**. With $n=5{,}565$, a tiny share of
variance is still precisely estimated.

### 10 · Stationary vs unit root (and "persistent" vs "nonstationary")

**The confusion.** A very persistent AR(1) is treated as nonstationary. Or a VAR with a
coefficient above 1 is treated as explosive.

**Counterexamples.** $\phi=0.9$ is stationary, with equilibrium variance $5.26\sigma^2$ and
half-life 6.6. Only $\phi=1$ has $V(y_t)=t\sigma^2$ and no equilibrium (L01-07 (9), (17), (18)).
Tsay's Example 8.3 has $\Phi_{22}=1.1$, yet its eigenvalues are 0.8 and 0.5, so it is
**stationary** (L01-07 §9.1).

> **Stationarity is decided by $\lvert\phi\rvert<1$, or by the eigenvalues of $\Phi$. It is not
> decided by how slowly the ACF decays, or by any single coefficient.**

### 11 · Consistency vs unbiasedness

**The confusion.** The two are treated as the same property, or one is assumed to imply the
other.

**Counterexamples** ($U(0,\theta)$):

| Estimator | Unbiased? | Consistent? | Why |
|---|---|---|---|
| $x_{(n)}$ | no (bias $-\theta/(n+1)$) | **yes** | MSE $2\theta^2/[(n+1)(n+2)]\to0$ |
| $2x_1$ (double the first draw) | **yes** | no | MSE $=\theta^2/3$ for every $n$ |
| $\bar x$ | no (for $\theta$) | no (it converges to $\theta/2$) | MSE $\to\theta^2/4$ |

Also $s/N$ in inverse sampling is biased (0.256 at $\theta=0.1$, $s=1$) but consistent as
$s\to\infty$ (L01-01 (15)).

> **Unbiasedness is about the centre at a fixed $n$. Consistency is about the limit. MSE $\to0$
> gives consistency, with or without bias.**

### 12 · The nonparametric bootstrap for the maximum

**The confusion.** "The bootstrap always works if $n$ is large."

**Counterexample** (L01-05 (32)). The resampled maximum equals the observed one with probability
$1-(1-1/n)^n$: 0.651 at $n=10$, **0.634 at $n=100$**, and $\to0.632$. The true law of $x_{(n)}$ is
continuous. In the deck the bootstrap SD of $x_{(n)}$ is too small at $n=50$ (0.041 against
0.058) and too large at $n=100$ (0.036 against 0.029). **The shape is wrong at every $n$.**

> **The empirical distribution has no mass beyond its own maximum. A statistic that lives on the
> edge of the support cannot be bootstrapped from it. Resample from the fitted
> $U(0,\hat\theta)$ instead** (L01-05 §11).

### 13 · Uncorrelated vs independent

**Counterexample** (IBM monthly returns, L01-07 §2). Ljung–Box on returns gives $Q(30)=38.2$,
$p=0.144$, so no autocorrelation. On **squared** returns it gives $Q(30)=182.1$,
$p\approx10^{-23}$. The returns are uncorrelated but not independent: their size is predictable
(volatility clustering, Class 8).

### 14 · Asymptotics where they do not apply

**Counterexamples.** With $s=1$, $n=10$, the Wald interval is $(-0.086,\ 0.286)$, which leaves
$[0,1]$ (L01-01 §8). The uniform MLE is **not** a root of the score:
$\partial\log L/\partial\theta=-n/\theta$ never vanishes, and the maximum is at the boundary
$x_{(n)}$ (L01-05 (25)). For iid Poisson with $s_n=0$, the MLE **does not exist** on $\lambda>0$
(L01-02 §4).

### 15 · A confident posterior vs a right model

**Counterexample** (L01-04 §7). On all 112 coal years the posterior mean is 1.707, with a tight
posterior around it. It is a precise estimate of a single rate that L01-03 showed does not
exist. **The prior regularises the estimate. It does not test the likelihood.**

### 16 · 0.81 as the false-positive rate of a specification search

**The confusion.** "32 tries means an 81% false-positive rate."

**Counterexample** (L01-08 §3). $1-0.95^{32}=0.806$ assumes **independent** tests. With 32
one-sided $z$-tests sharing a common component (pairwise correlation 0.5, like re-analyses of
the same 30 students) the family-wise rate is **0.405**. It is still eight times the nominal
0.05, but it is not 0.81. The real binary-choice count of the deck's setup is 162, not 32.

---

## Part II — True/False self-test (original)

**Scoring** ([[../../rules/00_estilo_avaliacao|rules/00]]): V/F score
$=\max\{0,\ \text{correct}-\text{wrong}/2\}\times$ item value; blank items do not count as wrong.
Difficulty: **[E]** easy · **[M]** medium · **[P]** hard. Numbers are illustrative unless a note
is cited. Answers follow each block.

### Block A — likelihood and sampling rules

**Setting (items 1–5).** Two Anvisa inspectors estimate the defect rate $\theta$ of a vaccine
line. Inspector A audits a **fixed** batch of 20 vials and finds 2 defective. Inspector B audits
vials **until the 2nd defective** appears, which happens at the 20th vial.

1. **[E]** Both inspectors' maximum likelihood estimates equal 0.10.
2. **[M]** Because the two MLEs coincide, B's estimator $2/N$ is unbiased for $\theta$, just as A's $S/20$ is.
3. **[M]** With a uniform Beta(1,1) prior, A and B obtain the same posterior for $\theta$.
4. **[P]** Testing $H_0:\theta=0.25$ against $\theta<0.25$ at the 5% level, A and B necessarily reach the same decision, since their likelihoods are proportional.
5. **[M]** The Wald 95% intervals of A and B, built from the observed information at the MLE, are identical.

**Answers.**

1. **True.** Both likelihoods are proportional to $\theta^2(1-\theta)^{18}$ (L01-01 (1)–(3)). The
   score (5) vanishes at $\hat\theta=2/20=0.10$ whichever constant, $\binom{20}{2}$ or $\binom{19}{1}$,
   multiplies the kernel. The MLE uses only the realised likelihood, so the sampling rule cannot
   change it.
2. **False.** The MLE is the same *function of the data*. Its *sampling distribution* is not.
   Under inverse sampling $N$ is random, and $1/x$ is convex, so Jensen gives $E(2/N)>\theta$
   (L01-01 (19)). At $\theta=0.1$ the exact mean is 0.165. Haldane's $(s-1)/(N-1)=1/(N-1)$ is the
   unbiased one. A's $S/20$ is unbiased by (10). The converse trap is "same likelihood ⇒ same
   bias".
3. **True.** The posterior is Beta$(1+2,\,1+18)=$ Beta(3,19), with mean 0.136, under either rule.
   The binomial coefficients cancel in the normalisation (L01-01 (21)). This is the likelihood
   principle at work: the stopping rule does not enter Bayesian inference.
4. **False.** "Extreme" is defined by each sample space. For A, $p=P(S\le2\mid n=20,\theta=0.25)=0.091$:
   **do not reject**. For B, $p=P(N\ge20\mid s=2,\theta=0.25)=P(\text{Bin}(19,0.25)\le1)=0.031$:
   **reject**. Identical vials, opposite verdicts. This is L01-01 §9 with new numbers.
5. **True.** $J(\hat\theta)=n/[\hat\theta(1-\hat\theta)]=20/(0.1\times0.9)=222.2$ in both cases
   (L01-01 (8)), and the plug-in variances coincide by (18). The interval is also poor in both
   cases, $0.10\pm1.96\times0.067=(-0.031,\ 0.231)$, which leaves $[0,1]$. Being "the same" is not
   being "right".

### Block B — the Poisson MLE

**Setting (items 6–9).** An analyst models the yearly number of offshore oil-spill incidents
reported to the ANP as iid Poisson$(\lambda)$ (illustrative).

6. **[E]** If the model is right, no unbiased estimator of $\lambda$ has a smaller variance than $\bar y$.
7. **[M]** The sample variance $s^2$ is also unbiased for $\lambda$. Both it and $\bar y$ are consistent, so for large samples they are equally precise.
8. **[M]** For any data set, the Poisson likelihood has a maximiser in $(0,\infty)$.
9. **[P]** At $\lambda=2$ and $n=50$, Chebyshev's lower bound on $P(\lvert\bar y-\lambda\rvert<0.25)$ is a close approximation to the exact probability.

**Answers.**

6. **True.** $V(\bar y)=\lambda/n$ equals the Cramér–Rao bound $1/I(\lambda)=\lambda/n$
   (L01-02 (12), (17)–(18)), so $\bar y$ is efficient. Under the bound's regularity conditions no
   unbiased competitor can do better. (It is also the UMVUE, L01-02 §9.)
7. **False.** Both are unbiased and consistent, but $V(s^2)=\lambda/n+2\lambda^2/(n-1)$
   (L01-02 (19)). Its efficiency tends to $1/(1+2\lambda)$, which is 0.2 at $\lambda=2$, so $s^2$
   needs about **five times** the data. Consistency is a limit statement. It says nothing about
   precision at any $n$.
8. **False.** If every year has zero incidents ($s_n=0$), then $\ell(\lambda)=\log c-n\lambda$ increases
   as $\lambda\downarrow0$, and there is no maximum on the open space (L01-02 §4). This happens with
   probability $e^{-n\lambda}$, which is not negligible for small $n\lambda$.
9. **False.** Chebyshev gives $1-2/(50\times0.25^2)=0.36$. The exact probability is 0.789, from
   $s_n\sim$ Poisson(100) (L01-02 §8). The bound proves consistency but is far too crude to quantify it.

### Block C — the change point and the first prior

**Setting (items 10–14).** Yearly counts of track incidents on a metro network (illustrative)
and the coal-mining series of L01-03.

10. **[M]** A dispersion index $s^2/\bar y=1.6$ with dispersion-test $p<0.001$ shows that the incident rate changed at some date.
11. **[P]** In the coal data, LR = 70.0 at the profile-maximising cut, so the correct p-value is $P(\chi^2_1>70)$.
12. **[E]** The single-rate model can never attain a higher maximised likelihood than the best two-regime model.
13. **[E]** With an Exp$(a)$ prior and $n$ iid Poisson counts summing to $s_n$, the posterior of $\lambda$ is Gamma with shape $s_n+1$ and rate $a+n$.
14. **[M]** With the Exp(1/2) prior, the posterior mean $(s_n+1)/(n+1/2)$ always exceeds the MLE $s_n/n$, because the prior adds one pseudo-event.

**Answers.**

10. **False.** The index ignores the order of the years. Shuffling the coal series leaves it at
    exactly 1.592, yet the shuffled best-cut LR has a 95% quantile near 14, against 70 in calendar
    order. Overdispersion rules out *one* Poisson rate. A change point is one explanation;
    year-to-year heterogeneity is another. Locating a break needs the time structure.
11. **False.** $\tau$ was **chosen to maximise** the statistic over 111 candidates. It is not
    identified under $\lambda_1=\lambda_2$, and it is discrete, so Wilks does not apply
    (L01-03 §6). Under an iid Poisson null with no break, the maximised LR has a 95% quantile of
    9.9, not 3.84. The single-rate model is still rejected, because 70 exceeds every simulated
    null draw.
12. **True.** One rate is the special case $\lambda_1=\lambda_2$ of the two-regime model (3).
    Maximising over a larger set cannot give a lower maximum, so the dashed line in
    `L01-coal-profile-likelihood` lies below every cut.
13. **True.** Prior kernel $e^{-a\lambda}$ times likelihood kernel $\lambda^{s_n}e^{-n\lambda}$
    gives $\lambda^{s_n}e^{-(a+n)\lambda}$, which is the Gamma$(s_n+1,\ a+n)$ kernel (L01-04 (6)–(8)).
    Exp$(a)$ is Gamma(1, $a$), so the update adds the count to the shape and the exposure to the rate.
14. **False.** The prior adds one event **and half a year**. By (13) the posterior mean is a
    weighted average of the prior mean $1/a=2$ and $\bar y$, so it exceeds the MLE only when
    $\bar y<2$. On the 1851–1891 data, $\bar y=3.098>2$ and the posterior mean is 3.084, which is
    *below* the MLE. The pull is toward the prior centre, not always upward.

### Block D — MSE and the bootstrap

**Setting (items 15–19).** A procurement auditor at the TCU models winning discounts in a
sealed-bid auction as iid $U(0,\theta)$ and wants the upper bound $\theta$ (illustrative).

15. **[E]** An unbiased estimator of $\theta$ always has a smaller MSE than a biased one.
16. **[M]** The MLE of $\theta$ is found by setting the score $\partial\log L/\partial\theta$ to zero.
17. **[M]** Among all estimators of the form $c\,x_{(n)}$, the unbiased one, $c=(n+1)/n$, has the smallest MSE.
18. **[M]** With $n=2$ bids, $x_{(n)}$ has strictly smaller MSE than $2\bar x$.
19. **[P]** As $n$ grows, the nonparametric bootstrap distribution of $x^*_{(n)}$ approaches the true sampling distribution of $x_{(n)}$.

**Answers.**

15. **False.** At $\theta=3$, $n=10$, the biased $x_{(n)}$ has MSE 0.136 and the unbiased $2\bar x$
    has 0.300 (L01-05 (17)–(18)). MSE $=V+B^2$: a small bias can buy a large cut in variance.
16. **False.** $L(\theta)=\theta^{-n}\mathbb 1(\theta\ge x_{(n)})$, so the score $-n/\theta$ never
    vanishes. The likelihood is decreasing wherever it is positive, so the maximum sits on the
    boundary $\theta=x_{(n)}$ (L01-05 (24)–(25); B Ex. 3.1.3).
17. **False.** $\text{MSE}(c)$ is minimised at $c^*=(n+2)/(n+1)$, which is below $(n+1)/n$. The
    optimum shrinks slightly and accepts a bias of $-\theta/(n+1)^2$. At $n=10$:
    $\theta^2/121<\theta^2/120$ (L01-05 (28)–(29)).
18. **False.** At $n=2$ both MSEs equal $\theta^2/6$, because $(n-1)(n-2)=0$ in (20). The strict
    ranking (22) needs $n\ge3$. That is why the handwritten "$n\ge2$" is wrong.
19. **False.** The resampled maximum equals the observed maximum with probability
    $1-(1-1/n)^n\to0.632$ (L01-05 (32)). That point mass never disappears, while the true law of
    $x_{(n)}$ is continuous. The bootstrap is **inconsistent** here. The parametric bootstrap from
    $U(0,\hat\theta)$ is not.

### Block E — Gaussian linear regression

**Setting (items 20–24).** An IPEA analyst regresses municipal outcomes on several regressors
by OLS with an intercept, as in the abstention study of L01-06 §8.

20. **[E]** Adding a regressor can never lower $R^2$.
21. **[M]** Adding a regressor raises adjusted $R^2$ only if its $t$-statistic is significant at 5%.
22. **[M]** Under Gaussian errors, the maximum likelihood estimator $\text{RSS}/n$ is unbiased for $\sigma^2$.
23. **[P]** For a fixed design and a correct linear model with $p$ columns, the expected training MSE understates the expected test MSE at the same design by $2p\sigma^2/n$.
24. **[M]** Since the four size dummies are jointly significant ($F=13.22$, $p<0.0001$), adding them must raise the adjusted $R^2$ substantially.

**Answers.**

20. **True.** The smaller model is the larger one with the extra coefficient set to zero, so the
    minimised RSS cannot rise (L01-06 (21)). That is exactly why $R^2$ cannot select a model.
21. **False.** The exact condition is $\lvert t\rvert>1$ (W p. 181; L01-06 §5), far below the 5%
    critical value. $\bar R^2$ is a lenient criterion: in the seeded best-subset simulation it keeps
    $d=5$ where BIC picks the true $d=3$.
22. **False.** $E(\text{RSS})=\sigma^2(n-q)$ (L01-06 (18)), so $E(\text{RSS}/n)=\sigma^2(n-q)/n<\sigma^2$.
    The unbiased estimator divides by $n-q$. The MLE and the unbiased estimator are different here,
    while the $\hat\beta$'s are the same.
23. **True.** $E(\text{MSE}_{in})=\sigma^2(1-p/n)$ and $E(\text{MSE}_{out})=\sigma^2(1+p/n)$
    (L01-06 (26)–(27)). The gap is $2p\sigma^2/n$: the training error is optimistic in proportion to
    the number of parameters, and $C_p$ adds exactly that back.
24. **False.** $\bar R^2$ moves from 0.754 to 0.756. With $n=5{,}565$, a very small share of
    variance is estimated precisely. Significance and explanatory share answer different questions.
    The group's $F>1$ guarantees only that $\bar R^2$ rises, not by how much.

### Block F — AR and VAR

**Setting (items 25–28).** A Banco Central analyst models a monthly inflation-gap series.

25. **[E]** An AR(1) with $\phi=0.95$ is nonstationary because shocks to it are very persistent.
26. **[M]** For a Gaussian AR(1) with $\lvert\phi\rvert<1$, the distribution of $y_t$ given any starting value $y_0$ converges to $N\big(\mu,\sigma^2/(1-\phi^2)\big)$.
27. **[P]** A VAR(1) whose coefficient matrix has an entry greater than 1 is necessarily explosive.
28. **[M]** OLS of $y_t$ on $(1,y_{t-1})$ gives the exact Gaussian maximum likelihood estimates of an AR(1).

**Answers.**

25. **False.** Stationarity needs only $\lvert\phi\rvert<1$ (L01-07 (9)). At $\phi=0.95$ the
    equilibrium variance is $\sigma^2/(1-0.9025)=10.26\sigma^2$, finite, and the half-life is about
    13.5 periods. Persistent is not the same as a unit root. Only at $\phi=1$ does the variance grow like $t\sigma^2$.
26. **True.** From (15), the conditional mean $\mu+\phi^t(y_0-\mu)\to\mu$ and the conditional
    variance $\sigma^2(1-\phi^{2t})/(1-\phi^2)\to\sigma^2/(1-\phi^2)$. The start is forgotten
    geometrically (L01-07 (16)).
27. **False.** Stationarity depends on the eigenvalues of $\Phi$, not on its entries. Tsay's
    Example 8.3 has $\Phi_{22}=1.1$ and eigenvalues 0.8 and 0.5, so it is stationary with mean
    $(1,2)'$ (L01-07 §9.1).
28. **False.** OLS maximises the **conditional** likelihood given $y_1$ (L01-07 (13)). The exact
    likelihood also contains $p(y_1)=N\big(\mu,\sigma^2/(1-\phi^2)\big)$, which depends on $\phi$
    and imposes $\lvert\phi\rvert<1$. The two estimates differ slightly and coincide asymptotically.

### Block G — p-values and evidence

29. **[E]** Under $H_0$, the p-value of a test with a continuous statistic is uniformly distributed on $[0,1]$.
30. **[P]** With $X\sim N(\theta,1)$, $H_0:\theta=0$, $H_1:\theta=4$ and equal prior probabilities, an observation whose one-sided p-value is 0.03 is evidence in favour of $H_1$.

**Answers.**

29. **True.** $p=1-F_0(T)$, and $F_0(T)\sim U(0,1)$ under $H_0$ by the probability integral
    transform, so $P_{H_0}(p\le\alpha)=\alpha$ (L01-08 (1)). This is what makes the *minimum* of
    many p-values misleading: 32 independent uniforms fall below 0.05 at least once with
    probability 0.806.
30. **False.** $p=0.03$ means $x=1.881$. By (8), $BF_{10}=e^{4(1.881)-8}=0.621<1$, so the data favour
    $H_0$, and $P(H_1\mid x)=0.383$. Any $x\in(1.645,2)$ is significant at 5% yet closer to 0 than
    to 4. The p-value never looks at where $H_1$ is.

---

## Part III — the distinctions that cost most points

| Pair | The difference |
|---|---|
| Likelihood vs sampling distribution | the observed curve vs the average over outcomes that did not happen |
| $J(\hat\theta)$ vs $I(\theta)$ | realised curvature (design-free) vs expected curvature (design-dependent) |
| Unbiased vs minimum MSE | the centre alone vs centre and spread together |
| Unbiased vs consistent | a fixed-$n$ statement vs a limit |
| Profile vs integrated likelihood | the peak height vs the area under the curve |
| Overdispersion vs change point | "not one rate" vs "two rates, in this order" |
| p-value vs Bayes factor vs posterior | a tail area under $H_0$ vs a ratio of heights vs a probability of the hypothesis |
| $R^2$ vs test error | can only rise with $p$ vs rises once noise is fitted |
| Persistent vs unit root | $\lvert\phi\rvert<1$ near 1 vs $\phi=1$ |
| Nonparametric vs parametric bootstrap | resample the data vs resample the fitted model |

---

## Links

Map: [[L01-00-map]] · Formulas: [[L01-09-formulas]] · Code: [[L01-11-python]] · Class 2
pitfalls: [[../L02/L02-08-pitfalls|L02 §8]] · Grading conventions:
[[../../rules/00_estilo_avaliacao|rules/00]].
