<!-- TIER-0 CONTRACT. Re-sent on every request, forever.
     Budget: 900 tokens, enforced by `python tools/token_report.py --budget`.
     The block below is GENERATED from rules/core.md — edit the pack, not this file. -->

# Econometria Avançada — MPE (Insper)

Study project for *Econometria Avançada* (Mestrado Profissional em Economia, Insper). Professor: Hedibert Freitas Lopes (site: `Aula/COURSE.md`). Code: **Python** (Jupyter; `/lab*` applies). The lecturer's examples are in R: read them as reference and port them, never write project code in R.

**Scope:** do NOT go beyond the syllabus topics and chapters in `rules/09_course_program.md` (lecture × book map, bibliography, editions).

**Format:** output in English (quotes and book/section titles verbatim; no translation of existing files). Math in LaTeX `$...$` / `$$...$$`, never a bare `$` for currency. pdflatex: `lmodern` + `cmap` after `fontenc`, check `pdffonts`. NotebookLM language is an app setting, never a prompt line — confirm it before each batch. Secrets live in `.env`, never read.

**Siblings:** Video explainer `../Video explainer` (pip -e linked), Efficient Token `../Efficient Token`. Grading style: default (`rules/00_estilo_avaliacao.md`).

# Operating contract

<!-- GENERATED:tier0:start -->
### Non-negotiable

1. Escalate retrieval in this order and stop at the first rung that answers the
   question: **graph query → symbol lookup → structural search → ripgrep → file slice
   → whole file**.

2. Do not switch the main-loop model mid-session. Delegate to a subagent instead.

3. Write the plan to `.agent/plans/<slug>.md` before implementing any non-trivial
   change, then implement against it.

4. Report only outcomes observed in tool output. Failing tests are quoted, not
   summarized away. Skipped steps are stated.

5. Never read secrets into context: `.env`, key material, credential stores, tokens.
   Reference them by name.

6. Memory-safety, point-in-time, and idempotency gates do not relax under deadline.

### Prefer

7. Persist findings to `.agent/notes/<topic>.md` rather than re-deriving them.

8. Reuse before writing. If you write new code anyway, say what you found and why it
   did not fit.

9. Match the surrounding code. `.agent/conventions.md` outranks this repo's style
   preferences; correctness rules never yield.

10. Doc comments on public functions: purpose, parameter meaning, failures, calling
    context. Inline comments state constraints the code cannot express, never narration.

### Avoid

11. Making the diff larger than the change. Refactor inside the change's own context;
    outside it, ask (`codebase-work.md`).

12. Abstractions, defensive branches for impossible states, and speculative generality.

13. Claiming completion when part of the task is unfinished. Do the rest; if truly
    blocked, state plainly what is missing and why.

14. Re-deriving facts already established in the session.

Rationale and verification commands for each rule: `rules/core.md`
<!-- GENERATED:tier0:end -->

Rule packs: `rules/INDEX.md`. Cite rules as `pack-id#n`.
