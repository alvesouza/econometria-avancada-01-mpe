---
description: Generate Obsidian-friendly cross-reference maps linking books, lectures, exercises, quizzes, and tutorials. Creates Map/ directory with wiki-links and tags.
argument-hint: <dir>
allowed-tools: Read Grep Glob Bash PowerShell Write Edit
---

Generate cross-reference maps for the study project at `$ARGUMENTS` (default: current directory).

## Instructions

### Step 0: Auto-discover project structure

**Do NOT assume fixed directory names.** Scan the project root and identify each directory's purpose by its name pattern AND contents:
- **Lectures**: slide PDFs, .html presentations, .R/.py scripts (e.g., `Aula`, `Aulas`, `Lectures`, `Slides`)
- **Exercise lists**: problem sets, homework PDFs (e.g., `Listas`, `Lista`, `Exercises`)
- **Books/Textbooks**: textbook PDFs, solution manuals (e.g., `Livros`, `Books`, `Textos`)
- **Tutorials/Office hours**: supplementary review materials (e.g., `Monitoria`, `Tutoria`)
- **Exams/Tests**: exam papers and solutions (e.g., `Prova`, `Provas`, `Exams`)
- **Quizzes**: quiz MD files (e.g., `Simulados`, `Quizzes`)
- **Rules**: topic rule files (e.g., `rules`, `regras`)

Store the discovered mapping and use actual directory names throughout.

### Step 0b: Check book conversion status

Check if books in the discovered books directory exist as PDFs without corresponding `.md` files.

If unconverted books are found, ask the user:
> "Found N book PDFs in <books-dir>/ without MD versions. Converting books enables precise chapter-level cross-references in the study map. Without conversion, the map will use references from CLAUDE.md and rules/ only."
>
> Options: **Convert books first** (run `/convert <books-dir>/`) / **Skip — use CLAUDE.md references only**

If the user chooses to convert, run `/convert` on the books directory before proceeding.

### Step 1: Scan the project (DEEP)

Find all materials in the discovered directories. Also read:
- `rules/` — topic rule files
- `CLAUDE.md` — course scope and bibliography
- **All converted MD files** in `markitdown/` subdirectories — these are the primary source for exercise-level detail

**For each exercise list**, read the converted MD (or PDF if no MD) and extract:
- **Each question number** and its **problem context** (e.g., "Q1: WAGE2 dataset, lwage regression with dummy black")
- **Specific econometric concepts** tested per question (e.g., "semi-elasticity with log(y)", "test H₀: β₃=β₄")
- **Variables and model specification** (e.g., "lwage = β₀ + β₁educ + β₂black + β₃exper + β₄tenure")
- **Cross-references to exam questions** testing the same concept

**For each lecture**, identify:
- **Applied examples** with company/dataset names (e.g., "Tyler Ltda — sales model with interaction", "TEMCO — multicollinearity case")
- **Key equations** and results shown in the slides

**For each exam/prova**, map each question to the specific list exercises and lecture examples that practice the same skill

**For each source book (textbook), build a per-exercise index.** Read the converted book MD and extract, for **every end-of-chapter exercise**:
- The **exercise number** (e.g., N&S `4.1`, `4.2`; MWG `3.G.4`) and the **page** (from TOC "Problems &lt;page&gt;" / "Exercises &lt;page&gt;" markers and the chapter body)
- The **subtopic(s)** it tests — tag using the SAME topic names as `topics-index.md` so the maps join cleanly
- The **knowledge level** (foundational / exam / advanced), inferred from what the exercise asks and from the source (N&S skews foundational/exam; MWG and J-R skew advanced)
- Mark any exercise whose number/page cannot be verified in an MD (book only in PDF) as **"to confirm"** — never fabricate numbers or pages.

This per-exercise index is what powers `/exercise-plan`.

**For each topic**, classify its complexity level:
- **Foundational**: definition-level concepts that appear in isolation (e.g., "what is R²", "OLS formula"). Prerequisites for other topics.
- **Intermediate**: requires understanding 1-2 prerequisites, multi-step reasoning (e.g., "multicollinearity diagnosis", "dummy interpretation with interaction").
- **Advanced**: inherently combines multiple topics or requires graduate-level math (e.g., "2SLS with heteroscedasticity-robust SEs", "asymptotic properties of IV estimators").

