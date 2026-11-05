---
name: quant
description: Quantitative research and trading — point-in-time data, feature engineering, backtesting, overfitting control, transaction costs, order execution, risk limits, and reconciliation. Use when writing or reviewing anything involving market data, signals, alpha, backtests, portfolio construction, order management, or when a live strategy diverges from its backtest.
---

# Quant

Rules: `rules/quant-research.md` (research), `rules/quant-execution.md` (live).

The failure mode here is not a crash. It is a backtest that looks excellent and is
wrong. Treat every rule as a defense against a specific class of silent error.

---

## Reviewing research code — the eight questions

Ask these in order. Most defective backtests fail at question 1 or 5.

1. **Lookahead** — does every feature at `t` use only what was observable at `t`,
   including revisions? Are fundamentals keyed on filing date, not period end? Is index
   membership as-of?
2. **Survivorship** — does the universe include delisted, merged, and bankrupt names
   with their terminal returns?
3. **Corporate actions** — one adjustment convention, applied identically in research
   and production? Total-return or price-only, stated?
4. **Time semantics** — UTC, timezone-aware, event time distinguished from arrival
   time? Signals keyed on arrival?
5. **Costs** — commissions, half-spread each side, borrow, financing, and impact
   (`σ·(Q/ADV)^0.5`) modelled *before* evaluation, not subtracted afterwards?
6. **Selection** — how many configurations were tried? Is a Deflated Sharpe or PBO
   reported? Was the holdout looked at more than once?
7. **Leakage** — is CV purged (labels overlapping the test window removed) and
   embargoed (gap after)? Are normalization statistics fit on train only?
8. **Parity** — do research and production call the *same* feature implementation, or
   two copies of it?

Report each as PASS / FAIL / CANNOT-VERIFY with `file:line` evidence. Report everything
including uncertain findings — filter in a separate pass, not during discovery.

## Numerical hygiene

- `float64` for prices and quantities; `Decimal` or integer minor units for cash
- Log returns to aggregate over time; simple returns across assets. Do not mix.
- Kahan or pairwise summation for long PnL accumulations
- `np.random.default_rng(seed)` — never legacy global `np.random.*`
- Keep a slow, obviously-correct reference implementation and property-test the fast
  one against it

## Escalating for speed

Vectorized NumPy/Polars → Numba → Rust or C++ extension. Go only as far as the target
requires, and keep the reference implementation at every step.

## Promotion gates

Each gate requires the previous one.

| Gate | Requires |
|---|---|
| Research | Point-in-time clean; costs modelled; purged CV; DSR/PBO reported |
| Walk-forward | Positive on rolling OOS windows; parameter stability shown |
| Paper | Live data, simulated fills, ≥1 month; slippage within modelled bounds |
| Live (limited) | Small capital; daily reconciliation; kill switch armed; drawdown limit |
| Live (full) | Sustained performance inside the paper confidence interval |

---

## Execution review

1. **Idempotency** — deterministic `client_order_id` generated before the first send and
   reused on every retry?
2. **Retry safety** — does a timeout query order status before re-sending?
3. **Pre-trade risk** — max size, max position, max gross/net, order rate, price collar,
   fat-finger notional — **in the order path**, not in a monitor beside it?
4. **Kill switch** — reachable without a deploy, tested, cancels + blocks + optionally
   flattens?
5. **Reconciliation** — positions, cash, and working orders reconciled against the
   venue continuously; a break halts that instrument?
6. **Durability** — every state transition persisted before it is acted on, append-only,
   replayable on crash?
7. **Money** — integer minor units or `Decimal`, never float?
8. **Clock** — NTP/PTP drift monitored and alerted; venue and local timestamps both
   logged?

## When live diverges from backtest

Work the list in order — the first three account for most cases.

1. **Costs** — compare realized slippage per order against the model. Drift here is the
   earliest signal of decaying edge.
2. **Train/serve skew** — is the live feature value identical to the research value for
   the same timestamp? Compute both and diff.
3. **Timing** — is live acting on arrival time while research used event time?
4. **Universe** — is the live universe filtered by something research did not apply?
5. **Fills** — partial fills, queue position, rejected orders that research assumed filled
6. **Overfitting** — if none of the above explains it, the edge was probably selection
   noise. Check the DSR.

## Anti-patterns worth naming

- Notebook as the artifact. Notebooks are for exploration; anything producing a result
  someone acts on lives in a tested module invoked by a pipeline.
- Dropping NaNs without understanding them — a missing price is information (halt,
  delisting, no trade), and dropping it silently changes the universe.
- Refitting on the same period after being disappointed. That loop is a fitting
  procedure with the researcher inside it.
- Reporting a single Sharpe. Report the distribution: Sortino, max drawdown and its
  duration, turnover, capacity, hit rate, tail ratio, and performance by year and regime.
