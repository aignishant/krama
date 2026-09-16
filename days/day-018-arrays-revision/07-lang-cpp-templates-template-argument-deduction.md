---
day: 18
track: lang-cpp
title: "Templates, template argument deduction, and instantiation"
theme: "Generics"
phase: "Languages: advanced features"
status: written
---

# Day 018 · C++ — Templates, template argument deduction, and instantiation

**Today's theme:** Generics

**After today you can:** You can write one Stack that works for ints and strings in each language.

**The interviewer asks it as:** *How would you write a function that works for any type?*

---

## 1. What this is, and why it matters

A **template** describes code that can be instantiated for different types. `template<class T>` introduces the varying type, and `Stack<int>` requests a stack whose elements are integers. Template requirements are checked as relevant code is instantiated; they are not runtime annotations.

Today you use generics to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Sana works at the entrance of a community hall. After lunch, she collects clean trays into a tall pile. The next person takes the tray on top. She does not reach into the middle, because that would disturb everything above it. When the pile is empty, she says there are no trays left rather than pretending to hand one over.

In the afternoon, the hall hosts a reading group. Sana arranges spare books in a pile by the door. The same habit works: add to the top, take from the top, and say clearly when nothing remains. She does not need a new arrangement just because the objects are books rather than trays.

There are still limits. A person who can stack trays does not automatically know how to wash books. The shared arrangement supports a few actions, not every possible action someone might perform on the things inside it. Sana keeps the common procedure separate from the care each object needs.

At closing time, a helper mixes keys into the book pile. Sana stops him. The shelf was promised to people expecting books. If the next person reaches for a book and receives keys, the procedure has failed even though the keys were placed neatly on top.

Sana keeps one useful arrangement and clearly states what each pile contains. That gives her reuse without surprise. She can teach the helper the same three actions once, then apply them to several kinds of object while preserving the promise made to whoever takes the next item.

## 3. The idea in plain English

A **template** describes code that can be instantiated for different types. `template<class T>` introduces the varying type, and `Stack<int>` requests a stack whose elements are integers. Template requirements are checked as relevant code is instantiated; they are not runtime annotations.

Sana's reusable piling procedure becomes a class template backed by vector<T>. **Template argument deduction** lets a function template infer T from call arguments in many cases. Class template argument deduction also exists, but this example writes Stack<int> explicitly so the element contract is visible.

Template definitions generally need to be visible where they are instantiated, so library templates commonly live in headers. A compiler generates or reuses the needed specialisations under the language's rules. This can increase compilation work and code size, but avoids requiring a shared virtual base merely to reuse an algorithm.

## 4. The picture

```text
one Stack[T] implementation
          /            \
         v              v
    Stack[int]      Stack[string / str]
    push 2, 3       push hello
    top -> 3        top -> hello
    next -> 2

empty pop ---> explicit failure policy, regardless of T
```

The operations stay the same while the element contract changes. Python relies on separate static checking; Go and C++ enforce the concrete uses during compilation.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```cpp
template<class T>
class Stack {
    std::vector<T> items;
public:
    void push(T value) { items.push_back(std::move(value)); }
};
```

The class template substitutes the chosen type into its vector and operations. This opening version only supports push; the complete class adds checked pop. Moving the parameter into storage allows transferable values without requiring another copy.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.cpp`.

```cpp
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

template<class T>
class Stack {
    std::vector<T> items;
public:
    void push(T value) { items.push_back(std::move(value)); }
    T pop() {
        if (items.empty()) throw std::out_of_range("empty stack");
        T value = std::move(items.back());
        items.pop_back();
        return value;
    }
};

int main() {
    Stack<int> numbers;
    numbers.push(2);
    numbers.push(3);
    const int first = numbers.pop();
    const int second = numbers.pop();
    std::cout << first << ' ' << second << '\n';
    Stack<std::string> words;
    words.push("hello");
    std::cout << words.pop() << '\n';
    try { numbers.pop(); }
    catch (const std::out_of_range& error) { std::cout << error.what() << '\n'; }
}
```

**Check the result:** Compile as C++20 and run. It prints `3 2`, `hello`, and `empty stack`. The separate pop statements make the removal order explicit.

## 6. How the other two languages do it

- **Python** — TypeVar names a relationship between input and output types.
- **Go** — Type parameters make one implementation work for several types.
- **C++** — Templates describe implementations parameterised by types.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** place all template definitions in a .cpp file and expose only declarations in a header. Callers may lack the definitions needed to instantiate their types, leading to unresolved definitions at link time. Put the definitions in the header or arrange explicit instantiations deliberately.

**Failure to reproduce:** add `numbers.push("wrong")`. GCC reports a diagnostic including `invalid conversion from 'const char*' to 'int'`. The generic declaration still creates concrete type requirements. Also do not put two state-changing pops in unrelated function arguments and assume a left-to-right evaluation order.

## 8. Say it out loud

**How it gets asked:** “How would you write a function that works for any type?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** A C++ template produces type-specific uses from one definition. The compiler checks the operations needed by each instantiation. I keep definitions visible where needed, preserve the element type, and specify empty-pop behaviour. I prefer templates for reusable operations across types when runtime selection through a common base interface is unnecessary.

**Follow-ups**

1. **Why are template definitions often in headers?** The compiler needs them where it instantiates a requested type.

2. **Does a template require inheritance?** No. Required operations come from the code or explicit constraints.

3. **What is deduction?** The compiler infers template arguments from a call or supported construction pattern.

**Model answer:** The class template substitutes the chosen type into its vector and operations. This opening version only supports push; the complete class adds checked pop. Moving the parameter into storage allows transferable values without requiring another copy. Specify failure and evaluation order as carefully as in non-template code.

## 9. Recall card

- Templates describe implementations parameterised by types.
- Instantiation checks the required operations.
- Stack<int> keeps an integer element contract.
- Make template definitions visible to instantiating code.
- Specify failure and evaluation order as carefully as in non-template code.
