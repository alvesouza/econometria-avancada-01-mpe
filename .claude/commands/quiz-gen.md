---
description: Generate quiz questions in MD format from course materials, and create/update the reusable HTML quiz template. Supports scoping by files or concepts, math-intensive and multi-part problems.
argument-hint: <source-files-or-concepts> [number-of-questions]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit
---

Generate a quiz from the materials or concepts specified by `$ARGUMENTS`.

## Workflow

### Step 0: Confirm quiz parameters with the user (MANDATORY — always ask)

**Every time you build a quiz, you MUST explicitly ask the user to confirm the generation parameters BEFORE writing any question — even when some were already provided in `$ARGUMENTS`.** Never silently fall back to defaults. Use a single interactive multi-question prompt (AskUserQuestion) and pre-fill each field with the value parsed from `$ARGUMENTS` (or the stated default) as the recommended first option, so the user can accept with one click or override.

Always ask about, at minimum:
1. **Number of questions** — recommend the count from `$ARGUMENTS`, else 20.
2. **Degree of math complexity / difficulty** — easy / medium / hard (see calibration in Step 4). This is the axis of how INTERTWINED topics are and how COMPLEX the math is.
3. **Math-intensive ratio** — confirm the 30–45% split; for non-math topics, whether to include math-intensive questions at all (see Step 3). Do **not** ask whether to use numbers: math questions are always symbolic (see "Symbolic, not numerical" in Step 4).
4. **Generation mode** — file-content / file-subject / topic-focused (see Step 1).

Only after the user confirms (or overrides) these do you proceed to Step 1. The one exception: if the user explicitly says "use defaults" / "don't ask", honor that for this run. The default posture is always to ask.

### Step 1: Understand the scope

Parse `$ARGUMENTS` to determine:
- **Source files**: specific files, a range, a directory, or "all". Do NOT assume fixed directory names — if given a directory, scan its contents to determine what kind of material it holds (lectures, lists, books, etc.)
- **Concepts**: specific topics (e.g., "Slutsky decomposition", "axiomas")
- **Number of questions**: explicit count, or default to 20 — **always confirmed with the user in Step 0**
- **Difficulty**: easy, medium, or hard (default: medium). **Always confirmed with the user in Step 0** (do not assume, even if provided).
  - **Easy**: single-topic, isolated concepts, direct formula application. Each question stays within one concept. Options are more distinct. Explanations are pedagogical.
  - **Medium**: 2-3 topics connected, multi-step reasoning, interpreting model outputs. Standard exam level. Questions may require applying a concept from one topic to answer about another.
  - **Hard**: graduate-level math complexity, deep cross-topic synthesis (e.g., endogeneity + heteroscedasticity + functional forms in one question), proofs, asymptotic arguments. Wrong options catch partial understanding of intertwined concepts.

  The key axis: how INTERTWINED topics become + how COMPLEX the math is.

- **Generation mode**: what drives the content. **Always confirmed with the user in Step 0** (3 options).
  - **File-content**: questions derived strictly from the file's content. Map cross-references enrich but don't expand scope.
  - **File-subject**: the file seeds the scope, but questions expand to the broader topics/subjects the file covers, pulling from any source via Map.
  - **Topic-focused**: questions organized by student weak areas. Auto-detect from latest quiz results in the quizzes directory (JSON exports, followup quizzes), present as suggestions, let user confirm/override/add. Pull from ANY source via Map.

### Step 2: Read project context

1. Read `CLAUDE.md` for course scope, bibliography, restrictions
2. Read `rules/` files for formulas, definitions, and code patterns
3. **ALWAYS** read `Map/` cross-references if they exist (from `/study-map`) — use them to:
   - Identify which concepts are covered where (lectures, exercises, exams, book chapters/pages)
   - Weight topics by importance (more cross-references = more questions)
   - Pull textbook references for `> Ref:` lines (include chapter AND page/section when available in the Map)
   - Find similar exercises for `> Similar:` lines
