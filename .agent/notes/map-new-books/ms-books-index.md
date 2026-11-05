# Morettin & Singer, Estatística e Ciência de Dados (preliminary version, April 2021)
#book/morettin-singer
> Link: [[Livros/Morettin, Singer - Estatística e Ciência de Dados (versão preliminar, abril 2021)|Morettin & Singer]]

> Page numbers are printed book pages (checked against the running heads of the PDF text). PDF-to-printed offset: constant, 1-based PDF page − 10 = printed page (printed p. 1 = PDF p. 11; roman front matter on PDF pp. 1–10). Preliminary version: numbering may differ from the 2022 LTC print edition.

> Coverage notes: the book has no time-series chapter (only AR(1) errors and the Durbin–Watson test in §6.2) and no dedicated Bayesian chapter (the Bayes classifier in §8.3.1 and posterior/data-augmentation material in Appendices B–C). Cross-validation is introduced in §1.3 and §1.6.1 and formalized in Nota 1 of §8.6 (the cross-references in §1.3 and §8.1 say "Nota de Capítulo 2", a numbering slip); the bootstrap appears inside bagging (§10.3.1) and the Ch. 10 notes.

## Ch. 1 — Estatística, Ciência de Dados e Megadados
**Pages:** pp. 1–20

### §1.1 — Introdução (pp. 1–4)
**Subtopics:**
- Data Science as statistics plus computation (Tukey, Breiman, Donoho, Efron & Hastie); the sample mean (1.1) and its standard error (1.2) as an example of algorithm plus inference.

