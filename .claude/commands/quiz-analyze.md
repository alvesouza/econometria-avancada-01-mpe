---
description: Analyze quiz results from the results directory, track progress over time without re-analyzing what is already done, and drive remediation, NotebookLM prompts, exercise lists, study packs and follow-up quizzes.
argument-hint: [result-file | --all] [--quiz] [--notebooklm] [--study-pack] [--exercises] [--force]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion Skill
---

Analyze quiz performance from `$ARGUMENTS`, update the longitudinal progress record, and optionally drive the downstream artifacts.

## Where results live (the convention)

- A quiz lives at `<quizzes>/<name>.md` (auto-discover the quizzes directory: `Simulados/`, `Quiz/`, …).
- **Its result lives at `<quizzes>/resultados/<name>.md` — the exact same filename.** That pairing is how a result is matched to the quiz that produced it. Do not rely on the title inside the file.
- The result file holds the **JSON exported by the quiz player**, even though the extension is `.md`. Parse it as JSON; do not expect Markdown.
- Multiple attempts at one quiz: `<name>.md`, then `<name>--2.md`, `<name>--3.md`, … Retakes are the raw material of the progress record, so never overwrite an earlier attempt.

Two bookkeeping files, both created on first run if absent:

| File | Purpose |
|---|---|
| `<quizzes>/resultados/_ledger.json` | which results are already analyzed, keyed by filename, with a content hash |
| `Listas/progresso.md` | the human-readable longitudinal record: scores over time, per-axis trend, which misconceptions closed |

## Instructions

### Step 0: Select which results to analyze (never redo work)

1. If `$ARGUMENTS` names a file, use it. If it names a bare quiz name, resolve to `<quizzes>/resultados/<name>.md`. With `--all` or no argument, glob `<quizzes>/resultados/*.md`, excluding files beginning with `_`.
2. Read `_ledger.json`. For each candidate, compute a content hash:
   ```bash
   python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()[:16])" <file>
   ```
3. **Skip any result already in the ledger with a matching hash.** Report each skip in one line (`already analyzed 2026-08-19 → Listas/remediation-….md`) and move on.
4. Analyze only new files, or files whose hash changed — a retake, or a corrected export.
5. `--force` re-analyzes what is named, ignoring the ledger. Use it when the analysis logic changed, not to redo a result.
6. If nothing is new, say so plainly, print the progress summary from Step 4, and stop. Do not manufacture work.

### Step 1: Parse and sanity-check each result

The JSON carries `quiz`, `date`, `total`, `correct`, `byTopic` (label → `{total, correct}`) and `wrong[]` (`{q, topic, text, your, correct}`). Accept the legacy `meta`/`topicScores`/`mistakes` shape and normalize.

**Cross-check the result against its source quiz before trusting it.** Decode the quiz's base64 answer markers and compare against each `wrong[].correct`:

- **Mismatch** ⟹ the result came from a different version of the quiz than the one on disk — a stale copy held in the player's memory, or the quiz was edited after the attempt. Report the mismatching question numbers and **stop** until the user says which version to trust. Analyzing a stale result yields a confident wrong diagnosis, which is worse than none.
- Verify `total` equals the question count in the quiz file.

Then read the source quiz to recover, for each wrong answer, the **full text of the chosen option and of the correct one**, plus its `> Ref:` and `> Similar:` lines. The JSON gives only letters; the option text is what reveals the misconception.

### Step 2: Diagnose misconception axes (not topics)

Topic scores say *where* errors fell, rarely *why*. Group the wrong answers into a few **misconception axes** — usually three to five, each explaining several errors across different topic sections. An axis earns its name when one faulty piece of reasoning produces errors in questions that look unrelated.

Record for each:

- a **stable kebab-case slug** — `ladder-of-assumptions`, `covariance-sign`, `two-measures`, `sml-vs-cml`, `index-model-vs-restriction`, `variance-units`, `ex-ante-vs-ex-post`. **Reuse a slug from `Listas/progresso.md` whenever the same misconception recurs**, even in another session or chapter. Slug stability is what makes the longitudinal record mean anything; a fresh slug for an old error hides a persistent weakness.
- the question numbers it explains;
- the wrong belief, in the student's own terms;
- the correct statement;
- an error type: *swapped concepts*, *sign error*, *formula slip*, *omitted assumption*, *scope error* (a result applied outside its domain), *units confusion*.

