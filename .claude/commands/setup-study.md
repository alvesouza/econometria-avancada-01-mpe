---
description: Scaffold a new study project with directory structure, CLAUDE.md, rules files, quiz template, README, and local copies of all commands.
argument-hint: <course-name>
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion
---

Create a new study project for the course `$ARGUMENTS`.

## Instructions

### Step 0: Auto-discover project structure

**CRITICAL — Do NOT assume fixed directory names.** Before anything else, scan the project root (or target directory) and identify what already exists:

1. List all directories and files in the project root.
2. Identify each directory's **purpose** by its name pattern AND contents — not by matching an exact name:
   - **Lectures**: slide PDFs, .html presentations, .R/.py scripts from class (e.g., `Aula`, `Aulas`, `Lectures`, `Slides`)
   - **Exercise lists**: problem sets, homework PDFs (e.g., `Listas`, `Lista`, `Exercises`, `Lists`)
   - **Books/Textbooks**: textbook PDFs, solution manuals (e.g., `Livros`, `Books`, `Textos`, `Bibliografia`)
   - **Tutorials/Office hours**: supplementary review materials (e.g., `Monitoria`, `Tutoria`, `Tutorial`)
   - **Exams/Tests**: exam papers and solutions (e.g., `Prova`, `Provas`, `Exams`, `Tests`)
   - **Quizzes**: quiz MD files for quiz.html (e.g., `Simulados`, `Quizzes`, `Quiz`)
   - **Rules**: topic rule files (e.g., `rules`, `regras`)
   - **Maps**: cross-reference files (e.g., `Map`, `Maps`)
   - **Solutions**: generated exercise solutions (e.g., `Resolucao`, `Resolução`, `Solutions`)
   - **NotebookLM prompts**: prompt files (e.g., `NotebookLM`)
   - **Readings / narrations**: isolated chapter extracts and TTS scripts (e.g., `Leituras`, `Readings`, `Narracoes`)
   - **Notebooks / lab**: Jupyter projects for simulation and data work, one subdirectory each (e.g., `Notebooks`, `Laboratorio`, `Lab`)
3. **Preserve existing names** — if the user already has `Aula/` (singular), do NOT create `Aulas/` (plural). Adapt to their convention.
4. Store the discovered mapping (purpose → actual directory name) and use it throughout all subsequent steps.
5. Only create directories that don't already exist, using the user's naming convention (language, singular/plural).

### Step 0.5: Locate the companion projects - ALWAYS, and ask if they are missing

Two sibling repositories carry work that must never be rewritten per project. Find them
before doing anything else, because what they contain changes how the rest of this command
behaves.

| Project | What it carries | Consumed by |
|---|---|---|
| **Video explainer** | the Manim kit (`manim_kit.py`), the narration client (`speechify_tts.py`), the frame-accurate compiler (`explainer_compile.py`), and the `/explainer`, `/manim-kit` and `/companion` commands | every video the study project makes |
| **Efficient Token** | the token-governance layer: rule packs, the retrieval escalation ladder, model routing, and enforced context budgets | how the agent works inside the study project |

**Where to look, in order:**

1. The **parent directory of the project being set up** - that is, as siblings of the new
   project folder. This is the expected layout.
2. The parent of the current working directory.
3. `~/Documents/Git/Github/`.

Match on the directory name, case-insensitively, allowing a hyphen or underscore in place of
the space (`video-explainer`, `Efficient_Token`).

**If either one is not found, ask. Do not proceed silently and do not invent a path.** Use a
single `AskUserQuestion` round covering both, with one question per missing project:

> "I could not find **Video explainer** next to this project. Does it exist?"
> - **Yes - it is at another path** (the user gives it; verify the path holds `install.py`
>   or `lib/manim_kit.py` before believing it)
> - **No - create it here** (scaffold it from `~/.claude/commands/templates/`, which holds
>   `manim_kit.py`, `speechify_tts.py` and `explainer_compile.py`)
> - **No - skip video tooling** (the study project is set up without `/explainer`,
>   `/manim-kit` or `/companion`, and the README says so rather than advertising commands
>   that will not work)

