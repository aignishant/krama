---
day: 33
track: lang-go
title: "sync.Mutex, sync.RWMutex, atomic, and go test -race"
theme: "Concurrency III: shared memory"
phase: "Languages: advanced features"
status: written
---

# Day 033 · Go — sync.Mutex, sync.RWMutex, atomic, and go test -race

**Today's theme:** Concurrency III: shared memory

**After today you can:** You can write a data race in each language, detect it with a tool, and fix it.

**The interviewer asks it as:** *What is a data race, and how do you find one?*

## 1. What this is, and why it matters

Mutex protects shared invariants, RWMutex permits concurrent readers under a disciplined protocol, and atomic types support individual atomic operations.

You use this when discussing concurrency iii: shared memory in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Imran and his sister collect coins for a shared gift. Their phone shows a total of ten. Imran receives two more coins, looks at ten, and prepares to change it to twelve. At the same moment his sister receives three, looks at the same ten, and prepares to change it to thirteen.

Imran saves twelve. His sister then saves thirteen. They have received fifteen coins altogether, but the phone says thirteen. Neither person made an arithmetic mistake. The trouble is that each began from a number that stopped being current before the new number was saved.

They agree that only the person holding a small wooden token may read and change the shared total. The other person waits until the token is handed back. Now the reading and the change stay together. Their sister cannot use an old total while Imran is halfway through updating it.

When their father only wants to hear the total, he still follows the same rule. Looking while somebody is changing several related amounts could give him a mixture that never existed as one agreed state.

They keep the token only long enough to make the change. They do not hold it while walking to the shop or making a phone call. The rule protects the shared calculation, but keeping everyone waiting during unrelated errands would turn a useful safeguard into an unnecessary obstacle.

## 3. The idea in plain English

Imran’s token is a Mutex. Lock before reading shared mutable state and unlock after the complete update. An **atomic operation** is indivisible with respect to the relevant concurrent accesses; atomic.Int64.Add is suitable for a standalone counter, not automatically for a balance-plus-ledger invariant.

RWMutex allows multiple RLock holders or one Lock holder. A read lock must not protect writes, and upgrading a held read lock to a write lock is not supported. The race detector instruments executed paths; run the workload that actually shares data. A clean run cannot prove unexecuted paths are safe.

## 4. The picture

```text
read 10 -> add 2 -> write 12
read 10 -> add 3 ------------> write 13  (lost update)
lock -> read current -> update -> unlock (one transaction)
```

Protect the whole read-modify-write sequence, not only its final assignment.

## 5. The code, built step by step

First isolate the important operation:

```go
mutex.Lock()
total++
mutex.Unlock()
```

Choose locks around invariants, not isolated lines.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import (
    "fmt"
    "sync"
    "sync/atomic"
)
func main() {
    var mutex sync.Mutex
    var group sync.WaitGroup
    var independent atomic.Int64
    total := 0
    for worker := 0; worker < 2; worker++ {
        group.Add(1)
        go func() {
            defer group.Done()
            for i := 0; i < 1000; i++ {
                mutex.Lock(); total++; mutex.Unlock()
                independent.Add(1)
            }
        }()
    }
    group.Wait()
    fmt.Println(total, independent.Load())
}
```

**Check the result:** Prints `2000 2000`. Run `go run -race main.go` on a supported platform; the two counters are independent and both protected.

## 6. How the other two languages do it

**Python**

```python
with lock:
    total[0] += 1
```

A Lock protects a compound operation. The GIL does not make a sequence of reads, calculations, and writes one indivisible application action.

**C++**

```cpp
{
    std::lock_guard lock(mutex);
    ++total;
}
```

std::mutex and RAII lock guards protect shared state. std::atomic makes selected accesses atomic; an ordinary conflicting unsynchronised access is a data race.

Python locks protect compound invariants despite the GIL. Go and C++ also provide atomic primitives for selected operations, but atomics do not automatically protect relationships among several fields.

## 7. The traps

**Near-miss:** use independent.Load()+1 followed by Store and assume the pair is atomic; concurrent increments can be lost. Use Add. An unsafe ordinary-counter version may produce `WARNING: DATA RACE` under -race. Unlocking an unlocked mutex is a fatal runtime error, so keep ownership and unlock paths clear.

## 8. Say it out loud

**How it gets asked:** “What is a data race, and how do you find one?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I choose a mutex for a relationship among fields and an atomic operation for an independent counter when appropriate. All access follows the same protocol, including reads. I use RWMutex only when its reader/writer distinction fits the workload and avoid lock upgrading. I exercise the concurrent paths under the race detector, while recognising that detection depends on which paths and schedules execute.

**Follow-ups**

1. **Does an atomic field protect neighbouring fields?** No. A multi-field invariant usually needs a shared lock or another complete protocol.

2. **Can a read lock be upgraded directly?** No. Release and reacquire with revalidation, or use an exclusive lock from the start.

3. **Does a clean race run prove correctness?** No. Unexecuted paths and higher-level logical races can remain.

**Model answer:** Mutex protects shared invariants, RWMutex permits concurrent readers under a disciplined protocol, and atomic types support individual atomic operations. Race detection is evidence about exercised execution, not a proof.

## 9. Recall card

- Choose locks around invariants, not isolated lines.
- Use Add for an atomic increment.
- Do not copy a used mutex or atomic value.
- Race detection is evidence about exercised execution, not a proof.

Further reading: [Official reference](https://go.dev/doc/articles/race_detector).
