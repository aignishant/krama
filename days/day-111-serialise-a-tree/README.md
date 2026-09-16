# Day 111 — Serialising and deserialising a tree

| Track | Today |
|---|---|
| **DSA** | Serialising and deserialising a tree |
| **System design** | Single points of failure |
| **Languages** | Parallelism and the scheduler |
| &nbsp;&nbsp;Python | multiprocessing, the GIL, and free-threaded Python |
| &nbsp;&nbsp;Go | GOMAXPROCS, the M:P:G scheduler, and preemption |
| &nbsp;&nbsp;C++ | std::execution policies and hardware_concurrency |

## What you can do by tonight

- **DSA** — You can turn a tree into a string and back, preserving structure including nulls.
- **System design** — You can look at an architecture diagram and circle every box that kills the system.
- **Languages** — You can use every core in each language and say what stops you from doing so.

## The questions today answers

- *Serialise this tree, then rebuild it from the string.*
- *Which component here takes the whole system down if it fails?*
- *How many goroutines can you run on one core?*

## Read in this order

1. [01-dsa-serialising-and-deserialising-a-tree.md](01-dsa-serialising-and-deserialising-a-tree.md) — the DSA lesson
2. [02-system-design-single-points-of-failure.md](02-system-design-single-points-of-failure.md) — the system design lesson
3. [05-lang-python-multiprocessing-the-gil-and.md](05-lang-python-multiprocessing-the-gil-and.md) — the Python lesson
4. [06-lang-go-gomaxprocs-the-m-p.md](06-lang-go-gomaxprocs-the-m-p.md) — the Go lesson
5. [07-lang-cpp-std-execution-policies-and.md](07-lang-cpp-std-execution-policies-and.md) — the C++ lesson
6. [03-practice.md](03-practice.md) — DSA, system design, and all three languages

## Where this sits

- DSA phase: **Trees and binary search trees**
- System design phase: **Scaling fundamentals**
- Languages phase: **Languages: idiomatic depth and design**

---

[← Day 110](../day-110-trees-from-traversals/README.md) · [All days](../README.md) · [Day 112 →](../day-112-trees-revision/README.md)
