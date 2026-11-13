---
quiz: "L07 · Class 7: More econometric models, hard conceptual — WLS/GLS, error structures, partial pooling, limited dependent variables"
tags:
  gls: "General linear model: WLS/GLS, AR(1) and Student-t errors"
  hlm: "Hierarchical models and partial pooling"
  ldv: "Tobit, ordered and multinomial probit"
---

## gls

Q: Savings are regressed on income by weighted least squares, assuming the error variance is proportional to income, and the WLS standard error of the income slope comes out much smaller than the heteroskedasticity-robust OLS one. In truth the error variance rises with the square of income. Which statement is correct?
- WLS is now biased, because weights built from the wrong variance function are correlated with the error, so the gain in precision is paid for with a slope that no longer estimates the population coefficient
- The small WLS standard error is valid, because any weighting that moves toward the true variance pattern removes the heteroskedasticity, and the remaining misspecification only affects the intercept
- WLS stays consistent under exogeneity but is no longer efficient, and its usual standard error, computed as if the variance model held, is invalid; robust standard errors on the weighted fit are needed
- The comparison proves the variance model correct, since a misspecified weighting can only inflate the standard error relative to robust OLS, never shrink it, so the gap is evidence for the assumed form
<!-- YW5zOjI= -->
> A is wrong: the weights are functions of income, which is exogenous, so weighting by any function of income keeps the estimator consistent; a wrong variance function costs efficiency, not consistency.
> B is wrong: weights proportional to the inverse of income leave the transformed errors heteroskedastic when the true variance rises with income squared, so the usual WLS standard error of the slope is still wrong.
> C is right: Wooldridge stresses that the WLS standard error is computed under the assumed variance function; if it is wrong, WLS is still consistent but its usual inference fails, and a robust variance for the weighted regression repairs it.
> D is wrong: a misspecified WLS can report a standard error that is too small, which is exactly why a smaller WLS standard error is no proof that the variance model is right.
> Ref: Wooldridge 6e §8.4, pp. 254–262 (WLS, FGLS, misspecified variance function p. 261); Class 7 slides, GLM3.pdf (known diagonal covariance)
> Similar: Wooldridge 6e, Ch. 8, Example 8.6 (401KSUBS), p. 257

Q: A static time-series regression with a strictly exogenous regressor has AR(1) errors with positive autocorrelation. In case 1 the regressor is serially uncorrelated; in case 2 it follows an AR(1) with a negative coefficient. Which statement about OLS is correct?
- In case 1 the usual OLS standard error is asymptotically right, yet OLS is still inefficient relative to GLS; in case 2 the usual standard error overstates the true sampling variability of the slope
- In both cases the usual OLS standard error understates the true sampling variability, since positive error autocorrelation always makes the residuals look more informative than they are
- In case 1 OLS is fully efficient, since an uncorrelated regressor makes the error autocorrelation irrelevant; in case 2 OLS becomes biased, because the regressor and the error now move together over time
- In both cases OLS is biased, since autocorrelated errors break the conditions for unbiasedness, and a Prais–Winsten correction is needed to recover the slope before any standard error is computed
<!-- YW5zOjA= -->
> A is right: the ratio of the true to the naive OLS variance depends on the product of the error and regressor autocorrelations; it is one when the regressor is white noise and below one when the product is negative, while GLS beats OLS in efficiency in both cases.
> B is wrong: understatement needs the regressor to be autocorrelated in the same direction as the errors; with a negatively autocorrelated regressor the naive standard error is too large.
> C is wrong: the correct standard error in case 1 does not make OLS efficient, since GLS still uses the error correlation; and strict exogeneity keeps OLS unbiased in case 2.
> D is wrong: with a strictly exogenous regressor, serial correlation affects variances and efficiency, not unbiasedness; Prais–Winsten is an efficiency correction for the same slope.
> Ref: Wooldridge 6e §12.1–12.3, pp. 373–387; Class 7 slides, GLM3.pdf (AR(1) errors)
> Similar: Wooldridge 6e, Ch. 12, C2 and C10

