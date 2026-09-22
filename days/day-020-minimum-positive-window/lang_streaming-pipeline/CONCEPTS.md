---
day: 20
part: "3.1"
title: "Keep every stage of a pipeline incremental"
ids: [PY-20]
level: working
prerequisites: ["Days 16–19 laziness, cleanup, consumption"]
failure: true
---

# Keep every stage of a pipeline incremental

Core reading: explanation, worked trace, and readiness. The production section offers optional
depth for another sitting; keep the existing track budget and record partial work honestly.

## One-line answer

Compose lazy stages and verify how far the source advances; one eager stage can materialize the entire input.

## The story

A preview needs one accepted row from a large feed. The final object is a generator, yet
creating it scans the entire feed because an earlier transformation returned a list.

## The idea in plain language

A pull pipeline lets the final consumer request one item, which requests enough upstream
items to produce it. A filter may skip several inputs for one output; a mapping transforms each
accepted input. A generator at the end does not make earlier list comprehensions lazy.

Use [Day 16 execution timing](../../day-016-unique-triples/lang_generator-laziness/CONCEPTS.md)
and [Day 19 consumption](../../day-019-longest-distinct-substring/lang_iterator-consumption/CONCEPTS.md)
to inspect the entire path: source, transforms, and sink. A sink that retains every result still
uses O(n) space. Streaming is an end-to-end resource claim, not a syntax property.

## Why Krama needs it

This develops PY-20 for the [Week 3 review](../../day-021-week-3-review/LESSON.md).
The tracks remain independent; use only this subject's prerequisites.

## The source behind it

[Python 3.12 generator expressions](https://docs.python.org/3.12/reference/expressions.html#generator-expressions)
specifies lazy body evaluation and immediate evaluation of the outer iterable expression.
[itertools](https://docs.python.org/3.12/library/itertools.html) provides composable iterator tools. Checked 2026-09-22; details are in the [source ledger](../../../docs/SOURCES.md).
The trace and counterexample below are original teaching examples.

## The mechanism

### Worked trace

The example source emits integers 0 through 5. A filter keeps odd values; a mapping multiplies
them by ten. Creating the pipeline should pull no integers. Requesting one result pulls 0,
rejects it, pulls 1, accepts it, and emits 10. The next request pulls 2 then 3 and emits 30.

| Consumer action | New source values read | Output |
| --- | --- | --- |
| Build lazy stages | none | none |
| First next | 0, 1 | 10 |
| Second next | 2, 3 | 30 |

Our source function only creates a generator on call; it acquires no eager resource. This is
why construction has no pulls in this example. A generator expression still evaluates its
outermost iterable expression immediately, so an eager source factory could do work then.

Correctness composes: the filter preserves the relative order of qualifying values, and the
mapping applies the same transformation to each retained value without adding or dropping
items. For N source items and constant-cost stages, complete traversal takes O(N). A bounded
number of scalar locals per stage needs O(1) auxiliary storage, assuming the source and sink
also retain bounded data. One output can still take arbitrarily long if few inputs qualify;
an infinite source with no matches may never yield. Laziness does not promise low latency.

## When it breaks

Run this separate teaching demonstration before implementing your own exercise.

```python
pulls = []
def source():
    for value in range(6):
        pulls.append(value)
        yield value

eager = [value for value in source() if value % 2]
wrapped = (value * 10 for value in eager)
print("eager construction pulls:", pulls)
try:
    assert pulls == [], "an earlier list stage already consumed the source"
except AssertionError as error:
    print(f"AssertionError: {error}")
wrapped.close()
pulls.clear()
raw = source()
filtered = (value for value in raw if value % 2)
mapped = (value * 10 for value in filtered)
try:
    print("lazy construction pulls:", pulls)
    assert pulls == []
    first = next(mapped)
    print("first output:", first, "pulls:", pulls)
    assert first == 10 and pulls == [0, 1]
    assert next(mapped) == 30 and pulls == [0, 1, 2, 3]
finally:
    mapped.close()
    filtered.close()
    raw.close()
```

**Line by line:** The first list comprehension exposes hidden eager consumption. Wrapping its result in
a generator cannot undo that work. The repaired filter and map are both generators; the pull
log measures source advancement rather than guessing from their types. The final block closes
each owned generator explicitly because these expression wrappers do not promise to close upstream.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
eager construction pulls: [0, 1, 2, 3, 4, 5]
AssertionError: an earlier list stage already consumed the source
lazy construction pulls: []
first output: 10 pulls: [0, 1]
```

**Line by line:** These are the actual printed observations, including the deliberately caught
assertion or exception. A caught failure documents the wrong assumption; later assertions check
the repair on the stated example, not on every possible input.

## In production

For real records, bound record size and batch size, keep resource ownership around the
whole consumption scope, and place error handling around next or the consumer loop. Exceptions
inside transformations are deferred until that item is requested. Sorting, global grouping,
unbounded caches, and accumulating all output can require materialization. An application
queue can add buffering beyond the simple synchronous pull model shown here. Prefer counters
over an ever-growing debug list when measuring a large pipeline; our pull log is deliberately tiny.

## Check yourself

### Readiness before practice

1. Why does a generator wrapped around a list fail the construction-time check?
2. How many source items are needed for the first output here?
3. What assumptions make O(1) auxiliary memory a valid claim?
4. Who closes a resource-owning source when the preview stops after one result?

Use [README.md](README.md) for the assignment and evidence route. Reading does not complete study.