### §1.2 — Aprendizado com Estatística (p. 4)
**Subtopics:**
- Supervised learning (prediction of a numeric response, classification of a qualitative one) vs unsupervised learning (association, grouping, dimension reduction); statistical inference as the broader aim.
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.3 — Aprendizado automático (pp. 4–6)
**Subtopics:**
- Machine learning vs "artificial intelligence" (Jordan 2019's three senses of AI; Turing 1950; Dartmouth 1955); classical rule-based programming vs training on data.
- Training vs validation sets; repeated random splitting with averaged prediction error as cross-validation (points to Note 2 of Ch. 8); refit the chosen model on the full data; prediction goal differs from interpreting coefficients.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §1.4 — Uma cronologia do desenvolvimento da Estatística (pp. 6–8)
**Subtopics:**
- §1.4.1 Probabilidades (p. 7) and §1.4.2 Estatística (p. 7): from Bayes and Laplace to Fisher and Neyman–Pearson; logistic regression, GLMs (Nelder & Wedderburn 1970), GAMs, bootstrap (Efron), ridge (Hoerl & Kennard 1970), CART, LASSO (Tibshirani 1996).
- §1.4.3 Estatística e computação (p. 8): computing eras and the R/CRAN ecosystem.

### §1.5 — Notação e tipos de dados (pp. 8–10)
**Subtopics:**
- Data matrix X (n × p), response vector y, data pairs (xᵢ, yᵢ); regimes n ≫ p, p ≫ n, both large; high-dimensional data; structured vs unstructured big data.

### §1.6 — Paradigmas para o aprendizado com Estatística (pp. 10–15)
**Subtopics:**
- Framework for supervised and unsupervised learning used by the rest of the book.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### §1.6.1 — Aprendizado supervisionado (pp. 10–14)
**Subtopics:**
- Model yᵢ = f(xᵢ) + eᵢ (1.3) with E(eᵢ) = 0; reducible vs irreducible error, E(ŷᵢ − yᵢ)² = E[f(xᵢ) − f̂(xᵢ)]² + Var(eᵢ) (1.4).
- Parametric vs non-parametric estimation of f (kernels, local polynomials/lowess, splines, orthogonal bases); flexibility vs interpretability; overfitting.
- Training MSE (1.5), RMSE, and validation MSE (1.6) for model choice; cross-validation previewed (points to Note 1 of Ch. 8).
- Bias–variance decomposition E[y₀ − f̂(x₀)]² = Var[f̂(x₀)] + [Bias(f̂(x₀))]² + Var(e₀) (1.7); U-shaped validation error against model size.
- Classification: risk L(g) = P{g(X) ≠ Y}, training error rate (1.8) and validation error rate (1.9); Bayes classifier maximizing P(y = j | x = x₀) (1.10) and the Bayes error rate.
- K-nearest-neighbour estimate of the conditional class probabilities; choice of K.

#### §1.6.2 — Aprendizado não supervisionado (pp. 14–15)
**Subtopics:**
- Cluster analysis with Euclidean (and non-Euclidean) distances, divisive vs agglomerative; dimension reduction (principal and independent components) as preprocessing for regression.

### §1.7 — Este livro (pp. 15–17)
**Subtopics:**
- Data science as a multidisciplinary pipeline (question, data, organization, description, method, algorithm, presentation); chapter plan; R packages used (caret, MASS, mgcv, nlme, randomForest, xgboost, …).

### §1.8 — Conjuntos de dados (pp. 17–18)
**Subtopics:**
- Table 1.1: the data sets used in examples and exercises, downloadable as .xls files from the authors' site.

### §1.9 — Notas de capítulo (pp. 19–20)
**Subtopics:**
- Reproductions of the first page of Turing (1950) and of the 1955 Dartmouth AI proposal.

## Ch. 2 — Preparação dos dados
**Pages:** pp. 23–41

### §2.1 — Considerações preliminares (pp. 23–26)
**Subtopics:**
- Populations vs samples; observational, sample-survey and experimental studies; units of investigation and variables; explanatory vs response variables.

### §2.2 — Planilhas de dados (pp. 26–31)
**Subtopics:**
- Building a data spreadsheet: data dictionary (operational definitions, mnemonic labels, units/categories), one row per unit, wide vs long layout for longitudinal data.

### §2.3 — Construção de tabelas (pp. 31–33)
**Subtopics:**
- Rules for tables: few decimals, self-explanatory titles, totals, ordering, row vs column percentages.

### §2.4 — Construção de gráficos (pp. 33–34)
**Subtopics:**
- Rules for graphs: titles, axis labels with units, scales, axis breaks, legends, avoiding area comparisons and chartjunk.

### §2.5 — Notas de capítulo (pp. 34–38)
**Subtopics:**
- Notes 1–4: data warehouses; operational definition of variables; order of magnitude, precision and rounding; proportions and percentages.

### §2.6 — Exercícios (pp. 38–41)
**Subtopics:**
- 9 exercises on preparing data dictionaries and spreadsheets (morfina, esforco, cidades data).

## Ch. 3 — Análise de dados de uma variável
**Pages:** pp. 43–91

### §3.1 — Introdução (pp. 43–44)
**Subtopics:**
- Aims of univariate description: frequency distribution, typical values, location, dispersion, shape.

### §3.2 — Distribuições de frequências (pp. 44–54)
**Subtopics:**
- §3.2.1 Variáveis qualitativas (p. 46): absolute/relative frequency tables, bar and pie charts; §3.2.2 Variáveis quantitativas (p. 48): class grouping, histograms, stem-and-leaf and dot plots (FGV questionnaire, ceagfgv data).

### §3.3 — Medidas resumo (pp. 54–62)
**Subtopics:**
- §3.3.1 Medidas de posição (p. 54): mean, median, trimmed mean, quantiles; §3.3.2 Medidas de dispersão (p. 56): variance (unbiased S²), standard deviation, mean absolute deviation, interquartile range; §3.3.3 Medidas de forma (p. 59): Fisher–Pearson skewness and kurtosis coefficients, symmetry plots.

### §3.4 — Boxplots (pp. 62–64)
**Subtopics:**
- Boxplot construction from Q1, median, Q3 and whiskers at 1.5 × IQR; outliers; side-by-side comparison of distributions.

### §3.5 — Modelos probabilísticos (pp. 64–67)
**Subtopics:**
- Probability models linking sample and population; discrete and continuous distributions; histogram approximated by a density.

### §3.6 — Dados amostrais (pp. 67–68)
**Subtopics:**
- Simple random sample (i.i.d. draws); correlated data as one trajectory of a stochastic process.

### §3.7 — Gráficos QQ (pp. 68–73)
**Subtopics:**
- Empirical distribution function; normal QQ plots comparing sample and theoretical quantiles; chi-squared QQ plots for skewed data.

### §3.8 — Desvio padrão e erro padrão (pp. 73–76)
**Subtopics:**
- Sampling distribution of the mean: E(X̄) = µ, Var(X̄) = σ²/n, approximate normality (CLT, illustrated by simulation); standard deviation vs standard error.

### §3.9 — Intervalo de confiança (pp. 76–78)
**Subtopics:**
- Approximate 95% confidence intervals X̄ ± 1.96 S/√n for a mean and p̂ ± 1.96 √(p̂(1 − p̂)/n) for a proportion; margin of error and interpretation.

### §3.10 — Transformação de variáveis (pp. 78–80)
**Subtopics:**
- Box–Cox family of power transformations to symmetrize skewed data and stabilize variance (log, square root, cube root).

### §3.11 — Notas de capítulo (pp. 80–83)
**Subtopics:**
- Notes 1–6: continuous variables; histogram bin width (Freedman–Diaconis); definition of the histogram; an alternative estimator of the standard deviation; standardization; confidence bands for QQ plots.

### §3.12 — Exercícios (pp. 83–91)
**Subtopics:**
- 33 exercises on frequency tables, summary measures, boxplots, QQ plots and transformations.

## Ch. 4 — Análise de dados de duas variáveis
**Pages:** pp. 93–144

### §4.1 — Introdução (pp. 93–94)
**Subtopics:**
- Association between two variables; three cases (qualitative–qualitative, quantitative–quantitative, mixed); explanatory vs response roles.

### §4.2 — Duas variáveis qualitativas (pp. 94–107)
**Subtopics:**
- Contingency tables, Pearson's chi-squared statistic and contingency coefficients; attributable risk, relative risk and odds ratio in prospective vs retrospective studies.
- Diagnostic tests (pp. 104–107): sensitivity, specificity, false positives/negatives, positive and negative predictive values and accuracy from the 2 × 2 table; predictive values depend on prevalence.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §4.3 — Duas variáveis quantitativas (pp. 107–119)
**Subtopics:**
- Scatter plots, covariance, Pearson and Spearman correlation; profile plots; agreement between observers with QQ plots and Tukey mean–difference (Bland–Altman) plots.

### §4.4 — Uma variável qualitativa e outra quantitativa (pp. 119–126)
**Subtopics:**
- Comparing distributions across groups with side-by-side boxplots and summary measures; one-way ANOVA model as a preview of regression.

### §4.5 — Notas de capítulo (pp. 126–135)
**Subtopics:**
- Notes 1–8: conditional probability and odds ratios; measures of dependence; linear dependence; robust dependence measures; PP plots; "significant" differences; confidence intervals for relative risk, odds ratio and sensitivity; a naive interpretation of the p-value.

### §4.6 — Exercícios (pp. 135–144)
**Subtopics:**
- 28 exercises on contingency tables, odds ratios, correlation, Bland–Altman plots and diagnostic-test characteristics.

## Ch. 5 — Análise de dados de várias variáveis
**Pages:** pp. 145–180

### §5.1 — Introdução (pp. 145–146)
**Subtopics:**
- Multivariate data matrices and joint distributions of p variables.

### §5.2 — Gráficos para três variáveis (pp. 146–159)
**Subtopics:**
- Draftsman's display (scatter-plot matrix with correlations), symbolic scatter plots, lowess-smoothed panels (ggplot2); main effects and interaction in two-factor designs with mean-profile plots and two-way ANOVA (pp. 153–159).

### §5.3 — Gráficos para quatro ou mais variáveis (pp. 159–160)
**Subtopics:**
- Draftsman's displays for four or more variables (tree-bark element concentrations).

### §5.4 — Medidas resumo multivariadas (pp. 160–161)
**Subtopics:**
- Mean vector, covariance and correlation matrices of a data matrix.

### §5.5 — Tabelas de contingência de múltiplas entradas (pp. 161–164)
**Subtopics:**
- Three-way contingency tables; joint, marginal and conditional independence; stratified odds ratios combined by Mantel–Haenszel.

### §5.6 — Notas de capítulo (pp. 164–175)
**Subtopics:**
- Notes 1–4: matrix notation for multivariate summaries; lowess smoothing; mean-deviation parametrization of ANOVA models; the Mantel–Haenszel statistic.

### §5.7 — Exercícios (pp. 175–180)
**Subtopics:**
- 11 exercises on multivariate graphs, interaction plots and multi-way tables.

## Ch. 6 — Análise de Regressão
**Pages:** pp. 181–242

> Ch. 6 has no numbered subsections; its regression results are split between the sections and the numbered chapter notes of §6.6, which are indexed below as subsections (note titles verbatim).

### §6.1 — Introdução (pp. 181–184)
**Subtopics:**
- Simple linear regression yᵢ = α + βxᵢ + eᵢ (6.1) with E(eᵢ) = 0 as a model for E(y | x); centring the regressor (6.2) to make α interpretable.
- "Linear" means linear in the parameters: (6.3) is non-linear, the quadratic (6.4) is a linear (polynomial) model.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §6.2 — Regressão linear simples (pp. 184–203)
**Subtopics:**
- Least squares Q(α, β) (6.5); closed-form β̂ (6.6) and α̂ = ȳ − β̂x̄ (6.7); unbiased S² = SQRes/(n − 2) (6.8); fitted values and residuals; R² = SQReg/SQTot; reading lm() output.
- Residual plots and standardized (studentized) residuals eᵢ* = êᵢ/(S√(1 − hᵢᵢ)) (6.9) with leverage hᵢᵢ = 1/n + (xᵢ − x̄)²/Σ(xᵢ − x̄)²; heteroscedasticity (CO data, polynomial fit); outliers (wind data); influential/high-leverage points and Cook's distance plots.
- QQ plots of residuals (t with n − 2 df vs normal quantiles); large-sample normality of β̂ without normal errors.
- Autocorrelated errors in a growth curve (6.10) with AR(1) errors eₜ = ρeₜ₋₁ + uₜ (6.11); Durbin–Watson statistic D (6.12) ≈ 2 − 2r₁ (6.13); remedies: generalized least squares or time-series methods.
- Multiplicative model yᵢ = βxᵢ^γ eᵢ (6.14) linearized by logs (6.15)–(6.17); t-test of H₀: γ = 1 and the reduced through-origin model (6.18)–(6.20) (dental plaque data).
**Linked materials:**
- Rules: [[rules/04_arima_raiz_unitaria|ARIMA & unit roots]] (residual autocorrelation and Durbin–Watson only)
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]] (heteroscedastic and AR(1) errors, GLS)
- Class: [[Map/class-plan#Class 8: Univariate time series|Class 8]] (AR(1) errors in regression only)

### §6.3 — Regressão linear múltipla (pp. 203–215)
**Subtopics:**
- Model (6.21), residuals (6.22), matrix form y = Xβ + e (6.23); least squares Q(β) = e′e (6.25) and β̂ = (X′X)⁻¹X′y (6.26); E(β̂) = β, Var(β̂) = σ²(X′X)⁻¹; S² = SSR/[n − (p + 1)]; normal and CLT-based inference.
- Treadmill example VO₂ ~ IMC + carga (6.24): coefficient interpretation "holding the other regressor fixed", residual plots vs each regressor and fitted values, Cook's distance cut-off 4/n, refit without influential points.
- Confidence interval for E(y | x₀) via x₀′(X′X)⁻¹x₀ vs prediction interval adding S² (R code).
- Collinearity (production data, r = 0.93): a "wrong-sign" coefficient that is not significant; R² always increases with regressors, adjusted R² penalizes; added-variable (partial regression) plot whose slope equals the multiple-regression coefficient (Frisch–Waugh logic).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §6.4 — Regressão para dados longitudinais (pp. 215–218)
**Subtopics:**
- Repeated weights of calves: pooled regression (6.27) vs linear mixed model with random intercept yᵢⱼ = α + β(xⱼ − 12) + aᵢ + eᵢⱼ (6.28); intra-unit correlation σₐ²/(σₐ² + σ²); same point estimates, smaller standard errors; profile and draftsman's plots.
**Linked materials:**
- Rules: [[rules/03_painel_did|Panel data & DiD]] (random-intercept model only)
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]] (hierarchical / mixed linear model)

