# Econometria Avançada — MPE (Insper)

Study project for *Econometria Avançada* (Mestrado Profissional em Economia, Insper). Topics: causal inference (IV, potential outcomes, panel, DiD), time series (ARIMA, cointegration, GARCH, state space, VAR), statistical learning (logistic regression, validation) and Bayesian methods (conjugate analysis, MCMC, sequential Monte Carlo). Code: Python (the lecturer's R examples are ported).

Course programme, lecture × book map and bibliography: [rules/09_course_program.md](rules/09_course_program.md). Books found / missing: [Livros/BOOKS.md](Livros/BOOKS.md).

## Structure

| Dir | Purpose |
|---|---|
| `Aula/` | lecture slides and class scripts |
| `Listas/` | exercise lists; `lista-exam.tex` (LaTeX template, `\ifsolucoes` toggles blank list vs. key + rubric) |
| `Livros/` | textbooks + `BOOKS.md` |
| `Monitoria/` | tutorial material |
| `Simulados/` | quiz MD files for `quiz.html` |
| `Resolucao/` | generated solutions |
| `Leituras/` | chapter extracts and `/speechify` narrations |
| `Map/` | Obsidian cross-reference maps (`/study-map`) |
| `NotebookLM/` | prompts in `slides/`, `audio/`, `video/`; upload-ready originals in `sources/` |
| `Videos/` | one subdir per `/explainer` video (created on first use) |
| `rules/` | `00`–`09`: course rules; the rest are Efficient Token governance packs |
| `.agent/` | `plans/` (write before non-trivial changes), `notes/` (persisted findings) |
| `tools/` | Efficient Token tooling: `sync_rules.py`, `token_report.py` |

## Commands

| Command | Example |
|---|---|
| `/convert` | `/convert Aula/` — lecture PDFs to Markdown |
| `/summarize` | `/summarize Aula/` |
| `/list-exercises` | `/list-exercises Listas/` |
| `/solution` | `/solution Listas/lista-1.md` |
| `/exam-gen` | `/exam-gen IV, diff-in-diff` — exam-style list + key & rubric (LaTeX); asks depth, tangential topics and math level first |
| `/exam-grade` | `/exam-grade Listas/lista-1.tex Resolucao/my-answers.pdf` |
| `/exercise-plan` | `/exercise-plan GARCH, cointegration` — real book exercises (number + page), weighted by subtopic |
| `/quiz-gen` | `/quiz-gen Simulados/` |
| `/quiz-analyze` | `/quiz-analyze <paste results>` |
| `/study-map` | `/study-map .` |
| `/notebooklm` | `/notebooklm Aula/` — slide, audio and video prompts |
| `/speechify` | `/speechify rules/07_bayes.md` (`--split`, `--short`) |
| `/intake` | `/intake Aula/aula3.pdf` — front door for new material; asks once what to derive |
| `/explainer` | `/explainer conjugate normal-normal updating` — narrated 1080p Manim video; needs `SPEECHIFY_API_KEY` in `.env` |
| `/manim-kit` | `/manim-kit .` — shared drawing layer from `../Video explainer` |
| `/companion` | `/companion GARCH(1,1)` — interactive page for one model, only on request |

`/lab`, `/lab-init`, `/lab-data` build the course's Python/Jupyter notebooks.

## Quizzes

1. `cd` into this directory
2. `python -m http.server`
3. Open `http://localhost:8000/quiz.html`
4. Pick a quiz MD file from `Simulados/`

## Obsidian

Open the project root as a vault; `Map/` holds the wiki-linked cross references.

## NotebookLM

1. In NotebookLM, confirm Settings → Output language = English.
2. Upload everything in `NotebookLM/sources/`.
3. Run `/notebooklm Aula/` to generate prompts.
4. Open each prompt file → Ctrl+A → Ctrl+C → paste into NotebookLM.
