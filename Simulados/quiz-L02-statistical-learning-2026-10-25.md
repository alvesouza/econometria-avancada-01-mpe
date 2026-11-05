---
quiz: "L02 · Introduction to Statistical Learning: Conceptual Synthesis"
tags:
  bv: "Prediction error and the bias–variance trade-off"
  cv: "Validation and cross-validation"
  cls: "Logistic regression and discriminant analysis"
  cnt: "Log-linear and Poisson regression"
---

## bv

Q: A straight line is fitted by OLS to data whose true regression function $E[Y\mid X]$ is curved. A student argues that the squared-bias term of the prediction-error decomposition is zero, because OLS is unbiased under the Gauss–Markov assumptions. Which reply is correct?
- The student is right: the bias term is zero, and the curvature the line misses is absorbed into the irreducible error, which is why the residuals of a misspecified line look larger than the true noise level.
- The bias term is positive only in finite samples; because OLS is consistent, the fitted line converges to the regression function as the sample grows, so the bias vanishes and only the variance term remains.
- OLS is unbiased for the coefficients of the best linear approximation, but the decomposition measures bias against the regression function itself, so the curvature leaves a bias no sample size removes.
- The bias term is zero, but the variance term absorbs the curvature instead, since the line's fitted values swing more across training samples when the regression function it approximates is curved.
<!-- YW5zOjI= -->
> "Unbiased" always names a target. Gauss–Markov's target is the coefficient vector of the fitted linear model, which here is the best linear approximation to a curve. The decomposition's target is the regression function at each $x$. Their gap is a squared-bias term that more data cannot shrink, because OLS converges to the best line, not to the curve. The irreducible error is the variance of the new noise around $E[Y\mid X]$ and does not depend on the fitted model; the variance term is the spread of the fitted curve across training samples, which shrinks with $n$.
> Ref: ISLP §2.2 (pp. 27–40); Izbicki & Mendonça §1.4–1.5 (pp. 9–24); slides `Fundamentos.pdf`
> Similar: Notas/L02/L02-01-prediction-error-bias-variance.md §4; Notas/L02/L02-08-pitfalls.md §2, items 2 and 4; I 2.3 (p. 63)

Q: In a setting where polynomial regressions of increasing degree are compared and the test-optimal degree is moderate, the training sample is doubled while the noise level stays the same. What happens?
- The irreducible error is unchanged; each degree's variance falls while its bias barely moves, so flexibility gets cheaper and the test-optimal degree can only stay put or move to more flexible fits.
- The irreducible error falls in proportion to the sample size, since a larger sample averages out more of the noise, so the whole test-error curve shifts down while its minimum stays at the same degree.
- The test-optimal degree moves toward simpler fits, because a larger sample reveals that the extra terms of flexible fits were capturing noise, which more data expose as spurious and penalise.
- The training error of every degree falls toward zero as the sample grows, so the gap between training and test error widens and the training curve becomes an even worse guide to the best degree.
<!-- YW5zOjA= -->
> The noise floor is the variance of a new error and no sample size touches it. A larger sample lowers the variance term (roughly in proportion to the number of coefficients over $n$) while leaving the squared bias of each degree almost unchanged, so the U-shaped test curve's minimum slides to the right: in the course's tanh example the optimum moves from degree 5 at $n=30$ to degree 7 at larger $n$. The training-test gap, the optimism, also shrinks with $n$ rather than widening.
> Ref: ISLP §2.2.2 (pp. 31–34); Morettin & Singer §1.6.1 (pp. 10–14); slides `Fundamentos.pdf`, `bias-variance-R.txt`
> Similar: Notas/L02/L02-01-prediction-error-bias-variance.md §5; Notas/L02/L02-08-pitfalls.md items 6–7; I 2.1 (p. 63); companion "The Flexibility Dial"

## cv