Q: A wage regression is fitted twice by MCMC, once with normal errors and once with Student-t errors with about five degrees of freedom. The posterior mean of the error scale parameter falls by about a third under the t model, and a few observations get very small posterior weights. An analyst concludes that the t model finds the wage equation much less noisy. Which assessment is correct?
- The conclusion is right, because the scale parameter of the t model is the error variance, and the t likelihood simply fits the bulk of the data more tightly once the outliers are allowed for
- The conclusion is right for a different reason: the small weights remove the outliers from the sample, so the t model is estimated on a cleaner subset whose error variance is truly lower
- The conclusion is wrong because the weights are random effects that must be added back to the residual variance, which makes the t model's error variance larger than the normal model's by construction
- The conclusion is wrong: under t errors the variance is the scale times a factor above one set by the degrees of freedom, so the total spread can be nearly unchanged while the outliers are downweighted
<!-- YW5zOjM= -->
> A is wrong: in the t model the scale is not the variance; with five degrees of freedom the variance is the scale times five thirds, which roughly undoes a fall of one third.
> B is wrong: the outliers are not removed; each observation keeps its likelihood contribution, and a large residual simply draws a large variance multiplier and a small weight.
> C is wrong: the multipliers are a computational device that is integrated out, not random effects to report, and adding them back does not make the t variance larger by construction.
> D is right: Greenberg's Vella–Verbeek example has the scale fall from about 0.165 to 0.105 under five degrees of freedom while the implied variance, about 0.175, barely moves; the t model reallocates weight, not spread.
> Ref: Greenberg 1e §8.1, pp. 111–117; Class 7 slides, GLM3.pdf (Student-t errors as a scale mixture)
> Similar: Greenberg 1e, Ch. 8, Exercises 8.3 and 8.5, p. 132

Q: In a Bayesian regression with Student-t errors and an exponential prior on the degrees of freedom, the chain for the degrees of freedom wanders between about 5 and 60, its autocorrelation is still high at lag 30, and deleting one outlier moves its posterior mean a lot. Which reading is correct?
- The sampler has failed, since a well-specified model always gives a concentrated posterior for the degrees of freedom; running the chain longer makes it settle on a single value that measures the tails
- The degrees of freedom are weakly identified, since tail thickness is learned from a few extreme residuals, so the posterior leans on the prior; a wide range is no evidence of normality
- Large draws of the degrees of freedom show the errors are normal, so the model should be refitted by OLS with normal errors; the t specification only adds a parameter that the data reject
- The wandering comes from the variance multipliers, which are random effects to report; once their posterior means are fixed at their estimates, the degrees of freedom become conjugate and the chain mixes well
<!-- YW5zOjE= -->
> A is wrong: a wide posterior is a property of the information in the data, not a sampler failure; longer runs describe the same wide posterior more precisely.
> B is right: only a few large residuals speak to tail thickness, so the posterior of the degrees of freedom is wide, sensitive to single points and to the prior, which already puts noticeable mass on large values.
> C is wrong: draws in the high range coexist with draws near five, so the data do not reject heavy tails; and the coefficient estimates under the t model are robust either way.
> D is wrong: the degrees of freedom have a non-standard full conditional and need a Metropolis step whatever is done to the multipliers, and fixing the multipliers would understate uncertainty.
> Ref: Class 7 slides, GLM3.pdf (Student-t errors, MCMC output for the degrees of freedom); Greenberg 1e §8.1, pp. 111–117
> Similar: Greenberg 1e, Ch. 8, Exercise 8.5, p. 132

## hlm

Q: In a hierarchical normal model, each unit's true mean is drawn from a common population distribution with unknown mean and unknown between-unit variance, and units differ in how many observations they contribute. Which statement about the posterior means of the unit effects is correct?
- Each estimate is pulled toward zero, as in ridge regression, and units with extreme raw means are pulled hardest because the penalty grows with the square of the estimate, whatever their sample sizes
- Every unit is pulled toward the population mean by the same fraction, set by the between-unit variance alone, so the ranking of units and the relative distances between their raw means are preserved
- Units with many observations are pulled further toward the population mean, because their larger samples estimate the population better, while units with few observations keep their raw means
- Each estimate moves toward the estimated population mean, more when the unit's data are noisy and the between-unit variance is small; units with few observations shrink most, so rankings can change
<!-- YW5zOjM= -->
> A is wrong: shrinkage is toward the estimated population mean, not toward zero; in the eight-schools example the school with a negative raw effect moves up toward the mean of about 8.
> B is wrong: the shrinkage fraction depends on each unit's own sampling variance relative to the between-unit variance, so it differs across units whenever their precisions differ.
> C is wrong: it inverts the weights; a unit's own data get more weight the more precise they are, so large units stay close to their raw means.
> D is right: the posterior mean is a precision-weighted average of the unit's raw mean and the population mean, so imprecise units move most, and units with different precisions can swap places.
> Ref: Class 7 slides, HLM.pdf (eight schools, slide 23; individual-effects model); Greenberg 1e §4.6, pp. 52–53
> Similar: Greenberg 1e, Ch. 4, Exercise 4.6

