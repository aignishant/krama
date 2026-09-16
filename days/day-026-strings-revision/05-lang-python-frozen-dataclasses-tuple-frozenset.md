---
day: 26
track: lang-python
title: "frozen dataclasses, tuple, frozenset, and Final"
theme: "Immutability"
phase: "Languages: advanced features"
status: written
---

# Day 026 · Python — frozen dataclasses, tuple, frozenset, and Final

**Today's theme:** Immutability

**After today you can:** You can mark something unchangeable in each language and say who enforces it.

**The interviewer asks it as:** *How do you prevent a value from being modified?*

## 1. What this is, and why it matters

A frozen dataclass rejects ordinary field assignment. tuple and frozenset are immutable containers; Final is a static-checker promise rather than runtime enforcement.

You use this when discussing immutability in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Ravi prepares the guest list for a family meal. In the morning, everyone suggests changes. By noon the family agrees on the final count and sends it to the cook. Ravi labels that version final so nobody accidentally edits the number the cook is relying on.

His sister asks whether final means nobody can ever make a different list. Ravi says no. They can make another list for next week, or agree to send the cook a revised count. What they should not do is silently change the already agreed version while someone else is using it.

There is a complication. The list names three households, and each household has its own list of guests. Ravi prevents changes to the three household names, but his brother can still add people inside one household’s list. The total changes even though the outer list looks untouched. Ravi realises that protecting the cover does not protect everything inside it.

They settle on keeping the agreed names and counts together in a form nobody is supposed to edit. New requests produce a new version. The old version remains available so the cook can say exactly which count was used.

Before dinner, Ravi checks who can make changes and at which stage. Some rules are enforced by the way the list is stored. Others still depend on the family keeping its promise. He does not pretend those are the same kind of protection.

## 3. The idea in plain English

Ravi’s agreed version becomes a frozen dataclass whose guests field is a tuple. **Shallow immutability** means the outer object is fixed but referenced objects may still change. A tuple containing a list illustrates that limit.

Final marks a binding that a type checker should not allow to be reassigned. It does not make a list immutable and Python does not enforce it at runtime. Frozen dataclasses likewise are an API guarantee, not a security boundary against deliberate object.__setattr__ use. Choose immutable contents when values must be safely shared as snapshots.

## 4. The picture

```text
original value -> read-only view -> cannot edit through this view
      |
      +--------> another owner may still change nested data
```

Read-only access, fixed bindings, and deeply immutable values are different guarantees.

## 5. The code, built step by step

First isolate the important operation:

```python
@dataclass(frozen=True)
class Plan:
    guests: tuple[str, ...]
```

Choose immutable contents for stable snapshots.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
from dataclasses import FrozenInstanceError, dataclass, replace
from typing import Final

@dataclass(frozen=True)
class Plan:
    guests: tuple[str, ...]

LIMIT: Final[int] = 3
original = Plan(("Ravi", "Mina"))
updated = replace(original, guests=original.guests + ("Dev",))
print(len(original.guests), len(updated.guests), LIMIT)
print(len(frozenset(("Ravi", "Ravi"))))
try:
    original.guests = ()
except FrozenInstanceError as error:
    print(type(error).__name__, str(error))
```

**Check the result:** Prints `2 3 3`, `1`, and `FrozenInstanceError cannot assign to field 'guests'`.

## 6. How the other two languages do it

**Go**

```go
return append([]string(nil), names...)
```

Go const applies to compile-time constants, not arbitrary structs or slices. Runtime immutability is usually enforced through ownership and API design.

**C++**

```cpp
int guests() const { return count; }
```

const restricts modification through a qualified object or access path. constexpr permits constant evaluation; consteval requires it for immediate calls.

Python frozen dataclasses block normal field assignment, Go relies on API boundaries for ordinary runtime values, and C++ const restricts modification through a qualified access path. None automatically freezes every referenced object.

## 7. The traps

**Near-miss:** a frozen dataclass with a list field still permits list.append. The shown assignment fails with `dataclasses.FrozenInstanceError: cannot assign to field 'guests'`. Rebinding a Final name does not produce that runtime exception; a static checker reports it instead.

## 8. Say it out loud

**How it gets asked:** “How do you prevent a value from being modified?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I distinguish a fixed binding from a fixed value. Final helps a static checker reject rebinding, while a frozen dataclass rejects ordinary field writes at runtime. I choose immutable nested contents when I need a stable snapshot and use replace to produce an updated value. A tuple of mutable objects does not give deep immutability, so I inspect the entire reachable data I plan to share.

**Follow-ups**

1. **Can a tuple contain a mutable list?** Yes. The tuple cannot replace its element, but the list itself can change.

2. **Who enforces Final?** A static type checker, not ordinary Python execution.

3. **How do you update a frozen record?** Create a new record, for example with dataclasses.replace.

**Model answer:** A frozen dataclass rejects ordinary field assignment. tuple and frozenset are immutable containers; Final is a static-checker promise rather than runtime enforcement. An immutable outer object does not freeze everything it references.

## 9. Recall card

- Choose immutable contents for stable snapshots.
- Frozen blocks ordinary field assignment.
- Final constrains rebinding in static analysis.
- An immutable outer object does not freeze everything it references.

Further reading: [Official reference](https://docs.python.org/3.12/library/dataclasses.html#frozen-instances).
