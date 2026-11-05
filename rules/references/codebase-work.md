# codebase-work — reference

Loaded on demand from `rules/codebase-work.md`. Rules live there; this is the detail
needed to implement them.

## 1. Precedence — what wins when rules conflict

Highest first. This is the answer to "the codebase does it differently".

| # | Source | Yields to |
|---|---|---|
| 1 | **Correctness, safety, security** — memory safety, injection, data loss, races | Nothing |
| 2 | **Explicit instruction for this task** | 1 |
| 3 | **Detected codebase convention** (`.agent/conventions.md`) | 1–2 |
| 4 | **Pack "Prefer" rules** in this repo | 1–3 |
| 5 | Model defaults | everything |

So: a codebase that uses 2-space indent, `snake_case`, and exceptions-for-control-flow
gets 2-space indent, `snake_case`, and exceptions-for-control-flow — even where a pack
prefers otherwise. A codebase that concatenates SQL strings does **not** get more
concatenated SQL.

State the override when you take one: *"following the local convention of X, which
differs from `pack#n`."* Silent divergence looks like an error.

## 2. Doc comments

The contract: **types come from the signature; meaning, validity, failure, and context
come from you.** Say what a caller cannot see.

Include, in this order: purpose · parameter meaning and valid values · return ·
failure modes · usage context (who calls this and why, or which of several similar
functions to pick) · non-obvious invariants (units, ownership, thread-safety,
complexity, allocation).

```csharp
/// <summary>
/// Settles a payment against the ledger and enqueues the domain event in the same
/// transaction.
/// </summary>
/// <param name="paymentId">Payment in <c>Authorized</c> state. Any other state throws.</param>
/// <param name="amountMinor">Amount in minor units (cents). Must be > 0 and ≤ the
/// authorized amount; partial settlement is allowed, over-settlement is not.</param>
/// <param name="ct">Cancels before the transaction opens; a cancel after commit is ignored.</param>
/// <returns>The ledger entry id. Returns the existing id if already settled (idempotent).</returns>
/// <exception cref="InvalidPaymentStateException">Payment is not <c>Authorized</c>.</exception>
/// <remarks>
/// Called by <c>SettlementJob</c> (batch, nightly) and by <c>PaymentsController.Settle</c>
/// (interactive). Both retry on failure, which is why this is idempotent on
/// <paramref name="paymentId"/>. Writes the outbox row inside the same transaction —
/// see outbox-cdc#1; do not move the enqueue outside it.
/// </remarks>
```

```python
def settle(payment_id: UUID, amount_minor: int, *, clock: Clock) -> LedgerEntryId:
    """Settle a payment against the ledger and enqueue its domain event atomically.

    Args:
        payment_id: Payment in ``AUTHORIZED`` state; any other state raises.
        amount_minor: Amount in minor units (cents), ``0 < amount_minor <= authorized``.
            Partial settlement is allowed; over-settlement is not.
        clock: Injected so settlement timestamps are deterministic in tests.

    Returns:
        The ledger entry id. Idempotent: returns the existing id if already settled.

    Raises:
        InvalidPaymentState: Payment is not ``AUTHORIZED``.

    Context:
        Called by ``settlement_job`` (nightly batch) and the ``POST /payments/settle``
        handler. Both retry, which is why this is idempotent on ``payment_id``.
        The outbox insert shares this function's transaction — see ``outbox-cdc#1``.
    """
```

```rust
/// Settles a payment against the ledger, enqueuing the domain event atomically.
///
/// # Parameters
/// - `payment_id`: must reference a payment in [`State::Authorized`].
/// - `amount_minor`: minor units (cents); `0 < amount_minor <= authorized`.
///
/// # Errors
/// [`SettleError::InvalidState`] if the payment is not authorized.
///
/// # Context
/// Called from the nightly `settlement_job` and the HTTP handler. Both retry, so this
/// is idempotent on `payment_id`. Holds the transaction across the outbox insert —
/// see `outbox-cdc#1`.
///
/// # Panics
/// Never. Errors are returned.
```

```typescript
/**
 * Settles a payment against the ledger and enqueues its domain event atomically.
 *
 * @param paymentId - Payment in `Authorized` state; other states reject.
 * @param amountMinor - Minor units (cents); `0 < amountMinor <= authorized`.
 *   Partial settlement allowed, over-settlement rejected.
 * @returns The ledger entry id; idempotent on `paymentId`.
 * @throws {InvalidPaymentStateError} Payment not in `Authorized`.
 *
 * @remarks
 * Called by the nightly `settlementJob` and by `POST /payments/settle`. Both retry,
 * hence idempotency. The outbox write shares this transaction (outbox-cdc#1).
 */
