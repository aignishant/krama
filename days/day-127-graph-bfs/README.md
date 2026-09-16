# Day 127 — Breadth-first search on a graph

| Track | Today |
|---|---|
| **DSA** | Breadth-first search on a graph |
| **System design** | Distributed locks |
| **Languages** | Error architecture |
| &nbsp;&nbsp;Python | A domain exception hierarchy mapped to HTTP codes |
| &nbsp;&nbsp;Go | Typed errors, sentinel errors, and mapping to gRPC codes |
| &nbsp;&nbsp;C++ | std::expected with a domain error enum, mapped to codes |

## What you can do by tonight

- **DSA** — You can write BFS with a queue and a visited set, and never revisit a node.
- **System design** — You can implement one and name the failure mode that makes it unsafe.
- **Languages** — You can design how errors flow from the database to the user, in each language.

## The questions today answers

- *Traverse this graph breadth-first.*
- *Implement a distributed lock. What if the holder crashes?*
- *A row is missing. What does the user see, and how did it get there?*

## Read in this order

1. [01-dsa-breadth-first-search-on-a-graph.md](01-dsa-breadth-first-search-on-a-graph.md) — the DSA lesson
2. [02-system-design-distributed-locks.md](02-system-design-distributed-locks.md) — the system design lesson
3. [03-practice.md](03-practice.md) — code it, then say it out loud
4. [05-lang-python-a-domain-exception-hierarchy.md](05-lang-python-a-domain-exception-hierarchy.md) — the Python lesson
5. [06-lang-go-typed-errors-sentinel-errors.md](06-lang-go-typed-errors-sentinel-errors.md) — the Go lesson
6. [07-lang-cpp-std-expected-with-a.md](07-lang-cpp-std-expected-with-a.md) — the C++ lesson
7. [08-lang-practice.md](08-lang-practice.md) — build it three times, then say it out loud

## Where this sits

- DSA phase: **Graphs**
- System design phase: **Distributed systems core**
- Languages phase: **Languages: idiomatic depth and design**

---

[← Day 126](../day-126-graph-representation/README.md) · [All days](../README.md) · [Day 128 →](../day-128-graph-dfs/README.md)