Q: Leave-one-out cross-validation fits the model on all but one point, once for each point, while 10-fold CV fits it ten times on 90% of the data. How do the two compare as estimators of the test error?
- LOOCV dominates on both counts: it uses more data in each fit and involves no random split, so it has both the smaller bias and the smaller variance, and it is preferred whenever it is affordable.
- 10-fold CV has the smaller bias, because averaging over fewer, more different fits removes the optimism of each one, while LOOCV has the smaller variance, because it averages over many more fits.
- LOOCV is biased upward more than a single hold-out split, because each of its test sets holds only one point, and a one-point test error overstates the error of a model fitted to the rest.
- LOOCV has the smaller bias, since each fit uses nearly all the data, but its fits are nearly identical, so their errors are highly correlated and the average can vary more than 10-fold's.
<!-- YW5zOjM= -->
> Bias falls from hold-out to 10-fold to LOOCV, because each fit gets closer to the full-sample fit. Variance does not follow: the $n$ LOOCV fits share all but one point with each other, so the leave-one-out errors are highly positively correlated and averaging them buys little. Being deterministic given the data does not make LOOCV precise: draw a new data set and it moves. Each single-point error is roughly unbiased for the error of an $(n-1)$-point fit; it is noisy, not biased upward.
> Ref: ISLP §5.1.2–5.1.4 (pp. 204–209); Izbicki & Mendonça §1.5.1 (pp. 14–21)
> Similar: Notas/L02/L02-03-cross-validation-motorcycle.md §5–§6; Notas/L02/L02-08-pitfalls.md §3, item 8; I 5.3 (p. 225)

Q: On the motorcycle data, a single random 80/20 hold-out split picks the course's chosen polynomial order in only about two thirds of repeated splits, while 10-fold CV picks it almost every time. The analyst then reports the CV error of the winning order as its expected test error. Which assessment is correct?
- The hold-out estimate is unbiased, so its instability across splits is harmless, and the minimum CV score is an unbiased estimate of the chosen model's test error, because CV never reuses the test folds.
- A single split is a random answer that depends on which points fell in the test set, and repeated folds average that noise away; but the minimum CV score is optimistic, because the same data chose the winner.
- The stability of the 10-fold choice shows that the true curve is a polynomial of that order, so the reported CV error is a fair grade, since a correctly specified model has no selection bias to correct.
- The instability comes from the high leverage of a high-order polynomial, and the one-fit LOOCV shortcut removes it, which also removes the selection bias of the minimum, since the shortcut never refits.
<!-- YW5zOjE= -->
> One split leaves the answer at the mercy of the partition; averaging over folds stabilises the choice (99 of 100 runs for 10-fold). Stability is not truth: CV ranks the candidates, and on stand-in data whose mean is no polynomial at all it still returns a winner. Reporting the minimum of many CV scores repeats the training-error mistake one level up: the data that chose the model cannot also grade it, so an untouched test set or nested CV is needed. The LOOCV shortcut changes how LOOCV is computed, not what it estimates.
> Ref: ISLP §5.1 (pp. 202–212), §7.1 (pp. 290–292); slides `motorcyle-polynomialregression.pdf`
> Similar: Notas/L02/L02-03-cross-validation-motorcycle.md §4, §8–§9; Notas/L02/L02-08-pitfalls.md §4–§5, items 11–12; I 5.8 (p. 227); I 7.9 (p. 327)

Q: For least squares, LOOCV can be computed from a single fit on all the data, by inflating each ordinary residual according to that point's leverage. Why does the same shortcut not give the exact LOOCV of a logistic regression?
- It does give the exact answer for the logit too, because at convergence IRLS is a weighted least-squares fit, so the final weighted hat matrix reproduces every leave-one-out residual exactly.
- The shortcut fails for least squares as well once the polynomial order is high, because leverages then exceed one, and the logistic case simply inherits this failure from its weighted least-squares steps.
- The shortcut relies on fitted values being a fixed linear map of the response; a logit estimate is the fixed point of a reweighted iteration whose weights shift when a point is dropped, so refits are needed.
- The shortcut works for any model fitted by maximum likelihood, because the score is linear near its root, so the logit's exact LOOCV only needs the same leverages computed from the observed information.
<!-- YW5zOjI= -->
> The one-fit formula follows from the hat matrix: least-squares fitted values are a linear map of $y$ that does not depend on $y$, and removing one row updates it in closed form. The logit's estimate solves a nonlinear score equation; IRLS reaches it by weighted least squares whose weights depend on the fitted probabilities, and those change when an observation is removed. The final weighted hat matrix gives only an approximation, so exact LOOCV for the logit (or LDA) needs $n$ refits. Leverages lie between zero and one, so the second option is false.
> Ref: ISLP §5.1.2 (pp. 204–206), §4.3 (pp. 138–146); Wooldridge 6e §17.1 (pp. 525–536)
> Similar: Notas/L02/L02-03-cross-validation-motorcycle.md §5; Notas/L02/L02-04-logistic-regression.md §4; Notas/L02/L02-08-pitfalls.md items 9–10; I 5.3 (p. 225)

