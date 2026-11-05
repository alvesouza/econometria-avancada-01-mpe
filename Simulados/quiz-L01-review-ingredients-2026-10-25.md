---
quiz: "L01 · Review of Basic Ingredients: Conceptual Synthesis"
tags:
  lik: "Likelihood, sampling rules and estimator properties"
  mse: "MSE, Monte Carlo and the bootstrap"
  poi: "Poisson counts, change point and a first prior"
  reg: "Regression, AR/VAR and evidence"
---

## lik

Q: Researcher A tosses a coin a fixed number of times; researcher B tosses until a fixed number of heads has appeared. They happen to record the same tosses and the same number of heads, so their likelihoods for the head probability are proportional. Which split between what must agree and what may differ is correct?
- Everything agrees, including the MLE, the Wald interval, the posterior, the bias and the p-value, because proportional likelihoods carry identical information and the likelihood principle binds every inference method.
- The MLE, the Wald interval built from observed information and the posterior under a common prior agree; the bias and the p-value may differ, because they average over outcomes the stopping rule could have produced.
- The MLEs differ, because the negative binomial kernel places the number of tosses in the denominator, while the posteriors agree because the prior absorbs the stopping rule through its normalising constant.
- The bias and the p-value agree, since both are functions of the same sufficient statistic, while the posteriors differ because each design implies its own conjugate family and so its own posterior shape.
<!-- YW5zOjE= -->
> Whatever depends only on the realised likelihood is design-free: the MLE, the observed information at the MLE (hence the Wald interval) and the posterior, where the binomial and negative binomial constants cancel. Whatever averages over unobserved outcomes depends on the sampling rule: under inverse sampling the number of tosses is random, so the same estimator is biased upward, and "more extreme than observed" is defined on a different sample space, so the p-values differ. The first option applies the likelihood principle to frequentist quantities that violate it; the third and fourth invert which side is design-dependent.
> Ref: Bolfarine & Sandoval §1.3 (pp. 4–13), §3.1 (pp. 35–42); Greenberg 1e §2.2 (pp. 12–18); slides `mle_sampling_rules.pdf`
> Similar: Notas/L01/L01-01-likelihood-sampling-rules.md §8–§10; Notas/L01/L01-10-pitfalls.md Block A, items 1–5; B 3.17 (p. 55)

Q: For iid Poisson counts with rate $\lambda$, an analyst notes that the sample variance, like the sample mean, is unbiased and consistent for $\lambda$, and concludes that in large samples the two are equally good. What is wrong with the conclusion?
- The sample variance is biased for the rate in finite samples, so it is unbiasedness, not efficiency, that separates the two, and the gap disappears once a degrees-of-freedom correction is applied to it.
- Nothing is wrong: both estimators attain the Cramér–Rao bound asymptotically, so their variances differ only by terms that vanish faster than the rate at which either estimator converges.
- The sample variance is inconsistent for the rate, because a Poisson model has unbounded fourth moments and the law of large numbers fails for squared deviations taken around the sample mean.
- Consistency is a limit statement, silent on precision at a given sample size; the mean attains the Cramér–Rao bound, while the variance estimator stays a fixed multiple noisier and needs far more data.
<!-- YW5zOjM= -->
> Unbiasedness fixes the centre at a given $n$; consistency fixes the limit; efficiency ranks spread. The sample mean is sufficient, unbiased, consistent and efficient (its variance equals the Cramér–Rao bound). The sample variance is also unbiased and consistent, but its variance is larger by a factor that does not shrink with $n$, so its relative efficiency stays below one; at a rate of 2 it is about one fifth. The first option confuses the Poisson case with the divisor-$n$ variance estimator; the second assumes all consistent estimators are asymptotically efficient; the third invents a moment problem the Poisson does not have.
> Ref: Bolfarine & Sandoval §2.1 (pp. 15–19), §2.2 (pp. 20–23), §3.2 (pp. 42–45); slides `class1-poisson.pdf`
> Similar: Notas/L01/L01-02-poisson-mle-properties.md; Notas/L01/L01-10-pitfalls.md §11 and items 6–7; B 2.2, 2.4 (p. 32)

## mse

