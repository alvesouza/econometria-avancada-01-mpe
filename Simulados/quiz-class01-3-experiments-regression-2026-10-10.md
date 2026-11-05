---
quiz: "Class 1 · Quiz 3: STAR, Experiments as Regressions and Covariates"
tags:
  star: "Tennessee STAR"
  reg: "Experiments as regressions"
  cov: "Covariates in experiments"
---

## star

Q: Tennessee STAR's balance table compares the small, regular and regular-with-aide arms on free lunch, race, age, attrition, kindergarten class size and kindergarten percentile score. How should these rows be read?
- All six rows test randomization, so the significant differences in class size and scores show that assignment failed in kindergarten
- Scores test randomization, class size tests compliance, and free lunch, race and age are outcomes the treatment could have changed
- Attrition tests randomization, while free lunch, race, age and class size are outcomes, and only the score row is pre-treatment
- Free lunch, race, age test randomization; class size shows the treatment took; attrition is a later threat; scores are outcomes
<!-- YW5zOjM= -->
> Only characteristics fixed before assignment can test randomization: free lunch, race and age, which are balanced. Class size differing (15.1 vs 22.4) is a manipulation check showing the experiment created the intended variation. Attrition happens after assignment and differs across arms (p = .02), a threat to later comparisons. Kindergarten scores are an outcome, so their difference is the effect itself.
> Ref: MHE Ch. 2, §2.2, Table 2.2.1, p. 14
> Similar: Class 1 notebook §9

Q: Why do Angrist and Pischke treat the STAR kindergarten results as more reliable than the results for later grades?
- Because kindergarten classes were smaller in every arm, so the treatment contrast was sharper than in grades one to three
- Because attrition differed across arms in later years, so later-grade samples are no longer randomly spread across class types
- Because teachers were randomized only in kindergarten, so later grades confound class size with teacher quality across schools
- Because pre-treatment test scores exist only for kindergarten, so balance on achievement can be checked only for that year
<!-- YW5zOjE= -->
> Footnote 3 explains that different attrition rates across groups can leave a non-random sample of students in higher grades. MHE also notes that after kindergarten some children switched classes and regular-class students were reassigned. Kindergarten outcomes were unaffected by attrition. STAR in fact has no pre-treatment test scores at all, which is why balance is checked on demographics.
> Ref: MHE Ch. 2, §2.2, p. 14 and fn. 3–4, pp. 14–15
> Similar: Class 1 notebook §9

## cov

Q: In STAR, the small-class estimate is 4.82 (SE 2.19) without controls, 5.37 (SE 1.26) with school fixed effects, and 5.36 (SE 1.21) when student covariates are added. Which reading is correct?
- School effects are needed because assignment was random only within schools; balanced student covariates then cut the SE, not the estimate
- School effects remove a bias from parents lobbying for small classes; student covariates then add a second layer of selection correction
- The rise from 4.82 to 5.37 proves that the unadjusted estimate was biased by failed randomization, which student covariates then confirm
- The falling SE shows the covariates were correlated with treatment, since only regressors correlated with $d_i$ can change its standard error
<!-- YW5zOjA= -->
> STAR randomized within schools (conditional random assignment), and schools differed slightly in the probability of a small class, so school effects belong to the design. MHE notes that adjusting for them has "rather minor" consequences. Student covariates are balanced, so they barely move the coefficient (5.37 to 5.36), but they explain test scores and cut the residual variance, so the SE falls. Regressors uncorrelated with $d_i$ are exactly the ones that reduce its SE without changing it.
> Ref: MHE Ch. 2, §2.2–2.3, Table 2.2.2, pp. 15, 17–18
> Similar: Wooldridge 6e, Ch. 6, C11, p. 202

## reg

Q: With a constant effect $y_{1i}-y_{0i}=\rho$, write $y_i=\alpha+\rho d_i+\eta_i$ with $\alpha=E[y_{0i}]$ and $\eta_i=y_{0i}-E[y_{0i}]$, where $y_{0i},y_{1i}$ are potential outcomes and $d_i$ is a treatment dummy. What does $E[y_i\mid d_i=1]-E[y_i\mid d_i=0]$ equal?
- $\rho+E[\eta_i\mid d_i=1]$, since $E[\eta_i]=0$ makes the untreated group's mean error vanish
- $\rho\,(1+E[\eta_i\mid d_i=1]-E[\eta_i\mid d_i=0])$, a proportional distortion of the effect
- $\rho+E[\eta_i\mid d_i=1]-E[\eta_i\mid d_i=0]$, so bias is a correlation of $d_i$ with $\eta_i$
- $\rho-E[\eta_i\mid d_i=0]$, since the treated group's mean error is absorbed into $\rho$
<!-- YW5zOjI= -->
> Conditional expectations give $\alpha+\rho+E[\eta_i\mid d_i=1]$ and $\alpha+E[\eta_i\mid d_i=0]$; subtract. The bias term equals $E[y_{0i}\mid d_i=1]-E[y_{0i}\mid d_i=0]$, the selection bias. Unconditional $E[\eta_i]=0$ says nothing about the conditional means. Random assignment makes $d_i$ independent of $\eta_i$, so the bias vanishes and OLS of $y_i$ on $d_i$ estimates $\rho$.
> Ref: MHE Ch. 2, §2.3, eq. 2.3.1, p. 17
> Similar: Wooldridge 6e, Ch. 7, §7-6, eq. 7.34, p. 230

