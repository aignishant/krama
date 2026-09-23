---
day: 38
part: "3.1"
title: "Ordering and hashing"
ids: [PY-38]
level: working
prerequisites: ["See the linked prerequisite explanation below"]
prev: README.md
next: README.md
failure: true
---

# Ordering and hashing

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Choose equality, ordering, and hashing together according to value identity and mutability; generated methods follow declared fields.

## The story

Two queue records compare equal, yet putting one in a set raises TypeError. The restriction protects hashed collections from keys whose value identity can change.

## The idea in plain language

Recall [frozen fields versus nested mutability](../../day-037-middle-node/lang_frozen-models/CONCEPTS.md).
Equality says which records represent the same value. Ordering determines priority among
records. Hashing routes keys into a dictionary or set: equal keys must have equal hashes,
and a key's hash must remain stable while stored. Unequal keys may share a hash.

## Why Krama needs it

This develops PY-38; the [day hub](../LESSON.md) keeps the tracks independent.
Use the explanation to reason before practice. Reading does not establish study completion.

## The source behind it

[Python 3.12 dataclass parameters](https://docs.python.org/3.12/library/dataclasses.html#dataclasses.dataclass) specifies generated methods; [field](https://docs.python.org/3.12/library/dataclasses.html#dataclasses.field) controls participation.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The worked examples, proofs, and numeric scenarios below are original teaching material.

## The mechanism

### Worked trace

Compare two deliberately different configurations:

| Configuration | Equality | Ordering | Implicit hash |
| --- | --- | --- | --- |
| dataclass defaults | field values, same class | not generated | disabled for mutable value records |
| frozen=True, order=True | field values, same class | lexicographic field order | generated from hash-participating fields |

For frozen Priority(priority, sequence), compare priority first and sequence only on a tie.
Thus (1,9) precedes (2,0), even though 9 exceeds 0. If the declaration were reversed, the
generated comparison would represent a different scheduling rule. A field with compare=False
is excluded from generated equality and ordering, and by default from the generated hash too.
That is appropriate for descriptive metadata only when changing it should not change identity.

The generated hash still calls hash on participating values: a frozen record containing a
list can raise TypeError. Freezing the wrapper does not make a list hashable. `unsafe_hash=True`
requests generation, not a proof that mutation is safe. Avoid mutating identity fields of any
key already stored in a hashed collection.

With eq=False, dataclasses leave equality/hash behavior to inheritance, often object identity;
that differs from value semantics. order=True requires eq=True. For a business order distinct
from full-record equality, an explicit sorting key is often clearer than generated ordering.
For k cheap comparable fields, equality/order can inspect up to O(k) fields; hashing also
visits participating fields. Nested values determine the real operation cost.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
from dataclasses import dataclass, field

@dataclass
class MutableJob:
    priority: int

left, right = MutableJob(2), MutableJob(2)
print('mutable equality:', left == right)
assert left == right and MutableJob.__hash__ is None
try:
    hash(left)
except TypeError as error:
    print('mutable hash:', type(error).__name__)

@dataclass(frozen=True, order=True)
class Priority:
    priority: int
    sequence: int
    label: str = field(compare=False)

a = Priority(1, 9, 'first')
b = Priority(1, 9, 'renamed')
c = Priority(2, 0, 'later')
print('value equality, order:', a == b, a < c)
print('equal hashes:', hash(a) == hash(b))
assert a == b and a < c and hash(a) == hash(b)
assert len({a, b, c}) == 2
```

**Line by line:** MutableJob shows generated value equality alongside disabled hashing. Priority includes two identity/order fields and excludes a descriptive label. The test checks hash equality rather than a specific hash number, and the set verifies that equal records occupy one logical key.

Observed author output on Python 3.12.10, 2026-09-23:

```text
mutable equality: True
mutable hash: TypeError
value equality, order: True True
equal hashes: True
```

These are author teaching observations. The deterministic models do not measure production
performance or prove the behavior of a deployed cache or concurrent service.

## In production

Before using a dataclass as a cache key, decide whether every identity field is stable and
whether excluded fields can alter the cached answer. Never persist Python hash values as
cross-process identifiers. Optional depth: test mixed-class comparisons and nested unhashable
values, then compare an explicit key function with generated ordering.

## Check yourself

### Readiness before practice

1. Why is the mutable default configuration unhashable despite having equality?
2. What scheduling behavior changes when field declaration order changes?
3. Why does frozen=True not guarantee hash(instance) succeeds?

Return to [README.md](README.md) for the assignment, verification, and evidence route.
Keep the independent 60/30/15-minute budgets; extra depth can wait for another sitting.
