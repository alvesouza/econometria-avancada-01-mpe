# Advanced Econometrics — official course site (2026)

Source: <https://hedibert.org/current-teaching/> (tab "Advanced Econometrics - Professional Master in Economics - 2026"). Files hosted on hedibert.org are saved under `Aula/<class>/materials/`; external links are listed only.

- Course: Advanced Econometrics
- Level: Professional Master in Economics – 4th quarter of 2026
- Professor: Hedibert Freitas Lopes – www.hedibert.org
- Objective: The main objective of this course is to introduce basic aspects i) Statistical Learning and ii) Bayesian Learning, as well as iii) Micro-econometrics, and iv) Macro-econometrics, that are necessary for the master’s degree program.
- Brief course description: Regression with endogeneity, regression with measurement error, instrumental variables, potential outcomes, Neyman-Rubin model, selection bias, reverse causality, and omitted variables, panel data, hierarchical models, fixed effect, and random effect, difference-in-differences methods, ARIMA models; long memory; unit root, GARCH models, and stochastic volatility. Vector autoregressive models, factorial models with stochastic volatility, and multivariate models with time-varying parameters, logistic regression; performance metrics for classification, training and testing data; cross-validation, bias-variance trade-off, prior, posterior, and predictive distributions; sequential Bayes and conjugate analysis, Monte Carlo methods.
- Teaching assistant: Henrique Wang
- Final exam: You will NOT be asked to write R script or similar during the final exam
- Evaluation: 30% final exam, 60% homework assignments (15% each), 10% participation
- Homework assignments: Homework can be done by groups of no more than 4 students.

## Class 1: Brief review of basic ingredients: i) Parametric models, likelihoods, estimators and their sampling distributions; ii) Gaussian linear regression: estimation and variable selection; iii) AR(1) model: estimation, unit root, equilibrium distribution; iv) AR(p) model: connection to Gaussian linear regression; v) VAR(1) model: multivariate estimation, matrix notation.

