---
quiz: "L02 · Introduction to Statistical Learning: Hard Conceptual Quiz"
tags:
  boot: "Bootstrap bands and honest validation"
  bv: "Prediction error, its floor and the Bayes rule"
  cls: "Classification rules and their error measures"
  reg: "Log scales and count regression"
---

## boot

Q: After 10-fold CV picks a degree-12 polynomial for motorcycle-crash acceleration data, an analyst refits the degree-12 model on 1,000 pairs-bootstrap resamples and draws the pointwise 2.5% and 97.5% quantiles of the refitted curves. On fresh crash tests, far fewer than 95% of the new readings fall inside this band. Which diagnosis is correct?
- The band is too narrow because 1,000 resamples are too few; with enough resamples the percentile band converges to a 95% prediction band for new readings at every value of the input variable.
- The pairs bootstrap fails here for the same reason it fails for the sample maximum: a polynomial fit is a boundary statistic, so only a parametric bootstrap from the fitted curve can give valid coverage.
- The band covers the regression function at each input, not where a new reading lands, which also needs the noise variance; and it holds the degree fixed, so the selection step is outside it too.
- The band is pointwise, so 95% coverage holds only at one input value at a time; across the whole range of inputs the share of readings inside must fall to about 5%, as Bonferroni's bound predicts.
<!-- YW5zOjI= -->
> A is wrong: more resamples only remove simulation error from the quantiles; the band still targets the fitted mean, whose spread shrinks with the sample size, while a new reading keeps its own noise.
> B is wrong: the maximum fails because it sits on the edge of the support; a least-squares fit is a smooth function of the data, which is the case where the pairs bootstrap works.
> C is right: a new response is the regression function plus fresh noise, so a prediction band adds the noise variance to the squared bootstrap standard error; and because every resample refits degree 12, the uncertainty of having chosen the degree is not counted, which re-running CV inside each resample would add.
> D is wrong: each new reading is judged at its own input, so pointwise coverage is the relevant notion for the share of readings inside; simultaneous coverage concerns the whole curve, and Bonferroni gives no such figure.
> Ref: ISLP §5.2 (pp. 212–215, eq. 5.8), §7.1 (pp. 290–292); slides `motorcyle-polynomialregression.pdf` (slide 11)
> Similar: I 5.4 (bootstrap standard deviation of a prediction; Listas/lista-L02-book-exercises.tex); Notas/L02/L02-03-cross-validation-motorcycle.md §7; Notas/L02/L02-08-pitfalls.md items 14–15

Q: For a quartic fit of wage on age, the pairs-bootstrap standard error of the fitted mean wage is close to the heteroskedasticity-robust standard error at ages 25, 50 and 75, while the classical least-squares formula is markedly larger at 25 and at 75. Which explanation is correct?
- Resampling pairs carries each region's own spread of wages, as the robust sandwich does, while the classical formula spreads one pooled error variance over all ages and overstates it where wages vary less.
- The classical formula is the right one, since a polynomial is linear in its coefficients; the bootstrap is smaller because resamples repeat observations, which artificially lowers the variability of each refitted curve.
- The bootstrap and the robust formula agree only by coincidence, because the bootstrap measures the prediction error for new workers while both formulas measure the uncertainty of the fitted mean at each age.
- The classical formula is larger at the ends because it includes the noise variance of a new worker, while the bootstrap and the robust formula leave it out, so the classical band is in fact a prediction band.
<!-- YW5zOjA= -->
> A is right: the classical variance assumes one error variance for every age; resampling whole pairs keeps the smaller spread of wages among young men and the local spread at older ages, which is what the White sandwich estimates too.
> B is wrong: linearity in the coefficients does not make the errors homoskedastic, and the resampling scheme is designed to mimic the sampling variability of the fit, not to reduce it.
> C is wrong: the bootstrap standard error here is the spread of the refitted mean at each age, the same target as both formulas; prediction of a new worker would add the noise variance.
> D is wrong: neither formula includes the noise of a new worker; the classical one is larger because its pooled variance is too big where the true spread is small.
> Ref: ISLP §5.2 (pp. 212–215), §7.1 (pp. 290–291, eq. 7.2); Wooldridge 6e §8.2 (heteroskedasticity-robust inference)
> Similar: I 5.4, illustration on the wage data (Listas/lista-L02-book-exercises.tex); Notas/L02/L02-03-cross-validation-motorcycle.md §7; I 7.6 (p. 326)

