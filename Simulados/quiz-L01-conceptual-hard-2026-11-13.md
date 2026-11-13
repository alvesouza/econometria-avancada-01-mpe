---
quiz: "L01 · Review of Basic Ingredients: Hard Conceptual Quiz"
tags:
  mt: "Multiple testing, p-hacking and evidence"
  lik: "Likelihood, estimator properties and their limits"
  reg: "Regression, model choice and time-series diagnostics"
---

## mt

Q: A simulation mimics a specification search with no true effect: 30 students, and 24 specifications obtained by crossing the test week, an outlier rule, an optional covariate and a one- or two-sided test. The share of data sets with at least one p-value below 0.05 is about 0.31, far below the 0.71 given by the formula for 24 independent tests, and Bonferroni at 0.05/24 rejects in under 2% of data sets. Which reading is correct?
- The independence formula is the right benchmark, so the gap is Monte Carlo error that more replications would close; Bonferroni rejects too rarely because its threshold assumes that the 24 tests are independent.
- The 24 tests reuse the same students and nest one another, so they are positively dependent and win less often than 24 independent tries; Bonferroni stays valid under any dependence and is conservative here.
- One-sided tests have half the size of two-sided ones, which is what pulls the rate down to 0.31; Bonferroni's union bound breaks down when the tests are dependent, which is why it under-rejects in this design.
- Positive dependence between the tests pushes the family-wise rate above the independence formula, so the simulated 0.31 must come from a coding error; Bonferroni gives exactly 5% whatever the dependence.
<!-- YW5zOjE= -->
> A is wrong: the formula assumes independent tests, which these are not, so the gap is systematic, not simulation noise; and Bonferroni rests on the union bound, which needs no independence.
> B is right: the specifications share the same 30 students, the weekly scores share ability and GPA, and a one-sided rejection contains most two-sided ones, so the 24 tests largely agree; the search is still about six times the nominal 5%, and Bonferroni is valid but conservative under such overlap.
> C is wrong on both counts: one-sided and two-sided tests each have size 0.05 when used alone, and the union bound holds under any dependence.
> D is wrong: positive dependence makes the tests redundant and lowers the chance of at least one rejection toward the single-test 5%; Bonferroni is an upper bound, not an equality.
> Ref: slides `part1-p-hacking.pdf` (slides 4–6), `p_hacking_slides-economics.pdf` (slides 3, 10); ISLP Ch. 13 (multiple testing)
> Similar: Listas/lista-L01-book-exercises.tex, original p-hacking question, parts (a), (b), (d); Notas/L01/L01-08-p-hacking-evidence.md §3; Notas/L01/L01-10-pitfalls.md §16

Q: In a field where one hypothesis in ten is true, findings are published whenever a searched specification gives a p-value below 0.05. One such finding is re-tested on fresh data, running only the specification that won the search, fixed in advance. Which statement is correct?
- If the published effect is null, the fresh test rejects with probability 0.05, because fixing the specification restores the nominal size; the search lowers the share of true findings among those published, so replication rates fall.
- The fresh test inherits the inflated size of the search, so a null finding replicates about as often as the search produced it, near three times in ten; replication rates therefore say little about how many published findings are true.
- A finding with a p-value below 0.05 has at least a 95% chance of replicating, because the p-value bounds the probability that it is a false positive; low replication rates must therefore reflect fraud rather than a search.
- The fresh test rejects with probability equal to the power of the original test whether or not the effect is real, since the search picked the most powerful specification; searching therefore raises the replication rate of a field.
<!-- YW5zOjA= -->
> A is right: the fresh data are independent of the search, which only chose which specification to run, so under a true null its p-value is uniform and rejects 5% of the time; with a searched size of about 0.3 instead of 0.05, the share of true findings among those published falls from about 0.64 to about 0.22, and so does the expected replication rate.
> B is wrong: the inflation came from choosing the best of many tests on the same data; one pre-specified test on new data has no choice left to exploit.
> C is wrong: a p-value is a tail probability computed under the null, not the probability that the null is true or that the result replicates.
> D is wrong: power is defined under a true effect; for a null effect the rejection probability is the size, so a field full of searched nulls replicates poorly.
> Ref: slides `p_hacking_slides-economics.pdf` (slides 5–6, replication crisis); `part1-p-hacking.pdf` (slides 4–6)
> Similar: Listas/lista-L01-book-exercises.tex, original p-hacking question, part (e); Notas/L01/L01-08-p-hacking-evidence.md §6

