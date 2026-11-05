---
description: Scaffold a Jupyter project for simulating or visualising a course topic — notebook skeleton with titled cells, data/ and figures/, the shared matplotlib style, pinned requirements, and a row in the Notebooks/ index. Wires the project to its lecture, its rules file and its Kurlat pages.
argument-hint: <slug-or-topic> [--lecture N] [--kind model|data|both]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit NotebookEdit AskUserQuestion
---

Create a notebook project for the topic in `$ARGUMENTS`, under `Notebooks/<slug>/`.

This command builds the **container**, not the analysis. It produces a notebook whose cells
are already titled and ordered, wired to the right lecture and the right Kurlat pages, with
the figure style and the data interface in place. `/lab` fills it in; `/lab-data` feeds it.

Run it on its own when you want a clean workspace to think in. Run `/lab` instead when you
want the finished analysis.

## Decisions already settled — do not ask these

- **Python / Jupyter.** `CLAUDE.md` sets the project's code language: *"Python
  (numpy/pandas/matplotlib). Sem R."* There is no R path.
- **Location**: `Notebooks/<slug>/`, one directory per project, parallel to `Listas/`,
  `Leituras/` and `Resolucao/`.
- **No data fetching here.** Network access belongs to `/lab-data`, which caches to
  `data/` and records provenance. A notebook's analysis cells read from disk, never from a URL.

## Verified environment — measured 2026-09-12, rely on it but re-check on failure

| Available | Not available |
|---|---|
| Python **3.12.10** | **pyarrow** — so parquet is optional, CSV is the baseline |
| numpy 2.4.2 · pandas 3.0.3 · matplotlib 3.10.8 · scipy 1.17.1 | **papermill** — use `jupyter nbconvert --execute` |
| statsmodels 0.14.6 · requests 2.34.2 · openpyxl 3.1.5 | |
| nbformat 5.11.0 · jupyterlab 4.6.2 · nbconvert 7.17.1 | |
| ffmpeg/ffprobe, MiKTeX (`pdflatex`, `dvisvgm`) | |

Note `Path.read_text(newline=...)` does **not** exist on 3.12 — use `open()` when newline
control matters. This bites on Windows line endings.

## Instructions

### Step 1: Ask only what cannot be inferred — one round

Infer as much as possible from `$ARGUMENTS` first, then ask once, with the inference
pre-filled as the recommended option:

1. **Slug and title** — the directory name (`kebab-case`, no spaces, no accents) and the
   human title for the notebook's header cell. Propose both from `$ARGUMENTS`.
2. **Which lecture or topic** (1–9) — this decides the `rules/*.md` file, the Kurlat chapter
   and printed pages, and the notation. Infer from the topic words; confirm.
3. **Kind** —
   - *model* — simulation and comparative statics only; no data, no network.
   - *data* — empirical: series, calibration against observations, cross-country work.
   - *both* — a model confronted with data. The most useful and the most work.

If `$ARGUMENTS` already names all three unambiguously and the user said "no questions",
proceed. Otherwise ask — a scaffold pointed at the wrong lecture wires in the wrong rules
file, the wrong notation and the wrong pages, and every later cell inherits the error.

### Step 2: Read the course context before writing a single cell

1. `CLAUDE.md` — scope guard, notation, language, code conventions.
2. The lecture's `rules/NN_*.md` — the formulas, the signed comparative statics, the **code
   patterns section** (most rules files already carry runnable Python for their topic; the
   parameters cell should start from it, not from invented numbers), and the
   *"Armadilhas frequentes"* list.
3. `Map/books-index.md` — the Kurlat chapter, section and **printed page**. Kurlat's offset
   is 0, so printed page = PDF page. Benigno is paginated 503–524 (`pdf = printed − 502`).
4. `Resolucao/kurlat_ch*_codigo/` for the same chapter — `*_numerico.py` and `*_figuras.py`.
   **If the geometry you need already exists there, the notebook imports or adapts it rather
   than re-deriving it.** That code was verified against independent solution paths; yours is not.

### Step 3: Create the directory

```
Notebooks/<slug>/
├── <slug>.ipynb          ← the notebook, cells titled and ordered
├── README.md             ← what it answers, which lecture, which pages, how to run
├── estilo_mpl.py         ← the shared figure style (copied, not invented)
├── requirements.txt       ← pinned to what the notebook actually imports
├── data/                 ← /lab-data writes here; .gitkeep so the dir survives
└── figures/              ← exported figures
```

Create `data/.gitkeep` and `figures/.gitkeep` so empty directories survive git.

### Step 4: Write the notebook skeleton

Build valid **nbformat 4** JSON and write it with explicit UTF-8, or use `NotebookEdit`.
Verify it opens without repair: `python -c "import nbformat; nbformat.read(open(p, encoding='utf-8'), as_version=4)"`.
A notebook Jupyter offers to "repair" is a broken deliverable.

The cells, in this order, each pre-titled with a markdown heading:

