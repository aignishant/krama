---
day: 3
part: "3.1"
title: "Match a default object's lifetime to the call"
ids: [PY-03]
level: working
prerequisites: ["Identity and mutation", "Function calls"]
failure: true
---

# Match a default object's lifetime to the call

Core reading precedes your independent list-default lab. Custom sentinels and deliberate caches
are optional follow-ups; they do not add another required experiment.

## One-line answer

A default expression runs when the function is defined; an omitted argument can reuse that same object.

## The story

A shop keeps a blank order form by the counter. Staff intend to give each customer a fresh
form, but keep writing on the same sheet. The next customer's order starts with the previous
customer's items. The mistake is the lifetime of the shared sheet, not the handwriting.

## The idea in plain language

Recall [aliasing and mutation](../../day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md).
A function stores references to its default argument values. Omitting an argument binds the
parameter to the stored object; it does not rerun the expression that originally made it.
Look for this issue when repeated calls behave differently from an isolated call.

## Why Krama needs it

This connects object ownership to function lifetime. A bug may survive ordinary unit tests
when each test creates a fresh function or only makes one call.

## The source behind it

[4. More Control Flow Tools — Default Argument Values](https://docs.python.org/3.12/tutorial/controlflow.html#default-argument-values),
checked 2026-09-22 (`spec:python-3.12-defaults`), specifies when defaults are evaluated. The
dictionary fixture below illustrates the rule without filling in your list exercise.

## The mechanism

### Worked trace

```text
Execute def -> allocate dictionary D -> store D on the function
First omitted call  -> parameter refers to D -> change D
Second omitted call -> parameter refers to D -> see the earlier change
Explicit argument   -> parameter refers to caller's object instead
```

Immutability matters: a shared integer default cannot be mutated in place like a dictionary.
Rebinding a parameter does not replace the function's stored default. Executing `def` again
creates a new function with newly evaluated defaults; “once” means once per definition execution.

To promise independent state for omitted arguments, use `None` as an absence marker and allocate
inside the call when the parameter `is None`. The branch runs on every omitted call. If the
caller supplies a dictionary, preserve it according to the documented mutation policy.

This works because each fresh allocation has its own identity and no earlier call retains an
alias to it. The repair does not make explicitly supplied shared containers private. Allocating
an empty dictionary takes constant initial work in this model; retained content still consumes
memory as it grows. Copying supplied data is a different policy with its own cost.

## When it breaks

```python
def stamp(label, fields={}):
    fields[label] = True
    return fields

first = stamp("packed")
second = stamp("shipped")
print("shared:", first is second)
print("second keys:", sorted(second))
try:
    assert "packed" not in second, "an earlier call leaked into this call"
except AssertionError as error:
    print(f"AssertionError: {error}")

def fresh_stamp(label, fields=None):
    if fields is None:
        fields = {}
    fields[label] = True
    return fields

first = fresh_stamp("packed")
second = fresh_stamp("shipped")
provided = {}
assert first is not second and "packed" not in second
assert fresh_stamp("checked", provided) is provided
assert provided == {"checked": True}
print("fresh calls and explicit ownership: PASS")
```

**Line by line:** the default dictionary belongs to the first function and both omitted calls
mutate it. Sorting makes the printed keys easy to compare. The assertion exposes call-history
dependence. The repaired function creates a dictionary inside the absence branch; explicit
arguments bypass it. The last assertions check both independent omitted calls and mutation of
an explicitly supplied empty dictionary.

Author verification on Python 3.12.10, 2026-09-22:

```text
shared: True
second keys: ['packed', 'shipped']
AssertionError: an earlier call leaked into this call
fresh calls and explicit ownership: PASS
```

Do not “repair” this with `fields = fields or {}`. That discards a caller's empty dictionary
because it is falsey, violating the explicit ownership case the final assertion tests.

## In production

Request metadata, accumulated errors, and batch buffers can leak across users through shared
defaults. Tests should make two calls in one process and separately pass an empty container.
Intentional shared caches need explicit ownership, bounds, and concurrency reasoning; a hidden
mutable default obscures all three. Optional: if `None` is meaningful data, use a unique sentinel
to distinguish omission, and document the public API's treatment of explicit `None`.

## Check yourself

### Readiness before practice

1. Which event allocates the broken dictionary: a call or execution of `def`?
2. Why does a single-call test miss this failure?
3. Why must the repaired code distinguish an empty container from an omitted one?
4. Does the sentinel fix protect a mutable container deliberately shared by the caller?

Implement your own **list** reproduction and repair in [lab.py](lab.py), following
[the assignment](README.md#assignment). Predict the second call and the first returned object's
contents after it. Record actual interpreter output and regression assertions in [NOTES.md](NOTES.md).

[Navigation](README.md) · [Quick recall](../../../docs/LANG_RECALL.md#day-003-mutable-defaults)
