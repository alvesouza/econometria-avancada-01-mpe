---
quiz: "L08 · Class 8: Univariate time series, hard conceptual — forecasting, unit roots, GARCH variants, SV and Bayesian GARCH"
tags:
  arma: "ARMA forecasting and overdifferencing"
  unitroot: "Unit roots and spurious regression"
  vol: "GARCH family: asymmetry, GARCH-M, IGARCH"
  sv: "Stochastic volatility and Bayesian GARCH"
---

## arma

Q: Two analysts forecast a quarterly log output series 40 quarters ahead. One fits a stationary AR(2) around a linear trend; the other fits an ARIMA with one difference and a drift. The point forecasts are close, but the second analyst's interval is several times wider at long horizons. Which reading is correct?
- The intervals must converge as the horizon grows, since both models share the same deterministic trend, so the gap reflects only the larger number of parameters estimated in the AR(2) around a trend
- The trend-stationary interval is the honest one, because the drift model counts the trend twice by differencing, and differenced models always overstate the uncertainty of forecasts of the level
- The gap comes only from parameter-estimation uncertainty, which grows with the horizon in the drift model; with known parameters both intervals would have the same width at every horizon
- With trend stationarity the forecast-error variance converges to a finite limit, while with a unit root it grows with the horizon; the choice is a unit-root question that tests settle poorly
<!-- YW5zOjM= -->
> A is wrong: sharing a trend in the mean does not make the error variances alike; one is bounded, the other grows linearly in the horizon.
> B is wrong: differencing does not double count the trend, since the drift is the trend's slope; the wider interval reflects permanent shocks, not an overstatement.
> C is wrong: even with known parameters, the forecast-error variance of a random walk is the horizon times the shock variance, while that of a stationary AR converges to the unconditional variance.
> D is right: bounded versus unbounded forecast uncertainty is exactly the stationary versus unit-root distinction, and Dickey–Fuller tests have low power against persistent stationary alternatives.
> Ref: Class 8 slides, unitroot.pdf and ar-ma.pdf (forecasting); Tsay 3e §2.6–2.7, pp. 54–79; Wooldridge 6e §18.2, pp. 574–578
> Similar: Tsay 3e, Ch. 2, Exercise 2.3

Q: An analyst takes first differences of a series that is in fact stationary around a deterministic linear trend, then fits an ARMA to the differences and finds an MA(1) coefficient at the invertibility boundary. Which interpretation is correct?
- The near-boundary MA coefficient signals long memory in the original series, so the right model is a fractionally integrated one with a differencing parameter strictly between zero and one
- It is the signature of overdifferencing: differencing a trend-stationary series puts a unit root in the MA polynomial, so the series should be detrended instead, and its shocks are transitory
- It confirms that differencing was right, since an MA(1) is the most parsimonious model for a differenced random walk, and a coefficient near the boundary means that shocks are very persistent
- It reveals a seasonal unit root that the regular difference left behind, so a seasonal difference should be added before re-estimating, as in the airline model for monthly passenger data
<!-- YW5zOjE= -->
> A is wrong: long memory shows up as slowly decaying autocorrelations in levels, not as a unit MA root in the differences.
> B is right: if the level is a trend plus stationary noise, its difference is the drift plus the differenced noise, whose MA polynomial has a root at one; that non-invertible root is the overdifferencing symptom.
> C is wrong: a differenced random walk is white noise, not an MA(1) near the boundary, and the unit MA root says shocks are transitory, the opposite of persistence.
> D is wrong: a seasonal unit root leaves autocorrelation at the seasonal lags, not a unit root in the regular MA(1) polynomial.
> Ref: Class 8 slides, unitroot.pdf (trend-stationary versus random walk with drift); Tsay 3e §2.7, pp. 72–79
> Similar: Wooldridge 6e, Ch. 18, C13

## unitroot

