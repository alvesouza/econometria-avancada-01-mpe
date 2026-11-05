---
description: Build a Jupyter project that answers a question about a course topic — plans the notebook cell by cell, calls /lab-init to scaffold and /lab-data for any series, writes the analysis and figures, then runs it end to end and verifies the numbers against an independent path. Asks goal, data, depth and figure destination first.
argument-hint: <topic-question-lecture-or-exercise> [--lecture N] [--data|--no-data] [--for-latex] [--plan-only]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit NotebookEdit AskUserQuestion
---

Build and run the notebook that answers `$ARGUMENTS`.

This is the orchestrator: it plans, delegates the scaffold to `/lab-init` and the data to
`/lab-data`, writes the actual economics, executes the notebook, and verifies the results.
A notebook is not delivered until it runs clean from a fresh kernel.

## Instructions

### Step 1: Ask — one round, before planning

Four questions, with the recommendation pre-filled from `$ARGUMENTS` and from what the project
already holds:

1. **Goal** — what should the notebook accomplish?
   - *Visualise a mechanism* the lecture derives — the figure is the deliverable.
   - *Replicate* a book figure, table or calculation, to check understanding against Kurlat.
   - *Calibrate and simulate* — put numbers through the model and trace the dynamics.
   - *Confront the model with data* — does the relation hold in observations?
2. **Data** — real series (and which family: international, Brazil, PWT/Maddison), or stay
   analytical and synthetic? Real data means `/lab-data` and a provenance registry; say so.
3. **Depth** —
   - *One figure* — a single question, one chart, ten cells.
   - *A worked exercise* — a Kurlat item or lista question end to end, with verification.
   - *A study project* — several sections, several figures, a written conclusion.
4. **Figure destination** — screen only, or embedded in a LaTeX document later? This decides the
   matplotlib backend and whether the font rule applies (see `/lab-init` Step 5). Getting it
   wrong means either invisible figures in Jupyter or Type 3 fonts in the PDF.

### Step 2: Read before planning

Never plan an analysis of a topic you have not read in this session.

1. `CLAUDE.md` — scope guard, notation, code language.
2. The topic's `rules/NN_*.md` — formulas, signed comparative statics, the **code patterns**
   section (start from its Python, do not reinvent it), and *"Armadilhas frequentes"*: each trap
   is a candidate for something the notebook should demonstrate rather than assert.
3. `Map/books-index.md` for the Kurlat chapter, section and **printed page** (offset 0, so
   printed = PDF); any reading map for the lecture; `Map/topics-index.md` for prerequisites.
4. The lecture material in `Aula/` and the lista in `Listas/`. **Slide PDFs converted by
   markitdown scramble two-column algebra — read the PDF for any derivation you will implement.**
5. `Resolucao/kurlat_ch*_codigo/*_numerico.py` and `*_figuras.py` for this chapter. **Reuse
   them.** They were verified against independent solution paths and their figures already
   appear in compiled documents. Re-deriving the same curve is how two versions of the truth
   get into one project.

### Step 3: Plan, and show the plan

Write the plan as a numbered **cell-by-cell outline**: for each cell, its type, its title, what
it computes or draws, and — for every figure — what the reader should conclude from it. State:

- the **question** in one sentence, and what answer would count as surprising;
- the **parameters** and where each comes from;
- the **verification** strategy: for each headline number, the independent path that will
  confirm it (closed form, limiting case, steady state, accounting identity);
- which **series** are needed, if any, and therefore what `/lab-data` must fetch;
- what is deliberately **out of scope** for this notebook.

Show it to the user before building. `--plan-only` stops here. Cells are cheap to re-plan and
expensive to debug after the fact.

### Step 4: Delegate the scaffold and the data

- `/lab-init` for the directory, the notebook skeleton, the figure style, the requirements and
  the `Notebooks/README.md` row. Pass the slug, the lecture and the kind.
- `/lab-data` for every series, **before** writing analysis cells, so the loader cell is written
  against a cache that exists and whose units are known.

Do not reimplement either. If something they produce is wrong for this project, say so in the
report rather than working around it silently — that is a bug in a shared command.

### Step 5: Write the analysis

Fill the skeleton, in the house idiom:

- **The economics goes in markdown cells**, not in comments. State the model, its assumptions
  and the equation being solved, in LaTeX, with the Kurlat page. A reader should be able to
  follow the argument without reading the code.
- **Code cells are functions plus one call.** No side effects buried in a plotting cell, no
  parameter redefined halfway down.