Same three-way question for **Efficient Token**, whose third option is "skip - do not apply
its conventions".

**When Video explainer is found**, install from it rather than from the global templates,
because the repo is the newer source:

```bash
python "<video-explainer>/install.py" --into "<project>"
```

It runs `pip install -e` on that repo, so the project imports the shared layer and **holds no
copy of its code**; it then installs the slash commands (which ARE copied, since a project
edits its own) and probes the toolchain. Scenes then use `from video_explainer import ...`,
and the gates are the console scripts `beatcheck`, `speechify-tts`, `explainer-compile`.

**Never vendor the shared layer into a study project.** If a copy of `manim_kit.py`,
`speechify_tts.py`, `explainer_compile.py` or `beatcheck.py` appears inside the project,
delete it and reinstall - a copy is how fixes stop propagating.

Record both resolved paths in the generated `CLAUDE.md`, so the next session does not repeat
this search.

### Step 0.6: Adopt Efficient Token properly - not just link it

Linking the repo and quoting two of its rules is **not** adoption. Run its own installer and
let it enforce its own budgets. This sequence was proven on `Macroeconomia 01 - MPE`, where it
cut the always-on file from **3,260 tokens to 882** - a 73 per cent reduction in what is
re-sent every single turn, or ~130,400 token-turns down to ~35,280 over a 40-turn session.

**1. Dry run first, always.** It tells you what would be touched, and answers the one
dangerous question - whether your hand-written `CLAUDE.md` survives:

```bash
python "<efficient-token>/tools/adopt.py" "<project>" --packs core,context --claude-only --dry-run
```

Look for `skip (exists) ... CLAUDE.md  <- add the GENERATED markers by hand`. That is the
tool telling you it will not clobber your file. If you see `would write CLAUDE.md` instead,
stop and work out why before proceeding.

**2. Choose packs that match the course.** `--list` prints them. Always take `core` and
`context`; add `codebase-work` and `model-routing`; then the **domain** pack and the
**language** pack:

| Course subject | Pack |
|---|---|
| Macroeconomics | `macroeconomics` |
| Microeconomics | `microeconomics` |
| Econometrics | `econometrics`, `microeconometrics` |
| Game theory | `game-theory` |
| Finance | `behavioral-finance` |

| Code language | Pack |
|---|---|
| Python | `lang-python` |
| JS/TS | `lang-js-ts` |
| C# | `lang-csharp` |

```bash
python "<efficient-token>/tools/adopt.py" "<project>" \
  --packs core,context,codebase-work,model-routing,<domain>,<lang> --claude-only
```

Use `--claude-only` unless the project also uses GitHub Copilot surfaces.

**3. Compile the tier-0 contract into `CLAUDE.md`.** The installer will not edit a file you
wrote. Add the markers by hand, with nothing between them, then sync:

```
<!-- GENERATED:tier0:start -->
<!-- GENERATED:tier0:end -->
```

```bash
cd "<project>" && python tools/sync_rules.py
```

The fourteen non-negotiable rules are now live in the project rather than quoted at it.

**4. Get under the 900-token budget, and verify it.** This is the step that makes adoption
real. The generated block costs ~570 tokens, so the course's own tier-0 content has ~330 to
work with:

```bash
python tools/token_report.py --budget
```

Iterate until it stops saying `BUDGET EXCEEDED`. **Keep in `CLAUDE.md`** only: the course
identity in two lines, the scope guard, the language and format rules, the sibling-project
paths, and the secrets rule. **Move out** to a tier-2 file such as `rules/11_curso_programa.md`,
loaded on demand: the lecture x bibliography table, the bibliography with edition divergences,
the evaluation weights, the rules index, and the directory structure.

Most of that detail usually **already exists** in `Map/`, so moving it is not a loss - it is
lever four, *do not say it twice*.

**5. Wire the check.** `python tools/sync_rules.py --check` belongs in CI so the surfaces
cannot drift from the packs.