4. **Formulate questions from your own understanding of the concepts, NOT by rephrasing source file content.** When the user asks for a quiz on a specific book/file/topic, use the Map to understand what concepts are involved and their cross-references, then write original questions that test understanding. Never copy or closely paraphrase exercises, examples, or text from the source material.
5. If `Map/` doesn't exist, build references from `CLAUDE.md` and `rules/` directly
6. **Apply generation mode:**
   - **File-content**: the source file(s) from Step 1 define the scope. Read them deeply. Use Map cross-references to enrich questions but keep all questions traceable to the source file's content.
   - **File-subject**: the source file is the seed. Use Map to find ALL materials on the same topics — other lectures, book chapters, exercises. Questions can test any aspect of those topics, not just what appears in the original file.
   - **Topic-focused**: use Map + rules/ + quiz results to find ALL materials covering the target topics. If Map has `Complexity` and `Cross-topic synthesis` metadata, use them to calibrate. Auto-detect weak areas from the latest quiz results (look for JSON exports or followup quizzes in the quizzes directory), present as suggestions, let user confirm/override/add topics.

### Step 3: Assess math content

- Scan the source materials for math density (formulas, derivations, proofs)
- If the content is math-heavy (economics, econometrics, physics): apply the 30-45% math-intensive rule
- If the content is NOT math-heavy (qualitative topics, design systems, humanities): the choice of whether to include math-intensive questions or keep it fully conceptual is **confirmed with the user in Step 0**

### Step 4: Generate questions

Write questions in the MD format below. Follow these rules:

**Language:**
- **Write quizzes in English** — question stems, options, explanations and the `quiz:` title. This overrides any project-level language default (e.g. a CLAUDE.md setting Portuguese for generated content); quizzes are the exception.
- Keep technical terms in the form the course uses them; in a finance course they are usually already English (*stochastic discount factor*, *mean–variance frontier*, *security market line*).
- Use another language only if the user asks for it explicitly for that quiz.

**Distribution:**
- 30-45% math-intensive (derivations, comparative statics, proofs) — if applicable
- 55-70% conceptual (definitions, intuitions, comparisons, edge cases)
- If >15 questions: every topic/concept within scope gets at least 2 questions

**Symbolic, not numerical (CRITICAL — this governs every math question):**

Math questions are posed and answered in **literal parameters**, never in numbers. State the
model with its symbols ($\alpha$, $\beta$, $\delta$, $\sigma$, $s$, $n$, $\tau$, $\theta$)
and ask for an **expression**, a **sign**, or a **comparison**. Never hand the student a set of
numerical parameter values and ask them to compute a number.

- **Ask:** "Find the expression for $k^*$", "How does $k^*$ depend on $\delta$?", "What is the
  sign of $\partial c_1/\partial r$, and what decides it?", "Which is larger, $K_{ss}$ or
  $K_{gr}$, and why?"
- **Do not ask:** "With $s=0{,}24$, $n=0{,}01$, $\delta=0{,}05$ and $\alpha=1/3$, what is
  $k^*$?" — that question is answered by arithmetic, and a student can get it right while
  understanding nothing about what $k^*$ depends on.
- **Options are expressions**, in the same symbols the stem uses. Distractors are plausible
  *wrong expressions*: a flipped exponent ($\frac{1}{\alpha}$ where $\frac{1}{1-\alpha}$
  belongs), a dropped term ($\rho$ instead of $\rho+\delta$), an inverted ratio, a sign error.
  Never a set of decimals to choose between.
- **Never ask the student to evaluate an expression they just derived.** If a multi-part `P:`
  problem derives a formula in part (a), part (b) asks what happens to it when a parameter
  moves — not what number it equals.

**The one exception — empirical magnitudes.** A number belongs in a quiz when it is a *fact the
course asks you to know*, not arithmetic to perform: the capital share $\approx 1/3$, a Frisch
elasticity of 0,4 to 1 against Prescott's 2,3, a US job-finding rate near 30% per month, the
34% and 53% tax rates in Kurlat's Prescott calibration. These are quoted, not computed, and they
are legitimate. The test is simple: **if the student has to reach for a calculator, the question
is wrong.**

