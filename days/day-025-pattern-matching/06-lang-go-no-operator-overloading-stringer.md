---
day: 25
track: lang-go
title: "No operator overloading: Stringer, sort.Slice, and cmp"
theme: "Making your type behave like a built-in"
phase: "Languages: advanced features"
status: written
---

# Day 025 · Go — No operator overloading: Stringer, sort.Slice, and cmp

**Today's theme:** Making your type behave like a built-in

**After today you can:** You can make a Money type compare, print and sort correctly in each language.

**The interviewer asks it as:** *How would you make your type sortable?*

## 1. What this is, and why it matters

Go does not overload arithmetic operators for structs. Named methods, String, and comparison functions provide explicit value behaviour.

You use this when discussing making your type behave like a built-in in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Sara compares prices for three bags of rice. One costs eighty rupees, another sixty, and another eighty. She can put the sixty-rupee bag first without knowing anything else. The two eighty-rupee bags are equal in price even though they are different bags on different shelves.

Her brother adds the price of two bags and tells her the total. Sara expects the answer to remain an amount of money. She would be surprised if adding the prices changed one of the labels on the shelf, or returned the name of a shop instead. The familiar action carries a familiar promise.

They then visit another shop where a price is written in a different currency. Her brother starts comparing the bare numbers. Sara stops him. Eighty in one currency is not automatically more expensive than sixty in another. They need a shared unit or an explicit conversion before the comparison means anything.

Back at home, Sara saves the chosen prices on her phone. She wants them displayed in a way she can read, but also wants a detailed view that reveals the exact amounts if she checks the calculation later. A pleasant display and a precise record serve different purposes.

When she shows the list to her father, he can guess how comparing and adding should behave without learning special rules. Sara keeps those expectations intact. A familiar action should not hide a surprising change behind a friendly name.

## 3. The idea in plain English

The price is a Money struct with an integer field. `Add` constructs a new amount. String controls fmt’s readable representation. `sort.Slice` takes a **less function**, which answers whether one element belongs before another.

A less function must be consistent: equal amounts should not be less than each other. `cmp.Compare` returns negative, zero, or positive and is convenient for three-way comparisons. A struct is comparable when all its fields are comparable, so this Money can be a map key. A struct containing a slice cannot. Sorting k amounts uses O(k log k) comparisons in the general case, rather than changing the cost of integer comparison itself.

## 4. The picture

```text
Money(80) + Money(60) -> Money(140)
Money(60) < Money(80) -> true
Money(80) == Money(80) -> true
```

Value operations should agree with the meaning of the type.

## 5. The code, built step by step

First isolate the important operation:

```go
sort.Slice(amounts, func(i, j int) bool {
    return amounts[i].Cents < amounts[j].Cents
})
```

Use a strict less function for sorting.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import (
    "cmp"
    "fmt"
    "sort"
)
type Money struct{ Cents int64 }
func (m Money) Add(other Money) Money { return Money{m.Cents + other.Cents} }
func (m Money) String() string { return fmt.Sprintf("%d cents", m.Cents) }
func main() {
    amounts := []Money{{80}, {60}, {80}}
    sort.Slice(amounts, func(i, j int) bool { return amounts[i].Cents < amounts[j].Cents })
    fmt.Println(amounts)
    fmt.Println(Money{80}.Add(Money{60}))
    fmt.Println(cmp.Compare(int64(60), int64(80)))
}
```

**Check the result:** Prints `[60 cents 80 cents 80 cents]`, `140 cents`, and `-1`.

## 6. How the other two languages do it

**Python**

```python
def __add__(self, other: object) -> "Money":
    if not isinstance(other, Money):
        return NotImplemented
    return Money(self.cents + other.cents)
```

Special methods such as __eq__, __lt__, and __add__ connect user-defined values to familiar Python operations.

**C++**

```cpp
auto operator<=>(const Money&) const = default;
```

C++ operator overloads let a value support equality, ordering, addition, and stream output. Their meaning should follow ordinary expectations.

Python and C++ let user types define operators. Go uses named methods and comparison functions. All three still need a consistent equality and ordering policy.

## 7. The traps

**Near-miss:** use <= in the less function; equality no longer satisfies the required ordering contract. Trying to add two Money structs with + is a compile error reporting that the operator is not defined on Money; exact wording depends on Go. Fixed-width integer addition can also overflow, so production money arithmetic needs bounds checks.

## 8. Say it out loud

**How it gets asked:** “How would you make your type sortable?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I keep the operations explicit: Add returns a new value, String prints it, and a less function tells the sort package how to order it. I use strictly less than, not less than or equal. Struct equality works for comparable fields, and that also permits map keys. I still define currency and overflow policies; the syntax does not supply those domain guarantees.

**Follow-ups**

1. **Can a struct customise +?** No. Define a named method or function.

2. **Why not <= in sorting?** An item must not compare less than itself; equality must be handled consistently.

3. **Can every struct be a map key?** No. All fields must be comparable; a slice field prevents comparability.

**Model answer:** Go does not overload arithmetic operators for structs. Named methods, String, and comparison functions provide explicit value behaviour. Named methods make Go’s custom arithmetic explicit.

## 9. Recall card

- Use a strict less function for sorting.
- String controls readable formatting.
- Comparable structs can be map keys.
- Named methods make Go’s custom arithmetic explicit.

Further reading: [Official reference](https://pkg.go.dev/sort#Slice).
