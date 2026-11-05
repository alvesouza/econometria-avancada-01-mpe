# HW1 (Advanced Econometrics 2026): solution and report in the notebook — plan (2026-11-02)

Target: `Listas/hw1-advancedeconometrics-2026.ipynb` (comment-only scaffold, 39 cells).
Statement: `Listas/hw1-advancedeconometrics-2026.pdf` (Portuguese; report written in English per global rule).

## Steps

1. Replace every comment-only code cell with working Python (numpy, pandas, scipy, statsmodels, matplotlib),
   keeping the cell order and ids. No new dependencies.
2. Rewrite the markdown cells as the report: each question opens with a header "Question k",
   each item with "Answer k(x)", and a one-line result (numbers) before the discussion.
   Plain prose, no em-dashes, no filler phrases.
3. Break point: tau = 84 (Dec 2021), justified by the annual means and the Poisson profile
   likelihood (maximiser tau = 86, Feb 2022). Sensitivity: tau in {70, 72, 86, 96}.
4. Execute the notebook in place (nbconvert) and fill the numbers in the markdown from the outputs.

## Verification

- Notebook runs top to bottom with no errors (nbconvert --execute).
- Every number quoted in markdown matches a printed output.
- Optional item 6: optimiser result cross-checked against statsmodels GLM identity link.
