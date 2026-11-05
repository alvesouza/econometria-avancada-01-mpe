# Rule index

Grep this file to find the right pack. **Do not read packs to find a rule** — that is
the expensive path this index exists to avoid.

Packs are self-contained: every rule states its own mechanism and carries no citation,
so nothing here depends on an external library. Optional provenance for a curious
reader lives in `docs/09-bibliography.md` and is never required to apply a rule.

## Contract

| Pack | Covers | Skill |
|---|---|---|
| `core.md` | Tier 0: context budget, plan/verify, gates, scope | — |

## Engineering

| Pack | Covers | Skill |
|---|---|---|
| `context.md` | Retrieval ladder, graph/symbol tooling, cache hygiene | `/ctx` |
| `model-routing.md` | Model + effort selection, delegation over switching | `/route` |
| `planning.md` | Plan artifacts, decomposition, acceptance criteria | `/plan-guard` |
| `codebase-work.md` | Reuse, refactor scope, minimal diff, doc comments, conventions | `/codebase` |
| `code-review.md` | Finding format, severity/confidence, verification | `/pr-review` |
| `system-design.md` | Consistency, failure models, sagas, scaling order | `/dataarch` |
| `scheduling.md` | Queueing, utilization, starvation, priority inversion | `/jobs` |
| `memory-safety.md` | Ownership, bounds, FFI, sanitizers, races | `/plan-guard` |
| `memory-management.md` | Allocators, GC, pooling, layout, leaks | `/plan-guard` |
| `computer-architecture.md` | Cache, branches, SIMD, NUMA, Amdahl | `/plan-guard` |
| `performance.md` | Measure-first, allocation, batching, async | `/plan-guard` |
| `security.md` | Secrets, input trust, supply chain, agent surface | — |
| `appsec.md` | Threat modeling, STRIDE, crypto, authz, injection | `/secreview` |
| `security-compliance.md` | Personal/payment data, audit trails, retention | `/secreview` |
| `testing.md` | Test shape, determinism, property tests, fixtures | — |
| `local-dev.md` | Concurrency knobs, dev profiles, build speed, hot reload | `/localdev` |
| `ux-design.md` | Hierarchy, scales, colour, motion, states, accessibility | `/design` |
| `agents.md` | Agent/subagent design, delegation limits, tools | `/agentforge` |
| `agent-integration.md` | API shape, run state, budgets, tool authority, rollout | `/agentapp` |
| `concurrency.md` | Routines, structured concurrency, bounding, cancellation | `/plan-guard` |
| `observability.md` | Metrics, logs, traces, cardinality, SLOs, alerting | `/observability` |

## Languages

| Pack | Covers | Skill |
|---|---|---|
| `lang-c-cpp.md` | C / C++ | `/langpack` |
| `lang-csharp.md` | C# / .NET | `/langpack` |
| `lang-python.md` | Python | `/langpack` |
| `lang-rust.md` | Rust | `/langpack` |
| `lang-js-ts.md` | JavaScript / TypeScript | `/langpack` |
| `lang-react.md` | React | `/langpack` |
| `lang-angular.md` | Angular | `/langpack` |
| `lang-flutter.md` | Flutter / Dart | `/langpack` |

## Domain

| Pack | Covers | Skill |
|---|---|---|
| `quant-research.md` | Point-in-time data, backtests, costs, promotion gates | `/quant` |
| `quant-ml.md` | Purged CV, labeling, PBO/DSR, meta-labeling | `/quant` |
| `quant-execution.md` | Order lifecycle, risk limits, reconciliation | `/quant` |
| `econometrics.md` | Time series, unit roots, cointegration, GARCH | `/econ` |
| `regression.md` | Inference vs prediction, robust SEs, OVB, regularization, CV | `/econ` |
| `microeconometrics.md` | Panel, DiD, RD, IV, discrete choice, spatial | `/econ` |
| `microeconomics.md` | Choice, duality, GE, uncertainty, mechanism design | `/econ` |
| `macroeconomics.md` | Vintage data, shock identification, nowcasting, cycle measurement | `/econ` |
| `game-theory.md` | Equilibria, repeated games, auctions, matching | `/econ` |
| `behavioral-finance.md` | Limits to arbitrage, prospect theory, anomalies | `/econ` |
| `game-design.md` | Game feel, juice, camera, difficulty, onboarding | `/design` |
| `data-architecture.md` | Storage selection, CQRS/ES, sagas, medallion | `/dataarch` |
| `message-brokers.md` | Delivery semantics, DLQ, retry, broker choice | `/dataflow` |
| `streaming-kafka.md` | Topics, partitioning, consumers, schema evolution | `/dataflow` |
| `outbox-cdc.md` | Transactional outbox, Debezium, inbox/idempotency | `/dataflow` |
| `jobs-hangfire.md` | Background jobs, recurring work, retries | `/jobs` |
| `containers-docker.md` | Images, compose, healthchecks, limits | `/container` |
| `langchain.md` | Layer choice, LCEL, LangGraph, middleware, RAG | `/agentapp` |
| `nosql.md` | Access-pattern modelling, partition keys, consistency, per-engine traps | `/dataarch` |
| `coordination.md` | ZooKeeper/etcd/Consul, locks, election, fencing | `/dataarch` |
| `orchestration.md` | Airflow/Dagster/Temporal, partitions, backfills, quality gates | `/dataarch` |
| `grpc.md` | Proto evolution, deadlines, status codes, streaming | `/dataarch` |
| `rabbitmq.md` | Exchanges, quorum queues, prefetch, DLX retry topology | `/dataflow` |
| `sqs.md` | SQS/SNS/EventBridge, visibility timeout, DLQ, FIFO groups | `/dataflow` |

## Rule citation

Rules are cited `<pack-id>#<number>` — e.g. `outbox-cdc#1`, `quant-ml#3`. Use the
citation in review comments, commit messages, and code comments where a non-obvious
constraint needs a reference.

## Editing

Use `/rulesmith`. One pack per change. `python tools/sync_rules.py` after every edit.
Never edit `CLAUDE.md`, `AGENTS.md`, or `.github/**` by hand — they are generated.
