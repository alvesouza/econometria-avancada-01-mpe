---
description: Front door for material that just arrived — converts it, analyses what it is and where it anchors in the bibliography, reports what the project already covers and what is missing, then asks in one round whether to produce a TTS narration, NotebookLM prompts (and with which characteristics), or anything else the analysis showed was absent.
argument-hint: <file-or-dir-or-lecture-or-topic> [--no-ask] [--stage-only]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion
---

Analyse the material in `$ARGUMENTS`, report what it is and what the project already has around
it, then ask what to derive from it.

New material arrives as a PDF and the useful question is never "convert it?" — it is *what now*:
a reading plan, a narration, NotebookLM prompts, a quiz, a notebook, a video, or nothing because
it is already covered. Answering that requires knowing what the material contains **and** what
the project already holds. This command does that reading first, and asks second.

**It never writes a narration or a NotebookLM prompt without asking.** That is
`rules/10_notebooklm_prompts.md` **R0**, and it exists because a 4,900-character prompt written
on the wrong cut is a total loss.

## Instructions

### Step 1: Resolve the target

- **A file** → that file.
- **A directory or glob** → the files in it; if several, list them and treat them as one batch.
- **A lecture or lista number** ("aula 7", "lista 6") → find its material by content, not by a
  hardcoded name.
- **A topic** → the `rules/` file, the lecture material and the book chapter that cover it.

If a PDF has no `.md` counterpart, convert it by delegating to **`/convert`** — never
reimplement markitdown. Record the converted size, and warn where it matters: **slide PDFs
converted by markitdown scramble two-column layout and equations.** The MD is good for locating
a topic; the PDF is what you read for a derivation. Say so explicitly in the report, because a
later reader will otherwise trust the MD.

Auto-discover directory names; do not assume `Aula/`, `Listas/`, `Livros/` are the only
possibilities.

### Step 2: Analyse it — and report the analysis before proposing anything

Read the material. Then produce an analysis that names **file paths and page numbers**, not
categories:

1. **What it is** — lecture slides, handout, problem set, book chapter, solution key, tutorial —
   its length, and its structure (the section list, the question list).
2. **Its bibliographic anchor** — the Kurlat chapter, section and **printed page**, or the
   Benigno section. Use the offsets in `Map/books-index.md`: Kurlat offset 0 (printed = PDF),
   Benigno printed 503–524 (`pdf = printed − 502`), Jones +25, Romer +22, Carlin & Soskice +24.
   **Verify each anchor against the PDF.** An anchor you could not confirm is reported as
   *unverified* — never quietly rounded to a plausible page.
3. **Which lecture and which lista** it belongs to, against `CLAUDE.md`'s lecture × chapter map.
4. **The named content** — the models, equations and results actually in it, in the course's own
   notation. For a problem set, one line per item.
5. **What is new** relative to what the project holds, and **what contradicts** it. A prediction
   in `Map/` that the new material falsifies is the single most valuable thing this command can
   surface — say it loudly rather than filing it.
6. **Scope check** — flag anything outside Kurlat chs. 1–7, 9–11 and Benigno. `CLAUDE.md`'s
   "NÃO extrapolar" applies to material the professor hands out too: if a slide reaches past the
   course, the right move is to note it, not to build a study artefact around it.

### Step 3: Report what already exists around it

Check each, by path, and report present/absent — this is what makes the Step 4 questions
informed rather than generic:

| Asset | Where to look |
|---|---|
| Topic rules | `rules/NN_*.md` — and whether it covers what this material actually does |
| Reading map | `Map/` — a per-lecture reading plan, if the project has one for this topic |
| Cross-references | `Map/cobertura.md`, `Map/00_indice.md`, `Map/aulas-x-bibliografia.md`, `Map/exercises-index.md` |
| Solutions | `Resolucao/` — the lista's solution, the chapter's book solutions, the figure code |
| Narration | `Leituras/*.txt` — a TTS script for this chapter or lista |
| Chapter extract | `Leituras/` — the isolated chapter PDF, where one exists |
| NotebookLM | `NotebookLM/{slides,audio,video}/` prompts, and whether it is staged in `NotebookLM/sources/` with the right prefix |
| Quizzes | `Simulados/` |
| Notebooks | `Notebooks/` |
| Videos | `Videos/` |

**Staging is part of intake.** If the material is not yet in `NotebookLM/sources/`, copy it with
the flat category prefix the project uses — `Aula_`, `Lista_`, `Livro_`, `Monitoria_`, `Prova_`
— preserving the exact name the prompts will cite. `--stage-only` stops after this step.

Where the material is a chapter of a large book that the course reads in full, consider cutting
a **standalone extract** into `Leituras/` (PDF + MD), as the project already does for isolated
chapters — it is what makes a 300-page book readable for one lecture, and what gets uploaded as
a source.

