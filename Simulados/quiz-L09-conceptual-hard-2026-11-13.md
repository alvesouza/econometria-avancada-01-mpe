---
quiz: "L09 · Class 9: Multivariate time series, hard conceptual — FEVD, SVAR identification, Minnesota BVAR, SSVS, FAVAR, TVP, DCC"
tags:
  var: "VAR inference: IRF bands and FEVD"
  svar: "Structural VAR identification"
  bvar: "Minnesota BVAR, Normal-Wishart and SSVS"
  favar: "FAVAR and time-varying parameters"
  mvol: "Time-varying covariances"
---

## var

Q: A bivariate VAR is identified recursively with variable 1 ordered first. At horizon one, the variance decomposition attributes none of variable 1's forecast-error variance to the second shock, and a share of variable 2's equal to the squared correlation of the two innovations to the first shock. An analyst concludes that variable 1 drives variable 2 within the period. Which assessment is correct?
- The one-step split is imposed by the ordering: the first variable takes all shared innovation variation and the zero is a normalization, not an estimate; reversing the order flips the split
- The zero is the result of a Granger-causality test, since a variance share is estimated from the lag coefficients, so it shows that the lags of variable 2 carry no information about variable 1
- The conclusion is sound, since the shares in each row sum to one whatever the ordering, so the variance decomposition is invariant to permuting the variables and reflects the data alone
- The share is a causal estimate robust to the ordering, since the innovation correlation is symmetric, so reversing the order would leave variable 2's one-step share from the first shock unchanged
<!-- YW5zOjA= -->
> A is right: at horizon one the orthogonalized responses are the Cholesky factor itself, so the first-ordered variable is credited with all the shared variation; with the order reversed, variable 1 would get the squared correlation from the other shock and variable 2 none from it.
> B is wrong: the one-step decomposition uses only the innovation covariance, not the lag coefficients, so it says nothing about Granger causality.
> C is wrong: shares summing to one is an accounting identity in every ordering; the split itself changes with the ordering whenever the innovations are correlated.
> D is wrong: the correlation is symmetric, but its attribution is not; reversing the order moves the whole shared part to the other variable's shock.
> Ref: Class 9 slides, BVAR-part11.pdf, slides 10–12 (VMA, IRF, FEVD); Tsay 3e §8.2, pp. 412–417
> Similar: Tsay 3e, Ch. 8, Exercises 8.1 and 8.2

Q: Bands for orthogonalized impulse responses are built by drawing VAR coefficients from their normal posterior while holding the residual covariance matrix at its point estimate. Which statement is correct?
- The residual covariance does not enter orthogonalized responses, which depend only on the lag coefficients, so holding it fixed has no effect on the bands at any horizon of the response
- The bands come out too wide, since fixing the covariance removes the negative correlation between its draws and the coefficient draws that would otherwise offset each other in the responses
- The responses depend on the covariance through its Cholesky factor, the impact response, so fixing it understates band width, most at short horizons; exact simulation draws the covariance first
- Fixing the covariance is exact under a diffuse prior, because its posterior collapses to the point estimate as the sample grows, so only forecasts and not impulse responses need draws of the covariance
<!-- YW5zOjI= -->
> A is wrong: orthogonalized responses are the reduced-form responses times the Cholesky factor of the covariance, so they depend on it at every horizon.
> B is wrong: leaving out a source of uncertainty can only narrow the bands; under the diffuse prior the covariance and the coefficients are not offsetting in this way.
> C is right: under the diffuse prior the covariance has an inverse-Wishart posterior and the coefficients are normal given it, so exact draws take the covariance first, then the coefficients; the site's recipe fixes the covariance and so understates uncertainty in the impact responses.
> D is wrong: a posterior that concentrates asymptotically is still dispersed in a finite sample, and the impact response is a direct function of the covariance.
> Ref: Class 9 slides, BVAR-part11.pdf, slides 10–12 and 25–26 (diffuse prior); site page VAR-Example.html (IRF bands)
> Similar: Tsay 3e, Ch. 8, Exercise 8.5

## svar

