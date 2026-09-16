# Day 032 — Variable-size sliding window

| Track | Today |
|---|---|
| **DSA** | Variable-size sliding window |
| **System design** | Query plans and the slow query |
| **Languages** | Concurrency II: passing messages |
| &nbsp;&nbsp;Python | queue.Queue and producer-consumer |
| &nbsp;&nbsp;Go | Channels: unbuffered, buffered, close, and range |
| &nbsp;&nbsp;C++ | std::condition_variable and a hand-built thread-safe queue |

## What you can do by tonight

- **DSA** — You can grow and shrink a window against a condition and never lose track of the invariant.
- **System design** — You can read an EXPLAIN output and say which part of the query is the problem.
- **Languages** — You can move work between threads safely in each language.

## The questions today answers

- *Find the smallest subarray with a sum at least k.*
- *Here is an EXPLAIN plan. What is wrong with this query?*
- *How do two threads hand data to each other safely?*

## Read in this order

1. [01-dsa-variable-size-sliding-window.md](01-dsa-variable-size-sliding-window.md) — the DSA lesson
2. [02-system-design-query-plans-and-the-slow.md](02-system-design-query-plans-and-the-slow.md) — the system design lesson
3. [03-practice.md](03-practice.md) — code it, then say it out loud
4. [05-lang-python-queue-queue-and-producer.md](05-lang-python-queue-queue-and-producer.md) — the Python lesson
5. [06-lang-go-channels-unbuffered-buffered-close.md](06-lang-go-channels-unbuffered-buffered-close.md) — the Go lesson
6. [07-lang-cpp-std-condition-variable-and.md](07-lang-cpp-std-condition-variable-and.md) — the C++ lesson
7. [08-lang-practice.md](08-lang-practice.md) — build it three times, then say it out loud

## Where this sits

- DSA phase: **Two pointers and sliding window**
- System design phase: **Databases from zero**
- Languages phase: **Languages: advanced features**

---

[← Day 031](../day-031-fixed-window/README.md) · [All days](../README.md) · [Day 033 →](../day-033-window-with-a-map/README.md)
