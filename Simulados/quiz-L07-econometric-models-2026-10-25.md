---
quiz: "L07 · Class 7: More econometric models — general linear model, hierarchical models, limited dependent variables"
tags:
  glm: "General linear model: heteroskedastic, Student-t, AR errors, SUR"
  hlm: "Hierarchical (multilevel) models"
  ldv: "Limited dependent variables: Tobit and probit family"
---

## glm

Q: In a cost function for US airlines, the log of the squared OLS residuals rises clearly with the load factor. A researcher then models the error variance as an exponential function of the load factor and fits the model by Bayesian MCMC. Which statement is correct?
- Heteroskedasticity makes the OLS slopes biased, so the variance model is needed to recover the cost elasticities, and the fitted elasticities should change sharply once it is introduced
- Modelling the variance changes the estimand, since the weighted fit targets the elasticity of high load-factor airlines, whose observations receive the largest weights under generalized least squares
- The OLS slopes stay unbiased under exogeneity, but their usual standard errors are wrong and they are inefficient; the variance parameters lack a conjugate update, so Metropolis steps are needed
- Robust standard errors would make the variance model redundant, since they deliver both valid inference and the efficiency gain of weighting without saying how variance depends on load factor
<!-- YW5zOjI= -->
> Heteroskedasticity does not touch unbiasedness or consistency of OLS under exogeneity; it breaks the usual variance formula and Gauss–Markov efficiency. Weighting by the modelled variance (GLS) targets the same coefficients, only more precisely. Robust standard errors repair inference but not efficiency. In the Bayesian fit, the coefficients and scale have standard conditionals given the variance function, but the parameters inside the exponential do not, so the lecturer uses random-walk Metropolis steps for them.
> Ref: Class 7 slides, GLM3.pdf (known diagonal covariance, variance as a function of covariates; US airlines example); Wooldridge 6e, Ch. 8, §8.1–8.4, pp. 243–265
> Similar: Wooldridge 6e, Ch. 12, C10, p. 399

Q: A linear regression has Student-t errors, and the Bayesian fit writes each error as normal with its own variance multiplier drawn from an inverse-gamma distribution governed by the degrees of freedom. What does this representation buy?
- Given the multipliers, the model is a normal regression with known weights, so coefficients and scale have standard conditionals; large multipliers flag outliers and downweight them
- It makes the degrees of freedom conjugate, so the whole sampler is Gibbs, and it forces every observation to receive the same weight, which preserves the unbiasedness of least squares
- It turns the t model into a mixture of a few normal components, one per cluster of observations, so the multipliers identify groups of units that share a common error variance in the data
- It removes the need for any prior on the degrees of freedom, since the multipliers average out to one in large samples and the tail thickness is then estimated without any uncertainty
<!-- YW5zOjA= -->
> The t distribution is a scale mixture of normals. Conditional on the multipliers, the model is a heteroskedastic normal regression with known weights, so the coefficients and scale have normal and inverse-gamma conditionals, and each multiplier has an inverse-gamma conditional; an observation with a large residual draws a large multiplier and gets a small weight. The degrees of freedom are not conjugate and need a Metropolis step, and their prior matters: Geweke shows that a flat prior on them can leave posterior moments undefined. Each observation gets its own multiplier, not a cluster.
> Ref: Class 7 slides, GLM3.pdf (Student-t errors as a scale mixture); Greenberg 1e, Ch. 8, §8.1, pp. 111–117
> Similar: Greenberg 1e, Ch. 8, Exercise 8.5, p. 132; Exercise 8.3, p. 132

