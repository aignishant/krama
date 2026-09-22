---
day: 16
part: "3.1"
title: "Generator bodies run when requested"
ids: [PY-16]
level: working
prerequisites: ["Day 15 iterator protocol", "Function calls"]
failure: true
---

# Generator bodies run when requested

Core: explanation, worked trace, and readiness. Production extensions are optional depth;
continue another sitting if needed within the existing track budget.

## One-line answer

Calling a generator function creates a suspended iterator; advancing it executes the body only until the next yield.

## The story

A job reports that it created a reader, yet no file was opened and no validation ran. The reader is a generator whose body has not been asked for a value.

## The idea in plain language

A generator function contains yield. Calling it binds arguments and returns a generator
object, but its body starts on first advancement. Yield sends one value to the consumer and
suspends the frame with its local state. A later next resumes immediately after that yield.
Return or reaching the end exhausts it. The [iterator protocol](../../day-015-sorted-pair-existence/lang_iterator-protocol/CONCEPTS.md)
explains why it is single-pass. Laziness defers work and exceptions; it does not eliminate them.
Argument expressions at the call site still run immediately.

## Why Krama needs it

The next Python sessions build on the distinction between producing an iterator and advancing its suspended body; use the [day map](../../../docs/00_MASTER_PLAN.md) to continue in order.

## The source behind it

[Expressions — Yield expressions](https://docs.python.org/3.12/reference/expressions.html#yield-expressions), Python 3.12, documents suspension and resumption. Checked 2026-09-22; see the dated [source ledger](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

Creation saves arguments but runs no body statement. The first next enters the body,
performs work before yield, and returns its value. The consumer now controls when execution
continues. A second next can do more work or raise a deferred error. An error escaping the
body ends the generator. Incremental consumption can avoid storing every result; total work
still depends on how many values are requested, and retained locals can be large.

## When it breaks

```python
events = []
def records():
    events.append("start")
    yield "first"
    events.append("resume")
    raise ValueError("bad second record")
stream = records()
print("created:", events)
print("next:", next(stream), events)
try:
    next(stream)
except ValueError as error:
    print(f"ValueError: {error}")
print("after error:", events)
assert next(stream, "exhausted") == "exhausted"
```

**Line by line:** Calling records creates stream without appending. The first next runs to yield and saves the frame. The second next resumes, appends, and raises the actual error. The final assertion checks that an exception escaping the body terminates traversal.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
created: []
next: first ['start']
ValueError: bad second record
after error: ['start', 'resume']
```

## In production

Place error handling around consumption when errors can be deferred. A generator expression evaluates its outermost iterable expression immediately, so do not generalize “nothing runs” to every expression involved. For eager input validation, use an ordinary factory that validates then returns an inner generator. Resource cleanup after partial consumption needs explicit ownership; a suspended generator can retain open resources and large locals.

## Check yourself

### Readiness before practice

1. Which events exist after creation and after first next?
2. Why would try around creation miss the deferred error?
3. Can a function argument expression run before first iteration?
4. Why does laziness not guarantee O(1) total memory?

Run the teaching block in a scratch interpreter, then explain the distinguishing failure aloud.
Use [README.md](README.md) to enter the assignment and record your own evidence.
