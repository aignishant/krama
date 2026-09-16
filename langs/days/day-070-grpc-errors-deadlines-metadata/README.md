# Day 070 — gRPC IV: errors, deadlines, metadata

| Track | Today |
|---|---|
| **Python** | grpc.StatusCode, timeouts, and metadata in Python |
| **Go** | status.Error, codes, context deadlines, and metadata.MD |
| **C++** | grpc::Status, deadlines, and ClientContext metadata |

## What you can do by tonight

You can return a proper error with a code, propagate a deadline, and pass a request ID, in each language.

## The question today answers

*How do errors work in gRPC?*

## Read in this order

1. [01-python-grpc-statuscode-timeouts-and.md](01-python-grpc-statuscode-timeouts-and.md) — the Python lesson
2. [02-go-status-error-codes-context.md](02-go-status-error-codes-context.md) — the Go lesson
3. [03-cpp-grpc-status-deadlines-and.md](03-cpp-grpc-status-deadlines-and.md) — the C++ lesson
4. [04-practice.md](04-practice.md) — build it three times, then say it out loud

## Where this sits

- Phase: **Protocol Buffers and gRPC**

---

[← Day 069](../day-069-grpc-streaming/README.md) · [All days](../README.md) · [Day 071 →](../day-071-grpc-interceptors-auth-tls/README.md)
