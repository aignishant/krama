---
day: 28
part: "2.1"
title: "Week 4 design review"
ids: [SD-28]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Week 4 design review

Cold review: attempt the task in [README.md](README.md) without this lesson first.
Use this explanation afterwards for repair and record any help.

Core reading: intuition, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting. Record partial progress if needed.

## One-line answer

Review one weak decision by stating its invariant, exposing a concrete failure, and replacing the decision with an enforceable boundary.

## The story

A design memo says "use transactions" but does not say what happens when two writers read the same quota. A review should turn that vague promise into a precise operation and failure response.

## The idea in plain language

Attempt your own review before reading this or the reference. An invariant describes valid
state; an access path describes how a query finds it. A fast index cannot make a stale edit
safe, and a transaction alone does not explain a retry policy. Select your weakest decision
from Days 22–27 and repair that one artifact within the 30-minute track.

## Why Krama needs it

This develops SD-28 independently of the other two tracks. The [day hub](../LESSON.md)
links the separate 60/30/15-minute routes; completing the reading is not passing the assignment.

Read the [complete reference answer](REFERENCE_DESIGN.md) within the concept/critique
window; keep your own practice in [DESIGN.md](DESIGN.md).

## The source behind it

[13.2. Transaction Isolation](https://www.postgresql.org/docs/18/transaction-iso.html) supplies database-specific concurrency rules. The review method and state example are original teaching material.
Checked 2026-09-23; details are in the [source ledger](../../../docs/SOURCES.md).
The traces, examples, and failure demonstrations here are original teaching material.

## The mechanism

### Worked trace

Use the existing recall/concept/artifact/critique windows as cold recall, locating your prior
artifact, revising one memo, and defending it. Read repair material or the reference after the
cold attempt, or explicitly record that the review became guided.

| Day | Decision to revisit | Concrete defense |
| --- | --- | --- |
| 22 | [Schema constraints](../../day-022-lower-bound/sd_schema-constraints/CONCEPTS.md) | valid rows and rejected invalid states |
| 23 | [Index selection](../../day-023-target-range/sd_index-selection/CONCEPTS.md) | query shape, ordering, and write/storage cost |
| 24 | [Query plans](../../day-024-rotated-search/sd_query-plans/CONCEPTS.md) | estimates versus actual observations |
| 25 | [Transactions](../../day-025-integer-square-root/sd_transactions/CONCEPTS.md) | commit boundary and lost acknowledgment |
| 26 | [Isolation](../../day-026-minimum-shipping-capacity/sd_isolation-anomalies/CONCEPTS.md) | two-writer schedule and retry classification |
| 27 | [Versioned edits](../../day-027-median-of-two-arrays/sd_optimistic-concurrency/CONCEPTS.md) | guarded update and client conflict resolution |

A complete review has before and after: "read quota, later save a computed count" becomes
"reserve by conditional increment and require one affected row before insertion." Explain
why the same two-writer schedule now admits only one reservation. Compare a row-lock alternative
and name the cost of coordination. Do not add unrelated infrastructure to make the diagram
look complete.

Use a three-point failure timeline: before mutation, after mutation before commit, and after
commit before response. For each, state durable state, caller-visible outcome, and safe next
action. The [reference](REFERENCE_DESIGN.md) chooses optimistic editing as its sample weak
decision; your own choice can differ. Reference scenarios are hypothetical, not measured tests.
Score requirements, data/API, scale, and failure tradeoffs 0–2; the gate is 6/8 and no unexplained
source of truth. Preserve the initial artifact so that the change in reasoning is visible.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
def weak_check(used, limit):
    return used <= limit

used, limit, actual_links = 5, 5, 6
print("counter-only review passes:", weak_check(used, limit))
consistent = used == actual_links and used <= limit
print("full accounting invariant passes:", consistent)
assert weak_check(used, limit) and not consistent
used, actual_links = 5, 5
assert used == actual_links and used <= limit
print("consistent committed-state example passes")
```

**Line by line:** The weak check only inspects a bounded counter. Adding actual_links exposes the broken relationship without pretending that this Python check is a database constraint. The repaired state is a valid example, not a recovery algorithm; the design must explain how writes maintain that state.

Observed author output on Python 3.12.10, 2026-09-23:

```text
counter-only review passes: True
full accounting invariant passes: False
consistent committed-state example passes
```

The deliberate failure and repaired assertions are teaching evidence, not learner progress.
Python state models do not demonstrate PostgreSQL isolation or production performance.

## In production

A useful review produces a falsifiable next check: a captured plan, a concurrent database test,
or an explicit conflict response assertion. Separate assumed contention from measured contention.
Under load, a correct row lock can still cause long waits; propose the measurement that would
justify changing the design. Optional depth: revisit the chosen decision with a new workload,
keeping the original correctness requirement explicit.

## Check yourself

### Readiness before practice

After the attempt, can you name the old failure, the new enforcement point, one credible
alternative, and the remaining uncertainty? Which statement in your memo is an assumption,
which follows from a source, and which has actually been observed?

Run the teaching block only if you need to check your prediction. Then return to
[README.md](README.md) for the assignment, verification, and personal evidence route.
