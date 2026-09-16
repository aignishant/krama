---
day: 11
track: lang-cpp
title: "Headers, translation units, #include, and namespaces"
theme: "Splitting code across files"
phase: "Languages: every language, every basic"
status: written
---

# Day 011 · C++ — Headers, translation units, #include, and namespaces

**Today's theme:** Splitting code across files

**After today you can:** You can split a program into three files in each language and explain what is visible from where.

**The interviewer asks it as:** *What makes a name visible to another file?*

---

## 1. What this is, and why it matters

A **declaration** tells the compiler that a name exists and how it may be used. A **definition** provides its implementation. A **header** shares declarations; `#include` inserts its contents into the source being compiled. A **translation unit** is that source after preprocessing.

Today you use splitting code across files to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Meera is arranging dinner for six friends. Until yesterday, everyone asked her everything. Where are the plates? When should the rice go on? Who is buying milk? Her phone kept buzzing while she tried to cook, and she answered the same question three times.

Tonight she divides the work. Arun handles food, Leela handles drinks, and Meera handles the table. Everyone knows who to ask. Arun tells the group when dinner will be ready, but he does not send them every small decision he makes in the kitchen. Leela needs the serving time, not the order in which he washes vegetables.

At seven, a guest asks Leela whether the rice is ready. She asks Arun rather than inventing an answer. Arun remains responsible for that one piece of information. If he changes the meal, he tells the group what has changed at the boundary: dinner is now at eight. The others can adjust without learning his whole recipe.

There is one final rule. Asking Arun about dinner must not cause him to start cooking a second meal. A question and the instruction to begin are different things. Meera sends the instruction once, after everyone arrives.

The arrangement works because each person has a clear job, a clear way to be reached, and a clear distinction between answering a question and starting the evening. Splitting the work helps only when those boundaries remain understandable.

## 3. The idea in plain English

A **declaration** tells the compiler that a name exists and how it may be used. A **definition** provides its implementation. A **header** shares declarations; `#include` inserts its contents into the source being compiled. A **translation unit** is that source after preprocessing.

Each dinner responsibility becomes a source file. The **linker** joins their compiled results and resolves references to definitions. A **namespace** groups names to avoid collisions; it does not make them private. A helper in an unnamed namespace has internal linkage within its translation unit.

The header guard checks a preprocessing name so the same header contents are not processed twice in one translation unit. It does not permit ordinary non-inline function definitions to appear in several translation units. Put this function's declaration in the header and its definition in exactly one source file.

## 4. The picture

```text
main (entry point)
  | calls add(2, 3)       | formats result
  v                       v
calculation component    presentation component
  | returns 5             | returns total=5
  +-----------------------+
              |
              v
         terminal output
```

The entry point coordinates two responsibilities. The calculation component does not need to know how the result will be displayed.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```cpp
namespace arithmetic {
    int add(int left, int right);
}
```

This declaration gives the caller a name and signature without providing its body. The implementation file supplies the body once. Compiling both .cpp files lets the linker connect the caller to that implementation.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.cpp`.

```cpp
// arithmetic.hpp
#ifndef KRAMA_ARITHMETIC_HPP
#define KRAMA_ARITHMETIC_HPP
namespace arithmetic {
    int add(int left, int right);
}
#endif

// arithmetic.cpp
#include "arithmetic.hpp"
int arithmetic::add(int left, int right) {
    return left + right;
}

// main.cpp
#include <iostream>
#include "arithmetic.hpp"
int main() {
    std::cout << "total=" << arithmetic::add(2, 3) << '\n';
}
```

**Check the result:** Build with `g++ -std=c++20 -Wall -Wextra main.cpp arithmetic.cpp -o demo`, then run `./demo` (PowerShell: `./demo.exe`). It prints `total=5`.

## 6. How the other two languages do it

- **Python** — A module owns a collection of names.
- **Go** — Packages, not files, control Go name visibility.
- **C++** — Headers publish declarations to callers.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** define `add` as an ordinary non-inline function in the header. Two source files including it create duplicate definitions at link time. A header guard cannot fix a problem spanning two translation units.

**Failure to reproduce:** omit `arithmetic.cpp` from the build command. GNU linkers commonly report `undefined reference to 'arithmetic::add(int, int)'`; quoting and surrounding text vary by platform. The declaration was visible, so compilation succeeded; the definition was absent, so linking failed.

## 8. Say it out loud

**How it gets asked:** “What makes a name visible to another file?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** I put the public declarations in a guarded header, include it from the implementation and caller, and compile both source files. Each source becomes a translation unit. The linker connects the call to the definition. Namespaces prevent accidental name collisions, while internal linkage controls whether a helper is visible to the linker from elsewhere.

**Follow-ups**

1. **Does include compile a source file separately?** No. It inserts text before compilation.

2. **Why include the header in its own implementation?** It lets the compiler check that the definition matches the declaration.

3. **When can definitions live in headers?** Templates and appropriately inline definitions commonly do; their rules differ from an ordinary non-inline function.

**Model answer:** This declaration gives the caller a name and signature without providing its body. The implementation file supplies the body once. Compiling both .cpp files lets the linker connect the caller to that implementation. Namespaces organise names; they are not privacy controls.

## 9. Recall card

- Headers publish declarations to callers.
- Each source is compiled as a translation unit.
- The linker needs the matching definition.
- Header guards prevent repeated inclusion within one unit.
- Namespaces organise names; they are not privacy controls.