### §6.5 — Regressão logística (pp. 218–224)
**Subtopics:**
- Binary response: logit model log[P(Y = 1 | x)/P(Y = 0 | x)] = α + βx (6.29) and logistic form (6.30); α as baseline log-odds, β as log odds ratio per unit of x.
- Maximum likelihood: likelihood ∏ p(xᵢ)^{yᵢ}[1 − p(xᵢ)]^{1−yᵢ}, score equations with no closed form, Newton–Raphson / Fisher scoring; glm(family = binomial) output (deviance, AIC); CIs for odds and odds ratios by exponentiating Wald limits (delta method for their SEs).
- Predicted probabilities (6.31) and classification by a threshold (0.7 vs default 0.5) with a confusion table and proportion correctly classified.
- Odds ratios are invariant to prospective vs retrospective sampling; grouped categorical data (6.32) fitted by generalized least squares (coronary-lesion data, Tables 6.11–6.13); multinomial (polytomous) logistic regression mentioned but not covered.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]]

### §6.6 — Notas de capítulo (pp. 224–234)
**Subtopics:**
- Nine technical notes backing §6.2–6.5 (inference, prediction, R², influence, delta method, logistic goodness of fit, resistant and basis-function regression).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### Nota 1 — Inferência baseada em modelos de regressão linear simples (pp. 224–225)
**Subtopics:**
- β̂ = Σwᵢyᵢ is linear in y; unbiasedness, Var(α̂), Var(β̂), Cov(α̂, β̂); t statistics with n − 2 df under normality; Gauss–Markov theorem (BLUE without normality); asymptotic normality via the CLT; robust estimators for heavy tails.

#### Nota 2 — Estimação e previsão sob modelos de regressão linear simples (p. 226)
**Subtopics:**
- Var(ŷ₀) = σ²[1/n + (x₀ − x̄)²/Σ(xᵢ − x̄)²]; confidence interval for E(Y | X = x₀) vs prediction interval for a new Y₀ (adds σ²); CI width → 0 while PI width → 2 × 1.96σ as n grows.

#### Nota 3 — Coeficiente de determinação (pp. 226–228)
**Subtopics:**
- Decomposition SQTot = SQRes + SQReg; SQReg = β̂²Σ(xᵢ − x̄)²; R² = SQReg/SQTot; adjusted R² = 1 − [SQRes/(n − p − 1)]/[SQTot/(n − 1)].

#### Nota 4 — Distância de Cook (p. 228)
**Subtopics:**
- Dᵢ = (ŷ − ŷ₍₋ᵢ₎)′(ŷ − ŷ₍₋ᵢ₎)/[(p + 1)S²] and its closed form in terms of eᵢ² and hᵢᵢ without refitting.

#### Nota 5 — Influência local e alavancagem (pp. 229–230)
**Subtopics:**
- Effect of a perturbation Δyⱼ on β̂ (6.33) and α̂ (6.34); leverage hⱼⱼ as the effect of Δyⱼ on ŷⱼ, growing with |xⱼ − x̄|.

#### Nota 6 — Método Delta (p. 230)
**Subtopics:**
- Var[g(β̂)] ≈ [g′(β)]²σ²_β̂ and the multivariate gradient form; used for SEs of exp(α̂), exp(β̂).

#### Nota 7 — Análise do ajuste de modelos de regressão logística (pp. 230–232)
**Subtopics:**
- Covariate patterns; Pearson residuals and Pearson statistic Q_P ~ χ²_{M−(p+1)}; Hosmer–Lemeshow statistic C with g = 10 risk-decile groups ~ χ²_{g−2}; deviance residuals.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]]

#### Nota 8 — Regressão resistente (pp. 232–233)
**Subtopics:**
- Median-based resistant line from three groups (left, centre, right): b₀ = (y_D − y_E)/(x_D − x_E), a₀ averaged; Example 6.11 vs least squares on the wind data.

#### Nota 9 — Formulação geral do modelo de regressão (pp. 233–234)
**Subtopics:**
- yᵢ = f(xᵢ, β) + eᵢ (6.35) with basis expansions f(x, β) = Σβⱼφⱼ(x): polynomials, splines, Gaussian, sigmoid, Fourier, wavelets; links to regularization (Ch. 11) and neural networks (Ch. 14).

