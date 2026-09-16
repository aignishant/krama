# Day 105 — Lowest common ancestor

| Track | Today |
|---|---|
| **DSA** | Lowest common ancestor |
| **System design** | Read replicas and replication lag |
| **Languages** | Mini project 7: orders, events, and notifications |
| &nbsp;&nbsp;Python | Python notification worker consuming Kafka |
| &nbsp;&nbsp;Go | Go order service with gRPC, Postgres, and the outbox |
| &nbsp;&nbsp;C++ | C++ pricing service called over gRPC |

## What you can do by tonight

- **DSA** — You can find the LCA in a general binary tree and in a BST, and know why they differ.
- **System design** — You can explain why a user sometimes does not see their own write.
- **Languages** — You can ship three services that talk over gRPC and Kafka, with CI and health checks.

## The questions today answers

- *Find the lowest common ancestor of these two nodes.*
- *The user posted a comment and cannot see it. What happened?*
- *Design an order pipeline with a notification step. Where can it lose a message?*

## Project

**Mini project 7: orders, events, and notifications** — the languages half of today is a build day. The three
lessons are the walkthrough; the languages practice sheet is the deliverable.

## Read in this order

1. [01-dsa-lowest-common-ancestor.md](01-dsa-lowest-common-ancestor.md) — the DSA lesson
2. [02-system-design-read-replicas-and-replication-lag.md](02-system-design-read-replicas-and-replication-lag.md) — the system design lesson
3. [03-practice.md](03-practice.md) — code it, then say it out loud
4. [05-lang-python-python-notification-worker-consuming.md](05-lang-python-python-notification-worker-consuming.md) — the Python lesson
5. [06-lang-go-go-order-service-with.md](06-lang-go-go-order-service-with.md) — the Go lesson
6. [07-lang-cpp-c-pricing-service-called.md](07-lang-cpp-c-pricing-service-called.md) — the C++ lesson
7. [08-lang-practice.md](08-lang-practice.md) — build it three times, then say it out loud

## Where this sits

- DSA phase: **Trees and binary search trees**
- System design phase: **Scaling fundamentals**
- Languages phase: **Languages: messaging, resilience, and deployment**

---

[← Day 104](../day-104-tree-path-problems/README.md) · [All days](../README.md) · [Day 106 →](../day-106-bst-property/README.md)
