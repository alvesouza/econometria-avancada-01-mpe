---
tags: [notes, lecture-01, poisson, overdispersion, change-point, profile-likelihood, likelihood-ratio, coal-mining]
date: 2026-10-19
status: taught
source: "poisson-with-breakpoint.pdf (slides 13–21); data .agent/notes/coal-mining-data.md (Jarrett 1979, 1851–1962); Bolfarine & Sandoval (2010) §3.4 (pp. 46–47, verossimilhança perfilada), §6.5 (pp. 103–108, (6.5.1), Thm 6.5.1, Ex. 6.5.5); Greenberg 1e §7.1.1 (pp. 93–94, (7.3)–(7.4)) as forward link"
---

# Coal-mining disasters · One Poisson rate does not fit; two do, and the break is around 1890

> **Claim.** The 112 yearly counts have mean 1.705 and variance 2.714. That is **overdispersed**
> ($s^2/\bar y=1.59$, dispersion test $p<0.001$), so a single $\lambda$ is rejected by the
> model's own $E=V$ fingerprint. Splitting at 1890 gives two series that each **pass** the test:
> rates **3.125** and **0.917**, with Wald intervals far apart. Profiling the two rates out of a
> two-regime likelihood puts the cut at **$\tau=1891$** (weight 0.251; 1889–1892 together carry
> 0.696). The likelihood-ratio statistic against one rate is **70.0**. The cut was **searched for**,
> so the statistic is not referred to $\chi^2_1$, but no reference distribution rescues the
> single-rate model.
> Prev: [[L01-02-poisson-mle-properties]] · Next: [[L01-04-first-bayesian-poisson]] · Map: [[L01-00-map]]

**Notation.**

| Symbol | Meaning | Range / value |
|---|---|---|
| $y_t$ | disasters in year $t$ | $\{0,\dots,6\}$ observed |
| $n$, $s$ | years, total disasters (full sample) | 112, 191 |
| $\tau$ | cut year = **last year of the high-rate regime** | $1851,\dots,1961$ |
| $n_1,s_1$ / $n_2,s_2$ | years and disasters up to $\tau$ / after $\tau$ | $n_1+n_2=112$, $s_1+s_2=191$ |
| $\lambda_1,\lambda_2$ | rates before and after the cut | $(0,\infty)$ |
| $\ell_p(\tau)$ | profile log-likelihood of $\tau$ | — |
| $w(\tau)$ | normalised profile likelihood over a window $W$ of cut years | $[0,1]$ |
| $D$ | dispersion statistic $(n-1)s^2/\bar y$ | $\ge0$ |

---

## 1 · U — the series (slide 13)

![Vertical bars of yearly coal-mining disaster counts from 1851 to 1962, with three horizontal MLE lines: a dashed line at 1.705 over the whole period, a line at 3.125 over 1851-1890 and a line at 0.917 over 1891-1962; counts of 3 to 6 are common before 1890 and rare afterwards.](figures/L01-coal-series.png)
*Yearly counts with the three MLEs, $\bar y$ over each span. Source: slide 13; data Jarrett (1979), `.agent/notes/coal-mining-data.md`.*

The eye does the change-point analysis before the algebra does. Before about 1890, years with
three or more disasters are the norm. After it, most years have zero or one. The dashed
full-period line at 1.705 sits **between** the two clouds and describes neither. Everything below
puts numbers on that impression.

---

## 2 · Worked — one Poisson per period (slide 14)

Each column applies the MLE $\hat\lambda=s_n/n$ and the Wald interval
$\hat\lambda\pm1.96\sqrt{\hat\lambda/n}$ from [[L01-02-poisson-mle-properties]] (9) and (14):

