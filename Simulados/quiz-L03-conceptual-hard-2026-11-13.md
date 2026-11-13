---
quiz: "L03 · Introduction to Bayesian Learning: Hard Conceptual Quiz"
tags:
  sim: "Simulation: HMC, random walks and importance sampling"
  shrink: "Hierarchical models and sparsity priors"
  dec: "Loss functions and Bayes risk"
  mod: "Posterior model probabilities and model averaging"
---

## sim

Q: On a strongly correlated two-parameter posterior, Hamiltonian Monte Carlo accepts about 99% of its proposals and gives a far larger effective sample size per gradient evaluation than any random-walk Metropolis scale, while a random walk with tiny steps also accepts most proposals but mixes badly. Why does a near-one acceptance rate signal good mixing for one sampler and poor mixing for the other?
- Acceptance rates are comparable across samplers, so the difference must come from burn-in: HMC was started at the posterior mode, while the random walk spent its early draws far from the region of high probability.
- HMC proposals are independent draws from the posterior, like accept–reject sampling, so every accepted proposal is a fresh sample, whereas a random walk keeps its current value whenever a proposal is rejected.
- HMC accepts more because its acceptance ratio ignores the posterior density and depends only on the momentum, so any trajectory is accepted, while the random walk must compare posterior densities at each step.
- A random walk accepts often only when its steps are short, so it crawls; HMC follows the gradient on a long path that nearly conserves energy, so distant proposals are accepted because the integrator is accurate.
<!-- YW5zOjM= -->
> A is wrong: the comparison is per evaluation after convergence, and the random walk's poor mixing persists however it is started; the acceptance rate means different things for different proposals.
> B is wrong: each HMC proposal starts from the current point, so successive draws are dependent, and a rejected trajectory also repeats the current value; HMC's draws are just far less autocorrelated.
> C is wrong: the acceptance ratio is the exponential of the change in total energy, which contains the potential, minus the log posterior; it would equal one only if the leapfrog steps solved the dynamics exactly.
> D is right: for a random walk, high acceptance and small moves go together, which is the high-acceptance trap of Classes 3+4; HMC decouples them, because its moves come from the gradient and its rejections come only from the discretisation error, which stays small below the step-size limit.
> Ref: class code `exemplos-1-2-3-R-STAN.txt` (Stan's HMC/NUTS); Greenberg 1e §7.2.1 (pp. 96–101), §7.3 (pp. 102–103); Neal (2011), Handbook of MCMC, ch. 5
> Similar: Listas/lista-L03-book-exercises.tex, original question on Hamiltonian Monte Carlo against random-walk Metropolis, parts (b) and (e); G 7.5 (p. 106); Notas/L03/L03-08-metropolis-hastings-hmc.md §4, §8

Q: With a fixed step size and trajectory length, an HMC chain on a correlated Gaussian posterior reports an effective sample size for the first parameter larger than the number of draws, but an effective sample size of about 15 for its square, and its sample variance is off by almost 20%. A separate run with a larger step size has energy errors that explode. Which diagnosis is correct?
- Both runs show that HMC cannot handle correlated posteriors; the first chain is stuck at its starting value, which inflates its effective sample size, and the second run merely needs a longer warm-up period before sampling.
- The trajectory is close to half the period of the slow direction, so each move nearly flips the draw's sign: the mean mixes superbly while the spread barely moves; the larger step breaks the narrow axis's stability limit.
- An effective sample size above the number of draws is impossible, so the chain has a coding error; the energy explosion shows that the gradient is wrong, since an exact leapfrog integrator conserves energy at any step size.
- The first run is fine, since the effective sample size of the parameter itself is what matters; the explosion shows that the step size is too small, so the trajectory needs more steps to cross the posterior before accepting.
<!-- YW5zOjE= -->
> A is wrong: a stuck chain has autocorrelations near one and a tiny effective sample size, not one above the number of draws; and no warm-up fixes an unstable integrator.
> B is right: strongly negative lag-one autocorrelation makes the effective sample size of the first parameter exceed the number of draws while its square barely changes between iterations; and the leapfrog integrator is stable only for step sizes below twice the posterior standard deviation in the narrowest direction. Stan's NUTS tunes the step and stops trajectories that turn back to avoid both traps.
> C is wrong: negative autocorrelation does push the effective sample size above the number of draws; and the leapfrog integrator conserves a modified energy only below its stability limit, beyond which the energy error grows geometrically.
> D is wrong: an effective sample size belongs to a function of the draws, and a chain can be excellent for one and useless for another; the explosion comes from a step that is too large, not too small.
> Ref: class code `exemplos-1-2-3-R-STAN.txt`; Greenberg 1e §7.3 (pp. 102–103, autocorrelation and numerical standard error); Neal (2011), Handbook of MCMC, ch. 5
> Similar: Listas/lista-L03-book-exercises.tex, original question on Hamiltonian Monte Carlo, parts (c)–(e); Notas/L03/L03-07-markov-chains-gibbs.md §8

Q: An importance sampler estimates a posterior expectation with a Beta(2,3) proposal, while the target density times the integrand stays positive at zero. A seeded run returns 0.800 with a reported standard error of 0.009, but the true value is 0.830. Which diagnosis is correct?
- The proposal vanishes at zero where the target does not, so the weights have infinite variance; the estimator is still consistent, but its standard-error formula is meaningless and rare huge weights dominate the run.
- The proposal is too heavy-tailed, so most draws land where the target has little mass; switching to a proposal with lighter tails than the target would cut the variance and bring the estimate within its reported error.
- Importance sampling is biased in finite samples whenever the proposal differs from the target, and 0.03 is that finite-sample bias; the reported standard error is correct and would shrink at the usual rate.
- The gap is ordinary Monte Carlo error, a little more than three reported standard errors, which happens in about one run in a thousand, so nothing is wrong with the design and the run can simply be repeated.
<!-- YW5zOjA= -->
> A is right: the variance of an importance-sampling estimate requires the integral of the squared integrand times the squared target over the proposal to be finite; a proposal that vanishes where the target does not makes it infinite, so most runs look precise and miss, and the printed standard error cannot reveal it.
> B is wrong: the problem is the opposite, a proposal with too little mass where the target has some; the rule is a proposal with tails at least as heavy as the target's.
> C is wrong: self-normalised importance sampling has a small finite-sample bias, but a gap of over three reported standard errors with a valid variance would be rare; here the variance itself does not exist.
> D is wrong: the reported standard error is the thing that is broken, so counting standard errors gives a false sense of rarity; repeated runs would keep missing in the same direction.
> Ref: Greenberg 1e §5.4 (importance sampling), §5.6 (pp. 72–74); Morettin & Singer App. B (pp. 453–478)
> Similar: Notas/L03/L03-06-monte-carlo-simulation.md §6; Notas/L03/L03-12-pitfalls.md §11; G 5.4 (Listas/lista-L03-book-exercises.tex)

## shrink

Q: A hierarchical Beta–Binomial model for the death rates of 13 hospitals changes their ranking: a hospital with 1 death in 35 cases ranks below one with 4 deaths in 129 on raw rates, but above it on posterior means. Which reading is correct?
- The crossing shows the sampler has not converged, because posterior means under a common prior must keep the order of the raw rates; a longer chain would restore the raw ranking of the two hospitals.
- The crossing reveals a misspecified prior, since a well-chosen Beta prior shrinks every hospital by the same proportion toward the common mean and therefore cannot change the order of any two raw rates.
- Shrinkage toward the common mean is strongest for small caseloads, so the small hospital's extreme low rate is pulled up more; ranks can cross because the weights differ by hospital, the point of partial pooling.
- The ranking by posterior means is arbitrary, because the common mean and precision are not identified by the data, so any league table built from the hierarchical model reflects the hyperprior, not the deaths.
<!-- YW5zOjI= -->
> A is wrong: posterior means under exchangeable priors preserve the raw order only when every unit has the same sample size; here the weight on the common mean differs by hospital.
> B is wrong: the weight on the common mean falls with the caseload, so equal proportional shrinkage would ignore how much information each hospital carries; that is the defect, not the remedy.
> C is right: with 35 cases the raw rate of 2.9% is mostly noise and moves to about 6.5%, while the hospital with 129 cases moves from 3.1% only to about 5.7%; a league table of raw rates rewards small units for luck, which partial pooling discounts.
> D is wrong: the hyperparameters do not enter the likelihood directly, but they are learned through the 13 rates, whose dispersion relative to binomial noise decides how much to pool.
> Ref: site page `hierarchical-beta-binomial.html`; Greenberg 1e §4.5–4.6 (pp. 50–53)
> Similar: Notas/L03/L03-09-hierarchical-models-shrinkage.md §4, §6; Notas/L03/L03-12-pitfalls.md §15; G 4.6, 4.7 (p. 59)

Q: In a simulated sparse regression with three non-zero coefficients, raising the number of null coefficients from 7 to 47 leaves the shrinkage of the nulls under a ridge prior and a Bayesian-lasso prior roughly unchanged, while under the horseshoe the typical null estimate becomes about eight times smaller than under ridge. Which explanation is correct?
- Its global scale, learned from all coefficients like a hierarchical variance, can fall as nulls accumulate because local scales let the three signals escape; ridge's one scale must stay large enough for the signals.
- The horseshoe shrinks every coefficient harder as their number grows, because its prior variance is split among them, so the three signals are shrunk eight times harder too and only the nulls happen to gain from it.
- Ridge and lasso estimates are posterior modes, while the horseshoe estimate is a posterior mean, and posterior means always sit closer to zero than modes, a gap that widens mechanically with the number of coefficients.
- With more coefficients than a ridge prior can handle, its posterior turns improper and is truncated by the sampler, while the horseshoe's Cauchy tails keep its posterior proper, so only the horseshoe output is valid.
<!-- YW5zOjA= -->
> A is right: the horseshoe combines one global scale with one local scale per coefficient; the signals take large local scales, so the global scale is free to shrink with the evidence of sparsity, which is the hierarchical idea of learning a common variance from the ensemble. A single ridge scale is pulled up by the signals and cannot do this.
> B is wrong: the three signals stay within a few hundredths of their true values under all three priors; the horseshoe's tails are what leave them almost unshrunk.
> C is wrong: in this simulation all three are posterior means from Gibbs samplers, and a posterior mean is not systematically closer to zero than a mode; under a Laplace prior the mode is the one with exact zeros.
> D is wrong: with 50 coefficients and 200 observations every prior here gives a proper posterior, and proper priors always do; the difference is in how each prior shares its scale across coefficients.
> Ref: slides `sparse-priors.pdf` (Carvalho, Polson and Scott 2010; Griffin and Brown 2010); class code `sparseregression-simulation-R.txt`; Greenberg 1e §4.6 (pp. 52–53)
> Similar: Listas/lista-L03-book-exercises.tex, original question on sparsity priors; Notas/L03/L03-10-sparsity-priors.md §4, §6; Notas/L03/L03-09-hierarchical-models-shrinkage.md §6

Q: An analyst fits a Bayesian lasso, that is a Laplace prior on each regression coefficient sampled by MCMC, and plans to select variables by keeping those whose posterior mean is not exactly zero, as the lasso does. Which statement is correct?
- The plan works, because the posterior mean under a Laplace prior equals the soft-thresholded lasso estimate, so coefficients whose data fall below the threshold have a posterior mean of exactly zero.
- The plan works only with a horseshoe prior, whose spike at zero places positive prior probability on each coefficient being exactly zero, so its posterior means are exactly zero for every noise coefficient.
- The plan fails only because MCMC draws are noisy; a long enough chain would show the exact zeros, since the posterior mean converges to the posterior mode as the number of draws grows without bound.
- Exact zeros belong to the posterior mode, the 0–1-loss summary; the posterior mean, the squared-loss summary, is never exactly zero, so selection needs a rule such as a spike-and-slab inclusion probability.
<!-- YW5zOjM= -->
> A is wrong: soft thresholding is the posterior mode under a Laplace prior; the posterior mean averages over a continuous posterior and is non-zero for every observation.
> B is wrong: the horseshoe density is infinite at zero but puts no point mass there, so its posterior means are small, never exactly zero.
> C is wrong: more draws make the estimate of the posterior mean more precise, not closer to the mode; the two are different summaries of the same posterior.
> D is right: which summary to report is a choice of loss function, and only the mode has exact zeros; a prior with a point mass at zero gives each variable a posterior probability of being in the model, which turns selection into model comparison.
> Ref: slides `sparse-priors.pdf`, `notas-bayesianas-slides.pdf`; Izbicki & Mendonça §3.6 (pp. 42–43); ISLP §6.2 (pp. 240–253); Greenberg 1e §8.3 (p. 130)
> Similar: Notas/L03/L03-10-sparsity-priors.md §2, §8; Notas/L03/L03-12-pitfalls.md §14; Notas/L03/L03-04-bayes-estimators-loss.md §3–§5

## dec

Q: A posterior for a Bernoulli probability is summarised by its mean, median and mode, and the analyst wants the corresponding summaries for the odds, a strictly increasing function of the probability. Which statement is correct?
- All three carry over, because a Bayes estimator under any loss is invariant to reparametrisation, just as the MLE is, so the analyst can apply the odds transformation to the three summaries already computed.
- Only the median carries over, since quantiles commute with increasing maps; the mean of the odds exceeds the odds of the mean, the map being convex, and the mode moves as the density picks up a Jacobian.
- The mean and the mode carry over, because both are computed from the whole density, while the median does not, since it uses only the ordering of the draws and ignores how far apart they lie on the new scale.
- The mode carries over, because the most probable value of the probability is also the most probable value of the odds, while the mean and the median both change because the odds transformation is nonlinear.
<!-- YW5zOjE= -->
> A is wrong: the MLE is invariant because it maximises a likelihood, which has no Jacobian; Bayes estimators are expectations or modes of a density, and both change under nonlinear maps.
> B is right: an increasing map preserves the order of the draws and so every quantile, including the median and the ends of an equal-tailed interval; by Jensen the posterior mean of the convex odds lies above the odds at the posterior mean; and the density of the odds is the density of the probability times a Jacobian, which moves its peak.
> C is wrong: the median is the one summary that carries over exactly, and the mean and mode do not, for the reasons in B.
> D is wrong: a density's peak is not preserved by a nonlinear change of variable, because the Jacobian reshapes the density; only quantiles are.
> Ref: slides `notas-bayesianas-slides.pdf`; Bolfarine & Sandoval §4.4 (pp. 64–70, non-invariance of Bayes estimators), §5.5 (pp. 85–87); Greenberg 1e §3.2.1–3.2.2 (pp. 29–32)
> Similar: Notas/L03/L03-04-bayes-estimators-loss.md §7, §9–§10; B 4.9 (p. 72)

Q: For Bernoulli data under a uniform prior and squared loss, the Bayes estimator is one plus the number of successes over two plus the sample size, and its Bayes risk is lower than that of the sample proportion. A student concludes that it has a lower frequentist risk at every value of the probability. Which statement is correct?
- The student is right, since a Bayes estimator minimises the posterior expected loss for every data set, and a rule that is best for every data set must also be best for every value of the probability.
- The student is right only in large samples, where the prior's weight vanishes; in small samples the sample proportion has the lower risk at every value, because it is unbiased and the Bayes estimator is not.
- The Bayes risk averages the frequentist risk over the prior, so a lower average allows a higher risk somewhere; near a probability of zero or one the sample proportion does better, so neither dominates.
- The comparison is meaningless, because the frequentist risk is defined only for unbiased estimators, so the Bayes estimator has no frequentist risk and can only be judged by its posterior expected loss.
<!-- YW5zOjI= -->
> A is wrong: posterior expected loss averages over the parameter given the data, while frequentist risk averages over the data given the parameter; being best in the first sense for every data set implies being best on average over the prior, not at every parameter value.
> B is wrong: at a probability of one half the Bayes estimator has the lower risk at every sample size; unbiasedness removes one term of the MSE, not the sum.
> C is right: at a probability of zero the sample proportion has zero risk, while the Bayes estimator keeps a positive bias; in the middle of the range shrinkage wins, and the prior-weighted average favours the Bayes estimator, 1/72 against 1/60 with ten trials.
> D is wrong: the frequentist risk of any rule is its expected loss at each parameter value, biased or not; for squared loss it is the MSE.
> Ref: Bolfarine & Sandoval §4.3–4.4 (pp. 61–70, Example 4.4.1); Greenberg 1e §3.2.1 (pp. 29–31); slides `notas-bayesianas-slides.pdf`
> Similar: B 4.3, 4.5 (p. 71); Notas/L03/L03-04-bayes-estimators-loss.md §9; Notas/L03/L03-12-pitfalls.md §6

## mod

Q: The log Bayes factor between two models is often approximated by the log-likelihood ratio at the MLEs minus half the log sample size per extra parameter, the BIC form. Which statement about this approximation is correct?
- It is exact for nested Gaussian models, because the Laplace approximation is exact for normal likelihoods, so the Bayes factor and its BIC form differ only when a likelihood is far from normal in shape.
- It shows that the Bayes factor penalises extra parameters as AIC does, by a fixed amount per parameter, so the two criteria rank models identically once the sample is large enough to swamp the prior.
- It makes the Bayes factor independent of the prior at every sample size, so improper priors can be used for the extra parameters of the larger model as long as the posterior in each model is proper.
- It keeps the terms that grow with the sample size and drops bounded ones, such as the log prior density at the MLE, so its error does not vanish, yet both select the same model in large samples.
<!-- YW5zOjM= -->
> A is wrong: even with a normal likelihood, the approximation drops the log prior density at the MLE and other bounded terms, so it differs from the exact Bayes factor by a constant; in the Michaela–Lila coin example the gap stays near 0.4 on the log10 scale.
> B is wrong: AIC charges a constant per parameter while the Bayes factor charges half the log sample size, which grows without bound; that is why BIC is consistent for the true model and AIC is not.
> C is wrong: the dropped prior term is exactly where the prior enters, and an improper prior makes it an arbitrary constant, so the Bayes factor becomes arbitrary; a very diffuse proper prior drives it toward the smaller model, the Jeffreys–Lindley effect.
> D is right: the growing part is the likelihood ratio and the Occam penalty of half the log sample size per parameter; the bounded part carries the prior, so BIC is a large-sample approximation that ignores it.
> Ref: Greenberg 1e §3.2.4 (pp. 33–38), §4.2 (pp. 43–44); Izbicki & Mendonça §1.5.1.1 (p. 21)
> Similar: G 3.7, 3.8 (p. 40); Notas/L03/L03-05-model-comparison-bayes-factors.md §6–§7; Notas/L01/L01-06-gaussian-linear-regression.md §6

Q: Three regression models have posterior probabilities 0.55, 0.30 and 0.15. An analyst keeps the most probable model and reports its predictive distribution for a new observation as the Bayesian answer. What does this lose?
- The predictive under model uncertainty averages each model's predictive with weights equal to the posterior model probabilities; keeping one drops 45% of that mass and usually understates the predictive spread.
- Nothing in expectation, because the most probable model's predictive equals the averaged predictive whenever its posterior probability exceeds one half, since the other models then contribute less than it does.
- Only the dependence on prior model probabilities, which averaging removes: model averaging weights the models by their Bayes factors alone, so its predictive no longer depends on the prior odds of each model.
- Only computing time, because the posterior probabilities of the three models are already conditional on the data, so the selected model's predictive already integrates over the uncertainty about which model holds.
<!-- YW5zOjA= -->
> A is right: Bayesian model averaging weights each model's predictive by its posterior probability, so the spread between models' predictions adds to the spread within each; choosing one model treats a 55% belief as certainty. In the Vanguard covariance example of the sparse-priors slides, model averaging is the benchmark that the horseshoe comes within 4–7% of.
> B is wrong: a mixture equals one component only when the other components predict the same thing; a probability above one half makes the chosen model the largest weight, not the whole answer.
> C is wrong: posterior model probabilities are prior model probabilities times marginal likelihoods, normalised, so the averaging weights always carry the prior odds.
> D is wrong: each model's predictive integrates over its own parameters only; the uncertainty about which model holds enters only through the posterior model probabilities that selection throws away.
> Ref: Greenberg 1e §3.2.4 (pp. 33–38, prediction under model uncertainty); slides `sparse-priors.pdf` (Vanguard table)
> Similar: Notas/L03/L03-05-model-comparison-bayes-factors.md §2, §8; Notas/L03/L03-10-sparsity-priors.md §7; G 3.7 (p. 40)
