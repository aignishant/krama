---
day: 15
part: "3.1"
title: "An iterator owns a position that only advances"
ids: [PY-15]
level: working
prerequisites: ["Object methods", "StopIteration"]
failure: true
---

# An iterator owns a position that only advances

Core: explanation, worked trace, and readiness. Production extensions are optional depth;
continue another sitting if needed within the existing track budget.

## One-line answer

An iterable supplies an iterator; an iterator returns itself from iter and stays exhausted once next raises StopIteration.

## The story

Two parts of a report read from the same open sequence. The second section is unexpectedly empty because the first section already consumed the cursor.

## The idea in plain language

An iterable can provide a traversal object through iter. That iterator stores progress and
produces one value per next call. A list can create independent iterators; an iterator is its
own iterator and does not reset when iter is called again. StopIteration signals normal
completion, distinct from a data value such as None. A for loop obtains an iterator, repeatedly
requests a value, and stops on that exception. This separates a reusable collection from one
consumable traversal.

## Why Krama needs it

[Day 16 generators](../../day-016-unique-triples/lang_generator-laziness/CONCEPTS.md) automate the saved-position machinery while retaining single-pass behavior.

## The source behind it

[Built-in Types — Iterator Types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types), Python 3.12, specifies __iter__, __next__, and permanent exhaustion. Checked 2026-09-22; see the dated [source ledger](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

For a list `['a', 'b']`, iter creates cursor I at position 0. next(I) yields 'a' and
advances to 1; iter(I) returns I at position 1. Another next yields 'b'. Every later next
signals exhaustion. A new iter(list) starts a different traversal; it does not revive I.
For a custom finite iterator, store the next position and check the terminal bound before
reading or advancing. After the bound is reached, no method should reset it accidentally.
Each indexed step can be O(1); collecting n outputs is O(n) time and O(n) output space.
Traversal state can be O(1) while still retaining a reference to an O(n) collection.

## When it breaks

```python
values = ["a", "b"]
cursor = iter(values)
print("same cursor:", iter(cursor) is cursor)
print("first pass:", list(cursor))
print("second pass:", list(cursor))
for attempt in range(2):
    try:
        next(cursor)
    except StopIteration:
        print("StopIteration")
try:
    assert list(cursor) == values, "iterators do not restart themselves"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert list(iter(values)) == ["a", "b"]
```

**Line by line:** iter(values) creates one cursor; iter(cursor) returns that object. list consumes it. Repeated next calls demonstrate permanent exhaustion. The failing assertion captures the reuse mistake; iter(values) is the explicit fresh-traversal repair.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
same cursor: True
first pass: ['a', 'b']
second pass: []
StopIteration
StopIteration
AssertionError: iterators do not restart themselves
```

## In production

Do not share a cursor between consumers expecting independent results. API documentation should say whether an input is consumed. File and network iterators also own resources; early loop exit does not by itself define cleanup. Choose an iterable container or iterator factory when callers need repeatable traversal, and define mutation behavior before exposing a custom iterator.

## Check yourself

### Readiness before practice

1. What should __iter__ return on an iterator?
2. How will your countdown lab test two next calls after exhaustion?
3. Why is returning None not a completion signal?
4. What object must be recreated for a second pass?

Run the teaching block in a scratch interpreter, then explain the distinguishing failure aloud.
Use [README.md](README.md) to enter the assignment and record your own evidence.
