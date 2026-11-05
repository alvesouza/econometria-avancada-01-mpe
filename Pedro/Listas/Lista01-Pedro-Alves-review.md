# Lista 01 (HW1) — review of the graded submission (50/100)

Submission: `Pedro/Listas/Lista01-Pedro-Alves (1).pdf` (8 pages, nbconvert export of `Lista01-Pedro-Alves.ipynb`).
Statement: `Listas/hw1-advancedeconometrics-2026.pdf` (Questions 1–5 required, Question 6 optional).

The returned PDF carries no grader marks or comments, so the breakdown below is a
reconstruction: equal weight per question (20 pts each for Q1–Q5) and equal weight per
sub-item, checked against the statement's own verbs. It lands on 50, which fits the grade.

## Estimated breakdown

| Q | Est. pts | Main loss |
|---|---|---|
| 1 | 12/20 | Wrong skew direction; tails, typical values and atypical months not discussed |
| 2 | 14/20 | (a) asks to *write* $L(\mu,\sigma^2;y)$ and *obtain* the MLEs: only $\ell$ shown, no scores |
| 3 | 13/20 | (a) "Mostre que" without a proof; (c) wrong reading of the interval; (d) statistic called a p-value; (e) no interpretation |
| 4 | 11/20 | Dates of the break wrong, autocorrelation claimed but not computed, atypical months missing |
| 5 | 0/20 | **Missing entirely** (5 sub-items: estimates, CIs/LR tests, sensitivity to $\tau$, dispersion by part) |
| **Total** | **~50** | |

## Item by item

### Q1 — Histogram (asked: shape, typical values, dispersion, atypical values; mean, median, variance, s.d.)
- Four statistics reported correctly.
- "O histograma é levemente deslocado para a esquerda" — wrong or at best ambiguous. The data are **right-skewed** (long right tail, mean 30.91 > median 30). A grader reads "deslocado para a esquerda" as left skew.
- Tails, typical values (e.g. half the months between 24 and 38) and atypical values (no outlier rule applied; Jun 2020 = 13, Dec 2024 = 56) are not discussed. Four aspects were requested; about one and a half were covered.

### Q2 — Gaussian model
- (a) The statement says "Escreva a função de verossimilhança $L(\mu,\sigma^2;y)$ e obtenha os EMV". The answer writes only $\ell$ and jumps to the result ("Zerando as derivadas, a gente chega em…"). Missing: $L$ as a product, the two score equations, solving them, the second-order check.
- (b) Correct.
- (c) Plot correct. The comment is right in substance but one sentence long, with a garbled clause ("que a variância cresce junto com a média").

### Q3 — Poisson model
- (a) "**Mostre que** $\hat\lambda = \bar y$" asks for a proof. Missing: $L(\lambda)$, $\ell'(\lambda)=\sum y_t/\lambda - n$, $\ell''<0$, $I(\lambda)=E[-\ell'']=n/\lambda$ derived (not asserted), asymptotic normality → se.
- (b) Correct.
- (c) "concentrada mais no intervalo de um desvio-padrão (+-): [21, 41]" is wrong. $[21,41]$ is roughly $\bar y \pm s$ with the **sample** s.d. (9.6). The Poisson s.d. is $\sqrt{30.9}=5.6$, so under the model $[21,41]$ is about $\pm 1.8$ Poisson s.d. The comparison itself (0.942 vs 0.729; tails 0.025/0.033 vs 0.136) is right; the label is not. "caldas" should be "caudas".
- (d) "teste de dispersão $D \approx 3\times10^{-29}$" confuses the **statistic** ($D = 414.8$, $\chi^2_{139}$) with its **p-value** ($3\times10^{-29}$). It is a conceptual error, not a typo. "O que isso sugere sobre a adequação do modelo?" is only half answered.
- (e) Only the AIC numbers. Missing: why the Gaussian wins (its free variance absorbs the overdispersion), that neither model is adequate, and the density-vs-probability caveat.

### Q4 — Time series (asked: level, trend, seasonality, regime changes, atypical months; discuss i.i.d.)
- Plot fine, but no smoother or yearly means drawn on it to support the claims.
- "De 2015 a 2020 a média ficava na casa dos 25 a 27" — the printed yearly means contradict it (2015: 29.58, 2018: 28.92).
- "De 2021 em diante … a média disparou" — 2021 is 26.08; the jump is in **2022** (34.67).
- "Um mês alto tende a ser seguido por outro mês alto" — asserted, never computed (lag-1 autocorrelation = 0.375 vs band ±0.166).
- Atypical months (2020: 40 in May, 13 in June; Dec 2021 = 17) not discussed.
- Causal story ("pós-pandemia/boom de entregas", "festas de fim de ano") stated as fact with no evidence; label it a hypothesis or drop it.

### Q5 — Structural break: missing
This is the question the whole list builds up to, with five sub-items. The short notebook had it (choice of $\tau=84$, normal and Poisson estimates per part, $t$ and Wald CIs, LR tests 144.25 and 63.60, sensitivity table and profile likelihood, dispersion by part); it did not reach the submission.

## Report-level problems
- **Answers too terse for a report.** The statement asks for "um relatório com gráficos, tabelas de estimativas e comentários". The answers are one line each, and most comment items do not cite the numbers the code printed. Part of this came from the "less detailed" short version: it removed the derivations that "Escreva…" and "Mostre que…" require. A shorter version should cut prose, never required steps.
- **No question context.** Removing the statements leaves bare "Resposta 2(a)" headings; the reader cannot tell what each item asks without the PDF next to it.
- **Register and spelling.** Informal ("a gente chega", "rola um pico", "Deixa à desejar" → "deixa a desejar") and typos ("distribuiçao", "caldas", "consideravel", "proximo", "frequencia", "valida", "sazional").
- **Code-heavy layout.** The PDF is mostly code cells; tables are raw `print` output. Figures have no captions or numbers to refer to.

## How to get the points back (ranked by points recovered)
1. Answer every required question. Check the statement item by item before exporting; Q5 alone was ~20 pts.
2. Treat the verbs literally: *Escreva/Mostre/Obtenha* → full derivation (likelihood, log-likelihood, score, solve, second-order check, information); *Calcule* → formula, numbers in place, result; *Teste* → $H_0$, statistic, reference distribution and df, p-value, decision.
3. Answer every aspect a comment item lists, each with a number from the output (Q1 has four, Q4 has five).
4. Check each sentence against your own output before submitting (2021 vs 2022, 25–27 vs 29.6, skew direction).
5. Keep statistics and p-values, sample s.d. and model s.d., apart in the wording.
6. Write the report for a reader: short statement of each question, formatted tables, figure titles, formal Portuguese, spell-check.

Use `/report-grade` on the next submission before exporting the PDF.
