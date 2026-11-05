---
tags: [notes, lecture-02, statistical-learning, regression-function, prediction-error, bias-variance]
date: 2026-10-19
status: taught
source: "Marques, Fundamentos.pdf slides 2–30 (regression function, prediction vs inference, additive model, reducible/irreducible error and bias–variance with proofs, tanh simulation slides 20–27, training MSE slides 28–30); bias-variance-R.txt; ISLP §2.1 (p. 15, eq. 2.1), §2.1.1 (pp. 17–20, eqs. 2.2–2.3), §2.2.1–2.2.2 (pp. 28–34, eqs. 2.5–2.7); AME §1.4 (pp. 9–11, Teorema 1, Observação 1.3), §1.5.1 (p. 14, eq. 1.1), §1.5.2 (pp. 22–23)"
---

# Fundamentos slides 6–30 · ISLP §2.1–2.2 · The best predictor is $E[Y\mid X]$, and every estimate of it pays bias², variance and noise

> **Claim.** Under squared loss the best possible predictor of $Y$ from $X$ is the regression
> function $\psi(x)=E[Y\mid X=x]$ — a two-line calculus result. Any *learned* $\hat\psi$ then
> misses $Y$ by three separate amounts: **noise $\sigma^2$ that no method can remove, squared
> bias that falls as the learner gets more flexible, and variance that rises with it.** The
> expected test error is U-shaped in flexibility, the training error is not — so the training
> error can never choose the flexibility. Notes 02–03 build on this: 02 reads the coefficients of
> the linear learners, 03 estimates the test error by cross-validation.
> Prev: [[../L01/L01-11-python]] · Next: [[L02-02-linear-log-linear-regression]] · Map: [[L02-00-map]]

**Notation.**

