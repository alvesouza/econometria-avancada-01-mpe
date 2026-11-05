# Bolfarine & Sandoval, Introdução à Inferência Estatística (2010)
#book/bolfarine
> Link: [[Livros/Bolfarine, Sandoval - Introdução à Inferência Estatística (2010)|Bolfarine & Sandoval]]

> Page numbers are printed book pages. PDF-to-printed offset: printed = PDF page − 6, constant through the whole file (verified from printed folios: PDF 8 = p. 2, PDF 49 = p. 43, PDF 126 = p. 120).
> TOC warning: the printed "CONTEÚDO" (PDF pp. 3–4) carries page numbers from a different layout and does not match the folios (e.g. it gives §1.4 at p. 17, §3.1 at p. 46, §4.1 at p. 49, "REFERÊNCIAS" at p. 155). All pages below are read from the running heads, not the TOC. The TOC also lists an "ÍNDICE REMISSIVO" (p. 156) that is not in this PDF; the text ends with "Referências" (pp. 119–120). Pages 56, 90 and 118 are blank.
> Language note: Portuguese text; titles below are verbatim. The preface is dated "São Paulo, setembro de 2000".

## Ch. 1 — Elementos Básicos
**Pages:** pp. 1–14

### §1.1 — Alguns Modelos Especiais (pp. 1–3)
**Subtopics:**
- §1.1.1 O modelo normal (p. 1): N(μ, σ²) density, support the whole real line, E[X] = μ, Var[X] = σ².
- §1.1.2 O modelo exponencial (pp. 1–2): Exp(θ) density θe^(−θx), mean 1/θ, variance 1/θ², and the memoryless property for lifetimes.
- §1.1.3 O modelo binomial (p. 2): Binomial(n, θ) as a sum of n independent Bernoulli(θ) variables, mean nθ, variance nθ(1 − θ).
- §1.1.4 O modelo de Poisson (pp. 2–3): Poisson(θ) probability function e^(−θ)θ^x/x!, with E[X] = Var[X] = θ, for counts in a fixed time interval.
- §1.1.5 O modelo uniforme (p. 3): U(0, θ) written with an indicator function; its support depends on θ, unlike the four models above.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] — **Assigned reading (Class 1)**: §1.1.4 only (pp. 2–3).

### §1.2 — Tipos de Problemas (p. 4)
**Subtopics:**
- Definition 1.2.1: statistical inference as specifying values of an unknown θ from observed data; estimation versus hypothesis testing.

### §1.3 — Amostras, Estatísticas e Estimadores (pp. 4–13)
**Subtopics:**
- definitions of population, random sample (i.i.d. draws), and the likelihood function L(θ; x) = ∏ f(xᵢ|θ) (1.3.1).
- statistic, parameter space Θ, estimator of θ and of g(θ) (Definitions 1.3.3–1.3.6).
- mean squared error and its decomposition MSE = Var + bias² (1.3.2); unbiased and asymptotically unbiased estimators.
- the sample mean is unbiased; the variance estimator with divisor n is biased but asymptotically unbiased (1.3.3).
- comparing estimators by MSE: better estimator, inadmissible estimator, optimal estimator and the uniformly minimum-variance unbiased estimator.
- the sample mean is the minimum-variance linear unbiased estimator (convex weights, also via Lagrange multipliers).
- normal variance: S² (unbiased) versus σ̂² (biased) — σ̂² has the smaller MSE.
- Bernoulli: X̄ versus the constant-MSE estimator (Y + √n/2)/(n + √n); neither dominates (Figure 1.1).
- U(0, θ): X̄ (biased, mean θ/2) versus the maximum X(n), MSE comparison table (Table 1.1); X(n) is better for every θ and n > 1.
- discrete uniform (taxi/urn) problem: estimating N with X̄, X(n), 2X̄ − 1 and an exactly unbiased N̂₅.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] — **Assigned reading (Class 1)**

### §1.4 — Exercícios (pp. 13–14)
**Subtopics:**
- exercises 1.1–1.13: MSE decomposition, bias of σ̂², order statistics of the uniform, MSE comparisons. See [[bolfarine-exercises]].

## Ch. 2 — Estimadores Eficientes e Estatísticas Suficientes
**Pages:** pp. 15–34