Q: For $U(0,\theta)$ data, the sample maximum is a biased estimator of $\theta$ yet has a smaller MSE than twice the sample mean, which is unbiased; and the nonparametric bootstrap gives a wrong sampling distribution for the maximum at every sample size. Which single feature explains both facts?
- The maximum sits on the edge of the support: it closes in on the bound unusually fast, beating the unbiased rival, but the sample has no mass beyond it, so resampled maxima pile up on the observed value.
- The sample size is too small for asymptotics; in large samples the MSE ranking reverses in favour of the unbiased estimator, and the bootstrap distribution of the maximum converges to the true one as usual.
- The maximum is not a sufficient statistic for the bound, so it discards information; this lost information shows up both as a smaller variance than it deserves and as a bootstrap that cannot reproduce its spread.
- The maximum is biased downward, and a biased statistic cannot be bootstrapped; rescaling it by the usual unbiasing factor restores both a fair MSE comparison and the consistency of the nonparametric bootstrap.
<!-- YW5zOjA= -->
> The likelihood of a uniform sample is decreasing in $\theta$ wherever it is positive, so the MLE is the boundary value, the sample maximum, and its variance shrinks much faster than the usual $1/n$ rate. A small downward bias buys a large cut in variance, so MSE favours it. The same boundary position breaks the bootstrap: a resample repeats the observed maximum with probability tending to about 63%, a point mass the true continuous law never has. Resampling from the fitted uniform (parametric bootstrap) fixes it. The maximum is sufficient, so the third option is false; unbiasing does not remove the point mass, so the fourth fails; the ranking holds for every $n\ge3$, so the second fails.
> Ref: Bolfarine & Sandoval §1.1.5 (p. 3), §1.3 Table 1.1 (pp. 4–13), §3.1 (pp. 35–42); ISLP §5.2 (pp. 212–215); slides `comparing-estimators-MSE-slides.pdf`
> Similar: Notas/L01/L01-05-comparing-estimators-mse-bootstrap.md §7–§11; Notas/L01/L01-10-pitfalls.md §1, §12; B 1.12 (p. 14); I 5.2 (pp. 224–225)

