---
tags: [notes, lecture-02, cross-validation, loocv, k-fold, bootstrap, polynomial-regression, model-selection]
date: 2026-10-19
status: taught
source: "motorcyle-polynomialregression.pdf (11 slides: mcycle data, fits d = 1–20, in-sample adj. R² and BIC, 80/20 split, 100 replications, LOOCV, 10-fold, 10-fold × 100, bootstrap of the order-12 fit); motorcycle-polynomialregression.html (Lopes, 28/10/2025: code, orders 1–15, 200 replications); Fundamentos.pdf slides 27–35 (LOOCV, k-fold, Var[CV(n)]); multiplelinearregression.pdf slides 36–38 (training vs testing for best subset); ISLP §5.1 (pp. 202–209, eqs. 5.1–5.3), §5.2 (pp. 212–214, eq. 5.8), §7.1 (pp. 290–291, eqs. 7.1–7.2); AME §1.5.1 (pp. 14–16, eqs. 1.1–1.2, Observação 1.5), §1.5.1.1 (p. 21)"
---

# ISLP §5.1–5.2, §7.1 · Choosing the polynomial order by cross-validation, and putting a bootstrap band on the winner

> **Claim.** The test error of [[L02-01-prediction-error-bias-variance]] is not observable, but it
> can be **estimated by refitting on part of the data and predicting the rest**. A single
> hold-out split is noisy (on the site, 100 random 80/20 splits pick order 12 only 63 times);
> **10-fold CV picks it 99 times out of 100**; LOOCV costs a *single* fit for least squares,
> thanks to $CV_{(n)}=\frac1n\sum\big(\frac{y_i-\hat y_i}{1-h_{ii}}\big)^2$. All of adjusted $R^2$, BIC,
> LOOCV and 10-fold land on **order 12** for the motorcycle data, and a pairs bootstrap draws the
> uncertainty band around that fit.
> Prev: [[L02-02-linear-log-linear-regression]] · Next: [[L02-04-logistic-regression]] · Map: [[L02-00-map]]

**Notation.**