### §6.7 — Exercícios (pp. 234–242)
**Subtopics:**
- 22 exercises: least squares derivations and diagnostics (1–17), logistic regression and odds ratios (18–22). The text of §6.5 cites "Exercício 20/21" for results that are Exercises 19/20 in the list (preliminary-version numbering slip).

## Ch. 7 — Análise de Sobrevivência
**Pages:** pp. 243–260

### §7.1 — Introdução (pp. 243–247)
**Subtopics:**
- Time-to-event data with right censoring, response pair (T, δ); survival function S(t), hazard function and cumulative hazard; exponential, Weibull and lognormal hazard shapes.

### §7.2 — Estimação da função de sobrevivência (pp. 247–253)
**Subtopics:**
- Kaplan–Meier (product-limit) estimator from numbers at risk and failures; mean survival as the area under the curve; median survival time; survfit()/ggsurvplot() examples (Examples 7.1–7.3).

### §7.3 — Comparação de curvas de sobrevivência (pp. 253–254)
**Subtopics:**
- Log-rank test: hypergeometric expected failures and variances at each failure time, approximate χ²₁ statistic (survdiff()).

### §7.4 — Regressão para dados de sobrevivência (pp. 254–256)
**Subtopics:**
- Parametric accelerated failure time models log T = α + x′β + σe (exponential, Weibull, lognormal; survreg()); Cox proportional hazards model and checking proportionality (coxph(), cox.zph()).
**Linked materials:**
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]] (duration models)

### §7.5 — Notas de capítulo (p. 256)
**Subtopics:**
- Notes 1–2: types of censoring (right, left, interval); alternatives when hazards are not proportional.

### §7.6 — Exercícios (pp. 256–260)
**Subtopics:**
- 6 exercises on coding censored data, Kaplan–Meier curves, log-rank tests and Cox regression.

## Ch. 8 — Classificação por meio de técnicas clássicas
**Pages:** pp. 263–290

### §8.1 — Introdução (pp. 263–264)
**Subtopics:**
- Classifier g: ℝᵖ → {−1, 1}, risk L(g) = P{g(X) ≠ Y} and training error rate (8.1); validation (test) error rate; refit the chosen classifier on training + validation data; cross-validation when only one data set exists.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §8.2 — Classificação por regressão logística (pp. 264–272)
**Subtopics:**
- Logit model for TMJ disc displacement (8.2) with a centred predictor: ML estimates, CIs for odds and odds ratios, predicted probability θ̂.
- Cut-off choice: 2 × 2 decision table (Table 8.2), sensitivity n₁₁/(n₁₁ + n₂₁) and specificity n₂₂/(n₁₂ + n₂₂); ROC curve (pROC) and the cut-off closest to the top-left corner; accuracy, false-positive and false-negative rates.
- Two predictors (8.3): marginal significance and correlated predictors ("confounding").
- Machine-learning comparison of four logistic models by 5-fold CV repeated 5 times (VC5/5) and LOOCV accuracy with caret (trainControl/train); Cohen's kappa; set.seed for reproducible splits (Table 8.6).
- Why multinomial logistic regression is less used than LDA for K > 2 (instability with well-separated classes).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §8.3 — Análise discriminante linear (pp. 272–282)
**Subtopics:**
- Classification into K ≥ 2 classes under Bayesian (known densities) and frequentist (Fisher) views.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

