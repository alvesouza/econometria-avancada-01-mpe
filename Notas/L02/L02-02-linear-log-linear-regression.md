---
tags: [notes, lecture-02, linear-regression, functional-form, log-linear, elasticity, interactions]
date: 2026-10-19
status: taught
source: "multiplelinearregression.pdf slides 17 (houseprice units), 29 (top models with interactions), 44 (Credit best model); capm-regression-R.txt; salaries-for-professors.txt; regressaomultipla-return-to-education.html (Mroz data, log family income); Wooldridge 6e §2.4 (pp. 36–40: eqs. 2.39–2.46, Examples 2.10–2.11, Table 2.3), §6.2 (pp. 171–178: eqs. 6.6–6.13, 6.17, Example 6.2); ISLP §3.3.1 p. 91 (Credit units)"
---

# W §2.4, §6.2 · Reading a linear regression: levels, logs, elasticities and interactions

> **Claim.** "Linear" regression is linear in the **parameters**, not in the variables, so logs,
> squares and products of the regressors are all fitted by the same OLS. What changes is the
> **reading** of a coefficient: a unit change (level-level), an approximate percentage
> (log-level: $100\beta$), an elasticity (log-log: $\beta$), or a slope that depends on another
> variable (interactions, quadratics). **The $100\beta$ reading is a first-order approximation; the
> exact change is $100(e^{\beta\Delta x}-1)$, and the gap is already 5 points at $\beta=0.306$.**
> Prev: [[L02-01-prediction-error-bias-variance]] · Next: [[L02-03-cross-validation-motorcycle]] · Map: [[L02-00-map]]

**Notation.**

