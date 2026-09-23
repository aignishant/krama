---
day: 40
part: "3.1"
title: "Composition"
ids: [PY-40]
level: working
prerequisites: ["See the linked prerequisite explanation below"]
prev: README.md
next: README.md
failure: true
---

# Composition

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Give a worker a policy object with a small behavioral contract so configuration can vary and be tested without subclassing the worker.

## The story

A runner subclasses another runner just to change one batch limit. Soon there are subclasses for each limit, tenant, and retry mode, although the execution behavior is identical.

## The idea in plain language

Recall [inheritance and super](../../day-033-kth-smallest/lang_inheritance-and-super/CONCEPTS.md).
Inheritance says an instance can substitute for a base type under its behavioral contract.
Composition stores a collaborator and delegates a decision to it. A batch runner has a
batch policy; it is not itself a kind of policy. Recognize composition when behavior varies
independently from the host's lifecycle or needs isolated testing.

## Why Krama needs it

This develops PY-40; the [day hub](../LESSON.md) keeps the tracks independent.
Use the explanation to reason before practice. Reading does not establish study completion.

## The source behind it

[Python 3.12 classes tutorial](https://docs.python.org/3.12/tutorial/classes.html) supplies attribute and inheritance semantics. The policy interface and refactoring are original teaching examples.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The worked examples, proofs, and numeric scenarios below are original teaching material.

## The mechanism

### Worked trace

An inheritance-only sketch has Worker.batch_size=10 and SmallWorker.batch_size=2. Adding
another independent choice, such as retry strategy, encourages combinations of subclasses.
Instead, define policy.take(available): for nonnegative available, return a positive count
when work exists, never exceed available, and return zero when available is zero.

| Step | Object responsible | Example |
| --- | --- | --- |
| construct | application wiring | Runner(BatchPolicy(limit=2)) |
| decide | BatchPolicy | take(5) -> 2 |
| perform orchestration | Runner | select two available jobs |
| verify policy alone | test | take(0)=0, take(1)=1, take(5)=2 |

Store the collaborator on self and call its method at the decision point. The runner knows
only the needed behavior. Python permits this through ordinary object references and method
calls; a formal Protocol can be introduced in the later typing track. A small fake object
with the same method lets a test observe delegation without running a whole job system.

Composition does not automatically guarantee isolation: reusing one mutable policy object
can share configuration just as a mutable class attribute can. Choose immutable configuration,
per-owner instances, or explicit shared ownership. Validate limits at construction, so zero
does not silently yield a runner that makes no progress. Define invalid available counts too.

The policy's integer decision is O(1) under the unit-cost model. A real runner's slicing,
queue I/O, or processing cost is separate; extracting a collaborator does not make those
operations constant time. Use this when the boundary earns its extra indirection, not for
every literal constant.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
from dataclasses import dataclass

class LegacyWorker:
    settings = {'limit': 10}

class SmallWorker(LegacyWorker):
    pass

SmallWorker.settings['limit'] = 2
print('base unexpectedly changed:', LegacyWorker.settings['limit'])
assert LegacyWorker.settings['limit'] == 2

@dataclass(frozen=True)
class BatchPolicy:
    limit: int
    def __post_init__(self):
        if self.limit <= 0:
            raise ValueError('limit must be positive')
    def take(self, available):
        if available < 0:
            raise ValueError('available must be nonnegative')
        return min(self.limit, available)

class Runner:
    def __init__(self, policy):
        self.policy = policy
    def next_count(self, available):
        return self.policy.take(available)

small, normal = BatchPolicy(2), BatchPolicy(10)
assert [small.take(n) for n in (0, 1, 5)] == [0, 1, 2]
print('independent policies:', Runner(small).next_count(5), Runner(normal).next_count(5))
try:
    BatchPolicy(0)
except ValueError as error:
    print('invalid policy:', type(error).__name__)
```

**Line by line:** The inherited dictionary is one shared object, so subclass mutation affects the base. BatchPolicy replaces that implicit configuration with validated per-instance values. Runner delegates to its collaborator. Direct policy assertions cover no work, little work, and capped work; the final check rejects a non-progressing limit.

Observed author output on Python 3.12.10, 2026-09-23:

```text
base unexpectedly changed: 2
independent policies: 2 5
invalid policy: ValueError
```

These are author teaching observations. The deterministic models do not measure production
performance or prove the behavior of a deployed cache or concurrent service.

## In production

Keep policy interfaces narrow enough to test without a database, clock, or network. The
application chooses collaborators; the runner should not secretly instantiate a different
one. Inheritance remains useful for genuine behavioral substitution. Optional depth: inject
a recording fake, or compose retry and batch policies as two independent collaborators.

## Check yourself

### Readiness before practice

1. Why did editing SmallWorker.settings change LegacyWorker.settings?
2. How could a composed mutable policy recreate the same sharing bug?
3. Which tests belong to BatchPolicy and which demonstrate Runner delegation?

Return to [README.md](README.md) for the assignment, verification, and evidence route.
Keep the independent 60/30/15-minute budgets; extra depth can wait for another sitting.
