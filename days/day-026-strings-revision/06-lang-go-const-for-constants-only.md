---
day: 26
track: lang-go
title: "const for constants only; immutability by convention"
theme: "Immutability"
phase: "Languages: advanced features"
status: written
---

# Day 026 · Go — const for constants only; immutability by convention

**Today's theme:** Immutability

**After today you can:** You can mark something unchangeable in each language and say who enforces it.

**The interviewer asks it as:** *How do you prevent a value from being modified?*

## 1. What this is, and why it matters

Go const applies to compile-time constants, not arbitrary structs or slices. Runtime immutability is usually enforced through ownership and API design.

You use this when discussing immutability in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Ravi prepares the guest list for a family meal. In the morning, everyone suggests changes. By noon the family agrees on the final count and sends it to the cook. Ravi labels that version final so nobody accidentally edits the number the cook is relying on.

His sister asks whether final means nobody can ever make a different list. Ravi says no. They can make another list for next week, or agree to send the cook a revised count. What they should not do is silently change the already agreed version while someone else is using it.

There is a complication. The list names three households, and each household has its own list of guests. Ravi prevents changes to the three household names, but his brother can still add people inside one household’s list. The total changes even though the outer list looks untouched. Ravi realises that protecting the cover does not protect everything inside it.

They settle on keeping the agreed names and counts together in a form nobody is supposed to edit. New requests produce a new version. The old version remains available so the cook can say exactly which count was used.

Before dinner, Ravi checks who can make changes and at which stage. Some rules are enforced by the way the list is stored. Others still depend on the family keeping its promise. He does not pretend those are the same kind of protection.

## 3. The idea in plain English

Ravi keeps the accepted list private and gives callers copies. **Encapsulation** hides representation behind operations. In Go, an unexported field is inaccessible from another package, but code in the same package can still modify it.

A value receiver copies the struct, not necessarily the data reached through slices or pointers. The constructor below copies its incoming slice, and Names copies on the way out. Those two boundaries prevent outside callers from changing the stored names through aliases. Each copy of n names takes O(n) time and O(n) additional slice storage. String contents are not copied because strings are immutable values.

## 4. The picture

```text
original value -> read-only view -> cannot edit through this view
      |
      +--------> another owner may still change nested data
```

Read-only access, fixed bindings, and deeply immutable values are different guarantees.

## 5. The code, built step by step

First isolate the important operation:

```go
return append([]string(nil), names...)
```

Copy mutable data at ownership boundaries when isolation is required.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import "fmt"

const MaxGuests = 3
type Plan struct{ names []string }
func NewPlan(names []string) Plan {
    return Plan{names: append([]string(nil), names...)}
}
func (p Plan) Names() []string { return append([]string(nil), p.names...) }
func main() {
    input := []string{"Ravi", "Mina"}
    plan := NewPlan(input)
    input[0] = "changed"
    output := plan.Names()
    output[1] = "changed too"
    fmt.Println(plan.Names(), MaxGuests)
}
```

**Check the result:** Prints `[Ravi Mina] 3` despite mutation of the input and returned slices.

## 6. How the other two languages do it

**Python**

```python
@dataclass(frozen=True)
class Plan:
    guests: tuple[str, ...]
```

A frozen dataclass rejects ordinary field assignment. tuple and frozenset are immutable containers; Final is a static-checker promise rather than runtime enforcement.

**C++**

```cpp
int guests() const { return count; }
```

const restricts modification through a qualified object or access path. constexpr permits constant evaluation; consteval requires it for immediate calls.

Python frozen dataclasses block normal field assignment, Go relies on API boundaries for ordinary runtime values, and C++ const restricts modification through a qualified access path. None automatically freezes every referenced object.

## 7. The traps

**Near-miss:** return p.names directly and callers can modify the stored elements. A value receiver alone does not fix this. Declaring `const names = []string{"Ravi"}` fails with a diagnostic ending `is not constant`; Go constants cannot hold slices. A copied slice of pointers would still share pointed-to objects.

## 8. Say it out loud

**How it gets asked:** “How do you prevent a value from being modified?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I do not call a Go runtime struct const. I define an API that owns its data, hides fields across the package boundary, and copies mutable inputs and outputs when isolation is required. The copy has a cost, so I weigh it against an ownership convention for internal code. A value receiver is not deep copying, and a slice of pointers requires another level of ownership reasoning.

**Follow-ups**

1. **Can a slice be const?** No. const is restricted to constant values, not runtime collections.

2. **Does a value receiver copy slice elements?** No. It copies the slice descriptor.

3. **Can code in the same package change unexported fields?** Yes. The package boundary, not the individual type, controls visibility.

**Model answer:** Go const applies to compile-time constants, not arbitrary structs or slices. Runtime immutability is usually enforced through ownership and API design. Read-only conventions must be supported by an ownership policy.

## 9. Recall card

- Copy mutable data at ownership boundaries when isolation is required.
- const is for compile-time constant values.
- Unexported fields are private to a package.
- Read-only conventions must be supported by an ownership policy.

Further reading: [Official reference](https://go.dev/ref/spec#Constants).
