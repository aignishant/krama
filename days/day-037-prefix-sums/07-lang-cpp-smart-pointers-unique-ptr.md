---
day: 37
track: lang-cpp
title: "Smart pointers: unique_ptr, shared_ptr, weak_ptr"
theme: "Memory model, deeper"
phase: "Languages: advanced features"
status: written
---

# Day 037 · C++ — Smart pointers: unique_ptr, shared_ptr, weak_ptr

**Today's theme:** Memory model, deeper

**After today you can:** You can say why a value moved to the heap in each language and what that costs.

**The interviewer asks it as:** *What is a memory leak in a garbage-collected language?*

## 1. What this is, and why it matters

unique_ptr expresses exclusive ownership, shared_ptr expresses shared ownership, and weak_ptr observes a shared object without extending its lifetime.

You use this when discussing memory model, deeper in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Farah lends a large serving bowl to her neighbours for a weekend meal. At first, one neighbour is responsible for returning it. The arrangement is simple: Farah knows whom to ask, and the neighbour knows when the job is finished.

Later, two households share the bowl. Each still needs it, so returning it when only one household is done would be too early. They agree that it can come back when neither household needs it any longer. That works as long as they actually say when they are finished.

One household keeps the bowl in a cupboard just in case they might want it again someday. Weeks pass. Nobody uses it, but nobody says it can be returned either. Farah has not lost the bowl physically; it is still being held for a reason that no longer serves the meal.

Another pair of neighbours each says the other might need a different dish. They keep both dishes because of that circular arrangement, even though the family meal ended days ago. Someone needs to look beyond each individual promise and notice that neither dish is serving anyone outside that pair.

Farah distinguishes responsibility from observation. Her sister can remember where the bowl is without being another person who must approve its return. Knowing about an object should not always mean keeping it in use forever. Clear ownership makes the end of its useful life easier to recognise.

## 3. The idea in plain English

Farah’s single responsible neighbour is a unique_ptr owner. Ownership can move but cannot be copied. A **shared_ptr control block** tracks shared ownership separately from the pointer value; the last strong owner destroys the managed object.

Two shared_ptr-owning objects can form a cycle that keeps both alive forever. A weak back-reference breaks that ownership cycle. weak_ptr::lock obtains a temporary shared owner if the target still exists. It does not protect concurrent mutation of the target; ownership coordination and data synchronisation are different concerns.

## 4. The picture

```text
root/owner -> object -> another object
observation - - -> object (does not own)
unneeded but still reachable -> retained, not automatically collectible
```

Automatic reclamation depends on ownership or reachability, not whether the application still finds the object useful.

## 5. The code, built step by step

First isolate the important operation:

```cpp
if (auto owner = observed.lock()) {
    std::cout << owner->value;
}
```

Prefer unique ownership when it fits.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <iostream>
#include <memory>

struct Node {
    int value;
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> previous;
    explicit Node(int number) : value(number) {}
};
int main() {
    auto exclusive = std::make_unique<int>(7);
    std::cout << *exclusive << '\n';
    std::weak_ptr<Node> observed;
    {
        auto first = std::make_shared<Node>(1);
        auto second = std::make_shared<Node>(2);
        first->next = second;
        second->previous = first;
        observed = first;
        if (auto owner = observed.lock()) std::cout << owner->value << '\n';
    }
    std::cout << std::boolalpha << observed.expired() << '\n';
}
```

**Check the result:** Prints `7`, `1`, and `true`. The weak back-reference does not keep the ownership chain alive.

## 6. How the other two languages do it

**Python**

```python
observed = weakref.ref(item)
del item
gc.collect()
```

CPython uses reference counts and a cyclic garbage collector. Reachable but unnecessary objects remain live, so garbage collection does not prevent every memory leak.

**Go**

```go
func makeValue() *int {
    value := 42
    return &value
}
```

Go’s tracing garbage collector reclaims unreachable heap objects. Escape analysis decides where values may be stored; source syntax alone does not decide stack versus heap.

CPython combines reference counting with cycle collection, Go traces reachable objects, and C++ smart pointers express ownership. Long-lived reachable data can waste memory under any of these models.

## 7. The traps

**Near-miss:** change previous to shared_ptr and create a strong cycle. The objects remain owned even after local handles disappear. Constructing shared_ptr directly from an expired weak_ptr throws `std::bad_weak_ptr`; lock instead returns an empty shared_ptr. Creating two unrelated shared_ptr owners from the same raw pointer can double-delete it.

## 8. Say it out loud

**How it gets asked:** “What is a memory leak in a garbage-collected language?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I prefer unique ownership when one component controls lifetime. I use shared_ptr only when independent owners really need to extend the same lifetime and weak_ptr for observations or back-links that should not own. I lock a weak reference once and retain that temporary owner while using the object. I still synchronise mutable fields separately; reference-count safety is not object-level thread safety.

**Follow-ups**

1. **Can smart pointers leak?** Yes. Strong shared ownership cycles retain objects.

2. **Does weak_ptr::lock always succeed?** No. It returns an empty shared_ptr after the target expires.

3. **Does shared_ptr make the object’s fields thread-safe?** No. It coordinates ownership, not arbitrary concurrent data access.

**Model answer:** unique_ptr expresses exclusive ownership, shared_ptr expresses shared ownership, and weak_ptr observes a shared object without extending its lifetime. Smart-pointer ownership does not synchronise the managed object’s fields.

## 9. Recall card

- Prefer unique ownership when it fits.
- Break shared ownership cycles with non-owning links.
- Lock a weak reference before use.
- Smart-pointer ownership does not synchronise the managed object’s fields.

Further reading: [Official reference](https://eel.is/c++draft/util.smartptr).
