---
day: 22
track: lang-python
title: "Enum, IntEnum, auto, and match on enums"
theme: "Enums and sum types"
phase: "Languages: advanced features"
status: written
---

# Day 022 · Python — Enum, IntEnum, auto, and match on enums

**Today's theme:** Enums and sum types

**After today you can:** You can model one-of-three-states in each language and be told, at compile time or run time, when you miss one.

**The interviewer asks it as:** *How do you represent a fixed set of values?*

## 1. What this is, and why it matters

Enum gives distinct named members. IntEnum also behaves like an integer, which is useful for interoperability but weakens separation from numbers.

You use this when discussing enums and sum types in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Arun helps his sister organise a family lunch. Every invitation on her phone has one of three labels: waiting, accepted, or declined. At first, he writes whatever comes to mind. One cousin is marked yes, another coming, and another accepted. His sister cannot count the guests without asking him what each word means.

They agree to use only the three labels. Now everyone who helps knows what a label means. Waiting is different from declined. Someone who has not answered must not quietly disappear from the list of people they still need to ask.

An accepted invitation needs one more detail: how many people are coming. Arun keeps that number with the accepted reply. A declined invitation instead carries a short reason, such as being away that weekend. They do not put an empty guest count beside every declined reply and hope someone remembers why it is empty.

On Friday, a cousin sends a reply saying perhaps. Arun does not squeeze it into accepted just because it sounds hopeful. He asks his sister whether they need another label or whether it should remain waiting. That decision matters because the food order depends on it.

When the family later adds cancelled, they revisit each place where they count or display invitations. A new label needs a deliberate meaning everywhere it is used. Giving it a name is only the first step.

## 3. The idea in plain English

Arun’s agreed labels are **enumeration members**, the named values of an Enum. `auto()` assigns values so you do not have to number internal states manually. Those generated numbers should not silently become a stable wire format.

A dotted name such as `State.ACCEPTED` is a value pattern in match. The final branch raises if an unexpected object reaches the function. Ordinary Python does not check that every member appears in match. A static checker can help, but runtime validation still belongs at input boundaries. Enum names describe states; a dataclass or a union of dataclasses is needed when alternatives carry different payloads.

## 4. The picture

```text
reply -> waiting
      -> accepted + guest count
      -> declined + reason
```

Names describe alternatives; some alternatives also carry different data.

## 5. The code, built step by step

First isolate the important operation:

```python
case State.ACCEPTED:
    return "coming"
```

Use dotted enum names in patterns.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
from enum import Enum, IntEnum, auto

class State(Enum):
    WAITING = auto()
    ACCEPTED = auto()
    DECLINED = auto()

class WireCode(IntEnum):
    OK = 200

def describe(state: State) -> str:
    match state:
        case State.WAITING:
            return "waiting"
        case State.ACCEPTED:
            return "coming"
        case State.DECLINED:
            return "not coming"
        case _:
            raise ValueError("unknown state")

print(describe(State.ACCEPTED))
print(WireCode.OK == 200)
try:
    State(99)
except ValueError as error:
    print(type(error).__name__, str(error))
```

**Check the result:** Prints `coming`, `True`, and `ValueError 99 is not a valid State`.

## 6. How the other two languages do it

**Go**

```go
switch state {
case Accepted:
    return "accepted"
default:
    return "unknown"
}
```

A defined integer type with iota constants names states. Go still permits other values of that type, so boundary validation is explicit.

**C++**

```cpp
using Reply = std::variant<Waiting, Accepted, Declined>;
std::visit(Display{}, reply);
```

enum class names scoped values without implicit conversion to int. std::variant stores one of several alternative types and std::visit handles the active alternative.

Python Enum and Go typed constants name states but need deliberate handling of unknown values. C++ variant represents alternatives with different payload types; enum class alone only names values.

## 7. The traps

**Near-miss:** use a bare name such as `case ACCEPTED:`. It captures a value instead of comparing an enum member. Use State.ACCEPTED. Converting 99 raises `ValueError: 99 is not a valid State`; this is a useful boundary rejection, not a state to ignore.

## 8. Say it out loud

**How it gets asked:** “How do you represent a fixed set of values?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I use Enum for a closed vocabulary and validate external values during conversion. I use dotted enum members in match and give unexpected input an explicit failure path. IntEnum is appropriate when integer compatibility is required, but a plain Enum prevents accidental equivalence to a number. I keep stable external codes explicit and represent payload-bearing alternatives separately.

**Follow-ups**

1. **Does match check all members?** Not at runtime. Add a fallback or use a static checker to help audit missing branches.

2. **Why avoid auto for public numeric codes?** Adding or reordering members can change generated values.

3. **Can an enum hold a different guest count per invitation?** No. Store per-invitation payload in an instance such as a dataclass.

**Model answer:** Enum gives distinct named members. IntEnum also behaves like an integer, which is useful for interoperability but weakens separation from numbers. Named states do not automatically make every branch exhaustive.

## 9. Recall card

- Use dotted enum names in patterns.
- Enum conversion validates known values.
- IntEnum compares equal to compatible integers.
- Named states do not automatically make every branch exhaustive.

Further reading: [Official reference](https://docs.python.org/3.12/library/enum.html).
