---
tags: [notes, lecture-03, normal-normal, predictive, posterior, precision, student-t-prior, robustness, physicists]
date: 2026-10-27
status: taught
source: "aprendizagembayesiana-bayesianingredients.pdf slides 26–52 (Example 2: Gaussian measurement error; physicists A, B, C); fisicos-ABCD.html (priors A–D, SIR summary table); Greenberg 1e §3.1.1 (pp. 20–21), §3.2.3 (pp. 32–33), §4.2 (pp. 43–44), §4.3 (pp. 44–47, (4.2)–(4.7)), §4.8 (p. 54); Bolfarine & Sandoval (2010) Ex. 4.4.3 (pp. 68–69), Ex. 5.5.1 (p. 86); Tsay AFTS 3e Result 12.1 (pp. 618–619)"
---

# Ingredients deck slides 26–52, fisicos-ABCD · The normal measurement model: predictive, posterior, and what a heavy-tailed prior changes

> **Claim.** With $x\mid\theta\sim N(\theta,\sigma^2)$ and a normal prior $N(\mu_0,\tau_0^2)$, the
> predictive is $N(\mu_0,\sigma^2+\tau_0^2)$ and the posterior is normal with mean
> $w\mu_0+(1-w)x$ and variance $w\tau_0^2$, where $w=\sigma^2/(\sigma^2+\tau_0^2)$: **precisions add, and
> the mean is the precision-weighted average.** For $x=850$, $\sigma=40$, physicist A (prior
> $N(900,20^2)$) ends at **$N(890,\,17.9^2)$** and physicist B ($N(800,80^2)$) at **$N(840,\,35.8^2)$**.
> Physicist C holds a Student-$t_5$ prior with A's mean and variance; there is no closed form, and
> quadrature gives a posterior mean of **891.1**. At $x=850$ A and C barely differ, but the normal
> prior pulls by the fixed share $w$ however far $x$ lands, while the $t$ prior's pull **dies away**
> when data and prior conflict: at $x=1100$ the posterior means are 940 (normal) and 1022 ($t$).
> Prev: [[L03-02-conjugate-sequential-updating]] · Next: [[L03-04-bayes-estimators-loss]] · Map: [[L03-00-map]]

**Notation.**

| Symbol | Meaning | Range / value |
|---|---|---|
| $\theta$ | the physical quantity | $\mathbb R$ |
| $x$ | one measurement | 850 (slide 39) |
| $\sigma$ | measurement sd | 40 (slide 28) |
| $\mu_0,\tau_0$ | prior mean and sd (normal prior) | A: 900, 20; B: 800, 80 |
| $w$ | weight on the prior mean, $\sigma^2/(\sigma^2+\tau_0^2)$ | $(0,1)$ |
| $\mu_1,\tau_1^2$ | posterior mean and variance | — |
| $h,h_0$ | precisions $1/\sigma^2$, $1/\tau_0^2$ | $>0$ |
| $t_\nu(\mu,s^2)$ | Student-$t$ with $\nu$ df, location $\mu$, scale $s$; variance $\nu s^2/(\nu-2)$ | C: $t_5(900,240)$ |

---

## 1 · U — two physicists, one instrument (slides 26–33)

The deck's second example learns a physical constant from one noisy reading. The instrument's error
is known: $x\mid\theta\sim N(\theta,40^2)$ (slide 28). Two physicists bring different experience:

- **A (large experience):** $\theta\sim N(900,20^2)$;
- **B (not so experienced):** $\theta\sim N(800,80^2)$.

Slide 33 draws each physicist's **joint** density $p(x,\theta)=p(x\mid\theta)p(\theta)$: a tilted ellipse
for A, a broad one for B. Everything below is a slice or a projection of that joint density: the
predictive is its projection on the $x$ axis; the posterior is its slice at the observed $x$.

> **Erratum.** Slide 40 prints B's prior as $N(800,(40)^2)$ and slide 44 as $N(800,1600)$. The
> posterior on slide 40, $N(840,35.7^2)$, and `fisicos-ABCD.html` (`sig.B = 80`) both require
> $\tau_0=80$, which is the value used here.