- $X\in\mathbb R^p$ predictors, $Y\in\mathbb R$ response, joint distribution $F_{X,Y}$ (unknown), marginal $F_X$.
- $\psi(x)=E[Y\mid X=x]$ the **regression function** (Marques's $\psi$; ISLP writes $f$, AME writes $r$).
- $\varphi:\mathbb R^p\to\mathbb R$ any candidate predictor; $t=\varphi(x)$ its value at one point.
- $\mathcal D=\{(X_1,Y_1),\dots,(X_n,Y_n)\}$ i.i.d. training data; $\hat\psi=\mathcal L[\mathcal D]$ the learned function, $\mathcal L$ the learning method.
- $\varepsilon$ the additive error: $E[\varepsilon]=0$, $\operatorname{Var}[\varepsilon]=\sigma^2$, independent of $X$ and of $\mathcal D$.
- $(X,Y)$ written without index is always a **new** observation, independent of $\mathcal D$.
- $\operatorname{EQM}[\hat\psi(x)]=E[(\hat\psi(x)-\psi(x))^2]$ (*erro quadrático médio*, MSE of the estimator at $x$); $\operatorname{Viés}$ = bias.
- gl (*graus de liberdade*) = degrees of freedom of a smoother; $d$ = polynomial degree (a degree-$d$ polynomial has $d+1$ df).

---

## 1 · U — supervised learning, and the two things one wants from it

**The set-up** (slides 2–5). One observes predictors $X$ and a response $Y$ — in ISLP's *Advertising*
data, TV, radio and newspaper budgets and the sales of 200 markets. **Regression** if $Y$ is
quantitative, **classification** if it is a label ([[L02-04-logistic-regression]],
[[L02-05-discriminant-analysis]]). With no $Y$ at all (clustering, PCA) the problem is
*unsupervised* and out of this course's scope.

**Two purposes, usually in tension** (slides 10–12; ISLP §2.1.1, pp. 17–20):

| | **Prediction** | **Inference** |
|---|---|---|
| Treat $\hat\psi$ as | a black box | an object to read |
| Success means | small $E[(Y-\hat\psi(X))^2]$ on *new* data | knowing which predictors matter, and how |
| Typical question | "what sales will this market have?" | "is TV associated with sales? what does +25% newspaper do?" |
| Favours | flexible methods (trees, boosting, SVMs) | rigid, interpretable ones (least squares, subset selection, lasso) |

> **Flexibility buys accuracy and costs interpretability** (slide 12, after ISLP Fig. 2.7). This
> note is about the prediction side; [[L02-02-linear-log-linear-regression]] is the inference side
> of the same linear learners.

---

## 2 · C — the regression function minimises the expected prediction error

**Problem** (slide 6). Find $\varphi:\mathbb R^p\to\mathbb R$ minimising the **expected prediction
error** (also *expected test error*, or just *test error*)

$$E\big[(Y-\varphi(X))^2\big]=\int (y-\varphi(x))^2\,dF_{X,Y}(x,y). \tag{1}$$

**Step 1 — condition on $X$** (slide 7). By iterated expectations,

$$E\big[(Y-\varphi(X))^2\big]=E\Big[E\big[(Y-\varphi(X))^2\mid X\big]\Big]=\int E\big[(Y-\varphi(x))^2\mid X=x\big]\,dF_X(x). \tag{2}$$

Every integrand in (2) is non-negative and involves $\varphi$ only through the single number
$\varphi(x)$, so **(2) is minimised by minimising the integrand separately at each $x$.**

**Step 2 — one variable at a time** (slide 8). Fix $x$ and write $t=\varphi(x)$. Expanding the square
inside the conditional expectation:

$$g(t):=E\big[(Y-t)^2\mid X=x\big]=E[Y^2\mid X=x]-2t\,E[Y\mid X=x]+t^2. \tag{3}$$

**Step 3 — first- and second-order conditions.** Differentiating (3) in $t$,

$$g'(t)=-2\,E[Y\mid X=x]+2t, \tag{4}$$

$$g'(t)=0\iff t=E[Y\mid X=x],\qquad g''(t)=2>0. \tag{5}$$

So the minimiser is unique at every $x$, and putting the pointwise solutions back into (2):

$$\boxed{\;\arg\min_{\varphi}E\big[(Y-\varphi(X))^2\big]=\psi(x)=E[Y\mid X=x]\;} \tag{6}$$

**The same result as a decomposition** (AME Teorema 1, p. 10). For any fixed $g$, add and subtract
$\psi(X)$:

$$E\big[(Y-g(X))^2\big]=E\big[(Y-\psi(X)+\psi(X)-g(X))^2\big]$$

$$=E\big[(\psi(X)-g(X))^2\big]+E\big[(Y-\psi(X))^2\big]+2E\big[(\psi(X)-g(X))(Y-\psi(X))\big]. \tag{7}$$

The cross term vanishes by conditioning on $X$, because $\psi(X)-g(X)$ is then a constant:

$$E\big[(\psi(X)-g(X))(Y-\psi(X))\big]=E\Big[(\psi(X)-g(X))\,\big(E[Y\mid X]-\psi(X)\big)\Big]=E\big[(\psi(X)-g(X))\cdot 0\big]=0, \tag{8}$$

and the middle term is $E\big[E[(Y-\psi(X))^2\mid X]\big]=E\big[V[Y\mid X]\big]$. Substituting (8) into (7):

$$\underbrace{E\big[(Y-g(X))^2\big]}_{R_{\text{pred}}(g)}=\underbrace{E\big[(\psi(X)-g(X))^2\big]}_{R_{\text{reg}}(g)}+E\big[V[Y\mid X]\big]. \tag{9}$$

> **Reading (9).** The second term does not depend on $g$. So **predicting $Y$ well and estimating
> the regression function well are the same problem** under squared loss — the reason the whole
> course of regression methods is also a course in prediction. With absolute loss the answer
> would be the conditional median instead (slide 6, remark 2; AME Observação 1.2).

**The catch** (slide 9). $\psi$ is a functional of the unknown $F_{X,Y}$. Learning means building
$\hat\psi=\mathcal L[\mathcal D]$ from the training data; each method (OLS, a spline, a tree) is one
functional $\mathcal L$.

---

## 3 · C — the additive model: reducible and irreducible error

**The model** (slides 13–14; ISLP eq. 2.1, p. 15):

$$Y=\psi(X)+\varepsilon,\qquad Y_i=\psi(X_i)+\varepsilon_i,\quad i=1,\dots,n, \tag{10}$$

with $X, X_1,\dots,X_n$ i.i.d. $F_X$; $\varepsilon,\varepsilon_1,\dots,\varepsilon_n$ i.i.d., mean $0$, variance
$\sigma^2$; and **$X$, the $X_i$'s and the $\varepsilon$'s all mutually independent.** Then
$E[Y\mid X=x]=\psi(x)+E[\varepsilon]=\psi(x)$, so $\psi$ in (10) *is* the regression function of §2.
The prediction for the new point is $\hat Y=\hat\psi(X)$.

**Conditioning on the new $X$** (slide 15), exactly as in (2):

$$E\big[(Y-\hat\psi(X))^2\big]=\int E\big[(Y-\hat\psi(x))^2\mid X=x\big]\,dF_X(x). \tag{11}$$

The expectation now runs over **both** the new $\varepsilon$ and the training sample $\mathcal D$
inside $\hat\psi$ (AME Observação 1.3, p. 11: the *expected* risk, as opposed to the conditional
risk of one fixed $\hat\psi$).

**Proof of the split** (slide 16). Substitute (10) for $Y$ at $X=x$:

$$E\big[(Y-\hat\psi(x))^2\mid X=x\big]=E\big[(\psi(x)+\varepsilon-\hat\psi(x))^2\big]. \tag{12}$$

Write the bracket as $-(\hat\psi(x)-\psi(x))+\varepsilon$ and expand:

$$=E\big[(\hat\psi(x)-\psi(x))^2\big]-2\,E\big[(\hat\psi(x)-\psi(x))\,\varepsilon\big]+E[\varepsilon^2]. \tag{13}$$

$\hat\psi$ is built from $\mathcal D$ alone and the new $\varepsilon$ is independent of $\mathcal D$, so the
expectation of the product factorises:

$$E\big[(\hat\psi(x)-\psi(x))\,\varepsilon\big]=\big(E[\hat\psi(x)]-\psi(x)\big)\cdot E[\varepsilon]=\big(E[\hat\psi(x)]-\psi(x)\big)\cdot 0=0. \tag{14}$$

*(The slide writes the cross term with a $+2$; the expansion gives $-2$. It is zero either way.)*
With $E[\varepsilon^2]=\operatorname{Var}[\varepsilon]+0^2=\sigma^2$, substituting (14) into (13):

$$\boxed{\;E\big[(Y-\hat\psi(x))^2\mid X=x\big]=\underbrace{\operatorname{EQM}[\hat\psi(x)]}_{\text{reducible}}+\underbrace{\sigma^2}_{\text{irreducible}}\;} \tag{15}$$

and integrating (15) through (11):

$$E\big[(Y-\hat\psi(X))^2\big]=\int\operatorname{EQM}[\hat\psi(x)]\,dF_X(x)+\sigma^2. \tag{16}$$

> **The choice of method moves $\operatorname{EQM}$; nothing moves $\sigma^2$** (slide 16). ISLP
> eq. (2.3), p. 18, is (15) with $\hat\psi$ and $X$ held fixed, so its reducible part is the plain
> square $[\psi(X)-\hat\psi(X)]^2$. **$\sigma^2$ is a floor on the test error that is almost always
> unknown in practice** (ISLP p. 18) — it is the variation in $Y$ due to everything not in $X$.

---

## 4 · C — the reducible part splits into squared bias plus variance

**Definitions** (slide 17), at a fixed $x$, with expectations over training samples $\mathcal D$:

$$\operatorname{Viés}[\hat\psi(x)]=E[\hat\psi(x)]-\psi(x),\qquad \operatorname{Var}[\hat\psi(x)]=E\big[(\hat\psi(x)-E[\hat\psi(x)])^2\big]. \tag{17}$$

**Proof** (slide 18) — the same add-and-subtract as Class 1's $\text{MSE}=\text{Var}+\text{bias}^2$
([[../L01/L01-05-comparing-estimators-mse-bootstrap|L01 §5]]), now pointwise in $x$. Insert
$E[\hat\psi(x)]$:

$$\operatorname{EQM}[\hat\psi(x)]=E\Big[\big((\hat\psi(x)-E[\hat\psi(x)])-(\psi(x)-E[\hat\psi(x)])\big)^2\Big] \tag{18}$$

$$=E\big[(\hat\psi(x)-E\hat\psi(x))^2\big]-2\,E\big[\hat\psi(x)-E\hat\psi(x)\big]\,\big(\psi(x)-E\hat\psi(x)\big)+\big(\psi(x)-E\hat\psi(x)\big)^2. \tag{19}$$

The middle factor is a constant times $E[\hat\psi(x)]-E[\hat\psi(x)]=0$, so

$$\operatorname{EQM}[\hat\psi(x)]=\operatorname{Var}[\hat\psi(x)]+\operatorname{Viés}^2[\hat\psi(x)]. \tag{20}$$

**Substituting (20) into (16)** gives the full factorisation:

$$\boxed{\;E\big[(Y-\hat\psi(X))^2\big]=\int\operatorname{Viés}^2[\hat\psi(x)]\,dF_X(x)+\int\operatorname{Var}[\hat\psi(x)]\,dF_X(x)+\sigma^2\;} \tag{21}$$

— expected squared bias, expected variance, irreducible error. ISLP eq. (2.7), p. 32, is the
pointwise version of (21) at $x_0$ (stated there without proof); AME §1.5.2, p. 22, writes it with
$V[Y\mid X=x]$ in place of $\sigma^2$, which also covers heteroskedastic noise.

**Where the randomness lives** — the point `bias-variance-R.txt` asks the reader to check:

| Term in (21) | Random over | What drives it |
|---|---|---|
| $\sigma^2$ | the new $\varepsilon$ | the world; untouchable |
| $\operatorname{Viés}^2[\hat\psi(x)]$ | nothing (a number per $x$) | how far the *average* learned curve is from $\psi$: a rigid learner cannot bend to $\psi$ |
| $\operatorname{Var}[\hat\psi(x)]$ | the training sample $\mathcal D$ | how much $\hat\psi$ moves when the sample is redrawn: a flexible learner chases its sample |

> **"Variance" here is the variance of the *learned function* across training samples, not of $Y$.**
> High-variance method: change 10% of the sample and $\hat\psi$ changes a lot (slide 19). High
> bias: the method can only learn a restricted class of functions — a straight line fitted to a
> strongly non-linear $\psi$.

### 4.1 · Worked — a high-bias, low-variance learner, quantified (`bias-variance-R.txt`)

The script draws $n=1000$ points from $y=1-x+2x^2+\varepsilon$, $x\sim U(0,1)$, $\sigma=0.1$, and refits a
straight line to 90% subsamples: *"Can you even see the fitted regression line changing?"*
The two terms of (21) can be computed exactly.

**Bias.** As $n$ grows, the OLS line converges to the population projection of $\psi$ on $\{1,x\}$.
For $x\sim U(0,1)$, the projection of $x^2$ is $x-\tfrac16$ (residual $x^2-x+\tfrac16$, orthogonal to
$1$ and $x$). Substituting into $\psi$:

$$\psi(x)=1-x+2x^2=1-x+2\big(x-\tfrac16\big)+2\big(x^2-x+\tfrac16\big)=\big(\tfrac23+x\big)+2\big(x^2-x+\tfrac16\big). \tag{22}$$

So the bias of the line is $-2(x^2-x+\tfrac16)$, and with $\int_0^1(x^2-x+\tfrac16)^2dx=\tfrac1{180}$:

$$\int_0^1\operatorname{Viés}^2\,dx=4\cdot\tfrac{1}{180}=\tfrac1{45}=0.0222. \tag{23}$$

**Variance.** OLS with 2 coefficients on $n'=900$ points averages $\sigma^2\cdot 2/n'$ over the design:

$$\overline{\operatorname{Var}}\approx\frac{0.1^2\times2}{900}=0.0000222. \tag{24}$$

> **Squared bias (0.0222) is 1000 times the variance (0.0000222) and more than twice the noise
> ($\sigma^2=0.01$).** (Holding the design fixed, as (24) does. If every training set draws fresh
> $x$ values the variance is about $8.6\times10^{-5}$, so bias² is "only" about 260 times larger;
> [[L02-09-python]] §1 computes both.) That is "high bias, low variance": the line is stable to the fourth decimal
> across subsamples *and* systematically wrong. The script's tall regression tree is the opposite
> corner (G layer: boosting attacks bias with many short trees, random forests attack variance by
> averaging many tall ones — named in the script, not developed in this course). Both numbers are
> checked in [[L02-09-python]].

---

## 5 · C — Worked: the tanh simulation (slides 20–27)

**The world, fully known** (slide 21). $X$ = years of schooling, $Y$ = annual income in thousand R\$:

$$\psi(x)=45\tanh\!\Big(\frac{x}{1.9}-7\Big)+57,\qquad X\sim U(8,18),\qquad \varepsilon\sim N(0,4^2),\qquad n=30. \tag{25}$$

**Reading (25) with numbers.** The argument of $\tanh$ is zero at $x=7\times1.9=13.3$, where
$\psi=45\cdot0+57=57$: the inflection point. At the ends,

$$\psi(8)=45\tanh(-2.7895)+57=45(-0.99248)+57=12.339,\qquad \psi(18)=45\tanh(2.4737)+57=45(0.98590)+57=101.365, \tag{26}$$

and the slope at the inflection is $\psi'(13.3)=\frac{45}{1.9}\operatorname{sech}^2(0)=23.68$ thousand R\$ per
extra year — an S-curve from about 12 to about 101 that no straight line can follow. The
irreducible error is $\sigma^2=4^2=16$, the dotted line of slide 26.

![The tanh regression function from 8 to 18 years of schooling, rising from 12.3 to 101.4 with an inflection at 13.3 years where it equals 57; thirty seeded training points scattered around it; the OLS line cuts across the S, the degree-6 polynomial follows it closely, and the polygonal interpolant passes through every point.](figures/L02-tanh-regression-function.png)
*ψ of (25), 30 pairs from a seeded draw (not the slide's sample), and three learners: df = 2 (the OLS line, which is what the slide's smoothing spline gives at gl = 2), df = 7 (a degree-6 polynomial standing in for gl = 7), df = 30 (the interpolant, as gl = 30 on slide 24). Fundamentos slides 21–24.*

The line is rigid: it under-predicts at 8 and 18 and over-predicts just below 13 years, and
redrawing the sample would barely move it — bias without variance. The interpolant has zero
training error (it passes through every point) but zigzags with the noise — variance without
bias. The degree-6 curve tracks $\psi$ to within a few thousand reais everywhere: the trade-off
in one picture.

**The slide's Monte Carlo** (slide 25). For each gl $=2,\dots,n$: draw $M$ test points
$x^{(i)}\sim F_X$; for each, draw $N$ training samples of size $n$, fit $\hat\psi^{(gl)}_j$, and
estimate the two terms of (21) by

$$\widehat{\operatorname{Viés}^2}(x^{(i)})=\Big(\tfrac1N\textstyle\sum_{j=1}^N\hat\psi^{(gl)}_j(x^{(i)})-\psi(x^{(i)})\Big)^2,\qquad \widehat{\operatorname{Var}}(x^{(i)})=\text{variance of the }N\text{ values }\hat\psi^{(gl)}_j(x^{(i)}), \tag{27}$$

then average each over the $M$ points. Slide 26 shows the result: bias² falls to near zero by
gl ≈ 7, variance climbs steadily, and the prediction error bottoms out near 20, above the dotted line at $\sigma^2=16$ —
**"aproximadamente 7 graus de liberdade"** (slide 27).

**The same experiment, exactly.** Swap the smoothing spline for an OLS polynomial of degree $d$ on a
fixed equispaced design of 30 points in $[8,18]$. Then $\hat\psi(x_0)=b(x_0)'(B'B)^{-1}B'\mathbf y$ is
linear in $\mathbf y=\boldsymbol\psi+\boldsymbol\varepsilon$ ($B$ the $30\times(d+1)$ basis matrix, $b(x_0)$ its row
at $x_0$), so both terms of (17) are closed-form:

