---
tags: [notes, lecture-02, statistical-learning, pitfalls, true-false, review]
date: 2026-10-19
status: taught
source: "L02-01 … L02-06 (all numbers from the decks as worked there); counterexamples checked in L02_python_checks.py section 7; V/F style of rules/00_estilo_avaliacao.md §2 (reciprocal falsehoods, one claim per item)"
---

# Class 2 · Pitfalls — fifteen confusions, and a 30-item True/False self-test

> Prev: [[L02-07-formulas]] · Next: [[L02-09-python]] · Map: [[L02-00-map]]

Every counterexample uses a number already derived in a section note; the few new ones are
checked in `L02_python_checks.py` (section 7, [[L02-09-python]] §7).

---

## Part I — the confusions

### 1 · Training error vs test error

**The confusion:** the model with the smaller training error predicts better.

**Counterexample** (tanh world, [[L02-01-prediction-error-bias-variance]] §5). Degree 15: expected
training MSE **7.47**, expected test error **26.20**. Degree 5: training **13.79**, test **19.81**.
Training ranks 15 above 5; test ranks them the other way. Degree 15 even trains *below* the noise
floor $\sigma^2=16$ — it has reproduced noise.

> **Training error falls with every added term (nested least squares cannot do worse in-sample);
> test error is U-shaped. The gap is $2\sigma^2(d+1)/n$ on average** (note 01 (33)).

### 2 · Bias–variance of a learner vs bias of an estimator

**The confusion:** "OLS is unbiased, so its bias term in (21) is zero."

**Counterexample** (note 01 §4.1). Fit a straight line to $\psi(x)=1-x+2x^2$. OLS *is* unbiased —
for the coefficients of the best **linear** approximation, $\frac23+x$. The bias in (21) is
measured against $\psi$ itself: $-2(x^2-x+\frac16)$, integrated **0.0222**, a thousand times the
variance. And the "variance" in (21) is the spread of $\hat\psi(x)$ **across training samples**, not
$\operatorname{Var}(Y)$ — that is $\sigma^2$.

> **"Unbiased" always names a target. Gauss–Markov's target is $\beta$ of the fitted model; (21)'s
> target is $E[Y\mid X=x]$.**

### 3 · LOOCV vs $k$-fold: which has less bias, which less variance

**The confusion:** "LOOCV uses $n-1$ points and involves no random split, so it is the best estimate
on every count."

**Counterexample** (note 03 (14)). Bias: yes, LOOCV's fits are the closest to the full fit. Variance:
its $n$ fits share $n-2$ of their $n-1$ points, so the errors $\text{EQM}_i$ are strongly positively
correlated; in the extreme of perfect correlation, (14) collapses to
$\operatorname{Var}[CV_{(n)}]=\operatorname{Var}[\text{EQM}_1]$ — **averaging $n$ terms buys
nothing.** Deterministic given the data does not mean precise: redraw the data and $CV_{(n)}$ moves.

> **Bias falls hold-out → 10-fold → LOOCV; variance does not** (note 03 §6 table). Cost too: one fit
> for OLS by (7), $n$ fits for a logit.

### 4 · CV picks a model, not a truth

**The confusion:** "10-fold CV chose order 12 in 99 of 100 runs, so the motorcycle curve is a
12th-degree polynomial."

**Counterexample** (note 03 §8). The stand-in data's mean is a sum of two Gaussian bumps — **no
polynomial at all** — and CV picks order 12 there too. CV ranks the *candidates* by estimated test
error; if the truth is not among them, it still returns a winner. ISLP (p. 290) warns that $d>4$
gives "very strange shapes", especially at the boundary — where the order-12 band flares.

### 5 · Selecting the order, then reporting its in-sample fit

**The confusion:** "Order 12 has adjusted $R^2=0.7798$; that is how well it will predict."

**Counterexample.** Regress pure noise on a 12-term polynomial with $n=132$: the expected $R^2$ is
$k/(n-1)=12/131=$ **0.0916** although the true $R^2$ is 0 (checked by simulation, 4,000 draws). Pick the
best of many candidates and the winner's in-sample fit is biased upward again — adjusted $R^2$
corrects for the parameters of *one* model, not for the search. The same holds for the smallest of
14 CV estimates (note 03 §9) and for the bootstrap band, which holds $d=12$ fixed in every resample
(§7).

