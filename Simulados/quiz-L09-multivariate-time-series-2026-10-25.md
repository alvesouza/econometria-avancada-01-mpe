---
quiz: "L09 · Class 9: Multivariate time series — VAR, SVAR, BVAR, FAVAR, TVP-VAR, factor SV and DCC"
tags:
  var: "VAR estimation, IRFs and lag choice"
  svar: "Structural VAR identification"
  bvar: "Bayesian VAR and the Minnesota prior"
  favar: "Factor models, FAVAR and TVP-VAR"
  mvol: "Time-varying covariances: factor SV and DCC"
---

## var

Q: A VAR is fitted to quarterly GDP growth of the UK, the US and Canada, and AIC, BIC and Hannan–Quinn are computed for orders 0 to 13. AIC points to a larger order than BIC. Which reading is correct?
- BIC's penalty grows with sample size and exceeds AIC's, so it picks the leaner order; as coefficients grow with the square of the number of series, each lag is costly
- AIC is consistent for the true order while BIC overfits in large samples, so the larger order selected by AIC should be preferred whenever the sample is long enough
- The two criteria disagree because the VAR is nonstationary, since information criteria select the same order whenever all companion eigenvalues lie inside the unit circle
- The criteria measure in-sample fit only, so they cannot differ in their choice of order unless the residual covariance matrix is singular at some of the candidate orders
<!-- YW5zOjA= -->
> All three criteria trade fit against the number of coefficients, but BIC's penalty per parameter grows with the log of the sample size, so it selects smaller models; BIC is the consistent one, while AIC tends to overfit and often forecasts well. In a VAR each extra lag adds one coefficient per pair of series, so the parameter count rises fast with the number of variables, the over-parameterization that motivates Bayesian shrinkage. Disagreement between criteria has nothing to do with stationarity or singularity.
> Ref: Class 9 site code, VAR-Example.html (VAR(3) for UK, US and Canada); Class 9 slides, BVAR-part11.pdf; Tsay AFTS 3e, Ch. 8, §8.2, pp. 399–417
> Similar: Tsay AFTS 3e, Ch. 8, Exercise 8.2, p. 462; Exercise 8.7, p. 463

Q: Orthogonalized impulse responses from a fitted VAR are computed with a Cholesky factor of the residual covariance. They change when the order of the variables is permuted, while the fitted values and forecasts do not. Why?
- The estimation itself depends on the ordering, so permuting the variables changes the coefficient matrices, and the impulse responses inherit those different estimates
- Permuting the variables changes the companion matrix eigenvalues, so the stability of the system and the persistence of all responses depend on the ordering chosen
- The Cholesky factor is recursive: the first variable's shock moves all others on impact and the last moves only itself, so ordering is an identifying assumption
- The ordering affects only the forecast error variance decomposition, while orthogonalized impulse responses are invariant, so the change must come from a numerical error
<!-- YW5zOjI= -->
> The reduced form, coefficients, covariance and forecasts, is invariant to ordering; equation-by-equation OLS gives the same estimates in any order. Orthogonalizing correlated innovations requires a factorization, and the Cholesky factor is lower triangular, so the ordering decides which variables respond within the period to which shocks. Both impulse responses and variance decompositions built on it depend on that choice; eigenvalues do not, since they come from the reduced-form coefficients alone.
> Ref: Class 9 slides, BVAR-part11.pdf (VMA representation, variance decomposition, IRF); Tsay AFTS 3e, Ch. 8, §8.2, pp. 399–417
> Similar: Tsay AFTS 3e, Ch. 8, Exercise 8.7, p. 463

## svar

