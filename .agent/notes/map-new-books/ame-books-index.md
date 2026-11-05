# Izbicki & Mendonça, Aprendizado de Máquina: uma abordagem estatística, 1st ed. (2020)
#book/ame
> Link: [[Livros/Izbicki, Mendonça - Aprendizado de Máquina_ uma abordagem estatística (2020)|AME]]

> Page numbers are printed book pages (taken from the book's table of contents, checked against the page footers). PDF-to-printed offset is constant: printed page = 1-based PDF page − 18 (front matter i–xvi plus two cover leaves; printed p. 1 = PDF p. 19, p. 242 = PDF p. 260). The book is in Portuguese; code is in R. There are no end-of-chapter exercises.

## Ch. 1 — Introdução
**Pages:** pp. 3–25

### §1.1 — Notação e Suposições (pp. 4–5)
**Subtopics:**
- Regression function r(x) := E[Y | X = x] as the target; quantitative Y = regression (Part I), qualitative Y = classification (Part II).
- i.i.d. sample (X₁, Y₁), …, (Xₙ, Yₙ) ∼ (X, Y) assumed throughout (relaxed in §9.3); notation xᵢ,ⱼ for covariate j of observation i (Tabela 1.1).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.2 — Predição versus Inferência: Por que estimar r(x)? (pp. 5–8)
**Subtopics:**
- Examples: life expectancy vs GDP per capita (211 countries), galaxy redshift from images, Isomap face data, song release year (YearPredictionMSD).
- Inferential goal (which predictors matter, effect of changing one) vs predictive goal (build g: ℝᵈ → ℝ with g(xₙ₊₁) ≈ yₙ₊₁ on new i.i.d. data).
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.3 — As Duas Culturas (pp. 8–9)
**Subtopics:**
- Breiman (2001): data modeling culture (assume the model is true, test assumptions, interpret βᵢ) vs algorithmic modeling culture (prediction, no assumption the model is correct); the book takes the second view.
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.4 — A Função de Risco (pp. 9–12)
**Subtopics:**
- Quadratic prediction risk R_pred(g) = E[(Y − g(X))²] on a new observation; general risk = expected loss (absolute loss |Y − g(X)| as an alternative).
- Teorema 1: R_pred(g) = R_reg(g) + E[V[Y | X]], with R_reg(g) = E[(r(X) − g(X))²]; hence argmin_g R_pred = r(x), the regression function is the best predictor.
- Conditional risk (g fixed) vs expected risk (averaged over training samples) (Observação 1.3); law of large numbers links the average loss on new data to R(g).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]; [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.5 — Seleção de Modelos: Super e Sub-Ajuste (pp. 12–24)
**Subtopics:**
- Polynomial fits of degree p ∈ {1, 4, 50} to the life-expectancy data: underfitting (p = 1) vs overfitting (p = 50); model selection picks g ∈ G with low estimated risk.
- Interpolation need not imply overfitting (Belkin et al.; Observação 1.4).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §1.5.1 — Data Splitting e Validação Cruzada (pp. 14–21)
**Subtopics:**
- Training MSE EQM(g) = n⁻¹ Σ (Yᵢ − g(Xᵢ))² (Eq. 1.1) is over-optimistic; hold-out estimator R̂(g) on a random validation split (e.g., 70/30) is consistent (Eq. 1.2).
- LOOCV R̂(g) = n⁻¹ Σ (Yᵢ − g₋ᵢ(Xᵢ))² and k-fold CV over folds L₁, …, L_k (k = n recovers LOOCV); hold-out is consistent for the conditional risk, LOOCV is approximately unbiased for the expected risk (Observação 1.5).
- Training vs validation vs test: validation picks tuning parameters, test compares the winners; CLT confidence interval for the risk on the test set, R̂(g) ± 2√(σ̂²/m) (Eq. 1.3), guides the split size.
- Exemplo 1.6 (training vs validation MSE against p) and Exemplo 1.7: a misspecified quadratic beats the true quintic model (lower variance; risk 1.7 vs 22354.08 over 1000 replications).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §1.5.1.1 — Penalização: uma alternativa (pp. 21–22)
**Subtopics:**
- R(g) ≈ EQM(g) + P(g): AIC penalty P(g) = 2pσ̂²/n, BIC penalty P(g) = log(n)pσ̂²/n; AIC curve on the life-expectancy data mirrors the validation curve (Figura 1.9).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]; [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §1.5.2 — Balanço entre Viés e Variância (pp. 22–24)
**Subtopics:**
- Decomposition E[(Y − g(X))² | X = x] = V[Y | X = x] + (r(x) − E[g(x)])² + V[g(x)]: irreducible variance, squared bias, estimator variance.
- Many parameters = low bias / high variance, few = the reverse; predictive inference accepts bias for lower variance and risk (Figura 1.10).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]; [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.6 — Tuning Parameters (p. 24)
**Subtopics:**
- The polynomial degree p is a tuning parameter controlling the bias–variance balance; the book always chooses tuning parameters by cross-validation or data splitting.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.7 — Resumo (pp. 24–25)
**Subtopics:**
- Recap: inference vs prediction, two cultures, risk = bias² + variance + noise, risk estimation by CV/data splitting and by penalization.

## Ch. 2 — Métodos Paramétricos
**Pages:** pp. 27–31

### §2.1 — O Método dos Mínimos Quadrados (pp. 28–30)
**Subtopics:**
- Linear predictor g(x) = βᵀx with x₀ ≡ 1 (covariates may be transformations, e.g., xᵢ², xᵢxⱼ); least squares β̂ = argmin Σ (Yᵢ − β₀ − … − β_d x_{i,d})² (Eq. 2.2) with closed form β̂ = (XᵀX)⁻¹XᵀY (Eq. 2.3).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §2.1.1 — Mínimos Quadrados quando a Suposição de Linearidade Falha (pp. 29–30)
**Subtopics:**
- Best linear predictor (oracle) β* = argmin_β E[(Y − βᵀX)²] = Σ⁻¹α with Σ = E[XXᵀ] (Eq. 2.4).
- Teorema 2: β̂ →ᴾ β* and R(g_β̂) →ᴾ R(g_β*) even when r(x) is not linear (weak LLN plus Mann–Wald).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §2.1.2 — Regressão Linear no R (p. 30)
**Subtopics:**
- lm(resposta ~ ., data) and predict(ajuste, newdata) (Python port: statsmodels OLS / scikit-learn LinearRegression).

### §2.2 — Resumo (p. 31)
**Subtopics:**
- OLS converges to the best linear predictor; with many covariates it overfits, and for d > n XᵀX is not invertible, motivating Ch. 3.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

## Ch. 3 — Métodos Paramétricos em Altas Dimensões
**Pages:** pp. 33–52

### §3.1 — Busca pelo Melhor Subconjunto de Covariáveis (pp. 33–35)
**Subtopics:**
- L0-penalized least squares β̂_L0 = argmin Σ (yₖ − β₀ − Σ βᵢxₖ,ᵢ)² + λ Σ I(βᵢ ≠ 0) (Eq. 3.1); λ = 0 gives OLS, λ → ∞ gives (ȳ, 0); intercept not penalized.
- With λ = 2σ̂²/n the problem is AIC selection over all 2ᵈ models; trade more bias for less variance; computationally infeasible for large d (Figura 3.1).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §3.2 — Regressão Stepwise (pp. 35–37)
**Subtopics:**
- Forward stepwise: add one variable per step by lowest estimated risk (AIC or CV), then pick the best model; fits 1 + d(d + 1)/2 models instead of 2ᵈ.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §3.3 — Lasso (pp. 37–40)
**Subtopics:**
- Lasso (Tibshirani, 1996): β̂_L1,λ = argmin Σ (yₖ − β₀ − Σ βⱼxₖ,ⱼ)² + λ Σ |βⱼ| (Eq. 3.2); L1 norm as a smooth measure of complexity vs L0 (Tabela 3.1).
- λ = 0 gives OLS, large λ shrinks all βⱼ to 0 (low variance, high bias); λ chosen by cross-validation (Figura 3.3).
- Advantages: convex problem, whole path in λ computed fast (LARS, glmnet; Friedman et al., 2010); sparse solutions are easy to interpret.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]; [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

#### §3.3.1 — Garantias Teóricas (pp. 39–40)
**Subtopics:**
- Teorema 3 (Greenshtein & Ritov, 2004): for bounded data, with probability ≥ 1 − δ, the constrained lasso's excess risk over the sparse oracle β*_L (‖β‖₁ ≤ L) is at most √(16(L + 1)⁴B²/n · log(√2·d/δ)), i.e., of order (L + 1)²B√(log(d/δ)/n); smaller L = easier to reach the oracle but a worse oracle.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §3.4 — Regressão Ridge (pp. 40–41)
**Subtopics:**
- Ridge (Hoerl & Kennard, 1970): L2 penalty λ Σ βⱼ² (Eq. 3.3) with closed form β̂_L2,λ = (XᵀX + λI₀)⁻¹XᵀY, I₀ the identity with I₀(1, 1) = 0 (Eq. 3.4).
- Shrinkage without zeros: under XᵀX = I, β̂_ridge = β̂/(1 + λ) and V[β̂ᵢ,ridge] = V[β̂ᵢ]/(1 + λ)²; λ by cross-validation; kernel ridge regression in §4.6.3.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]; [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

### §3.5 — Formulação Alternativa (pp. 41–42)
**Subtopics:**
- Constrained forms: lasso ⇔ min RSS s.t. Σ |βⱼ| ≤ B (Eq. 3.5); best subset s.t. Σ I(βⱼ ≠ 0) ≤ B₁; ridge s.t. Σ βⱼ² ≤ B₂; lasso and AIC select variables, ridge does not.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §3.6 — Interpretação Bayesiana (pp. 42–43)
**Subtopics:**
- With Yᵢ | xᵢ, β ∼ N(βᵀxᵢ, σ²) independent and σ² known, ridge and lasso are posterior modes (MAP estimators).
- Gaussian prior β ∼ N(0, σ_β² I_d) gives ridge with λ = σ²/σ_β²; i.i.d. Laplace(0, τ_β) prior (τ_β a precision) gives lasso with λ = σ²τ_β.
- Tighter prior = larger λ = more shrinkage; choosing λ by CV equals choosing the prior with the best predictive power (refs. Bishop, 2006; Park & Casella, 2008, Bayesian lasso).
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]; [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

### §3.7 — Regressão ridge e lasso no R (p. 43)
**Subtopics:**
- cv.glmnet(x, y, alpha = 1) for the lasso, alpha = 0 for ridge (Python port: scikit-learn LassoCV / RidgeCV).

### §3.8 — Exemplos (pp. 43–51)
**Subtopics:**
- Exemplo 3.1: simulation with n = 500, 20 covariates, 5 active; OLS risk 14.63 vs best-subset AIC 0.30 (1 h 20 min), forward stepwise 0.30, ridge 0.33, lasso 0.25 selecting exactly x₁–x₅ (Tabela 3.2).
- Exemplo 3.2: prostate cancer (lpsa, 97 men, train column split); coefficient paths against λ for ridge and lasso (Figuras 3.4–3.5), validation MSE with standard errors (Tabela 3.5).
- Exemplo 3.3: Amazon Fine Food Reviews, sparse document-term matrix; lasso MSE 1.136 < ridge 1.205 ≪ OLS 7.675, lasso keeps 558 words (Tabela 3.6).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §3.9 — Resumo (pp. 51–52)
**Subtopics:**
- L0 (best subset/stepwise), L1 (lasso, sparse) and L2 (ridge, shrinkage) penalties all cut variance at the cost of bias; non-parametric methods do the reverse (Figura 3.8).

## Ch. 4 — Métodos Não Paramétricos
**Pages:** pp. 53–106

### §4.1 — Séries Ortogonais (pp. 53–56)
**Subtopics:**
- Expand r(x) in an orthonormal basis of L²([0, 1]) (Fourier, polynomial/Hermite) with βⱼ = E[Yψⱼ(X)]; unbiased β̂ⱼ = n⁻¹ Σ Yᵢψⱼ(Xᵢ) and truncation g(x) = Σ_{j≤J} β̂ⱼψⱼ(x) (Eq. 4.1), J the bias–variance tuning parameter; tensor-product bases for d > 1.

### §4.2 — Splines (pp. 56–57)
**Subtopics:**
- Piecewise polynomials of order k with continuous derivatives at knots t₁ < … < t_p; r(x) approximated by a linear combination of spline basis functions fitted by least squares.

### §4.3 — k Vizinhos Mais Próximos (pp. 57–59)
**Subtopics:**
- KNN regression g(x) = k⁻¹ Σ_{i∈N_x} yᵢ (Eq. 4.2), a local average; k is the bias–variance tuning parameter chosen by cross-validation.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §4.4 — Nadaraya-Watson (pp. 59–61)
**Subtopics:**
- Kernel-weighted average g(x) = Σ wᵢ(x)yᵢ with wᵢ(x) = K(x, xᵢ)/Σⱼ K(x, xⱼ); uniform, Gaussian, triangular and Epanechnikov kernels; bandwidth h tuned by CV.

### §4.5 — Regressão Polinomial Local (pp. 61–62)
**Subtopics:**
- Kernel-weighted least squares fit of a degree-p polynomial around each x (Nadaraya–Watson is p = 0; local linear is p = 1).

### §4.6 — Métodos baseados em RKHSs (pp. 62–74)
**Subtopics:**
- Penalized risk minimization argmin_{g∈H} Σ L(g(xₖ), yₖ) + P(g) over a reproducing kernel Hilbert space; §4.6.1 A matemática do RKHS (Mercer kernels, ‖g‖_{H_K}); §4.6.2 representer theorem g(x) = Σ αₖK(xₖ, x) (Teorema 6).
- §4.6.3 Exemplo 1: Kernel Ridge Regression (pp. 67–73): quadratic loss generalizes ridge, closed-form α = (K + λI)⁻¹y; smoothing splines as a special case; the kernel trick; efficient implementation.
- §4.6.4 Exemplo 2: Support Vector Regression Machine (pp. 73–74): ε-insensitive loss (|y − g(x)| − ε)₊, solved numerically (e1071::svm).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §4.7 — Modelos Aditivos (pp. 74–77)
**Subtopics:**
- g(x) = α + Σⱼ gⱼ(xⱼ) with smooth univariate gⱼ, identified by α = Ȳ and Σᵢ gⱼ(Xᵢ,ⱼ) = 0; fitted by backfitting; interpretability between linear and fully non-parametric models.

### §4.8 — Árvores de Regressão (pp. 77–82)
**Subtopics:**
- Recursive binary partitioning (nodes, leaves), leaf prediction = mean of the training responses (Eq. 4.19), splits by squared error (Eq. 4.20); grow a large tree then prune by validation risk (rpart).

### §4.9 — Bagging e Florestas Aleatórias (pp. 82–89)
**Subtopics:**
- Averaging two unbiased, uncorrelated, equal-variance predictors halves the variance term: E[(Y − ḡ(x))² | x] = V[Y | x] + ½V[gᵢ(x) | x] (Eq. 4.21).
- Bagging: grow B unpruned trees on B bootstrap samples (random draws with replacement of size n) and average g(x) = B⁻¹ Σ g_b(x); variable importance by mean RSS reduction of the splits on each covariate (varImpPlot).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §4.9.1 — Florestas Aleatórias (pp. 85–89)
**Subtopics:**
- Decorrelate the bagged trees by drawing m < d candidate covariates at each split (m ≈ d/3 as a rule of thumb, m = d is bagging); m tuned by CV (randomForest, CO2 data).

### §4.10 — Boosting (pp. 89–91)
**Subtopics:**
- Start from g ≡ 0 and repeatedly fit a shallow tree to the residuals, adding it scaled by the learning rate λ ∈ (0, 1); B, λ and tree size are tuning parameters.

### §4.11 — Redes Neurais Artificiais (pp. 91–99)
**Subtopics:**
- Feed-forward network with hidden layers and activation functions as a non-linear estimator of r(x); §4.11.1 Estimação: Backpropagation (gradient descent layer by layer on the MSE); §4.11.2 Deep Learning (stochastic gradient descent, GPUs, keras; Exemplo 4.3 bike sharing training vs validation risk by epoch).

### §4.12 — Exemplo (pp. 99–102)
**Subtopics:**
- Exemplo 4.4: Amazon reviews revisited with KNN, XGBoost and a pruned tree on validation MSE; XGBoost is best, comparable to lasso and ridge from Exemplo 3.3 (Tabelas 4.1–4.2).

### §4.13 — Um Pouco de Teoria (pp. 102–106)
**Subtopics:**
- §4.13.1 k-vizinhos Mais Próximos: for L-Lipschitz r, Teorema 7 bounds E[(r̂ₖ(X) − r(X))²] ≤ K(k/n)^{2/d} + σ²/k (bias vs variance), optimal k ≍ n^{2/(2+d)}.
- §4.13.2 Séries Ortogonais: with m integrable derivatives, Teorema 8 gives risk ≤ K₁J^{−2m} + K₂J/n, i.e., the minimax rate n^{−2m/(2m+1)} (n^{−2m/(2m+d)} in d dimensions).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §4.14 — Resumo (p. 106)
**Subtopics:**
- Non-parametric methods trade parametric rates n⁻¹ for slower rates n^{−α/(α+d)} in exchange for flexibility; worse as d grows (Ch. 5).

## Ch. 5 — Métodos Não Paramétricos em Altas Dimensões
**Pages:** pp. 107–117

### §5.1 — Taxas de convergência e a maldição da dimensionalidade (pp. 107–110)
**Subtopics:**
- Curse of dimensionality: minimax risk of order n^{−α/(α+d)}, so the sample size needed grows exponentially in d; §5.1.1 Esparsidade (r depends on few covariates) and §5.1.2 Redundâcia (X on a low-dimensional manifold) as escape assumptions.

### §5.2 — k Vizinhos Mais Próximos e Regressão Linear Local (pp. 110–111)
**Subtopics:**
- Both adapt automatically to the intrinsic dimension u of the data, with rate n^{−4/(4+u)} instead of n^{−4/(4+d)}.

### §5.3 — Support Vector Regression (p. 111)
**Subtopics:**
- SVR with a Gaussian kernel also performs well under redundancy.

### §5.4 — Séries Ortogonais (pp. 111–115)
**Subtopics:**
- §5.4.1 Bases espectrais: data-driven orthonormal basis from the eigenfunctions of a Mercer-kernel operator; §5.4.2 O estimador: spectral series g(x) = Σ_{j≤J} β̂ⱼψ̂ⱼ(x) with β̂ⱼ = n⁻¹ Σ Yᵢψ̂ⱼ(Xᵢ) (Lee & Izbicki, 2016).

### §5.5 — Florestas Aleatórias (p. 115)
**Subtopics:**
- Convergence rate depends only on the number of relevant covariates (Biau, 2012).

### §5.6 — SpAM - Modelos Aditivos Esparsos (pp. 115–116)
**Subtopics:**
- Additive model with lasso-type constraint Σ |βⱼ| ≤ L on the component weights (Ravikumar et al., 2009); wine data example (Figura 5.3).

### §5.7 — Resumo (pp. 116–117)
**Subtopics:**
- Sparsity and redundancy are the assumptions that make high-dimensional non-parametric regression feasible; several Ch. 4 methods adapt to them automatically.

## Ch. 6 — Outros Aspectos de Regressão
**Pages:** pp. 119–129

### §6.1 — Interpretabilidade (ExplainableML) (pp. 119–124)
**Subtopics:**
- Why interpretability matters (trust, insight, detecting selection bias); §6.1.1 LIME - Local Interpretable Model-agnostic Explanations (local weighted lasso around x*); §6.1.2 PDP e ICE (partial dependence hᵢ(x) = n⁻¹ Σⱼ g(…, x, …) and individual conditional expectation curves, preferably on held-out data).

### §6.2 — Estimação de Densidades Condicionais (pp. 124–127)
**Subtopics:**
- Estimating the full f(y | x) rather than E[Y | x]; FlexCode expands f(y | x) = Σ βᵢ(x)φᵢ(y) in an orthonormal basis and estimates each βᵢ(x) by regression (Izbicki & Lee, 2017).

### §6.3 — Inferência Conformal (pp. 127–129)
**Subtopics:**
- Distribution-free prediction bands with P(Yₙ₊₁ ∈ C(Xₙ₊₁)) ≥ 1 − α under i.i.d. data only; split conformal: fit r̂ on one half, compute split residuals |y − r̂(x)| on the other, cut at an order statistic.
- Conditional coverage is impossible without strong assumptions; CD-split and Dist-split (conditional-density scores) control it asymptotically (predictionBands package; Exemplo 6.3 bike sharing).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

## Ch. 7 — Introdução
**Pages:** pp. 133–139 (Parte II — Classificação, p. 131)

### §7.1 — Função de Risco (pp. 134–136)
**Subtopics:**
- 0-1 loss and classification risk R(g) := E[I(Y ≠ g(X))] = P(Y ≠ g(X)) (Eq. 7.1); the quadratic risk makes no sense for qualitative Y.
- Teorema 9: the Bayes classifier g(x) = argmax_d P(Y = d | x) minimizes the 0-1 risk; in the binary case g(x) = c₁ ⇔ P(Y = c₁ | x) ≥ 1/2 (other cut-offs in §9.1).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §7.2 — Estimação do Risco e Seleção de Modelos (pp. 136–137)
**Subtopics:**
- Hold-out estimate of the error rate R̂(g) = (n − s)⁻¹ Σ_{i>s} I(Yᵢ ≠ g(Xᵢ)) (Eq. 7.2); choose g ∈ G with the smallest estimated risk by data splitting or cross-validation.
- Teorema 10 (Hoeffding + union bound): for a finite class of N classifiers, with probability ≥ 1 − ε, |R(ĝ) − R(g*)| ≤ 2√(log(2N/ε)/(2(n − s))); more candidates = weaker guarantee, so the test set should compare only a few tuned winners.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §7.3 — Balanço entre Viés e Variância (pp. 137–138)
**Subtopics:**
- Excess risk R(g) − R* = T₁ + T₂ with T₁ = R(g) − R_or (variance analogue, large for rich G) and T₂ = R_or − R* (squared-bias analogue, oracle R_or = inf_{g∈G} R(g) vs Bayes risk R*).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §7.4 — Outras medidas de desempenho (pp. 138–139)
**Subtopics:**
- Rare-disease example: the trivial classifier g ≡ 0 has low 0-1 risk but is useless.
- Confusion matrix (VN, FN, FP, VP; Tabela 7.1); sensitivity/recall S = VP/(VP + FN), specificity E = VN/(VN + FP), PPV/precision VP/(VP + FP), NPV VN/(VN + FN), F1 = harmonic mean of S and PPV.
- Sensitivity estimates P(g(X) = 1 | Y = 1) and specificity P(g(X) = 0 | Y = 0); compute them on validation/test data, not training data; essential for imbalanced data.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

## Ch. 8 — Métodos de classificação
**Pages:** pp. 141–168

### §8.1 — Classificadores Plug-in (pp. 141–151)
**Subtopics:**
- Plug-in rule: estimate P(Y = c | x) for every class, then g(x) = argmax_c P̂(Y = c | x) (binary: g(x) = 1 ⇔ P̂(Y = 1 | x) > 1/2).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §8.1.1 — Métodos de regressão (p. 142)
**Subtopics:**
- P(Y = c | x) = E[I(Y = c) | x], so any Part I regression method (linear, lasso, trees, …) on Z = I(Y = c) gives a plug-in classifier; linear fits can leave [0, 1] (linear probability model).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §8.1.2 — Regressão logística (pp. 142–144)
**Subtopics:**
- Logistic model P(Y = 1 | x) = e^{β₀+Σβᵢxᵢ}/(1 + e^{β₀+Σβᵢxᵢ}), used as a working model rather than assumed true.
- Estimation by maximum (conditional) likelihood L = Π P(Yₖ = 1 | xₖ, β)^{yₖ}(1 − P(Yₖ = 1 | xₖ, β))^{1−yₖ}, maximized numerically (glm, family = binomial).
- Penalized (lasso/ridge) logistic regression via glmnet(…, family = "binomial") and cv.glmnet; multi-class via one logistic regression per class Z = I(Y = c).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]; [[Map/class-plan#Class 7: More econometric models|Class 7]]

#### §8.1.3 — Bayes Ingênuo (pp. 144–147)
**Subtopics:**
- Bayes' theorem P(Y = c | x) = f(x | Y = c)P(Y = c)/Σₛ f(x | Y = s)P(Y = s); naive Bayes assumes conditional independence f(x | Y = s) = Πⱼ f(xⱼ | Y = s).
- Gaussian components Xⱼ | Y = s ∼ N(μⱼ,ₛ, σ²ⱼ,ₛ) with MLE class means and variances; multinomial components for discrete X; compute in logs to avoid underflow (Observação 8.1); special case of Bayesian networks.
- Exemplo 8.1 (Spambase, n = 4601, 57 word frequencies): test risk linear 0.111, logistic 0.086, naive Bayes 0.188 (Tabela 8.1).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §8.1.4 — Análise Discriminante (pp. 147–151)
**Subtopics:**
- X | Y = c multivariate normal; plug the estimated class densities into the Bayes rule.
- §8.1.4.1 Análise Discriminante Linear (pp. 147–149): common covariance, X | Y = c ∼ N(μ_c, Σ); MLEs μ̂_c and pooled Σ̂; log-ratio of class densities is linear in x, so the boundary is a hyperplane aᵀx ≥ K′ (MASS::lda).
- §8.1.4.2 Análise Discriminante Quadrática (pp. 149–151): class-specific Σ_c gives a quadratic boundary; Exemplo 8.2 (simulated) where QDA beats LDA (MASS::qda).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §8.2 — Support Vector Machines (SVM) (pp. 151–156)
**Subtopics:**
- Maximal-margin hyperplane for separable data (support vectors), soft margin with slack εᵢ and budget C; kernel trick f(x) = β₀ + Σ_{k∈S} αₖK(x, xₖ); RKHS view with hinge loss (1 − y g(x))₊ (e1071::svm, tune).

### §8.3 — Árvores de Classificação (pp. 156–158)
**Subtopics:**
- Leaf prediction = mode (Eq. 8.5); splits by the Gini index Σ_R Σ_c p_{R,c}(1 − p_{R,c}) (worked hospital/tomograph example, Exemplo 8.3); pruning by validation error rate (rpart).

### §8.4 — Bagging e Florestas Aleatórias (pp. 158–159)
**Subtopics:**
- Majority vote g(x) = mode{g_b(x)} over bootstrap trees (randomForest, ranger).

### §8.5 — Boosting (pp. 159–161)
**Subtopics:**
- AdaBoost.M1: reweight misclassified points, classifier weight α_b = log((1 − err_b)/err_b), final g(x) = sign(Σ α_b g_b(x)) (gbm, distribution = "adaboost").

### §8.6 — Método dos k Vizinhos Mais Próximos (p. 161)
**Subtopics:**
- KNN classifier g(x) = mode of the labels of the k nearest neighbours (FNN::knn).

### §8.7 — Redes Neurais Artificiais (pp. 161–163)
**Subtopics:**
- One output per class with softmax activation; cross-entropy loss −n⁻¹ ΣΣ I(yₖ = c) log g_{β;c}(xₖ).

### §8.8 — Exemplos (pp. 163–168)
**Subtopics:**
- Exemplo 8.4: Amazon reviews (score 5 vs rest; 40,000 train / 10,000 validation); logistic MLE, ridge, lasso (cut-off = training share of class 1), tree, random forest, XGBoost compared by accuracy, sensitivity and specificity (Tabela 8.3; XGBoost best accuracy 81.7%, tree worst specificity 34.1%).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

## Ch. 9 — Outros Aspectos de Classificação
**Pages:** pp. 169–186

### §9.1 — Assimetria na Função de Perda, Conjuntos de Dados Desbalanceados e Outros Cortes (pp. 169–172)
**Subtopics:**
- With rare events and weak covariates the Bayes rule I(P(Y = 1 | x) ≥ 0.5) collapses to g ≡ 0; use cut-offs g(x) = I(P̂(Y = 1 | x) ≥ K).
- ROC curve: sensitivity against specificity across K, drawn on validation/test data (Figura 9.1); common choice maximizes sensitivity + specificity.
- Cost-weighted risk l₁P(error, Y = 0) + l₀P(error, Y = 1) is minimized by g(x) = I(P(Y = 1 | x) > l₁/(l₀ + l₁)); with l₀ = π₀, l₁ = π₁ the cut-off is the class prevalence P̂(Y = 1).
- Alternatives for non-probabilistic classifiers: observation weights, over/under-sampling; the root problem is unequal costs, not imbalance.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §9.2 — Classificação vs Estimação de Probabilidades (p. 172)
**Subtopics:**
- A good plug-in classifier only needs the sign of P̂ − C right, not P̂ ≈ P; when probabilities matter (ranking, conformal inference) tune with proper scores: cross-entropy (log-likelihood) or Brier score.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §9.3 — Dataset Shift e Viés de Seleção (pp. 172–177)
**Subtopics:**
- Labelled and target samples not identically distributed, often from selection bias (bright galaxies easier to label, Amazon vs Twitter domains).
- §9.3.1 Covariate Shift (pp. 173–176): Y | X equal in both sets; target risk E[L(g(X_L), Y_L)β(X_L)] with importance weights β(x) = f_U(x)/f_L(x) (Eq. 9.1), estimated by density ratios or by a logistic regression of the "labelled" indicator S on x; weighted risk estimation and weighted fitting (glmnet weights).
- §9.3.2 Prior Shift (pp. 176–177): X | Y equal, class prevalences differ (case–control studies); Saerens et al. (2002) reweighting of P(Y_L = 1 | x) by P(Y_U = i)/P(Y_L = i); estimating P(Y_U = 1) from a classifier's rates (Forman, 2006).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]; [[rules/02_causalidade_potential_outcomes|Potential outcomes & selection bias]]

### §9.4 — Combinando Classificadores (pp. 177–179)
**Subtopics:**
- Blending / stacked ensembling: meta-classifier fitted on held-out predictions (ensemble set); Exemplo 9.1 (spam) logistic stacking of LDA, L1-logistic, random forest and SVM, risk 0.061 vs best single 0.067 (Tabelas 9.1–9.2).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §9.5 — Teoria do Aprendizado Estatístico (pp. 179–186)
**Subtopics:**
- Empirical risk minimization ĝ = argmin_{g∈G} R_tr(g) and the oracle g* = argmin_{g∈G} R(g); bounding sup_g |R_tr(g) − R(g)| bounds R(ĝ) − R(g*) ≤ 2ε.
- Teorema 11 (VC): P(sup_f |P_n(f) − P(f)| > ε) ≤ 4s(F, 2n)e^{−nε²/8}; shattering number s(F, n), VC dimension, Sauer's lemma s(F, n) ≤ (en/d)^d; ERM is consistent iff the VC dimension is finite.
- Exemplo 9.5: VC theory justifies tuning-parameter choice by data splitting.
- §9.5.1 Prova do teorema VC (pp. 184–186): Hoeffding's inequality (Teorema 13, Corolário 1), symmetrization lemma (Lema 3), union bound over s(F, 2n) patterns.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §9.6 — Resumo (p. 186)
**Subtopics:**
- 0-1 risk plus sensitivity/specificity and cost-weighted risks; Bayes classifier motivates plug-in methods; tools for non-i.i.d. prediction settings.

## Ch. 10 — Redução de Dimensionalidade e Mudança de Representação
**Pages:** pp. 189–208 (Parte III — Aprendizado não supervisionado, p. 187)

### §10.1 — Componentes Principais (PCA - Principal Component Analysis) (pp. 190–198)
**Subtopics:**
- Principal components as variance-maximizing, mutually uncorrelated linear combinations Z₁ = φ₁₁X₁ + … + φ_d1X_d of centred covariates; eigen-decomposition XᵀX = UΣUᵀ, scores Z = XU.
- §10.1.1 Interpretação alternativa: escalonamento multidimensional (PCA preserves pairwise Euclidean distances best among linear maps; Zip Code digits, Exemplo 10.1); §10.1.2 Aplicação: compressão de imagens (reconstruction from the first m components).

### §10.2 — Kernel PCA (KPCA) (pp. 198–201)
**Subtopics:**
- Non-linear components via the kernel trick: eigenvectors of the Gram matrix instead of XᵀX.

### §10.3 — Projeções Aleatórias (pp. 201–202)
**Subtopics:**
- Random Gaussian projections zᵢ = Σ s_{i,k}xₖ/√m; Teorema 14 (Johnson–Lindenstrauss): m ≥ 32 log n/ε² preserves all pairwise distances within (1 ± ε) with high probability.

### §10.4 — Autoencoders (pp. 202–208)
**Subtopics:**
- Neural networks whose output reproduces the input through a narrow hidden layer, trained on reconstruction error; worked example with reconstruction error plots (Figura 10.10).

## Ch. 11 — Análise de Agrupamento
**Pages:** pp. 209–222

### §11.1 — K-Médias (pp. 210–215)
**Subtopics:**
- Minimize the within-cluster sum of squares Σₖ |Cₖ|⁻¹ Σ_{i,j∈Cₖ} d²(xᵢ, xⱼ) for a fixed K; Lloyd's algorithm as an iterative approximation without global guarantees.

### §11.2 — Agrupamento Espectral (pp. 215–219)
**Subtopics:**
- Diffusion maps: a Markov random walk on the data built from a Mercer kernel defines a diffusion distance that captures connectivity better than Euclidean distance; k-means run on the diffusion-map coordinates (leading eigenvectors) separates non-convex clusters that plain k-means misses (Figura 11.4).

### §11.3 — Métodos Hierárquicos (pp. 219–222)
**Subtopics:**
- Agglomerative merging of the closest clusters into a dendrogram (no K needed in advance); single, complete, average and centroid linkage (hclust, cutree, factoextra::fviz_dend).

## Ch. 12 — Regras de Associação
**Pages:** pp. 223–228

### Ch. 12 (no numbered sections) (pp. 223–228)
**Subtopics:**
- Market-basket rules A ⇒ B on binary purchase data; support of an itemset P(∩_{i∈S} Xᵢ = 1), Apriori algorithm (Agrawal et al., 1993) exploiting monotone support; confidence P̂(B | A) and lift P̂(B | A)/P̂(B) (arules, Groceries data).

## Ch. 13 — Sistemas de Recomendação
**Pages:** pp. 229–234

### §13.1 — Filtro Colaborativo Baseado no Usuário (pp. 230–231)
**Subtopics:**
- KNN over users: Pearson-correlation similarity on co-rated items, predict Rⱼ,ₗ as the mean rating of the k most similar users who rated item l.

### §13.2 — Filtro Colaborativo Baseado no Produto (p. 231)
**Subtopics:**
- Same idea over items: average of user j's ratings of the k items most similar to l.

### §13.3 — FunkSVD (pp. 231–232)
**Subtopics:**
- Latent-factor model Rⱼ,ₗ ≈ uⱼᵀvₗ fitted by stochastic gradient descent on the observed ratings.

### §13.4 — Seleção de Modelos (pp. 232–234)
**Subtopics:**
- Data splitting over users with hidden ratings; MSE, RMSE, MAE; top-N recommendation confusion matrix with accuracy, precision and recall (Tabela 13.2), compared on MovieLense (recommenderlab).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

## Apêndice A — Apêndice
**Pages:** pp. 237–242 (Parte IV — Apêndice, p. 235)

### §A.1 — Imagens (pp. 237–240)
**Subtopics:**
- Raster images as pixel matrices (binary, greyscale, RGB channels) turned into covariate vectors.

### §A.2 — Textos (pp. 240–241)
**Subtopics:**
- Bag-of-words representation and the document-term matrix (Tabela A.1) used in the Amazon examples.

### §A.3 — Matrizes esparsas (pp. 241–242)
**Subtopics:**
- Sparse (row, column, value) storage of mostly-zero matrices; glmnet accepts sparse input, lm does not.
