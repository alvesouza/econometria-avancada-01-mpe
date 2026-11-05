---
id: context
title: Context and token discipline
tier: 2
applyTo: ""
skills: [ctx]
owner: repo-owner
---

## Non-negotiable

1. Answer structural questions ("what calls X", "how does A reach B", "what breaks if
   I change C") with `graphify query`, not with search-and-read.
   *Check:* `graphify query "<q>" --graph graphify-out/graph.json --budget 1500`

2. Fetch symbol bodies with `find_symbol` (Serena MCP) or `Read` with `offset`/`limit`.
   Never read a whole file to obtain one function.
   *Why:* a 2,000-line file costs ~25k tokens; the symbol costs a few hundred, and the
   difference is re-paid on every later turn.

3. Never load into context: `node_modules/`, `dist/`, `build/`, `target/`, lockfiles,
   generated code (`*.g.dart`, `*.freezed.dart`, `*_pb2.py`, `*.designer.cs`),
   minified bundles, binary fixtures, `.env*`.
   *Check:* `.graphifyignore` and `.gitignore` cover all of these.

4. Findings that will be needed later go to `.agent/notes/<topic>.md` with file:line
   references. The transcript is not storage.

## Prefer

5. `ast-grep` over `ripgrep` when the target is a code *shape* rather than a string.
   `sg -p 'await $C.query($$$)' -l ts` returns matches; `rg "query"` returns noise.

6. `Read` with `offset`/`limit` over full reads, always. When you do not know the
   offset, `get_symbols_overview` first (~200 tokens, no bodies).

7. `graphify path A B` to trace a dependency chain, `graphify explain X` to understand
   a single node, before opening anything.

8. `/compact` at a task boundary (tests green, feature done) rather than when context
   pressure forces it — the summary is written from a coherent state.

9. `npx repomix --compress` only for whole-repo questions in a surface with no
   filesystem access. Never inside an agentic session that can read files.

10. Subagents for fan-out reading. A scout on a small model reading 40 files returns a
    300-token report; the 40 files never enter the main context at all.

## Avoid

11. `grep -r` / `find` across the repo root. Scope to a directory, or query the graph.
    *Why:* unscoped recursive search pulls in vendored and generated trees and its
    output is mostly noise you then pay to re-send.

12. Re-reading a file already read this session. If you cannot remember it, it belongs
    in `.agent/notes/`.

13. Pasting file contents into a summary, report, or subagent return value. Return
    `file:line` references and conclusions.

14. Volatile content early in a prompt prefix — timestamps, UUIDs, session IDs,
    unsorted `json.dumps`, per-user tool lists.
    *Why:* caching is a prefix match; one changed byte invalidates everything after it.
    *Check:* `usage.cache_read_input_tokens` > 0 on repeated identical-prefix requests.

15. Changing the tool list mid-conversation. Tools render at position 0, so any change
    invalidates the entire cache. Use `defer_loading` + `tool_addition` blocks if the
    set genuinely must change.

16. `tiktoken` for measuring Claude token counts. It is OpenAI's tokenizer and
    undercounts by 15–20% on prose, more on code. Use `messages.count_tokens`.
