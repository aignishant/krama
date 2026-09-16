# Day 065 — Hashing your own objects

| Track | Today |
|---|---|
| **DSA** | Hashing your own objects |
| **System design** | Factory and abstract factory |
| **Languages** | Well-known types |
| &nbsp;&nbsp;Python | Timestamp, Duration, Any, Empty, and wrappers from Python |
| &nbsp;&nbsp;Go | timestamppb, durationpb, anypb, and emptypb |
| &nbsp;&nbsp;C++ | google/protobuf/timestamp.pb.h and friends |

## What you can do by tonight

- **DSA** — You can make a custom class usable as a dictionary key without subtle bugs.
- **System design** — You can hide object creation behind a factory and say what that buys you.
- **Languages** — You can represent time, absence, and a payload of unknown type in a message, in each language.

## The questions today answers

- *Why did putting this object in a set not deduplicate it?*
- *How do you create the right notification object for each channel?*
- *How do you represent a time in protobuf?*

## Read in this order

1. [01-dsa-hashing-your-own-objects.md](01-dsa-hashing-your-own-objects.md) — the DSA lesson
2. [02-system-design-factory-and-abstract-factory.md](02-system-design-factory-and-abstract-factory.md) — the system design lesson
3. [03-practice.md](03-practice.md) — code it, then say it out loud
4. [05-lang-python-timestamp-duration-any-empty.md](05-lang-python-timestamp-duration-any-empty.md) — the Python lesson
5. [06-lang-go-timestamppb-durationpb-anypb-and.md](06-lang-go-timestamppb-durationpb-anypb-and.md) — the Go lesson
6. [07-lang-cpp-google-protobuf-timestamp-pb.md](07-lang-cpp-google-protobuf-timestamp-pb.md) — the C++ lesson
7. [08-lang-practice.md](08-lang-practice.md) — build it three times, then say it out loud

## Where this sits

- DSA phase: **Hashing: maps and sets**
- System design phase: **Design patterns**
- Languages phase: **Languages: Protocol Buffers and gRPC**

---

[← Day 064](../day-064-grouping/README.md) · [All days](../README.md) · [Day 066 →](../day-066-when-hashing-is-wrong/README.md)
