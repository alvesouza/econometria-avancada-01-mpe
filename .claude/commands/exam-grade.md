---
description: Corrige e analisa a qualidade da resolução do aluno para uma lista/simulado no estilo MPE, aplicando a rubrica (tetos por erro conceitual, penalidades leves, não-cumulatividade), com feedback e referências aos livros. Atribui nota por item e total.
argument-hint: <lista .tex/.pdf> [arquivo da resolução do aluno | cole a resolução] [style: <nome>]
allowed-tools: Read Grep Glob Bash PowerShell Write Edit AskUserQuestion
---

Corrige a resolução do aluno para a lista indicada em `$ARGUMENTS`, no estilo de correção do MPE.

Estilo de rubrica e solução: siga **`~/.claude/commands/templates/estilo-avaliacao.md`** (ou `rules/00_estilo_avaliacao.md`).

**Named style.** If `$ARGUMENTS` names a grading style (`style: macro 1`, `--style macro-1`,
"no estilo macro 1"), grade by `~/.claude/commands/templates/styles/<name>.md` instead (match
case-insensitively, spaces as hyphens; if no file matches, list `styles/` and ask). A named
style outranks the project's `rules/00_estilo_avaliacao.md`. Keep its scoring, rubric caps,
light penalties, non-cumulativity and graduate-mode (§8) grading; take the course bindings
(bibliography for the `Ref:` anchors, scope exclusions, block-to-lecture table) from this
project's `CLAUDE.md`, `rules/` and `Map/`.

## Passo 1 — Carregue a lista e o gabarito

1. Identifique a lista (`.tex` ou `.pdf`) em `$ARGUMENTS` ou em `Listas/`.
2. Obtenha a **solução de referência**: se houver `*-gabarito.*` ou blocos `sol`/`\rubrica` no `.tex`, use-os. Se não houver, **derive** a solução e a rubrica seguindo o estilo (com `Map/`, `rules/` e os livros: N&S piso; J-R/MWG para rigor).
   Any solution written here (a derived reference solution, or the correct path shown in the feedback) follows the style's "Equations, notation and layout" rule: a Notation list, numbered equations cited at each step, one operation per displayed line. Show every substitution as its own line: the receiving equation with the substituted expression in place, in parentheses, before simplifying (with (1) $A=B+C$ and (2) $B=2A$: first $A=(2A)+C$, then $C=-A$); numbers plugged in are shown in place before the result, with enough decimals that the displayed arithmetic reproduces the printed value.

## Passo 2 — Ingira a resolução do aluno

A resolução pode vir como: caminho de arquivo (`.txt`, `.tex`, `.md`, `.pdf`, **imagem/foto** de manuscrito), ou colada no comando. Use `Read` (lê imagens e PDFs). Se nada foi fornecido, peça (AskUserQuestion) como o aluno quer enviar.

## Passo 3 — Corrija item a item (aplique a rubrica)

Para **cada** item (a, b, c, …):
- **Objetivas:** compare a alternativa/V-F marcada com o gabarito. Em V/F, lembre a regra de anulação ($\max\{0,\text{acertos}-\text{erros}/2\}$).
- **Discursivas:** compare passo a passo contra a rubrica. Atribua pontos por passo. Aplique:
  - **Teto por erro conceitual** (ex.: soma horizontal em bem público, avaliar MEC no nível errado, confundir Marshalliana/Hicksiana) — limita o item independentemente do resto.
  - **Penalidade leve** ($-1$ pt) por erro aritmético com método correto.
  - **Não-cumulatividade:** o teto conceitual prevalece sobre a penalidade leve (não somam).
- Seja específico: cite o passo onde o raciocínio do aluno divergiu e **por quê**, e qual seria o passo correto (com a fórmula/nome de variável).

## Passo 4 — Feedback qualitativo

- Resuma **acertos** (o que está sólido) e **lacunas conceituais** (o que revisar), distinguindo erro de método (grave) de erro de conta (leve).
- Aponte **o que estudar**: tópico + referência de livro (capítulo/seção e página via `Map/`), e exercícios similares.
- Se houver padrão de erro (ex.: sempre esquece o efeito-renda), nomeie-o.

## Passo 5 — Saída

- **Relatório de correção** (markdown) com, por item: nota atribuída / nota máxima, justificativa curta, e o passo correto quando errou.
- **Tabela-resumo:** item → nota → tópico a revisar; e **nota total** (por bloco e geral).
- Opcional (se o aluno pedir): gere um `.tex` "Correção" com os comentários inline ao lado da resolução, no mesmo estilo (compilável, regra global lmodern+cmap).
- Sugira: rodar `/exam-gen` para uma lista de reforço focada nas lacunas, ou `/quiz-gen` para um quiz rápido dos pontos fracos.

## Princípios

- Seja **justo e rigoroso como o gabarito**: dê crédito parcial por método correto mesmo com conta errada; penalize método errado mesmo com resposta "certa por sorte".
- Não invente exigências fora do estilo do curso. Ancore toda crítica num passo da rubrica e numa referência do material.
