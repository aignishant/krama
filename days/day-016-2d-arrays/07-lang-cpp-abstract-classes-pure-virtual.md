---
day: 16
track: lang-cpp
title: "Abstract classes, pure virtual functions, and vtables"
theme: "Interfaces"
phase: "Languages: advanced features"
status: written
---

# Day 016 · C++ — Abstract classes, pure virtual functions, and vtables

**Today's theme:** Interfaces

**After today you can:** You can define a behaviour without naming a type in each language, and say when the check happens.

**The interviewer asks it as:** *What is an interface, and when does the compiler check it?*

---

## 1. What this is, and why it matters

An **abstract class** cannot be instantiated while it has an unimplemented pure virtual operation. A **pure virtual function**, written with `= 0`, describes behaviour derived classes must provide. Calling a virtual function through a base reference selects the implementation belonging to the actual derived object.

Today you use interfaces to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Priya runs a neighbourhood book exchange. At the entrance, every volunteer has one job: welcome a visitor and tell them where to leave a book. Priya does not care whether the volunteer is a teacher, a student, or a retired neighbour. She cares that the visitor receives a clear greeting and the right directions.

On the first morning, Priya asks each person to demonstrate. Arun says hello and points to the table. Leela does the same in another language for visitors who prefer it. Their words differ, but each fulfils the promise. Priya can send the next visitor to either of them without changing the rest of the event.

A new volunteer arrives and offers to carry chairs. That is useful, but it does not prove that he can greet visitors. Priya gives him the directions and asks him to practise before taking a place at the entrance. Being willing to help is not the same as being ready for this particular job.

Later, one visitor needs directions spoken slowly. Priya swaps the greeter without moving the book tables or stopping the exchange. The other volunteers do not need to know the new greeter's whole background. They need to know that the same small promise will still be kept.

By closing time, Priya has learned to describe jobs by what someone must do, rather than by who they are. A narrow promise makes it easier to welcome new helpers and easier to notice when an essential part of the job is missing.

## 3. The idea in plain English

An **abstract class** cannot be instantiated while it has an unimplemented pure virtual operation. A **pure virtual function**, written with `= 0`, describes behaviour derived classes must provide. Calling a virtual function through a base reference selects the implementation belonging to the actual derived object.

Priya's greeting role becomes the Greeter base class. Friend and Neighbour publicly inherit it and override greet. The `override` keyword asks the compiler to verify that the declaration really overrides a base virtual function; it catches subtle mismatches such as forgetting `const`.

A **virtual destructor** allows correct destruction through a base pointer. Include one when the interface may own derived objects polymorphically. The example only borrows a const reference, so it does not copy or own its argument. Ownership and the behavioural contract remain separate decisions.

## 4. The picture

```text
                    welcome(greeter)
                            |
                            v
                     greet() -> text
                       /         \
                      v           v
                    Friend     Neighbour
                    hello       namaste
```

The caller needs one operation. Python Protocol and Go interfaces allow structural matching; the C++ example uses an explicitly inherited abstract base.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```cpp
struct Greeter {
    virtual std::string greet() const = 0;
    virtual ~Greeter() = default;
};
```

The equals-zero declaration makes greet pure virtual; Greeter cannot itself supply a complete object. The virtual destructor supports derived destruction through the interface, while welcome merely borrows a const reference.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.cpp`.

```cpp
#include <iostream>
#include <string>

struct Greeter {
    virtual std::string greet() const = 0;
    virtual ~Greeter() = default;
};
struct Friend : Greeter {
    std::string greet() const override { return "hello"; }
};
struct Neighbour : Greeter {
    std::string greet() const override { return "namaste"; }
};
void welcome(const Greeter& greeter) {
    std::cout << greeter.greet() << '\n';
}
int main() {
    Friend friend_greeter;
    Neighbour neighbour;
    welcome(friend_greeter);
    welcome(neighbour);
}
```

**Check the result:** Compile with `g++ -std=c++20 -Wall -Wextra main.cpp -o demo`. The executable prints `hello` then `namaste`.

## 6. How the other two languages do it

- **Python** — Duck typing asks whether an object supports an operation.
- **Go** — An interface lists required methods.
- **C++** — A pure virtual operation defines required behaviour.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** remove const from Friend.greet while retaining override. A compiler diagnostic includes `marked 'override', but does not override`. That is the compiler protecting you from accidentally declaring another function.

**Second trap:** deleting a derived object through a base pointer whose base has a non-virtual destructor can cause undefined behaviour. Give an owning polymorphic interface a virtual destructor. Do not confuse a reference used to call a method with an ownership policy.

## 8. Say it out loud

**How it gets asked:** “What is an interface, and when does the compiler check it?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** For runtime polymorphism I use an abstract base with pure virtual methods, derived implementations marked override, and a virtual destructor when deletion through the base is supported. The consumer takes a reference or pointer to preserve dynamic dispatch and avoid copying away derived state. The interface states behaviour; a separate owner manages the object's lifetime.

**Follow-ups**

1. **Can I create a Greeter object?** No, it is abstract.

2. **Why write override?** The compiler checks that your signature overrides a base virtual function.

3. **Must every reusable algorithm use virtual calls?** No. Templates provide another form of polymorphism, covered on day 018.

**Model answer:** The equals-zero declaration makes greet pure virtual; Greeter cannot itself supply a complete object. The virtual destructor supports derived destruction through the interface, while welcome merely borrows a const reference. An owning polymorphic base needs appropriate destruction.

## 9. Recall card

- A pure virtual operation defines required behaviour.
- Derived classes implement that behaviour.
- Base references preserve virtual dispatch.
- override catches signature mistakes.
- An owning polymorphic base needs appropriate destruction.
