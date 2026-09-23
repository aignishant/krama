---
day: 25
part: "3.1"
title: "Indexing and slicing"
ids: [PY-25]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Indexing and slicing

Core reading: intuition, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting. Record partial progress if needed.

## One-line answer

Subscription sends either an index or a slice object to __getitem__; your type must define normalization, errors, and result ownership.

## The story

A page viewer supports the last page and every second page. Its custom wrapper handles page 2, then crashes on a range because it assumed everything inside brackets was an integer.

## The idea in plain language

Review [the container protocol](../../day-024-rotated-search/lang_container-protocol/CONCEPTS.md).
An index selects one position; a slice describes a start, an exclusive stop, and a step. Python
passes the description to your object. It does not automatically make a custom object behave
like a list. Decide whether slices produce another wrapper, a list, or a view, and whether
mutations are shared. This choice is part of the public API.

## Why Krama needs it

This develops PY-25 independently of the other two tracks. The [day hub](../LESSON.md)
links the separate 60/30/15-minute routes; completing the reading is not passing the assignment.

## The source behind it

[3. Data model](https://docs.python.org/3.12/reference/datamodel.html#object.__getitem__) defines subscription dispatch; [Built-in Functions](https://docs.python.org/3.12/library/functions.html#slice) defines slice objects.
Checked 2026-09-23; details are in the [source ledger](../../../docs/SOURCES.md).
The traces, examples, and failure demonstrations here are original teaching material.

## The mechanism

### Worked trace

Use a four-element teaching sequence [10,20,30,40]. The trace concerns dispatch and boundaries:

| Expression | Key received | Intended list-like behavior |
| --- | --- | --- |
| obj[-1] | integer -1 | normalize once to index 3, return 40 |
| obj[1:99:2] | slice(1,99,2) | clip stop to 4, select positions 1 and 3 |
| obj[::-1] | slice(None,None,-1) | positions 3,2,1,0 |
| obj[99] | integer 99 | IndexError |
| obj[::0] | slice(None,None,0) | ValueError |

For slices, slice.indices(length) yields a normalized (start,stop,step) for range(), including
reverse traversal and clipped bounds. Use range(*normalized) to enumerate positions. Do not
turn a normalized reverse stop of -1 back into an ordinary slice: normalization and applying
raw negative-index syntax are different operations.

For a scalar key, operator.index supports the integer-index protocol without silently truncating
floats. A negative index gets length added once; after that it must be in [0,length). Modulo
would wrongly turn an index that is too negative into an accepted index. Decide explicitly
whether bool keys, which act as 0/1 in built-in sequences, are appropriate for your API.

Correctness means every selected position matches the chosen contract, not merely that slices
avoid exceptions. A tuple-backed wrapper can delegate both operations, but still must document
the returned type. Indexing takes O(1) on tuple/list storage; materializing k selected elements
takes O(k) time and space. Element references are copied, not recursively cloned.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
values = [10, 20, 30, 40]
key = slice(None, None, -1)
try:
    print(key < 0)
except TypeError as exc:
    print(type(exc).__name__ + ": " + str(exc))
positions = range(*key.indices(len(values)))
fixed = [values[i] for i in positions]
print("normalized reverse:", fixed)
assert fixed == values[::-1]
try:
    slice(None, None, 0).indices(len(values))
except ValueError as exc:
    print(type(exc).__name__ + ": " + str(exc))
```

**Line by line:** Comparing a slice object with zero reproduces an integer-only implementation mistake. indices computes valid range arguments; the comprehension follows those positions. The assertion compares with a built-in sequence oracle. The final block records the actual zero-step error.

Observed author output on Python 3.12.10, 2026-09-23:

```text
TypeError: '<' not supported between instances of 'slice' and 'int'
normalized reverse: [40, 30, 20, 10]
ValueError: slice step cannot be zero
```

The deliberate failure and repaired assertions are teaching evidence, not learner progress.
Python state models do not demonstrate PostgreSQL isolation or production performance.

## In production

A database-backed container should not imply cheap random access if a slice performs a large
query. Returning a view saves copying but creates lifetime and shared-mutation questions.
For a stable snapshot API, copying references can be the clearer contract. Review errors for
wrong key type separately from out-of-range positions. Optional depth: support multidimensional
tuple keys only with an explicit indexing model; the core lab requires integers and slices.

## Check yourself

### Readiness before practice

1. How do obj[99] and obj[:99] differ?
2. What positions does slice(None,None,-2).indices(5) describe?
3. Why should int(2.9) not be the index conversion rule?
4. If a slice contains a mutable element, what can remain shared?

Run the teaching block only if you need to check your prediction. Then return to
[README.md](README.md) for the assignment, verification, and personal evidence route.
