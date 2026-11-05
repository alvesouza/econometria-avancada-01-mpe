# Estilo de Avaliação (MPE) — regras de listas, simulados e correção

Especificação do estilo das avaliações do MPE. É a fonte única de verdade para os comandos `/exam-gen` (gerar lista + gabarito) e `/exam-grade` (corrigir a resolução do aluno). Casada com o template `templates/lista-exam.tex`.

## 1. Estrutura do documento

- Organização em **blocos temáticos** (1 a 4). Cada bloco mapeia a um conjunto de aulas e vale um total de pontos (no simulado completo: 4 blocos × 25 = 100 pts; numa lista temática, use 1–2 blocos).
- Cada bloco tem, tipicamente, **duas questões**:
  - **Questão objetiva** (10 pts): itens **a) e b)** de múltipla escolha (3 pts cada, 4–5 alternativas, sem penalização por erro) + itens **c) e d)** de **Verdadeiro/Falso** (2 pts cada).
  - **Questão discursiva** (15 pts): um enunciado-mãe contextualizado + sub-itens **a), b), c)** (5 pts cada), com espaço "Resolução:".
- Numa **lista de exercícios** o tamanho é flexível (o aluno escolhe o escopo); mantenha a mesma anatomia de questões.

### Regra de V/F (sempre na capa/instruções)
Nota dos itens V/F $=\max\{0,\ \text{acertos}-\text{erros}/2\}\times$ valor do item. Itens em branco não contam como erro.

## 2. Taxonomia das questões

- **Múltipla escolha (a, b):** aplicação direta de fórmula ou identificação de conceito. 4–5 alternativas. Distratores plausíveis e do **mesmo comprimento** da correta (anti-chute), refletindo erros comuns (sinal trocado, avaliar no ponto errado, confundir Marshalliana/Hicksiana, etc.).
- **Verdadeiro/Falso (c, d):** testam **recíprocas falsas** e armadilhas conceituais (ex.: "Giffen ⟹ inferior" é V; "inferior ⟹ Giffen" é F; "2º TBE vale sem convexidade" é F). Uma afirmação por item, sem ambiguidade.
- **Discursiva (a, b, c):** progressão crescente — montar o problema → resolver/derivar → interpretar/comparar bem-estar. Cada sub-item testa um aspecto distinto do mesmo cenário.

## 3. Contextualização (marca do estilo)

- **Toda** questão é ancorada em um cenário aplicado brasileiro **plausível e atual**: empresa, política pública, mercado ou regulador real (ex.: Petrobras, Metrô Rio, CCEE, ANS, CETESB, SISU, B3, Itaipu). O contexto é casca; o núcleo é o modelo do curso.
- Parâmetros numéricos **escolhidos para dar respostas fechadas limpas** (frações simples, raízes exatas). Declare "valores ilustrativos" quando convém.
- Não confundir realismo institucional com extrapolação teórica: **só modelos do curso**.

## 4. Formato da solução (gabarito)

- **Objetivas:** `Gabarito: X` + 1–3 linhas justificando (conta ou conceito).
- **Discursivas:** sequência numerada **"Passo — título. texto."** (montagem → derivação → resultado → verificação). Inclua:
  - **Intuição econômica.** parágrafo curto com o "porquê".
  - **Ref:** âncora bibliográfica (capítulo + seção, e página quando o `Map/` tiver).
  - **Rubrica de correção.** distribuição de pontos por passo, com:
    - **Tetos por erro conceitual** (ex.: "usar soma horizontal em bem público → máx. 1 pt no sub-item").
    - **Penalidades leves** por erro aritmético com método correto (ex.: $-1$ pt).
    - **Não-cumulatividade:** tetos conceituais prevalecem sobre penalidades leves (não se somam).
  - **Risco residual** (opcional): pegadinha comum / ambiguidade do enunciado a evitar.
- **Graphs.** When a question is solved in a diagram, the rubric scores **labelled axes, named
  curves and the direction of the shift** separately from the verbal conclusion.
