---
day: 37
track: lang-python
title: "Object headers, refcounts, cycles, and the gc module"
theme: "Memory model, deeper"
phase: "Languages: advanced features"
status: written
---

# Day 037 · Python — Object headers, refcounts, cycles, and the gc module

**Today's theme:** Memory model, deeper

**After today you can:** You can say why a value moved to the heap in each language and what that costs.

**The interviewer asks it as:** *What is a memory leak in a garbage-collected language?*

## 1. What this is, and why it matters

CPython uses reference counts and a cyclic garbage collector. Reachable but unnecessary objects remain live, so garbage collection does not prevent every memory leak.

You use this when discussing memory model, deeper in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Farah lends a large serving bowl to her neighbours for a weekend meal. At first, one neighbour is responsible for returning it. The arrangement is simple: Farah knows whom to ask, and the neighbour knows when the job is finished.

Later, two households share the bowl. Each still needs it, so returning it when only one household is done would be too early. They agree that it can come back when neither household needs it any longer. That works as long as they actually say when they are finished.

One household keeps the bowl in a cupboard just in case they might want it again someday. Weeks pass. Nobody uses it, but nobody says it can be returned either. Farah has not lost the bowl physically; it is still being held for a reason that no longer serves the meal.

Another pair of neighbours each says the other might need a different dish. They keep both dishes because of that circular arrangement, even though the family meal ended days ago. Someone needs to look beyond each individual promise and notice that neither dish is serving anyone outside that pair.

Farah distinguishes responsibility from observation. Her sister can remember where the bowl is without being another person who must approve its return. Knowing about an object should not always mean keeping it in use forever. Clear ownership makes the end of its useful life easier to recognise.

## 3. The idea in plain English

Farah’s shared bowl resembles a referenced object. CPython objects carry bookkeeping such as type and reference-count information; exact header sizes are implementation details. Assignment adds another reference rather than copying the object. When ordinary strong references disappear, reference counting can reclaim many objects promptly.

A **reference cycle** has objects keeping one another alive through references. The gc module exposes the cycle collector. A weakref observes without owning; calling it returns the object or None. A long-lived list holding an obsolete object is still a strong reachable path, so no collector should free it. Use tracemalloc or an appropriate profiler to investigate retention rather than guessing from process size alone.

## 4. The picture

```text
root/owner -> object -> another object
observation - - -> object (does not own)
unneeded but still reachable -> retained, not automatically collectible
```

Automatic reclamation depends on ownership or reachability, not whether the application still finds the object useful.

## 5. The code, built step by step

First isolate the important operation:

```python
observed = weakref.ref(item)
del item
gc.collect()
```

Reachability is different from usefulness.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
import gc
import weakref

class Node:
    def __init__(self) -> None:
        self.next: Node | None = None

first = Node()
second = Node()
first.next = second
second.next = first
observed = weakref.ref(first)
del first, second
gc.collect()
print(observed() is None)
```

**Check the result:** Prints `True`: the unreachable cycle is collected before the weak reference is inspected. The number returned by gc.collect is deliberately not used as a stable expected value.

## 6. How the other two languages do it

**Go**

```go
func makeValue() *int {
    value := 42
    return &value
}
```

Go’s tracing garbage collector reclaims unreachable heap objects. Escape analysis decides where values may be stored; source syntax alone does not decide stack versus heap.

**C++**

```cpp
if (auto owner = observed.lock()) {
    std::cout << owner->value;
}
```

unique_ptr expresses exclusive ownership, shared_ptr expresses shared ownership, and weak_ptr observes a shared object without extending its lifetime.

CPython combines reference counting with cycle collection, Go traces reachable objects, and C++ smart pointers express ownership. Long-lived reachable data can waste memory under any of these models.

## 7. The traps

**Near-miss:** call gc.collect while a global list still holds the object and expect reclamation. That object is reachable. Calling a dead weak reference returns None; accessing an attribute without checking can raise `AttributeError: 'NoneType' object has no attribute 'next'`. Not every built-in type supports weak references.

## 8. Say it out loud

**How it gets asked:** “What is a memory leak in a garbage-collected language?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I distinguish unreachable garbage from reachable data the application forgot to release. CPython reference counting handles many lifetimes promptly, and the cycle collector handles eligible unreachable cycles. I use weak references only when observation should not own the object and check whether the object still exists. I measure retaining paths and allocation sources rather than promising that manual collection will fix growing memory.

**Follow-ups**

1. **Can a garbage-collected program leak memory?** Yes. Unneeded objects may remain reachable from long-lived owners.

2. **What does a weak reference keep alive?** Nothing by ownership alone; check its result before use.

3. **Does collection guarantee the OS memory graph immediately shrinks?** No. Allocators may retain freed storage for reuse.

**Model answer:** CPython uses reference counts and a cyclic garbage collector. Reachable but unnecessary objects remain live, so garbage collection does not prevent every memory leak. Find the retaining owner before trying to tune collection.

## 9. Recall card

- Reachability is different from usefulness.
- Cycles need more than simple reference counting.
- Weak references do not own their targets.
- Find the retaining owner before trying to tune collection.

Further reading: [Official reference](https://docs.python.org/3.12/library/gc.html).
