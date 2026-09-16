---
day: 19
track: lang-cpp
title: "Lambdas, capture lists by value and by reference, std::function"
theme: "Closures"
phase: "Languages: advanced features"
status: written
---

# Day 019 · C++ — Lambdas, capture lists by value and by reference, std::function

**Today's theme:** Closures

**After today you can:** You can return a function from a function in each language and say what it captured.

**The interviewer asks it as:** *What is a closure, and what does it capture?*

---

## 1. What this is, and why it matters

A **lambda** creates an object that can be called like a function. Its **capture list** specifies which surrounding values it retains. `[amount]` copies amount into the closure; `[&amount]` refers to the original variable. This makes the ownership decision visible at the declaration.

Today you use closures to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Tara helps three children practise multiplication. She gives the first child the instruction to add two to any number she says. The second child must add five. The third must add ten. All three follow the same kind of instruction, but each remembers a different extra amount.

Tara goes to the kitchen and calls out seven. The children answer nine, twelve, and seventeen. The instructions remain useful even after she has left the room. Each child needs the remembered amount as well as the number just announced.

Then Tara changes the game. She puts a bowl of counters on the table and tells all three children to add however many counters are currently in the bowl. There are initially two. Before the next round, she adds three more. Now all three answer twelve when she calls seven. They are consulting one shared, changing thing rather than remembering three separate amounts.

Neither game is wrong, but they answer different promises. A child told to remember two should not silently switch to five. A child told to consult the bowl should notice when its contents change. Tara repeats the rule before each round so the children can predict what the next answer will be.

When she explains the game to another parent, she includes both parts: what each child should do, and which information that child carries or consults later. The action alone is not enough to determine the answer.

## 3. The idea in plain English

A **lambda** creates an object that can be called like a function. Its **capture list** specifies which surrounding values it retains. `[amount]` copies amount into the closure; `[&amount]` refers to the original variable. This makes the ownership decision visible at the declaration.

Tara's remembered number corresponds to capture by value, while consulting the shared bowl corresponds to capture by reference. A returned closure that refers to a local variable will outlive that local and become invalid. Capture by value is appropriate for the small configuration integer below.

Each lambda expression has its own closure type. Returning `auto` lets the compiler preserve that type. `std::function<int(int)>` can store different callable types behind one common function signature, at the cost of a wrapper that may allocate and adds indirection. A `mutable` lambda may change its captured copies; that does not change the original copied-from variable.

## 4. The picture

```text
make_adder(2) ---> function + retained amount 2 ---> call(7) = 9
make_adder(5) ---> function + retained amount 5 ---> call(7) = 12

snapshot capture ---> private copied value
shared capture   ---> live binding / original object
                          |
                          v
                 later changes may be observed
```

A closure includes retained context as well as code. The second part distinguishes snapshots from shared state; use each language's precise capture rules.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```cpp
auto make_adder(int amount) {
    return [amount](int value) { return value + amount; };
}
```

The named capture stores its own amount, so the result remains valid after the parameter dies. In main, snapshot copies 2 while shared refers to the still-live variable; changing that variable to 5 affects only shared's result.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.cpp`.

```cpp
#include <functional>
#include <iostream>

auto make_adder(int amount) {
    return [amount](int value) { return value + amount; };
}

int main() {
    auto add_two = make_adder(2);
    std::function<int(int)> add_five = make_adder(5);
    std::cout << add_two(7) << ' ' << add_five(7) << '\n';
    int amount = 2;
    auto snapshot = [amount] { return amount; };
    auto shared = [&amount] { return amount; };
    amount = 5;
    std::cout << snapshot() << ' ' << shared() << '\n';
}
```

**Check the result:** Compile as C++20 and run. It prints `9 12` then `2 5`. The by-reference closure is used while amount is still alive.

## 6. How the other two languages do it

- **Python** — Functions can be returned and stored as values.
- **Go** — A function value preserves its parameter and result types.
- **C++** — Lambdas are callable objects with captured state.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** return `[&amount]` from make_adder. That refers to a local parameter whose lifetime ends when the factory returns. Later invocation has undefined behaviour; no particular output is promised.

**Failure to reproduce:** change the factory to `return [](int value) { return value + amount; };`. GCC reports a diagnostic including `'amount' is not captured`. Choose the capture deliberately rather than adding `[&]` everywhere, especially for callbacks that may outlive their creators.

## 8. Say it out loud

**How it gets asked:** “What is a closure, and what does it capture?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** A C++ lambda has an explicit capture policy. By-value capture owns a copy, while by-reference capture relies on the original object's lifetime. I return a by-value capture for a configured adder, so it remains valid after the factory returns. I use auto for its concrete closure type or std::function when I need a common callable signature for different implementations.

**Follow-ups**

1. **Does mutable modify the original by-value source?** No. It permits mutation of the closure's stored copy.

2. **Can a reference capture outlive its source?** It can be stored that long, but using the dangling reference is invalid.

3. **Why avoid default capture in long-lived callbacks?** Explicit captures make retained state and lifetime assumptions visible.

**Model answer:** The named capture stores its own amount, so the result remains valid after the parameter dies. In main, snapshot copies 2 while shared refers to the still-live variable; changing that variable to 5 affects only shared's result. Never return a closure referring to a destroyed local.

## 9. Recall card

- Lambdas are callable objects with captured state.
- Value capture stores a copy in the closure.
- Reference capture depends on the original lifetime.
- auto preserves the closure type; std::function wraps callables.
- Never return a closure referring to a destroyed local.
