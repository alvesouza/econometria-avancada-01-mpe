---
name: codebase
description: Change existing code well — reuse what exists, decide whether to refactor or
  add alongside, keep the diff minimal, document functions with their parameters and
  calling context, and match the codebase's own conventions. Use before editing an
  unfamiliar repo, or when a change would touch a shared function.
---

# Working in an existing codebase

Load `rules/codebase-work.md`. Load `rules/references/codebase-work.md` for doc-comment
templates, the ask-vs-act table, and the precedence order.

## 1. Learn the conventions before writing anything

```bash
python tools/detect_conventions.py          # writes .agent/conventions.md
cat .agent/conventions.md
```

It reports indentation, line length, naming, doc-comment style, comment density, test
framework and layout, and error-handling idiom — each with a confidence share.

- **High confidence** — follow it silently.
- **Low confidence** — the codebase is inconsistent; follow the file you are editing and
  say which you matched.
- **Formatter/linter configs listed** — those are authoritative and outrank everything
  inferred.

Precedence when things conflict: correctness and security → explicit instruction →
codebase convention → this repo's preferences → defaults. **No convention makes a race
condition acceptable.**

## 2. Search before you write

Four searches, because the existing version is rarely named what you would name it:

```bash
graphify query "what handles <domain noun>" --graph graphify-out/graph.json --budget 1200
sg -p '<shape of the function you were about to write>' -l <lang>
rg -n --glob '!{node_modules,dist,build,target}' '<verb>|<noun>' src/
rg -n '<behaviour in words>' --glob '**/*{test,spec}*'
```

Operation, domain noun, type shape, and test names. If you write new code anyway, say
what you found and why it did not fit.

## 3. Decide: extend, refactor, or ask

| Callers | Same module? | Do |
|---|---|---|
| Just the one you are changing | yes | Refactor freely |
| A handful, same module | yes | Refactor, update them in the same commit |
| Several, across modules | no | **Ask** |
| Public API or another repo | no | New function; deprecate the old one on a stated path |
| Cannot enumerate | no | Treat as public API |

When you ask, make it cheap to answer — name the function, the callers you found, both
options, the trade-off, and your recommendation:

> `normalizePrice()` rounds half-up; the ledger needs half-even. 7 callers: 5 in
> `pricing/`, 2 in `reporting/`. (a) add a `rounding` param defaulting to current
> behaviour — no call site must change; (b) new `normalizePriceHalfEven()` — zero risk,
> two near-identical functions. I'd take (a). Which?

## 4. Write the smallest change that fully solves it

The diff contains the change and nothing else — no reformatting, no renames, no import
reordering, no unrelated fix you noticed. Note those separately instead.

The one exception: a smaller diff is *not* smaller if it leaves a correctness, safety,
or **measured** performance problem in code you are already touching. Measured, per
`performance#1` — a performance refactor without a before/after number is a preference.

When the change is larger, split the commits so refactoring and behaviour are separable:

```
1. refactor: extract rounding mode into a parameter    (no behaviour change)
2. fix: use half-even rounding for ledger amounts      (3 lines that matter)
```

## 5. Document what the signature cannot say

Every public function, method, and type: purpose, what each parameter *means* and what
values are valid, return, failure modes, and **where and why it is called**. Use the
language's native doc format so tooling picks it up — templates in the reference.

The split that keeps this coherent with `core#10`:

- **Doc comment** (above the declaration) — the contract, for callers. Required.
- **Inline comment** (inside the body) — constraints the code cannot express, for the
  next editor. Never narration.

```python
# BAD   i += 1  # increment i
# GOOD  # Vendor caps the batch at 500; above that the API silently truncates.
```

## 6. Greenfield is the exception

A genuinely new module or service with no established convention is the one case where
you set the standard instead of inferring it. Use the best current approach rather than
copying an unrelated part of the repo, fix the mechanical choices early (formatter,
lint, test layout, error idiom), and **write down what you chose and why** so the next
person inherits a decision rather than an accident.

Cross-cutting conventions — logging, config, CI, dependency policy — still apply. Those
are integration surface, not style.

## Report

Say which conventions you matched, what you reused, and what you deliberately left
alone. If you diverged from a convention, give the reason — silent divergence reads as a
mistake.