**Difficulty calibration:**
- **Easy**: each question tests ONE concept. No multi-part P: problems. Math = read one formula and say what it implies, or identify the correct expression among near-misses. 60-70% conceptual, 30-40% math.
- **Medium**: questions may connect 2-3 concepts. Multi-part P: problems allowed. Math = derive an expression in two or three steps, or sign a comparative static. Standard 55-70% conceptual / 30-45% math split.
- **Hard**: questions MUST cross topic boundaries. Multi-part P: problems encouraged. Math = proofs, asymptotic arguments, full derivations, comparisons of two expressions that differ by one term. 40-50% math-intensive, 50-60% conceptual (but "conceptual" here means deep synthesis, not recall). If Map has `Cross-topic synthesis` entries, use them to design intertwined questions.

**Multi-part problems and P: scoping:**
- Use `P:` to define a shared problem setup
- Follow with up to 3 `Q:` questions sharing that stem
- Each sub-question tests a different aspect
- Multi-part questions count toward the math-intensive quota
- **CRITICAL**: `P:` persists until the next `P:` or `##` boundary. If a standalone question follows multi-part questions in the same `##` section, insert an empty `P:` line before it to clear the problem stem. Failing to do this causes unrelated questions to display a wrong problem context.
- **A `P:` stem does NOT survive a `##` section boundary.** The parser resets the problem stem to null at every `##`. A `P:` written in one section is invisible to every question in the next one, so a stem that says "throughout this quiz" is a lie: it applies only until the section ends.

**Self-containment (CRITICAL — every question must stand alone):**

A student answers one question at a time, on one screen, seeing only that question's stem, its options, and the `P:` block currently active *in the same section*. Anything else you rely on is invisible to them.

- **Never refer to context the student cannot see on that screen.** Banned in a `Q:` stem unless a `P:` in the *same* `##` section supplies it: "the economy above", "in the same economy", "the stock above", "as before", "throughout this quiz", "that economy", "this discount factor" (when defined in a previous question). These render as dangling references and make the question unanswerable.
- **Restate every given the question needs, in the question.** Repetition across questions is correct and expected — it costs a few words and it is what makes each item independently gradable. A symbolic question must **define every symbol it uses**: if the answer is an expression in $\alpha$, $\beta$ and $\delta$, say what each one is in the stem, even if you said it two questions earlier. An undefined symbol is exactly as unanswerable as a dangling reference.
- **Never cite a book section number as the subject of a question.** "Which association between hypothesis and result of §1.5 is correct?" tests whether the student memorized the book's numbering, not whether they know the material — and a student reading the stem has no idea what §1.5 contains. State the substance instead ("Match each assumption to exactly what it buys"). Section and page numbers belong in the `> Ref:` line, which exists for exactly that purpose.
- Same rule for internal cross-references: no "as shown in the previous question", no "recall from item 12".
- **Sharing one model across a whole quiz is good design** — it lets a student follow one setup end to end — but implement it by *restating* the relevant symbols and assumptions in each stem, never by a single `P:` at the top and references back to it.
- **Verify before shipping.** After generating, confirm that no `Q:` stem outside an active `P:` contains: `above`, `the same economy`, `this quiz`, `earlier`, `previous`, `as before`, `that economy`. Every hit is a bug.

**Option quality (CRITICAL):**
- 3-5 options per question
- ALL options must be equally detailed, substantive, and plausible
- Wrong options should reflect common misconceptions or partial understanding
- Never use generic fillers like "None of the above" or obviously wrong answers
- For math questions: wrong options should contain plausible but incorrect formulas

