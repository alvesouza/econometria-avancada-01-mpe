# model-routing — reference

Loaded on demand from `rules/model-routing.md`. Rules live there; this is the detail
needed to implement them.

**Model lists go stale within months.** Treat the tables below as a snapshot and verify
against the platform's own picker before pinning anything. The tier framing is the
durable part.

## 1. Tiers, and what fills them

| Tier | Claude Code | Copilot (picker) | Direct API |
|---|---|---|---|
| **Frontier reasoning** | Fable 5, Opus 5 | Claude Opus, GPT-5-Codex family | Fable 5, Opus 5, or the vendor's top reasoning model |
| **Balanced coding** | Sonnet 5 | Claude Sonnet, mid GPT-5 | Sonnet-class |
| **Fast / cheap** | Haiku 4.5 | small/mini tiers where offered | Haiku-class |
| **Long context** | any 1M-context model | plan-dependent | model with the context you need |

As of mid-2026 Copilot exposes OpenAI and Claude models across price points; **Gemini
models were removed from Copilot Chat on the web**. The coding-agent picker offers Auto
plus a fixed list of Claude Opus/Sonnet and GPT-Codex builds. Which of these a given
user sees depends on their subscription and on organization model rules.

The consequence for anything you commit: **do not pin a vendor model in a shared prompt
file.** Someone on another plan gets an error, and Auto — which weighs task complexity
against live provider health — is disabled for no benefit.

## 2. Writing platform-neutral prompt files

Omit `model:` and state the tier in prose. The user's picker or the platform's automatic
selection then resolves it.

```markdown
---
mode: agent
description: Security review of the current diff.
tools: ['codebase', 'search', 'usages', 'findTestFiles']
---

Use a **frontier-reasoning** model — this task's failure mode is a plausible-looking
miss, not a visible error. If your picker offers Auto, override it here.

Read `rules/appsec.md` first...
```

Pin a specific model only when the task depends on a capability that is not uniform
across the tier — a specific tool-use behaviour, a context length, or a modality.
Then say why in a comment, so the pin can be re-evaluated when it goes stale.

## 3. Effort and reasoning dials

Where a platform exposes a reasoning or effort setting, it is usually the better first
move: it shifts quality more than a model downgrade shifts cost, and unlike a model
change it does not invalidate the prompt cache.

| Level | Use |
|---|---|
| Low | Mechanically specified, latency-sensitive |
| Medium | Routine work; often the honest sweet spot |
| High | Default for intelligence-sensitive work |
| Highest | Hard coding and agentic runs; correctness over cost |

Two traps that generalize across platforms:

- **Thinking and response share the output budget.** Raising effort without raising
  `max_tokens` produces expensive thinking followed by a truncated answer.
- **Effort does not shorten prose.** Verbosity is a prompt problem. Lowering effort to
  get a shorter answer buys a worse answer of the same length.

## 4. Delegation economics

Switching the main-loop model throws away the cached conversation prefix. Delegation
does not — the subagent gets its own context and its own cache.

```
✗  switch to cheap → grunt work → switch back      cache destroyed twice
✓  spawn a subagent pinned to the cheap tier       main loop's prefix intact
```

The saving on fan-out reading is multiplicative, not additive: a scout on a cheap model
reading 40 files costs a fraction per token **and** those 40 files never enter the main
context, so they are never re-sent on any later turn.

Delegation is not free — the worker re-establishes context, explores, and reports, and
the coordinator reads that report. Delegate work that is genuinely independent and
sizeable. Do not delegate something you could finish in three tool calls, and do not
delegate verification.

Calibration differs by model generation, which is not intuitive: older frontier models
tended to under-delegate and needed encouragement; current ones over-delegate and need
an explicit cap. Any "delegate more" instruction inherited from an older prompt should
be removed.

## 5. Cross-provider differences that change behaviour

Worth knowing before writing code that must work across providers:

| Area | Varies how |
|---|---|
| **Refusals** | Some return a policy decline as a *successful* response with a distinct stop reason rather than an error. Check the stop reason before reading content |
| **Prompt caching** | Prefix-matched everywhere it exists, but minimum cacheable length, TTL, and whether it is automatic or explicitly marked all differ |
| **Structured output** | Native schema-constrained output vs function-calling vs JSON mode; strictness and failure behaviour differ |
| **Tool calling** | Parallel tool calls, forced tool choice, and how errors are returned to the model all differ |
| **Reasoning tokens** | Billed and surfaced differently; some hide them, some return them, some charge for hidden ones |
| **Context window** | Advertised vs *usefully* attended length are not the same number |
| **Rate limits** | Per-token, per-request, or per-tenant; retry semantics differ |

Write provider-specific behaviour behind one adapter, not scattered through the
codebase — see `agent-integration.md`.

## 6. Task-to-tier table

| Task | Tier | Note |
|---|---|---|
| Repo-wide refactor, migration, overnight run | Frontier | Full spec in the first turn |
| Multi-file feature, architecture, hard debugging | Frontier | Default for real work |
| Code review, bug hunt | Frontier | Ask for everything with severity + confidence; filter after |
| Security review, numerical/quant correctness | Frontier, highest effort | Silent wrongness is the failure mode |
| Implementation from an accepted plan | Balanced | The plan carries the hard thinking |
| Tests, codemods, mechanical refactor | Balanced | |
| Search, extraction, file summarizing | Fast | Subagent only, never the main loop |
| Commit messages, changelogs, renames | Fast | |
| Whole-corpus synthesis | Long context | Verify it will not fit after retrieval first |

## 7. Auto selection

Where a platform offers automatic model selection, it routes on task complexity **and**
live provider health — the second of which you cannot observe. Use it for routine work.

Override it when the task has a property the router cannot see: a correctness-critical
review, a long autonomous run where a mid-run switch would be disruptive, or a
capability requirement (context length, modality, a specific tool behaviour).

## 8. Organization policy

Enterprise platforms increasingly let an organization restrict which models are
available, per team or per surface. Two consequences:

- A prompt file pinning a model may simply fail for some colleagues. Another reason to
  state the tier.
- The tier table above is *your* mapping, not a universal one. If your organization
  restricts the frontier tier, write down what fills each tier locally and keep that
  next to this file.
