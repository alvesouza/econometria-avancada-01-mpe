---
tags: [notes, lecture-01, p-values, p-hacking, multiple-testing, bonferroni, bayes-factor, replication]
date: 2026-10-19
status: taught
source: "part1-p-hacking.pdf (13 slides: p-hacking setup, 1 − 0.95^32, Bonferroni, X = 1.8 example, Bayes factor, required prior odds); p_hacking_slides-economics.pdf (12 slides: definitions, replication crisis, evidence in economics, reforms, references)"
---

# p-hacking and evidence · why 32 tries make "significance" likely, and why p = 0.036 can favour the null

> **Claim.** **A p-value is calibrated for one pre-specified test.** Search over 32 specifications of a null effect and, if they were independent, the chance that at least one gives $p<0.05$ is $1-0.95^{32}\approx0.81$; Bonferroni restores the 5% family-wise rate by demanding $p<0.05/32\approx0.0016$. **Even a single honest $p<0.05$ is not evidence for $H_1$**: with $X\sim N(\theta,1)$, $H_0:\theta=0$ vs $H_1:\theta=4$ and $X=1.8$, $p=0.036$, yet the data are $e^{0.8}=2.23$ times likelier under $H_0$, and with equal priors $P(H_1\mid x)=0.31$. **To reach $P(H_1\mid x)=0.9$ from these data one must start from prior odds of about 20:1 for $H_1$** — the hidden prior that reading $p<0.05$ as strong evidence assumes.
> Prev: [[L01-07-ar-var-review]] · Next: [[L01-09-formulas]] · Map: [[L01-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $\alpha$ | nominal size of each test | deck: 0.05 |
| $m$ | number of specifications (tests) tried | deck: 32 |
| $p$ | p-value of one test | $[0,1]$ |
| $X$ | the single observation, $X\sim N(\theta,1)$ | |
| $H_0,H_1$ | $\theta=0$ and $\theta=4$ | |
| $\Phi,\phi$ | standard normal CDF and density | |
| $f(x\mid H_j)$ | density of $X$ under $H_j$ | |
| $BF_{10}=f(x\mid H_1)/f(x\mid H_0)$, $BF_{01}=1/BF_{10}$ | Bayes factors (likelihood ratio for two point hypotheses) | $>0$ |
| $P(H_j)$, $P(H_j\mid x)$ | prior and posterior probabilities | |

---

## 1 · U — what p-hacking is (part1 slide 3; economics deck slides 3–4)

> "P-hacking (or data dredging) is the misuse of data analysis to produce statistically significant results (P < 0.05) where none may exist, often by trying multiple methods until a desired result appears." (part1, slide 3, quoting Wikipedia)

The practices (economics deck, slide 4): **specification searching** (many regressions, report the cleanest); **selective controls**; **sample slicing** (outliers, windows, subsamples); **outcome switching**; **optional stopping** (collect until significant); **HARKing** — hypothesising after the results are known. None requires bad faith; each is a fork in what Gelman and Loken (2014) call "the garden of forking paths". The formal symptom (slide 3): **under $H_0$ p-values are uniform on $[0,1]$, and selective search produces a discontinuity at $p=0.05$** (Brodeur et al., 2016).

---

## 2 · C — why a single p-value has size α

Let $T$ be a test statistic with continuous CDF $F_0$ under $H_0$, rejecting for large $T$, so $p=1-F_0(T)$. For $0<\alpha<1$:

$$P_{H_0}(p\le\alpha)=P_{H_0}\big(F_0(T)\ge1-\alpha\big)=1-P_{H_0}\big(F_0(T)<1-\alpha\big)=1-(1-\alpha)=\alpha,\tag{1}$$

because $F_0(T)\sim U(0,1)$ under $H_0$ (probability integral transform). **(1) is a statement about one test, chosen before seeing the data.** It says nothing about the smallest of several p-values — which is what a reader is shown after a search.

---

## 3 · C — the combinatorial explosion (part1 slides 4–6)

**The setup (slide 4).** Does a new teaching method raise test scores? $n=30$ students, treatment vs control, **true effect zero**. The researcher explores: outlier rule (all / exclude >2 SD / exclude >1.5 SD); covariates (none / GPA / GPA + gender); sample (all / exclude late enrollees / exclude absentees); one- or two-tailed; outcome at week 4, 6 or 8.

**The count (slide 5).** "With 5 binary decisions, there are up to $2^5=32$ specifications." Let $A_j$ be "specification $j$ rejects". If the $m$ tests were independent, each with size $\alpha$ by (1):

$$P(\text{no rejection})=\prod_{j=1}^m P(A_j^c)=(1-\alpha)^m\tag{2}$$

$$P(\text{at least one rejection})=1-(1-\alpha)^m\tag{3}$$

Substituting $\alpha=0.05$, $m=32$ into (3):

$$1-0.95^{32}=1-0.1937=0.806\approx0.81.$$

> **"There is roughly an 81% chance of finding at least one 'significant' result purely by chance, if the researcher reports only the best-looking specification."** (slide 5). A seeded check run for this note — 200,000 replications of 32 independent size-0.05 tests — gives 0.808.

| $m$ | 1 | 5 | 10 | 32 | 162 |
|---|---|---|---|---|---|
| $1-0.95^m$ | 0.050 | 0.226 | 0.401 | **0.806** | 0.9998 |

**Two qualifications the slide's arithmetic hides.**

- **The count.** The table's options are not binary: $3\times3\times3\times2\times3=162$ combinations, for which (3) gives $0.9998$. "Up to 32" is the binary simplification.
- **The independence.** All specifications use the *same 30 students*, so their test statistics are strongly positively correlated, and (2) does not hold. For two-sided tests on jointly normal statistics, Šidák's inequality gives $P(\text{no rejection})\ge(1-\alpha)^m$, so **0.81 is an upper bound**; at the other extreme, 32 perfectly correlated tests are one test, with rate 0.05. The true family-wise rate lies between — usually far above 0.05, which is the point.

**Bonferroni (slide 6).** Test each specification at $\alpha/m$. By the union bound, with no independence assumption at all,

$$P\Big(\bigcup_{j=1}^m A_j\Big)\le\sum_{j=1}^mP(A_j)=m\cdot\frac\alpha m=\alpha,\tag{4}$$

so the family-wise rate is at most $\alpha$: here $p<0.05/32=0.0015625\approx0.0016$. (Without the correction the same bound reads $32\times0.05=1.6$ — useless, which is why (3) was needed.)

**What the frequentist correction cannot fix (slide 6).** "From the likelihood principle: inference should depend only on the data observed, not on the hypothetical tests that could have been run" — yet a p-value's meaning depends on exactly those unrun tests, and "the unreported search path is invisible to the reader." The same tension drives the stopping-rule example of [[L01-01-likelihood-sampling-rules]]: identical likelihoods, different p-values. **Remedy (slide 6): Bayesian model averaging or a multiverse analysis** — report the estimate across all specifications, so fragility is visible. The abstention regressions of [[L01-06-gaussian-linear-regression]] §8 are a small honest instance: five specifications side by side, with persistence stable at 0.65–0.72 in all.

---

## 4 · C — a p-value below 0.05 that favours $H_0$ (part1 slides 7–9)

$X\sim N(\theta,1)$, $H_0:\theta=0$ vs $H_1:\theta=4$, observed $X=1.8$.

**The p-value (slide 7):**

$$p=P(X\ge1.8\mid\theta=0)=1-\Phi(1.8)=1-0.96407=0.0359<0.05.\tag{5}$$

"The result is 'statistically significant', so reject $H_0$. Surprisingly, nothing is said about $H_1$!" Swap the roles ($H_0:\theta=4$, $H_1:\theta=0$, reject for small $X$) and the p-value is

$$P(X\le1.8\mid\theta=4)=\Phi(1.8-4)=\Phi(-2.2)=0.0139:\tag{6}$$

**1.8 is "significant" against either hypothesis — it sits in the tail of both** ("an even more extreme tail of $H_1$", slide 8).

**The likelihood ratio (slide 8).** With $\phi(z)=e^{-z^2/2}/\sqrt{2\pi}$, the constants cancel:

$$BF_{01}=\frac{f(x\mid H_0)}{f(x\mid H_1)}=\frac{\phi(1.8-0)}{\phi(1.8-4)}=\frac{\exp(-1.8^2/2)}{\exp(-(-2.2)^2/2)}=\frac{\exp(-1.62)}{\exp(-2.42)}=\exp(0.80)=2.2255.\tag{7}$$

> **"The data are more than twice as likely under $H_0$ than under $H_1$. The observation $X=1.8$ is closer to the null than to the alternative"** — 1.8 from 0, 2.2 from 4.

**For every $x$.** Expanding the squares,

$$\log BF_{10}(x)=-\frac{(x-4)^2}{2}+\frac{x^2}{2}=\frac{x^2-(x^2-8x+16)}{2}=4x-8,\tag{8}$$

so $BF_{10}=1$ at $x=2$, the midpoint. **Any $x$ in $(1.645,\ 2)$ is significant at 5% one-sided (since $1-\Phi(1.645)=0.05$) and yet favours $H_0$.** At $x=1.8$, (8) gives $4(1.8)-8=-0.8$, i.e. $BF_{10}=e^{-0.8}=0.449$, the reciprocal of (7).

**The posterior (slide 9).** Bayes' theorem over the two hypotheses:

$$P(H_1\mid x)=\frac{f(x\mid H_1)P(H_1)}{f(x\mid H_1)P(H_1)+f(x\mid H_0)P(H_0)}.\tag{9}$$

With $P(H_0)=P(H_1)=0.5$ the priors cancel; divide through by $f(x\mid H_1)$ and substitute (7):

$$P(H_1\mid x)=\frac{1}{1+\frac{f(x\mid H_0)}{f(x\mid H_1)}}=\frac{1}{1+BF_{01}}=\frac{1}{1+2.2255}=\frac{1}{3.2255}=0.310.\tag{10}$$

> **"Despite a p-value of 0.036, the posterior probability of $H_1$ is only 31%."** The Bayes factor $BF_{10}\approx0.45$ "constitutes evidence in favour of $H_0$". A clean instance "of the Jeffreys–Lindley paradox in spirit": **a p-value measures distance from $H_0$ and is completely blind to where $H_1$ is.**

![Left: the N(0,1) and N(4,1) densities with X = 1.8 marked; the right tail of H0 beyond 1.8 has area 0.036, the left tail of H1 below 1.8 has area 0.014, and the density height under H0 is e^0.8 = 2.23 times that under H1. Right: as functions of the observation x from 0 to 4, the one-sided p-value falls while the posterior probability of H1 with equal priors rises, crossing 0.5 at x = 2; the band from 1.645 to 2 marks p below 0.05 with the Bayes factor favouring H0; at x = 1.8 the p-value is 0.036 and the posterior 0.31](figures/L01-p-vs-bayes-factor.png)
*Figure — left: the two sampling densities at $x=1.8$, tail areas (5)–(6) shaded; right: $p(x)=1-\Phi(x)$ and $P(H_1\mid x)=1/(1+e^{-(4x-8)})$ from (8) and (10). Source: part1-p-hacking.pdf slides 7–9.*

The left panel separates the two questions: the p-value is a *tail area* (shaded), the Bayes factor a *ratio of heights* at the observed point (the vertical line meets the blue curve higher than the orange one). On the right the two curves move in opposite directions, and the shaded band is where they disagree about which hypothesis the data support; $x=1.8$ sits inside it.

---

## 5 · C — the prior that would make $p=0.036$ convincing (part1 slides 10–13)

Keep (9) but leave the priors free. Dividing numerator and denominator by $f(x\mid H_1)P(H_1)$:

$$P(H_1\mid X)=\frac{1}{1+BF_{01}\cdot\frac{P(H_0)}{P(H_1)}}.\tag{11}$$

Set (11) equal to 0.9 (slide 10):

$$1+BF_{01}\frac{P(H_0)}{P(H_1)}=\frac1{0.9}\iff BF_{01}\frac{P(H_0)}{P(H_1)}=\frac1{0.9}-1=\frac19.\tag{12}$$

Substitute $BF_{01}=2.2255$ from (7) and solve (slide 11):

$$\frac{P(H_0)}{P(H_1)}=\frac{1}{9\times2.2255}=\frac{1}{20.03},\qquad\boxed{\;\frac{P(H_1)}{P(H_0)}=20.03\approx20\;}\tag{13}$$

(The deck, rounding $BF_{01}$ to 2.23, prints $1/20.07$.) Odds of 20:1 mean

$$P(H_1)=\frac{20}{21}=0.952,\qquad P(H_0)=\frac1{21}=0.048.$$

Equivalently, in odds form — posterior odds = Bayes factor × prior odds — $9=0.449\times20.03$.

| Scenario (slide 13) | p-value | $P(H_1\mid X)$ |
|---|---|---|
| Equal priors, $X=1.8$, $H_1:\theta=4$ | 0.036 | 0.31 |
| Prior odds 20:1 in favour of $H_1$ | 0.036 | 0.90 |

> **"To obtain $P(H_1\mid X)=0.9$ from data that actually favour $H_0$ by a factor of 2.23, one must enter the analysis believing $H_1$ is 20 times more probable than $H_0$ a priori."** That is the implicit prior behind treating $p<0.05$ as strong evidence here — "Making the prior explicit is not a weakness of Bayesian analysis, it is in fact its central virtue." (slide 12)

**The three lessons (slide 13):** p-hacking inflates false positives multiplicatively across specifications (§3); a significant p-value can coexist with a Bayes factor favouring $H_0$ (§4); a high posterior for $H_1$ despite unfavourable data needs a heavily loaded prior (§5).

---

## 6 · U — the replication crisis and economics (economics deck)

All figures and studies below are the deck's, cited as the deck cites them.

**Replication (slide 5).** Open Science Collaboration (2015): only 36% of 100 psychology studies replicated. Camerer et al. (2016, 2018): 61% in experimental economics, 62% for social-science papers in *Nature*/*Science*. Effect sizes in successful replications are typically about 50% of the originals. Drivers: p-hacking, publication bias, low power, weak pre-registration.

**Why it compounds (slide 6).** Journals reward significant findings → incentives to reach $p<0.05$ → forking paths push the real Type I error far above 5% → published effects biased upward, standard errors downward → meta-analyses and policy inherit the bias.

**Evidence in economics (slide 7).** Brodeur, Lé, Sangnier & Zylberberg (2016, *AEJ: Applied*; "Star Wars: The Empirics Strike Back") examined 50,000+ test statistics from top journals: a two-humped distribution of $z$ around 1.96, with roughly 10–20% of marginally significant results attributable to p-hacking and selective reporting. Brodeur, Cook & Heyes (2020, *AER*): **IV and difference-in-differences show the most inflation near $p=0.05$; RCTs and RDD less.** *(The deck's text lists the 2016 authors as "Brodeur, Lé, Sánchez, & Cook"; its reference list repeats that.)*

**Why economics is vulnerable (slide 8)** — observational data with many defensible specifications, a weak replication culture, significance stars as gatekeepers, long lags weakening pre-specification, and policy stakes. **Examples (slide 9):** minimum-wage employment effects (Neumark & Wascher vs Card & Krueger); Sala-i-Martin's (1997) two million growth regressions; Reinhart & Rogoff's 90% debt threshold reversed after coding errors (Herndon et al., 2014); behavioural headline effects weakened by Many Labs.

**Responses (slide 10):** pre-registration and pre-analysis plans (AEA RCT Registry, since 2013); mandatory data and code archives; replication journals; multiple-testing corrections (Bonferroni — (4) — Romano–Wolf, sharpened FDR by Anderson, 2008); specification curves and multiverse analyses; and Benjamin et al. (2018): redefine "significant" as $p<0.005$.

> **"The fundamental fix is cultural: rewarding credible research, not just significant research."** (slide 11)

---

## 7 · G — where this goes

Bayes factors for composite hypotheses (priors over $\theta$ under $H_1$, marginal likelihoods), posterior model probabilities and Bayesian model averaging are Classes 3+4 (G §3.2.4; [[../../rules/07_bayes|rules/07]]). There the Jeffreys–Lindley paradox appears in full: with a diffuse prior under $H_1$, a fixed $p=0.05$ supports $H_0$ ever more strongly as $n$ grows.

---

## Links

- Neighbours: [[L01-07-ar-var-review]] · [[L01-09-formulas]].
- Unit: [[L01-00-map]] · [[L01-10-pitfalls]] · [[L01-11-python]] · [[L01-01-likelihood-sampling-rules]] (same likelihood, different p-values; the likelihood principle) · [[L01-06-gaussian-linear-regression]] (§6 model selection, §8 reporting several specifications) · [[L01-04-first-bayesian-poisson]] (the first prior-to-posterior update).
- Class 2: [[../L02/L02-03-cross-validation-motorcycle|L02 §3]] (choosing among many models without fooling yourself).
- Rules: [[../../rules/07_bayes|rules/07]] (Bayes factors, model probabilities).
- **Practice (forward, Classes 3+4; number and printed page only):** G 3.7 and G 3.8 (p. 40), Bayes factors.