Rank by errors explained, then by how foundational the axis is.

### Step 3: Read project context

1. `CLAUDE.md` — course scope, bibliography, page-offset conventions, restrictions.
2. `rules/` — formulas, definitions, known pitfalls per topic.
3. `Map/` — `books-index.md`, `exercises-index.md` for cross-references.
4. **Verify every page number against the PDFs before writing it.** Index files go stale when a book is rebuilt. Cite printed pages and say which build you checked.

### Step 4: Update the longitudinal record (`Listas/progresso.md`)

The file that answers "am I getting better?". **Update it in place — never regenerate it**, since it holds history the current result cannot reconstruct.

```markdown
# Progress record

## Attempts

| Date | Quiz | Score | % | Δ vs. previous attempt on this chapter |
|---|---|---|---|---|

## Topic trend

One row per topic label ever seen, one column per attempt, cells `correct/total`.
Blank where a topic did not appear. Mark improvement, decline, first appearance.

## Misconception axes

| Axis (slug) | First seen | Last seen | Attempts touched | Errors | Status |
|---|---|---|---|---|---|

Status: **🔴 open** = errors on its most recent appearance · **🟡 closing** = fewer errors
than last time but not zero · **🟢 closed** = zero errors on a later attempt that actually
tested it. An axis not re-tested stays open — absence of evidence is not improvement.

## What changed this run

Two or three sentences: which axes moved, which did not, and any axis recurring after
being thought closed. A recurrence is the most important signal in this file.
```

When a new result re-tests an axis, update its row rather than appending a duplicate.

### Step 5: Write the remediation file

Save to `Listas/remediation-<quiz-slug>-<analysis-date>.md` with frontmatter:

```yaml
---
tags: [remediation, quiz, <session>, <axis-slugs>]
quiz: "<title>"
result: <quizzes>/resultados/<name>.md
date: <analysis date>
score: "16/30 (53%)"
axes: [slug1, slug2, slug3]
---
```

Body, in order:

1. Score, and a note of which book build the pages were verified against.
2. **Error table by topic** — correct, error rate, section, priority (🔴/🟠/🟢).
3. **A sentence saying the topic table is not the diagnosis**, then the axes.
4. **One block per axis**, in priority order: the wrong belief, the correct statement, and each question it explains with what was chosen and why that is wrong.
5. **Per-axis remediation** — required reading (source, section, verified printed pages, focus) and exercises (number, book, page, why this one).
6. The three consolidated tables below.
7. **Exit test** — six to eight closed-book questions, at least one per axis, that decide whether an axis may be marked closed.

#### Mandatory ending: the three consolidated tables

A machine-readable contract consumed by `/study-pack`. Use these exact headings:

```markdown
## Consolidated Reading by Book

### <Book short name — must match a key in Livros/book-registry.json>
| Topic | Chapter / Section | Pages | Priority |
|---|---|---|---|
| … | … | p. 117–119 | 🔴 |

## Consolidated Exercises

| # | Exercise | Book | Page | Axis | Priority |
|---|---|---|---|---|---|
| 1 | 4.3 | Ribeiro (2026) | p. 147 | variance-units | 🔴 |

## Study Roadmap

| Priority | Axis | Reading | Exercises | Time |
|---|---|---|---|---|
```

Rules:
- The `###` book heading **must match a registry key or a registered alias**, or `/study-pack` silently skips that book. Check `Livros/book-registry.json` first; if a book or chapter is missing, add a verified entry rather than letting the extraction drop it.
- Every reading row needs a concrete printed page range, not just a section id.
- Every exercise needs the page it appears on.
- English headings are canonical; the extraction script also accepts the older Portuguese ones.

### Step 6: Update the ledger