> **The data that chose the model cannot also grade it.** Keep an untouched test set, or nest the CV.

### 6 · Log points vs percent

**The confusion:** "$\log(\text{price})$ has coefficient 0.306 on rooms: one more room, +30.6%."

**Counterexample** (note 02 §4.1). Exactly, $100(e^{0.306}-1)=$ **+35.8%**; one *fewer* room,
$100(e^{-0.306}-1)=$ **−26.4%**. The 30.6 is a first-order approximation, five points off here.
And a **percentage point** is not a percent: unemployment 8 → 9 is one point, **12.5%**, and
$\log9-\log8=$ **0.118** log points.

### 7 · Odds vs probability

**The confusion:** "An odds ratio of 1.733 means the probability rises by 73%."

**Counterexample** (note 04 §2.1). At the `default` cut-off, $\hat\pi=0.5$, odds 1. USD 100 more balance
multiplies the odds by $e^{0.55}=1.733$: odds 1.733, probability $1.733/2.733=$ **0.634** — a 27% rise,
not 73%. The two coincide only when $\pi$ is small: on the student table the probability ratio is
$4.31/2.92=1.478$ against an odds ratio of 1.499.

### 8 · A logit coefficient vs a marginal effect

**The confusion:** "$\hat\beta_{\text{balance}}=0.0055$: each dollar adds 0.0055 to the default
probability."

**Counterexample** (note 04 (8)). $\partial\pi/\partial x=\beta\pi(1-\pi)$: **0.001375** per dollar at
the cut-off, **0.0000315** at a balance of 1,000 — 44 times apart, and both far below 0.0055. The
coefficient is constant on the **log-odds** scale only.

### 9 · The 0.5 cut-off is not cost-neutral

**The confusion:** "Classify at 0.5; any other cut-off is arbitrary."

**Counterexample** (note 05 (15), §10). 0.5 *is* a cost choice: $c_{12}/(c_{12}+c_{21})=\frac12$
means a missed defaulter costs the same as a false alarm. If a missed defaulter costs four times as
much, the Bayes cut-off is $1/(1+4)=0.2$, and ISLP's LDA tables give costs **1031** at 0.5 against
**787** at 0.2.

### 10 · Accuracy under class imbalance

**The confusion:** "The rule with the lower error rate is the better classifier."

**Counterexample** (note 05 §10, ISLP `default`). "Nobody defaults" has error **3.33%**
($333/10{,}000$) and catches no defaulter. LDA at 0.2 has error **3.73%** — *higher* — and catches
195 of 333. At a 4:1 cost the trivial rule costs $4\times333=1332$, the LDA rule 787.

> **With 3% positives, the error rate is dominated by the negatives.** Read the confusion matrix
> (note 04 §9), or the ROC curve (note 05 §11), not one number.

### 11 · FDR vs FPR

**The confusion:** "The false-positive rate is the share of flagged e-mails that are not spam."

**Counterexample** (spam `glm`, note 04 §9). FPR $=FP/(FP+TN)=80/1405=$ **5.69%** — of the ham, how
much was flagged. FDR $=FP/(FP+TP)=80/883=$ **9.06%** — of the flagged, how much was ham. Same
numerator, different denominators; FDR > FPR here because fewer e-mails were flagged (883) than were
ham (1405). The deck's column, $FP/(FP+TP+FN)=8.20\%$, is neither.

### 12 · LDA vs logistic regression

**The confusion:** "LDA's posterior is a logistic function of $x$ (note 05 §7.1), so LDA and logistic
regression are the same method."

**Counterexample.** Same **form**, different **estimator**: LDA plugs Gaussian MLEs of $\mu_k,\Sigma$
into Bayes' theorem; the logit maximises the conditional likelihood of $y$. On perfectly separated
data the logit MLE **does not exist** — IRLS runs off to infinity (note 04 §3; the check in
[[L02-09-python]] §4) — while LDA returns a finite rule. With $x$ = the `student` dummy, LDA's
Gaussian assumption is plainly false, while the logit is exact (saturated, note 04 §4.1).

