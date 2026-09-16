---
day: 33
track: lang-python
title: "threading.Lock, RLock, and a race you can reproduce"
theme: "Concurrency III: shared memory"
phase: "Languages: advanced features"
status: written
---

# Day 033 · Python — threading.Lock, RLock, and a race you can reproduce

**Today's theme:** Concurrency III: shared memory

**After today you can:** You can write a data race in each language, detect it with a tool, and fix it.

**The interviewer asks it as:** *What is a data race, and how do you find one?*

## 1. What this is, and why it matters

A Lock protects a compound operation. The GIL does not make a sequence of reads, calculations, and writes one indivisible application action.

You use this when discussing concurrency iii: shared memory in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Imran and his sister collect coins for a shared gift. Their phone shows a total of ten. Imran receives two more coins, looks at ten, and prepares to change it to twelve. At the same moment his sister receives three, looks at the same ten, and prepares to change it to thirteen.

Imran saves twelve. His sister then saves thirteen. They have received fifteen coins altogether, but the phone says thirteen. Neither person made an arithmetic mistake. The trouble is that each began from a number that stopped being current before the new number was saved.

They agree that only the person holding a small wooden token may read and change the shared total. The other person waits until the token is handed back. Now the reading and the change stay together. Their sister cannot use an old total while Imran is halfway through updating it.

When their father only wants to hear the total, he still follows the same rule. Looking while somebody is changing several related amounts could give him a mixture that never existed as one agreed state.

They keep the token only long enough to make the change. They do not hold it while walking to the shop or making a phone call. The rule protects the shared calculation, but keeping everyone waiting during unrelated errands would turn a useful safeguard into an unnecessary obstacle.

## 3. The idea in plain English

Imran’s token becomes Lock. A **critical section** is the code that runs while holding it. `with lock` releases the lock even when the block raises. Every access that participates in the protected invariant must follow the same locking rule.

An RLock permits the same thread to acquire it repeatedly, with matching releases. It can help nested calls but can also conceal an unclear design. To reproduce a lost update reliably, separate a read from a write and coordinate two workers with a Barrier so both read the old value before either writes. Timing sleeps alone are not a proof of a race.

## 4. The picture

```text
read 10 -> add 2 -> write 12
read 10 -> add 3 ------------> write 13  (lost update)
lock -> read current -> update -> unlock (one transaction)
```

Protect the whole read-modify-write sequence, not only its final assignment.

## 5. The code, built step by step

First isolate the important operation:

```python
with lock:
    total[0] += 1
```

Protect the whole read-modify-write operation.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
from _thread import LockType
from threading import Lock, Thread

def increment(total: list[int], lock: LockType) -> None:
    for _ in range(1000):
        with lock:
            total[0] += 1

def main() -> None:
    total = [0]
    lock = Lock()
    workers = [Thread(target=increment, args=(total, lock)) for _ in range(2)]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    print(total[0])

if __name__ == "__main__":
    main()
```

**Check the result:** Prints `2000`. There are 2 × 1,000 protected increments. The lock adds serial coordination; it does not make a CPU counter faster.

## 6. How the other two languages do it

**Go**

```go
mutex.Lock()
total++
mutex.Unlock()
```

Mutex protects shared invariants, RWMutex permits concurrent readers under a disciplined protocol, and atomic types support individual atomic operations.

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

**Near-miss:** lock only the final assignment while reading the old count outside it. The old value can already be stale. Calling release on an unlocked Lock raises `RuntimeError: release unlocked lock`. Acquiring the same ordinary Lock twice in the same thread can deadlock; use a simpler call structure or a justified RLock.

## 8. Say it out loud

**How it gets asked:** “What is a data race, and how do you find one?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I identify the invariant first, then hold one lock across every read and write needed to preserve it. I release through a context manager and avoid slow I/O inside the critical section. I do not rely on the GIL for an application transaction. To demonstrate a bug I coordinate the bad interleaving explicitly, and after repair I check the invariant rather than merely observing that the program did not crash.

**Follow-ups**

1. **Does the GIL protect a compound invariant?** No. It does not promise atomicity for an arbitrary sequence of application operations.

2. **When choose RLock?** When the same thread must acquire the same lock through nested calls, after considering a simpler design.

3. **Does a successful run prove no race?** No. The harmful interleaving may not have occurred.

**Model answer:** A Lock protects a compound operation. The GIL does not make a sequence of reads, calculations, and writes one indivisible application action. A passing schedule does not prove all schedules are safe.

## 9. Recall card

- Protect the whole read-modify-write operation.
- Release locks with a context manager.
- Keep critical sections focused.
- A passing schedule does not prove all schedules are safe.

Further reading: [Official reference](https://docs.python.org/3.12/library/threading.html#lock-objects).