| | 1851–1962 | 1851–1890 | 1891–1962 |
|---|---|---|---|
| $n$ | 112 | 40 | 72 |
| $s_n$ | 191 | 125 | 66 |
| $\hat\lambda_{MLE}=\bar y$ | $191/112=$ **1.705** | $125/40=$ **3.125** | $66/72=$ **0.917** |
| SE $=\sqrt{\hat\lambda/n}$ | $\sqrt{0.015227}=0.123$ | $\sqrt{0.078125}=0.280$ | $\sqrt{0.012731}=0.113$ |
| 95% CI | $1.705\pm0.242=(1.464,\,1.947)$ | $3.125\pm0.548=(2.577,\,3.673)$ | $0.917\pm0.221=(0.696,\,1.138)$ |
| $s^2$ | 2.714 | 2.574 | 1.063 |
| $s^2/\bar y$ | 1.592 | 0.824 | 1.160 |
| Dispersion test p-value | $<0.001$ | 0.774 | 0.168 |

> **The rate falls from about 3.1 to about 0.9 disasters a year, and the two intervals are
> nowhere near each other** (2.577 against 1.138).

---

## 3 · C — the dispersion test (slide 14)

Under the Poisson model, $V(y)=E(y)=\lambda$ ([[L01-02-poisson-mle-properties]] (2)–(3)), so
$s^2/\bar y$ should be near 1. The statistic is

$$D=\frac{(n-1)s^2}{\bar y}\ \stackrel a\sim\ \chi^2_{n-1}\quad\text{under the Poisson model.}\tag{1}$$

The logic is the Gaussian fact $(n-1)s^2/\sigma^2\sim\chi^2_{n-1}$ (B Thm 5.1, p. 73), with
$\sigma^2=\lambda$ replaced by its estimate $\bar y$. For counts it is an approximation. The deck
reports the **upper-tail** p-value $P(\chi^2_{n-1}\ge D)$, a test against **over**dispersion.

**Arithmetic.**

$$\text{1851–1962: } D=\frac{111\times2.7142}{1.7054}=176.7,\quad P(\chi^2_{111}\ge176.7)=0.00007<0.001;$$

$$\text{1851–1890: } D=\frac{39\times2.5737}{3.125}=32.1,\quad P(\chi^2_{39}\ge32.1)=0.774;$$

$$\text{1891–1962: } D=\frac{71\times1.0634}{0.9167}=82.4,\quad P(\chi^2_{71}\ge82.4)=0.168.$$

> **Overdispersion is a symptom of a change in rate** (slide 21). The full series fails, and each
> part is consistent with the Poisson.

**Why a mixture inflates the variance (law of total variance).** Let year $t$'s rate be
$\lambda_1=3.125$ with weight $\pi=40/112$ and $\lambda_2=0.917$ otherwise. Then

$$V(y)=E[V(y\mid\lambda)]+V[E(y\mid\lambda)]=E(\lambda)+\pi(1-\pi)(\lambda_1-\lambda_2)^2.\tag{2}$$

Substitute the numbers:

$$V(y)=1.705+\frac{40}{112}\cdot\frac{72}{112}\,(3.125-0.917)^2=1.705+0.3571\times0.6429\times4.876=1.705+1.120=2.825.$$

The excess over the mean, $1.12$, is the between-regime term. The sample confirms the mechanism.
Its own split $(n-1)s^2=\sum_j(n_j-1)s_j^2+\sum_jn_j(\bar y_j-\bar y)^2$ is
$301.3=175.9+125.4$, and the **between** part alone, $125.4/111=1.13$, is what pushes $s^2$ from
about 1.6 up to 2.714.

**Observed against fitted frequencies (slide 15).** Under Poisson(1.705) the share of zero years
is $e^{-1.705}=0.182$; the data have $33/112=0.295$. The share of years with four or more is 0.094
under the model, against $20/112=0.179$ in the data. **Too few zeros and too few large counts is
the signature of a mixture of two rates.** The two separate fits have no such gap.

