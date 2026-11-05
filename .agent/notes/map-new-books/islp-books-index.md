# James, Witten, Hastie, Tibshirani & Taylor, An Introduction to Statistical Learning with Applications in Python (ISLP), 2023
#book/islp
> Link: [[Livros/James, Witten, Hastie, Tibshirani, Taylor - An Introduction to Statistical Learning with Applications in Python (2023)|ISLP]]

> Page numbers are printed book pages (from the book's table of contents, checked against the running heads with pdftotext). First printing, July 5, 2023. The PDF drops the blank page before most chapter openers, so the PDF-to-printed offset drifts: 1-based PDF page − 11 (ch. 1), − 10 (ch. 2), − 9 (ch. 3–4), − 8 (ch. 5–7), − 7 (ch. 8–10), − 6 (ch. 11–13 and the index).

**Differences from ISLR 1e** (section numbers below are ISLP's):
- Ch. 2–3: same section numbers; page numbers shift down (e.g. §2.2 starts p. 27, not p. 29). The labs are rewritten in Python: §2.3 now has nine subsections (§2.3.1 Getting Started … §2.3.9), §3.6 adds §3.6.4 Multivariate Goodness of Fit and drops Writing Functions.
- Ch. 4: §4.3.5 becomes "Multinomial Logistic Regression" (baseline and softmax coding). §4.4 is renamed "Generative Models for Classification": the 1e §4.4.1 (Bayes' theorem) is folded into the §4.4 introduction, so LDA p = 1 is §4.4.1 (1e §4.4.2), LDA p > 1 is §4.4.2 (1e §4.4.3), QDA is §4.4.3 (1e §4.4.4), and §4.4.4 Naive Bayes is new. §4.5 splits into §4.5.1 An Analytical Comparison and §4.5.2 An Empirical Comparison. **§4.6 Generalized Linear Models (Poisson regression, Bikeshare data) is new.** The lab moves from §4.6 to §4.7 (adds Naive Bayes and Bikeshare linear/Poisson regression) and the exercises from §4.7 to §4.8.
- Ch. 5: same section numbers; in the lab, LOOCV and k-fold are merged into §5.3.2 Cross-Validation, so the bootstrap lab is §5.3.3 (1e §5.3.4).
- Ch. 6: the three labs (1e §6.5–6.7) are merged into one §6.5 Lab: Linear Models and Regularization Methods (§6.5.1–6.5.3), so the exercises move from 1e §6.8 to §6.6.
- Ch. 7: same section numbers; lab §7.8 is reorganised into four subsections; exercises remain §7.9.
- Ch. 8: §8.2 adds §8.2.4 Bayesian Additive Regression Trees and §8.2.5 Summary of Tree Ensemble Methods.
- New chapters: Ch. 10 Deep Learning, Ch. 11 Survival Analysis and Censored Data, Ch. 13 Multiple Testing. Unsupervised learning moves from 1e Ch. 10 to Ch. 12 (PCA 1e §10.2 → §12.2; new §12.3 Missing Values and Matrix Completion; clustering 1e §10.3 → §12.4).

## Ch. 1 — Introduction
**Pages:** pp. 1–13

## Ch. 2 — Statistical Learning
**Pages:** pp. 15–67

### §2.1 — What Is Statistical Learning? (pp. 15–27)
**Subtopics:**
- Model Y = f(X) + ε (2.1): statistical learning as estimating the systematic part f from data; ε is mean-zero error independent of X.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §2.1.1 — Why Estimate f? (pp. 17–20)
**Subtopics:**
- Prediction vs inference: prediction treats f̂ as a black box (2.2); inference asks which predictors matter and how.
- Reducible vs irreducible error (2.3): E(Y − Ŷ)² = [f(X) − f̂(X)]² + Var(ε); Var(ε) bounds achievable accuracy.

#### §2.1.2 — How Do We Estimate f? (pp. 20–23)
**Subtopics:**
- Parametric methods: assume a functional form, e.g. linear (2.4), and fit by least squares; risk of misspecification.
- Non-parametric methods: thin-plate splines need no form assumption but need many observations; overfitting the noise.

#### §2.1.3 — The Trade-Off Between Prediction Accuracy and Model Interpretability (pp. 23–25)
**Subtopics:**
- Flexibility vs interpretability: subset selection/lasso and least squares (interpretable, rigid) vs GAMs, trees, bagging, boosting, SVMs and deep learning (flexible, opaque); flexible is not always more accurate.

#### §2.1.4 — Supervised Versus Unsupervised Learning (pp. 25–27)
**Subtopics:**
- Supervised (response observed) vs unsupervised (no response; e.g. cluster analysis) vs semi-supervised settings.

#### §2.1.5 — Regression Versus Classification Problems (p. 27)
**Subtopics:**
- Quantitative vs qualitative responses; method choice depends on the response type more than on the predictor type.

### §2.2 — Assessing Model Accuracy (pp. 27–40)
**Subtopics:**
- No free lunch: no single method dominates on all data sets, so model selection is needed.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §2.2.1 — Measuring the Quality of Fit (pp. 28–31)
**Subtopics:**
- Training MSE (2.5) vs test MSE Ave(y₀ − f̂(x₀))² (2.6): training MSE falls monotonically with flexibility, test MSE is U-shaped; overfitting defined by this gap.
- Degrees of freedom as a summary of flexibility; cross-validation previewed as the way to estimate test MSE.

#### §2.2.2 — The Bias-Variance Trade-Off (pp. 31–34)
**Subtopics:**
- Bias–variance decomposition (2.7): E(y₀ − f̂(x₀))² = Var(f̂(x₀)) + [Bias(f̂(x₀))]² + Var(ε).
- More flexible methods have higher variance and lower bias; the U-shaped test MSE is the net effect.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §2.2.3 — The Classification Setting (pp. 34–40)
**Subtopics:**
- Training error rate (1/n) Σ I(yᵢ ≠ ŷᵢ) (2.8) and test error rate Ave(I(y₀ ≠ ŷ₀)) (2.9).
- Bayes classifier: assign to argmax_j Pr(Y = j | X = x₀) (2.10); Bayes decision boundary; Bayes error rate 1 − E[max_j Pr(Y = j | X)] (2.11) as the irreducible error.
- K-nearest neighbors (2.12): estimates conditional class probabilities by neighbor fractions; small K = flexible/low bias/high variance, large K = smooth; training vs test error against 1/K.

### §2.3 — Lab: Introduction to Python (pp. 40–63)
**Subtopics:**
- §2.3.1 Getting Started (p. 40): Ch2-statlearn-lab.ipynb, Jupyter.
- §2.3.2 Basic Commands (p. 40): print(), lists, strings.
- §2.3.3 Introduction to Numerical Python (p. 42): numpy arrays, shape, sum, np.corrcoef(), random draws with np.random.default_rng(), mean/var/std.
- §2.3.4 Graphics (p. 48): matplotlib subplots(), scatter, contour, imshow.
- §2.3.5 Sequences and Slice Notation (p. 51): np.linspace(), np.arange(), slices.
- §2.3.6 Indexing Data (p. 51): row/column indexing with lists, np.ix_(), Boolean indexing.
- §2.3.7 Loading Data (p. 55): pd.read_csv(), Auto data, missing values, dropna(), loc[] and iloc[].
- §2.3.8 For Loops (p. 59): loops, zip(), string formatting.
- §2.3.9 Additional Graphical and Numerical Summaries (pp. 61–63): boxplots, histograms, scatter_matrix(), describe().
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §2.4 — Exercises (pp. 63–67)
**Subtopics:**
- Conceptual 1–7 (flexibility, bias–variance curves, parametric vs non-parametric, KNN by hand); Applied 8–10 (College, Auto, Boston data, in pandas).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

## Ch. 3 — Linear Regression
**Pages:** pp. 69–134

### §3.1 — Simple Linear Regression (pp. 70–80)
**Subtopics:**
- Model Y ≈ β₀ + β₁X (3.1) fit by least squares on the Advertising data.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §3.1.1 — Estimating the Coefficients (pp. 71–72)
**Subtopics:**
- Least squares minimizes RSS (3.3); closed-form β̂₁ = Σ(xᵢ − x̄)(yᵢ − ȳ)/Σ(xᵢ − x̄)², β̂₀ = ȳ − β̂₁x̄ (3.4).

#### §3.1.2 — Assessing the Accuracy of the Coefficient Estimates (pp. 72–77)
**Subtopics:**
- Population regression line Y = β₀ + β₁X + ε (3.5) vs least squares line; unbiasedness by analogy with SE(μ̂)² = σ²/n (3.7).
- SE(β̂₀)², SE(β̂₁)² (3.8); approximate 95% CI β̂₁ ± 2·SE(β̂₁) (3.9); t-statistic t = (β̂₁ − 0)/SE(β̂₁) (3.14) and p-value for H₀: β₁ = 0.

#### §3.1.3 — Assessing the Accuracy of the Model (pp. 77–80)
**Subtopics:**
- Residual standard error RSE = √(RSS/(n − 2)) (3.15) as absolute lack of fit; R² = 1 − RSS/TSS (3.17); in simple regression R² = Cor(X, Y)² (3.18).

### §3.2 — Multiple Linear Regression (pp. 80–91)
**Subtopics:**
- Y = β₀ + β₁X₁ + ⋯ + β_pX_p + ε (3.19); βⱼ is the average effect of Xⱼ holding the other predictors fixed.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §3.2.1 — Estimating the Regression Coefficients (pp. 81–83)
**Subtopics:**
- Least squares minimizes RSS (3.22); multiple vs simple regression coefficients differ (newspaper's marginal association disappears once radio is controlled, via correlation among predictors).

#### §3.2.2 — Some Important Questions (pp. 83–91)
**Subtopics:**
- One: is at least one predictor useful? F = [(TSS − RSS)/p]/[RSS/(n − p − 1)] (3.23) for H₀: all βⱼ = 0; partial F (3.24) for a subset of q coefficients; why individual t-tests mislead when p is large.
- Two: deciding on important variables: forward, backward and mixed selection; Mallow's Cp, AIC, BIC, adjusted R² (backward selection impossible when p > n).
- Three: model fit via RSE (3.25) and R² (R² always rises when variables are added).
- Four: predictions: reducible error, model bias, confidence vs prediction intervals.

### §3.3 — Other Considerations in the Regression Model (pp. 91–109)
**Subtopics:**
- Qualitative predictors, relaxing the linear-additive assumptions, and diagnosing the six potential problems of a linear fit.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §3.3.1 — Qualitative Predictors (pp. 91–94)
**Subtopics:**
- Predictors with Only Two Levels: dummy variable (3.26)–(3.27), baseline level, 0/1 vs ±1 coding changes interpretation not fit.
- Qualitative Predictors with More than Two Levels: one fewer dummy than levels (3.28)–(3.30); F-test for the joint null; coding choices.

#### §3.3.2 — Extensions of the Linear Model (pp. 94–100)
**Subtopics:**
- Removing the Additive Assumption: interaction term X₁X₂ (3.31)–(3.33) (synergy in TV × radio); hierarchical principle; interactions with qualitative variables (3.34)–(3.35).
- Non-linear Relationships: polynomial regression mpg = β₀ + β₁·horsepower + β₂·horsepower² + ε (3.36) is still a linear model.
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §3.3.3 — Potential Problems (pp. 100–109)
**Subtopics:**
- 1. Non-linearity of the Data: residual plots against fitted values; transform predictors (log X, √X, X²).
- 2. Correlation of Error Terms: tracking in time series residuals; understated standard errors and narrow intervals.
- 3. Non-constant Variance of Error Terms: funnel-shaped residuals; log Y or √Y transforms; weighted least squares.
- 4. Outliers: studentized residuals above 3 in absolute value; effect on RSE and R².
- 5. High Leverage Points: leverage statistic hᵢ (3.37), average leverage (p + 1)/n; studentized residual vs leverage plot.
- 6. Collinearity: inflates SE(β̂ⱼ) and reduces power; correlation matrix misses multicollinearity; VIF(β̂ⱼ) = 1/(1 − R²_{Xⱼ|X₋ⱼ}), worrying above 5–10.
**Linked materials:**
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]]

### §3.4 — The Marketing Plan (pp. 109–111)

### §3.5 — Comparison of Linear Regression with K-Nearest Neighbors (pp. 111–116)
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §3.6 — Lab: Linear Regression (pp. 116–127)

### §3.7 — Exercises (pp. 127–134)
**Subtopics:**
- Conceptual 1–7 (p-values, KNN, interactions, training vs test RSS, regression through origin, R² = cor²); Applied 8–15 (Auto, Carseats, simulated data, collinearity, Boston).

## Ch. 4 — Classification
**Pages:** pp. 135–199

### §4.1 — An Overview of Classification (pp. 135–136)
**Subtopics:**
- Qualitative responses; Default data (default as a function of balance and income) as the running example.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §4.2 — Why Not Linear Regression? (pp. 136–138)
**Subtopics:**
- Coding a multi-class response as numbers imposes an arbitrary ordering; for binary 0/1 the linear probability fit estimates Pr(Y = 1 | X) but can fall outside [0, 1].
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §4.3 — Logistic Regression (pp. 138–146)
**Subtopics:**
- Models Pr(Y = 1 | X) directly, keeping predictions inside [0, 1].
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §4.3.1 — The Logistic Model (pp. 139–140)
**Subtopics:**
- Linear probability model p(X) = β₀ + β₁X (4.1) vs logistic function p(X) = e^{β₀+β₁X}/(1 + e^{β₀+β₁X}) (4.2); odds p/(1 − p) = e^{β₀+β₁X} (4.3) and log-odds (logit) linear in X (4.4); a one-unit change in X multiplies the odds by e^{β₁}.

#### §4.3.2 — Estimating the Regression Coefficients (pp. 140–141)
**Subtopics:**
- Maximum likelihood: ℓ(β₀, β₁) = ∏_{i: yᵢ=1} p(xᵢ) ∏_{i′: yᵢ′=0} (1 − p(xᵢ′)) (4.5); z-statistics and p-values for coefficients.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §4.3.3 — Making Predictions (pp. 141–142)
**Subtopics:**
- Plugging β̂ into the logistic function to get predicted probabilities; dummy predictors (student status).

#### §4.3.4 — Multiple Logistic Regression (pp. 142–144)
**Subtopics:**
- Log-odds linear in p predictors (4.6)–(4.7); confounding: the student coefficient is positive alone but negative once balance is controlled (Figure 4.3); predicted default 0.058 (student) vs 0.105 (non-student) (4.8)–(4.9).

#### §4.3.5 — Multinomial Logistic Regression (pp. 144–146)
**Subtopics:**
- K > 2 classes with baseline class K: Pr(Y = k | X = x) (4.10)–(4.11); log odds against the baseline are linear in x (4.12); fitted values do not depend on the baseline, coefficient interpretation does.
- Softmax coding treats all K classes symmetrically (4.13); log odds ratio between two classes (4.14); reappears in Chapter 10.

### §4.4 — Generative Models for Classification (pp. 146–161)
**Subtopics:**
- Model the class-conditional distribution of X, then flip it with Bayes' theorem: Pr(Y = k | X = x) = π_k f_k(x)/Σ_l π_l f_l(x) (4.15), with prior π_k and class density f_k.
- Why not just logistic regression: unstable estimates under strong class separation, better accuracy with small n and near-normal X, natural extension to K > 2.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Rules: [[rules/07_bayes|Bayesian inference]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §4.4.1 — Linear Discriminant Analysis for p = 1 (pp. 147–150)
**Subtopics:**
- Gaussian classes with common σ² (4.16)–(4.17); discriminant δ_k(x) = x·μ_k/σ² − μ_k²/(2σ²) + log π_k (4.18), linear in x; boundary x = (μ₁ + μ₂)/2 with equal priors (4.19).
- Plug-in estimates μ̂_k, pooled σ̂² (4.20), π̂_k = n_k/n (4.21) and the estimated discriminant (4.22).

#### §4.4.2 — Linear Discriminant Analysis for p > 1 (pp. 150–156)
**Subtopics:**
- Multivariate Gaussian density (4.23) with class-specific means and common covariance Σ; δ_k(x) = xᵀΣ⁻¹μ_k − ½μ_kᵀΣ⁻¹μ_k + log π_k (4.24); Bayes boundaries (4.25).
- Confusion matrix on the Default data (Table 4.4); trivial null classifier benchmark; sensitivity vs specificity; lowering the threshold from 0.5 (4.26) to 0.2 (4.27) trades overall error for fewer missed defaulters (Table 4.5).
- ROC curve and AUC (0.95 for LDA on Default) as threshold-free summaries; true/false positive rates, precision, power and Type I/II error terminology (Tables 4.6–4.7).

#### §4.4.3 — Quadratic Discriminant Analysis (pp. 156–158)
**Subtopics:**
- Class-specific covariance Σ_k gives a quadratic discriminant (4.28); LDA vs QDA as a bias–variance trade-off (Kp(p + 1)/2 covariance parameters).

#### §4.4.4 — Naive Bayes (pp. 158–161)
**Subtopics:**
- Predictors independent within each class: f_k(x) = f_k1(x₁) × ⋯ × f_kp(x_p) (4.29), posterior (4.30); one-dimensional densities via a Gaussian, histogram or kernel density, or class proportions for qualitative X.
- Biased but low-variance; on Default (n = 10,000, p = 2) it does not beat LDA (Tables 4.8–4.9); pays off when p is large or n is small.

### §4.5 — A Comparison of Classification Methods (pp. 161–167)
**Subtopics:**
- No method dominates; the choice depends on the true class distributions, n and p (bias–variance).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §4.5.1 — An Analytical Comparison (pp. 161–164)
**Subtopics:**
- Log posterior odds against baseline K (4.31): linear for LDA (4.32), quadratic for QDA (4.33), additive (GAM form) for naive Bayes (4.34).
- LDA is a special case of QDA; any linear-boundary classifier is a special case of naive Bayes; Gaussian naive Bayes is LDA with diagonal Σ; logistic regression has LDA's linear form but fits by maximum likelihood (better when normality fails).
- KNN: non-parametric, wins for highly non-linear boundaries only with large n and small p; QDA as the middle ground; no coefficient table.

#### §4.5.2 — An Empirical Comparison (pp. 164–167)
**Subtopics:**
- Six simulated scenarios (p = 2, 100 training sets each): linear Bayes boundaries (1–3) favour LDA/logistic, non-linear ones (4–6) favour QDA, naive Bayes or KNN-CV; KNN-1 can be worst; adding polynomial terms moves logistic/LDA towards QDA.

### §4.6 — Generalized Linear Models (pp. 167–173)
**Subtopics:**
- Responses that are neither qualitative nor continuous quantitative: counts (bikers per hour in the Bikeshare data).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]]

#### §4.6.1 — Linear Regression on the Bikeshare Data (pp. 167–169)
**Subtopics:**
- Least squares fit (Table 4.10, Figure 4.13): sensible month/hour patterns but 9.6% negative fitted values, variance rising with the mean (heteroscedasticity), and a continuous model for an integer response; log(Y) fixes some issues but complicates interpretation and fails at Y = 0.

#### §4.6.2 — Poisson Regression on the Bikeshare Data (pp. 169–172)
**Subtopics:**
- Poisson distribution Pr(Y = k) = e^{−λ}λᵏ/k! (4.35) with E(Y) = Var(Y) = λ; log link log λ(X) = β₀ + β₁X₁ + ⋯ + β_pX_p (4.36)–(4.37); maximum likelihood (4.38).
- Interpretation: a one-unit increase in Xⱼ multiplies E(Y) by exp(βⱼ) (cloudy vs clear: exp(−0.08) = 0.923); built-in mean–variance relationship; no negative fitted values (Table 4.11, Figure 4.15); overdispersion inflates the z-values (footnote 5).

#### §4.6.3 — Generalized Linear Models in Greater Generality (pp. 172–173)
**Subtopics:**
- Common recipe: Y from an exponential-family distribution (Gaussian, Bernoulli, Poisson; also exponential, Gamma, negative binomial) and a link η with η(E(Y | X)) = β₀ + Σ βⱼXⱼ (4.39)–(4.42); links μ, log(μ/(1 − μ)) and log μ.

### §4.7 — Lab: Logistic Regression, LDA, QDA, and KNN (pp. 173–193)
**Subtopics:**
- §4.7.1 The Stock Market Data (p. 173): Smarket data via ISLP load_data().
- §4.7.2 Logistic Regression (p. 174): sm.GLM(family=sm.families.Binomial()), predicted probabilities, confusion_table(), training vs held-out 2005 data.
- §4.7.3 Linear Discriminant Analysis (p. 179): sklearn LinearDiscriminantAnalysis, predict_proba() and posterior thresholds.
- §4.7.4 Quadratic Discriminant Analysis (p. 181): QuadraticDiscriminantAnalysis.
- §4.7.5 Naive Bayes (p. 182): GaussianNB.
- §4.7.6 K-Nearest Neighbors (p. 183): KNeighborsClassifier; Caravan insurance data, StandardScaler(), precision among predicted buyers, logistic threshold 0.25.
- §4.7.7 Linear and Poisson Regression on the Bikeshare Data (pp. 188–193): sm.OLS with sum-to-zero contrasts, sm.GLM(family=sm.families.Poisson()), comparison of fitted values.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §4.8 — Exercises (pp. 193–199)
**Subtopics:**
- Conceptual 1–12 (logit equivalence, LDA/QDA derivations, curse of dimensionality, odds, Bayes' theorem, analytical forms of (4.32)–(4.33), baseline vs softmax coding); Applied 13–16 (Weekly, Auto, Python functions, Boston), now including naive Bayes.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

## Ch. 5 — Resampling Methods
**Pages:** pp. 201–228

### §5.1 — Cross-Validation (pp. 202–212)
**Subtopics:**
- Model assessment (estimating test error) vs model selection (choosing flexibility) when no designated test set exists.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §5.1.1 — The Validation Set Approach (pp. 202–204)
**Subtopics:**
- Random split into training and validation halves (Auto: linear vs quadratic vs cubic mpg ~ horsepower); drawbacks: high variability across splits and overestimation of test error (fits on fewer observations).

#### §5.1.2 — Leave-One-Out Cross-Validation (pp. 204–206)
**Subtopics:**
- CV₍ₙ₎ = (1/n) Σ MSEᵢ (5.1); less bias, no split randomness; least-squares shortcut CV₍ₙ₎ = (1/n) Σ [(yᵢ − ŷᵢ)/(1 − hᵢ)]² (5.2) using leverage hᵢ.

#### §5.1.3 — k-Fold Cross-Validation (pp. 206–208)
**Subtopics:**
- CV₍k₎ = (1/k) Σ MSEᵢ over k folds (5.3), typically k = 5 or 10; LOOCV is the case k = n; cheaper than LOOCV; locating the minimum of the test MSE curve matters more than its level (Figure 5.6).

#### §5.1.4 — Bias-Variance Trade-Off for k-Fold Cross-Validation (pp. 208–209)
**Subtopics:**
- LOOCV is nearly unbiased but has higher variance (averaged fits are highly correlated); k = 5 or 10 balances the two.

#### §5.1.5 — Cross-Validation on Classification Problems (pp. 209–212)
**Subtopics:**
- CV error as the average misclassification indicator Errᵢ = I(yᵢ ≠ ŷᵢ) (5.4); choosing polynomial degree in logistic regression (5.5) and K in KNN; training error is a poor guide.

### §5.2 — The Bootstrap (pp. 212–215)
**Subtopics:**
- Portfolio example: α = (σ²_Y − σ_XY)/(σ²_X + σ²_Y − 2σ_XY) minimizes Var(αX + (1 − α)Y) (5.6), plug-in α̂ (5.7); "true" SE(α̂) ≈ 0.083 from 1,000 simulated data sets.
- Resampling with replacement from the observed data; bootstrap standard error SE_B(α̂) as the standard deviation of B replicates (5.8), here 0.087.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §5.3 — Lab: Cross-Validation and the Bootstrap (pp. 215–224)
**Subtopics:**
- §5.3.1 The Validation Set Approach (p. 216): train_test_split(), polynomial fits on Auto, evalMSE().
- §5.3.2 Cross-Validation (p. 217): sklearn_sm() wrapper, cross_validate() with cv = n (LOOCV), KFold(n_splits=10), ShuffleSplit() for repeated validation splits.
- §5.3.3 The Bootstrap (pp. 220–224): alpha_func() and boot_SE() on Portfolio (bootstrap SE(α̂) = 0.0912); bootstrap SEs of linear and quadratic regression coefficients vs sm.OLS formula SEs when model assumptions fail.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §5.4 — Exercises (pp. 224–228)
**Subtopics:**
- Conceptual 1–4 (α derivation, bootstrap inclusion probability, k-fold CV, prediction SD); Applied 5–9 (Default, Weekly, simulated data, Boston).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

## Ch. 6 — Linear Model Selection and Regularization
**Pages:** pp. 229–288

### §6.1 — Subset Selection (pp. 231–240)
**Subtopics:**
- Fit the linear model (6.1) on a subset of the p predictors chosen for prediction accuracy and interpretability.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §6.1.1 — Best Subset Selection (pp. 231–233)
**Subtopics:**
- Algorithm 6.1: best model of each size by RSS/R², then choose among M₀, …, M_p by validation error, Cp (AIC), BIC or adjusted R²; 2ᵖ models make it infeasible beyond p ≈ 40; deviance replaces RSS for logistic regression.

#### §6.1.2 — Stepwise Selection (pp. 233–235)
**Subtopics:**
- Forward stepwise (Algorithm 6.2, 1 + p(p + 1)/2 models, usable when p > n), backward stepwise (Algorithm 6.3, needs n > p), Hybrid Approaches; not guaranteed to find the best subset.

#### §6.1.3 — Choosing the Optimal Model (pp. 235–240)
**Subtopics:**
- Cp, AIC, BIC, and Adjusted R²: Cp = (1/n)(RSS + 2dσ̂²) (6.2), unbiased for test MSE; AIC proportional to Cp for Gaussian least squares; BIC = (1/n)(RSS + log(n)dσ̂²) (6.3) penalizes size more heavily; adjusted R² = 1 − [RSS/(n − d − 1)]/[TSS/(n − 1)] (6.4).
- Validation and Cross-Validation: direct test-error estimates with fewer assumptions; one-standard-error rule picks the smallest model within one SE of the minimum.

### §6.2 — Shrinkage Methods (pp. 240–253)
**Subtopics:**
- Fit all p predictors with a penalty that shrinks coefficients toward zero, trading a little bias for a large variance reduction.
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

#### §6.2.1 — Ridge Regression (pp. 240–244)
**Subtopics:**
- Minimize RSS + λ Σ βⱼ² (6.5) (ℓ₂ penalty, intercept unpenalized); λ = 0 gives least squares, λ → ∞ the null model; coefficient paths against λ and ‖β̂_λ^R‖₂/‖β̂‖₂.
- Not scale equivariant: standardize predictors first (6.6).
- Why Does Ridge Regression Improve Over Least Squares?: bias–variance trade-off; gains largest when least squares has high variance (p close to n); far cheaper than best subset.

#### §6.2.2 — The Lasso (pp. 244–252)
**Subtopics:**
- Minimize RSS + λ Σ |βⱼ| (6.7) (ℓ₁ penalty) sets some coefficients exactly to zero: sparse, interpretable models (variable selection).
- Another Formulation for Ridge Regression and the Lasso: constrained forms with budget s (6.8)–(6.9), link to best subset (6.10); The Variable Selection Property of the Lasso: diamond vs circle constraint regions and RSS ellipses (Figure 6.7).
- Comparing the Lasso and Ridge Regression: lasso wins when few predictors matter, ridge when many have similar effects; neither dominates, use CV.
- A Simple Special Case for Ridge Regression and the Lasso (n = p, X = I, least squares β̂ⱼ = yⱼ (6.11)): ridge shrinks proportionally β̂ⱼ = yⱼ/(1 + λ) (6.12), (6.14); lasso soft-thresholds by λ/2 (6.13), (6.15).
- Bayesian Interpretation of Ridge Regression and the Lasso: posterior mode under a Gaussian prior is ridge (also the posterior mean), under a double-exponential (Laplace) prior is the lasso (Figure 6.11).
**Linked materials:**
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

#### §6.2.3 — Selecting the Tuning Parameter (pp. 252–253)
**Subtopics:**
- Choose λ (or s) by cross-validation over a grid, then refit on all observations (Figures 6.12–6.13).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §6.3 — Dimension Reduction Methods (pp. 253–262)

### §6.4 — Considerations in High Dimensions (pp. 262–267)

### §6.5 — Lab: Linear Models and Regularization Methods (pp. 267–283)

### §6.6 — Exercises (pp. 283–288)
**Subtopics:**
- Conceptual 1–7 (subset vs stepwise nesting, lasso/ridge bias–variance, special case (6.12)–(6.15), Bayesian lasso/ridge derivation); Applied 8–11 (simulated stepwise/lasso, College, best subset on simulated data, Boston).

## Ch. 7 — Moving Beyond Linearity
**Pages:** pp. 289–329

### §7.1 — Polynomial Regression (pp. 290–292)
**Subtopics:**
- yᵢ = β₀ + β₁xᵢ + β₂xᵢ² + ⋯ + β_dxᵢᵈ + εᵢ (7.1) is a linear model in xᵢ, …, xᵢᵈ fit by least squares; d rarely above 3 or 4 because high-degree curves behave wildly, especially near the boundary of X.
- Pointwise standard error of f̂(x₀) (7.2) from the coefficient covariance matrix, Var[f̂(x₀)] = ℓ₀ᵀĈℓ₀ (footnote 1); ±2 SE bands as an approximate 95% interval (Wage vs age, degree 4).
- Polynomial logistic regression for Pr(wage > 250 | age) (7.3); wide intervals because only 79 of 3,000 are high earners.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §7.2 — Step Functions (pp. 292–293)

### §7.3 — Basis Functions (pp. 293–294)

### §7.4 — Regression Splines (pp. 294–300)

### §7.5 — Smoothing Splines (pp. 300–303)

### §7.6 — Local Regression (pp. 303–305)

### §7.7 — Generalized Additive Models (pp. 305–309)

### §7.8 — Lab: Non-Linear Modeling (pp. 309–325)
**Subtopics:**
- §7.8.1 Polynomial Regression and Step Functions (p. 310) is the Python lab for §7.1 (poly() fits, anova_lm() comparison of degrees, polynomial logistic regression with sm.GLM(family=sm.families.Binomial()) for wage > 250).
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §7.9 — Exercises (pp. 325–329)
**Subtopics:**
- Conceptual 1–5 (truncated power basis, penalized smoothing sketches, basis-function curves); Applied 6–12 (Wage polynomial degree and cuts by CV, Auto, Boston nox ~ dis with poly() and bs(), College GAM, backfitting).

## Ch. 8 — Tree-Based Methods
**Pages:** pp. 331–366

## Ch. 9 — Support Vector Machines
**Pages:** pp. 367–398

## Ch. 10 — Deep Learning
**Pages:** pp. 399–467

## Ch. 11 — Survival Analysis and Censored Data
**Pages:** pp. 469–502

## Ch. 12 — Unsupervised Learning
**Pages:** pp. 503–556

### §12.1 — The Challenge of Unsupervised Learning (pp. 503–504)

### §12.2 — Principal Components Analysis (pp. 504–515)
**Subtopics:**
- PCA finds a low-dimensional set of directions that capture as much of the variation in the n × p data as possible; used for visualization, data summary and as input to PCR (§6.3.1).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §12.2.1 — What Are Principal Components? (pp. 505–508)
**Subtopics:**
- First principal component Z₁ = φ₁₁X₁ + ⋯ + φ_p1X_p (12.1), scores zᵢ₁ (12.2) chosen to maximize sample variance subject to Σⱼ φⱼ₁² = 1 (12.3); later components (12.4) are uncorrelated with (orthogonal to) earlier ones; loadings via the eigen/singular value decomposition.
- USArrests example: first loading weights the three crime variables, second loads on UrbanPop; biplot of scores and loadings (Figure 12.1).

#### §12.2.2 — Another Interpretation of Principal Components (pp. 508–510)
**Subtopics:**
- Principal components span the M-dimensional subspace closest to the observations; xᵢⱼ ≈ Σₘ zᵢₘφⱼₘ (12.5) is the best rank-M approximation, solving the least squares problem (12.6) with minimum value (12.7).

#### §12.2.3 — The Proportion of Variance Explained (pp. 510–512)
**Subtopics:**
- Total variance Σⱼ (1/n)Σᵢ xᵢⱼ² (12.8), variance of the mth component (12.9), PVE of component m (12.10); decomposition (12.11) shows PVE equals the R² of the rank-M approximation; min(n − 1, p) components with PVEs summing to one.
- USArrests: first two components explain 62.0% and 24.7% (almost 87%); scree plot and cumulative PVE (Figure 12.3).

#### §12.2.4 — More on PCA (pp. 512–515)
**Subtopics:**
- Scaling the Variables: results depend on scale, so standardize to unit SD unless all variables share units (Assault dominates unscaled, Figure 12.4).
- Uniqueness of the Principal Components: loadings and scores are unique up to a sign flip.
- Deciding How Many Principal Components to Use: no single answer; eyeball the scree plot for an elbow; CV is available only when the scores feed a supervised method such as PCR.

#### §12.2.5 — Other Uses for Principal Components (p. 515)
**Subtopics:**
- Use the first M score vectors as features in regression, classification and clustering (less noisy than the full data).

### §12.3 — Missing Values and Matrix Completion (pp. 515–520)

### §12.4 — Clustering Methods (pp. 520–535)

### §12.5 — Lab: Unsupervised Learning (pp. 535–552)
**Subtopics:**
- §12.5.1 Principal Components Analysis (p. 535) is the Python lab for §12.2.

### §12.6 — Exercises (pp. 552–556)

## Ch. 13 — Multiple Testing
**Pages:** pp. 557–596