Q: A meta-study collects tens of thousands of test statistics from economics journals and finds too few z-statistics just below 1.96 and too many just above it, a hump that is sharper for IV and difference-in-differences papers than for randomised trials. What does this pattern diagnose?
- That true effects in economics tend to be just large enough to be detected, because researchers design their studies with exactly the power needed to clear the 5% threshold, so the hump measures good study design.
- That IV and difference-in-differences papers apply multiple-testing corrections more often, which raises their critical values and moves statistics from just below the usual threshold to just above it.
- Selective reporting and specification search: without a threshold rule the distribution of statistics across studies would be smooth at 1.96, so a jump there reflects choices made after seeing results, not effect sizes.
- That p-values are not uniform under the null in observational designs, because IV and difference-in-differences estimators are biased, so the hump is a property of those estimators and would appear even with full reporting.
<!-- YW5zOjI= -->
> A is wrong: designed power spreads statistics smoothly around their expected value; it cannot create a discontinuity exactly at the conventional cut-off.
> B is wrong: corrections make rejection harder and are applied to the threshold, not to the reported statistic; they cannot pile statistics up just above 1.96.
> C is right: nothing in nature knows where 1.96 is, so mass missing just below it and piling up just above it reveals the forking paths of specification search; designs with more researcher freedom, such as IV and DiD, show more of it.
> D is wrong: an estimator's bias shifts the whole distribution of its statistics smoothly; only a decision rule keyed to the threshold produces a jump at it.
> Ref: slides `p_hacking_slides-economics.pdf` (slides 3, 7: Brodeur et al. 2016, 2020); `part1-p-hacking.pdf` (slide 3)
> Similar: Notas/L01/L01-08-p-hacking-evidence.md §1, §6

Q: A researcher adds one observation at a time, runs a test after each, and stops as soon as the p-value falls below 0.05. Which statement about this optional-stopping design is correct?
- Optional stopping is harmless for the p-value, because each interim test has size 0.05, and the probability of a false rejection over all the looks is bounded by the size of the last test that was run.
- Optional stopping distorts the likelihood itself, so the MLE and the posterior must both be corrected for the number of looks, in the same way that Bonferroni corrects the threshold used at each interim test.
- The stopping rule changes the sampling distribution, so the nominal 5% no longer bounds the false-rejection rate; but it only rescales the likelihood, so the MLE and a posterior under a fixed prior are unchanged.
- With unlimited looks the p-value keeps its size but the posterior becomes inconsistent, because a Bayesian who ignores the stopping rule is guaranteed to reach any posterior probability she happens to want.
<!-- YW5zOjI= -->
> A is wrong: each look is another chance to cross the threshold, so the error rate across looks exceeds 0.05 and, with unlimited looks, a true null is eventually rejected with probability one.
> B is wrong: a stopping rule that depends only on data already seen multiplies the likelihood by a factor free of the parameter, so the likelihood kernel, the MLE and the posterior are untouched; correcting thresholds is a frequentist device.
> C is right: this is the stopping-rule lesson of Class 1 in its p-hacking form; p-values average over outcomes the rule could have produced, while the likelihood principle makes the posterior depend only on the data observed.
> D is wrong on both counts: the p-value is the quantity whose size is destroyed, and the probability that a posterior for a false hypothesis ever climbs to a high value is bounded, so ignoring the rule does not let the Bayesian manufacture certainty.
> Ref: slides `mle_sampling_rules.pdf`; `part1-p-hacking.pdf` (slide 6: the likelihood principle); `p_hacking_slides-economics.pdf` (slide 4: optional stopping); Bolfarine & Sandoval §1.3 (pp. 4–13); Greenberg 1e §2.2 (pp. 12–18)
> Similar: Notas/L01/L01-01-likelihood-sampling-rules.md §9–§10; Notas/L01/L01-08-p-hacking-evidence.md §1, §3