**Relative likelihoods (slide 16).** $L(\lambda)/L(\hat\lambda)=(\lambda/\hat\lambda)^{s_n}e^{-n(\lambda-\hat\lambda)}$
from [[L01-02-poisson-mle-properties]] (5). Evaluate each part's relative likelihood at the
full-period $\hat\lambda=1.705$. For 1851–1890:

$$\log\frac{L_1(1.705)}{L_1(3.125)}=125\log\frac{1.705}{3.125}-40(1.705-3.125)=125(-0.6057)+56.79=-18.92,$$

a ratio of $6\times10^{-9}$. For 1891–1962 the same computation gives $-15.81$ ($1.4\times10^{-7}$).
**The full-period likelihood sits in between, supported by neither** (slide 16).

---

## 4 · C — the two-regime model and its profile likelihood (slide 17; B §3.4)

$$y_t\mid\lambda_1,\lambda_2,\tau\ \sim\ \begin{cases}\text{Poisson}(\lambda_1),& t=1851,\dots,\tau,\\ \text{Poisson}(\lambda_2),& t=\tau+1,\dots,1962.\end{cases}\tag{3}$$

The log-likelihood is the sum of two Poisson log-likelihoods
([[L01-02-poisson-mle-properties]] (7)), one per segment:

$$\ell(\lambda_1,\lambda_2,\tau)=s_1\log\lambda_1-n_1\lambda_1+s_2\log\lambda_2-n_2\lambda_2-\sum_t\log y_t!\tag{4}$$

where $(n_j,s_j)$ depend on $\tau$. **Step 1: fix $\tau$ and maximise over the rates.** (4) separates,
so each rate solves its own likelihood equation:

$$\frac{\partial\ell}{\partial\lambda_j}=\frac{s_j}{\lambda_j}-n_j=0\quad\Longrightarrow\quad\hat\lambda_j(\tau)=\frac{s_j}{n_j},\qquad j=1,2.\tag{5}$$

**Step 2: substitute (5) back into (4).** This is Bolfarine's *verossimilhança perfilada*
$g(\theta_2;x)=l(\hat\theta_1(\theta_2),\theta_2;x)$ (p. 47), with $\theta_2=\tau$ and
$\theta_1=(\lambda_1,\lambda_2)$:

$$\ell_p(\tau)=s_1\log\hat\lambda_1-n_1\Big(\frac{s_1}{n_1}\Big)+s_2\log\hat\lambda_2-n_2\Big(\frac{s_2}{n_2}\Big)+\text{const}=s_1\log\hat\lambda_1-s_1+s_2\log\hat\lambda_2-s_2+\text{const}.\tag{6}$$

Since $s_1+s_2=191$ for every $\tau$, the $-s_j$ terms add to the constant $-191$. Only
$s_1\log\hat\lambda_1+s_2\log\hat\lambda_2$ moves with $\tau$. The slide writes (6) as
$s_1\log\hat\lambda_1-n_1\hat\lambda_1+s_2\log\hat\lambda_2-n_2\hat\lambda_2$ (+ const.), which is
the same expression. A segment with $s_j=0$ uses $0\log0=0$.

**Step 3: normalise over a window** $W$ of candidate cuts. The slide uses
$W=\{1885,\dots,1895\}$, "5 years on each side of 1890":

$$w(\tau)=\frac{e^{\ell_p(\tau)}}{\sum_{\tau'\in W}e^{\ell_p(\tau')}}.\tag{7}$$

> **What $w(\tau)$ is (slide 17).** It is the posterior of $\tau$ under a **uniform prior on $\tau$**
> when $(\lambda_1,\lambda_2)$ are **profiled out** (plugged in at their MLEs) rather than
> **integrated out**. §8 shows the integrated version.

---

## 5 · Worked — the cut points around 1890 (slide 18)

**One row in full, $\tau=1891$.** $n_1=41$, $s_1=127$ (the first 41 years); $n_2=71$,
$s_2=191-127=64$. By (5), $\hat\lambda_1=127/41=3.0976$ and $\hat\lambda_2=64/71=0.9014$, with
ratio $3.436$. By (6), dropping the constant:

