---
day: 31
track: lang-python
title: "threading.Thread, the GIL, and what it really blocks"
theme: "Concurrency I: threads"
phase: "Languages: advanced features"
status: written
---

# Day 031 · Python — threading.Thread, the GIL, and what it really blocks

**Today's theme:** Concurrency I: threads

**After today you can:** You can start ten workers in each language and wait for all of them.

**The interviewer asks it as:** *What is the difference between a thread and a goroutine?*

## 1. What this is, and why it matters

threading.Thread starts work in the same process. join waits for completion; it does not automatically forward a worker’s exception to the caller.

You use this when discussing concurrency i: threads in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Maya has ten cushions to put into covers before guests arrive. She asks her brother to help. Each takes a different cushion, fits its cover, and places it on the sofa. They can both work because they have separate cushions and enough room to move.

Her younger cousin wants to help too, but there is only one pair of scissors for cutting loose ends. Whenever someone needs it, they must wait for the person holding it. Adding more helpers does not make that shared step happen all at once. Sometimes the scissors are the reason everyone else waits.

Maya also needs to answer the door. While her brother works on a cushion, she lets the visitors in and comes back. Several things are making progress during the same period, even though she personally does only one thing at a time.

Before serving tea, she checks that both helpers have finished. Asking them to begin is not the same as knowing the sofa is ready. If she leaves immediately after handing out cushions, guests may find half the covers still on the floor.

They agree that each helper will place finished cushions in a separate corner and tell Maya when done. She combines the results afterwards. This avoids everyone trying to rearrange the same sofa at once and gives her a clear moment when all the promised work is complete.

## 3. The idea in plain English

Maya’s helpers become threads. **Concurrency** means multiple tasks make progress over overlapping periods. **Parallelism** means work executes at the same instant. In standard CPython 3.12 the global interpreter lock, or GIL, allows one thread at a time to execute Python bytecode, though blocking I/O and some native code release it.

The example gives each thread a separate result slot and reads after joining. For CPU-heavy Python work, processes are often a better fit. Later Python builds can have different GIL options, so state the implementation and version instead of claiming the same limit for every Python runtime.

## 4. The picture

```text
start A -> work A -> finish A --+
start B -> work B -> finish B --+-> join/wait -> use results
```

Starting work creates a completion obligation. Wait before using results.

## 5. The code, built step by step

First isolate the important operation:

```python
for worker in workers:
    worker.start()
for worker in workers:
    worker.join()
```

Start all workers before waiting when overlap is intended.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
from threading import Thread

def square_into(values: list[int], position: int) -> None:
    values[position] = position * position

def main() -> None:
    results = [0] * 10
    workers = [Thread(target=square_into, args=(results, i)) for i in range(10)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    print(results)

if __name__ == "__main__":
    main()
```

**Check the result:** Prints `[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]`. Thread execution order is unspecified, but each result has a fixed position.

## 6. How the other two languages do it

**Go**

```go
group.Add(1)
go func(index int) {
    defer group.Done()
    results[index] = index * index
}(i)
```

A goroutine is a function executing concurrently under the Go runtime. WaitGroup tracks completion; it does not collect results or errors.

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

**Near-miss:** start one thread and immediately join it before starting the next, serialising the work. Starting the same Thread twice raises `RuntimeError: threads can only be started once`. An uncaught worker exception is reported but join does not re-raise it in main; use an executor Future when result/exception propagation is needed.

## 8. Say it out loud

**How it gets asked:** “What is the difference between a thread and a goroutine?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I start independent work, retain its handles, and join before consuming results. Each worker owns one output slot, so no two workers update the same item. I distinguish overlapping work from parallel CPU execution and state the CPython GIL assumption. I also choose how worker failures reach the caller; join only proves termination, not success. Thread creation is overhead, so ten tiny squares demonstrate the mechanics rather than a speedup.

**Follow-ups**

1. **Does join re-raise a worker exception?** No. Use explicit reporting or an executor Future.

2. **Does the GIL make compound updates safe?** No. Shared read-modify-write operations still need synchronisation.

3. **Why use processes for CPU-heavy Python?** Separate interpreters can execute on separate cores, at the cost of serialisation and process overhead.

**Model answer:** threading.Thread starts work in the same process. join waits for completion; it does not automatically forward a worker’s exception to the caller. More workers cannot remove a serial bottleneck.

## 9. Recall card

- Start all workers before waiting when overlap is intended.
- join waits for completion, not success.
- State the runtime’s GIL assumptions.
- More workers cannot remove a serial bottleneck.

Further reading: [Official reference](https://docs.python.org/3.12/library/threading.html).
