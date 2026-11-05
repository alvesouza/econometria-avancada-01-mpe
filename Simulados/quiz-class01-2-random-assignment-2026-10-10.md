---
quiz: "Class 1 · Quiz 2: Random Assignment, SUTVA and Precision vs Identification"
tags:
  ra: "Random assignment"
  sutva: "SUTVA and what randomization cannot fix"
  prec: "Precision vs identification"
---

## ra

Q: Treatment $d_i$ is randomly assigned, so $(y_{0i},y_{1i})$ is independent of $d_i$, where $y_{0i},y_{1i}$ are potential outcomes and $y_i$ the observed outcome. The derivation runs $E[y_i\mid d_i=1]-E[y_i\mid d_i=0]=E[y_{1i}\mid d_i=1]-E[y_{0i}\mid d_i=0]=E[y_{1i}\mid d_i=1]-E[y_{0i}\mid d_i=1]=E[y_{1i}-y_{0i}]$. Where is independence used?
- The first step, where independence lets $y_i$ be replaced by $y_{1i}$ among the treated and by $y_{0i}$ among the untreated
- The last step only, where independence turns $E[y_{1i}\mid d_i=1]$ into $E[y_{0i}\mid d_i=1]$ plus a constant effect
- The second step, swapping $E[y_{0i}\mid d_i=0]$ for $E[y_{0i}\mid d_i=1]$, and the last, dropping the conditioning on $d_i=1$
- No step: the chain is an identity under self-selection too, and independence matters only for the SE of the estimate $\hat\rho$
<!-- YW5zOjI= -->
> The first step is the switching equation, an identity. The second uses independence of $y_{0i}$ from $d_i$ to replace the untreated group's mean with the treated group's counterfactual mean, which sets selection bias to zero. The last uses independence of the effect from $d_i$, turning the ATT into the ATE. Under self-selection the second step fails, which is the whole selection problem.
> Ref: MHE Ch. 2, §2.2, p. 12
> Similar: Class 1 notebook §6

Q: A finite population has $N$ people with fixed potential outcomes $y_{0i},y_{1i}$. Exactly $k$ of them ($1\le k\le N-1$) are treated, the treated set being drawn uniformly from all $\binom{N}{k}$ subsets. What is the expectation, over assignments, of the treated mean of $y_{1i}$ minus the untreated mean of $y_{0i}$?
- $\frac{1}{N}\sum_{i=1}^N (y_{1i}-y_{0i})$, the finite-population ATE, for every $k$ between $1$ and $N-1$
- $\frac{1}{N}\sum_{i=1}^N (y_{1i}-y_{0i})$, the finite-population ATE, but only in the balanced design $k=N/2$
- $\frac{k}{N}\sum_{i=1}^N (y_{1i}-y_{0i})$, the ATE scaled by the treated share, for every $k$ between $1$ and $N-1$
- $\frac{1}{k}\sum_{i=1}^N d_i\,(y_{1i}-y_{0i})$, the ATT of the realised draw, which changes across assignments
<!-- YW5zOjA= -->
> Each person is treated with probability $k/N$. So the expected treated mean of $y_{1i}$ is $\frac{1}{k}\sum_i \frac{k}{N}y_{1i}=\bar y_1$, and likewise the expected untreated mean of $y_{0i}$ is $\bar y_0$. The difference is the ATE for any $k$; balance affects only the variance. On the class's 8-person table, all 70 four-of-eight assignments average exactly 1.125, the ATE.
> Ref: MHE Ch. 2, §2.2, p. 12
> Similar: Class 1 notebook §6; companion "The Eight-Person Table"

