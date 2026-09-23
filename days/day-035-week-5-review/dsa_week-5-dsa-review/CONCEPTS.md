---
day: 35
part: "1.1"
title: "Week 5 DSA review"
ids: [DSA-35]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Week 5 DSA review

Cold review: attempt [the assignment](README.md) first. Use this lesson afterwards for repair; record any help.

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

The Week 5 gate checks two independent solves and the reasoning behind ordering, ties, and rank.

## The story

A remembered selection template passes distinct values but fails on a repeated pivot. A cold review reveals the gap that rereading had hidden.

## The idea in plain language

Attempt first, then use this repair map. Revisit [stable sorting](../../day-029-stable-record-sorting/dsa_stable-record-sorting/CONCEPTS.md) and
[selection](../../day-033-kth-smallest/dsa_kth-smallest/CONCEPTS.md) only after the cold attempts. The shared skill is identifying
which ordering information the result needs and proving that a local step preserves it.
Sorting retains every rank; selection keeps only the region containing one rank.

## Why Krama needs it

This develops DSA-35. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Official LeetCode companion](https://leetcode.com/problems/sort-an-array/) defines the online contract; [LEETCODE.md](LEETCODE.md) compares it with local practice.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Use 5 minutes recall, 20 minutes first re-solve, 20 minutes second re-solve,
10 minutes critique, and 5 minutes logging. Re-solve Day 29 and Day 33 from blank code.
A harder unresolved problem may replace the second slot. Local Day 35 fixtures cover only
selection: verify the first attempt separately against the Day 29 contract.

| Topic | Certificate to explain after the attempt | Distinguishing boundary |
| --- | --- | --- |
| [Day 29](../../day-029-stable-record-sorting/dsa_stable-record-sorting/CONCEPTS.md) | left-first equality preserves stability | distinct names with equal scores |
| [Day 30](../../day-030-merge-overlapping-intervals/dsa_merge-overlapping-intervals/CONCEPTS.md) | finalized intervals cannot reconnect | nested interval |
| [Day 31](../../day-031-insert-an-interval/dsa_insert-an-interval/CONCEPTS.md) | sorted prefix / merge / suffix | bridge at both endpoints |
| [Day 32](../../day-032-minimum-meeting-rooms/dsa_minimum-meeting-rooms/CONCEPTS.md) | peak overlap equals needed rooms | simultaneous end and start |
| [Day 33](../../day-033-kth-smallest/dsa_kth-smallest/CONCEPTS.md) | pivot band covers consecutive ranks | all equal values |
| [Day 34](../../day-034-count-inversions/dsa_count-inversions/CONCEPTS.md) | disjoint classes of counted pairs | equal and negative values |

Score correctness, explanation, complexity, and tests from 0–2 each. Passing requires 6/8,
correctness=2, and at least one hint-free solve across both scheduled attempts. Preserve an
honest partial result if time expires. Repair notes should name the violated invariant,
minimal counterexample, corrected transition, and next cold check. A memorized complexity
label without explaining buffer allocation or pivot choice is incomplete evidence.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
records = [('older', 4), ('newer', 4)]
bad = list(reversed(records))
scores_only = [x[1] for x in bad] == sorted(x[1] for x in records)
identity_order = [x[0] for x in bad] == [x[0] for x in records]
print('weak sortedness check:', scores_only)
print('stability check:', identity_order)
assert scores_only and not identity_order
fixed = sorted(records, key=lambda x: x[1])
assert fixed == records
print('repaired order:', [x[0] for x in fixed])
```

**Line by line:** Reversing two tied records simulates an unstable merge. A score-only check passes, while identity order rejects the bug. The stable built-in is a repair oracle, not permission to replace the assigned merge-sort implementation.

Observed author output on Python 3.12.10, 2026-09-23:

```text
weak sortedness check: True
stability check: False
repaired order: ['older', 'newer']
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

A useful review artifact lets another person reproduce the failure. Record input, expected
result, actual result, and the reason the fix generalizes beyond that input. Keep the original
cold result after repair; otherwise the record loses diagnostic value. Optional depth is
additional adversarial testing in another sitting, not a third required solve today.

## Check yourself

### Readiness before practice

After the attempts: can you defend equality handling, partition progress, and actual memory use? Which counterexample defeated the first draft, and what remains unresolved?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
