# Day 137 — Bellman-Ford, and what negative edges break

| Track | Today |
|---|---|
| **DSA** | Bellman-Ford, and what negative edges break |
| **System design** | Time-series and metrics stores |
| **Languages** | Build A, day 2: the server core |
| &nbsp;&nbsp;Python | Property tests against the server |
| &nbsp;&nbsp;Go | Sharded maps, TTLs, eviction, and the gRPC service |
| &nbsp;&nbsp;C++ | A load generator |

## What you can do by tonight

- **DSA** — You can say exactly why Dijkstra fails on negative weights, with an example graph.
- **System design** — You can say why a million metric points per second do not belong in a relational table.
- **Languages** — You can implement an LRU-with-TTL store behind a gRPC service in Go.

## The questions today answers

- *Why can't you use Dijkstra here?*
- *Where would you store the metrics for this system?*
- *How do you evict from a cache under memory pressure?*

## Read in this order

1. [01-dsa-bellman-ford-and-what-negative-edges.md](01-dsa-bellman-ford-and-what-negative-edges.md) — the DSA lesson
2. [02-system-design-time-series-and-metrics-stores.md](02-system-design-time-series-and-metrics-stores.md) — the system design lesson
3. [03-practice.md](03-practice.md) — code it, then say it out loud
4. [05-lang-python-property-tests-against-the.md](05-lang-python-property-tests-against-the.md) — the Python lesson
5. [06-lang-go-sharded-maps-ttls-eviction.md](06-lang-go-sharded-maps-ttls-eviction.md) — the Go lesson
6. [07-lang-cpp-a-load-generator.md](07-lang-cpp-a-load-generator.md) — the C++ lesson
7. [08-lang-practice.md](08-lang-practice.md) — build it three times, then say it out loud

## Where this sits

- DSA phase: **Graphs**
- System design phase: **Building blocks of big systems**
- Languages phase: **Languages: six five-day builds**

---

[← Day 136](../day-136-dijkstra/README.md) · [All days](../README.md) · [Day 138 →](../day-138-union-find/README.md)