### §2.1 — Estimadores Eficientes (pp. 15–19)
**Subtopics:**
- efficiency of an unbiased estimator, e(θ̂) = LI(θ)/Var[θ̂], with LI(θ) the lower bound for the variance of unbiased estimators (Definition 2.1.1).
- regularity conditions: support not depending on θ, and differentiation under the integral sign.
- score function ∂ log f(X|θ)/∂θ and its zero expectation (2.1.4).
- Fisher information I_F(θ) = E[(∂ log f/∂θ)²] = −E[∂² log f/∂θ²], and additivity: n I_F(θ) for a random sample (2.1.6).
- Theorem 2.1.1, the information inequality (Cramér–Rao lower bound) Var[θ̂] ≥ 1/(n I_F(θ)), proved via the correlation between θ̂ and the score.
- the sample mean is efficient for the normal mean (Example 2.1.1) and for the Poisson mean (Example 2.1.2).
- the bound checks efficiency; it is not a method for constructing estimators.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] — **Assigned reading (Class 1)**

### §2.2 — Estatísticas Suficientes (pp. 20–23)
**Subtopics:**
- Definition 2.2.1: T is sufficient for θ when the conditional distribution of the sample given T does not depend on θ.
- ΣXᵢ is sufficient for Bernoulli θ (Example 2.2.1) and for Poisson θ (Example 2.2.3); X₁ + 2X₂ + X₃ is not sufficient for Bernoulli θ (Example 2.2.2).
- Theorem 2.2.1, the Neyman factorization criterion L(θ; x) = h(x) g_θ(T(x)), proved for the discrete case.
- factorization applied: Poisson (ΣXᵢ), U(0, θ) (X(n)), N(μ, 1) (ΣXᵢ).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] — **Assigned reading (Class 1)**

### §2.3 — Estatísticas Conjuntamente Suficientes (pp. 23–25)
**Subtopics:**
- Theorem 2.3.1, the factorization criterion for a parameter vector: jointly sufficient statistics of dimension r.
- (ΣXᵢ, ΣXᵢ²) jointly sufficient for (μ, σ²) in the normal model.
- equivalent statistics (one-to-one maps) are sufficient together: (X̄, S²) for the normal model, (Σ log Xᵢ, X̄) for the gamma model.

### §2.4 — Famílias Exponenciais (pp. 25–29)
**Subtopics:**
- Definition 2.4.1, the one-parameter exponential family f(x|θ) = exp{c(θ)T(x) + d(θ) + S(x)}, with support not depending on θ.
- Bernoulli and N(μ, 1) written in exponential-family form.
- Theorem 2.4.1: a random sample from an exponential family is again an exponential family, so ΣT(Xᵢ) is sufficient.
- Definition 2.4.2, the k-parameter exponential family; N(μ, σ²) as a two-parameter member.
- bivariate normal as a five-parameter exponential family; sample means, variances and the Pearson correlation as functions of the sufficient statistic.

### §2.5 — Estimadores Baseados em Estatísticas Suficientes (pp. 29–32)
**Subtopics:**
- conditioning an unbiased estimator on a sufficient statistic, θ̂ = E[S|T], keeps it unbiased.
- Rao–Blackwell theorem: Var[E[S|T]] ≤ Var[S], via the law of total variance.
- Poisson example: Rao–Blackwellizing the indicator of {X₁ = 0} gives ((n − 1)/n)^ΣXᵢ for e^(−θ).
- complete statistics (Definition 2.5.1); ΣXᵢ complete for Bernoulli, X₁ − X₂ not complete.
- Theorem 2.5.2: the natural statistic of a k-parameter exponential family is sufficient and complete when the range of c(θ) contains a k-dimensional rectangle.
- Lehmann–Scheffé theorem (Theorem 2.5.3): E[S|T] with T sufficient and complete is the unique UMVUE ("ENVVUM"); X̄ is the UMVUE of the Poisson mean.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (related, not assigned)

### §2.6 — Exercícios (pp. 32–34)
**Subtopics:**
- exercises 2.1–2.12: Cramér–Rao bounds, sufficiency, exponential families, Rao–Blackwell and UMVUEs, including a regression model Yᵢ ~ N(βxᵢ, σ²). See [[bolfarine-exercises]].

## Ch. 3 — Métodos de Estimação
**Pages:** pp. 35–55