Q: From 5,000 candidate predictors and 50 observations of a binary outcome, an analyst keeps the 20 predictors most correlated with the outcome in the full sample, then estimates the test error of a linear discriminant rule on those 20 by 10-fold CV and finds it far below 50%. The outcome was generated independently of every predictor. What went wrong?
- Nothing went wrong in principle: CV estimates the test error of whatever model it is given, so a low error shows that the screened predictors are genuinely related to the outcome despite the design.
- The estimate is optimistic only because 10 folds are too few; LOOCV, which leaves out a single observation at a time, would remove the optimism, since each of its fits then uses almost all of the data.
- The trouble is the number of predictors relative to observations, not the screening; with 20 predictors and 50 observations the rule overfits, and an adjusted R-squared on the fit would expose the problem.
- The screening used the outcomes of every fold, so each held-out fold had already helped choose the predictors; CV must repeat the whole procedure, screening included, inside each of the training splits.
<!-- YW5zOjM= -->
> A is wrong: CV grades a procedure only if every step that looked at the outcomes is redone without the held-out fold; here the held-out outcomes shaped the model before the folds were drawn.
> B is wrong: LOOCV inherits the same leak, because the left-out point also took part in the screening; fewer or more folds change bias and variance, not the leak.
> C is wrong: overfitting of a fixed set of 20 predictors would show up in a correctly run CV; the low error here comes from choosing those 20 with the outcomes that later serve as test data.
> D is right: among 5,000 noise predictors, the 20 most correlated with the observed labels fit those labels by construction; only screening inside each training split gives an honest error near 50%. It is the CV version of reporting the best of many specifications.
> Ref: ISLP §5.1 (pp. 202–212); Izbicki & Mendonça §1.5.1 (pp. 14–21)
> Similar: Notas/L02/L02-08-pitfalls.md §5 (the data that chose the model cannot also grade it); Notas/L01/L01-08-p-hacking-evidence.md §3; I 5.8 (p. 227)

## bv

Q: In a simulation whose noise variance is known to be 16, a degree-15 polynomial fitted to 30 points has an expected training MSE of about 7.5 and an expected test error of about 26, while a degree-5 fit has about 13.8 and 19.8. Which reading is correct?
- The degree-15 fit has found structure that the degree-5 fit misses, since its training error is below the noise variance; its higher test error comes from noise in the test sample and averages out over test sets.
- No fitted function predicts new responses better than the noise variance, so a training MSE below it shows the degree-15 fit has absorbed noise; the gap between training and test error grows with the coefficient count.
- The noise variance must be smaller than 16 in this sample, since a training MSE cannot fall below the irreducible error; the comparison of the two fits should be repeated with a better estimate of the noise.
- Both fits are unbiased for the regression function, so their test errors differ only in variance; the training MSE below 16 means that the degree-15 fit has the smaller bias and should be preferred for interpretation.
<!-- YW5zOjE= -->
> A is wrong: the quoted test errors are expectations, already averaged over test sets; the gap is systematic, not test-sample noise.
> B is right: the noise variance is the floor for the expected error on new responses, and in-sample the fit can go below it only by bending toward the realised noise; the optimism, test minus training error, grows with the number of coefficients over the sample size.
> C is wrong: the training error is not bounded by the noise variance, because the fit is chosen to make the in-sample residuals small; only the test error has that floor.
> D is wrong: a degree-5 polynomial approximating a non-polynomial curve is biased, and a lower training error says nothing about bias at new points; the test error, not the training error, decides.
> Ref: ISLP §2.2.1–2.2.2 (pp. 29–36); Izbicki & Mendonça §1.4–1.5 (pp. 9–24); slides `Fundamentos.pdf`
> Similar: Notas/L02/L02-01-prediction-error-bias-variance.md §5–§6; Notas/L02/L02-08-pitfalls.md §1, items 3 and 5; I 2.3 (p. 63)