Q: For one woman in a hierarchical growth model of weight during pregnancy, a 95% band around her fitted line is computed from the posterior draws of her own intercept and slope. A clinician flags any new measurement that falls outside that band as abnormal. What is wrong with the rule?
- The band describes uncertainty about her mean line only; a new measurement also carries the within-woman noise, so the predictive band is wider and the rule flags far too many normal visits
- Nothing is wrong, since a posterior band already integrates over all parameter uncertainty, including the measurement noise, and so it is the predictive band for a new visit of the same woman
- The band is too narrow because shrinkage toward the population line removes her individual variation; refitting her line by separate least squares would give the right band for new visits
- The band is too wide because it includes the between-woman variance of the population distribution, which no longer applies once her own intercept and slope are learned from her visits
<!-- YW5zOjA= -->
> A is right: the band is the posterior of her intercept plus slope times week, a band for the mean line; a new measurement adds the observation noise, so the predictive band is wider.
> B is wrong: integrating over parameters gives a band for a function of parameters; the observation noise enters only when a new observation is simulated from the likelihood.
> C is wrong: the narrowness has nothing to do with shrinkage, and separate least squares on five to seven points would give a noisier line with a band for the mean line all the same.
> D is wrong: her posterior already conditions on her data, and the between-woman variance enters only through the prior for her coefficients; it would matter fully only for a new woman.
> Ref: Class 7 slides, HLM.pdf (random-coefficients model, nutrition of pregnant women); site page hierarchicalmodel.html
> Similar: Greenberg 1e, Ch. 9, Exercises 9.2 and 9.3

Q: In the Gibbs sampler for a hierarchical model in which unit intercepts are drawn from a normal population with unknown mean, the full conditional of that population mean is drawn given the current intercepts, the data and the other parameters. Which statement is correct?
- The likelihood does not involve the population mean, so it is not identified and its full conditional equals its prior; the sampler only carries it along as a device to speed up mixing
- Each intercept enters the update with the precision of the observation noise times the number of observations of its unit, since that is how precisely its own data measure the intercept
- Given the intercepts, the data carry no more information on the population mean, so its update is a normal–normal step treating the intercepts as data, each with the between-unit precision
- The update must condition on the data directly rather than on the intercepts, since conditioning on drawn intercepts counts the same information twice and makes the posterior of the mean too narrow
<!-- YW5zOjI= -->
> A is wrong: the data do not depend on the population mean directly, but the intercepts do, so its full conditional is updated by the intercept draws; Greenberg's remark is that it is not identified by the likelihood alone, not that it is never learned.
> B is wrong: that precision belongs to the update of each intercept from its own data; in the population-mean step each intercept is a draw from the population, with the between-unit precision.
> C is right: in the hierarchy the data depend on the population mean only through the intercepts, so conditioning on them makes the data irrelevant, and the step is a conjugate normal update.
> D is wrong: Gibbs sampling alternates full conditionals and does not double count; marginalizing over the intercept draws across iterations gives the correct posterior of the mean.
> Ref: Class 7 slides, HLM.pdf (full conditionals, slides 11–13); Greenberg 1e §4.6, p. 52, and §9.3, pp. 144–149
> Similar: Greenberg 1e, Ch. 4, Exercise 4.6

## ldv

