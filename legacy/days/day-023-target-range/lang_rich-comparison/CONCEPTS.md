---
day: 23
part: "3.1"
title: "Decline unsupported comparisons correctly"
ids: [PY-23]
level: working
prerequisites: ["Special methods; equality versus ordering"]
failure: true
---

# Decline unsupported comparisons correctly

Core reading: explanation, worked trace, and readiness within the existing track cap.
Production extensions are optional depth for another sitting; record partial progress if needed.

## One-line answer

Return NotImplemented when an operand pair is unsupported so Python can try the other operand or its final fallback.

## The story

A custom quantity returns False for every unfamiliar object. A second type could have compared the values, but it never gets the chance.

## The idea in plain language

False means the comparison was understood and its answer is false. NotImplemented means
this method does not handle the operand pair. It is a return value, not NotImplementedError.
For ordering, __lt__ and __gt__ form a reflected pair: left < right may try right.__gt__(left).
If neither supports ordering, the expression raises TypeError. Equality instead has an
identity-based fallback when both methods decline. Do not use NotImplemented as a boolean.

## Why Krama needs it

This develops PY-23 in its independent track. Use the prerequisite named above;
the other two tracks are not prerequisites. The [day hub](../LESSON.md) preserves the daily budgets.

## The source behind it

[Python 3.12 rich comparisons](https://docs.python.org/3.12/reference/datamodel.html#object.__lt__) specifies reflected dispatch, subclass priority, and final fallbacks.
Source links checked 2026-09-22; see [the source ledger](../../../docs/SOURCES.md).
The examples and small failure models below are original teaching demonstrations.

## The mechanism

### Worked trace

In the demonstration, Low.__lt__ declines comparison with High. High.__gt__ recognizes Low
and returns True, so Low() < High() is True. If a bad Low.__lt__ returns False, dispatch has
an answer already and the reflected method is not tried. Neither Low nor a plain object
understands their ordering, so Low() < object() raises TypeError.

| Step for unrelated operand classes | Result |
| --- | --- |
| left.__lt__(right) | NotImplemented permits another attempt |
| right.__gt__(left) | A supported result completes the expression |
| Both decline | Ordering raises TypeError |

There is a subclass priority rule: when the right operand's type is a strict subclass of
the left operand's type, its reflected method has priority. This demo uses unrelated classes
to make the simple trace visible. Implementing one comparison does not automatically define
every other ordering operation. Correctness means the supported domain and order are clear;
do not invent an order between unrelated types just to suppress errors. Dispatch itself is
bounded overhead, but comparing payloads can cost O(m) for m-element sequences.

## When it breaks

Predict this separate demonstration before running it in a scratch interpreter.

```python
class Low:
    def __lt__(self, other):
        print('Low declines')
        return NotImplemented

class High:
    def __gt__(self, other):
        if isinstance(other, Low):
            print('High accepts reflected comparison')
            return True
        return NotImplemented

class BadLow(Low):
    def __lt__(self, other):
        return False

print('premature False:', BadLow() < High())
assert (Low() < High()) is True
try:
    Low() < object()
except TypeError:
    print('unsupported ordering: TypeError')
else:
    raise AssertionError('unsupported ordering should fail')
x, y = Low(), Low()
assert (x == x) is True and (x == y) is False
```

**Line by line:** BadLow supplies a definitive False. Low declines and High handles the reflected comparison. The final ordering has no implementation, and the caught exception confirms that boundary. The equality assertions demonstrate a different fallback.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
premature False: False
Low declines
High accepts reflected comparison
Low declines
unsupported ordering: TypeError
```

The failing behavior is deliberate; subsequent assertions check the repair on these examples.
An executed Python model does not establish database behavior or production performance.

## In production

Document whether subclasses share your value semantics. Changing equality also requires
revisiting hashing; reuse the [hash/equality lesson](../../day-004-reverse-a-segment/lang_hash-and-equality/CONCEPTS.md)
before using custom values as keys. Optional depth: explicitly trace subclass priority and
verify a total ordering's transitivity instead of assuming dispatch guarantees it.

## Check yourself

### Readiness before practice

1. What information differs between False and NotImplemented?
2. Which method reflects __lt__?
3. What happens when both operands decline equality versus ordering?
4. Why is raising NotImplementedError the wrong way to decline an operand?

Use [README.md](README.md) for the assignment, verification, and personal evidence route.
Reading the lesson does not complete study.