### §3.1 — O Método de Máxima Verossimilhança (pp. 35–42)
**Subtopics:**
- likelihood L(θ; x) = ∏ f(xᵢ|θ) and log-likelihood l(θ; x) (Definition 3.1.1); the MLE maximizes L (Definition 3.1.2).
- likelihood equation l′(θ; x) = 0 with the second-order check l″(θ̂; x) < 0 (3.1.3–3.1.4).
- MLE of the normal mean is X̄ (Example 3.1.1) and of the Bernoulli θ is X̄ (Example 3.1.2).
- U(0, θ): the likelihood equation fails and the MLE X(n) is found by inspecting L (boundary maximum; the MLE is biased).
- discrete parameter space: choosing θ ∈ {1/3, 2/3} by comparing likelihood values (Example 3.1.4).
- non-unique MLE for U(θ − 1/2, θ + 1/2): any point in [x(n) − 1/2, x(1) + 1/2] (Example 3.1.5).
- numerical MLE: Newton–Raphson iteration on the score U(θ), and Fisher scoring (replacing U′ by −n I_F); worked example with f(x|θ) = (1 + θx)/2, data generated by the inverse-CDF method (Tables 3.1–3.2).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] — **Assigned reading (Class 1)**

### §3.2 — Propriedades dos Estimadores de Máxima Verossimilhança (pp. 42–45)
**Subtopics:**
- Theorem 3.2.1: the MLE, if it exists, is a function of any sufficient statistic.
- §3.2.1 Invariância (pp. 43–44): Theorem 3.2.2, MLE invariance — g(θ̂) is the MLE of g(θ); examples θ(1 − θ) for Bernoulli, Φ(−μ) for the normal, e^(−θ) for the exponential.
- §3.2.2 Distribuição em grandes amostras (pp. 44–45): asymptotic normality of the MLE, √n(θ̂ − θ) → N(0, 1/I_F(θ)), and the delta-method version for g(θ̂) (3.2.3–3.2.4); the MLE is asymptotically unbiased and efficient; Bernoulli and Poisson e^(−X̄) examples.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] — **Assigned reading (Class 1)**

### §3.3 — Verossimilhança para Amostras Independentes (pp. 45–46)
**Subtopics:**
- the joint likelihood of independent samples is the product of their likelihoods (log-likelihoods add).
- common mean from N(μ, 4) and N(μ, 9) samples: the MLE is the precision-weighted mean, a function of the sufficient statistic.

### §3.4 — O Caso Multiparamétrico (pp. 46–49)
**Subtopics:**
- likelihood equations for θ = (θ₁, …, θ_r); boundary or support-dependent cases need inspection of L.
- profile likelihood: solve for θ₁ as a function of θ₂ and maximize the profiled g(θ₂; x).
- normal MLEs μ̂ = X̄ and σ̂² = Σ(Xᵢ − X̄)²/n via the profile likelihood.
- two normal samples with a common variance: the MLE of σ² pools both sums of squares over n + m.

### §3.5 — Família Exponencial e o Método de Máxima Verossimilhança (pp. 49–50)
**Subtopics:**
- in an exponential family the MLE solves E[T(X)] = T(X) (3.5.1), and E[T_j(X)] = T_j(X) in k dimensions (3.5.2).
- Hardy–Weinberg proportions: θ̂ = (2N₁ + N₂)/2n.
- bivariate normal MLEs recovered from the moment equations of the sufficient statistic.

### §3.6 — O Método dos Momentos (pp. 50–51)
**Subtopics:**
- method of moments: equate sample moments m_r to population moments μ_r, r = 1, …, k.
- taxi problem: N̂ = 2X̄ − 1, which is not a function of the sufficient statistic X(n).
- gamma(α, β): moment estimators α̂ = X̄²/σ̂², β̂ = X̄/σ̂², used as starting values for the numerical MLE.

### §3.7 — Estimadores Consistentes (p. 52)
**Subtopics:**
- consistency as convergence in probability, lim P(|θ̂ − θ| > ε) = 0 (Definition 3.7.1).
- Chebyshev's inequality shows X̄ is consistent for the mean.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (related, not assigned)

### §3.8 — Exercícios (pp. 52–55)
**Subtopics:**
- exercises 3.1–3.21: MLEs and their large-sample distributions, invariance, method of moments, Weibull and Gumbel-type numerical MLEs, consistency, and MLE versus least squares in simple regression. See [[bolfarine-exercises]].

## Ch. 4 — Introdução à Teoria das Decisões. Os Princípios Minimax e de Bayes
**Pages:** pp. 57–72