$$\ell_p(1891)=127\log3.0976-127+64\log0.9014-64=127(1.13062)-127+64(-0.10380)-64$$

$$=143.588-127-6.643-64=-54.055.$$

This is the maximum over all $\tau$, so $\ell_p(1891)-\max=0.00$. Every other row is computed the
same way. All are reproduced to three decimals in [[L01-11-python]]:

| $\tau$ | $n_1/n_2$ | $\hat\lambda_1$ | $\hat\lambda_2$ | $\hat\lambda_1/\hat\lambda_2$ | $\ell_p(\tau)-\max$ | $w(\tau)$ |
|---|---|---|---|---|---|---|
| 1885 | 35/77 | 3.229 | 1.013 | 3.187 | −3.50 | 0.008 |
| 1886 | 36/76 | 3.250 | 0.974 | 3.338 | −1.02 | 0.091 |
| 1887 | 37/75 | 3.216 | 0.960 | 3.350 | −0.87 | 0.105 |
| 1888 | 38/74 | 3.158 | 0.959 | 3.291 | −1.89 | 0.038 |
| 1889 | 39/73 | 3.154 | 0.932 | 3.386 | −0.49 | 0.154 |
| 1890 | 40/72 | 3.125 | 0.917 | 3.409 | −0.26 | 0.194 |
| **1891** | **41/71** | **3.098** | **0.901** | **3.436** | **0.00** | **0.251** |
| 1892 | 42/70 | 3.048 | 0.900 | 3.386 | −0.94 | 0.098 |
| 1893 | 43/69 | 3.000 | 0.899 | 3.339 | −1.86 | 0.039 |
| 1894 | 44/68 | 2.955 | 0.897 | 3.294 | −2.74 | 0.016 |
| 1895 | 45/67 | 2.911 | 0.896 | 3.251 | −3.59 | 0.007 |

**$w(\tau)$, arithmetic.** (7) needs only the differences $d_\tau=\ell_p(\tau)-\max$:
$w(\tau)=e^{d_\tau}/\sum_{\tau'}e^{d_{\tau'}}$. The sum is
$e^{-3.50}+e^{-1.02}+\dots+e^{-3.59}=0.030+0.362+0.420+0.150+0.613+0.772+1+0.389+0.156+0.065+0.028=3.985$
(terms from the unrounded gaps; exponentiating the rounded gaps shown gives 3.983),
so $w(1891)=1/3.985=0.251$ and $w(1890)=0.772/3.985=0.194$.

![Left: profile log-likelihood of the cut year minus its maximum, for every cut from 1851 to 1961, rising from about -34 to a peak of 0 at 1891 and falling again, with a dashed horizontal line at -34.99 for the single-rate model (LR = 70.0) and the 1885-1895 window shaded. Right: bars of the normalised likelihood w(tau) for 1885 to 1895, highest at 1891 with 0.251, then 1890 at 0.194 and 1889 at 0.154.](figures/L01-coal-profile-likelihood.png)
*Profile log-likelihood (6) over all admissible cuts (left) and $w(\tau)$ from (7) over the slide's window (right). Source: slides 18–19.*

The profile is high and **bumpy** around 1885–1895. Its local dips match single years: a cut
just after a year with 0 or 3+ disasters assigns that year to the "wrong" regime, and the profile
pays for it (slide 20). Far from the peak it falls 20–35 log-units. The dashed line, the
single-rate fit, lies **below every two-regime cut**. That is unavoidable: one rate is the special
case $\lambda_1=\lambda_2$ of (3), so it can never fit better.

> **What the data can and cannot say (slides 19–20).** The maximum is at $\tau=1891$ with weight
> 0.251. The years 1889–1892 together carry
> $0.154+0.194+0.251+0.098=\mathbf{0.696}$. **The data locate the change around 1890 but cannot
> pin down the exact year.** Across all eleven cuts the rates barely move ($\hat\lambda_1\approx3$,
> $\hat\lambda_2\approx0.9$): **the rate fell by a factor of about 3.4.**

