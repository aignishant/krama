---
day: 23
track: lang-cpp
title: "std::optional, nullptr, and value_or"
theme: "Nothing, safely"
phase: "Languages: advanced features"
status: written
---

# Day 023 · C++ — std::optional, nullptr, and value_or

**Today's theme:** Nothing, safely

**After today you can:** You can express 'maybe no value' in each language and say what happens when you forget to check.

**The interviewer asks it as:** *How does your language represent the absence of a value?*

## 1. What this is, and why it matters

std::optional<T> owns either a T or no value. nullptr is a null pointer literal; it is not a general replacement for an absent integer.

You use this when discussing nothing, safely in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Nila checks how many guests want tea. Her aunt answers zero because she has already had some. Her cousin has not answered at all. At first Nila puts zero beside both names. When her father asks whether everyone has replied, she says yes. Then her cousin arrives expecting two cups.

They look at the list together. Zero was a real answer from the aunt. No answer was a different situation. Nila removes the number beside her cousin’s name and marks it as unanswered. Now she knows whom to ask again, and she can still add up the replies she actually received.

Later, she asks how much sugar each person wants. Someone says none. That is another real answer, not a reason to use the usual two spoons. Nila learns to check whether an answer exists before deciding what it says. She does not replace every answer that looks small with a familiar choice.

Her father suggests a household rule: when nobody has replied, prepare one spare cup. Nila writes that rule separately. It is a decision about missing information, not a claim that the missing answer was one all along.

Before pouring, she reads the list aloud. Each entry is either a known amount or a question still waiting for an answer. The distinction prevents both wasted tea and an empty cup for a guest.

## 3. The idea in plain English

Nila’s amount becomes optional<int>. **Engaged** means the optional contains a value. Its boolean conversion tests engagement, so optional<int>{0} is true in a condition. It does not test whether the integer is nonzero.

`value_or(1)` selects a fallback. `value()` throws on absence, while dereferencing an empty optional violates its precondition and must not be used as a check. Optional stores its value within itself; it does not require a separate heap allocation for an int. A pointer is a better fit when referring to an existing object with a separately managed lifetime.

## 4. The picture

```text
lookup -> present: 0 cups -> use 0
       -> absent          -> ask or apply explicit default
```

Zero is data. Absence needs its own representation.

## 5. The code, built step by step

First isolate the important operation:

```cpp
if (amount) {
    std::cout << *amount;
}
```

Test engagement before dereferencing.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <iostream>
#include <optional>
#include <string_view>

std::optional<int> lookup(std::string_view name) {
    if (name == "aunt") return 0;
    return std::nullopt;
}
int main() {
    auto amount = lookup("aunt");
    if (amount) std::cout << *amount << '\n';
    std::cout << lookup("unknown").value_or(1) << '\n';
    int* address = nullptr;
    std::cout << std::boolalpha << (address == nullptr) << '\n';
}
```

**Check the result:** Prints `0`, `1`, and `true`.

## 6. How the other two languages do it

**Python**

```python
if (amount := lookup("aunt")) is not None:
    print(amount)
```

None is a singleton used for absence. Optional[T] means T | None; it does not mean that a function argument may be omitted.

**Go**

```go
amount, ok := counts["aunt"]
fmt.Println(amount, ok)
```

Go has zero values and nil for certain types. A map lookup needs the comma-ok result when zero and absence must differ.

Python uses None, Go often pairs a value with a boolean, and C++ optional packages presence with a value. A null pointer concerns an object address, not every kind of missing result.

## 7. The traps

**Near-miss:** use zero as a sentinel and then reject a valid zero result. An empty optional’s value() throws `std::bad_optional_access`; what() text depends on the library. Dereferencing an empty optional is not a portable way to get that exception. Also, the argument to value_or is evaluated even when the optional is engaged.

## 8. Say it out loud

**How it gets asked:** “How does your language represent the absence of a value?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I return optional<int> when an integer may be absent. The presence test is independent of the integer value, so zero survives. I either branch on engagement or provide a deliberate fallback. I use value only when an exception is the desired failure contract. A nullable pointer answers a different question: it refers to an object that may not exist and whose lifetime must still be valid.

**Follow-ups**

1. **Is optional containing zero false?** No. Its presence test is true.

2. **Does optional<int> allocate separately?** No. The contained value is stored within the optional.

3. **Is value_or lazy?** No. Its argument is evaluated before the call; branch explicitly for an expensive fallback.

**Model answer:** std::optional<T> owns either a T or no value. nullptr is a null pointer literal; it is not a general replacement for an absent integer. A present zero must survive a presence check.

## 9. Recall card

- Test engagement before dereferencing.
- nullopt represents an empty optional.
- nullptr represents a null pointer.
- A present zero must survive a presence check.

Further reading: [Official reference](https://eel.is/c++draft/optional).
