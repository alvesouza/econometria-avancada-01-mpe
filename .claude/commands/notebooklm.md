---
description: Generate detailed NotebookLM prompts (slide-style, audio-style and video-style), based on cross-references from Map/ and rules/. Always asks first what the prompts should be organised around (aulas/chapters/sessions), how many of each type, and which content. All course sources are already uploaded to NotebookLM — the prompts guide how to process them. Each file is pure prompt text — open, Ctrl+A, Ctrl+C, paste.
argument-hint: [Aulas/ | aula-NN.md | Livros/bookname.md] [--slides] [--audio] [--video]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion
---

Generate detailed NotebookLM prompts for the materials specified by `$ARGUMENTS`.

## Context

The user uploads ALL course materials to NotebookLM as sources — lecture slides/notes, textbooks (PDFs/MD), exercise lists, simulados, monitorias. The prompts generated here are **instructions** that tell NotebookLM how to synthesize, explain, and present the already-uploaded content. They are NOT standalone educational content.

Each prompt should:
- Reference the uploaded sources by their **exact filename** as found in `NotebookLM/sources/` (e.g., "Using the source `Aula_Econometria2026-2 - Aula3 - RLM - Multicolinearidade_Caso.pdf` and `Livro_Wooldridge...pdf` Chapter 5...")
- Tell NotebookLM what to focus on, what depth to reach, how to structure output
- Assume the reader/listener has access to all the source materials
- Guide NotebookLM to cross-reference between sources (e.g., "connect the proof in `Livro_Hayashi...pdf` §1.4 with the intuition from `Aula_...pdf`")

**CRITICAL — Source name resolution:** Before generating any prompts, list all files in `NotebookLM/sources/` and use those exact filenames when referencing sources in prompts. NotebookLM matches source references by filename — using the wrong name means the reference won't resolve.

**CRITICAL — Prompt language:** All prompts MUST be written in **English**, regardless of the course language, CLAUDE.md language setting, or source material language. NotebookLM processes English prompts more reliably.

**CRITICAL — Output language is an app setting, never a prompt line.** Do NOT write an output-language instruction into any prompt you generate, of any type. The language is set once in NotebookLM's Settings → Output language (English, for every type — audio included) and applies to everything the notebook generates; no prompt can override it. A language line burns ~140 of the ~5,000-character budget restating a setting that is already in force, and that budget belongs to content.

Two consequences for how you work:

- **Before generating a batch, remind the user to confirm Settings → Output language.** If it is wrong, everything comes back in the wrong language and no prompt can rescue it.
- **Spend the reclaimed characters.** The budget freed by dropping the language line goes into depth — one more derivation step, one more numerical detail, one richer code snippet — never into slack. The fill targets below are unchanged and still binding.

## Limits reference

- **NotebookLM source upload:** up to 500,000 words per source
- **Slide prompts** (pasted into the slide creation field "Descreva a apresentação de slides"): must not exceed **5,000 characters**. The field truncates silently at ~6,000 chars — no error, text just disappears. **Maximize usage: fill the budget, aiming for ~4,500–4,950 characters (as close to the 5,000 cap as possible without exceeding it). A slide prompt under ~4,000 chars is under-using the field — add depth (more derivation steps, more numerical detail, richer code) until it fills the budget.**
- **Audio prompts — Custom Prompt** (pasted into Audio Overview "Customize" field): must not exceed **5,000 characters**. Same silent truncation at ~6,000 chars. Target ~700–900 words.
- **Audio prompts — Source** (uploaded as a notebook source via paste text): target up to 3,000 words (~18,000 chars). Much higher limit since it's a source upload.

## Instructions

### Step 0: Confirm scope with the user (MANDATORY - always ask)

**Every time you are asked to create NotebookLM prompts, you MUST ask the user for the
scope BEFORE writing a single prompt - even when `$ARGUMENTS` already names a directory or
a file, and even when the request looks unambiguous.** Never infer the unit of organisation
and never invent the counts. Use one interactive multi-question prompt (AskUserQuestion),
pre-filling whatever `$ARGUMENTS` implies as the recommended first option so the user can
accept with one click or override.

