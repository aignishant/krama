---
day: 14
part: "2.1"
title: "Revise one decision using a failure trace"
ids: [SD-14]
level: working
prerequisites: ["Days 8\u201313 design artifacts"]
failure: true
---

# Revise one decision using a failure trace

Begin with the cold assignment in [README.md](README.md). Read this repair lesson only after
the attempt, or record that you deliberately used help.

Core: explanation, worked trace, and readiness. Production extensions are optional depth;
continue another sitting if needed within the existing track budget.

## One-line answer

A useful review links a violated requirement to a concrete failure and revises the smallest decision that prevents it.

## The story

A listing appears correct in a quiet demo but repeats a row when someone adds a link. Saying the design is scalable does not explain which guarantee failed or how to repair it.

## The idea in plain language

A design review compares promised behavior with a request-by-request scenario. Begin cold
with your weakest prior memo; its weakness must come from your evidence, not a supplied answer.
Afterward, use the reference's pagination example to compare the shape of your argument. A
tradeoff names what gets better and what gets worse. An assumption is a chosen premise, not
a measured fact. No traffic load, database latency, or learner weakness is measured here.

## Why Krama needs it

[Day 15 domain model](../../day-015-sorted-pair-existence/sd_domain-model/CONCEPTS.md) relies on stable identities and explicit ownership to make later promises testable.

## The source behind it

[PostgreSQL 18 — LIMIT and OFFSET](https://www.postgresql.org/docs/18/queries-limit.html) supports the pagination example. Other review choices should use their original lesson sources. Checked 2026-09-22; see the dated [source ledger](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

Choose one entry, retain its user-visible requirement, and write the failure before the revision:

| Prior decision | Concrete question | Repair reading |
| --- | --- | --- |
| Request journey | Where did latency or failure first occur? | [Day 8](../../day-008-first-repeated-value/sd_request-journey/CONCEPTS.md) |
| HTTP methods | Can this operation be safely prefetched? | [Day 9](../../day-009-frequency-ranking/sd_http-methods/CONCEPTS.md) |
| Idempotency | What happens after commit but before response? | [Day 10](../../day-010-pair-sum-indices/sd_idempotency-semantics/CONCEPTS.md) |
| Connections | Does the limit hold during fleet growth? | [Day 11](../../day-011-group-anagrams/sd_connection-budgets/CONCEPTS.md) |
| Deadlines | How much time remains after queueing? | [Day 12](../../day-012-range-sums/sd_timeout-propagation/CONCEPTS.md) |
| Pagination | Does insertion shift continuation? | [Day 13](../../day-013-count-target-subarrays/sd_pagination/CONCEPTS.md) |

Worked review trace: old decision uses OFFSET 2. Page one returns keys 8 and 7. Inserting
key 9 changes the order to 9,8,7,6,5, so page two repeats 7. Revision: continue strictly below
the last key 7, yielding 6 and 5. The identity/order invariant prevents this repeat for
unchanged keys. The cost is losing arbitrary numbered-page jumps; it still does not promise
a snapshot. Real keys must use creation time plus a unique ID, not a timestamp alone.

Use 5 minutes for cold recall, 10 for the failure and concept comparison after that attempt,
12 to revise one artifact, and 3 to critique. If you consult material, record it as help.

## When it breaks

```python
before = [8, 7, 6, 5]
first = before[:2]
after = [9] + before
wrong = after[2:4]
fixed = [key for key in after if key < first[-1]][:2]
print("old continuation:", wrong, "revised:", fixed)
try:
    assert not set(first) & set(wrong), "review found a repeated link"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert fixed == [6, 5]
```

**Line by line:** Integer keys stand in for already-unique ordering tuples. The inserted row shifts the offset. The saved key survives the change. The assertion makes the violated no-repeat requirement explicit in an executed model.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
old continuation: [7, 6] revised: [6, 5]
AssertionError: review found a repeated link
```

## In production

A revision can move risk elsewhere: retry handling consumes storage, tighter timeouts reject useful work, and cursor traversal sacrifices random access. Defend the alternative under requirements where it would win. Choose observable checks for a later implementation without inventing successful measurements. A complete review includes residual limits, not merely a revised diagram.

## Check yourself

### Readiness before practice

1. Which exact requirement did your failure violate?
2. What assumption makes the repair correct?
3. Under which requirement would your alternative win?
4. Which part is modeled evidence and which remains unmeasured?

Run the teaching block in a scratch interpreter, then explain the distinguishing failure aloud.
Use [README.md](README.md) to enter the assignment and record your own evidence.