Q: A school offers tutoring mainly to students with low prior ability. In $score_i=\beta_0+\beta_1 tutor_i+u_i$, where $u_i$ contains prior ability and $tutor_i\in\{0,1\}$, what is $\text{plim}\,\hat\beta_1-\beta_1$ for OLS, and what is its sign?
- $\mathrm{Cov}(tutor_i,u_i)/\mathrm{Var}(u_i)$, negative, since tutored students have lower ability
- $\mathrm{Cov}(tutor_i,u_i)/\mathrm{Var}(tutor_i)$, negative, since tutored students have lower ability
- $\mathrm{Cov}(tutor_i,u_i)/\mathrm{Var}(tutor_i)$, positive, since weaker students gain the most from it
- $0$ whatever the rule, since $E[u_i]=0$ holds in the population and OLS fits an intercept
<!-- YW5zOjE= -->
> For a simple regression, $\hat\beta_1\to\beta_1+\mathrm{Cov}(tutor_i,u_i)/\mathrm{Var}(tutor_i)$. Selection of low-ability students makes the covariance negative, so OLS understates the effect (it can even turn negative): the classroom version of the hospital allegory. Who gains most is a question about heterogeneity, not about the covariance with the error, and a zero mean of $u_i$ is not zero correlation with $tutor_i$.
> Ref: MHE Ch. 2, §2.3, p. 17; Wooldridge 6e, Ch. 7, §7-6, pp. 229–230
> Similar: Wooldridge 6e, Ch. 7, Problem 7.6, p. 234

## cov

Q: In an experiment, $d_i$ is randomly assigned and independent of a covariate vector $X_i$; the long regression is $y_i=\alpha+\rho d_i+X_i'\gamma+\eta_i$. In the population, what is the coefficient on $d_i$ in the short regression of $y_i$ on $d_i$ alone?
- $\rho+\gamma'\mathrm{Var}(X_i)/\mathrm{Var}(d_i)$, which exceeds $\rho$ whenever $X_i$ predicts $y_i$
- $\rho\,(1-R^2_{X})$, with $R^2_X$ the share of $y_i$ explained by $X_i$, so controls raise it
- $\rho-\gamma'\mathrm{Cov}(X_i,d_i)/\mathrm{Var}(X_i)$, which differs from $\rho$ in any finite sample
- $\rho+\gamma'\mathrm{Cov}(X_i,d_i)/\mathrm{Var}(d_i)$, which equals $\rho$ because $\mathrm{Cov}(X_i,d_i)=0$
<!-- YW5zOjM= -->
> Short equals long plus the effect of omitted $X_i$ times the regression of $X_i$ on $d_i$: $\rho+\gamma'\mathrm{Cov}(X_i,d_i)/\mathrm{Var}(d_i)$. Random assignment sets the covariance to zero, so short and long coincide in the population, as MHE says of STAR. In a given sample, chance imbalance moves the short estimate slightly. The general formula, omitted variable bias, is the subject of Class 2.
> Ref: MHE Ch. 2, §2.3, eq. 2.3.2, p. 18 (developed in Ch. 3)
> Similar: Class 1 notebook §10

