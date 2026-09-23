---
day: 9
part: "1.1"
title: "A callback reads a binding when it runs"
ids: [PY-09]
level: working
prerequisites: ["Names and objects", "Default arguments"]
failure: true
---

# A callback reads a binding when it runs

Core: delayed lookup, capture with defaults, and a factory alternative. Object lifetime and
mutable configuration are optional depth. Python syntax is assumed; this track stands alone.

## One-line answer

A closure retains access to an enclosing binding; it does not automatically snapshot its value.

## The story

A shop creates three buttons, one for each item code. Every button later opens the last item.
The callbacks were created at different moments, but each reads the same name after the loop ends.

## The idea in plain language

A closure is a function that keeps access to names from an enclosing function even after that
outer call returns. A free variable is used by the inner function but bound outside it. In this
example all callbacks share the enclosing loop variable's binding. Calling them later observes
its final value. The same issue occurs with nested `def`; it is not specific to `lambda`.

Recall [names and objects](../../day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md)
and [default evaluation](../../day-003-stable-compaction/lang_mutable-defaults/CONCEPTS.md).
Distinguish retaining a binding from retaining the object currently bound to it. Recognize the
issue when a callback runs after a loop, request, or configuration update has changed a name.

## Why Krama needs it

[Nonlocal state](../../day-010-pair-sum-indices/lang_nonlocal-state/CONCEPTS.md) intentionally
changes a retained binding. Understanding shared state first explains both the bug and that feature.

## The source behind it

[Programming FAQ](https://docs.python.org/3.12/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result)
(`spec:python-3.12-programming-faq`, checked 2026-09-22) explains delayed lookup in loop-created
functions and default arguments as one capture technique. The trace below is an original experiment.

## The mechanism

### Worked trace

| Creation step | Shared outer binding | Late callback keeps | Default-based callback keeps |
| --- | --- | --- | --- |
| First iteration | code = 4 | Access to code | Default object 4 |
| Second iteration | code = 7 | Access to the same code | Default object 7 |
| Third iteration | code = 9 | Access to the same code | Default object 9 |
| Call after return | code remains 9 | All read 9 | Each reads its own parameter |

The default expression is evaluated when that inner function is created. At call time the
parameter shadows the outer name, so an omitted argument uses the captured object. This is
not a deep copy: capturing a list still shares that list. The callback also exposes a parameter
that callers can override; choose a factory if the public signature must remain argument-free.

A factory accepts one code and returns a callback reading that factory call's local code.
Each factory invocation creates separate enclosing state. Both approaches take O(m) creation
time and function storage for m callbacks; retained objects can dominate memory.

## When it breaks

```python
def make_callbacks():
    late, captured = [], []
    for code in (4, 7, 9):
        late.append(lambda: code)
        captured.append(lambda code=code: code)
    return late, captured

late, captured = make_callbacks()
actual = [callback() for callback in late]
fixed = [callback() for callback in captured]
print("late:", actual)
print("captured:", fixed)
try:
    assert actual == [4, 7, 9], "callbacks share the final loop binding"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert fixed == [4, 7, 9]
```

**Line by line:** the outer function makes this an enclosing-function example, avoiding confusion
with module globals. `lambda: code` delays reading the shared name. In `lambda code=code: code`,
the right-hand code is evaluated now and stored as the parameter default. The list comprehensions
call after the outer function has returned. The caught assertion exposes the wrong assumption;
the last checks separate captured values. Use a new scratch session to run this whole block.

Author verification on Python 3.12.10, 2026-09-22:

```text
late: [9, 9, 9]
captured: [4, 7, 9]
AssertionError: callbacks share the final loop binding
```

## In production

A queued callback can retain an entire request object long after response delivery. Capture only
the small stable data needed, or use an explicit object with a defined lifetime. Snapshot mutable
configuration deliberately; a default argument freezes a reference, not the object's contents.
A senior review question is whether the callback should see creation-time or execution-time state.
Both can be correct, but tests must call after the enclosing value changes, not only immediately
inside the creation loop. Immediate invocation can hide the defect.

## Check yourself

### Readiness before practice

1. What changes if each callback runs immediately inside the loop?
2. Why does rewriting the lambda as `def` alone fail to repair the problem?
3. Does capturing a mutable list freeze its contents?
4. How would a factory avoid adding a public default parameter?

Run the block, explain the binding lifetime aloud, then attempt [the lab assignment](README.md#assignment)
in your own [lab.py](lab.py). Record predictions and actual output in [NOTES.md](NOTES.md).

[Navigation](README.md) · [Recall](../../../docs/LANG_RECALL.md#day-009-closure-binding)
