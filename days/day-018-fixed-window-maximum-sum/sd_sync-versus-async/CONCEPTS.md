---
day: 18
part: "2.1"
title: "Separate redirect success from analytics completion"
ids: [SD-18]
level: working
prerequisites: ["Day 5 latency budgets; Day 10 duplicate effects"]
failure: true
---

# Separate redirect success from analytics completion

Core reading: explanation, worked trace, and readiness. The production section offers optional
depth for another sitting; keep the existing track budget and record partial work honestly.

## One-line answer

Keep redirect decisions on the response path, defer derived analytics, and state exactly which events can be lost or duplicated.

## The story

A short link takes two seconds to open because its server waits for a dashboard counter
and location lookup. Moving both to a background task helps until a worker restart loses the task.

## The idea in plain language

Synchronous work must finish before the response; asynchronous work continues separately.
For a redirect, destination lookup and expiry checks determine the answer. Aggregation and
enrichment usually determine a later report. A queue moves work in time but does not decide
whether it is durably accepted, retried, duplicated, or allowed to fail.

Reuse [latency budgets](../../day-005-merge-sorted-arrays/sd_latency-budgets/CONCEPTS.md) and
[idempotency](../../day-010-pair-sum-indices/sd_idempotency-semantics/CONCEPTS.md). Define an
analytics event precisely: here it records a validated redirect attempt, not proof that a
browser loaded the destination. Assign one event ID per attempt and preserve it on delivery retries.

## Why Krama needs it

This develops SD-18 for the [Week 3 review](../../day-021-week-3-review/LESSON.md).
The tracks remain independent; use only this subject's prerequisites.

## The source behind it

[Asynchronous Request-Reply pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/asynchronous-request-reply)
distinguishes accepting work from completing it. This lesson applies that distinction to
internal analytics; the redirect itself still returns a redirect, not an analytics polling API. Checked 2026-09-22; details are in the [source ledger](../../../docs/SOURCES.md).
The trace and counterexample below are original teaching examples.

## The mechanism

### Worked trace

Trace these boundaries rather than writing only an async arrow:

| Stage | Before redirect response? | Failure meaning |
| --- | --- | --- |
| Resolve destination and check expiry | Yes | Cannot safely choose redirect |
| Attempt bounded event enqueue | Chosen policy | Timeout means event outcome may be unknown |
| Enrich, aggregate, update dashboard | No | Redirect can succeed while report lags |

If the producer returns before a durable handoff, a crash can lose its event. If it waits for
durable acknowledgement, queue delay enters the redirect budget. If an acknowledgement is
lost after storage accepted the event, a retry can duplicate delivery. A consumer that commits
the effect and crashes before acknowledging also causes redelivery. Make effect application
and the event-ID deduplication record atomic, then acknowledge; a naked increment is unsafe.

For arrival rate lambda and consumer rate mu, backlog grows at lambda-mu events/second while
lambda exceeds mu. A queue buffers overload; it cannot make sustained excess work disappear.
The reference chooses approximate analytics and a bounded enqueue attempt, explicitly accepting
loss when storage is unavailable. A stricter business requirement would need a different response
and durability policy.

## When it breaks

Run this separate teaching demonstration before implementing your own exercise.
For SD, it is a local model of a failure, not a running service or a production measurement.

```python
pending = ["event-1"]
redirect_sent = True
pending.clear()  # model process loss before a durable handoff
print("redirect sent:", redirect_sent, "recoverable in-memory events:", len(pending))
try:
    assert len(pending) == 1, "background memory did not preserve the event"
except AssertionError as error:
    print(f"AssertionError: {error}")
deliveries = ["event-1", "event-1"]
naive_count = len(deliveries)
deduplicated_count = len(set(deliveries))
print("delivery count:", naive_count, "distinct event count:", deduplicated_count)
assert deduplicated_count == 1
```

**Line by line:** Clearing pending models a lost in-memory task after the redirect. Duplicate strings
model delivery retries of one event. Set cardinality demonstrates the desired counting rule;
a real concurrent consumer needs transactional deduplication, not this in-memory substitute.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
redirect sent: True recoverable in-memory events: 0
AssertionError: background memory did not preserve the event
delivery count: 2 distinct event count: 1
```

**Line by line:** These are the actual printed observations, including the deliberately caught
assertion or exception. A caught failure documents the wrong assumption; later assertions check
the repair on the stated example, not on every possible input.

## In production

Choose queue bounds, delivery retention, deduplication retention, maximum event size, and
backpressure policy together. Report oldest pending-event age rather than queue length alone.
Measure enqueue failures, processing retries, dropped events, and dashboard freshness. Calling
an in-process function async does not establish durable acceptance or isolate CPU usage.
Do not claim exactly-once browser clicks from exactly-once application of an event ID.

## Check yourself

### Readiness before practice

1. Which actions are necessary to choose the redirect response?
2. Where can a producer crash lose work in the chosen policy?
3. Why can a durable queue deliver the same event twice?
4. What does lambda > mu predict about freshness?

Compare the [complete reference answer](REFERENCE_DESIGN.md) before guided practice or after your own attempt.

Use [README.md](README.md) for the assignment and evidence route. Reading does not complete study.
