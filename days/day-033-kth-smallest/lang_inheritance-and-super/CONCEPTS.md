---
day: 33
part: "3.1"
title: "Inheritance and super"
ids: [PY-33]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Inheritance and super

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Cooperative super follows the next implementation in the actual instance’s MRO, which need not be a direct parent.

## The story

Two mixins both add a cleanup step. Calling the shared base directly from each mixin runs that base twice and skips the intended cooperative route.

## The idea in plain language

Prerequisite: [method binding](../../day-032-minimum-meeting-rooms/lang_method-binding/CONCEPTS.md). Multiple inheritance can form a diamond:
D inherits B and C, and both inherit A. The method resolution order is a consistent linear
ordering of these classes. In a method defined on B, super() starts searching after B in
the actual object's MRO. It does not mean “call B's direct parent” in every context.

## Why Krama needs it

This develops PY-33. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Built-in Functions — super](https://docs.python.org/3.12/library/functions.html#super) documents MRO-based delegation; [Data model](https://docs.python.org/3.12/reference/datamodel.html) defines attribute access and slots.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

For D(B,C), with B(A) and C(A), the MRO is D,B,C,A,object. D.run appends D and delegates.
B.run appends B then super().run reaches C.run, even though C is not B's parent. C delegates
to A, and A terminates this particular protocol without asking object for a nonexistent run.

```text
D.run -> B.run -> C.run -> A.run
MRO: D, B, C, A, object
```

The cooperation contract is that each participant consumes its own work and delegates once,
using compatible signatures. Skipping super in B stops before C. Calling A.run explicitly
from both B and C can duplicate A and breaks composability. Python's ordering preserves the
declared local base ordering and consistent inherited ordering; inconsistent hierarchies can
be rejected at class creation. Inspect __mro__ to understand a concrete hierarchy rather than
guessing from the diagram. Work is proportional to participating method bodies, and lookup
can invoke arbitrary behavior; super supplies dispatch, not an optimization guarantee.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
class A:
    def run(self, out):
        out.append('A')
class B(A):
    def run(self, out):
        out.append('B')
        super().run(out)
class C(A):
    def run(self, out):
        out.append('C')
        super().run(out)
class D(B, C):
    def run(self, out):
        out.append('D')
        super().run(out)

out = []
D().run(out)
print('MRO:', [c.__name__ for c in D.__mro__])
print('cooperative:', out)
assert out == ['D', 'B', 'C', 'A']
bad = []
A.run(D(), bad)
A.run(D(), bad)
print('two explicit base calls:', bad)
assert bad == ['A', 'A']
```

**Line by line:** Each cooperative override adds one label and passes the same output list onward. A is the endpoint for this custom protocol. Explicitly invoking A twice demonstrates duplicated work without involving the MRO traversal that prevents that duplication in the cooperative version.

Observed author output on Python 3.12.10, 2026-09-23:

```text
MRO: ['D', 'B', 'C', 'A', 'object']
cooperative: ['D', 'B', 'C', 'A']
two explicit base calls: ['A', 'A']
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Keep mixin interfaces small and document whether super delegation is mandatory. Constructor
mixins need an agreed argument-consumption protocol; forwarding arbitrary arguments to object
can fail. Prefer composition when unrelated lifecycles make cooperation hard to explain.
A reviewer should test the actual combined class, since a mixin working alone does not prove
its behavior in a new MRO. Optional depth: construct and explain an inconsistent hierarchy.

## Check yourself

### Readiness before practice

1. Why does super inside B reach C for a D instance?
2. What breaks if B omits delegation?
3. Why is A the endpoint in this example?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
