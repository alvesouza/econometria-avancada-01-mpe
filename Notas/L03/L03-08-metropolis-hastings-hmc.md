---
tags: [notes, lecture-03, metropolis-hastings, random-walk, independence-sampler, acceptance-rate, bayesian-logit, stochastic-volatility, hmc, stan]
date: 2026-10-29
status: taught
source: "Greenberg 1e §7.2 (pp. 96–101: (7.5)–(7.6), Algorithms 7.4–7.6, Theorem 7.2, Beta(3,4) example, Fig. 7.1), §8.2.3 (pp. 126–129, (8.10), Table 8.3); Tsay AFTS 3e §12.4 (pp. 622–624), §12.7 (pp. 636–638, (12.20)–(12.23)); Bayesian-logistic-regression.html; petrobras-gaussian-student-SV-models.html; exemplos-1-2-3-R-STAN.txt; Bayesian-beta-regression.html (named)"
---

# G §7.2, §8.2.3, T §12.4, §12.7 · Metropolis–Hastings: propose anywhere, accept with the right probability

> **Claim.** When a full conditional is not a standard distribution, propose a move from any density
> $q(x,y)$ and accept it with probability $\alpha(x,y)=\min\{1,\ f(y)q(y,x)/[f(x)q(x,y)]\}$; otherwise stay.
> This makes the chain **reversible** with respect to $f$, so $f$ is invariant, and the unknown
> normalising constant cancels in the ratio. Gibbs is the special case where the proposal is the
> full conditional and $\alpha=1$. The proposal's scale trades acceptance against step size: for a
> $N(0,1)$ target and random-walk steps $N(0,s^2)$ the acceptance rate is exactly
> $\frac2\pi\arctan(2/s)$, **0.445 at $s=2.38$**. The Bayesian logit is the standard use: a normal prior is not
> conjugate, a tailored random walk samples it, and the posterior means sit next to the MLE.
> Prev: [[L03-07-markov-chains-gibbs]] · Next: [[L03-09-hierarchical-models-shrinkage]] · Map: [[L03-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $f$ | target density (posterior), known up to a constant | — |
| $q(x,y)$ | proposal density of $y$ given the current $x$ | — |
| $\alpha(x,y)$ | acceptance probability | $[0,1]$ |
| $s$ | random-walk proposal sd | $>0$ |
| $\beta$ | logit coefficients | $\mathbb R^K$ |
| $P_i$ | $P(y_i=1)=e^{x_i'\beta}/(1+e^{x_i'\beta})$ | $(0,1)$ |
| $h_t$ | log-volatility (SV) | $\mathbb R$ |

---

## 1 · U — accept or stay

Gibbs needs every full conditional in a form we can sample. Many models break this at one block: the
logit coefficients, a GARCH parameter, a log-volatility. Metropolis–Hastings needs only the ability to
**evaluate** the target up to a constant. It proposes a candidate from a convenient density and then
corrects for the mismatch between proposal and target by accepting some moves and rejecting others.
Unlike accept–reject ([[L03-06-monte-carlo-simulation]] §5), a rejection does not mean "try again": the
chain **repeats its current value**, so values recur and draws are correlated (G p. 97).

---

## 2 · C — reversibility and the acceptance probability (G pp. 96–98)

A kernel $p(x,y)$ is **reversible** with respect to $f$ if

$$f(x)p(x,y)=f(y)p(y,x)\quad\text{for all }x,y.\tag{1}$$

Integrating (1) over $x$ gives $\int f(x)p(x,y)dx=f(y)\int p(y,x)dx=f(y)$: **reversibility implies that $f$ is
invariant** ([[L03-07-markov-chains-gibbs]] (4)).

A proposal $q$ is usually not reversible: for some pair, $f(x)q(x,y)>f(y)q(y,x)$, so moves $x\to y$ happen
too often. Multiply by a factor $\alpha$ to restore balance (G (7.5)):

$$f(x)\,\alpha(x,y)\,q(x,y)=f(y)\,\alpha(y,x)\,q(y,x).\tag{2}$$

Moves $y\to x$ are too rare, so make them as frequent as possible: $\alpha(y,x)=1$. Substitute into (2) and
solve for $\alpha(x,y)$:

$$\alpha(x,y)=\frac{f(y)q(y,x)}{f(x)q(x,y)}.\tag{3}$$

Combining both cases gives G (7.6):

$$\alpha(x,y)=\min\Big\{\frac{f(y)\,q(y,x)}{f(x)\,q(x,y)},\ 1\Big\}\quad\text{if }f(x)q(x,y)>0,\ \text{and 0 otherwise}.\tag{4}$$

> **The normalising constant cancels.** Only the ratio $f(y)/f(x)$ enters (4), so a posterior known as
> likelihood × prior is enough (G p. 98; T p. 622).

**Algorithm 7.4.** Given $x$: (1) draw $Y\sim q(x,\cdot)$; (2) draw $U\sim U(0,1)$; if $U\le\alpha(x,Y)$ return $Y$,
otherwise return $x$. Theorem 7.2 (Tierney): a $\pi$-irreducible Metropolis kernel is Harris
recurrent, so (5) of [[L03-07-markov-chains-gibbs]] applies.

---

## 3 · C — two standard kernels (G p. 99; T §12.4.1–12.4.2)

**Random walk.** $y=x+u$ with $u$ symmetric about 0, so $q(x,y)=q(y,x)$ and (4) becomes

$$\alpha(x,y)=\min\Big\{\frac{f(y)}{f(x)},1\Big\}.\tag{5}$$

This is the original **Metropolis** algorithm (T §12.4.1, symmetric "jumping distribution"): uphill moves
are always accepted, downhill moves with probability equal to the density ratio. Hastings's
generalisation (T §12.4.2) allows asymmetric $q$ through the correction in (4).

**Independence kernel.** $q(x,y)=q(y)$, so

$$\alpha(x,y)=\min\Big\{\frac{f(y)/q(y)}{f(x)/q(x)},1\Big\},\tag{6}$$

a random walk on the importance ratio $f/q$ (compare [[L03-06-monte-carlo-simulation]] (9)). Greenberg
recommends a **tailored** kernel: a fat-tailed density (a multivariate $t$ with small $\nu$) centred at the
posterior mode with scale equal to the negative inverse Hessian there (p. 99).

**Worked — Beta(3, 4) from $U(0,1)$ proposals (G Algorithm 7.5).** With $q=1$ on $(0,1)$ and
$f(x)\propto x^2(1-x)^3$, (6) gives

$$\alpha(x^{(g-1)},U_2)=\min\Big\{\frac{U_2^2(1-U_2)^3}{(x^{(g-1)})^2(1-x^{(g-1)})^3},\ 1\Big\}.\tag{7}$$

Greenberg: 5000 draws after 500 burn-in, acceptance 0.57, sample mean 0.4296 against $3/7=0.4286$.
The stationary acceptance rate of an independence sampler with $q=1$ is
$\int\!\!\int\min\{f(x),f(y)\}\,dx\,dy$ (average (6) over $x\sim f$, $y\sim U$), which for Beta(3, 4) is **0.5726**. A
seeded Python run: acceptance 0.581, mean 0.4224.

---

## 4 · C — the proposal scale: an exact acceptance curve

Take the target $N(0,1)$ and random-walk proposals $y=x+u$, $u\sim N(0,s^2)$. The stationary acceptance
rate is $E[\min\{1,r\}]$ with $r=f(y)/f(x)$, $x\sim f$. Split it:

$$E[\min\{1,r\}]=P(r\ge1)+E[r\,\mathbf 1\{r<1\}].\tag{8}$$

The second term is $\int\!\!\int f(y)q(y-x)\mathbf 1\{f(y)<f(x)\}dx\,dy$; relabelling $x\leftrightarrow y$ and using the symmetry
of $q$ turns it into $P(r>1)$. So the acceptance rate is $2P(f(y)>f(x))=2P(|x+u|<|x|)$. Write $u=sz$ with
$z\sim N(0,1)$ independent of $x$: $|x+sz|<|x|\iff z(2x+sz)<0$, the double wedge between the lines $z=0$ and
$z=-2x/s$. That wedge has angle $\arctan(2/s)$ on each side, and $(x,z)$ is rotation-invariant, so its
probability is $2\arctan(2/s)/(2\pi)$. Hence

$$\text{acceptance}(s)=\frac2\pi\arctan\frac2s.\tag{9}$$

| $s$ | 0.1 | 0.5 | 1 | 2.38 | 8 | 20 |
|---|---|---|---|---|---|---|
| acceptance (9) | 0.968 | 0.844 | 0.705 | **0.445** | 0.156 | 0.063 |

The right panel of the [[L03-07-markov-chains-gibbs]] mixing figure plots (9) with seeded runs on it.
Small $s$ accepts almost everything but crawls (high autocorrelation, as with $\rho\to1$ in Gibbs); large
$s$ proposes bold moves that are almost always rejected, and the chain sits still. Greenberg's
warning (p. 98) in numbers: neither a high nor a low acceptance rate is a goal in itself. The value
$s=2.38$ (for one dimension) is the scale that minimises the autocorrelation time of this chain
(Gelman, Roberts and Gilks; G-layer), and the tailored kernels in §6 use $2.38^2/K$ times the inverse
Hessian.

---

## 5 · C — Gibbs is MH with acceptance 1 (G pp. 100–101)

In a block update, propose $Y_1$ from the full conditional $f(x_1\mid x_2)$. Then (4) reads

$$\alpha(x_1,Y_1\mid x_2)=\frac{f(Y_1,x_2)\,f(x_1\mid x_2)}{f(x_1,x_2)\,f(Y_1\mid x_2)}=\frac{f(Y_1,x_2)\,f(x_1,x_2)/f(x_2)}{f(x_1,x_2)\,f(Y_1,x_2)/f(x_2)}=1.\tag{10}$$

Every proposal is accepted. This licenses **MH-within-Gibbs** (G Algorithm 7.6): Gibbs steps for the
blocks with standard conditionals, MH steps for the rest, in any order within a sweep. Tsay's
**Griddy Gibbs** (§12.4.3) is a third option for a univariate nonstandard conditional: evaluate it on
a grid, build an approximate inverse cdf, and draw by [[L03-06-monte-carlo-simulation]] (4).

---

## 6 · Worked — the Bayesian logit (G §8.2.3; Bayesian-logistic-regression.html)

**Model.** $P(y_i=1)=P_i=e^{x_i'\beta}/(1+e^{x_i'\beta})$, so $\log\frac{P_i}{1-P_i}=x_i'\beta$: the log-odds are linear in the
covariates (G p. 127). Likelihood and normal prior $\beta\sim N(\beta_0,B_0)$:

