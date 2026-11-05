---
id: core
title: Operating contract
tier: 0
applyTo: "**"
skills: []
owner: repo-owner
---

## Non-negotiable

1. Escalate retrieval in this order and stop at the first rung that answers the
   question: **graph query → symbol lookup → structural search → ripgrep → file slice
   → whole file**.
   *Why:* every token entering context is re-paid on every subsequent turn; a graph
   query answers in ~1.5k tokens what read-everything exploration answers in ~100k.
   *Check:* no `Read` of a whole file when one symbol was needed.

2. Do not switch the main-loop model mid-session. Delegate to a subagent instead.
   *Why:* caches are model-scoped and prefix-matched, so a switch re-bills the entire
   conversation at full input price.
   *Check:* one `/model` at session start, none after.

3. Write the plan to `.agent/plans/<slug>.md` before implementing any non-trivial
   change, then implement against it.
   *Why:* plans in the transcript are re-sent every turn and get lost to compaction;
   plans on disk are free to re-read and survive session death.

4. Report only outcomes observed in tool output. Failing tests are quoted, not
   summarized away. Skipped steps are stated.
   *Why:* an unverified success claim is worse than a failure — it ends the loop that
   would have caught it.

5. Never read secrets into context: `.env`, key material, credential stores, tokens.
   Reference them by name.
   *Why:* anything in context is in the transcript, in compaction summaries, and in
   any log of them, permanently.

6. Memory-safety, point-in-time, and idempotency gates do not relax under deadline.
   *Why:* all three fail silently and are discovered in production.
   *Check:* `rules/memory-safety.md`, `rules/quant-research.md`, `rules/outbox-cdc.md`.

## Prefer

7. Persist findings to `.agent/notes/<topic>.md` rather than re-deriving them.

8. Reuse before writing. If you write new code anyway, say what you found and why it
   did not fit.
   *Why:* a duplicated helper is two things to fix, and the copy is the one nobody
   remembers to update.

9. Match the surrounding code. `.agent/conventions.md` outranks this repo's style
   preferences; correctness rules never yield.
   *Check:* `python tools/detect_conventions.py`

10. Doc comments on public functions: purpose, parameter meaning, failures, calling
    context. Inline comments state constraints the code cannot express, never narration.

## Avoid

11. Making the diff larger than the change. Refactor inside the change's own context;
    outside it, ask (`codebase-work.md`).

12. Abstractions, defensive branches for impossible states, and speculative generality.
    *Why:* each enlarges the diff, the review, and the blast radius with no requested
    benefit.

13. Claiming completion when part of the task is unfinished. Do the rest; if truly
    blocked, state plainly what is missing and why.

14. Re-deriving facts already established in the session.
