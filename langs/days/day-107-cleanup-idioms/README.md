# Day 107 — Cleanup: context managers, defer, RAII

| Track | Today |
|---|---|
| **Python** | with, __enter__/__exit__, and contextlib |
| **Go** | defer, its evaluation order, and the loop trap |
| **C++** | RAII, scope guards, and destructors that never throw |

## What you can do by tonight

You can guarantee a file closes or a lock releases on every path, in each language.

## The question today answers

*How do you make sure a resource is released even if the code throws?*

## Read in this order

1. [01-python-with-enter-exit-and.md](01-python-with-enter-exit-and.md) — the Python lesson
2. [02-go-defer-its-evaluation-order.md](02-go-defer-its-evaluation-order.md) — the Go lesson
3. [03-cpp-raii-scope-guards-and.md](03-cpp-raii-scope-guards-and.md) — the C++ lesson
4. [04-practice.md](04-practice.md) — build it three times, then say it out loud

## Where this sits

- Phase: **Idiomatic depth and design**

---

[← Day 106](../day-106-data-modelling-idioms/README.md) · [All days](../README.md) · [Day 108 →](../day-108-properties-and-encapsulation/README.md)