| Item | Link | Local copy |
|---|---|---|
| Reproducibility crisis: p-hacking | <https://hedibert.org/wp-content/uploads/2026/04/part1-p-hacking.pdf> | [part1-p-hacking.pdf](class-01/materials/part1-p-hacking.pdf) |
| p-hacking in the economics field | <https://hedibert.org/wp-content/uploads/2026/04/p_hacking_slides-economics.pdf> | [p_hacking_slides-economics.pdf](class-01/materials/p_hacking_slides-economics.pdf) |
| Maximum likelihood estimation and its estimators | <https://hedibert.org/wp-content/uploads/2026/10/mle_sampling_rules.pdf> | [mle_sampling_rules.pdf](class-01/materials/mle_sampling_rules.pdf) |
| Tradeoff bias-variance: a linear regression exercise | <https://hedibert.org/wp-content/uploads/2026/10/overfitting_a_linear_model.html> | [overfitting_a_linear_model.html](class-01/materials/overfitting_a_linear_model.html) |
| Abstenção no 1º turno presidencial de 2026 | <https://hedibert.org/wp-content/uploads/2026/10/regressao_abstencao_2026.pdf> | [regressao_abstencao_2026.pdf](class-01/materials/regressao_abstencao_2026.pdf) |
| Bernoulli trials: iid vs logistic regression | <https://hedibert.org/wp-content/uploads/2025/10/bernoulli-iid-logistic-R.txt> | [bernoulli-iid-logistic-R.txt](class-01/materials/bernoulli-iid-logistic-R.txt) |
| Selecting the sample size of iid Bernoulli trials | <https://hedibert.org/wp-content/uploads/2025/10/optimal-samplesize.html> | [optimal-samplesize.html](class-01/materials/optimal-samplesize.html) |
| Poisson model and poisson with breakpoint: MLE, sufficiency, unbiasedness, consistency, efficiency | <https://hedibert.org/wp-content/uploads/2024/10/class1-poisson.pdf> | [class1-poisson.pdf](class-01/materials/class1-poisson.pdf) |
| AI-assisted slides (Poisson with breakpoint) | <https://hedibert.org/wp-content/uploads/2026/10/poisson-with-breakpoint.pdf> | [poisson-with-breakpoint.pdf](class-01/materials/poisson-with-breakpoint.pdf) |
| Comparing estimators via Mean Square Error (MSE) | <https://hedibert.org/wp-content/uploads/2024/10/Class1-comparing-estimators-MSE.pdf> | [Class1-comparing-estimators-MSE.pdf](class-01/materials/Class1-comparing-estimators-MSE.pdf) |
| AI-assisted slides (comparing estimators via MSE) | <https://hedibert.org/wp-content/uploads/2026/10/comparing-estimators-MSE-slides.pdf> | [comparing-estimators-MSE-slides.pdf](class-01/materials/comparing-estimators-MSE-slides.pdf) |
| Comparing estimators: sample mean, sample weighted mean, trimmed mean, sample median | <https://hedibert.org/wp-content/uploads/2025/10/comparing-estimators.html> | [comparing-estimators.html](class-01/materials/comparing-estimators.html) |
| Poisson model: R code for the coal mining disaster data | <https://hedibert.org/wp-content/uploads/2024/10/class1-poisson.html> | [class1-poisson.html](class-01/materials/class1-poisson.html) |
| Poisson model: Our first Bayesian experience | <https://hedibert.org/wp-content/uploads/2024/10/class1-poisson-with-exponential-prior.pdf> | [class1-poisson-with-exponential-prior.pdf](class-01/materials/class1-poisson-with-exponential-prior.pdf) |
| Bayesian hierarchical Beta-Binomial regression | <https://hedibert.org/wp-content/uploads/2025/10/hierarchical-beta-binomial.html> | [hierarchical-beta-binomial.html](class-01/materials/hierarchical-beta-binomial.html) |
| Gaussian linear regression | <https://hedibert.org/wp-content/uploads/2018/05/multiplelinearregression.pdf> | [multiplelinearregression.pdf](class-01/materials/multiplelinearregression.pdf) |
| A few examples | <https://hedibert.org/wp-content/uploads/2024/10/normallinearregression-R.txt> | [normallinearregression-R.txt](class-01/materials/normallinearregression-R.txt) |
| Autoregressive model of order one | <https://hedibert.org/wp-content/uploads/2017/04/ar-ma.pdf> | [ar-ma.pdf](class-01/materials/ar-ma.pdf) |
| A few examples | <https://hedibert.org/wp-content/uploads/2024/10/ar-var-R.txt> | [ar-var-R.txt](class-01/materials/ar-var-R.txt) |
| A bit about Monte Carlo simulation and the bootstrap technique | <https://hedibert.org/wp-content/uploads/2025/10/bootstrap-example.html> | [bootstrap-example.html](class-01/materials/bootstrap-example.html) |
| Bivariate normal correlation coefficient: MLE, sample correlation and the bootstrap | <https://hedibert.org/wp-content/uploads/2025/10/correlation-bivariate-gaussian.html> | [correlation-bivariate-gaussian.html](class-01/materials/correlation-bivariate-gaussian.html) |
| Complementary bibliography: Introdução à Inferência Estatística (Bolfarine & Sandoval, 2010), Sections 1.1.4, 1.3, 2.1, 2.2, 3.1, 3.2 | <https://docs.ufpr.br/~lucambio/CE210/LIVRO%20de%20infer%EAncia%20bolfarine.pdf> | — |

## Class 2: Introduction to statistical learning: i) Linear and log-linear regression modeling; ii) Training and testing samples; iii) Validation. Bias-variance trade-off.

