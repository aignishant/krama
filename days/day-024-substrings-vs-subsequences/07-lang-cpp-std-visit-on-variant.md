---
day: 24
track: lang-cpp
title: "std::visit on variant, if constexpr, and structured bindings"
theme: "Pattern matching"
phase: "Languages: advanced features"
status: written
---

# Day 024 · C++ — std::visit on variant, if constexpr, and structured bindings

**Today's theme:** Pattern matching

**After today you can:** You can branch on the shape of data in each language.

**The interviewer asks it as:** *How do you handle a value that could be one of several types?*

## 1. What this is, and why it matters

std::visit dispatches on a variant’s active alternative. if constexpr selects code at compile time for the alternative’s type.

You use this when discussing pattern matching in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Dev sorts deliveries for a family gathering. A box of fruit goes to the kitchen. A bag of clothes goes to the spare room. A small envelope goes to his aunt. He could inspect everything in exactly the same way, but the outside of each delivery already tells him which questions to ask.

For fruit, he checks whether it needs to stay cool. For clothes, he checks whose name is on the bag. For an envelope, he checks whether his aunt is home. The first decision narrows the next decision. Asking whether an envelope needs washing would not help anyone.

One afternoon a box arrives with a picture of fruit on it, but inside are cups. Dev stops relying on the picture alone. He checks what is actually there before carrying it into the kitchen. The label is a useful clue, not a guarantee.

His sister adds another instruction: small fruit boxes can go on the shelf, but heavy ones must stay on the floor. Dev first recognises the kind of delivery, then checks its weight. Both facts matter. A heavy box must not take the small-box route merely because both contain fruit.

Finally, something arrives that neither of them recognises. They leave it beside the door and ask the person who ordered it. A deliberate place for the unknown delivery is better than quietly treating it as something familiar and sending it to the wrong room.

## 3. The idea in plain English

The delivery’s shape is one of the types listed in variant. A **generic lambda** has an auto parameter, so its call operator can be instantiated for each alternative. `std::decay_t` removes reference and cv qualifiers when comparing that parameter’s type.

`if constexpr` discards the inappropriate branch for a particular instantiation. A normal if still requires both branches to be well-formed. Structured bindings, such as `auto [steps] = value`, unpack named pieces of an aggregate. They copy here; `auto& [steps]` would refer to the original object. A static_assert in the final branch prevents a future unhandled alternative from silently taking a fallback.

## 4. The picture

```text
input -> recognise shape/type -> extract fields -> check condition -> action
                    unknown -------------------------------------> reject
```

Recognise the alternative before interpreting its fields.

## 5. The code, built step by step

First isolate the important operation:

```cpp
if constexpr (std::is_same_v<T, Move>) {
    auto [steps] = value;
    return "move " + std::to_string(steps);
}
```

Visit first, then use the selected type’s fields.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <iostream>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <variant>

struct Move { int steps; };
struct Stop {};
using Command = std::variant<Move, Stop>;

std::string describe(const Command& command) {
    return std::visit([](const auto& value) -> std::string {
        using T = std::decay_t<decltype(value)>;
        if constexpr (std::is_same_v<T, Move>) {
            auto [steps] = value;
            if (steps <= 0) throw std::invalid_argument("invalid command");
            return "move " + std::to_string(steps);
        } else {
            static_assert(std::is_same_v<T, Stop>);
            return "stop";
        }
    }, command);
}
int main() {
    std::cout << describe(Move{3}) << '\n';
    std::cout << describe(Stop{}) << '\n';
}
```

**Check the result:** Prints `move 3` and `stop`.

## 6. How the other two languages do it

**Python**

```python
case {"kind": "move", "steps": int(steps)} if steps > 0:
    return f"move {steps}"
```

Structural pattern matching selects a branch by a value’s shape and can bind pieces of that value to names. Guards add conditions after a match.

**Go**

```go
switch value := command.(type) {
case Move:
    return fmt.Sprintf("move %d", value.Steps)
}
```

A type switch inspects the dynamic type of an interface value. A value switch compares values and does not fall through by default.

Python matches runtime shapes, Go switches on a dynamic type or value, and C++ visits a declared variant alternative. A guard is an extra condition after a match.

## 7. The traps

**Near-miss:** replace if constexpr with if and try to read value.steps for Stop; that branch is still checked and compilation fails. Compiler wording varies. Calling describe(Move{-2}) throws std::invalid_argument with the message `invalid command`. The selected alternative does not guarantee a valid distance.

## 8. Say it out loud

**How it gets asked:** “How do you handle a value that could be one of several types?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I list the permitted representations in variant and visit the active one. The generic lambda is instantiated for each alternative, and if constexpr keeps type-specific operations in the correct branch. I make the final branch assert its expected type so a later alternative cannot be silently accepted. Structured bindings unpack fields, but I choose copy or reference deliberately. Payload conditions still need runtime validation.

**Follow-ups**

1. **Why not an ordinary if?** Both branches must compile; if constexpr discards the non-selected branch during instantiation.

2. **Does auto [steps] refer to the original?** No. It binds into a copy. Use an appropriate reference binding when needed.

3. **What if a new alternative is added?** The static_assert fails until the visitor is extended.

**Model answer:** std::visit dispatches on a variant’s active alternative. if constexpr selects code at compile time for the alternative’s type. Type selection does not validate the payload’s meaning.

## 9. Recall card

- Visit first, then use the selected type’s fields.
- if constexpr discards an inappropriate branch.
- Structured bindings may copy or borrow.
- Type selection does not validate the payload’s meaning.

Further reading: [Official reference](https://eel.is/c++draft/stmt.if).
