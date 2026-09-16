---
day: 26
track: lang-cpp
title: "const, constexpr, consteval, and const-correct methods"
theme: "Immutability"
phase: "Languages: advanced features"
status: written
---

# Day 026 · C++ — const, constexpr, consteval, and const-correct methods

**Today's theme:** Immutability

**After today you can:** You can mark something unchangeable in each language and say who enforces it.

**The interviewer asks it as:** *How do you prevent a value from being modified?*

## 1. What this is, and why it matters

const restricts modification through a qualified object or access path. constexpr permits constant evaluation; consteval requires it for immediate calls.

You use this when discussing immutability in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Ravi prepares the guest list for a family meal. In the morning, everyone suggests changes. By noon the family agrees on the final count and sends it to the cook. Ravi labels that version final so nobody accidentally edits the number the cook is relying on.

His sister asks whether final means nobody can ever make a different list. Ravi says no. They can make another list for next week, or agree to send the cook a revised count. What they should not do is silently change the already agreed version while someone else is using it.

There is a complication. The list names three households, and each household has its own list of guests. Ravi prevents changes to the three household names, but his brother can still add people inside one household’s list. The total changes even though the outer list looks untouched. Ravi realises that protecting the cover does not protect everything inside it.

They settle on keeping the agreed names and counts together in a form nobody is supposed to edit. New requests produce a new version. The old version remains available so the cook can say exactly which count was used.

Before dinner, Ravi checks who can make changes and at which stage. Some rules are enforced by the way the list is stored. Others still depend on the family keeping its promise. He does not pretend those are the same kind of protection.

## 3. The idea in plain English

Ravi’s final count is a const object. A **const member function** promises not to modify ordinary data members through this. It lets callers read a const instance. Mutable members are an explicit exception and should have a clear purpose.

`constexpr` functions can run during compilation when used in a constant-expression context; they can also run at runtime. `consteval` functions require constant evaluation. Neither keyword means every value reachable through a pointer becomes immutable. A const pointer cannot be reseated; a pointer to const cannot modify its pointee through that pointer.

## 4. The picture

```text
original value -> read-only view -> cannot edit through this view
      |
      +--------> another owner may still change nested data
```

Read-only access, fixed bindings, and deeply immutable values are different guarantees.

## 5. The code, built step by step

First isolate the important operation:

```cpp
int guests() const { return count; }
```

Mark read-only member functions const.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <iostream>

constexpr int double_count(int value) { return value * 2; }
consteval int fixed_limit() { return 6; }
class Plan {
    int count;
public:
    explicit constexpr Plan(int value) : count(value) {}
    int guests() const { return count; }
};
int main() {
    constexpr int limit = fixed_limit();
    const Plan plan(double_count(2));
    std::cout << plan.guests() << ' ' << limit << '\n';
    int original = 2;
    const int* view = &original;
    original = 3;
    std::cout << *view << '\n';
}
```

**Check the result:** Prints `4 6` and `3`. A const access path did not freeze the separately mutable original.

## 6. How the other two languages do it

**Python**

```python
@dataclass(frozen=True)
class Plan:
    guests: tuple[str, ...]
```

A frozen dataclass rejects ordinary field assignment. tuple and frozenset are immutable containers; Final is a static-checker promise rather than runtime enforcement.

**Go**

```go
return append([]string(nil), names...)
```

Go const applies to compile-time constants, not arbitrary structs or slices. Runtime immutability is usually enforced through ownership and API design.

Python frozen dataclasses block normal field assignment, Go relies on API boundaries for ordinary runtime values, and C++ const restricts modification through a qualified access path. None automatically freezes every referenced object.

## 7. The traps

**Near-miss:** assume const int* proves nobody can change the integer. Another mutable alias can. Attempting `*view = 4` fails to compile with a diagnostic about assignment to a read-only location; exact wording varies. Casting away const and modifying an object originally defined const is undefined behaviour.

## 8. Say it out loud

**How it gets asked:** “How do you prevent a value from being modified?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I use const to communicate which access paths may modify data and mark read-only member functions accordingly. I use constexpr when a value or operation should support constant evaluation and consteval when it must happen there. I still inspect pointer ownership: const on one view does not remove other mutable aliases. For stable shared values, I combine const-correct access with controlled construction and ownership.

**Follow-ups**

1. **Is constexpr always executed at compile time?** No. A constexpr function can run at runtime outside a required constant-expression context.

2. **What does consteval add?** An immediate invocation must be a constant expression.

3. **Does const on a pointer freeze its target?** Only const on the pointee restricts writes through that pointer; other aliases may still modify it.

**Model answer:** const restricts modification through a qualified object or access path. constexpr permits constant evaluation; consteval requires it for immediate calls. Const access and globally immutable state are different guarantees.

## 9. Recall card

- Mark read-only member functions const.
- constexpr supports constant evaluation.
- consteval requires immediate constant evaluation.
- Const access and globally immutable state are different guarantees.

Further reading: [Official reference](https://eel.is/c++draft/dcl.constexpr).
