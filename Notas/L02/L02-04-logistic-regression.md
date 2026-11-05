---
tags: [notes, lecture-02, logistic-regression, glm, maximum-likelihood, irls, odds-ratio, confusion-matrix]
date: 2026-10-19
status: taught
source: "logisticregression-discriminantanalysis.pdf (Lopes & Marques), logistic part, slides 4–38; graduate-school-admission.txt + graduate-school-admission.pdf (7 pages of R output); I §4.3 (pp. 139–144: eqs. 4.1–4.9, Tables 4.1–4.3, Fig. 4.3), §4.4.2 confusion-matrix vocabulary (pp. 152–156, Tables 4.4–4.7); W §17.1 (pp. 525–531: eqs. 17.2–17.3, 17.7, 17.10–17.12, McFadden pseudo-R² p. 531); AME §7.4 (pp. 138–139, Tabela 7.1), §8.1.2 (pp. 142–143)"
---

# Logistic part, slides 4–38 · The logit model, its MLE by IRLS, and what the `default` and spam outputs actually say

> **Claim.** A binary $y$ is Bernoulli with an individual probability $\pi_i$, and logistic
> regression makes the **log-odds** $\log\{\pi_i/(1-\pi_i)\}$ linear in $x_i$. The log-likelihood
> is concave, its score is $X'(y-\pi)$, its Hessian is $-X'WX$, and **one Newton–Raphson step
> is one weighted least-squares fit** on an adjusted response $z$ (IRLS). Coefficients are read
> as **odds ratios** $e^{\beta_j}$, a probability cut-off $c$ maps to a covariate cut-off
> $x^*=(\operatorname{logit}c-\beta_0)/\beta_1$, and a classifier is judged by its **confusion
> matrix**, not by one error rate. Six slips in the deck (slides 9, 10, 15, 18, 22 and 38) are corrected below, each where it arises, plus a reversed comment in the admission script (§10).
> Prev: [[L02-03-cross-validation-motorcycle]] · Next: [[L02-05-discriminant-analysis]] · Map: [[L02-00-map]]

**Notation.**

