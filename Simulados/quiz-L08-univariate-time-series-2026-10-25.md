---
quiz: "L08 · Class 8: Univariate time series — ARMA, unit roots, long memory, seasonality, GARCH and SV"
tags:
  arma: "AR, MA and ARMA models"
  unitroot: "Unit roots and long memory"
  seasonal: "Seasonal models"
  vol: "ARCH/GARCH"
  sv: "Stochastic volatility"
---

## arma

Q: A fitted AR(3) for quarterly US GNP growth has one real characteristic root and a pair of complex roots, all consistent with stationarity. What does the complex pair imply?
- The series contains a deterministic sine wave of fixed period, which forecasts can extrapolate indefinitely with no loss of accuracy as the forecast horizon grows
- The process is close to a unit root, since complex roots arise only when the autoregressive coefficients sum to nearly one, so shocks have permanent effects on growth
- The partial autocorrelation function decays as a damped sine wave and cuts off nowhere, so the model should be replaced with a moving average of the same order
- The ACF decays as a damped sine wave, so the series shows stochastic cycles whose average length follows from the roots, while forecasts still revert to the mean
<!-- YW5zOjM= -->
> Complex roots make the autocorrelation function a damped oscillation, which Tsay reads as stochastic business cycles whose average period is set by the argument of the roots. They are stochastic, not deterministic: each cycle is driven by shocks and dies out, and multi-step forecasts converge to the mean. Complex roots say nothing about proximity to a unit root, which depends on their modulus. An AR(3) has a PACF that cuts off after lag 3; it is the ACF that oscillates.
> Ref: Class 8 slides, ar-ma.pdf (AR(2) stationarity region, ACF shapes, US GNP AR(3)); Tsay AFTS 3e, Ch. 2, §2.4, pp. 37–57
> Similar: Tsay AFTS 3e, Ch. 2, Exercise 2.3, p. 104; Exercise 2.2, p. 104

Q: For monthly IBM returns, the Ljung–Box test on 30 lags gives a p-value of about 0.14 for the returns and below 0.0001 for the squared returns. Which conclusion is correct?
- Returns are white noise in the strict sense, independent and identically distributed, so neither the mean nor the variance of next month's return can be predicted from the past
- Returns are serially uncorrelated but not independent, since their variance is predictable, so a constant-mean model can fit while the shocks need an ARCH-type variance
- Returns need an ARMA model for the mean, since predictable squared returns imply predictable returns, and the squared-return test is a more powerful test of that same hypothesis
- The squared-return result is an artefact of fat tails, since heavy-tailed independent data produce large squared values that the Ljung–Box statistic mistakes for autocorrelation
<!-- YW5zOjE= -->
> No significant autocorrelation in returns means the conditional mean is close to constant; strong autocorrelation in squared returns means the conditional variance moves predictably. Uncorrelated is not independent, the distinction ARCH models are built on. Predictable squares do not imply a predictable sign. Independent heavy-tailed data have uncorrelated squares, so the second test is not an artefact; it is the standard ARCH-effect check before fitting a volatility model.
> Ref: Class 8 slides, ar-ma.pdf (Ljung–Box on IBM returns and squared returns); Tsay AFTS 3e, Ch. 2, §2.2, pp. 30–36 and Ch. 3, §3.3, pp. 113–115
> Similar: Tsay AFTS 3e, Ch. 3, Exercise 3.6, p. 169; Ch. 2, Exercise 2.4, p. 105

## unitroot