---

## 2 · C — the predictive distribution (slides 34–36; G Ex. 3.3 setting)

Write the measurement as the quantity plus an independent error:

$$x=\theta+e,\qquad\theta\sim N(\mu_0,\tau_0^2),\quad e\sim N(0,\sigma^2),\quad\theta\perp e.\tag{1}$$

A sum of independent normals is normal, with means and variances added:

$$x\sim N(\mu_0+0,\ \tau_0^2+\sigma^2).\tag{2}$$

This is slide 35's result $x\sim N(\theta_0,\sigma^2+\tau_0^2)$, obtained there by computing
$p(x)=\int p(x\mid\theta)p(\theta)\,d\theta$ and completing the square in $\theta$. Numbers:

| | Predictive | Predictive sd |
|---|---|---|
| A | $N(900,\ 1600+400)=N(900,2000)$ | $\sqrt{2000}=44.72$ |
| B | $N(800,\ 1600+6400)=N(800,8000)$ | $\sqrt{8000}=89.44$ |

> **The predictive is wider than the instrument.** Before measuring, a physicist is uncertain both
> about $\theta$ and about the error; (2) adds the two. The observed $x=850$ is
> $(850-900)/44.72=-1.12$ predictive sd from A's centre and $(850-800)/89.44=0.56$ from B's: neither
> physicist is surprised.

---

## 3 · C — the posterior (slides 37–38; B Ex. 4.4.3; T Result 12.1)

Keep only the factors of $p(x\mid\theta)p(\theta)$ that involve $\theta$:

$$p(\theta\mid x)\propto\exp\Big\{-\frac{(x-\theta)^2}{2\sigma^2}\Big\}\exp\Big\{-\frac{(\theta-\mu_0)^2}{2\tau_0^2}\Big\}=\exp\Big\{-\frac12\Big[\frac{\theta^2-2\theta x}{\sigma^2}+\frac{\theta^2-2\theta\mu_0}{\tau_0^2}\Big]+c\Big\},\tag{3}$$

where $c$ collects $x^2/\sigma^2$ and $\mu_0^2/\tau_0^2$. Collect $\theta^2$ and $\theta$:

$$p(\theta\mid x)\propto\exp\Big\{-\frac12\Big[\theta^2\Big(\frac1{\sigma^2}+\frac1{\tau_0^2}\Big)-2\theta\Big(\frac{x}{\sigma^2}+\frac{\mu_0}{\tau_0^2}\Big)\Big]\Big\}.\tag{4}$$

Define the posterior precision and mean

$$\frac1{\tau_1^2}=\frac1{\sigma^2}+\frac1{\tau_0^2},\qquad\mu_1=\tau_1^2\Big(\frac{x}{\sigma^2}+\frac{\mu_0}{\tau_0^2}\Big).\tag{5}$$

Substitute (5) into (4) and complete the square: the bracket is
$(\theta^2-2\theta\mu_1)/\tau_1^2=(\theta-\mu_1)^2/\tau_1^2-\mu_1^2/\tau_1^2$, and the last term is a constant, so

$$\theta\mid x\sim N(\mu_1,\tau_1^2).\tag{6}$$

**Slide 37's form.** From (5), $\tau_1^2=\sigma^2\tau_0^2/(\sigma^2+\tau_0^2)$. Then

$$\mu_1=\frac{\sigma^2\tau_0^2}{\sigma^2+\tau_0^2}\Big(\frac{x}{\sigma^2}+\frac{\mu_0}{\tau_0^2}\Big)=\frac{\sigma^2}{\sigma^2+\tau_0^2}\mu_0+\frac{\tau_0^2}{\sigma^2+\tau_0^2}x.\tag{7}$$

With $w=\sigma^2/(\sigma^2+\tau_0^2)\in(0,1)$ (slide 38):

