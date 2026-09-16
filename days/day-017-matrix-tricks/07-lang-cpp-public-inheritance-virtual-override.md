---
day: 17
track: lang-cpp
title: "Public inheritance, virtual, override, and object slicing"
theme: "Composition versus inheritance"
phase: "Languages: advanced features"
status: written
---

# Day 017 · C++ — Public inheritance, virtual, override, and object slicing

**Today's theme:** Composition versus inheritance

**After today you can:** You can extend a type in each language and say why composition is the usual answer.

**The interviewer asks it as:** *Why is composition preferred over inheritance?*

---

## 1. What this is, and why it matters

**Public inheritance** expresses that a derived object may be used through the base interface. A **virtual** method chooses its implementation using the dynamic object when called through a base reference or pointer. Composition instead keeps a collaborator as a member.

Today you use composition versus inheritance to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Nikhil buys a bicycle for his commute. After a wet journey, he adds a removable rain cover to his bag. The bag has not become a different kind of bicycle, and the bicycle has not become a kind of rain cover. Each item has one job, and they work together when he needs them.

His friend buys a delivery bicycle with a large rear box fixed to it. That is still a bicycle: it can be steered, pedalled, and parked in the same way. The added box changes how much it carries, but it must not invalidate the ordinary expectations of someone borrowing a bicycle.

They test both arrangements on Saturday. Nikhil can lend the bag to his sister while keeping the bicycle. His friend cannot remove the rear box without tools. That is acceptable if the box always belongs there, but inconvenient if every trip needs a different arrangement.

Later, a shop offers Nikhil a complicated vehicle that looks like a bicycle but cannot be pedalled. Calling it a special bicycle does not make it suitable for the same job. His route includes a narrow path where he must pedal slowly, so he declines it.

He now asks two different questions when buying equipment. Is this genuinely a kind of thing I already know how to use? Or is it a separate thing that should work alongside it? Keeping those questions separate helps him choose equipment he can change without replacing everything at once.

## 3. The idea in plain English

**Public inheritance** expresses that a derived object may be used through the base interface. A **virtual** method chooses its implementation using the dynamic object when called through a base reference or pointer. Composition instead keeps a collaborator as a member.

The delivery bicycle may satisfy the bicycle contract, but the removable bag is a separate component. In C++, copying a derived object into a base value causes **object slicing**: only the base portion is copied. That new base object has no derived portion left to dispatch through.

Use a reference or pointer when you intend polymorphism. Mark overriding methods with `override` so signature mistakes are caught. Give a polymorphic owning base appropriate destruction, usually a virtual destructor. Inheritance reuses implementation but also commits the derived type to the base's behavioural promises.

## 4. The picture

```text
INHERITANCE                       COMPOSITION
base contract                     outer object
      ^                                | contains
      | must preserve promises         v
derived implementation            collaborator
                                       |
                                       v
                                  delegated work

Go embedding: containment plus promoted selectors, not inheritance.
```

Ask whether the new object can fulfil the base contract, or whether it merely needs another component to do part of its job.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```cpp
const Greeter& borrowed = warm;
Greeter sliced = warm;
```

The reference still reaches warm, so virtual dispatch selects the warm greeting. The second statement creates a base object from only the base portion; its later greeting is the base implementation. The different output follows from two different objects.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.cpp`.

```cpp
#include <iostream>
#include <string>

struct Greeter {
    virtual std::string greet() const { return "hello"; }
    virtual ~Greeter() = default;
};
struct WarmGreeter : public Greeter {
    std::string greet() const override { return "hello, friend"; }
};

int main() {
    WarmGreeter warm;
    const Greeter& borrowed = warm;
    Greeter sliced = warm;
    std::cout << borrowed.greet() << '\n';
    std::cout << sliced.greet() << '\n';
}
```

**Check the result:** Build with C++20 and run. It prints `hello, friend` then `hello`. The second object is a new base value, not another view of warm.

## 6. How the other two languages do it

- **Python** — Inheritance should preserve the base contract.
- **Go** — Go composition stores another value in a struct.
- **C++** — Public inheritance commits to the base's contract.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** change a consumer from `const Greeter&` to `Greeter` because references look complicated. The copy slices derived state and changes dispatch. A vector of base values similarly cannot preserve arbitrary derived objects.

**Failure to reproduce:** remove const from WarmGreeter.greet while leaving override. A diagnostic includes `marked 'override', but does not override`. Keep override so a silent behaviour change becomes a visible build failure.

## 8. Say it out loud

**How it gets asked:** “Why is composition preferred over inheritance?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** Public inheritance should express substitutability, not merely shared code. Virtual dispatch works through references and pointers to the original object. Copying a derived object into a base value slices it, creating a different object with only base state. For replaceable internal machinery, I usually keep a collaborator as a member instead of extending a hierarchy.

**Follow-ups**

1. **Does a virtual method prevent slicing?** No. Slicing happens when constructing the base value.

2. **Why use override?** It verifies that the derived signature overrides a virtual base method.

3. **What is composition here?** A desk containing a greeter object or owning pointer and forwarding calls to it.

**Model answer:** The reference still reaches warm, so virtual dispatch selects the warm greeting. The second statement creates a base object from only the base portion; its later greeting is the base implementation. The different output follows from two different objects. Composition often makes replaceable parts easier to reason about.

## 9. Recall card

- Public inheritance commits to the base's contract.
- Virtual dispatch follows the dynamic object.
- Base references preserve the derived object.
- Copying into a base value slices derived state.
- Composition often makes replaceable parts easier to reason about.
