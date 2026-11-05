---
tags: [notes, lecture-03, monte-carlo, numerical-standard-error, inverse-cdf, composition, accept-reject, importance-sampling, sir, zero-inflated-poisson, correlation]
date: 2026-10-27
status: taught
source: "aprendizagembayesiana-bayesianingredients.pdf slides 53–56 (MC toy example: π); Greenberg 1e Ch. 5 (pp. 63–75: §5.1 (5.1), §5.2, §5.3 Algorithms 5.2–5.4, (5.2), §5.4 Algorithm 5.5, §5.5, §5.6), §4.5 (p. 52); Morettin & Singer (2021) App. B §B.2 (pp. 456–457), §B.6.1–B.6.2 (pp. 467–471, (B.15)–(B.17)); fisicos-ABCD.html (SIR); correlationcoefficient.html; ZIP-fishing.html"
---

# Ingredients deck slides 53–56, G Ch. 5, MS App. B · Monte Carlo: replace an integral by an average of draws, and know its error

> **Claim.** Every Bayesian summary is an integral (a posterior mean, a probability, a predictive, a
> marginal likelihood). Monte Carlo writes it as an expectation, draws $M$ independent values and
> averages; the error falls like $1/\sqrt M$ and is measured by the **numerical standard error**.
> Hit-or-miss gives $\hat\pi$ with standard error $0.052$ at $M=1000$, so the deck's 3.196 is one error
> away from $\pi$. When direct draws are impossible: the **inverse cdf** for univariate targets,
> **composition** for mixtures (a Student-$t$ is a normal with a gamma precision), **accept–reject** with
> acceptance probability $1/c$ (Beta(3,3) from uniforms: $c=1.875$, 53%), and **importance sampling /
> SIR**, which reweight draws from another density. Importance sampling fails silently when the
> proposal's tails are too thin: Greenberg's own Beta(2,3) example has **infinite variance**.
> Prev: [[L03-05-model-comparison-bayes-factors]] · Next: [[L03-07-markov-chains-gibbs]] · Map: [[L03-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $f$ | target density (often a posterior known up to a constant) | — |
| $g$ or $h$ | proposal / importance density we can sample | — |
| $M$ (deck), $G$ (Greenberg), $n$ (MS) | number of draws | integer |
| $\bar g_M$ | Monte Carlo average of $g(X^{(i)})$ | — |
| n.s.e. | numerical standard error $\sqrt{\widehat{V}(g(X))/M}$ | $>0$ |
| $c$ | accept–reject constant with $f\le c\,g$ | $\ge1$ for normalised $f,g$ |
| $w_i$ | importance weight $f(x_i)/g(x_i)$ | $\ge0$ |

---

## 1 · U — integrals that cannot be done by hand (slides 42–43, 48–52)

The physicist C posterior of [[L03-03-normal-measurement-physicists]] needs
$\int\theta\,p(x\mid\theta)p(\theta)d\theta$ with a Student-$t$ prior: no closed form. The deck: "Bayesian computation was
done on limited, unrealistic models until the Monte Carlo revolution (and the computing revolution)
of the late 1980's and early 1990's" (slide 43). The idea is the law of large numbers: if we can draw
from a distribution, sample averages approximate its expectations.

---

## 2 · C — Monte Carlo integration and its error (slides 53–56; G p. 63, §5.6; MS §B.2)

For $X\sim f$ and a function $g$ with $E|g(X)|<\infty$,

$$E[g(X)]=\int g(x)f(x)dx\ \approx\ \bar g_M=\frac1M\sum_{i=1}^Mg(X^{(i)}),\qquad X^{(i)}\stackrel{iid}{\sim}f.\tag{1}$$

$\bar g_M$ is unbiased, converges by the law of large numbers, and has variance $V(g(X))/M$; Greenberg's
**numerical standard error** (p. 73) is

$$\text{n.s.e.}=\sqrt{\widehat V(g(X))/M}.\tag{2}$$

Probabilities are the case $g=\mathbf 1_A$: $P(A)\approx$ the fraction of draws in $A$ (G p. 63).

**Worked — hit-or-miss $\pi$ (slides 53–56).** Draw $(x_i,y_i)$ uniform on the unit square;
$P(x^2+y^2<1)=\pi/4$ (the area of a quarter disc), so $\hat\pi=4\times$ (fraction inside). The indicator
is Bernoulli with $p=\pi/4=0.7854$; by (2)

$$\text{se}(\hat\pi)=4\sqrt{\frac{p(1-p)}{M}}=4\sqrt{\frac{0.7854\times0.2146}{M}}=\frac{1.6422}{\sqrt M}.\tag{3}$$

At $M=1000$: $1.6422/31.623=0.0519$. The deck's $\hat\pi=3.196$ (slide 54) is $(3.196-3.1416)/0.0519=1.05$
standard errors high, an ordinary draw. At $M=10{,}000$: 0.0164; a seeded Python run gives 3.1452.

![Left: Beta(3,3) target density under the flat line c g(y) = 1.875, with 600 seeded proposals plotted as points at height u times 1.875; points under the density are accepted (52 percent) and points above it rejected. Right: six seeded running estimates of pi against thousands of draws, all inside a funnel pi plus or minus two standard errors that narrows from about plus or minus 0.1 at 1000 draws to 0.033 at 10000.](figures/L03-monte-carlo-accept-reject.png)
*Left: accept–reject for Beta(3, 3) with a $U(0,1)$ proposal, Algorithm 5.3 (G p. 67). Right: running hit-or-miss estimates of $\pi$ (slides 55–56) inside $\pi\pm2\,$se of (3). Both panels seeded.*

The right panel is slide 56 with its envelope drawn: every path wanders, none escapes the
$\pm2/\sqrt M$ funnel for long, and the funnel narrows slowly: **four times the draws for half the
error**.

---

## 3 · C — the inverse-cdf (probability integral transform) method (G §5.1; MS §B.4)

If $U\sim U(0,1)$ and $F$ is a continuous cdf, $Z=F^{-1}(U)$ has cdf $F$:

$$P(Z\le z)=P(F^{-1}(U)\le z)=P(U\le F(z))=F(z).\tag{4}$$

*Example (G pp. 64–65).* $f(y)=\frac38y^2$ on $[0,2]$: $F(y)=y^3/8$, so $Y=2U^{1/3}$. *Truncation (G (5.1)).*
To draw $X$ from $F$ restricted to $[c_1,c_2]$, set $X=F^{-1}\big(F(c_1)+U[F(c_2)-F(c_1)]\big)$; this is how the
truncated normals of the Tobit and probit samplers are drawn (G §8.2). The method needs the full cdf
and is univariate only.

---

## 4 · C — composition and scale mixtures (G §5.2, §4.5)

If $f(x)=\int g(x\mid y)h(y)dy$, draw $y\sim h$ then $x\sim g(\cdot\mid y)$; the $x$'s are draws from $f$.

**The Student-$t$ as a normal scale mixture (G p. 52).** Let $u\mid\lambda\sim N(0,\sigma^2/\lambda)$ and
$\lambda\sim G(\nu/2,\nu/2)$. The joint density is

$$f(u,\lambda)\propto\lambda^{1/2}e^{-\lambda u^2/2\sigma^2}\cdot\lambda^{\nu/2-1}e^{-\nu\lambda/2}=\lambda^{(\nu+1)/2-1}\exp\Big[-\lambda\,\frac{u^2+\nu\sigma^2}{2\sigma^2}\Big].\tag{5}$$

(5) is a $G\big(\frac{\nu+1}2,\frac{u^2+\nu\sigma^2}{2\sigma^2}\big)$ kernel in $\lambda$; integrating it out leaves the reciprocal of
its rate raised to the shape:

$$f(u)\propto\Big(\frac{u^2+\nu\sigma^2}{2\sigma^2}\Big)^{-(\nu+1)/2}\propto\Big(1+\frac{u^2}{\nu\sigma^2}\Big)^{-(\nu+1)/2},\tag{6}$$

the $t_\nu(0,\sigma^2)$ kernel. So a $t$ draw is a gamma draw followed by a normal draw. Seeded check
with $\nu=5$, 400,000 draws: variance 1.660 (theory $5/3$), $P(|u|>2.571)=0.0502$ (theory 0.05). This
representation is why Student-$t$ errors and priors fit inside Gibbs samplers ([[L03-07-markov-chains-gibbs]],
G §8.1.2) and why the horseshoe is a normal with a random scale ([[L03-10-sparsity-priors]]).

---

## 5 · C — accept–reject (G §5.3; MS §B.6.1)

**Algorithm 5.2.** Find a density $g$ we can sample and a constant $c$ with $f(y)\le c\,g(y)$ for all $y$.
(1) Draw $y\sim g$. (2) Draw $u\sim U(0,1)$. (3) Accept $y$ if $u\le f(y)/[c\,g(y)]$; otherwise return to (1).

**Why it works (G p. 67).** By Bayes' rule, the density of an accepted value is

$$h\big(y\mid\text{accept}\big)=\frac{P(\text{accept}\mid y)g(y)}{\int P(\text{accept}\mid y)g(y)dy}=\frac{[f(y)/cg(y)]\,g(y)}{\int[f(y)/cg(y)]\,g(y)dy}=\frac{f(y)/c}{1/c}=f(y),\tag{7}$$

and the acceptance probability is the denominator, $1/c$. Choose $c$ as small as possible. If $f$ is
known only up to a constant, $f=kr$ with $r\le cg$, accepting with probability $r/cg$ still yields draws
from $f$; then $c$ need not exceed 1.

**Worked — Beta(3, 3) from $U(0,1)$ (Algorithm 5.3).** $f(y)=30y^2(1-y)^2$ peaks at $y=\frac12$:
$c=30\times\frac1{16}=1.875$, acceptance $1/1.875=0.5333$. A proposal $y=0.15$ has
$f(0.15)=30(0.0225)(0.7225)=0.4877$ and is accepted with probability $0.4877/1.875=0.2601$. Seeded run
of 200,000: acceptance 0.5339; accepted draws have mean 0.500 and variance 0.0357 ($=1/28$).

**Worked — $N(0,1)$ from a Laplace proposal (Algorithm 5.4).** By symmetry, sample $|y|$ from the
half-normal $f(x)=\sqrt{2/\pi}\,e^{-x^2/2}$ with proposal $g(x)=e^{-x}$, $x>0$, and attach a random sign. The ratio
$f/g=\sqrt{2/\pi}\,e^{x-x^2/2}$ is maximised at $x=1$:

$$c=\sqrt{2/\pi}\,e^{1/2}=\sqrt{2e/\pi}=1.3155,\qquad\text{acceptance }1/c=0.7602.\tag{8}$$

Greenberg's test (5.2), accept if $u\le e^{x-x^2/2-1/2}$, is exactly $u\le f(x)/[c\,g(x)]$ with (8). His text gives
"the probability of acceptance is $1/c=0.6577$": $0.6577=\sqrt{e/2\pi}$ is the constant that dominates the
unnormalised kernel $\frac1{\sqrt{2\pi}}e^{-x^2/2}$, whose integral over $x>0$ is $\frac12$, so the acceptance rate is
$\frac12/0.6577=0.7602$ either way. A seeded run of 200,000 accepts 0.7605.

---

## 6 · C — importance sampling (G §5.4; MS §B.6.2)

Multiply and divide by a density $h$ we can sample:

$$E_f[g(X)]=\int g(x)\frac{f(x)}{h(x)}h(x)dx\ \approx\ \frac1G\sum_{i=1}^Gg(X^{(i)})\,w_i,\qquad w_i=\frac{f(X^{(i)})}{h(X^{(i)})},\ X^{(i)}\sim h.\tag{9}$$

When $f$ is known only up to a constant, use the self-normalised form (MS (B.17)):

$$\tilde\theta=\frac{\sum_iw_ig(X^{(i)})}{\sum_iw_i},\tag{10}$$

consistent if the support of $h$ covers that of $f$ (Geweke 1989, as cited by MS).

**The variance condition (G p. 70).** The estimator's second moment is
$E_h[(gf/h)^2]=\int g^2f^2/h\,dx$, large "when the tail values of $h(\cdot)$ are very small compared to the tail
values of $f(\cdot)$".

**Worked — Greenberg's Algorithm 5.5, and its hidden flaw.** Target $E[(1+x^2)^{-1}]$ for $x\sim\text{Exp}(1)$
truncated to $[0,1]$, $f(x)=e^{-x}/(1-e^{-1})$; importance density $h=\text{Beta}(2,3)$, $h(x)=12x(1-x)^2$. The
exact value is 0.8302 (G p. 71; quadrature 0.830217). Greenberg reports 0.8268 with n.s.e. 0.0030 from
$G=10{,}000$; a seeded Python run gives 0.8003 with a computed n.s.e. of 0.0089, three "standard errors"
away. The reason is near $x=0$: $f(0)g(0)=1.582$ while $h(x)\approx12x$, so

$$\int_0^\varepsilon\frac{g^2f^2}{h}dx\approx\int_0^\varepsilon\frac{1.582^2}{12x}dx=\infty.\tag{11}$$

**The estimator has infinite variance.** It is still consistent, but its sample standard error means
nothing and convergence is erratic. (Numerically, each factor of 100 closer to zero adds
$1.582^2\log(100)/12=0.960$ to the truncated second moment.) A proposal with a positive density at 0,
such as $U(0,1)$ or the truncated exponential itself, removes the problem.

---

## 7 · C — sampling importance resampling (SIR) (MS §B.6.2; fisicos-ABCD, correlation, ZIP pages)

(a) Draw $x_1,\dots,x_n$ from $g$. (b) Compute normalised weights $w_i=\frac{f(x_i)/g(x_i)}{\sum_jf(x_j)/g(x_j)}$.
(c) Resample from $\{x_i\}$ with probabilities $w_i$. The resampled values are approximately draws from $f$;
MS's argument: the resampled cdf $\sum_{i:x_i\le a}w_i$ converges to $\int_{-\infty}^af$ by the strong law (p. 470).

With a uniform $g$ on a box, $w_i\propto$ likelihood × prior: the lecturer's pages use exactly this.

**Worked — physicist C (`fisicos-ABCD.html`).** $10^6$ proposals from $U(600,1000)$, weights
$N(850\mid\theta,40^2)\,t_5(\theta\mid900,240)$, $10^6$ resampled draws. Seeded Python: mean 891.13 against the quadrature
value 891.12. The **effective sample size** $(\sum w_i)^2/\sum w_i^2$ is 144,275: only one draw in seven
carries real weight, because most uniform proposals land where the posterior is negligible.

### 7.1 · Worked — the correlation coefficient (`correlationcoefficient.html`)

Standardised pairs $x_i=(x_{i1},x_{i2})$, $n=14$, modelled as bivariate normal with unit variances and
correlation $\rho$:

$$p(x_{1:n}\mid\rho)=\Big(\frac1{2\pi\sqrt{1-\rho^2}}\Big)^n\exp\Big\{-\frac{1}{2(1-\rho^2)}\Big[\sum_i(x_{i1}^2+x_{i2}^2)-2\rho\sum_ix_{i1}x_{i2}\Big]\Big\},\tag{12}$$

which "has no known form, regardless of which prior one uses". Data: heights and weights of 14
students (the 15th, the lecturer, removed as an outlier), sample correlation 0.615. Posterior
quantiles (2.5%, 50%, 97.5%):

| Prior | Page (SIR) | Exact (quadrature on $\rho$) |
|---|---|---|
| uniform $p(\rho)=\frac12$ | 0.102, 0.569, 0.784 | 0.105, 0.567, 0.784 |
| what the page codes, $\propto1/\sqrt{1+\rho^2}$ | 0.081, 0.558, 0.783 | 0.089, 0.556, 0.781 |
| arc-sine $\frac1\pi(1-\rho^2)^{-1/2}$, as stated | — | 0.130, 0.589, 0.794 |

The page states the arc-sine prior but codes `prior = 1/sqrt(1+rho^2)`; its second column is the
posterior under that other prior. The true arc-sine prior puts more mass near $\pm1$ and moves the
posterior up. With 14 observations the prior visibly matters in the lower tail.

### 7.2 · Worked — zero-inflated Poisson (`ZIP-fishing.html`)

Fish caught by groups that brought a camper and children. Some groups never fish, so zeros come from
two sources: with probability $\pi$ a structural zero, otherwise a Poisson$(\lambda)$ count:

$$P(y_i\mid\lambda,\pi)=\begin{cases}\pi+(1-\pi)e^{-\lambda},&y_i=0,\\(1-\pi)\dfrac{\lambda^{y_i}e^{-\lambda}}{y_i!},&y_i=1,2,\dots\end{cases}\qquad E(y_i)=(1-\pi)\lambda,\ \ V(y_i)=(1-\pi)\lambda(1+\pi\lambda).\tag{13}$$

**Data.** The page's frequency table: 24 zeros, then counts 1 (6), 2 (2), 3 (4), 4 (2), 5 (3), 7, 8, 14,
16 (one each). That is $n=45$ groups (the text says 42; the printed estimates below need 45), $n_0=24$,
$\sum y_i=90$, $\bar y=2$, $s^2=12.318$.

**MLE.** Set the two score equations of $\log L=n_0\log D+(n-n_0)[\log(1-\pi)-\lambda]+\sum y_i\log\lambda$,
$D=\pi+(1-\pi)e^{-\lambda}$, to zero. The $\pi$-equation gives $D=n_0(1-\pi)(1-e^{-\lambda})/(n-n_0)$; substituting it into
the $\lambda$-equation leaves

$$\frac{\lambda}{1-e^{-\lambda}}=\bar z=\frac{\sum y_i}{n-n_0}=\frac{90}{21}=4.2857,\qquad\hat\pi=1-\frac{\bar y}{\hat\lambda},\tag{14}$$

whose root is $\hat\lambda=\bar z+W_0(-\bar ze^{-\bar z})=\mathbf{4.223}$ ($W_0$ the principal Lambert branch), and
$\hat\pi=1-2/4.223=\mathbf{0.526}$. (14) says the fitted probability of a positive count,
$(1-\hat\pi)(1-e^{-\hat\lambda})$, equals the observed share $21/45$.

**Method of moments.** Equate $\bar y$ and $s^2$ to (13)'s moments: $\lambda_{mm}=(s^2+\bar y^2)/\bar y-1=(12.318+4)/2-1=7.159$
and $\pi_{mm}=(s^2-\bar y)/(s^2+\bar y^2-\bar y)=10.318/14.318=0.721$, the page's values. The two large counts
(14, 16) inflate $s^2$ and drive the moment estimates; the page's fitted-frequency table shows the MLE
fitting the zeros exactly and MM overpredicting them (32 vs 24).

**Posterior.** Uniform priors on $\lambda\in(1,8)$ and $\pi\in(0.1,0.9)$ (the page's SIR box). On a fine grid the
posterior means are $E(\lambda\mid y)=4.266$ and $E(\pi\mid y)=0.524$, close to the MLE because the priors are flat
over the region the likelihood occupies. The page's posterior predictive intervals for each count come
from pushing the SIR draws through (13).

---

## 8 · C — using simulated output (G §5.6)

Draws $\theta^{(1)},\dots,\theta^{(G)}$ from a joint posterior give, column by column, draws from each
**marginal** without computing any integral (G p. 74); functions of the draws (ratios, $XY$, predicted
probabilities) are draws of the function. Quantiles of the sorted draws give credible intervals;
kernel-smoothed histograms give densities. Greenberg's illustration $Z=XY$ with $X\sim\text{Beta}(3,3)$,
$Y\sim\text{Beta}(5,3)$: mean 0.3146, n.s.e. 0.0021, 95% interval (0.0719, 0.6279) from $G=5000$.

---

## 9 · G — multivariate draws (G §5.5, named)

$X=\mu+C'Z$ with $Z\sim N_p(0,I)$ and $\Sigma=C'C$ (Cholesky) gives $X\sim N_p(\mu,\Sigma)$, used in every Gibbs
step that draws a coefficient vector. Accept–reject and importance sampling become hard in many
dimensions (a dominating density over the whole support, tails heavy enough everywhere), which is
what motivates MCMC.

---

## Links

- Prev: [[L03-05-model-comparison-bayes-factors]]; next: dependent draws from a Markov chain,
  [[L03-07-markov-chains-gibbs]]. Formulas: [[L03-11-formulas]]; pitfalls: [[L03-12-pitfalls]]; code:
  [[L03-13-python]] §6.
- Earlier: Monte Carlo for sampling distributions and the bootstrap,
  [[../L01/L01-05-comparing-estimators-mse-bootstrap|L01 §5]]; [[../L01/L01-02-poisson-mle-properties|L01 §2]].
- Rules: [[../../rules/08_monte_carlo_mcmc|rules/08]] (Monte Carlo integration).
- Practice (statements in the books): **G 5.4** (p. 75, accept–reject Beta(3,3)), **MS B.16** (p. 478,
  accept–reject for a truncated gamma), **MS B.19** (p. 478, discrete accept–reject).