**6. Create `.agent/`.** `plans/` takes a written plan before any non-trivial change;
`notes/<topic>.md` takes findings that would otherwise be re-derived next session. Both are
tier-0 rules 3 and 7, and both are worthless unless the directory exists.

> **Known wrinkle, do not be alarmed by it.** `sync_rules.py` will report the course's own
> content rules - `rules/00_*` through `rules/NN_*` - as *"missing frontmatter `id`, skipped"*.
> That is correct: they are content rules sharing a directory with governance packs, and only
> the packs are machine-managed. If it bothers you, move the course rules to `rules/curso/`.

**What the project gets.** Six-plus rule packs, the `ctx` / `route` / `codebase` / `rulesmith`
skills and a domain skill, seven subagent definitions, two `PreToolUse` hooks, the token and
sync tooling, and a CI workflow - all governed by an enforced budget rather than good
intentions.

### Step 1: Gather information

Ask the user for:
- **Course name** (full name and abbreviation)
- **Professor** name
- **Institution / program** (e.g., "Insper — Mestrado Profissional em Economia")
- **Bibliography**: main textbook + complementary references (title, author, edition) — or say "look at the files" to auto-detect from existing book PDFs and lecture slides
- **Topics list**: each topic with its corresponding lecture number and textbook chapters — or say "look at the files" to auto-extract from lecture filenames/contents and match to book TOCs
- **Language**: for content output (default: **English**, per the global rule in
  `~/.claude/CLAUDE.md` — everything generated is written in English even when the course,
  the slides and the books are in another language). Ask only to confirm; a different
  language is set here only if the user explicitly asks for one, and existing files already
  written in another language are never translated as part of the setup.
- **Grading style**: the default exam style, or a named one from
  `~/.claude/commands/templates/styles/` (list the files, e.g. `macro-1` — the Macroeconomia I
  MPE style). Default: the generic template.
- **Code language**: R, Python, or both (default: R). ⚠️ The notebook commands (`/lab`,
  `/lab-init`, `/lab-data`) are **Python/Jupyter only** — if the course is R-based, record
  that in `CLAUDE.md` and tell the user those three do not apply.

**If the user says "look at the files" for bibliography or topics:**
1. Read the first few pages of each lecture PDF to extract topic titles, chapter references, and bibliography slides
2. Read the TOC pages of each textbook PDF in the books directory
3. Cross-reference lecture topics with book chapters to build the mapping automatically
4. Present the extracted mapping to the user for confirmation before proceeding

### Step 2: Create directory structure

Create only the directories that don't already exist. Use the discovered naming convention. The required purposes (with example names) are:

```
<course-name>/
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── settings.json
│   └── commands/          ← copies of all global commands
├── <lectures-dir>/        ← existing or new (e.g., Aula, Aulas)
├── <lists-dir>/           ← existing or new (e.g., Listas, Lista)
├── <tutorials-dir>/       ← existing or new (e.g., Monitoria)
├── <quizzes-dir>/         ← existing or new (e.g., Simulados)
├── <books-dir>/           ← existing or new (e.g., Livros)
├── rules/
├── <solutions-dir>/       ← existing or new (e.g., Resolucao)
├── Map/
├── NotebookLM/
│   ├── slides/
│   ├── audio/
│   └── video/
├── <readings-dir>/        ← existing or new (e.g., Leituras) — chapter extracts + TTS scripts
├── <notebooks-dir>/       ← existing or new (e.g., Notebooks) — one subdir per Jupyter project
├── Videos/                ← one subdir per /explainer video (created on first use)
├── .env.example           ← template for API keys; the real .env is gitignored
└── quiz.html
```

`<readings-dir>/` is where `/speechify` writes its narrations and where an isolated book
chapter cut out of a large PDF belongs. `<notebooks-dir>/` is created on first use by
`/lab-init`, which also writes its index `README.md` there — do not pre-populate it.

### Step 3: Generate CLAUDE.md