### §4.1 — Os Elementos Básicos (pp. 57–60)
**Subtopics:**
- elements of a decision problem: parameter space Θ, action space A, decision function d, and loss l(θ, a) (quadratic, absolute, and c(θ)|θ − a|^r).
- risk function R(θ, d) = E[l(θ, d(X))] (Definition 4.1.1), the "better than" ordering and inadmissibility (Definition 4.1.2).
- coin example with Θ = {1/3, 2/3}: risks of four decision rules (Table 4.1); d₄ is inadmissible.

### §4.2 — O Princípio Minimax (pp. 60–61)
**Subtopics:**
- minimax rule: minimize the maximum risk (Definition 4.2.1).
- coin example: d₁ is minimax; Poisson with loss (θ − a)²/θ: d(X) = X is minimax in the class {cX}.

### §4.3 — O Princípio de Bayes (pp. 61–63)
**Subtopics:**
- prior distribution π(θ) and Bayes risk r(π, d) = E_π[R(θ, d)] (Definition 4.3.1); Bayes decision rule (Definition 4.3.2).
- coin example: the Bayes rule depends on the prior weight p and need not be unique.
- Poisson with an Exp(1) prior: Bayes rule X/2 within the class {cX}.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]] (related, not assigned)

### §4.4 — Estimadores de Bayes com Perda Quadrática (pp. 63–70)
**Subtopics:**
- Theorem 4.4.1: under quadratic loss the Bayes estimator is the posterior mean E[θ|X] (Bayes estimator under quadratic loss); posterior π(θ|x) = f(x|θ)π(θ)/g(x), marginal g(x).
- Bayes estimators are not invariant, unlike MLEs.
- beta–Bernoulli conjugacy: posterior Beta(Σxᵢ + a, n − Σxᵢ + b), posterior mean (Σxᵢ + a)/(n + a + b); uniform prior gives (ΣXᵢ + 1)/(n + 2), with risk and Bayes risk 1/(6(n + 2)).
- gamma–Poisson conjugacy: posterior Gamma(Σxᵢ + a, n + b) and its risk.
- normal–normal conjugacy with known variance: the posterior mean is a convex combination of X̄ and the prior mean a; prior influence fades as n grows or as b → ∞.
- Theorem 4.4.2: the Bayes estimator depends on the data only through a sufficient statistic.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]] (related, not assigned)

### §4.5 — Exercícios (pp. 70–72)
**Subtopics:**
- exercises 4.1–4.12: risks, minimax and Bayes rules in restricted classes, conjugate posteriors (Pareto–uniform, gamma–exponential, gamma–Poisson) and Bayes estimators. See [[bolfarine-exercises]].

## Ch. 5 — Estimação por Intervalo
**Pages:** pp. 73–89

### §5.1 — Amostras de Populações Normais (pp. 73–75)
**Subtopics:**
- Theorem 5.1: for a normal sample, X̄ and S² are independent, (n − 1)S²/σ² ~ χ²_{n−1}, and √n(X̄ − μ)/S ~ t_{n−1}; proofs by moment generating functions.

### §5.2 — O Método da Quantidade Pivotal (pp. 75–80)
**Subtopics:**
- pivotal quantity Q(X; θ) whose distribution is free of θ (Definition 5.2.1), and inversion into a confidence interval with coefficient γ = 1 − α.
- exponential: 2θΣXᵢ ~ χ²_{2n} gives an exact interval; simulated data by the inverse-CDF method (Tables 5.1–5.2).
- uniform: X(n)/θ is pivotal; equal-tail interval and the frequentist reading of the confidence coefficient.

### §5.3 — Intervalos para Populações Normais (pp. 80–83)
**Subtopics:**
- §5.3.1 O caso de uma única amostra (pp. 80–81): z-interval for μ with σ² known, t-interval with σ² unknown, and χ² interval for σ².
- §5.3.2 Duas amostras independentes (pp. 82–83): interval for μ₁ − μ₂ with pooled variance S_p² (t_{n+m−2}), and the F-based interval for σ₁²/σ₂².

### §5.4 — Intervalos de Confiança Aproximados (pp. 83–85)
**Subtopics:**
- approximate pivots from the asymptotic normality of the MLE, with I_F(θ) replaced by I_F(θ̂) (5.4.1), and a delta-method pivot for g(θ) (5.4.2).
- Bernoulli: Wald interval for θ and for θ(1 − θ); exponential: approximate interval for θ, compared with the exact one.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (related, not assigned)

