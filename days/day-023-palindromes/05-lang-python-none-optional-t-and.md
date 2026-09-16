---
day: 23
track: lang-python
title: "None, Optional[T], and the walrus operator"
theme: "Nothing, safely"
phase: "Languages: advanced features"
status: written
---

# Day 023 · Python — None, Optional[T], and the walrus operator

**Today's theme:** Nothing, safely

**After today you can:** You can express 'maybe no value' in each language and say what happens when you forget to check.

**The interviewer asks it as:** *How does your language represent the absence of a value?*

## 1. What this is, and why it matters

None is a singleton used for absence. Optional[T] means T | None; it does not mean that a function argument may be omitted.

You use this when discussing nothing, safely in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Nila checks how many guests want tea. Her aunt answers zero because she has already had some. Her cousin has not answered at all. At first Nila puts zero beside both names. When her father asks whether everyone has replied, she says yes. Then her cousin arrives expecting two cups.

They look at the list together. Zero was a real answer from the aunt. No answer was a different situation. Nila removes the number beside her cousin’s name and marks it as unanswered. Now she knows whom to ask again, and she can still add up the replies she actually received.

Later, she asks how much sugar each person wants. Someone says none. That is another real answer, not a reason to use the usual two spoons. Nila learns to check whether an answer exists before deciding what it says. She does not replace every answer that looks small with a familiar choice.

Her father suggests a household rule: when nobody has replied, prepare one spare cup. Nila writes that rule separately. It is a decision about missing information, not a claim that the missing answer was one all along.

Before pouring, she reads the list aloud. Each entry is either a known amount or a question still waiting for an answer. The distinction prevents both wasted tea and an empty cup for a guest.

## 3. The idea in plain English

Nila’s unanswered entry becomes None. Use **identity**, written `is`, to check this singleton. A zero count is false in a condition but is still a present value. An empty string and an empty collection have the same trap.

The **walrus operator** `:=` assigns a value inside an expression. Parentheses in `(amount := lookup(...)) is not None` make the presence test explicit. A type annotation documents that a caller must handle absence; Python does not enforce the annotation at runtime. Supplying a default argument and accepting None are independent choices.

## 4. The picture

```text
lookup -> present: 0 cups -> use 0
       -> absent          -> ask or apply explicit default
```

Zero is data. Absence needs its own representation.

## 5. The code, built step by step

First isolate the important operation:

```python
if (amount := lookup("aunt")) is not None:
    print(amount)
```

Check is not None before using a possibly absent result.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
from typing import Optional

def lookup(name: str) -> Optional[int]:
    counts = {"aunt": 0, "cousin": 2}
    return counts.get(name)

def with_default(value: int | None, default: int) -> int:
    return default if value is None else value

if (amount := lookup("aunt")) is not None:
    print(amount)
print(with_default(lookup("unknown"), 1))
print(with_default(lookup("aunt"), 1))
```

**Check the result:** Prints `0`, `1`, and `0`.

## 6. How the other two languages do it

**Go**

```go
amount, ok := counts["aunt"]
fmt.Println(amount, ok)
```

Go has zero values and nil for certain types. A map lookup needs the comma-ok result when zero and absence must differ.

**C++**

```cpp
if (amount) {
    std::cout << *amount;
}
```

std::optional<T> owns either a T or no value. nullptr is a null pointer literal; it is not a general replacement for an absent integer.

Python uses None, Go often pairs a value with a boolean, and C++ optional packages presence with a value. A null pointer concerns an object address, not every kind of missing result.

## 7. The traps

**Near-miss:** `lookup("aunt") or 1` incorrectly returns 1. Check is None. Trying `None + 1` raises `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'`. Narrow the result before arithmetic.

## 8. Say it out loud

**How it gets asked:** “How does your language represent the absence of a value?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I use a union with None for a possibly missing result and check it with is None. I preserve zero, false, and empty values rather than confusing them with absence. Optional is an annotation, not runtime validation and not a default argument. If the caller chooses a fallback, that policy is explicit. The walrus operator can save a repeated lookup, provided the test still distinguishes presence from truthiness.

**Follow-ups**

1. **Is zero missing?** No. It is a valid integer, so use an explicit None check.

2. **Does Optional make an argument optional?** No. A default value in the signature does that.

3. **What if None is itself valid data?** Use a unique sentinel object or a result object with a separate presence field.

**Model answer:** None is a singleton used for absence. Optional[T] means T | None; it does not mean that a function argument may be omitted. Choose a fallback only after proving absence.

## 9. Recall card

- Check is not None before using a possibly absent result.
- Optional[T] is T | None.
- Truthiness discards valid zero and empty values.
- Choose a fallback only after proving absence.

Further reading: [Official reference](https://docs.python.org/3.12/library/typing.html#typing.Optional).