Follow the Econometria project pattern:
- Course scope (which topics, which lectures)
- "NAO extrapolar" restriction
- Topic × textbook reference table (Aula | Tópico | Livro principal | Outros)
- Lists covered
- Bibliography section with usage guidelines
- Language and format restrictions (see below)
- Rules index table linking to each `rules/*.md` file

**The language and format section must agree with `~/.claude/CLAUDE.md`, and must not
restate it at length.** The global file already mandates these; the project file records
only what is project-specific. Write it as:

- **Output language: English** — every new file, document, prompt and answer generated for
  this project is written in English, even when the course, the books and the existing
  materials are in another language. Quotes keep the original language; identifiers, file
  paths and book/chapter/section titles are cited verbatim. Existing files written in
  another language are not translated unless the user asks.
- **Technical terms** stay in the form the course uses them, and section, chapter and figure
  names from the books are cited in the original.
- **Math in LaTeX**: `$...$` inline, `$$...$$` display. Never a bare `$` for currency —
  write "120 reais" / "120 dollars".
- **PDFs must be copyable**: any `.tex` compiled with `pdflatex` carries `\usepackage{lmodern}`
  and `\usepackage{cmap}` right after `\usepackage[T1]{fontenc}`; verify with `pdffonts`
  (every font Type 1, never Type 3). LuaLaTeX or XeLaTeX is the equivalent alternative.
- **NotebookLM output language is an app setting**, never a prompt line: it is set once in
  NotebookLM's Settings → Output language and applies to every type, audio included. A
  generated prompt must not carry a language instruction — it burns ~140 of the ~5,000
  characters to restate a setting no prompt can override. Record in `CLAUDE.md` that the
  setting is confirmed before generating a batch.
- **Code language** as chosen in Step 1, with the reference implementation named.

### Step 4: Generate rules/ files

One file per topic (e.g., `rules/01_topicname.md`), each with:
```markdown
# Topico N - Topic Title

> **Aula N** - Topic subtitle
> **Main Book** - Chapter X, Sections Y-Z
> **Other refs** - ...

---

## Key Concept 1
[placeholder for formulas, definitions]

## Key Concept 2
[placeholder]

## Code Patterns
[placeholder for R/Python code templates]
```

### Step 5: Copy global commands and shared templates