Q: Why does a structural VAR need restrictions such as zeros in the contemporaneous matrix, signs on responses, or long-run neutrality?
- Because the reduced-form coefficients are not estimable without them, since OLS on each equation is inconsistent when contemporaneous correlations among variables are non-zero
- Because the reduced-form covariance has fewer free elements than the structural impact matrix has unknowns, so many structures fit equally well and economics must choose one
- Because restrictions make the structural shocks forecastable, which is what policy analysis requires, since unrestricted shocks are white noise and carry no information about the future
- Because without restrictions the structural VAR is overidentified, so the restrictions are tested against the data and retained only when the test fails to reject them
<!-- YW5zOjE= -->
> The data identify the reduced form: lag coefficients and a symmetric residual covariance. Many structural impact matrices map to the same reduced form, so without extra information impulse responses to structural shocks are not pinned down; this is the identification problem Rubio-Ramírez, Waggoner and Zha call unresolved since Sims (1980). Restrictions come from theory, such as which variables cannot react within the month. In the common exactly identified case they cannot be tested at all, and the reduced form is consistently estimated by OLS regardless. Structural shocks remain unforecastable.
> Ref: Class 9 slides, BVAR-part11.pdf (structural VAR, exact identification); Tsay AFTS 3e, Ch. 8, §8.2, pp. 399–417
> Similar: Tsay AFTS 3e, Ch. 8, Exercise 8.2, p. 462

## bvar

Q: A VAR for seven quarterly US macro series with six lags has about 300 coefficients and only 133 observations, yet Litterman's Minnesota prior makes it forecast well. Why?
- It replaces the likelihood with the prior, since with more parameters than observations the data carry no information, so forecasts come purely from the random-walk benchmark
- It selects a subset of variables in each equation and sets the rest exactly to zero, so the model becomes a small VAR whose coefficients OLS can estimate precisely
- It shrinks every coefficient to zero with equal strength, which removes all dynamics from the forecasts, and the gain comes from forecasting each series by its sample mean
- It centres each equation on a random walk, shrinks other variables' lags more than own lags and distant lags most, trading a little bias for a large cut in variance
<!-- YW5zOjM= -->
> The Minnesota prior centres the first own lag at one and everything else at zero, a random walk for each series, which is a hard benchmark to beat for persistent macro data. Prior variances shrink cross-variable lags more than own lags and tighten with the lag length. The posterior combines prior and likelihood: data still move coefficients where they are informative. Exact zeros are what spike-and-slab selection (SSVS) does, a different approach. For series in growth rates the prior mean on the first lag is usually set to zero instead of one.
> Ref: Class 9 slides, BVAR-part11.pdf (Minnesota prior; Kadiyala–Karlsson revisit of Litterman); Greenberg 1e, Ch. 10, §10.3, pp. 161–165
> Similar: Tsay AFTS 3e, Ch. 8, Exercise 8.5, p. 463

Q: Bańbura, Giannone and Reichlin find that a Bayesian VAR with 131 macro series forecasts better than small VARs, provided the overall tightness of the prior rises with the number of series. Why must shrinkage rise with model size?
- Because a larger model has more observations per coefficient, so a tighter prior is needed only to speed up the computations, with no effect on the forecasts themselves
- Because adding series makes the error covariance matrix singular, and tighter shrinkage is the only way to make that matrix invertible again in a Bayesian VAR
- Because coefficients grow with the square of the number of series, so without tighter shrinkage extra noise swamps extra signal; tight priors let weak signals add up
- Because the Minnesota prior becomes improper as the number of series grows, so its tightness must be raised to keep the posterior distribution proper and well defined
<!-- YW5zOjI= -->
> Each new series adds a full row and column of lag coefficients, so parameter uncertainty grows much faster than the information each series brings. Raising the tightness with the cross-section keeps the model's effective complexity under control, and the many small cross-series effects then pool into better forecasts; Bańbura et al. also find credible impulse responses from the large model. This is the Bayesian counterpart of compressing a large panel into a few factors. A larger model has fewer observations per coefficient, and the Minnesota prior is proper at any size.
> Ref: Class 9 slides, BVAR-part2.pdf (large BVAR, Bańbura, Giannone and Reichlin 2010); Tsay AFTS 3e, Ch. 9, §9.2, pp. 470–476
> Similar: Tsay AFTS 3e, Ch. 9, Exercise 9.7, p. 503

