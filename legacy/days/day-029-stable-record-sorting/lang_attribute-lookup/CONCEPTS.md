---
day: 29
part: "3.1"
title: "Attribute lookup"
ids: [PY-29]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Attribute lookup

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

An ordinary instance attribute shadows a class attribute; mutating a shared class object does not create an instance attribute.

## The story

Changing one worker’s queue unexpectedly changes another worker’s queue. Both names still refer to the same list stored on their class.

## The idea in plain language

Recall [identity and equality](../../day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md) and [mutation contracts](../../day-006-best-single-trade/lang_mutation-contracts/CONCEPTS.md).
An attribute is a name resolved through an object and its type. For ordinary attributes,
an instance dictionary can supply a per-instance value; otherwise lookup can find the class
value along the method resolution order (MRO), the ordered sequence of classes to search.
Assignment and mutation are different: w.queue=[] assigns a new instance attribute, while
w.queue.append(x) first retrieves an object and then changes that object.

## Why Krama needs it

This develops PY-29. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Data model](https://docs.python.org/3.12/reference/datamodel.html) defines attribute access and slots.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Start with class Worker.queue=[] and two instances a and b whose dictionaries are empty.
Reading a.queue falls through to Worker.queue. Appending a job changes that shared list, so
b sees it too. Assigning a.queue=[] adds a dictionary entry only to a. Now a.queue resolves
locally, while b.queue still finds the class list. Deleting a.queue removes the shadow and
reveals the class value again; it does not delete Worker.queue.

That simple order has an important boundary: under default object attribute lookup, a data
descriptor found on the class takes precedence over the instance dictionary. A descriptor
is an object implementing hooks for managed attribute access. Properties and validators are
examples studied on Days 30–31. After data descriptors, instance entries precede non-data
descriptors and ordinary class values. __getattr__ is a fallback for missing attributes;
overriding __getattribute__ can change the normal machinery.

The useful retained state is the class dictionary plus each instance's own dictionary and
MRO. Lookup does not copy inherited mutable objects. Correct reasoning names the object being
mutated, not merely the spelling of the attribute. Dictionary storage grows with per-instance
attributes; exact lookup speed depends on the interpreter, caches, and invoked descriptor code.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
class Worker:
    queue = []

a, b = Worker(), Worker()
a.queue.append('job')
print('shared:', a.queue is b.queue, b.queue)
assert b.queue == ['job']
a.queue = []
print('shadowed:', a.queue, b.queue)
assert a.queue is not b.queue
del a.queue
print('revealed:', a.queue)
assert a.queue is Worker.queue
```

**Line by line:** The append mutates the class list reached through a. Assignment installs a local shadow. Deletion removes that shadow, making lookup fall back again; identity assertions distinguish shared storage from merely equal content.

Observed author output on Python 3.12.10, 2026-09-23:

```text
shared: True ['job']
shadowed: [] ['job']
revealed: ['job']
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Initialize mutable per-instance state in __init__ or a suitable dataclass factory. Class
attributes are useful for deliberately shared configuration, but mutation then needs an
ownership policy. A reviewer should ask whether tests create fresh classes or accidentally
reuse shared state between cases. Optional depth: inspect vars(instance), vars(type(instance)),
and type(instance).__mro__ before overriding any attribute hook.

## Check yourself

### Readiness before practice

1. Why does append affect b but assignment not affect b?
2. What does deleting a shadow reveal?
3. Which mechanism can outrank the instance dictionary?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