Q: Compare a random walk with drift and a trend-stationary process, each with the same linear deterministic trend in its mean. Which statement is correct?
- A shock moves the random walk for good and its forecast-error variance grows without bound, while the trend-stationary series returns to trend and its forecast variance levels off
- Both processes return to the trend after a shock, since the drift in the random walk acts as an attractor, so the two differ only in how fast deviations from the trend disappear
- Differencing is the right transformation for both, since it removes the deterministic trend from each and leaves the trend-stationary series with a well-behaved invertible ARMA
- Regressing either on a time trend leaves stationary residuals, so detrending is equally valid for both, and the choice between the two models has no effect on forecasts
<!-- YW5zOjA= -->
> In a random walk with drift every past shock stays in the level (the MA weights never decay), the variance grows linearly in time and forecast intervals fan out without limit; the drift sets a moving mean, not an attractor. A trend-stationary series has finite, constant variance around the trend, so shocks fade and forecast variance converges. Differencing a trend-stationary series over-differences it and creates a non-invertible MA unit root; detrending a random walk leaves a unit-root residual. The two models give very different long-horizon forecasts and intervals.
> Ref: Class 8 slides, unitroot.pdf (random walk, drift, trend-stationarity, ARIMA); Tsay AFTS 3e, Ch. 2, §2.7, pp. 71–81; Wooldridge 6e, Ch. 11, §11.3, pp. 354–360
> Similar: Wooldridge 6e, Ch. 11, Problem 11.4, p. 366

Q: An augmented Dickey–Fuller test gives a p-value of about 0.45 for log US GDP, 0.60 for the log S&P 500 index, and 0.01 for S&P 500 log returns. Which reading is correct?
- Log GDP and the log index are proven to have unit roots, since a high p-value confirms the null, while returns are trend-stationary, since the test rejects in their case
- The statistics can be read with ordinary t tables, since enough lagged differences in the test regression whiten the errors and restore the usual asymptotic normal distribution
- The levels fail to reject a unit root, which is no proof of one since power near one is low; returns reject, consistent with log prices being integrated of order one
- The deterministic terms in the test regression make no difference to the conclusion, since they affect only the intercept and leave the distribution of the statistic unchanged
<!-- YW5zOjI= -->
> Failing to reject is not accepting: ADF tests have low power against stationary roots close to one, so a near-integrated GDP is hard to distinguish from a random walk in these samples. Rejection for returns says the first difference of log prices is stationary, which is what an I(1) log price implies. The Dickey–Fuller statistic has a nonstandard limit, a functional of Brownian motion, even after augmentation, and its distribution changes with the constant and trend included, so those choices matter.
> Ref: Class 8 slides, unitroot.pdf (ADF test; US GDP and S&P 500 examples); Tsay AFTS 3e, Ch. 2, §2.7, pp. 71–81; Wooldridge 6e, Ch. 18, §18.2, pp. 574–578
> Similar: Wooldridge 6e, Ch. 18, C13, p. 604

Q: The sample autocorrelations of absolute daily returns are small but stay positive and decay very slowly over hundreds of lags. Which model and reading fit best?
- A fractionally integrated process with memory parameter between zero and one half: stationary, with hyperbolically decaying autocorrelations and a spectrum unbounded at frequency zero
- A random walk, since autocorrelations that stay positive over hundreds of lags can arise only from a unit root, so absolute returns should be differenced before any further modelling
- A stationary AR(1) with coefficient near one, since such a process already produces autocorrelations that decay at a hyperbolic rate, which is all that long memory refers to
- A moving average of very high order, since slowly decaying autocorrelations show that each shock's effect is cut off after a large but finite number of lags, as in any MA model
<!-- YW5zOjA= -->
> Long memory sits between short memory and a unit root. A fractionally differenced process with memory parameter below one half is stationary, but its autocorrelations decay polynomially rather than exponentially, and its spectral density diverges at frequency zero, while an ARMA spectrum is bounded. An AR(1) with a large coefficient decays geometrically and so eventually fast; a random walk has autocorrelations near one, not small; an MA cuts off sharply. Small but persistent autocorrelations are the signature Tsay points to for absolute returns.
> Ref: Class 8 slides, unitroot.pdf (long memory, fractional differencing); Tsay AFTS 3e, Ch. 2, §2.11, pp. 101–103
> Similar: Tsay AFTS 3e, Ch. 2, Exercise 2.5, p. 105

## seasonal

