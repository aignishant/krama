---
day: 30
part: "3.1"
title: "Properties"
ids: [PY-30]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Properties

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

A property preserves attribute syntax while routing reads and writes through explicit behavior.

## The story

A retry count used to be a public field. After validation is added, existing callers should still write config.retries=3 and get a clear error for a negative value.

## The idea in plain language

Prerequisite: [attribute lookup](../../day-029-stable-record-sorting/lang_attribute-lookup/CONCEPTS.md). A property is a class-level managed
attribute whose getter serves reads and whose setter handles assignments. Store the actual
value under a different backing name such as _retries. Validation must happen before replacing
the backing value so a rejected write leaves the object valid. External syntax compatibility
does not mean every old value remains acceptable; tighter validation changes behavior.

## Why Krama needs it

This develops PY-30. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Descriptor Guide](https://docs.python.org/3.12/howto/descriptor.html) describes attribute precedence and method binding.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

For a Config starting at retries=2, initialization assigns through the property, so it uses
the same validation as later writes. Reading config.retries calls the getter and returns
_retries. Writing 4 validates then stores 4. Writing -1 raises ValueError and keeps 4.

The dangerous setter self.retries=value invokes itself recursively. Using self._retries=value
changes a separate ordinary attribute and avoids that loop. A getter-only property rejects
assignment; an instance dictionary entry with the public name cannot shadow a property under
normal lookup because the property participates as a data descriptor.

Choose a domain contract, not a vague check. This example accepts nonnegative integers and
rejects bool even though bool is a subclass of int. It deliberately uses type(value) is int;
an API allowing integer subclasses would need a different validation rule. Getter/setter
dispatch adds behavior to a familiar-looking expression. Cost is that behavior's cost, so a
property that performs remote I/O is not a cheap field merely because its syntax is short.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
class Config:
    def __init__(self, retries):
        self.retries = retries
    @property
    def retries(self):
        return self._retries
    @retries.setter
    def retries(self, value):
        if type(value) is not int or value < 0:
            raise ValueError('retries must be a nonnegative integer')
        self._retries = value

c = Config(2)
c.retries = 4
try:
    c.retries = -1
except ValueError as exc:
    print(type(exc).__name__ + ': ' + str(exc))
assert c.retries == 4
c.__dict__['retries'] = -9
print('public read:', c.retries, 'dictionary shadow:', c.__dict__['retries'])
assert c.retries == 4
```

**Line by line:** Initialization and subsequent writes share the setter. Validation precedes mutation, preserving 4 after failure. Injecting a same-name dictionary entry demonstrates property precedence rather than changing the backing _retries.

Observed author output on Python 3.12.10, 2026-09-23:

```text
ValueError: retries must be a nonnegative integer
public read: 4 dictionary shadow: -9
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Preserve documented exceptions and avoid hidden expensive work in properties. Validation
does not create a security boundary against code that directly changes private state. If
multiple fields must change atomically, a method with a transaction-like contract is clearer
than unrelated setters. A reviewer should check that constructor and update paths enforce
the same invariant. Optional follow-up: how should serialization handle backing fields?

## Check yourself

### Readiness before practice

1. Why does the backing name differ from the public name?
2. What should remain true after a rejected write?
3. Why does the injected dictionary entry not win?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