Ask about, at minimum:

1. **Unit of organisation** - what does one set of prompts correspond to? Offer:
   **aulas/classes** (one set per lecture), **chapters** (one set per book chapter),
   **sessions/themes** (one set per topic block spanning several lectures), or a
   **single set** covering everything requested. This choice changes every filename and
   every source reference, so it is never safe to guess.
2. **How many prompts of each type** - ask for a count per type, separately:
   **slides**, **audio**, **video**. Accept zero for a type the user does not want. Do not
   assume the historical two-slides-plus-one-audio split; that was one project's choice.
3. **Which content** - which specific aulas, chapters or topics the prompts should cover,
   and whether anything in scope should be deliberately left out.

Only after the user answers do you proceed to auto-discovery. The one exception: if the
user explicitly says "use defaults" or "don't ask", honour that for this run. The default
posture is always to ask.

When the user's answer implies a count that does not divide evenly across the chosen unit
(for example four slide prompts across three aulas), state how you intend to allocate them
and proceed - do not ask a second round of questions about it.

### Step 1: Auto-discover project structure

**Do NOT assume fixed directory names.** Scan the project root and identify each directory's purpose by its name pattern AND contents:
- **Lectures**: slide PDFs, .html presentations, .R/.py scripts (e.g., `Aula`, `Aulas`, `Lectures`, `Slides`)
- **Books/Textbooks**: textbook PDFs (e.g., `Livros`, `Books`, `Textos`)
- **Exercise lists**: problem sets (e.g., `Listas`, `Lista`, `Exercises`)
- **Quizzes**: quiz MD files (e.g., `Simulados`, `Quizzes`)
- **Tutorials**: supplementary materials (e.g., `Monitoria`, `Tutoria`)
- **Rules/Maps**: `rules/`, `Map/`

Store the discovered mapping and use actual directory names throughout.

### Step 2: Read project context

1. Read `CLAUDE.md` for course scope, topic map, bibliography, **code language**
2. **Read ALL `Map/*.md` files** — these contain exercise-level cross-references linking each topic to specific exercises, applied examples, and parallel problems across lists, lectures, monitoria, and exams. Use the `Prova Relacionada` and `Exercícios Similares` columns to find concrete examples for each concept. If the maps lack exercise-level detail (no specific question numbers, no problem contexts, no cross-references to exam questions), **improve them first** by reading the converted MD files in `markitdown/` directories and adding the missing detail before generating prompts.
3. Read `rules/` files for key concepts, formulas, definitions per topic
4. Read the target lecture/book MD files to understand the actual content structure (blocks, sub-topics, examples, boxes)
5. List all files in `NotebookLM/sources/` to get exact filenames for source references

### Step 3: Determine scope and ask user preferences

Parse `$ARGUMENTS`:
- If a directory: identify whether it contains lectures, books, or other materials and generate prompts accordingly
- If a specific file: generate prompts for that file only
- If a book file: generate chapter-level prompts for the book
- If `--slides`, `--audio` or `--video` is given: generate only those types
- If no type flag: use the per-type counts the user gave in Step 0

**Ask the user (once) with AskUserQuestion:**

Question 1: "What difficulty level for the prompts?"
- **Easy** — foundational intuition, one topic at a time. Prompts instruct NotebookLM to explain each concept in isolation with clear definitions, basic examples, and step-by-step intuition. No cross-topic connections demanded.
- **Medium** — standard lecture depth, connecting 2-3 related concepts. Prompts ask for multi-step explanations, model output interpretation, and links between related topics within the same lecture.
- **Hard** — graduate-level depth, deep cross-topic synthesis. Prompts demand proofs, asymptotic arguments, connections across lectures/chapters, edge cases, and mathematical rigor. Prompts reference advanced sources (e.g., Hayashi, Greene) alongside standard ones.