Q: A static regression of a time series on a strictly exogenous regressor has AR(1) errors, and the Bayesian version puts a normal prior on the error autocorrelation truncated to the interval between minus one and one. Which statement is correct?
- OLS slopes are inconsistent whenever the errors are autocorrelated, so the truncation matters for the coefficients themselves, and the AR error model is required for any valid slope estimate
- The truncation is a numerical convenience that speeds up the sampler and carries no substantive content, since the likelihood alone already rules out an explosive error process
- With positively autocorrelated errors and regressor, the usual OLS standard errors are too large, so OLS is conservative and the AR error model mainly serves to narrow confidence intervals
- OLS stays consistent under strict exogeneity but overstates precision when errors and regressor are both positively autocorrelated; the truncation keeps the error process stationary
<!-- YW5zOjM= -->
> With strictly exogenous regressors, serial correlation leaves OLS unbiased and consistent; inconsistency arises when a lagged dependent variable meets autocorrelated errors. Positive autocorrelation in both errors and regressor makes the usual standard errors too small, so OLS t statistics look better than they are. Restricting the autocorrelation to the stationary region is substantive: it makes the error covariance matrix well defined and rules out unit-root or explosive errors, which links this model to the unit-root issues of class 8. The truncated-normal conditional is sampled by inverse-cdf draws inside a Metropolis step.
> Ref: Class 7 slides, GLM3.pdf (autoregressive errors, truncated-normal prior); Wooldridge 6e, Ch. 12, §12.1, pp. 373–376 and §12.3, pp. 381–387; Tsay AFTS 3e, Ch. 2, §2.9, pp. 90–97
> Similar: Wooldridge 6e, Ch. 12, C2, p. 397; C10, p. 399

Q: Seemingly unrelated regressions stack several equations whose errors are correlated across equations at the same date. When does joint GLS estimation beat equation-by-equation OLS?
- Always, since joint estimation uses more data per equation, and the gain grows with the number of equations even when the error correlations across the equations are all zero
- Only when errors are correlated across equations and the equations have different regressors; with identical regressors, as in a VAR, equation-by-equation OLS is already efficient
- Only when the regressors are identical across equations, since then the cross-equation error correlation is estimated precisely and can be used to reweight all of the equations together
- Only when errors are uncorrelated across equations, since correlated errors make the stacked system singular and force the analyst back to estimating each of the equations separately
<!-- YW5zOjE= -->
> SUR gains come from borrowing information through correlated errors, and they need different regressors across equations. With uncorrelated errors the equations are unrelated; with identical regressors, GLS collapses to OLS equation by equation. That is why a reduced-form VAR, a SUR system in which every equation has the same lagged regressors, is estimated efficiently by OLS per equation, the bridge to class 9. Correlated errors do not make the system singular; they are its point.
> Ref: Class 7 slides, GLM3.pdf (seemingly unrelated regressions); Greenberg 1e, Ch. 9, §9.1, pp. 134–139; Tsay AFTS 3e, Ch. 8, §8.2, pp. 399–417
> Similar: Greenberg 1e, Ch. 10, Exercise 10.4, p. 167

## hlm

Q: Weight gain of 68 pregnant women is recorded at 5 to 7 visits each. Three fits are compared: one regression per woman, one pooled regression for all women, and a hierarchical model in which each woman's intercept and slope are drawn from a common population distribution. How do the hierarchical estimates relate to the other two?
- They match the per-woman regressions exactly, since the population distribution only affects predictions for new women and leaves the estimated lines of the observed women unchanged
- Each line is pulled toward the population line, harder when her data are few or noisy relative to between-woman spread; zero spread gives pooling, a huge spread separate fits
- They match the pooled regression, since a common population distribution means that all women share one line, with the individual deviations treated as part of the error term
- Each line is pulled toward the population line by the same fraction, fixed by the prior, so women with seven visits are shrunk exactly as much as women with only five visits
<!-- YW5zOjE= -->
> Partial pooling: each woman's posterior mean is a precision-weighted compromise between her own regression and the population line. The weight on her own data rises with the number and precision of her observations and with the between-woman variance. The two limits recover the other fits: between-woman variance to zero gives complete pooling, to infinity gives no pooling. The shrinkage is learned from data, not fixed, and it differs across women.
> Ref: Class 7 slides, HLM.pdf (pooled, individual-effects and random-coefficients models); Class 7 site code, hierarchicalmodel.html; Greenberg 1e, Ch. 4, §4.5–4.6, pp. 50–53 and Ch. 9, §9.3, pp. 144–149
> Similar: Greenberg 1e, Ch. 9, Exercise 9.2, p. 151; Exercise 9.3, p. 151

