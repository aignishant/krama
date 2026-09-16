# Krama Languages

**180 days. Three languages, side by side. Python, Go, and C++.**

Every day teaches one idea in all three languages. You write the same thing three
times, and the differences become the lesson. By day 15 you can build a small tool in
any of them. By day 45 you know the features that make each language itself. By day 180
you have shipped ten projects, one of them an order platform with a Python gateway, Go
services talking over gRPC with Protocol Buffers, and a C++ pricing engine.

Written for someone starting from **zero**. If you have never written a program, you
are the reader.

---

## Start here

```bash
./l status        # where you are
./l day 1         # today's hub
```

Then open [`days/day-001-hello-three-languages/README.md`](days/day-001-hello-three-languages/README.md).

---

## What a day looks like

```
days/day-012-pointers-and-references/
    README.md                              the hub — today in one screen
    01-python-everything-is-a-reference.md the Python lesson
    02-go-pointers-with-and-value.md       the Go lesson
    03-cpp-pointers-references-const-and.md the C++ lesson
    04-practice.md                         three exercises, built three times
```

Five files. No lab folder, no starter code. The code is inside the lessons, complete,
with the command that runs it and the output it prints.

---

## The shape of the 180 days

| Days | Phase | What you get |
|---|---|---|
| 1-15 | Foundations | Every basic in every language. Ends with a to-do CLI in all three. |
| 16-45 | Advanced features | Interfaces, generics, closures, concurrency, memory, testing. Ends with a concurrent downloader. |
| 46-60 | Networking, HTTP, data | Sockets, HTTP, Postgres, Redis, Docker. Ends with a URL shortener. |
| 61-75 | Protocol Buffers and gRPC | Schemas, code generation, evolution, streaming, auth, the wire format by hand. Go serves; Python and C++ call. Ends with an inventory service. |
| 76-90 | Performance and systems | Benchmarks, profilers, memory layout, FFI, processes, streams. Ends with a log pipeline. |
| 91-105 | Messaging and resilience | Kafka, jobs, WebSockets, rate limits, breakers, metrics, Kubernetes, CI. Ends with an order pipeline. |
| 106-135 | Idiomatic depth | The standard libraries, design patterns, architecture, each language's deep end. Ends with a key-value store. |
| 136-165 | Six five-day builds | A distributed cache, a job queue, a storage engine, a chat system, an observability toolkit, an interpreter. |
| 166-180 | Interview and capstone | Forty questions per language, then an eight-day order platform. |

The full plan is in [`docs/CURRICULUM_INDEX.md`](docs/CURRICULUM_INDEX.md).

---

## Writing a day

```
/day-langs 12
```

Every lesson follows the nine-section contract in
[`docs/00_HOW_A_DAY_WORKS.md`](docs/00_HOW_A_DAY_WORKS.md). The rules for the writing
partner are in [`CLAUDE.md`](CLAUDE.md).