- $y$ response, $x_1,\dots,x_k$ regressors, $u$ error with $E[u\mid x]=0$; $\beta_0,\dots,\beta_k$ population coefficients, $\hat\beta_j$ OLS estimates.
- $\Delta$ a discrete change; $\%\Delta y=100\,\Delta y/y$ a percentage change; "ceteris paribus" = all other regressors and $u$ held fixed ($\Delta u=0$).
- $\log$ is the natural log throughout (W's convention).
- $s_y,s_{x_j}$ sample standard deviations; a superscript $^*$ marks a standardised variable $(v-\bar v)/s_v$.
- Dummies: $D=1$ for the named category, $0$ for the base category.

---

## 1 · U — "linear" means linear in $\beta$

The model $y=\beta_0+\beta_1x+u$ is *linear* because it is linear in $\beta_0,\beta_1$; nothing stops
$y$ or $x$ from being $\log(\text{wage})$, $\sqrt{\text{inc}}$, $x^2$ or $x_1x_2$ (W §2-4c, p. 40). The
mechanics of OLS — $\hat\beta=(X'X)^{-1}X'y$ from [[../L01/L01-06-gaussian-linear-regression|L01 §6]] —
do not care how the columns of $X$ were built.

> **The mechanics are free; the interpretation is not.** W p. 40: *"it is much more important to
> become proficient at interpreting coefficients than to become efficient at computing formulas."*
> The same fact is what makes polynomial regression a linear model
> ([[L02-03-cross-validation-motorcycle]] §2).

---

## 2 · C — level-level: a coefficient is a slope in the variables' own units

For $y=\beta_0+\beta_1x_1+\dots+\beta_kx_k+u$, holding the other regressors and $u$ fixed,

$$\Delta y=\beta_j\,\Delta x_j. \tag{1}$$

**Units move the coefficient, never the fit** (W §2-4a, pp. 36–37). If $x_j$ is replaced by
$c\,x_j$, (1) stays true only if the slope becomes $\beta_j/c$; if $y$ is replaced by $c\,y$, every
coefficient is multiplied by $c$. $R^2$ is unchanged. W's own case: the CEO-salary slope on
$roe$ is $18.501$ (eq. 2.39, salary in thousand dollars per percentage point) and on
$roedec=roe/100$ it is $1{,}850.1$ (eq. 2.41, p. 37) — dividing $x$ by 100 multiplied the slope by 100.

### 2.1 · Worked — the Credit best model (multiplelinearregression.pdf slide 44)

$$\widehat{\text{Balance}}=-499.7-7.84\,\text{Income}+0.267\,\text{Limit}+23.18\,\text{Cards}+429.6\,\text{Student}, \tag{2}$$

$n=400$, residual standard error $99.56$ on $395$ df, $R^2=0.9536$, adjusted $R^2=0.9531$.
Balance is the average credit-card debt in dollars; Income is in **thousands** of dollars
(ISLP §3.3.1, p. 91).

| Coefficient | Reading by (1), others held fixed |
|---|---|
| Income $-7.839$ | \$1,000 more income goes with \$7.84 *less* balance |
| Limit $0.2666$ | each extra dollar of credit limit goes with \$0.27 more balance |
| Cards $23.18$ | one more card: \$23.18 more balance |
| Student $429.6$ (dummy) | a student carries \$429.6 more balance than a non-student with the same income, limit and cards |

**Check the printout's own arithmetic.** The $t$-statistic is the estimate over its standard error:

$$t_{\text{Student}}=\frac{429.6}{16.61}=25.86\ \checkmark,\qquad t_{\text{Cards}}=\frac{23.18}{3.639}=6.37\ \checkmark \tag{3}$$

and adjusted $R^2=1-(1-R^2)\frac{n-1}{n-k-1}$ with $k=4$:

$$\bar R^2=1-(1-0.9536)\,\frac{399}{395}=1-0.0464\times1.010127=1-0.04687=0.9531\ \checkmark \tag{4}$$

### 2.2 · Worked — rescaling in the houseprice data (slides 17 and 29)

Slide 17 converts the data before fitting: square feet to m² (`SqFt*0.092903`) and price from US
dollars to **thousand reais** (`Price*3.2/1000`). The six-variable model of slide 29 has
$\hat\beta_{\text{size}}=1.886008$: **R\$1,886 per extra m²**, other regressors fixed. Undoing the
conversion with the rule under (1): since $\text{m}^2=0.092903\,\text{sqft}$, the slope per square
foot is

$$\hat\beta_{\text{sqft}}=0.092903\times1.886008=0.17522\ \text{thousand R\$}=\text{R\$}175.2\ \text{per sqft}, \tag{5}$$

and at 3.2 reais per dollar that is $175.22/3.2=\$54.75$ per square foot.

**The CAPM regressions** (`capm-regression-R.txt`) are level-level too: monthly *excess* returns of
the food, durables and construction industries on the market's excess return (Ecdat `Capm`, 516
months, 1960–2002). There $\beta$ reads "percentage points of industry excess return per
percentage point of market excess return", and the intercept is the pricing error $\alpha$. The
script prints no output, so there are no numbers to work here; its conjugate-prior part belongs
to Classes 3+4.

---

## 3 · C — interactions: the slope of one variable depends on another

With an interaction (W §6-2c, pp. 177–178, eq. 6.17),

$$y=\beta_0+\beta_1x_1+\beta_2x_2+\beta_3x_1x_2+u\quad\Longrightarrow\quad \frac{\Delta y}{\Delta x_2}=\beta_2+\beta_3x_1. \tag{6}$$

**$\beta_2$ alone is the effect of $x_2$ at $x_1=0$** — often meaningless (W's example: the effect of a
bedroom on a house of zero square feet). Report (6) at interesting values of $x_1$, or centre $x_1$
at its mean before forming the product so that $\beta_2$ becomes the effect at the mean (W p. 178).

**When $x_1$ is a dummy, (6) gives two slopes.** `salaries-for-professors.txt` fits the full model
`salary ~ sex.dum*yrs.service` (salary in thousand dollars, `sex.dum` = 1 for men):

$$E[\text{salary}\mid\text{male},\text{yrs}]=\beta_0+\beta_1\,\text{male}+\beta_2\,\text{yrs}+\beta_3\,\text{male}\cdot\text{yrs}, \tag{7}$$

$$\frac{\partial E[\text{salary}]}{\partial\,\text{yrs}}=\begin{cases}\beta_2 & \text{women}\\ \beta_2+\beta_3 & \text{men}\end{cases},\qquad \text{gap}(\text{yrs})=E[\cdot\mid\text{male}]-E[\cdot\mid\text{female}]=\beta_1+\beta_3\,\text{yrs}. \tag{8}$$

So $\beta_1$ is the gender gap **at zero years of service**, and $\beta_3$ is how much the gap widens
per year. The reduced model `salary ~ sex.dum + yrs.service` forces $\beta_3=0$: parallel lines, one
constant gap. The script prints no estimates; it compares the two models by a Bayes factor
(Classes 3+4).

### 3.1 · Worked — the seven-variable houseprice model (slide 29)

`coef(regs,7)` includes `sizeN2` $=-0.3614412$ and `sizebrick` $=0.2907379$ with
$\hat\beta_{\text{size}}=1.9374668$. By (6), the price of one more m² (thousand R\$) is
$1.9375-0.3614\,N2+0.2907\,\text{brick}$:

| | not brick | brick |
|---|---|---|
| **not neighbourhood 2** | $1.9375$ | $1.9375+0.2907=2.2282$ |
| **neighbourhood 2** | $1.9375-0.3614=1.5760$ | $1.9375-0.3614+0.2907=1.8668$ |

> **One coefficient per row of the printout, but four different "effects of size".** A square metre
> is worth R\$2,228 in a brick house outside N2 and R\$1,576 in a non-brick house in N2.

---

## 4 · C — log-level: $100\beta$ is a semi-elasticity, and an approximation

**Model** (W eq. 2.42, p. 37):

$$\log y=\beta_0+\beta_1x+u. \tag{9}$$

**Step 1.** Two values of $x$, same $u$; subtract the two versions of (9):

$$\log y_1-\log y_0=\beta_1(x_1-x_0)=\beta_1\Delta x. \tag{10}$$

**Step 2 — exact.** Exponentiate (10): $y_1/y_0=e^{\beta_1\Delta x}$, so

$$\%\Delta y=100\Big(\frac{y_1}{y_0}-1\Big)=100\big(e^{\beta_1\Delta x}-1\big). \tag{11}$$

**Step 3 — approximate.** For small $z$, $e^z=1+z+z^2/2+\dots\approx1+z$. Substituting
$z=\beta_1\Delta x$ into (11):

$$\%\Delta y\approx100\,\beta_1\Delta x, \tag{12}$$

W's eq. (2.43); $100\beta_1$ is the **semi-elasticity** of $y$ with respect to $x$. Eq. (11) is W's
(6.8), p. 171; with $\Delta x=1$ it is (6.9). The error of (12) is about $100z^2/2$: negligible for
$|z|\le0.05$, five points at $z=0.3$.

### 4.1 · Worked — W's own numbers, approximate vs exact

| Source | $\hat\beta\,\Delta x$ | (12): $100\hat\beta\Delta x$ | (11): $100(e^{\hat\beta\Delta x}-1)$ |
|---|---|---|---|
| Ex. 2.10, $\log(\text{wage})=0.584+0.083\,\text{educ}$ ($n=526$, $R^2=0.186$), one more year | $0.083$ | $8.3\%$ | $100(e^{0.083}-1)=8.65\%$ |
| (6.7) $\log(\text{price})=9.23-0.718\log(\text{nox})+0.306\,\text{rooms}$, one more room | $0.306$ | $30.6\%$ | $100(e^{0.306}-1)=35.8\%$ |
| same, one *fewer* room ($\Delta x=-1$) | $-0.306$ | $-30.6\%$ | $100(e^{-0.306}-1)=-26.4\%$ |
| stratio coefficient $-0.052$, $+1$ | $-0.052$ | $-5.2\%$ | $100(e^{-0.052}-1)=-5.1\%$ |
| same, $+5$ | $-0.260$ | $-26\%$ | $100(e^{-0.26}-1)=-22.9\%$ |

(W pp. 38, 171–172.) Note the room row: **the approximation $30.6\%$ always lies between the exact
decrease ($26.4\%$) and the exact increase ($35.8\%$)** — it is the symmetric, "arc" version (W p. 172).

![Left: percentage change in y against the change in log y from minus 0.8 to 0.8; the exact curve 100(e^z minus 1) lies above the straight approximation 100z on both sides, with W's points marked: education 8.7%, one more room 35.8%, one fewer room minus 26.4%, five more students per teacher minus 22.9%. Right: percentage change in salary against percentage change in sales for elasticity 0.257; the exact curve bends below the straight approximation, 2.48% versus 2.57% at plus 10%.](figures/L02-log-linear-readings.png)
*Exact (11) vs approximation (12) at W's coefficients (eqs. 2.44, 6.7, pp. 38, 171–172), and the log-log analogue (16) at W's elasticity 0.257 (eq. 2.46, p. 39).*

The vertical gaps on the left are the error of reading $100\beta$: invisible at $\beta=0.083$,
five points at $0.306$. Exact changes are asymmetric — up 35.8%, down 26.4% for the same
$|\Delta\text{rooms}|$ — because a log-linear model is multiplicative in $y$.

**Three cautions.** (i) *Not* "log(wage) rises by 8.3%": the log rises by 0.083 (W p. 38).
(ii) Rescaling $y$ (dollars to thousands) changes only the intercept by $\log c$, never the slope
(W p. 39). (iii) $R^2$ from a regression of $\log y$ cannot be compared with one of $y$ — they
explain the variation of different variables (W p. 173).

> **G — what (11) is a change of.** With $u$ held fixed, (11) is the change in $e^{\beta_0+\beta_1x+u}$,
> i.e. in the median of $y$ when $u$ is symmetric. If $u$ is independent of $x$,
> $E[y\mid x]=e^{\beta_0+\beta_1x}E[e^u]$ and the ratio $E[y\mid x_1]/E[y\mid x_0]=e^{\beta_1\Delta x}$ is
> the same, so (11) also holds for the mean. Plugging $\hat\beta$ into (11) is consistent but not
> unbiased, since $\exp$ is non-linear (W p. 171).

---

## 5 · C — log-log and level-log

**Log-log** (W eq. 2.45, p. 39): $\log y=\beta_0+\beta_1\log x+u$. Differencing as in (10),

$$\Delta\log y=\beta_1\,\Delta\log x\quad\Longrightarrow\quad \beta_1=\frac{d\log y}{d\log x}=\frac{dy/y}{dx/x}, \tag{13}$$

the **elasticity** of $y$ with respect to $x$. Using $\Delta\log v\approx\%\Delta v/100$ on both sides of (13):

$$\%\Delta y\approx\beta_1\,\%\Delta x. \tag{14}$$

Exactly, exponentiating (13): $y_1/y_0=(x_1/x_0)^{\beta_1}$, so

$$\%\Delta y=100\Big[\Big(1+\frac{\%\Delta x}{100}\Big)^{\beta_1}-1\Big]. \tag{15}$$

**Worked — W Example 2.11** (p. 39): $\widehat{\log(\text{salary})}=4.822+0.257\log(\text{sales})$, $n=209$,
$R^2=0.211$. A 1% rise in sales goes with a $0.257\%$ rise in CEO salary. For a 10% rise, (14) gives
$0.257\times10=2.57\%$ and (15) gives

$$100\big(1.10^{0.257}-1\big)=100(1.024797-1)=2.48\%. \tag{16}$$

**Level-log**: $y=\beta_0+\beta_1\log x+u$ gives $\Delta y=\beta_1\Delta\log x\approx(\beta_1/100)\,\%\Delta x$.

**W Table 2.3** (p. 39), the summary to keep:

| Model | Dependent | Independent | Interpretation of $\beta_1$ |
|---|---|---|---|
| Level-level | $y$ | $x$ | $\Delta y=\beta_1\Delta x$ |
| Level-log | $y$ | $\log(x)$ | $\Delta y=(\beta_1/100)\%\Delta x$ |
| Log-level | $\log(y)$ | $x$ | $\%\Delta y=(100\beta_1)\Delta x$ |
| Log-log | $\log(y)$ | $\log(x)$ | $\%\Delta y=\beta_1\%\Delta x$ |

**When to log** (W pp. 172–173): positive money amounts and large counts usually; years
(education, experience, age) usually not; proportions either way — and then a "percentage" change
(log) must not be confused with a "percentage point" change (level): unemployment from 8 to 9 is
one point, $12.5\%$, and $\log9-\log8=0.118$.

---

## 6 · C — Worked: the site's log-family-income regression (Mroz data)

`regressaomultipla-return-to-education.html` (Lopes, 5/30/2023) uses Mroz's 1975 PSID sample of
$n=753$ married women and fits

$$y^*=\sum_{j=1}^{18}\beta_j^*x_j^*+e,\qquad y^*=\frac{\log(\text{FAMINC})-\overline{\log\text{FAMINC}}}{s_y},\quad x_j^*=\frac{x_j-\bar x_j}{s_{x_j}}, \tag{17}$$

by `lm(y~X-1)` — no intercept, because every variable has mean zero.

**Reading a standardised log-level coefficient.** Undo the standardisation in (17):

$$\log(\text{FAMINC})=\overline{\log\text{FAMINC}}+s_y\sum_j\beta_j^*\frac{x_j-\bar x_j}{s_{x_j}}+s_ye\quad\Longrightarrow\quad\frac{\partial\log(\text{FAMINC})}{\partial x_j}=\beta_j^*\,\frac{s_y}{s_{x_j}}. \tag{18}$$

So $\beta_j^*$ reads "**one standard deviation more of $x_j$ goes with $\beta_j^*$ standard deviations more
of log family income**", and the semi-elasticity per unit of $x_j$ is $100\beta_j^*s_y/s_{x_j}$ by (12).
The page does not print $s_y$ or $s_{x_j}$ (and the data are not in the repo), so the percentage
reading cannot be completed from the page — the SD reading is the one available.

| Regressor | $\hat\beta^*$ | SE | $t$ | Reading |
|---|---|---|---|---|
| MTR (wife's marginal tax rate) | $-0.7119$ | $0.0329$ | $-21.64$ | by far the strongest association; but tax rates are computed from income, so this is a predictive association, not an effect |
| HW (husband's wage) | $0.1476$ | $0.0320$ | $4.62$ | +1 SD of husband's wage, +0.148 SD of log family income |
| WHRS (wife's hours) | $0.1323$ | $0.0285$ | $4.65$ | |
| WE (wife's education) | $-0.0053$ | $0.0238$ | $-0.22$ | no association **holding the wife's wage, hours and the other 15 fixed** |

> **The page's "return to education" is nil — because of what is held fixed.** Education works
> partly *through* the wife's wage (WW) and hours, which are in the regression; conditioning on
> them removes that channel. Which controls are legitimate is a Classes 5+6 question (bad controls).

**Check the printout** (residual SE $0.4511$ on $735$ df, $R^2=0.8011$, adjusted $0.7962$).

$t$ for MTR: $-0.711872/0.032891=-21.64$ ✓. The residual sum of squares and, because
$y^*$ has mean 0 and variance 1, the total sum of squares $\sum y_i^{*2}=n-1=752$:

$$\text{RSS}=735\times0.4511^2=735\times0.203491=149.57,\qquad R^2=1-\frac{149.57}{752}=1-0.19889=0.8011\ \checkmark \tag{19}$$

R's no-intercept adjusted $R^2$ uses $n$ and $n-p$ with $p=18$:

$$\bar R^2=1-(1-0.8011)\,\frac{753}{735}=1-0.1989\times1.02449=1-0.20377=0.7962\ \checkmark \tag{20}$$

The page's "MLE" standard errors use $\hat\sigma^2_{\text{MLE}}=\text{RSS}/n$ instead of $\text{RSS}/(n-p)$,
so each is the OLS one times $\sqrt{735/753}=0.98798$: for LFP, $0.029839\times0.98798=0.029480$,
the printed $0.02947983$ ✓ (the MLE of $\sigma^2$ is the biased one, [[../L01/L01-06-gaussian-linear-regression|L01 §6]]).

The rest of the page (prior predictive densities $-2253.0$, $-2107.2$, $-2015.1$ and log Bayes
factors $145.8$, $238.0$, $92.1$ selecting LFP, WHRS, K618, HW, MTR) is Bayesian model
comparison: Classes 3+4.

---

## 7 · C — quadratics: a slope that changes with $x$

$y=\beta_0+\beta_1x+\beta_2x^2+u$ (W eq. 6.10, p. 173). The slope is not $\beta_1$:

$$\frac{\Delta\hat y}{\Delta x}\approx\hat\beta_1+2\hat\beta_2x, \tag{21}$$

zero at the turning point

$$x^*=\Big|\frac{\hat\beta_1}{2\hat\beta_2}\Big|. \tag{22}$$

**Worked** (W pp. 174–176). Wage on experience, $\hat\beta_1=0.298$, $\hat\beta_2=-0.0061$ (eq. 6.12):
$x^*=0.298/(2\times0.0061)=0.298/0.0122=24.4$ years. Example 6.2, $\log(\text{price})$ with
$\hat\beta_{\text{rooms}}=-0.545$, $\hat\beta_{\text{rooms}^2}=0.062$: $x^*=0.545/0.124=4.4$ rooms, and by (21)
and (12)

$$\%\Delta\text{price}\approx100\big[-0.545+2(0.062)\,\text{rooms}\big]\Delta\text{rooms}=(-54.5+12.4\,\text{rooms})\,\Delta\text{rooms}, \tag{23}$$

$=-54.5+12.4(5)=7.5\%$ from five to six rooms and $-54.5+12.4(6)=19.9\%$ from six to seven.

> **A quadratic is a degree-2 polynomial regression.** Raising the degree buys flexibility and,
> by [[L02-01-prediction-error-bias-variance]], variance; choosing the degree from data is
> [[L02-03-cross-validation-motorcycle]].

---

## Links

- Prev: the prediction view of the same models → [[L02-01-prediction-error-bias-variance]]; next: polynomial degree by cross-validation → [[L02-03-cross-validation-motorcycle]].
- Class 1: OLS, $R^2$, adjusted $R^2$, MLE vs unbiased $\hat\sigma^2$ → [[../L01/L01-06-gaussian-linear-regression|L01 §6]].
- Unit: Poisson coefficients read as rate ratios use the same $e^\beta$ step as (11) → [[L02-06-gaussian-vs-poisson-regression]]; logit coefficients as odds ratios → [[L02-04-logistic-regression]]; [[L02-07-formulas]], [[L02-08-pitfalls]], [[L02-09-python]].
- Class plan: [[../../Map/class-plan#Class 2: Introduction to statistical learning|Class 2]].
- **Practice:** W Ch. 2 Problem 9 (p. 55, units in log models); W Ch. 6 Computer Exercise C2 (p. 199, the experience quadratic with $\log(\text{wage})$).