Q: A panel of firms is analysed with firm-specific intercepts in two ways: as free parameters with a flat prior, and as draws from a common normal distribution independent of the regressors. Which comparison is correct?
- The two always give identical slope estimates, because with a flat prior on the common coefficients the hierarchical layer has no effect on their posterior distribution
- The free-intercept version is the more efficient one, since estimating each intercept separately uses more information than assuming that intercepts come from a shared distribution
- The hierarchical version is robust to correlation between intercepts and regressors, since the second-level distribution absorbs that correlation into the estimated between-firm variance
- The free version mirrors fixed effects, valid if intercepts correlate with regressors; the hierarchical one mirrors random effects, more efficient but biased under that correlation
<!-- YW5zOjM= -->
> Free intercepts with a flat prior reproduce the within (fixed-effects) estimator, which allows intercepts to be correlated with the regressors. A normal hierarchical prior independent of the regressors is the Bayesian random-effects model: it uses between-firm variation and shrinks intercepts, which is more efficient when the independence assumption holds and biased when it fails, the comparison a Hausman test makes. The hierarchical layer does change the slope posterior, because the intercepts are no longer free; it does not absorb correlation with regressors unless that correlation is modelled.
> Ref: Class 7 slides, HLM.pdf (individual-effects model, non-hierarchical vs hierarchical prior); Wooldridge 6e, Ch. 14, §14.1–14.3, pp. 435–448; MHE Ch. 5, §5.1, pp. 165–168
> Similar: Wooldridge 6e, Ch. 14, C5, p. 454

Q: In a hierarchical normal model for eight schools, each school's estimated coaching effect has a known standard error, the true effects are drawn from a normal with unknown mean and unknown between-school standard deviation, and that standard deviation gets a uniform prior from 0 to 100. Its posterior piles up near zero. What does that mean?
- The estimates are pooled strongly toward the common mean, but the data cannot rule out moderate differences, and with only eight groups the prior on that spread still matters
- The data prove the eight coaching effects identical, so separate school estimates are pointless, and the result would not change under any other reasonable prior on the spread
- The sampler has failed to converge, since a variance parameter piling up at the boundary of its support is a sign of poor mixing rather than a feature of the posterior itself
- The uniform prior is too informative and has forced the spread toward zero, so the separate per-school estimates are the correct answer and the hierarchy should be abandoned
<!-- YW5zOjA= -->
> A posterior for the between-group spread concentrated near zero drives strong shrinkage toward the common mean, but it is a distribution, not a point: its right tail leaves room for real differences. With eight noisy estimates the likelihood for the spread is flat-ish, so the prior's shape near zero influences the answer, a known sensitivity of hierarchical variance priors. Mass at a boundary is a legitimate posterior feature, not a convergence failure, and a uniform prior on the standard deviation is fairly weak, not one that forces zero.
> Ref: Class 7 slides, HLM.pdf (simple hierarchical model in WinBUGS); Greenberg 1e, Ch. 4, §4.5–4.6, pp. 50–53
> Similar: Greenberg 1e, Ch. 9, Exercise 9.3, p. 151

## ldv

Q: Weekly hours worked are zero for many women in a sample. A researcher fits a Tobit with a latent normal index and, in a Bayesian version, draws a latent value below zero for each woman with zero hours. Which statement is correct?
- OLS on the women with positive hours is unbiased for the latent slope, since dropping the zeros removes the censoring, so the Tobit matters only for the women who do not work at all
- Tobit and OLS on the full sample target the same slope, and the Tobit is preferred only because it is more efficient when the share of zeros in the sample happens to be large
- OLS on all women or on workers alone is biased for the latent slope; Tobit fixes this if one index drives both whether and how much to work, a strong claim for corner solutions
- The latent draws free the Tobit from distributional assumptions, since the truncated normal is only a sampling device and does not restrict the shape of the hours distribution
<!-- YW5zOjI= -->
> Dropping the zeros truncates the sample on the outcome and biases OLS; keeping them and fitting a line flattens it. The Tobit corrects both under its assumptions: normal, homoskedastic latent errors and a single index governing participation and intensity. If zeros are corner solutions from a separate decision, those assumptions bite, and Angrist and Pischke stress that the Tobit's latent-index parameters are of interest only when the data are genuinely censored. Data augmentation (Chib) imputes latent values from a truncated normal, but the normality is part of the model, not a device.
> Ref: Class 7 slides, limiteddependentvariablemodels.pdf (Tobit, data augmentation); Wooldridge 6e, Ch. 17, §17.2, pp. 536–543 and §17.4, pp. 547–553; MHE Ch. 3, §3.4.2, pp. 70–80
> Similar: Wooldridge 6e, Ch. 17, C9, p. 562; Greenberg 1e, Ch. 8, Exercise 8.6, p. 132

