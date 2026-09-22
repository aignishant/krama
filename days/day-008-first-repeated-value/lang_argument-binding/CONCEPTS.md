---
day: 8
part: "3.1"
title: "Treat a function signature as a binding contract"
ids: [PY-08]
level: working
prerequisites: ["Object references", "Default argument lifetime"]
failure: true
---

# Treat a function signature as a binding contract

Core: trace positional-only, positional-or-keyword, and keyword-only binding, then capture a
real invalid call. Flexible wrappers and signature introspection are optional later reading.

## One-line answer

Binding maps supplied arguments onto parameter slots, rejecting invalid combinations before the function body runs.

## The story

A parcel form puts the parcel number in a fixed box and asks you to label optional instructions.
An unlabeled `True` in the next box is ambiguous. Requiring `urgent=True` makes the instruction clear.

## The idea in plain language

A parameter is a named slot in the function definition; an argument is a value supplied by
the call. The `/` marker makes parameters before it positional-only. Parameters after a bare
`*` are keyword-only. Slots between them can be filled by either position or name.
Defaults fill omitted optional slots; they do not permit filling the same slot twice.

Recognize binding design work when Boolean options are easy to swap, a wrapper forwards duplicate
keywords, or callers accidentally depend on a positional parameter's internal name. Binding
is separate from type and business validation. An accepted call can still contain an invalid
parcel number, and annotations alone do not enforce validation.

## Why Krama needs it

[Closure binding](../../day-009-frequency-ranking/lang_closure-binding/README.md) and later
decorator lessons distinguish values supplied at call time from names looked up later.
Precise signatures establish the boundary those wrappers must preserve.

## The source behind it

[4. More Control Flow Tools — Special parameters](https://docs.python.org/3.12/tutorial/controlflow.html#special-parameters)
(`spec:python-3.12-special-parameters`) defines the signature markers.
[6. Expressions — Calls](https://docs.python.org/3.12/reference/expressions.html#calls)
(`spec:python-3.12-expressions`) describes binding and duplicate arguments. Both checked 2026-09-22.
The parcel interface and recorded exceptions below are original author experiments.

## The mechanism

### Worked trace

Consider `label(parcel, /, copies=1, *, urgent=False)`:

| Call | parcel slot | copies slot | urgent slot | Result |
| --- | --- | --- | --- | --- |
| `label("P7")` | "P7" | default 1 | default False | Body runs |
| `label("P7", 2, urgent=True)` | "P7" | positional 2 | keyword True | Body runs |
| `label("P7", copies=2)` | "P7" | keyword 2 | default False | Body runs |
| `label(parcel="P7")` | Cannot be filled by keyword | — | — | TypeError |
| `label("P7", 2, True)` | "P7" | 2 | Cannot be positional | TypeError |
| `label("P7", 2, copies=3)` | "P7" | Filled twice | — | TypeError |

Reason about the call by filling eligible positional slots, matching keyword names to eligible
slots, rejecting collisions, and applying defaults to omitted slots. This is a reasoning model,
not a promise about the interpreter's implementation order. Argument expressions themselves
are evaluated before the call, so they may have effects even if binding fails. The function
body does not run on a binding error.

Binding a list fills a slot with a reference; it does not copy the list. Defaults are evaluated
when the definition executes, as in [Day 3](../../day-003-stable-compaction/lang_mutable-defaults/CONCEPTS.md).
Keeping these boundaries distinct explains why `/` or `*` cannot fix a shared mutable default.

## When it breaks

```python
body_calls = []

def label(parcel, /, copies=1, *, urgent=False):
    body_calls.append(parcel)
    return parcel, copies, urgent

print("valid:", label("P7", 2, urgent=True))
invalid_calls = [
    lambda: label(parcel="P7"),
    lambda: label("P7", 2, True),
    lambda: label("P7", 2, copies=3),
]
for call in invalid_calls:
    try:
        call()
    except TypeError as error:
        print(f"TypeError: {error}")
    else:
        raise AssertionError("invalid call unexpectedly bound")
assert body_calls == ["P7"]
assert label("P8", copies=2) == ("P8", 2, False)
print("binding and body-entry checks: PASS")
```

**Line by line:** `body_calls` instruments body entry. The valid call fills all slots legally.
Each lambda delays a distinct invalid call until its own `try` block. Capturing `TypeError`
records the interpreter's actual diagnostic; the `else` ensures unexpected acceptance fails
the test. The call log proves the invalid calls never entered this function's body. The final
valid call demonstrates keyword binding to the middle slot and the default urgent flag.

Author verification on Python 3.12.10, 2026-09-22; exact error wording is version-dependent:

```text
valid: ('P7', 2, True)
TypeError: label() got some positional-only arguments passed as keyword arguments: 'parcel'
TypeError: label() takes from 1 to 2 positional arguments but 3 were given
TypeError: label() got multiple values for argument 'copies'
binding and body-entry checks: PASS
```

## In production

Use keyword-only options when names carry essential meaning and positional-only slots when
the caller should not depend on the internal parameter name. These choices constrain future
compatibility: renaming a keyword parameter breaks callers that use it. Avoid blanket `**kwargs`
unless the forwarding contract is explicit; accepting arbitrary names can postpone useful errors.
For a fixed small signature, this exercise's binding work is bounded. Building large `*args`
or `**kwargs` containers has separate work and storage costs; markers are API choices, not
a measured performance optimization.

Optional edge: with `def f(name, /, **extra)`, a keyword `name` can live in `extra` because it
does not bind the positional-only slot. That slot must still receive a positional argument.
Review wrappers for preserved restrictions and duplicated keywords; test error type and body
effects rather than depending on exact interpreter error text as a stable application API.

## Check yourself

### Readiness before practice

1. Which slots may be named in `label`, and which must be named?
2. Why does a default not resolve duplicate positional and keyword values?
3. Does a binding failure imply no argument expression ran?
4. Do the markers copy objects or validate their business meaning?

Run the author block, then create your own function and invalid-call experiment in [lab.py](lab.py)
under [the assignment](README.md#assignment). Predict first; capture the real exception and a
regression assertion in [NOTES.md](NOTES.md). Keep the 15-minute budget and explain the slots aloud.

[Navigation](README.md) · [Quick recall](../../../docs/LANG_RECALL.md#day-008-argument-binding)