Question 2: "What should drive the content?"
- **File-content** — prompts cover exactly what's in the target file, in order. The file defines the scope.
- **File-subject** — prompts cover the broader topics/subjects the file relates to, pulling from other sources via Map cross-references. The file is the starting point, but prompts expand to the full topic.
- **Topic-focused** — prompts organized by student weak areas / exam priorities, not tied to any file. Auto-detect weak areas from: (1) remediation maps in `Listas/remediation-*.md` (produced by `/quiz-analyze`), (2) quiz result JSONs, (3) followup quizzes in the quizzes directory. Present detected weak topics ranked by error rate as suggestions, let user confirm/override/add. For each weak topic, the prompt must address the **specific misconceptions** identified in the remediation map (e.g., "the student confuses X with Y — explain the distinction explicitly").

> **Do not ask about counts or unit of organisation here** — Step 0 already settled how
> many prompts of each type the user wants and what one set corresponds to. Asking again is
> a second round of questions the user did not agree to.

Question 4: "Should I also generate standalone prompts for any of the books?"
- **No** — only lectures
- **Yes, main textbook only** (the primary book from CLAUDE.md)
- **Yes, all books in bibliography** — one prompt per relevant chapter of each book

Question 5: "Audio prompt format?"
- **Custom Prompt** — must not exceed 5,000 characters, for pasting into NotebookLM's Audio Overview "Customize" field (truncates silently at ~6,000)
- **Source** — longer form (~3,000 words), for uploading as a notebook source (much higher limit)

### Step 4: Generate slide prompts

For each lecture (or book chapter), generate a **slide prompt** — a dense, exhaustive instruction telling NotebookLM how to synthesize the uploaded sources into a detailed slide-style explanation.

**Target: fill the character budget. Aim for ~4,500–4,950 characters — as close to the 5,000 cap as possible without exceeding it (the field truncates silently beyond ~6,000). Do not stop at ~700–900 words if that leaves the budget half-empty; keep adding depth until the prompt is dense and near the cap.**

**Format:**

```
<Topic> — Slides [Part N/M if split]

Explain in detail: <Lecture title and number>. Using the uploaded sources (<Book Name> <Chapter>, <other sources>), cover:

<For each major concept block in the lecture, write a concise instruction (40-80 words) that specifies:>
- What to explain and which source contains it
- Key formal objects, equations, and derivation steps to walk through
- Economic intuition and cross-references to other sources
- Code snippets where computation is relevant (see code rules below)

<Cover all major blocks from the lecture and USE the full 5,000-char budget — expand each block with derivation steps, numerical examples, and code until the prompt is near the cap.>
```

**Difficulty calibration for slide prompts:**
- **Easy**: instruct NotebookLM to explain each concept one at a time. Use phrases like "explain clearly", "define step by step", "give a simple numerical example". Reference only the primary textbook. No cross-source synthesis demanded.
- **Medium**: instruct NotebookLM to connect related concepts and show multi-step derivations. Reference 2 sources per concept. Demand "explain why" and "connect to [related concept]".
- **Hard**: instruct NotebookLM to provide formal proofs, asymptotic arguments, and cross-topic connections. Reference advanced sources (Hayashi, Greene). Use phrases like "prove formally", "derive the asymptotic distribution", "contrast with [concept from another lecture]", "show when the standard result breaks down".

**Mode-aware logic for slide prompts:**
- **File-content**: prompts follow the source file structure sequentially. Each prompt covers exactly what that file contains.
- **File-subject**: prompts use the file as a seed but expand scope via Map. If the file covers "dummy variables", the prompt also pulls from book chapters, exercises, and other lectures on dummies.
- **Topic-focused**: prompts organized by topic, referencing multiple lectures/chapters. Use Map cross-references and `Cross-topic synthesis` entries if available.

**Rules for slide prompts:**
- Maximize use of the budget: aim for **4,500–4,950 characters** (as close to the 5,000 cap as possible, never over) — count before saving. A slide prompt that comes in under ~4,000 chars is under-using the field: go back and add depth before saving.
- Prioritize coverage of all major lecture blocks; when the budget still has room, deepen each instruction (more derivation steps, more numerical detail, richer code) rather than leaving it short.
- Name uploaded sources explicitly (e.g., "as in N&S §4.3 and the Aula 2 slides")
- Reference specific equations and theorems by name
- Demand derivations and economic intuition, not summaries
- If splitting into 2 parts: Part 1 covers the first half, Part 2 the second half

