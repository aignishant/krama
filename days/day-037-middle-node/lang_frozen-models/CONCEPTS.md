---
day: 37
part: "3.1"
title: "Frozen models"
ids: [PY-37]
level: working
prerequisites: ["See the linked prerequisite explanation below"]
prev: README.md
next: README.md
failure: true
---

# Frozen models

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

A frozen dataclass blocks ordinary field rebinding; mutable objects reachable through its fields remain mutable.

## The story

A job configuration is frozen, so a reviewer assumes its tag list cannot change. Another owner appends through a shared list reference and the supposedly stable configuration changes.

## The idea in plain language

Recall [dataclass default factories](../../day-036-reverse-a-linked-list/lang_dataclass-defaults/CONCEPTS.md).
A field holds a reference to an object. Reassigning that field changes the reference; calling
a method on the referenced object can change that object's contents without rebinding the
field. A default factory gives each instance its own container but does not freeze it.
Use frozen value models when stable snapshots simplify reasoning, and inspect the entire
reachable representation before describing them as immutable.

## Why Krama needs it

This develops PY-37; the [day hub](../LESSON.md) keeps the tracks independent.
Use the explanation to reason before practice. Reading does not establish study completion.

## The source behind it

[Python 3.12 dataclasses: frozen instances](https://docs.python.org/3.12/library/dataclasses.html#frozen-instances) documents emulated assignment protection.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The worked examples, proofs, and numeric scenarios below are original teaching material.

## The mechanism

### Worked trace

Consider a frozen Packet with tags pointing at list L:

| Operation | Object affected | Outcome |
| --- | --- | --- |
| packet.tags = ['new'] | Packet field binding | FrozenInstanceError |
| packet.tags.append('new') | list L | succeeds |
| external_alias.append('other') | same list L | packet observes change |

The decorator supplies assignment/deletion guards, not recursive conversion. For a snapshot
of string labels, convert incoming labels to a tuple during construction. Later mutations
of the original list no longer change the tuple. This is a shallow snapshot: tuple elements
that are themselves mutable would still be shared. An immutable boundary needs suitable
representations all the way down, not just a tuple around arbitrary objects.

The model also separates mutation from evolution: `dataclasses.replace` can create a new
instance with changed fields while leaving the old snapshot in place. It does not recursively
copy unchanged mutable fields. Frozen is a cooperative API guard, not a security boundary;
low-level assignment mechanisms can bypass it.

Converting k labels to a tuple takes O(k) time and reference storage. Ordinary frozen field
reads remain attribute reads. The representation decision should reflect who owns a value
and whether callers need a shared live view or an independent snapshot.

## When it breaks

Predict this separate teaching demonstration before running it in a scratch interpreter.

```python
from dataclasses import dataclass, FrozenInstanceError

@dataclass(frozen=True)
class Packet:
    tags: list[str]

labels = ['queued']
packet = Packet(labels)
try:
    packet.tags = ['done']
except FrozenInstanceError as error:
    print('rebind:', type(error).__name__)
labels.append('shared')
print('contained mutation:', packet.tags)
assert packet.tags == ['queued', 'shared']

@dataclass(frozen=True)
class Snapshot:
    tags: tuple[str, ...]

snapshot = Snapshot(tuple(labels))
labels.append('later')
print('snapshot:', snapshot.tags)
assert snapshot.tags == ('queued', 'shared')
```

**Line by line:** Packet stores the supplied list reference. Ordinary assignment raises the observed exception, but appending through the alias changes that list. Snapshot receives a newly constructed tuple of strings, so a later list append does not change the captured sequence.

Observed author output on Python 3.12.10, 2026-09-23:

```text
rebind: FrozenInstanceError
contained mutation: ['queued', 'shared']
snapshot: ('queued', 'shared')
```

These are author teaching observations. The deterministic models do not measure production
performance or prove the behavior of a deployed cache or concurrent service.

## In production

Use frozen records to express value ownership and replace whole records on change. Do not
infer thread safety from the decorator when nested objects or external resources remain
mutable. Optional depth: inspect nested aliasing and serialization boundaries; generated
hash behavior is the next lesson's separate concern.

## Check yourself

### Readiness before practice

1. Why does append avoid the field-assignment guard?
2. Would a tuple containing a list establish deep immutability?
3. Which constructor boundary should snapshot a caller-owned sequence?

Return to [README.md](README.md) for the assignment, verification, and evidence route.
Keep the independent 60/30/15-minute budgets; extra depth can wait for another sitting.