**Option length balance (CRITICAL — anti-cheat):**
- The correct answer must NOT be consistently the most detailed or the longest option. A test-taker who picks "the most elaborate answer" must do no better than chance. This is the #1 giveaway in quizzes.
- Write the wrong options at a **similar level of detail** to the correct one — sometimes longer, sometimes shorter, sometimes the same. Across the whole quiz, the longest option should land on the correct answer no more often than on any distractor (roughly 1/n of the time).
- Distractors must carry the same kind of substance as the correct answer: plausible justifications, qualifications, or technical phrasing — not thin filler. If you cannot make a wrong option detailed without making it obviously wrong, make the correct answer more concise instead so the set evens out.
- **Match the writing style across all options of a question**, not just the length:
  - If the correct answer ends with a parenthetical (a clarification, a formula, a worked number, an example), the distractors must also end with comparable parentheticals — same kind, same approximate length. Never let parentheses appear on the correct option alone.
  - Match punctuation and structure: hedges ("necessariamente", "em geral"), inline formulas/symbols, units, em-dashes, lists, and sentence shape should appear in similar proportion on correct and wrong options.
  - The options should read as if written by the same hand with the same template — the only thing distinguishing the right one is that it is *true*, never that it is *formatted differently*.
- **Do not eyeball this — validate with the script.** After generating, run the established validator:
  ```bash
  python ~/.claude/commands/templates/quiz-validate.py <quiz.md>   # or the project copy at .claude/quiz-validate.py
  ```
  It gates (FAIL → exit 1) on: parse integrity; answer letters spread ~evenly with no run ≥3; **no question where the correct option is ≥8 chars longer than every distractor** (the perceptible giveaway); **mean length of correct vs distractors within ±2 chars**; and **no question where a parenthesis/inline-formula/hedge marks the correct option alone — or marks every option but the correct**. Rewrite the flagged options and re-run until it prints `PASS`. A correct option that is longest by only 1–2 chars is reported as `INFO`, not a failure — that margin is not exploitable. Do not hand-write a one-off check; extend `quiz-validate.py` if a new gate is needed.

**Answer position distribution (CRITICAL — anti-pattern):**
- Correct answers MUST be distributed roughly evenly across positions A, B, C, D across the full quiz.
- For a quiz with N questions and 4 options: each letter should appear as correct ~N/4 times (±2).
- NEVER cluster the same correct letter for consecutive questions.
- After writing all questions, tally the distribution and shuffle correct positions if needed.
- Use all base64 encodings: `YW5zOjA=` (A), `YW5zOjE=` (B), `YW5zOjI=` (C), `YW5zOjM=` (D).

**Currency and special characters:**
- NEVER use bare `$` for currency (e.g., `R$1`), as KaTeX interprets `$` as a math delimiter. Write `1 real`, `1.000 reais`, `USD 100`, etc. instead. This comes up rarely now that math questions are symbolic — currency belongs only in an empirical-magnitude question.

**Answer encoding:**
- Encode the correct answer as `<!-- base64(ans:N) -->` where N is the 0-indexed position
- Use Python: `import base64; base64.b64encode(b'ans:N').decode()`
- The encoding prevents students from spotting correct answers when browsing the MD file

### MD Question Format

```markdown
---
quiz: "Quiz Title"
tags:
  tag-id: "Topic Display Label"
  another-tag: "Another Topic"
---

## tag-id

Q: Question text with $\LaTeX$ math support?
- Option A with detailed explanation of why this might seem correct
- Option B with equally detailed reasoning
- Option C with substantive technical content
- Option D with plausible alternative interpretation
- Option E (optional 5th option)
<!-- base64(ans:N) -->
> Explanation of why the correct answer is correct and why common wrong answers are wrong.
> Ref: Book Title, Cap. N, Sec. X-Y; Another Book §M.N
> Similar: Book, Cap. N, Exercício N.M; Lista K, QN

P: Multi-part problem setup with given values and conditions.

Q: First sub-question?
- Option A
- Option B
- Option C
- Option D
<!-- base64(ans:N) -->
> Explanation for Q1.
> Ref: ...
> Similar: ...

Q: Second sub-question building on the same setup?
- Option A
- Option B
- Option C
- Option D
<!-- base64(ans:N) -->
> Explanation for Q2.
> Ref: ...
> Similar: ...

P:

Q: Standalone question (no problem stem — empty P: clears the context)
- Option A
- Option B
- Option C
<!-- base64(ans:N) -->
> Explanation.
```