- **Equations, notation and layout (every solution).**
  1. Number every equation a later step uses (`\label`/`\eqref`, or `(1)`, `(2)`... in
     Markdown) and name the source at each step: "Using (2) and (4)...", "Substituting (7)
     into (5)...", "Dividing (3) by $L_t$...". Equations of the statement keep the statement's
     numbers. *Why:* a step that does not say where its terms come from cannot be checked
     line by line; the reader has to reverse-engineer it.
  2. Open each solution with a **Notation** list: every variable and parameter, what it
     means, and its admissible range. Define any new symbol on the line where it first
     appears. *Why:* the same letter means different things across topics ($\sigma$ is the
     capital share in Solow and the intertemporal elasticity in Benigno).
  3. One operation per displayed line. Use display equations, not long inline chains, with a
     short sentence between displays saying what was done. *Why:* clustered math hides the
     step where an error happens (Prova 01 lost its golden-rule exponent inside an inline
     chain).
  4. Show every substitution as its own line: write the receiving equation with the substituted
     expression in place, in parentheses, before simplifying. With (1) $A=B+C$ and (2) $B=2A$,
     "substituting (2) into (1)" gives $A=(2A)+C$ on one line, and only the next line gives
     $C=-A$. *Why:* jumping from the cited equations straight to the result hides the one line a
     reader needs to check the substitution, and sign and exponent errors live there.
     Plugging in numbers is a substitution too: show the numbers in place, then the result,
     e.g. $VA_B=(1000)-(600)$, then $=400$. The displayed arithmetic must reproduce the printed
     result: carry enough decimals that the shown operation gives the stated value (not
     $-0.6365-(-0.6460)$ printed as $0.00946$), and keep any check script asserting that value.

## 5. Uso da bibliografia (obrigatório)

