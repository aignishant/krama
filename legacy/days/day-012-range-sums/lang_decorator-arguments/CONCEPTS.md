---
day: 12
part: "1.1"
title: "Separate decorator configuration from each call"
ids: [PY-12]
level: working
prerequisites: ["Decorator metadata", "Closure binding"]
failure: true
---

# Separate decorator configuration from each call

Core: the three call stages, validation boundaries, and exception preservation. General signature
binding and async decorators are optional depth; the demonstration explicitly accepts one integer.

## One-line answer

A decorator factory captures configuration, its decorator captures the function, and its wrapper handles each invocation.

## The story

A shop gives each checkout a configured maximum receipt size. That limit belongs to the checkout;
the amount changes for every customer. A broken receipt printer must still report its own failure
instead of being disguised as an invalid purchase.

## The idea in plain language

A configurable decorator adds an outer function around [yesterday's decorator](../../day-011-group-anagrams/lang_decorator-metadata/CONCEPTS.md).
The factory is called with policy, then its returned decorator is called with the function,
then its returned wrapper is called with ordinary arguments. These are three different inputs
and lifetimes. Configuration errors should be found when configuration is supplied; argument
validation happens per call; failures inside valid business work must remain observable.

Recognize this pattern when several functions need the same kind of guard with different fixed
settings. Avoid a catch-all handler that returns an ordinary value on failure: it changes a failed
operation into apparent success and can hide bugs in the wrapped function.

## Why Krama needs it

[Exception boundaries](../../day-058-level-order/lang_exception-boundaries/README.md) later
formalizes where exceptions should be handled. Here the boundary is already visible: a validation
wrapper owns validation, while the original callable owns its execution errors.

## The source behind it

[8. Compound statements](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
(`spec:python-3.12-compound-statements`, checked 2026-09-22) specifies decorator application.
Reuse [Day 11's metadata explanation](../../day-011-group-anagrams/lang_decorator-metadata/CONCEPTS.md)
for `functools.wraps` rather than treating each nesting level as a new API.

## The mechanism

### Worked trace

| Stage | Example input | Returned object | Work performed |
| --- | --- | --- | --- |
| Factory | limit 20 | Decorator | Validate and retain limit |
| Decoration | receipt function | Wrapper | Retain function, preserve metadata |
| Invocation | amount 12 | Receipt result | Validate amount, invoke once |
| Invocation | amount 30 | Raises ValueError | Reject before business work |
| Invocation | amount 13 | Original failure | Forward without hiding the exception |

For `@bounded(20)`, the effective assignment is `receipt = bounded(20)(receipt)`.
The limit does not get recreated for every call. Choose immutable configuration or an intentional
snapshot; [closure capture](../../day-009-frequency-ranking/lang_closure-binding/CONCEPTS.md) does
not deep-copy mutable settings. Each wrapper here adds O(1) validation under the integer model,
with O(1) retained references per decorated function; wrapped execution retains its own cost.

## When it breaks

```python
from functools import wraps

def bounded(limit):
    if type(limit) is not int or limit < 0:
        raise ValueError("limit must be a nonnegative integer")
    def decorate(function):
        @wraps(function)
        def wrapper(amount):
            if type(amount) is not int or not 0 <= amount <= limit:
                raise ValueError("amount outside configured range")
            return function(amount)
        return wrapper
    return decorate

failure = RuntimeError("printer unavailable")

@bounded(20)
def receipt(amount):
    if amount == 13:
        raise failure
    return amount * 2

print("valid:", receipt(12))
try:
    receipt(30)
except ValueError as error:
    print(f"ValueError: {error}")

def swallowed(amount):
    try:
        return receipt(amount)
    except Exception:
        return None

print("bad catch-all:", swallowed(13))
try:
    receipt(13)
except RuntimeError as error:
    print(f"RuntimeError: {error}; same object: {error is failure}")
    assert error is failure
else:
    raise AssertionError("the wrapped failure was swallowed")
assert receipt(0) == 0
```

**Line by line:** the factory validates policy before returning a decorator. `type(...) is int`
deliberately excludes Boolean amounts for this example; it is an explicit domain choice. The
decorator retains the function and uses `wraps` on the replacement. The wrapper validates one
argument, calls once, and returns the result without catching business errors. `swallowed` is
the intentionally broken comparison. The final try/else fails if no original exception arrives,
and the identity assertion proves that the original exception object survived.

Author verification on Python 3.12.10, 2026-09-22:

```text
valid: 24
ValueError: amount outside configured range
bad catch-all: None
RuntimeError: printer unavailable; same object: True
```

## In production

Document the supported signature. This wrapper accepts `amount` positionally or by keyword,
but it is not a universal validator for arbitrary signatures. General wrappers can use explicit
parameter binding, whose extra cost and default handling must be understood before adoption.
Do not merely index `args[0]` if callers may use keywords.

Keep business failures separate from validation failures in metrics and logs. An async wrapper
must await the operation to observe its actual completion. A reviewer should ask whether the
decorator retries or invokes the function more than once, whether configuration is mutable,
and whether a valid falsy result such as zero is preserved. Avoid catching an exception merely
to replace it with `None`; if logging is required, preserve the exception with an explicit policy.

## Check yourself

### Readiness before practice

1. What is executed at factory time, definition time, and invocation time?
2. Why does limit validation belong outside the wrapper?
3. How does the failure assertion distinguish a real error from a `None` result?
4. What contract must change to decorate a function with several named parameters?

Run the block and explain the three lifetimes aloud. Then implement [your validation lab](README.md#assignment)
with a different rule in [lab.py](lab.py); assert rejection, a valid boundary, and an unchanged wrapped exception.

[Navigation](README.md) · [Recall](../../../docs/LANG_RECALL.md#day-012-decorator-arguments)
