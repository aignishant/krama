---
day: 11
part: "1.1"
title: "Preserve a wrapped function's public identity"
ids: [PY-11]
level: working
prerequisites: ["Closures", "Argument forwarding"]
failure: true
---

# Preserve a wrapped function's public identity

Core: decoration, argument forwarding, `wraps`, and `__wrapped__`. Signature inspection and
async boundaries are optional depth. No other track needs to be completed first.

## One-line answer

Use `functools.wraps` to preserve metadata and an unwrap link while the wrapper supplies behavior.

## The story

A shop adds a logging step around its receipt function. Receipts still calculate correctly,
but diagnostics call every operation `wrapper` and documentation loses the original explanation.
The replacement function changed the labels that other tools inspect.

## The idea in plain language

A decorator takes a function and returns the object that replaces its public binding.
For a forwarding decorator, the replacement wrapper calls the original function retained in a
[closure](../../day-009-frequency-ranking/lang_closure-binding/CONCEPTS.md). Correct return values
alone do not preserve the original name, docstring, annotations, or introspection path.

Metadata describes a callable; it is distinct from execution. `wraps` applies metadata copying
and sets `__wrapped__` to the wrapped callable. It does not make the two objects identical and
does not fix missing argument forwarding or a forgotten return. Recognize this need when
instrumentation, registries, documentation tools, or debugging inspect decorated functions.

## Why Krama needs it

[Configurable decorators](../../day-012-range-sums/lang_decorator-arguments/CONCEPTS.md) add one
more nesting level. Keeping the public callable understandable is necessary before adding policy.

## The source behind it

[functools — Higher-order functions and operations on callable objects](https://docs.python.org/3.12/library/functools.html#functools.wraps)
(`spec:python-3.12-functools`) documents `wraps` and `update_wrapper`.
[inspect — Inspect live objects](https://docs.python.org/3.12/library/inspect.html#inspect.signature)
(`spec:python-3.12-inspect`) documents signature unwrapping. Both checked 2026-09-22.

## The mechanism

### Worked trace

| Stage | Public binding | Retained object |
| --- | --- | --- |
| Define original | receipt → original function | Its code and metadata |
| Decorate | receipt → wrapper | Wrapper closes over original |
| Call | Wrapper receives arguments | Original receives forwarded arguments |
| Inspect | Wrapper exposes copied metadata | `__wrapped__` points to original |

`@decorate` above a definition is effectively assignment of `decorate(original)` to the name.
The decoration happens at definition time; the wrapper body runs on each later call. Forward
both positional and keyword arguments, and return the original result. A generic wrapper's
actual parameters remain `*args, **kwargs`; `inspect.signature` normally follows `__wrapped__`
to show the original signature. Setting `follow_wrapped=False` reveals the wrapper's signature.

## When it breaks

```python
from functools import wraps
from inspect import signature

def receipt(amount, *, currency="INR"):
    """Format a receipt total."""
    return f"{currency} {amount}"

def forward(function, preserve):
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    return wraps(function)(wrapper) if preserve else wrapper

plain = forward(receipt, False)
kept = forward(receipt, True)
print("names:", plain.__name__, kept.__name__)
print("doc:", kept.__doc__)
print("wrapped:", kept.__wrapped__ is receipt)
print("signatures:", signature(kept), signature(kept, follow_wrapped=False))
try:
    assert plain.__name__ == "receipt", "forwarding alone loses metadata"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert kept(12, currency="EUR") == "EUR 12"
assert kept.__doc__ == receipt.__doc__
assert kept.__wrapped__ is receipt
```

**Line by line:** `receipt` supplies a meaningful signature and docstring. The wrapper forwards
both argument channels and the result. `wraps(function)(wrapper)` is the same metadata operation
as placing `@wraps(function)` above the wrapper definition. The Boolean switch isolates its
effect. Identity checks test the unwrap link rather than confusing copied names with identical
objects. Signature inspection contrasts the advertised callable with the implementation parameters.

Author verification on Python 3.12.10, 2026-09-22:

```text
names: wrapper receipt
doc: Format a receipt total.
wrapped: True
signatures: (amount, *, currency='INR') (*args, **kwargs)
AssertionError: forwarding alone loses metadata
```

## In production

A tracing wrapper adds overhead on every call; synchronous log I/O can dominate a fast function.
Avoid recording sensitive argument values by default. Metadata copying is definition-time work,
while allocating argument containers and tracing are call-time work. Decorator stacks should
preserve one unwrap link per layer so tools can follow the chain.

This wrapper is synchronous. Wrapping a coroutine function without awaiting it only observes
coroutine creation, not completion or later exceptions. A reviewer should ask what duration and
failure the trace actually represents. Exposing `__wrapped__` also permits direct invocation of
the original; a decorator alone is not an access-control boundary.

## Check yourself

### Readiness before practice

1. Which object does the public name identify after decoration?
2. Why does `wraps` not repair a missing `return`?
3. What does `__wrapped__` point to in a stack of decorators?
4. Why can displayed and actual wrapper signatures differ?

Run the block and explain both signatures aloud. Then write [the tracing lab](README.md#assignment)
in [lab.py](lab.py), including metadata assertions and a keyword-only call.

[Navigation](README.md) · [Recall](../../../docs/LANG_RECALL.md#day-011-decorator-metadata)
