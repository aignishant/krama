---
day: 31
track: lang-cpp
title: "std::thread, std::jthread, and join"
theme: "Concurrency I: threads"
phase: "Languages: advanced features"
status: written
---

# Day 031 · C++ — std::thread, std::jthread, and join

**Today's theme:** Concurrency I: threads

**After today you can:** You can start ten workers in each language and wait for all of them.

**The interviewer asks it as:** *What is the difference between a thread and a goroutine?*

## 1. What this is, and why it matters

std::thread requires explicit lifecycle management. std::jthread adds automatic stop request and joining on destruction.

You use this when discussing concurrency i: threads in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Maya has ten cushions to put into covers before guests arrive. She asks her brother to help. Each takes a different cushion, fits its cover, and places it on the sofa. They can both work because they have separate cushions and enough room to move.

Her younger cousin wants to help too, but there is only one pair of scissors for cutting loose ends. Whenever someone needs it, they must wait for the person holding it. Adding more helpers does not make that shared step happen all at once. Sometimes the scissors are the reason everyone else waits.

Maya also needs to answer the door. While her brother works on a cushion, she lets the visitors in and comes back. Several things are making progress during the same period, even though she personally does only one thing at a time.

Before serving tea, she checks that both helpers have finished. Asking them to begin is not the same as knowing the sofa is ready. If she leaves immediately after handing out cushions, guests may find half the covers still on the floor.

They agree that each helper will place finished cushions in a separate corner and tell Maya when done. She combines the results afterwards. This avoids everyone trying to rearrange the same sofa at once and gives her a clear moment when all the promised work is complete.

## 3. The idea in plain English

Maya must wait for her helpers. A **joinable thread** still has an execution handle that must be joined or detached. Destroying a joinable std::thread calls terminate. C++20 jthread instead requests cooperative stop and joins in its destructor.

The scoped vector below owns ten jthreads. Leaving that scope waits before results are printed. Each thread writes a distinct int element in a vector whose size never changes; vector<bool> has different packed-storage concerns and is not interchangeable here. Automatic joining solves lifetime management, not data races or exception reporting.

## 4. The picture

```text
start A -> work A -> finish A --+
start B -> work B -> finish B --+-> join/wait -> use results
```

Starting work creates a completion obligation. Wait before using results.

## 5. The code, built step by step

First isolate the important operation:

```cpp
{
    std::vector<std::jthread> workers;
    // Add workers; scope exit joins them.
}
```

Own thread handles until their work has finished.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <iostream>
#include <thread>
#include <vector>

int main() {
    std::vector<int> results(10);
    {
        std::vector<std::jthread> workers;
        for (int i = 0; i < 10; ++i) {
            workers.emplace_back([&results, i] { results[i] = i * i; });
        }
    }
    for (int value : results) std::cout << value << ' ';
    std::cout << '\n';
}
```

**Check the result:** Prints `0 1 4 9 16 25 36 49 64 81` followed by a trailing space. All workers have joined before printing.

## 6. How the other two languages do it

**Python**

```python
for worker in workers:
    worker.start()
for worker in workers:
    worker.join()
```

threading.Thread starts work in the same process. join waits for completion; it does not automatically forward a worker’s exception to the caller.

**Go**

```go
group.Add(1)
go func(index int) {
    defer group.Done()
    results[index] = index * index
}(i)
```

A goroutine is a function executing concurrently under the Go runtime. WaitGroup tracks completion; it does not collect results or errors.

Python threads share a process and, in standard CPython 3.12, the GIL limits parallel Python bytecode. Go schedules goroutines over threads. C++ threads can execute simultaneously subject to hardware and scheduling.

## 7. The traps

**Near-miss:** print results before the worker-owning scope ends, creating unsynchronised reads. Destroying a joinable std::thread invokes terminate; many implementations print `terminate called without an active exception`, but the wording is not standardised. An uncaught exception escaping the thread function also terminates the process.

## 8. Say it out loud

**How it gets asked:** “What is the difference between a thread and a goroutine?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I use an owning thread handle and make the join point visible. jthread helps with cleanup, but its stop request is cooperative and the task must observe it when cancellation is needed. I capture the index by value, share only the fixed result storage, and wait before reading it. I catch failures inside workers or use futures to transport them; automatic joining does not turn worker exceptions into caller exceptions.

**Follow-ups**

1. **Does jthread forcibly stop the work?** No. It requests stop and joins; the function must cooperate.

2. **Why capture i by value?** Each worker needs its own stable index rather than a reference to changing loop state.

3. **Does joining prevent all races?** No. It orders completion with later reads but does not protect concurrent shared updates.

**Model answer:** std::thread requires explicit lifecycle management. std::jthread adds automatic stop request and joining on destruction. Lifecycle safety does not replace synchronisation of shared data.

## 9. Recall card

- Own thread handles until their work has finished.
- jthread joins on destruction.
- Keep referenced storage alive until joining.
- Lifecycle safety does not replace synchronisation of shared data.

Further reading: [Official reference](https://eel.is/c++draft/thread.jthread).