## cls

Q: A logistic regression of loan default on credit-card balance gives a positive balance coefficient. Which reading of that coefficient is correct?
- It is constant on the log-odds scale only; the implied probability change is largest near one half and tiny in the tails, and an odds ratio tracks a probability ratio only when the event is rare.
- It is the change in the default probability per unit of balance, the same at every balance level, which is why the logit and the linear probability model give nearly identical answers near the cut-off.
- It implies an odds ratio that equals the ratio of default probabilities at every balance level, since the logistic function is monotone and so preserves every ratio between the probabilities it maps.
- It gives a constant marginal effect on the probability, while the odds ratio varies with balance, because the odds are a nonlinear transformation of the probability and the probability is linear in balance.
<!-- YW5zOjA= -->
> The logit is linear in the log-odds, so the coefficient is a constant log odds ratio. The marginal effect on the probability is the coefficient times $\pi(1-\pi)$, which is largest at one half and vanishes in both tails; in the course's default example it differs by a factor of more than 40 between the cut-off and a balance of 1,000. An odds ratio of 1.73 at a probability of one half raises the probability to about 0.63, not by 73%; odds and probability ratios coincide only when the event is rare.
> Ref: ISLP §4.3.1–4.3.3 (pp. 139–142); Wooldridge 6e §17.1 (pp. 525–536); slides `logisticregression-discriminantanalysis.pdf`
> Similar: Notas/L02/L02-04-logistic-regression.md §2, §5; Notas/L02/L02-08-pitfalls.md §7–§8; I 4.6, 4.9 (p. 195)

Q: In a default data set, a logit of default on a student dummy alone gives a positive coefficient, but adding credit-card balance turns the student coefficient negative. Which interpretation is correct?
- The model with balance suffers from collinearity between the two regressors, which flips the sign spuriously, so the coefficient from the student-only model is the trustworthy estimate of the student effect.
- The sign flip shows that logistic regression is unstable in small cells, and a linear probability model would not flip, because its coefficients are averages that cannot change sign when a regressor is added.
- The flip is a separation artefact: once balance enters, students are perfectly predicted at high balances, the student coefficient diverges, and its sign then reflects the iteration rather than the data.
- Students carry higher balances and balance drives default, so the student-only coefficient mixes both; at equal balance students default less, and neither is causal without further identifying assumptions.
<!-- YW5zOjM= -->
> This is confounding: the marginal association (students default more) and the conditional one (at equal balance, students default less) answer different questions, and both are correct descriptions of the data. The student-only logit is saturated and reproduces the two group rates exactly; adding balance compares students with non-students at the same balance. Collinearity inflates standard errors, it does not reverse signs on its own; the linear probability model has the same omitted-variable logic; nothing here is separated. Turning either coefficient into a causal effect is the identification problem of Classes 5+6.
> Ref: ISLP §4.3.4 (pp. 142–144); slides `logisticregression-discriminantanalysis.pdf`
> Similar: Notas/L02/L02-04-logistic-regression.md §4.1, §6; Notas/L02/L02-08-pitfalls.md §12; I 4.13 (pp. 196–197)

Q: With Gaussian classes sharing one covariance matrix, the LDA posterior class probability is a logistic function of $x$. Does this make LDA and logistic regression the same method?
- Yes: the two share the same functional form, so on any data set they produce the same coefficients, the same fitted probabilities and the same classification rule, and the choice between them is cosmetic.
- No: same form, different estimator; LDA plugs Gaussian class means and covariance into Bayes' theorem, the logit maximises the conditional likelihood of the label and alone fails on separated data.
- No: LDA is the more flexible of the two, because it allows a separate covariance matrix for each class and so draws quadratic boundaries, while the logistic model can only ever draw linear ones.
- No: the logit requires the predictors to be Gaussian within each class to be valid, while LDA requires no distributional assumption on the predictors, which is why LDA is preferred with dummy predictors.
<!-- YW5zOjE= -->
> The common form hides two estimators. LDA models the distribution of $x$ within each class and turns it into a posterior by Bayes' theorem; the logit models only $P(y=1\mid x)$. On perfectly separated data the logit MLE does not exist (IRLS diverges) while LDA returns a finite rule; with a dummy predictor LDA's Gaussian assumption is plainly false while the logit can be exact. Class-specific covariances define QDA, not LDA. The assumptions in the last option are swapped.
> Ref: ISLP §4.4 (pp. 146–161), §4.5 (pp. 161–167); Izbicki & Mendonça §8.1 (pp. 141–151)
> Similar: Notas/L02/L02-05-discriminant-analysis.md §7–§8; Notas/L02/L02-08-pitfalls.md §12; I 4.5 (pp. 194–195); I 4.2 (p. 193)