| Item | Link | Local copy |
|---|---|---|
| Multiple linear regression | <https://hedibert.org/wp-content/uploads/2018/05/multiplelinearregression.pdf> | [multiplelinearregression.pdf](class-02/materials/multiplelinearregression.pdf) |
| CAPM model | <https://hedibert.org/wp-content/uploads/2022/05/capm-regression-R.txt> | [capm-regression-R.txt](class-02/materials/capm-regression-R.txt) |
| Return on education | <https://hedibert.org/wp-content/uploads/2024/01/regressaomultipla-return-to-education.html> | [regressaomultipla-return-to-education.html](class-02/materials/regressaomultipla-return-to-education.html) |
| Professors salaries | <https://hedibert.org/wp-content/uploads/2024/04/salaries-for-professors.txt> | [salaries-for-professors.txt](class-02/materials/salaries-for-professors.txt) |
| Motorcycle example | <https://hedibert.org/wp-content/uploads/2018/05/motorcyle-polynomialregression.pdf> | [motorcyle-polynomialregression.pdf](class-02/materials/motorcyle-polynomialregression.pdf) |
| HTML version from Rmarkdown | <https://hedibert.org/wp-content/uploads/2025/10/motorcycle-polynomialregression.html> | [motorcycle-polynomialregression.html](class-02/materials/motorcycle-polynomialregression.html) |
| *Class note (site):* "We studied the selection of the polynomial order that best fits the “motorcycle” data. We discussed cross-validation (CV), replicated CV, leave-one-out CV (LOOCV), and 10-fold CV. After concluding that the polynomial model of order 12 was the best, we implemented a bootstrap algorithm to obtain approximate confidence bands." | — | — |
| Logistic regression | <https://hedibert.org/wp-content/uploads/2018/05/logisticregression-discriminantanalysis.pdf> | [logisticregression-discriminantanalysis.pdf](class-02/materials/logisticregression-discriminantanalysis.pdf) |
| Graduate school admission | <https://hedibert.org/wp-content/uploads/2024/04/graduate-school-admission.txt> | [graduate-school-admission.txt](class-02/materials/graduate-school-admission.txt) |
| Figures | <https://hedibert.org/wp-content/uploads/2024/04/graduate-school-admission.pdf> | [graduate-school-admission.pdf](class-02/materials/graduate-school-admission.pdf) |
| Gaussian vs Poisson regression: Counts of visitors to a website | <https://hedibert.org/wp-content/uploads/2025/10/Gaussian-vs-Poisson-regression.html> | [Gaussian-vs-Poisson-regression.html](class-02/materials/Gaussian-vs-Poisson-regression.html) |
| Fundamentos de Machine Learning (Notas do Prof. Paulo C. Marques F.) | <https://hedibert.org/wp-content/uploads/2024/10/Fundamentos.pdf> | [Fundamentos.pdf](class-02/materials/Fundamentos.pdf) |
| Código R | <https://hedibert.org/wp-content/uploads/2024/10/bias-variance-R.txt> | [bias-variance-R.txt](class-02/materials/bias-variance-R.txt) |

## Classes 3+4: Introduction to Bayesian learning: Prior, posterior, and predictive distributions; Sequential Bayesian updating and conjugate analysis, Bayes factor, posterior model probability, model selection; Monte Carlo & Markov Chain Monte Carlo methods; Sparsity in linear and log-linear models.

