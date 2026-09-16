---
day: 31
track: lang-go
title: "goroutines, go func(), and sync.WaitGroup"
theme: "Concurrency I: threads"
phase: "Languages: advanced features"
status: written
---

# Day 031 · Go — goroutines, go func(), and sync.WaitGroup

**Today's theme:** Concurrency I: threads

**After today you can:** You can start ten workers in each language and wait for all of them.

**The interviewer asks it as:** *What is the difference between a thread and a goroutine?*

## 1. What this is, and why it matters

A goroutine is a function executing concurrently under the Go runtime. WaitGroup tracks completion; it does not collect results or errors.

You use this when discussing concurrency i: threads in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Maya has ten cushions to put into covers before guests arrive. She asks her brother to help. Each takes a different cushion, fits its cover, and places it on the sofa. They can both work because they have separate cushions and enough room to move.

Her younger cousin wants to help too, but there is only one pair of scissors for cutting loose ends. Whenever someone needs it, they must wait for the person holding it. Adding more helpers does not make that shared step happen all at once. Sometimes the scissors are the reason everyone else waits.

Maya also needs to answer the door. While her brother works on a cushion, she lets the visitors in and comes back. Several things are making progress during the same period, even though she personally does only one thing at a time.

Before serving tea, she checks that both helpers have finished. Asking them to begin is not the same as knowing the sofa is ready. If she leaves immediately after handing out cushions, guests may find half the covers still on the floor.

They agree that each helper will place finished cushions in a separate corner and tell Maya when done. She combines the results afterwards. This avoids everyone trying to rearrange the same sofa at once and gives her a clear moment when all the promised work is complete.

## 3. The idea in plain English

Maya’s helpers become goroutines, started with go. The runtime schedules them onto operating-system threads. A **WaitGroup** holds a count: Add registers work, Done completes one item, and Wait blocks until the count reaches zero.

Call Add before launching the goroutine so Wait cannot see zero before registration. Defer Done to keep completion accounting on every normal return and panic unwind. The example preallocates the slice and gives each goroutine a distinct index. It never appends while workers are using it. Ten tiny tasks demonstrate coordination; goroutines are cheap relative to many OS threads, not free.

## 4. The picture

```text
start A -> work A -> finish A --+
start B -> work B -> finish B --+-> join/wait -> use results
```

Starting work creates a completion obligation. Wait before using results.

## 5. The code, built step by step

First isolate the important operation:

```go
group.Add(1)
go func(index int) {
    defer group.Done()
    results[index] = index * index
}(i)
```

Register work before launching it.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import (
    "fmt"
    "sync"
)
func main() {
    results := make([]int, 10)
    var group sync.WaitGroup
    for i := range results {
        group.Add(1)
        go func(index int) {
            defer group.Done()
            results[index] = index * index
        }(i)
    }
    group.Wait()
    fmt.Println(results)
}
```

**Check the result:** Prints `[0 1 4 9 16 25 36 49 64 81]`. Run `go run -race main.go` on a supported platform to check exercised accesses.

## 6. How the other two languages do it

**Python**

```python
for worker in workers:
    worker.start()
for worker in workers:
    worker.join()
```

threading.Thread starts work in the same process. join waits for completion; it does not automatically forward a worker’s exception to the caller.

**C++**

```cpp
{
    std::vector<std::jthread> workers;
    // Add workers; scope exit joins them.
}
```

std::thread requires explicit lifecycle management. std::jthread adds automatic stop request and joining on destruction.

Python threads share a process and, in standard CPython 3.12, the GIL limits parallel Python bytecode. Go schedules goroutines over threads. C++ threads can execute simultaneously subject to hardware and scheduling.

## 7. The traps

**Near-miss:** call Add inside the goroutine, after Wait may already return. Calling Done more times than Add panics with `sync: negative WaitGroup counter`. Do not copy a WaitGroup after first use or assume it reports the worker’s success.

## 8. Say it out loud

**How it gets asked:** “What is the difference between a thread and a goroutine?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I register work before starting it and defer Done in each goroutine. I wait before reading the shared results and give each worker an exclusive index in a fixed-size slice. A goroutine is a runtime-scheduled activity, not one guaranteed OS thread. WaitGroup coordinates lifetime only, so errors need a separate channel or another coordination helper. I run the race detector on meaningful exercised paths.

**Follow-ups**

1. **Does WaitGroup return worker errors?** No. Results and errors need another mechanism.

2. **Why call Add before go?** It prevents Wait from observing zero before the work is registered.

3. **Can main return while goroutines run?** Yes, and the process then exits. Wait for work that must finish.

**Model answer:** A goroutine is a function executing concurrently under the Go runtime. WaitGroup tracks completion; it does not collect results or errors. A completion counter does not report whether work succeeded.

## 9. Recall card

- Register work before launching it.
- Defer Done inside each worker.
- Wait before reading results.
- A completion counter does not report whether work succeeded.

Further reading: [Official reference](https://pkg.go.dev/sync#WaitGroup).