### 13 · ML rule vs Bayes rule

**The confusion:** "Allocate to the class under which the observation is most likely."

**Counterexample** (note 05 §4). Bernoulli example with prior $\pi_1=0.25$. The ML rule ($x=0\to1$,
$x=1\to2$) errs with probability $0.25(\frac12)+0.75(\frac14)=$ **0.3125**. Since $\pi_1<\frac13$, the
Bayes rule sends **everything** to class 2 and errs only **0.25** of the time. The likelihood ratio
must clear the **prior odds** (5), not 1.

### 14 · Gaussian vs Poisson regression for counts

**The confusion:** "On the blog data both models give the means 109 and 83.33, so it does not
matter which one is fitted."

**Counterexample** (note 06 §4). The means coincide because the model is saturated in two groups;
the **variance** each model assumes does not: constant 140.4 vs equal to the mean. Hence $t=-5.67$
vs $z=-6.77$ for the same effect. With a continuous covariate and small counts the Gaussian line
also goes negative (9.6% of ISLP's Bikeshare fits, p. 168); the log link cannot.

### 15 · Overdispersion

**The confusion (two-sided):** "Var > mean makes the Poisson coefficients wrong" — or — "Poisson
standard errors are fine whatever the variance."

**Counterexample** (note 06 §5). The blog data have variance/mean 1.36 and 1.57, $\hat\sigma^2=1.444$.
Quasi-Poisson leaves $\hat\beta=-0.26850$ **unchanged** (the mean model is still right, the score
equations (4) are the same) but multiplies the SE by $\hat\sigma=1.202$: $z$ falls from $-6.77$ to
**−5.63**. Point estimates survive; precision was overstated.

---

## Part II — True/False self-test (original items)

**[E]** easy · **[M]** medium · **[P]** hard. Scoring as in [[../../rules/00_estilo_avaliacao|rules/00]]:
$\max\{0,\ \text{right}-\text{wrong}/2\}$ per block. Numbers marked "illustrative" are invented for the
item; all others come from the notes.

### Block A — prediction error and bias–variance

**1. [E]** Under squared loss, among all functions of $X$, the conditional mean $E[Y\mid X]$ has the
smallest expected prediction error, whatever the joint distribution of $(X,Y)$ (with finite second
moments).
**True.** Conditioning on $X$ turns the problem into minimising $g(t)=E[(Y-t)^2\mid X=x]$ separately at
each $x$; $g'(t)=-2E[Y\mid X=x]+2t=0$ at the conditional mean and $g''=2>0$ (note 01 (2)–(6)). No
distributional assumption enters beyond the existence of the moments. Under absolute loss the answer
would be the conditional median instead.

**2. [M]** A straight line fitted by OLS to a curved regression function contributes no squared-bias
term to (21), because OLS is unbiased.
**False.** OLS is unbiased for the coefficients of the best *linear* approximation, not for
$\psi(x)$. On $\psi(x)=1-x+2x^2$ with $x\sim U(0,1)$ the line's bias is $-2(x^2-x+\frac16)$ and its
integrated square is $1/45=0.0222$, more than twice the noise variance $0.01$ (note 01 §4.1).

**3. [M]** If method A has a lower expected training MSE than method B, A also has a lower expected
test error.
**False.** This is the reciprocal the training error invites. In the tanh world the degree-15
polynomial trains at 7.47 against 13.79 for degree 5, yet its test error is 26.20 against 19.81
(note 01 §5). The training error rewards variance; the test error charges for it.

**4. [M]** In the decomposition (21), the variance term measures how much $Y$ varies around
$\psi(X)$.
**False.** That is the irreducible term $\sigma^2$, random over the new $\varepsilon$. The variance term is
$\operatorname{Var}[\hat\psi(x)]$, random over the **training sample**: how much the learned curve
moves when the data are redrawn (note 01 §4 table). A perfectly noise-free world ($\sigma=0$) can still
have a positive variance term if the design is random.

**5. [P]** For OLS with $d+1$ coefficients on a fixed design and homoskedastic noise, the expected
training MSE understates the expected error on new responses at the same design points by exactly
$2\sigma^2(d+1)/n$, whatever the true regression function.
**True.** The residual vector is $(I-H)(\boldsymbol\psi+\boldsymbol\varepsilon)$; the $\psi$ part
$\|(I-H)\boldsymbol\psi\|^2/n$ appears in both expectations and cancels, leaving
$\sigma^2(d+1)/n+\sigma^2-\sigma^2(1-(d+1)/n)=2\sigma^2(d+1)/n$ (note 01 (30)–(33)). At $d=5$, $n=30$,
$\sigma=4$: 6.4. This is the penalty $C_p$ and AIC add back.

**6. [M]** Doubling the training sample lowers the irreducible error.
**False.** $\sigma^2$ is the variance of the new noise $\varepsilon$, which no sample size touches; the
floor of the tanh curves stays at 16 for every $n$. A larger $n$ lowers the **variance** term (roughly
in proportion to $(d+1)/n$ for polynomial OLS), which is what moves the next item's optimum.

**7. [M]** In the tanh world with $\sigma=4$, raising the training size from $n=30$ to $n=200$ cannot
lower the test-optimal polynomial degree.
**True.** Larger $n$ shrinks every degree's variance while leaving bias² nearly unchanged, so
flexibility gets cheaper; the exact computation gives $d^*=5$ at $n=30$ and $d^*=7$ at $n=60$ and
at $n=200$ ([[L02-09-python]] §7). The Flexibility Dial shows the optimum sliding right as $n$ grows.

### Block B — validation and cross-validation

**8. [M]** Although LOOCV involves no random split, it can have a larger variance as an estimator of
the test error than 10-fold CV.
**True.** Given the data LOOCV is deterministic, but as a function of
a random sample it has a sampling variance, and its $n$ nearly identical fits make the $\text{EQM}_i$
strongly positively correlated, so the covariance term of (14) dominates (note 03 §5; ISLP §5.1.4).
10-fold's fits overlap less.

**9. [E]** For a least-squares fit, LOOCV can be computed from a single fit on all $n$ points.
**True.** $CV_{(n)}=\frac1n\sum(e_i/(1-h_{ii}))^2$ (note 03 (7)), derived by Sherman–Morrison: the
left-out residual is the ordinary residual inflated by $1/(1-h_{ii})$ (13).

**10. [M]** The same one-fit shortcut gives the exact LOOCV of a logistic regression fitted by IRLS.
**False.** The derivation uses that $\hat\beta$ is linear in $y$ through $(X'X)^{-1}X'y$; a logit's
$\hat\beta$ is the fixed point of a re-weighted iteration whose weights change when a point leaves.
LOOCV for the logit (or LDA) needs $n$ refits (ISLP p. 205; note 03 §5).

**11. [M]** An 80/20 hold-out estimate tends to overstate the test error of the model refitted on
all $n$ observations.
**True.** It is computed from a fit on about 80% of the data — 105 points of 132 for the motorcycle —
and a fit on fewer points is noisier, so its error is higher than that of the full-sample fit
(ISLP p. 208; note 03 §4, §6 table).

**12. [M]** A fintech's analyst picks the polynomial degree that maximises adjusted $R^2$ among
degrees 1–20 and reports that adjusted $R^2$ as the model's out-of-sample fit; since adjusted $R^2$
penalises the number of parameters, the report is unbiased.
**False.** The penalty corrects for the parameters of one fixed model, not for choosing the best of
twenty on the same data. Under pure noise a 12-term polynomial with $n=132$ already has
$E[R^2]=12/131=0.0916$; taking the maximum over candidates pushes the reported figure up further
(pitfall 5). An untouched test set or nested CV is needed.

**13. [E]** Since 10-fold CV picked order 12 in 99 of 100 repetitions, the true regression function
of the motorcycle data is a polynomial of degree 12.
**False.** CV ranks the candidates by estimated test error; it says nothing about whether any
candidate is the truth. On the stand-in data, whose mean is a sum of Gaussian bumps, CV also picks
12 (note 03 §8). The 99/100 measures the stability of the choice, not its truth.

**14. [P]** The pairs-bootstrap band drawn around the order-12 fit includes the uncertainty of having
chosen the order from the same data.
**False.** Every resample refits order 12; the selection step is outside the loop. Putting it inside —
re-running CV in each resample — would widen the band (note 03 §7, the "what the band does not
cover" box).

**15. [M]** On data whose noise variance changes with $x$, the pairs-bootstrap band and the formula
band $\hat f(x_0)\pm2\sqrt{\ell_0'\hat C\ell_0}$ will generally differ.
**True.** The formula uses one $\hat\sigma^2$ for every $x$; resampling pairs carries the quiet and the
noisy regions in their own proportions. On the stand-in the bootstrap band is wider in the noisy
region; on homoskedastic data the two agree to within 10% ([[L02-09-python]] §3).

### Block C — logistic regression and classification metrics

**16. [E]** In a logit, $e^{\beta_j}$ is the factor that multiplies the odds when $x_j$ rises by one
unit, the same at every value of the covariates.
**True.** The odds are $e^{\eta}$ (note 04 (3)); raising $x_j$ by one adds $\beta_j$ to $\eta$, so the
odds go from $e^\eta$ to $e^{\eta+\beta_j}$ — ratio $e^{\beta_j}$ whatever $\eta$ was (6).

**17. [M]** In a logit, $\beta_j$ is the change in $P(y=1)$ per unit of $x_j$.
**False.** The probability effect is $\beta_j\pi(1-\pi)$, largest ($\beta_j/4$) at $\pi=\frac12$
(note 04 (8)). For `default`, 0.001375 per dollar at the cut-off and 0.0000315 at a balance of 1,000,
neither equal to 0.0055.

**18. [M]** A positive coefficient on `student` alone (0.405) and a negative one given `balance`
(−0.715) can both be correct.
**True.** They answer different questions: students default more *overall* because they carry larger
balances; *at the same balance* they default less. Balance confounds the marginal comparison (note
04 §5.3) — the sign flip is evidence of confounding, not of an error.

**19. [P]** At the MLE of a logit that includes an intercept, the average fitted probability equals
the sample share of ones.
**True.** The score is $X'(y-\pi)$ (note 04 (12)); its intercept row is $\sum_i(y_i-\hat\pi_i)=0$, so
$\frac1n\sum\hat\pi_i=\bar y$ — 0.0333 in `default`. It holds for any canonical-link GLM with an
intercept (the Poisson version: fitted total = observed total, note 06 (4)).

**20. [M]** Lowering the probability cut-off of a credit model from 0.5 to 0.2 lowers its overall
error rate.
**False.** ISLP's LDA on `default`: error 2.75% at 0.5, **3.73%** at 0.2 — 212 more false alarms buy
114 fewer missed defaulters (note 05 §10). The lower cut-off is right when a missed defaulter costs
about four times a false alarm (cost 1031 → 787), not because errors fall.

**21. [M]** A digital bank in São Paulo has 3.33% defaulters in its portfolio. A rule that predicts
"no default" for every client has a lower error rate (3.33%) than an LDA rule with cut-off 0.2
(3.73%), so the trivial rule is the better credit tool.
**False.** The trivial rule catches none of the defaulters; at any cost ratio above the one that makes
the two equal, it loses — at 4:1, $4\times333=1332$ against 787 (pitfall 10). With 3% positives the
error rate is dominated by the negatives and cannot rank credit rules.

**22. [M]** For the spam `glm`, the false discovery rate exceeds the false-positive rate because fewer
e-mails were flagged as spam than were actually ham.
**True.** Both have numerator FP $=80$; FDR divides by the flagged $FP+TP=883$, FPR by the ham
$FP+TN=1405$. FDR > FPR exactly when $883<1405$: **9.06% vs 5.69%** (note 04 §9).

**23. [P]** For ungrouped 0/1 data, a residual deviance of 1596.5 on 9998 degrees of freedom shows a
good fit, because it is far below its $\chi^2_{9998}$ expectation.
**False.** With one observation per covariate pattern the deviance does not have a $\chi^2_{n-p}$
reference distribution; it equals $-2\ell(\hat\beta)$ and depends on the $\hat\pi_i$ alone (note 04
(23), §7). Only **differences** of deviances between nested models are safely referred to $\chi^2$ —
e.g. $1596.5-1571.7=24.8$ on 1 df for `student`.

### Block D — discriminant analysis

**24. [E]** With equal priors and equal misallocation costs, the Bayes discriminant rule coincides
with the ML rule.
**True.** The threshold in (14) of note 05 is $\log\{\pi_2c_{12}/(\pi_1c_{21})\}=\log1=0$, which is the ML
rule $h(x)>0$.

**25. [M]** Two univariate Gaussian classes with unequal variances can produce a Bayes rule that
allocates **both** tails of the real line to the same class.
**True.** $h$ is then quadratic (note 05 (8)); in the deck's example ($\mu=(1,5)$, $\sigma=(6,2.5)$)
it is a U with roots 1.680 and 10.001, so class 1 — the wider one — takes $(-\infty,1.680)$ and
$(10.001,\infty)$. A single midpoint arises only when $\sigma_1=\sigma_2$.

**26. [M]** In that example, an observation at $x=12$ is allocated to class 2 because it is closer to
$\mu_2=5$ than to $\mu_1=1$.
**False.** $h(12)=0.066111(144)-0.772222(12)+1.110642=1.364>0$: class 1. Far from both means the
density with the fatter tails is the larger one; distance to the mean decides only when the
variances are equal (note 05 §5.2).

**27. [P]** A public hospital in Recife screens for a disease (class 1) with the deck's two Gaussians
and equal priors (illustrative). Raising the cost of a missed case far enough sends every patient
to class 1.
**True.** The threshold $\log(c_{12}/c_{21})$ falls as $c_{21}$ rises; once $c_{21}/c_{12}>e^{1.144}=3.14$
it sits below $\min_xh(x)=-1.144$, so $h(x)$ exceeds it everywhere and $R_2$ is empty (note 05 §10).

**28. [M]** Since every Bayes rule is admissible, an admissible rule is a sensible rule.
**False** — the reciprocal fails. "Allocate everything to class 2" is admissible in the Bernoulli
example (it is the Bayes rule for $\pi_1<1/3$) but ignores the data. Admissibility only excludes
rules beaten everywhere, such as the reversed rule with $p_{11}=\frac12$, $p_{22}=\frac14$ (note 05 §9).

### Block E — counts

**29. [M]** Because the Gaussian and Poisson regressions on the weekend dummy give the same fitted
means (109 and 83.33), they attach the same statistical significance to the weekend effect.
**False.** Same means, different variance functions: constant $s^2=140.4$ vs $\operatorname{Var}=\lambda$.
The Gaussian $t$ is $-5.67$, the Poisson $z$ is $-6.77$, and the quasi-Poisson $z$ is $-5.63$ (note
06 §4–§5).

**30. [M]** Overdispersion ($\operatorname{Var}>$ mean) makes the Poisson estimate of the weekend
coefficient inconsistent.
**False.** The score equations $X'(y-\lambda)=0$ only need the **mean** to be right; with $\hat\sigma^2=1.444$
the quasi-Poisson fit returns the same $\hat\beta=-0.26850$. What overdispersion breaks is the
**standard error** — too small by the factor $\hat\sigma=1.202$ (note 06 §5; pitfall 15).

**Answer key at a glance:** T — 1, 5, 7, 8, 9, 11, 15, 16, 18, 19, 22, 24, 25, 27 (14 items);
F — 2, 3, 4, 6, 10, 12, 13, 14, 17, 20, 21, 23, 26, 28, 29, 30 (16 items).

---

## Links

Map: [[L02-00-map]] · Formulas: [[L02-07-formulas]] · Code: [[L02-09-python]] · Class 1 pitfalls:
[[../L01/L01-10-pitfalls|L01-10]] · Grading conventions: [[../../rules/00_estilo_avaliacao|rules/00]]
· Rules: [[../../rules/06_classificacao_validacao|rules/06]].