Q: Two structural VARs for the same three variables use different sets of three zero restrictions on the contemporaneous matrix; both are exactly identified, yet they give very different responses to a monetary-policy shock. Which statement is correct?
- The model with the higher likelihood should be chosen, since the two schemes imply different reduced forms and the data can therefore discriminate between them by a likelihood-ratio test
- Exactly identified schemes fit the reduced-form covariance equally well, so the data cannot choose between them; the choice rests on economics, and only overidentifying restrictions are testable
- Both are equally valid, since any scheme with the required number of zeros identifies the contemporaneous matrix, so the difference in responses only reflects sampling error in the coefficients
- The scheme whose responses are more significant should be preferred, since a correctly identified structure isolates a cleaner shock and therefore yields narrower bands around the policy responses
<!-- YW5zOjE= -->
> A is wrong: both schemes fit the same reduced form exactly, so their likelihoods are equal and no test can rank them.
> B is right: an exactly identified SVAR is a reparametrization of the reduced-form covariance, so the identifying zeros are untestable; overidentified schemes restrict the covariance and can be tested.
> C is wrong: counting zeros is necessary, not sufficient, and two identified schemes define different shocks, so the differences are substantive rather than sampling error.
> D is wrong: band width reflects precision, not validity; a mislabelled shock can be estimated very precisely.
> Ref: Class 9 slides, BVAR-part11.pdf, slides 31–37 (structural VAR, illustrations 1–2); Tsay 3e §8.2, pp. 400–401
> Similar: Tsay 3e, Ch. 8, Exercise 8.7

Q: A monthly VAR in output, prices and the policy interest rate is identified recursively with the interest rate ordered last, and a Primiceri-type TVP-VAR with stochastic volatility is later fitted to the same data. Which statement is correct?
- Ordering the rate last makes policy the most exogenous variable, reacting to nothing within the month, and in the TVP-VAR the ordering no longer matters because the covariance can change over time
- The ordering affects only the variance decomposition, not the impulse responses, and the TVP-VAR removes even that dependence because its contemporaneous coefficients are drawn as random walks
- Ordering the rate last means output and prices respond to the policy shock within the month, while the rate reacts only with a lag; the TVP-VAR keeps this timing but lets the size of the responses drift
- The rate reacts within the month to output and prices, which respond to policy with a lag; the TVP-VAR also uses a lower-triangular contemporaneous matrix, so its ordering matters at every date
<!-- YW5zOjM= -->
> A is wrong: the last-ordered variable responds to every other innovation within the period, so it is the least restricted; and a time-varying covariance does not remove the need for identification.
> B is wrong: the ordering changes the orthogonalized impulse responses as well as the variance decomposition, and random-walk drift does not make it irrelevant.
> C is wrong: it reverses the timing; under a recursive ordering, a variable ordered earlier does not respond within the period to shocks of variables ordered after it.
> D is right: Primiceri writes the covariance through a lower-triangular contemporaneous matrix and diagonal stochastic volatilities, a recursive SVAR whose coefficients and variances drift, so the ordering is an identifying assumption at each date.
> Ref: Class 9 slides, BVAR-part11.pdf, slides 31–37 (recursive identification) and 41–44 (TVP-VAR-SV, Primiceri 2005)
> Similar: Lista L09, original exercise on the TVP-VAR and the Kalman filter

## bvar

