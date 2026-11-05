---
quiz: "L05 · Classes 5+6: Causal inference beyond randomization — DAGs, OVB, errors-in-variables, IV, DiD, RDD"
tags:
  dag: "DAGs, Simpson's paradox and d-separation"
  ovb: "Omitted-variable bias and bad controls"
  eiv: "Errors-in-variables"
  iv: "Instrumental variables"
  did: "Difference-in-differences"
  rdd: "Regression discontinuity"
---

## dag

Q: Two studies report exactly the same table of recovery by drug use and a binary third variable: within each stratum the drug group recovers more often, but in the pooled table it recovers less often. In study 1 the third variable is gender, which affects both drug take-up and recovery; in study 2 it is blood pressure measured after treatment, which the drug lowers. Which reading is correct?
- Use the stratified table in both studies, because conditioning on a third variable can only remove confounding and never add bias, so finer comparisons are at least as credible as pooled ones
- Use the stratified table for gender, a common cause whose back-door path must be blocked, and the pooled table for blood pressure, a mediator whose conditioning cuts out part of the drug's effect
- Use the pooled table in both studies, because patients chose the drug themselves, and conditioning on any variable that responds to that choice opens a collider path between drug and recovery
- Use the stratified table for blood pressure and the pooled table for gender, since only a variable that the drug itself can move is able to confound the comparison of takers with non-takers
<!-- YW5zOjE= -->
> Identical numbers, opposite answers: the causal story decides, not the table. Gender is pre-treatment and points into both drug and recovery (a fork), so the pooled comparison mixes women, who take the drug more and recover less, with men; stratifying blocks that back door. Post-treatment blood pressure sits on the path drug → BP → recovery, so stratifying on it removes the beneficial channel and leaves only the toxic direct effect; the pooled table answers the total-effect question. Conditioning can add bias (mediators, colliders), so the first option is false; gender is not a response to treatment, so the collider argument is misapplied; the last option swaps confounder and mediator.
> Ref: Class 5+6 slides, notes-on-causal-inference.pdf, §2–3 (Simpson's paradox, examples 1–2 and their DAGs); MHE Ch. 3, §3.2.3, pp. 47–50
> Similar: MHE Table 3.2.1, Ch. 3, §3.2.2, p. 46

Q: In a causal graph, a treatment D affects a variable M, and M affects the outcome Y; a pre-treatment variable C affects both D and Y; and a variable S is caused both by D and by an unobserved U that also affects Y. To estimate the total effect of D on Y, which variables should be conditioned on?
- Condition on C and M, since blocking every route between D and Y other than the direct arrow is what isolates the causal effect from both confounding and mediation
- Condition on C and S, since S is a consequence of treatment that also carries information about U, so adjusting for it soaks up part of the unobserved confounding
- Condition on nothing, since U is unobserved and no adjustment set can block a path through an unmeasured variable, so any partial adjustment only moves the bias around
- Condition on C alone, since that closes the fork through C, keeps the mediated path through M open, and leaves the path through S blocked because S is a collider
<!-- YW5zOjM= -->
> Paths from D to Y: the chain D → M → Y (part of the total effect, keep it open), the fork D ← C → Y (a back door, block it by conditioning on C), and D → S ← U → Y, which is already blocked because S is a collider. Conditioning on M blocks part of the effect and leaves only the direct effect; conditioning on S (or any descendant of S) opens the collider and creates a spurious D–U link; conditioning on nothing leaves the fork open. The unobserved U is harmless here precisely because its only route to D runs through a collider.
> Ref: Class 5+6 slides, notes-on-causal-inference.pdf, §4–6 (chains, forks, colliders, d-separation); MHE Ch. 3, §3.2.3, pp. 47–50
> Similar: MHE Table 3.2.1, Ch. 3, §3.2.2, p. 46

## ovb

Q: College attendance is assigned by lottery, and a researcher regresses earnings on college while controlling for occupation, arguing that comparing people within the same occupation makes the comparison cleaner. Occupation is affected by college and by unobserved ability, which also affects earnings. What does the occupation control do?
- It turns a clean experimental contrast into a biased one, since within an occupation graduates and non-graduates differ in ability, so selection returns even though college was randomized
- It leaves the college coefficient unbiased but less precise, since random assignment guarantees balance on every variable, including those measured after assignment such as occupation
- It removes omitted-variable bias from ability, since occupation is a good proxy for ability and proxies are valid controls whenever they are correlated with the omitted factor
- It changes the target from the total to the direct effect of college but adds no bias, since conditioning on a variable caused by the treatment only blocks the mediated channel
<!-- YW5zOjA= -->
> Occupation is a bad control: an outcome of the treatment. In DAG terms it is a collider between college and ability, so conditioning on it opens college → occupation ← ability → earnings. A non-graduate who reached a white-collar job is likely more able than a graduate in the same job, so within-occupation comparisons are contaminated by selection even under random assignment. Randomization balances only pre-treatment variables; the "direct effect" reading would be bias-free only if nothing unobserved affected both occupation and earnings; a proxy must be determined before treatment to be a valid control.
> Ref: MHE Ch. 3, §3.2.3, pp. 47–50; Class 5+6 slides, notes-on-causal-inference.pdf, §4.3 and §6 (colliders, d-separation)
> Similar: MHE Table 3.2.1, Ch. 3, §3.2.2, p. 46

Q: A simulation draws a regressor x and an omitted variable z with correlation ranging from 0 to 0.95, generates the outcome from both with positive coefficients, and for each correlation repeats two fits many times: a short regression of the outcome on x alone and a long regression on x and z. How should the sampling distributions of the x-coefficient behave as the correlation rises?
- Both stay centred on the true value at every correlation, because a positive coefficient on z adds noise to the short regression rather than bias, so only the spread of the short fit grows
- The short fit stays centred on the true value, while the long fit drifts away from it at high correlation, because collinearity between x and z biases the coefficients of the long regression
- The long fit stays centred on the true value with a widening spread, while the short fit drifts further above it, the two agreeing in centre only when the regressors are uncorrelated
- Both drift upward together, because the omitted-variable bias depends only on the correlation between x and z and on nothing that the long regression is able to condition away
<!-- YW5zOjI= -->
> This is the lecturer's omitted-variable simulation. Short equals long plus the effect of the omitted variable times the regression of omitted on included: with a positive coefficient on z and positive correlation, the short coefficient is biased upward, more so as the correlation rises, and unbiased only at zero correlation. The long regression is unbiased at every correlation; collinearity inflates its variance (wider boxplots), not its bias. Confusing "imprecise" with "biased" is the trap in the second option.
> Ref: Class 5+6 site code, omitted-variable.html; MHE Ch. 3, §3.2.2, pp. 44–46; Wooldridge 6e, Ch. 3, §3.3, pp. 73–81
> Similar: MHE Table 3.2.1, Ch. 3, §3.2.2, p. 46

## eiv

Q: Which statement about classical measurement error — noise with mean zero, independent of the true values and of the regression error — is correct?
- Noise in the outcome only inflates residual variance, while noise in a regressor pulls its slope toward zero, and first-differencing a panel worsens this as signal partly cancels and noise does not
- Noise in a regressor attenuates its slope only in a simple regression, since adding correctly measured controls lets them absorb the noise and restores a consistent estimate of the slope of interest
- Noise in the outcome attenuates slopes just as noise in a regressor does, since both lower the share of variance explained, and the attenuation factor is the same reliability ratio in the two cases
- Noise in a regressor biases its slope toward zero in small samples only, since the noise averages out as the sample grows, so with enough observations least squares becomes consistent again
<!-- YW5zOjA= -->
> Outcome noise joins the error term: slopes stay consistent, only less precise. Regressor noise makes the observed regressor correlated with the composite error, so the slope converges to the true slope times the reliability ratio, signal variance over signal-plus-noise variance: attenuation that does not vanish with n. Controls correlated with the true regressor make it worse, since they explain part of the signal and leave relatively more noise. Differencing removes the persistent signal but not the independent noise, lowering reliability further, which is why fixed-effects estimates are often smaller.
> Ref: Class 5+6 slides, error-in-variables.pdf; Wooldridge 6e, Ch. 9, §9.4, pp. 287–293; MHE Ch. 5, §5.1, pp. 165–168
> Similar: Wooldridge 6e, Ch. 9, Problem 9.7, p. 305

## iv

P: Card (1995) estimates the return to schooling for US men in 1976, with log wage as the outcome, years of education as the endogenous regressor and a dummy for growing up near a four-year college as the instrument, plus controls for experience, race, region and urban residence. OLS gives 0.075 with standard error 0.003; IV gives 0.132 with standard error 0.055.

Q: Which reading of the gap between the two estimates is coherent?
- IV above OLS shows that omitted ability biases OLS upward, so the IV figure strips out the ability premium that able people earn regardless of how much schooling they end up completing
- IV above OLS fits attenuation from misreported schooling or a higher return among men whose schooling responds to proximity, and the wide IV interval still contains the OLS value
- The large IV standard error signals a weak instrument, and since weak-instrument bias pushes IV away from OLS, the figure of 0.132 overstates the true return, so OLS should be preferred
- Because the IV interval excludes zero while it contains the OLS value, a comparison of the two estimates rejects the exogeneity of schooling at the conventional significance levels
<!-- YW5zOjE= -->
> Upward ability bias would put OLS above IV, the opposite of what is observed. Two stories fit IV > OLS: classical error in reported schooling attenuates OLS while IV is immune if the instrument is unrelated to the error, and with heterogeneous returns IV estimates a LATE for compliers, men whose schooling was moved by proximity, who may have high marginal returns. The twentyfold standard error is the price of using only proximity-driven variation; the 95% interval (about 0.02 to 0.24) contains 0.075, so a Hausman-type contrast cannot reject exogeneity. Weak-instrument bias pulls 2SLS toward OLS, not away.
> Ref: Class 5+6 slides, notes-on-causal-inference.pdf, §9.3(D); MHE Ch. 4, §4.4, pp. 111–129 and §4.6.4, pp. 153–159; Wooldridge 6e, Ch. 15, §15.4–15.5, pp. 479–484
> Similar: Wooldridge 6e, Ch. 15, C3, p. 492; C5, p. 493

Q: A colleague proposes three checks: regress education on the proximity dummy and the controls; regress log wage on education, the proximity dummy and the controls, and test whether the dummy's coefficient is zero; and verify that proximity is unrelated to family background. Which assessment is right?
- The second check is decisive, since a zero proximity coefficient in the wage equation with education included is exactly the exclusion restriction, so it validates the instrument directly
- Only the first check matters, since an instrument that strongly predicts education is valid by construction, and any link with background is absorbed by the controls in the second stage
- None of the checks is informative, since both relevance and exclusion are statements about unobservables, so with a single instrument neither of them can be confronted with any data
- The first tests relevance, the one IV condition the data can test; the second fails because education is endogenous; the third probes the plausibility of exclusion without testing it
<!-- YW5zOjM= -->
> Relevance involves only observables, so the first stage tests it; this is "the one requirement of an IV that we can always test", which the cigarette-price instrument fails in the lecturer's examples. With education endogenous, its coefficient in the wage equation is biased, so the coefficient on proximity in that regression is contaminated too; the lecturer shows that simply adding the instrument to the outcome regression neither recovers the effect nor tests anything. Exclusion and independence are statements about the unobserved error and cannot be tested with one instrument; balance on background makes them more plausible.
> Ref: Class 5+6 slides, notes-on-causal-inference.pdf, §9.1–9.3; Wooldridge 6e, Ch. 15, §15.1, pp. 462–471 and §15.5, pp. 481–484; MHE Ch. 4, §4.1, pp. 84–102
> Similar: Wooldridge 6e, Ch. 15, C3, p. 492; C5, p. 493

## did

Q: In the Card–Krueger data, mean employment per restaurant in New Jersey, which raised its minimum wage, rose by about 0.47 between February and November 1992, while in Pennsylvania, which did not, it fell by about 2.28. In the regression with time, treatment-group and interaction dummies, the interaction is 2.75 with standard error 1.73, and the treatment-group dummy is −2.95 and significant. Which reading is correct?
- The significant treatment-group dummy shows that New Jersey and Pennsylvania restaurants differ, which violates the design, so the interaction cannot be read causally before matching the states
- The time dummy of −2.28 is the causal effect of the policy on Pennsylvania, and the interaction measures how much more strongly New Jersey restaurants responded to that same common shock
- The interaction is the effect only if Pennsylvania's change is New Jersey's counterfactual; its sign defies the competitive prediction, but it is not significant, so a zero effect is not rejected
- The interaction is significant at conventional levels because the two-period difference removes all noise from restaurant heterogeneity, so the minimum wage clearly raised employment
<!-- YW5zOjI= -->
> The interaction equals the difference of the two changes, 0.47 − (−2.28) = 2.75, and it is causal under parallel trends: New Jersey would have followed Pennsylvania's path without the increase. A level difference between the states (the group dummy) is differenced out and does not threaten the design; what matters is the trend. The time dummy is Pennsylvania's change, a counterfactual trend, not a policy effect. With t ≈ 1.6 the estimate is positive but not significant at 5%, so the data fail to show the employment loss the competitive model predicts.
> Ref: Class 5+6 slides, notes-on-causal-inference.pdf, §10.1–10.2; MHE Ch. 5, §5.2, pp. 169–181; Wooldridge 6e, Ch. 13, §13.2, pp. 407–412
> Similar: Wooldridge 6e, Ch. 13, Problem 13.2, p. 425; C3, p. 427

Q: A two-group, two-period study finds very different pre-period outcome levels across the groups, and the analyst is willing to assume common trends in levels. A referee asks for the same difference-in-differences in logs. What follows?
- Common trends in levels generally imply non-common trends in logs when baseline levels differ, so both scales cannot be right, and the scale choice is itself part of the identifying assumption
- The log specification inherits the assumption automatically, since the logarithm is monotone and so preserves the ranking of the four group-period means on which the estimator is built
- The log specification is more robust, since logs remove group effects multiplicatively, so any level gap between the groups is differenced out more completely in logs than in levels
- Either scale is valid as long as covariates are added to the regression, since controlling for observed characteristics guarantees parallel trends whatever transformation the outcome is given
<!-- YW5zOjA= -->
> Equal absolute changes from different baselines are unequal percentage changes, so parallel trends cannot hold in both levels and logs unless the counterfactual trend is zero. The scale is part of the untestable assumption about the counterfactual. Monotonicity preserves rankings, not differences; covariates help only if the trend gap is explained by them. With several pre-periods one can at least check whether trends were parallel before treatment, on the chosen scale.
> Ref: MHE Ch. 5, §5.2, pp. 169–181; Class 5+6 slides, notes-on-causal-inference.pdf, §10 (DiD DAG with time and group back doors)
> Similar: Wooldridge 6e, Ch. 13, Problem 13.6, p. 426

## rdd

Q: In the minimum-drinking-age design, death rates are plotted against age in months around the 21st birthday. Motor-vehicle deaths jump at 21 while deaths from internal causes do not, and linear and quadratic fits with separate slopes on each side give similar jumps. Which conclusion is justified?
- Since no one under 21 has legal access, the design lacks overlap, so identification comes only from the chosen polynomial, and agreement across the polynomials is itself the identifying assumption
- The flat internal-cause series is a placebo suggesting nothing else at 21 shifts mortality broadly, and agreement across fits eases the worry that curvature is being mistaken for a jump
- The internal-cause series acts as a control group, so the causal effect is the motor-vehicle jump minus the internal-cause jump, which turns the design into a difference-in-differences across causes
- A higher-order polynomial over the whole age range would be preferable, since it captures curvature far from the cutoff better and therefore gives a more reliable estimate of the jump at 21
<!-- YW5zOjE= -->
> Sharp RD identifies the effect at the cutoff by continuity: without legal access, mean death rates would evolve smoothly through 21. Internal causes, which alcohol access should not affect, act as a placebo outcome; no jump there supports continuity of other determinants. Robustness across functional forms addresses the danger that nonlinearity is mistaken for a discontinuity. Lack of overlap is real, but identification rests on continuity, not on a polynomial; the placebo is a check, not a control to subtract; and high-order global polynomials are exactly what Gelman and Imbens warn against, with local linear fits near the cutoff trading bias against variance.
> Ref: Class 5+6 slides, notes-on-causal-inference.pdf, §11.1–11.6; MHE Ch. 6, §6.1, pp. 189–195
> Similar: Class 5+6 site code, example3-RDD-age-mva-internal.html
