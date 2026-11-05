---
description: Generate a SOURCE-REFERENCED practice plan — only the exercise number and page in the textbook — with subtopics weighted and distributed across knowledge levels. Does NOT reproduce problem statements; points to real exercises in the course books. Asks sources, level distribution, count, and weighting before generating.
argument-hint: <topics to practice> [number of exercises]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion
---

Generate a **practice plan** from `$ARGUMENTS` (the topics the student wants to drill): a curated list of exercises **from the source books**, with their numbering and page, weighted by subtopic and distributed across knowledge levels. **Do not write the problem statements** — point to the real exercises in the books.

This differs from `/list-exercises` (which extracts every exercise from a file) and from `/exam-gen` (which writes original exercises): here the deliverable is a **referenced curation** so the student practices directly from the source.

Write everything in English, per the global rule in `~/.claude/CLAUDE.md` — the instructions, the user-facing question text and the "what it trains" notes alike — whatever language the course and the books are in. Exercise titles, chapter and section names are cited verbatim from the source. Another language only when the user asks for it explicitly.

## Step 1 — Scope

Parse `$ARGUMENTS`: topics/lectures to practice and the count (if given). If vague, infer from `CLAUDE.md`.

## Step 2 — Read the exercise index FIRST, then sources for gaps

1. **`Map/exercises-index.md` is the primary source.** Built by `/study-map`, it already maps every source exercise → number, page, subtopic(s), knowledge level, and a `Verificado` flag. Read it first and filter to the subtopics in scope — this is your candidate pool, with numbers and pages pre-verified.
   - If `Map/exercises-index.md` is **missing or stale** (doesn't cover the requested topics), tell the student and **suggest running `/study-map`** to build/refresh it. You may proceed by reading the book MDs directly (step 3) as a fallback.
2. Read `Map/topics-index.md` for subtopic **weights** (cross-reference density) and `Map/books-index.md`/`study-guide.md` for context. Read `CLAUDE.md` and `rules/` for scope and the topic names.
3. **Fallback / gap-filling only:** for any subtopic the index doesn't cover, list the converted books in `Livros/` (or `<books-dir>`) and **read the MD** to extract the **real exercise numbers** and **page** (e.g., N&S "Problems &lt;page&gt;" in the TOC + exercises `chapter.number`; MWG "Exercises" per chapter).
4. **NEVER invent a number or page.** Use only exercises with `Verificado = sim` in the index, or ones you verified yourself in a source MD. Index rows marked `não`, or sources not converted (J-R, ZaE as PDF), are carried through **"to confirm"** — do not fabricate.
5. Identify the **adjacent** topics (via `topics-index.md`) for the tangential question.

## Step 3 — Ask the student (AskUserQuestion)

Make **one** call (adapt options to the scope and to the available sources; option text in English):

1. **Sources** — which books to pull exercises from? (multiSelect: *N&S 12e* [floor], *Jehle-Reny*, *MWG*, *ZaE*, *course problem sets*). Flag non-converted ones as "ref. via Map, to confirm".
2. **Knowledge-level distribution** —
   - *Progression* (foundations → exam level → advanced) [recommended]
   - *Exam level* (AF focus)
   - *Foundations* (drilling, direct application)
   - *Advanced* (proofs/limits, MWG/J-R)
3. **Count** — total number of exercises (or per subtopic): *10* / *20* / *30*.
4. **Subtopic weighting** —
   - *By exam relevance / `Map/` cross-reference density* [recommended]
   - *By lecture coverage*
   - *Even across subtopics*

If the content mixes mathematizable and conceptual parts, also offer an emphasis option (as in `/exam-gen`). Skip any question already answered in `$ARGUMENTS`.

## Step 4 — Weight and distribute

- **Subtopic weights:** derive from `Map/` cross-reference density (more links = more central = more exercises) or the chosen option. **Show the weights** to the student.
- **Levels:** classify each exercise as *Foundations* (definition/direct application), *Exam* (multi-step, duality, interpretation), or *Advanced* (proof/limit/extension). Use the source as a hint (N&S skews foundations/exam; MWG and J-R skew advanced) and what the exercise actually tests.
- Allocate the total count by **weight × level** per the chosen distribution (in a progression, more foundations early, tapering to advanced).

## Step 5 — Build the plan (references only)

Markdown table, grouped by subtopic (or by level), saved to `<lists-dir>/pratica-<topic>.md`:

```markdown
### <Subtopic> — weight <w>%
| Level | Source | Ch./Sec. | Exercise(s) | Page | What it trains |
|-------|--------|----------|-------------|------|----------------|
| Foundations | N&S 12e | Ch. 4 | 4.1, 4.2 | 132 | CD demand via UMP |
| Exam | N&S 12e | Ch. 5 | 5.6 | 168 | Slutsky + CV/EV |
| Advanced | MWG | §3.G | 3.G.4 | 96 | Slutsky matrix symmetry/neg. (to confirm) |
```

- `Exercise(s)` and `Page` are the **real** numbering and page in the source. `What it trains` is **one line** — never the problem statement.
- Include a **suggested study order** (the progression) and the **weighting rationale**.
- Use Obsidian wiki-links to `Map/` where useful. (Optional: a compilable LaTeX version if the student asks — global lmodern+cmap rule.)

## Step 5b — Mandatory ending: Consolidated Reading & Exercises

The file MUST end with three structured tables that collect ALL recommendations in machine-parseable format. These tables serve as both a study guide and as input for `/study-pack` (which extracts the pages into a single PDF).

**Table 1 — Leituras Consolidadas por Livro** (all reading sections grouped by book, sorted by page):

```markdown
## Leituras Consolidadas por Livro

### N&S 12e — Nicholson & Snyder
| Tópico | Capítulo / Seção | Páginas | Prioridade |
|--------|------------------|---------|------------|
| Utilidade esperada | Cap. 7, §Expected Utility | p. 218–226 | Fundamentos |
| State-Preference | Cap. 7, §State-Preference | p. 232–238 | Prova |
| ... | ... | ... | ... |

### MWG — Mas-Colell, Whinston & Green
| Tópico | Capítulo / Seção | Páginas | Prioridade |
|--------|------------------|---------|------------|
| Equilíbrio AD | §19.C | p. 691–698 | Avançado |
| ... | ... | ... | ... |
```

Rules:
- One section per book (short names matching CLAUDE.md bibliography)
- Rows sorted by page number within each book; merge overlapping ranges
- Every row must have a **concrete page range** (`p. NNN–MMM`), not just section IDs
- Priority column matches the knowledge level: Fundamentos / Prova / Avançado
- Include the reading sections that **contain** the recommended exercises (the student needs context, not just the problem page)

**Table 2 — Exercícios Consolidados** (all exercises in one flat table, sorted by book then number):

```markdown
## Exercícios Consolidados

| # | Exercício | Livro | Página | Tópico | Nível |
|---|-----------|-------|--------|--------|-------|
| 1 | 7.1 | N&S 12e | p. 239 | Utilidade esperada | Fundamentos |
| 2 | 7.4 | N&S 12e | p. 239 | Seguro | Prova |
| 3 | 19.C.1 | MWG | p. 725 | Equilíbrio AD | Avançado |
| ... | ... | ... | ... | ... | ... |
```

Rules:
- Flat list, sorted by book then exercise number
- Every exercise must have the **page number** where it appears in the book
- Include ALL exercises from every subtopic section (no omissions)
- Exercises marked `(a confirmar)` stay as-is in the table

**Table 3 — Roteiro de Estudo** (study roadmap):

```markdown
## Roteiro de Estudo

| Prioridade | Tópico | Leitura | Exercícios | Tempo sugerido |
|:---:|--------|---------|------------|:---------:|
| 1 | Utilidade esperada + seguro | N&S Cap. 7 p. 218–238 | N&S 7.1, 7.4, 7.7, 7.8 | 2–3h |
| 2 | Equilíbrio AD + Radner | MWG §19.C–D p. 691–708 | MWG 19.C.1, 19.C.2, 19.D.1, 19.D.3 | 2–3h |
| ... | ... | ... | ... | ... |
```

These three tables make the file self-contained and consumable by `/study-pack`.

## Step 6 — Report

Show: number of exercises per subtopic and per level; sources used; any **"to confirm"** items (not verified in an MD); file saved. Suggest `/solution <source> <exercise>` to solve a specific one, `/exam-gen <topic>` for an original list, or `/study-pack <file>` to extract the recommended pages into a single PDF.

Then ask (one AskUserQuestion call, two questions), every time:

1. **Split the study roadmap into a PDF?** *Yes* runs `/study-pack` on the saved file.
2. **Write the solutions of the plan's exercises as a PDF?** *Yes* solves every exercise with `/solution` in plan order (each cited by number and page, never restated) and compiles `Listas/pratica-<topic>-solutions.pdf`.

Rule: `rules/00_estilo_avaliacao.md` §9.

## Principles

- **References only** (number + page); **never** reproduce problem statements (they belong to the sources).
- Every reference **verified in the source MD**; anything unverifiable is marked "to confirm".
- Weight transparently (show the weights) and respect the requested level.
- Do not go beyond the course content (`CLAUDE.md`).