## lik

Q: Three textbook cases misbehave: a Wald interval for a Bernoulli probability after 1 success in 10 trials extends below zero; an iid Poisson sample made only of zeros has no MLE for a positive rate; and the MLE of the upper bound of a uniform distribution does not solve the score equation. What do the three have in common?
- Each is a small-sample problem only: the score equation has an interior root in every case, and with a larger sample the Wald interval, the Poisson MLE and the uniform MLE all behave in the usual regular way.
- Each comes from using expected instead of observed information, and replacing the expected information by the observed curvature at the MLE repairs the interval, the all-zero sample and the uniform case alike.
- Each reflects a biased estimator, and maximum likelihood fails whenever bias is present; switching to an unbiased estimator, such as the unbiased multiple of the maximum, restores the usual normal theory.
- Each breaks a condition of the usual large-sample recipe: an interior maximum of a smooth log-likelihood, close to a quadratic near its peak, with enough information for the normal approximation to be accurate.
<!-- YW5zOjM= -->
> A is wrong: the uniform likelihood decreases wherever it is positive, so its score never vanishes at any sample size, and the maximum stays on the boundary of the support.
> B is wrong: the Bernoulli Wald interval already uses the observed curvature, which equals the plug-in expected information there; the all-zero sample and the uniform case have no interior peak whose curvature could be used.
> C is wrong: the Poisson mean is unbiased and still has no MLE in the all-zero sample, and the unbiased multiple of the maximum is just as non-normal as the maximum itself.
> D is right: the Wald interval relies on a quadratic log-likelihood that is a poor approximation with one success near the edge of the parameter space; the all-zero sample has its supremum on the boundary at a rate of zero; and the uniform support depends on the parameter, so the maximum is a boundary point that converges faster than the usual root-n rate.
> Ref: Bolfarine & Sandoval §3.1 (pp. 35–42), §3.2 (pp. 42–45); slides `mle_sampling_rules.pdf`, `class1-poisson.pdf`, `comparing-estimators-MSE-slides.pdf`
> Similar: Notas/L01/L01-10-pitfalls.md §14; Notas/L01/L01-02-poisson-mle-properties.md §4; B 3.6 (p. 53)

Q: A short count series has one large count in its first year followed by seven years of ones. Over the candidate break years, a profile likelihood puts about 0.78 of its normalised weight on a break after year one, while integrating both segment rates out under proper priors puts about 0.65 there. Which explanation is correct?
- Profiling plugs in the best rate for each segment, so a one-year segment fits its count exactly at no cost; integrating averages over the rates and so charges for a rate estimated from one observation.
- The integrated weight is lower because the priors pull both rates toward a common value, so the gap reflects prior bias and would vanish with flat improper priors placed on each of the two segment rates.
- The profile is the correct posterior of the break year under a uniform prior on the cut, and the integrated version double-counts the data, since it uses them once for the two rates and again for the cut.
- The gap comes from the discreteness of the break year, which breaks Wilks' theorem; with a continuous break date the profile weights and the integrated weights would coincide for every series length.
<!-- YW5zOjA= -->
> A is right: the profile keeps the peak height of each segment's likelihood, and a segment of one year reaches a perfect fit; the integrated likelihood keeps the area, which is small when one observation leaves the rate poorly determined. On the coal data both routes give about 0.25 at 1891, because both segments are long.
> B is wrong: the penalty comes from averaging over the rate, not from pulling it; a flat prior still integrates a likelihood that is wide for a one-year segment, and its constant is common to all cuts.
> C is wrong: the posterior of the cut integrates the rates out, which is the second route; plugging in maximised rates is what makes the profile an optimistic summary.
> D is wrong: Wilks concerns the reference distribution of a likelihood-ratio statistic; the gap here is between maximising and integrating over nuisance parameters, which would remain with a continuous break date.
> Ref: Bolfarine & Sandoval §3.4 (pp. 46–49); slides `poisson-with-breakpoint.pdf`; Greenberg 1e §7.1.1 (pp. 91–95)
> Similar: Notas/L01/L01-03-coal-mining-change-point.md §7–§8; Notas/L01/L01-10-pitfalls.md §5; G 7.3 (p. 106)

