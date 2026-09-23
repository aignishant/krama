---
day: 26
part: "3.1"
title: "Callable instances"
ids: [PY-26]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Callable instances

Core reading: intuition, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting. Record partial progress if needed.

## One-line answer

A callable instance puts persistent behavior state on an object; a closure retains state in captured bindings.

## The story

A callback remembers how many times a report was requested. After a test fails, a named calls attribute is easier to inspect than a count hidden inside a function, but it also becomes state you must manage.

## The idea in plain language

Use [nonlocal state](../../day-010-pair-sum-indices/lang_nonlocal-state/CONCEPTS.md) as the closure
prerequisite. A callable is an object used with parentheses. Defining __call__ on a class lets
its instances provide that interface. Construction configures a particular instance; later
calls can reuse and update its state. A closure achieves similar persistence by retaining
bindings from its enclosing function. Neither representation automatically grants concurrency
safety or a fresh state per request.

## Why Krama needs it

This develops PY-26 independently of the other two tracks. The [day hub](../LESSON.md)
links the separate 60/30/15-minute routes; completing the reading is not passing the assignment.

## The source behind it

[3. Data model](https://docs.python.org/3.12/reference/datamodel.html#object.__call__) covers call dispatch; [inspect — Inspect live objects](https://docs.python.org/3.12/library/inspect.html#inspect.getclosurevars) documents named closure inspection.
Checked 2026-09-23; details are in the [source ledger](../../../docs/SOURCES.md).
The traces, examples, and failure demonstrations here are original teaching material.

## The mechanism

### Worked trace

Imagine a prefix formatter with configuration prefix="job" and a counter calls=0.
Construction makes one formatter. Calling it with 7 increments calls to 1 and returns "job:7";
calling it with 8 increments the same instance to 2. A separately constructed formatter starts
at zero. Put per-instance mutable state in __init__, not in a shared class-level list.

| Concern | Callable instance | Closure |
| --- | --- | --- |
| Retained data | instance attributes | enclosing bindings |
| State inspection | named fields, optional repr | inspect.getclosurevars(function).nonlocals |
| Reset behavior | explicit method can define it | factory can create fresh state |
| Configuration changes | expose deliberately or keep internal | normally another factory call |

The choice is about ownership and discoverability, not a promise that classes are faster.
Ordinary special-method dispatch looks on the type: assigning an instance attribute named
__call__ does not by itself make a plain instance callable. Define the protocol on its class.
A callback's success still depends on its accepted arguments and current state even when
callable(obj) is true. Keep call cost separate from object construction cost.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
import inspect

class Plain:
    pass

plain = Plain()
plain.__call__ = lambda value: value * 2
try:
    plain(3)
except TypeError as exc:
    print(type(exc).__name__ + ": " + str(exc))

class Scale:
    def __init__(self, factor):
        self.factor = factor
    def __call__(self, value):
        return self.factor * value

def make_scale(factor):
    def scale(value):
        return factor * value
    return scale

obj, closure = Scale(2), make_scale(2)
assert obj(3) == closure(3) == 6
print("instance state:", vars(obj))
print("closure state:", inspect.getclosurevars(closure).nonlocals)
```

**Line by line:** Plain receives an ordinary instance attribute, exposing the special-method lookup trap. Scale defines the method on its type and stores configuration on self. The factory captures the same factor in a closure. vars and getclosurevars expose the two representations without reaching into numeric closure-cell positions. The assigned lab still asks you to implement evolving state.

Observed author output on Python 3.12.10, 2026-09-23:

```text
TypeError: 'Plain' object is not callable
instance state: {'factor': 2}
closure state: {'factor': 2}
```

The deliberate failure and repaired assertions are teaching evidence, not learner progress.
Python state models do not demonstrate PostgreSQL isolation or production performance.

## In production

Use a callable object when configuration, counters, reset, or diagnostic representation form
a coherent public interface. Prefer a closure for a small private callback whose retained state
does not need a management API. Review shared use across requests: per-instance counters can
mix tenants or make tests order-dependent. Optional depth: specify locking or task ownership
before using mutable callable state concurrently; choosing an object does not solve races.

## Check yourself

### Readiness before practice

1. Where does each representation retain its configuration?
2. Why does assigning plain.__call__ fail to change plain(3)?
3. What assertion would catch state shared by two separately constructed callables?
4. What does a reset operation mean for callbacks already holding the object?

Run the teaching block only if you need to check your prediction. Then return to
[README.md](README.md) for the assignment, verification, and personal evidence route.
