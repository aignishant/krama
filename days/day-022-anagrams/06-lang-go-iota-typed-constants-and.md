---
day: 22
track: lang-go
title: "iota, typed constants, and the Stringer pattern"
theme: "Enums and sum types"
phase: "Languages: advanced features"
status: written
---

# Day 022 · Go — iota, typed constants, and the Stringer pattern

**Today's theme:** Enums and sum types

**After today you can:** You can model one-of-three-states in each language and be told, at compile time or run time, when you miss one.

**The interviewer asks it as:** *How do you represent a fixed set of values?*

## 1. What this is, and why it matters

A defined integer type with iota constants names states. Go still permits other values of that type, so boundary validation is explicit.

You use this when discussing enums and sum types in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Arun helps his sister organise a family lunch. Every invitation on her phone has one of three labels: waiting, accepted, or declined. At first, he writes whatever comes to mind. One cousin is marked yes, another coming, and another accepted. His sister cannot count the guests without asking him what each word means.

They agree to use only the three labels. Now everyone who helps knows what a label means. Waiting is different from declined. Someone who has not answered must not quietly disappear from the list of people they still need to ask.

An accepted invitation needs one more detail: how many people are coming. Arun keeps that number with the accepted reply. A declined invitation instead carries a short reason, such as being away that weekend. They do not put an empty guest count beside every declined reply and hope someone remembers why it is empty.

On Friday, a cousin sends a reply saying perhaps. Arun does not squeeze it into accepted just because it sounds hopeful. He asks his sister whether they need another label or whether it should remain waiting. That decision matters because the food order depends on it.

When the family later adds cancelled, they revisit each place where they count or display invitations. A new label needs a deliberate meaning everywhere it is used. Giving it a name is only the first step.

## 3. The idea in plain English

Arun’s labels become constants of the defined type `State`. **iota** is a counter inside a const declaration; it starts at zero and advances for each specification. Naming zero `Unknown` makes the default value visible instead of treating it as an accepted reply.

The **Stringer** interface requires `String() string`. fmt uses it to display a value. That method must handle unknown numbers because `State(99)` is legal. A switch has no automatic exhaustiveness check. Parsing and validation are separate from formatting: an unknown value may have a useful printed form while still being rejected as input.

## 4. The picture

```text
reply -> waiting
      -> accepted + guest count
      -> declined + reason
```

Names describe alternatives; some alternatives also carry different data.

## 5. The code, built step by step

First isolate the important operation:

```go
switch state {
case Accepted:
    return "accepted"
default:
    return "unknown"
}
```

Validate external integers before accepting a state.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import "fmt"

type State int
const (
    Unknown State = iota
    Waiting
    Accepted
    Declined
)
func (state State) String() string {
    switch state {
    case Waiting: return "waiting"
    case Accepted: return "accepted"
    case Declined: return "declined"
    default: return fmt.Sprintf("unknown(%d)", int(state))
    }
}
func parse(value int) (State, error) {
    state := State(value)
    if state < Waiting || state > Declined {
        return Unknown, fmt.Errorf("invalid state: %d", value)
    }
    return state, nil
}
func main() {
    fmt.Println(Accepted)
    fmt.Println(State(99))
    _, err := parse(99)
    fmt.Println(err)
}
```

**Check the result:** Prints `accepted`, `unknown(99)`, and `invalid state: 99`.

## 6. How the other two languages do it

**Python**

```python
case State.ACCEPTED:
    return "coming"
```

Enum gives distinct named members. IntEnum also behaves like an integer, which is useful for interoperability but weakens separation from numbers.

**C++**

```cpp
using Reply = std::variant<Waiting, Accepted, Declined>;
std::visit(Display{}, reply);
```

enum class names scoped values without implicit conversion to int. std::variant stores one of several alternative types and std::visit handles the active alternative.

Python Enum and Go typed constants name states but need deliberate handling of unknown values. C++ variant represents alternatives with different payload types; enum class alone only names values.

## 7. The traps

**Near-miss:** assume converting to State validates the number. It does not. The example produces `invalid state: 99` only because parse checks it. Inside String, formatting state with `%v` can call String again indefinitely; format int(state) to avoid recursive formatting.

## 8. Say it out loud

**How it gets asked:** “How do you represent a fixed set of values?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I define a State type and typed constants, reserving a meaningful zero value. I do not claim this is a closed set: any representable integer can be converted to State. I validate external input and use String for readable output, including an unknown fallback. If the protocol requires stable numbers, I assign those numbers explicitly instead of relying on the position of iota constants.

**Follow-ups**

1. **Is State(99) a compile error?** No. A defined integer type is not a closed enumeration.

2. **Does String validate input?** No. It only formats the value.

3. **What happens when a new state is added?** Audit switches and validation; the compiler does not force every switch to change.

**Model answer:** A defined integer type with iota constants names states. Go still permits other values of that type, so boundary validation is explicit. Formatting unknown states and accepting them are separate decisions.

## 9. Recall card

- Validate external integers before accepting a state.
- iota numbers constant declarations.
- Give zero a deliberate meaning.
- Formatting unknown states and accepting them are separate decisions.

Further reading: [Official reference](https://go.dev/ref/spec#Iota).