#### §8.3.1 — Classificador de Bayes (pp. 272–280)
**Subtopics:**
- Posterior class probabilities pₖ(x) = πₖfₖ(x)/Σπₗfₗ(x) (8.4); misclassification probabilities (8.5) and expected misclassification cost (8.6); Bayes rule maximizes πₖfₖ(x) (8.8), likelihood-ratio form for K = 2 (8.9).
- Gaussian classes with common Σ: linear discriminant (8.11), δₖ(x) = µₖ′Σ⁻¹x − ½µₖ′Σ⁻¹µₖ + log πₖ (8.12), p = 1 case (8.13)–(8.14), Bayes boundaries (8.15); plug-in estimates π̂ₖ = nₖ/n, class means, pooled S (8.17); Fisher's linear discriminant function (8.18).
- Examples: two normals with misclassification probability 0.159 (Ex. 8.2); lda() on inibina (Ex. 8.3), 70/30 train–validation split on disc data (Ex. 8.4, 9.4% error), three facial types with posterior probabilities and "proportion of trace" (Ex. 8.5).
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]] (Bayes' theorem for class posteriors only)

#### §8.3.2 — Classificador linear de Fisher (pp. 280–282)
**Subtopics:**
- Choose W = d′x maximizing (d′δ)²/(d′Σd) (8.21) ⇒ d = Σ⁻¹(µ₁ − µ₂) (8.22)–(8.23); Mahalanobis distance; midpoint threshold (8.24)–(8.25); equivalent to Bayes LDA with equal priors (Ex. 8.6).

### §8.4 — Classificador do vizinho mais próximo (pp. 282–284)
**Subtopics:**
- Bayes classifier and Bayes error rate 1 − E[maxⱼ P(Y = j | X)]; KNN estimate (8.27); choice of K = 1…5 by LOOCV with caret (Ex. 8.7); confusionMatrix output: accuracy CI, no-information rate, kappa, McNemar p-value, sensitivity, specificity, PPV, NPV, balanced accuracy.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

### §8.5 — Algumas extensões (pp. 284–285)
**Subtopics:**
- Quadratic discriminant analysis with class-specific Σₖ (8.28): more parameters, lower bias and higher variance than LDA; regularized discriminant analysis (Friedman 1989) shrinking Σₖ toward the pooled matrix and the mean eigenvalue (8.29)–(8.30), λ and γ chosen by LOOCV; qda(), rda(); LDA vs QDA accuracy on the disc data (Ex. 8.8).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §8.6 — Notas de capítulo (pp. 285–288)
**Subtopics:**
- Three notes on model assessment: cross-validation, McNemar's test, comparison of classifiers.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### Nota 1 — Validação cruzada (pp. 285–287)
**Subtopics:**
- Prediction error E(y₀ − ŷ)²; in-sample residual MSE is optimistic; LOOCV (Efron & Tibshirani 1993) MSE₍₋ᵢ₎ (8.31) and its leverage shortcut Σ[(yᵢ − ŷᵢ)/(1 − hᵢ)]²/n (8.32); k-fold CV (k = 5 or 10) averaging fold MSEs (8.33); validation error rate for classifiers (8.34).

#### Nota 2 — Teste de McNemar (pp. 287–288)
**Subtopics:**
- Marginal homogeneity in a paired 2 × 2 table, M = (n₁₂ − n₂₁)²/(n₁₂ + n₂₁) ~ χ²₁ (8.35); exact binomial version and Edwards' continuity correction; Dietterich (1998): McNemar keeps type I error, unlike paired t tests on resampled splits.

#### Nota 3 — Comparação de classificadores (p. 288)
**Subtopics:**
- Comparing two classifiers on a validation set by a correct/wrong cross-table and McNemar's test; limitations (single training set, smaller evaluation size).

### §8.7 — Exercícios (pp. 289–290)
**Subtopics:**
- 20 exercises: LDA/QDA derivations (1, 2, 12, 17, 19), cross-validated comparisons of logistic, LDA, KNN (3–11, 13), Bayes classifiers for exponential and normal populations by simulation (14–16, 20), odds-ratio CI (18).

## Ch. 9 — Algoritmos de Suporte Vetorial
**Pages:** pp. 291–317

### §9.1 — Introdução (pp. 291–292)
**Subtopics:**
- Support vector machines (Vapnik and co-authors; Cortes & Vapnik 1995) for binary classification; comparison with GLMs, GAMs, neural networks and trees on interpretability, accuracy and computation.

### §9.2 — Fundamentação dos algoritmos de suporte vetorial (pp. 292–294)
**Subtopics:**
- Data space, response y ∈ {−1, 1}; three cases (linearly separable, not separable, non-linear boundary); kernels (Gaussian, polynomial, …) to enlarge the feature space; tuning by cross-validation.

### §9.3 — Classificador de margem máxima (pp. 294–297)
**Subtopics:**
- Separating hyperplane f(x) = α + β′x and classification by its sign; maximal-margin hyperplane and support vectors; optimization with Lagrange multipliers (Ex. 9.1).

### §9.4 — Classificador de margem flexível (pp. 297–302)
**Subtopics:**
- Soft-margin (support vector) classifier (9.4) with slack variables ξᵢ and budget C; C chosen by cross-validation with tune() (e1071); facial-type data (Ex. 9.2) with C and gamma by 10-fold CV.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §9.5 — Classificador de margem não linear (pp. 302–305)
**Subtopics:**
- Kernel trick: the classifier depends only on inner products with support vectors; polynomial (degree 3, Ex. 9.3) and radial kernels.

### §9.6 — Regressão por algoritmos de suporte vetorial (pp. 305–309)
**Subtopics:**
- ε-insensitive support vector regression (9.8) with slack variables; linear and radial kernels, ε and cost tuned by CV (distance-vs-age data, Ex. 9.4–9.5).

### §9.7 — Notas de capítulo (pp. 309–316)
**Subtopics:**
- Notes 1–6: separating hyperplane; maximal-margin classifier (Bishop 2006, Lagrangian dual); soft-margin classifier; non-linear-margin classifier; more than two classes; SVM for regression.

### §9.8 — Exercícios (pp. 316–317)
**Subtopics:**
- 8 exercises on margins, the role of C in the bias–variance trade-off, kernels and simulated non-linear boundaries.

## Ch. 10 — Árvores e Florestas
**Pages:** pp. 319–344

> Trees are outside the syllabus; §10.3.1 and Notas 3 and 5 of §10.5 are indexed at subsection depth because they hold the book's only treatment of the bootstrap.

### §10.1 — Introdução (pp. 319–320)
**Subtopics:**
- CART (Breiman et al.): partition of the predictor space into rectangles, mode/mean as prediction; recursive binary splitting as a top-down greedy algorithm.

### §10.2 — Classificação por árvores (pp. 320–327)
**Subtopics:**
- Node class proportions p̂ₘₖ (10.1), majority class and node error rate; ctree() on facial types (Ex. 10.1); rpart() on coronary-lesion data with built-in cross-validation (rel error, xerror, xstd), the one-standard-error pruning rule and the complexity parameter CP (Ex. 10.2); overfitting and pruning as a variance–bias trade.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §10.3 — Bagging, boosting e florestas (pp. 327–334)
**Subtopics:**
- Ensembles to reduce the high variance of single trees.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

#### §10.3.1 — Bagging (pp. 327–329)
**Subtopics:**
- Bootstrap aggregating: B bootstrap replicates of the training set, f̂_bag(x) = (1/B)Σf̂ᵇ(x) for regression and majority vote for classification; weak vs strong learners; B ≈ 200; subagging (Bühlmann & Yu 2002); bagging() with nbagg = 200 on the coronary data (Ex. 10.3).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]] (bootstrap resampling)
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

#### §10.3.2 — Boosting (pp. 329–332)
**Subtopics:**
- Sequential reweighting of misclassified cases; weighted vote c_boost(x) (10.2); additive model of weak learners (10.3) and L2-boosting under squared loss (10.4)–(10.5); AdaBoost algorithm (stumps, α(b) = log[(1 − err)/err]); tuning B by CV, shrinkage λ and depth d; adabag (Ex. 10.4).

#### §10.3.3 — Florestas aleatórias (pp. 332–334)
**Subtopics:**
- Bagging plus a random subset of m ≈ √p predictors at each split; out-of-bag (OOB) error; decorrelated trees reduce variance; randomForest with 70/30 train–validation split (Ex. 10.5).

### §10.4 — Árvores para regressão (pp. 334–338)
**Subtopics:**
- Regression trees minimizing squared error, CP and 1 − R² for pruning (rsq.rpart), RMSE (anthracosis data, Ex. 10.6); trees for prediction may omit variables that matter for inference.

### §10.5 — Notas de capítulo (pp. 338–343)
**Subtopics:**
- Five notes: node-impurity criteria, pruning, bootstrap, regression trees, bagging theory.

#### Nota 1 — Critérios para avaliação de árvores de classificação (pp. 338–339)
**Subtopics:**
- Gini index Gₘ = Σp̂ₘₖ(1 − p̂ₘₖ), cross-entropy, and Breiman's relative variable importance from impurity decreases.

#### Nota 2 — Poda de árvores (p. 339)
**Subtopics:**
- Pre- vs post-pruning; cost-complexity criterion CP(α) = Σⱼ Σ_{xᵢ∈Rⱼ}(yᵢ − ŷ_{Rⱼ})² + α|A| (10.6) with α chosen by cross-validation.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

#### Nota 3 — Bootstrap (pp. 339–340)
**Subtopics:**
- Efron's (1979) nonparametric bootstrap: resample n points with replacement, B replicates of the estimator (10.7), bootstrap standard error as their sample standard deviation (example: the sample median); general θ̂ = t(X); B = 200 as a rule of thumb (Efron & Tibshirani 1993).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]

#### Nota 4 — Árvores para regressão (p. 340)
**Subtopics:**
- Piecewise-constant model y = Σfⱼ I(x ∈ Rⱼ) (10.8); the region mean minimizes the sum of squares.

#### Nota 5 — Bagging: noções sobre a teoria (pp. 340–343)
**Subtopics:**
- Breiman (1996): aggregated predictor f_A(x) = E_P[f(x, T)]; Jensen's inequality gives MSEP ≥ MSEP(A) (10.9)–(10.10); bagging helps unstable procedures (trees, subset selection, neural networks) but not stable ones (KNN); the bootstrap aggregate uses the empirical distribution P_T; classification case can turn poor predictors worse.