Q: A regression of one monthly price index on another, unrelated one gives a t statistic of 5 and an R-squared of 0.9, and its residuals are strongly autocorrelated. Both series look like random walks. Which reading is correct?
- It is likely spurious: with no true relation the error is a random walk, so the t statistic rejects far too often, and more so as the sample grows; difference the data or test the residuals
- The high R-squared rules out spuriousness, because a spurious regression explains little of the variation; the autocorrelated residuals only mean the standard errors should be made robust to it
- With a long enough sample the problem disappears, because the law of large numbers makes the estimated slope converge to zero when the two series are independent, so the t statistic shrinks
- The regression is valid as long as both series are integrated of the same order, since a common order of integration guarantees stationary residuals, and then the usual inference applies
<!-- YW5zOjA= -->
> A is right: Granger and Newbold's result; under the null the residual inherits the random walk, the nominal 5% t test rejects most of the time, and the rejection rate rises with the sample size; a unit-root test on the residuals is the cointegration check.
> B is wrong: high R-squared with autocorrelated residuals is the classic spurious-regression pattern, and robust standard errors do not restore a valid null distribution.
> C is wrong: the slope does not converge to zero; it converges to a random variable, and the t statistic diverges with the sample size.
> D is wrong: two independent random walks are both integrated of order one, yet their regression residual is nonstationary; stationary residuals require cointegration, not just a common order.
> Ref: Wooldridge 6e §18.3, pp. 578–580; Class 8 slides, unitroot.pdf
> Similar: Wooldridge 6e, Ch. 18, C13

Q: For a trending log price series, an analyst runs a Dickey–Fuller regression with an intercept but no trend, and rejects a unit root because the t statistic on the lagged level is below the 5% normal critical value. Which criticism is correct?
- None is needed, since the regression has many observations and the central limit theorem makes the t statistic close to standard normal under the null, as in any regression with a stationary regressor
- The only flaw is the missing trend, since once a trend term is added the normal critical value becomes valid, because detrending removes the source of the nonstandard behaviour of the statistic
- Under a unit root the statistic has a left-shifted nonstandard law, so normal values reject a true unit root too often; trending data also need a trend term, with even more negative critical values
- The flaw is the direction of the test: a unit root is rejected for large positive values of the statistic, because a lagged-level coefficient above zero is what signals mean reversion in the data
<!-- YW5zOjI= -->
> A is wrong: under the null the regressor is a random walk, not stationary, so the central limit theorem does not deliver a normal t statistic; its 5% quantile is near minus 2.86 with an intercept.
> B is wrong: with a trend the distribution is still nonstandard, and its critical values move further left, not to the normal ones.
> C is right: using the normal value rejects a true unit root far more often than 5%, and against a trend-stationary alternative the test regression must include the trend, which changes the null distribution again.
> D is wrong: mean reversion means a negative coefficient on the lagged level in the differenced regression, so the test rejects for large negative values.
> Ref: Class 8 slides, unitroot.pdf; Wooldridge 6e §18.2, pp. 574–578; Tsay 3e §2.7, pp. 76–79
> Similar: Wooldridge 6e, Ch. 18, C13

## vol

Q: Two models capture the leverage effect in daily stock returns: a GJR-GARCH and an EGARCH. Which comparison is correct?
- Both produce the same news-impact curve, a parabola steeper on the left, and differ only in estimation: EGARCH is fitted by MCMC since its log form has no closed-form likelihood, while GJR uses maximum likelihood
- GJR adds an extra coefficient on squared negative shocks and needs nonnegativity constraints; EGARCH models the log variance with a signed term in the standardized shock, so positivity is automatic
- EGARCH is symmetric, since the log of the variance responds to the absolute value of the shock only, so leverage can be captured only by GJR, whose indicator for negative shocks has no EGARCH counterpart
- GJR detects leverage when its asymmetry coefficient is negative, because bad news must then raise the variance less than good news, while in EGARCH leverage needs a positive coefficient on the signed shock
<!-- YW5zOjE= -->
> A is wrong: both have closed-form conditional likelihoods and are fitted by maximum likelihood; and the curves differ, since GJR is a two-sided parabola and EGARCH an asymmetric exponential in the shock.
> B is right: GJR's indicator term needs nonnegative coefficients to keep the variance positive; EGARCH works on the log variance, so any coefficients give a positive variance, and its signed term creates the asymmetry.
> C is wrong: EGARCH has both a signed term and an absolute-value term; the signed term is what lets a negative shock raise volatility more than a positive one.
> D is wrong: in GJR leverage means a positive coefficient on the negative-shock indicator, and in EGARCH a negative coefficient on the signed shock, the reverse of both claims.
> Ref: Tsay 3e §3.8–3.9, pp. 143–150; site page garchmodeling.html (GJR, APARCH, EGARCH on Petrobras)
> Similar: Tsay 3e, Ch. 3, Exercises 3.11 and 3.12

