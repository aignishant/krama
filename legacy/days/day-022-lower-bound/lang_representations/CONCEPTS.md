---
day: 22
part: "3.1"
title: "Design useful object representations"
ids: [PY-22]
level: working
prerequisites: ["Objects; special methods; public versus secret fields"]
failure: true
---

# Design useful object representations

Core reading: explanation, worked trace, and readiness within the existing track cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Use repr for diagnostic identity and str for a readable label, with an explicit allowlist of safe fields.

## The story

A connection object reaches an exception message. A convenient dump of its entire attribute dictionary also exposes the credential it stores.

## The idea in plain language

The representation protocol lets tools ask an object for diagnostic or readable text.
`repr(obj)` calls its type's __repr__; `str(obj)` calls __str__ and falls back to __repr__
when no __str__ is supplied. Both methods must return strings. Container displays such as
lists use element repr, so a safe __str__ alone does not protect diagnostic output.
Treat field selection as part of the class contract. A representation can be useful without
being executable constructor syntax; secrets should not be included just to make it reconstructible.

## Why Krama needs it

This develops PY-22 in its independent track. Use the prerequisite named above;
the other two tracks are not prerequisites. The [day hub](../LESSON.md) preserves the daily budgets.

## The source behind it

[Python 3.12 representations](https://docs.python.org/3.12/reference/datamodel.html#object.__repr__) defines repr/str dispatch; field redaction is an application design decision illustrated here.
Source links checked 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
The examples and small failure models below are original teaching demonstrations.

## The mechanism

### Worked trace

Consider an endpoint with public host `api.example` and synthetic token `demo-secret`.

| Expression | Intended result | Audience |
| --- | --- | --- |
| str(endpoint) | endpoint at api.example | Human-facing label |
| repr(endpoint) | Endpoint(host='api.example', token=<redacted>) | Debugging |
| repr([endpoint]) | List containing the diagnostic representation | Debugging containers |

Select host explicitly, quote it with !r in repr so escapes are visible, and substitute a
constant redaction marker for token. This preserves diagnostic object type and destination
without retaining the secret in these output strings. Dumping __dict__ is an open-ended
policy: a new secret field would silently become visible. An allowlist stays closed when
unrelated attributes are added. Building a representation costs time and output storage
proportional to the displayed text; avoid reading remote data or formatting huge payloads.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
class UnsafeEndpoint:
    def __init__(self):
        self.host = 'api.example'
        self.token = 'demo-secret'
    def __repr__(self):
        return f'UnsafeEndpoint({self.__dict__!r})'

class Endpoint(UnsafeEndpoint):
    def __repr__(self):
        return f'Endpoint(host={self.host!r}, token=<redacted>)'
    def __str__(self):
        return f'endpoint at {self.host}'

unsafe, safe = UnsafeEndpoint(), Endpoint()
print('unsafe representation includes synthetic token:', unsafe.token in repr(unsafe))
print(str(safe))
print(repr([safe]))
for rendered in (str(safe), repr(safe), repr([safe]), f'{safe!r}'):
    assert safe.token not in rendered
assert 'api.example' in repr(safe)
```

**Line by line:** The first class deliberately dumps all attributes. The repaired class overrides diagnostic and readable forms. A list exercises repr indirectly, and the assertions check that each tested rendering excludes the synthetic token.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
unsafe representation includes synthetic token: True
endpoint at api.example
[Endpoint(host='api.example', token=<redacted>)]
```

The failing behavior is deliberate; subsequent assertions check the repair on these examples.
An executed Python model does not establish database behavior or production performance.

## In production

Use only artificial credentials in experiments. An allowlisted field is safe only under
its data contract: a host field containing a credential-bearing URL would still leak through
this example. Redacting repr does not sanitize explicit attribute logging, serialization,
traceback locals, or memory. Optional depth: truncate large public fields and test escaping
and container rendering without hiding the identity needed to debug.

## Check yourself

### Readiness before practice

1. Why can print(obj) look safe while print([obj]) leaks?
2. Why is an explicit field allowlist safer than dumping all attributes?
3. What should happen if __repr__ returns a non-string?
4. Which debugging details does your safe representation preserve?

Use [README.md](README.md) for the assignment, verification, and personal evidence route.
Reading the lesson does not complete study.