Q: For iid draws from a uniform distribution on zero to an unknown upper bound, consider three estimators of the bound: twice the first draw, the sample maximum, and the multiple of the maximum that minimises MSE among all multiples of it. Which classification is correct?
- Twice the first draw is unbiased and therefore consistent; the maximum is biased and therefore inconsistent; the best multiple is the unbiased rescaling, since removing the bias always minimises MSE within a family.
- Twice the first draw is unbiased but inconsistent; the maximum is biased but consistent; the best multiple inflates the maximum by less than the unbiased rescaling does, and so it accepts a small downward bias.
- Twice the first draw is biased, because a single draw cannot represent the sample; the maximum is unbiased and consistent; the best multiple inflates the maximum by more than the unbiased rescaling to offset its bias.
- Twice the first draw is unbiased but inconsistent; the maximum is biased and also inconsistent, because its bias never vanishes; the best multiple is the unbiased rescaling, which also has the least variance in the family.
<!-- YW5zOjE= -->
> A is wrong three times: unbiasedness is a fixed-sample property that does not imply convergence, the maximum's bias and variance both vanish, and an MSE minimum generally trades a little bias for less variance.
> B is right: twice one draw has expectation equal to the bound but an MSE that never shrinks; the maximum has MSE going to zero, hence consistency despite its bias; within the multiples of the maximum the MSE is minimised by a factor below the unbiased one, which keeps a small bias in exchange for lower variance.
> C is wrong: twice the first draw is exactly unbiased, the maximum is biased downward, and inflating beyond the unbiased factor adds both bias and variance.
> D is wrong: the maximum's bias shrinks like the bound over the sample size, so it is consistent; and among multiples of the maximum the variance rises with the multiple, so the unbiased one is not the least variable.
> Ref: Bolfarine & Sandoval §1.1.5 (p. 3), §1.3 (pp. 4–13, Table 1.1), §2.1 (pp. 15–19); slides `comparing-estimators-MSE-slides.pdf`
> Similar: Notas/L01/L01-05-comparing-estimators-mse-bootstrap.md §5, §8; Notas/L01/L01-10-pitfalls.md §1, §11; B 1.12 (p. 14)

## reg

Q: For monthly stock returns, a Ljung–Box test on the returns finds no autocorrelation up to lag 30, while the same test on the squared returns rejects overwhelmingly. Which conclusion is correct?
- The two results contradict each other, because squaring is a fixed function of the return and cannot create dependence that the returns themselves lack; one of the two tests must have been misapplied to the data.
- The returns are independent, and the squared-return rejection only reflects that squares are non-negative and skewed, which violates the normality the Ljung–Box statistic needs, so the rejection is a size distortion.
- The returns follow a stationary AR(1) with a small coefficient that the first test lacks power to detect, and squaring amplifies it, so fitting an AR(1) to the returns would remove both of the rejections.
- The returns are serially uncorrelated but not independent: the sign and level are unpredictable from the past while the size is predictable, so an iid model is wrong even though a white-noise mean model fits.
<!-- YW5zOjM= -->
> A is wrong: zero correlation rules out linear dependence only; functions of uncorrelated variables, such as their squares, can be correlated whenever the variables are dependent.
> B is wrong: under independence the squares would be independent too, and the Ljung–Box statistic relies on large-sample autocorrelation theory rather than on normality; a rejection this strong is a real signal.
> C is wrong: a small linear coefficient would show up in the returns' own autocorrelations; and an AR(1) for the mean leaves the clustering of the squared residuals untouched.
> D is right: this is the uncorrelated-but-dependent case; large moves follow large moves, which is the volatility clustering modelled by ARCH, GARCH and stochastic volatility in Class 8.
> Ref: Tsay AFTS 3e §2.1–2.3 (pp. 30–37); slides `ar-ma.pdf`
> Similar: Notas/L01/L01-07-ar-var-review.md §2–§3; Notas/L01/L01-10-pitfalls.md §13; T 2.2 (p. 104)

