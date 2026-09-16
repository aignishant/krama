---
day: 25
track: lang-cpp
title: "operator==, operator<=>, operator<<, and the rule of least surprise"
theme: "Making your type behave like a built-in"
phase: "Languages: advanced features"
status: written
---

# Day 025 · C++ — operator==, operator<=>, operator<<, and the rule of least surprise

**Today's theme:** Making your type behave like a built-in

**After today you can:** You can make a Money type compare, print and sort correctly in each language.

**The interviewer asks it as:** *How would you make your type sortable?*

## 1. What this is, and why it matters

C++ operator overloads let a value support equality, ordering, addition, and stream output. Their meaning should follow ordinary expectations.

You use this when discussing making your type behave like a built-in in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Sara compares prices for three bags of rice. One costs eighty rupees, another sixty, and another eighty. She can put the sixty-rupee bag first without knowing anything else. The two eighty-rupee bags are equal in price even though they are different bags on different shelves.

Her brother adds the price of two bags and tells her the total. Sara expects the answer to remain an amount of money. She would be surprised if adding the prices changed one of the labels on the shelf, or returned the name of a shop instead. The familiar action carries a familiar promise.

They then visit another shop where a price is written in a different currency. Her brother starts comparing the bare numbers. Sara stops him. Eighty in one currency is not automatically more expensive than sixty in another. They need a shared unit or an explicit conversion before the comparison means anything.

Back at home, Sara saves the chosen prices on her phone. She wants them displayed in a way she can read, but also wants a detailed view that reveals the exact amounts if she checks the calculation later. A pleasant display and a precise record serve different purposes.

When she shows the list to her father, he can guess how comparing and adding should behave without learning special rules. Sara keeps those expectations intact. A familiar action should not hide a surprising change behind a friendly name.

## 3. The idea in plain English

Money stores integer cents. The **three-way comparison operator** `<=>` can generate ordering relationships; a defaulted version compares members in declaration order. A defaulted spaceship operator also supports generated equality under the language’s rules.

The stream operator returns the same stream so `out << first << second` can chain. Addition returns a new Money rather than changing either input. For this single-field value, comparisons are constant-time; sorting three amounts requires only a few such comparisons. Production arithmetic must handle overflow before adding signed integers, because signed overflow is undefined behaviour.

## 4. The picture

```text
Money(80) + Money(60) -> Money(140)
Money(60) < Money(80) -> true
Money(80) == Money(80) -> true
```

Value operations should agree with the meaning of the type.

## 5. The code, built step by step

First isolate the important operation:

```cpp
auto operator<=>(const Money&) const = default;
```

Defaulted comparisons follow member order.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <algorithm>
#include <compare>
#include <iostream>
#include <vector>

struct Money {
    long long cents;
    auto operator<=>(const Money&) const = default;
    Money operator+(const Money& other) const { return {cents + other.cents}; }
};
std::ostream& operator<<(std::ostream& out, const Money& value) {
    return out << value.cents << " cents";
}
int main() {
    std::vector<Money> amounts{{80}, {60}, {80}};
    std::sort(amounts.begin(), amounts.end());
    for (const auto& value : amounts) std::cout << value << '\n';
    std::cout << (Money{80} + Money{60}) << '\n';
}
```

**Check the result:** Prints `60 cents`, `80 cents`, `80 cents`, and `140 cents`.

## 6. How the other two languages do it

**Python**

```python
def __add__(self, other: object) -> "Money":
    if not isinstance(other, Money):
        return NotImplemented
    return Money(self.cents + other.cents)
```

Special methods such as __eq__, __lt__, and __add__ connect user-defined values to familiar Python operations.

**Go**

```go
sort.Slice(amounts, func(i, j int) bool {
    return amounts[i].Cents < amounts[j].Cents
})
```

Go does not overload arithmetic operators for structs. Named methods, String, and comparison functions provide explicit value behaviour.

Python and C++ let user types define operators. Go uses named methods and comparison functions. All three still need a consistent equality and ordering policy.

## 7. The traps

**Near-miss:** make operator+ modify the left operand; callers expect addition to leave inputs intact. A Money type with comparison operators still has no automatic std::hash specialisation. Trying unordered_set<Money> without a hasher fails to compile; diagnostics vary. Provide a hash consistent with equality when hash containers are needed.

## 8. Say it out loud

**How it gets asked:** “How would you make your type sortable?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I use defaulted comparisons when memberwise ordering matches the domain. Addition returns a value, and stream insertion returns the stream for chaining. I avoid surprising side effects and make units explicit. Comparison support does not automatically create hashing support. I also state bounds on arithmetic because C++ signed overflow is undefined, even when the overloaded operator looks like familiar integer addition.

**Follow-ups**

1. **Does <=> provide a hash?** No. Unordered containers need a separate compatible hasher.

2. **Why return ostream&?** It supports chained output and preserves the original stream.

3. **When is memberwise ordering wrong?** When field order or domain rules differ from lexicographic member order, such as incomparable currencies.

**Model answer:** C++ operator overloads let a value support equality, ordering, addition, and stream output. Their meaning should follow ordinary expectations. Familiar operators should not hide surprising mutation.

## 9. Recall card

- Defaulted comparisons follow member order.
- Return the stream from operator<<.
- Hashing must agree with equality.
- Familiar operators should not hide surprising mutation.

Further reading: [Official reference](https://eel.is/c++draft/class.compare.default).