Q: Annual hours of work are zero for many married women. Three fits of hours on years of education are compared: OLS on all women including the zeros, OLS on the working women only, and a Tobit with a latent normal index. Which statement is correct?
- OLS on working women is unbiased for the effect on hours among workers, because dropping the zeros removes the censoring, and the Tobit coefficient should match it once the sample is restricted the same way
- Both OLS fits are biased, in different ways; the Tobit coefficient is the effect on latent desired hours, and its effect on expected observed hours is scaled down by the probability of working
- The Tobit coefficient is the marginal effect on observed hours, so it should be compared directly with the full-sample OLS slope, which is biased only because zeros are rounded values of small positive hours
- Censoring and truncation are the same problem here, since in both samples the zeros carry no information on education, so the two OLS fits share one bias and the Tobit corrects both by the same factor
<!-- YW5zOjE= -->
> A is wrong: keeping only workers truncates the sample on the outcome, so the error is no longer mean-zero given education, and OLS on that subsample is biased too.
> B is right: the full-sample OLS slope is roughly the latent slope times the share uncensored, the truncated fit has its own bias, and the Tobit's effect on expected observed hours multiplies the coefficient by the probability of a positive outcome.
> C is wrong: the Tobit coefficient refers to the latent index; zeros are corner solutions, not rounding, and the marginal effect on observed hours is smaller than the coefficient.
> D is wrong: a censored sample keeps the women with zero hours and their education, while a truncated sample loses them; the two OLS biases differ, as the notes' simulation shows.
> Ref: Class 7 slides, limiteddependentvariablemodels.pdf (Tobit); Wooldridge 6e §17.2, pp. 536–543; Greenberg 1e §8.2.1, pp. 117–122
> Similar: Wooldridge 6e, Ch. 17, C2 and C3; Greenberg 1e, Ch. 8, Exercise 8.6

Q: An ordered probit is fitted to a four-category job-satisfaction rating, and a regressor has a positive estimated coefficient. Which statement about its effect is correct?
- It lowers the probability of the lowest category and raises the highest, but its effect on the middle categories can go either way; the coefficient is on a latent scale set by the error variance
- It raises the probability of every category above the lowest, since a higher latent index moves mass upward through all cut-points, and its size is the change in the probability of moving up one category
- Coding the categories one to four and running OLS gives the same sign and, after rescaling by the error variance, the same magnitude, so the ordered probit adds only correct standard errors
- Its effect on each category probability has the coefficient's sign, because the cut-points are fixed in advance by the researcher and only the latent index moves when the regressor changes
<!-- YW5zOjA= -->
> A is right: a higher index shifts the latent distribution past fixed cut-points, so the bottom probability falls and the top rises, while a middle category gains from below and loses above; the scale is set by the unit error variance.
> B is wrong: a middle category can lose probability when the index rises, and the coefficient is a shift in the latent index, not a probability.
> C is wrong: OLS on category codes assumes equally spaced categories; the ordered probit estimates the spacing through the cut-points, and the two need not agree even in sign for particular probabilities.
> D is wrong: the cut-points are estimated, with one normalized to fix the location; and fixed cut-points would not make the middle-category effects share the coefficient's sign.
> Ref: Class 7 slides, limiteddependentvariablemodels.pdf, slides 11–12 (ordered probit); Greenberg 1e §8.2, pp. 117–129
> Similar: Lista L07, original exercise on the ordered probit

Q: Labour-force status is coded as not working, part-time or full-time. A researcher must choose between an ordered probit and a multinomial probit for it. Which comparison is correct?
- The ordered probit is the more flexible model, since its cut-points are free parameters that let each category respond to the regressors in its own way, while the multinomial probit fixes a single index
- The two models coincide when the multinomial error covariance is the identity, because utility differences from the base alternative then line up along one latent index cut by two thresholds
- The ordered probit cuts one index by thresholds, so a regressor cannot raise both extremes at once; the multinomial probit gives each alternative its own coefficients and correlated utilities
- The multinomial probit cannot be used, because its utility differences assume unordered alternatives, and with ordered categories its covariance matrix is not identified even after one variance is fixed
<!-- YW5zOjI= -->
> A is wrong: the cut-points shift the thresholds but every category shares one coefficient vector, so the ordered model is the restrictive one.
> B is wrong: with identity covariance the multinomial probit still has a separate coefficient vector for each utility difference, so it does not collapse to one index with thresholds.
> C is right: the ordered probit imposes a single latent intensity; the multinomial probit is a latent SUR with alternative-specific coefficients and a free covariance, which also needs a scale normalization.
> D is wrong: an ordered outcome can be modelled as an unordered choice; the multinomial probit simply ignores the ordering, and its identification needs the usual location and scale normalizations only.
> Ref: Class 7 slides, limiteddependentvariablemodels.pdf, slides 11–15 (ordered and multinomial probit); Greenberg 1e §8.2, pp. 117–129, and §9.2, pp. 139–144
> Similar: Lista L07, original exercises on ordered and multinomial probit
