---
day: 20
part: "2.1"
title: "Keep module ownership before splitting deployments"
ids: [SD-20]
level: working
prerequisites: ["Day 15 domain model; Day 18 analytics handoff"]
failure: true
---

# Keep module ownership before splitting deployments

Core reading: explanation, worked trace, and readiness. The production section offers optional
depth for another sitting; keep the existing track budget and record partial work honestly.

## One-line answer

Give links and analytics explicit internal interfaces and owned data, then extract a service only for a measured need.

## The story

An analytics report changes the links table directly because it is in the same database.
A later split becomes expensive: nobody knows which module owns link state or which callers
depend on private columns.

## The idea in plain language

A modular monolith is one deployable application organized into modules with explicit
responsibilities. Links owns link creation, resolution, and lifecycle; Analytics owns event
processing and aggregates. An internal call is still an interface, even without HTTP.
Shared deployment need not mean every module may write every table.

Build on [domain ownership](../../day-015-sorted-pair-existence/sd_domain-model/CONCEPTS.md)
and [asynchronous analytics](../../day-018-fixed-window-maximum-sum/sd_sync-versus-async/CONCEPTS.md).
Separating modules simplifies reasoning; separating services additionally introduces network
calls, independently failing processes, and release coordination. The second step needs evidence.

## Why Krama needs it

This develops SD-20 for the [Week 3 review](../../day-021-week-3-review/LESSON.md).
The tracks remain independent; use only this subject's prerequisites.

## The source behind it

[Microservices architecture style](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices)
describes independent scaling alongside distributed-system and operational complexity.
The monolith boundary and extraction threshold below are proposed design choices, not universal rules. Checked 2026-09-22; details are in the [source ledger](../../../docs/SOURCES.md).
The trace and counterexample below are original teaching examples.

## The mechanism

### Worked trace

Assign responsibilities before drawing hosts:

| Module | Public operation or event | Owned data | Forbidden shortcut |
| --- | --- | --- | --- |
| Links | create_link, resolve_link | links and create replay records | Analytics updating link expiry |
| Analytics | accept/process ClickObserved | events and aggregates | Joining private links columns everywhere |
| HTTP adapter | Translate HTTP into module calls | No domain authority | Duplicating expiry rules |

On redirect, the adapter invokes Links.resolve_link; Links checks lifecycle and returns the
destination. A small ClickObserved event carries the link ID and attempt identity across the
analytics boundary. Analytics processes it according to Day 18's declared loss policy. Modules
can share one database instance while using separate tables and repository interfaces.

An ownership invariant is reviewable even before services exist: every write to a domain
table must pass through its owning module. The local experiment below makes a forbidden
dependency fail explicitly. In real code, import boundaries, public APIs, and architecture
checks supplement code review; this small registry is only a teaching model.

One deployment is easier to change atomically but shares CPU, memory, failure, and release
boundaries. Independent analytics scaling is valuable only if measurements show a meaningful
need and a separate service's operational cost is justified. A slow SQL query or missing index
may be the actual problem; moving it behind HTTP would preserve that problem.

## When it breaks

Run this separate teaching demonstration before implementing your own exercise.
For SD, it is a local model of a failure, not a running service or a production measurement.

```python
owners = {"links": "Links", "click_events": "Analytics", "daily_counts": "Analytics"}
def authorize_write(module, table):
    if owners[table] != module:
        raise PermissionError(f"{module} cannot write {table}; owner is {owners[table]}")
    return "allowed"

try:
    authorize_write("Analytics", "links")
except PermissionError as error:
    print(f"PermissionError: {error}")
print("public owner path:", authorize_write("Links", "links"))
print("analytics-owned path:", authorize_write("Analytics", "daily_counts"))
assert authorize_write("Links", "links") == "allowed"
```

**Line by line:** owners records the proposed data boundary. The authorization function deliberately
rejects a cross-module write; the repaired paths use each owner. This model does not provide
database security, process isolation, or a complete implementation of module encapsulation.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
PermissionError: Analytics cannot write links; owner is Links
public owner path: allowed
analytics-owned path: allowed
```

**Line by line:** These are the actual printed observations, including the deliberately caught
assertion or exception. A caught failure documents the wrong assumption; later assertions check
the repair on the stated example, not on every possible input.

## In production

Track per-module resource use, deployment causes, and request traces before extraction.
Keep event schemas explicit and versioned so an eventual network boundary has a stable contract.
An asynchronous in-process worker can still exhaust the same memory or CPU as the request
handler. Extracting Analytics alone also does not isolate a shared database; allocate storage
capacity and ownership deliberately. Keep one team able to operate and roll back the result.

## Check yourself

### Readiness before practice

1. Which module owns the link expiry write, and why?
2. What failure isolation does an internal module boundary not provide?
3. What evidence would justify independently scaling Analytics?
4. What would still be coupled if two services kept unrestricted shared table access?

Compare the [complete reference answer](REFERENCE_DESIGN.md) before guided practice or after your own attempt.

Use [README.md](README.md) for the assignment and evidence route. Reading does not complete study.
