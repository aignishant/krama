---
day: 37
track: lang-go
title: "Escape analysis, the GC pacer, and GOGC"
theme: "Memory model, deeper"
phase: "Languages: advanced features"
status: written
---

# Day 037 · Go — Escape analysis, the GC pacer, and GOGC

**Today's theme:** Memory model, deeper

**After today you can:** You can say why a value moved to the heap in each language and what that costs.

**The interviewer asks it as:** *What is a memory leak in a garbage-collected language?*

## 1. What this is, and why it matters

Go’s tracing garbage collector reclaims unreachable heap objects. Escape analysis decides where values may be stored; source syntax alone does not decide stack versus heap.

You use this when discussing memory model, deeper in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Farah lends a large serving bowl to her neighbours for a weekend meal. At first, one neighbour is responsible for returning it. The arrangement is simple: Farah knows whom to ask, and the neighbour knows when the job is finished.

Later, two households share the bowl. Each still needs it, so returning it when only one household is done would be too early. They agree that it can come back when neither household needs it any longer. That works as long as they actually say when they are finished.

One household keeps the bowl in a cupboard just in case they might want it again someday. Weeks pass. Nobody uses it, but nobody says it can be returned either. Farah has not lost the bowl physically; it is still being held for a reason that no longer serves the meal.

Another pair of neighbours each says the other might need a different dish. They keep both dishes because of that circular arrangement, even though the family meal ended days ago. Someone needs to look beyond each individual promise and notice that neither dish is serving anyone outside that pair.

Farah distinguishes responsibility from observation. Her sister can remember where the bowl is without being another person who must approve its return. Knowing about an object should not always mean keeping it in use forever. Clear ownership makes the end of its useful life easier to recognise.

## 3. The idea in plain English

Farah’s still-needed bowl corresponds to a reachable object. **Escape analysis** checks whether a value must outlive the scope or storage where it was created. Returning a pointer to a local value is safe in Go because the implementation arranges a suitable lifetime.

The **GC pacer** schedules collection work toward a heap-growth goal. GOGC controls the growth target relative to the live heap with additional runtime considerations. Higher targets generally trade memory for less frequent collection work; actual performance depends on allocation and workload. GOMEMLIMIT is a soft runtime memory limit, not a cure for live data that cannot fit. Measure before tuning.

## 4. The picture

```text
root/owner -> object -> another object
observation - - -> object (does not own)
unneeded but still reachable -> retained, not automatically collectible
```

Automatic reclamation depends on ownership or reachability, not whether the application still finds the object useful.

## 5. The code, built step by step

First isolate the important operation:

```go
func makeValue() *int {
    value := 42
    return &value
}
```

Use escape diagnostics as measurements, not syntax rules.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import (
    "fmt"
    "runtime"
)
func makeValue() *int {
    value := 42
    return &value
}
func main() {
    value := makeValue()
    retained := make([]byte, 1024*1024)
    fmt.Println(*value, len(retained))
    runtime.GC()
    runtime.KeepAlive(retained)
}
```

**Check the result:** Prints `42 1048576`. Inspect compiler decisions with `go build -gcflags="-m=2" main.go`; escape messages and inlining decisions vary by toolchain and context.

## 6. How the other two languages do it

**Python**

```python
observed = weakref.ref(item)
del item
gc.collect()
```

CPython uses reference counts and a cyclic garbage collector. Reachable but unnecessary objects remain live, so garbage collection does not prevent every memory leak.

**C++**

```cpp
if (auto owner = observed.lock()) {
    std::cout << owner->value;
}
```

unique_ptr expresses exclusive ownership, shared_ptr expresses shared ownership, and weak_ptr observes a shared object without extending its lifetime.

CPython combines reference counting with cycle collection, Go traces reachable objects, and C++ smart pointers express ownership. Long-lived reachable data can waste memory under any of these models.

## 7. The traps

**Near-miss:** claim every new allocation lives on the heap or every local variable lives on the stack. Compiler analysis can choose otherwise. Diagnostic output may include `escapes to heap` or `moved to heap`; these are optimisation reports, not correctness errors. Retaining old entries in a map keeps them reachable regardless of how often GC runs.

## 8. Say it out loud

**How it gets asked:** “What is a memory leak in a garbage-collected language?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I separate safe language lifetimes from compiler placement decisions. Escape analysis may move or optimise storage, and the tracing collector follows reachable heap data. A memory leak in Go often means something remains reachable longer than intended, such as a map entry or blocked goroutine. I inspect allocation profiles and retaining behaviour before changing GOGC, because tuning cannot reclaim objects the program still references.

**Follow-ups**

1. **Is returning a pointer to a local safe?** Yes. Go arranges a valid lifetime; placement is an implementation decision.

2. **Does new always force a heap allocation?** No. Escape analysis and optimisation determine placement.

3. **Can forced GC reclaim a live map entry?** No. Reachable entries remain live until the retaining path is removed.

**Model answer:** Go’s tracing garbage collector reclaims unreachable heap objects. Escape analysis decides where values may be stored; source syntax alone does not decide stack versus heap. Tuning cannot remove live references the application still retains.

## 9. Recall card

- Use escape diagnostics as measurements, not syntax rules.
- GC reclaims unreachable heap objects.
- GOGC trades heap growth against collection work.
- Tuning cannot remove live references the application still retains.

Further reading: [Official reference](https://go.dev/doc/gc-guide).