## favar

Q: In a factor model, the loading matrix is often constrained to be lower triangular with a positive diagonal. Why, and with what side effect?
- The likelihood is unchanged by rotating factors and loadings together, so a unique solution needs a constraint; the triangular form fixes one, but the series placed first then matter
- The triangular form ensures that the factors are uncorrelated with the idiosyncratic errors, and its side effect is that the number of factors can no longer be chosen from the data
- The triangular form is needed to make the covariance matrix positive definite, and its side effect is that the idiosyncratic variances are forced to be equal across all series
- The triangular form makes each factor load on exactly one series, so factors become interpretable, and its side effect is that the common variance explained by the factors falls
<!-- YW5zOjA= -->
> Factors and loadings enter only through their product, so any orthogonal rotation gives the same covariance and the same likelihood, with multimodality and label switching in MCMC. Fixing the upper triangle to zero picks one rotation. The cost: the first series act as founders of the factors, so their choice and ordering matter, which Lopes and West address and later work relaxes with generalized lower-triangular structures. The constraint has nothing to do with positive definiteness or equal idiosyncratic variances, and loadings below the diagonal remain free.
> Ref: Class 9 slides, BVAR-part2.pdf (factor analysis, identification, ordering); Tsay AFTS 3e, Ch. 9, §9.1, pp. 468–470
> Similar: Tsay AFTS 3e, Ch. 9, Exercise 9.2, p. 501

Q: A time-varying-parameter VAR lets its coefficients drift as random walks. Why does a Primiceri-type specification also give the shocks stochastic volatility?
- Because random-walk coefficients make the VAR nonstationary, and stochastic volatility is the device that restores stationarity by shrinking the variance of the drifting coefficients
- Because stochastic volatility replaces the need for coefficient drift, so in practice the coefficient variances are set to zero and only the volatilities are allowed to change
- Because without it the posterior of the drifting coefficients cannot be sampled at all, since the Kalman filter needs a time-varying measurement variance in order to run
- Because without it a change in shock size, such as the Great Moderation, would be read as a change in transmission; SV separates changing shocks from changing propagation
<!-- YW5zOjM= -->
> If the error covariance is held fixed, the only way for the model to fit calmer or more turbulent periods is to move the coefficients, so changes in shock variance masquerade as changes in the economy's response, the "good luck versus good policy" debate. Letting the variances, and in Primiceri also the contemporaneous Cholesky elements, drift lets the data attribute change to the right source. Both blocks are state-space models sampled with Kalman-filter-based steps, which work with constant variances too; the coefficient drift is still estimated, usually with tight priors on its innovation variance.
> Ref: Class 9 slides, BVAR-part11.pdf (TVP-VAR-SV, Primiceri 2005) and BVAR-part2.pdf (TVP-BVAR); Tsay AFTS 3e, Ch. 11, §11.1–11.3, pp. 558–591; Greenberg 1e, Ch. 10, §10.3, pp. 161–165
> Similar: Tsay AFTS 3e, Ch. 11, Exercise 11.3, p. 609

## mvol