| Item | Link | Local copy |
|---|---|---|
| Bayesian ingredients | <https://hedibert.org/wp-content/uploads/2020/01/aprendizagembayesiana-bayesianingredients.pdf> | [aprendizagembayesiana-bayesianingredients.pdf](class-03-04/materials/aprendizagembayesiana-bayesianingredients.pdf) |
| Bayesian estimator and loss functions – em português | <https://hedibert.org/wp-content/uploads/2026/05/notas-bayesianas-slides.pdf> | [notas-bayesianas-slides.pdf](class-03-04/materials/notas-bayesianas-slides.pdf) |
| Sequential Bayes: i) Bernoulli trials with Beta prior and ii) Uniform trials with Pareto prior | <https://hedibert.org/wp-content/uploads/2024/10/sequential-bayes-bernoulli-uniform-trials.html> | [sequential-bayes-bernoulli-uniform-trials.html](class-03-04/materials/sequential-bayes-bernoulli-uniform-trials.html) |
| Sequential Bayes: Bernoulli trials with discrete sucess probability | <https://hedibert.org/wp-content/uploads/2024/10/bernoulli-trials-discrete-prior.html> | [bernoulli-trials-discrete-prior.html](class-03-04/materials/bernoulli-trials-discrete-prior.html) |
| Tiago Mendonca’s shiny for the physicists example | <https://tiagomendonca.shinyapps.io/bayes/> | — |
| Phisycists A, B, C and D: Normal model and 4 priors | <https://hedibert.org/wp-content/uploads/2024/01/fisicos-ABCD.html> | [fisicos-ABCD.html](class-03-04/materials/fisicos-ABCD.html) |
| Flipping one of three coins three times and observing three heads | <https://hedibert.org/wp-content/uploads/2021/04/question0.pdf> | [question0.pdf](class-03-04/materials/question0.pdf) |
| R code | <https://hedibert.org/wp-content/uploads/2021/04/question0-R.txt> | [question0-R.txt](class-03-04/materials/question0-R.txt) |
| Chapter 1 of “Bayes’ Rule: A tutorial Introduction to Bayesian Analysis | <https://www.researchgate.net/publication/237020329_Bayes'_Rule_A_Tutorial_Introduction_to_Bayesian_Analysis> | — |
| Slide | <https://hedibert.org/wp-content/uploads/2020/02/examples-from-stone-2013.pdf> | [examples-from-stone-2013.pdf](class-03-04/materials/examples-from-stone-2013.pdf) |
| Bayesian inference for the correlation coefficient of bivariate Gaussian data | <https://hedibert.org/wp-content/uploads/2021/05/correlationcoefficient.html> | [correlationcoefficient.html](class-03-04/materials/correlationcoefficient.html) |
| Bayesian stochastic volatility (SV) model with various error distributions | <https://hedibert.org/wp-content/uploads/2024/09/petrobras-gaussian-student-SV-models.html> | [petrobras-gaussian-student-SV-models.html](class-03-04/materials/petrobras-gaussian-student-SV-models.html) |
| Hosszejni & Kastner, 2021 | <https://www.jstatsoft.org/article/view/v100i12> | — |
| Bayesian Logistic Regression | <https://hedibert.org/wp-content/uploads/2024/10/Bayesian-logistic-regression.html> | [Bayesian-logistic-regression.html](class-03-04/materials/Bayesian-logistic-regression.html) |
| Bayesian Beta Regression | <https://hedibert.org/wp-content/uploads/2024/10/Bayesian-beta-regression.html> | [Bayesian-beta-regression.html](class-03-04/materials/Bayesian-beta-regression.html) |
| Bayesian hierarchical Beta-Binomial regression | <https://hedibert.org/wp-content/uploads/2025/10/hierarchical-beta-binomial.html> | [hierarchical-beta-binomial.html](class-03-04/materials/hierarchical-beta-binomial.html) |
| Bayesian hierarchical linear regression | <https://hedibert.org/wp-content/uploads/2025/11/hierarchical-gaussian-linear-model.html> | [hierarchical-gaussian-linear-model.html](class-03-04/materials/hierarchical-gaussian-linear-model.html) |
| Zero-inflated Poisson data | <https://hedibert.org/wp-content/uploads/2025/11/ZIP-fishing.html> | [ZIP-fishing.html](class-03-04/materials/ZIP-fishing.html) |
| Three examples of HMC/RSTAN in action: iid Gaussian, Gaussian linear regression, and stochastic volatility AR(1) model. | <https://hedibert.org/wp-content/uploads/2024/10/exemplos-1-2-3-R-STAN.txt> | [exemplos-1-2-3-R-STAN.txt](class-03-04/materials/exemplos-1-2-3-R-STAN.txt) |
| Sparse priors: Brief summaries of Carvalho, Polson and Scott (2010) and Griffin and Brown (2010) | <https://hedibert.org/wp-content/uploads/2024/10/sparse-priors.pdf> | [sparse-priors.pdf](class-03-04/materials/sparse-priors.pdf) |
| Sparse priors: simulation exercise | <https://hedibert.org/wp-content/uploads/2024/10/sparseregression-simulation-R.txt> | [sparseregression-simulation-R.txt](class-03-04/materials/sparseregression-simulation-R.txt) |
| graphs | <https://hedibert.org/wp-content/uploads/2024/10/sparseregression-simulation.pdf> | [sparseregression-simulation.pdf](class-03-04/materials/sparseregression-simulation.pdf) |