Q: Which correspondence between regression under squared loss and classification under 0–1 loss is correct?
- The conditional mean minimises squared error as the most probable class minimises expected misclassification; the noise variance and the Bayes error rate are floors that no model, however flexible, beats.
- The conditional mean minimises expected squared error, and the conditional median minimises the misclassification rate; the Bayes error rate falls to zero as the sample grows, while the noise variance stays fixed.
- The Bayes classifier assigns each point to the class with the largest likelihood, and it reaches zero error whenever the classes have different means, just as the regression function does when the noise is absent.
- Under squared loss the best predictor is the conditional mode, and under 0–1 loss it is the conditional mean of the class indicator; both floors shrink with the sample size, since more data reduce irreducible error.
<!-- YW5zOjA= -->
> A is right: minimising the expected loss point by point gives the conditional mean under squared loss and the class with the largest posterior probability under 0–1 loss; their floors, the noise variance and the Bayes error rate, are properties of the joint distribution, not of the sample.
> B is wrong: the median minimises absolute loss, not 0–1 loss, and the Bayes error rate is positive whenever the class distributions overlap, at any sample size.
> C is wrong: the Bayes classifier weights the likelihood by the prior class probabilities, and classes with different means but overlapping distributions still have a positive Bayes error.
> D is wrong: the roles are swapped, and neither floor depends on the sample size; more data shrink the variance of the estimated rule, not the irreducible error.
> Ref: ISLP §2.2.3 (pp. 37–40); Izbicki & Mendonça Ch. 7 (pp. 133–139); slides `logisticregression-discriminantanalysis.pdf` (slides 41–42)
> Similar: Notas/L02/L02-01-prediction-error-bias-variance.md §2–§3; Notas/L02/L02-05-discriminant-analysis.md §2.1; I 2.1 (p. 63)

## cls

Q: A spam filter is evaluated on a test set of e-mails. Its false-positive rate is about 5.7%, yet about 9.1% of the e-mails it flags as spam are legitimate. Which statement is correct?
- One of the two numbers must be miscomputed, because the false-positive rate is by definition the share of flagged e-mails that turn out to be legitimate, so the two figures describe one and the same quantity.
- The 9.1% is one minus the sensitivity, so the filter misses about one spam in eleven, while the false-positive rate measures how often legitimate mail is flagged; together they give the whole confusion matrix.
- Both count legitimate e-mails that were flagged, over different totals: all legitimate e-mails for the false-positive rate, all flagged e-mails for the false-discovery rate, so the two figures do not conflict.
- The gap shows that the test set is unbalanced; both rates would equal the overall error rate if spam and legitimate e-mails appeared in equal numbers, since balance makes all the error measures coincide.
<!-- YW5zOjI= -->
> A is wrong: the false-positive rate conditions on the true class, legitimate mail, while the share of flagged mail that is legitimate conditions on the decision; they are different quantities.
> B is wrong: one minus the sensitivity is the share of spam that is missed, which conditions on spam; the 9.1% conditions on being flagged.
> C is right: same numerator, different denominators; the false-discovery rate exceeds the false-positive rate here because fewer e-mails were flagged than were legitimate. Unlike the false-positive rate, the false-discovery rate also moves with the share of spam, the way a posterior moves with the prior.
> D is wrong: balance changes the false-discovery rate but not the false-positive rate, and even with equal classes the two coincide only by accident; neither has to equal the overall error rate.
> Ref: ISLP §4.4.2 (pp. 150–156); Izbicki & Mendonça Ch. 7 (pp. 133–139), §9.1 (pp. 169–172); slides `logisticregression-discriminantanalysis.pdf` (spam confusion matrix)
> Similar: Notas/L02/L02-04-logistic-regression.md §9; Notas/L02/L02-08-pitfalls.md §11; MS 8.9