### Step 5: Code in prompts

**Check `CLAUDE.md` for the project's code language (R, Python, or both).**

- If the course content involves computation (econometrics, optimization, simulation, data analysis): demand detailed code snippets in every slide prompt. Specify: "Include a complete, runnable code snippet in [language] that demonstrates [concept], with comments explaining each step and the economic/statistical intuition."
- If the course content is language-agnostic (e.g., pure econometrics theory, microeconomics with computational examples): default to **Python** (numpy, scipy, sympy, matplotlib).
- Demand code for: solving optimization problems, plotting curves, computing equilibria, running simulations, verifying analytical results numerically.
- For each code block demanded, specify:
  - What the code should compute or demonstrate
  - What libraries/packages to use
  - That the code must be complete and runnable (not pseudocode)
  - That comments should explain the economic/statistical intuition, not just the syntax

### Step 6: Generate audio prompts

For each lecture, generate an **audio prompt** — instructions for NotebookLM's Audio Overview.

**If Custom Prompt format (must not exceed 5,000 characters — field truncates silently at ~6,000):**

```
Explain and describe in detail (<part>/<total>) <Lecture block title>. Using the uploaded sources (lecture slides from Aula N, <Book> Chapter M, and related exercise lists), this covers: <one-sentence summary>. It covers:

<Sub-topic 1 title>: <1-2 sentence description of what to explain, key objects, and cross-references.>

<Sub-topic 2 title>: <1-2 sentence description...>

<Continue for all sub-topics, staying under 5,000 chars total.>
```

**If Source format (up to 3,000 words):**

Same structure but expanded — each sub-topic gets a full paragraph (80-120 words) referencing specific uploaded sources.

**Difficulty calibration for audio prompts:**
- **Easy**: conversational, one-concept-at-a-time explanations. "Explain what [concept] means intuitively, then give a concrete example."
- **Medium**: connect concepts, explain tradeoffs, walk through model interpretation. "Explain how [concept A] relates to [concept B] and what happens when [assumption] is violated."
- **Hard**: deep analytical discussion. "Discuss the formal conditions under which [result] holds, what happens asymptotically, and how this connects to [concept from another lecture]. Address common misconceptions about [edge case]."

**Mode-aware logic for audio prompts:** same as slide prompts above (file-content / file-subject / topic-focused).

**Rules for audio prompts:**
- More narrative/conversational than slides — emphasize intuition and "why"
- Still technically precise — name theorems, equations, conditions
- Reference what the listener should already know from prior uploaded lectures
- Tell NotebookLM to draw connections between the uploaded lecture and the uploaded book chapter
- If code is relevant: ask for verbal walkthrough of code logic, not printed code
- If splitting into 2 audio prompts: split by conceptual vs. computational

### Step 7: Generate video prompts (if requested)

A **Video Overview** is narrated slides: it has images, unlike audio, and a fixed pace, unlike a deck the reader scrolls. Write for that, not for either neighbour.

- **One visual per beat, named in the prompt.** Each beat says what appears on screen — a chart, an axis, a two-column table, a timeline. A beat with no visual of its own is not a video beat; fold it into a neighbour.
- **At most 6 beats**, at most 3 sub-points each. More generous than audio because the image sustains attention, but the depth budget still binds.
- **Numbers go on screen, not into the narration.** The viewer reads a table; the narration names only the cells that carry the argument.
- **Every transition is a step in the argument** and the prompt says which: a curve shifting, an axis rescaling, a column lighting up. If the transition is just "next topic", it should have been a slide.
- **Close on one image** the student should be able to redraw from memory, named explicitly.
- Same character budget as the other types, and the same rule: no output-language line — the language comes from NotebookLM's own setting.

Save to `NotebookLM/video/`.

### Step 8: Generate book prompts (if requested)