Q: Monthly returns on a small-firm index show significant autocorrelation at lags 12, 24 and 36. A seasonal ARMA fitted by exact likelihood gives a seasonal AR coefficient of about 0.95 and a seasonal MA coefficient of about 0.997. What is the best reading?
- Both coefficients near one show a seasonal unit root, so the series must be seasonally differenced, and the remaining dynamics should then be modelled as a regular ARIMA process
- The two estimates are strong evidence of rich seasonal dynamics, since both are highly significant and each captures a distinct seasonal feature of small-firm returns
- The estimates show that conditional likelihood is preferable here, since exact likelihood pushes the seasonal MA to the boundary and so overstates the seasonal persistence
- The seasonal AR and MA factors nearly cancel, pointing to a deterministic seasonal mean, a January effect, which a January dummy captures with far fewer parameters
<!-- YW5zOjM= -->
> When a seasonal AR factor and a seasonal MA factor are almost equal, they nearly cancel, and what is left is a fixed seasonal pattern in the mean. Tsay confirms this with a regression of returns on a January dummy, whose coefficient is large and significant. A seasonal MA at the invertibility boundary is the hallmark of over-differencing or deterministic seasonality, not of a seasonal unit root in the data. Exact likelihood is the method that reveals the cancellation; conditional likelihood masks it.
> Ref: Class 8 slides, seasonal.pdf (CRSP Decile 1 example, January effect); Tsay AFTS 3e, Ch. 2, §2.8, pp. 81–90; Wooldridge 6e, Ch. 10, §10.5, pp. 329–338
> Similar: Tsay AFTS 3e, Ch. 2, Exercise 2.6, p. 105

Q: The airline model applies a regular and a seasonal difference and then a regular MA(1) times a seasonal MA(1). Why use this multiplicative form instead of a non-multiplicative model with the same number of parameters?
- It is needed for invertibility, since a non-multiplicative MA with lags one and twelve can never be invertible, whatever its coefficients, once both differences are applied
- It encodes roughly separate regular and seasonal dynamics, whose product adds an interaction lag at no cost in parameters, giving a parsimonious yet constrained high-order ARMA
- It removes the need for differencing, since the product of the two MA factors already has a unit root at both the regular and the seasonal frequency of the series
- It makes the residuals uncorrelated at every lag by construction, so diagnostics such as the Ljung–Box test are no longer needed when the airline model is fitted to monthly data
<!-- YW5zOjE= -->
> Multiplying the two MA factors produces an extra term at lag s + 1 whose coefficient is the product of the two, so the model allows autocorrelation at lags 1, s − 1, s and s + 1 with only two parameters. This reflects the assumption that regular and seasonal dynamics are approximately orthogonal. Expanded, a multiplicative seasonal model is a high-order ARMA with tight cross-coefficient restrictions. It still needs both differences, its MA factors can be invertible, and its residuals must still be checked: Tsay reports Q(12) for the Johnson & Johnson fit.
> Ref: Class 8 slides, seasonal.pdf (airline model, multiplicative seasonality); Tsay AFTS 3e, Ch. 2, §2.8, pp. 81–90
> Similar: Tsay AFTS 3e, Ch. 2, Exercise 2.6, p. 105

## vol

Q: A GARCH(1,1) with Student-t innovations fitted to daily Petrobras returns gives ARCH and GARCH coefficients summing to just under one and few degrees of freedom. Which reading is correct?
- The sum near one shows the unconditional variance is infinite, so the model cannot be used for forecasting, and the low degrees of freedom confirm that the variance does not exist
- The t innovations make the GARCH terms redundant, since fat tails and volatility clustering are two descriptions of one feature of returns, so one of the two can be dropped
- Volatility shocks die out slowly, and the t matters because clustering alone leaves tail thickness unexplained; symmetric GARCH misses leverage, which GJR or EGARCH capture
- The few degrees of freedom mean the conditional variance is undefined, so the fitted volatility path is meaningless, and only the median of returns can be modelled reliably
<!-- YW5zOjI= -->
> A persistence sum below one keeps the unconditional variance finite; near one, volatility shocks decay slowly (the IGARCH limit). A Gaussian GARCH already produces fat unconditional tails, but empirically not enough, so standardized residuals remain leptokurtic; t innovations absorb that conditional tail mass. The t has a finite variance whenever its degrees of freedom exceed two. Symmetric GARCH responds equally to good and bad news; the leverage effect needs an asymmetric term as in GJR, T-GARCH or EGARCH.
> Ref: Class 8 site code, garchmodeling.html and garch-sv-petrobras.html; Tsay AFTS 3e, Ch. 3, §3.5, pp. 131–140, §3.8–3.9, pp. 143–150 and §3.16, pp. 165–167
> Similar: Tsay AFTS 3e, Ch. 3, Exercise 3.4, p. 168; Exercise 3.11, p. 170