Q: A binary feature is used to allocate an individual to one of two classes. The maximum-likelihood rule sends each value of the feature to the class under which that value is more likely. With a prior probability of 0.25 on the first class, the Bayes rule allocates every individual to the second class. Which statement is correct?
- The Bayes rule here is inadmissible, because it never allocates anyone to the first class, while the maximum-likelihood rule is the only admissible rule, since it uses all of the information in the feature.
- The two rules must coincide whenever the feature is informative, so this Bayes rule signals a prior so strong that it overrides the likelihood, and the maximum-likelihood rule should be preferred in practice.
- The maximum-likelihood rule minimises the probability of error whatever the prior, because it treats the two classes symmetrically, so the Bayes rule can lower the error only by using a different loss function.
- The Bayes rule compares the likelihood ratio with the prior odds, not with one, so with this prior no feature value is strong enough to favour the first class; sending everyone to the second class lowers the error.
<!-- YW5zOjM= -->
> A is wrong: a rule is inadmissible only if another rule does at least as well in every class and better in one; sending everyone to the second class is the Bayes rule for small priors and is admissible, and so is the maximum-likelihood rule.
> B is wrong: the rules coincide only for priors in an intermediate range; a prior of 0.25 is not extreme, and the Bayes rule is the one that minimises the error probability under it.
> C is wrong: the maximum-likelihood rule is the Bayes rule for equal priors only, so its symmetry is a choice of prior, not a guarantee of minimal error.
> D is right: allocate to the first class only where the likelihood ratio exceeds the prior odds of the second class, here three; in the course's example the maximum-likelihood rule errs with probability 0.3125 and the all-to-second rule with 0.25.
> Ref: Izbicki & Mendonça Ch. 7 (pp. 133–139); slides `logisticregression-discriminantanalysis.pdf` (slides 41–44, 50–52); ISLP §4.4 (pp. 146–148)
> Similar: Notas/L02/L02-05-discriminant-analysis.md §2, §4, §9; Notas/L02/L02-08-pitfalls.md §13; I 4.2 (p. 193)

Q: On 85 graduate applicants in three admission classes, linear discriminant analysis misclassifies 8.2% of the applicants it was fitted on and quadratic discriminant analysis 3.5%. Which conclusion is justified?
- QDA is the better classifier, since its error is lower on the same applicants, and its quadratic boundaries nest LDA's linear ones, so a more flexible rule can never predict worse than one it contains.
- None yet: both are resubstitution errors, optimistic by construction, and QDA estimates a covariance matrix per class, so its training edge may be variance; a cross-validated error is needed to compare them.
- LDA is the better classifier, because QDA always overfits when each class has fewer than a hundred members, so its lower training error should be read as proof of overfitting rather than of a better fit.
- QDA is better if and only if the class covariance matrices differ, which its lower error rate already shows, so a formal test of equal covariance matrices would add nothing to the comparison of the two rules.
<!-- YW5zOjE= -->
> A is wrong: nesting guarantees a lower training error, not a lower test error; the extra parameters add variance, which is the bias–variance trade-off of Class 2.
> B is right: errors measured on the fitting data reward flexibility; QDA estimates three covariance matrices instead of one, and only an error estimated on held-out data, as by CV, can say whether that buys accuracy.
> C is wrong: whether QDA overfits depends on the number of predictors, the class sizes and how different the covariances are; no fixed sample size settles it, and a lower training error proves nothing either way.
> D is wrong: even with different covariances, LDA can predict better in small samples because it estimates fewer parameters; and a lower training error does not show the covariances differ.
> Ref: ISLP §4.4.3–4.4.4 (pp. 156–161), §5.1 (pp. 202–212); Izbicki & Mendonça §8.1 (pp. 141–151); slides `logisticregression-discriminantanalysis.pdf` (slides 58–65)
> Similar: Notas/L02/L02-05-discriminant-analysis.md §8; I 4.12, 4.13 (p. 196)