1. Copy all `.md` files from `C:\Users\pedro\.claude\commands\` into the project's `.claude\commands\` directory (local copies the user can customize). This includes `exam-gen.md` and `exam-grade.md`, the material front door `intake.md`, and the three notebook commands `lab.md`, `lab-init.md` and `lab-data.md`. Copy the whole directory — do not hand-pick a subset, or a new command added globally will silently never reach new projects.
   **Exception:** if **Video explainer** was located in Step 0.5, take `explainer.md`, `manim-kit.md`, `companion.md` and the three Python modules from that repo's `install.py` instead — it is the newer source, and the installer reports any file that differs rather than clobbering local edits.
2. Set up the **exam/list tooling** (used by `/exam-gen` and `/exam-grade`):
   - Copy `~/.claude/commands/templates/lista-exam.tex` into the project (e.g., `<lists-dir>/lista-exam.tex`) — the LaTeX template for lists/simulados (single source, `\ifsolucoes` toggle for blank list vs. gabarito+rubrica; preamble already follows the global lmodern+cmap copyable-PDF rule).
   - Copy `~/.claude/commands/templates/estilo-avaliacao.md` into `rules/00_estilo_avaliacao.md` — the exam-style rules (taxonomy, contextualization, solution/rubric format, bibliography usage). Adapt the institution/bibliography names to this course.
     If Step 1 chose a **named grading style**, copy `~/.claude/commands/templates/styles/<name>.md`
     instead. Keep its grading rules (question anatomy, scoring, distractors, solution and
     rubric format, graduate mode); rewrite its course bindings for this course (bibliography,
     block-to-lecture table, scope exclusions, institutional context, template path, and
     subject-specific examples when the subject differs). Record the style's name in `CLAUDE.md`.

### Step 6: Generate quiz.html

Copy the canonical quiz player from `~/.claude/commands/templates/quiz.html` into the project root as `quiz.html` (verbatim — it has the perfect standalone-export feature). See `/quiz-gen` for the MD format the player consumes.

Also copy the quiz validator `~/.claude/commands/templates/quiz-validate.py` into the project's `.claude/` directory — `/quiz-gen` runs it to gate every generated quiz (parse integrity + anti-cheat length/style checks). Do not hand-write one-off checks; this script is the single source of truth.

### Step 6.5: Set up the video tooling (only if the user wants narrated videos)

`/explainer` depends on two shipped scripts and one secret. Copy both scripts from
`~/.claude/commands/templates/` into the project's `.claude/` directory:

- `speechify_tts.py` — text-to-speech narration; turns a beat sheet into audio clips plus a
  manifest of **measured** durations, which is what the animation times itself against.
- `explainer_compile.py` — compiles the rendered beats and the narration into one video,
  frame-accurately, and fails if audio and video drift by more than a frame.

Then create `.env.example` in the project root (committed, no values) and add `.env`,
`.env.*`, `!.env.example` to `.gitignore`. The real key goes in `.env`, which is never
committed. Verify the ignore actually works with `git check-ignore -v .env` — do not assume it.

Also add the render artefacts to `.gitignore`: `Videos/*/media*/` (covers any `--media_dir`
variant such as `media_nocache/`), `Videos/*/audio/`, `Videos/*/build/`, `Videos/**/*.mp4`
(every generated video at any depth, the final one included) and `Videos/*/*.log`.

Tell the user what `/explainer` needs that this step cannot provide: a **Speechify API key**
in `.env` as `SPEECHIFY_API_KEY`, **Manim CE** (`python -m pip install manim`), **ffmpeg** on
PATH, and a **LaTeX** install for `MathTex`. Then have them run
`speechify-tts --check`, which verifies the key, the models, the voice list
and ffprobe in one call. Do not install anything silently.

### Step 6.6: Set up the agent tooling (Ponytail, Graphify)

Both are **third-party** and neither is installed silently — print the commands and let the
user run them, the same contract as Step 6.5.

**Ponytail** ([DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)) — a
Claude Code plugin that makes the agent justify code before writing it. It is installed at
**user scope, once per machine**, and then applies to every project, so this step is a
*check*, not a per-project install. Run `claude plugin list`; if it is absent, tell the user:

```bash
claude plugin marketplace add DietrichGebert/ponytail
claude plugin install ponytail@ponytail --scope user
```

Controls are `/ponytail [lite|full|ultra|off]` and `/ponytail-review`. Do not pin a default
mode in the project's settings unless the user asks — `PONYTAIL_DEFAULT_MODE` is a personal
preference, not a project convention.

**Graphify** — the code-knowledge-graph behind the first rung of the retrieval ladder in
`CLAUDE.md` ("graph query → symbol lookup → structural search → ripgrep → file slice →
whole file"). Efficient Token's `docs/03-context-tooling.md` is the authority; `tools/adopt.py`
prints the canonical sequence:

```bash
pip install graphifyy          # note: two y's on PyPI; the CLI is `graphify`
graphify update .              # AST-only, fast, no API key
graphify claude install        # PreToolUse hook: redirects grep/find to graph queries
```

Then, in the project:

1. Write a **`.graphifyignore`** at the repo root. For a study project this matters more than
   in a code repo: the bibliography is hundreds of megabytes of PDFs plus their plain-text
   conversions, and indexing it swamps the graph. At minimum exclude the books directory, the
   NotebookLM sources, converted readings, `graphify-out/`, `__pycache__/`, `.venv/`, `*.pdf`
   and every `data/`, `cache/` and `figures/` directory.
2. Add `graphify-out/` to `.gitignore`.
3. Add to `.claude/settings.json`: `"Bash(graphify query:*)"`, `"Bash(graphify path:*)"`,
   `"Bash(graphify explain:*)"`, `"Bash(graphify update:*)"` under `permissions.allow`, and
   `"GRAPH_PATH": "graphify-out/graph.json"` under `env` — matching Efficient Token's own
   `.claude/settings.json`.

> ⚠️ **Measure before adopting, and say so.** Efficient Token's own guidance: Graphify is the
> *wrong* tool for "small repos (<200 files) where ripgrep is already cheap" and "repos that
> are mostly config or data". A study project is usually exactly that — mostly markdown, PDFs
> and notebooks, with a handful of Python files. Count the parseable code files first
> (`git ls-files | grep -cE '\.(py|ipynb|js|ts)$'`). If the answer is a few dozen against
> hundreds of prose files, install Graphify but **skip `graphify claude install`**: the hook
> intercepts grep/find and redirects to the graph, which actively gets in the way when most
> searching is over prose. Report the count to the user and let them decide, rather than
> wiring the hook by default.

### Step 7: Generate README.md

Include:
- Project structure explanation (what each directory is for)
- Available slash commands with usage examples (use the actual directory names from the project):
  - `/convert <lectures-dir>/` — convert lecture PDFs to markdown
  - `/summarize <lectures-dir>/` — summarize all lectures
  - `/list-exercises <lists-dir>/` — extract all exercises
  - `/solution <lists-dir>/list-file.md` — solve exercises from a list
  - `/exam-gen <topics>` — generate an exam-style exercise list + solution key & rubric (LaTeX, simulado style); asks depth / tangential topics / math complexity first
  - `/exam-grade <lists-dir>/lista-X.tex <my-resolution>` — grade and analyze your own resolution against the rubric, with book references
  - `/exercise-plan <topics>` — curated practice plan referencing real exercises in the source books (number + page), weighted by subtopic and distributed across knowledge levels
  - `/quiz-gen <quizzes-dir>/` — generate quiz from MD question files
  - `/quiz-analyze <paste results>` — analyze quiz performance
  - `/study-map .` — generate Obsidian cross-reference maps
  - `/notebooklm <lectures-dir>/` — generate NotebookLM prompts (slides, audio, video) for all lectures; asks the unit of organisation and the count per type first
  - `/speechify <topic-or-file>` — narrated plain-text script for Speechify or any TTS app (math spoken in words, no tables, no code); `--split` for one file per part, `--short` for a revision-only pass
  - `/intake <file-or-dir-or-topic>` — front door for material that just arrived: converts it, analyses it against what the project already holds, then asks **in one round** whether to produce a TTS narration (`/speechify`) and/or NotebookLM prompts (`/notebooklm`), and with which characteristics
  - `/lab <topic-or-question>` — build a Jupyter project that visualises or tests a mechanism; orchestrates `/lab-init` and `/lab-data`, then runs the notebook end to end and verifies its numbers
  - `/lab-init <slug>` — scaffold `<notebooks-dir>/<slug>/`: notebook skeleton, `data/`, `figures/`, the shared figure style, `requirements.txt`
  - `/lab-data <series-or-concept>` — fetch and cache macro series (FRED, World Bank WDI, Penn World Table, Maddison, BCB SGS, IBGE SIDRA, Ipeadata) with a provenance registry; `--offline` never touches the network
  - `/explainer <topic>` — plan and produce a 3blue1brown-style narrated video: beat sheet, script, Manim CE scenes timed to synthesised speech, compiled into one **1080p** `.mp4` with subtitles; asks purpose, length, math intensity and examples first. Needs a Speechify key in `.env` (see Step 6.5)
  - `/manim-kit <project>` — install and drive the shared drawing layer from the **Video explainer** repo, so a new video costs a short scene file instead of a thousand lines of animation
  - `/companion <model>` — an interactive page with several controls for one model; only ever runs when asked for, and asks in detail first
- How to run quizzes:
  1. `cd <project-dir>`
  2. `python -m http.server`
  3. Open `http://localhost:8000/quiz.html` in browser
  4. Select the quiz MD file to load
- How to navigate the project in Obsidian (open the root as a vault)
- NotebookLM workflow (use actual directory names):
  1. Upload all course materials (lectures, books, lists, quizzes) to NotebookLM
  2. Run `/notebooklm <lectures-dir>/` to generate prompts
  3. Open each prompt file → Ctrl+A → Ctrl+C → paste into NotebookLM

### Step 8: Auto-convert all materials

Scan the entire project for convertible files (HTML, PDF, PPTX, DOCX, EPUB, TXT, etc.) in **all discovered directories** and root.

**For the books directory:** Ask the user before converting:
> "Found N book PDFs in <books-dir>/. Converting large textbooks can take several minutes and produce very large MD files. Convert books now?"
>
> Options: **Yes, convert all books** / **No, skip books for now** / **Let me pick which books**

Run `/convert` on the selected files. This is the entry point for the rest of the ecosystem:
- Converted lectures feed `/summarize` and `/quiz-gen`
- Converted books feed `/study-map` cross-references (more precise chapter-level linking)
- Converted exercise lists feed `/list-exercises` and `/solution`
- Any converted reading feeds `/speechify` when the user wants to study by listening
- Anything that arrives **after** setup — a new lecture, a new list, a chapter extract —
  goes through `/intake`, which analyses it and asks what to derive from it instead of
  guessing; and `/lab` when the topic is worth simulating or confronting with data

If existing `.md` files are found, ask the user once (overwrite all / skip all / let me pick).

### Step 9: Generate initial study map

**Before generating:** Check if books in the books directory have been converted to MD. If not, warn:
> "Books are not yet converted to MD. The study map will use chapter references from CLAUDE.md and rules/ only. For precise chapter-level cross-references, run `/convert <books-dir>/` first."

After conversion (or warning), run `/study-map .` to create the `Map/` cross-reference files linking books to lectures to exercises.

### Step 9.5: Copy original sources for NotebookLM upload

Create a `NotebookLM/sources/` directory and copy **all original source files** into it as a flat collection ready for bulk upload to NotebookLM. This saves the user from hunting across subdirectories.

**What to copy:**
1. All files from `<lectures-dir>/` (slides, scripts, articles)
2. All files from `<lists-dir>/` (including subdirectories)
3. All files from `<books-dir>/`
4. All files from `<tutorials-dir>/`
5. All files from `<exams-dir>/`

**NotebookLM supported formats:**
pdf, txt, md, docx, csv, pptx, epub, 3g2, 3gp, aac, aif, aifc, aiff, amr, au, avi, cda, m4a, mid, mp3, mp4, mpeg, ogg, opus, ra, ram, snd, wav, wma, avif, bmp, gif, ico, jp2, png, webp, tif, tiff, heic, heif, jpeg, jpg, jpe

**Conversion rule:** For each file, check its extension against the supported list above.
- **If supported** → copy as-is to `NotebookLM/sources/` with the category prefix.
- **If NOT supported** → convert to `.txt` (cheapest for AI) before copying:
  - **Code files** (.R, .py, .jl, .m, .do, .sas, .sql, .js, .ts, etc.) → copy as `.txt` (just change the extension — the content is already plain text)
  - **HTML files** (.html, .htm) → convert to `.md` via `markitdown`, then copy the `.md`
  - **Other text-based files** (.json, .xml, .yaml, .yml, .toml, .ini, .cfg, .log, .tex, .bib, .sty) → copy as `.txt`
  - **Binary files with no supported equivalent** → skip and warn the user

**Naming convention:** Prefix each copied file with its source category:
- `Aula_<filename>.ext` (or `.txt` / `.md` if converted)
- `Lista_<filename>.ext`
- `Livro_<filename>.ext`
- `Monitoria_<filename>.ext`
- `Prova_<filename>.ext`

**After copying:** List all filenames in `NotebookLM/sources/` so the `/notebooklm` command can reference them by exact name when generating prompts.

### Step 10: Show summary

Print what was created and list available commands with examples. Include:
- Directory structure created
- Number of rules files generated
- Number of files converted
- Number of cross-references in Map/
- Reminder about `/notebooklm` for generating study prompts