```json
{
  "quiz-sessao-04-capm-2026-08-16.md": {
    "sha256": "9f2c…",
    "analyzed_at": "2026-08-19",
    "score": "16/30",
    "taken_at": "2026-08-20T02:34:29Z",
    "remediation": "Listas/remediation-sessao-04-capm-2026-08-19.md",
    "axes": ["sml-vs-cml", "index-model-vs-restriction", "variance-units"]
  }
}
```

Write it **after** the remediation file exists, so a crash mid-run leaves the result marked unanalyzed rather than falsely done.

### Step 7: Report, then the four downstream artifacts

Report: score, anything skipped as already analyzed, the error table, the axes with what each explains, files written, and the lines from "What changed this run".

Run only what a flag requests, or what the user picks:

**a. NotebookLM prompts (`--notebooklm`)** — for each axis at error rate ≥ 25%, write **three** prompts — slides, audio and **video** — to `NotebookLM/slides|audio|video/remediation-<axis-slug>-{slides,audio,video}.md`.
- Each file is **pure prompt text**: no frontmatter, no headings, ready for Ctrl+A / Ctrl+C.
- **Hard cap 5.000 characters** — the NotebookLM fields truncate silently near 6.000. Measure after writing and trim until every file passes. Draft near 4.600: trimming by rephrasing recovers almost nothing, so cut whole clauses.
- Name uploaded sources by their exact filename in `NotebookLM/sources/`.
- Each prompt names the misconception explicitly and states what the student believed.
- The **video** prompt must be built on **one recurring visual** carried throughout — a split screen, a ladder, a plane with a ruler — because the format rewards construction over bullets. It is not the slide prompt re-paced.
- Respect the course's method ceiling (this course: OLS only).

**b. Exercise list (`--exercises`)** — pass the axes and their weights to `/exercise-plan`, which cites exercise number and page without reproducing statements.

**c. Study pack (`--study-pack`)** — run `/study-pack <remediation file>`, which reads the three consolidated tables and extracts the pages into one PDF. Verify the output: confirm each book's first and last extracted page is what you intended, and report the page count.

**d. Follow-up quiz (`--quiz`)** — Step 8.

### Step 8: The follow-up quiz, and the weighting question (MANDATORY ask)

A new quiz's subject may differ from where the mistakes were made. How much the old mistakes should drive the new questions is **the user's call, and you must ask before writing any question.**

Use AskUserQuestion:

> **How should your earlier mistakes weigh in this quiz, given its subject?**
>
> - **Relevance-weighted (recommended)** — each open axis appears in proportion to how much it actually bears on the new subject. A prerequisite axis gets real coverage; an unrelated one gets none.
> - **Heavy** — open axes drive selection even where tangential to the new subject. Choose this to hunt a persistent weakness.
> - **Light** — the new subject drives the quiz; earlier mistakes appear only where they are strict prerequisites.
> - **None** — ignore the history; quiz the new subject on its own terms.

Ask in the same prompt for question count, difficulty, and whether to reuse one shared numeric economy.

Then hand off to `/quiz-gen`, whose rules govern the writing — questions in **English**, every question **self-contained** (a `P:` stem does not survive a `##` boundary, so never write "the economy above"), no bare section numbers in stems, balanced answer positions, and `quiz-validate.py` printing `PASS` before shipping.

Design questions against the axes, not the topics: where the student swapped two concepts, write items in which exactly that distinction decides the answer, and make the distractor the belief they actually held.

Save to `<quizzes>/quiz-followup-<slug>-<date>.md`. Its result will later land in `resultados/` under the same name and re-enter this pipeline — which is how an axis earns 🟢 closed.

## Examples

```
/quiz-analyze                          → analyze every unanalyzed result, update progress
/quiz-analyze --all --notebooklm       → same, plus slide/audio/video prompts per weak axis
/quiz-analyze quiz-sessao-04-capm-2026-08-16.md --study-pack
/quiz-analyze --quiz                   → analyze, then build a follow-up (asks about weighting)
/quiz-analyze --force <file>           → re-analyze a result already in the ledger
```