## sv

Q: Compare a GARCH(1,1) and an SV-AR(1), in which the log-variance follows its own AR(1) driven by a separate shock. Which statement is correct?
- Both have closed-form likelihoods built recursively from the data, so they differ only in the functional form that links yesterday's squared return to today's variance
- GARCH variance is a fixed function of past returns, so its likelihood follows by recursion; SV variance is latent with its own shock, so its likelihood needs MCMC or filtering
- SV variance is a deterministic function of past returns, while GARCH variance carries its own random shock, which is why GARCH needs MCMC and SV can be fitted by recursion
- The two are observationally equivalent, since any SV-AR(1) can be rewritten as a GARCH(1,1) with suitably chosen coefficients, so the choice between them is purely computational
<!-- YW5zOjE= -->
> GARCH is observation-driven: given the parameters and a starting value, the conditional variance is known at every date, so the likelihood is a product of one-step densities. SV is parameter-driven: log-volatility is a latent AR(1) with its own innovation, so the likelihood integrates over the whole latent path and has no closed form; Bayesian MCMC, as in stochvol, samples the path jointly with the parameters. The extra shock makes SV more flexible, and the two models are not equivalent. Bayesian GARCH still uses MCMC, but because its posterior is non-standard, not because of latent states.
> Ref: Class 8 site code, GARCH11-SVar1.html; Class 8 slides, bayes-garch.pdf; Tsay AFTS 3e, Ch. 3, §3.12, pp. 153–154 and Ch. 12, §12.7, pp. 636–649
> Similar: Tsay AFTS 3e, Ch. 3, Exercise 3.12, p. 170

Q: For S&P 500 daily returns, three models are compared: iid normal, iid Student-t, and SV-AR(1) with normal errors. Standardized residuals from the SV model look close to normal, while the iid-t model fits the marginal histogram but leaves volatility clustering. What is the right interpretation?
- Much of the marginal fat tail is variance moving over time; modelled, it leaves a near-normal conditional law, while an iid t treats the tails as static and ignores data order
- The iid-t model is the best one, since it fits the marginal distribution of returns, and residual clustering does not matter for any use of the model, including risk forecasting
- The SV model is misspecified, since normal standardized residuals mean the model has removed genuine tail risk that a risk manager needs, so the iid-t model should be preferred
- The comparison is uninformative, since standardized residuals depend on the fitted volatility path, so they look normal for any volatility model, whether correct or incorrect
<!-- YW5zOjA= -->
> A normal with randomly changing variance is a scale mixture and has fat tails unconditionally; SV explains most of the observed kurtosis this way, and dividing by the fitted volatility leaves near-normal residuals. An iid t matches the histogram but is invariant to shuffling the data, so it cannot capture clustering, which matters for risk forecasts: tomorrow's risk depends on today's volatility. Standardized residuals are a genuine diagnostic, since a wrong volatility path leaves clustering and excess kurtosis behind.
> Ref: Class 8 site code, sp500-gaussian-student-SV-models.html and GARCH11-SVar1.html; Tsay AFTS 3e, Ch. 3, §3.12, pp. 153–154
> Similar: Tsay AFTS 3e, Ch. 3, Exercise 3.11, p. 170
