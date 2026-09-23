---
day: 18
part: "3.1"
title: "Delegate values and capture a final result"
ids: [PY-18]
level: working
prerequisites: ["Day 16 yield; Day 17 closure; StopIteration"]
failure: true
---

# Delegate values and capture a final result

Core reading: explanation, worked trace, and readiness. The production section offers optional
depth for another sitting; keep the existing track budget and record partial work honestly.

## One-line answer

yield from forwards iteration to a child and evaluates to the child's return value when that child finishes.

## The story

A parser emits records one at a time and returns a final record count. A wrapper forwards
the records with a for loop, then discovers that the count never appeared among them.

## The idea in plain language

A child generator has two output channels: yield produces stream items; return value
finishes it with StopIteration.value. An ordinary for loop consumes that termination signal
without exposing the value. The expression result = yield from child() forwards the stream
and binds the terminal value to result in the parent.

This builds on [generator suspension](../../day-016-unique-triples/lang_generator-laziness/CONCEPTS.md).
The parent remains suspended while the child yields. Calling list(parent) collects only
items that reach the consumer through yield; a child return is not automatically such an item.
The parent may deliberately yield or otherwise use the captured result.

## Why Krama needs it

This develops PY-18 for the [Week 3 review](../../day-021-week-3-review/LESSON.md).
The tracks remain independent; use only this subject's prerequisites.

## The source behind it

[PEP 380 — Syntax for Delegating to a Subgenerator](https://peps.python.org/pep-0380/)
specifies delegated iteration and the terminal return value. The examples target Python 3.12. Checked 2026-09-22; details are in the [source ledger](../../../docs/SOURCES.md).
The trace and counterexample below are original teaching examples.

## The mechanism

### Worked trace

Let child yield "row" and then return 7. The number 7 is an arbitrary completion marker,
not a measured row count. The caller advances parent, which advances child and receives "row".
The next advancement resumes child; its return completes delegation, binds result=7, and
allows parent to continue. If parent now yields ("result", result), the caller sees that tuple
because of an explicit parent yield, not because returns normally appear in iteration.

| Child action | Plain forwarding loop | yield from expression |
| --- | --- | --- |
| yield "row" | Emits row | Emits row |
| return 7 | Ends loop, value discarded | Expression becomes 7 |
| raise ValueError | Exception propagates unless handled | Exception propagates unless handled |

For plain next-driven consumption, a forwarding loop resembles delegation only while values
are being yielded. Delegation also forwards send/throw interactions and closure to a compatible
delegate. Closing a suspended delegating generator closes a delegate with close; this matters
for Day 17 resource ownership. Capturing the final value requires normal completion: early
closure does not execute the parent's normal post-delegation code as if the child had returned.
Work is proportional to consumed items plus each generator's own computation; nested frames
use memory proportional to active delegation depth, not necessarily constant space.

## When it breaks

Run this separate teaching demonstration before implementing your own exercise.

```python
def child():
    yield "row"
    return 7

def forwarding_loop():
    for item in child():
        yield item

def delegating():
    result = yield from child()
    yield ("result", result)

plain = list(forwarding_loop())
delegated = list(delegating())
print("loop:", plain)
print("delegation:", delegated)
try:
    assert plain == delegated, "for-loop forwarding discarded the return value"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert delegated == ["row", ("result", 7)]
cursor = child()
assert next(cursor) == "row"
try:
    next(cursor)
except StopIteration as stop:
    print("terminal value:", stop.value)
    assert stop.value == 7
```

**Line by line:** child separates an emitted row from a terminal marker. The plain wrapper loses the
terminal value; the delegating wrapper explicitly emits it in a tagged tuple. Direct next calls
then reveal StopIteration.value, independently confirming where the marker travels.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
loop: ['row']
delegation: ['row', ('result', 7)]
AssertionError: for-loop forwarding discarded the return value
terminal value: 7
```

**Line by line:** These are the actual printed observations, including the deliberately caught
assertion or exception. A caught failure documents the wrong assumption; later assertions check
the repair on the stated example, not on every possible input.

## In production

Use tagged records or a separate result API if mixing data and summaries would confuse
callers. Explicit return is the way to finish a generator with a value; manually raising
StopIteration in its body is not an interchangeable technique in modern Python. A subgenerator
shared with another consumer may be unexpectedly closed by its delegating owner, so ownership
must be clear. yield from is not await and does not make synchronous I/O asynchronous.

## Check yourself

### Readiness before practice

1. Which part of the example causes the final tuple to become a stream item?
2. What does list(child()) contain, and where did 7 go?
3. What changes if the consumer closes the parent after the first item?
4. Why is a plain forwarding loop not a complete substitute for delegation?

Use [README.md](README.md) for the assignment and evidence route. Reading does not complete study.