$$E(\theta\mid x)=w\,E(\theta)+(1-w)\,x,\qquad V(\theta\mid x)=w\,V(\theta).\tag{8}$$

> **Precisions add; means are precision-weighted (Tsay, p. 619).** (5) says the posterior precision is
> the prior precision plus the data precision, and (7) weights each source by its share of the total
> precision. The weight on the prior, $w$, is large when the instrument is noisy relative to the
> prior ($\sigma^2\gg\tau_0^2$).

**Limits (slide 38).** As $\tau_0^2\to\infty$ (a vague prior), $w\to0$ and $\theta\mid x\to N(x,\sigma^2)$: "the
posterior collapses at the observed value $x$". As $\tau_0^2\to0$, $w\to1$: the data are ignored.

**$n$ observations (B Ex. 4.4.3; T Result 12.1).** With $x_1,\dots,x_n$ iid $N(\theta,\sigma^2)$, the sample
mean $\bar x\sim N(\theta,\sigma^2/n)$ is sufficient, so (5)–(8) hold with $\sigma^2/n$ in place of $\sigma^2$:
$w_n=\sigma^2/(\sigma^2+n\tau_0^2)\to0$ like $1/n$.

---

## 4 · Worked — physicists A and B at $x=850$ (slides 39–41)

**A:** $w=1600/(1600+400)=0.8$. Substitute into (8):

$$E(\theta\mid x)=0.8\times900+0.2\times850=720+170=\mathbf{890},\qquad V(\theta\mid x)=0.8\times400=320,\quad\text{sd}=\sqrt{320}=\mathbf{17.89}.$$

**B:** $w=1600/(1600+6400)=0.2$:

$$E(\theta\mid x)=0.2\times800+0.8\times850=160+680=\mathbf{840},\qquad V(\theta\mid x)=0.2\times6400=1280,\quad\text{sd}=\sqrt{1280}=\mathbf{35.78}.$$

Slide 40 prints $N(890,(17.9)^2)$ and $N(840,(35.7)^2)$; 35.78 rounds to 35.8.

> **The experienced physicist barely moves; the inexperienced one mostly follows the data.** A moves
> 10 units toward $x$ (20% of the 50-unit gap), B moves 40 units (80% of the gap). Both posteriors are
> narrower than both their prior and the instrument: $17.9<\min(20,40)$, $35.8<\min(80,40)$.

---

## 5 · C — physicist C: a Student-$t$ prior (slides 44–52)

**Prior C (slide 45).** $\theta\sim t_5(900,240)$, whose variance is

$$V(\theta)=\frac{\nu}{\nu-2}s^2=\frac53\times240=400=V(\text{prior A}).\tag{9}$$

Same centre, same variance as A, but heavier tails: slide 47's log densities show C's log prior
falling like $-(\nu+1)\log|\theta-900|=-6\log|\theta-900|$ instead of $-(\theta-900)^2/800$.

**No closed form (slide 48).** The predictive and the posterior are

$$p(x)=\int\frac{e^{-(x-\theta)^2/2\sigma^2}}{\sqrt{2\pi\sigma^2}}\,\frac{\Gamma(3)}{\Gamma(5/2)\sqrt{5\pi\,240}}\Big[1+\frac{(\theta-900)^2}{5\times240}\Big]^{-3}d\theta,\qquad p(\theta\mid x)\propto e^{-(x-\theta)^2/2\sigma^2}\Big[1+\frac{(\theta-900)^2}{1200}\Big]^{-3},\tag{10}$$