Q: For the OLS coefficient on $d_i$ in $y_i=\alpha+\rho d_i+X_i'\gamma+e_i$ with $N$ observations, $\mathrm{Var}(\hat\rho)\approx\sigma_e^2/[N\,\mathrm{Var}(d_i)(1-R^2_{d\cdot X})]$, where $\sigma_e^2$ is the error variance and $R^2_{d\cdot X}$ the $R^2$ of $d_i$ on $X_i$. Why do balanced covariates shrink the SE in an experiment?
- $\sigma_e^2$ falls because $X_i$ explains part of $y_i$, while $1-R^2_{d\cdot X}$ stays near one because $X_i\perp d_i$
- $1-R^2_{d\cdot X}$ falls because $X_i$ explains part of $d_i$, while $\sigma_e^2$ stays put because $X_i$ is balanced
- $\mathrm{Var}(d_i)$ rises because conditioning on $X_i$ spreads treatment more evenly over strata of the sample
- $N$ rises effectively because each covariate adds information, while $\sigma_e^2$ and $R^2_{d\cdot X}$ do not change
<!-- YW5zOjA= -->
> Covariates that predict the outcome remove part of the residual variance, the numerator. Because they are independent of the randomly assigned $d_i$, they do not create collinearity, so the factor $1-R^2_{d\cdot X}$ stays near one. If $X_i$ explained $d_i$, the SE would rise, not fall. This is STAR's 2.19 to 1.21 pattern, and Wooldridge's case for adding regressors to reduce the error variance.
> Ref: Wooldridge 6e, Ch. 6, §6-3d, pp. 185–186; MHE Ch. 2, §2.3, p. 18
> Similar: Wooldridge 6e, Ch. 6, C11, p. 202; Class 1 notebook §10

## reg

Q: In a randomized experiment, adding pre-specified controls moves the treatment coefficient by much more than its standard error. What is the most plausible reading?
- An efficiency gain: controls reduce residual variance, and a large move is the expected sign that precision has improved
- Effect heterogeneity: the controls shift weight from the ATT toward the ATE, and these can differ a lot in any experiment
- A warning: randomization may have failed, or some controls are outcomes of treatment, so conditioning on them biases it
- Chance imbalance of the usual size: large moves are common in experiments and carry no information about the design
<!-- YW5zOjI= -->
> Under random assignment, balanced controls should move the estimate only by chance amounts, typically small relative to its SE. A large move suggests either imbalance (failed or compromised randomization) or controls affected by treatment. Conditioning on such "bad controls" reintroduces selection bias, a topic for Class 2. Precision gains show up in the SE, not in the point estimate, and with randomization the ATT equals the ATE.
> Ref: MHE Ch. 2, §2.3, pp. 17–18
> Similar: Wooldridge 6e, Ch. 9, C10, p. 308

## star

Q: In STAR's simplest regression of test scores on class-type dummies, $R^2$ is about 0.01. What does this low $R^2$ imply for the small-class estimate?
- That it is biased, since a model explaining one per cent of the variance must omit confounders correlated with class type
- That it is unreliable, since a low $R^2$ makes the OLS coefficient inconsistent until enough controls enter the model
- That small classes do not matter, since an effect explaining so little of the variance cannot be economically large
- Nothing about bias, since random assignment makes the coefficient unbiased whatever the $R^2$; it bears on precision
<!-- YW5zOjM= -->
> $R^2$ measures how much of the outcome's variance the regressors explain. It does not measure whether the coefficient is causal. With randomly assigned class type, the coefficient is unbiased at $R^2=.01$; the omitted factors are uncorrelated with treatment. A small share of explained variance is compatible with an effect of about 0.2 standard deviations, which is large in education.
> Ref: MHE Ch. 2, Table 2.2.2, p. 15; Wooldridge 6e, Ch. 6, §6-3, pp. 180–181
> Similar: Wooldridge 6e, Ch. 4, Problem 4.12 (ii), p. 145; Ch. 6, C11, p. 202

## cov

Q: The same training programme is evaluated twice: once with experimental data, where participation was randomized, and once with observational data, where men chose whether to participate. Adding prior earnings, education, age and race as controls changes which estimate more, and why?
- The experimental one, because randomized samples are smaller, so each control absorbs a bigger share of earnings variation
- The observational one, because participation there tracks prior earnings, so controls remove some selection bias
- Neither, because controls never change a treatment coefficient; they change only its standard error in every regression
- Both equally, because in each dataset the controls predict earnings and so shift the coefficient by the same amount
<!-- YW5zOjE= -->
> In the experiment, controls are balanced across arms, so they barely move the estimate. In the observational sample, participants differ systematically in prior earnings, which proxy for $y_{0i}$. Controlling for them removes the part of the selection bias that runs through observables, and only that part. Whether that suffices is the conditional independence question of Class 2. MHE notes that non-experimental training comparisons tend to show negative effects that randomized evaluations overturn.
> Ref: MHE Ch. 2, §2.2, p. 13; Wooldridge 6e, Ch. 7, §7-6, pp. 229–230
> Similar: Wooldridge 6e, Ch. 1, C4, p. 16; Ch. 9, C10, p. 308