### §10.6 — Exercícios (pp. 343–344)
**Subtopics:**
- 11 exercises on classification and regression trees, pruning, bagging, boosting (gbm) and random forests.

## Ch. 11 — Regularização e Modelos Aditivos Generalizados
**Pages:** pp. 345–364

### §11.1 — Introdução (p. 345)
**Subtopics:**
- Model selection for prediction of a continuous response: fit candidates on training data, compare MSE/RMSE/R² on validation data, usually by cross-validation.
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]

### §11.2 — Regularização (pp. 345–353)
**Subtopics:**
- Overfitting illustrated by polynomials of degree 0, 1, 3, 9 fitted to sin(2πx) + noise (Bishop 2006); penalized loss functions; sparse vs non-sparse solutions; constraint-region geometry (Figure 11.2).
**Linked materials:**
- Rules: [[rules/06_classificacao_validacao|Classification & validation]]
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (variable selection)
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]] (frequentist counterpart of sparsity priors)

#### §11.2.1 — Regularização L2 (Ridge) (pp. 346–348)
**Subtopics:**
- Ridge (Hoerl & Kennard 1970) for multicollinearity and overfitting: β̂_Ridge(λ) = argmin Σ(yₜ − β′xₜ)² + λΣβⱼ² (11.2) = (X′X + λI)⁻¹X′y (11.3); constrained form Σβⱼ² ≤ m (11.4); intercept not penalized.
- Properties: biased for non-zero coefficients, consistent only under conditions on λ, p, n; no variable selection; λ by cross-validation or information criteria.

#### §11.2.2 — Regularização L1 (Lasso) (pp. 348–349)
**Subtopics:**
- Lasso (11.5) with constraint Σ|βⱼ| ≤ m (11.6): shrinks redundant coefficients exactly to zero (sparsity, variable selection), biased for non-zero coefficients; soft-threshold solution β̂ⱼ = sign(Zⱼ)(|Zⱼ| − λ/2)₊ (11.7) in the orthonormal case.

#### §11.2.3 — Outras propostas (pp. 349–353)
**Subtopics:**
- Elastic net (11.8) mixing L2 and L1 penalties (α = λ₂/(λ₁ + λ₂)); adaptive lasso (11.9) with weights |β̂ⱼ|^−τ, consistent under mild conditions; glmnet also covers logistic, multinomial, Poisson and Cox models.
- Example 11.1 (anthracosis data): OLS vs cv.glmnet ridge (α = 0), lasso (α = 1, drops tmunic and distmin) and elastic net (α = 0.5); CV curves of MSE against log λ, lambda.min and CV RMSE.

### §11.3 — Modelos aditivos generalizados (GAM ) (pp. 353–361)
**Subtopics:**
- Additive model (11.10) with unspecified smooth fᵢ; GAM as an extension of GLMs, g(µᵢ) = β₀ + Σβⱼfⱼ(xᵢⱼ) (11.11); basis expansions (11.13); piecewise cubic polynomials (11.14), cubic splines with k knots and k + 4 df (11.15), truncated-power basis, natural splines; knots by cross-validation.
- Smoothing splines minimizing Σ[yᵢ − f(xᵢ)]² + λ∫f″(u)²du (11.16), λ by CV; local regression (span s = k/n, weighted least squares); backfitting.
- Example 11.2 (esforco data, mgcv gam()): linear fit vs GAM with s() terms, effective degrees of freedom, GCV, gam.check() diagnostics, analysis of deviance between nested models, prediction with standard errors.
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]] (flexible polynomial/spline fits)

### §11.4 — Notas de capítulo (pp. 361–363)
**Subtopics:**
- Three notes: ridge bias, choice of λ, generalized linear models.

#### Nota 1 — Viés da regularização Ridge. (p. 361)
**Subtopics:**
- β̂_Ridge(λ) = (I + λR⁻¹)⁻¹β̂_MQ with R = X′X (11.17), so E[β̂_Ridge(λ)] = (I + λR⁻¹)⁻¹β ≠ β (11.18).

#### Nota 2 — Escolha do parâmetro λ (p. 361)
**Subtopics:**
- SVD form of ridge with shrinkage factors dⱼ²/(dⱼ² + λ); effective degrees of freedom gl(λ) = tr[X(X′X + λI)⁻¹X′] = Σdⱼ²/(dⱼ² + λ); AIC, BIC and Hannan–Quinn criteria over a λ grid.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (model selection)

#### Nota 3 — Modelos Lineares Generalizados (pp. 362–363)
**Subtopics:**
- Exponential family f(y | θ, φ) (11.19): E(y) = b′(θ), Var(y) = a(φ)b″(θ) = a(φ)V(µ) with variance function (11.20); normal and binomial members; link g(µ) = x′β (identity → linear model, logit → logistic regression); log-likelihood (11.21) maximized by Newton–Raphson / Fisher scoring with score u(β) and information I(β).
**Linked materials:**
- Class: [[Map/class-plan#Class 2: Introduction to statistical learning|Class 2]] (logistic and Poisson regression as GLMs)
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]]

### §11.5 — Exercícios (pp. 363–364)
**Subtopics:**
- 4 exercises: regression on Telebrás vs IBV prices, ridge/lasso/elastic net on earlier examples, gamma-log GAM.

## Ch. 12 — Análise de Agrupamentos
**Pages:** pp. 367–382

### §12.1 — Introdução (pp. 367–369)
**Subtopics:**
- Cluster analysis (data segmentation) as unsupervised learning; Euclidean and non-Euclidean spaces; distances between units (height, weight, age data, Table 12.1).

### §12.2 — Estratégias de agrupamento (pp. 369–370)
**Subtopics:**
- Combinatorial, model-based (mixture densities) and bump-hunting algorithms (Hastie et al. 2009); hierarchical vs partition algorithms.

### §12.3 — Algoritmos hierárquicos (pp. 370–373)
**Subtopics:**
- Agglomerative clustering by centroid distance worked step by step; dendrograms (Ex. 12.1).

### §12.4 — Algoritmos de partição: K–médias (pp. 373–379)
**Subtopics:**
- K-means minimizing within-cluster sums of squares (Hartigan–Wong, Lloyd, MacQueen, Forgy algorithms); kmeans(); choice of K; simulated and traffic-data examples (Ex. 12.2–12.5).

### §12.5 — Notas de capítulo (pp. 379–382)
**Subtopics:**
- Notes 1–4: distances for non-Euclidean spaces (edit distance); single, complete and average linkage; cophenetic matrix and cophenetic correlation; other algorithms.

### §12.6 — Exercícios (p. 382)
**Subtopics:**
- 7 exercises on hierarchical and K-means clustering, linkage choices, edit distance and the cophenetic correlation.

