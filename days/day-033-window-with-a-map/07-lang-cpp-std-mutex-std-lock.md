---
day: 33
track: lang-cpp
title: "std::mutex, std::lock_guard, std::atomic, and ThreadSanitizer"
theme: "Concurrency III: shared memory"
phase: "Languages: advanced features"
status: written
---

# Day 033 · C++ — std::mutex, std::lock_guard, std::atomic, and ThreadSanitizer

**Today's theme:** Concurrency III: shared memory

**After today you can:** You can write a data race in each language, detect it with a tool, and fix it.

**The interviewer asks it as:** *What is a data race, and how do you find one?*

## 1. What this is, and why it matters

std::mutex and RAII lock guards protect shared state. std::atomic makes selected accesses atomic; an ordinary conflicting unsynchronised access is a data race.

You use this when discussing concurrency iii: shared memory in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Imran and his sister collect coins for a shared gift. Their phone shows a total of ten. Imran receives two more coins, looks at ten, and prepares to change it to twelve. At the same moment his sister receives three, looks at the same ten, and prepares to change it to thirteen.

Imran saves twelve. His sister then saves thirteen. They have received fifteen coins altogether, but the phone says thirteen. Neither person made an arithmetic mistake. The trouble is that each began from a number that stopped being current before the new number was saved.

They agree that only the person holding a small wooden token may read and change the shared total. The other person waits until the token is handed back. Now the reading and the change stay together. Their sister cannot use an old total while Imran is halfway through updating it.

When their father only wants to hear the total, he still follows the same rule. Looking while somebody is changing several related amounts could give him a mixture that never existed as one agreed state.

They keep the token only long enough to make the change. They do not hold it while walking to the shop or making a phone call. The rule protects the shared calculation, but keeping everyone waiting during unrelated errands would turn a useful safeguard into an unnecessary obstacle.

## 3. The idea in plain English

Imran’s token becomes mutex. A **data race** in C++ involves conflicting accesses from threads, at least one a write, without the required synchronisation and without both accesses being atomic. It gives undefined behaviour, not merely an occasionally wrong count.

lock_guard owns a lock for its scope and releases on every exit. std::atomic<int>::fetch_add performs one indivisible update. Its default ordering is sequentially consistent; weaker memory orders require a separate argument and are not needed here. volatile does not provide inter-thread synchronisation. ThreadSanitizer can report executed races on supported toolchains.

## 4. The picture

```text
read 10 -> add 2 -> write 12
read 10 -> add 3 ------------> write 13  (lost update)
lock -> read current -> update -> unlock (one transaction)
```

Protect the whole read-modify-write sequence, not only its final assignment.

## 5. The code, built step by step

First isolate the important operation:

```cpp
{
    std::lock_guard lock(mutex);
    ++total;
}
```

Use RAII to hold the lock for the whole update.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <atomic>
#include <iostream>
#include <mutex>
#include <thread>

int main() {
    int total = 0;
    std::atomic<int> independent{0};
    std::mutex mutex;
    auto work = [&] {
        for (int i = 0; i < 1000; ++i) {
            { std::lock_guard lock(mutex); ++total; }
            independent.fetch_add(1);
        }
    };
    std::jthread first(work), second(work);
    first.join(); second.join();
    std::cout << total << ' ' << independent.load() << '\n';
}
```

**Check the result:** Prints `2000 2000`. On a compatible platform build a separate diagnostic version with `-fsanitize=thread -g -O1 -pthread`; do not combine ThreadSanitizer and AddressSanitizer in the same executable.

## 6. How the other two languages do it

**Python**

```python
with lock:
    total[0] += 1
```

A Lock protects a compound operation. The GIL does not make a sequence of reads, calculations, and writes one indivisible application action.

**Go**

```go
mutex.Lock()
total++
mutex.Unlock()
```

Mutex protects shared invariants, RWMutex permits concurrent readers under a disciplined protocol, and atomic types support individual atomic operations.

Python locks protect compound invariants despite the GIL. Go and C++ also provide atomic primitives for selected operations, but atomics do not automatically protect relationships among several fields.

## 7. The traps

**Near-miss:** mark total volatile and remove the mutex. That is still a data race. A diagnostic build of the unsafe variant can report `WARNING: ThreadSanitizer: data race`; addresses and frames vary. Naming the guard matters: a temporary guard destroyed at the end of its expression does not protect subsequent statements.

## 8. Say it out loud

**How it gets asked:** “What is a data race, and how do you find one?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I identify all conflicting accesses and establish a lock or atomic protocol for them. The lock guard’s lifetime encloses the invariant update. An atomic increment is useful for an independent counter, but separately atomic fields do not automatically preserve a combined business rule. I join before reading final results and run ThreadSanitizer on representative paths. I never use volatile as a substitute for thread synchronisation.

**Follow-ups**

1. **Does volatile remove a data race?** No. It does not establish the required inter-thread synchronisation.

2. **Why name a lock guard?** Its scope lifetime must cover the protected statements.

3. **Does a clean sanitizer run prove safety?** No. It observes only the paths and schedules that execute.

**Model answer:** std::mutex and RAII lock guards protect shared state. std::atomic makes selected accesses atomic; an ordinary conflicting unsynchronised access is a data race. volatile is not a thread-synchronisation tool.

## 9. Recall card

- Use RAII to hold the lock for the whole update.
- An ordinary data race is undefined behaviour.
- Atomics protect defined operations, not arbitrary invariants.
- volatile is not a thread-synchronisation tool.

Further reading: [Official reference](https://clang.llvm.org/docs/ThreadSanitizer.html).
