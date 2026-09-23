---
day: 39
part: "3.1"
title: "Enums"
ids: [PY-39]
level: working
prerequisites: ["See the linked prerequisite explanation below"]
prev: README.md
next: README.md
failure: true
---

# Enums

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Parse external state values into Enum members, then validate allowed edges explicitly; enumerating states does not enforce transitions.

## The story

A job accidentally moves directly from queued to succeeded. All strings are spelled correctly, so checking membership in a list of states does not catch the skipped execution.

## The idea in plain language

Recall [value identity in models](../../day-038-cycle-entry/lang_ordering-and-hashing/CONCEPTS.md).
An Enum supplies named members with explicit values. The member is the domain state; its
value can be a stable wire representation. A transition is an allowed ordered pair of states.
Use a finite state model when legal values and legal movements are both part of the contract.

## Why Krama needs it

This develops PY-39; the [day hub](../LESSON.md) keeps the tracks independent.
Use the explanation to reason before practice. Reading does not establish study completion.

## The source behind it

[Python 3.12 enum documentation](https://docs.python.org/3.12/library/enum.html) defines member names, values, and lookup. The job transition graph is a local design choice.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The worked examples, proofs, and numeric scenarios below are original teaching material.

## The mechanism

### Worked trace

Choose QUEUED='queued', RUNNING='running', SUCCEEDED='succeeded', FAILED='failed'.

| Current state | Allowed next states | Example rejected edge |
| --- | --- | --- |
| QUEUED | RUNNING | QUEUED -> SUCCEEDED |
| RUNNING | SUCCEEDED, FAILED | RUNNING -> QUEUED |
| SUCCEEDED | none | SUCCEEDED -> RUNNING |
| FAILED | none in this model | FAILED -> SUCCEEDED |

At the input boundary, State(raw_value) resolves a value or raises ValueError. State['RUNNING']
instead resolves a member name; that is a different contract. Keep `.value` for serialization
and members for internal logic. Plain Enum members do not silently equal raw strings.

The transition table is a second layer: both QUEUED and SUCCEEDED are valid members, but the
pair is not allowed. Validate first, then assign. The table below treats terminal states as
terminal and rejects self-transitions. A system that permits retry or idempotent repeated
events must specify those additional edges/semantics explicitly.

For a fixed small state set the table has bounded size and checks are constant-scale lookups.
The important gain is an explicit contract and a place to audit changes, not a performance
optimization. Avoid auto-generated numeric values for a long-lived external protocol unless
its compatibility rules deliberately permit renumbering.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
from enum import Enum

class State(Enum):
    QUEUED = 'queued'
    RUNNING = 'running'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'

allowed = {
    State.QUEUED: {State.RUNNING},
    State.RUNNING: {State.SUCCEEDED, State.FAILED},
    State.SUCCEEDED: set(),
    State.FAILED: set(),
}
def transition(current, requested):
    target = State(requested)
    if target not in allowed[current]:
        raise ValueError('illegal transition')
    return target

print('raw string equal:', State.QUEUED == 'queued')
for raw in ['suceeded', 'succeeded']:
    try:
        transition(State.QUEUED, raw)
    except ValueError as error:
        print('rejected:', raw, type(error).__name__)
running = transition(State.QUEUED, 'running')
finished = transition(running, 'succeeded')
print('legal route:', running.value, finished.value)
assert finished is State.SUCCEEDED
```

**Line by line:** The explicit values define the external vocabulary. The transition function first parses, then checks the allowed edge. The misspelling fails parsing; the correctly spelled direct jump fails edge validation. The final two calls demonstrate a legal path and serialize its values.

Observed author output on Python 3.12.10, 2026-09-23:

```text
raw string equal: False
rejected: suceeded ValueError
rejected: succeeded ValueError
legal route: running succeeded
```

These are author teaching observations. The deterministic models do not measure production
performance or prove the behavior of a deployed cache or concurrent service.

## In production

In a database, reading RUNNING and later writing SUCCEEDED without a condition can race with
another transition. Use an atomic expected-state/version check at the storage boundary when
needed; an Enum alone adds no concurrency control. Optional depth: document handling for
unknown future values, aliases, retries, and terminal-state duplicate events.

## Check yourself

### Readiness before practice

1. How do State('running') and State['RUNNING'] differ?
2. Why does a valid state member not imply a valid transition?
3. Which race remains if two workers validate the same current state concurrently?

Return to [README.md](README.md) for the assignment, verification, and evidence route.
Keep the independent 60/30/15-minute budgets; extra depth can wait for another sitting.
