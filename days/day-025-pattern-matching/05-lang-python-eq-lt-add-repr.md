---
day: 25
track: lang-python
title: "__eq__, __lt__, __add__, __repr__, __hash__"
theme: "Making your type behave like a built-in"
phase: "Languages: advanced features"
status: written
---

# Day 025 · Python — __eq__, __lt__, __add__, __repr__, __hash__

**Today's theme:** Making your type behave like a built-in

**After today you can:** You can make a Money type compare, print and sort correctly in each language.

**The interviewer asks it as:** *How would you make your type sortable?*

## 1. What this is, and why it matters

Special methods such as __eq__, __lt__, and __add__ connect user-defined values to familiar Python operations.

You use this when discussing making your type behave like a built-in in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Sara compares prices for three bags of rice. One costs eighty rupees, another sixty, and another eighty. She can put the sixty-rupee bag first without knowing anything else. The two eighty-rupee bags are equal in price even though they are different bags on different shelves.

Her brother adds the price of two bags and tells her the total. Sara expects the answer to remain an amount of money. She would be surprised if adding the prices changed one of the labels on the shelf, or returned the name of a shop instead. The familiar action carries a familiar promise.

They then visit another shop where a price is written in a different currency. Her brother starts comparing the bare numbers. Sara stops him. Eighty in one currency is not automatically more expensive than sixty in another. They need a shared unit or an explicit conversion before the comparison means anything.

Back at home, Sara saves the chosen prices on her phone. She wants them displayed in a way she can read, but also wants a detailed view that reveals the exact amounts if she checks the calculation later. A pleasant display and a precise record serve different purposes.

When she shows the list to her father, he can guess how comparing and adding should behave without learning special rules. Sara keeps those expectations intact. A familiar action should not hide a surprising change behind a friendly name.

## 3. The idea in plain English

Sara’s prices become immutable Money values storing integer cents. **Value equality** means equal contents count as equal even when objects differ. The dataclass generates equality, representation, ordering, and, because it is frozen, a compatible hash.

`__add__` returns a new value. `NotImplemented` tells Python that an operand combination is unsupported so another implementation may be tried. It is different from raising NotImplementedError. Equality and hashing must agree: equal values must have equal hashes. If fields used by the hash can change while an object is in a set, lookups become unreliable. Generated ordering compares fields in declaration order; here there is only one field.

## 4. The picture

```text
Money(80) + Money(60) -> Money(140)
Money(60) < Money(80) -> true
Money(80) == Money(80) -> true
```

Value operations should agree with the meaning of the type.

## 5. The code, built step by step

First isolate the important operation:

```python
def __add__(self, other: object) -> "Money":
    if not isinstance(other, Money):
        return NotImplemented
    return Money(self.cents + other.cents)
```

Return a new value for addition.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Money:
    cents: int

    def __add__(self, other: object) -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.cents + other.cents)

amounts = [Money(80), Money(60), Money(80)]
print(sorted(amounts))
print(Money(80) + Money(60))
print(len(set(amounts)))
```

**Check the result:** Prints `[Money(cents=60), Money(cents=80), Money(cents=80)]`, `Money(cents=140)`, and `2`.

## 6. How the other two languages do it

**Go**

```go
sort.Slice(amounts, func(i, j int) bool {
    return amounts[i].Cents < amounts[j].Cents
})
```

Go does not overload arithmetic operators for structs. Named methods, String, and comparison functions provide explicit value behaviour.

**C++**

```cpp
auto operator<=>(const Money&) const = default;
```

C++ operator overloads let a value support equality, ordering, addition, and stream output. Their meaning should follow ordinary expectations.

Python and C++ let user types define operators. Go uses named methods and comparison functions. All three still need a consistent equality and ordering policy.

## 7. The traps

**Near-miss:** define equality but leave identity-based hashing; equal amounts can occupy different hash buckets. Defining __eq__ normally disables inherited hashing unless supplied appropriately. `Money(1) + 2` raises `TypeError: unsupported operand type(s) for +: 'Money' and 'int'` because neither side accepts the pair.

## 8. Say it out loud

**How it gets asked:** “How would you make your type sortable?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I store money in integer minor units and define operations in terms of those units. Equality, ordering, addition, and representation should agree with the domain. I return a new value from addition and NotImplemented for unsupported operands. Frozen dataclasses can generate consistent equality and hashing when their fields are themselves suitable. I would add an explicit currency policy before comparing amounts from different currencies.

**Follow-ups**

1. **Why does hashing depend on equality?** Equal keys must land in compatible hash buckets so a lookup can find the existing entry.

2. **Is NotImplemented an exception?** No. It is a special return value for unsupported binary operations.

3. **Does frozen make nested data immutable?** No. Frozen blocks field assignment; contained mutable objects remain mutable.

**Model answer:** Special methods such as __eq__, __lt__, and __add__ connect user-defined values to familiar Python operations. An operator should preserve the expectations of its familiar notation.

## 9. Recall card

- Return a new value for addition.
- Equal objects must have equal hashes.
- Use NotImplemented for unsupported operands.
- An operator should preserve the expectations of its familiar notation.

Further reading: [Official reference](https://docs.python.org/3.12/reference/datamodel.html#special-method-names).
