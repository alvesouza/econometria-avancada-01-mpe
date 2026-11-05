---
tags: [notes, lecture-01, ols, gaussian-regression, mle, projection, r2, aic, bic, model-selection, overfitting, robust-se]
date: 2026-10-19
status: taught
source: "multiplelinearregression.pdf pp. 1–22 (slides 4–22: OLS, centring, matrix form, hat matrix, R², adjusted R², Cp, AIC, BIC, best subset, houseprice); normallinearregression-R.txt (Koop–Tobias returns to schooling); overfitting_a_linear_model.html; regressao_abstencao_2026.pdf (20 slides); W §2.2 (pp. 24–32), §3.1–3.3 (pp. 61–81), §4.5 eq. (4.41) (p. 133), §5.1–5.2 (pp. 150–161), §6.3a eqs. (6.21)–(6.22) (p. 181), §8.2 eq. (8.4) (pp. 245–246), App. E (pp. 720–733); AME §1.5.1.1 (p. 21), Ch. 2 (pp. 27–31), §3.1–3.2 (pp. 33–37)"
---

# Gaussian linear regression · OLS as a projection and as an MLE, and why R² cannot choose the model

> **Claim.** **Least squares is a projection**: $\hat\beta=(X'X)^{-1}X'y$ solves the normal equations, and $\hat y=Py$ is the orthogonal projection of $y$ on the columns of $X$. **Add Gaussian errors and the same $\hat\beta$ is the maximum likelihood estimator**; the MLE of $\sigma^2$ divides the residual sum of squares by $n$, the unbiased one by $n-q$. **$R^2$ can only rise as regressors are added, so it cannot select a model**: adjusted $R^2$, $C_p$, AIC and BIC subtract a price per parameter, and out-of-sample error is the honest referee — in the site's Boston example, the model with $R^2_{in}=1.0000$ predicts eleven times worse than the plain one. The municipal-abstention regressions show the whole toolkit read on real output: coefficients, HC1 standard errors, joint $F$ tests and a small $R^2$ gain.
> Prev: [[L01-05-comparing-estimators-mse-bootstrap]] · Next: [[L01-07-ar-var-review]] · Map: [[L01-00-map]]

**Notation.**

| Symbol | Meaning | Range |
|---|---|---|
| $n$ | observations | |
| $p$ | slopes (predictors); deck slide 13 sets $q=p+1$ columns with the intercept | |
| $q$ | columns of $X$ (parameters in $\beta$) | $q\le n$ |
| $y$ | $n\times1$ response | |
| $X$ | $n\times q$ design matrix, full column rank | |
| $\beta$ | $q\times1$ coefficients | |
| $\varepsilon$ | errors, $E(\varepsilon)=0$, $V(\varepsilon)=\sigma^2I$ (Gaussian in §4) | |
| $\hat\beta$, $\hat y=X\hat\beta$, $e=y-\hat y$ | OLS estimate, fitted values, residuals | |
| $P=X(X'X)^{-1}X'$ | hat (projection) matrix | |
| $\mathrm{RSS}=e'e$, $\mathrm{TSS}$ | residual and total sums of squares | |
| $d$ | predictors in a candidate model (§6) | $1\le d\le p$ |
| $\hat\sigma^2$ | error-variance estimate (§4; in §6 from the full model) | |
| $k$ | Wooldridge's slope count ($k=p$) in (6.21)–(6.22) | |

---

## 1 · U — one covariate is rarely enough (slides 4–12)

The deck starts from what the class "already studied": $y_i=\beta_0+\beta_1x_i+\varepsilon_i$ with $E(\varepsilon_i)=0$, $V(\varepsilon_i)=\sigma^2$, $\mathrm{Cov}(x_i,\varepsilon_i)=0$, and OLS estimates

$$\hat\beta_1=\frac{\sum_i(y_i-\bar y)(x_i-\bar x)}{\sum_i(x_i-\bar x)^2},\qquad \hat\beta_0=\bar y-\hat\beta_1\bar x\tag{1}$$

(W §2.2, pp. 24–32). The houseprice data ($n=128$ sales; price, size, offers, bedrooms, bathrooms, brick, neighbourhood) show why one covariate is not the end (slide 11): price on size alone gives $R^2=31\%$ with residual SD 71.4; letting the line shift by brick/non-brick, 47% and 62.1; by neighbourhood, **69% and 48.1**. **The same size–price slope explains far more once the groups it was averaging over are separated** — the multiple-regression idea, "holding other factors fixed" (W §3.1, pp. 61–64).

**Centring and standardising (slide 5).** Replace $y_i,x_i$ by $\tilde y_i=(y_i-\bar y)/s_y$, $\tilde x_i=(x_i-\bar x)/s_x$ with $s^2=\frac1n\sum(\cdot-\text{mean})^2$. The intercept in (1) becomes $\hat\beta_0=0-\hat\beta_1\cdot0=0$, and since $\sum_i\tilde x_i^2=n$,

$$\hat\beta_1=\frac{\sum_i\tilde y_i\tilde x_i}{\sum_i\tilde x_i^2}=\frac{\tilde x'\tilde y}{\tilde x'\tilde x}=\frac1n\sum_i\tilde x_i\tilde y_i=r_{xy}:\tag{2}$$

**on standardised data the slope is the sample correlation**, and its form $(\tilde x'\tilde x)^{-1}\tilde x'\tilde y$ already previews the matrix formula.

---

## 2 · C — matrix form and the normal equations (slides 12–14; W App. E)

Stack the $n$ equations $y_i=\beta_0+\beta_1x_{i1}+\dots+\beta_px_{ip}+\varepsilon_i$:

$$y=X\beta+\varepsilon,\qquad \varepsilon\sim(0,\sigma^2I_n).\tag{3}$$

OLS minimises the residual sum of squares

$$\mathrm{RSS}(\beta)=(y-X\beta)'(y-X\beta)=y'y-2\beta'X'y+\beta'X'X\beta\tag{4}$$

(the two cross terms $\beta'X'y$ and $y'X\beta$ are the same scalar). Slide 14 writes the $\beta$-dependent part, $\beta'X'X\beta-2\beta'X'y$. Differentiate (4), using $\partial(\beta'a)/\partial\beta=a$ and $\partial(\beta'A\beta)/\partial\beta=2A\beta$ for symmetric $A$:

$$\frac{\partial\,\mathrm{RSS}}{\partial\beta}=-2X'y+2X'X\beta\tag{5}$$

Setting (5) to zero gives the **normal equations**

$$X'X\hat\beta=X'y,\tag{6}$$

and, when $X$ has full column rank so that $X'X$ is invertible,

$$\boxed{\;\hat\beta_{ols}=(X'X)^{-1}X'y\;}\tag{7}$$

**It is the global minimum, without second derivatives.** For any $\beta$ write $y-X\beta=(y-X\hat\beta)+X(\hat\beta-\beta)$ and expand:

$$\mathrm{RSS}(\beta)=\mathrm{RSS}(\hat\beta)+2(\hat\beta-\beta)'X'(y-X\hat\beta)+(\hat\beta-\beta)'X'X(\hat\beta-\beta)$$

The middle term is zero by (6) ($X'(y-X\hat\beta)=X'y-X'X\hat\beta=0$), so

$$\mathrm{RSS}(\beta)=\mathrm{RSS}(\hat\beta)+\|X(\hat\beta-\beta)\|^2\ \ge\ \mathrm{RSS}(\hat\beta),\tag{8}$$

with equality only at $\beta=\hat\beta$ (full rank).

### 2.1 · The projection (slide 14)

Substituting (7) into $\hat y=X\hat\beta$:

$$\hat y=X(X'X)^{-1}X'y=Py,\qquad P=X(X'X)^{-1}X'.\tag{9}$$

| Property of $P$ | One-line proof | Meaning |
|---|---|---|
| $P'=P$ | $(X(X'X)^{-1}X')'=X(X'X)^{-1}X'$ | orthogonal (not oblique) projection |
| $PP=P$ | $X(X'X)^{-1}\underbrace{X'X(X'X)^{-1}}_{I}X'=P$ | projecting twice changes nothing |
| $PX=X$ | $X(X'X)^{-1}X'X=X$ | the column space is left fixed |
| $\mathrm{tr}(P)=q$ | $\mathrm{tr}(X(X'X)^{-1}X')=\mathrm{tr}((X'X)^{-1}X'X)=\mathrm{tr}(I_q)$ | $q$ fitted dimensions |

Residuals and their sum of squares (slide 14):

$$e=y-Py=(I-P)y,\qquad X'e=X'(I-P)y=(X'-X')y=0,\tag{10}$$

$$\mathrm{RSS}=e'e=y'(I-P)'(I-P)y=y'(I-P)y,\tag{11}$$

because $I-P$ is also symmetric and idempotent. **(10) says the residuals are orthogonal to every column of $X$**; with an intercept column, they sum to zero (W §2.3, pp. 32–36). Two consequences used in §7 and §8: since $(I-P)X=0$,

$$e=(I-P)(X\beta+\varepsilon)=(I-P)\varepsilon,\tag{12}$$

and the fitted plane passes through the sample means.

> **The geometry to hold: $y$ splits into $Py$ (in the plane spanned by the regressors) plus $(I-P)y$ (perpendicular to it), and OLS is nothing more than dropping the perpendicular.**

---

## 3 · C — sampling properties without normality (W §3.3, §5.1–5.2)

Substituting (3) into (7):

$$\hat\beta=(X'X)^{-1}X'(X\beta+\varepsilon)=\beta+(X'X)^{-1}X'\varepsilon\tag{13}$$

so $E(\hat\beta\mid X)=\beta$ whenever $E(\varepsilon\mid X)=0$ (W Theorem 3.1, §3.3), and

$$V(\hat\beta\mid X)=(X'X)^{-1}X'\,(\sigma^2I)\,X(X'X)^{-1}=\sigma^2(X'X)^{-1}.\tag{14}$$

Consistency and asymptotic normality need only $E(\varepsilon)=0$ and $\mathrm{Cov}(x,\varepsilon)=0$ plus finite moments (W §5.1, pp. 150–154; §5.2, pp. 154–161): **Gaussianity is not what makes OLS work; it is what makes it the MLE and makes small-sample $t$ and $F$ exact.** If $V(\varepsilon\mid X)$ is not $\sigma^2I$, (14) is wrong but (13) still centres on $\beta$ — the robust-SE fix of §8.

---

## 4 · C — Gaussian errors: OLS = MLE (slide 6)

Assume $\varepsilon\sim N(0,\sigma^2I_n)$, so $y\mid X\sim N(X\beta,\sigma^2I_n)$. The log-likelihood is

$$\ell(\beta,\sigma^2)=-\frac n2\log(2\pi)-\frac n2\log\sigma^2-\frac{(y-X\beta)'(y-X\beta)}{2\sigma^2}=-\frac n2\log(2\pi\sigma^2)-\frac{\mathrm{RSS}(\beta)}{2\sigma^2}.\tag{15}$$

**Step 1 — $\beta$.** For every fixed $\sigma^2>0$, $\beta$ enters (15) only through $-\mathrm{RSS}(\beta)/(2\sigma^2)$, which is largest where $\mathrm{RSS}$ is smallest: by (8),

$$\hat\beta_{MLE}=\hat\beta_{ols}.\tag{16}$$

**Step 2 — $\sigma^2$.** Substitute (16) into (15) and differentiate in $\sigma^2$:

$$\frac{\partial\ell}{\partial\sigma^2}=-\frac{n}{2\sigma^2}+\frac{\mathrm{RSS}(\hat\beta)}{2\sigma^4}=0\iff\hat\sigma^2_{MLE}=\frac{\mathrm{RSS}}{n}.\tag{17}$$

**Step 3 — its bias.** By (12), $\mathrm{RSS}=\varepsilon'(I-P)\varepsilon$. A scalar equals its trace, and trace is invariant to cycling:

$$E(\mathrm{RSS})=E\,\mathrm{tr}\big[(I-P)\varepsilon\varepsilon'\big]=\mathrm{tr}\big[(I-P)\,\sigma^2I\big]=\sigma^2\big(n-\mathrm{tr}P\big)=\sigma^2(n-q),\tag{18}$$

using $\mathrm{tr}P=q$ from §2.1. Hence $E(\hat\sigma^2_{MLE})=\sigma^2(n-q)/n<\sigma^2$, and the unbiased estimator is

$$\hat\sigma^2=\frac{\mathrm{RSS}}{n-q}.\tag{19}$$

*(Slide 14 writes $\hat\sigma^2=\varepsilon'\varepsilon/(n-p)$: with slide 13's convention — $y$ centred, intercept dropped, $p$ columns — the divisor is the column count, which is (19).)*

> **"OLS estimates and maximum likelihood estimates are the same. ML is usually more suitable for formal inference. The paid price is more modeling assumptions."** (slide 6). Under (15), $\hat\beta\sim N(\beta,\sigma^2(X'X)^{-1})$ exactly, and $\mathrm{RSS}/\sigma^2\sim\chi^2_{n-q}$ independent of $\hat\beta$ (W §4.1) — which is where exact $t$ and $F$ come from.

The site's companion script `normallinearregression-R.txt` runs this on the Koop–Tobias NLSY data ($N=2{,}178$; log hourly wage on education, potential experience, ability, mother's education): four simple regressions with their adjusted $R^2$ in the titles, the correlation matrix, then `lm(logwage~educ+exper+ability)`. The file reads the data from the web and prints no output, so no numbers are reproduced here; the Python port is in [[L01-11-python]].

---

## 5 · C — $R^2$ and adjusted $R^2$ (slide 15; W §6.3a, p. 181)

$$R^2=1-\frac{\mathrm{RSS}}{\mathrm{TSS}}=1-\frac{y'(I-P)y}{y'y}\tag{20}$$

(slide 15, with $y$ centred so that $\mathrm{TSS}=y'y$): the share of the variance of $y$ explained by the predictors.

**Why it can never fall.** Nest model $M_1$ inside $M_2$ (the columns of $X_1$ are among those of $X_2$). Any $\beta_1$ for $M_1$ is a $\beta_2$ for $M_2$ with the extra coefficients set to zero, so the minimum over the larger set is no larger:

$$\mathrm{RSS}_2=\min_{\beta_2}\|y-X_2\beta_2\|^2\le\min_{\beta_1}\|y-X_1\beta_1\|^2=\mathrm{RSS}_1\ \Longrightarrow\ R^2_2\ge R^2_1.\tag{21}$$

**Adding pure noise cannot lower $R^2$**, and with $q\ge n$ and $\mathrm{rank}\,X=n$, $\hat y=y$ and $R^2=1$.

**Adjusted $R^2$.** Wooldridge replaces both "variances" in (20) by unbiased versions (6.21):

$$\bar R^2=1-\frac{\mathrm{RSS}/(n-k-1)}{\mathrm{TSS}/(n-1)}=1-\frac{\hat\sigma^2}{\mathrm{TSS}/(n-1)},\tag{22}$$

equivalently (6.22):

$$\bar R^2=1-(1-R^2)\,\frac{n-1}{n-k-1}.\tag{23}$$

Slide 15 uses the centred-data version, $1-\frac{y'(I-P)y}{y'y}\cdot\frac{n}{n-p}$; for houseprice "with $n=128$ and $p=6$, $n/(n-6)=1.049$" ($128/122=1.0492$).

**Wooldridge's numbers (p. 181), in (23):** $R^2=0.30$, $n=51$, $k=10$:

$$\bar R^2=1-(1-0.30)\cdot\frac{50}{40}=1-0.70\times1.25=1-0.875=0.125;$$

and $R^2=0.10$ gives $1-0.90\times1.25=-0.125$ — **adjusted $R^2$ can be negative.**

> **An exact fact about the penalty (W, p. 181): adding one regressor raises $\bar R^2$ if and only if its $|t|>1$; adding a group raises it iff the group's $F>1$.** Since $|t|=1$ is nowhere near significance, $\bar R^2$ is a lenient selector — it tends to keep too much (§6's figure).

---

## 6 · C — $C_p$, AIC, BIC and best subset (slides 16–22; AME §1.5.1.1, p. 21)

For a model with $d$ predictors and $\hat\sigma^2$ estimated from the largest model (slide 16):

$$C_p=\frac1n\big(\mathrm{RSS}+2d\hat\sigma^2\big),\qquad \mathrm{AIC}=\frac1{n\hat\sigma^2}\big(\mathrm{RSS}+2d\hat\sigma^2\big),\qquad \mathrm{BIC}=\frac1n\big(\mathrm{RSS}+\log(n)\,d\hat\sigma^2\big).\tag{24}$$

**Read (24) as "training error + price per parameter".** AME (p. 21) writes the same idea as $R(g)\approx\mathrm{EQM}(g)+P(g)$ with $P(g)=2p\hat\sigma^2/n$ (AIC) or $\log(n)p\hat\sigma^2/n$ (BIC). In the deck's Gaussian form AIC is $C_p/\hat\sigma^2$, so the two rank models identically. BIC charges $\log(n)\hat\sigma^2$ per parameter instead of $2\hat\sigma^2$, heavier whenever $\log n>2$, i.e. $n>e^2=7.39$; for houseprice $\log128=4.85$, **so BIC penalises each extra predictor about 2.4 times as hard as $C_p$.**

**Why $2d\hat\sigma^2$ is the right price for $C_p$.** By (18), $E(\mathrm{RSS})=\sigma^2(n-q)$ understates the error a new sample would show, $\sigma^2(n+q)$ (derived in §7), by $2q\sigma^2$: $C_p$ adds that optimism back, so it is an (approximately) unbiased estimate of test error per observation.

**Best subset (slides 17–20).** With $p$ candidates there are $2^p$ models; slide 17 counts "$2^6=64$" for houseprice's six raw variables, while `regsubsets` sees seven columns (neighbourhood becomes the two dummies N1, N2), i.e. $2^7=128$. The exhaustive search keeps the best model of each size (slide 20): size 1 is SqFt; 2 adds Offers; 3 adds Brick; size 4 swaps Offers for the two neighbourhood dummies; 5 restores Offers; 6 adds Bathrooms; 7 adds Bedrooms. **The best models are not nested** (size 4 drops a variable size 3 had), which is why stepwise search can miss them (AME §3.1, pp. 33–35). Slides 21–22 then plot $R^2$, $R^2_{adj}$, $C_p$ and BIC against size: the $R^2$ curve rises with size by (21).

![Three panels against the number of predictors d from 1 to 7 for simulated data with n = 128 and three true predictors: R-squared rises monotonically while adjusted R-squared peaks at d = 5; Cp is minimised at d = 4, essentially tied with d = 3; BIC is minimised at d = 3](figures/L01-r2-vs-criteria.png)
*Figure — best-subset curves on a reproducible simulation (seed 128; n = 128 as houseprice, 7 candidates as in slide 20, 3 with nonzero slopes 1, 0.7, 0.5 and unit noise), each criterion exactly as in (22) and (24); dotted line = chosen size.*

$R^2$ climbs from 0.337 to 0.644 and never turns down — by (21) it cannot. Adjusted $R^2$ peaks at $d=5$ (0.627), keeping two noise predictors, as the $|t|>1$ rule predicts; $C_p$ chooses $d=4$, by a hair over $d=3$ (1.1356 vs 1.1361); **BIC's heavier price picks the true $d=3$ (1.211)**. One simulated data set proves nothing general — but the ordering of the three penalties is exactly what (23)–(24) imply.

---

## 7 · C — overfitting, measured (`overfitting_a_linear_model.html`)

**The experiment.** Boston housing, $n=506$ tracts, response `medv`, $d=13$ standardised predictors, split in halves (253 training, 253 test). Model $M_k$ contains all interactions of up to $k$ distinct predictors, so it has

$$p_k=1+\sum_{j=1}^k\binom{13}{j}\tag{25}$$

coefficients: $p_1=1+13=14$; $p_2=14+78=92$; $p_3=92+286=378$; $p_4=378+715=1093$; $p_5=1093+1287=2380$. From $k=3$ on, $p>n=253$: $X'X$ is singular, and the page uses a ridge solve with $\lambda=0.001$ purely so the linear system has a solution ("not to regularize in any meaningful way"; the ridge estimator itself is Classes 3+4).

| $k$ | $p$ | $R^2_{in}$ | RMSE$_{in}$ | MAD$_{in}$ | $R^2_{out}$ | RMSE$_{out}$ | MAD$_{out}$ |
|---|---|---|---|---|---|---|---|
| 1 | 14 | 0.7303 | 4.97 | 3.51 | 0.7469 | 4.48 | 3.41 |
| 2 | 92 | 0.9307 | 2.52 | 1.82 | 0.5854 | 6.83 | 4.06 |
| 3 | 378 | 0.9946 | 0.70 | 0.36 | 0.1407 | 25.41 | 13.66 |
| 4 | 1093 | 0.9998 | 0.13 | 0.05 | 0.1381 | 36.82 | 16.02 |
| 5 | 2380 | 1.0000 | 0.03 | 0.01 | 0.0519 | 47.13 | 16.71 |

**Why the gap opens — the page's formulas, derived.** Fix $X$, assume the linear model is correct with $p<n$ columns.

*In sample.* By (18), $E(\mathrm{RSS})=\sigma^2(n-p)$, so

$$E(\mathrm{MSE}_{in})=\frac{E(\mathrm{RSS})}{n}=\sigma^2\Big(1-\frac pn\Big).\tag{26}$$

*Out of sample* (new errors $\varepsilon^*$ at the same design): the prediction error is $y^*-X\hat\beta=X\beta+\varepsilon^*-X\beta-P\varepsilon=\varepsilon^*-P\varepsilon$, using (13). Since $\varepsilon^*$ and $\varepsilon$ are independent,

$$E\|\varepsilon^*-P\varepsilon\|^2=E\|\varepsilon^*\|^2+E(\varepsilon'P'P\varepsilon)=n\sigma^2+\sigma^2\,\mathrm{tr}P=\sigma^2(n+p),$$

$$E(\mathrm{MSE}_{out})=\sigma^2\Big(1+\frac pn\Big).\tag{27}$$

**Subtracting (26) from (27): the training error is optimistic by $2\sigma^2p/n$, linear in the number of parameters** (for random designs the page notes the out-of-sample error blows up like $\sigma^2(n-1)/(n-p-1)$ as $p\to n$).

**Reading the table.** $M_1$ is honest: RMSE 4.97 in vs 4.48 out (the test half happens to be easier — (26)–(27) are expectations, and one split is one draw). $M_2$ already loses out of sample (6.83) while $R^2_{in}$ jumps to 0.931. From $M_3$ the training data are interpolated and the test RMSE explodes to 47.13 — **$47.13/4.48=10.5$, "roughly 11 times worse than the simplest model"**, with $R^2_{out}=0.052$.

![Two panels across interaction orders k = 1 to 5: training RMSE falls from 4.97 to 0.03 while test RMSE rises from 4.48 to 47.13 on a log scale; in-sample R-squared climbs to 1.0000 while out-of-sample R-squared falls from 0.747 to 0.052, with the p > n region shaded](figures/L01-overfitting-train-test.png)
*Figure — the page's table plotted: in-sample vs out-of-sample RMSE (log scale) and $R^2$; shaded where $p>n=253$. Source: `overfitting_a_linear_model.html`, table "In-sample versus out-of-sample performance".*

The two lines cross between $k=1$ and $k=2$ and then diverge for good: every coefficient beyond the first fourteen fits noise that is not in the test half. The right panel is the page's headline — **"The 'holy grail' $R^2=1$ is reached exactly where prediction collapses."** Class 2 turns this into a procedure (validation set, $k$-fold CV, LOOCV): [[../L02/L02-03-cross-validation-motorcycle|L02 §3]].

---

## 8 · Worked — municipal abstention in the 2026 presidential first round (`regressao_abstencao_2026.pdf`)

**Data and model (slides 1, 7–8).** Unit: municipality, 5,565 of 5,570 (five created in 2013 lack IDHM 2010). Response $y_i$ = "% de abstenção no 1º turno de 2026" (preliminary ballot-box totals of 05/10). Specification (slide 8):

$$y_i=\alpha+\beta_1\,\mathrm{Abst22}_i+\beta_2\,\mathrm{BN26}_i+\beta_3\,\mathrm{IDHM}_i+\sum_{r\ne SE}\gamma_rD^{reg}_{ri}\ \Big(\text{or}\ \sum_{s\ne SP}\delta_sD^{UF}_{si}\Big)+\sum_{k\ne\le10\text{mil}}\theta_kD^{porte}_{ki}+\varepsilon_i\tag{28}$$

"IDHM em décimos ($\beta_3$ = efeito de +0,1). MQO com erros-padrão HC1." References: Sudeste, SP, municipalities up to 10 thousand eligible voters ("aptos"). Models: (0) no dummies; (1) region; (2) UF; (3) region + size ("porte"); (4) UF + size.

**The results table (slide 11), coefficient (HC1 SE):**

| | (0) | (1) Região | (2) UF | (3) Região+porte | (4) UF+porte |
|---|---|---|---|---|---|
| Intercepto | −2.200 (0.354) | 9.025 (0.555) | 5.578 (0.641) | 9.817 (0.638) | 7.378 (0.756) |
| % Abstenção 2022 | 0.717 (0.007) | 0.649 (0.008) | 0.686 (0.009) | 0.651 (0.008) | 0.684 (0.009) |
| % Brancos+Nulos 2026 | 0.225 (0.024) | 0.286 (0.026) | 0.228 (0.030) | 0.276 (0.026) | 0.196 (0.031) |
| IDHM 2010 (+0,1) | 1.013 (0.042) | −0.356 (0.064) | −0.010 (0.069) | −0.473 (0.076) | −0.246 (0.085) |
| 10 a 45 mil aptos | | | | −0.130 (0.067) | 0.069 (0.067) |
| 45 a 100 mil aptos | | | | 0.225 (0.107) | 0.439 (0.112) |
| 100 a 500 mil aptos | | | | 0.635 (0.140) | 0.960 (0.152) |
| Acima de 500 mil aptos | | | | 1.005 (0.304) | 1.140 (0.317) |
| $R^2$ | 0.682 | 0.727 | 0.755 | 0.728 | 0.757 |
| $R^2$ ajustado | 0.682 | 0.727 | 0.754 | 0.728 | 0.756 |

(Region coefficients in (1)/(3): Norte −1.872/−1.959, Nordeste −2.750/−2.821, Sul −0.271/−0.236, Centro-Oeste 0.693/0.687.) Decimal commas of the slide are written as points here.

### 8.1 · Persistence — a coefficient, its $t$ and its interval

"1 p.p. de abstenção em 2022 se traduz em 0,65–0,72 p.p. em 2026" (slide 13). In model (4):

$$t=\frac{0.684}{0.009}=76.0,\qquad 0.684\pm1.96\times0.009=0.684\pm0.018=[0.666,\ 0.702].$$

The interval excludes 1 by a wide margin: **abstention persists but regresses toward the mean** — a municipality 10 p.p. above average in 2022 is expected about 6.8 p.p. above in 2026, other regressors fixed.

**A check on the arithmetic of OLS.** With an intercept, (10) makes the fitted plane pass through the sample means (slide 7: 20.72, 21.27, 4.45, IDHM 0.659 → 6.59 in tenths). Model (0) at the means:

$$-2.200+0.717(21.27)+0.225(4.45)+1.013(6.59)=-2.200+15.251+1.001+6.676=20.728\approx20.72\ \checkmark$$

### 8.2 · IDHM changes sign: omitted-variable bias in action

| Model | (0) | (1) | (2) | (3) | (4) |
|---|---|---|---|---|---|
| IDHM (+0,1) | 1.01 | −0.36 | −0.01 | −0.47 | −0.25 |

In (0), IDHM proxies for *where* a municipality is: the Nordeste combines low IDHM with low abstention (−2.75 p.p. in (1)), so across Brazil higher IDHM goes with higher abstention. Once region dummies absorb that, the within-region association is negative. The omitted-variable bias formula (W §3.3, pp. 73–81) gives the sign: bias $=(\text{effect of omitted variable})\times(\text{slope of omitted on included})$. **Size works the same way:** "Cidades grandes têm IDHM alto; separando o porte, o IDHM volta a ter efeito negativo" (slide 13) — size raises abstention ($\theta_k>0$) and correlates positively with IDHM, so omitting it biases $\beta_3$ upward: −0.010 in (2) becomes −0.246 in (4).

### 8.3 · Size: individual $t$s and the joint test

Model (4), relative to municipalities up to 10 thousand voters (slide 12):

| Size | Coef. | SE | $t$ | 95% interval |
|---|---|---|---|---|
| 10–45 mil | 0.069 | 0.067 | 1.03 | [−0.062, 0.200] |
| 45–100 mil | 0.439 | 0.112 | 3.92 | [0.219, 0.659] |
| 100–500 mil | 0.960 | 0.152 | 6.32 | [0.662, 1.258] |
| > 500 mil | 1.140 | 0.317 | 3.60 | [0.519, 1.761] |

"+0,07 p.p. (não significativo)" is the first row: $|t|=1.03<1.96$. **Conditional on 2022 abstention, the gradient in size appears although the raw means by size are flat (20.0%–21.1%, slide 5).** The joint robust Wald test that all four are zero gives $F=13.22$ with UF and $10.84$ with region, $p<0.0001$ (the 5% critical value of $F_{4,5531}$ is 2.37).

**Is $F=13.22$ consistent with the $R^2$ gain?** Under homoskedasticity the $R^2$ form (W (4.41), p. 133) with $q=4$ restrictions, $34$ parameters and $n-34=5531$ residual df:

$$F=\frac{(R^2_{ur}-R^2_r)/q}{(1-R^2_{ur})/(n-34)}=\frac{(0.757-0.755)/4}{(1-0.757)/5531}=\frac{0.000500}{0.0000439}=11.4$$

Since each $R^2$ is rounded to three decimals, $R^2_{ur}-R^2_r$ lies anywhere in $[0.001,0.003]$ and the formula in $[5.7,\ 17.1]$: **the robust 13.22 sits inside what the printed $R^2$s allow.** (The robust statistic need not equal the $R^2$ form; the two coincide only under homoskedasticity.)

**And with the adjusted $R^2$.** (23) with $k=29$ slopes for (2) and $k=33$ for (4):

$$\bar R^2_{(2)}=1-0.245\cdot\frac{5564}{5535}=1-0.24628=0.754,\qquad \bar R^2_{(4)}=1-0.243\cdot\frac{5564}{5531}=1-0.24445=0.756,$$

reproducing slide 11. The rise matches Wooldridge's rule: the size group's $F>1$, so $\bar R^2$ must go up. **"O ganho de ajuste é pequeno (R² ajustado de 0,754 para 0,756): a abstenção passada já captura quase tudo"** — a variable can be highly significant and add almost nothing to fit; significance and explanatory share are different questions.

### 8.4 · UF or region? A test of 22 restrictions (slide 15)

The region model is the UF model with all UFs of a region forced to share one coefficient: 26 UF dummies collapse to 4 region dummies, **$26-4=22$ linear restrictions**. Robust Wald: $F=31.08$ (without size, (1) vs (2)) and $F=32.09$ (with size, (3) vs (4)), both $p<0.0001$: rejected — e.g. in the Centro-Oeste MS and GO are positive, MT negative.

### 8.5 · HC1 standard errors and the caveats

HC1 is White's heteroskedasticity-robust variance (W (8.4), pp. 245–246) times the degrees-of-freedom factor $n/(n-k-1)$ mentioned on p. 246:

$$\hat V_{HC1}(\hat\beta)=\frac{n}{n-q}\,(X'X)^{-1}\Big(\sum_{i=1}^n e_i^2\,x_ix_i'\Big)(X'X)^{-1}\tag{29}$$

— (14) with $\sigma^2I$ replaced by $\mathrm{diag}(e_i^2)$. It is the `vcovHC(m, type = "HC1")` of the slides' R code.

The deck's own "Ressalvas" (slide 17), each a lesson in reading a regression: 2026 data are preliminary; IDHM is from 2010; "Brancos+nulos de 2026 é determinado junto com a abstenção, então o coeficiente descreve associação" (not a causal effect); all municipalities weigh the same (an electorate-weighted version would favour large cities); and **errors may be correlated within UF — with 27 clusters, UF-clustered SEs "seriam uma verificação natural"**, since HC1 handles heteroskedasticity, not within-cluster correlation.

---

## 9 · G — named, not developed

- **Gauss–Markov** (W §3.5, pp. 89–90): under $V(\varepsilon)=\sigma^2I$, OLS has the smallest variance among linear unbiased estimators — §12.1 of [[L01-05-comparing-estimators-mse-bootstrap]] (equal weights beat triangular ones) is its one-parameter case.
- **Shrinkage**: ridge, lasso, elastic net, normal–gamma and horseshoe priors — the later pages of the same deck, after the best-subset and Credit examples — trade bias for variance exactly as §8 of the previous note did for $c\,x_{(n)}$. **Classes 3+4.**
- **OLS as the best linear predictor** even when $E(y\mid x)$ is not linear (AME Ch. 2, pp. 27–31; Teorema 2): $\hat\beta\to\beta^*=\arg\min E[(Y-\beta'X)^2]$.

---

## Links

- Neighbours: [[L01-05-comparing-estimators-mse-bootstrap]] (MSE = variance + bias²) · [[L01-07-ar-var-review]] (the AR(p) is this regression with lagged $y$ as regressors).
- Unit: [[L01-00-map]] · [[L01-09-formulas]] · [[L01-10-pitfalls]] · [[L01-11-python]] · [[L01-08-p-hacking-evidence]] (specification search on regressions like §8's).
- Class 2: [[../L02/L02-01-prediction-error-bias-variance|L02 §1]] (bias–variance behind (26)–(27)) · [[../L02/L02-02-linear-log-linear-regression|L02 §2]] (reading level/log coefficients) · [[../L02/L02-03-cross-validation-motorcycle|L02 §3]] (CV and the LOOCV hat-matrix shortcut, which uses $P$ from §2.1).
- Rules: [[../../rules/06_classificacao_validacao|rules/06]] (validation, model selection); [[../../rules/01_endogeneidade_iv|rules/01]] (omitted-variable bias, §8.2).
- **Practice (number and printed page only):** W 11.C8 (p. 370) uses this regression with a lagged regressor; I 3.7 (p. 129), I 3.9 (pp. 129–130).