## Classes 5+6: Introduction to causal inference: Simpson’s Paradox, Directed Acyclic Graphs (Paths, Junctions, Chains, Forks, Colliders and d-separation), Potential outcome, average treatment effect (ATE), quantile treatment effect (QTE), conditional average treatment effect (CATE), Stable Unit Treatment Value Assumption (SUTVA), Instrumental Variables (IV), Difference in Difference (DiD) and Regression Discontinuity Design (RDD).

| Item | Link | Local copy |
|---|---|---|
| Omitted variable example | <https://hedibert.org/wp-content/uploads/2025/11/omitted-variable.html> | [omitted-variable.html](class-05-06/materials/omitted-variable.html) |
| Error-in-variable problem | <https://hedibert.org/wp-content/uploads/2025/11/error-in-variables.pdf> | [error-in-variables.pdf](class-05-06/materials/error-in-variables.pdf) |
| Notes on causality | <https://hedibert.org/wp-content/uploads/2024/11/notes-on-causal-inference.pdf> | [notes-on-causal-inference.pdf](class-05-06/materials/notes-on-causal-inference.pdf) |
| Example 1: Instrumental variables (IV) | <https://hedibert.org/wp-content/uploads/2025/11/example1-iv-card.html> | [example1-iv-card.html](class-05-06/materials/example1-iv-card.html) |
| dataset | <https://hedibert.org/wp-content/uploads/2024/11/card.csv> | [card.csv](class-05-06/materials/card.csv) |
| Example 2: Difference in Difference (DiD) | <https://hedibert.org/wp-content/uploads/2025/11/example2-DiD-card-krueger.html> | [example2-DiD-card-krueger.html](class-05-06/materials/example2-DiD-card-krueger.html) |
| dataset | <https://hedibert.org/wp-content/uploads/2024/10/card-krueger.txt> | [card-krueger.txt](class-05-06/materials/card-krueger.txt) |
| Example 3: Regression Discontinuity Design (RDD) | <https://hedibert.org/wp-content/uploads/2025/11/example3-RDD-age-mva-internal.html> | [example3-RDD-age-mva-internal.html](class-05-06/materials/example3-RDD-age-mva-internal.html) |
| dataset | <https://hedibert.org/wp-content/uploads/2024/11/age-mva-internal.txt> | [age-mva-internal.txt](class-05-06/materials/age-mva-internal.txt) |
| CausalML Book | <https://causalml-book.org/> | — |
| Athey and Imbens (2017) The State of Applied Econometrics: Causality and Policy Evaluation | <https://pubs.aeaweb.org/doi/pdfplus/10.1257/jep.31.2.3> | — |
| Li, Ding and Mealli (2023) Bayesian causal inference: a critical review | <https://doi.org/10.1098/rsta.2022.0153> | — |
| Neal (2020) Introduction to Causal Inference from a Machine Learning Perspective | <https://www.bradyneal.com/Introduction_to_Causal_Inference-Dec17_2020-Neal.pdf> | — |
| Neal (2020) Introduction to Causal Inference (course lots of illustration, very didactical) | <https://www.bradyneal.com/causal-inference-course> | — |
| Cunningham (2021) Causal Inference: The Mixtape | <https://mixtape.scunning.com> | — |
| Hahn and Herren (2025) Regression Adjustment for Causal Inference: A Primer with Examples | <https://drive.google.com/file/d/1nqGqhrR57vF3rRT258QaTSmgnnwDCzio/edit> | — |
| Heckman and Pinto (2015) Causal analysis after Haavelmo | <https://www.jstor.org/stable/24537770> | — |
| Pearl (2013) Reflections on Heckman and Pinto’s “Causal Analysis After Haavelmo” | <http://ftp.cs.ucla.edu/pub/stat_ser/r420.pdf> | — |
| Heckman and Pinto (2022) Causality and econometrics | <https://www.nber.org/papers/w29787> | — |
| Causal Inference is Easy | <https://nothing-so-practical.com/post/causal-inference-is-easy/> | — |
| Causal Inference is Hard | <https://nothing-so-practical.com/post/causal-inference-is-hard/> | — |