## reg

Q: A regression of the log of house price on the number of rooms gives a rooms coefficient of 0.306, with normal errors independent of rooms. An analyst reads it as a 30.6% rise per room and predicts prices by exponentiating the fitted log price. Which assessment is correct?
- Both steps are right: 100 times the coefficient is the exact percentage change in price per room, and the exponential undoes the log, so the exponentiated fit is an unbiased prediction of the mean price.
- The percentage reading is right, but exponentiating the fitted log price overstates the mean price, because the exponential is convex, so the predictions should be divided by the mean of the exponentiated error.
- The exact change is about 36% for one more room and about 26% less for one fewer, and the exponentiated fit estimates the median price; the mean price is that times the mean of the exponentiated error, above one.
- The percentage reading is wrong because the coefficient is in percentage points, not percent, and exponentiating is invalid, since a log-level model identifies only ratios and so cannot predict any price level.
<!-- YW5zOjI= -->
> A is wrong: 100 times the coefficient is a first-order approximation, five points off at this size; and the exponential of an expected log is not the expected level.
> B is wrong on both counts: the approximation is not exact, and by convexity the mean of the exponentiated error exceeds one, so the exponentiated fit understates the mean price and must be multiplied, not divided.
> C is right: the exact change is 100 times the exponential of the coefficient minus one, asymmetric up and down; with symmetric errors the exponentiated fit is the conditional median, and with normal errors the conditional mean is larger by the factor of the exponential of half the error variance.
> D is wrong: a log-point change in a level variable is a percentage, not a percentage-point change, and the model does predict levels once the error distribution is accounted for.
> Ref: Wooldridge 6e §2.4 (pp. 38–39), §6.2 (pp. 171–173), §6.4 (predicting y when log y is the dependent variable); slides `multiplelinearregression.pdf`
> Similar: Notas/L02/L02-02-linear-log-linear-regression.md §4, §4.1; Notas/L02/L02-08-pitfalls.md §6

Q: Daily counts with many zeros are modelled two ways: OLS of the log of one plus the count on a covariate, and a Poisson regression of the count with a log link. Which statement is correct?
- The Poisson slope is a log rate ratio for the mean count, consistent whenever the log of the mean is linear even without Poisson variance; the OLS slope describes the mean of a transformed count and is no rate ratio.
- The two slopes estimate the same log rate ratio, since both models put the covariate inside a log; OLS is preferred because its standard errors do not rest on the Poisson assumption that the variance equals the mean.
- The Poisson model is invalid with many zeros, because the log of zero is undefined, so the shifted OLS model is the only one that can be fitted to these counts without dropping the days with no events at all.
- The Poisson slope is biased when the variance exceeds the mean, while the OLS slope on the shifted log is unbiased for the rate ratio, so overdispersed counts should always be modelled by the shifted regression.
<!-- YW5zOjA= -->
> A is right: the log link models the log of the expected count, so the slope is a log rate ratio; its score equations involve only the mean, so the estimate stays consistent under overdispersion, and only the standard errors need a dispersion correction.
> B is wrong: the expected log of one plus the count is not the log of the expected count, so the OLS slope estimates a different quantity that depends on the whole distribution of the counts.
> C is wrong: the Poisson likelihood takes the log of the mean, not of the observed count, so zeros enter without any difficulty.
> D is wrong: overdispersion leaves the Poisson coefficients consistent and inflates only their true standard errors, while the shifted regression has no rate-ratio target to be unbiased for.
> Ref: ISLP §4.6 (pp. 167–173); Wooldridge 6e §17.3 (pp. 543–547); site page `Gaussian-vs-Poisson-regression.html`
> Similar: Notas/L02/L02-06-gaussian-vs-poisson-regression.md §3–§5; Notas/L02/L02-08-pitfalls.md §14–§15; W 17.C5
