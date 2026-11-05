# AGENTS.md

Tool-neutral contract for any coding agent here. Claude Code also reads `CLAUDE.md`;
Copilot also reads `.github/copilot-instructions.md` and `.github/instructions/`.
All are generated from `rules/` by `python tools/sync_rules.py`.

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

## Rule packs

Load what matches. Index: `rules/INDEX.md`. Cite as `pack-id#n`.

<!-- GENERATED:packs:start -->
`rules/` holds 5 packs: 3 engineering · 2 domain.

**Read `rules/INDEX.md` to find the one that matches your task** — it maps pack to subject in one table. Load only that pack. Each pack may point to a `rules/references/<id>.md` appendix; load that only when implementing.
<!-- GENERATED:packs:end -->

## Working state

Plans go to `.agent/plans/<slug>.md`, findings to `.agent/notes/<topic>.md` as
`file:line` references. Cheap to re-read, and they survive session death — the
transcript is not storage.