Q: A one-factor stochastic volatility model for daily returns of an oil-and-gas firm and the S&P 500 has loadings fixed over time, yet the implied correlation between the two rises in turbulent periods. What produces this?
- The loadings are re-estimated each day, so in turbulent periods they rise, and higher loadings mechanically imply a higher correlation between the two return series
- When the factor's volatility rises relative to the idiosyncratic ones, the common part takes a larger share of each variance, so correlation rises even with fixed loadings
- The idiosyncratic volatilities rise in turbulent periods, and since they enter the covariance between the two series, a larger idiosyncratic variance raises the correlation
- The rise is an artefact of the MCMC sampler, since with fixed loadings the correlation implied by a factor model is constant over time by construction of the model
<!-- YW5zOjE= -->
> In a factor SV model the covariance is the loadings times the factor's time-varying variance times the loadings, plus a diagonal of idiosyncratic SV variances. Covariance moves with the factor variance only, while each variance moves with both parts, so correlation rises when the factor's volatility rises relative to the idiosyncratic ones and falls when firm-specific turbulence dominates. Idiosyncratic variances never enter the covariance between two series. Time-varying correlation with constant loadings is a built-in feature, not an artefact.
> Ref: Class 9 site code, wti-sp500-timevaryingcovariance.html and sv-fsv-US-BR.html; Class 9 slides, BVAR-part2.pdf (factor stochastic volatility); Tsay AFTS 3e, Ch. 10, §10.1–10.5, pp. 506–543
> Similar: Tsay AFTS 3e, Ch. 10, Exercise 10.6, p. 555

Q: Compare DCC and factor stochastic volatility as models for the time-varying covariance matrix of many assets. Which statement is correct?
- DCC fits univariate GARCH first, then drives all correlations with a couple of shared scalars; FSV builds covariance from a few latent factors with their own volatilities
- DCC lets every pairwise correlation follow its own dynamics with separate parameters, which is why it scales better than FSV to portfolios holding hundreds of different assets
- FSV requires the number of factors to equal the number of assets, so it is a reparametrization of the full covariance matrix and gains nothing in parsimony relative to DCC
- Both are observation-driven models whose likelihoods are available in closed form, so they are estimated by maximum likelihood without latent variables or any simulation
<!-- YW5zOjA= -->
> DCC is a two-step, observation-driven model: univariate GARCH volatilities, then a correlation recursion governed by two scalars shared by all pairs, which buys scalability at the price of identical correlation dynamics for every pair. FSV is parameter-driven: a few latent factors with SV, plus idiosyncratic SV, give a covariance whose parameter count grows linearly in the number of assets; its likelihood has no closed form and is handled by MCMC, as in factorstochvol. Its parsimony comes precisely from using far fewer factors than assets.
> Ref: Class 9 site code, wti-sp500-timevaryingcovariance.html (FSV vs DCC); Tsay AFTS 3e, Ch. 10, §10.1–10.5, pp. 506–543
> Similar: Tsay AFTS 3e, Ch. 10, Exercise 10.6, p. 555; Exercise 10.4, p. 554

Q: For daily stock returns, an analyst must choose between a VAR with constant error covariance and a factor stochastic volatility model with constant mean. Which statement describes what each one captures?
- Both capture the same features, since a VAR's lag structure induces time-varying conditional covariances, so the choice depends only on the number of assets in the system
- The VAR captures time-varying covariances through its lags, while the FSV captures lead–lag predictability in mean returns through the dynamics of its latent factors
- The VAR models lead–lag dynamics in means with a fixed covariance and FSV models moving covariance; for returns, mean predictability is weak and covariance dynamics strong
- Neither suits returns, since returns are serially uncorrelated, so both their conditional means and their conditional covariances are constant and only unconditional moments matter
<!-- YW5zOjI= -->
> A VAR is a model for conditional means; its error covariance is constant, so conditional covariances do not change. FSV, like GARCH-type models, targets second moments and assumes little about the mean. Daily returns show weak serial correlation in levels (the IBM Ljung–Box result of class 8) but strong dependence in squares and cross-products, so for risk and portfolio questions the covariance model is the one that matters. Serially uncorrelated does not mean constant conditional variance.
> Ref: Class 9 slides, BVAR-part11.pdf and BVAR-part2.pdf; Tsay AFTS 3e, Ch. 8, §8.1–8.2, pp. 390–417 and Ch. 10, §10.1–10.5, pp. 506–543
> Similar: Tsay AFTS 3e, Ch. 8, Exercise 8.1, p. 462; Ch. 10, Exercise 10.1, p. 554