```

**Doc comment vs inline comment** — the split that keeps both rules coherent:

| | Doc comment (above the declaration) | Inline comment (inside the body) |
|---|---|---|
| Audience | Callers | The next person editing this function |
| Says | Contract, meaning, context | Constraints the code cannot express |
| Required | Every public function/type | Only where non-obvious |
| Never | Implementation detail that may change | Narration of the next line |

```python
# BAD  — narrates
i += 1  # increment i

# GOOD — states a constraint the code cannot express
# Vendor caps the batch at 500; above that the API silently truncates.
for chunk in batched(rows, 500):
```

Private helpers need a one-line doc comment only when the name does not already say it.

## 3. Reuse search protocol

Before writing a new function, run all four. Two minutes here saves a duplicate.

```bash
graphify query "what handles <domain noun>" --graph graphify-out/graph.json --budget 1200
sg -p 'fn $NAME($$$) { $$$ }' -l rust          # or the language's shape
rg -n --glob '!{node_modules,dist,build,target}' '<verb>|<noun>' src/
```

Search for four things, because the existing version is rarely named what you would
name it:

1. The **operation** — `settle`, `reconcile`, `normalize`.
2. The **domain noun** — `payment`, `ledger`, `position`.
3. The **shape** — a function taking the same types, via structural search.
4. The **test names** — tests describe behaviour in words closer to intent than code is.

If you find something close but not identical, decide with §4 before extending it.

## 4. Blast radius — refactor, extend, or ask

"Context" means: a scope where you can enumerate every caller and verify them.

| Callers | Same module/package? | Do |
|---|---|---|
| Only the one you are changing | yes | **Refactor freely** |
| A handful, all in the same module | yes | **Refactor**, update them in the same commit |
| Several, across modules, same repo | no | **Ask** — offer new-function vs refactor, name the callers |
| Public API / published package / other repos | no | **New function**; deprecate the old one on a stated path |
| Unknown — cannot enumerate | no | Treat as public API |

**How to ask**, so the answer is cheap to give:

> `normalizePrice()` in `pricing/format.ts` does what I need but rounds half-up;
> I need half-even for the ledger. It has 7 callers: 5 in `pricing/`, 2 in `reporting/`.
> Options: (a) add a `rounding` parameter, defaulting to current behaviour — one-line
> change per call site, none required; (b) new `normalizePriceHalfEven()` — no risk to
> existing callers, two near-identical functions. I'd take (a). Which?

Name the function, the callers, both options, and your recommendation. A question
without those forces the reader to do the investigation you already did.

**When a boolean parameter is the wrong answer:** if the flag selects between two
genuinely different behaviours rather than a variation on one, you have merged two
functions to avoid writing a second. Split it.

## 5. Minimal change, and its exception

The diff should contain the change and nothing else. Not reformatting, not renames, not
import reordering, not the unrelated bug you noticed.

Rule 3's exception is narrow and specific: a smaller diff is not smaller if it leaves
behind a correctness, safety, or **measured** performance problem in the code you are
already touching. "Measured" is load-bearing — see `performance#1`. A performance
refactor without a before/after number is a preference.

When you do take the larger change, split the commits:

```
1. refactor: extract rounding mode into a parameter   (no behaviour change)
2. fix: use half-even rounding in ledger normalization (behaviour change, 3 lines)
```

The reviewer can verify commit 1 mechanically and think hard only about commit 2.

## 6. Conventions file

Generated, not written by hand:

```bash
python tools/detect_conventions.py            # writes .agent/conventions.md
python tools/detect_conventions.py --print    # inspect without writing
```

It samples the repo for indentation, line length, naming, doc-comment style, comment
density, test framework and layout, error-handling idiom, and formatter/linter configs,
then records what it found and how confident it is.

Read it at the start of work on an unfamiliar codebase. Where it reports **high**
confidence, follow it without comment. Where it reports **low** confidence, the codebase
is inconsistent — follow the file you are editing, and say so.

Regenerate it after large merges or when it disagrees with what you see. It is a
snapshot, not an authority: **the file you are editing wins over the aggregate.**

## 7. Greenfield

A genuinely new context — new service, new package, no established convention — is the
one case where you set the standard rather than infer it. Then:

- Use the best current approach, not the one used elsewhere in the repo for unrelated
  reasons. Inheriting a 2014 convention into a new service is not consistency.
- Set the mechanical things first: formatter, linter, line length, test layout,
  error-handling idiom. They are cheap now and expensive later.
- **Write down what you chose and why**, in the module's README or the ADR. The next
  person then inherits a decision instead of an accident.
- Stay inside the repo's *cross-cutting* conventions — logging, config, CI, dependency
  policy — even while choosing new local ones. Those are integration surface, not style.

If the user asked for a specific approach, that is instruction and it outranks all of
this (precedence 2).