For each relevant chapter of a book:
- One slide prompt covering the chapter's core content, referencing the uploaded book PDF/MD
- One audio prompt giving the chapter overview
- Reference which uploaded lectures use this chapter (from `Map/books-index.md`)
- Focus on content that complements the uploaded lectures (proofs the lecture skipped, examples not covered, extensions)
- Include code snippets where computational examples exist
- Tell NotebookLM to cross-reference the book chapter with the uploaded lecture slides

### Step 9: Save output

Save all prompts to `NotebookLM/` directory:

```
NotebookLM/
├── slides/
│   ├── aula-01-slides.md          (or aula-01-slides-part1.md, part2.md)
│   ├── aula-02-slides.md
│   ├── ...
│   └── livro-nicholson-cap03.md   (if books requested)
├── audio/
│   ├── aula-01-audio.md           (or aula-01-audio-part1.md, part2.md)
│   ├── aula-02-audio.md
│   ├── ...
│   └── livro-nicholson-cap03.md
├── video/
│   ├── aula-01-video.md
│   ├── aula-02-video.md
│   └── ...
└── README.md                       (index of all prompts with copy instructions)
```

**If topic-focused mode**: name files by topic instead of lecture number (e.g., `endogeneidade-slides.md`, `heterocedasticidade-audio.md`). Group related topics if they were requested together.

**CRITICAL — One-click copy format:**

Each prompt file must contain ONLY the raw prompt text — no frontmatter, no markdown headers, no file metadata, no instructions, no code fences wrapping the prompt. The entire file content IS the prompt.

The user's workflow: open file → Ctrl+A → Ctrl+C → paste into NotebookLM. Nothing else needed.

Do NOT wrap the prompt in code blocks. Do NOT add "## Prompt" headers. Do NOT add "Copy this:" prefixes. Do NOT add frontmatter. The file IS the prompt.

The `README.md` is the ONLY file with metadata. It contains:
- One-line instruction: **"Open any prompt file → Ctrl+A → Ctrl+C → paste into NotebookLM (slides → slide creation field; audio → Audio Overview Customize field or as Source)"**
- Index table: `| File | Type | Lecture/Book | Words | Chars | Paste into |`
- For each file: path, type (Slide/Audio), what it covers, word count, character count, where to paste in NotebookLM (slide creation field / Audio Customize / Source)
- Warning: "Slide and Audio Customize fields truncate silently at ~6,000 chars. All prompts are kept under 5,000 chars for safety."
- Note: "All course materials (lecture slides, books, lists, simulados) should be uploaded as separate sources in the same NotebookLM notebook. These prompts guide how NotebookLM processes those sources."

### Step 10: Report

Show:
- Number of prompts generated (slides, audio, book)
- Per-prompt word and character counts
- Files saved to
- How to use: "Open file → Ctrl+A → Ctrl+C → paste into NotebookLM (slides → slide creation field; audio → Audio Customize or Source)"
- Reminder: "Upload all course materials (lectures, books, exercise lists, quizzes) as sources in the same notebook first" (reference actual directory names found in the project)

## Quality checklist (apply to every prompt)

- [ ] Slide prompt does not exceed 5,000 characters (field truncates silently at ~6,000)
- [ ] Audio Custom Prompt does not exceed 5,000 characters (field truncates silently at ~6,000)
- [ ] Audio Source prompt is ~3,000 words (higher limit — uploaded as source)
- [ ] Every major concept from the lecture/chapter is covered with its own paragraph of instructions
- [ ] Uploaded sources are referenced by name (e.g., "from the Aula 3 slides", "as in the uploaded N&S Chapter 5")
- [ ] Specific equations are named (e.g., "derive the Slutsky equation", not "discuss the decomposition")
- [ ] Textbook references are included (e.g., "as formalized in N&S §4.3")
- [ ] Cross-source connections are explicit (e.g., "connect the proof in J-R with the intuition from the lecture slides")
- [ ] Economic intuition is demanded alongside every formal result
- [ ] No bullet-point summaries — full paragraph explanations demanded
- [ ] Derivation steps are requested, not just results
- [ ] Code snippets demanded where computation is relevant (in the project's code language, default Python)
- [ ] File contains ONLY the prompt — zero metadata, zero headers, pure copy-paste ready