Q: In a Minnesota prior for a VAR, which description of the hyperparameters is correct?
- A larger overall tightness parameter means a stronger prior; lag decay makes the first lags tighter than distant ones; a cross-variable factor above one lets other variables count more than own lags
- The overall tightness scales the prior means toward zero; lag decay shortens the lag order directly; the cross-variable factor equals one by default; the variance ratio standardizes the data first
- The overall tightness scales all prior standard deviations: small means a random walk, large means OLS; lag decay tightens distant lags; a cross-variable factor below one tightens other variables' lags
- The overall tightness sets the prior on the error covariance; lag decay applies only to other variables' lags; the cross-variable factor below one loosens them relative to own lags; the variance ratio fixes heteroskedasticity
<!-- YW5zOjI= -->
> A is wrong: the overall tightness multiplies prior standard deviations, so larger means looser; lag decay tightens distant lags, not the first ones; and the cross-variable factor is set below one.
> B is wrong: the prior means are fixed at the random walk, with own first lag one and all else zero; lag decay shrinks distant lags toward zero without cutting them, and the cross-variable factor is usually below one.
> C is right: shrinking the overall tightness to zero returns the random-walk prior mean, letting it grow returns OLS; the lag factor makes the prior tighter as the lag grows, and the cross-variable factor below one encodes that own lags matter most.
> D is wrong: the original Minnesota prior fixes the error covariance; lag decay applies to all lags; the cross-variable factor below one tightens other variables' lags; and the variance ratio only puts coefficients in the right units.
> Ref: Class 9 slides, BVAR-part11.pdf, slides 22–24 (Litterman's Minnesota prior)
> Similar: Lista L09, original exercise on a large BVAR with a Minnesota-type prior

Q: A large Bayesian VAR uses a conjugate Normal–inverse-Wishart prior instead of the original Minnesota prior with a fixed diagonal error covariance. What does the switch cost and buy?
- Its Kronecker form gives every equation the same relative tightness across regressors, so own lags cannot be shrunk less than others; in exchange the covariance is unknown and the posterior is closed-form
- Nothing is lost, since the Normal–inverse-Wishart prior is the Minnesota prior with the error covariance treated as unknown, and both allow own and other lags to be shrunk at different rates
- It forces the equations to be estimated independently, since the Kronecker form makes the error covariance diagonal, so the gain in speed is paid for by ignoring correlated innovations across equations
- It removes shrinkage toward the random walk, since a conjugate prior must be centred at zero for all coefficients, so the prior can only be used for series that are stationary in levels
<!-- YW5zOjA= -->
> A is right: with prior covariance equal to the error covariance times a common matrix, each equation's coefficients get the same relative tightness, which forces the cross-variable factor to one; the gain is a closed-form matrix-t posterior with the covariance unknown.
> B is wrong: the Kronecker restriction is exactly what rules out Minnesota's asymmetric treatment of own and other lags, forcing the cross-variable factor to one; for more general prior beliefs Kadiyala and Karlsson point to the Normal-Diffuse and extended natural conjugate priors instead.
> C is wrong: the Kronecker form does not make the covariance diagonal; the inverse-Wishart prior leaves it unrestricted.
> D is wrong: a conjugate normal prior can be centred anywhere, including the random walk.
> Ref: Class 9 slides, BVAR-part11.pdf, slides 25–30 (Kadiyala and Karlsson priors)
> Similar: Lista L09, original exercise on a large BVAR with a Minnesota-type prior

Q: Compare the Minnesota prior with stochastic search variable selection, which gives each VAR coefficient a mixture of a narrow spike and a wide slab around zero. Which statement is correct?
- SSVS sets coefficients exactly to zero and selects one restricted VAR, keeping a coefficient when its t statistic exceeds about two, so it is a Bayesian version of sequential significance testing
- SSVS is the Minnesota prior with a smaller overall tightness, since both shrink every coefficient by the same factor toward zero, and they differ only in how that factor is chosen from the data
- SSVS needs the same random-walk prior means as Minnesota, since without them the spike would pull own first lags toward zero and make every series look like white noise in the posterior
- Minnesota shrinks each coefficient continuously toward its prior mean; SSVS gives each an inclusion probability, with a cut-off set by the spike-to-slab scale ratio, averaging over restricted VARs
<!-- YW5zOjM= -->
> A is wrong: the spike is a narrow normal, not an exact zero, and the posterior averages over many inclusion patterns; with slab and spike scales of 10 and 0.1 standard errors, coefficients beyond about 0.3 standard errors are kept, far more than a t test keeps.
> B is wrong: Minnesota applies one deterministic tightness pattern; SSVS lets each coefficient be either nearly zero or nearly free, according to the data.
> C is wrong: a coefficient that matters lands in the wide slab, where the zero-centred prior hardly shrinks it, so own first lags near one survive.
> D is right: Minnesota is continuous shrinkage toward the random walk, while SSVS mixes two normals per coefficient and the ratio of their scales, not a significance level, sets the threshold.
> Ref: Class 9 slides, BVAR-part2.pdf, slides 5–13 (ON/OFF switch, SSVS)
> Similar: Lista L09, original exercise on a large BVAR with a Minnesota-type prior

## favar

Q: Bańbura, Giannone and Reichlin compare one-step forecasts from a three-factor FAVAR estimated by OLS with 13 lags, the same FAVAR with Bayesian shrinkage, and a Bayesian VAR in 131 series. Which reading of their results is correct?
- The factors summarize all the information in the panel, so the FAVAR must beat the large BVAR at every horizon, and its OLS and Bayesian versions should forecast about equally well
- Factors shrink the cross-section but not the lags, so the unshrunk FAVAR still overfits and loses to a random walk; with shrinkage it does well, and the shrunk 131-series BVAR does better still
- The FAVAR forecasts are arbitrary, because its factors are identified only up to a rotation, so the large BVAR wins simply because its coefficients are identified while the FAVAR's are not
- The large BVAR wins only because it uses more data, so once each model sees the same 131 series the ranking reverses, and shrinkage plays no part in the comparison at any horizon
<!-- YW5zOjE= -->
> A is wrong: the OLS FAVAR with 13 lags has a mean squared forecast error two to three times the random walk's, far worse than its shrunk version.
> B is right: factor extraction reduces the number of series, but 13 lags of a few variables still leave many free coefficients; with shrinkage the FAVAR reaches about 0.65 of the random walk's error for employment, and the large BVAR about 0.46.
> C is wrong: a rotation of the factors is offset by the coefficients that load on them, so the forecasts do not depend on the rotation.
> D is wrong: the FAVAR also extracts its factors from the same panel; the decisive ingredient in both is shrinkage, as the unshrunk versions show.
> Ref: Class 9 slides, BVAR-part2.pdf, slides 51–59 (FAVAR, Bańbura, Giannone and Reichlin 2010)
> Similar: Lista L09, original exercise on the FAVAR

Q: In a regression whose coefficients follow random walks, the posterior paths of the coefficients move a lot over the sample, yet the marginal likelihood favours the constant-coefficient model. Which reading is correct?
- There is no contradiction: the random-walk prior lets each coefficient's variance grow with time, so paths can wander, while the marginal likelihood charges for the extra states
- The marginal likelihood must be wrong, since moving posterior paths are direct evidence of parameter instability, and a model that allows instability can never fit worse than one that rules it out
- The paths move because the Kalman gain was set too high by the analyst, and with a smaller gain the paths would be flat and the two models would have the same marginal likelihood
- The comparison is invalid because marginal likelihoods cannot compare models with different numbers of parameters; a likelihood-ratio test of zero state variance should be used, with standard critical values
<!-- YW5zOjA= -->
> A is right: Greenberg's Phillips-curve example has large movement in the coefficient paths and still a larger marginal likelihood for the constant AR(1); the marginal likelihood averages the fit over the prior and so penalizes the many extra states.
> B is wrong: wandering posterior paths are allowed by the prior even when the data do not need them, and a more flexible model can have a lower marginal likelihood.
> C is wrong: the Kalman gain is not a tuning knob; it is derived from the ratio of state to observation variance, which is estimated.
> D is wrong: marginal likelihoods compare models of any size, which is their purpose, and a test of zero state variance sits on the boundary, where standard critical values fail.
> Ref: Greenberg 1e §10.3, pp. 161–165; Tsay 3e §11.1–11.3, pp. 558–591; Class 9 slides, BVAR-part2.pdf, slide 61
> Similar: Greenberg 1e, Ch. 10, Exercise 10.4

## mvol

Q: Compare an exponentially weighted moving-average estimate of the conditional covariance matrix of several assets with a DCC model. Which statement is correct?
- Both are mean-reverting, since the moving average down-weights old observations and so pulls the covariance back toward its sample value, and DCC differs only by giving each pair its own decay rate
- The moving average guarantees a positive-definite matrix only for two assets, while DCC needs simulation-based estimation because its correlation recursion has no closed-form likelihood
- The moving average updates all entries at one decay rate with no long-run anchor, so its forecasts stay flat; DCC fits univariate GARCH, then correlations that revert to a long-run level
- DCC is the moving average applied to standardized residuals, with the same single decay parameter and no long-run level, so the two give the same correlation forecasts and differ only in volatilities
<!-- YW5zOjI= -->
> A is wrong: the moving average has no unconditional level to revert to, and DCC's two scalar parameters are shared by all pairs rather than pair-specific.
> B is wrong: the moving average of outer products is positive semi-definite in any dimension, and DCC is estimated in two steps by quasi-maximum likelihood, with no simulation.
> C is right: the moving average is an integrated recursion, so multi-step forecasts are flat at the current estimate, while DCC's correlation recursion reverts to the unconditional correlation of the standardized residuals.
> D is wrong: DCC adds a mean-reverting intercept built from the unconditional correlation and rescales its recursion into a correlation matrix, which the moving average lacks.
> Ref: Tsay 3e §10.1, p. 506, and §10.4.3, pp. 531–532; site page wti-sp500-timevaryingcovariance.html; Class 9 slides, BVAR-part2.pdf, slides 38–43
> Similar: Tsay 3e, Ch. 10, Exercises 10.1 and 10.6
