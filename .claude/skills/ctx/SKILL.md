---
name: ctx
description: Cut context and token cost — code-graph queries (Graphify), symbol lookup (Serena), structural search (ast-grep), repo packing (Repomix), prompt-cache hygiene, and compaction. Use when exploring an unfamiliar codebase, when a session is getting expensive or slow, when asked "where is X" / "what calls Y" / "what breaks if I change Z", or when setting up context tooling for a repo.
---

# Context operations

Rules: `rules/context.md`. Setup and rationale: `docs/03-context-tooling.md`.

## The ladder

Stop at the first rung that answers the question.

```
graph query → symbol lookup → structural search → ripgrep → file slice → whole file
   ~1.5k         ~400            ~300              ~800       ~1k        ~5–25k
```

## 1. Graph query — relationships

```bash
graphify query "what connects payment to enrollment" \
  --graph graphify-out/graph.json --budget 1500

graphify path "UserDashboard.vue" "PaymentService" --graph graphify-out/graph.json
graphify explain "PaymentService" --graph graphify-out/graph.json
```

Budget guidance: `800` for "which module owns this", `1500` for "how do these two
subsystems interact", `3000` only for a genuinely deep dependency trace.

If `graphify-out/graph.json` is missing:

```bash
pip install graphifyy          # CLI is `graphify`, package is `graphifyy`
graphify update .              # AST-only, no API key
graphify claude install        # PreToolUse hook: intercepts grep/find → graph query
graphify hook install          # git post-commit + post-checkout rebuild
```

Do **not** wire rebuilds to a Claude `Stop` hook — `graphify update` takes 10s+ on a
monorepo and would tax every turn.

## 2. Symbol lookup — bodies

With Serena MCP available:

```
get_symbols_overview(file)        structure only, ~200 tokens, no bodies
find_symbol("Class/method")       just that body
find_referencing_symbols(sym)     call sites without reading callers
replace_symbol_body(sym, code)    edit without ever holding the file
```

Without it: `Read` with `offset`/`limit`. Get the line number from the graph or from
`rg -n` first.

## 3. Structural search — shapes

```bash
sg -p 'await $C.query($$$)' -l ts        # awaited DB calls (N+1 audit)
sg -p 'unsafe { $$$ }' -l rust
sg -p 'catch ($E) { }' -l cs             # swallowed exceptions
sg -p '$X.Result' -l cs                  # sync-over-async
sg -p 'memcpy($D, $S, $N)' -l c          # memory-safety audit
```

Prefer over `rg` whenever the target is a code shape — far fewer false positives, which
is the same as far fewer tokens.

## 4. Repo packing — last resort

```bash
npx repomix --compress                    # signatures only, ~70% smaller
npx repomix --include "src/**/*.ts" --compress
```

Only for a surface with no filesystem access, or a genuinely global audit. **Never**
inside an agentic session that can already read files.

## Diagnosing an expensive session

| Symptom | Likely cause | Fix |
|---|---|---|
| Cost far above expectation, early | Cache miss | Check `usage.cache_read_input_tokens`; look for a volatile prefix or a mid-session model/tool change |
| Slow degradation over the session | Transcript accumulation | `/compact` at the next task boundary |
| Huge input on every turn | Standing-cost bloat | `python tools/token_report.py` |
| Repeated exploration of the same area | Findings living in the transcript | Write to `.agent/notes/`, then compact |
| Agent reading whole files | Ladder not being followed | Verify the graphify hook is installed |

## Prompt-cache hygiene

Caching is a **prefix match** — one changed byte invalidates everything after it.

Silent invalidators to grep for in prompt-building code:

- `datetime.now()` / `Date.now()` / `uuid4()` in a system prompt
- `json.dumps(d)` without `sort_keys=True`; iteration over a `set`
- session or user id interpolated into the system prompt
- `if flag: system += ...`
- `tools=build_tools(user)` — tools render at position 0

Verify with `usage.cache_read_input_tokens > 0` across repeated identical-prefix
requests. Note `input_tokens` is the **uncached remainder only** — total prompt size is
the sum of all three usage fields.

## Notes discipline

```
.agent/notes/<topic>.md
```

Findings with `file:line` references and conclusions. No pasted code. Written as you
go, so a compaction or a crash costs nothing.

## Measuring

```bash
python tools/token_report.py            # standing cost of tier-0 surfaces
python tools/token_report.py --all      # every pack and skill
python tools/token_report.py --budget   # CI gate
```

Never `tiktoken` — it is OpenAI's tokenizer and undercounts Claude by 15–20% on prose,
more on code.
