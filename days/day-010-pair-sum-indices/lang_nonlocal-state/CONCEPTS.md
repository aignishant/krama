---
day: 10
part: "1.1"
title: "Choose the owner of a persistent binding"
ids: [PY-10]
level: working
prerequisites: ["Closure binding", "Mutation versus rebinding"]
failure: true
---

# Choose the owner of a persistent binding

Core: local assignment, nonlocal rebinding, and comparison with a callable instance. Concurrency
and persistence are optional depth; today's lab is a small sequential experiment.

## One-line answer

Use `nonlocal` to rebind an existing enclosing function variable, with state owned by that outer call.

## The story

A shop's ticket dispenser needs to remember the next ticket between calls. Two dispensers must
advance independently. Putting the count in one global variable would accidentally join their queues.

## The idea in plain language

[Closures](../../day-009-frequency-ranking/lang_closure-binding/CONCEPTS.md) retain enclosing
bindings. Assignment to a name in a function normally makes it local throughout that function.
A read followed by an assignment therefore does not automatically mean “update the outer value.”
It can read an as-yet-unassigned local name and raise `UnboundLocalError`.

The declaration `nonlocal` chooses an existing binding in the nearest enclosing function scope.
It cannot create an outer binding, and it does not mean global. With nested factories, identify
the precise owner before adding the declaration. Recognize this pattern when a small callable
needs private state across calls without a module-wide singleton.

## Why Krama needs it

[Decorator arguments](../../day-012-range-sums/lang_decorator-arguments/CONCEPTS.md) uses nested
functions with distinct lifetimes. Confusing configuration state with per-call state causes leaks
between invocations and between separately decorated functions.

## The source behind it

[7. Simple statements](https://docs.python.org/3.12/reference/simple_stmts.html#the-nonlocal-statement)
(`spec:python-3.12-simple-statements`, checked 2026-09-22) specifies nonlocal binding.
The comparison below is an original state-ownership example.

## The mechanism

### Worked trace

Suppose factory call A starts a running receipt total at zero. Its returned callable adds 5,
then 2: A's binding changes 0 → 5 → 7. Factory call B has a different binding; adding 2 there
changes 0 → 2. Assigning a second name to A's callable shares A's state; it does not create B.

A callable instance expresses the same ownership explicitly: construction stores a total on
`self`, and `__call__` updates `self.total`. Two instances have separate attributes. A closure
fits a single small operation; an instance becomes clearer when reset, inspection, validation,
or several operations need names. Neither representation supplies synchronization automatically.

| Operation | Binding affected | Declaration needed? |
| --- | --- | --- |
| Rebind an enclosing integer name | Outer function's binding | `nonlocal` |
| Append through an enclosing list reference | Existing list object | No, if the name is not assigned |
| Assign `self.total` | Instance attribute | No `nonlocal` |
| Assign a module variable | Module namespace | `global`, a different ownership choice |

## When it breaks

```python
def broken_total():
    total = 0
    def add(amount):
        total += amount
        return total
    return add

def running_total():
    total = 0
    def add(amount):
        nonlocal total
        total += amount
        return total
    return add

try:
    broken_total()(5)
except UnboundLocalError as error:
    print(f"UnboundLocalError: {error}")
a, b = running_total(), running_total()
observed = [a(5), a(2), b(2)]
print("separate totals:", observed)
assert observed == [5, 7, 2]
```

**Line by line:** `total += amount` both reads and assigns total, making the broken version's
name local. The second inner function declares the outer owner before using it. Returning `add`
keeps that binding alive. Two calls to `running_total` create independent state; the assertion
would detect accidental global sharing. This demonstrates a running total on different inputs;
the learner still implements and compares the assigned counter and callable instance.

Author verification on Python 3.12.10, 2026-09-22:

```text
UnboundLocalError: cannot access local variable 'total' where it is not associated with a value
separate totals: [5, 7, 2]
```

## In production

Each closure adds constant-sized state here, but referenced objects remain live with it.
State disappears with the process; neither a closure nor an ordinary instance is durable storage.
Concurrent callers require an explicit synchronization or ownership strategy. Do not infer
atomic business operations from one short Python statement or from a particular interpreter.
A reviewer should ask how state is reset and tested, and whether hidden state makes reuse surprising.
When callers need serialization or several related operations, named instance attributes may
make the lifecycle easier to inspect than an opaque closure.

## Check yourself

### Readiness before practice

1. Why does assignment change the meaning of the earlier read?
2. Which factory call owns each value in `[5, 7, 2]`?
3. Why can list mutation work without `nonlocal` while rebinding cannot?
4. What does a callable instance improve, and what safety does it not add?

Run the block and explain the error aloud. Then implement [the assigned comparison](README.md#assignment)
in [lab.py](lab.py), testing two independent objects as well as repeated calls to one.

[Navigation](README.md) · [Recall](../../../docs/LANG_RECALL.md#day-010-nonlocal-state)