| # | Type | Content |
|---|---|---|
| 1 | markdown | **Title** · lecture number and name · Kurlat anchor with printed pages · the `rules/` file · the date · one sentence on the question it answers |
| 2 | markdown | **Assumptions** — what the model takes as given, in the lecture's own terms, and what it deliberately excludes |
| 3 | code | **Imports and reproducibility** — imports, `np.random.default_rng(SEED)` with `SEED` named, pandas display options, and the printed versions of numpy/pandas/matplotlib so a stale run is self-identifying |
| 4 | code | **Parameters** — every parameter on its own line, each with a comment giving its **source** (`rules/` formula, Kurlat page, a calibration, a `/lab-data` series). No bare literals |
| 5 | markdown | **The model** — the equations in LaTeX, as the lecture writes them, with the Kurlat page |
| 6 | code | **Implementation** — functions only, no side effects, each with a docstring naming the equation it implements |
| 7 | code | **Verification** — the cell that makes the notebook trustworthy. Check each result against an independent path: a closed form, a limiting case, a known steady state, an accounting identity. `assert` with a tolerance and a message. **It must fail loudly, not print a warning** |
| 8 | code | **Results** — the numbers, as a small labelled DataFrame, not loose prints |
| 9 | code | **Figures** — one figure per cell, each followed by… |
| 10 | markdown | …**what the figure shows** and what would change it. A figure with no reading is decoration |
| 11 | markdown | **What this shows** — the conclusion in three sentences, and the one thing that would overturn it |

For `kind=data` or `both`, insert after cell 4 a **Data** section: a markdown cell naming the
series and their provenance, and a code cell that loads **only from `data/`** — with a clear
error telling the user to run `/lab-data` if the cache is absent. Never fetch in the notebook.

### Step 5: Copy the figure style — do not invent one

Copy `Resolucao/kurlat_ch09_codigo/estilo_mpl.py` verbatim into the project. It sets the
**pgf** backend with `lmodern` + `cmap` so text in an exported PDF stays copyable — the global
rule in `~/.claude/CLAUDE.md`, and the reason `TEXTWIDTH_IN = 16.2 / 2.54` matches the
documents' text width.

Then document both paths in the notebook, because they conflict:

- **On screen** (the normal case): do **not** import `estilo_mpl`. The pgf backend renders
  nothing inline, so importing it makes every figure invisible in Jupyter. Use the default
  backend and a plain `rcParams` tweak for readable sizes.
- **Exporting for a LaTeX document**: import `estilo_mpl` **before** `matplotlib.pyplot`, in a
  separate export cell or a small script, and save to `figures/*.pdf`. Then check the fonts:

```bash
pdffonts figures/fig_name.pdf     # every font Type 1; no Type 3, "uni" column yes
```

Put that command in the notebook's export cell as a comment, and in the project README.

### Step 6: Pin requirements

Write `requirements.txt` listing only what the notebook imports, at the versions actually
installed (read them; do not guess). Mark optional extras as comments — `pyarrow` for parquet
and `papermill` are **not installed**, so nothing may depend on them without saying so.

### Step 7: Check the environment, report, do not install

Verify and report, in a table: the Python version, that `jupyter` and `nbconvert` are
reachable, and which required imports are present or missing. If something is missing, print
the exact install command and let the user decide. **Never install silently** — this is their
interpreter, shared with the rest of the project.

### Step 8: Register the project

Create `Notebooks/README.md` on first run, as an index table: project, lecture, kind, what it
answers, its Kurlat anchor, and status. Add a row per project afterwards. Also confirm
`.gitignore` covers `data/` caches and `.ipynb_checkpoints/` — check with
`git check-ignore -v <path>` rather than assuming.

Then report:

| Created | Path |
|---|---|
| Notebook | `Notebooks/<slug>/<slug>.ipynb` (N cells) |
| … | |

Plus the lecture and Kurlat pages it was wired to, the parameters it starts from and their
sources, what is missing from the environment, and the next command to run (`/lab-data` if it
needs series, `/lab` to fill in the analysis).

## Important

- **The scaffold is wired to the course or it is worthless.** A notebook that cannot say which
  lecture, which rules file and which printed pages it implements is a loose script.
- **Every parameter carries its source.** A bare `0.3` in a calibration is a defect; `alpha =
  0.30  # capital share, rules/02 calibration` is not.
- **The verification cell is not optional.** The project's existing solution code checks every
  result by an independent path and aborts on disagreement; a notebook that only prints is
  weaker than the code already in `Resolucao/`.
- **Reproducible means reproducible**: fixed seed, no hidden state, runs top to bottom from a
  clean kernel, no network in analysis cells.
- **Scope guard** (`CLAUDE.md`): nothing from Kurlat ch. 8 or chs. 12–15, no stochastic DSGE,
  no Bellman or dynamic programming, no stochastic RBC, no time-series econometrics, no Calvo
  NKPC, nothing from Ljungqvist & Sargent. A notebook is not a loophole.
- **English** in code, comments, markdown cells and variable names (global rule), even though
  the course runs in pt-BR. Math in LaTeX; never a bare `$` for currency.
- **Do not reproduce exercise statements** — cite number and page, as `/exercise-plan` does.
- Windows: the repo path contains spaces, so quote every path; be explicit about UTF-8 on
  every file write.

## Ecosystem

- `/lab-data` → fetches and caches the series this project's `data/` expects, with provenance.
- `/lab` → the orchestrator: calls this command, then `/lab-data`, then writes and runs the
  actual analysis. Use `/lab` unless you specifically want an empty workspace.
- `Resolucao/kurlat_ch*_codigo/` → verified figure geometry and numerics. Reuse before rewriting.
- `/solution`, `/book-solutions` → where a notebook's result becomes written-up mathematics.
- `/explainer` → turns a notebook's figure into an animated, narrated explanation.
- `/setup-study` copies this command into new study projects.