Also identify **cross-topic synthesis points**: exercises, exams, or book sections that combine multiple topics. These are critical for Hard-level quiz generation and NotebookLM prompts.

This exercise-level detail is what makes maps useful for `/notebooklm` and `/quiz-gen` — without it, maps are just topic labels.

### Step 2: Create Map/ directory

Generate four files:

#### `Map/books-index.md`

For each book in the bibliography, map **every section and subtopic in depth** — not just chapters. The map must serve as a detailed table of contents with economic content, key results, and cross-references at the section/subsection level.

```markdown
# Book Title, Edition

#book/shortname

## Cap. N — Chapter Title
**Páginas:** pp. A–B (when available from TOC or converted MD)

### §N.A — Section Title (pp. X–Y)
**Subtópicos:**
- Subtopic 1: one-sentence description of the key concept, definition, or result
- Subtopic 2: one-sentence description
- Key result: formal name of theorem/lemma/proposition if applicable

**Materiais vinculados:**
- Aula: [[<lectures-dir>/file|Aula N — Title]]
- Regras: [[rules/NN_topic|Regras — Topic]]

### §N.B — Section Title (pp. X–Y)
**Subtópicos:**
- Subtopic 1: description
- Subtopic 2: description

**Materiais vinculados:**
- Exercícios: [[<lists-dir>/file|Lista N, QN (description)]]
- Quiz: [[<quizzes-dir>/quiz-name|QN, QN]]

### Questões que requerem este conhecimento
- Lista 1, Q2: requires concept from §N.A
- Lista 2, Q5: requires result from §N.B
- Quiz Q3: tests theorem from §N.C
```

**Subtopic depth rules:**
- List EVERY named section (§N.A, §N.B, ...) from the book's table of contents
- For each section, list its key subtopics as bullet points with one-sentence descriptions
- Name theorems, lemmas, propositions, and key definitions explicitly (e.g., "Debreu's representation theorem", "Slutsky equation", "Arrow's impossibility theorem")
- Include page ranges per section when available from the book's TOC or converted MD
- Cross-reference at the section level, not just the chapter level — link each section to the specific aula, rule, exercise, or quiz that uses it
- If the book's MD conversion is poor or unavailable, extract section structure from the TOC pages and mark subtopics as "to confirm"
- The goal is that a student can look up ANY concept and find exactly which section covers it, what page it's on, and which course material connects to it

#### `Map/topics-index.md`

Topic-centric view:

```markdown
# Índice de Tópicos

## Tópico: Topic Name
#topic/topicname

**Complexity:** foundational | intermediate | advanced
**Cross-topic links:** [[Topic B]], [[Topic C]]
**Prerequisites:** [[Topic A]]

**Progressão de dificuldade:**
1. 📖 Conceito isolado (Easy): [[<books-dir>/bookname|Book, Cap. N, Sec. X-Y]] — definition and basic examples
2. 🎓 Aula (Easy→Medium): [[<lectures-dir>/file|Aula N — Title]] — lecture presentation with context
3. 📝 Regras (Medium): [[rules/NN_topic|Fórmulas e padrões]] — formulas, conditions, edge cases
4. ✏️ Exercícios diretos (Medium): [[<lists-dir>/file|Lista N, Q2, Q3]] — single-topic application
5. ✏️ Exercícios integradores (Hard): [[<lists-dir>/file|Lista N, Q7, Q12]] — multi-topic problems
6. 🧪 Quiz (varies): [[<quizzes-dir>/quiz-name|Q1, Q5, Q12]]
7. 📊 Prova (Hard): [[<exams-dir>/prova|QN]] — exam questions integrating this + other topics
8. 👨‍🏫 Monitoria: [[<tutorials-dir>/file|Monitoria N]]

**Cross-topic synthesis (Hard):**
- Combined with [[Topic B]]: see [[Lista N, QN]], [[Prova QN]]
- Combined with [[Topic C]]: see [[Book, Cap. N, example on p. X]]
```

#### `Map/study-guide.md`

Suggested study order:

