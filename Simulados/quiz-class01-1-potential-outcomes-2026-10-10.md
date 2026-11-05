---
quiz: "Class 1 · Quiz 1: Potential Outcomes and the Selection-Bias Decomposition"
tags:
  po: "Potential outcomes"
  est: "Estimands: ATE, ATT, ATU"
  decomp: "Selection-bias decomposition"
---

## po

Q: In the Neyman–Rubin model, person $i$ has potential outcomes $y_{0i}$ (untreated) and $y_{1i}$ (treated), treatment $d_i\in\{0,1\}$, and observed outcome $y_i = y_{0i} + (y_{1i}-y_{0i})d_i$. Which statement about this switching equation is correct?
- It is a behavioural assumption that the effect $y_{1i}-y_{0i}$ is one constant for every $i$, which is why it reappears as $y_i=\alpha+\rho d_i+\eta_i$.
- It is an identity once outcomes depend on $i$'s own $d_i$ alone, which already assumes no interference: others' treatment cannot move $y_{1i}$.
- It holds only under random assignment, since without it $E[y_i \mid d_i=1]$ need not equal $E[y_{1i} \mid d_i=1]$ and the equation mixes the groups.
- It identifies the individual effect $y_{1i}-y_{0i}$ for every person whose $y_i$ and $d_i$ are both observed, which makes the naive gap informative.
<!-- YW5zOjE= -->
> The switching equation is an accounting identity: plug in $d_i=0$ and $d_i=1$ and it returns $y_{0i}$ and $y_{1i}$. It needs no constant effect (that is the extra assumption of MHE eq. 2.3.1) and no randomization. Writing $y_{0i},y_{1i}$ as functions of $i$'s own treatment already assumes SUTVA, including no interference. It never identifies $y_{1i}-y_{0i}$, because only one outcome is observed per person (Holland's fundamental problem).
> Ref: MHE Ch. 2, §2.1, eq. 2.1.1, p. 11 and fn. 2; class-01 notes §3
> Similar: Class 1 notebook §3; companion "The Eight-Person Table"

## decomp

Q: Let $\pi=P(d_i=1)$, $\text{ATT}=E[y_{1i}-y_{0i}\mid d_i=1]$, $\text{ATU}=E[y_{1i}-y_{0i}\mid d_i=0]$ and $\text{ATE}=E[y_{1i}-y_{0i}]$, where $y_{0i},y_{1i}$ are potential outcomes and $d_i$ is treatment. Which expression equals the naive gap $E[y_i\mid d_i=1]-E[y_i\mid d_i=0]$?
- $\text{ATE} + \{E[y_{0i}\mid d_i=1]-E[y_{0i}\mid d_i=0]\} + \pi(\text{ATT}-\text{ATU})$
- $\text{ATE} + \{E[y_{1i}\mid d_i=1]-E[y_{1i}\mid d_i=0]\} + (1-\pi)(\text{ATT}-\text{ATU})$
- $\text{ATE} + \{E[y_{0i}\mid d_i=1]-E[y_{0i}\mid d_i=0]\} + (1-\pi)(\text{ATU}-\text{ATT})$
- $\text{ATE} + \{E[y_{0i}\mid d_i=1]-E[y_{0i}\mid d_i=0]\} + (1-\pi)(\text{ATT}-\text{ATU})$
<!-- YW5zOjM= -->
> First, naive gap $=$ ATT $+$ selection bias, with selection bias $=E[y_{0i}\mid d_i=1]-E[y_{0i}\mid d_i=0]$, a difference in untreated outcomes. Second, iterated expectations give $\text{ATE}=\pi\,\text{ATT}+(1-\pi)\text{ATU}$, so $\text{ATT}=\text{ATE}+(1-\pi)(\text{ATT}-\text{ATU})$. Substituting gives the last option. Using $\pi$ instead of $1-\pi$, flipping the heterogeneity term, or defining the bias with $y_{1i}$ are the usual slips.
> Ref: MHE Ch. 2, §2.1, p. 11 (ATT form); ATE form: class-01 notes §5
> Similar: Class 1 notebook §5; companion "Selection Bias Decomposer"

## est

Q: Treatment share is $\pi=P(d_i=1)\in(0,1)$, and people sort into treatment on their own gains, so $\text{ATT}>\text{ATU}$, where ATT and ATU are the mean effects $y_{1i}-y_{0i}$ among the treated and the untreated and ATE is the population mean effect. What is $\text{ATT}-\text{ATE}$?
- $(1-\pi)(\text{ATT}-\text{ATU})$, which is positive, so the treated gain more than a randomly chosen person
- $\pi(\text{ATT}-\text{ATU})$, which is positive, so the gap widens as the treated share approaches one
- $(1-\pi)(\text{ATU}-\text{ATT})$, which is negative, so the ATE overstates the gain of those who chose it
- $0$, because $\text{ATE}=\pi\,\text{ATT}+(1-\pi)\,\text{ATU}$ forces the ATT and the ATE to coincide
<!-- YW5zOjA= -->
> From $\text{ATE}=\pi\,\text{ATT}+(1-\pi)\text{ATU}$: $\text{ATT}-\text{ATE}=(1-\pi)\text{ATT}-(1-\pi)\text{ATU}=(1-\pi)(\text{ATT}-\text{ATU})$, positive under sorting on gains. The gap vanishes as $\pi\to 1$ (then the treated are everyone), not as $\pi\to 0$. The weighting identity relates the three estimands; it does not force them to be equal.
> Ref: MHE Ch. 2, §2.1, p. 11; class-01 notes §4
> Similar: Class 1 notebook §4 (ATT 2, ATU 0.25, ATE 1.125)

