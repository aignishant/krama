---
day: 24
part: "3.1"
title: "Make a collection safely repeatable"
ids: [PY-24]
level: working
prerequisites: ["Day 15 iterator protocol; representation ownership"]
failure: true
---

# Make a collection safely repeatable

Core reading: explanation, worked trace, and readiness within the existing track cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Keep immutable contents separate from traversal state, and give each iteration a fresh cursor.

## The story

A tiny collection stores one iterator and returns it to every loop. The first display works; the next loop sees nothing, even though len still reports three items.

## The idea in plain language

The assignment needs three operations: len(collection), iter(collection), and value in
collection. Define __len__, __iter__, and __contains__ on the class. Their meanings should
agree about which items belong to the collection. The collection should retain contents;
each iterator retains only its own traversal position. A tuple snapshot of immutable values
is a simple backing representation. Snapshotting a list of mutable objects does not freeze
the objects, and a tuple-valued attribute alone does not prevent attribute rebinding.

## Why Krama needs it

This develops PY-24 in its independent track. Use the prerequisite named above;
the other two tracks are not prerequisites. The [day hub](../LESSON.md) preserves the daily budgets.

## The source behind it

[Python 3.12 container protocol](https://docs.python.org/3.12/reference/datamodel.html#emulating-container-types) and [iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types) define the operation hooks and cursor expectations.
Source links checked 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
The examples and small failure models below are original teaching demonstrations.

## The mechanism

### Worked trace

For a collection snapshot (2,4,6), len returns 3. Iterator a and iterator b each start
before 2. Advancing a yields 2 and then 4; advancing b still yields 2. A membership test
for 4 consults contents without changing either cursor. A new traversal yields all three.

| Operation | Tuple-backed cost in this teaching design | State changed |
| --- | --- | --- |
| Construction from finite source | O(n) time and O(n) stored references | Snapshot created |
| len | O(1) | None |
| iter | O(1) cursor allocation | New independent cursor |
| Full traversal | O(n) with O(1) cursor state | That cursor only |
| contains | O(n) worst-case equality checks | No traversal cursor |

The demonstration uses a tuple subclass for an immutable integer collection and explicitly
delegates the three requested hooks. __slots__=() prevents an instance attribute dictionary;
the inherited tuple payload cannot be reassigned. Integer contents make this example deeply
immutable as well. The exercise can use another representation if its immutability contract
is explicit. Without __contains__, membership can fall back to iteration; repeated traversal
still depends on a correctly implemented __iter__.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
class BadCollection:
    def __init__(self, items):
        self.items = tuple(items)
        self.cursor = iter(self.items)
    def __len__(self):
        return len(self.items)
    def __iter__(self):
        return self.cursor

class IntCollection(tuple):
    __slots__ = ()
    def __new__(cls, items):
        values = tuple(items)
        if not all(type(value) is int for value in values):
            raise TypeError('integer items required')
        return super().__new__(cls, values)
    def __len__(self):
        return tuple.__len__(self)
    def __iter__(self):
        return tuple.__iter__(self)
    def __contains__(self, value):
        return tuple.__contains__(self, value)

bad = BadCollection([2, 4, 6])
print('shared cursor:', list(bad), list(bad), 'length:', len(bad))
source = [2, 4, 6]
good = IntCollection(source)
source.append(8)
a, b = iter(good), iter(good)
assert next(a) == 2 and next(a) == 4 and next(b) == 2
assert 4 in good and 8 not in good and len(good) == 3
assert list(good) == list(good) == [2, 4, 6]
try:
    good[0] = 9
except TypeError:
    print('immutable payload: TypeError')
print('fresh traversal:', list(good))
```

**Line by line:** BadCollection stores one cursor, causing its second traversal to be empty. IntCollection snapshots and validates inputs, delegates each protocol to immutable tuple storage, and verifies separate cursors, source independence, membership, and rejected mutation.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
shared cursor: [2, 4, 6] [] length: 3
immutable payload: TypeError
fresh traversal: [2, 4, 6]
```

The failing behavior is deliberate; subsequent assertions check the repair on these examples.
An executed Python model does not establish database behavior or production performance.

## In production

Choose between order and faster lookup deliberately: adding a set can accelerate repeated
membership but adds O(n) storage and requires hashable elements. A tuple holding mutable
elements promises only an immutable outer structure. State that limit if you broaden this
example beyond integers. Special methods belong on the type; assigning a hook only to one
instance is not a reliable way to customize implicit protocol operations.

## Check yourself

### Readiness before practice

1. Why can len(bad) remain three after iteration is exhausted?
2. Which object owns contents and which owns position?
3. Why does a tuple of lists fail to promise deep immutability?
4. What test detects two loops accidentally sharing one cursor?

Use [README.md](README.md) for the assignment, verification, and personal evidence route.
Reading the lesson does not complete study.