Q: A probit sets the latent error variance to one and the threshold to zero, an ordered probit fixes its first cutpoint, and a multinomial probit models utilities relative to a base alternative. What do these normalizations have in common?
- They are conveniences that speed up estimation but leave every parameter identified, so dropping them would only make the sampler slower without changing what the data can reveal
- They make coefficients directly comparable across models with different error assumptions, so a probit coefficient can be read as a logit coefficient or as a linear-probability slope
- They are needed only in Bayesian estimation, since maximum likelihood identifies the latent scale and location from the curvature of the likelihood, which priors would otherwise distort
- Choices reveal only the sign or order of latent utility, not its location or scale, so these are fixed; coefficients are identified up to scale, and marginal effects are what compare
<!-- YW5zOjM= -->
> A binary or ordered outcome records which interval the latent variable fell in; shifting the latent variable and the thresholds together, or rescaling everything, leaves every probability unchanged. Fixing the threshold and the variance (probit), one cutpoint (ordered probit), or the base utility and a scale of the covariance (multinomial probit, as Keane and McCulloch–Rossi discuss) removes that indeterminacy. Coefficients are then on an arbitrary scale, so probit and logit coefficients differ by roughly a constant factor while marginal effects are comparable. The problem is the same for maximum likelihood and Bayes.
> Ref: Class 7 slides, limiteddependentvariablemodels.pdf (probit, ordered and multinomial probit); Wooldridge 6e, Ch. 17, §17.1, pp. 525–536; Greenberg 1e, Ch. 8, §8.2, pp. 117–129
> Similar: Wooldridge 6e, Ch. 17, C2, p. 561; Greenberg 1e, Ch. 8, Exercise 8.7, p. 132

Q: A Bayesian treatment of Student-t regression, Tobit, probit and multinomial probit uses the same computational device in all four. What is that device, and why does it work?
- Adding latent variables, such as variance multipliers, latent outcomes or latent utilities, so that given them each model is a Gaussian linear regression whose conditionals are standard
- Replacing each likelihood with a normal approximation at its mode, so that the posterior is Gaussian and can be sampled directly without any Markov chain or latent quantities at all
- Rewriting each model as a generalized linear model with a link function, so that iteratively reweighted least squares gives the posterior mode and its curvature gives the uncertainty
- Running one Metropolis random walk on all parameters jointly, since none of these models has a tractable conditional distribution for its regression coefficients given the data
<!-- YW5zOjA= -->
> Data augmentation: t errors become normal given observation-specific multipliers; Tobit becomes normal regression given latent values for the censored points; probit (Albert and Chib) becomes normal regression given latent utilities drawn from truncated normals; multinomial probit becomes a SUR-type system given the latent utility vector. The Gibbs sampler then alternates between the latent quantities and conjugate updates for coefficients and variances. Normal approximations and IRLS are alternatives, not what unifies these slides, and coefficient conditionals are exactly what augmentation makes tractable.
> Ref: Class 7 slides, GLM3.pdf and limiteddependentvariablemodels.pdf; Greenberg 1e, Ch. 8, §8.1–8.2, pp. 111–129
> Similar: Greenberg 1e, Ch. 8, Exercise 8.6, p. 132; Exercise 8.7, p. 132
