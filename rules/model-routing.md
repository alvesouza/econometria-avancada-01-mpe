---
id: model-routing
title: Model and effort routing
tier: 2
applyTo: ""
skills: [route]
owner: repo-owner
---

Route by **capability tier**, not by vendor. Tier is a durable property of the task;
the model that currently fills a tier changes every few months, and differs by platform,
subscription, and organization policy.

## Non-negotiable

1. **Pick the tier from the task shape, then pick a model that fills it.**

   | Tier | Task shape |
   |---|---|
   | **Frontier reasoning** | Architecture, hard debugging, security and numerical review, long autonomous runs |
   | **Balanced coding** | Implementation from an accepted plan, multi-file edits, refactors |
   | **Fast / cheap** | Search, extraction, summarizing, classification, commit messages, fan-out reading |
   | **Long context** | Whole-repo or whole-corpus reasoning that genuinely will not fit otherwise |

   *Why:* naming a vendor model in a shared config makes it wrong on every other
   platform and stale on the next release. Naming a tier stays correct.

2. **Do not switch the main-loop model mid-session.** Delegate to a subagent instead.
   *Why:* prompt caches are model-scoped and prefix-matched, so a switch re-processes
   the whole conversation at full input price.
   *Check:* one model selection at session start, none after.

3. **Record the model id and version on any run whose output is acted on** — a review,
   a generated artifact, a production response.
   *Why:* without it you cannot tell whether a regression came from your change or from
   a model update underneath you.

4. **Verify what is actually available before pinning.** Model availability varies by
   platform, subscription tier, and organization policy, and models are withdrawn.
   *Check:* the platform's model picker or model list — not a table written months ago.

## Prefer

5. **Tune the reasoning/effort dial before changing model.** Where a platform exposes
   one, raising it usually moves quality more than a model upgrade moves cost, and it
   does not invalidate the cache.

6. **Delegate rather than switch.** Spawn a subagent pinned to the tier you need; it
   gets its own context and its own cache while the main loop's prefix survives.

7. **Pin the tier in the agent or prompt definition, not at the call site**, so the
   choice is reviewable and changeable in one place.

8. **Let the platform route routine work where it offers automatic selection.** Auto
   modes weigh task complexity and provider health together, which is information you
   do not have. Override for tasks where a specific capability matters.

9. **Frontier tier for silent-wrongness tasks** — numerical code, concurrency,
   financial logic, migrations, security review. The failure mode is a plausible wrong
   answer that passes review, and the cheaper model is a false economy.

10. **Fast tier for anything that reads and reports.** Fan-out reading belongs in a
    subagent on a cheap model: the files never enter the main context, so the saving is
    multiplicative rather than additive.

11. **Give long-horizon work its complete specification in the first turn.** Current
    models plan far better from a full spec than from requirements revealed across
    turns.

12. **Headroom for output when reasoning is high.** Thinking and response share the
    budget on most platforms; a tight cap yields a truncated answer after expensive
    thinking.

## Avoid

13. **Vendor model names in shared configuration** — prompt files, chat modes, CI
    definitions that others run on other platforms. State the tier; let the picker or
    the organization policy resolve it.

14. **Lowering effort to shorten output.** Effort controls thinking depth, not prose
    length. Verbosity is a prompt fix.

15. **Toggling latency modes mid-session.** They buy speed, not intelligence, and the
    toggle invalidates the cache.

16. **Assuming a model exists.** Handle the unavailable-model case explicitly; a hard
    pin becomes a hard failure when the model is withdrawn or not in the caller's plan.

17. **Assuming a refusal is an error.** Some platforms return a policy decline as a
    successful response with a distinct stop reason; code that reads the first content
    block unconditionally breaks on it.

**Reference:** `rules/references/model-routing.md` — tier-to-model mapping per platform
(Claude Code, Copilot, direct API), effort levels, delegation economics, cross-provider
differences that change behaviour, and how to write platform-neutral prompt files.
Load it when implementing; the rules above stand on their own.
