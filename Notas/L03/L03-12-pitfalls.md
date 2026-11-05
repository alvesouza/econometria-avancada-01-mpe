---
tags: [notes, lecture-03, pitfalls, true-false, self-test, review, bayes, mcmc]
date: 2026-10-29
status: taught
source: "The ten section notes L03-01 … L03-10; V/F conventions of rules/00_estilo_avaliacao.md (macro-1 style); every number re-checked by Notas/L03/L03_python_checks.py (§1–§10). The self-test is original; no textbook exercise is reproduced."
---

# Classes 3+4 · Pitfalls — the confusions, each with its minimal counterexample, and an original True/False self-test

> Prev: [[L03-11-formulas]] · Next: [[L03-13-python]] · Map: [[L03-00-map]]

Every number below is asserted in [[L03-13-python]]. Equations are cited by the section note's own
numbering.

---

## Part I — the confusions this material produces

### 1 · $P(\text{data}\mid\text{state})$ vs $P(\text{state}\mid\text{data})$

**The confusion.** A test with 95% sensitivity means a positive patient is 95% likely to be ill.

**Counterexample** (Diego, L03-01 (8)). $P(X=1\mid\text{ill})=0.95$, but $P(\text{ill}\mid X=1)=0.847$ with a 70% prior,
and it would be far lower with a rare disease (Stone: smallpox 0.011 despite the better likelihood).

> **The likelihood is a forward probability; the posterior needs the prior and the predictive.**
> → [[L03-01-bayes-rule-discrete]] §1, §6.

### 2 · Sequential vs batch updating

**The confusion.** Updating one test at a time double-counts or loses information.

**Counterexample** (L03-01 §4). Sequential: 0.70 → 0.8471 → 0.992762. Batch on $(X=1,Y=1)$: 0.992762. Equal
whenever the data are conditionally independent given $\theta$ (L03-01 (9)).
→ [[L03-01-bayes-rule-discrete]] §4; [[L03-02-conjugate-sequential-updating]] §3.

### 3 · Posterior mode, mean and MLE under a uniform prior

**The confusion.** A flat prior makes the Bayes estimate equal the MLE.

**Counterexample** (L03-04 §7). Uniform prior, $s=1$, $n=10$: the **mode** is 0.100 = MLE, but the **mean**
(the quadratic-loss Bayes estimator) is $2/12=0.167$ and the median 0.148. "Flat" fixes the mode,
not the estimator. → [[L03-02-conjugate-sequential-updating]] (7); [[L03-04-bayes-estimators-loss]].

### 4 · Plug-in prediction vs the predictive distribution

**The confusion.** $P(\text{next success})=\hat\theta_{MLE}$.

**Counterexample** (L03-02 (11)). After 0 successes in $n$ trials, the MLE predicts 0 forever; the predictive
under a uniform prior is $1/(n+2)$. The predictive averages over $\theta$'s uncertainty.
→ [[L03-02-conjugate-sequential-updating]] §4.

### 5 · A normal prior's pull vs a heavy-tailed prior's pull

**The confusion.** Two priors with the same mean and variance give the same posterior.

**Counterexample** (L03-03 §6). Normal $N(900,20^2)$ and $t_5(900,240)$ (variance 400 too). At $x=850$: 890.0 vs 891.1.
At $x=1100$: 940.0 vs 1022.0. The normal pull is proportional to the conflict; the $t$ pull is bounded
and fades. → [[L03-03-normal-measurement-physicists]] (11)–(12).

### 6 · "The Bayes estimator is biased, the MLE is not"

**The confusion.** The deck's slide 13 contrast taken as a general rule.

**Counterexample** (L03-04 (14)). Exponential data: $E(n/\sum x_i)=n\theta/(n-1)$, so the MLE is biased too. Bayes
estimators are optimal for Bayes risk ($1/72<1/60$ in B Ex. 4.4.1), not for unbiasedness.
→ [[L03-04-bayes-estimators-loss]] §8–§9.

### 7 · Credible vs confidence interval

**The confusion.** "95% probability that $\theta$ is in my confidence interval."

**Counterexample** (L03-04 §10). A credible interval conditions on the data and is a statement about $\theta$; a
confidence interval is a statement about the procedure over repeated samples (G p. 31). For the
skewed Beta(2, 10) posterior, the equal-tail and HPD intervals differ: (0.023, 0.413) vs (0.006, 0.368).
→ [[L03-04-bayes-estimators-loss]] §10.

