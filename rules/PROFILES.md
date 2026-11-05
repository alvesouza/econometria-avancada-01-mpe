---
active: full
---

# Profiles

A profile selects which rule packs and which skills are **active** in this repo. Packs
outside the profile stay in `rules/` — they are just not compiled into
`.github/instructions/`, and their skills are moved to `.claude/skills.disabled/`.

```bash
python tools/profile.py list            # profiles and what they cost
python tools/profile.py status          # what is active now
python tools/profile.py apply quant     # switch
python tools/profile.py apply quant --dry-run
python tools/profile.py reset           # back to `full`
```

`active:` in the frontmatter above is the source of truth and is committed, so everyone
working in this repo — and CI — gets the same set.

**Why this exists.** Every enabled skill costs ~90 tokens of tier-1 context on every
request, forever, and every enabled pack with a matching `applyTo` glob can pull its
body into Copilot. In a Flutter repo, `rabbitmq` and `quant-ml` are pure overhead.

### Format

One `##` section per profile. Two keys, comma-separated, `*` globs allowed:

```
packs:  <ids or globs>      # `core` is always added; it is the contract
skills: <names>             # `rulesmith` is always added; you need it to edit rules
```

Sub-pack selection is deliberately not supported. Rules are numbered and cited
(`outbox-cdc#1`), so including half a pack would break every citation pointing into it.
If a pack is half-relevant, that is a signal to split the pack.

---

## full

Everything. The default, and the right choice for this repo itself.

```
packs:  *
skills: *
```

## minimal

The contract and the universal engineering rules. Any repo, any language.

```
packs:  context, planning, codebase-work, code-review, testing, security, local-dev,
        performance, concurrency, observability
skills: ctx, route, plan-guard, codebase, localdev, observability
```

## backend

Services, messaging, storage, containers.

```
packs:  context, planning, codebase-work, code-review, testing, security, appsec,
        local-dev, performance, concurrency, observability, scheduling, system-design,
        data-architecture, nosql, message-brokers, streaming-kafka, rabbitmq, sqs,
        outbox-cdc, jobs-hangfire, containers-docker, coordination, grpc, agents
skills: ctx, route, plan-guard, codebase, localdev, observability, dataflow, dataarch,
        jobs, container, pr-review, secreview, agentforge
```

## web

Front end and BFF.

```
packs:  context, planning, codebase-work, code-review, testing, security, appsec,
        local-dev, performance, observability, lang-js-ts, lang-react, lang-angular,
        ux-design, system-design, containers-docker, grpc
skills: ctx, route, plan-guard, codebase, localdev, observability, design, langpack,
        pr-review, secreview
```

## mobile

Flutter and React Native.

```
packs:  context, planning, codebase-work, code-review, testing, security, appsec,
        local-dev, performance, observability, lang-flutter, lang-js-ts, lang-react,
        ux-design, system-design
skills: ctx, route, plan-guard, codebase, localdev, observability, design, langpack,
        pr-review, secreview
```

## quant

Research and trading.

```
packs:  context, planning, codebase-work, code-review, testing, security, local-dev,
        performance, concurrency, observability, memory-safety, memory-management,
        computer-architecture, lang-python, lang-rust, lang-c-cpp, quant-*, regression,
        econometrics, microeconometrics, microeconomics, game-theory,
        behavioral-finance, data-architecture, nosql, streaming-kafka, outbox-cdc
skills: ctx, route, plan-guard, codebase, localdev, observability, quant, econ,
        langpack, pr-review
```

## econ

Economics and econometrics coursework or research.

```
packs:  context, planning, codebase-work, testing, local-dev, lang-python, regression,
        econometrics, microeconometrics, microeconomics, macroeconomics, game-theory,
        behavioral-finance
skills: ctx, route, codebase, econ, langpack
```

## systems

C, C++, Rust — performance and memory.

```
packs:  context, planning, codebase-work, code-review, testing, security, local-dev,
        performance, concurrency, memory-safety, memory-management,
        computer-architecture, scheduling, observability, lang-c-cpp, lang-rust
skills: ctx, route, plan-guard, codebase, localdev, observability, langpack, pr-review
```

## gamedev

```
packs:  context, planning, codebase-work, code-review, testing, local-dev, performance,
        concurrency, memory-safety, memory-management, computer-architecture,
        game-design, ux-design, lang-c-cpp, lang-csharp, lang-rust
skills: ctx, route, plan-guard, codebase, localdev, design, langpack, pr-review
```

## dotnet-events

C# services with Kafka, outbox, Hangfire.

```
packs:  context, planning, codebase-work, code-review, testing, security, appsec,
        local-dev, performance, concurrency, observability, scheduling, lang-csharp,
        memory-management, system-design, data-architecture, nosql, message-brokers,
        streaming-kafka, rabbitmq, outbox-cdc, jobs-hangfire, containers-docker, grpc
skills: ctx, route, plan-guard, codebase, localdev, observability, dataflow, dataarch,
        jobs, container, pr-review, secreview
```

## ai

Building LLM features into an application.

```
packs:  context, planning, codebase-work, code-review, testing, security, appsec,
        security-compliance, local-dev, performance, concurrency, observability,
        agents, agent-integration, langchain, lang-python, lang-js-ts, data-architecture,
        nosql, message-brokers
skills: ctx, route, plan-guard, codebase, localdev, observability, agentapp,
        agentforge, secreview, pr-review
```