- $y_i\in\{0,1\}$: response of individual $i=1,\dots,n$ (1 = "yes", default, spam, admitted).
- $x_i=(1,x_{i1},\dots,x_{ip})'$: covariates with a leading 1; $X$ the $n\times(p+1)$ matrix with rows $x_i'$.
- $\beta=(\beta_0,\dots,\beta_p)'$: coefficients; $\eta_i=x_i'\beta$ the **linear predictor**, $\eta_i\in\mathbb R$.
- $\pi_i=P(y_i=1\mid x_i)\in(0,1)$; the deck also writes it $g(x_i'\beta)$ and, on slide 9, $p$.
- $g(\mu)=e^\mu/(1+e^\mu)$: logistic function (W writes $\Lambda$, eq. 17.3); $g^{-1}(\pi)=\log\{\pi/(1-\pi)\}=\operatorname{logit}\pi$.
- $\ell(\beta)$: log-likelihood; $W=\operatorname{diag}\{\pi_i(1-\pi_i)\}$: the weight matrix; $z$: IRLS adjusted response.
- $c\in(0,1)$: probability cut-off of a classifier; $x^*$: the covariate value where $\hat\pi=c$.
- TN, FP, FN, TP: confusion-matrix counts (true negative, false positive, false negative, true positive).

---

## 1 · U — why a straight line fails on a 0/1 response

The `default` data (ISLR, $n=10{,}000$; slide 4) has 9,667 non-defaulters and 333 defaulters
(slide 12). Regressing the 0/1 indicator on `balance` by OLS — the **linear probability model**
(I eq. 4.1, p. 139; W §17.1, p. 525) — gives (slide 13)

$$\hat\pi^{LM}(x)=-0.07519+0.0001299\,x .$$

It crosses zero at $x=0.07519/0.0001299=578.8$, so **every customer with a balance under
USD 579 gets a negative "probability"**, and at $x=2000$ it says $-0.07519+0.2598=0.185$ where
the logit says 0.586 (§5.1). W's two complaints (p. 525) are exactly these: fitted values outside
$[0,1]$ and a **constant** partial effect. The fix is to model a transformation of $\pi$ that is
free to range over $\mathbb R$.

![Left: logistic curve for P(default | balance) with coefficients -10.6513 and 0.0055 against the OLS line, marked at balance 1000 (0.58%), 2000 (58.6%) and the 50% cut-off 1936.6; right: balance-plus-student logit curves for students and non-students with 50% cut-offs at 1998 and 1873 and the 1500-balance probabilities 5.4% and 10.5%](figures/L02-logistic-default.png)
*Left: the fitted logit (slides 13, 15) never leaves $[0,1]$; the LM line is negative below 578.8. Right: adding `student` shifts the curve, not its shape (slide 20). Curves drawn from the printed coefficients only — the data are not on disk.*

The logit is flat near 0 for balances below about 1,000, rises steepest where $\hat\pi=1/2$, and
saturates near 1; the straight line cannot bend, so it is too high at small balances, too low at
large ones, and wrong in sign at the left end. On the right the two curves are horizontal
translates of each other — the dummy moves the intercept, which is all a dummy can do in a
logit without interactions.

---

## 2 · C — the model: logistic function, odds, logit (slides 5–6)

**Model (slide 5; I eq. 4.2, p. 139; W eq. 17.2–17.3, pp. 525–526).**

$$\pi_i=P(y_i=1\mid x_i)=\frac{\exp\{x_i'\beta\}}{1+\exp\{x_i'\beta\}}=g(x_i'\beta).\tag{1}$$

**From (1) to the log-odds, one step at a time.** Write $\eta_i=x_i'\beta$.

$$1-\pi_i=1-\frac{e^{\eta_i}}{1+e^{\eta_i}}=\frac{1+e^{\eta_i}-e^{\eta_i}}{1+e^{\eta_i}}=\frac{1}{1+e^{\eta_i}}.\tag{2}$$

Dividing (1) by (2):

$$\frac{\pi_i}{1-\pi_i}=\frac{e^{\eta_i}/(1+e^{\eta_i})}{1/(1+e^{\eta_i})}=e^{\eta_i}\qquad\text{(the odds; I eq. 4.3, p. 140)}.\tag{3}$$

Taking logs of (3):

$$\log\frac{\pi_i}{1-\pi_i}=x_i'\beta\qquad\text{(the log-odds or logit; I eq. 4.4, p. 140)}.\tag{4}$$

**The GLM reading (slide 6).** $y_i\sim\text{Bernoulli}(\pi_i)$ with

$$E(y_i\mid x_i)=\pi_i=g(x_i'\beta),\qquad V(y_i\mid x_i)=\pi_i(1-\pi_i),\tag{5}$$

and $g^{-1}=\operatorname{logit}$ is the **link**: it maps the mean to the scale on which the model is
linear. Note 06 uses the same template with a log link ([[L02-06-gaussian-vs-poisson-regression]] §6).

### 2.1 · C — reading a coefficient: odds ratio and partial effect

Raise $x_j$ by one unit, everything else fixed. From (3) the odds go from $e^{\eta}$ to
$e^{\eta+\beta_j}$, so

$$\frac{\text{odds}(x_j+1)}{\text{odds}(x_j)}=\frac{e^{\eta+\beta_j}}{e^{\eta}}=e^{\beta_j}\qquad\text{(odds ratio; I p. 140)}.\tag{6}$$

The effect on the **probability** is not constant. Differentiate (1) with the quotient rule:

$$\frac{d g}{d\eta}=\frac{e^\eta(1+e^\eta)-e^\eta e^\eta}{(1+e^\eta)^2}=\frac{e^\eta}{(1+e^\eta)^2}=g(\eta)\,\{1-g(\eta)\},\tag{7}$$

so by the chain rule

$$\frac{\partial\pi_i}{\partial x_{ij}}=\beta_j\,\pi_i(1-\pi_i)\le\frac{\beta_j}{4},\tag{8}$$

with the maximum $\beta_j/4$ at $\pi_i=1/2$ (W eq. 17.7, p. 527: partial effect $g(\beta_0+x\beta)\beta_j$, and for the logit $g(0)=0.25$).

**Worked, `default` (slide 15: $\hat\beta_1=0.0055$ per USD of balance).**

| Quantity | Substitution | Value |
|---|---|---|
| odds ratio per USD 1 | $e^{0.0055}$ | 1.0055 |
| odds ratio per USD 100 | $e^{0.0055\times100}=e^{0.55}$ | **1.733** (+73%) |
| $\partial\pi/\partial x$ at the 50% cut-off | $0.0055\times0.5\times0.5$ | 0.001375 per USD = 13.75 pp per USD 100 |
| $\partial\pi/\partial x$ at $x=1000$ ($\hat\pi=0.005759$) | $0.0055\times0.005759\times0.994241$ | 0.0000315 per USD = 0.31 pp per USD 100 |

> **The odds ratio is the same everywhere; the probability effect is 44 times larger at the cut-off
> than at a balance of 1,000.** "A one-unit increase in balance raises the log-odds by 0.0055"
> (I Table 4.1 caption, p. 142) is exact; "raises the probability by 0.0055" is wrong.

---

## 3 · C — likelihood, score and Hessian (slides 7–8)

**Likelihood (slide 7; I eq. 4.5, p. 141; W eq. 17.10, p. 528).** Independent Bernoulli draws:

$$p(y_{1:n}\mid x_{1:n},\beta)=\prod_{i=1}^n\pi_i^{\,y_i}(1-\pi_i)^{1-y_i}=\prod_{i:y_i=1}\pi_i\prod_{i:y_i=0}(1-\pi_i).\tag{9}$$

This is the Bernoulli likelihood of [[../L01/L01-01-likelihood-sampling-rules|L01 §1]] with one
change: $\theta$ is no longer common, each $\pi_i$ is tied to $x_i$ through (1).

**Log-likelihood (W eq. 17.11).**

$$\ell(\beta)=\sum_{i=1}^n\big[y_i\log\pi_i+(1-y_i)\log(1-\pi_i)\big].\tag{10}$$

**Rewrite each term in $\eta_i$.** Group the $y_i$ terms:

$$y_i\log\pi_i+(1-y_i)\log(1-\pi_i)=y_i\log\frac{\pi_i}{1-\pi_i}+\log(1-\pi_i).$$

Substitute (4) for the log-odds and (2) for $1-\pi_i$:

$$\ell(\beta)=\sum_{i=1}^n\Big[y_i\,(x_i'\beta)+\log\frac{1}{1+e^{x_i'\beta}}\Big]=\sum_{i=1}^n\big[y_i\,x_i'\beta-\log(1+e^{x_i'\beta})\big].\tag{11}$$