### 8 · Maximised likelihood vs marginal likelihood

**The confusion.** The bigger model always wins because it fits at least as well.

**Counterexample** (L03-05 §4). Michaela and Lila both at 0.5 with $m=100$: the two-probability model's
maximised likelihood equals the one-probability model's, yet $\log_{10}B_{12}=+0.756$ for the simpler
model. The marginal likelihood averages over the prior and charges $\frac12\log n$ per extra parameter.
→ [[L03-05-model-comparison-bayes-factors]] §6.

### 9 · Improper priors in Bayes factors

**The confusion.** "Non-informative" priors are safe everywhere.

**Counterexample** (L03-05 (9)). With $c\,\pi(\theta)$ improper, $B_{12}$ scales by $c_1/c_2$, an arbitrary number. Fine
for one model's posterior, meaningless for comparing models. → [[L03-05-model-comparison-bayes-factors]] §7.

### 10 · Accept–reject vs Metropolis–Hastings

**The confusion.** Both reject proposals, so both give independent draws.

**Counterexample** (L03-06 §5, L03-08 §1). Accept–reject retries until acceptance: accepted values are iid
from $f$. MH keeps the current value on rejection: the chain repeats values and its draws are
correlated. → [[L03-06-monte-carlo-simulation]] (7); [[L03-08-metropolis-hastings-hmc]] §2.

### 11 · A printed Monte Carlo standard error vs a valid one

**The confusion.** Any simulation's standard error formula can be trusted.

**Counterexample** (L03-06 §6). Greenberg's importance sampler for the truncated exponential has
$\int g^2f^2/h=\infty$ because $h=\text{Beta}(2,3)$ vanishes at 0. Seeded run: 0.800 with "se" 0.009 against the
truth 0.830. For MCMC, the naive se ignores autocorrelation by a factor $\sqrt{\text{IF}}$.
→ [[L03-06-monte-carlo-simulation]] (11); [[L03-07-markov-chains-gibbs]] (19)–(20).

### 12 · High acceptance rate vs good mixing

**The confusion.** An MH sampler accepting 95% of proposals works well.

**Counterexample** (L03-08 (9)). On $N(0,1)$ with $s=0.1$, acceptance is 0.968 but every step is tiny and the
chain crawls; $s=2.38$ accepts 0.445 and mixes far better. → [[L03-08-metropolis-hastings-hmc]] §4.

### 13 · Many Gibbs draws vs many independent draws

**The confusion.** 5000 draws give a Monte Carlo error of $\sigma/\sqrt{5000}$.

**Counterexample** (L03-07 (18)–(19)). For the bivariate normal with $\rho=0.999$, IF $=999.5$: 5000 draws carry the
information of about 5. Greenberg's means of 1.084 and $-0.623$ from two starts show it.
→ [[L03-07-markov-chains-gibbs]] §8.

### 14 · Lasso zeros vs posterior zeros

**The confusion.** The Bayesian lasso sets coefficients exactly to zero.

