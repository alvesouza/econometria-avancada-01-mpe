---
name: rulesmith
description: Add, change, or delete a rule or a skill in this repo at minimum token cost, then recompile the Claude and Copilot surfaces. Use when the user says "add a rule", "we should always/never X", "change the convention for Y", "create a skill for Z", "that keeps happening — codify it", or asks why an agent behaved a certain way and wants the instruction fixed.
---

# Rulesmith

Rules live in `rules/*.md` (source of truth). `CLAUDE.md`, `AGENTS.md`, and everything
under `.github/` are **generated**. Editing a generated file is wasted work — it is
overwritten on the next sync.

## Procedure — adding or changing a rule

Do not read rule packs to find where a rule belongs. Read the index.

```
1. Read rules/INDEX.md                       (~400 tokens)
2. Read the ONE matching pack                (~600 tokens)
3. One Edit call, one rule
4. python tools/sync_rules.py
5. python tools/token_report.py --budget
6. Commit: rules(<pack-id>): <imperative summary>
```

If no pack fits, create one — see *New pack* below. If two packs fit, the rule is
probably two rules.

## Before writing the rule, answer three questions

**1. Can a machine enforce it instead?**
A lint rule, a type, an ast-grep pattern, or a hook beats prose every time — it cannot
be forgotten, argued with, or silently dropped. If the answer is yes, write that
instead and do not add the rule.

```bash
sg -p '<pattern>' -l <lang>        # prototype the check first
```

**2. What tier?**
Does it change behavior on *every* task, in *every* language, in *every* part of the
repo? Almost always no ⇒ `tier: 2`. Tier 0 has a 900-token budget that CI enforces, and
it currently holds six rules. Adding a seventh should feel hard.

**3. Is it path-scopeable?**
If yes, it gets an `applyTo` glob and Copilot loads it only for matching files. If no,
it needs a `skills:` entry so Claude can route to it, and it has no good Copilot home
beyond a prompt file.

## Rule form

```markdown
N. <One imperative sentence. Present tense. No hedging.>
   *Why:* <the failure this prevents — mandatory for non-negotiables>
   *Check:* <command, lint rule, or observable condition>
```

Sections in order: **Non-negotiable**, **Prefer**, **Avoid**. Numbering is stable and
citable (`outbox-cdc#3`).

`*Why:*` is not decoration. A rule whose reason nobody remembers cannot be safely
deleted, and cannot be correctly generalized to a case the author did not foresee.

### Packs cite nothing, and carry the detail themselves

**State the mechanism, never the source.** No `## Sources`, no "Grounded in X", no
`(Author ch. 4)` — CI rejects all three.

- A citation is unresolvable wherever the library is absent, and still costs tokens.
- "Because Kleppmann says so" cannot be generalized; *"clock skew means a later event
  can carry an earlier timestamp"* can.
- If you cannot state the mechanism in a clause, you copied a conclusion instead of
  learning it, and the rule will be misapplied at the first edge case.

A pack should be **sufficient on its own** — a reader with no library applies it
correctly. When a rule depends on a procedure, a formula, a threshold, or a parameter
name, put it in a `## Quick reference` section at the end of the pack rather than
assuming the reader will look it up. Reference sections are tier 2: they cost nothing
until the pack loads.

Optional provenance, if anyone wants it, lives in `docs/09-bibliography.md` — outside
the rule surface, required by nothing.

## New pack

```markdown
---
id: <slug>                  # must equal the filename
title: <Human readable>
tier: 2
applyTo: "<glob>, <glob>"   # empty string if not path-scopeable
skills: [<skill-name>]
owner: <team>
---
```

Then add a row to `rules/INDEX.md`. A pack missing from the index is a pack nobody finds.

## Writing a skill

```
.claude/skills/<name>/
  SKILL.md              frontmatter + body under ~500 lines
  references/*.md       loaded on demand by the body
```

The `description` is the only part that sits in context permanently. It is a **routing
rule**: it must answer *when should this fire*, in the words a user actually says.
Name the triggers, the inputs, and the output.

| Weak | Strong |
|---|---|
| `description: Helps with Kafka.` | `description: Kafka, transactional outbox, Debezium/CDC, schema evolution, consumer idempotency, DLQ and retry topics. Use when adding or changing anything that publishes or consumes events, or when a consumer is dropping or duplicating messages.` |

Rules for skill bodies:

- **Never inline a rule pack.** Reference it by path. Duplicated rules drift silently.
- **One skill, one job.** A skill that does everything triggers unpredictably.
- **Include the actual commands.** "Consider using X" saves nothing; the exact command
  line saves a research round-trip.
- Over ~500 lines ⇒ split into `references/` and load on demand.

## Deleting

Deletion is the operation nobody performs, which is why instruction files only grow.
Delete when:

- The `*Why:*` describes a model generation or a system you no longer run
- A lint rule, type, or hook now enforces it
- Nothing has violated it in a year and nobody remembers why it exists
- It restates a trained default (`be accurate`, `write clean code`, `don't hallucinate`)

Grep for the rule id before removing it — citations in code comments and PR templates
must go too.

## Never write

Pressure language. Current models follow instructions closely and *literally*, so
inflated emphasis causes over-triggering and rigid behavior:

| Don't | Do |
|---|---|
| `CRITICAL: You MUST always...` | `Use X when...` |
| `NEVER EVER under any circumstances` | `Avoid X. *Why:* ...` |
| `If in doubt, use [tool]` | delete |
| `Be thorough and do not be lazy` | delete |

## Verify

```bash
python tools/sync_rules.py --check      # generated files in sync?
python tools/token_report.py --budget   # tier 0 within budget?
```

Both are CI gates. If either fails locally it will fail the PR.
