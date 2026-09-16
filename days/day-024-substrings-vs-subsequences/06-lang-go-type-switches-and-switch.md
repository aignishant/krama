---
day: 24
track: lang-go
title: "Type switches and switch on values"
theme: "Pattern matching"
phase: "Languages: advanced features"
status: written
---

# Day 024 · Go — Type switches and switch on values

**Today's theme:** Pattern matching

**After today you can:** You can branch on the shape of data in each language.

**The interviewer asks it as:** *How do you handle a value that could be one of several types?*

## 1. What this is, and why it matters

A type switch inspects the dynamic type of an interface value. A value switch compares values and does not fall through by default.

You use this when discussing pattern matching in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Dev sorts deliveries for a family gathering. A box of fruit goes to the kitchen. A bag of clothes goes to the spare room. A small envelope goes to his aunt. He could inspect everything in exactly the same way, but the outside of each delivery already tells him which questions to ask.

For fruit, he checks whether it needs to stay cool. For clothes, he checks whose name is on the bag. For an envelope, he checks whether his aunt is home. The first decision narrows the next decision. Asking whether an envelope needs washing would not help anyone.

One afternoon a box arrives with a picture of fruit on it, but inside are cups. Dev stops relying on the picture alone. He checks what is actually there before carrying it into the kitchen. The label is a useful clue, not a guarantee.

His sister adds another instruction: small fruit boxes can go on the shelf, but heavy ones must stay on the floor. Dev first recognises the kind of delivery, then checks its weight. Both facts matter. A heavy box must not take the small-box route merely because both contain fruit.

Finally, something arrives that neither of them recognises. They leave it beside the door and ask the person who ordered it. A deliberate place for the unknown delivery is better than quietly treating it as something familiar and sending it to the wrong room.

## 3. The idea in plain English

Dev’s initial recognition becomes `switch value := command.(type)`. Inside each case, value has the selected concrete type. This is different from switching on a string field; a type switch selects a representation before its fields are accessed.

Go has no direct structural-pattern syntax. Conditions inside the branch perform the guard’s work. The default branch keeps unknown types visible. Switching on an interface makes an open set of alternatives: another type may be added elsewhere, and the compiler does not demand a new case.

## 4. The picture

```text
input -> recognise shape/type -> extract fields -> check condition -> action
                    unknown -------------------------------------> reject
```

Recognise the alternative before interpreting its fields.

## 5. The code, built step by step

First isolate the important operation:

```go
switch value := command.(type) {
case Move:
    return fmt.Sprintf("move %d", value.Steps)
}
```

A type switch narrows an interface’s dynamic type.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import "fmt"

type Move struct{ Steps int }
type Stop struct{}

func describe(command any) (string, error) {
    switch value := command.(type) {
    case Move:
        if value.Steps > 0 { return fmt.Sprintf("move %d", value.Steps), nil }
    case Stop:
        return "stop", nil
    }
    return "", fmt.Errorf("invalid command")
}
func main() {
    for _, command := range []any{Move{3}, Stop{}, Move{-2}} {
        text, err := describe(command)
        if err != nil { fmt.Println(err) } else { fmt.Println(text) }
    }
}
```

**Check the result:** Prints `move 3`, `stop`, and `invalid command`.

## 6. How the other two languages do it

**Python**

```python
case {"kind": "move", "steps": int(steps)} if steps > 0:
    return f"move {steps}"
```

Structural pattern matching selects a branch by a value’s shape and can bind pieces of that value to names. Guards add conditions after a match.

**C++**

```cpp
if constexpr (std::is_same_v<T, Move>) {
    auto [steps] = value;
    return "move " + std::to_string(steps);
}
```

std::visit dispatches on a variant’s active alternative. if constexpr selects code at compile time for the alternative’s type.

Python matches runtime shapes, Go switches on a dynamic type or value, and C++ visits a declared variant alternative. A guard is an extra condition after a match.

## 7. The traps

**Near-miss:** a case for Move does not match *Move. Include the pointer type if that is part of the contract. An unchecked assertion such as `any("stop").(Move)` panics with a message beginning `interface conversion: interface {} is string, not main.Move`. Use a type switch or a comma-ok assertion for uncertain input.

## 8. Say it out loud

**How it gets asked:** “How do you handle a value that could be one of several types?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I use a type switch when an interface may hold several concrete types. Each branch gets a value of the matched type, and I then check its fields. A value switch is enough when only an existing tag or number matters. I handle unknown types explicitly and remember that pointer and value forms are different dynamic types. This is runtime selection, not compiler-enforced exhaustive handling.

**Follow-ups**

1. **Does a Go switch fall through?** No, not by default. Ordinary value switches have an explicit fallthrough statement; type switches do not.

2. **Does Move match *Move?** No. They are distinct dynamic types.

3. **What handles a new concrete type?** A new case or the explicit default path; Go does not require exhaustive type switches.

**Model answer:** A type switch inspects the dynamic type of an interface value. A value switch compares values and does not fall through by default. An open interface needs an unknown-type policy.

## 9. Recall card

- A type switch narrows an interface’s dynamic type.
- Check domain conditions inside the selected case.
- Value and pointer cases are different.
- An open interface needs an unknown-type policy.

Further reading: [Official reference](https://go.dev/ref/spec#Type_switches).
