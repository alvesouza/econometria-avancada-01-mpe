---
quiz: "L03 · Introduction to Bayesian Learning: Conceptual Synthesis"
tags:
  post: "Prior, posterior, predictive and sequential learning"
  conj: "Conjugacy, loss functions and model comparison"
  mcmc: "Monte Carlo and MCMC"
  shrink: "Hierarchical models and sparsity priors"
---

## post

Q: A doctor holds a high prior probability that a patient is ill. A cheap, noisy test comes back positive, and then a far more reliable test also comes back positive. Which statement is correct?
- Order matters: running the reliable test first and the noisy one second would give a different final posterior, because each update conditions on a different prior and the two likelihoods are not symmetric.
- The maximum likelihood decision and the Bayes decision always coincide once the likelihood ratio of a positive result exceeds one, so the prior never changes what the doctor concludes about the patient.
- After both positives the posterior equals the sensitivity of the better test, since the noisier test is dominated and drops out of the calculation once a more reliable result is available to condition on.
- Sensitivity is not the chance of illness given a positive result; sequential and batch updates give the same posterior, and with a far better second test the first adds little unless it is nearly free.
<!-- YW5zOjM= -->
> The common error is to read $P(\text{positive}\mid\text{ill})$ as $P(\text{ill}\mid\text{positive})$; Bayes' theorem needs the prior and the overall rate of positives. Today's posterior is tomorrow's prior, and with conditionally independent tests the product of likelihoods does not depend on the order, so sequential and batch updating agree. In the course's example the posterior moves from 70% to about 85% after the noisy test and to about 99% after both, while the reliable test alone already gives about 98%. The ML decision ignores the prior odds, which is exactly where it and the Bayes decision can part.
> Ref: slides `aprendizagembayesiana-bayesianingredients.pdf` (Diego example), `question0.pdf`; Greenberg 1e §2.2 (pp. 12–18), §3.1.3 (pp. 24–25)
> Similar: G 3.4 (p. 39); Notas/L01/L01-08-p-hacking-evidence.md §4 (likelihood ratio versus prior odds); site page `question0-R.txt` (three coins)

Q: For a normal measurement of a physical constant with a normal prior, the predictive density of a new measurement is wider than the sampling density evaluated at a point estimate of the constant. Why, and what does the prior predictive density let two physicists with different priors do before any data arrive?
- The predictive is the sampling density evaluated at the posterior mean, so the spreads are identical; the prior predictive is undefined before data arrive, because it needs a likelihood evaluated at an observation.
- The predictive averages the sampling model over parameter uncertainty, adding that spread to the noise; the prior predictive says what each prior expects to see, so the realised datum can grade the priors.
- The extra width is Monte Carlo error from approximating the predictive integral, which vanishes as the number of draws grows; the prior predictive is a device for choosing that number of draws in advance.
- The predictive is wider only when the prior is improper, since a flat prior spreads mass everywhere; with a proper prior the predictive and the plug-in sampling density coincide, so the priors cannot be compared.
<!-- YW5zOjE= -->
> Integrating the sampling density over the posterior (or, before data, over the prior) adds parameter uncertainty to measurement noise; for the normal–normal case the prior predictive variance is the noise variance plus the prior variance, in closed form. A plug-in density ignores the first source, so it is overconfident. Evaluated at the observed measurement, the prior predictive is the marginal likelihood of that prior-plus-model, and the ratio of two of them is a Bayes factor: an experienced physicist whose prior is centred far from the datum predicted it badly. With a proper prior the predictive is well defined and is always wider than the plug-in.
> Ref: slides `aprendizagembayesiana-bayesianingredients.pdf` (Example 2, predictive); Greenberg 1e §3.2.3 (pp. 32–33), §3.2.4 (pp. 33–38)
> Similar: G 3.2, 3.3 (p. 39); Notas/L02/L02-04-logistic-regression.md (posterior predictive versus plug-in, pointer to Classes 3+4)

