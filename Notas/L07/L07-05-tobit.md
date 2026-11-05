---
tags: [notes, lecture-07, tobit, censoring, truncation, data-augmentation, gibbs, limited-dependent-variables]
date: 2026-10-25
status: taught
source: "limiteddependentvariablemodels.pdf (Lopes), slides 4–10: Tobit examples (Greene p. 761), censoring rule, likelihood, data augmentation, linear Tobit full conditionals, truncation-probability example, posteriors with and without the censoring. G §8.2.1 (pp. 117–122: likelihood, eq. 8.6, Algorithm 8.2, Mroz example Table 8.1). W 6e §17.2 (pp. 536–543: eqs. 17.18–17.30, Example 17.2, Tables 17.3–17.4), §17.4 (pp. 547–553: eqs. 17.36–17.41). Numbers re-run in L07_python_checks.py §5."
---

# LDV slides 4–10 · The Tobit: a regression on a latent y*, seen only above zero — fill in the hidden part and it is OLS again

> **Claim.** A **corner solution** or **censored** outcome is $y=\max(0,y^*)$ with $y^*=x'\beta+u$,
> $u\sim N(0,\sigma^2)$. The likelihood mixes densities (for $y>0$) and probabilities $\Phi(-x'\beta/\sigma)$ (for $y=0$)
> and is awkward for Bayes; **data augmentation** (Chib 1992) draws the hidden $y_i^*$ of the zeros from
> a normal **truncated to $(-\infty,0]$**, after which β and σ² have the plain regression conditionals. The
> coefficient β is the effect on the *latent* mean; the effect on what is observed is
> $\partial E(y\mid x)/\partial x_j=\beta_j\Phi(x'\beta/\sigma)$ — and OLS on the censored data estimates roughly that, not β:
> with normal regressors exactly $\beta\cdot P(y>0)$.
> Prev: [[L07-04-hierarchical-linear-models]] · Next: [[L07-06-probit-ordered-multinomial]] · Map: [[L07-00-map]]

**Notation.**

- $y_i^*=x_i'\beta+u_i$, $u_i\sim N(0,\sigma^2)$: latent outcome; $y_i=y_i^*1(y_i^*>0)=\max(0,y_i^*)$ observed (slide 5; G p. 118; W 17.18–17.19).
- $C=\{i:y_i=0\}$, $k=|C|$ the number of zeros (slide 6).
- $z_i=x_i'\beta/\sigma$; $\phi,\Phi$ standard normal pdf and cdf; $\lambda(c)=\phi(c)/\Phi(c)$ inverse Mills ratio (W p. 538).
- $TN_{(a,b]}(\mu,\sigma^2)$: normal truncated to $(a,b]$ (slide 8 writes $N_{[-\infty,0]}$).

---

## 1 · U — corner solutions, censoring, truncation

Slide 4 lists Tobin's (1958) durable-goods purchases, hours worked by married women, extramarital
affairs, arrests, vacation spending: many exact zeros, a continuous spread above zero. Two stories
produce the same data (G p. 118): **top/bottom coding** — the value exists but is reported as the
limit (true censoring) — and **corner solutions** — the zero is a genuine choice. The Tobit algebra
is the same; the interpretation differs (W p. 539: for corner solutions $y^*$ often has no meaning
and σ is not "ancillary"). **Truncation** is different again: observations with $y^*\le0$ are not in the
sample at all, $x$ included (G p. 118; W §17.4b). The slides call the censoring rule "truncation"
(slide 5) and $P(y=0)$ "probability of truncation" (slides 9–10); read **censoring** throughout.

## 2 · C — the likelihood (slide 6; W 17.20–17.22)

For $y_i>0$, $y_i=y_i^*$ and the density is the normal one:

$$f(y_i\mid x_i,\beta,\sigma)=\frac1\sigma\phi\Big(\frac{y_i-x_i'\beta}{\sigma}\Big),\quad y_i>0.\tag{1}$$

For $y_i=0$, a probability mass:

$$P(y_i=0\mid x_i)=P(u_i\le-x_i'\beta)=\Phi(-x_i'\beta/\sigma)=1-\Phi(z_i).\tag{2}$$

Multiplying over independent observations (slide 6 writes $\prod_{i:y_i>0}f(y_i\mid x_i,\theta)\{F(0\mid x_i,\theta)\}^k$, the
second factor as if all zeros had the same $x$; it is $\prod_{i\in C}F(0\mid x_i,\theta)$):

$$L(\beta,\sigma)=\prod_{i\in C}\Phi\Big(-\frac{x_i'\beta}{\sigma}\Big)\prod_{i\notin C}\frac1\sigma\phi\Big(\frac{y_i-x_i'\beta}{\sigma}\Big)\qquad(\text{G p. 118}),\tag{3}$$

$$\ell_i(\beta,\sigma)=1(y_i=0)\log[1-\Phi(z_i)]+1(y_i>0)\log\{\sigma^{-1}\phi[(y_i-x_i'\beta)/\sigma]\}\qquad(\text{W 17.22}).\tag{4}$$

With a normal prior on β and inverse gamma on σ², (3) × prior is not a standard family (the Φ
factors): "very complex" (G p. 118).

## 3 · C — data augmentation (slide 7; G pp. 118–120)

Add the latent $y_i^*$ for $i\in C$ to the unknowns. Slide 7's "complete likelihood" step:

$$p(y_i\mid x_i,\theta)=\int p(y_i\mid y_i^*)f(y_i^*\mid x_i,\theta)\,dy_i^*=p(y_i\mid y_i^*>0)[1-F(0\mid x_i,\theta)]+p(y_i\mid y_i^*\le0)F(0\mid x_i,\theta),$$

with $p(y_i\mid y_i^*)=1(y_i=0)1(y_i^*\le0)+1(y_i>0)1(y_i=y_i^*)$: given $y^*$, $y$ is known. Hence the joint posterior
of $(\beta,\sigma^2,y_C^*)$ (G eq. 8.6, p. 119):

$$\pi(\beta,\sigma^2,y_C^*\mid y)\propto\prod_{i=1}^n\big[1(y_i=0)1(y_i^*\le0)+1(y_i>0)\big]\,N(y^*\mid X\beta,\sigma^2I)\,\pi(\beta)\pi(\sigma^2),\tag{5}$$

where $y^*$ has $y_i^*=y_i$ for $i\notin C$. Read off the conditionals:

- **β, σ² given $y^*$:** (5) is the normal regression likelihood of $y^*$ times the priors — the conditionals
  (8.2)–(8.3) of G (note 01's (7)–(8) with Ω = I) **with $y^*$ in place of $y$**. Given $y^*$, β and σ² do not
  depend on $y$ (G p. 119).
- **$y_i^*$, $i\in C$, given β, σ²:** the factor in $y_i^*$ is $1(y_i^*\le0)N(y_i^*\mid x_i'\beta,\sigma^2)$:

$$y_i^*\mid y_i=0,\beta,\sigma^2\sim TN_{(-\infty,0]}(x_i'\beta,\sigma^2),\qquad y_i^*=y_i\ \text{if}\ y_i>0\qquad(\text{slide 7}).\tag{6}$$

(6) is drawn by the inverse-CDF formula of [[L07-03-ar1-errors]] (15) with $a=-\infty$, $b=0$. This is G's
Algorithm 8.2 (p. 120). The marginal posterior of $(\beta,\sigma^2)$ is obtained by "ignoring the draws" of $y_C^*$.

## 4 · C — the linear Tobit conditionals (slide 8)

Prior $\beta\sim N(\beta_0,V_0)$, $\sigma^2\sim IG(\nu_0/2,\nu_0s_0^2/2)$. From (5):

$$\beta\mid\sigma^2,y^*\sim N\big(V_\beta(V_0^{-1}\beta_0+\sigma^{-2}X'y^*),V_\beta\big),\qquad V_\beta^{-1}=V_0^{-1}+\sigma^{-2}X'X,\tag{7}$$
$$\sigma^2\mid\beta,y^*\sim IG\Big(\frac{\nu_0+n}{2},\frac{\nu_0s_0^2+(y^*-X\beta)'(y^*-X\beta)}{2}\Big).\tag{8}$$

**Two slips on slide 8:** it prints $V_\beta^{-1}=V_0^{-1}+\sigma^{-2}(X'X)^{-1}$ — the data precision is $\sigma^{-2}X'X$, not its
inverse — and the mean $V_\beta(V_0^{-1}\beta_0+X'y^*)$ without the $\sigma^{-2}$ on $X'y^*$. (7) is G's step 8.1 (p. 120).

## 5 · C — what β means: three conditional means (W §17.2a, pp. 538–539)

**Positive part.** For $z\sim N(0,1)$, $E(z\mid z>c)=\phi(c)/[1-\Phi(c)]$. Then

$$E(y\mid y>0,x)=x'\beta+E(u\mid u>-x'\beta)=x'\beta+\sigma\frac{\phi(-z)}{1-\Phi(-z)}=x'\beta+\sigma\lambda(z)\qquad(\text{W 17.24}),\tag{9}$$

using $\phi(-z)=\phi(z)$, $1-\Phi(-z)=\Phi(z)$. **Unconditional.** $E(y\mid x)=P(y>0\mid x)E(y\mid y>0,x)$ (W 17.23); substitute
(9) and $\Phi\lambda=\phi$:

$$E(y\mid x)=\Phi(z)[x'\beta+\sigma\lambda(z)]=\Phi(z)\,x'\beta+\sigma\phi(z)\qquad(\text{W 17.25}).\tag{10}$$

**Partial effects.** With $d\lambda/dc=-\lambda(c)[c+\lambda(c)]$ and $\partial z/\partial x_j=\beta_j/\sigma$, differentiate (9):

$$\frac{\partial E(y\mid y>0,x)}{\partial x_j}=\beta_j+\sigma\frac{\beta_j}{\sigma}\cdot\{-\lambda(z)[z+\lambda(z)]\}=\beta_j\{1-\lambda(z)[z+\lambda(z)]\}\qquad(\text{W 17.26}).\tag{11}$$

Differentiate (10), with $d\phi/dz=-z\phi$:

$$\frac{\partial E(y\mid x)}{\partial x_j}=\frac{\beta_j}{\sigma}\phi(z)x'\beta+\Phi(z)\beta_j+\sigma\frac{\beta_j}{\sigma}(-z\phi(z))=\frac{\beta_j}{\sigma}\phi(z)\,\sigma z+\Phi(z)\beta_j-\beta_jz\phi(z)=\beta_j\Phi(z)\qquad(\text{W 17.30}).\tag{12}$$

(Both derivatives are checked numerically against (9)–(10) in `L07_python_checks.py` §5.) The bracket
in (11) lies strictly between 0 and 1 (W p. 539), and $\Phi(z)\in(0,1)$: **every observable effect is β
shrunk**, by a factor that depends on $x$ and on σ.

![Left: the latent mean 2x, the Tobit mean Phi(z)2x + 0.5 phi(z) and the conditional-on-positive mean 2x + 0.5 lambda(z) against x from -1.5 to 1.5; right: the slide-9 probability P(y = 0) = Phi(-2a/2.062) against a with points at a = 0, 0.7, 1.3 (0.500, 0.249, 0.104) and the OLS attenuation factor P(y > 0)](figures/L07-tobit-moments.png)
*Left: (9), (10) and the latent line, $\beta=2$, $\sigma=0.5$. Right: (13) and $1-$(13), slide 9's example.*

Far to the right all three means coincide (almost nobody is censored). Far to the left $E(y\mid x)\to0$
while $E(y\mid y>0,x)$ stays positive — the few who are above zero are those with large $u$, the
selection that makes OLS on the positive subsample biased (§7).

## 6 · C — slide 9's example and what OLS on censored data estimates

**Slide 9.** $y_i^*\mid x_i\sim N(\beta x_i,\sigma^2)$, $x_i\sim N(a,1)$, so unconditionally $y^*\sim N(\beta a,\beta^2+\sigma^2)$ and

$$P(y=0\mid a,\beta=2,\sigma^2=0.25)=\Phi\Big(\frac{-2a}{\sqrt{4.25}}\Big)=\Phi(-2a/2.062).\tag{13}$$

At $a=0$: $\Phi(0)=0.500$. At $a=0.7$: $\Phi(-1.4/2.062)=\Phi(-0.679)=0.249$. At $a=1.3$: $\Phi(-2.6/2.062)=\Phi(-1.261)=0.104$ —
the slide's "Prob. trunc. = 0.5, 0.25, 0.1" (slide 10).

**Slide 10** compares, under a non-informative prior ($\nu_0=0$, $V_0^{-1}=0$), the posterior of β that ignores the
censoring (red: the zeros treated as data) with the Tobit posterior (black, centred on the true 2).
The red curve is centred well below 2 at $a=0$ and approaches 2 as censoring falls. How far below:

**Claim.** With normal $x$, the population OLS slope of $y$ on $x$ is $\beta\,P(y>0)$.
*Proof.* $(x,y^*)$ is bivariate normal. Stein's lemma: for jointly normal $(x,w)$ and smooth $g$,
$\mathrm{Cov}(x,g(w))=\mathrm{Cov}(x,w)\,E[g'(w)]$. Take $w=y^*$, $g(w)=\max(0,w)$, $g'(w)=1(w>0)$:

$$\mathrm{Cov}(x,y)=\mathrm{Cov}(x,y^*)\,P(y^*>0)=\beta\,\mathrm{Var}(x)\,P(y>0)\ \Rightarrow\ \frac{\mathrm{Cov}(x,y)}{\mathrm{Var}(x)}=\beta P(y>0).\tag{14}$$

Slide 9's values: $2\times0.500=1.00$, $2\times0.751=1.50$, $2\times0.896=1.79$ (a Monte Carlo with $10^6$ draws at
$a=0.7$ gives 1.5033 vs 1.5029, `L07_python_checks.py` §5). (14) is the population version of W's
remark that OLS slopes estimate $\partial E(y\mid x)/\partial x_j=\beta_j\Phi$ and must be compared with
$\hat\beta_j\times$ a scale factor (W p. 539).

> **Interactive companion.** [The Censoring Dial](companions/companion-tobit-censoring.html) — move the
> covariate mean $a$, β, σ and an evaluation point $x_0$; read $P(y=0)$ (0.249 at slide 9's $a=0.7$), the OLS
> slope $\beta P(y>0)$ and every term of (9)–(12) at $x_0$.

## 7 · C — W Example 17.2: married women's hours (Table 17.3, p. 541)

MROZ: 753 women, 325 with zero hours. Reproduced exactly here by MLE of (4) (`L07_python_checks.py` §5):

| | OLS | Tobit MLE | Tobit Gibbs (flat prior) mean (sd) |
|---|---|---|---|
| nwifeinc | −3.45 | −8.81 (4.46) | |
| educ | 28.76 | 80.65 (21.58) | 81.84 (21.76) |
| exper | 65.67 | 131.56 (17.28) | |
| exper² | −0.700 | −1.86 (0.54) | |
| age | −30.51 | −54.41 (7.42) | |
| kidslt6 | −442.09 | −894.02 (111.88) | −902.63 (112.86) |
| kidsge6 | −32.78 | −16.22 (38.64) | |
| constant | 1,330.48 | 965.31 (446.44) | |
| $\hat\sigma$ | 750.18 | 1,122.02 | 1,138.8 |
| log-likelihood | — | −3,819.09 | |

The Gibbs column is Algorithm 8.2 with $V_0^{-1}=0$, $\nu_0=0$ (1,000 burn-in + 5,000 draws): posterior means
and sds within a fraction of an SE of the MLE, as a flat-prior posterior should be.

**Comparing with OLS.** The Tobit educ coefficient is almost three times OLS's, but they measure
different things. The APE scale factor $n^{-1}\sum_i\Phi(x_i'\hat\beta/\hat\sigma)=$ **0.589**, so the Tobit average partial
effect of educ is $0.589\times80.65=$ **47.5** hours vs OLS 28.8; at the averages (with $(\overline{exper})^2$) the
factor is **0.645** (W pp. 540–541; both reproduced).

**G's version (Table 8.1, p. 121).** Same data, covariates children under 6, children 6+, age, husband's
wage, informative priors: posterior means −556.4 (young children) and −191.7 (older children). From
the predictive distribution, $P(\text{zero hours})$ is 0.431 with young children vs 0.328 with older children;
mean hours about 214 vs 587; given positive hours about 1,284 vs 1,105 (G pp. 121–122).

## 8 · C/G — censored and truncated regression (W §17.4, pp. 547–553)

**Censored regression** (W 17.36–17.39): $w_i=\min(y_i^*,c_i)$ with a known, possibly observation-specific
censoring point (durations, top-coding): density $\sigma^{-1}\phi((w-x_i'\beta)/\sigma)$ below $c_i$, mass
$1-\Phi((c_i-x_i'\beta)/\sigma)$ at $c_i$ — (3) with the inequality reversed. With true censoring, $y^*$ is the
variable of interest and β its regression coefficient, unlike a corner solution.

**Truncated regression** (W 17.40–17.41): $(x_i,y_i)$ seen only if $y_i\le c_i$; the density of the observed
$y$ is $f(y\mid x_i'\beta,\sigma^2)/F(c_i\mid x_i'\beta,\sigma^2)$. No point masses, and no information about the excluded
units. OLS on a truncated sample is biased: with slide 9's design ($a=0.7$, $\beta=2$), OLS on the units
with $y^*>0$ only gives a slope of **1.902** (simulated, `L07_python_checks.py` §7) — the inverse Mills
ratio in (9) is an omitted regressor correlated with $x$ (W p. 538).

## Links

- Unit: [[L07-00-map]] · [[L07-03-ar1-errors]] (the truncated-normal draw) · [[L07-06-probit-ordered-multinomial]] (the same augmentation with σ = 1) · [[L07-02-student-t-errors]] (t errors: G 8.6) · [[L07-07-formulas]] · [[L07-08-pitfalls]] · [[L07-09-python]] §5.
- Class 2: [[../L02/L02-04-logistic-regression|L02 §4]] (binary outcomes, partial effects shrunk by a density factor — the logit analogue of (12)).
- Rules pack: [[../../rules/06_classificacao_validacao|rules/06]] (probit/Tobit listed for Class 7).
- **Practice** (statements in the books): G 8.6 (p. 132, Tobit with Student-t errors); W 17.3 (p. 559, partial effects of a log regressor in the Tobit); W 17.C3 (p. 561, FRINGE pensions); W 17.C9 (p. 562, APPLE ecolabeled apples).