## Class 7: More econometric models: i) General linear models: heteroskedasticity, Student’s t errors and autoregressive errors); ii) Hierarchical models; iii) Limited dependent variable models (Tobit, probit, ordered probit, multinomial probit).

| Item | Link | Local copy |
|---|---|---|
| General linear models | <https://hedibert.org/wp-content/uploads/2013/12/GLM3.pdf> | [GLM3.pdf](class-07/materials/GLM3.pdf) |
| Hierarchical linear models | <https://hedibert.org/wp-content/uploads/2013/12/HLM.pdf> | [HLM.pdf](class-07/materials/HLM.pdf) |
| Example from Gamerman and Lopes (2006) – Modeling the nutritional patterns of pregnant women | <https://hedibert.org/wp-content/uploads/2024/11/hierarchicalmodel.html> | [hierarchicalmodel.html](class-07/materials/hierarchicalmodel.html) |
| Limited dependent variable models | <https://hedibert.org/wp-content/uploads/2013/12/limiteddependentvariablemodels.pdf> | [limiteddependentvariablemodels.pdf](class-07/materials/limiteddependentvariablemodels.pdf) |

## Class 8: Introduction to univariate time series econometrics: i) Autoregressive moving average models; ii) Unit root econometrics; iii) Seasonal models; iv) ARCH/GARCH and related models; v) Stochastic volatility models.

| Item | Link | Local copy |
|---|---|---|
| Autoregressive (AR) models and moving average (MA) models | <https://hedibert.org/wp-content/uploads/2017/04/ar-ma.pdf> | [ar-ma.pdf](class-08/materials/ar-ma.pdf) |
| IBM returns, US real GNP business cycles | <https://hedibert.org/wp-content/uploads/2017/04/ar-ma.html> | [ar-ma.html](class-08/materials/ar-ma.html) |
| AR(2): h-step-ahead forecasting | <https://hedibert.org/wp-content/uploads/2024/11/ar2-forecast.html> | [ar2-forecast.html](class-08/materials/ar2-forecast.html) |
| Unit-root nonstationarity and long-memory processes | <https://hedibert.org/wp-content/uploads/2017/04/unitroot.pdf> | [unitroot.pdf](class-08/materials/unitroot.pdf) |
| Random walk, RW with drift, US quarterly GDP, S&P500 returns | <https://hedibert.org/wp-content/uploads/2017/04/unitroot.html> | [unitroot.html](class-08/materials/unitroot.html) |
| Seasonal models | <https://hedibert.org/wp-content/uploads/2017/04/seasonal.pdf> | [seasonal.pdf](class-08/materials/seasonal.pdf) |
| Modeling monthly totals of international airline passengers from 1949-1960 | <https://hedibert.org/wp-content/uploads/2017/05/airpassengers-seasonalmodels.html> | [airpassengers-seasonalmodels.html](class-08/materials/airpassengers-seasonalmodels.html) |
| Glossary of ARCH models | <https://hedibert.org/wp-content/uploads/2021/03/garchmodeling.html> | [garchmodeling.html](class-08/materials/garchmodeling.html) |
| Bayesian GARCH | <https://hedibert.org/wp-content/uploads/2016/04/bayes-garch.pdf> | [bayes-garch.pdf](class-08/materials/bayes-garch.pdf) |
| Stochastic volatility (SV) models | <https://hedibert.org/wp-content/uploads/2022/05/sp500-gaussian-student-SV-models.html> | [sp500-gaussian-student-SV-models.html](class-08/materials/sp500-gaussian-student-SV-models.html) |
| GARCH(1,1) vs SV-AR(1) models with Students t errors | <https://hedibert.org/wp-content/uploads/2021/03/GARCH11-SVar1.html> | [GARCH11-SVar1.html](class-08/materials/GARCH11-SVar1.html) |
| Petrobrás data: ARCH(1), GARCH(1,1) and SV-AR(1) models | <https://hedibert.org/wp-content/uploads/2025/12/garch-sv-petrobras.html> | [garch-sv-petrobras.html](class-08/materials/garch-sv-petrobras.html) |

