---
day: 36
part: "3.1"
title: "Dataclass defaults"
ids: [PY-36]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Dataclass defaults

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Use a default factory that creates a fresh mutable object for each dataclass instance.

## The story

Two work batches start empty, but adding a job to one unexpectedly fills the other. The factory was called twice but returned the same global list.

## The idea in plain language

Recall [mutable defaults](../../day-003-stable-compaction/lang_mutable-defaults/CONCEPTS.md) and [attribute ownership](../../day-029-stable-record-sorting/lang_attribute-lookup/CONCEPTS.md).
A dataclass generates methods such as __init__ from declared fields. A default is a value
reused when an argument is omitted; default_factory is a zero-argument callable invoked to
supply a missing value. Freshness depends on what it returns. list creates a new list each
time, while lambda: shared returns the same list on every call.

## Why Krama needs it

This develops PY-36. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[dataclasses — Data Classes](https://docs.python.org/3.12/library/dataclasses.html) documents field factories and mutable-default checks.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

For @dataclass Batch with jobs=field(default_factory=list), generated initialization calls
list() when jobs is omitted. Construct a and b with no argument: each call creates a separate
empty list. Appending to a.jobs leaves b.jobs empty. If a caller explicitly passes jobs=shared,
the factory is bypassed and that supplied object is stored under the usual generated initializer.
The factory is not a defensive copy policy.

Python 3.12 rejects unhashable field defaults such as a literal list at dataclass creation.
That catches a common mistake, not every possible mutable shared object. A factory that returns
a global mutable object passes that check but still aliases. frozen=True restricts field
assignment; it does not deeply freeze the list stored in a field. Type annotations describe
intended types but do not by themselves validate runtime values.

Creating an empty list is constant-sized work in this example; a factory loading data can be
expensive or fail. Treat factories as initialization logic with ordinary ownership and failure
contracts. Equality of two empty fields proves equal content, not separate identity.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
from dataclasses import dataclass, field
try:
    @dataclass
    class Rejected:
        jobs: list = []
except ValueError as exc:
    print(type(exc).__name__ + ': ' + str(exc))
shared = []
@dataclass
class BadFactory:
    jobs: list = field(default_factory=lambda: shared)
x, y = BadFactory(), BadFactory()
x.jobs.append('leak')
print('bad factory second:', y.jobs)
assert x.jobs is y.jobs
@dataclass
class Batch:
    jobs: list = field(default_factory=list)
a, b = Batch(), Batch()
a.jobs.append('own')
print('fresh fields:', a.jobs, b.jobs)
assert a.jobs is not b.jobs and b.jobs == []
explicit = Batch(jobs=shared)
assert explicit.jobs is shared
```

**Line by line:** The first class definition captures the runtime rejection. BadFactory demonstrates that a callable can still return shared state. Batch uses list itself as the factory, allocating fresh storage. Explicitly supplying shared shows the boundary of the factory guarantee.

Observed author output on Python 3.12.10, 2026-09-23:

```text
ValueError: mutable default <class 'list'> for field jobs is not allowed: use default_factory
bad factory second: ['leak']
fresh fields: ['own'] []
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Use default_factory for nested containers as well, and inspect whether their contents need
copying. Resource-opening factories complicate cleanup and can be better expressed through
explicit lifecycle methods. A reviewer should require two-instance mutation tests for
ownership-sensitive fields. Optional follow-up: why does a frozen dataclass containing a list
still permit appending to that list?

## Check yourself

### Readiness before practice

1. Why is default_factory=list different from default_factory=list()?
2. Can a factory still share state?
3. What happens when the caller supplies an explicit list?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
