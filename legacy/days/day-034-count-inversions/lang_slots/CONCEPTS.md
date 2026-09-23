---
day: 34
part: "3.1"
title: "Slots"
ids: [PY-34]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Slots

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Slots can remove per-instance dictionaries, but inheritance and measurement determine the actual storage benefit.

## The story

A service has many tiny records. A developer adds slots and announces a fixed percentage saving without measuring the records or noticing a subclass regained a dictionary.

## The idea in plain language

Prerequisites: [attribute storage](../../day-029-stable-record-sorting/lang_attribute-lookup/CONCEPTS.md) and [inheritance](../../day-033-kth-smallest/lang_inheritance-and-super/CONCEPTS.md).
__slots__ declares permitted storage names for instances and creates corresponding class
descriptors. A directly slotted class without a dictionary-providing base normally has no
instance __dict__. This restricts adding arbitrary fields; it does not make stored values
immutable or automatically remove dictionaries inherited from another class.

## Why Krama needs it

This develops PY-34. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Data model](https://docs.python.org/3.12/reference/datamodel.html) defines attribute access and slots. [sys.getsizeof](https://docs.python.org/3.12/library/sys.html#sys.getsizeof) defines the shallow measurement boundary.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Compare Plain with an ordinary attribute x and Slotted with __slots__=('x',). Both can
assign x. Plain can add typo=1; Slotted rejects that unlisted field. A subclass of Slotted
without its own slots gains a dictionary; __slots__=() on a subclass avoids adding one, but
does not erase a dictionary already supplied by a base. Weak-reference support is also a
separate requirement, commonly needing __weakref__ when not inherited.

Use a stated measurement boundary. sys.getsizeof(instance) is shallow: for Plain it does
not include the separate instance dictionary. Adding getsizeof(instance.__dict__) gives a
limited object-plus-dictionary comparison, still excluding referenced payloads and allocator
effects. Shared-key dictionaries, number of instances, interpreter version, and inheritance
affect results. The demonstration measures one pair after assignment and labels that scope.
It does not assert a universal byte difference or an application-wide saving. For a real
decision measure representative populations and lifecycle allocation with appropriate tooling.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
import sys
class Plain:
    pass
class Slotted:
    __slots__ = ('x',)
class Child(Slotted):
    pass
p, s = Plain(), Slotted()
p.x = s.x = 1
print('instance dictionaries:', hasattr(p, '__dict__'), hasattr(s, '__dict__'))
assert hasattr(p, '__dict__') and not hasattr(s, '__dict__')
try:
    s.typo = 2
except AttributeError as exc:
    print(type(exc).__name__ + ': ' + str(exc))
print('shallow bytes, ordinary/slotted:', sys.getsizeof(p), sys.getsizeof(s))
print('ordinary plus dict bytes:', sys.getsizeof(p) + sys.getsizeof(p.__dict__))
print('subclass dictionary:', hasattr(Child(), '__dict__'))
assert hasattr(Child(), '__dict__')
```

**Line by line:** The presence checks establish structure independently of byte counts. The rejected typo shows the behavior change. getsizeof observations are shallow and specific to this run. Child intentionally omits slots, exposing the inheritance trap.

Observed author output on Python 3.12.10, 2026-09-23:

```text
instance dictionaries: True False
AttributeError: 'Slotted' object has no attribute 'typo'
shallow bytes, ordinary/slotted: 48 40
ordinary plus dict bytes: 344
subclass dictionary: True
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Use slots when a stable shape and measured population cost justify the restriction. They
can interfere with frameworks expecting dynamic attributes or dictionaries. Do not redeclare
an inherited slot name. A reviewer should ask for representative memory observations and
serialization, weak-reference, and subclass compatibility checks. Optional depth: compare a
large retained population, recording what the measurement includes and excludes.

## Check yourself

### Readiness before practice

1. Why is comparing only two instance getsizeof calls incomplete?
2. How can a subclass regain __dict__?
3. Does slots make x immutable?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
