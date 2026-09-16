---
day: 13
track: lang-cpp
title: "RAII, new/delete, and why you almost never write delete"
theme: "Memory: who frees what"
phase: "Languages: every language, every basic"
status: written
---

# Day 013 · C++ — RAII, new/delete, and why you almost never write delete

**Today's theme:** Memory: who frees what

**After today you can:** You can say where a value lives, who frees it, and when, in each language.

**The interviewer asks it as:** *How does memory get freed in your language?*

---

## 1. What this is, and why it matters

**RAII** means acquiring a resource through an object whose destructor releases it. A **destructor** runs when the object's lifetime ends. For an ordinary local object, leaving its scope triggers destruction, including when an exception unwinds that scope.

Today you use memory: who frees what to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Anika borrows a badminton racket at the sports centre. The attendant gives her a numbered tag and says to return the racket before leaving. Anika plays one game and hands both items back. The racket is ready for the next person, and nobody has to search the building for it.

Her brother borrows a second racket, then lends it to a friend while he gets water. When he returns, the friend is still playing. He cannot return that racket merely because he has stopped using it. Someone else still needs it. The attendant waits until the last person brings it back.

Two friends make a different mistake. Each believes the other will return a pair of spare rackets. Both leave. No one is playing with them, but the rackets remain beside a bench because the responsibility has gone round in a circle. At closing time, an attendant walks through the hall and finds the forgotten equipment.

Anika notices that the three arrangements have different costs. Returning her own racket promptly is simple because responsibility is clear. Shared borrowing needs everyone to keep track of who still needs the racket. The final walk through the building finds things that ordinary handovers miss, but it takes work and happens later.

Before borrowing again, she asks who is responsible for returning the equipment and when that must happen. Being finished with something and having actually returned it are related, but they are not the same event.

## 3. The idea in plain English

**RAII** means acquiring a resource through an object whose destructor releases it. A **destructor** runs when the object's lifetime ends. For an ordinary local object, leaving its scope triggers destruction, including when an exception unwinds that scope.

Anika's clear borrowing responsibility is unique ownership. `std::unique_ptr<T>` owns one dynamically allocated object and deletes it when the owning smart pointer is destroyed. `std::make_unique<T>` constructs that owner safely. Moving a unique pointer transfers ownership; copying it is disallowed.

Raw `new` creates an object that needs a matching `delete`, but writing that pair by hand makes early returns and exceptions harder to handle. Prefer ordinary local objects and standard containers; use a smart pointer when dynamic ownership is necessary. `std::shared_ptr` supports shared ownership by counting owners, but cycles of strong shared owners require redesign or `std::weak_ptr` links.

## 4. The picture

```text
live owner / root ----> object A ----> object B
                          ^               |
                          +---------------+

Remove the outside path:
  tracing collector: A and B may become unreachable
  strong reference counts: the cycle can retain owners
  unique ownership: one responsible owner releases its object
```

Distinguish a live outside path from a cycle's internal links. Go traces reachability; CPython supplements reference counting with cyclic collection; C++ shared ownership needs cycles broken explicitly.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```cpp
auto owner = std::make_unique<Racket>();
auto next_owner = std::move(owner);
```

The move transfers exclusive ownership; it does not destroy the racket. The old pointer becomes empty. When next_owner leaves its inner scope, it destroys the racket before the later left message is printed.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.cpp`.

```cpp
#include <iostream>
#include <memory>
#include <utility>

struct Racket {
    ~Racket() { std::cout << "returned\n"; }
};

int main() {
    {
        auto owner = std::make_unique<Racket>();
        auto next_owner = std::move(owner);
        std::cout << std::boolalpha << (owner == nullptr) << '\n';
        std::cout << "playing\n";
    }
    std::cout << "left\n";
}
```

**Check the result:** Build with `g++ -std=c++20 -Wall -Wextra main.cpp -o demo`. Running it prints `true`, `playing`, `returned`, and `left` in that order.

## 6. How the other two languages do it

- **Python** — CPython uses reference counting plus cyclic collection.
- **Go** — Go keeps reachable objects alive.
- **C++** — RAII ties release to an owning object's lifetime.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** call `delete owner.get()` on an object owned by unique_ptr. The owner later tries to delete it again, causing undefined behaviour. A borrowed raw pointer is not an additional owner.

**Failure to reproduce:** replace `std::move(owner)` with `owner`. GCC's diagnostic contains `use of deleted function` because unique_ptr's copy constructor is deleted. Transfer ownership with a move only when the old owner is meant to give it up.

## 8. Say it out loud

**How it gets asked:** “How does memory get freed in your language?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** C++ normally manages resources through object lifetimes. RAII puts release in the destructor, so scope exit handles ordinary and exceptional paths. I use values first and unique_ptr for exclusive dynamic ownership. Shared ownership has a cost and can form cycles, so it should describe a real need rather than replace a clear ownership design.

**Follow-ups**

1. **Does every object require new?** No. Local values and containers already manage lifetimes.

2. **What survives moving a unique_ptr?** The allocated object survives under the destination owner; the source becomes empty.

3. **Can shared_ptr collect its own strong cycles?** No. Break an ownership edge, often with weak_ptr.

**Model answer:** The move transfers exclusive ownership; it does not destroy the racket. The old pointer becomes empty. When next_owner leaves its inner scope, it destroys the racket before the later left message is printed. Use values first; use shared ownership only when needed.

## 9. Recall card

- RAII ties release to an owning object's lifetime.
- A unique_ptr has one owner at a time.
- Scope exit destroys local owners deterministically.
- Borrowed pointers do not own what they observe.
- Use values first; use shared ownership only when needed.
