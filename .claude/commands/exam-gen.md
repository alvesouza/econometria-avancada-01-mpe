---
description: Gera uma lista de exercícios (ou simulado) no estilo da Avaliação Final do MPE — questões objetivas + discursivas contextualizadas — com gabarito e rubrica, em LaTeX (um único .tex com toggle lista/gabarito). Pergunta profundidade, temas tangenciais e complexidade antes de gerar, including a graduate-level option (harder math, symbolic by default, solutions derived from primitives).
argument-hint: <conteúdo/tópicos a testar> [nº de questões] [style: <nome>]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion
---

Gera uma lista de exercícios no estilo de avaliação do MPE a partir de `$ARGUMENTS` (o conteúdo que o aluno quer testar).

Estilo, taxonomia, formato de solução, rubrica e regras LaTeX: siga **`~/.claude/commands/templates/estilo-avaliacao.md`** (cópia local em `rules/00_estilo_avaliacao.md` quando existir). Template LaTeX: **`~/.claude/commands/templates/lista-exam.tex`**.

**Named style.** If `$ARGUMENTS` names a grading style (`style: macro 1`, `--style macro-1`,
"no estilo macro 1"), load `~/.claude/commands/templates/styles/<name>.md` instead (match
case-insensitively, spaces as hyphens; if no file matches, list `styles/` and ask). A named
style outranks the project's `rules/00_estilo_avaliacao.md`. It was written for one course:
keep its question anatomy, scoring, distractor and anti-guessing rules, solution and rubric
format, and graduate mode (§8); take the course bindings (bibliography, block-to-lecture
table, scope exclusions, institutional context, LaTeX template path) from this project's
`CLAUDE.md`, `rules/` and `Map/`. Its subject-specific examples (common-mistake lists,
rubric-cap examples) stay when the subject matches and are replaced by this course's own
otherwise.

## Passo 1 — Escopo

Interprete `$ARGUMENTS`: tópicos/aulas/arquivos a cobrir e nº de questões (padrão: 1 bloco objetivo + 1 discursivo por tema; ou o que o aluno pedir). Se vago, infira do `CLAUDE.md`.

## Passo 2 — Contexto e bibliografia

1. Leia `CLAUDE.md` (escopo do curso, restrição "não extrapolar", bibliografia).
2. Leia `rules/` (fórmulas, definições) e **`Map/`** (cross-references: pesos por tópico, páginas dos livros para as linhas `Ref:`, exercícios similares).
3. Use os **livros** (N&S piso; J-R rigor; ZaE narrativa; MWG cross-check) para garantir correção e referências. Formule questões **originais** — nunca copie exercícios.
4. Identifique tópicos **adjacentes** ao escopo (via `Map/`) para oferecer como temas tangenciais no Passo 3.

## Passo 3 — Avalie a matematizabilidade e pergunte ao aluno

**Primeiro** avalie se o conteúdo é **matematizável** (tem fórmulas, derivações, cálculo numérico — ex.: Slutsky, UMP/EMP, Pigou, Arrow-Debreu) ou é **predominantemente conceitual** (ex.: intuições de Coase, tipologia de assimetria, estabilidade em matching). Isso decide se a pergunta de complexidade matemática aparece.

Faça **uma** chamada AskUserQuestion com as perguntas abaixo (adapte as opções ao escopo; pule qualquer uma já respondida em `$ARGUMENTS`):