- $(x_i,y_i)$, $i=1,\dots,n$: the data; for mcycle, $x$ = time after impact (ms), $y$ = head acceleration ($g$), both standardised; $n=132$.
- $d$: polynomial order (tuning parameter); the model has $d+1$ coefficients.
- $X$: the $n\times(d+1)$ design $[1,x,\dots,x^d]$; $\hat\beta=(X'X)^{-1}X'y$; $\hat y_i=x_i'\hat\beta$; $e_i=y_i-\hat y_i$.
- $H=X(X'X)^{-1}X'$ the hat matrix, $h_{ii}=x_i'(X'X)^{-1}x_i$ the **leverage** of point $i$.
- $\hat\beta_{(i)}$, $\hat y_{(i)}=x_i'\hat\beta_{(i)}$: fit and prediction with point $i$ left out.
- $k$: number of folds; $\mathcal F_1,\dots,\mathcal F_k$ the index sets of the folds, $n_j=|\mathcal F_j|$.
- $B$: number of bootstrap resamples; $\hat f^{*b}$ the fit on resample $b$.

---

## 1 · U — two jobs for an error estimate

Fundamentos slide 27 names them: **model selection** (pick the flexibility — here $d$ — that best
balances bias and variance) and **model assessment** (say how well the chosen model will
predict). The training MSE does neither: it falls with every added term
([[L02-01-prediction-error-bias-variance]] §6). Two fixes exist: **penalise** the training error
(adjusted $R^2$, $C_p$, AIC, BIC — [[../L01/L01-06-gaussian-linear-regression|L01 §6]]), or
**estimate the test error directly** by predicting observations the fit has not seen (this note).

---

## 2 · C — polynomial regression and the mcycle data

**Polynomial regression is a linear model** (ISLP eq. 7.1, p. 290):

$$y_i=\beta_0+\beta_1x_i+\beta_2x_i^2+\dots+\beta_dx_i^d+\varepsilon_i, \tag{1}$$

OLS on the columns $x,x^2,\dots,x^d$ ([[L02-02-linear-log-linear-regression]] §1). ISLP warns that
$d$ above 3 or 4 gives "very strange shapes", "especially near the boundary of the X variable"
(p. 290) — keep that in mind when order 12 wins below.

**The data** (slides 2–3). MASS's `mcycle`: head acceleration in a simulated motorcycle crash,
used to test helmets (Silverman 1985). The code keeps the first 132 rows, maps $x\mapsto x/\max x$,
then $x\mapsto-1+2x$, then standardises; $y$ likewise. **The first two maps are wasted work:**
standardising $a x+b$ ($a>0$) gives back the standardised $x$, because the mean shifts by $b$ and
scales by $a$ while the SD scales by $a$:

$$\frac{(ax_i+b)-(a\bar x+b)}{a\,s_x}=\frac{x_i-\bar x}{s_x}. \tag{2}$$

The plot (slide 3) is flat and tight before impact, then a deep dip, a rebound and a noisy tail:
**the noise variance is far from constant**, which matters for §7.

---

## 3 · C — in-sample criteria: adjusted $R^2$ and BIC (slides 4–5)

Slide 4 fits $d=1,2,5,8,10,11,12,20$; the panel labels read

| $d$ | 1 | 2 | 5 | 8 | 10 | 11 | 12 | 20 |
|---|---|---|---|---|---|---|---|---|
| label "R2" | 0.0769 | 0.1323 | 0.5259 | 0.6941 | 0.769 | 0.7686 | **0.7798** | 0.7688 |

(the html code prints adjusted $R^2$ in that legend, and slide 5's adjusted-$R^2$ curve peaks at
the same $\approx0.78$, at $d=12$). The html computes, with $\hat\sigma^2=\text{RSS}/(n-d-1)$,

$$\bar R^2_d=1-(1-R^2_d)\frac{n-1}{n-d-1},\qquad \text{BIC}_d=\frac1n\big(\text{RSS}_d+\log(n)\,(d+1)\,\hat\sigma^2_d\big), \tag{3}$$

the BIC in AME's penalised-risk form $\text{EQM}(g)+\log(n)\,p\,\hat\sigma^2/n$ with $p=d+1$
(AME §1.5.1.1, p. 21). **Both pick $d=12$** (slide 5, dotted lines). Going from 12 to 20 adds eight
coefficients and *lowers* $\bar R^2$ from 0.7798 to 0.7688: the penalty at work.

**A number to carry.** $y$ is standardised, so $s_y^2=1$ and $\bar R^2=1-\hat\sigma^2/s_y^2$ gives at $d=12$

$$\hat\sigma^2_{12}=1-0.7798=0.2202,\qquad\hat\sigma_{12}=\sqrt{0.2202}=0.4693. \tag{4}$$

---

## 4 · C — the validation-set (hold-out) approach

**Estimator** (ISLP §5.1.1, pp. 202–204; AME eq. 1.2, p. 14). Split at random into a training part
$\mathcal T$ and a validation part $\mathcal V$; fit on $\mathcal T$ only; then

$$\hat R(d)=\frac1{|\mathcal V|}\sum_{i\in\mathcal V}\big(y_i-\hat f_{\mathcal T}(x_i)\big)^2. \tag{5}$$

Since $\mathcal V$ played no part in the fit, (5) is an honest estimate (consistent by the law of
large numbers, AME p. 14). **Two drawbacks** (ISLP §5.1.1 and p. 208): it varies a lot with the split, and it
fits on fewer points than $n$, so it tends to *overestimate* the error of the full-sample fit.

**One split** (slide 6, 80% / 20%): the root-MSE curve falls from about 0.92 at $d\le4$ to its
minimum at $d=12$.

**One hundred splits** (slide 7) — the variability made visible. Times each order wins:

| $d$ | 1–5 | 6 | 7 | 8 | 9 | **10** | 11 | **12** | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|
| wins (of 100) | 0 | 1 | 0 | 2 | 2 | **15** | 7 | **63** | 10 | 0 |

Total $1+2+2+15+7+63+10=100$ ✓. Order 12 wins 63% of the time; orders 10–13 together
$15+7+63+10=95\%$. The same experiment drives the best-subset size $k$ in the houseprice data
(multiplelinearregression.pdf slides 36–38: 1,000 random splits at 50%, 60%, 70%, 80% training;
the winners pile up at $k=5$–$7$).

> **A single split answers "which $d$?" with a random variable.** Repeating the split and
> reporting the distribution of winners is honest; reporting one split is not.

---

## 5 · C — leave-one-out CV, and the one-fit shortcut

**Definition** (Fundamentos slide 31; ISLP eq. 5.1, p. 204; AME p. 15). For each $i$, fit on the
other $n-1$ points and predict $y_i$:

$$CV_{(n)}=\frac1n\sum_{i=1}^n\big(y_i-\hat y_{(i)}\big)^2. \tag{6}$$

No randomness, and each fit uses $n-1$ points, so little bias (ISLP p. 205). AME Observação 1.5
(pp. 15–16): LOOCV on $n+1$ points is *exactly* unbiased for the expected risk of the method fitted
on $n$.

**The shortcut** (ISLP eq. 5.2, p. 205, stated there without proof). For least squares,

$$\boxed{\;CV_{(n)}=\frac1n\sum_{i=1}^n\Big(\frac{y_i-\hat y_i}{1-h_{ii}}\Big)^2\;} \tag{7}$$

— one fit instead of $n$. **Derivation.** Write $A=X'X$ and $u=x_i$, so $h_{ii}=u'A^{-1}u$.

*Step 1 — drop row $i$.* Removing one row from $X$ and $y$:

$$X_{(i)}'X_{(i)}=A-uu',\qquad X_{(i)}'y_{(i)}=X'y-u\,y_i. \tag{8}$$

*Step 2 — Sherman–Morrison* (for $1-u'A^{-1}u\neq0$):

$$(A-uu')^{-1}=A^{-1}+\frac{A^{-1}uu'A^{-1}}{1-h_{ii}}. \tag{9}$$

*Step 3 — substitute (8) and (9) into $\hat\beta_{(i)}=(X_{(i)}'X_{(i)})^{-1}X_{(i)}'y_{(i)}$:*

$$\hat\beta_{(i)}=\Big(A^{-1}+\frac{A^{-1}uu'A^{-1}}{1-h_{ii}}\Big)(X'y-u\,y_i). \tag{10}$$

Multiply out, using $A^{-1}X'y=\hat\beta$, $u'\hat\beta=\hat y_i$ and $u'A^{-1}u=h_{ii}$:

$$\hat\beta_{(i)}=\hat\beta-A^{-1}u\,y_i+\frac{A^{-1}u\,\hat y_i}{1-h_{ii}}-\frac{A^{-1}u\,h_{ii}\,y_i}{1-h_{ii}}. \tag{11}$$

Put the last three terms over $1-h_{ii}$:

$$\hat\beta_{(i)}=\hat\beta+\frac{A^{-1}u\,\big[-y_i(1-h_{ii})+\hat y_i-h_{ii}y_i\big]}{1-h_{ii}}=\hat\beta-\frac{A^{-1}u\,(y_i-\hat y_i)}{1-h_{ii}}=\hat\beta-\frac{A^{-1}x_i\,e_i}{1-h_{ii}}. \tag{12}$$

*Step 4 — the left-out residual.* Premultiply (12) by $x_i'$:

$$y_i-\hat y_{(i)}=y_i-\hat y_i+\frac{h_{ii}\,e_i}{1-h_{ii}}=e_i\Big(1+\frac{h_{ii}}{1-h_{ii}}\Big)=\frac{e_i}{1-h_{ii}}. \tag{13}$$

Substituting (13) into (6) gives (7). $\blacksquare$

> **Reading (13).** The left-out residual is the ordinary residual inflated by $1/(1-h_{ii})$ —
> "exactly the right amount" (ISLP p. 205). Since $\sum_ih_{ii}=\operatorname{tr}H=d+1$, the average
> leverage is $(d+1)/n$: at $d=12$, $n=132$, it is $13/132=0.0985$. But leverages are largest at the
> ends of the $x$ range, which is where a degree-12 polynomial is least trustworthy. (7) holds for
> least squares and some linear smoothers, **not** in general — logistic regression or LDA must be
> refitted $n$ times (ISLP p. 205).

**On the site** (slide 8): the LOOCV curve's minimum is at $d=12$, about 0.48 on the slide's
"Root MSE" axis.

**Variance of $CV_{(n)}$** (Fundamentos slide 35). With $\text{EQM}_i=(y_i-\hat y_{(i)})^2$,

$$\operatorname{Var}[CV_{(n)}]=\frac1{n^2}\sum_{i=1}^n\operatorname{Var}[\text{EQM}_i]+\frac2{n^2}\sum_{1\le i<j\le n}\operatorname{Cov}[\text{EQM}_i,\text{EQM}_j]. \tag{14}$$

The $n$ fits share $n-2$ of their $n-1$ points, so the covariances are large and positive: LOOCV is
nearly unbiased but **high-variance** (ISLP §5.1.4, pp. 208–209).

---

## 6 · C — $k$-fold CV

**Definition** (Fundamentos slide 33; ISLP eq. 5.3, p. 206). Split at random into $k$ folds of about
equal size; fit without fold $j$, compute $\text{MSE}_j$ on fold $j$; average:

$$CV_{(k)}=\frac1k\sum_{j=1}^k\text{MSE}_j,\qquad \text{MSE}_j=\frac1{n_j}\sum_{i\in\mathcal F_j}\big(y_i-\hat f_{-j}(x_i)\big)^2. \tag{15}$$

$k=n$ is LOOCV (slide 35). AME (p. 15) and the site's code use the observation-weighted version

$$\widetilde{CV}_{(k)}=\frac1n\sum_{j=1}^k\sum_{i\in\mathcal F_j}\big(y_i-\hat f_{-j}(x_i)\big)^2=\sum_{j=1}^k\frac{n_j}{n}\,\text{MSE}_j, \tag{16}$$

equal to (15) only when all $n_j=n/k$.

**The site's folds, worked.** `L = trunc(n/fold)` $=\lfloor132/10\rfloor=13$; folds 1–9 are 13
consecutive (shuffled) positions each, $9\times13=117$, and fold 10 takes the rest,
$132-117=15$. So $n_j/n=13/132$ or $15/132$, not $1/10$ — (16) and (15) differ slightly.

**Why $k=5$ or $10$** (ISLP §5.1.4; Fundamentos slide 35):

| Method | fit size here ($n=132$) | bias of the error estimate | variance | cost (fits) |
|---|---|---|---|---|
| 80/20 hold-out | $\approx105$ ($0.8\times132=105.6$) | highest | high (one split) | 1 |
| 10-fold | $\approx119$ ($0.9\times132=118.8$) | small | moderate | 10 |
| LOOCV | 131 | smallest | highest (correlated fits) | $n$ (1 with (7)) |

**On the site**: one 10-fold run (slide 9) has its minimum at $d=12$; repeating the random fold
assignment 100 times (slide 10), **$d=12$ wins 99 times and $d=13$ once**. Compare 63 for the
hold-out in §4: every observation is predicted once in every run, so the only randomness left is
the fold assignment.

> **The axis label is not the quantity — but the argmin is safe.** In the html code the LOO loop
> accumulates the *sum* of squared errors and the 10-fold loop divides it by $n$ (an MSE), both
> plotted under "Root MSE". On the slides the curves sit near 0.48 at $d=12$; by (4) an MSE there
> cannot be below about $\hat\sigma^2=0.22$, while $\sqrt{0.22}=0.47$ — so the slides show root
> MSE. SSE, MSE and root MSE are increasing transforms of one another: **the chosen $d$ is the
> same**, only the vertical scale differs.

---

## 7 · C — bootstrap bands for the chosen fit

**Pairs bootstrap** (slide 11; html §8; ISLP §5.2, pp. 212–214). With $d^*=12$ fixed, for
$b=1,\dots,B=1000$: draw $n$ indices with replacement, refit (1) on those pairs, keep the fitted
curve $\hat f^{*b}$. Slide 11 draws all 1,000 curves in grey under the red order-12 fit. A
pointwise 95% **percentile band** keeps, at each $x$, the 2.5% and 97.5% quantiles of
$\{\hat f^{*b}(x)\}_{b=1}^B$; the bootstrap standard error at $x$ is ISLP's (5.8), p. 214:

$$\text{SE}_B\big(\hat f(x)\big)=\sqrt{\frac1{B-1}\sum_{r=1}^B\Big(\hat f^{*r}(x)-\frac1B\sum_{r'=1}^B\hat f^{*r'}(x)\Big)^2}. \tag{17}$$

**The formula alternative** (ISLP eq. 7.2 and footnote 1, p. 291): with
$\ell_0=(1,x_0,\dots,x_0^d)'$ and $\hat C=\hat\sigma^2(X'X)^{-1}$,

$$\widehat{\operatorname{Var}}\big[\hat f(x_0)\big]=\ell_0'\hat C\,\ell_0,\qquad \hat f(x_0)\pm2\sqrt{\ell_0'\hat C\,\ell_0}. \tag{18}$$

(18) assumes **one** error variance for all $x$. Resampling pairs does not: each resample carries
the quiet pre-impact points and the noisy tail in their own proportions. With mcycle's
heteroskedasticity (§2) the two bands disagree, the bootstrap one being wider where the noise is
large.

> **What the band does not cover:** the order was chosen on the same data and is held at 12 in
> every resample. Model-selection uncertainty is outside it (G: re-running the CV inside each
> resample would put it in).

---

## 8 · C — Worked: the whole pipeline on a reproducible stand-in

The `mcycle` data are not in the repo, so the figures below run every step on a **simulated
stand-in** built to look like slide 3 — $n=132$, a flat start, a dip to about $-2$ and a rebound to
about $+1.3$ in standardised units, noise SD 0.15 before the dip and 0.45 after (seeded; definition
in `figures/make_figures.py`). **Its numbers are not the site's.** That its CV also lands on 12 is a
property of how the stand-in was drawn, not evidence about `mcycle`.

| $d$ | training MSE | 80/20 hold-out (mean of 100) | LOOCV by (7) | 10-fold (mean of 100) |
|---|---|---|---|---|
| 1 | 0.9252 | 0.9550 | 0.9461 | 0.9481 |
| 3 | 0.7376 | 0.7954 | 0.7781 | 0.7810 |
| 5 | 0.5388 | 0.6192 | 0.5900 | 0.5917 |
| 7 | 0.3219 | 0.3746 | 0.3567 | 0.3577 |
| 10 | 0.1847 | 0.2262 | 0.2174 | 0.2197 |
| **12** | 0.1737 | **0.2220** | **0.2082** | **0.2117** |
| 13 | 0.1736 | 0.2357 | 0.2109 | 0.2164 |
| 14 | 0.1722 | 0.2501 | 0.2107 | 0.2179 |

Read across a row: training < LOOCV < 10-fold < hold-out, the ordering of §6's table (fit size
$132>131>\approx119>\approx105$). Read down: training keeps falling to $d=14$; the three honest estimates
turn up after 12. Over 100 random splits, the hold-out winners scatter (order 14: 31, 12: 30,
10: 23, 13: 10, others 6) while 10-fold picks 12 82 times — the same contrast as the site's 63 vs 99.

![Three panels on simulated stand-in data. Left: training MSE, mean 80/20 hold-out MSE, LOOCV and mean 10-fold CV against polynomial order 1 to 14; all fall steeply to order 10, training keeps falling, the three CV curves are lowest at order 12. Middle: bars of how often each order wins over 100 random splits; hold-out wins spread over orders 10, 12, 13 and 14, 10-fold concentrates 82 of 100 at order 12. Right: the stand-in data with the order-12 fit, a pairs-bootstrap 95% band and the ±2 SE formula band; the bootstrap band is wider in the noisy region after the dip and flares at both ends.](figures/L02-cv-curves.png)
*Stand-in data (simulated, labelled on the figure): estimated test error by (5), (7), (16); winners over 100 splits; percentile band from B = 1000 pairs resamples vs the formula band (18). Mirrors motorcycle slides 6–11.*

The right panel shows both lessons of §7 and §2 at once: in the noisy tail the bootstrap band is
wider than the constant-variance formula band, and at both ends of the $x$ range the band flares,
the boundary misbehaviour ISLP warns about for high degrees.

![Two panels on the stand-in data. Left: leverage of each point against x for orders 3 and 12 on a log scale; both are U-shaped, smallest in the middle and largest at the two ends, with means 0.0303 and 0.0985 marked as dotted lines at (d+1)/n. Right: LOOCV computed by 132 refits against LOOCV from the one-fit shortcut for orders 1 to 14; every point lies on the 45-degree line.](figures/L02-loocv-shortcut.png)
*Leverages $h_{ii}$ (mean $(d+1)/n$: $4/132=0.0303$, $13/132=0.0985$) and the identity (7) checked against brute force (6), stand-in data. ISLP eq. 5.2, p. 205.*

Every point sits on the diagonal (agreement to relative $10^{-8}$, asserted in the script): the
derivation (8)–(13) in numbers. The left panel shows where the inflation $1/(1-h_{ii})$ bites —
at the edges, more so for $d=12$.

> **Interactive companion.** [The Flexibility Dial](companions/companion-bias-variance-polynomial.html) — the population version of the left panel: move the degree $d$, the training size $n$ and the noise $\sigma$ on the tanh model of L02-01 and watch the *true* test error that CV is trying to estimate, and where its minimum sits.

---

## 9 · G — named, not developed here

- **One-standard-error rule**: pick the simplest model whose CV error is within one standard error of the minimum (ISLP Ch. 6). On the stand-in, orders 10 and 12 differ by less than 0.01 in CV error, so the rule could well prefer the simpler one.
- **Selection bias of the minimum**: the smallest of 14 CV estimates is optimistic for the chosen model; an untouched test set (AME's training / validation / test split, p. 16) or nested CV fixes it.
- **CV for classification** (ISLP eq. 5.4): the error indicator replaces the squared error → [[L02-04-logistic-regression]], [[L02-05-discriminant-analysis]].
- **Ridge and lasso**, whose penalty is chosen by CV (`cv.glmnet` in multiplelinearregression.pdf): Classes 3+4.

---

## Links

- Prev: [[L02-02-linear-log-linear-regression]]; Next: [[L02-04-logistic-regression]]; the target being estimated: [[L02-01-prediction-error-bias-variance]] §4–§6.
- Class 1: $R^2$, adjusted $R^2$, AIC/BIC, overfitting → [[../L01/L01-06-gaussian-linear-regression|L01 §6]]; the bootstrap and where it fails ($x_{(n)}$) → [[../L01/L01-05-comparing-estimators-mse-bootstrap|L01 §5]].
- Unit: [[L02-07-formulas]] ((7), (15), (17), (18)), [[L02-08-pitfalls]], [[L02-09-python]] (CV by hand, the shortcut, the bootstrap band).
- Rules pack: [[../../rules/06_classificacao_validacao|rules/06]] (training and test samples, LOOCV, k-fold). Class plan: [[../../Map/class-plan#Class 2: Introduction to statistical learning|Class 2]].
- Reading: ISLP §5.1 pp. 202–209, §5.2 pp. 212–214, §7.1 pp. 290–291; AME §1.5.1 pp. 14–16 (in Portuguese).
- **Practice:** ISLP 5.3 (p. 225), 5.5 (p. 225), 5.8 (p. 227, LOOCV for polynomial degree); ISLP 7.6 (p. 327), 7.9 (p. 327, CV-chosen degree).
