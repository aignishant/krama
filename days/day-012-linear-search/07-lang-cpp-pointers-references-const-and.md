---
day: 12
track: lang-cpp
title: "Pointers, references, const, and passing by value"
theme: "Pointers, references, and value semantics"
phase: "Languages: every language, every basic"
status: written
---

# Day 012 · C++ — Pointers, references, const, and passing by value

**Today's theme:** Pointers, references, and value semantics

**After today you can:** You can say, for each language, whether a function receives a copy or the original, and prove it with a print.

**The interviewer asks it as:** *Is this passed by value or by reference?*

---

## 1. What this is, and why it matters

A **reference**, written `T&`, is an alias for an existing object. A pointer, written `T*`, stores an address and can be null or reassigned. A plain `T` parameter receives a value; changing it does not change the caller's object.

Today you use pointers, references, and value semantics to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Ravi and his sister share a shopping basket at the market. Ravi puts two oranges in it. His sister adds a third. When Ravi looks down, he sees three oranges. They have two people talking about one basket, not two baskets that somehow stay in agreement.

At the next stall, the shopkeeper offers his sister a fresh basket. She takes it and puts a mango inside. Ravi's basket still contains three oranges. Changing which basket she carries has not moved the fruit in his basket. Earlier she changed the shared contents. Now she changed what she was holding.

Ravi then asks for a second basket with exactly the same three oranges. He can compare the contents and say the two baskets match. He cannot honestly say they are the very same basket. If one falls, the other remains upright. Equal contents and being the same thing answer different questions.

Before they leave, their mother asks them to carry the heavy shopping upstairs. She can hand Ravi the actual basket, or she can ask him to assemble another basket containing the same purchases. One choice lets him change what everyone will receive; the other gives him something separate to rearrange.

The family avoids confusion by asking two questions before anyone moves anything: which basket are you holding, and are you changing its contents or choosing a different basket? Those questions explain the whole disagreement without blaming anyone for remembering the oranges incorrectly.

## 3. The idea in plain English

A **reference**, written `T&`, is an alias for an existing object. A pointer, written `T*`, stores an address and can be null or reassigned. A plain `T` parameter receives a value; changing it does not change the caller's object.

Ravi's shared basket corresponds to a reference parameter. A `const T&` gives access without permitting mutation through that reference. `const` limits this access path; it does not promise that no other part of the program can change a non-const underlying object.

Use a value for a small independent quantity, a const reference to read a large object without copying it, and a mutable reference when changing the caller is the operation's purpose. A reference must refer to a live object. Returning a reference to a local variable leaves a dangling reference once the function ends.

## 4. The picture

```text
caller --------------------> object A: [1, 2]
                                  ^
local parameter / alias -----------+

mutate A: both paths observe the change
rebind local: local -------------> object B: [99]
             caller still ------> object A
```

This is the shared-object case. In Go it requires a reference-bearing value such as a pointer or slice; a copied struct is different. In C++, compare a reference parameter with a plain value parameter.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```cpp
void change_copy(int value) { value = 9; (void)value; }
void change_original(int& value) { value = 9; }
```

The first signature asks for an independent integer. The second aliases the caller's integer. The cast to void only acknowledges the deliberately unused local result in this teaching example; it has no effect on the caller.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.cpp`.

```cpp
#include <iostream>

void change_copy(int value) { value = 9; (void)value; }
void change_original(int& value) { value = 9; }
int read(const int& value) { return value; }

int main() {
    int value = 2;
    change_copy(value);
    std::cout << value << '\n';
    change_original(value);
    int* pointer = &value;
    *pointer = 12;
    std::cout << read(value) << '\n';
}
```

**Check the result:** Build with `g++ -std=c++20 -Wall -Wextra main.cpp -o demo` and run the executable. It prints `2` then `12`.

## 6. How the other two languages do it

- **Python** — Assignment binds names to objects; it does not copy.
- **Go** — Every Go argument is passed by value.
- **C++** — A value parameter is independent of its caller's value.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** return `const int&` bound to a local integer. The program may compile, but using the returned reference has undefined behaviour. Return the small integer by value instead.

**Failure to reproduce:** change `read` to assign `value = 4`. GCC reports a diagnostic such as `assignment of read-only reference 'value'`. That rejection is useful: the signature promised read-only access. Do not cast away const to hide a mistaken contract.

## 8. Say it out loud

**How it gets asked:** “Is this passed by value or by reference?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** Passing by value gives the function its own value. Passing by reference aliases the caller's object, and const reference prevents mutation through that alias. A pointer also reaches an object but can express absence with nullptr. I choose the signature to state ownership and mutation expectations, then ensure any referenced object outlives its use.

**Follow-ups**

1. **Can a reference be reseated?** Assignment through it changes the referred-to object; it does not bind it to another object.

2. **Does const reference always avoid a temporary?** No. It can bind a temporary; lifetime rules still matter.

3. **What should return a small computed number?** A value, not a reference to a local number.

**Model answer:** The first signature asks for an independent integer. The second aliases the caller's integer. The cast to void only acknowledges the deliberately unused local result in this teaching example; it has no effect on the caller. Never return a reference to a local object.

## 9. Recall card

- A value parameter is independent of its caller's value.
- T& aliases an existing live object.
- const T& prevents mutation through that reference.
- Pointers can be null; check before dereferencing.
- Never return a reference to a local object.