### Parser contract (CRITICAL — violating these silently breaks the quiz)

The HTML player parses line-by-line with no tolerance for stray blank lines inside a question. The failure mode is silent: the answer defaults to A and the explanation is dropped. Enforce exactly:

- **`## tag-id` is a single whitespace-delimited token** and must match a key in the frontmatter `tags:` map. The parser captures only the first token, so `## Equilíbrio Geral` becomes the tag `Equilíbrio` (label lost). Use `## eg` with `eg: "Equilíbrio Geral"` in frontmatter.
- **No blank line between the last `- option` and the `<!-- ans -->` comment.** The answer comment must be the very next line after the options.
- **No blank line between the `<!-- ans -->` comment and the first `>` explanation line.** Explanation lines (`>`, `> Ref:`, `> Similar:`) are contiguous.
- **One blank line between questions** (after the last `>` line, before the next `Q:`/`P:`/`##`). This is the only blank line allowed inside a question region.
- **`Q:` text is one line** (continuation lines are folded only until the first `- option`); keep each question stem on a single line.
- **Base64 answer table** (`ans:N`, 0-indexed): A→`YW5zOjA=`, B→`YW5zOjE=`, C→`YW5zOjI=`, D→`YW5zOjM=`, E→`YW5zOjQ=`, F→`YW5zOjU=`.

After writing the file, run `quiz-validate.py` (see "Option length balance" above) — one command covers parse integrity (every `<!--` decodes; each question has ≥2 options + a decoded answer + an explanation), answer spread/runs, and the anti-cheat length/style gates. Ship only on `PASS`.

### Step 5: Save the quiz MD file

Save to the project's quizzes directory (auto-discovered — e.g., `Simulados/`, `Quiz/`, etc.) as `quiz-<topic>-<date>.md`, or to the directory the user specified.

### Step 6: Ensure quiz.html exists (copy the canonical template)

There is ONE canonical player, kept at `~/.claude/commands/templates/quiz.html` (Windows: `C:\Users\<user>\.claude\commands\templates\quiz.html`). Do not hand-write or redesign the HTML — the parser is a strict contract (see "Parser contract" above) and the export feature is fragile.

- If the project root has **no** `quiz.html`: copy the template verbatim to the project root.
- If the project root **already has** a `quiz.html` but it lacks the standalone-export feature (no `id="embeddedQuiz"` / `exportStandaloneHTML`): overwrite it with the template so exports work. Tell the user you replaced it.
- Never edit the project copy by hand; if the player needs a change, edit the template and re-copy.

```bash
cp ~/.claude/commands/templates/quiz.html ./quiz.html
```

The template (course-agnostic — title/tags come from the .md frontmatter) provides:
- **File picker** + drag-and-drop to load a quiz `.md`; KaTeX math; dark-mode card UI with letter-labeled options, progress bar, topic-colored badges.
- **Per-question feedback**: correct (green) / wrong (red) highlight, explanation, `📚 Ref:` and `🔗 Similar:` lines.
- **Dashboard**: score ring, per-topic bars, wrong-answer list, JSON export for `/quiz-analyze`.
- **localStorage** resume.
- **Perfect standalone export** (the key feature): the `💾 HTML` / `Exportar HTML` button serializes the live DOM and bakes the quiz `.md` into `<script type="text/quiz" id="embeddedQuiz">` and the progress into `<script type="text/quiz-state" id="embeddedState">`. On open, `autoStart()` reads those tags, hides the picker, and restores the exact session — so the exported file works identically to the original with the questions already imported, offline, no `.md` needed.
- Empty `P:` clears the current problem stem (`currentProblem = null`).

### Step 7: Report

Show:
- Number of questions generated (total, math-intensive, conceptual, multi-part)
- Confirmation that every math question is symbolic, and the list of any questions that quote an empirical magnitude, with the source of each number
- Topic distribution
- File saved to
- How to run: `python -m http.server` + open quiz.html