```markdown
# Guia de Estudo

## Semana 1 — Topic Name

### Antes da aula
- Ler: [[<books-dir>/bookname|Book, Cap. N, Sec. X-Y]] (pp. A-B)
- Revisar: [[rules/NN_topic|Fórmulas-chave]]

### Depois da aula
- Praticar: [[<lists-dir>/file|Lista N, Q1-Q5]]
- Testar: [[<quizzes-dir>/quiz-topic|Quiz — Topic]] (20 questões)
- Monitoria: [[<tutorials-dir>/file|Monitoria N]] (se disponível)

### Conexões
- Pré-requisito para: [[Map/topics-index#Tópico: Next Topic|Next Topic]]
- Depende de: [[Map/topics-index#Tópico: Prev Topic|Prev Topic]]
```

#### `Map/exercises-index.md`

Per-exercise index of the source books — the lookup table `/exercise-plan` reads **first**. One row per end-of-chapter exercise, tagged by subtopic and knowledge level:

```markdown
# Índice de Exercícios das Fontes

#map/exercises

## N&S 12e
| Exercício | Cap./Seção | Pág. | Subtópico(s) | Nível | Verificado |
|-----------|-----------|------|--------------|-------|------------|
| 4.1 | Cap. 4 | 132 | UMP, demanda Cobb-Douglas | foundational | sim |
| 5.6 | Cap. 5 | 168 | Slutsky, CV/EV | exam | sim |

## MWG
| Exercício | Cap./Seção | Pág. | Subtópico(s) | Nível | Verificado |
|-----------|-----------|------|--------------|-------|------------|
| 3.G.4 | §3.G | 96 | Matriz de Slutsky (simetria/neg.) | advanced | sim |

## Jehle-Reny (a confirmar — só PDF)
| Exercício | Cap./Seção | Pág. | Subtópico(s) | Nível | Verificado |
|-----------|-----------|------|--------------|-------|------------|
| 1.x | §1.4 | — | Dualidade | exam | não |
```

Rules:
- `Verificado = sim` **only** when both the number AND the page were read from a converted MD; otherwise `não` (= "to confirm"). Never fabricate.
- Group by source; within a source, order by chapter then exercise number.
- `Subtópico(s)` must reuse the topic names from `topics-index.md` so `/exercise-plan` can weight by the same topics it reads there.
- Re-running `/study-map` refreshes this index; add newly converted sources, keep existing verified rows.

### Step 3: Use Obsidian conventions

- Wiki-links: `[[path|display text]]` for all cross-references
- Tags: `#topic/name`, `#book/shortname`, `#lista/N`, `#aula/N` for graph view
- Frontmatter in each Map file:
  ```yaml
  ---
  tags: [map, cross-reference]
  date: YYYY-MM-DD
  ---
  ```

### Step 4: Report

Show what was generated and how many cross-references were created. Suggest opening the project as an Obsidian vault.

## Important

- If books are in MD format (converted), parse chapter headings AND page numbers for precise references (chapter, section, AND pages when available — e.g., "Wooldridge Cap. 4, Sec. 4-3, pp. 118–125").
- If books are only in PDF, use what's available from CLAUDE.md and rules/ files. Try to extract page numbers from the PDF TOC if accessible.
- Re-running this command updates the maps — it doesn't duplicate entries.
- Match the language of the project (from CLAUDE.md or source materials).
- If source files are not in MD format, suggest running `/convert .` first — MD files enable deeper parsing for cross-references.
- Part of the study ecosystem: maps are used by `/quiz-gen` to weight topics and source book references, and by `/quiz-analyze` to find remediation materials.

## Metadata contract with other commands

The difficulty metadata in `topics-index.md` is consumed by:
- `/quiz-gen`: uses `Complexity` and `Cross-topic synthesis` to calibrate question difficulty. Easy questions pull from "Conceito isolado" materials; Hard questions pull from "Exercícios integradores" and "Cross-topic synthesis" entries.
- `/notebooklm`: uses `Complexity` and `Prerequisites` to determine prompt depth. Easy prompts cover foundational concepts; Hard prompts demand cross-topic connections listed in the synthesis section.
- `/quiz-analyze`: uses `Prerequisites` to identify foundational gaps when a student fails on an advanced topic.
- `/exercise-plan`: reads `exercises-index.md` **first** to build a weighted, level-graded practice plan from real source exercises (number + page), weighting subtopics by `topics-index.md` density; it falls back to reading the book MDs only for gaps or unindexed sources.

**Fallback**: if Map lacks difficulty metadata (old maps), treat all content as Medium. If `exercises-index.md` is missing, `/exercise-plan` reads the book MDs directly and should suggest running `/study-map` to build the index.
