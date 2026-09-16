---
day: 22
track: lang-cpp
title: "enum class, std::variant, and std::visit"
theme: "Enums and sum types"
phase: "Languages: advanced features"
status: written
---

# Day 022 · C++ — enum class, std::variant, and std::visit

**Today's theme:** Enums and sum types

**After today you can:** You can model one-of-three-states in each language and be told, at compile time or run time, when you miss one.

**The interviewer asks it as:** *How do you represent a fixed set of values?*

## 1. What this is, and why it matters

enum class names scoped values without implicit conversion to int. std::variant stores one of several alternative types and std::visit handles the active alternative.

You use this when discussing enums and sum types in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Arun helps his sister organise a family lunch. Every invitation on her phone has one of three labels: waiting, accepted, or declined. At first, he writes whatever comes to mind. One cousin is marked yes, another coming, and another accepted. His sister cannot count the guests without asking him what each word means.

They agree to use only the three labels. Now everyone who helps knows what a label means. Waiting is different from declined. Someone who has not answered must not quietly disappear from the list of people they still need to ask.

An accepted invitation needs one more detail: how many people are coming. Arun keeps that number with the accepted reply. A declined invitation instead carries a short reason, such as being away that weekend. They do not put an empty guest count beside every declined reply and hope someone remembers why it is empty.

On Friday, a cousin sends a reply saying perhaps. Arun does not squeeze it into accepted just because it sounds hopeful. He asks his sister whether they need another label or whether it should remain waiting. That decision matters because the food order depends on it.

When the family later adds cancelled, they revisit each place where they count or display invitations. A new label needs a deliberate meaning everywhere it is used. Giving it a name is only the first step.

## 3. The idea in plain English

An invitation can be waiting, accepted with a count, or declined with a reason. A **sum type** represents one alternative at a time. Here variant is the sum type; each small struct describes one alternative’s data.

An overloaded visitor supplies one operation for each alternative. Adding a distinct new alternative without a matching overload makes this visitor ill-formed. A generic catch-all could hide that omission, so exhaustiveness depends on the visitor you write. enum class is useful when only the name is needed; it cannot enforce the relationship between a tag and unrelated fields. The variant stores its active payload inside the object, though payloads such as string may allocate.

## 4. The picture

```text
reply -> waiting
      -> accepted + guest count
      -> declined + reason
```

Names describe alternatives; some alternatives also carry different data.

## 5. The code, built step by step

First isolate the important operation:

```cpp
using Reply = std::variant<Waiting, Accepted, Declined>;
std::visit(Display{}, reply);
```

Visit the active alternative instead of guessing it.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <iostream>
#include <string>
#include <variant>

enum class State { waiting, accepted, declined };
struct Waiting {};
struct Accepted { int guests; };
struct Declined { std::string reason; };
using Reply = std::variant<Waiting, Accepted, Declined>;
struct Display {
    void operator()(const Waiting&) const { std::cout << "waiting\n"; }
    void operator()(const Accepted& value) const {
        std::cout << "guests " << value.guests << '\n';
    }
    void operator()(const Declined& value) const {
        std::cout << value.reason << '\n';
    }
};
int main() {
    Reply reply = Accepted{3};
    std::visit(Display{}, reply);
    reply = Declined{"away"};
    std::visit(Display{}, reply);
}
```

**Check the result:** Prints `guests 3` and `away`.

## 6. How the other two languages do it

**Python**

```python
case State.ACCEPTED:
    return "coming"
```

Enum gives distinct named members. IntEnum also behaves like an integer, which is useful for interoperability but weakens separation from numbers.

**Go**

```go
switch state {
case Accepted:
    return "accepted"
default:
    return "unknown"
}
```

A defined integer type with iota constants names states. Go still permits other values of that type, so boundary validation is explicit.

Python Enum and Go typed constants name states but need deliberate handling of unknown values. C++ variant represents alternatives with different payload types; enum class alone only names values.

## 7. The traps

**Near-miss:** keep an enum tag plus every possible payload in unrelated fields; they can disagree. With variant, `std::get<Waiting>(reply)` while Declined is active throws `std::bad_variant_access`. The exception type is specified; its message varies across libraries. Use visit or get_if when the active type is uncertain.

## 8. Say it out loud

**How it gets asked:** “How do you represent a fixed set of values?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I separate a named set of states from a set of payload-bearing alternatives. enum class solves the first problem; variant solves the second. Each accepted reply owns its guest count, and each declined reply owns its reason. A visitor with explicit overloads forces me to handle the declared alternatives. I still validate the contents, such as a negative guest count, because the type cannot enforce every domain rule.

**Follow-ups**

1. **Does enum class reject every cast from int?** No. Explicit casts can create unnamed values; validate external input.

2. **What does variant store?** One active alternative, with storage suitable for any declared alternative.

3. **Is every visitor exhaustive by design?** It must be invocable for every alternative, but a generic catch-all can accept new ones unintentionally.

**Model answer:** enum class names scoped values without implicit conversion to int. std::variant stores one of several alternative types and std::visit handles the active alternative. Types rule out some invalid states; payload validation handles the rest.

## 9. Recall card

- Visit the active alternative instead of guessing it.
- enum class avoids implicit integer conversion.
- Payloads belong with their alternative.
- Types rule out some invalid states; payload validation handles the rest.

Further reading: [Official reference](https://eel.is/c++draft/variant).