$$E[\hat\psi(x_0)]=b(x_0)'(B'B)^{-1}B'\boldsymbol\psi,\qquad \operatorname{Var}[\hat\psi(x_0)]=\sigma^2\,b(x_0)'(B'B)^{-1}b(x_0), \tag{28}$$

averaged over a uniform grid on $[8,18]$ in place of $dF_X$. The numbers (computed in
`figures/make_figures.py`):

| $d$ (df) | avg bias² | avg variance | $\sigma^2$ | **expected test error** | expected training MSE |
|---|---|---|---|---|---|
| 1 (2) | 74.80 | 1.03 | 16 | 91.83 | 93.87 |
| 3 (4) | 7.98 | 1.97 | 16 | 25.95 | 22.39 |
| 5 (6) | 0.94 | 2.87 | 16 | **19.81** | 13.79 |
| 6 (7) | 0.70 | 3.33 | 16 | 20.03 | 13.01 |
| 7 (8) | 0.11 | 3.80 | 16 | 19.91 | 11.85 |
| 10 (11) | 0.007 | 5.37 | 16 | 21.38 | 10.14 |
| 15 (16) | 0.000 | 10.20 | 16 | 26.20 | 7.47 |

Check one row against (21): at $d=5$, $0.94+2.87+16=19.81$. ✓

![Expected test error, average squared bias, average variance, expected training MSE and the irreducible level 16 against polynomial degree 0 to 15; bias falls from over 1000 to nearly zero by degree 9, variance rises from 0.5 to 10, test error bottoms at 19.8 at degree 5 and rises after, training error keeps falling below 16.](figures/L02-bias-variance-curves.png)
*Exact (21) for an OLS polynomial on 30 equispaced points, σ = 4 (symmetric-log axis). Same world as Fundamentos slides 21 and 26; different learner and design, stated above.*

The minimum is flat: degrees 5, 6 and 7 (6–8 df) are within 0.25 of each other, right where the
slide's spline lands (about 7 df). Past it, bias² has nothing left to give and the variance curve
carries the test error up; the training curve slides *below* $\sigma^2=16$ — the fit is now
reproducing noise.

> **Interactive companion.** [The Flexibility Dial](companions/companion-bias-variance-polynomial.html) — move the degree $d$, the training size $n$ and the noise $\sigma$ on this tanh model; watch bias², variance, training and test error, and where the optimal degree goes (larger $n$ or smaller $\sigma$ push it right).

---

## 6 · C — why the training error cannot pick the flexibility

**Training MSE** (slide 28; ISLP eq. 2.5, p. 28; AME eq. 1.1, p. 14):

$$\text{EQM}_{\text{train}}=\frac1n\sum_{i=1}^n\big(y_i-\hat\psi(x_i)\big)^2. \tag{29}$$

Slides 29–30: as gl grows, (29) **falls monotonically** and hits **zero at gl = 30**, where the
spline interpolates. Choosing gl by (29) always picks the most overfitted model. ISLP's test MSE
(eq. 2.6, p. 29) is the average of $(y_0-\hat\psi(x_0))^2$ over *previously unseen* pairs — the
quantity (21) describes.

**How optimistic is it? Exactly, for OLS** (G layer, proved because it explains the AIC/$C_p$
penalties of [[../L01/L01-06-gaussian-linear-regression|L01 §6]]). With hat matrix
$H=B(B'B)^{-1}B'$, the residual vector is

$$\mathbf e=(I-H)\mathbf y=(I-H)\boldsymbol\psi+(I-H)\boldsymbol\varepsilon. \tag{30}$$

$I-H$ is symmetric and idempotent with trace $n-(d+1)$, and $E[\boldsymbol\varepsilon]=\mathbf 0$ kills the
cross term, so

$$E\|\mathbf e\|^2=\|(I-H)\boldsymbol\psi\|^2+E[\boldsymbol\varepsilon'(I-H)\boldsymbol\varepsilon]=\|(I-H)\boldsymbol\psi\|^2+\sigma^2\big(n-d-1\big). \tag{31}$$

Dividing by $n$:

$$E[\text{EQM}_{\text{train}}]=\frac{\|(I-H)\boldsymbol\psi\|^2}{n}+\sigma^2\Big(1-\frac{d+1}{n}\Big). \tag{32}$$

For a *new* response at the same design points, the error is
$\|(I-H)\boldsymbol\psi\|^2/n+\sigma^2(d+1)/n+\sigma^2$ (bias² + variance + noise, averaged over the
$x_i$). Subtracting (32):

$$E[\text{in-sample test error}]-E[\text{EQM}_{\text{train}}]=\frac{2\sigma^2(d+1)}{n}. \tag{33}$$

> **The training error understates the error on new responses by $2\sigma^2(d+1)/n$ — growing with
> every parameter.** Adding exactly that penalty back is Mallows' $C_p$ / AIC; BIC uses
> $\log(n)$ in place of 2 (AME §1.5.1.1, p. 21). At $d=5$, $n=30$, $\sigma^2=16$:
> $2(16)(6)/30=6.4$. The other route — estimate the test error directly on held-out data — is
> cross-validation, [[L02-03-cross-validation-motorcycle]].

---

## 7 · G — named, not developed here

- **Smoothing splines** (the slide's learner, `smooth.spline()` with gl): a black box on purpose (slide 23). Polynomials stand in for them in this unit.
- **Trees, boosting, random forests** (`bias-variance-R.txt` comments): the bias–variance trade-off "in orthogonal directions". Outside this course's syllabus.
- **The same decomposition for classification** (slides 36–50: 0–1 loss, the Bayes classifier and its optimality proof, k-NN with k chosen by 10-fold CV, Bayes error 0.0183 by Monte Carlo): the classification side is [[L02-05-discriminant-analysis]].
- **Ridge and lasso** — buying lower variance with deliberate bias — are Classes 3+4.

---

## Links

- Next: reading the coefficients of the linear learners → [[L02-02-linear-log-linear-regression]]; estimating (21) from data → [[L02-03-cross-validation-motorcycle]].
- Class 1: MSE = variance + bias² for a parameter estimator → [[../L01/L01-05-comparing-estimators-mse-bootstrap|L01 §5]]; OLS, hat matrix, $R^2$, AIC/BIC and overfitting → [[../L01/L01-06-gaussian-linear-regression|L01 §6]].
- Unit: [[L02-07-formulas]] (equations (6), (15), (21), (33)), [[L02-08-pitfalls]], [[L02-09-python]].
- Rules pack: [[../../rules/06_classificacao_validacao|rules/06]] (bias–variance trade-off). Class plan: [[../../Map/class-plan#Class 2: Introduction to statistical learning|Class 2]].
- Reading: ISLP §2.1.1 pp. 17–20, §2.2.1–2.2.2 pp. 28–34; AME §1.4 pp. 9–11, §1.5.2 pp. 22–23 (in Portuguese).
- **Practice:** ISLP Ch. 2 exercises 1 and 3 (p. 63).
