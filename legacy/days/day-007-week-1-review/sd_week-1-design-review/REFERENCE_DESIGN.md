# Reference design — Week 1 design review

**Open after your cold attempt.** This assistant-authored example revises one hypothetical
weak decision from Days 1–6, defends an alternative, and walks through a failure. It does not
identify your personal weakest decision or supply your assessment evidence. Use [DESIGN.md](DESIGN.md)
for your own revision. Comparison belongs in the existing 30-minute review budget.

## Selected weakness and original memo

Selected weakness: acknowledging a create before its mapping is committed. The illustrative
draft says, “Return a code immediately and write the mapping afterwards to keep creation fast.”
Its quality promise says an acknowledged code can be resolved after a service-process restart,
assuming the database and disk remain healthy. Those two statements conflict.

The weakness is the acknowledgment boundary, not a need for more services. I revise that
boundary and keep the [Day 6 baseline](../../day-006-best-single-trade/sd_single-node-baseline/REFERENCE_DESIGN.md).
This is an invented draft for teaching, not a claim about anything in your earlier memos.

## Assumptions and requirement

Assume one service process and a relational mapping database on one host. The database is the
source of truth; `code` is unique and destinations are immutable. Creation succeeds only when
the code can subsequently be looked up after a service-process restart. Host or disk destruction
is a separate recovery requirement that this design does not claim to satisfy without backups.

Use the Day 6 hypothetical workload of 100 redirects/s and 2 creates/s. Retain its proposed
service-boundary p95 ≤ 200 ms target, measured separately per operation with errors/timeouts
tracked too. It is a target, not a result. Each request performs one modeled database operation;
at an assumed 4 ms serialized operation cost, demand is 102 operations/s versus an ideal
250 operations/s ceiling. Actual commit latency and contention remain to be measured.

## Revised artifact

```text
Draft:   request -> choose code -> acknowledge -> insert -> commit
                                      ^ crash here can lose an acknowledged mapping

Revised: request -> validate -> insert unique code -> durable commit -> acknowledge
                                                   ^ truth boundary
```

| State | Database fact | What the browser may know | Allowed response |
| --- | --- | --- | --- |
| Before commit | No durable new mapping established | Waiting | No success acknowledgment |
| After commit, response lost | Mapping exists | Outcome unknown | Retry may duplicate creation |
| After response delivered | Mapping exists | Creation succeeded | Code can be used |

The service returns the created code only after the database confirms its configured durable
commit. Database failure before confirmed commit produces a temporary failure or an uncertain
outcome if confirmation is lost; it must not fabricate success. A redirect reads the same
authoritative table. A miss and an unavailable database remain separate outcomes.

The revised invariant is: every success acknowledgment follows a committed mapping. It does
not establish that every committed mapping was acknowledged, because responses can be lost.
That asymmetry is the core of the revision.

## Decision and alternative

Choose synchronous commit before a success acknowledgment because it directly supports the
restart requirement. Its cost is that creation latency includes database commit and any queue
wait. Measure this path and reduce avoidable work before weakening the user promise.

An alternative is an explicit asynchronous creation operation: durably record accepted work,
return an operation identifier, and let the client check until the code is ready. That requires
a pending state, a status endpoint, and recovery of unfinished work. It does not allow returning
a supposedly usable code before it exists. This alternative fits only if the product accepts
eventual readiness and measured commit/processing latency makes synchronous completion unsuitable.
It is more machinery than the current small workload has justified.

## Failure walkthrough and proposed validation

For the original draft, inject a process crash after success is emitted but before insertion.
After restart, the user follows the acknowledged code and receives not found. The promised
restart behavior is violated. This is a hypothetical walkthrough, not an executed crash test.

For the revision, a crash before commit yields no success response. After commit but before
the response, the mapping survives a service-process crash under the stated database assumption,
but the browser has an unknown outcome. Retrying creation can yield another code, which is
allowed here. Exactly one effect would require a durable idempotency design beyond this revision.

The concrete validation plan is to record every acknowledged code, interrupt the service at
each boundary, restart it, and verify each acknowledged code's destination against the database.
Also check the lost-response case without pretending the browser can distinguish it from an
uncommitted request. Run mixed traffic while recording commit time and end-to-end latency.
Do not count a mere process restart test as a disk-loss recovery test.

## Self-review and reference rubric

| Criterion | Reference assessment |
| --- | --- |
| Requirements | 2/2: usable acknowledged code and process-restart boundary are explicit |
| Data/API | 2/2: authoritative mapping, unique code, and acknowledgment states are explicit |
| Scale | 1/2: rate arithmetic is present, but operation costs are assumed and unmeasured |
| Failure tradeoffs | 2/2: precommit and lost-response failures plus the async alternative are explained |

This illustrative 7/8 scores the written reference against the review rubric; it is neither
your score nor evidence of production readiness. Remaining uncertainty includes database
durability settings, actual commit latency, and whether duplicate creation is acceptable.
The next step is the proposed boundary-injection test and requirements confirmation. Your
review passes only through your own revised artifact, defense, and failure explanation.

[Concepts for repair](CONCEPTS.md) · [Assignment](README.md#assignment) · [Your practice](DESIGN.md)