Q: An 8-person table has an ATE of 1.125. Across all 70 ways of treating 4 people, the naive gap averages exactly 1.125, but it ranges from −3 to 5.25 and 17 of the 70 gaps are zero or negative. What does this show about random assignment?
- That random assignment fails in small samples, since unbiasedness needs the number of people to grow before selection bias averages away
- That selection bias survives on average, since the 17 wrong-sign draws show that the expected bias is negative in a table this small
- That the ATT and the ATE differ under randomization, since each draw treats different people whose individual effects are not equal
- That unbiasedness holds over the randomization distribution, not draw by draw; the spread is sampling variation a larger N shrinks
<!-- YW5zOjM= -->
> The mean over all assignments equals the ATE, so the expected selection bias is exactly zero even at $N=8$. Any single draw can still be far off, even in sign. That dispersion is what a standard error measures, and it falls with $N$. Unbiasedness is a property of the assignment mechanism, not of one realised experiment. (Numbers from the class's teaching table.)
> Ref: MHE Ch. 2, §2.2, p. 12
> Similar: Class 1 notebook §6; companion "The Eight-Person Table"

## sutva

Q: A randomized trial assigns some patients in each ward to an intensive treatment, and treated patients' infections spread to untreated patients in the same ward. Which part of the potential-outcomes framework fails, and does randomization repair it?
- Selection bias: untreated patients are sicker on average, and randomization repairs it by balancing $y_{0i}$ in expectation across the arms
- No interference: $y_{0i}$ depends on others' treatment, so outcomes are not indexed by $d_i$ alone, and randomization does not repair it
- One version of treatment: $d_i=1$ means something different in each ward, and randomization repairs it if wards are stratified first
- Mean independence: infection correlates $d_i$ with $y_{0i}$, and randomization repairs it once the sample grows large enough
<!-- YW5zOjE= -->
> Spillovers make a patient's outcome depend on the whole treatment vector, so "$y_{0i}$" is not one number. This is a failure of the no-interference half of SUTVA, which the notation $y_{0i},y_{1i}$ assumes from the start. Randomization balances potential outcomes, but it cannot make them well defined. The usual remedies are design changes, such as randomizing whole wards.
> Ref: MHE Ch. 2, fn. 2, p. 11 (Rubin 1974, 1977); class-01 notes §3
> Similar: Class 1 notebook §3, §12

Q: A small randomized job-training pilot finds that trainees earn more than controls. The government then trains half of all low-skill workers in the country. Why might the pilot's estimate misstate the effect of the scaled-up programme even though the pilot was perfectly randomized?
- Because the pilot estimates the ATT while the national programme needs the ATU, and these coincide only with constant effects
- Because randomization balances observables only, so the pilot's controls differed in unobserved ability from future trainees
- Because larger samples shrink the standard error, and a precisely estimated effect is mechanically smaller than a noisy one
- Because at scale training shifts market wages for everyone, so outcomes depend on how many others train, a SUTVA failure
<!-- YW5zOjM= -->
> In a small pilot, one worker's earnings do not depend on how many others are trained. At national scale they can, through general-equilibrium effects on wages. Then the potential outcomes themselves change with the programme's size, so the pilot's well-identified effect answers a different question. Randomization balances unobservables in expectation too, and the pilot's ATT equals its ATE.
> Ref: MHE Ch. 2, §2.1 fn. 2, p. 11; class-01 notes §3
> Similar: Wooldridge 6e, Ch. 1, Problem 1.2, p. 15

## prec

Q: In the illustrative model $y_{0i}\sim N(\mu_0,\sigma^2)$, $z_i=(y_{0i}-\mu_0)/\sigma$, $d_i=1\{\lambda z_i+\sqrt{1-\lambda^2}\,\nu_i>c\}$ with $\nu_i\sim N(0,1)$ independent of $z_i$, $c=\Phi^{-1}(1-\pi)$ for treated share $\pi$, and $\phi,\Phi$ the standard normal density and CDF, what is the selection bias $E[y_{0i}\mid d_i=1]-E[y_{0i}\mid d_i=0]$?
- $\sigma\lambda\,\phi(c)\,/\,[\pi(1-\pi)]$
- $\sigma\lambda\,\phi(c)\,/\,(1-\pi)$
- $\lambda\,\phi(c)\,/\,[\pi(1-\pi)]$
- $\sigma\lambda\,\Phi(c)\,/\,[\pi(1-\pi)]$
<!-- YW5zOjA= -->
> The latent index $s_i$ is standard normal with $\mathrm{corr}(z_i,s_i)=\lambda$, so $E[z_i\mid s_i]=\lambda s_i$. Truncated-normal means give $E[s\mid s>c]=\phi(c)/\pi$ and $E[s\mid s<c]=-\phi(c)/(1-\pi)$. The difference is $\phi(c)/[\pi(1-\pi)]$; multiplying by $\lambda$ and by $\sigma$ (to return to the units of $y_0$) gives the answer. The sign follows $\lambda$: negative when the sick select in. (This model is the class's illustration, not MHE's.)
> Ref: class-01 notes §7 (illustrative model, verified by simulation)
> Similar: companion "Selection Bias Decomposer"

Q: A naive estimator has a homogeneous-effect target $\tau$, a selection bias $SB\neq0$ that does not depend on the sample size $N$, and standard error $SE_N=k/\sqrt N$ for some $k>0$. The interval $\hat\tau\pm1.96\,SE_N$ then covers $\tau$ with probability $\Phi(1.96-SB/SE_N)-\Phi(-1.96-SB/SE_N)$, with $\Phi$ the standard normal CDF. What happens as $N\to\infty$?
- Coverage tends to $0.95$, because $SE_N\to0$ removes sampling error and leaves the interval centred correctly
- Coverage tends to $\Phi(1.96)-\Phi(-1.96-SB/k)$, a constant set by the ratio of the bias to $k$
- Coverage tends to $0$, because $|SB|/SE_N\to\infty$ sends both arguments of $\Phi$ to the same infinity
- Coverage stays at its small-$N$ value, because $SB$ and $SE_N$ are both fixed features of the design
<!-- YW5zOjI= -->
> $SE_N\to0$ while $SB$ is fixed, so $SB/SE_N\to\pm\infty$ and both $\Phi$ terms tend to the same limit (0 or 1): coverage tends to zero. The interval shrinks around $\tau+SB$, the wrong number. In the class simulation with $\lambda=-0.6$, coverage is already 0.2 per cent at $N=100$ and zero at $N=1{,}000$ and $10{,}000$. That is precision without identification.
> Ref: MHE Ch. 2, §2.1, p. 10 (t = 58.9); class-01 notes §8
> Similar: companion "Bigger Sample, Same Bias"

Q: Under coin-flip assignment with about 5 people per group, simulated intervals built as estimate ± 1.96 SE cover the true effect only about 89 per cent of the time. Why?
- Because random assignment is unbiased only asymptotically, so with 10 people the estimate is biased toward zero and misses
- Because 1.96 is a large-sample normal critical value; with tiny groups the SE is estimated noisily and a t value is needed
- Because chance imbalance in $y_{0i}$ is a form of selection bias, which returns whenever each group holds few people
- Because the ATT and the ATE diverge in small samples, so the interval targets an estimand other than the one covered
<!-- YW5zOjE= -->
> Unbiasedness holds at any $N$ (see the 70-assignment table). The shortfall is about inference: the unpooled SE is itself estimated from about 5 observations per group, and the ratio has heavier tails than a normal, so $\pm1.96$ is too narrow. Chance imbalance is variance, not bias. With random assignment the ATT equals the ATE at every $N$.
> Ref: class-01 notes §8; companion "Bigger Sample, Same Bias" (N = 10, λ = 0)
> Similar: Class 1 notebook §8

## sutva

Q: Which threat to an experiment's treatment–control comparison remains even when treatment was assigned perfectly at random?
- Differential attrition after assignment, as in STAR, where 49, 52 and 53 per cent of the three arms were lost to follow-up
- Imbalance of unobserved untreated outcomes in expectation, since a balance table checks only the characteristics recorded
- A population correlation between $d_i$ and the error $\eta_i$ in $y_i=\alpha+\rho d_i+\eta_i$, which least squares cannot remove
- A gap between the ATT and the ATE, since the people assigned to treatment are a different group from those assigned to control
<!-- YW5zOjA= -->
> Randomization balances everything determined before assignment, in expectation, including unobservables. So the population correlation between $d_i$ and $\eta_i$ is zero, and ATT $=$ ATE. Losses after assignment that differ by arm (STAR's attrition differed significantly, joint p of .02) can make the surviving samples non-comparable. That is why MHE treats the kindergarten results as the most reliable.
> Ref: MHE Ch. 2, §2.2, Table 2.2.1 and fn. 3, p. 14
> Similar: Class 1 notebook §9

## ra

Q: In the random-slopes model $y_i=a_i+b_i x_i$, where the intercept $a_i$ and slope $b_i$ vary across people and $x_i$ is observed, which condition is enough for OLS of $y_i$ on $x_i$ to estimate $E[a_i]$ and $E[b_i]$ consistently?
- $b_i=b$ for every $i$ with $\mathrm{Cov}(a_i,x_i)=0$, since any varying slope biases the OLS slope away from its mean
- $\mathrm{Cov}(a_i,x_i)=0$ alone, since the slope heterogeneity averages out in the error whatever its link to $x_i$
- $\mathrm{Cov}(a_i,x_i)=0$ with $\mathrm{Cov}(b_i,x_i)=\mathrm{Cov}(b_i,x_i^2)=0$, weaker than full independence
- $E[b_i\mid x_i]=0$, since the OLS slope then tends to zero and the intercept absorbs the mean effect
<!-- YW5zOjI= -->
> Write $y_i=E[a_i]+E[b_i]x_i+u_i$ with $u_i=(a_i-E a_i)+(b_i-E b_i)x_i$. OLS is consistent when $E[u_i]=0$ and $\mathrm{Cov}(x_i,u_i)=0$, which the three covariance conditions deliver. A randomly assigned binary $x_i$ is independent of $(a_i,b_i)$, so OLS on a treatment dummy estimates the average effect even with heterogeneous effects: the regression version of "random assignment identifies the ATE".
> Ref: Wooldridge 6e, Ch. 9, §9-3, pp. 285–286
> Similar: Wooldridge 6e, Ch. 9, Problem 9.6, p. 305
