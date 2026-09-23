---
day: 12
part: "1.1"
title: "Carry the remaining deadline through each dependency"
ids: [SD-12]
level: working
prerequisites: ["Latency budgets", "Connection pools"]
failure: true
---

# Carry the remaining deadline through each dependency

Core: one request lifetime, smaller nested budgets, and cooperative cancellation. Clock-domain
conversion and retry policy are optional depth. The timeline below is hypothetical, not a benchmark.

## One-line answer

Give each child call no more than the parent's remaining time, and propagate cancellation when its result is no longer useful.

## The story

A customer will wait only half a second for a shop's lookup. Three services each start a fresh
half-second timer. The innermost service keeps working after the customer has gone, occupying
the database connection needed by the next request.

## The idea in plain language

A timeout is a duration allowed for an operation. A deadline is the point after which its result
is no longer timely. [Latency budgets](../../day-005-merge-sorted-arrays/sd_latency-budgets/CONCEPTS.md)
allocate a request's lifetime; [pool waits](../../day-011-group-anagrams/sd_connection-budgets/CONCEPTS.md)
consume that lifetime before execution begins. Never reset the whole budget at each hop.

Cancellation is a signal that work is no longer wanted. It is cooperative: handlers and libraries
must notice it, stop useful work, and release resources. It does not undo a committed write.
Recognize this problem when nested calls, queueing, or retries continue after their caller gives up.

## Why Krama needs it

[Retry budgets](../../day-064-k-largest-stream-values/sd_retry-budgets/README.md) later limits
repeated attempts. Without a shared deadline, a retry policy can extend a request indefinitely.

## The source behind it

[Deadlines](https://grpc.io/docs/guides/deadlines/) (`spec:grpc-deadlines`) and
[Cancellation](https://grpc.io/docs/guides/cancellation/) (`spec:grpc-cancellation`), checked
2026-09-22, explain propagation and handler responsibility. Automatic propagation differs by
language/runtime; configure and test the actual stack rather than assuming generic HTTP does it.

## The mechanism

### Worked trace

Use a single conceptual timeline in milliseconds to make the arithmetic inspectable. Suppose the
client deadline is t=500. Gateway A starts a child call at t=40, reserves 40 ms for its own response,
and caps the child duration at 350 ms. Available duration is min(350, 500−40−40)=350, so that child
must finish by t=390. Service B reaches its child call at t=100, inherits t=390, reserves 30 ms,
and caps the next call at 220 ms: min(220, 390−100−30)=220, giving t=320.

```text
Client --overall deadline 500--> A
  A at t=40 --child deadline 390--> B
    B at t=100 --child deadline 320--> C
      C stops or cancels pending dependency work by its deadline
    B observes failure/cancellation, releases resources, returns
  A returns while client budget remains
```

At each boundary calculate `remaining = parent_deadline - now - response_reserve` and bound the
call by both remaining time and a local cap. If remaining is nonpositive, do not start the call.
Queueing, pool acquisition, connect time, execution, and response transfer all consume elapsed
time. The invariant is that no child is intentionally scheduled beyond its parent's useful lifetime.
Nested call durations overlap; adding all nested caps as sequential work double-counts them.

## When it breaks

```python
deadline, now, reserve, local_cap = 500, 380, 40, 350
wrong_finish = now + local_cap
allowed = max(0, min(local_cap, deadline - now - reserve))
print("fresh timeout finishes at:", wrong_finish)
print("remaining child budget:", allowed, "finish:", now + allowed)
try:
    assert wrong_finish <= deadline - reserve, "child outlives the response budget"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert allowed == 80
assert max(0, min(local_cap, deadline - 490 - reserve)) == 0
```

**Line by line:** all values are hypothetical milliseconds on one timeline. Resetting a 350 ms
timer at t=380 finishes at t=730. Subtracting elapsed time and reserve leaves only 80 ms. The
final assertion tests refusal to start when the response reserve already consumes the remainder.
This arithmetic does not test real cancellation delivery or scheduler precision.

Author verification on Python 3.12.10, 2026-09-22:

```text
fresh timeout finishes at: 730
remaining child budget: 80 finish: 460
AssertionError: child outlives the response budget
```

## In production

Use monotonic time for local elapsed durations. Monotonic timestamps are process/host-local;
do not send one host's raw value as another's deadline. Use the protocol's deadline/remaining-time
mechanism and account for elapsed time at every hop. Cancellation should reach queued tasks,
outbound calls, and DB work where supported; cleanup itself needs bounded resource ownership.

If C committed before cancellation, the effect persists even when the client sees a timeout.
Use [operation identity](../../day-010-pair-sum-indices/sd_idempotency-semantics/CONCEPTS.md) to
resolve retries safely. A reviewer should ask whether timeout means “stop waiting” or “work stopped,”
and request metrics for time spent queued, cancelled work still running, and deadline overruns.

## Check yourself

### Readiness before practice

1. Why must a pool wait consume the same overall budget?
2. At t=380, why is an otherwise valid 350 ms timeout too large?
3. What can cancellation do before a commit, and what can it not undo after it?
4. Why must raw monotonic timestamps not cross hosts?

Run the arithmetic and explain the nested deadlines aloud. Use [the reference](REFERENCE_DESIGN.md)
for a complete three-hop answer before guided practice or after writing [DESIGN.md](DESIGN.md).

[Navigation](README.md) · [Recall](../../../docs/SD_RECALL.md#day-012-timeout-propagation)