## Ch. 13 — Redução de dimensionalidade
**Pages:** pp. 383–414

### §13.1 — Introdução (p. 383)
**Subtopics:**
- Principal components, factor analysis and independent components reduce dimension while preserving the covariance structure; factors as regressors in later analyses.

### §13.2 — Análise de Componentes Principais (pp. 383–390)
**Subtopics:**
- Orthogonal rotation of axes that sequentially maximizes explained variance (eigen-decomposition of the covariance or correlation matrix); component scores, elbow (scree) plot, biplot (Ex. 13.1).

### §13.3 — Análise fatorial (pp. 390–403)
**Subtopics:**
- Orthogonal factor model with loadings Λ and specific variances ψ; principal-factor and maximum-likelihood estimation; rotations (Varimax, Quartimax, Equimax); number of factors by elbow plot, parallel analysis and optimal coordinates; factor scores; factanal() on suicide data.

### §13.4 — Análise de componentes independentes (pp. 403–411)
**Subtopics:**
- ICA for non-Gaussian sources (Hyvärinen & Oja 2000): centring, whitening and dimension reduction; non-Gaussianity via excess kurtosis and negentropy; the FastICA fixed-point algorithm.

### §13.5 — Notas de capítulo (pp. 411–413)
**Subtopics:**
- Notes 1–4: deriving principal components with a Lagrangian; decomposition of symmetric matrices; the Wishart distribution and the system (13.7); determining the number of factors.

### §13.6 — Exercícios (pp. 413–414)
**Subtopics:**
- 9 exercises on principal components, factor analysis and ICA derivations and applications.

## Ch. 14 — Redes neurais
**Pages:** pp. 417–434

### §14.1 — Introdução (pp. 417–418)
**Subtopics:**
- Neurons and activation functions; single-layer, multilayer feed-forward and recurrent networks.

### §14.2 — Perceptron (pp. 418–421)
**Subtopics:**
- Rosenblatt's perceptron as a linear classifier updated on misclassified points; simulated data and the disc-displacement data (Ex. 14.1–14.2).

### §14.3 — Redes com camadas escondidas (pp. 421–423)
**Subtopics:**
- One-hidden-layer network: inputs x, hidden units y, outputs z, weights α and β; one output for regression, K outputs for classification.

### §14.4 — O algoritmo retropropagação (backpropagation) (pp. 423–430)
**Subtopics:**
- Fitting by minimizing SSE (regression) or cross-entropy (classification) with gradient descent / stochastic gradient descent via backpropagation; neuralnet examples with one and two hidden layers (Ex. 14.3–14.4); one-against-all and one-against-one strategies for K > 2 classes.

### §14.5 — Aprendizado profundo (Deep learning ) (pp. 430–431)
**Subtopics:**
- Deep learning as many-layer networks learning a hierarchy of representations; multilayer perceptron; historical waves (Goodfellow et al. 2016); MNIST.

### §14.6 — Notas de capítulo (pp. 431–433)
**Subtopics:**
- Notes 1–3: the Mark I perceptron; perceptron convergence; the backpropagation algorithm.

### §14.7 — Exercícios (pp. 433–434)
**Subtopics:**
- 3 exercises: network equations from fitted weights, and loss functions for K binary vs K mutually exclusive classes (softmax, cross-entropy).

## App. A — Otimização numérica
**Pages:** pp. 437–451

### §A.1 — Introdução (pp. 437–440)
**Subtopics:**
- Gradient vs non-gradient optimization; iterative schemes with a convergence tolerance; main use is maximizing a likelihood (MLE) or a posterior density (posterior mode); gradient, Hessian and Fisher information.
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §A.2 — O método de Newton-Raphson (pp. 440–442)
**Subtopics:**
- Newton–Raphson from a quadratic approximation: θ⁽ⁱ⁺¹⁾ = θ⁽ⁱ⁾ − H⁻¹g; worked univariate example (Ex. A.1–A.2).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §A.3 — O método scoring (p. 442)
**Subtopics:**
- Fisher scoring replaces the Hessian by minus the expected information, θ⁽ⁱ⁺¹⁾ = θ⁽ⁱ⁾ + I(θ⁽ⁱ⁾)⁻¹g (A.11); slower but sometimes easier; Cauchy location MLE (Ex. A.3).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]] (GLM / probit fitting)

### §A.4 — O método de Gauss-Newton (pp. 442–444)
**Subtopics:**
- Non-linear least squares solved as a sequence of linearized regressions (Ex. A.4).

### §A.5 — Métodos Quase-Newton (pp. 444–445)
**Subtopics:**
- Hessian approximations (BFGS, variable-metric/secant methods): cheaper steps, more iterations.

### §A.6 — Aspectos computacionais (pp. 445–449)
**Subtopics:**
- optim() methods (Nelder–Mead, BFGS, CG, L-BFGS-B, SANN), packages optimization and maxLik (maxNR()); examples including MLE of a normal mean and variance (Ex. A.5–A.8).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]]

### §A.7 — Notas de capítulo (pp. 449–450)
**Subtopics:**
- Notes 1–2: non-gradient algorithms (genetic algorithms, Nelder–Mead simplex, simulated annealing); constrained optimization.

### §A.8 — Exercícios (pp. 450–451)
**Subtopics:**
- 12 exercises: steepest descent and quadratic hill climbing, Newton–Raphson and scoring for Cauchy and multinomial MLEs, non-linear regression, maxLik/optimization packages.

## App. B — Noções de simulação
**Pages:** pp. 453–478

### §B.1 — Introdução (pp. 453–456)
**Subtopics:**
- Monte Carlo origins (Metropolis & Ulam 1949); area of a figure by uniform points; random vs pseudo-random numbers (middle-square, congruential generators, runif()); static (Monte Carlo, acceptance–rejection, weighted resampling), imputation (EM, data augmentation) and dynamic (Gibbs, Metropolis–Hastings = MCMC) simulation.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §B.2 — Método Monte Carlo (pp. 456–457)
**Subtopics:**
- E_F[h(X)] ≈ (1/n)Σh(Xᵢ) (B.1), strong-law convergence and O(n^{−1/2}) standard error (B.2); π/4 by simulating √(1 − X²) (Ex. B.4); sampling marginals by composition (mixtures) (B.4).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]] (Monte Carlo)

### §B.3 — Simulação de variáveis discretas (pp. 457–459)
**Subtopics:**
- Inverse-cdf method for discrete distributions (B.5)–(B.6); Bernoulli, binomial and Poisson generators via the recursion pⱼ₊₁ = λpⱼ/(j + 1) (B.7)–(B.8); R r-functions and Excel tools.

### §B.4 — Simulação de variáveis contínuas (pp. 459–464)
**Subtopics:**
- Probability integral transform (Theorem B.1, x = F⁻¹(u)); exponential −β log u; normal via Φ⁻¹ and the Box–Muller transform (B.13); chi-squared as sums of squared normals; t, F, gamma, beta in R.

