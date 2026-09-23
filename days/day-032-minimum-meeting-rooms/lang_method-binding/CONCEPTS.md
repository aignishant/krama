---
day: 32
part: "3.1"
title: "Method binding"
ids: [PY-32]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Method binding

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

A bound method pairs a function with its receiver; static and class methods choose different receiver behavior.

## The story

A callback saved from one object keeps acting on that object even when another object has the same method name.

## The idea in plain language

Prerequisite: [descriptors](../../day-031-insert-an-interval/lang_descriptors/CONCEPTS.md). A normal function stored on a class is a
non-data descriptor. Retrieving it through an instance creates a bound method: __func__ is
the underlying function and __self__ is the receiver to pass as its first argument. A
staticmethod suppresses this binding; a classmethod binds the accessed class instead.

## Why Krama needs it

This develops PY-32. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Descriptor Guide](https://docs.python.org/3.12/howto/descriptor.html) describes attribute precedence and method binding.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Suppose Worker.label(self) returns self.name. Access Worker.label to get the function;
access worker.label to get a method with worker attached. Calling worker.label() is equivalent
in argument binding to Worker.label(worker). Saving bound=worker.label saves that receiver
association; it does not dynamically choose a worker at every call.

| Declaration | Access through instance | Implicit first argument |
| --- | --- | --- |
| ordinary def | bound method | the instance |
| @staticmethod | original function | none |
| @classmethod | bound method | the accessed class |

For class Child(Worker), an inherited classmethod reached via Child binds Child, which enables
constructors returning cls(...). Hard-coding Worker inside that constructor loses this behavior.
Calling the unbound function without a receiver does not invent self; Python raises TypeError.
Method binding is a small wrapper operation, but a saved bound method retains a reference to
its receiver, which can extend the receiver's lifetime. Do not rely on repeated attribute
reads producing the identical wrapper object.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
class Worker:
    def __init__(self, name):
        self.name = name
    def label(self):
        return self.name
    @staticmethod
    def normalize(name):
        return name.upper()
    @classmethod
    def make(cls):
        return cls('made')

class Child(Worker):
    pass
w = Worker('one')
bound = w.label
assert bound.__self__ is w and bound.__func__ is Worker.label
print('bound and explicit:', bound(), Worker.label(w))
try:
    Worker.label()
except TypeError as exc:
    print(type(exc).__name__ + ': ' + str(exc))
print('static:', w.normalize('ab'), 'class:', type(Child.make()).__name__)
assert isinstance(Child.make(), Child)
```

**Line by line:** Inspecting __self__ and __func__ verifies the two parts of binding. The explicit class call supplies the same receiver manually. Omitting it produces the captured TypeError. The inherited factory proves that classmethod binds Child, while staticmethod adds no implicit argument.

Observed author output on Python 3.12.10, 2026-09-23:

```text
bound and explicit: one one
TypeError: Worker.label() missing 1 required positional argument: 'self'
static: AB class: Child
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Callback registries holding bound methods can keep objects alive after their intended
owner releases them. Deregister callbacks or use suitable weak references when lifetime matters.
Use staticmethod for a namespace-related function and classmethod for class-polymorphic
behavior; neither is merely a workaround for a missing self parameter. Optional follow-up:
why can an instance attribute shadow an ordinary method under default lookup?

## Check yourself

### Readiness before practice

1. What do __self__ and __func__ hold?
2. Why does Child.make return Child?
3. How can a saved callback affect object lifetime?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
