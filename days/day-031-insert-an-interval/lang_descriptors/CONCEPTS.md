---
day: 31
part: "3.1"
title: "Descriptors"
ids: [PY-31]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Descriptors

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

A data descriptor centralizes managed-field rules while storing each owner instance’s value separately.

## The story

Two fields reuse the same validator idea, but one user’s new value appears on another user. The validator stored state on itself, which is shared by all instances.

## The idea in plain language

Prerequisites: [lookup](../../day-029-stable-record-sorting/lang_attribute-lookup/CONCEPTS.md) and [properties](../../day-030-merge-overlapping-intervals/lang_properties/CONCEPTS.md). A descriptor
is an object installed on a class that defines access hooks. __get__ handles retrieval;
__set__ handles assignment; __set_name__ learns the owner and assigned name during class
creation. A descriptor with __set__ or __delete__ is a data descriptor. With __get__, it can
override a same-name instance dictionary entry. A descriptor with only __get__ is non-data
and can be shadowed by the instance dictionary.

## Why Krama needs it

This develops PY-31. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Descriptor Guide](https://docs.python.org/3.12/howto/descriptor.html) describes attribute precedence and method binding.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

For class Meter with level=Nonnegative(), one descriptor object belongs to Meter. During
class creation it records a backing name _level. Assignment m.level=5 calls
descriptor.__set__(m,5), validates 5, then stores m.__dict__['_level']=5. Reading m.level calls
__get__(m,Meter) and retrieves that per-instance value. Reading Meter.level passes obj=None;
returning the descriptor itself makes class-level introspection useful.

Compare two precedence paths:

| Class attribute | Instance contains public name | Normal read |
| --- | --- | --- |
| __get__ only | yes | instance entry |
| __get__ and __set__ | yes | descriptor __get__ |

The backing name prevents recursive writes through the descriptor and allows a descriptor
class to serve several fields. Each assigned field needs its own descriptor instance unless
the implementation explicitly supports reuse under multiple names. The dictionary-based
version below requires owner instances with __dict__; a purely slotted owner needs a different
storage strategy. Validation code and storage operations determine cost; the protocol does
not make arbitrary getters constant-time.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
class Nonnegative:
    def __set_name__(self, owner, name):
        self.storage = '_' + name
    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return obj.__dict__[self.storage]
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError('negative level')
        obj.__dict__[self.storage] = value

class Meter:
    level = Nonnegative()

a, b = Meter(), Meter()
a.level, b.level = 2, 8
a.__dict__['level'] = -1
print('independent managed values:', a.level, b.level)
assert (a.level, b.level) == (2, 8)
try:
    a.level = -4
except ValueError as exc:
    print(type(exc).__name__ + ': ' + str(exc))
assert a.level == 2
assert Meter.level is Meter.__dict__['level']
class NonData:
    def __get__(self, obj, owner=None):
        return 99
class Plain:
    level = NonData()
p = Plain()
p.level = 7
print('non-data shadow:', p.level)
assert p.level == 7
```

**Line by line:** __set_name__ chooses private storage once. __set__ writes to the owner instance, not the shared descriptor. The injected public entry loses to the data descriptor, while Plain.level permits shadowing because NonData has no setter. The failed assignment leaves a’s value unchanged.

Observed author output on Python 3.12.10, 2026-09-23:

```text
independent managed values: 2 8
ValueError: negative level
non-data shadow: 7
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Descriptors are useful for repeated validation or field mappings; a single managed field
may be clearer as a property. Avoid retaining owner objects in a global descriptor dictionary
without a lifetime policy. Frameworks that add descriptors after class creation must arrange
name initialization explicitly. A reviewer should request tests using two instances and two
different managed fields, not just repeated access to one object.

## Check yourself

### Readiness before practice

1. Where should per-instance values live?
2. What argument distinguishes class access from instance access?
3. Which hook changes precedence?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
