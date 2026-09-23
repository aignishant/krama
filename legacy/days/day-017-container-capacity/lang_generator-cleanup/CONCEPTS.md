---
day: 17
part: "3.1"
title: "Own cleanup after partial iteration"
ids: [PY-17]
level: working
prerequisites: ["Day 16 generator suspension; try/finally"]
failure: true
---

# Own cleanup after partial iteration

Core reading: explanation, worked trace, and readiness. The production section offers optional
depth for another sitting; keep the existing track budget and record partial work honestly.

## One-line answer

A suspended generator keeps its resources; the consumer that stops early must arrange explicit closure.

## The story

A report reads one row and stops. The reader is still referenced in a variable, so its
finally block has not run and its resource is still held. The loop ended; the generator did not.

## The idea in plain language

Start with [Day 16 suspension](../../day-016-unique-triples/lang_generator-laziness/CONCEPTS.md).
Yield preserves the active try block and local state. A for-loop break changes the consumer's
control flow; it does not call close on an arbitrary iterator. Exhaustion, an escaping exception,
or explicit generator closure can unwind an entered finally block.

The useful ownership rule is: acquire inside the generator's protected lifetime, and let the
consumer guarantee close when it stops early. Use try/finally around consumption, or
contextlib.closing for an object exposing close. A finally inside a never-started generator
has never been entered, so closing it cannot clean up a resource acquired elsewhere.

## Why Krama needs it

This develops PY-17 for the [Week 3 review](../../day-021-week-3-review/LESSON.md).
The tracks remain independent; use only this subject's prerequisites.

## The source behind it

[Python 3.12 generator methods](https://docs.python.org/3.12/reference/expressions.html#generator-iterator-methods)
defines close; [contextlib.closing](https://docs.python.org/3.12/library/contextlib.html#contextlib.closing)
provides a consumer-side context manager. Checked 2026-09-22; details are in the [source ledger](../../../docs/SOURCES.md).
The trace and counterexample below are original teaching examples.

## The mechanism

### Worked trace

The important states are:

| Action | Generator state | Cleanup |
| --- | --- | --- |
| Call reader() | Created, body not entered | Nothing acquired inside it |
| next(reader) | Suspended at first yield inside try | Resource retained |
| Consumer break | Still suspended | No automatic close from break |
| reader.close() | Unwinds entered frame | finally runs |
| Another close() | Already closed | No second cleanup |

In Python 3.12 close injects GeneratorExit at the suspension point. Normal unwinding executes
finally; do not yield another value during that cleanup. A yield during closure raises
RuntimeError. Other cleanup errors can propagate to the consumer, so cleanup is observable
work, not an infallible signal. Let GeneratorExit propagate rather than catching it broadly.

The model below uses an event list in place of a real resource. Holding the generator in a
variable makes the partial-consumption failure deterministic without relying on garbage
collection timing. The event count lets us verify that cleanup happens exactly once in this
example. Resource retention follows live frames, not the number of yielded items.

## When it breaks

Run this separate teaching demonstration before implementing your own exercise.

```python
events = []
def reader():
    events.append("acquire")
    try:
        yield "row"
        yield "later"
    finally:
        events.append("release")

stream = reader()
for row in stream:
    print("read:", row)
    break
print("after break:", events)
try:
    assert events == ["acquire", "release"], "break did not close the generator"
except AssertionError as error:
    print(f"AssertionError: {error}")
finally:
    stream.close()
stream.close()
print("after explicit close:", events)
assert events == ["acquire", "release"]
never_started = reader()
never_started.close()
assert events == ["acquire", "release"]
```

**Line by line:** reader records acquisition only when first advanced. break leaves stream referenced and
suspended. The deliberately failed assertion exposes the missing cleanup. The consumer's
finally closes stream, and the repeated close proves no duplicate release. Closing an unstarted
reader adds no events because none of its body has executed.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
read: row
after break: ['acquire']
AssertionError: break did not close the generator
after explicit close: ['acquire', 'release']
```

**Line by line:** These are the actual printed observations, including the deliberately caught
assertion or exception. A caught failure documents the wrong assumption; later assertions check
the repair on the stated example, not on every possible input.

## In production

Use with around real file ownership and contextlib.closing around partial generator
consumption when appropriate. Place consumer code inside that scope so exceptions also close
the reader. Ordinary iterator wrappers do not universally forward close to their inputs;
close the actual resource owner. CPython reference counting can hide missing ownership in a
small demo, and other runtimes or reference cycles can defer finalization. Neither finally nor
close guarantees recovery from a process being forcibly terminated. Measure file descriptors
or checked-out connections when diagnosing resource retention.

## Check yourself

### Readiness before practice

1. Why does break leave the generator's finally pending?
2. Who should guarantee cleanup if processing the first row raises?
3. What happens when close is called before the first next?
4. Why should cleanup avoid yielding another item?

Use [README.md](README.md) for the assignment and evidence route. Reading does not complete study.