Q: A GARCH-in-mean model adds the conditional variance to the mean equation of monthly excess stock returns, with a positive coefficient. Which statement is correct?
- The model implies serially uncorrelated returns, since the mean depends only on the current conditional variance, which is known at the start of the period, and the shocks themselves are uncorrelated
- A positive coefficient means volatility shocks lower future prices, so the model captures the leverage effect, which is why GARCH-M is used in place of asymmetric models such as GJR and EGARCH
- The risk-premium coefficient is identified from the unconditional mean of returns alone, so an insignificant estimate means the volatility equation is misspecified and should be refitted
- Expected excess returns rise with volatility, and since the conditional variance is persistent, returns become slightly autocorrelated; an insignificant premium leaves the variance equation intact
<!-- YW5zOjM= -->
> A is wrong: the conditional mean moves with a persistent conditional variance, so returns inherit serial correlation even though the shocks are uncorrelated.
> B is wrong: a positive coefficient is a risk premium in the mean, not an asymmetric response of volatility to bad news; the two effects are modelled separately.
> C is wrong: the premium is identified from the co-movement of returns with the time-varying conditional variance, and its significance says nothing about the variance equation.
> D is right: Tsay notes that GARCH-M makes returns serially correlated; his S&P 500 example has a positive but insignificant premium alongside a well-determined GARCH(1,1).
> Ref: Tsay 3e §3.7, p. 142
> Similar: Tsay 3e, Ch. 3, Exercise 3.6

Q: Two GARCH(1,1) fits to the same daily returns differ only in persistence: one estimates the sum of the ARCH and GARCH coefficients at 0.98, the other imposes exactly one, an integrated GARCH with a positive constant. Which statement about long-horizon variance forecasts is correct?
- At 0.98 forecasts revert geometrically to a finite unconditional variance; under the integrated model there is no unconditional variance, shocks never fade, and forecasts rise linearly with the horizon
- The forecasts are practically identical at every horizon, since 0.98 is within sampling error of one, and the difference between the two models matters only for the in-sample fit of the variance
- The integrated model forecasts revert faster, since imposing a unit sum removes the GARCH term's memory and leaves the constant to pull the variance back to its long-run level within a few days
- At 0.98 the forecasts explode, since persistence close to one makes the variance a random walk, while the integrated model's forecasts stay flat at the current conditional variance at every horizon
<!-- YW5zOjA= -->
> A is right: below one the h-step forecast approaches the unconditional variance at the rate of the persistence, with a half-life of about 34 trading days at 0.98; at exactly one there is no unconditional variance and each step adds the constant.
> B is wrong: the two agree at short horizons but diverge at long ones, one converging and the other growing without bound; a Bayesian can report the posterior probability that persistence exceeds one instead of assuming it away.
> C is wrong: the unit sum is what removes mean reversion; the constant then adds to the forecast every step rather than pulling it back.
> D is wrong: persistence below one keeps forecasts bounded; and with a positive constant the integrated forecasts rise linearly instead of staying flat.
> Ref: Tsay 3e §3.5–3.6, pp. 131–142; Class 8 slides, bayes-garch.pdf
> Similar: Tsay 3e, Ch. 3, Exercise 3.4

## sv

Q: On the same daily returns, a GARCH(1,1) with Student-t errors estimates about 7 degrees of freedom, while an SV-AR(1) with Student-t errors estimates about 12. Both report persistence near 0.98. Which reading is correct?
- The SV model sees thinner tails in the returns, so it predicts fewer extreme days than the GARCH model, and the gap in degrees of freedom is a direct comparison of the two models' tail risk
- The gap reflects the prior used in the MCMC fit of the SV model, which pulls the degrees of freedom toward large values, while the GARCH fit by maximum likelihood is free of any such pull
- Both must match the same sample kurtosis; in SV the volatility shock supplies part of it, so the errors need thinner tails, and the degrees of freedom are not comparable across the two models
- The SV model is misspecified, since a model whose volatility has its own shock already has fat tails, so adding Student-t errors double-counts them and biases the degrees of freedom upward
<!-- YW5zOjI= -->
> A is wrong: the marginal tails of returns combine the innovation tails with the volatility variation, so a larger degrees-of-freedom value in SV does not mean fewer extreme days.
> B is wrong: the prior has some influence, but the structural reason is the split of kurtosis between two sources, which would remain under a flat prior.
> C is right: in SV the lognormal volatility shock alone multiplies kurtosis by a factor above one, so the t errors carry less of it; GARCH loads most of the kurtosis on the innovation, hence its lower degrees of freedom.
> D is wrong: SV with t errors is a legitimate extension that the site fits; the estimated degrees of freedom adjust to what the volatility shock leaves unexplained.
> Ref: Tsay 3e §3.12, pp. 153–155; site page GARCH11-SVar1.html (Petrobras GARCH-t versus SV-t)
> Similar: Tsay 3e, Ch. 12, Exercise 12.4

