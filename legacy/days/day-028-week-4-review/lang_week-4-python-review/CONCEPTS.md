---
day: 28
part: "3.1"
title: "Week 4 Python review"
ids: [PY-28]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Week 4 Python review

Cold review: attempt the task in [README.md](README.md) without this lesson first.
Use this explanation afterwards for repair and record any help.

Core reading: intuition, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting. Record partial progress if needed.

## One-line answer

A protocol regression needs to check the caller-visible contract as well as the internal state change.

## The story

A cleanup test stayed green while exceptions disappeared. It checked only that a resource closed, so it missed the behavior that the caller depended on.

## The idea in plain language

Attempt the review from memory first. A protocol is the behavior Python asks of an object
through special methods, not just a list of method names. A regression test is a small check
that fails for a specific old mistake and passes after its repair. Pick one surprising behavior
from Days 22–27; the 15-minute review is one focused reproduction, not six new labs.

## Why Krama needs it

This develops PY-28 independently of the other two tracks. The [day hub](../LESSON.md)
links the separate 60/30/15-minute routes; completing the reading is not passing the assignment.

## The source behind it

[3. Data model](https://docs.python.org/3.12/reference/datamodel.html) is the protocol reference. The reverse-slice counterexample is an original executable review example.
Checked 2026-09-23; details are in the [source ledger](../../../docs/SOURCES.md).
The traces, examples, and failure demonstrations here are original teaching material.

## The mechanism

### Worked trace

Use the existing 3 predict + 8 experiment + 4 explain/test allocation. Write the prediction
without notes, reproduce the behavior, then construct a check that detects the broken contract.
After the attempt, use this repair map:

| Topic | Repair reading | Distinguishing check |
| --- | --- | --- |
| Representations | [Day 22](../../day-022-lower-bound/lang_representations/CONCEPTS.md) | useful repr without leaking sensitive values |
| Rich comparison | [Day 23](../../day-023-target-range/lang_rich-comparison/CONCEPTS.md) | unsupported operand dispatch and equal values |
| Containers | [Day 24](../../day-024-rotated-search/lang_container-protocol/CONCEPTS.md) | membership and iteration agree with the contract |
| Slices | [Day 25](../../day-025-integer-square-root/lang_indexing-and-slicing/CONCEPTS.md) | reverse, clipping, and zero step |
| Callable objects | [Day 26](../../day-026-minimum-shipping-capacity/lang_callable-instances/CONCEPTS.md) | separate instances retain separate state |
| Context managers | [Day 27](../../day-027-median-of-two-arrays/lang_context-managers/CONCEPTS.md) | cleanup occurs and body errors propagate |

For example, a slice implementation that works for forward ranges may reuse the default
start=0 for reverse ranges. The resulting positions can be empty or incomplete. Normalization
must depend on step direction. A single [1:3] test cannot distinguish that bug from a correct
implementation. Test the contract boundary, explain the mechanism, and retain the original
wrong prediction in your notes.

The review passes through prediction, observed reproduction, repaired regression, and a spoken
explanation. A test copied from this lesson is guided repair, not independent evidence. Name
the cost of the chosen operation: a materialized slice takes O(k), while a field lookup in a
small object is not a linear scan through the sequence.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
values = [1, 2, 3]
key = slice(None, None, -1)
normalized = key.indices(len(values))
wrong = values[slice(*normalized)]
right = [values[i] for i in range(*normalized)]
print("reapplied normalized slice:", wrong)
print("normalized positions:", right)
assert wrong != values[::-1]
assert right == values[::-1] == [3, 2, 1]
```

**Line by line:** indices yields range arguments (2,-1,-1). Feeding -1 back through ordinary slice syntax normalizes it again as a relative index and changes its meaning. range consumes the normalized bounds directly. The assertions compare both approaches with the intended reversed sequence.

Observed author output on Python 3.12.10, 2026-09-23:

```text
reapplied normalized slice: []
normalized positions: [3, 2, 1]
```

The deliberate failure and repaired assertions are teaching evidence, not learner progress.
Python state models do not demonstrate PostgreSQL isolation or production performance.

## In production

An assertion about private state can survive a public API regression. Favor observable
behavior and add internal checks only when they explain a failure. State the interpreter version
and avoid relying on nondeterministic repr addresses. Optional depth: compare another interpreter
after the core review, separating documented protocol behavior from implementation details.

## Check yourself

### Readiness before practice

After your cold lab, explain which line caused the surprise, why the regression would have
failed before the repair, and which boundary remains untested. Save the actual error/output
and help used; do not mark a read-through as a completed lab.

Run the teaching block only if you need to check your prediction. Then return to
[README.md](README.md) for the assignment, verification, and personal evidence route.