**Score (slide 8).** Differentiate (11); the derivative of $\log(1+e^{\eta})$ is $e^\eta/(1+e^\eta)=\pi$:

$$\frac{\partial\ell}{\partial\beta}=\sum_{i=1}^n\big[y_i\,x_i-\pi_i\,x_i\big]=\sum_{i=1}^n x_i\,(y_i-\pi_i)=X'(y-\pi).\tag{12}$$

Setting (12) to zero gives $p+1$ equations, **nonlinear in $\beta$** because $\pi_i$ is.

**Hessian (slide 8).** Differentiate (12) once more; only $\pi_i$ depends on $\beta$, and by (7)
$\partial\pi_i/\partial\beta'=\pi_i(1-\pi_i)\,x_i'$:

$$\frac{\partial^2\ell}{\partial\beta\,\partial\beta'}=-\sum_{i=1}^n x_i\,x_i'\,\pi_i(1-\pi_i)=-X'WX,\qquad W=\operatorname{diag}\{\pi_i(1-\pi_i)\}.\tag{13}$$

**Two consequences.**

1. Every $\pi_i(1-\pi_i)>0$, so $X'WX$ is positive definite when $X$ has full column rank: $\ell$ is
   **strictly concave**, and a stationary point is the unique maximum. *(G: if some linear
   combination of $x$ separates the 0s from the 1s perfectly, $\ell$ keeps rising as
   $\|\beta\|\to\infty$ and no finite MLE exists — the "unstable when classes are well-separated"
   bullet on slide 40.)*
2. The first row of (12) at $\hat\beta$ (the intercept's column of ones) reads
   $\sum_i(y_i-\hat\pi_i)=0$: **the average fitted probability equals the sample share of 1s** —
   0.0333 in `default` (I p. 140).

---

## 4 · C — Newton–Raphson is iteratively reweighted least squares (slides 8–9)

**Newton–Raphson (slide 8).** Starting from $\beta^{\text{old}}$,

$$\beta^{\text{new}}=\beta^{\text{old}}-\Big(\frac{\partial^2\ell}{\partial\beta\,\partial\beta'}\Big)^{-1}\frac{\partial\ell}{\partial\beta},\tag{14}$$

both derivatives evaluated at $\beta^{\text{old}}$.

**Substitute (12) and (13) into (14):**

$$\beta^{\text{new}}=\beta^{\text{old}}-\big(-X'WX\big)^{-1}X'(y-\pi)=\beta^{\text{old}}+(X'WX)^{-1}X'(y-\pi).\tag{15}$$

**Factor $(X'WX)^{-1}$ out of both terms** (write $\beta^{\text{old}}=(X'WX)^{-1}X'WX\beta^{\text{old}}$):

$$\beta^{\text{new}}=(X'WX)^{-1}\big[X'WX\beta^{\text{old}}+X'(y-\pi)\big].$$

**Insert $WW^{-1}=I$ in front of $(y-\pi)$** ($W$ is diagonal with positive entries):

$$\beta^{\text{new}}=(X'WX)^{-1}X'W\big[X\beta^{\text{old}}+W^{-1}(y-\pi)\big]=(X'WX)^{-1}X'Wz,\tag{16}$$

$$z=X\beta^{\text{old}}+W^{-1}(y-\pi),\qquad z_i=\eta_i^{\text{old}}+\frac{y_i-\pi_i}{\pi_i(1-\pi_i)}.\tag{17}$$

(16) is the **weighted least-squares** estimator of a regression of $z$ on $X$ with weights $W$, i.e.

$$\beta^{\text{new}}=\arg\min_\beta\,(z-X\beta)'W(z-X\beta),\tag{18}$$

whose normal equations $X'W(z-X\beta)=0$ give (16). **Slide 9 prints the objective as
$(z-X\beta)'(z-X\beta)$; the weight matrix is needed** — without it the minimiser is
$(X'X)^{-1}X'z$, not (16). Recompute $\pi$ and $W$ at $\beta^{\text{new}}$ and repeat: weights are
"re-weighted" each pass, hence IRLS (R's `glm` reports "Fisher scoring iterations"; for the logit
link Fisher scoring and Newton–Raphson coincide because (13) does not depend on $y$).

**Standard errors** come from the same matrix at convergence: $\widehat{\operatorname{Var}}(\hat\beta)=(X'\hat WX)^{-1}$,
the inverse observed information — the "Std. Error" column of every `glm` printout below, and the
$z$-statistic is $\hat\beta_j/\text{SE}$ (I p. 141; W p. 529).

### 4.1 · Worked — IRLS by hand on the `student` table (slide 18)

The slide prints the full $2\times2$ table, so this fit **can be reproduced exactly** (it is the
only `default` model whose data are fully on the page):

| default \ student | No | Yes | Total |
|---|---|---|---|
| No | 6850 | 2817 | 9667 |
| Yes | 206 | 127 | 333 |
| Total | 7056 | 2944 | 10000 |

Model: $\eta_i=\beta_0+\beta_1 s_i$, $s_i=1$ for a student.

**Iteration 1 from $\beta=(0,0)$.** Every $\pi_i=g(0)=0.5$, every weight $0.5\times0.5=0.25$, and (17) gives

$$z_i=0+\frac{y_i-0.5}{0.25}=4y_i-2 .$$

With a constant $W=0.25I$, (16) collapses to OLS of $z$ on a dummy, i.e. **group means of $z$**:

$$\beta_0^{(1)}=4\cdot\frac{206}{7056}-2=4(0.029195)-2=-1.88322,$$
$$\beta_0^{(1)}+\beta_1^{(1)}=4\cdot\frac{127}{2944}-2=4(0.043139)-2=-1.82745\ \Rightarrow\ \beta_1^{(1)}=0.05577.$$

**Subsequent iterations** (computed in Python, `L02-09`):

| iteration | $\beta_0$ | $\beta_1$ | $-2\ell$ |
|---|---|---|---|
| 1 | −1.88322 | 0.05577 | 4116.20 |
| 2 | −2.78054 | 0.15372 | 3072.81 |
| 3 | −3.31150 | 0.29836 | 2917.50 |
| 4 | −3.48780 | 0.39184 | 2908.74 |
| 5 | −3.50400 | 0.40477 | 2908.683 |
| 6 | **−3.50413** | **0.40489** | **2908.683** |

**The limit in closed form.** With one dummy, the two score equations (12) split by group:
$\sum_{s_i=0}(y_i-\pi_0)=0$ and $\sum_{s_i=1}(y_i-\pi_1)=0$, so $\hat\pi_0=206/7056$ and
$\hat\pi_1=127/2944$ — the group shares. Then by (4) and (6):

$$\hat\beta_0=\log\frac{206}{6850}=-3.50413,\qquad \hat\beta_1=\log\frac{127/2817}{206/6850}=\log1.49913=0.40489 .$$

**Standard errors** from $(X'\hat WX)^{-1}$ reduce to sums of reciprocal cell counts:

$$\text{SE}(\hat\beta_0)=\sqrt{\tfrac1{206}+\tfrac1{6850}}=0.07071,\qquad \text{SE}(\hat\beta_1)=\sqrt{\tfrac1{206}+\tfrac1{6850}+\tfrac1{127}+\tfrac1{2817}}=0.11502,$$

exactly the slide's 0.07071 and 0.11502; and $-2\ell(\hat\beta)=2908.7$ is the slide's residual deviance (§7).

> **The deck's two probabilities on slide 18 are off by a factor of ten.** It prints
> $\hat P(y=1\mid\text{student})=0.43\%$ and $0.29\%$; the fitted values are $127/2944=0.0431=$
> **4.31%** and $206/7056=0.0292=$ **2.92%**, as I prints (p. 142). The odds ratio
> $e^{0.40489}=1.499$: alone, being a student multiplies the odds of default by 1.5.

---

## 5 · C — the `default` outputs, read (slides 13, 15, 17, 18, 20, 22)

| Model (slide) | $\hat\beta_0$ | $\hat\beta$ balance | $\hat\beta$ student | Resid. dev. (df) | AIC |
|---|---|---|---|---|---|
| balance (13) | −10.65 (SE 0.3612) | 0.005499 (SE 0.0002204) | — | 1596.5 (9998) | 1600.5 |
| student (18) | −3.50413 (0.07071) | — | 0.40489 (0.11502) | 2908.7 (9998) | 2912.7 |
| balance + student (20) | −10.75 (0.3692) | 0.005738 (0.0002318) | −0.7149 (0.1475) | 1571.7 (9997) | 1577.7 |

Null deviance 2920.6 on 9999 df in all three. AIC = deviance + 2(number of coefficients):
$1596.5+4=1600.5$, $2908.7+4=2912.7$, $1571.7+6=1577.7$. $z$-values: $-10.65/0.3612=-29.49$,
$0.005499/0.0002204=24.95$, as printed.

### 5.1 · Balance only: plug-in probabilities (slide 15; I p. 142)

**At $x=1000$.** Linear predictor, then (1):

$$\hat\eta=-10.6513+0.0055(1000)=-10.6513+5.5=-5.1513,$$
$$\hat\pi=\frac{e^{-5.1513}}{1+e^{-5.1513}}=\frac{0.005792}{1.005792}=0.005759=\mathbf{0.58\%}.$$

**At $x=2000$.**

$$\hat\eta=-10.6513+0.0055(2000)=-10.6513+11=0.3487,$$
$$\hat\pi=\frac{e^{0.3487}}{1+e^{0.3487}}=\frac{1.41722}{2.41722}=0.5863=\mathbf{58.6\%}.$$

(Slide 15's second line keeps the label "$x=1000$"; the arithmetic is for 2000.)

### 5.2 · From a probability cut-off to a balance cut-off (slide 17)

Classify "yes" when $\hat\pi(x)\ge c$. Since $g$ is increasing, $\hat\pi(x)\ge c\iff\hat\eta(x)\ge\operatorname{logit}c$; set equality and solve:

$$\hat\beta_0+\hat\beta_1x^*=\operatorname{logit}c\quad\Longrightarrow\quad x^*=\frac{\operatorname{logit}c-\hat\beta_0}{\hat\beta_1}.\tag{19}$$

**At $c=0.5$**, $\operatorname{logit}0.5=\log1=0$:

$$x^*=\frac{0-(-10.6513)}{0.0055}=\frac{10.6513}{0.0055}=1936.6 .$$

The whole axis of slide 17, recomputed from (19):

| $c$ | $\operatorname{logit}c$ | $x^*$ with $\hat\beta_1=0.0055$ | $x^*$ with $\hat\beta_1=0.005499$ | slide label |
|---|---|---|---|---|
| 0.1 | −2.1972 | 1537.1 | 1537.4 | 1537 |
| 0.2 | −1.3863 | 1684.5 | 1684.9 | 1684 |
| 0.3 | −0.8473 | 1782.5 | 1782.9 | 1782 |
| 0.4 | −0.4055 | 1862.9 | 1863.2 | 1863 |
| **0.5** | **0** | **1936.6** | **1937.0** | **1936** |
| 0.6 | 0.4055 | 2010.3 | 2010.7 | 2010 |
| 0.7 | 0.8473 | 2090.7 | 2091.0 | 2091 |
| 0.8 | 1.3863 | 2188.7 | 2189.1 | 2189 |
| 0.9 | 2.1972 | 2336.1 | 2336.5 | 2336 |

The labels are the unrounded-slope column truncated to the dollar. **A classifier on one
covariate is a threshold on that covariate**; moving $c$ (note 05 §10) just slides $x^*$.

### 5.3 · Balance + student, and confounding (slides 19–22; I §4.3.4, pp. 142–144)

**At balance 1500.** For a student ($s=1$):

$$\hat\eta=-10.75+0.005738(1500)-0.7149(1)=-10.75+8.607-0.7149=-2.8579,$$
$$\hat\pi=\frac{e^{-2.8579}}{1+e^{-2.8579}}=\frac{0.057389}{1.057389}=0.0543=\mathbf{5.4\%}.$$

For a non-student ($s=0$):

$$\hat\eta=-10.75+8.607=-2.1430,\qquad\hat\pi=\frac{0.117302}{1.117302}=0.1050=\mathbf{10.5\%}.$$

**50% cut-offs by group**, from (19) with $\hat\beta_0+\hat\beta_2 s$ in place of $\hat\beta_0$:

$$x^*_{\text{student}}=\frac{0-(-10.75-0.7149)}{0.005738}=\frac{11.4649}{0.005738}=\mathbf{1998.1},\qquad x^*_{\text{non-student}}=\frac{10.75}{0.005738}=\mathbf{1873.5}.$$

> **Slide 22 attaches 1873 to students and 1998 to non-students, and its legend colours the
> curves the same way; the printed coefficients say the reverse.** With $\hat\beta_2=-0.7149<0$
> a student needs a *higher* balance to reach 50%. Slide 25 (Bayes fit) draws the non-student curve
> above the student one, consistent with the coefficients.

**Confounding.** Alone, `student` has a **positive** coefficient (0.405: students default more,
§4.1); given `balance` it is **negative** (−0.715; odds ratio $e^{-0.7149}=0.489$, half the odds at
the same balance). Both are right: students carry larger balances (slide 19's boxplots), and
balance drives default. I's version adds `income` (Table 4.3, p. 143, income not significant,
$p=0.71$) and gets 0.058 vs 0.105 at balance 1,500 and income 40,000 (eqs. 4.8–4.9, p. 144) —
the deck drops income and gets 0.054 vs 0.105.

**Likelihood-ratio tests from the printed deviances** (W eq. 17.12, p. 529: $LR=2(\ell_{ur}-\ell_r)$, and
for 0/1 data deviance $=-2\ell$, §7):

| Comparison | $LR$ = difference in deviance | df |
|---|---|---|
| balance vs null | $2920.6-1596.5=1324.1$ | 1 |
| student vs null | $2920.6-2908.7=11.9$ | 1 |
| balance + student vs balance | $1596.5-1571.7=24.8$ | 1 |

All far beyond $\chi^2_{1;0.95}=3.84$. **McFadden's pseudo-$R^2$** (W p. 531),
$1-\ell_{ur}/\ell_0=1-1596.5/2920.6=0.453$ for balance alone, $0.462$ with student, $0.004$ for student alone.

---

## 6 · C — classifying a new individual: plug-in vs posterior predictive (slides 11, 23)

The deck **plugs in** the MLE (slide 11):

$$\hat P(y_{n+1}=1\mid x_{n+1},y_{1:n},x_{1:n})=\frac{\exp\{x_{n+1}'\hat\beta_{MLE}\}}{1+\exp\{x_{n+1}'\hat\beta_{MLE}\}},\tag{20}$$

and classifies "yes" when (20) exceeds $1-$(20), i.e. $c=1/2$. The Bayesian answer (slide 23)
**integrates** over the posterior instead:

$$P(y_{n+1}=1\mid x_{n+1},y_{1:n},x_{1:n})=\int P(y_{n+1}=1\mid x_{n+1},\beta)\,p(\beta\mid y_{1:n},x_{1:n})\,d\beta,\tag{21}$$

and (20) is (21) with all posterior mass at $\hat\beta$. Slides 24–25 show the posterior of
$P(y=1\mid1500,\text{student})$ centred near 0.054 and 0.105 — **name only here; the Bayesian
logit is Classes 3+4** (`Aula/class-03-04/materials/Bayesian-logistic-regression.html`).

---

## 7 · C/G — deviance and residuals (slide 10)

**Pearson residual** $r_i=(y_i-\hat\pi_i)/\sqrt{\hat\pi_i(1-\hat\pi_i)}$; **deviance residual**

$$d_i=\operatorname{sign}(y_i-\hat\pi_i)\sqrt{2\Big[y_i\log\frac{y_i}{\hat\pi_i}+(1-y_i)\log\frac{1-y_i}{1-\hat\pi_i}\Big]}.\tag{22}$$

**For 0/1 data the deviance is $-2\ell(\hat\beta)$.** With $y_i\in\{0,1\}$, $y_i\log y_i=0$ and
$(1-y_i)\log(1-y_i)=0$ (convention $0\log0=0$), so

$$d_i^2=2\big[-y_i\log\hat\pi_i-(1-y_i)\log(1-\hat\pi_i)\big]\quad\Rightarrow\quad D=\sum_i d_i^2=-2\ell(\hat\beta)\ \text{by (10)}.\tag{23}$$

Check on the null model: $\hat\pi=0.0333$ for all, $-2[333\log0.0333+9667\log0.9667]=2920.6$, the
printed null deviance.

**Two slips on slide 10:** the statistics are $\chi^2=\sum r_i^{\,2}$ and $D=\sum d_i^{\,2}$
(squares missing). *G caution:* with one observation per covariate pattern, the
$\chi^2_{n-p}$ reference for $D$ itself is unreliable; **differences** of deviances between nested
models (§5.3) are the safe use.

---

## 8 · G — regularized logistic regression (slides 26–27, 32–35), named only

The penalized objective (slide 26) is $-\ell(\beta)$ from (11) plus the elastic-net penalty:

$$\hat\beta=\arg\min_\beta\Big\{-\sum_{i=1}^n\big(y_ix_i'\beta-\log(1+e^{x_i'\beta})\big)+\lambda\big[(1-\alpha)\|\beta\|_2^2+\alpha\|\beta\|_1\big]\Big\},$$

$\alpha=1$ lasso, $\alpha=0$ ridge, $\lambda$ chosen by CV (`cv.glmnet`; AME §8.1.2, p. 143).
Ridge/lasso/elastic net are **Classes 3+4** material; here they matter only as rows of the spam
table.

---

## 9 · C — the spam confusion matrix (slides 28, 36–38)

**Data.** 4,601 e-mails labelled spam ($y=1$) or ham ($y=0$), 40% spam, 57 word-frequency
predictors (Efron & Hastie 2016, pp. 113–115, cited on slide 28); trained on 2,300, tested on 2,301 (slide 33).

**Vocabulary** (I Tables 4.6–4.7, p. 156; AME Tabela 7.1, p. 138), "positive" = spam:

| | predicted ham ($\hat y=0$) | predicted spam ($\hat y=1$) |
|---|---|---|
| ham ($y=0$) | TN | FP — *a ham sent to the spam folder* |
| spam ($y=1$) | FN — *a spam let through* | TP |

FN rate $=FN/(FN+TP)$ (1 − sensitivity); FP rate $=FP/(FP+TN)$ (1 − specificity, Type I error);
**false discovery rate** $=FP/(FP+TP)$ (1 − precision).

**Worked, the `glm` row** (TN 1325, FP 80, FN 93, TP 803; total 2301; 896 spam in the test set):

| Measure | Substitution | Value |
|---|---|---|
| error rate | $(80+93)/2301=173/2301$ | **7.52%** |
| FN rate | $93/(93+803)=93/896$ | **10.38%** |
| FP rate | $80/(80+1325)=80/1405$ | **5.69%** |
| sensitivity | $803/896$ | 89.62% |
| specificity | $1325/1405$ | 94.31% |
| precision | $803/(803+80)=803/883$ | 90.94% |
| FDR | $80/883$ | **9.06%** |

**All five rows** (error, FN and FP rates match the slide; the last two columns are recomputed):

| Method | TN | FP | FN | TP | error % | FN % | FP % | FDR $=FP/(FP+TP)$ % | slide's "false.discovery" % $=FP/(FP+TP+FN)$ |
|---|---|---|---|---|---|---|---|---|---|
| glm | 1325 | 80 | 93 | 803 | 7.52 | 10.38 | 5.69 | 9.06 | 8.20 |
| ridge | 1345 | 60 | 128 | 768 | 8.17 | 14.29 | 4.27 | 7.25 | 6.28 |
| enet | 1349 | 56 | 94 | 802 | 6.52 | 10.49 | 3.99 | 6.53 | 5.88 |
| lasso | 1347 | 58 | 95 | 801 | 6.65 | 10.60 | 4.13 | 6.75 | 6.08 |
| bayes | 1326 | 79 | 91 | 805 | 7.39 | 10.16 | 5.62 | 8.94 | 8.10 |

> **The slide defines false discoveries as "false positives over positives" but its column divides
> FP by FP + (all actual spam)**: $80/(80+896)=8.20$ reproduces every row. Over *predicted*
> positives (the standard FDR, the slide's own words) the glm figure is 9.06%.

**Reading.** Elastic net has the lowest error (6.52%) and FP rate (3.99%); ridge lets the most
spam through (14.29%). A mail filter cares more about FP (a lost real e-mail) than FN, so the
50% threshold behind these rows is not the right one for that loss — the cost-adjusted cut-off
of [[L02-05-discriminant-analysis]] §10 is.

---

## 10 · U — the graduate-school admission script (site code)

`graduate-school-admission.txt` (Albert & Hu 2020, Problem 8, pp. 480–481): 400 applicants,
admission (0/1) on GRE and a dummy `GPA35` = 1{GPA ≥ 3.5}; it fits `lm` and
`glm(..., family=binomial(link="logit"))` and then a Bayesian version by sampling–importance
resampling. **The data are fetched from a URL and are not on disk**, and the script prints no
coefficient table, so only the figures can be read:

- Page 3 of the PDF: the LM and GLM fitted values almost coincide over GRE 400–800 for both GPA
  groups and stay inside about 0.1–0.55. **When fitted probabilities stay in the middle of $(0,1)$
  the logistic curve is nearly linear** (slope $\approx\beta\pi(1-\pi)$ from (8) barely changes),
  so the LPM is a fair approximation there; the two separate only at the extreme (GRE 220: LM
  ≈ 0.06, GLM ≈ 0.11). In `default`, where most $\hat\pi$ are near 0, they disagree badly (§1).
- The horizontal line (sample admission rate) sits near 0.32, so about one third were admitted —
  the script's comment "2/3 admitted and 1/3 not admitted" has the shares reversed.
- Page 5 marks the MLE (blue dots) at roughly $\hat\beta_0\approx-2.7$, $\hat\beta_{GRE}\approx0.0027$,
  $\hat\beta_{GPA35}\approx0.6$ — **figure readings, approximate**; the GPA odds ratio is then about $e^{0.6}\approx1.8$.
- The prior/posterior pages are Bayesian logit (Classes 3+4).

---

## Links

- Neighbours: [[L02-03-cross-validation-motorcycle]] (CV estimates the test error of a classifier as of a regression) · [[L02-05-discriminant-analysis]] (the generative route to the same posterior, cut-offs and costs) · [[L02-06-gaussian-vs-poisson-regression]] (same GLM/IRLS machinery, log link).
- Unit: [[L02-00-map]] · [[L02-01-prediction-error-bias-variance]] · [[L02-02-linear-log-linear-regression]] · [[L02-07-formulas]] · [[L02-08-pitfalls]] · [[L02-09-python]] (IRLS by hand with asserts).
- Class 1: [[../L01/L01-01-likelihood-sampling-rules|L01 §1]] (Bernoulli likelihood; iid vs logistic in `bernoulli-iid-logistic-R.txt`) · [[../L01/L01-06-gaussian-linear-regression|L01 §6]] (OLS = MLE; IRLS is repeated weighted OLS).
- Later: Bayesian logit, ridge/lasso — Classes 3+4; probit and multinomial models — Class 7 (`Map/class-plan.md`).
- Rules pack: [[../../rules/06_classificacao_validacao|rules/06]] (logistic regression, confusion matrix).
- **Practice** (statements in the books): I 4.1 (p. 193), I 4.9 (p. 195), I 4.12 (p. 196), I 4.13 (p. 196), I 4.14 (p. 197); W 17.C1 (p. 560).