**Counterexample** (L03-10 §2). The lasso estimate is the posterior **mode** under a Laplace prior; the
posterior **mean** is never exactly zero, and at large $|y|$ it stays $1/b$ below $y$ (4.59 at $y=6$ vs the
horseshoe's 5.66). → [[L03-10-sparsity-priors]] §2, §5.

### 15 · Complete pooling, no pooling, partial pooling

**The confusion.** Either all hospitals share one rate or each has its own estimate.

**Counterexample** (L03-09 §4). Hierarchical posterior means run from 0.057 to 0.089, between the separate
estimates (0.029–0.130) and the pooled 0.069, with weights $\eta/(\eta+n_i)$ estimated from the data.
→ [[L03-09-hierarchical-models-shrinkage]].

---

## Part II — True/False self-test (original)

**Scoring** ([[../../rules/00_estilo_avaliacao|rules/00]]): V/F score
$=\max\{0,\ \text{correct}-\text{wrong}/2\}\times$ item value; blank items do not count as wrong.
Difficulty: **[E]** easy · **[M]** medium · **[P]** hard. Numbers are illustrative unless a note is cited.
Answers follow each block.

### Block A — Bayes' rule

**Setting (items 1–5).** A Brazilian bank's fraud filter flags 98% of fraudulent card transactions and
3% of legitimate ones. One transaction in a hundred is fraudulent.

1. **[E]** A flagged transaction is more likely fraudulent than not.
2. **[M]** The probability that a random transaction is flagged is 0.0395.
3. **[M]** If a second, independent filter with the same error rates also flags it, the probability of fraud exceeds 0.9.
4. **[P]** If the fraud rate doubled to 2%, the probability of fraud given one flag would double.
5. **[E]** With the two filters, the posterior depends on which filter is consulted first.

**Answers.**

1. **False.** By L03-01 (3)–(4): $0.98\times0.01/(0.98\times0.01+0.03\times0.99)=0.0098/0.0395=0.248$. The filter's 98%
   is $P(\text{flag}\mid\text{fraud})$, not $P(\text{fraud}\mid\text{flag})$ (Part I, 1).
2. **True.** The predictive (L03-01 (4)): $0.0098+0.0297=0.0395$.
3. **True.** Each flag multiplies the odds by the likelihood ratio $0.98/0.03=32.67$. Prior odds $1/99$;
   after two flags $32.67^2/99=10.78$, so $P=10.78/11.78=0.915$ (L03-01 (9), sequential = batch).
4. **False.** The odds double, not the probability: odds $=(0.02/0.98)\times32.67=0.667$, so $P=0.400$, up from
   0.248. The posterior ratio is likelihood ratio × prior ratio (L03-01 §6).
5. **False.** With conditionally independent data the joint likelihood is a product, and products commute
   (L03-01 (9); Part I, 2).

### Block B — conjugate updating and Bayes estimators

**Setting (items 6–10).** A startup models the conversion probability $\theta$ of its landing page with a
Beta(2, 8) prior. Of 30 visitors, 6 sign up.

6. **[E]** The posterior is Beta(8, 32), and its mean is a weighted average of the prior mean and the MLE with weight 0.25 on the prior.
7. **[M]** Under absolute-error loss the Bayes estimate is 0.20.
8. **[M]** The probability that the next visitor signs up, given the data, is 0.20.
9. **[P]** Had the startup recorded visitors until the 6th sign-up (which came at visitor 30), its posterior would differ.
10. **[M]** As the number of visitors grows with the conversion share fixed, the prior's weight in the posterior mean falls like $1/n$.

**Answers.**

6. **True.** L03-02 (4): $(2+6,\ 8+24)$. By (6), $w=(2+8)/(2+8+30)=0.25$; both centres equal 0.2 here
   ($2/10$ and $6/30$), so the mean is $8/40=0.20$.
7. **False.** Absolute loss gives the median (L03-04 (8)). Beta(8, 32) is right-skewed, so the median, 0.195,
   is below the mean 0.200. The mode is $7/38=0.184$.
8. **True.** The predictive equals the posterior mean, L03-02 (11): $8/40$.
9. **False.** Inverse sampling multiplies the likelihood by a different constant only; the kernel
   $\theta^6(1-\theta)^{24}$ and hence the posterior are unchanged (the likelihood principle,
   [[../L01/L01-01-likelihood-sampling-rules|L01-01]] §10). Frequentist bias and p-values would change.
10. **True.** $w=(\alpha_0+\beta_0)/(\alpha_0+\beta_0+n)\approx10/n$ (L03-02 (6), §7).

### Block C — the normal model and Bayes factors

**Setting (items 11–15).** An analyst's prior for next year's inflation is $\theta\sim N(4,0.5^2)$ (%). A survey
gives one reading $x\mid\theta\sim N(\theta,1)$, and $x=6$.

11. **[E]** The posterior mean is 4.4%.
12. **[M]** Because the reading conflicts with the prior, the posterior sd exceeds the prior sd of 0.5.
13. **[P]** A Student-$t_5$ prior with the same centre and variance would put the posterior mean closer to 6 than the normal prior does.
14. **[P]** Comparing $M_1:\theta=4$ with $M_2:\theta\sim N(4,0.5^2)$, the reading favours the sharp hypothesis $M_1$.
15. **[M]** Making $M_2$'s prior very diffuse, $N(4,100^2)$, moves the Bayes factor toward $M_1$, even though $x=6$ is unchanged.

**Answers.**

11. **True.** $w=1/(1+0.25)=0.8$; L03-03 (8): $0.8\times4+0.2\times6=4.4$.
12. **False.** In the normal–normal model $V(\theta\mid x)=w\tau_0^2=0.8\times0.25=0.2$, sd 0.447, whatever $x$ is
    (L03-03 (8)). Conflict does not widen a conjugate normal posterior; it does widen a $t$-prior posterior
    (L03-03 §6).
13. **False.** The conflict is $2/\sqrt{1.25}=1.79$ predictive sd, too mild for the $t$ prior's bounded
    influence to show. Near its centre a $t$ prior with the same variance is more peaked, so it pulls
    slightly harder: quadrature gives 4.387 against 4.400. The $t$ posterior overtakes the normal one only
    for larger conflicts (L03-03 Fig., right panel; Part I, 5).
14. **False.** $m_1=\phi(2)=0.0540$; $m_2$ is the predictive density $N(6\mid4,1.25)=0.0720$; $B_{12}=0.75$, weak
    evidence for $M_2$ (L03-05 (3)–(4)).
15. **True.** $m_2$ becomes $N(6\mid4,10001)\approx0.0040$, so $B_{12}\approx13.5$: a diffuse prior spreads $M_2$'s
    predictive mass over values never seen (L03-05 §7, the Jeffreys–Lindley effect).

### Block D — Monte Carlo and MCMC

**Setting (items 16–21).** A team computes posterior summaries by simulation.

16. **[E]** To halve the Monte Carlo error of an average of independent draws, they need four times as many draws.
17. **[M]** An accept–reject sampler with $c=2.5$ needs on average 2.5 proposals per accepted draw.
18. **[M]** A random-walk Metropolis sampler that accepts 90% of its proposals is mixing well.
19. **[P]** In a two-block Gibbs sampler on a bivariate normal posterior with correlation 0.95, each chain's lag-1 autocorrelation is about 0.90, and about 20 draws carry the information of one independent draw.
20. **[M]** The Metropolis–Hastings acceptance probability requires the posterior's normalising constant.
21. **[E]** Gibbs sampling is Metropolis–Hastings with every proposal accepted.

**Answers.**

16. **True.** The n.s.e. is $\sqrt{V/M}$ (L03-06 (2)).
17. **True.** Each proposal is accepted with probability $1/c$ (L03-06 (7)), so the number of proposals is
    geometric with mean $c$.
18. **False.** High acceptance usually means tiny steps: on $N(0,1)$, $s=0.1$ accepts 96.8% and crawls
    (L03-08 (9); Part I, 12).
19. **True.** $\rho_1=\rho^2=0.9025$ and IF $=(1+0.9025)/(1-0.9025)=19.5$ (L03-07 (18)–(19)).
20. **False.** It enters only through $f(y)/f(x)$, where the constant cancels (L03-08 (4)).
21. **True.** With the full conditional as proposal, $\alpha=1$ (L03-08 (10)).

### Block E — hierarchical and sparsity priors

**Setting (items 22–25).** A regulator compares death rates across hospitals with a Beta–Binomial
hierarchy; a data scientist chooses priors for a regression with 200 candidate predictors.

22. **[M]** In the hierarchical model, a hospital with more cases is pulled more strongly toward the group mean.
23. **[P]** The population precision $\eta$ does not enter the binomial likelihood of the counts given the $p_i$; the data inform it only through how dispersed the $p_i$ appear.
24. **[M]** With a Gaussian prior, the ridge estimate is both the posterior mode and the posterior mean.
25. **[M]** Under a horseshoe prior, a very large observation is shrunk by roughly a constant amount, as under the lasso.

**Answers.**

22. **False.** The weight on the group mean is $\eta/(\eta+n_i)$ (L03-09 (5)): more cases, less pull. Harlem (35
    cases) moves from 0.029 to 0.065; NYP Columbia (353) stays at 0.071.
23. **True.** $f(y\mid p,\eta)=f(y\mid p)$: $\eta$ is not identified through the likelihood (G p. 53; L03-09 §3), and is
    learned from the spread of the $p_i$ relative to binomial noise.
24. **True.** The posterior is normal, so mode = mean (L03-10 (2)); under a Laplace prior they differ.
25. **False.** The Laplace prior keeps a constant bias $1/b$; the horseshoe's $E(\kappa\mid y)\to0$, so large
    observations are left almost unshrunk (5.66 at $y=6$ vs 4.59; L03-10 §5).

---

## Links

- All section notes: [[L03-00-map]]. Formulas: [[L03-11-formulas]]. Code with the asserts: [[L03-13-python]].
- Style: [[../../rules/00_estilo_avaliacao|rules/00]].