---

## 6 · C — the likelihood-ratio statistic (slide 19; B §6.5)

**The single-rate fit.** With $\hat\lambda=191/112=1.70536$ and the same constant as (6):

$$\ell(\hat\lambda)=191\log1.70536-191=191(0.53377)-191=101.951-191=-89.049.$$

**The statistic.** Twice the gap between the two maximised log-likelihoods:

$$\text{LR}=2\{\ell_p(1891)-\ell(\hat\lambda)\}=2\{-54.055-(-89.049)\}=2\times34.994=69.99\approx\mathbf{70.0}.\tag{8}$$

**A compact form.** Write both fits with (6). The $-s_j$ terms and the single-rate $-191$ cancel,
because $s_1+s_2=191$:

$$\text{LR}=2\Big[s_1\log\frac{\hat\lambda_1}{\hat\lambda}+s_2\log\frac{\hat\lambda_2}{\hat\lambda}\Big]=2\big[143.588-6.643-101.951\big]=69.99.\tag{9}$$

(9) is the two-sample version of Bolfarine's Poisson GLRT (Ex. 6.5.5, p. 108), where the
null value is fixed instead of estimated:
$-2\log\lambda(x)=-2[-n(\lambda_0-\bar x)+\sum x_i\log(\lambda_0/\bar x)]$.

**In Bolfarine's terms** (6.5.1), p. 103, the GLRT statistic is
$\lambda(x)=\sup_{\Theta_0}L/\sup_\Theta L$, and LR $=-2\log\lambda(x)$ with
$\Theta_0=\{\lambda_1=\lambda_2\}$. **Wilks** (Thm 6.5.1, p. 108) says that under regularity
$-2\log\lambda(X)\to\chi^2$, with degrees of freedom equal to the difference in free parameters.

> **Why 70.0 is not referred to $\chi^2_1$.** Wilks needs a regular problem. Here:
> (i) the cut $\tau$ was **chosen to maximise** the statistic over about 111 candidates, so 70.0 is a
> *maximum* of LR statistics, not one of them; (ii) under $H_0$ ($\lambda_1=\lambda_2$) the cut
> $\tau$ **is not identified**, since every $\tau$ gives the same likelihood; (iii) $\tau$ is
> discrete. No standard $\chi^2$ count of parameters applies. **It does not matter here.** Had
> 1890 been fixed in advance (LR 69.47 at $\tau=1890$), $\chi^2_1$ would be legitimate and
> $p\approx8\times10^{-17}$. Even a $\chi^2_2$ tail at 70.0 is $6\times10^{-16}$. The evidence is
> overwhelming on any reading.

> **Interactive companion.** [The Change-Point Dial](companions/companion-poisson-change-point.html):
> drag the **cut year** $\tau$ and watch the two rate lines, the profile curve's marker and the
> **LR read-out** (70.0 at $\tau=1891$; it is not referred to $\chi^2_1$). Change the **weight
> window** $h$ to see $w(1891)$ move from 0.251 at the slide's $h=5$. At $\tau=1890$ the
> per-segment dispersion read-outs reproduce §2's p-values, 0.774 and 0.168: each part is
> consistent with a Poisson.

---

## 7 · C — what the slides conclude (slides 20–21)

1. **For iid Poisson data**, $\hat\lambda_{MLE}=\bar y$ is sufficient-based, unbiased, consistent and
   efficient ([[L01-02-poisson-mle-properties]]).
2. **A single Poisson does not fit the coal-mining series.** Overdispersion (§3) is the symptom
   of a change in rate.
3. **Splitting gives two well-fitting Poissons**, $\hat\lambda_1\approx3.1$ and
   $\hat\lambda_2\approx0.9$, and the profile likelihood points to a change around 1890–1891.
