---
day: 35
part: "3.1"
title: "Week 5 Python review"
ids: [PY-35]
level: working
prerequisites: ["See the linked prerequisite explanations below"]
prev: README.md
next: README.md
failure: true
---

# Week 5 Python review

Cold review: attempt [the assignment](README.md) first. Use this lesson afterwards for repair; record any help.

Core reading: explanation, worked trace, and readiness within this track's existing cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

A useful Python cold review reproduces one object-model surprise and tests the mechanism of its repair.

## The story

A test checks the expected field value on one object. It misses shared storage until a second object is created in production.

## The idea in plain language

Attempt the assigned review without notes first. Afterwards, use [lookup](../../day-029-stable-record-sorting/lang_attribute-lookup/CONCEPTS.md),
[properties](../../day-030-merge-overlapping-intervals/lang_properties/CONCEPTS.md), [descriptors](../../day-031-insert-an-interval/lang_descriptors/CONCEPTS.md),
[binding](../../day-032-minimum-meeting-rooms/lang_method-binding/CONCEPTS.md), [super](../../day-033-kth-smallest/lang_inheritance-and-super/CONCEPTS.md), or [slots](../../day-034-count-inversions/lang_slots/CONCEPTS.md)
to repair the selected gap. Choose one behavior, not six new experiments. A regression test
must fail for the original defect and pass after its cause is fixed.

## Why Krama needs it

This develops PY-35. The [day hub](../LESSON.md) keeps the three tracks independent.
The mechanism supports the practice contract and the later review; reading is not study completion.

## The source behind it

[Data model](https://docs.python.org/3.12/reference/datamodel.html) defines attribute access and slots.
Official pages checked 2026-09-23; see [the source ledger](../../../docs/SOURCES.md).
The examples, traces, and failure models are original teaching material.

## The mechanism

### Worked trace

Keep the 15-minute session: 3 minutes prediction from memory, 8 minutes reproduction and
repair, 4 minutes explanation and checks. Before running, state which object owns the state
and which lookup path will be used. Capture the actual surprise. Change the ownership or
dispatch rule, then check both the affected object and an independent instance.

| Suspected gap | Evidence that distinguishes it |
| --- | --- |
| class mutable storage | identity and mutation across two instances |
| property validation | rejected assignment preserves old value |
| descriptor precedence | same-name instance dictionary entry |
| method binding | __self__ and __func__ |
| cooperative super | ordered call log for a diamond |
| slots | dictionary presence in base and subclass |

For a shared-list defect, a one-object value assertion can pass. With two objects, append
through one and observe the other. Repair by allocating in each instance's initializer;
assert both nonidentity and isolation after mutation. Merely copying expected values in a
test can hide continued aliasing. Record interpreter version, prediction, output, explanation,
help used, and next step. A copied demonstration is repair reading, not a cold pass.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
class Bad:
    items = []
a, b = Bad(), Bad()
a.items.append('x')
print('bug, second instance:', b.items)
assert b.items == ['x']
class Good:
    def __init__(self):
        self.items = []
c, d = Good(), Good()
c.items.append('x')
print('repair, second instance:', d.items)
assert c.items is not d.items and d.items == []
```

**Line by line:** Bad has one shared class list; Good allocates once per instance. The regression checks both identity and mutation isolation, so it can reject equal-but-shared empty lists before their contents diverge.

Observed author output on Python 3.12.10, 2026-09-23:

```text
bug, second instance: ['x']
repair, second instance: []
```

These checks are author teaching evidence. A small Python model does not establish database
behavior, production performance, or learner mastery.

## In production

Add the smallest reproduction to a real regression suite only where it protects a public
behavior or prior bug. A test that asserts interpreter implementation details may block harmless
upgrades. Keep conclusions about language semantics separate from measured object sizes.
Optional depth: repeat the selected experiment with a subclass to see whether ownership or
dispatch assumptions still hold.

## Check yourself

### Readiness before practice

After the cold attempt: can you name the owner, trace lookup, and explain why the test rejects the old behavior? Did the repair introduce a new inheritance assumption?

Run the block to check your prediction if needed, then use [README.md](README.md) for the
assignment, verification, and evidence route. Keep the 60/30/15-minute track budgets.
