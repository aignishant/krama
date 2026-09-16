---
day: 38
track: lang-cpp
title: "Copy constructors, std::move, and the rule of five"
theme: "Copies, shares, and moves"
phase: "Languages: advanced features"
status: written
---

# Day 038 · C++ — Copy constructors, std::move, and the rule of five

**Today's theme:** Copies, shares, and moves

**After today you can:** You can predict whether a change through one variable shows up in another, in each language.

**The interviewer asks it as:** *If I modify the copy, does the original change?*

## 1. What this is, and why it matters

Copy and move constructors define how values acquire resources. std::move casts to an rvalue expression; the selected operation determines whether anything actually moves.

You use this when discussing copies, shares, and moves in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Ira makes a list of food requests on her phone and sends her brother a copy. He changes the first family’s requested dish. Ira opens her own view and sees that it changed too. What looked like a separate list still led to the same family details underneath.

They try again. Her brother gets a separate outer list, so he can reorder the families without changing Ira’s order. But editing one family’s details still appears in both places. Copying the row of names did not copy every detail each name led to.

For an independent planning session, Ira duplicates the family details as well. Now her brother can experiment without changing the version she is using. It takes more work and space, so she does not do it when both people are supposed to share the same current information.

Later, Ira hands the whole job to her sister. Instead of making another full copy, she gives her responsibility for the existing list and stops using it herself. Her sister can continue where she left off. Ira still has her phone, but that particular job no longer belongs to her.

Before each handover, they ask a simple question: should a change made here be visible there? If the answer is yes, they share deliberately. If it is no, they make a sufficiently independent copy. If responsibility is moving, they agree what the previous owner may still do afterwards.

## 3. The idea in plain English

Ira’s independent plan is a value copy. vector<int> copies its elements, while a vector of shared_ptr values copies shared ownership rather than duplicating pointees. **Move semantics** let a destination take resources when the source is no longer needed in its former state.

Prefer the **rule of zero**: use members that already manage their own resources so default operations work. A class manually managing a resource must consider destructor, copy constructor, copy assignment, move constructor, and move assignment together, the rule of five. A moved-from standard-library object is generally valid but has unspecified state unless its operation gives a stronger guarantee.

## 4. The picture

```text
shallow copy: outer A -> inner X <- outer B
deep copy:    outer A -> inner X    outer B -> inner Y
move:        old owner --ownership--> new owner
```

Copying an outer container and copying its reachable data are different operations.

## 5. The code, built step by step

First isolate the important operation:

```cpp
auto copied = original;
auto moved = std::move(original);
```

std::move enables an operation; it does not perform one itself.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <iostream>
#include <memory>
#include <utility>
#include <vector>

int main() {
    std::vector<int> original{1, 2, 3};
    auto copied = original;
    copied[0] = 9;
    auto moved = std::move(original);
    std::cout << copied[0] << ' ' << moved[0] << '\n';
    original.clear();
    original.push_back(7);
    std::cout << original[0] << '\n';
    auto owner = std::make_unique<int>(42);
    auto next = std::move(owner);
    std::cout << std::boolalpha << (owner == nullptr) << ' ' << *next << '\n';
}
```

**Check the result:** Prints `9 1`, `7`, and `true 42`. The example does not assume the moved-from vector is empty; it resets it before use.

## 6. How the other two languages do it

**Python**

```python
shallow = original.copy()
deep = deepcopy(original)
```

A shallow copy creates a new outer container while retaining references to its elements. deepcopy recursively copies an object graph while preserving internal sharing through memoisation.

**Go**

```go
independent := make([]int, len(original))
copy(independent, original)
```

Copying a slice value copies its descriptor, not its backing array. copy duplicates elements into destination storage; nested references may still be shared.

Python copy can share nested objects, Go slices share backing arrays unless elements are copied, and C++ value types define copy/move behaviour. State exactly which level is independent.

## 7. The traps

**Near-miss:** read original[0] immediately after moving the vector, assuming its size is unchanged. No such size guarantee is made. Copying unique_ptr fails to compile because its copy constructor is deleted; use an intentional move. std::move on a const value often selects a copy because a normal move operation needs a non-const source.

## 8. Say it out loud

**How it gets asked:** “If I modify the copy, does the original change?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I distinguish the cast from the resource transfer. std::move enables move-aware overload selection, but the type decides what happens. Value containers can provide deep element copies while pointer-like elements still share pointees. I prefer the rule of zero and only write special ownership operations when necessary. After moving, I rely only on the source’s documented valid operations and explicit postconditions, not a guessed empty state.

**Follow-ups**

1. **Does std::move itself transfer storage?** No. It changes the expression category; a constructor or assignment performs the transfer.

2. **Why prefer the rule of zero?** Resource-owning members already implement correct cleanup and copy/move behaviour.

3. **Can every moved-from object be indexed?** No. Its state may not satisfy indexing preconditions.

**Model answer:** Copy and move constructors define how values acquire resources. std::move casts to an rvalue expression; the selected operation determines whether anything actually moves. Use only documented operations on moved-from values.

## 9. Recall card

- std::move enables an operation; it does not perform one itself.
- Copy behaviour depends on element ownership.
- Prefer resource-managing members and the rule of zero.
- Use only documented operations on moved-from values.

Further reading: [Official reference](https://eel.is/c++draft/lib.types.movedfrom).