### §5.5 — Intervalos de Confiança Bayesianos (pp. 85–87)
**Subtopics:**
- Bayesian (credible) interval: posterior probability γ over [t₁, t₂] (Definition 5.5.1); the shortest one is the highest posterior density (HPD) interval.
- normal mean with a N(μ₀, 1) prior: symmetric HPD interval.
- uniform with a Pareto prior: equal-tail interval from the Pareto posterior, which is not HPD.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]] (related, not assigned)

### §5.6 — Exercícios (pp. 87–89)
**Subtopics:**
- exercises 5.1–5.14: pivotal quantities, normal-theory intervals, approximate MLE-based intervals, and Bayesian intervals for Poisson and gamma posteriors. See [[bolfarine-exercises]].

## Ch. 6 — Testes de Hipóteses
**Pages:** pp. 91–117

### §6.1 — Idéias Básicas (pp. 91–92)
**Subtopics:**
- informal motivation for testing (a jury trial, a vaccine trial) and the two possible errors.

### §6.2 — Formulação Estatística (pp. 92–94)
**Subtopics:**
- statistical hypothesis, simple versus composite hypotheses (Definition 6.2.1), and a test as a decision function with acceptance and critical regions (Definition 6.2.2).
- type I and type II error probabilities α and β as risks under 0–1 loss (Table 6.1); power π(θ₁) = 1 − β (Definition 6.2.3).
- normal-mean example: choosing the cutoff c for a level-0.05 test.

### §6.3 — Hipótese Nula Simples contra Alternativa Simples. Testes Mais Poderosos (pp. 94–100)
**Subtopics:**
- Lemma 6.3.1: the test minimizing aα + bβ rejects when L₁(x)/L₀(x) ≥ a/b.
- Neyman–Pearson lemma (Lemma 6.3.2): the likelihood-ratio critical region is most powerful at its level.
- most powerful tests for the normal mean (ΣXᵢ ≥ c), the normal variance with known mean (χ²), and Bernoulli θ (binomial cutoff, normal approximation).
- p-value ("nível descritivo") as the smallest level at which H₀ is rejected (Definition 6.3.1).

### §6.4 — Testes Uniformemente Mais Poderosos (pp. 100–103)
**Subtopics:**
- §6.4.1 Hipótese nula simples contra alternativa composta (pp. 100–102): uniformly most powerful (UMP) tests (Definition 6.4.1); one-sided normal and Bernoulli examples; no UMP test exists for a two-sided alternative; power function (Definition 6.4.2, Figure 6.1).
- §6.4.2 Hipóteses compostas (pp. 102–103): Theorem 6.4.1 — in an exponential family the one-sided UMP test for θ = θ₀ is also UMP for θ ≤ θ₀ (and symmetrically).

### §6.5 — Testes da Razão de Verossimilhanças Generalizada (pp. 103–114)
**Subtopics:**
- generalized likelihood ratio test (GLRT, "TRVG"): λ(x) = sup_{Θ₀} L / sup_Θ L, and the five-step recipe using the unrestricted and restricted MLEs.
- two-sided z-test and its power function (Figure 6.2); t-test for μ with σ² unknown; χ² test for σ²; a shifted-exponential location test.
- Theorem 6.5.1: −2 log λ(X) is asymptotically χ² with degrees of freedom equal to the difference in free parameters (Wilks); Poisson example.
- two-sample tests: pooled t-test for equal normal means, F-test for equal variances, asymptotic test for two Bernoulli proportions.
- multinomial (three-type) MLEs and the Hardy–Weinberg GLRT; Pearson chi-square statistic as its large-sample equivalent.
- duality between tests and confidence intervals.

### §6.6 — Testes Bayesianos (p. 114)
**Subtopics:**
- Bayesian test of a point null by checking whether θ₀ lies in the Bayesian (credible) interval; normal mean with a N(0, 1) prior.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]] (related, not assigned)

### §6.7 — Exercícios (pp. 115–117)
**Subtopics:**
- exercises 6.1–6.17: most powerful and UMP tests, power functions, GLRTs for one and two samples, multinomial goodness of fit, and the paired t-test. See [[bolfarine-exercises]].

## Referências (pp. 119–120)
**Subtopics:**
- seven references: Bickel & Doksum (1977), Bussab & Morettin (1987), DeGroot (1989), Feller (1976), James (1981), Lehmann (1986), Sen & Singer (1993).