neither of which is a standard form. The deck postpones them to Monte Carlo (footnotes "yet to be
learned!", slides 49 and 51); `fisicos-ABCD.html` uses sampling importance resampling
([[L03-06-monte-carlo-simulation]] §7). A one-dimensional posterior can also be computed **exactly**
by quadrature: evaluate the kernel (10) on a fine grid and normalise.

**Prior D (`fisicos-ABCD.html`).** The equal mixture $\frac13N(900,20^2)+\frac13N(800,80^2)+\frac13t_5(900,240)$
of the three physicists. (The page's text writes $N(\mu_A,\sigma_A^2)$ twice; its code uses A, B and C.)

**The page's table against quadrature.** The SIR draws come from $U(600,1000)$ proposals, so the
targets are the posteriors restricted to $[600,1000]$ (the restriction changes nothing at two decimals).

| Posterior | $E(\theta\mid x)$ SIR / exact | Median SIR / exact | $P(\theta<x\mid x)$ SIR / exact | 5% quantile SIR / exact |
|---|---|---|---|---|
| A | 890.06 / 890.00 | 890.10 / 890.00 | 0.01 / 0.013 | 860.52 / 860.58 |
| B | 840.02 / 840.00 | 840.09 / 840.00 | 0.61 / 0.610 | 781.18 / 781.15 |
| C | 891.16 / 891.12 | 892.45 / 892.41 | 0.02 / 0.022 | 860.30 / 860.31 |
| D | 876.15 / 876.08 | 884.35 / 884.30 | 0.19 / 0.187 | 806.53 / 806.40 |

The SIR column agrees with quadrature to Monte Carlo error (a million draws). C's posterior is
slightly right of A's and slightly **narrower** (sd 17.70 vs 17.89): near the centre a $t$ prior with
A's variance is more peaked than A. D is bimodal-looking with a long left shoulder: B's component keeps
values near 800 alive, so its median (884.3) exceeds its mean (876.1).

![Three panels. Left: priors A (normal at 900, sd 20), B (normal at 800, sd 80), C (Student-t, peaked at 900), D (mixture), and the dashed likelihood centred at 850. Middle: the four posteriors on 680 to 960 with means 890.0, 840.0, 891.1 and 876.1. Right: posterior mean against the observed x from 700 to 1150; the normal-prior line has slope 0.2 and passes through 900 at x = 900; the Student-t curve follows it near 900 but bends back toward the 45-degree line for x far from 900 on either side.](figures/L03-normal-four-priors.png)
*Left and middle: (6) for A and B, quadrature of (10) for C and D, at $x=850$, $\sigma=40$ (slides 39–52; `fisicos-ABCD.html`). Right: $E(\theta\mid x)$ against $x$ for prior A, by (7), and prior C, by quadrature.*

The right panel is the comparative static that matters. Under the normal prior the posterior mean is
the straight line $0.8\times900+0.2x$: the pull toward 900 is $0.8(x-900)$, proportional to the
conflict, without limit. Under the $t$ prior the curve hugs the normal line for $|x-900|\lesssim100$
and then turns back toward the 45° line: the prior gives way when the data contradict it strongly.

---

## 6 · C — why the $t$ prior gives way: bounded influence

Take logs of the posterior kernel and differentiate. The posterior mode $\tilde\theta$ solves

$$\frac{x-\tilde\theta}{\sigma^2}=\psi(\tilde\theta),\qquad\psi(\theta)=-\frac{d}{d\theta}\log p(\theta).\tag{11}$$

The left side is the data's pull toward $x$; $\psi$ is the prior's pull back toward $\mu_0$.

- **Normal prior:** $\log p(\theta)=-(\theta-\mu_0)^2/2\tau_0^2+c$, so $\psi(\theta)=(\theta-\mu_0)/\tau_0^2$. It grows
  linearly without bound. Substituting into (11) gives $\tilde\theta=\mu_1$ of (5) for every $x$.
- **Student-$t$ prior:** $\log p(\theta)=-\frac{\nu+1}2\log\big(1+\frac{(\theta-\mu_0)^2}{\nu s^2}\big)+c$, so

$$\psi(\theta)=\frac{(\nu+1)(\theta-\mu_0)}{\nu s^2+(\theta-\mu_0)^2}.\tag{12}$$

(12) rises to a maximum at $|\theta-\mu_0|=s\sqrt\nu$ and then falls to 0. The prior's pull is
**bounded** and vanishes in the tails. For C: $s\sqrt\nu=\sqrt{240\times5}=34.6$, and the largest pull is
$\psi=6/(2\times34.6)=0.087$, against a data pull of $(x-\theta)/1600$. When $x$ is far from 900, the data
pull wins and $\tilde\theta\to x$.

**Numbers (quadrature).** At $x=1100$, $4.47$ predictive sd from A's centre: normal posterior mean
$0.8\times900+0.2\times1100=940.0$; $t$ posterior mean **1022.0**, posterior sd 53.6 (against 17.9): the
$t$ posterior is wide because it is torn between the prior and the data.

> **A normal prior is never contradicted; it is averaged in.** A heavy-tailed prior encodes "I am
> fairly sure, unless the data say otherwise". Greenberg makes the same point about likelihoods in
> §3.1.1 (pp. 20–21): a Student-$t$ puts more probability in the tails than a normal with the same
> variance, and the choice can be compared by posterior odds. The Petrobras page applies it to returns
> ([[L03-08-metropolis-hastings-hmc]] §7).

> **Interactive companion.** [The Prior-Conflict Dial](companions/companion-normal-prior-conflict.html) —
> move the observation $x$, the instrument's $\sigma$, the prior mean and sd, and the $t$ degrees of
> freedom; watch both posteriors and the posterior-mean-vs-$x$ curve, with the normal pull $w$ and the
> $t$ pull side by side. Defaults reproduce 890.0 / 17.9 and 891.1; "Set x = μ₀" shows the no-conflict
> case.

---

## 7 · G — improper priors and the regression version (G §4.2–4.3)

- **Flat prior.** $p(\theta)\propto c$ on $\mathbb R$ is improper (§4.2, pp. 43–44); with the normal
  likelihood it still gives the proper posterior $N(x,\sigma^2)$, the $\tau_0\to\infty$ limit of §3. It is
  unusable for Bayes factors ([[L03-05-model-comparison-bayes-factors]] §6).
- **Normal linear regression (G (4.2)–(4.7), pp. 45–46).** With
  $\beta\mid\sigma^2\sim N_K(\beta_0,\sigma^2B_0)$ and $\sigma^2\sim IG(\alpha_0/2,\delta_0/2)$, the posterior is
  $\beta\mid\sigma^2,y\sim N_K(\bar\beta,\sigma^2B_1)$ with $B_1=(X'X+B_0^{-1})^{-1}$,
  $\bar\beta=B_1(X'y+B_0^{-1}\beta_0)$, and $\sigma^2\mid y\sim IG(\alpha_1/2,\delta_1/2)$, $\alpha_1=\alpha_0+n$; marginally
  $\beta\mid y$ is multivariate $t$ (4.7). $\bar\beta$ is the matrix version of (7): a precision-weighted
  average of $\beta_0$ and the OLS estimate. Dropping the proportionality to $\sigma^2$ (§4.9) loses the
  closed form and leads to the Gibbs sampler of [[L03-07-markov-chains-gibbs]].

---

## Links

- Prev: [[L03-02-conjugate-sequential-updating]]; next: which summary of this posterior to report,
  [[L03-04-bayes-estimators-loss]]. Monte Carlo for physicist C: [[L03-06-monte-carlo-simulation]] §7.
  Formulas: [[L03-11-formulas]]; pitfalls: [[L03-12-pitfalls]]; code: [[L03-13-python]] §3.
- Earlier: OLS as a projection and the Gaussian likelihood, [[../L01/L01-06-gaussian-linear-regression|L01 §6]].
  Later: shrinkage estimators built on (7), [[L03-09-hierarchical-models-shrinkage]], [[L03-10-sparsity-priors]].
- Rules: [[../../rules/07_bayes|rules/07]] (normal–normal conjugacy, predictive).
- Practice (statements in the books): **G 3.3** (p. 39, normal predictive), **G 4.5** (p. 58, marginal
  likelihood of the normal–inverse-gamma model), **T 12.1** (p. 670, normal–normal posterior).