Q: In a regression of municipal abstention on about 5,500 municipalities, four municipality-size dummies are jointly significant, with an F statistic above 13 and a p-value below 0.0001, yet adjusted R-squared moves only from 0.754 to 0.756. Which reading is correct?
- With thousands of observations a small share of variance is still estimated precisely; the F test asks whether effects are zero, not how much they explain, and any group with F above one raises adjusted R-squared.
- The two results conflict, so the heteroskedasticity-robust F must be inflated; under homoskedasticity a jointly significant group of regressors always raises adjusted R-squared by a substantial amount in a sample this large.
- Adjusted R-squared penalises each added dummy, so a group can be significant and still lower it; here it rose only because the four dummies happen to be jointly significant at the conventional 5% level of the test.
- The small change shows that the size dummies are irrelevant and should be dropped, because a precisely estimated effect that explains little variance must be a spurious artefact of a very large sample of municipalities.
<!-- YW5zOjA= -->
> A is right: significance measures signal relative to sampling noise, which shrinks with the sample size, while adjusted R-squared measures share of variance; the exact rule is that adjusted R-squared rises when the group's F exceeds one, far below any significance threshold.
> B is wrong: with homoskedastic errors the F statistic is a function of the two R-squared values and the degrees of freedom, so a large F with a tiny R-squared gain is exactly what a large sample produces; the robust F sits inside what the printed R-squared values allow.
> C is wrong: significance is not the condition; any group with F above one raises adjusted R-squared, significant or not, and a significant group cannot lower it.
> D is wrong: small and spurious are different things; the dummies capture a real size gradient once past abstention is held fixed, and whether to keep them depends on the question, not on their share of variance.
> Ref: Wooldridge 6e §4.5 (F test, R-squared form), §6.3 (pp. 180–186); slides `regressao_abstencao_2026.pdf`, `multiplelinearregression.pdf`
> Similar: Notas/L01/L01-06-gaussian-linear-regression.md §5, §8.3; Notas/L01/L01-10-pitfalls.md §9, items 21 and 24

Q: Best-subset regression on simulated data with three true predictors among seven candidates and 128 observations selects five predictors under adjusted R-squared, four under Mallows' Cp and three under BIC. Which explanation is correct?
- BIC chose the true size because it estimates test error without bias, while Cp and adjusted R-squared ignore the number of parameters and therefore always pick the largest subset among those compared.
- All three price each parameter: adjusted R-squared admits any term whose absolute t exceeds one, Cp charges twice the noise variance, and BIC charges log n times it, which is heavier once n exceeds about seven.
- The three criteria rank models identically in large samples, so the disagreement is noise from one simulated data set, and with more observations all three would settle on the three true predictors.
- Adjusted R-squared penalises parameters the most, since it divides by the residual degrees of freedom, so its choice of five must reflect strong signals in the two extra predictors that BIC wrongly discards.
<!-- YW5zOjE= -->
> A is wrong: Cp is the criterion built as an approximately unbiased estimate of test error, and both Cp and adjusted R-squared do penalise size, which is why neither picked all seven.
> B is right: the three penalties are ordered from lenient to strict; Cp adds the expected optimism of twice the noise variance per parameter, and BIC's log n per parameter exceeds two whenever n is above about 7.4, so here it is about 2.4 times Cp's price.
> C is wrong: the penalties differ at every sample size; BIC is consistent for the true size, while Cp and AIC keep a positive probability of including a noise predictor however large n becomes.
> D is wrong: adjusted R-squared is the most lenient of the three, so it keeps predictors with modest t statistics; its larger choice reflects a weak penalty, not strong signals.
> Ref: Izbicki & Mendonça §1.5.1.1 (p. 21), §3.1–3.2 (pp. 33–37); Wooldridge 6e §6.3 (pp. 180–186); slides `multiplelinearregression.pdf` (slides 16–22)
> Similar: Notas/L01/L01-06-gaussian-linear-regression.md §5–§6; Notas/L01/L01-10-pitfalls.md §8; MS 6.15