### §B.5 — Simulação de vetores aleatórios (pp. 464–467)
**Subtopics:**
- Joint = marginal × conditional; bivariate uniform (Monte Carlo area) and independent bivariate normal examples.

### §B.6 — Métodos de reamostragem (pp. 467–472)
**Subtopics:**
- Sampling from a target π via an easy density g plus a correction step.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Rules: [[rules/07_bayes|Bayesian inference]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

#### §B.6.1 — Amostragem por aceitação-rejeição (pp. 468–470)
**Subtopics:**
- Envelope π(x) ≤ Ag(x); accept x* if u ≤ π(x*)/[Ag(x*)]; acceptance probability 1/A (B.14), geometric number of trials with mean A; only the kernel of π is needed; Beta(2,2) from uniforms (Ex. B.15).

#### §B.6.2 — Reamostragem ponderada (pp. 470–472)
**Subtopics:**
- Sampling–importance resampling with weights wᵢ ∝ π(xᵢ)/g(xᵢ); importance sampling estimators (B.15)–(B.16) and the self-normalized estimator (B.17) with Geweke's (1989) consistency conditions and standard error; posterior mean of θ in the genetic-linkage model under a flat prior using a Beta(35, 39) proposal, θ̂ = 0.6180 (Ex. B.16).

### §B.7 — Notas de capítulo (pp. 472–476)
**Subtopics:**
- Five notes: MCMC overview, Gibbs sampler, Metropolis–Hastings, Box–Muller, gamma simulation.
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

#### Nota 1 — Métodos MCMC (p. 472)
**Subtopics:**
- Markov chains whose stationary distribution is the target (Metropolis et al. 1953; Hastings 1970; Geman & Geman 1984; Gelfand & Smith 1990); references including Gamerman & Lopes (2006).

#### Nota 2 — O Amostrador de Gibbs (pp. 472–473)
**Subtopics:**
- Two-variable Gibbs sequence (B.19) and Rao–Blackwellized marginal density estimates (B.20)–(B.21) (Casella & George 1992); general case with full conditionals π(θᵢ | θ₋ᵢ) (B.22) and the transition kernel of the homogeneous chain (B.23)–(B.24).

#### Nota 3 — O algoritmo de Metropolis-Hastings (pp. 474–475)
**Subtopics:**
- Reversibility π(θ)p(θ, φ) = π(φ)p(φ, θ); kernel q·α (B.25) with acceptance probability α = min{1, π(φ)q(φ, θ)/[π(θ)q(θ, φ)]} (B.26); acceptance rates of 20–50%; symmetric (Metropolis), random-walk and independence chains; Metropolis-within-Gibbs; irreducibility and aperiodicity (Chib & Greenberg 1995).

#### Nota 4 — Transformação de Box-Müller. (pp. 475–476)
**Subtopics:**
- Polar-coordinate derivation: R² ~ Exp(2) and θ ~ U(0, 2π) independent give two independent N(0, 1) draws.

#### Nota 5 — Simulação de uma distribuição gama. (p. 476)
**Subtopics:**
- Gamma(r, β) with integer r as a sum of r independent exponentials.

### §B.8 — Exercícios (pp. 476–478)
**Subtopics:**
- 20 exercises: pseudo-random generators (1–6), inverse-cdf simulation of discrete and continuous laws (7–15), acceptance–rejection (16, 18–20), Monte Carlo probability for a correlated bivariate normal (17).

## App. C — Algoritmos para dados aumentados
**Pages:** pp. 479–489

### §C.1 — Introdução (p. 479)
**Subtopics:**
- Latent (unobserved) data introduced to ease likelihood or posterior computation; complete vs incomplete data (cumulative fish-trap counts, Ex. C.1); multiple imputation (Rubin 1977, 1987; Little & Rubin 1987).
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]

### §C.2 — O algoritmo EM (pp. 480–485)
**Subtopics:**
- Observed-data likelihood as an integral of the complete-data likelihood (C.1); genetic-linkage multinomial (C.2)–(C.3): E step with binomial conditional expectations, M step (C.4)–(C.5), iterations from θ⁽⁰⁾ = 0.5 to θ̂ = 0.62682 (Table C.1).
- General E step Q(θ, θ⁽ⁱ⁾) = E[ℓ(θ | x) | y, θ⁽ⁱ⁾] (C.6), M step, convergence check; posterior-mode version (C.7); Example C.3.
- Monotonicity (Proposition C.1, Dempster, Laird & Rubin 1977) via the Q − H + K decomposition (C.8)–(C.9); generalized EM; Wu (1983) convergence to a stationary point (Proposition C.2), multiple starting values, linear convergence rate and Louis's acceleration.
- Censored regression of log failure times of motors on temperature (Schmee & Hahn 1979; Tanner 1996): truncated-normal E step with the inverse Mills ratio H(x) = φ(x)/[1 − Φ(x)] (C.10)–(C.14); estimates after 11 iterations (Ex. C.4).
**Linked materials:**
- Class: [[Map/class-plan#Class 1: Review of basic ingredients|Class 1]] (likelihood maximization)
- Class: [[Map/class-plan#Class 7: More econometric models|Class 7]] (censored / Tobit-type regression)

### §C.3 — O algoritmo EM Monte Carlo (pp. 485–486)
**Subtopics:**
- MCEM (Wei & Tanner 1990): Monte Carlo average over simulated latent data in the E step, growing m and monitoring θ⁽ⁱ⁾ against i; genetic-linkage iterations (Table C.3, Ex. C.5).
**Linked materials:**
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]

### §C.4 — Cálculo de erros padrões (pp. 486–487)
**Subtopics:**
- Standard errors after EM: direct/numerical Hessian; Louis's method and the missing-information principle (C.15) — observed = complete − missing information (Proposition C.3); genetic-linkage case 435.3 − 57.8 = 377.5, s.e.(θ̂) ≈ 0.05; simulation approximations.

### §C.5 — O Algoritmo de dados aumentados (pp. 487–489)
**Subtopics:**
- Tanner–Wong data augmentation: posterior identity (C.16) and predictive identity (C.17) iterated by simulation (S) and integration (I) steps, giving a mixture estimate of p(θ | y); relation to the Gibbs sampler and the chained-data algorithm; Beta–binomial mixture for the genetic-linkage posterior (Ex. C.6).
**Linked materials:**
- Rules: [[rules/07_bayes|Bayesian inference]]
- Rules: [[rules/08_monte_carlo_mcmc|Monte Carlo & MCMC]]
- Class: [[Map/class-plan#Classes 3+4: Introduction to Bayesian learning|Classes 3+4]]

### §C.6 — Exercícios (p. 489)
**Subtopics:**
- 8 exercises: EM for exponential families, censored regression updates, MCEM, EM standard errors by simulation, chained-data (Gibbs) algorithm with burn-in, SI algorithm, EM for censored exponential data.
