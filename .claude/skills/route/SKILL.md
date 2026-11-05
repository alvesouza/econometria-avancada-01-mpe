---
name: route
description: Choose the model, effort level, and delegation strategy for a task, and explain the cost consequences. Use when asked "which model should I use", "is this worth Opus", "how do I make this cheaper/faster", when a session is unexpectedly expensive, or before starting a long autonomous run.
---

# Routing

Rules: `rules/model-routing.md`. Detail: `docs/01-model-routing.md`.

## The rule that dominates

**Never switch the main-loop model mid-session.** Caches are model-scoped and
prefix-matched; a switch re-processes the entire conversation at full input price. On a
long session, that single `/model` costs more than the work you were economizing on.

Need a different capability level mid-task ⇒ **delegate**, do not switch.

```
✗  /model haiku → grunt work → /model opus       # cache destroyed twice
✓  Task(subagent_type="scout")                   # pinned to Haiku, own context
```

## Choose effort before you change model

`effort` moves quality more than a model downgrade moves cost, and it does not touch
the cache.

| Effort | For |
|---|---|
| `low` | Mechanically specified, latency-sensitive. Risks under-thinking on branches. |
| `medium` | Routine work, cost-sensitive. |
| `high` | Default for anything intelligence-sensitive. |
| `xhigh` | Hard coding and agentic runs. Claude Code's own default. |
| `max` | Correctness over cost. Diminishing returns; can overthink. |

At `xhigh`/`max`, set `max_tokens ≥ 64000`. Thinking and response share the budget;
a tight cap yields mostly thinking, then truncation.

`effort` does **not** shorten prose. Verbosity is a prompt fix.

## Routing table

| Task | Model | Effort |
|---|---|---|
| Repo-wide refactor, migration, overnight run | Fable 5 | `high` |
| Multi-file feature, architecture, hard debugging | Opus 5 | `xhigh` |
| Code review, bug hunt | Opus 5 | `high` |
| Implementation from an accepted plan | Sonnet 5 | `high` |
| Tests, codemods, mechanical refactor | Sonnet 5 | `medium` |
| Search, extraction, file summarizing | Haiku 4.5 | `low` — subagent only |
| Commit messages, changelogs | Haiku 4.5 | `low` |
| Numerical / quant correctness review | Opus 5 or Fable 5 | `max` |

Prices per Mtok (in/out): Fable 5 $10/$50 · Opus 5 $5/$25 · Sonnet 5 $3/$15 ·
Haiku 4.5 $1/$5.

## Delegation economics

A scout on Haiku reading 40 files costs roughly a fifth of the same reading on Opus —
**and** those 40 files never enter the main context, so they are not re-sent on every
subsequent turn. The saving is multiplicative. This is why fan-out reading should
essentially never happen in the main loop.

But delegation is not free: each worker re-establishes context, re-explores, writes a
report, and the coordinator reads it.

**Delegate:** independent and sizeable sub-tasks; wide multi-file investigation; work
that would flood the coordinator's context.

**Do not delegate:** anything finishable in a handful of tool calls; verification (keep
it in the main loop); one modest job split for the sake of parallelism.

Model-specific and counter-intuitive: **Opus 4.8 under-delegates** and needs
encouragement; **Opus 5 over-delegates** and needs an explicit cap. Any "delegate more"
prompting written for 4.8 should be removed when moving to 5.

## Long-horizon runs

Give the **complete specification in the first turn**. Current models plan far better
from a full spec than from requirements revealed across turns, and progressive
revelation measurably reduces both token efficiency and output quality.

Expect minutes-long single turns at high effort. Plan timeouts, streaming, and progress
UX accordingly.

## Fast mode

`/fast` buys output throughput on Opus at premium pricing. It is a latency purchase,
not an intelligence one, and toggling it invalidates the cache. On for an interactive
burst; off for a long autonomous run.

## API callers

On Fable 5 / Opus 5, a policy decline is HTTP 200 with `stop_reason: "refusal"` —
check it before reading `content`.

```python
resp = client.beta.messages.create(
    model="claude-opus-5", max_tokens=64000,
    output_config={"effort": "xhigh"},
    betas=["server-side-fallback-2026-07-01"],
    fallbacks="default",     # routes by refusal category; no model list to maintain
    messages=[...],
)
```

Prefer `"default"` over pinning a fallback model — different fallbacks carry different
classifiers, and a pin becomes a migration you owe later. Unavailable on Bedrock,
Vertex, and Foundry; use the SDK's client-side refusal-fallback middleware there.