1. **Profundidade** — quão a fundo abordar o tema?
   - *Revisão rápida* (conceitos centrais, aplicação direta)
   - *Padrão de prova* (recomendado — montar→resolver→interpretar)
   - *Aprofundado* (inclui provas/derivações e casos-limite, estilo J-R/MWG)
   - *Graduate level* (graduate problem-set difficulty within the course's topics: every question built from primitives, proofs, dynamics, limits; follows §8 of the style guide)
2. **Temas tangenciais** — incluir tópicos adjacentes? (multiSelect, opções vindas do `Map/`; ex.: para Slutsky → elasticidades, bem-estar CV/EV, Giffen). Inclua a opção "Só o tema principal".
3. **Complexidade matemática** — **somente se o conteúdo for matematizável**:
   - *Leve* (plug-and-play, números limpos)
   - *Média* (recomendado — multi-passo, dualidade)
   - *Pesada* (derivações, integrais de bem-estar, prova/limite)
   - *Graduate* (general functional forms before special cases, implicit differentiation, linearization and eigenvalues, second-order welfare costs; style guide §8)

   Picking *Graduate level* depth or *Graduate* complexity switches the whole list to §8 of the style guide: symbolic by default, cross-topic and integrative questions, no answer in the statement, a parameter-analysis sub-item in every discursive question, graphs in some sub-items (not all), four or five sub-items, solutions rebuilt from primitives, a check script, and an answer key of 10 to 15 pages. It also triggers a second AskUserQuestion call (the tool takes at most four questions per call) with one question, **Numbers**: *Symbolic only* (Recommended — parameters with admissible ranges, closed forms, proved sign tables, graphs without numeric ticks) / *Symbolic + calibrated numbers* (adds numeric items, sensitivity tables and numbered axes). Without an explicit opt-in, the list stays symbolic.

   Se o conteúdo for **predominantemente conceitual**, substitua esta pergunta por **Ênfase quantitativa**: *100% conceitual* / *Maioria conceitual com 1–2 itens quantitativos* / *Equilibrado* — e não force matemática onde o tema não pede.
4. **Formato** — *Completo* (objetivas + discursivas) / *Só objetivas* (MC + V/F) / *Só discursivas*.

Se o conteúdo misturar partes matematizáveis e conceituais, você pode oferecer a complexidade matemática referida apenas à parte quantitativa.

## Passo 4 — Projete a lista

Conforme o estilo: blocos temáticos; em cada bloco, questão objetiva (a,b MC 3 pts; c,d V/F 2 pts) e/ou discursiva (a,b,c × 5 pts; at graduate level a–d, 3+4+4+4). Calibre pela complexidade escolhida. At graduate level, take ideas from the course's graduate reference and its hardest end-of-chapter problems (never copy them), and check, block by block, the mix of §8: proof, dynamics/characterization, limit, quantification; every discursive question chains two or more topics and ends with a parameter analysis (proved signs, a sensitivity table, limits, economic reading); at least one sub-item per block, and at most half of them, asks for a graph. A graduate list also gets an integrative block (three or more topics from at least two lectures in one model); in a graduate mock exam every block has at least one integrative question. Distribua a posição da alternativa correta (não fixar A). V/F deve testar recíprocas/armadilhas. Contextualize cada questão num cenário brasileiro plausível, com parâmetros que dão resposta fechada limpa (in graduate symbolic mode the scenario is narrative only and the parameters stay symbols).

## Passo 5 — Escreva o `.tex`

Copie o template e preencha o corpo com as questões e as soluções:
```bash
mkdir -p Listas && cp ~/.claude/commands/templates/lista-exam.tex "Listas/lista-<tema>.tex"
```
- Defina `\listatema`. Remova o exemplo do template.
- Cada questão usa as macros (`\bloco`, `\questao`, `\alternativas`, `\gabarito`, `\resolespaco`) e cada solução vai dentro de `\begin{sol}...\end{sol}` com `\passo`, `\intuicao`, `\refbib` e `\rubrica` (com tetos conceituais + penalidades leves + não-cumulatividade).
- Every solution follows the style's "Equations, notation and layout" rule: open with `\begin{notacao}` (every variable and parameter, meaning and range); number every equation a later step uses (`\label` with a question prefix, e.g. `q3:euler`) and cite it at each step with `\eqref` ("substituting (7) into (5)"); tag the statement's own equations so solutions can cite them; one operation per displayed line (`align` + `\nonumber`), no long inline chains. Never `\eqref` a label that lives inside `sol` from statement text. Show every substitution as its own line: the receiving equation with the substituted expression in place, in parentheses, before simplifying (with (1) $A=B+C$ and (2) $B=2A$: first $A=(2A)+C$, then $C=-A$); numbers plugged in are shown in place before the result, with enough decimals that the displayed arithmetic reproduces the printed value.
- Write and edit `.tex` with the file Write/Edit tools, not shell heredocs or `sed`: the shell here collapses `\\` to `\` and turns `\b`, `\n` into control characters.
- Deixe o toggle em `\solucoesfalse` (a lista em branco é o default).

## Passo 6 — Compile e verifique

Compile os **dois** PDFs a partir do mesmo fonte (regra global lmodern+cmap):
```bash
cd Listas
pdflatex -interaction=nonstopmode -halt-on-error "lista-<tema>.tex"   # 2x -> lista em branco
# gabarito: flip do toggle só para compilar, depois restaure \solucoesfalse
python3 - <<'PY'
import re
f="lista-<tema>.tex"; s=open(f,encoding="utf-8").read()
g=re.sub(r'(?m)^\\solucoesfalse\b','\\\\solucoestrue',s)
open("_gab.tex","w",encoding="utf-8").write(g.replace('lista-<tema>','lista-<tema>-gabarito'))
PY
pdflatex -interaction=nonstopmode -halt-on-error _gab.tex   # 2x
mv _gab.pdf "lista-<tema>-gabarito.pdf"; rm -f _gab.* *.aux *.log
```
Verifique: `pdffonts lista-<tema>.pdf` — tudo **Type 1**, zero Type 3. Sem erros de compilação.

Graduate level: before compiling, write `Listas/lista-<tema>-check.py`, which verifies every result and aborts on a mismatch: closed forms with sympy; each sign, limit and ordering (symbolically or at many random admissible parameter draws); that each MC distractor differs from the key; and, with numbers opted in, every number, sensitivity-table entry and plotted coordinate. Run it; it must pass. Then check the answer key's page count: 10 to 15 pages per list (at least 10 for a mock exam). Below 10, add questions, integrative ones first, and rebuild; above 15, cut questions, never steps.

O aluno edita o `.tex` e, para ver o gabarito, troca `\solucoesfalse`→`\solucoestrue` e recompila.

## Passo 7 — Relatório

Mostre: nº de questões (objetivas/discursivas) por bloco; complexidade e temas escolhidos (graduate: symbolic or with numbers); arquivos gerados (`lista-<tema>.tex`, `.pdf` em branco, `-gabarito.pdf`); contagem de páginas; como resolver e depois rodar `/exam-grade Listas/lista-<tema>.tex` para corrigir a própria resolução.

Then ask (AskUserQuestion), every time: **split the study roadmap into a PDF?** *Yes*: write the list's reading and roadmap tables (the `/exercise-plan` format) to `Listas/roteiro-<tema>.md` and run `/study-pack` on it; *No* stops. Rule: `rules/00_estilo_avaliacao.md` §9.