Q: As the sample grows, a posterior usually concentrates near the MLE and the prior "washes out". In which situations does this fail?
- When the likelihood does not depend on a parameter, its conditional posterior equals its conditional prior at any sample size; and a prior that puts zero mass near the true value can never be overturned by data.
- Never, provided the prior is proper: any proper prior is eventually dominated by the likelihood, including a discrete prior on a grid that omits the true value, whose posterior moves to the true value itself.
- Only when the prior is improper, because an improper prior has infinite mass that no finite amount of data can outweigh, whereas any proper prior, identified or not, is washed out by the likelihood.
- Only when the prior is not conjugate, because non-conjugate posteriors have no closed form and therefore do not concentrate, which is why simulation is needed to locate the posterior at all.
<!-- YW5zOjA= -->
> Two conditions sit behind the large-sample result: identification and prior support. For an unidentified parameter the data never update the conditional prior. If the prior density is zero somewhere, Bayes' theorem multiplies the likelihood by zero there: a discrete prior on three values concentrates on the grid point closest to the truth, never on the truth; a Pareto prior with a lower bound above the true value can never reach it. Proper or improper and conjugate or not are irrelevant to concentration; conjugacy only buys a closed form.
> Ref: Greenberg 1e §3.1.4 (pp. 25–28), §3.1.5 (pp. 28–29); site pages `bernoulli-trials-discrete-prior.html`, `sequential-bayes-bernoulli-uniform-trials.html`
> Similar: G 3.1 (p. 39); G 2.4 (p. 19); B 4.10 (p. 72)

## conj

Q: Which statement correctly links point estimates, loss functions and familiar frequentist estimators?
- The posterior mean minimises expected absolute loss and the posterior median expected squared loss; Bayes estimators are unbiased whenever the prior is centred at the true value, so their bias never needs a separate check.
- The posterior mode minimises expected squared loss, because squared loss rewards being exactly right; Bayes estimators therefore coincide with the MLE at every sample size once the prior is flat on the parameter space.
- The mean minimises squared loss, the median absolute loss and the mode a 0–1 loss; these are biased yet approach the MLE as data dominate, and ridge and lasso are posterior modes under Gaussian and Laplace priors.
- The mean minimises expected squared loss, the median absolute loss and the mode a 0–1 loss; Bayes estimators are unbiased, and ridge and lasso are posterior means under Laplace and Gaussian priors respectively.
<!-- YW5zOjI= -->
> Minimising posterior expected loss gives the mean under squared loss, the median under absolute loss and, in the limit of a shrinking window, the mode under 0–1 loss. Bayes estimators are generally biased (the exponential–gamma example shrinks toward the prior) but asymptotically efficient, converging to the MLE as the prior's weight vanishes. A Gaussian prior on the coefficients makes the posterior mode the ridge estimate and a Laplace prior makes it the lasso; the last option swaps the priors and calls them means. A flat prior makes the mode equal the MLE, not the mean.
> Ref: slides `notas-bayesianas-slides.pdf`; Bolfarine & Sandoval §4.3–4.4 (pp. 61–70); Greenberg 1e §3.2.1 (pp. 29–31); Izbicki & Mendonça §3.6 (pp. 42–43)
> Similar: G 3.5, 3.6 (p. 39); B 4.3, 4.5 (p. 71); B 4.9 (p. 72)