## decomp

Q: Subsidised training programmes target workers with low earnings potential; suppose training raises earnings for every participant. With $y_{0i}$ the earnings a worker would have without training and $d_i=1$ for participants, what does a naive participant versus non-participant comparison of earnings show?
- An overstatement of the effect, because participants are the workers who gain most, so $E[y_{0i}\mid d_i=1]-E[y_{0i}\mid d_i=0]>0$ inflates the gap
- The ATT exactly, because selection on earnings potential affects only $y_{1i}$ and leaves $E[y_{0i}\mid d_i=1]=E[y_{0i}\mid d_i=0]$ intact
- An understatement that can turn negative, because $E[y_{0i}\mid d_i=1]-E[y_{0i}\mid d_i=0]<0$ is added to a positive effect on the treated
- The ATE plus noise, because an open programme makes participation as good as random, so $E[y_{0i}\mid d_i]$ does not depend on $d_i$
<!-- YW5zOjI= -->
> Low earnings potential means low $y_{0i}$ among participants: selection bias is negative. Naive gap $=$ ATT $+$ (negative bias), so it understates the effect and can make trainees look worse off. MHE reports exactly this: non-experimental comparisons often show trainees earning less, while randomized evaluations mostly find positive effects. Selection on earnings potential is selection on $y_{0i}$, so it does not leave $y_{0i}$ balanced.
> Ref: MHE Ch. 2, §2.2, pp. 12–13
> Similar: Wooldridge 6e, Ch. 7, Problem 7.6, p. 234; Ch. 9, C10, p. 308

## po