- **Every parameter carries its source** in a comment. No bare literals in a calibration.
- **After every figure, a markdown cell** saying what it shows and what would change it. If you
  cannot write that sentence, the figure does not belong in the notebook.
- **Notation follows Kurlat.** Where the slides diverge, say which you use, in the first cell.
- **Scope guard**: nothing from Kurlat ch. 8 or chs. 12–15, no stochastic DSGE, no Bellman or
  dynamic programming, no stochastic RBC, no time-series econometrics, no Calvo NKPC, nothing
  from Ljungqvist & Sargent. A notebook is not a loophole for machinery the course excludes.

### Step 6: Run it, and verify

```bash
cd "Notebooks/<slug>"
jupyter nbconvert --to notebook --execute --inplace "<slug>.ipynb"
```

`papermill` is **not installed**; `nbconvert` is. A non-zero exit is a failure, not a warning.

- **Fix the notebook, never the assertion.** If verification fails, the model or the code is
  wrong; loosening the tolerance to make it pass is falsification.
- Check each headline number against its independent path, as planned. The project's existing
  solution code aborts on disagreement — match that standard.
- Confirm the notebook still opens cleanly:
  `python -c "import nbformat; nbformat.read(open(p, encoding='utf-8'), as_version=4)"`.
- If figures are for LaTeX, export them and run `pdffonts` on each: every font Type 1, no Type 3.
- **A notebook that did not execute clean is not delivered.** Report the failure instead.

### Step 7: Report

| Item | Detail |
|---|---|
| Notebook | path, cell count, executed ✅/❌ |
| Question | the one-sentence question and the answer found |
| Figures | path and the one-line reading of each |
| Series | key, source, units, rows, fresh/cache/offline |
| Verified | each headline number and the independent path that confirmed it |
| Uncertain | what could not be verified, and why |

Then offer, without assuming: a figure exported for a `Resolucao/` document, a `/speechify`
narration of the findings, an `/explainer` video of the mechanism, or a `/quiz-gen` question set
from what the notebook showed.

## Worked examples — the pattern, not the limits

- **Solow convergence and the Golden Rule** (Kurlat ch. 4, pp. 53–72) — pure simulation: the
  diagram, a transition path, and the consumption hump whose peak is *not* the competitive
  steady state.
- **Development accounting on PWT** (Kurlat ch. 5, pp. 75–93) — data: decompose output per
  worker into capital, human capital and the residual, then ask how big the residual is.
- **Baumol-Tobin money demand** (Kurlat §10.4, pp. 199–202; Lista 6) — both: the sawtooth cash
  path, the cost-minimising number of trips, and the income and interest elasticities of ½ and −½.
- **Money growth and inflation** (Kurlat ch. 11, pp. 205–222; Lista 6 Q2) — both: $\pi = \mu -
  \eta g$, the targeting arithmetic under $\eta = \tfrac{1}{2}$ versus $\eta = 1$, and the
  cross-country long-run scatter.
- **The inflation Laffer curve** (Kurlat §11.3, p. 215; exercise 11.6, p. 219, Cagan demand) —
  revenue against inflation, and the peak past which more inflation raises less.

## Important

- **Plan before building, and show the plan.** The questions in Step 1 change every cell.
- **Delegate, do not duplicate.** `/lab-init` owns the scaffold; `/lab-data` owns the network.
  This command owns the economics.
- **Reuse `Resolucao/` code** before writing new geometry for a figure that already exists.
- **Verification is the deliverable's backbone.** A notebook that prints numbers nobody checked
  is a liability: it looks authoritative and is unfalsified.
- **Reproducible**: fixed seed, no hidden state, no network in analysis cells, clean top-to-bottom run.
- **Missing data is reported, never approximated.** Synthetic data is labelled `SYNTHETIC` in the
  figure title, not only in the registry.
- **English** in code, comments and markdown cells; math in LaTeX; never a bare `$` for currency.
- **Do not reproduce exercise statements** — number and page, as `/exercise-plan` does.

## Ecosystem

- `/lab-init` → the scaffold. `/lab-data` → the series and their provenance. This command uses both.
- `/solution`, `/book-solutions` → where a verified result becomes written-up mathematics; a
  notebook's figure can be exported straight into those documents.
- `/explainer` → animates a mechanism a notebook made static.
- `/quiz-gen` → turns a result into self-assessment.
- `/study-pack`, `/exercise-plan` → the reading and practice around the topic.
- `/setup-study` copies this command into new study projects.
