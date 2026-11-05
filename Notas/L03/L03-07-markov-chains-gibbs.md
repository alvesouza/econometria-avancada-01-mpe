---
tags: [notes, lecture-03, markov-chain, invariant-distribution, gibbs-sampler, data-augmentation, switch-point, coal-mining, mixing, numerical-standard-error]
date: 2026-10-29
status: taught
source: "Greenberg 1e Ch. 6 (pp. 76–87: (6.1)–(6.9), Theorems 6.1–6.7), §7.1 (pp. 91–95: Algorithms 7.1–7.3, (7.1)–(7.4), bivariate-normal example), §7.3 (pp. 102–103, batch means, r.n.e.); Tsay AFTS 3e §12.1–12.3 (pp. 614–621, (12.1)–(12.3), Results 12.1–12.8); Morettin & Singer (2021) §C.5 (pp. 487–488, (C.16)–(C.17)); coal data .agent/notes/coal-mining-data.md (Jarrett 1979); hierarchical-gaussian-linear-model.html (Gibbs code, used in L03-09)"
---

# G Ch. 6, §7.1, §7.3, T §12.1–12.3 · Gibbs sampling: a Markov chain whose invariant distribution is the posterior

> **Claim.** When a posterior cannot be sampled directly but each **full conditional** can, draw the
> blocks one at a time, each from its conditional given the latest values of the others. The draws
> form a Markov chain whose **invariant distribution is the joint posterior**; after a burn-in, their
> histograms are the marginals. On the coal-mining series with the L01-04 prior on both rates, a
> three-block Gibbs sampler puts the switch at **1891** (posterior probability 0.240, against the exact
> 0.240), with $E(\lambda_1\mid y)=3.106$ and $E(\lambda_2\mid y)=0.930$. The price is **dependence**: on a bivariate
> normal with correlation $\rho$, the chain's lag-$h$ autocorrelation is $\rho^{2h}$, so $\rho=0.999$ needs about
> 1000 draws for the information of one independent draw.
> Prev: [[L03-06-monte-carlo-simulation]] · Next: [[L03-08-metropolis-hastings-hmc]] · Map: [[L03-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $P=\{p_{ij}\}$ | transition matrix, $p_{ij}=P(X_{t+1}=j\mid X_t=i)$ | rows sum to 1 |
| $\pi$ | invariant distribution, $\pi P=\pi$ | probability vector / density |
| $p(x,y)$ | transition kernel (continuous state) | density in $y$ |
| $\theta=(\theta_1,\dots,\theta_d)$ | parameter blocks | — |
| $\theta_{-j}$ | all blocks except $\theta_j$ | — |
| $B$, $G$ | burn-in length, retained draws | integers |
| $k$ | switch point: last year of the first regime | $1,\dots,n$ |
| $\lambda_1,\lambda_2$ | Poisson rates before and after the switch | $>0$ |
| $S_k=\sum_{i\le k}y_i$ | cumulative count | — |
| $\rho_h$ | lag-$h$ autocorrelation of a chain | $[-1,1]$ |

---

## 1 · U — independent draws are a luxury

Chapter 5's methods ([[L03-06-monte-carlo-simulation]]) need a density we can sample whose shape is
close to the target: hard to find in many dimensions. MCMC reverses the question. Instead of a
distribution that is easy to sample, build a **process** that is easy to run and that settles into
the target. The draws are no longer independent, but averages still converge (Theorem 6.3), and the
recipe works for "a great variety of distributions without having to undertake an intensive analysis
of the special features of the distribution" (G p. 76).

---

## 2 · C — Markov chains on a finite state space (G §6.1)

A process $X_t$ on $S=\{1,\dots,s\}$ is a homogeneous **Markov chain** if

$$p_{ij}=P(X_{t+1}=j\mid X_t=i)\quad\text{does not depend on }t\text{ or on }X_{t-1},X_{t-2},\dots\tag{1}$$

The $n$-step transition probabilities are the entries of $P^n$ (G (6.3)). A distribution $\pi$ is
**invariant** if

$$\pi_j=\sum_i\pi_ip_{ij}\ \ \text{for all }j,\qquad\text{i.e. }\pi P=\pi.\tag{2}$$

**Worked (G (6.2), p. 79).** $P=\begin{pmatrix}0.750&0.250\\0.125&0.875\end{pmatrix}$. The first column of (2) gives
$\pi_1=0.750\pi_1+0.125\pi_2$. Substitute $\pi_2=1-\pi_1$:

$$\pi_1=0.750\pi_1+0.125(1-\pi_1)\ \Longrightarrow\ 0.375\pi_1=0.125\ \Longrightarrow\ \pi=(1/3,\ 2/3).\tag{3}$$

Powers of $P$ (G p. 80): $P^{10}=\begin{pmatrix}0.339&0.661\\0.330&0.670\end{pmatrix}$ and $P^{20}=\begin{pmatrix}0.333&0.667\\0.333&0.667\end{pmatrix}$:
every row converges to $\pi$, so after 20 steps the starting state is forgotten to three decimals.
The speed is set by the second eigenvalue of $P$, $1-0.250-0.125=0.625$ (G Ex. 6.5): the distance to
$\pi$ shrinks like $0.625^n$.

**When convergence fails (G pp. 78–81).** A **reducible** chain (block-diagonal $P$) never leaves the
block it starts in, and has many invariant distributions; a **periodic** chain alternates and $P^n$
does not converge. Theorem 6.2: if $P$ is irreducible and aperiodic on a finite space, there is a
unique invariant $\pi$ and $|p^{(n)}_{ij}-\pi_j|\le r^{n/\nu}$ with $r<1$.

---

## 3 · C — general state spaces and the ergodic average (G §6.2–6.3)

For continuous states the transition kernel $p(x,y)$ replaces $p_{ij}$, and a density $\pi$ is
invariant if (G (6.9))

$$\pi(y)=\int\pi(x)p(x,y)\,dx.\tag{4}$$

**Example (G pp. 85–86).** The AR(1) $y_t=\phi y_{t-1}+u_t$, $|\phi|<1$, $u_t\sim N(0,\sigma^2)$, has invariant density
$N(0,\sigma^2/(1-\phi^2))$, the equilibrium distribution of [[../L01/L01-07-ar-var-review|L01-07]]: if
$y_{t-1}\sim N(0,v)$ with $v=\sigma^2/(1-\phi^2)$, then $V(y_t)=\phi^2v+\sigma^2=v$.

**Theorem 6.3 (ergodic average).** For an irreducible chain whose states are positive recurrent, there
is a unique invariant $\pi$ and, for any starting distribution,

$$\frac1n\sum_{m=1}^nf(X_m)\ \longrightarrow\ E_\pi f(X)\quad\text{whenever }E_\pi|f(X)|<\infty.\tag{5}$$

(5) is the law of large numbers that MCMC needs: chain averages estimate posterior expectations.
**MCMC turns Markov-chain theory around** (G p. 84): instead of finding $\pi$ for a given $P$, it
starts from the target $\pi$ and constructs a kernel with that invariant distribution (Theorems 6.5–6.6
then give convergence for $\pi$-irreducible, aperiodic kernels).

---

## 4 · C — the Gibbs algorithm (G §7.1.1; T §12.2)

**Algorithm 7.1 (two blocks).** Choose $x_2^{(0)}$. At iteration $g$ draw

$$x_1^{(g)}\sim f(x_1\mid x_2^{(g-1)}),\qquad x_2^{(g)}\sim f(x_2\mid x_1^{(g)}).\tag{6}$$

Discard the first $B$ draws (burn-in); keep $G$ draws. With $d$ blocks (Algorithm 7.2; Tsay's three
parameters in (12.1)), each block is drawn from its full conditional given the most recent values of
all others.

**Why the target is invariant (G pp. 91–92).** The Gibbs kernel from $x=(x_1,x_2)$ to $y=(y_1,y_2)$ is
$p(x,y)=f(y_1\mid x_2)f(y_2\mid y_1)$. Check (4):

$$\int p(x,y)f(x)dx=\int\!\!\int f(y_1\mid x_2)f(y_2\mid y_1)f(x_1,x_2)\,dx_1dx_2=f(y_2\mid y_1)\int f(y_1\mid x_2)f(x_2)\,dx_2=f(y_2\mid y_1)f(y_1)=f(y).\tag{7}$$

The second equality integrates $x_1$ out of $f(x_1,x_2)$; the third is the law of total probability.

**How to find a full conditional (G p. 55).** Write the joint posterior (likelihood × prior), keep only
the factors that contain the block, and recognise the kernel. Everything else goes into the constant.
Conditionally conjugate priors (G §4.9) make every kernel standard.

**Using the output (T (12.3)).** Point estimates and variances are sample moments of the retained
draws; differences, ratios and other functions are computed draw by draw (T p. 616).


---

## 5 · Worked — normal mean and precision (G Algorithm 7.3, (7.1)–(7.2))

$y_i\sim N(\mu,h^{-1})$ iid, priors $\mu\sim N(\mu_0,h_0^{-1})$ and $h\sim G(\alpha_0/2,\delta_0/2)$, independent (G §4.9: not
conjugate jointly). The joint posterior is

$$\pi(\mu,h\mid y)\propto h^{n/2}\exp\Big[-\frac h2\sum_i(y_i-\mu)^2\Big]\exp\Big[-\frac{h_0}2(\mu-\mu_0)^2\Big]h^{\alpha_0/2-1}\exp\Big[-\frac{\delta_0h}{2}\Big].\tag{8}$$

**$h\mid\mu,y$.** Keep the factors of (8) with $h$:

$$\pi(h\mid\mu,y)\propto h^{(\alpha_0+n)/2-1}\exp\Big[-h\,\frac{\delta_0+\sum_i(y_i-\mu)^2}{2}\Big]\ \Rightarrow\ h\mid\mu,y\sim G\Big(\frac{\alpha_0+n}2,\ \frac{\delta_0+\sum_i(y_i-\mu)^2}{2}\Big).\tag{9}$$

**$\mu\mid h,y$.** Keep the factors with $\mu$; this is [[L03-03-normal-measurement-physicists]] (5) with
data precision $hn$ and prior precision $h_0$:

$$\mu\mid h,y\sim N\Big(\frac{h_0\mu_0+hn\bar y}{h_0+hn},\ (h_0+hn)^{-1}\Big).\tag{10}$$

Alternate (9) and (10). On a seeded data set with the design of the lecturer's Stan `exemplo1`
($n=100$, $y\sim N(1.6,0.2^2)$, prior $\mu\sim N(1.7,0.3^2)$): 5000 draws after 1000 burn-in give
$E(\mu\mid y)=1.6079$ against $\bar y=1.6077$, and $1/\sqrt{E(h\mid y)}=0.195$, the sample sd. The prior on $\mu$ is
worth $h_0/(hn)=(1/0.09)/(100/0.04)=0.4\%$ of the data.

---

## 6 · Worked — the coal-mining switch point (G (7.3)–(7.4), pp. 93–94)

**Model.** Counts $y_1,\dots,y_n$ ($n=112$ years, 1851–1962, $\sum y_i=191$) with

$$y_i\sim\text{Poisson}(\lambda_1)\ (i\le k),\qquad y_i\sim\text{Poisson}(\lambda_2)\ (i>k),\tag{11}$$

priors $\lambda_j\sim G(\alpha_0,\beta_0)$ and $k$ uniform on $\{1,\dots,n\}$ ($k=n$ means no change). Here both rates get
**the L01-04 prior** $G(1,\ 1/2)$, i.e. Exp(1/2), so the results connect to [[../L01/L01-04-first-bayesian-poisson|L01-04]].

**Joint posterior.** Likelihood × priors, dropping $\prod y_i!$ and constants:

$$\pi(\lambda_1,\lambda_2,k\mid y)\propto\lambda_1^{\alpha_0-1}e^{-\beta_0\lambda_1}\lambda_2^{\alpha_0-1}e^{-\beta_0\lambda_2}\cdot\lambda_1^{S_k}e^{-k\lambda_1}\cdot\lambda_2^{S_n-S_k}e^{-(n-k)\lambda_2}.\tag{12}$$

**Full conditionals.** Keep the factors of (12) with each block:

$$\lambda_1\mid k,y\sim G(\alpha_0+S_k,\ \beta_0+k),\qquad\lambda_2\mid k,y\sim G(\alpha_0+S_n-S_k,\ \beta_0+n-k),\tag{13}$$

$$P(k\mid\lambda_1,\lambda_2,y)=\frac{e^{k(\lambda_2-\lambda_1)}(\lambda_1/\lambda_2)^{S_k}}{\sum_{k'=1}^ne^{k'(\lambda_2-\lambda_1)}(\lambda_1/\lambda_2)^{S_{k'}}},\tag{14}$$

where (14) divides (12) by the factors free of $k$, $e^{-n\lambda_2}\lambda_2^{S_n}$. Each sweep: two gamma draws and one
draw from a discrete distribution on 112 points.

**An exact check.** The rates can be integrated out of (12) with the gamma integral
([[../L01/L01-04-first-bayesian-poisson|L01-04]] (2)), giving the marginal posterior of $k$ in closed form:

$$P(k\mid y)\propto\frac{\Gamma(\alpha_0+S_k)}{(\beta_0+k)^{\alpha_0+S_k}}\cdot\frac{\Gamma(\alpha_0+S_n-S_k)}{(\beta_0+n-k)^{\alpha_0+S_n-S_k}}.\tag{15}$$

This is the integrated likelihood of [[../L01/L01-03-coal-mining-change-point|L01-03]] §8, now with a prior.
It lets the Gibbs output be checked against the truth.

| Year | $k$ | $S_k$ | $P(k\mid y)$ exact | $E(\lambda_1\mid k,y)$ | $E(\lambda_2\mid k,y)$ |
|---|---|---|---|---|---|
| 1886 | 36 | 117 | 0.0854 | 3.233 | 0.980 |
| 1887 | 37 | 119 | 0.0995 | 3.200 | 0.967 |
| 1889 | 39 | 123 | 0.1463 | 3.139 | 0.939 |
| 1890 | 40 | 125 | 0.1849 | 3.111 | 0.924 |
| **1891** | **41** | **127** | **0.2402** | **3.084** | **0.909** |
| 1892 | 42 | 128 | 0.0945 | 3.035 | 0.908 |
| 1896 | 46 | 134 | 0.0328 | 2.903 | 0.872 |

The years 1886–1896 hold 98.1% of the posterior mass. At $k=41$, $E(\lambda_1\mid k,y)=128/41.5=3.084$: L01-04's
posterior mean for 1851–1891, the same computation. Averaging (13) over (15): $E(\lambda_1\mid y)=3.106$ (sd 0.289)
and $E(\lambda_2\mid y)=0.930$ (sd 0.117). A Gibbs run of 20,000 sweeps after 1000 burn-in gives 3.107 and 0.931,
and its histogram of $k$ is within total-variation distance 0.010 of (15).

![Left: bar chart of the exact posterior probability of the switch year for 1880 to 1902, peaking at 1891 (0.24) with secondary mass at 1886-1887 and 1889-1890, overlaid with Gibbs relative frequencies as dots that sit on the bars. Right: histograms of Gibbs draws of lambda1 (centred near 3.1) and lambda2 (centred near 0.93) with the exact marginal densities, mixtures of gammas, drawn over them; legend means 3.106 and 0.930.](figures/L03-gibbs-switch-point.png)
*Left: (15) as bars, Gibbs frequencies from (13)–(14) as dots (10,000 seeded sweeps). Right: Gibbs histograms of the rates against the exact marginals $\sum_kP(k\mid y)\,G(\lambda\mid\cdot)$ from (13).*

The switch is located to within a few years but not to one year: the posterior is jagged because a
single year's count (a 4 in 1886, a 3 in 1896) can make a candidate split better or worse. The rates are
well determined: about 3.1 disasters a year before, 0.93 after, a ratio of about 3.3, as in L01-03's
profile likelihood (3.098 vs 0.901 at 1891).

> **Profiling vs integrating, once more.** L01-03 maximised over $\lambda_1,\lambda_2$ for each $\tau$; (15)
> integrates them out against a prior, and the Gibbs sampler does the integration by simulation. Here
> all three agree on 1891; with a vaguer prior or a shorter series they need not.

---

## 7 · C — data augmentation (T §12.1; MS §C.5)

A "parameter" can be anything unobserved: a missing value, a latent volatility, a latent utility, a
regime indicator (T p. 615). Adding such variables $z$ to the sampler (Tanner–Wong's **data
augmentation**) often turns an intractable posterior into easy conditionals. MS (C.16)–(C.17) write the
two identities the algorithm iterates:

$$p(\theta\mid y)=\int p(\theta\mid y,z)p(z\mid y)\,dz,\qquad p(z\mid y)=\int p(z\mid\theta,y)p(\theta\mid y)\,d\theta;\tag{16}$$

drawing $z\sim p(z\mid\theta,y)$ and then $\theta\sim p(\theta\mid y,z)$ is a two-block Gibbs sampler. The switch point $k$ is
such a variable; so are the Student-$t$ precisions $\lambda_i$ of [[L03-06-monte-carlo-simulation]] §4 (G §8.1.2),
the latent utilities of the probit (G Algorithm 8.3) and the log-volatilities of the SV model
([[L03-08-metropolis-hastings-hmc]] §7).

---

## 8 · C — mixing, burn-in and the numerical standard error (G p. 94, §7.3)

**When Gibbs mixes badly (G p. 94).** Sample $(X_1,X_2)\sim N_2\big(0,\begin{pmatrix}1&\rho\\\rho&1\end{pmatrix}\big)$ by Gibbs with
$X_1\mid x_2\sim N(\rho x_2,1-\rho^2)$ and $X_2\mid x_1\sim N(\rho x_1,1-\rho^2)$. Substitute one conditional into the other:

$$x_1^{(g)}=\rho x_2^{(g-1)}+e_1=\rho\big(\rho x_1^{(g-1)}+e_2\big)+e_1=\rho^2x_1^{(g-1)}+(\rho e_2+e_1),\tag{17}$$

so the $x_1$ chain is an AR(1) with coefficient $\rho^2$, and its lag-$h$ autocorrelation is

$$\rho_h=\rho^{2h}.\tag{18}$$

For $\rho=0.5$: $\rho_1=0.25$, and $|\rho_h|<0.05$ from lag 3 ($0.5^6=0.016$), Greenberg's report. For $\rho=0.999$:
$\rho_{20}=0.998^{20}=0.961$, "over 0.900 even at lag 20"; with $G=5000$ the sample mean of $x_1$ was 1.084 or
$-0.623$ depending on the start (G p. 94), against the true 0.

**The cost of dependence.** The variance of a chain average is $\frac{V(X)}{G}\big(1+2\sum_{h\ge1}\rho_h\big)$; the bracket
is the **inefficiency factor** (autocorrelation time; G p. 103, the reciprocal of the relative numerical
efficiency). For an AR(1) with coefficient $\phi$ it is $(1+\phi)/(1-\phi)$; with $\phi=\rho^2$:

$$\text{IF}=\frac{1+\rho^2}{1-\rho^2}:\quad\rho=0.5\Rightarrow1.67,\qquad\rho=0.9\Rightarrow9.5,\qquad\rho=0.999\Rightarrow999.5.\tag{19}$$

A chain of $G$ draws carries the information of $G/\text{IF}$ independent ones.

![Left: autocorrelation of the Gibbs chain for x1 against lag 0 to 30 for rho = 0.5 (falls to zero by lag 3), 0.9 (decays over about 15 lags) and 0.999 (stays above 0.94 at lag 30); exact curves rho to the power 2h with simulated dots on them. Right: acceptance rate of random-walk Metropolis on a standard normal target against the proposal standard deviation s on a log scale, the curve (2/pi) arctan(2/s) falling from near 1 to near 0, with simulated points on it and s = 2.38 marked at 0.445.](figures/L03-mcmc-mixing.png)
*Left: (18) for three correlations, with autocorrelations of seeded Gibbs chains (G p. 94, Fig. 7.2). Right: random-walk Metropolis acceptance, [[L03-08-metropolis-hastings-hmc]] (9).*

**Remedies.** Block the correlated parameters together (T p. 617: "when parameters are highly
correlated, it pays to draw them jointly"), reparameterise, run several chains from dispersed starts.

**Numerical standard error by batch means (G §7.3).** Find a lag $j_0$ with $|\hat\rho_{j_0}|<0.05$, cut the $G$
draws into $N=G/j_0$ batches, and use the variance of the batch means:

$$\text{n.s.e.}=\sqrt{\frac{1}{N}\cdot\frac{1}{N-1}\sum_{b=1}^N(\bar Z_b-\bar Z)^2}.\tag{20}$$

The naive $\sqrt{\widehat V/G}$ understates the error by the factor $\sqrt{\text{IF}}$.

**Burn-in and convergence.** There is no theorem giving $B$ (G p. 91); diagnostics are informal: trace
plots, autocorrelations that die quickly, and agreement across chains started far apart (T p. 617).
Stan reports $\hat R$ and $n_{eff}$ for this purpose (the heart-attack output in
[[L03-09-hierarchical-models-shrinkage]] shows $n_{eff}=766$ of 20,000 draws for $\eta$).

---

## 9 · G — beyond this note (named)

Rao–Blackwellisation (estimate a marginal density by averaging the known conditional over the draws,
G p. 105), Chib's marginal likelihood from Gibbs output (G §7.1.2), multiple switch points and hidden
Markov regimes (Carlin et al. 1992; G p. 104). Not examinable here.

---

## Links

- Prev: [[L03-06-monte-carlo-simulation]]; next: when a full conditional is not standard,
  [[L03-08-metropolis-hastings-hmc]]. Gibbs for hierarchical models: [[L03-09-hierarchical-models-shrinkage]] §5;
  for sparse regression: [[L03-10-sparsity-priors]] §6. Formulas: [[L03-11-formulas]]; code: [[L03-13-python]] §7.
- Earlier: the change point by profile likelihood, [[../L01/L01-03-coal-mining-change-point|L01 §3]]; the
  Exp(1/2) prior on the same data, [[../L01/L01-04-first-bayesian-poisson|L01 §4]]; AR(1) equilibrium,
  [[../L01/L01-07-ar-var-review|L01 §7]].
- Rules: [[../../rules/08_monte_carlo_mcmc|rules/08]] (Gibbs sampling, convergence diagnostics).
- Practice (statements in the books): **G 6.2** (p. 87, two-state chain), **G 7.1** (p. 105, verify (7.1)–(7.2)),
  **G 7.3** (p. 106, switch-point Gibbs on the coal data), **T 12.2** (p. 670, Gibbs for regression with
  AR errors), **T 12.3** (p. 670), **MS C.5** (p. 489, chained-data Gibbs).
