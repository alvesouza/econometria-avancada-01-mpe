# Full study set for all 7 units — plan (2026-10-25)

User request: for each lecture, a quiz, a NotebookLM audio prompt, a TTS narration, notes, and
book exercises with solutions. Decisions (asked 2026-10-25):

| Deliverable | Decision |
|---|---|
| Quiz | 10 questions per unit, **hard but no math**: deep cross-topic conceptual synthesis, no derivations, no choose-the-expression items; notation only to name an object. Mode: file-subject (slides + the unit's book sections). |
| NotebookLM audio | 1 Custom prompt (≤ 5,000 chars) per unit; 2 parts for L01, L03, L05. Hard. ~10 prompts. |
| TTS | one narration per unit (`/speechify`), from the unit's notes. |
| Notes | units without notes: full depth, equation-led, 4–8 model figures, 1–2 companions per unit, one PDF per unit. L01/L02 notes kept as they are; PDF added. |
| Exercises | every "Practice" item of `Map/class-plan.md` for the unit, verbatim from the book PDF with a source line, full solutions; computer exercises solved in Python with code and output. |

## Units

| Unit | Classes | Slides | Practice list (Map/class-plan.md) |
|---|---|---|---|
| L01 | 1 | `Aula/class-01/materials/` | Class 1 block |
| L02 | 2 | `Aula/class-02/materials/` | Class 2 block |
| L03 | 3+4 | `Aula/class-03-04/materials/` | Classes 3+4 block |
| L05 | 5+6 | `Aula/class-05-06/materials/` | Classes 5+6 block |
| L07 | 7 | `Aula/class-07/materials/` | Class 7 block |
| L08 | 8 | `Aula/class-08/materials/` | Class 8 block |
| L09 | 9 | `Aula/class-09/materials/` | Class 9 block |

Unit id = first class number, so a paired class keeps its number (L03 = 3+4, L05 = 5+6).

## Outputs and owners

| Output | Path | Owner |
|---|---|---|
| Notes | `Notas/LNN/` (+ `LNN-notes.pdf`), plan `.agent/plans/notas-LNN.md` | one agent per unit (L03, L05, L07, L08, L09) |
| Exercise list | `Listas/lista-LNN-book-exercises.tex`, `.pdf`, `-gabarito.pdf`, `Listas/LNN-book-exercises-check.py`, data in `Listas/data/` | one agent per unit |
| Quizzes | `Simulados/quiz-LNN-<slug>-2026-10-25.md` | 2 agents (L01–L03, L05–L09) |
| Audio prompts | `NotebookLM/audio/LNN-audio[-partK].md`, `NotebookLM/README.md`, slide copies `NotebookLM/sources/Aula_<class>_<file>.pdf` | 1 agent |
| TTS | `Leituras/LNN-narrated.txt` | after each unit's notes exist |
| Shared indexes (`Notas/00-index.md`, `Map/`) and L01/L02 PDFs | lead | lead, at the end |

No agent edits a file owned by another. Parallel LaTeX builds use per-unit temp names
(`_gab-LNN.tex`), never a shared `_gab.tex`.

## Shared facts (do not re-derive)

- Specs, binding: `.claude/commands/{notes,companion,quiz-gen,notebooklm,speechify,exam-gen}.md`;
  style `rules/00_estilo_avaliacao.md` (Equations/notation rule; Book-questions rule).
- Finished reference unit: `Notas/L01/`, `Notas/L02/`, plan `.agent/plans/notas-L01-L02.md`.
- Page offsets: `.agent/notes/book-offsets.md`. Book Markdown in `Livros/*.md` locates a
  section; text and pages are taken from the PDF.
- Python only. Installed: numpy, scipy, pandas, matplotlib, statsmodels, linearmodels.
  **Not installed:** scikit-learn, arch, PyMC, ISLP, wooldridge — write samplers/GARCH MLE in
  NumPy/SciPy; `pip install wooldridge` is allowed for Wooldridge data sets.
- Old draft-plan material (`Simulados/quiz-class01-*`, `NotebookLM/audio/aula-01-*`,
  `Leituras/class-01-narrated.txt`, `Listas/pratica-class-01-*`, `Videos/class-01-*`) is
  potential outcomes = Classes 5+6 content. Kept, not deleted; linked as L05 material.
- Toolchain: pdflatex, lualatex, pandoc, pdftotext, pdffonts present. PDFs: `lmodern` + `cmap`,
  `pdffonts` shows no Type 3.

## Status — done 2026-10-29

All deliverables exist for all 7 units and pass their checks (re-run by the lead). Indexes updated:
`Notas/00-index.md` (all units), `Map/class-plan.md` ("Project material" line per class),
`NotebookLM/README.md`. Source errata found by the agents are listed in each unit's map note.
Also built: `Listas/hw1-advancedeconometrics-2026.ipynb` (comment-only scaffold for HW1).
Lessons: subagents stall on very large single writes (narration parts, long notes) — have them
write per-note chunks and join with `cat`; parallel LaTeX builds need per-unit temp names.

## Verification

- Quizzes: `python .claude/quiz-validate.py <file>` prints PASS.
- Notes: `python Notas/LNN/figures/make_figures.py` runs; `python tools/check_note_links.py`
  clean; notes PDF builds with no `Missing character`; companions checked as in L01.
- Lists: both PDFs compile; check script passes; `pdffonts` Type 1 only.
- Audio: every prompt ≤ 5,000 chars; every source name exists in `NotebookLM/sources/`.
