# Book-exercise list: Poisson and Monte Carlo methods for inference — plan (2026-10-31)

Command: `/exam-gen` (`.claude/commands/exam-gen.md`), answers given 2026-10-31:

| Question | Answer |
|---|---|
| Source | book exercises, **plus original math and conceptual questions** (user, 2026-10-31, replacing "book exercises only") |
| Per block | (i) the book exercises with their programming parts; (ii) ≥ 1 original **math** exercise (derivation or proof, symbolic, with parameter analysis); (iii) ≥ 1 original **conceptual** question in exam-gen objective form (MC 3 pts + V/F 2 pts, traps on converses, answer position spread). Original items are labelled "Original question" in their source line, never disguised book exercises. |
| Depth | in depth (proofs) |
| Math | heavy (derivations, asymptotics, MC-estimator variance, proofs, limits) |
| Tangential | change point + LR test; bootstrap; Bayesian Gamma–Poisson; MCMC (Gibbs/MH) |
| Format | discursive (book problems), full solutions |
| Programming | **every exercise also a programming exercise** (user, 2026-10-31): after the verbatim statement, an added part "Programming (added, not in the book)" — implement the estimator/test/sampler in Python and verify the proved result numerically (simulation, quadrature, coverage); its code + output in the answer key; plus a comment-only scaffold notebook `Listas/lista-poisson-monte-carlo.ipynb` (one cell per programming part, like the HW1 scaffold) |

Binding rules: global "Exercise lists built from real exercises" (`~/.claude/CLAUDE.md`) and
`rules/00_estilo_avaliacao.md` (Equations/notation rule; Book-questions rule). Books allowed
(`rules/09_course_program.md`): B, G, I (ISLP), T, W, MS. Not Koop–Poirier–Tobias.

## Blocks (target 16–22 exercises, ordered from Poisson basics to MCMC)

1. Poisson likelihood: sufficiency, MLE, invariance, Fisher information, Cramér–Rao, UMVU, consistency (B Ch. 1–3).
2. Poisson tests and intervals: LR test, Wilks, pivotal/asymptotic intervals (B Ch. 5–6).
3. Change point + LR test (G 7.x; B profile likelihood if an exercise exists).
4. Bayesian Gamma–Poisson: conjugacy, predictive, Bayes estimators (G 2.x/3.x; B Ch. 4).
5. Monte Carlo for inference: MC integration and its variance, accept–reject, importance sampling, simulation of estimator properties (MS App. B; G Ch. 5; B if any).
6. Bootstrap (I 5.x; MS B.6).
7. MCMC: Gibbs, Metropolis–Hastings, switch-point Gibbs (G Ch. 6–7; MS App. C; T 12.x).

Overlap with `Listas/lista-L01-book-exercises.tex` / `lista-L03-…` is allowed (this list must
stand alone); reuse their verified solution text where an item repeats, and prefer items not
already there when two cover the same point.

## Outputs

`Listas/lista-poisson-monte-carlo.tex`, `.pdf`, `-gabarito.pdf`, `Listas/poisson-monte-carlo-check.py`.
Temp answer-key file `_gab-pmc.tex`.

## Verification

Both PDFs compile; `pdffonts` Type 1 only; check script asserts every printed number and
verifies proofs' closed forms numerically (quadrature / simulation with seeds).