Q: A Monte Carlo study of an estimator and a nonparametric bootstrap of the same estimator both redraw samples and recompute the statistic thousands of times. Which statement captures the essential difference between them?
- Monte Carlo belongs to Bayesian inference, where it approximates posterior integrals, while the bootstrap belongs to frequentist inference, where it approximates sampling distributions; the two solve unrelated problems.
- The only real difference is the number of replications: a bootstrap with enough resamples eliminates its approximation error entirely, just as a long Monte Carlo run converges to the exact answer.
- Monte Carlo draws from a process the analyst fully specifies, so it reveals the sampling distribution at that parameter; the bootstrap draws from the one observed sample, so it is only as good as that sample.
- Monte Carlo needs a closed-form expression for the sampling distribution before it can be run, while the bootstrap needs no model at all and is therefore valid for any statistic computed from iid data.
<!-- YW5zOjI= -->
> A Monte Carlo study fixes the model and the parameter, so its only error is simulation error, which more replications remove. The bootstrap replaces the unknown population by the empirical distribution (nonparametric) or by the fitted model (parametric); more resamples remove simulation error but not the gap between the sample and the population, which is why the nonparametric bootstrap fails for the uniform maximum however many resamples are taken. Monte Carlo needs a way to simulate, not a closed form, and it serves frequentist checks (the course's MSE tables) as much as posterior integrals.
> Ref: ISLP §5.2 (pp. 212–215); Morettin & Singer §B.6 (pp. 467–472); slides `comparing-estimators-MSE-slides.pdf`
> Similar: Notas/L01/L01-05-comparing-estimators-mse-bootstrap.md §9–§12; I 5.9 (pp. 227–228); B 1.4 (p. 13)

## poi

Q: The yearly counts of coal-mining disasters give a dispersion index well over one, with a tiny p-value under the single-rate Poisson model. What does this result license, and what does it not?
- One constant rate is inadequate, but the index ignores the order of the years, so rate heterogeneity with no break gives the same result; finding a break needs the time order, as in a profile likelihood.
- It shows that the rate changed at some date, and the break year can be read off as the year around which the yearly variance is largest, since overdispersion is generated exactly at the switch between two regimes.
- It rules out every Poisson model for these data, including a model with two rates on either side of a break, because each regime would inherit the same excess variance found in the pooled series.
- It matters only for the standard errors: the single-rate MLE stays the right summary of the series, and the excess variance is handled by inflating its standard error with a dispersion factor.
<!-- YW5zOjA= -->
> Overdispersion says "not one Poisson rate". It is invariant to shuffling the years, so it cannot distinguish a change point from year-to-year rate heterogeneity. The time structure does that: the profile likelihood over cut years peaks near 1891, while a shuffled series keeps the same index but loses the peak. A two-rate model can absorb the pooled excess variance because mixing two means creates it, so the third option fails. The fourth treats a mean-model failure as a variance nuisance, which is the quasi-Poisson remedy only when the mean model is right.
> Ref: Bolfarine & Sandoval §3.4 (pp. 46–49); slides `poisson-with-breakpoint.pdf`; Greenberg 1e §7.1.1 (pp. 91–95)
> Similar: Notas/L01/L01-03-coal-mining-change-point.md §3–§5; Notas/L01/L01-10-pitfalls.md §6, item 10; G 7.3 (p. 106)

Q: In the yearly coal-mining disaster counts of 1851–1962, the likelihood-ratio statistic comparing the best two-rate model with the one-rate model is very large. A student refers it to a chi-square with one degree of freedom. Why is that reference distribution wrong?
- Two rates are compared with one, but the cut year is a second extra parameter, so the right reference is a chi-square with two degrees of freedom, and the rest of the standard Wilks argument goes through.
- The two models are not nested, because the one-rate model cannot be obtained from the two-rate model, so likelihood-ratio theory does not apply and the comparison has to be made by an information criterion.
- The chi-square reference is too strict, because searching over many cut years averages out noise, so the stated p-value understates how strongly the data reject the single rate and the evidence is stronger still.
- Wilks' result needs a regular problem, but the cut year is discrete, chosen to maximise the statistic and undefined when the rates are equal, so under no change the statistic exceeds what chi-square predicts.
<!-- YW5zOjM= -->
> The one-rate model is the two-rate model with equal rates, so the models are nested; the trouble is the cut year. It is searched over, it is discrete, and it is not identified under the null, so none of Wilks' regularity conditions hold. Under a simulated no-change null the maximised statistic has a 95% quantile near 10, far above the chi-square value of 3.84, so the textbook reference would reject too often. The right reference is simulated (null or permutation draws). In the coal data the conclusion survives anyway, because the observed statistic exceeds every simulated draw.
> Ref: Bolfarine & Sandoval §6.5 (pp. 103–114), §3.4 (pp. 46–49); slides `poisson-with-breakpoint.pdf`
> Similar: Notas/L01/L01-03-coal-mining-change-point.md §6; Notas/L01/L01-10-pitfalls.md §7, item 11; B 6.11 (p. 116)

Q: An exponential prior with prior mean 2 is placed on a Poisson rate, and the posterior is computed on yearly counts. A student claims that (i) the posterior mean always exceeds the MLE, because the prior adds one pseudo-event, and (ii) the narrow posterior obtained on the full sample confirms the constant-rate model. Which assessment is correct?
- Claim (i) is right, because the prior always adds a pseudo-event to the count, and claim (ii) is wrong, because a narrow posterior only shows that the sample is long, not that the model is adequate.
- Both claims are wrong: the prior also adds exposure, so the posterior mean is pulled toward the prior mean from either side, and a posterior is conditional on the model, so it cannot test it.
- Claim (i) is wrong, because the prior adds exposure as well as a count, but claim (ii) is right, since a well-specified likelihood is exactly what makes a posterior concentrate around one value.
- Both claims are right: the pseudo-event raises every posterior mean, and the posterior would spread out over several values if the data really came from two different regimes over time.
<!-- YW5zOjE= -->
> The gamma posterior adds the count to the shape and the number of years to the rate, so its mean is a weighted average of the prior mean and the sample mean: above the MLE when the sample mean is below 2, below it otherwise (on 1851–1891 the posterior mean is slightly below the MLE). A posterior is computed inside the model; on all 112 years it is a precise estimate of a single rate that the dispersion test and the change-point analysis show does not exist. Concentration measures how much data there are, not whether the likelihood is right; the prior regularises, it does not test.
> Ref: Greenberg 1e §2.2 (pp. 12–18); slides `class1-poisson-with-exponential-prior.pdf`
> Similar: Notas/L01/L01-04-first-bayesian-poisson.md §5–§7; Notas/L01/L01-10-pitfalls.md §15, item 14; G 2.2 (p. 19)

## reg

Q: A researcher fits a sequence of ever richer regressions with interactions and picks the one with the highest $R^2$, which ends up close to one on the training data. Which diagnosis is correct?
- Adjusted $R^2$ would fully solve the problem, since it corrects for the number of parameters of the chosen model and therefore also for the fact that the model was picked as the best of many candidates.
- The choice is acceptable as long as every coefficient of the chosen model is significant at the 5% level, because significance guarantees that each added term improves the out-of-sample fit of the model.
- $R^2$ cannot fall when a column is added, so it ranks nested models by size; the training error is optimistic by an amount growing with the parameter count, and picking the winner biases it up again.
- The near-one $R^2$ signals multicollinearity, which only inflates standard errors; predictions stay reliable, because least squares remains unbiased however many correlated regressors enter the model.
<!-- YW5zOjI= -->
> Nested least squares cannot do worse in-sample, so $R^2$ always prefers the biggest model; with more columns than observations it reaches one while the out-of-sample fit collapses (the Boston example). The expected training error understates the test error by a term proportional to the number of parameters, which is what $C_p$, AIC and BIC add back, and held-out data measure directly. Adjusted $R^2$ penalises one model's size, not the search; significance is a different question from predictive gain (a single added regressor raises adjusted $R^2$ when its $t$ exceeds one in absolute value).
> Ref: Wooldridge 6e §3.1–3.3 (pp. 60–81), §6.3 (pp. 180–186); Izbicki & Mendonça §1.4–1.5 (pp. 9–24), §3.1–3.2 (pp. 33–37); slides `multiplelinearregression.pdf`
> Similar: Notas/L01/L01-06-gaussian-linear-regression.md §5–§7; Notas/L01/L01-10-pitfalls.md §8–§9, items 20–24; MS 6.15

Q: Compare three processes: an AR(1) whose coefficient is just below one, a random walk, and a bivariate VAR(1) with one diagonal coefficient exceeding one but all eigenvalues of its coefficient matrix inside the unit circle. Which statement is correct?
- All three are nonstationary: the first because shocks to it persist for many periods, the second by construction, and the third because a single coefficient above one is enough to make one component explosive.
- The first and third are stationary but the second is not; OLS on the lag is the exact Gaussian MLE for the AR(1), and the VAR's stationarity can be read from its largest single coefficient.
- Only the random walk lacks an equilibrium, but the persistent AR(1) has an infinite long-run variance as well, so it behaves like a random walk for every practical purpose despite being stationary on paper.
- The AR(1) is stationary and its law converges to an equilibrium that forgets the start; the random walk has no equilibrium and a variance growing with time; the VAR is stationary, as eigenvalues decide.
<!-- YW5zOjM= -->
> For an AR(1) stationarity needs only the coefficient to be below one in absolute value; then the conditional distribution given any start converges to a normal equilibrium with finite variance, however slowly. At a unit root the variance grows linearly in time and there is no equilibrium. For a VAR(1) the condition is that every eigenvalue of the coefficient matrix lies inside the unit circle; Tsay's Example 8.3 has a diagonal entry of 1.1 and is stationary. OLS on the lag maximises the likelihood conditional on the first observation, not the exact one, and the persistent AR(1) has a finite long-run variance.
> Ref: Tsay AFTS 3e §2.1–2.4 (pp. 30–57), §8.1–8.2 (pp. 390–417); slides `ar-ma.pdf`
> Similar: Notas/L01/L01-07-ar-var-review.md §6–§9; Notas/L01/L01-10-pitfalls.md §10, items 25–28; T 2.2 (p. 104); T 8.1 (p. 462)

Q: With one normal observation, a null mean of 0 and a simple alternative mean of 4, an observation gives a one-sided p-value of about 0.036, yet with equal prior odds the posterior probability of the alternative is only about 0.31. Which explanation is correct?
- The p-value is a tail area under the null that ignores the alternative; the observation is nearer the null value than the alternative, so the likelihood ratio favours the null despite its tail position.
- The p-value is the probability that the null is true, so a value of 3.6% against a posterior of 69% for the null shows that equal prior odds were a poor choice that a better calibrated prior would repair.
- The two disagree only because there is a single observation; with a large sample the p-value and the posterior probability always converge to each other, so the conflict is a small-sample artefact.
- A Bonferroni correction for the number of hypotheses compared would reconcile the two numbers, since the gap arises from testing the null against an alternative chosen after looking at the data.
<!-- YW5zOjA= -->
> Significance and evidence answer different questions. The p-value measures how unusual the data are under the null alone. The Bayes factor compares the density heights under both hypotheses, and an observation of about 1.8 is nearer to 0 than to 4, so it favours the null with a Bayes factor of about 2.2. The large-sample claim is backwards: the Jeffreys–Lindley paradox shows the two can diverge more as $n$ grows. Bonferroni addresses the family-wise error of many tests, which is the p-hacking problem (the minimum of many p-values is not a p-value), not the gap between a tail area and a posterior probability.
> Ref: slides `part1-p-hacking.pdf`, `p_hacking_slides-economics.pdf`; Greenberg 1e §3.2.4 (pp. 33–38)
> Similar: Notas/L01/L01-08-p-hacking-evidence.md §3–§4; Notas/L01/L01-10-pitfalls.md §4, §16, items 29–30; G 3.8 (p. 40)
