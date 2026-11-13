---
quiz: "L05 · Classes 5+6: Causal inference, hard conceptual — DAGs, potential outcomes, measurement error, designs"
tags:
  dag: "DAGs, d-separation, Simpson's paradox and OVB"
  po: "Potential outcomes: QTE, positivity, identification"
  eiv: "Errors in variables"
  design: "IV, fuzzy RDD and design assumptions"
---

## dag

Q: In a causal graph for the effect of a treatment X on an outcome Y, a pre-treatment covariate Z3 lies on every back-door path from X to Y. On one path Z3 is a fork, with arrows into X and into Y; on another, Z3 is a common effect of Z1, which causes X, and of Z2, which causes Y. A colleague argues that because Z3 is measured before treatment and sits on every back-door path, adjusting for Z3 alone removes all confounding. Which assessment is correct?
- The argument is right: a variable measured before treatment cannot be a collider for the effect of X, so conditioning on Z3 blocks every back-door path and the adjusted contrast is causal
- Adjusting for Z3 blocks the fork but opens the path through Z1 and Z2, on which Z3 is a collider, so the set must also include Z1 or Z2; pre-treatment timing does not rule out collider bias
- Z3 must be left out altogether, because conditioning on a collider is never allowed, and the unadjusted comparison of X and Y is then unbiased for the causal effect of X on Y
- Adjusting for Z3 is fine only if Z1 and Z2 are dropped from the data, since conditioning on the parents of a collider is what opens the path that runs through the collider itself
<!-- YW5zOjE= -->
> A is wrong: timing does not decide collider status; Z3 is a collider on the path through Z1 and Z2 even though it precedes X, and conditioning on it opens that path.
> B is right: conditioning on Z3 closes the fork path but opens the collider path, so a valid adjustment set is Z3 together with Z1, or Z3 together with Z2, which closes the newly opened path.
> C is wrong: leaving Z3 out keeps the fork path through Z3 open, so the unadjusted contrast is confounded; the problem is solved by adding a parent of the collider, not by dropping Z3.
> D is wrong: it reverses the rule; conditioning on a collider or its descendant opens a path, while conditioning on a non-collider on that path, such as Z1 or Z2, blocks it.
> Ref: Classes 5+6 slides, notes-on-causal-inference.pdf, pp. 8–12 (junctions, d-separation, Harrison's DAG); Neal (2020), Ch. 3–4 (back-door criterion)
> Similar: Lista L05, original exercises on DAGs and the back-door criterion

Q: A study of start-ups uses only firms that survived five years. In the population of all start-ups, founder experience and initial market demand are independent, and both raise the chance of survival. Among survivors the two are clearly negatively correlated, and a regression of later profits on experience, controlling for demand, is run on the survivors only. Which reading is correct?
- The negative correlation shows that strong demand discourages experienced founders from entering, a causal link that the population data hide by averaging across sectors with different entry costs
- The correlation is a small-sample accident: since the two are independent in the population, any subsample keeps that independence, and with more survivors the negative correlation would vanish
- Selecting on survival is harmless for the profit regression as long as survival is not the outcome, since conditioning on a variable matters only when it lies on the causal path being estimated
- Survival is a common effect of experience and demand, so keeping only survivors conditions on a collider and opens a path between them; selecting on a noisy proxy of survival weakens that link
<!-- YW5zOjM= -->
> A is wrong: nothing in the setup lets demand cause experience; the dependence appears only inside the selected sample, which is the mark of selection on a common effect.
> B is wrong: independence in the population does not survive conditioning on a common effect, and a larger sample of survivors estimates the induced correlation more precisely instead of removing it.
> C is wrong: conditioning on a collider anywhere in the graph can open a non-causal path; here it links experience to demand, which is controlled for, so the experience coefficient is contaminated.
> D is right: survival is a collider of experience and demand; selecting on it, or on a descendant of it, d-connects its two causes, the Berkson-type bias of the slides' collider examples.
> Ref: Classes 5+6 slides, notes-on-causal-inference.pdf, pp. 8–11 (colliders, descendants, d-separation); Neal (2020), Ch. 3
> Similar: Lista L05, original exercise on collider bias

Q: A short regression of recovery on a drug dummy gives a negative coefficient, and adding a binary third variable flips it to positive. A student invokes the omitted-variables formula, by which the short coefficient equals the long one plus the omitted variable's effect times its regression on the drug dummy, to argue that the long regression is the causal one. Which assessment is correct?
- The formula is an identity linking the two regressions whether or not either is causal; which one is causal depends on whether the third variable is a confounder or a mediator, which only the graph can say
- The formula holds only when the long regression is causal, so the student's argument is valid as long as the third variable is measured without error and is binary, as in the slides' drug example
- A sign reversal can arise only from confounding, because a mediator can shrink an effect toward zero but cannot flip its sign, so the reversal itself proves that the long regression is the right one
- The long regression is causal whenever the third variable is correlated with the drug dummy, because that correlation is exactly the term the formula subtracts, so a nonzero auxiliary slope proves confounding
<!-- YW5zOjA= -->
> A is right: MHE stresses that the OVB formula is a mechanical link between short and long regressions that holds whether or not the long one is causal; with gender as the third variable the long table is right, with post-treatment blood pressure the short one is.
> B is wrong: the formula needs no causal assumption at all, and measurement properties of the third variable have nothing to do with which regression answers the causal question.
> C is wrong: the slides' blood-pressure version of the same numbers shows a reversal produced by stratifying on a mediator; the arithmetic of Simpson's paradox is identical either way.
> D is wrong: a mediator is also correlated with the treatment, since the treatment causes it, so a nonzero auxiliary slope cannot tell confounding from mediation.
> Ref: Classes 5+6 slides, notes-on-causal-inference.pdf, pp. 5–7 (Simpson's paradox); MHE §3.2.2–3.2.3, pp. 44–50 (OVB formula, bad control)
> Similar: Lista L05, original exercise on Simpson's paradox; MHE Table 3.2.1

## po

Q: A randomized job-training experiment finds that the earnings distribution of the treated group coincides with that of the control group at every quantile, so the quantile treatment effect is zero everywhere and the average effect is zero. Which conclusion does the design support?
- Training had no effect on anyone, because randomization makes the two groups exchangeable, and identical margins under exchangeability imply that each person's two potential outcomes are equal
- The median of the individual gains is zero, since under random assignment the quantile treatment effect at one half equals the median of the person-by-person differences in earnings
- Only the two margins are identified, so the data cannot exclude training raising some people's earnings and lowering others' by offsetting amounts; the joint law of the outcomes is not learned
- Heterogeneity can be checked by comparing the variance of earnings across arms, since randomization identifies the joint distribution of the two potential outcomes and hence the variance of individual effects
<!-- YW5zOjI= -->
> A is wrong: exchangeability gives equal margins of each potential outcome across arms, not equality of the two potential outcomes for each person; a swap of outcomes across people leaves every margin unchanged.
> B is wrong: a quantile treatment effect is a difference of marginal quantiles, while the median of individual effects depends on the unobserved joint distribution; the notes' swap counterexample has zero QTE and individual effects of plus or minus one.
> C is right: randomization identifies each marginal law, hence the ATE and every QTE, but never how a person's two potential outcomes pair up, which is what any statement about individual gains needs.
> D is wrong: the variance of individual effects involves the covariance of the two potential outcomes, which is never observed for the same person; equal arm variances are compatible with large heterogeneity.
> Ref: Classes 5+6 slides, notes-on-causal-inference.pdf, p. 15 (ATE, ATT, QTE, CATE); MHE Ch. 2, pp. 10–18
> Similar: Lista L05, QTE item

Q: An observational study of a drug adjusts for age group, and in the oldest group every patient received the drug. A sharp regression-discontinuity design has the same feature at every value of its running variable: given the running variable, treatment is either certain or impossible. Which statement is correct?
- Both violate positivity, not ignorability: the oldest cell needs a model to extrapolate its untreated outcome, and sharp RD swaps overlap for continuity at the cutoff, so it identifies the effect only there
- Both cases violate ignorability, since treatment is fully determined by an observed covariate, and that is why neither the adjustment formula nor the RD comparison can recover a causal effect without an instrument
- The oldest cell can simply be dropped, and inverse-probability weighting of the remaining cells then recovers the average effect for the whole population, because the weights rebalance the sample to the population age mix
- Sharp RD restores overlap by narrowing the bandwidth until treated and untreated units share the same values of the running variable, which is why its estimate keeps improving as the window around the cutoff shrinks
<!-- YW5zOjA= -->
> A is right: when treatment is a deterministic function of the covariate, ignorability given it holds trivially, but the propensity is 0 or 1, so positivity fails; RD replaces overlap with the continuity assumption and identifies the effect at the cutoff only.
> B is wrong: deterministic assignment given an observed variable is the most favourable case for ignorability; what breaks is the existence of comparable untreated units, not their comparability.
> C is wrong: dropping the cell changes the estimand to the average effect among the younger groups; no weight can recreate untreated outcomes in a cell that has none, since the inverse propensity is infinite there.
> D is wrong: in sharp RD no value of the running variable has both treated and untreated units at any bandwidth, and narrowing the window trades bias for variance rather than improving the estimate without limit.
> Ref: Classes 5+6 slides, notes-on-causal-inference.pdf, p. 16 (identifying assumptions, positivity), p. 28 (sharp RD); MHE §6.1, pp. 189–195
> Similar: Lista L05, RDD items

## eiv

Q: Years of schooling are recorded with classical measurement error, and the return to schooling is estimated by OLS of log wage on reported schooling. To reduce the bias, a researcher adds parents' education as a control; it is measured without error and is correlated with true schooling. What happens to the schooling coefficient?
- Attenuation falls, because the control explains part of true schooling and so leaves reported schooling less contaminated, raising the share of its remaining variance that is signal rather than noise
- Attenuation is unchanged, because the reporting noise is independent of parents' education, so the control cannot interact with the noise and the attenuation factor stays at its bivariate value
- Attenuation disappears, because once a correctly measured correlate of true schooling is held fixed, the remaining variation in reported schooling is pure signal and OLS becomes consistent again
- Attenuation gets worse, because the control absorbs part of the signal in reported schooling but none of the noise, lowering the signal share; parents' education fits better as an instrument
<!-- YW5zOjM= -->
> A is wrong: the control removes signal, not noise; the noise is independent of parents' education, so partialling out the control leaves all of it in the residual regressor.
> B is wrong: the attenuation factor with other regressors uses the residual variance of true schooling given the controls, which is smaller than its total variance, so the factor falls even though the noise is unchanged.
> C is wrong: the residual of reported schooling still contains the full measurement noise, so OLS stays inconsistent; only the signal part shrank.
> D is right: Wooldridge's formula with other regressors replaces the signal variance with its residual variance given the controls, so attenuation worsens; parents' education is Wooldridge's example of an instrument for mismeasured schooling, valid only if it is excluded from the wage equation.
> Ref: Wooldridge 6e §9.4, eq. 9.36, pp. 289–291; §15.4, pp. 479–481; Classes 5+6 slides, error-in-variables.pdf
> Similar: Lista L05, measurement-error items

Q: A survey records two self-reports of each person's schooling, each equal to true schooling plus classical noise, with the two noises independent of each other and of the wage-equation error. Analyst 1 averages the two reports and runs OLS of log wage on the average; analyst 2 instruments the first report with the second. Which comparison is correct?
- Both are consistent, because the noises have mean zero and cancel in the average just as they cancel in the instrument, so the two analysts estimate the same return with about the same precision
- Averaging halves the noise variance, so OLS on the average is still attenuated, only less; IV is consistent, since the second report's noise is unrelated to the composite error, but less precise
- IV is inconsistent, because the instrument is itself mismeasured and an instrument must be measured exactly to be exogenous, so only the averaged regression removes the attenuation bias
- Averaging removes the bias entirely, since independent noises cancel in large samples, whereas IV only exchanges attenuation for a weak-instrument bias of the same size and in the same direction
<!-- YW5zOjE= -->
> A is wrong: averaging two noisy reports leaves half the noise variance in every observation, and a large sample does not shrink per-observation noise, so OLS stays attenuated.
> B is right: the reliability ratio rises with the average but stays below one; the other report is correlated with true schooling and its noise is unrelated to the first report's noise and to the wage error, so the IV ratio recovers the slope.
> C is wrong: an instrument need not be measured exactly; it needs relevance and no correlation with the composite error, and independent noise in the instrument does not create such a correlation.
> D is wrong: averaging cancels noise only across many reports per person, not across people; and the second report is a strong instrument when the noise is moderate, so there is no comparable weak-instrument bias.
> Ref: Wooldridge 6e §9.4, pp. 287–293; §15.4, pp. 479–481; MHE p. 84
> Similar: Wooldridge 6e, Ch. 9, Problem 9.7 (measurement error with several measures)

## design

Q: Two candidate instruments for the same endogenous regressor each have the same small direct effect on the outcome, so neither satisfies exclusion exactly. Instrument 1 has a strong first stage; instrument 2 has a first-stage F statistic of about 4. Which statement is correct?
- The two IV estimators share the same probability limit, because the exclusion violation is identical, and instrument 2 only produces a wider confidence interval that still covers the truth at the nominal rate
- Instrument 2 is preferable on bias grounds, because a weaker first stage moves less endogenous variation into the fitted values, so less of the direct effect is picked up by the second stage
- IV is off by the direct effect divided by the first-stage coefficient, so the weak instrument magnifies the same small violation and can end up more biased than OLS, with poor small-sample behaviour too
- Both are unbiased in finite samples once the first stage is significant at 5%, which a first-stage F near 4 already guarantees, so the choice between the two instruments is only about precision
<!-- YW5zOjI= -->
> A is wrong: the probability limit differs, because the same direct effect is divided by a smaller first-stage coefficient; coverage of the usual interval is also poor with a weak instrument.
> B is wrong: it inverts the mechanism; the weaker the first stage, the larger the share of the reduced form that is the direct effect rather than the causal channel.
> C is right: with an exclusion violation the IV probability limit is off by the direct effect over the first-stage slope, so a weak first stage amplifies it, and Wooldridge shows IV can be worse than OLS on bias unless the instrument is far cleaner than the regressor.
> D is wrong: IV is essentially never unbiased, and an F near 4 fails the Stock–Yogo rule of thumb of about 10, so even the consistent case has unreliable finite-sample inference.
> Ref: Wooldridge 6e §15.1, pp. 466–470, and §15.3, p. 478; Classes 5+6 slides, notes-on-causal-inference.pdf, pp. 17–19
> Similar: Wooldridge 6e, Ch. 15, C3 and C5 (CARD)

Q: At a test-score cutoff for a scholarship, crossing the cutoff raises the probability of receiving the scholarship from about 30% to about 70% rather than from zero to one, and later earnings jump at the cutoff. Which estimand and assumptions are right?
- The earnings jump over the jump in scholarship probability is a Wald estimator with the cutoff indicator as instrument; under exclusion and monotonicity it is the effect for compliers at the cutoff
- The earnings jump alone is the scholarship effect, since the design is still a regression discontinuity, and the imperfect take-up only reduces precision while leaving the size of the jump unbiased
- The ratio of the two jumps estimates the average effect for every student whose score is at the cutoff, including those who get the scholarship on either side, because continuity holds for all of them
- Imperfect take-up breaks the design, so the cutoff should be dropped and the effect estimated by difference-in-differences, comparing scholarship winners before and after their scores were reported
<!-- YW5zOjA= -->
> A is right: this is fuzzy RD, which MHE treats as IV: the cutoff indicator shifts treatment probability, the outcome jump is the reduced form, and the ratio identifies a local average effect for students whose take-up the cutoff changes.
> B is wrong: with a 40-point jump in take-up, the earnings jump is an intention-to-treat effect, diluted by the students whose treatment does not change at the cutoff.
> C is wrong: always-takers and never-takers do not change treatment at the cutoff, so the ratio carries no information on their effects; it is a complier average.
> D is wrong: the discontinuity in the probability of treatment is exactly what identifies the effect; DiD would need a control group and a common-trends assumption that the setup does not supply.
> Ref: MHE §6.2, pp. 196–198 (eq. 6.2.5), and §4.4.1, p. 114 (LATE); Classes 5+6 slides, notes-on-causal-inference.pdf, p. 28
> Similar: MHE Table 6.2.1 (Angrist–Lavy class size, fuzzy RD)

Q: Each quasi-experimental design replaces random assignment with one assumption that the data cannot fully verify, and offers only a partial check of it. Which pairing is correct?
- IV rests on a strong first stage, checked by the first-stage F; DiD on equal pre-treatment outcome levels, checked by comparing baseline means; RDD on random assignment over the whole running-variable range
- IV rests on the instrument being excluded, checked by regressing the outcome on the instrument and the regressor; DiD on common trends in logs and levels alike; RDD on a linear running-variable trend
- IV rests on monotonicity alone, checked by the sign of the reduced form; DiD on the absence of any group-specific shock, checked by the post-period gap; RDD on effects that are constant along the running variable
- IV rests on exclusion, partly checked by balance on pre-determined traits; DiD on common trends absent treatment, checked by pre-period trends; RDD on continuity of the untreated mean, checked by placebo cutoffs
<!-- YW5zOjM= -->
> A is wrong: first-stage strength is testable and is not the identifying assumption; DiD allows different levels, which the group effect absorbs; RDD needs no randomization away from the cutoff.
> B is wrong: adding the instrument to the outcome regression leaves the same confounding, so that test is uninformative; and common trends in logs and in levels cannot both hold when levels differ.
> C is wrong: monotonicity matters for the LATE reading, not for exclusion; the post-period gap contains the effect itself; and RD identifies the effect at the cutoff without assuming constant effects.
> D is right: exclusion is untestable with one instrument, common trends are checked only before treatment, and continuity of the untreated mean at the cutoff is probed with placebo cutoffs and placebo outcomes.
> Ref: MHE §4.1, pp. 84–102; §5.2, pp. 169–181; §6.1, pp. 189–195; Classes 5+6 slides, notes-on-causal-inference.pdf, pp. 17–36
> Similar: Lista L05, IV, DiD and RDD items
