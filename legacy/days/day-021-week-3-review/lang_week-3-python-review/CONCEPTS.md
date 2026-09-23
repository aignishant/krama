---
day: 21
part: "3.1"
title: "Review who advances and who closes"
ids: [PY-21]
level: working
prerequisites: ["Days 15–20 iteration and generators"]
failure: true
---

# Review who advances and who closes

Start with the cold assignment in [README.md](README.md). Open this repair lesson only
after the attempt, or record the explanation as help.

Core reading: explanation, worked trace, and readiness within the existing track cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Trace cursor ownership, advancement, suspension, and cleanup before deciding that an iterable can be reused.

## The story

A validation pass succeeds, then the export writes nothing. Both functions received the same exhausted iterator; no data disappeared from storage.

## The idea in plain language

Begin cold: choose one surprise from your own Days 15–20 notes, predict its output, reproduce
it from memory, and add a regression assertion for the repair. Use 3 minutes prediction,
8 experiment, 4 explanation/testing. Afterward, this repair lesson connects the models.
An iterable supplies an iterator; the iterator carries traversal state. A generator is an
iterator with suspended execution. Exhaustion, explicit closure, and normal return are
distinct events. A wrapper must preserve the parts of this contract its consumer relies on.

## Why Krama needs it

This develops PY-21 in its independent track. Use the prerequisite named above;
the other two tracks are not prerequisites. The [day hub](../LESSON.md) preserves the daily budgets.

## The source behind it

[Python 3.12 iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types) supports the cursor model; use the original six lessons for their generator-specific references.
Source links checked 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
The examples and small failure models below are original teaching demonstrations.

## The mechanism

### Worked trace

Repair navigation: [iterator protocol](../../day-015-sorted-pair-existence/lang_iterator-protocol/CONCEPTS.md),
[laziness](../../day-016-unique-triples/lang_generator-laziness/CONCEPTS.md),
[cleanup](../../day-017-container-capacity/lang_generator-cleanup/CONCEPTS.md),
[delegation](../../day-018-fixed-window-maximum-sum/lang_yield-delegation/CONCEPTS.md),
[consumption](../../day-019-longest-distinct-substring/lang_iterator-consumption/CONCEPTS.md), and
[pipelines](../../day-020-minimum-positive-window/lang_streaming-pipeline/CONCEPTS.md).

Trace one cursor over [2,4,6]: creation consumes nothing; asking whether 4 is present reads
2 and 4; converting the remainder to a list yields [6]; a second conversion yields [].
Membership did work even though its public result was only True. To support two complete
passes over a finite source, snapshot before either consumer. That costs O(n) time and
space up front. A fresh source factory can avoid retaining all items if reopening is cheap
and the source remains consistent. A one-pass pipeline can instead change the contract.

The repair is correct because each traversal of the stored sequence gets a fresh cursor;
it is not correct because iter was called twice on the same iterator. Large or infinite
sources rule out unconditional materialization. Cleanup ownership still needs a separate
decision: exhaustion during normal use does not guarantee early-stop cleanup.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
cursor = iter([2, 4, 6])
found = 4 in cursor
remaining = list(cursor)
print('membership:', found, 'remaining:', remaining, 'again:', list(cursor))
assert remaining == [6]
snapshot = tuple(iter([2, 4, 6]))
assert 4 in snapshot
assert list(snapshot) == [2, 4, 6]
assert list(snapshot) == [2, 4, 6]
print('replay:', list(snapshot))
```

**Line by line:** The first consumer advances the shared cursor. The snapshot is created from a fresh source before any read, so membership and later traversal do not share a traversal position. Repeated assertions verify replay.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
membership: True remaining: [6] again: []
replay: [2, 4, 6]
```

The failing behavior is deliberate; subsequent assertions check the repair on these examples.
An executed Python model does not establish database behavior or production performance.

## In production

Name who owns resource closure when a consumer stops early. A lazy pipeline may still
retain unbounded data if a stage caches or sorts everything. Keep the regression small and
predictable; evidence should explain a language mechanism, not merely paste the output.

## Check yourself

### Readiness before practice

1. Which operations in the trace advance the cursor?
2. Why does iter(cursor) fail to provide a fresh traversal?
3. When is snapshotting a bad repair?
4. What evidence would distinguish early closure from normal exhaustion?

Use [README.md](README.md) for the assignment, verification, and personal evidence route.
Reading the lesson does not complete study.