## Class 9: Introduction to multivariate time series econometrics: i) Factor SV models; ii) Dynamic Conditional Correlation (DCC) models; iii) Vector autoregressive (VAR) models, impulses-response function, structural VAR (SVAR); iv) Large BVAR, Factor-augmented VAR (FAVAR); v) Time-varying parameter (TVP)-VAR; vi) Bayesian VAR (BVAR) and Bayesian FAVAR (BFAVAR).

| Item | Link | Local copy |
|---|---|---|
| Vector autoregressive models (VAR) | <https://hedibert.org/wp-content/uploads/2013/12/BVAR-part11.pdf> | [BVAR-part11.pdf](class-09/materials/BVAR-part11.pdf) |
| Modeling seasonally adjusted GDP – VAR(3) with UK, USA and Canada | <https://hedibert.org/wp-content/uploads/2025/12/VAR-Example.html> | [VAR-Example.html](class-09/materials/VAR-Example.html) |
| Large Bayesian VAR (BVAR), Factor-Augmented VAR (FAVAR), Time-Varying-Parameter-BVAR (TVP-BVAR) & Bayesian FAVAR | <https://hedibert.org/wp-content/uploads/2013/12/BVAR-part2.pdf> | [BVAR-part2.pdf](class-09/materials/BVAR-part2.pdf) |
| Factor Stochastic Volatility (FSV) | <https://hedibert.org/wp-content/uploads/2021/03/sv-fsv-US-BR.html> | [sv-fsv-US-BR.html](class-09/materials/sv-fsv-US-BR.html) |
| FSV x Dynamic Conditional Correlation (DCC) | <https://hedibert.org/wp-content/uploads/2023/04/wti-sp500-timevaryingcovariance.html> | [wti-sp500-timevaryingcovariance.html](class-09/materials/wti-sp500-timevaryingcovariance.html) |

## Class: Final exam

## Bibliography (as listed on the site)

- Basic bibliography
- Mostly Harmless Econometrics: An Empiricist’s Companion (Angrist and Pischke, 2009)
- Analysis of Financial Time Series, 3rd Edition (Tsay, 2010)
- An Introduction to Statistical Learning (James, Witten, Hastie and Tibshirani, 2023) – https://www.statlearning.com
- Introduction to Bayesian Econometrics (Greenberg, 2013)
- Additional bibliography
- Introduction to Econometrics, 3rd edition (Stock and Watson, 2010)
- Introductory Econometrics: A Modern Approach (Wooldridge, 2012)
- Time Series Analysis (Hamilton, 1994)
- Aprendizado de Máquina: Uma Abordagem Estatística (Izbicki and Mendonça, 2020) – https://tiagoms.com/publications/ame
- Estatística e Ciência de Dados (Morettin and Singer, 2021) – https://www.ime.usp.br/~pam/cdadosf3.pdf
- Introduction to Modern Bayesian Econometrics (Lancaster, 2004)
- Bayesian Econometric Methods, 2a edição (Chan, Koop, Poirier and Tobias)
- Bayesian Statistics and Marketing (Rossi, Allenby and McCulloch, 2005)
- Time Series: Modeling, Computation, and Inference (Prado and West, 2010)