### Step 4: Ask — one round, informed by the analysis

One `AskUserQuestion` round. **Never a second.** Each question's recommended option must be the
one the analysis actually supports, with a one-line reason. Cover:

1. **TTS narration** (`/speechify`) — yes/no, and if yes the **cut**: the whole chapter, the
   lista's questions, the solutions, or a short revision pass. Note that output is **English by
   default** per the global rule, `--lang pt-BR` to override, and that a chapter-length narration
   runs to hours — that is the point, not a defect.
2. **NotebookLM prompts** (`/notebooklm`) — yes/no, and if yes the characteristics
   `rules/10_notebooklm_prompts.md` R0 requires settling *before* writing:
   - **unit of organisation**: per lecture · per book chapter · **per mechanism across a lista**
     (the cut the project has used for its best batches) · one single set;
   - **count per type**: slides, video, audio, separately. **Zero is a valid answer** for a type;
   - **the content cut**, and what to deliberately leave out — including which threads are
     already taken by existing prompts, so the new batch does not restate them.
   State plainly: **audio is always requested in English, never pt-BR, under any circumstances.**
3. **What else the analysis showed missing** — offered as options, never assumed: a reading map,
   a `rules/` update, `/solution` for a new lista, `/book-solutions` for the chapter's exercises,
   `/quiz-gen`, a `/lab` notebook, an `/explainer` video, or updating the coverage maps only.
4. **Whether the maps should be updated now** — `Map/cobertura.md`, `Map/00_indice.md`,
   `Map/aulas-x-bibliografia.md`, `Map/exercises-index.md`, `NotebookLM/README.md`. Default yes:
   material that is not registered anywhere is material that gets forgotten.

If an answer implies an uneven split, **state the allocation and proceed**. `--no-ask` honours
the user's explicit "use defaults" and takes the recommended option for each.

### Step 5: Dispatch and register

Hand the settled parameters to the chosen commands — `/speechify`, `/notebooklm`,
`/solution`, `/book-solutions`, `/quiz-gen`, `/lab`, `/explainer` — in that order of usefulness,
and **do not reimplement any of them**.

Then update the maps, editing **in place** and in each file's own language (the `Map/` files and
`NotebookLM/README.md` are in Portuguese; keep them Portuguese — new standalone documents you
author are in English per the global rule):

- `Map/cobertura.md` — the status cells and counts for this lecture and lista; bump its date.
- `Map/00_indice.md` — the lecture row, and a row for any new map file.
- `Map/aulas-x-bibliografia.md` — the lecture entry: material, lista, what the lecture does,
  complementary readings.
- `Map/exercises-index.md` — new book exercises with number, exact title, page and level; and
  the lista's item-to-exercise mapping.
- `NotebookLM/README.md` — the staged sources, with their exact filenames.

Quote a due date **verbatim** as printed, and flag any discrepancy rather than silently
correcting it.

### Step 6: Report

| Step | Result |
|---|---|
| Converted | file → `.md`, size, and whether the MD is trustworthy for derivations |
| Anchored | Kurlat/Benigno chapter, section, printed pages — verified or unverified |
| New | what this adds |
| Contradicts | what it falsifies in the existing maps |
| Staged | the `NotebookLM/sources/` filenames |
| Produced | what each dispatched command generated |
| Registered | which map files were updated |
| Still missing | what was offered and declined, so it is on the record |

## Important

- **Analyse before proposing, ask before writing.** Both halves matter: a generic question set
  is as useless as no question at all.
- **One `AskUserQuestion` round**, never per-file, never a second round.
- **R0 is not a preference.** `rules/10_notebooklm_prompts.md` requires unit, counts and content
  to be settled before a single prompt is written. Cite it when you ask.
- **Audio is always English.** No pt-BR audio prompts, under any circumstances.
- **Never invent a page number.** Verify against the PDF with the offsets in
  `Map/books-index.md`, and report what you could not confirm.
- **Never reproduce exercise statements** — number and page only.
- **Flag, do not absorb, out-of-scope content**, even when it came from the professor.
- **Do not silently fix a contradiction in the maps** — surface it, then fix it where the user
  agrees. A falsified prediction is information about how the course works.
- `NotebookLM/sources/` and `Livros/` are **gitignored for copyright**. Staging a source is a
  local act; do not try to commit it.

## Ecosystem

- `/convert` → the conversion this command delegates; run on its own for a bulk pass.
- `/summarize` → the compressed read. `/speechify` → the full listen. Different deliverables.
- `/notebooklm` → prompt batches, once this command has settled their characteristics.
- `/study-map` → regenerates the cross-reference maps this command edits by hand for one arrival.
- `/solution`, `/book-solutions`, `/exercise-plan`, `/study-pack` → the practice side.
- `/lab`, `/explainer` → when a topic deserves computation or animation rather than more text.
- `/setup-study` copies this command into new study projects.