$$\pi(\beta\mid y)\propto\prod_{i=1}^nP_i^{y_i}(1-P_i)^{1-y_i}\cdot\exp\Big[-\frac12(\beta-\beta_0)'B_0^{-1}(\beta-\beta_0)\Big],\qquad\log\pi(\beta\mid y)=\sum_i\big[y_ix_i'\beta-\log(1+e^{x_i'\beta})\big]-\frac12(\beta-\beta_0)'B_0^{-1}(\beta-\beta_0)+c.\tag{11}$$

(11) is not a standard form, and latent logistic data do not make it conditionally conjugate (G
Ex. 8.8), so Greenberg uses MH with a random walk or a tailored independence kernel (p. 128).

**Reading coefficients for a prior (G pp. 127–128).** $\partial P_i/\partial x_{ik}=\beta_kP_i(1-P_i)$, largest at $P_i=\frac12$, so the
largest effect of covariate $k$ on the probability is $\beta_k/4$. The probit's is $0.4\beta_k$ (from $\phi(0)=0.3989$),
so logit coefficients are about **1.6 times** probit ones. Greenberg elicits $\beta_{01}=\log(1/9)=-2.1972$ from
"a 10% chance of owning a computer" for the baseline household, and reports
$P(\beta_2>0\mid y)=0.98$, $P(\beta_3>0\mid y)=0.88$ (Table 8.3).

**Seeded check (L03-13 §8).** $n=2000$ simulated observations with $\beta=(-1,0.8,0.5)$; prior $N(0,100I)$;
random walk with covariance $2.38^2/3$ times the MLE covariance, 10,000 draws after 1000 burn-in. MLE
$(-1.072,\ 0.845,\ 0.602)$; posterior means $(-1.074,\ 0.850,\ 0.605)$; acceptance 0.32.

**The site page (5000 bank clients; loan on income and education).** The GLM fit gives intercept
$-11.304$ (s.e. 0.419), income 0.0596 (0.0024), education (2 or 3 vs 1) 4.055 (0.221). The Bayesian fit
(package `UPG`, a Gibbs sampler based on Pólya–Gamma data augmentation, G-layer) gives posterior means
$-10.82$ (0.39), 0.06 (0.00) and 3.82 (0.21), with every 95% interval excluding 0. The posterior means are
4–6% smaller in absolute value than the MLE ($-10.82/-11.30=0.957$, $3.82/4.06=0.942$): the package's
default prior shrinks toward 0. The page's payoff is the **posterior of a probability**: draw by draw,
$P(\text{loan}\mid\text{income},\text{education})=1/(1+e^{-x'\beta^{(g)}})$, plotted at incomes 145, 170 and 193 (the 90%, 95% and
99% income quantiles) for both education groups ([[L03-06-monte-carlo-simulation]] §8).

---

## 7 · C — stochastic volatility by MCMC (T §12.7; petrobras page)

Tsay's univariate SV model (12.20)–(12.21):

$$r_t=x_t'\beta+a_t,\quad a_t=\sqrt{h_t}\,\epsilon_t,\qquad\ln h_t=\alpha_0+\alpha_1\ln h_{t-1}+v_t,\quad\epsilon_t\sim N(0,1),\ v_t\sim N(0,\sigma_v^2),\tag{12}$$

with $|\alpha_1|<1$. The likelihood $f(R\mid\beta,\alpha)=\int f(R\mid\beta,H)f(H\mid\alpha)dH$ is an $n$-dimensional integral, but
treating $H=(h_1,\dots,h_n)$ as augmented parameters ([[L03-07-markov-chains-gibbs]] §7) gives three
blocks: $\beta\mid H$ is a weighted regression (Result 12.1a after dividing by $\sqrt{h_t}$); $\alpha\mid H$ is an AR(1)
regression for $\ln h_t$; and each $h_t$ given its neighbours has (12.23)

$$f(h_t\mid\cdot)\propto h_t^{-1.5}\exp\Big[-\frac{(r_t-x_t'\beta)^2}{2h_t}-\frac{(\ln h_t-\mu_t)^2}{2\sigma^2}\Big],\tag{13}$$

with $\mu_t=[\alpha_0(1-\alpha_1)+\alpha_1(\ln h_{t+1}+\ln h_{t-1})]/(1+\alpha_1^2)$ and $\sigma^2=\sigma_v^2/(1+\alpha_1^2)$. (13) is not standard:
Jacquier, Polson and Rossi draw it by Metropolis, Tsay by Griddy Gibbs.

The **Petrobras page** (daily PBR log-returns since 2019) first compares iid models by maximum
likelihood: Gaussian $\hat\sigma=0.0328$; Student-$t$ with $\hat\nu=3$ and scale 0.0193, much heavier tails. It
then fits four SV variants with Kastner's `stochvol` (Gaussian or $t$ errors, with or without leverage
$\text{cor}(\epsilon_t,u_t)=\rho$), priors $\mu\sim N(0,100^2)$, $(\phi+1)/2\sim\text{Beta}(5,1.5)$, $\sigma^2\sim G(1/2,1/2)$,
$(\rho+1)/2\sim\text{Beta}(4,4)$, $\nu\sim\text{Exp}(0.1)$, and plots the posterior median volatility paths. The model and
its estimation belong to Class 8; here it is the example of MCMC with thousands of latent states.

---

## 8 · G — Hamiltonian Monte Carlo and Stan (exemplos-1-2-3-R-STAN.txt)

The lecturer's Stan programs state a model and priors and let the software sample: example 1, a normal
mean and sd with $\mu\sim N(1.7,0.3^2)$ and $\sigma\sim$ half-Cauchy$(0,1)$; example 2, a regression with $N(0,1)$
priors on $\alpha,\beta$ and half-Cauchy$(0,2.5)$ on $\sigma$; example 3, an SV model with Student-$t$ errors on DAX
returns, with $\phi\sim N(0.8,0.3^2)$ on $(-1,1)$, $\sigma\sim G(0.5,0.5)$, $\nu\sim G(1,0.05)$ and $h_1$ from the stationary
distribution. Stan's sampler is **Hamiltonian Monte Carlo** (NUTS): it treats $-\log\pi(\theta\mid y)$ as a potential
energy, adds a random momentum, and follows the gradient-driven trajectory for many steps before an
MH accept/reject. Proposals land far from the current point yet are accepted with high probability,
which beats random walks in high dimensions. The hierarchical Beta–Binomial of
[[L03-09-hierarchical-models-shrinkage]] is fitted this way; `Bayesian-beta-regression.html` fits a Beta
regression (Lula's vote share on abstention, population size and state dummies) with the `betaBayes`
MCMC sampler alongside the MLE. Python equivalents (PyMC, ArviZ) are not installed in this project; the
notes write every sampler in NumPy. Named only; not examinable.

---

## Links

- Prev: [[L03-07-markov-chains-gibbs]]; next: Gibbs and HMC on hierarchical models,
  [[L03-09-hierarchical-models-shrinkage]]. Formulas: [[L03-11-formulas]]; pitfalls: [[L03-12-pitfalls]];
  code: [[L03-13-python]] §8.
- Earlier: the logit by maximum likelihood (IRLS), [[../L02/L02-04-logistic-regression|L02 §4]].
- Rules: [[../../rules/08_monte_carlo_mcmc|rules/08]] (Metropolis–Hastings).
- Practice (statements in the books): **G 7.5** (p. 106, random-walk MH for the Laplace; proposal scale),
  **G 7.8** (p. 107, MH-within-Gibbs), **G 8.8** (p. 132, logit posterior), **T 12.4** (p. 670, SV by MCMC).