Q: In the 2005 NHIS, people hospitalised in the past year report worse health than others (2.79 vs 2.07 on a 1–5 scale where 5 is poor), a gap of 0.71 with a t statistic of 58.9. What does the t statistic establish?
- That the gap is very precisely estimated; it is silent on selection bias, a population difference in untreated health that no sample size can shrink
- That hospitals harm health, because a t this large rules out sampling error and selection bias together at every conventional significance level
- That selection bias is small, because a large bias would inflate the standard error and push the t statistic far below conventional thresholds
- That the ATT is 0.71, since with nearly 98,000 respondents the law of large numbers makes the hospitalised and the others comparable on average
<!-- YW5zOjA= -->
> A t statistic measures the gap relative to its sampling error: precision, not identification. Selection bias, $E[y_{0i}\mid d_i=1]-E[y_{0i}\mid d_i=0]$, is a population quantity; more data estimate the biased gap more precisely. Bias does not enter the standard error, and a large sample does not balance groups that self-selected. (The numbers are MHE's, quoted as facts.)
> Ref: MHE Ch. 2, §2.1, p. 10; MHE Ch. 1, pp. 3–7
> Similar: Class 1 notebook §8; companion "Bigger Sample, Same Bias"

## decomp

Q: A dataset records only $(y_i,d_i)$ for each person, where $y_i=y_{0i}+(y_{1i}-y_{0i})d_i$ and $y_{0i},y_{1i}$ are potential outcomes. In the decomposition naive gap $=$ ATT $+$ selection bias, which quantity cannot be estimated from these data without further assumptions?
- $E[y_{1i}\mid d_i=1]$, because $y_{1i}$ is a potential outcome and potential outcomes are never observed for anyone
- $E[y_{0i}\mid d_i=0]$, because the untreated may have selected out for reasons correlated with $y_{0i}$ itself
- $P(d_i=1)$, because the share treated depends on a selection rule the researcher does not get to observe
- $E[y_{0i}\mid d_i=1]$, because it is the untreated outcome of people who were treated, which no dataset records
<!-- YW5zOjM= -->
> Among the treated, $y_i=y_{1i}$, so $E[y_{1i}\mid d_i=1]$ is a sample mean; among the untreated, $y_i=y_{0i}$, so $E[y_{0i}\mid d_i=0]$ is too; and $P(d_i=1)$ is a sample share. Only the counterfactual $E[y_{0i}\mid d_i=1]$ is missing. It is the term added and subtracted in the derivation, and both the ATT and the selection bias depend on it.
> Ref: MHE Ch. 2, §2.1, p. 11
> Similar: Class 1 notebook §5; companion "The Eight-Person Table" (god's view off)

P: Higher $y$ means better health. The effect of treatment is the same for everyone, $y_{1i}-y_{0i}=\rho>0$. The treated are sicker to begin with: $E[y_{0i}\mid d_i=1]=\mu_0-\delta$ and $E[y_{0i}\mid d_i=0]=\mu_0$, with $\delta>0$.

Q: What is the naive gap $E[y_i\mid d_i=1]-E[y_i\mid d_i=0]$, and when does it get the sign of the effect wrong?
- $\rho+\delta$; it has the wrong sign only when $\delta>\rho$ and the effect itself is negative
- $\rho-\delta$; it is negative, the wrong sign, exactly when $\delta>\rho$
- $\rho-\delta$; it is negative only when $\delta>2\rho$, since the treated share halves the bias
- $\delta-\rho$; it is negative, the wrong sign, exactly when $\rho>\delta$
<!-- YW5zOjE= -->
> With a constant effect, ATT $=\rho$. Selection bias $=(\mu_0-\delta)-\mu_0=-\delta$. Naive gap $=\rho-\delta$, which is negative (hospitals "hurt") exactly when $\delta>\rho$: the bias masks and flips a positive effect, MHE's hospital allegory. The share treated does not enter the ATT form of the decomposition.
> Ref: MHE Ch. 2, §2.1, pp. 11–12
> Similar: Class 1 notebook §5 (ATT 2, bias −5, gap −3)

P:

Q: Untreated outcomes are mean independent of treatment, $E[y_{0i}\mid d_i=1]=E[y_{0i}\mid d_i=0]$, but effects $y_{1i}-y_{0i}$ are heterogeneous and the treated share is $\pi\in(0,1)$; ATT and ATU are the mean effects among treated and untreated. What does the naive gap $E[y_i\mid d_i=1]-E[y_i\mid d_i=0]$ estimate?
- The ATE, because zero selection bias is the only condition random assignment adds, so $\text{ATT}=\text{ATE}$ follows
- $\pi\,\text{ATT}+(1-\pi)\,\text{ATU}$, the ATE, because the untreated term cancels in both groups at once
- The ATT, which differs from the ATE by $(1-\pi)(\text{ATT}-\text{ATU})$ unless effects are also independent of $d_i$
- The ATU, $E[y_{1i}-y_{0i}\mid d_i=0]$, because with $y_{0i}$ balanced the untreated column reveals it
<!-- YW5zOjI= -->
> Mean independence of $y_{0i}$ sets the selection bias to zero, so naive gap $=$ ATT. Equality with the ATE needs more: independence of the effect from $d_i$ (which full random assignment delivers, because $(y_{0i},y_{1i})\perp d_i$). Otherwise the gap to the ATE is the heterogeneity term $(1-\pi)(\text{ATT}-\text{ATU})$.
> Ref: MHE Ch. 2, §2.2, p. 12; class-01 notes §5–§6
> Similar: Class 1 notebook §6

## po

Q: Why do Angrist and Pischke call the effect of school start age on first-grade test scores a fundamentally unidentified question?
- Because start age equals current age minus time in school, so no experiment can move one of the three while holding the other two fixed
- Because ethics committees forbid assigning start ages at random, so only observational data exist and they suffer from selection on family background
- Because test scores at age six are too noisy, so any experiment would need samples far larger than school districts could plausibly supply
- Because parents who delay entry differ in income, and this selection bias cannot be removed by any design that leaves enrolment voluntary
<!-- YW5zOjA= -->
> The problem is an identity, not a practical obstacle. Testing in first grade confounds start age with maturation; testing at a fixed age confounds it with time in school. No manipulation separates the three while children are still in school (it becomes possible for adult outcomes). Ethics, noise and parental selection are design problems an ideal experiment could solve.
> Ref: MHE Ch. 1, p. 5
> Similar: Wooldridge 6e, Ch. 1, Problems 1.1–1.2, p. 15

## est

Q: A government asks two questions about a voluntary programme: (1) whether to shut it down for its current participants, and (2) whether to make it compulsory for the whole eligible population. Which estimands answer them?
- The ATE for (1) and the ATT for (2), since shutting it down affects all who are eligible while a mandate adds new people
- The ATU for (1) and the ATE for (2), since current participants were once untreated and a mandate averages both groups
- The ATT for (1) and for (2), since a voluntary programme reveals only the effect on those who chose it, and policy must use it
- The ATT for (1) and the ATE for (2), since (1) concerns those now treated and (2) concerns a randomly chosen eligible person
<!-- YW5zOjM= -->
> Shutting the programme down removes treatment from the current participants: their mean effect is the ATT. A mandate treats everyone eligible: the relevant mean is over the whole population, the ATE, which equals $\pi\,\text{ATT}+(1-\pi)\text{ATU}$. With sorting on gains, the ATT overstates what a mandate would deliver.
> Ref: MHE Ch. 2, §2.1–2.2, pp. 11–12
> Similar: Class 1 notebook §4