Ancore conteúdo e referências nos livros do curso, via `Map/` e `rules/` quando existirem:
- **MHE (Angrist & Pischke)**: the baseline for causal topics 01–03 (chapter/section in every question).
- **Tsay AFTS 3e**: time series, volatility, state space, MCMC (topics 04, 05, 08).
- **ISLP (2023)**: classification and validation (topic 06); same chapters as ISLR 1e/2e, cite ISLP numbers.
- **Bolfarine & Sandoval (2010)**: likelihood, estimators and their properties (Class 1 review). **Izbicki & Mendonça (2020)** and **Morettin & Singer (2021)**: Portuguese cross-checks for statistical learning.
- **Greenberg 1e**: Bayesian topics 07–08, plus Bayesian panel (03), IV and selection (01–02). The syllabus names the 2e.
- **Wooldridge 6e**: textbook-level cross-check (syllabus names the 5e).
**Book questions used in a list or mock exam.** Reproduce the question's text verbatim, every
sub-item, table and number, never only its number and page. Open it with an explicit source
line before the text: author (year), title, chapter, exercise number and name, printed page
with the PDF page in brackets, whether the source gives the answer, and "reproduced verbatim".
Copy into the same block anything the statement refers to (an earlier problem, example, table,
or the values of a figure it reads from), so the list is solvable away from the book. Allowed
edits only: math re-typeset in LaTeX, tables rebuilt, hyphenation undone, margin notes dropped
(global rule, `~/.claude/CLAUDE.md`). Mark anything added or changed ("Added parts (not in the book)", "numbers
changed", "items (a)-(c) only"). Take the text from the PDF, not from the `.md` conversion,
which garbles spacing, tables and glyphs. When the source has no exercise (an article
section), say so in the source line and write the statement as your own. *Why:* a list that
says "Kurlat 6.1, p. 121" cannot be worked without the book open, and the source line keeps
the reproduced text attributed.
Questions you create stay original: do not disguise a book exercise as your own.
Use o `Map/` para pesos por tópico e para páginas nas linhas `Ref:`.

## 6. Convenções LaTeX

- Template: `templates/lista-exam.tex`. Um único `.tex` com `\ifsolucoes`:
  - `\solucoesfalse` → **lista em branco** (espaço para resolver).
  - `\solucoestrue` → **gabarito + rubrica** (mesmo arquivo).
- Macros: `\bloco`, `\questao`, `\alternativas`, `\gabarito`, `\resolespaco`, `\passo`, `\intuicao`, `\refbib`, `\rubrica`; blocos de solução dentro do ambiente `sol` (excluído na lista em branco via pacote `comment`).
- **Regra global de PDF copiável:** preâmbulo já traz `\usepackage{lmodern}` e `\usepackage{cmap}` após `fontenc`. Compilar com `pdflatex` (2×) e verificar `pdffonts` (tudo **Type 1**, nunca Type 3).
- Matemática em `$...$`/`$$...$$`. Nunca usar `$` solto para moeda (escreva "120 reais").
- Graphs in **TikZ/pgfplots**, never a raster image.

## 7. Anti-padrões

- Não extrapolar o conteúdo do curso (checar `CLAUDE.md`).
- **Anti-chute de formatação:** a correta não pode ser sistematicamente a mais longa, nem a única com parênteses/fórmula/exemplo. Escreva os distratores no mesmo nível de detalhe e no mesmo estilo da correta (parênteses, hedges, símbolos, unidades) — às vezes mais longos, às vezes mais curtos. Se a correta termina com um parêntese (esclarecimento, fórmula, número), os distratores também devem terminar. A única coisa que distingue a correta é ser verdadeira, nunca o formato. Distribua a posição da correta (não fixar A).
- **Majority-vote guessing.** If every distractor changes exactly one feature of the key, the
  key is the feature-by-feature majority of the options and can be found without the
  content: at least one distractor per item combines two named mistakes. Check the correct
  letters across the whole list too (every letter used, no repeating pattern), above all
  when different blocks were written separately.
- V/F sem pegadinha = questão fraca; prefira recíprocas e hipóteses que "quebram".
- Solução sem rubrica e sem intuição = incompleta.

## 8. Graduate level (opt-in for lists and mock exams)

Chosen in `/exam-gen` Step 3 (*Graduate level* depth, *Graduate* math complexity). The
anatomy of §1–§4 stays (blocks, objective + discursive, rubric, intuition, `Ref:`); the bar
moves. A project copy of this guide (`rules/00_estilo_avaliacao.md`) may specialize this
section to its course.

**Scope.** The syllabus does not grow: the course's exclusions in `CLAUDE.md` still hold.
What rises is the mathematics applied to the course's own models. In this mode the course's
graduate reference (e.g. MWG or Jehle-Reny in micro, Romer in macro) is the main source of
ideas, and complementary books may raise the level. *Why:* a harder list that changes the
topics trains for an exam the student will not sit.

**Symbolic by default.** Graduate lists and mock exams are posed and solved in parameters
(with their admissible ranges), without calibrated numbers: answers are closed forms,
conditions, signs, orderings and limits; multiple-choice options are expressions or
conditions; a result with no closed form is characterized (existence, uniqueness,
monotonicity, bounds) and proved. The applied context stays as narrative. `/exam-gen` asks
whether to include numbers; only on an explicit yes do items add calibrated values, numeric
sensitivity tables and numbered axes. *Why:* at this level the skill tested is deriving and
signing results; calibrated numbers move the effort to arithmetic and let a student who
cannot read the model score by computing.

**Questions.**
- Every discursive question starts from **primitives** (preferences, technology,
  constraints, information, market structure). The student derives what an intermediate
  list would hand over (demand, cost function, FOCs, equilibrium conditions) and then uses it.
- General functional forms come before special cases (CES before Cobb-Douglas, CRRA before
  log, general $u$ before a parametric one). Distractors and traps come from applying the
  special case where it fails.
- Each block contains at least one item of each kind: a **proof** ("show that", existence,
  uniqueness, sign of a derivative by implicit differentiation); a **characterization**
  (stability, dynamics, uniqueness of equilibrium, duality); a **limit or knife-edge case**;
  a **quantification** in closed form (a welfare integral, a second-order loss; calibrated
  numbers only when opted in).
- Objective items need three or more derivation steps or a trap only the general case
  reveals; none is answerable by plugging into a memorized formula.
- **Cross-topic questions.** Every discursive question chains at least two course topics
  that interact inside one model: the result of one is an input of the other (e.g. in micro:
  demand × welfare measurement × taxation, production × general equilibrium, uncertainty ×
  information; in macro: consumption × equilibrium interest rates, money × fiscal policy).
  Name the topics in the question's heading. At least two objective items per block also
  cross topics. *Why:* at this level the exam tests whether a result can be carried from one
  model into another, not whether one model can be reproduced.
- **Integrative questions.** Each graduate list has an integrative block, and each block of a
  graduate mock exam has at least one integrative question: one model in which three or more
  topics from at least two different lectures cross (e.g. in micro: demand × welfare
  measurement × taxation × general equilibrium; in macro: life-cycle saving × labor supply ×
  pension design). Name the topics in the heading. *Why:* the final exam rewards carrying a
  result through several models; questions that stay inside one topic do not train it.
- **No answer in the statement.** Ask to find, characterize or determine; do not print the
  formula to be proven, except when the result has a name the student should recognize.
- **Parameter analysis in every discursive question**, as the course's own problem sets do
  ("what happens to … if … rises", "for which values of …", limits): (i) the sign of each
  comparative static, proved by implicit differentiation or a closed form; (ii) a table of
  those signs (results × parameters; +, −, 0, or the condition that decides the sign), plus a
  numeric sensitivity table computed by the check script when numbers are opted in;
  (iii) limiting and knife-edge values; (iv) the economic reading of each change.
- **Graphs where the model is read graphically, not in every question.** Each block has at
  least one sub-item that asks the student to draw (phase diagram, curve shifts, budget or
  production sets, a trade-off or Laffer curve), and at most half of the sub-items do. The
  answer key draws it in TikZ/pgfplots from the model's own equations; in symbolic mode any
  admissible parameter values shape the curves, numeric ticks are suppressed, and axes,
  curves and points carry symbolic labels.
- Discursive questions have four or five sub-items **a)–e)** (e.g. 3×5 = 15 pts): set up →
  derive → characterize (proof, dynamics, limits) → quantify → parameter analysis.

