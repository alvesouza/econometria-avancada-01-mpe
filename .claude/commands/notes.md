---
description: Write dense, interlinked study notes for one lecture (or a set) — a map, one note per section with U/C/G layers and every step worked, a formula sheet, a pitfalls/self-test note, a Python note, reproducible figures and, if wanted, linked interactive companions. Builds from the slides when they exist and from the syllabus when they do not, marking the unit as estimated.
argument-hint: <lecture-number(s) | all> [--companions | --no-companions] [--reconcile]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion Agent Skill
---

Write study notes for the lecture(s) in `$ARGUMENTS`, under `Notas/LNN/`.

The notes are the project's **reading layer**: the place a student goes to *understand* a
lecture end to end, before the lists drill it and the quizzes test it. They are not a summary.
A summary tells you what the chapter says; a note **shows every step**, works every example with
the arithmetic in view, says which result is examinable, and links to everything else the project
has on the same idea.

The design is copied from `../Finanças 01 - MPE/Notas/` (look at `S04/` for a finished unit when
in doubt). This file is where it is binding.

## Step 0: One question round, then work

Every run that writes notes for a topic not yet in `Notas/` opens with **one** `AskUserQuestion`
round, even when an earlier topic was already answered — the right depth differs per topic.
*Why:* a single fixed depth produced notes too heavy for light topics and too thin on the
model-driven ones. Ask these, in this order:

1. **Depth** — *Full: every step, U/C/G layers, all support notes (Recommended)* ·
   *Exam-focused: C layer only, key derivations, formulas + pitfalls* ·
   *Overview: intuition and results, no full proofs*.
2. **Math ↔ theory** — *Equation-led: derive every equation, then read it — which assumption
   drives it and what it says about the theory (Recommended)* · *Theory-led: the economic
   argument first, equations as support* · *Results only: state each result and interpret it*.
3. **Graphs** — *Model curves: 4–8 figures, exact expressions, comparative statics in the key
   parameter (Recommended)* · *Reproduce the slides'/book's diagrams* · *Minimal: 1–3 key
   figures* · *None*. Name in the option description the figures you would draw for this
   topic (e.g. best-response curves, an indifference map, an equilibrium vs. a parameter).
4. **Companions** — only if `$ARGUMENTS` carries neither `--companions` nor `--no-companions`:
   *Yes, every unit (Recommended)* · *Yes, taught units only* · *Link existing ones only* · *No*.
5. **PDF** — asked on **every** run that creates or rewrites a unit, never skipped or defaulted:
   *Yes, one PDF per unit (Recommended)* · *No, Markdown only*. *Why:* students print and
   annotate the notes; a run that finished with Markdown only left them asking afterwards
   whether a PDF existed. A "yes" runs Step 4b.

The answers override the matching defaults in *Note anatomy*, *Support notes* and *Figures*
below; record them in the map's plan (Step 2). Everything else keeps its default — **do not
add further questions.**

When companions are on, the answer **stands in for `/companion`'s Step 0**: write each page's
control contract into the plan (Step 2) from the source's own calibration, and follow
`/companion` Steps 2–6 for everything else.

## Step 1: Pin the unit and its status

For each lecture `N`:

| Status | When | Source of truth |
|---|---|---|
| `taught` | `Aula/LectureNN.pdf` (or the lecture's slides) exists | the slides first, then the book sections they follow |
| `estimated` | no slides yet | the lecture's row and block in `Map/study-guide.md`, then the book sections listed there |

Read, in this order and no further than needed:

1. `Map/study-guide.md` — the lecture's block: content, before/after class, formal side,
   applications, project material. It fixes the sections and the page ranges.
2. The slides, if taught: `pdftotext -layout Aula/LectureNN.pdf -` (strip the build-up
   duplicates — beamer repeats each slide as it reveals).
3. The book sections at their **printed pages**. Convert with the offset in
   `Livros/book-registry.json`: PDF page (1-based) = printed + offset + 1 for scale 1
   (Tadelis offset 18 → printed p. 43 is PDF p. 62). `pdftotext -f A -l B -layout <pdf> -`
   into the scratchpad. Never quote a page you did not open.
4. The topic's `rules/*.md` pack, `rules/game-theory.md`, and `CLAUDE.md`'s scope block.
5. What the project already has for this lecture: `Listas/`, `Simulados/`, `Resolucao/`,
   `Aula/`, `Videos/`, any companion. Link it; never rebuild it.

## Step 2: Plan, then write

Write `.agent/plans/notas-LNN.md` (one plan may cover several lectures): the note list with
the section and pages each covers, the figures, and — when on — each companion's control
contract (`/companion` Step 2 table). Then write against it.

## What gets produced

```
Notas/
  _figstyle.py                  shared matplotlib look (colour roles main/warn/good/ref/hi)
  00-index.md                   every unit, its status, its companions
  LNN/
    LNN-00-map.md               the unit's front door
    LNN-01-<slug>.md ...        one note per section of the lecture
    LNN-<k>-formulas.md         every definition, result and number; the exam spec mapped
    LNN-<k+1>-pitfalls.md       the confusions, plus an original True/False self-test
    LNN-<k+2>-python.md         reference implementation with self-checks
    figures/make_figures.py     one script, writes LNN-<slug>.png beside itself
    figures/LNN-<slug>.png
    companions/companion-<model>.html
    LNN-notes.pdf               rendered from the .md notes (Step 4b, when PDF = yes)
```

Slugs are English, lowercase, hyphenated. Book, chapter and section titles stay verbatim.

## The map — `LNN-00-map.md`

1. Front matter: `tags: [notes, lecture-NN, <topics>, map]`, `date`, `status`, `source`
   (slides + book sections with printed pages).
2. **Estimated banner** (estimated units only), right under the title:
   `> **Estimated unit.** Built on <date> from the study guide before the lecture. Reconcile with the slides when Aula/LectureNN.pdf arrives (/notes NN --reconcile).`
3. **One claim** block: the lecture's argument in three to five bold-led sentences.
4. **The layers table** — U / C / G and what each means *for this unit*.
5. **Reading order**, in parts, one entry per note: wiki-link, the sections and pages, and one
   line saying what the note *settles* (the result, the trap, the example).
6. **The one result to hold** — a boxed equation or statement.
7. **Numbers / cases to have memorized** — a small table.
8. **Figures** table (file → what it shows → which note embeds it) and the run command.
9. **Interactive companions** — one bullet each: title, what moves, which notes link it.
10. **Scope and ceiling** — what is examinable, what is named only, what is out
    (`CLAUDE.md` scope block).
11. **Course-wide position** — a table of the other lectures and how each relates to this one.
12. **Bibliography actually used**, and **related project material** (lists, quizzes,
    solutions, videos) with paths.

## A section note — `LNN-NN-<slug>.md`

- Front matter: `tags`, `date`, `status`, `source` (the exact section, printed pages, the
  book's examples used).
- Title `# <section numbers> · <what it settles>`.
- **Claim** block, then `Prev: [[...]] · Next: [[...]] · Map: [[LNN-00-map]]`.
- Numbered sections `## 1 · C — <title>`, tagged by layer:
  - **U** — intuition and mechanics (Gibbons, the book's prose, the slides' story);
  - **C** — course, examinable: the slides' and the main book's definitions, propositions and
    methods, **stated exactly and with the book's numbering**;
  - **G** — formal or graduate (MWG): named, or proved when it clarifies; **not examinable**
    unless the lecture brings it.
- **Every derivation step written** — no "it can be shown", no skipped algebra.
- **Equations numbered and cited** — every equation a later step uses carries a number, and each step names its sources ("substituting (7) into (5)"); each note opens with a Notation list (every variable and parameter, meaning and range); one operation per displayed line, no long inline chains. Show every substitution as its own line: the receiving equation with the substituted expression in place, in parentheses, before simplifying (with (1) $A=B+C$ and (2) $B=2A$: first $A=(2A)+C$, then $C=-A$); numbers plugged in are shown in place before the result, with enough decimals that the displayed arithmetic reproduces the printed value.
- **At least one worked example** from the slides or the book's text, the arithmetic in view,
  laid out as tables where the book uses matrices.
- Bold-led **blockquotes** for the sentence to remember; tables for comparisons.
- Figures embedded right after the paragraph they illustrate:
  `![<full alt text>](figures/LNN-<slug>.png)` then one italic caption line —
  *what to see + source (equation/page)* — then one plain paragraph reading the figure.
- `> **Interactive companion.** [<Title>](companions/companion-<model>.html) — what to move and
  what to watch.` wherever a companion serves the section.
- `## Links` at the end: the neighbouring notes, other lectures that use or are used by this one
  (`[[../LMM/LMM-NN-...|LMM §x]]`), the `rules/` pack, the practice material, and the
  exercises **by number and page**.

## Support notes

- **`-formulas`** — §0 the exam specification mapped to notes (the slides' learning goals or the
  study guide's content list, item by item); §1 every definition and proposition with its
  number, statement and the note that derives it; §2 every number and worked case in the
  lecture.
- **`-pitfalls`** — Part I: the confusions this material produces (weak vs strict, a strategy vs
  an action, Pareto vs equilibrium, …), each with the minimal counterexample. Part II: an
  **original** True/False self-test of 15–30 items with a one-paragraph justification each,
  in the `macro-1` V/F style (`rules/00_estilo_avaliacao.md`).
- **`-python`** — every routine the lecture needs (solvers, best responses, backward induction,
  equilibrium checks), each with `assert` self-checks against the book's own numbers. Python
  only, numpy/scipy/matplotlib; reuse existing code (`Listas/*-check.py`,
  `Aula/**/check_*.py`) by import or by citation before writing new.

## Figures

- `Notas/LNN/figures/make_figures.py`: imports `Notas/_figstyle.py`
  (`sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))`), calls `apply()`,
  writes each PNG with `save(fig, "LNN-<slug>")`, and ends with `assert` checks on at least one
  plotted number per figure.
- Four to eight figures per unit. **Every curve is the model's exact expression**, every number
  the book's or the slides' own, cited in a comment. Payoff matrices are drawn as tables, game
  trees as trees, best responses as correspondences — whatever the lecture actually reasons
  with.
- Colour roles: `main` the object of attention, `warn` the thing that fails or is eliminated,
  `good` the result that survives (the equilibrium), `ref` neutral reference, `hi` highlight.
- Run it (`python Notas/LNN/figures/make_figures.py`) and confirm every embedded PNG exists.

## Companions (when on)

- One self-contained HTML per model, `Notas/LNN/companions/companion-<model>.html`, built to
  `/companion` Steps 2–5: 3–6 controls, the exact expression, live read-outs with the page's
  answer emphasised, landmarks exactly reachable, theme tokens with both dark-mode guards,
  ≥ 400 px responsive, inline SVG, no network except fonts, provenance line with printed pages.
- Verify to `/companion` Step 6: compute the read-outs in Python at **three control vectors**
  (both ends and the default) and compare with the page's own function (run its JS with `node`
  when available — `Aula/aula-01-companions/check_companions.py` shows how). Keep the check as
  `companions/check_companions.py`.
- Link each page from the map's companion list **and** from every note it serves.

## `--reconcile` (an estimated unit whose slides have arrived)

1. Read the slides; list what they cover, in their order and notation.
2. Diff against the unit's notes: sections the lecture skipped, sections it added, notation
   and examples that differ, results stated differently.
3. Add notes for new sections, move skipped ones under a `G`/"not covered in class" heading
   (never delete worked material), switch the notation to the slides', set
   `status: taught` everywhere, remove the banner, and update `Notas/00-index.md` and
   `Map/study-guide.md`.
4. Report the diff as a table.

## Step 3: Wire it in

- `Notas/00-index.md` — the unit's row: status, map link, companions.
- `Map/study-guide.md` — under the lecture's block, a `- **Notes:** [[Notas/LNN/LNN-00-map|...]]`
  line.
- Leave other lectures' notes alone except to fix a link into this unit.

## Step 4: Verify, then report

1. `make_figures.py` runs clean; every `![...](figures/...)` target exists.
2. Every `[[wiki-link]]` resolves to a file under `Notas/`, `Map/`, `rules/` or another project
   path; every `](path)` link exists. Check with a script, not by eye.
3. Companion checks pass (when on).
4. No exercise statement reproduced anywhere — only number and page.
5. Report: units built and their status, note count and line counts, figures, companions with
   their three verification vectors, the PDF (path, pages) or "PDF: declined", anything skipped
   and why.

## Step 4b: Compile the PDF (when the Step 0 PDF answer is yes)

After Step 4 passes, for each unit:
`python -I ~/.claude/commands/templates/notes_pdf.py Notas/LNN` → `Notas/LNN/LNN-notes.pdf`
(pandoc + LuaLaTeX; Latin Modern with a Cambria/Segoe glyph fallback; the Markdown stays the
source, so rerun it after any note edit). Then check:
- the build prints no `Missing character` warning (a missing glyph silently drops text);
- `pdffonts` shows no Type 3 font;
- every figure embedded in the notes appears (page count well above the note count; open one
  figure page).
Link the PDF from the unit's map and from `Notas/00-index.md`.

## Important

- **English** prose (global rule); quotes, titles and file names verbatim. LaTeX `$...$` for
  all math, never a bare `$` for currency.
- **Scope** is the lecture's block in `Map/study-guide.md` and the `CLAUDE.md` scope list. Out-of-
  scope material (mechanism design, cheap talk, moral hazard here) is not written up, not even as
  `G`.
- **Never reproduce an exercise statement** — cite number and printed page. Book *examples* in
  the running text may be worked in full, with their page.
- **Estimated means estimated**: say so in the front matter and the banner, and never write
  "the lecture showed…" for a lecture that has not happened.
- **Reuse before writing**: existing lists, solutions, quizzes, videos and companions are linked,
  not rebuilt. Code from `Listas/*-check.py` is imported or cited.
- Notes are dense, but every line earns its place: no restating the claim in three places, no
  filler transitions.

## Ecosystem

- `/companion` → the page standard the companions follow (Steps 2–6).
- `/summarize`, `/convert` → raw material; the notes go further (every step, every link).
- `/list-exercises`, `/exercise-plan`, `/solution` → the drill the notes point to.
- `/quiz-gen` → quizzes can be generated from a unit's `-formulas` and `-pitfalls` notes.
- `/speechify`, `/notebooklm` → narrations and prompts can take a unit's notes as source.
- `/study-map` → the `Map/` indexes that the notes link into.