4. **Next step** (deck's last bullet): a Bayesian change-point model $p(\tau,\lambda_1,\lambda_2\mid y)$
   that **integrates rather than profiles** the rates.

---

## 8 · G — profiling against integrating (forward link to Classes 3+4)

**The model on the slide's last bullet** is Greenberg's switch-point model (§7.1.1, pp. 93–94):
$p(y_i)$ is Poisson($\theta_1$) for $i\le k$ and Poisson($\theta_2$) after, as in his (7.3), with
priors $\theta_1\sim G(\alpha_{10},\beta_{10})$, $\theta_2\sim G(\alpha_{20},\beta_{20})$ and
$\pi(k=j)=1/n$, as in his (7.4). There it is sampled by Gibbs. That belongs to Classes 3+4 and is
**not developed here**.

**The integrated likelihood of $\tau$ in closed form.** Use [[L01-04-first-bayesian-poisson]]'s
prior, $\lambda_j\sim$ Exp$(a)$ independently, and that note's Gamma integral (2). For each
segment,

$$\int_0^\infty\lambda^{s_j}e^{-n_j\lambda}\cdot ae^{-a\lambda}\,d\lambda=a\int_0^\infty\lambda^{s_j}e^{-(n_j+a)\lambda}d\lambda=\frac{a\,\Gamma(s_j+1)}{(n_j+a)^{s_j+1}},$$

so, with a uniform prior on $\tau$,

$$p(\tau\mid y)\ \propto\ \prod_{j=1}^2\frac{a\,\Gamma(s_j+1)}{(n_j+a)^{s_j+1}}.\tag{10}$$

Profiling keeps the **height** of each segment's likelihood at its peak. Integrating keeps its
**area**: roughly height times width, where the width is about $\sqrt{2\pi\hat\lambda_j/n_j}$ and
is weighted by the prior. **On the coal data with $a=1/2$ the two give the same answer.** (10)
normalised over 1885–1895 gives 0.008, 0.089, 0.104, 0.038, 0.153, 0.194, **0.251**, 0.099, 0.040,
0.017, 0.007, against the table's $w(\tau)$. Both segments are long, and the width factor hardly
changes across the window. The two routes part ways when a segment is short or the prior is
informative, which is when the uncertainty about a rate is itself large. That uncertainty is
exactly what profiling ignores.

---

## Links

- Prev: the MLE properties used in every column of §2, [[L01-02-poisson-mle-properties]]. Next:
  the first prior on $\lambda$ (1851–1891 data), [[L01-04-first-bayesian-poisson]]. Formulas:
  [[L01-09-formulas]]; pitfalls (profile ≠ posterior, searched LR ≠ $\chi^2_1$):
  [[L01-10-pitfalls]]; code: [[L01-11-python]].
- Class 2: letting the rate depend on covariates (Poisson regression, mean–variance check),
  [[../L02/L02-06-gaussian-vs-poisson-regression|L02 §6]].
- Rules: [[../../rules/08_monte_carlo_mcmc|rules/08]] (Gibbs, for the Bayesian version);
  [[../../rules/07_bayes|rules/07]]; scope [[../../rules/09_course_program|rules/09]].
- Companion: [The Change-Point Dial](companions/companion-poisson-change-point.html).
- Data provenance: `.agent/notes/coal-mining-data.md`; the site's R page `Aula/class-01/materials/class1-poisson.html` (1851–1891 only).
- Reading: B §3.4 (pp. 46–49, profile likelihood), §6.5 (pp. 103–114, GLRT and Wilks);
  G §7.1.1 (pp. 91–95, switch-point model).
- Practice (statements in the books; see [[../../Map/exercises-index]]): **B 6.11** (p. 116,
  approximate GLRT for equal Poisson means of two samples, the fixed-cut version of (9));
  **G 7.3** (p. 106, Gibbs for the coal switch point, a preview of Classes 3+4).