Q: Overlaying the fitted GARCH(1,1) volatility and the posterior-mean SV volatility path for the same returns, the SV path rises on the very day of a crash, while the GARCH path rises only on the following day. Which explanation is correct?
- The SV model contains a leverage term that anticipates crashes, so its path leads the GARCH path, and in real time it would forecast a crash one day before it happens
- The GARCH model is misspecified, since a correctly specified volatility model should respond on the day of a large return, so the lag shows the recursion is missing a contemporaneous term
- The SV path reacts faster because its volatility shock has a larger variance than the GARCH innovation, and a larger shock variance makes volatility track squared returns with no delay
- GARCH volatility is a function of past returns only, while the SV posterior path is a smoother using same-day and later returns; a fair real-time comparison needs filtered SV volatility instead
<!-- YW5zOjM= -->
> A is wrong: a leverage correlation links today's return shock to tomorrow's volatility; it does not let the model see a crash before it happens.
> B is wrong: GARCH's conditional variance is by design known one step ahead, so responding the next day is the model, not a misspecification.
> C is wrong: the same-day response comes from conditioning on the same-day return in the posterior, not from the size of the volatility shock variance.
> D is right: the MCMC draws of each log variance condition on the whole sample, including the current return and the neighbouring volatilities, so the posterior path is a smoothed estimate.
> Ref: Tsay 3e §12.7, pp. 636–649; site page GARCH11-SVar1.html (volatility paths)
> Similar: Tsay 3e, Ch. 12, Exercise 12.4

Q: A Bayesian GARCH(1,1) with Student-t errors and priors that do not restrict persistence is fitted by Metropolis–Hastings. The posterior means of the constant, ARCH and GARCH coefficients each differ from the MLE by about one posterior standard deviation, the degrees of freedom barely move, and the output reports a posterior probability of 0.3% that persistence exceeds one. Which reading is correct?
- The gaps show that the chain has not converged, since with near-flat priors the posterior mean must equal the MLE, and the 0.3% is a p-value for the null hypothesis of covariance stationarity
- With flat priors the MLE is the posterior mode; a curved likelihood ridge along which the coefficients trade off skews the posterior, so its mean leaves the mode; the 0.3% is a direct probability
- The coefficients move because the prior shrinks them toward stationarity, which also forces the 0.3% figure, so the probability reflects the prior rather than the data and says nothing about persistence
- The gaps arise because the Student-t errors are not conjugate, which biases the posterior mean of every coefficient by the same amount, and the degrees of freedom escape only because they enter linearly
<!-- YW5zOjE= -->
> A is wrong: a flat prior makes the MLE the posterior mode, not the mean; and the 0.3% is a probability about the parameter given the data, not a probability about data under a null.
> B is right: the data pin down the unconditional variance and persistence better than each coefficient, so the posterior is skewed along the ridge and its mean differs from the mode, while the nearly symmetric posterior of the degrees of freedom stays put.
> C is wrong: the priors do not truncate at stationarity, which is why the 0.3% is the data's verdict rather than an artefact of the prior.
> D is wrong: non-conjugacy only means the sampler needs Metropolis steps; it does not bias the posterior, and the degrees of freedom enter the likelihood nonlinearly.
> Ref: Class 8 slides, bayes-garch.pdf, slides 14–21; site page GARCH11-SVar1.html (Bayes versus ML)
> Similar: Lista L08, original exercise on Bayesian GARCH(1,1) by Metropolis–Hastings
