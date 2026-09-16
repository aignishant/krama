---
day: 23
track: lang-go
title: "nil, zero values, and the nil-interface trap"
theme: "Nothing, safely"
phase: "Languages: advanced features"
status: written
---

# Day 023 · Go — nil, zero values, and the nil-interface trap

**Today's theme:** Nothing, safely

**After today you can:** You can express 'maybe no value' in each language and say what happens when you forget to check.

**The interviewer asks it as:** *How does your language represent the absence of a value?*

## 1. What this is, and why it matters

Go has zero values and nil for certain types. A map lookup needs the comma-ok result when zero and absence must differ.

You use this when discussing nothing, safely in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Nila checks how many guests want tea. Her aunt answers zero because she has already had some. Her cousin has not answered at all. At first Nila puts zero beside both names. When her father asks whether everyone has replied, she says yes. Then her cousin arrives expecting two cups.

They look at the list together. Zero was a real answer from the aunt. No answer was a different situation. Nila removes the number beside her cousin’s name and marks it as unanswered. Now she knows whom to ask again, and she can still add up the replies she actually received.

Later, she asks how much sugar each person wants. Someone says none. That is another real answer, not a reason to use the usual two spoons. Nila learns to check whether an answer exists before deciding what it says. She does not replace every answer that looks small with a familiar choice.

Her father suggests a household rule: when nobody has replied, prepare one spare cup. Nila writes that rule separately. It is a decision about missing information, not a claim that the missing answer was one all along.

Before pouring, she reads the list aloud. Each entry is either a known amount or a question still waiting for an answer. The distinction prevents both wasted tea and an empty cup for a guest.

## 3. The idea in plain English

An int cannot be nil. A map lookup returns zero when the key is absent, so `amount, ok := counts[name]` supplies a separate presence flag. Pointers, maps, slices, functions, channels, and interfaces can be nil, but their behaviour differs.

An **interface value** contains a dynamic type and a dynamic value. A nil *Guest assigned to any retains the dynamic type *Guest. The resulting interface is not nil. This also explains why returning a typed nil pointer as error can accidentally signal a failure. Return a plain nil interface when you mean no error.

## 4. The picture

```text
lookup -> present: 0 cups -> use 0
       -> absent          -> ask or apply explicit default
```

Zero is data. Absence needs its own representation.

## 5. The code, built step by step

First isolate the important operation:

```go
amount, ok := counts["aunt"]
fmt.Println(amount, ok)
```

Keep the comma-ok flag when zero is valid data.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import "fmt"

type Guest struct{ Name string }

func main() {
    counts := map[string]int{"aunt": 0}
    amount, ok := counts["aunt"]
    fmt.Println(amount, ok)
    amount, ok = counts["unknown"]
    fmt.Println(amount, ok)
    var guest *Guest
    var wrapped any = guest
    fmt.Println(guest == nil, wrapped == nil)
}
```

**Check the result:** Prints `0 true`, `0 false`, and `true false`.

## 6. How the other two languages do it

**Python**

```python
if (amount := lookup("aunt")) is not None:
    print(amount)
```

None is a singleton used for absence. Optional[T] means T | None; it does not mean that a function argument may be omitted.

**C++**

```cpp
if (amount) {
    std::cout << *amount;
}
```

std::optional<T> owns either a T or no value. nullptr is a null pointer literal; it is not a general replacement for an absent integer.

Python uses None, Go often pairs a value with a boolean, and C++ optional packages presence with a value. A null pointer concerns an object address, not every kind of missing result.

## 7. The traps

**Near-miss:** test only amount == 0 and lose the distinction between the first two outputs. Writing to `var counts map[string]int` before allocating it panics with `assignment to entry in nil map`. Reading that nil map is allowed and returns the zero value with ok false.

## 8. Say it out loud

**How it gets asked:** “How does your language represent the absence of a value?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I choose absence according to the API. For a map, I keep the comma-ok boolean. For a pointer, I check nil before dereferencing. For an interface, I remember that a typed nil pointer still leaves a dynamic type inside the interface. I therefore return plain nil on successful error-returning paths. Zero values are useful defaults but they do not tell me whether an external value was supplied.

**Follow-ups**

1. **Can an int be nil?** No. Pair it with a boolean, use a pointer, or define a result type.

2. **Can a nil slice be appended to?** Yes. append can allocate its backing storage.

3. **Is a typed nil pointer inside an interface nil?** No. The interface retains the concrete type.

**Model answer:** Go has zero values and nil for certain types. A map lookup needs the comma-ok result when zero and absence must differ. Zero values and missing values are separate API decisions.

## 9. Recall card

- Keep the comma-ok flag when zero is valid data.
- An interface is nil only when both type and value are absent.
- Nil maps can be read but not written.
- Zero values and missing values are separate API decisions.

Further reading: [Official reference](https://go.dev/doc/faq#nil_error).
