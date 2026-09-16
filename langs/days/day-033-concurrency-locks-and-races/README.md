# Day 033 — Concurrency III: shared memory

| Track | Today |
|---|---|
| **Python** | threading.Lock, RLock, and a race you can reproduce |
| **Go** | sync.Mutex, sync.RWMutex, atomic, and go test -race |
| **C++** | std::mutex, std::lock_guard, std::atomic, and ThreadSanitizer |

## What you can do by tonight

You can write a data race in each language, detect it with a tool, and fix it.

## The question today answers

*What is a data race, and how do you find one?*

## Read in this order

1. [01-python-threading-lock-rlock-and.md](01-python-threading-lock-rlock-and.md) — the Python lesson
2. [02-go-sync-mutex-sync-rwmutex.md](02-go-sync-mutex-sync-rwmutex.md) — the Go lesson
3. [03-cpp-std-mutex-std-lock.md](03-cpp-std-mutex-std-lock.md) — the C++ lesson
4. [04-practice.md](04-practice.md) — build it three times, then say it out loud

## Where this sits

- Phase: **Advanced features**

---

[← Day 032](../day-032-concurrency-channels-and-queues/README.md) · [All days](../README.md) · [Day 034 →](../day-034-concurrency-async/README.md)
