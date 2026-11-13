# Topic lists L01–L09: upgrade to the current global exercise rules — plan (2026-11-12)

User decisions (asked 2026-11-12): **upgrade in place** (keep verified statements, solutions, check
scripts); **add book exercises where they exist + original exercises for confirmed gaps**.

## Rules applied (global `~/.claude/CLAUDE.md`)

1. Every exercise block opens with its source: book, chapter, exercise number, printed page with
   the PDF page in brackets, and whether the source gives the answer.
2. The statement is complete: anything it refers to (earlier problem, example, table, figure values)
   goes in the same block. Referenced worked examples are given as a short "Referenced material"
   summary (model, data set, variables, the numbers needed) with page refs, not copied wholesale.
3. Statements keep the source wording (existing statements are already verbatim; do not retype).
4. Original exercises carry `Origin: original exercise on <topic>, built on <slides / section, pages>`,
   never a book source line, and are solved like the others.

## Work per unit (one agent each; owns only its files)

Files: `Listas/lista-LNN-book-exercises.tex` (+ both PDFs), `Listas/LNN-book-exercises-check.py`,
data in `Listas/data/`. Temp build names `_gab-LNN.tex` (never shared).

| Unit | Additions |
|---|---|
| L01 | original: p-hacking / reproducibility |
| L02 | none known; report any uncovered goal |
| L03 | originals: sparsity priors (horseshoe, normal–gamma); HMC |
| L05 | book: errors-in-variables (W §9.4); originals: DAGs + d-separation, Simpson's paradox |
| L07 | book: ordered / multinomial probit (G Ch. 8) if it exists, else original |
| L08 | book: stochastic volatility (T Ch. 12 beyond 12.3); original: Bayesian GARCH |
| L09 | originals: large BVAR (Minnesota), FAVAR, TVP-VAR, factor SV |

## Verification (per unit)

- Every `\fonte{}` has printed + [PDF] page and the answer flag; every original has `Origin:`.
- `python Listas/LNN-book-exercises-check.py` passes (new exercises' numbers asserted).
- List and answer-key PDFs compile; `pdffonts` shows Type 1 only.

Lead, at the end: `Map/exercises-index.md` and `Map/class-plan.md` Practice lines updated.

## Status — 2026-11-12

Done for all 7 units: 133 questions (was 119); every `\fonte` has printed + [PDF] page and the
answer flag (no book on disk prints answers; Wooldridge App. F answers only in-text questions);
11 originals with `\origem`; new book exercises W 9.7 (L05), I 5.4 (L02), T 12.4 (L08, data
`Listas/data/L08-m-fsp6508.txt`). All 14 PDFs Type 1 only. `Map/class-plan.md` Practice lines
and `Listas/data/README.md` updated; `Map/exercises-index.md` already listed the new book items.

Correction: ISLP (2023) Ch. 13 has multiple-testing exercises (FWER, Bonferroni, Holm), so the
p-hacking topic was not book-less; the original stays and cites ISLP Ch. 13.

## Round 2 — 2026-11-13 (user: book first, then originals; replace the p-hacking original by ISLP 13)

Done: L01 25 questions (I 13.1, 13.8 replace the original; B 6.11, I 6.8, W 11.4, T 8.5; originals
U(0,θ) estimators and bootstrap for the max); L03 34 (G 3.5–3.6, KPT 12.2, 6.7; originals hierarchical
Beta–Binomial, sequential updating, physicists A–D); L05 20 (MHE Table 7.2.1; original MLDA RDD);
L07 19 (W 8.C12; KPT 12.2 + original part (d) nutrition data); L08 19 (T 3.13, 3.9; original t-SV);
L09 19 (Hamilton 11.5, KPT 16.4; original non-recursive SVAR). L02 unchanged (20). Books outside the
course bibliography (KPT, Hamilton) and syllabus-map exceptions (ISLP Ch. 13, MHE Ch. 7) are flagged
in each source line. Also on 2026-11-13: 7 hard conceptual quizzes
`Simulados/quiz-LNN-conceptual-hard-2026-11-13.md` (validator PASS); HW2 solution notebooks now
quote each item's statement right before its solution. Still uncovered: numerical TVP-VAR with SV.

## Gaps reported by the unit agents in round 1 (resolved in round 2 above)

- L01: four U(0,θ) estimators; parametric bootstrap and the failure for the maximum; frequentist
  Poisson change point (profile likelihood, LR); variable selection; AR(1) unit root; VAR(1).
- L03: hierarchical Beta–Binomial / Gaussian; Beta–Bernoulli and discrete-prior updating;
  physicists A–D four priors; Bayes estimators under absolute and 0–1 loss; posterior model probs.
- L05: SUTVA, CATE, QTE; the drinking-age RDD application.
- L07: heteroskedasticity and WLS/GLS; nutrition hierarchical example / partial pooling.
- L08: GARCH variants (T 3.13 exists, data on disk); Student-t SV.
- L09: non-recursive SVAR; FEVD; SSVS; numerical TVP-VAR with SV.