**Solutions.**
- Rebuild each model from its primitives every time: state the problem, the Lagrangian or
  the substitution used, every FOC (with what the multiplier means), the equilibrium
  conditions, then solve. No step is "it can be shown"; second-order or sufficiency
  conditions are noted where they decide the answer.
- Each step says what it uses ("from the FOC (2) and market clearing (4)").
- An independent script (`Listas/<list>-check.py`) verifies every result and aborts on a
  mismatch: each closed form with sympy; each claimed sign, limit and ordering (symbolically,
  or at many random admissible parameter draws); each existence claim by root-finding at
  random draws; that every multiple-choice distractor differs from the key; and, with numbers
  opted in, every number, table entry and plotted coordinate. *Why:* long derivations hide
  sign and exponent slips that a reader cannot catch at a glance.
- **Length: 10 to 15 pages of answer key per list**, in the same format (numbered steps,
  intuition, `Ref:`, rubric). If the key has fewer than 10 pages, add questions (integrative
  ones first) until it reaches 10, never pad the prose; above 15, cut questions, never
  steps. A graduate mock exam's key has at least 10 pages. Spend the space on derivations,
  proofs, sign tables and figures. *Why:* a cross-topic question with a parameter analysis
  cannot be solved step by step in one page, and the student studies from the key.

**Rubric.** Score the setup and each derivation step separately. Caps: a special-case
result used in the general case (max. half the item); a result the item asks to derive that
is quoted instead (max. a third); a stability, sign or limit claim without proof (0 for that
line); a parameter analysis that lists signs without proving them or without reading them
economically (max. half the item); a cross-topic question answered inside one model only,
ignoring the link (max. half the item). A requested graph is scored on its own lines: axes
and labels, each curve with its slope, the shift or dynamics, and the point read off it; a
graph contradicting the student's algebra loses the graph points.

## 9. Study-roadmap PDF and practice-plan solutions (every exercise list)

- After building any exercise list, ask the user whether to split its study roadmap into a
  PDF. This covers `/exam-gen` lists and mock exams, and `/exercise-plan` practice plans built
  from existing book exercises. Ask once, at the end, after the list exists; it is never a
  silent default in either direction.
  *Why:* the roadmap lists reading pages and exercise pages scattered across several book
  PDFs; without the extracted PDF the student re-finds each page by hand, and generating it
  unasked costs a build the student may not want.
  *Check:* the final report of every list ends with this question (AskUserQuestion), and a
  "yes" produces `/study-pack <roadmap file>`.
- On "yes", run `/study-pack` on the file that carries the roadmap tables (an `/exercise-plan`
  file already does; for an `/exam-gen` list, first write the reading and roadmap tables of the
  `/exercise-plan` format to `Listas/roteiro-<topic>.md`).
- After building an `/exercise-plan` practice plan, also ask whether to write the solutions of
  its exercises as a PDF, in the same AskUserQuestion call as the roadmap question.
  *Why:* a practice plan points to book exercises whose answers are usually not in the books,
  so without solutions the student cannot check the work; writing 30 solutions unasked is a
  long build the student may not want. (`/exam-gen` lists already ship their answer key.)
  *Check:* the plan's final question offers both PDFs; a "yes" produces
  `Listas/pratica-<topic>-solutions.pdf`.
- On "yes", solve every exercise of the plan with `/solution` in plan order, cite each one by
  number and page without restating it, and compile one pdflatex PDF (lmodern + cmap) from
  `Listas/pratica-<topic>-solutions.tex`, with a check script for every computed number.