Q: About 3% of a bank's clients default. The trivial rule "nobody defaults" has a lower overall error rate than an LDA rule that flags clients whose posterior default probability exceeds 0.2. Which conclusion is correct?
- Rare positives make the error rate track the negatives; a cut-off encodes the relative cost of misses and false alarms, so a lower one can raise the error rate and still cut the expected cost.
- The rule with the lower error rate is the better classifier, and 0.5 is the only cost-neutral cut-off, so the LDA rule should be moved back to 0.5, where it will match or beat the trivial rule.
- Lowering the cut-off from 0.5 to 0.2 reduces both the false-positive and the false-negative rate at once, so the LDA rule is better on every count, and its higher error rate must be a sampling accident.
- Neither rule can be judged from these figures, since the ROC curve and its area also depend on which cut-off is chosen, so a cost-free comparison of the two classifiers is impossible in principle.
<!-- YW5zOjA= -->
> The 0.5 cut-off is itself a cost choice: it treats a missed defaulter and a false alarm as equally costly. If a miss costs four times as much, the Bayes cut-off is 0.2. In ISLP's default data the trivial rule errs 3.33% of the time and catches no defaulter, while LDA at 0.2 errs 3.73% but catches most of them and has a much lower total cost. Lowering a cut-off trades false negatives for false positives, never both down. The ROC curve sweeps over all cut-offs, so it is precisely the threshold-free summary.
> Ref: ISLP §4.4.2 (pp. 150–156); Izbicki & Mendonça Ch. 7 (pp. 133–139), §9.1 (pp. 169–172); Morettin & Singer Ch. 8 (pp. 263–290)
> Similar: Notas/L02/L02-05-discriminant-analysis.md §10–§11; Notas/L02/L02-08-pitfalls.md §9–§11; I 4.14 (pp. 197–198); MS 8.9

## cnt

Q: Daily blog visits are recorded for two groups of days, and both a Gaussian linear regression and a Poisson regression with a log link are fitted on a group dummy. Both reproduce the two group means exactly. Which statement is correct?
- Because the fitted means coincide, the two models are equivalent for inference as well: they give the same standard errors and the same test of the group effect, and the choice is a matter of reporting scale.
- If the counts are overdispersed, the Poisson coefficients are biased toward zero, so a quasi-Poisson fit changes the point estimate of the group effect as well as its standard error.
- The Poisson coefficient on the dummy is an additive change in the expected count, while the Gaussian coefficient is a percentage change, which is why the two models agree on the means but not on the effect.
- The design is saturated, so the means coincide, but the assumed variances differ, constant versus equal to the mean, so tests differ; overdispersion keeps the Poisson estimates and inflates their errors.
<!-- YW5zOjM= -->
> With one dummy, any model with a group-specific mean fits the two sample means, so the point estimates agree. Inference rests on the variance function: the Gaussian model pools one constant variance, the Poisson ties it to the mean, hence different standard errors and test statistics for the same effect. If the variance exceeds the mean, the score equations for the coefficients are unchanged, so quasi-Poisson keeps them and multiplies the standard errors by the square root of the dispersion. The log link reads the coefficient as a log rate ratio (a percentage change); the Gaussian one is additive.
> Ref: ISLP §4.6 (pp. 167–173); Wooldridge 6e §17.3 (pp. 543–547); site page `Gaussian-vs-Poisson-regression.html`
> Similar: Notas/L02/L02-06-gaussian-vs-poisson-regression.md §4–§5; Notas/L02/L02-02-linear-log-linear-regression.md §4; Notas/L02/L02-08-pitfalls.md §14–§15; W 17.C5
