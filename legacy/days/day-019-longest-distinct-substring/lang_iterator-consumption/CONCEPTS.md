---
day: 19
part: "3.1"
title: "Account for every consumer of an iterator"
ids: [PY-19]
level: working
prerequisites: ["Day 15 iterator protocol; Day 16 laziness"]
failure: true
---

# Account for every consumer of an iterator

Core reading: explanation, worked trace, and readiness. The production section offers optional
depth for another sitting; keep the existing track budget and record partial work honestly.

## One-line answer

Membership searches and materialization advance a one-shot iterator; choose explicit storage or a fresh source for another pass.

## The story

A validation check confirms that a report contains a marker. The export that follows loses
the report's opening rows because the check already read through them.

## The idea in plain language

Review [iterable versus iterator](../../day-015-sorted-pair-existence/lang_iterator-protocol/CONCEPTS.md).
For the built-in list iterator used here, x in cursor repeatedly advances until it finds x or
exhausts the cursor. The matching item is consumed too. list(cursor) drains whatever remains;
calling iter(cursor) again does not rewind it. Custom containers may provide __contains__
with different behavior, so this statement concerns searches using the iterator protocol.

Recognition cue: two operations share the same cursor but each expects the original sequence.
Audit sum, any, all, membership, loops, and list as consumers. Short-circuiting can consume a
prefix, while a search that misses can consume the entire finite stream.

## Why Krama needs it

This develops PY-19 for the [Week 3 review](../../day-021-week-3-review/LESSON.md).
The tracks remain independent; use only this subject's prerequisites.

## The source behind it

[Python 3.12 membership tests](https://docs.python.org/3.12/reference/expressions.html#membership-test-operations)
describes iteration-based membership; [itertools.tee](https://docs.python.org/3.12/library/itertools.html#itertools.tee)
documents buffering and shared-source constraints. Checked 2026-09-22; details are in the [source ledger](../../../docs/SOURCES.md).
The trace and counterexample below are original teaching examples.

## The mechanism

### Worked trace

Trace cursor=iter([2, 4, 6]). Searching for 4 requests 2 and then 4, returns True, and leaves
only 6. Turning that cursor into a list returns [6]. A second list returns []. Searching for
99 on a fresh cursor returns False and leaves nothing. On an infinite cursor, a missing value
may never terminate the search.

| Need | Repair | Cost and limit |
| --- | --- | --- |
| Small finite snapshot used twice | Materialize once before either pass | O(n) memory; stable stored values |
| Reopenable source | Use a factory for a fresh iterator each time | Repeats work; source may change |
| Two consumers advancing together | tee(source, 2) | Buffers their lag; worst case O(n) |
| One combined result | Fuse validation and processing in one traversal | May delay when a decision is available |

Do not use the original source iterator after splitting it with tee; the clones depend on
coordinated advancement. tee does not make an infinite stream safe to pre-scan. Materializing
after membership cannot recover the already consumed prefix. Snapshot before consumption when
repeatability is required, and distinguish replaying data from repeating external side effects.

## When it breaks

Run this separate teaching demonstration before implementing your own exercise.

```python
cursor = iter([2, 4, 6])
print("contains 4:", 4 in cursor)
remaining = list(cursor)
print("remaining:", remaining, "second list:", list(cursor))
try:
    assert remaining == [2, 4, 6], "membership consumed the prefix and match"
except AssertionError as error:
    print(f"AssertionError: {error}")
snapshot = list(iter([2, 4, 6]))
assert 4 in snapshot
assert list(snapshot) == [2, 4, 6]
print("snapshot replay:", list(snapshot))
missing = iter([2, 4, 6])
assert 99 not in missing
assert list(missing) == []
```

**Line by line:** The same cursor first feeds membership, then list, then another list. The assertion
deliberately expects an impossible rewind. The repair materializes a fresh source before either
consumer. The final missing-value case verifies full exhaustion without relying on printed output.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
contains 4: True
remaining: [6] second list: []
AssertionError: membership consumed the prefix and match
snapshot replay: [2, 4, 6]
```

**Line by line:** These are the actual printed observations, including the deliberately caught
assertion or exception. A caught failure documents the wrong assumption; later assertions check
the repair on the stated example, not on every possible input.

## In production

A database cursor or network stream may not be replayable or stable across fresh queries.
An unbounded list conversion can exhaust memory, and a fast tee branch can retain everything
for a slow one. Pick a bounded batch, spool, or explicit snapshot contract when replay is
essential. Avoid logging list(cursor) for inspection when the application still needs it;
logging is then a destructive reader of the stream, even if it does not mutate the source data.

## Check yourself

### Readiness before practice

1. Which items remain after 4 in iter([2, 4, 6])?
2. Why is list(cursor) after the search too late to make a complete snapshot?
3. What determines tee's memory usage?
4. When can a fresh iterator factory still fail to reproduce the same report?

Use [README.md](README.md) for the assignment and evidence route. Reading does not complete study.