Q: Physicist A has a normal prior for a constant; Physicist C has a Student-t prior with the same mean and the same variance. A single measurement lands far in the tail of both priors. Which describes the two posteriors?
- Since the two priors share their mean and variance, they carry the same information, so the two posteriors share their mean and variance as well, whatever value the measurement takes.
- The normal prior gives a fixed precision-weighted compromise however surprising the datum; the t prior's heavy tails let the likelihood win under conflict, and its posterior needs simulation.
- The t prior is more peaked at its centre than the normal prior, so it is the more informative of the two and pulls the posterior harder toward the prior mean when the measurement conflicts with it.
- Conjugacy guarantees that both posteriors are Student-t, since a normal likelihood combined with any symmetric prior yields a Student-t posterior whose degrees of freedom grow with the sample size.
<!-- YW5zOjE= -->
> Under the normal–normal model the posterior mean is a weighted average with weights fixed by the two precisions, so a surprising measurement is still discounted by the same proportion. A heavy-tailed prior keeps non-negligible mass far from its centre, so when prior and datum conflict the posterior follows the likelihood: robustness. Equal variance is not equal information about tails. The t prior is not conjugate to a normal likelihood: its predictive and posterior have no known form, which is why the course approximates them by Monte Carlo (sampling importance resampling on the physicists' page).
> Ref: slides `aprendizagembayesiana-bayesianingredients.pdf` (physicists A–C); site page `fisicos-ABCD.html`; Greenberg 1e §4.3 (pp. 44–47), §4.8 (p. 54)
> Similar: G 3.3 (p. 39); G 8.4 (p. 132) (prior sensitivity)

Q: Two models are compared by their Bayes factor and posterior model probabilities. Which statement is correct?
- The Bayes factor is the ratio of the two maximised likelihoods, so it coincides with the likelihood-ratio statistic, and posterior model probabilities can be read from a chi-square table as in a test.
- With a large sample the Bayes factor stops depending on the prior, so improper priors are harmless for parameters that appear in only one model, as long as their posterior is proper in each model.
- Posterior model probabilities equal the Bayes factor whatever the prior model probabilities, because the data swamp the prior odds, so prior odds need not be stated when reporting a comparison.
- It is a ratio of marginal likelihoods of the data, so it penalises diffuse priors on extra parameters; improper priors are unusable there, and a diffuse prior can favour a null a test rejects.
<!-- YW5zOjM= -->
> The marginal likelihood averages the likelihood over the prior, so spreading prior mass over implausible values lowers it: an automatic Occam penalty. An improper prior is defined only up to an arbitrary constant, which then multiplies the Bayes factor, so it can be used only for parameters common to both models. The same averaging produces the Jeffreys–Lindley effect: with a very diffuse alternative the Bayes factor can favour the point null while a p-value rejects it. Posterior odds are prior odds times the Bayes factor, so the prior odds always enter.
> Ref: Greenberg 1e §3.2.4 (pp. 33–38), §4.2 (pp. 43–44); slides `aprendizagembayesiana-bayesianingredients.pdf`
> Similar: G 3.7, 3.8 (p. 40); G 4.5 (p. 58); Notas/L01/L01-08-p-hacking-evidence.md §4

## mcmc

Q: A posterior mean is estimated twice with the same number of draws: once from independent draws, once from a random-walk Metropolis–Hastings chain. Which statement about the two estimates is correct?
- Chain draws are autocorrelated, so the effective sample size is below the chain length; steps far too small or too large both worsen it, and neither the numerical error nor acceptance measures posterior spread.
- Once the chain has converged its draws are as good as independent ones, so both estimates have the same numerical error, and the acceptance rate of the chain only determines how long the burn-in has to be.
- The numerical error of both estimates shrinks in proportion to the number of draws, and with enough draws it drives the posterior standard deviation itself toward zero, so long runs also sharpen inference.
- An acceptance rate close to one is the best sign for the chain, because every accepted draw is a new value, so a chain with tiny proposal steps beats one with larger steps and matches independent draws.
<!-- YW5zOjA= -->
> For independent draws the Monte Carlo error falls with the square root of the number of draws, as in the course's estimate of $\pi$. MCMC draws are positively autocorrelated, so the numerical standard error is inflated by an inefficiency factor (batch means, autocorrelation time). Tiny random-walk steps are almost always accepted but barely move; huge ones are mostly rejected and the chain sticks; intermediate scales with acceptance roughly between 20% and 50% mix best. Numerical error is about the simulation; the posterior standard deviation describes the parameter and does not shrink with more draws.
> Ref: Greenberg 1e §5.6 (pp. 72–74), §7.2.1 (pp. 96–101), §7.3 (pp. 102–103); Morettin & Singer App. B (pp. 453–478); Tsay AFTS 3e §12.1–12.4 (pp. 614–624)
> Similar: G 7.5 (p. 106); G 7.2 (p. 105); G 6.5 (p. 88)

Q: Why can a Gibbs sampler be used for a normal regression with independent normal and inverse-gamma priors and for the Poisson switch-point model, while a Bayesian logit is usually sampled by Metropolis–Hastings?
- Gibbs requires the joint posterior to be a known distribution, which holds for the regression and the switch-point model but not for the logit, whose joint posterior has no closed form at all.
- Metropolis–Hastings needs the normalising constant of the posterior, which is available for the logit through its likelihood but not for the other two models, where the marginal likelihood is intractable.
- Gibbs needs full conditionals that can be sampled directly; conditional conjugacy and latent variables supply them even when the joint is non-standard, but not for the logit, so MH is used instead.
- Gibbs fails for the logit because its coefficients are not identified without a proper prior, and MH is the only sampler that remains valid for unidentified models, since it never conditions on the parameters.
<!-- YW5zOjI= -->
> With independent normal and inverse-gamma priors the joint posterior of the regression is non-standard, yet each full conditional is normal or inverse gamma, so Gibbs cycles through them. In the switch-point model the break year has a discrete conditional and each rate a gamma conditional. Latent variables do the same job for probit and Student-t errors (data augmentation). The logit's conditionals are of no standard form and have no simple latent representation, so MH proposes and accepts with a ratio in which the unknown normalising constant cancels. Neither sampler needs that constant.
> Ref: Greenberg 1e §4.9 (pp. 54–56), §7.1 (pp. 91–96), §7.2 (pp. 96–102), §8.2.3 (pp. 126–129); Tsay AFTS 3e §12.1–12.4 (pp. 614–624)
> Similar: G 7.3 (p. 106); G 8.2, 8.8 (p. 132); MS C.5

## shrink

Q: Thirteen hospitals report deaths among heart-attack cases, with caseloads ranging from a few dozen to several hundred. A hierarchical Beta–Binomial model draws each hospital's death rate from a common Beta distribution whose mean and precision are themselves given priors. Which statement is correct?
- Every hospital's estimate is shrunk toward the common mean by the same proportion, because the shrinkage weight is set by the common Beta's precision, which is a single parameter shared by all thirteen hospitals.
- Each hospital's rate is pulled toward a common mean learned from all hospitals, most strongly where caseloads are small and raw rates noisiest: a compromise between one pooled rate and thirteen separate ones.
- The largest hospitals are shrunk the most, because they contribute most of the information about the common mean, so their estimates are pulled hardest toward it while small hospitals keep their raw rates.
- Once the common mean and precision are estimated, the model collapses to complete pooling, so every hospital receives the same posterior death rate and the differences between hospitals are treated as noise.
<!-- YW5zOjE= -->
> Partial pooling. Conditional on the hyperparameters, each hospital's posterior mean is a weighted average of its raw rate and the common mean, and the weight on the common mean falls with the hospital's caseload, as the prior weight $a/(n+a)$ does in the first Bayesian Poisson example of Class 1. A hospital with 35 cases is pulled much more than one with 350. The hyperparameters are learned from all hospitals, so each borrows strength from the others; complete pooling (one rate) and no pooling (thirteen raw rates) are the two limits the model interpolates between.
> Ref: site page `hierarchical-beta-binomial.html`; Greenberg 1e §4.5–4.6 (pp. 50–53)
> Similar: Notas/L01/L01-04-first-bayesian-poisson.md §5 (prior weight); G 4.6, 4.7 (p. 59) (exchangeability)

Q: In a regression with many candidate coefficients of which only a few are truly non-zero, how do ridge, lasso and the horseshoe prior differ in what they do to small and to large coefficients?
- The horseshoe's spike at zero and heavy tails shrink noise coefficients hard while leaving large signals nearly untouched; ridge shrinks every coefficient in proportion, and lasso zeroes some but also shrinks the large ones.
- The horseshoe is a posterior mode that sets small coefficients exactly to zero, like the lasso, and differs from it only in the tuning constant, while ridge leaves all coefficients unshrunk when the sample is large enough.
- Ridge is the best suited to sparse problems, because the light Gaussian tails of its prior keep large coefficients intact, while lasso and the horseshoe shrink large coefficients more than small ones because of their tails.
- All three give the same estimates whenever there are more candidate coefficients than observations, because the likelihood is then flat and any prior centred at zero determines the solution in the same way.
<!-- YW5zOjA= -->
> A Gaussian prior (ridge) scales every coefficient toward zero by a common factor, so it cannot both kill noise and spare signals. A Laplace prior (lasso) gives exact zeros at the posterior mode but subtracts a constant from large coefficients too. The horseshoe is a global–local scale mixture: an infinite density spike at zero shrinks noise aggressively, and Cauchy-like tails leave big coefficients almost unshrunk. Light tails are exactly what makes ridge shrink large coefficients.
> Ref: slides `sparse-priors.pdf`, `sparseregression-simulation.pdf`; ISLP §6.2 (pp. 240–253); Izbicki & Mendonça §3.6 (pp. 42–43)
> Similar: site code `sparseregression-simulation-R.txt` (port to Python); no book exercise covers sparsity priors (Map/class-plan.md, Classes 3+4)
