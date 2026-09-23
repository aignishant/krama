---
day: 27
part: "3.1"
title: "Context managers"
ids: [PY-27]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Context managers

Core reading: intuition, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting. Record partial progress if needed.

## One-line answer

A context manager pairs successful entry with exit, and its exit return value decides whether a body exception propagates.

## The story

A report opens a scratch buffer and fails while writing. Closing the buffer is necessary, but reporting success just because cleanup finished would hide the failed report.

## The idea in plain language

Recall [generator cleanup](../../day-017-container-capacity/lang_generator-cleanup/CONCEPTS.md).
A resource has a lifetime: a point where ownership begins and one where it must end. The with
statement makes that lifetime lexical, meaning it is visible as a block in the code. __enter__
acquires or exposes the resource; __exit__ handles leaving the block. Cleanup and recovery are
different decisions: closing a resource does not mean the failed operation succeeded.

## Why Krama needs it

This develops PY-27 independently of the other two tracks. The [day hub](../LESSON.md)
links the separate 60/30/15-minute routes; completing the reading is not passing the assignment.

## The source behind it

[8. Compound statements, the with statement](https://docs.python.org/3.12/reference/compound_stmts.html#the-with-statement) defines entry, exit, and suppression behavior.
Checked 2026-09-23; details are in the [source ledger](../../../docs/SOURCES.md).
The traces, examples, and failure demonstrations here are original teaching material.

## The mechanism

### Worked trace

Read this as a state transition sequence:

| Stage | Normal body | Body raises ValueError |
| --- | --- | --- |
| Evaluate manager | obtain manager | obtain manager |
| Enter | __enter__ returns value bound by as | same |
| Run body | reach end, return, or break | exception leaves body |
| Exit | __exit__(None,None,None) | __exit__(ValueError, exception, traceback) |
| Continue | normal control flow resumes | false-like return propagates; true suppresses |

__enter__ may return a resource different from the manager. If __enter__ itself raises, the
with statement does not call that manager's __exit__; acquisition code must clean up any
partially acquired resources. If __exit__ raises, that new failure becomes active and can
obscure the body failure, so cleanup errors need deliberate handling.

For an ordinary ownership scope, return False or None from __exit__ after cleanup. Return True
only for a specific exception the abstraction is designed to handle. Test success and body
failure, then check both final resource state and whether the exception was visible. A check
that merely sees closed=True cannot catch accidental suppression. Scope setup/teardown add
constant dispatch overhead; the underlying resource operations determine real cost.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
class Scope:
    def __init__(self, suppress):
        self.suppress = suppress
        self.closed = False
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, traceback):
        self.closed = True
        return self.suppress

for suppress in (True, False):
    scope = Scope(suppress)
    propagated = False
    try:
        with scope:
            raise ValueError("report failed")
    except ValueError as exc:
        propagated = True
        print(type(exc).__name__ + ": " + str(exc))
    print("suppress:", suppress, "closed:", scope.closed, "propagated:", propagated)
    assert scope.closed and propagated == (not suppress)

normal = Scope(False)
with normal:
    pass
assert normal.closed
print("normal cleanup checked")
```

**Line by line:** Scope toggles only the exception policy, keeping cleanup identical. Each loop uses a fresh manager. Raising in the body distinguishes propagation from closure. The final normal block verifies that cleanup also runs without an exception. This is an ablation demonstration, separate from the learner lab.

Observed author output on Python 3.12.10, 2026-09-23:

```text
suppress: True closed: True propagated: False
ValueError: report failed
suppress: False closed: True propagated: True
normal cleanup checked
```

The deliberate failure and repaired assertions are teaching evidence, not learner progress.
Python state models do not demonstrate PostgreSQL isolation or production performance.

## In production

Use existing context managers for files and locks instead of rebuilding their resource rules.
A transaction manager needs a documented commit/rollback policy; merely using with does not
promise a commit. Reentrancy and reuse are separate contracts: a manager valid once may not be
valid twice or nested. Optional depth: nested acquisition and ExitStack, introduced later,
help handle resources acquired in stages. A process kill is outside Python block cleanup.

## Check yourself

### Readiness before practice

1. Why is closed=True insufficient to prove the operation succeeded?
2. What arguments reach __exit__ after a normal body?
3. Who cleans up if __enter__ raises halfway through acquiring resources?
4. What changed assertion would expose a manager that accidentally returns True?

Run the teaching block only if you need to check your prediction. Then return to
[README.md](README.md) for the assignment, verification, and personal evidence route.
